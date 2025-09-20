#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "chonkie[semantic]",
#     "sentence-transformers",
#     "httpx",
#     "pydantic",
#     "pydantic-settings",
#     "python-dotenv"
# ]
# ///

"""
Test Chonkie's SemanticChunker with actual Roam data.
This will help us understand how it chunks hierarchical content.
"""

import json
from typing import Dict, List, Tuple
from chonkie import SemanticChunker

def linearize_page_simple(page_data: Dict) -> Tuple[str, List[Dict]]:
    """
    Simple linearization: just concatenate all text with newlines.
    Returns (text, metadata) where metadata tracks UIDs.
    """
    text_parts = []
    metadata = []

    def process_block(block: Dict, level: int = 0):
        """Recursively process a block and its children"""
        # Get block text (either title for pages or string for blocks)
        text = block.get(':block/string', '') or block.get(':node/title', '')
        uid = block.get(':block/uid', '')

        if text:
            # Add indentation to show hierarchy
            indent = "  " * level
            text_parts.append(f"{indent}{text}")
            metadata.append({
                'uid': uid,
                'text': text,
                'level': level,
                'start_pos': sum(len(t) + 1 for t in text_parts[:-1])  # +1 for newlines
            })

        # Process children
        children = block.get(':block/children', [])
        if children:
            # Sort by order if available
            sorted_children = sorted(children, key=lambda x: x.get(':block/order', 0))
            for child in sorted_children:
                process_block(child, level + 1)

    process_block(page_data)

    full_text = "\n".join(text_parts)
    return full_text, metadata

def test_basic_chunking():
    """Test basic semantic chunking on a Roam page"""
    print("="*60)
    print("TEST 1: Basic Semantic Chunking")
    print("="*60)

    # Load a sample page
    with open('page_response_sample.json', 'r') as f:
        page_data = json.load(f)

    # Linearize the page
    text, metadata = linearize_page_simple(page_data)

    print(f"\nLinearized text ({len(text)} chars):")
    print("-" * 40)
    print(text[:500] + "..." if len(text) > 500 else text)
    print("-" * 40)

    # Test with different thresholds
    thresholds = [0.5, 0.7, 0.9]

    for threshold in thresholds:
        print(f"\n### Threshold: {threshold}")

        chunker = SemanticChunker(
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            threshold=threshold,
            chunk_size=512,
            similarity_window=3
        )

        chunks = chunker.chunk(text)

        print(f"Number of chunks: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            print(f"\nChunk {i+1} ({chunk.token_count} tokens):")
            print(f"  Text: {chunk.text[:100]}...")
            print(f"  Start: {chunk.start_index}, End: {chunk.end_index}")

            # Find which UIDs are in this chunk
            chunk_uids = []
            for meta in metadata:
                if meta['start_pos'] >= chunk.start_index and meta['start_pos'] < chunk.end_index:
                    chunk_uids.append(meta['uid'])
            print(f"  UIDs: {chunk_uids}")

def test_skip_window():
    """Test skip-window merging for interleaved topics"""
    print("\n" + "="*60)
    print("TEST 2: Skip-Window Merging")
    print("="*60)

    # Create synthetic interleaved content similar to daily notes
    interleaved_text = """
Meeting notes about Project Alpha
We discussed the new API design
Need to implement authentication

Personal reminder: Buy groceries
Don't forget milk and bread

Back to Project Alpha details
The authentication should use OAuth2
We'll need rate limiting too

Another personal note
Call dentist tomorrow

More about Project Alpha
Database schema needs updating
Consider using PostgreSQL
"""

    skip_windows = [0, 1, 2]

    for skip in skip_windows:
        print(f"\n### Skip-window: {skip}")

        chunker = SemanticChunker(
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            threshold=0.7,
            chunk_size=512,
            skip_window=skip
        )

        chunks = chunker.chunk(interleaved_text)

        print(f"Number of chunks: {len(chunks)}")
        for i, chunk in enumerate(chunks):
            print(f"\nChunk {i+1}:")
            # Show first line to identify topic
            first_line = chunk.text.split('\n')[0]
            print(f"  Starts with: {first_line}")
            print(f"  Total lines: {len(chunk.text.split(chr(10)))}")

def test_daily_note_structure():
    """Test with actual daily note structure from our samples"""
    print("\n" + "="*60)
    print("TEST 3: Daily Note Structure")
    print("="*60)

    # Load the January 27th sample (it has interleaved topics)
    try:
        with open('../docs/roam_samples/January 27th, 2025.json', 'r') as f:
            daily_note = json.load(f)
    except FileNotFoundError:
        print("Could not find daily note sample file")
        return

    # Extract just the first page's content
    if isinstance(daily_note, list) and daily_note:
        page_data = daily_note[0]
    else:
        print("Unexpected daily note format")
        return

    # Linearize
    text, metadata = linearize_page_simple(page_data)

    print(f"\nDaily note has {len(metadata)} blocks")
    print(f"Total text length: {len(text)} chars")

    # Test with skip-window to handle interleaved topics
    chunker = SemanticChunker(
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        threshold=0.7,
        chunk_size=2048,  # Larger chunks for daily notes
        skip_window=2  # Enable merging of related but non-consecutive content
    )

    chunks = chunker.chunk(text)

    print(f"\nCreated {len(chunks)} chunks from daily note")

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} ({chunk.token_count} tokens):")

        # Show topic indicators
        lines = chunk.text.split('\n')
        topics = []
        for line in lines[:5]:  # Check first 5 lines
            if "Project" in line or "SFG" in line:
                topics.append("Project")
            if "TODO" in line or "DONE" in line:
                topics.append("Task")
            if "[[" in line and "]]" in line:
                # Extract page references
                import re
                refs = re.findall(r'\[\[([^\]]+)\]\]', line)
                topics.extend(refs[:2])  # Just first 2 refs

        print(f"  Topics detected: {list(set(topics))[:3]}")
        print(f"  Preview: {chunk.text[:150]}...")

def main():
    """Run all tests"""
    test_basic_chunking()
    test_skip_window()
    test_daily_note_structure()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
Key findings:
1. How does threshold affect chunk boundaries?
2. Does skip-window help with interleaved topics?
3. What's the best way to track UIDs through chunks?
""")

if __name__ == "__main__":
    main()