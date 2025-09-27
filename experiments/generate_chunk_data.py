"""
Generate chunk boundary data for visualization

Pulls pages from Roam and applies different chunking configurations,
then exports as JSON for the Svelte visualizer.
"""
import json
import asyncio
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add backend to path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))

from linearize import linearize_page_markdown_style
from chonkie import SemanticChunker
from dotenv import load_dotenv
import httpx

load_dotenv()

# Chunker configurations to test
CHUNKER_CONFIGS = {
    "default": {
        "embedding_model": "ibm-granite/granite-embedding-small-english-r2",
        "threshold": 0.6,
        "skip_window": 1,
        "min_chunk_size": 50
    },
    "roam_optimized": {
        "embedding_model": "ibm-granite/granite-embedding-small-english-r2",
        "threshold": 0.6,             # Much lower - fewer boundaries
        "chunk_size": 800,            # Moderate size for search
        "skip_window": 2,             # Small window
        "min_chunk_size": 50,        # Higher minimum (characters!)
        # "similarity_window": 7,       # Wider window for boundary detection
        # "min_sentences_per_chunk": 2, # Force meaningful chunks
    }
    # "tight": {
    #     # "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    #     "embedding_model": "ibm-granite/granite-embedding-small-english-r2",
    #     "threshold": 0.8,  # Higher = more splits
    #     "skip_window": 1,
    #     "min_chunk_size": 30
    # },
    # "loose": {
    #     # "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    #     "embedding_model": "ibm-granite/granite-embedding-small-english-r2",
    #     "threshold": 0.4,  # Lower = fewer splits
    #     "skip_window": 1,
    #     "min_chunk_size": 100
    # },
    # "no_skip": {
    #     # "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    #     "embedding_model": "ibm-granite/granite-embedding-small-english-r2",
    #     "threshold": 0.6,
    #     "skip_window": 0,  # No merging of non-consecutive
    #     "min_chunk_size": 50
    # },
    # "large_skip": {
    #     # "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    #     "embedding_model": "ibm-granite/granite-embedding-small-english-r2",
    #     "threshold": 0.6,
    #     "skip_window": 3,  # Look further for similar content
    #     "min_chunk_size": 50
    # }
}

async def pull_page(page_uid: str) -> Optional[Dict]:
    """Pull a single page from Roam by UID."""
    token = os.getenv('ROAM_API_TOKEN')
    graph = os.getenv('ROAM_GRAPH_NAME')

    if not token or not graph:
        raise ValueError("ROAM_API_TOKEN and ROAM_GRAPH_NAME must be set in .env")

    url = f"https://api.roamresearch.com/api/graph/{graph}/pull-many"
    headers = {
        "X-Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Recursive selector to get all children
    selector_str = "[:block/uid :block/string :node/title :block/order {:block/children ...}]"

    pull_data = {
        "eids": f'[[:block/uid "{page_uid}"]]',
        "selector": selector_str
    }

    import httpx
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        response = await client.post(url, headers=headers, json=pull_data)
        if response.status_code == 200:
            # pull-many returns a list directly
            result = response.json()
            print(f"    Debug: pull-many response type: {type(result)}, length: {len(result) if isinstance(result, (list, dict)) else 'N/A'}")
            if isinstance(result, list):
                return result[0] if len(result) > 0 else None
            elif isinstance(result, dict) and 'result' in result:
                # Sometimes wrapped in {result: [...]}
                actual_result = result['result']
                return actual_result[0] if actual_result and len(actual_result) > 0 else None
            else:
                print(f"    Unexpected response structure: {result}")
                return None
        else:
            print(f"Error pulling page: {response.status_code}")
            if response.status_code == 308:
                print(f"  Redirect location: {response.headers.get('location')}")
            return None

async def get_sample_page_uids(limit: int = 5) -> List[str]:
    """Get some sample page UIDs from the graph."""
    token = os.getenv('ROAM_API_TOKEN')
    graph = os.getenv('ROAM_GRAPH_NAME')

    print(f"    Querying graph for pages...")

    # Query for pages with content (children)
    query = """[:find ?uid ?title
               :where [?e :node/title ?title]
                      [?e :block/uid ?uid]
                      [?e :block/children]]"""

    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
        response = await client.post(
            f"https://api.roamresearch.com/api/graph/{graph}/q",
            headers={'X-Authorization': f'Bearer {token}'},
            json={"query": query}
        )

        if response.status_code != 200:
            print(f"    Error querying: {response.status_code}")
            return []

        result = response.json()

        if result and result.get('result'):
            # Don't filter out daily notes - include all pages
            pages = []
            import re
            total_results = len(result['result'])
            print(f"    Query returned {total_results} total pages")

            for item in result['result'][:limit]:  # Take first 'limit' pages
                uid, title = item
                pages.append({'uid': uid, 'title': title})
                # Note if it's a daily note
                if re.match(r'^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(st|nd|rd|th)?,\s+\d{4}$', title) or re.match(r'^\d{2}-\d{2}-\d{4}$', uid):
                    print(f"      Including daily note: {title}")

            print(f"    Selected {len(pages)} pages to process")
            return pages
    return []

def detect_gaps(chunks: List) -> List[Dict]:
    """Detect gaps between chunks (from skip_window behavior)."""
    gaps = []
    for i in range(len(chunks) - 1):
        if chunks[i].end_index < chunks[i + 1].start_index:
            gaps.append({
                'after_chunk': i,
                'gap_start': chunks[i].end_index,
                'gap_end': chunks[i + 1].start_index,
                'gap_size': chunks[i + 1].start_index - chunks[i].end_index
            })
    return gaps

def process_page(page_data: Dict, chunkers: Dict) -> Dict:
    """Process a single page with multiple pre-created chunkers."""

    # Linearize the page
    print(f"    [DEBUG] Starting linearization...")
    linearized_text, uid_map, _page_meta = linearize_page_markdown_style(page_data)
    print(f"    [DEBUG] Linearized to {len(linearized_text)} chars")

    result = {
        'uid': page_data.get(':block/uid'),
        'title': page_data.get(':node/title', 'Untitled'),
        'linearized_text': linearized_text,
        'text_length': len(linearized_text),
        'uid_map': uid_map,
        'configs': {}
    }

    # Apply each config
    for config_name, chunker_info in chunkers.items():
        print(f"    Applying config: {config_name}")

        try:
            import time
            chunk_start = time.time()
            chunks = chunker_info['chunker'].chunk(linearized_text)
            print(f"      [DEBUG] Chunking completed in {time.time() - chunk_start:.2f}s")

            # Process chunks and detect gaps
            chunk_data = []
            for i, chunk in enumerate(chunks):
                chunk_data.append({
                    'id': i + 1,
                    'text': chunk.text,
                    'start_index': chunk.start_index,
                    'end_index': chunk.end_index,
                    'token_count': chunk.token_count,
                    'length': chunk.end_index - chunk.start_index
                })

            # Detect gaps (non-contiguous chunks from skip_window)
            gaps = detect_gaps(chunks)

            result['configs'][config_name] = {
                'params': chunker_info['params'],
                'chunks': chunk_data,
                'gaps': gaps,
                'total_chunks': len(chunks),
                'has_gaps': len(gaps) > 0
            }

            print(f"      Created {len(chunks)} chunks, {len(gaps)} gaps")

        except Exception as e:
            print(f"      Error: {e}")
            result['configs'][config_name] = {'error': str(e)}

    return result

async def main():
    parser = argparse.ArgumentParser(description='Generate chunk visualization data from Roam')
    parser.add_argument(
        '--pages',
        type=int,
        default=3,
        help='Number of pages to process'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='experiments/chunk_data.json',
        help='Output JSON file'
    )
    parser.add_argument(
        '--page-uids',
        nargs='+',
        help='Specific page UIDs to process (overrides --pages)'
    )
    parser.add_argument(
        '--use-sample',
        action='store_true',
        help='Use the real_page_sample.json file for testing'
    )

    args = parser.parse_args()

    print("🚀 Starting chunk data generation...")
    print(f"Configurations to test: {list(CHUNKER_CONFIGS.keys())}")

    # Get pages to process
    pages_to_process = []

    if args.use_sample:
        # Load the sample file
        print("  Using real_page_sample.json")
        sample_path = Path('experiments/real_page_sample.json')
        if not sample_path.exists():
            sample_path = Path('real_page_sample.json')

        print(f"  [DEBUG] Loading from {sample_path}")
        with open(sample_path, 'r', encoding='utf-8') as f:
            page_data = json.load(f)
            print(f"  [DEBUG] Loaded page data: {page_data.get(':node/title', 'Unknown')}")
            pages_to_process.append(page_data)
    elif args.page_uids:
        # Use specified UIDs
        for uid in args.page_uids:
            print(f"  Pulling page: {uid}")
            page_data = await pull_page(uid)
            if page_data:
                pages_to_process.append(page_data)
    else:
        # Get sample pages
        print(f"  Finding {args.pages} sample pages...")
        sample_pages = await get_sample_page_uids(args.pages)

        for page_info in sample_pages:
            print(f"  Pulling page: {page_info['title']}")
            page_data = await pull_page(page_info['uid'])
            if page_data:
                pages_to_process.append(page_data)

    if not pages_to_process:
        print("❌ No pages found to process")
        return

    print(f"\n📄 Processing {len(pages_to_process)} pages...")

    # Create chunkers once for all pages
    print("\n🔧 Initializing chunkers...")
    chunkers = {}
    import time
    for config_name, config_params in CHUNKER_CONFIGS.items():
        print(f"  Creating chunker: {config_name}")
        print(f"    Model: {config_params.get('embedding_model')}")
        chunker_start = time.time()
        chunkers[config_name] = {
            'chunker': SemanticChunker(**config_params),
            'params': config_params
        }
        print(f"    Created in {time.time() - chunker_start:.2f}s")
    print(f"  Total chunkers initialized: {len(chunkers)}")

    # Process each page
    results = {
        'generated_at': datetime.now().isoformat(),
        'configs': CHUNKER_CONFIGS,
        'pages': []
    }

    for idx, page_data in enumerate(pages_to_process, 1):
        title = page_data.get(':node/title', 'Untitled')
        print(f"\n  Processing page {idx}/{len(pages_to_process)}: {title}")

        page_start = time.time()
        page_result = process_page(page_data, chunkers)
        results['pages'].append(page_result)
        print(f"  [DEBUG] Page processed in {time.time() - page_start:.2f}s")

    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Saved chunk data to: {output_path}")
    print(f"   Total pages: {len(results['pages'])}")
    print(f"   Total configs: {len(CHUNKER_CONFIGS)}")

    # Show summary
    for page in results['pages']:
        print(f"\n   {page['title']}:")
        for config_name, config_data in page['configs'].items():
            if 'error' not in config_data:
                chunks = config_data['total_chunks']
                gaps = len(config_data['gaps'])
                print(f"     {config_name}: {chunks} chunks, {gaps} gaps")

if __name__ == "__main__":
    asyncio.run(main())
