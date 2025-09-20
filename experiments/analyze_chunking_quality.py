# /// script
# dependencies = ["matplotlib", "seaborn", "pandas", "numpy"]
# ///

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import re
from typing import Dict, List, Tuple, Set

def load_data():
    """Load all the chunk files and original data"""
    with open('/Users/sheikmeeran/roam-test/experiments/real_page_sample.json', 'r') as f:
        original_data = json.load(f)

    with open('/Users/sheikmeeran/roam-test/experiments/chunks_standard.json', 'r') as f:
        chunks_standard = json.load(f)

    with open('/Users/sheikmeeran/roam-test/experiments/chunks_with_skip-window.json', 'r') as f:
        chunks_skip_window = json.load(f)

    with open('/Users/sheikmeeran/roam-test/experiments/chunks_lower_threshold.json', 'r') as f:
        chunks_lower_threshold = json.load(f)

    return original_data, {
        'standard': chunks_standard,
        'skip-window': chunks_skip_window,
        'lower-threshold': chunks_lower_threshold
    }

def extract_all_uids_from_original(data) -> Dict[str, Dict]:
    """Extract all UIDs and their data from original hierarchical structure"""
    uid_map = {}

    def traverse(node, parent_uid=None, level=0):
        if isinstance(node, dict):
            # Handle page-level node
            if ':node/title' in node:
                page_uid = node.get(':block/uid', 'ROOT')
                uid_map[page_uid] = {
                    'type': 'page',
                    'title': node[':node/title'],
                    'level': level,
                    'parent': parent_uid,
                    'children': []
                }

                # Process children
                if ':block/children' in node:
                    for child in node[':block/children']:
                        traverse(child, page_uid, level + 1)

            # Handle block-level node
            elif ':block/uid' in node:
                block_uid = node[':block/uid']
                uid_map[block_uid] = {
                    'type': 'block',
                    'string': node.get(':block/string', ''),
                    'level': level,
                    'parent': parent_uid,
                    'children': []
                }

                # Add to parent's children list
                if parent_uid and parent_uid in uid_map:
                    uid_map[parent_uid]['children'].append(block_uid)

                # Process children
                if ':block/children' in node:
                    for child in node[':block/children']:
                        traverse(child, block_uid, level + 1)

    traverse(data)
    return uid_map

def verify_uid_accuracy(chunks: List[Dict], uid_map: Dict[str, Dict]) -> Dict:
    """Verify UID tracking accuracy"""
    results = {
        'missing_uids': [],
        'invalid_uids': [],
        'incorrect_primary_uids': [],
        'position_mismatches': [],
        'total_chunks': len(chunks),
        'total_source_uids': 0
    }

    for i, chunk in enumerate(chunks):
        source_uids = chunk.get('source_uids', [])
        primary_uid = chunk.get('primary_uid')
        chunk_text = chunk.get('text', '')
        start_pos = chunk.get('start', 0)
        end_pos = chunk.get('end', 0)

        results['total_source_uids'] += len(source_uids)

        # Check if all source UIDs exist in original data
        for uid in source_uids:
            if uid not in uid_map:
                results['missing_uids'].append({'chunk': i, 'uid': uid})

        # Check if primary UID is in source UIDs
        if primary_uid not in source_uids:
            results['incorrect_primary_uids'].append({
                'chunk': i,
                'primary_uid': primary_uid,
                'source_uids': source_uids
            })

        # Verify character positions align with actual text length
        actual_length = len(chunk_text)
        expected_length = end_pos - start_pos
        if abs(actual_length - expected_length) > 5:  # Allow small tolerance
            results['position_mismatches'].append({
                'chunk': i,
                'actual_length': actual_length,
                'expected_length': expected_length,
                'start': start_pos,
                'end': end_pos
            })

    return results

def analyze_semantic_coherence(chunks: List[Dict], uid_map: Dict[str, Dict]) -> Dict:
    """Analyze semantic coherence of chunks"""
    results = {
        'hierarchy_violations': [],
        'topic_splits': [],
        'sentence_breaks': [],
        'context_preservation': [],
        'total_chunks': len(chunks)
    }

    for i, chunk in enumerate(chunks):
        source_uids = chunk.get('source_uids', [])
        chunk_text = chunk.get('text', '')

        # Check for hierarchy violations (child without parent)
        uid_levels = []
        for uid in source_uids:
            if uid in uid_map:
                uid_levels.append(uid_map[uid]['level'])

        if uid_levels:
            level_range = max(uid_levels) - min(uid_levels)
            if level_range > 2:  # Flag if spanning more than 2 hierarchy levels
                results['hierarchy_violations'].append({
                    'chunk': i,
                    'level_range': level_range,
                    'min_level': min(uid_levels),
                    'max_level': max(uid_levels),
                    'uids': source_uids
                })

        # Check for mid-sentence splits
        if chunk_text.strip() and not chunk_text.strip()[-1] in '.!?':
            # Check if chunk ends abruptly (not at sentence boundary)
            if not chunk_text.strip().endswith((':', '...', '--')):
                results['sentence_breaks'].append({
                    'chunk': i,
                    'ending': chunk_text[-50:] if len(chunk_text) > 50 else chunk_text
                })

        # Analyze context preservation - blocks with very few tokens might lack context
        token_count = chunk.get('token_count', 0)
        if token_count < 20 and len(source_uids) == 1:
            results['context_preservation'].append({
                'chunk': i,
                'token_count': token_count,
                'single_uid': source_uids[0] if source_uids else None
            })

    return results

def analyze_chunking_boundaries(chunks: List[Dict], uid_map: Dict[str, Dict]) -> Dict:
    """Analyze where chunks split and boundary quality"""
    results = {
        'natural_boundaries': 0,
        'mid_thought_splits': 0,
        'orphaned_chunks': [],
        'reference_splits': [],
        'boundary_analysis': []
    }

    for i, chunk in enumerate(chunks):
        chunk_text = chunk.get('text', '').strip()
        token_count = chunk.get('token_count', 0)
        source_uids = chunk.get('source_uids', [])

        # Check for orphaned single-line chunks
        if token_count < 15 and len(source_uids) == 1:
            results['orphaned_chunks'].append({
                'chunk': i,
                'token_count': token_count,
                'text_preview': chunk_text[:100]
            })

        # Check for block reference splits
        block_ref_pattern = r'\(\([^)]+\)\)'
        page_ref_pattern = r'\[\[[^\]]+\]\]'

        if re.search(block_ref_pattern, chunk_text) or re.search(page_ref_pattern, chunk_text):
            # Check if references are split across chunks
            if chunk_text.count('((') != chunk_text.count('))'):
                results['reference_splits'].append({
                    'chunk': i,
                    'type': 'block_reference',
                    'text_preview': chunk_text[:200]
                })
            if chunk_text.count('[[') != chunk_text.count(']]'):
                results['reference_splits'].append({
                    'chunk': i,
                    'type': 'page_reference',
                    'text_preview': chunk_text[:200]
                })

        # Analyze boundary quality
        ends_naturally = chunk_text.endswith(('.', '!', '?', ':', '\n'))
        starts_naturally = chunk_text[0].isupper() if chunk_text else False

        results['boundary_analysis'].append({
            'chunk': i,
            'ends_naturally': ends_naturally,
            'starts_naturally': starts_naturally,
            'token_count': token_count
        })

        if ends_naturally:
            results['natural_boundaries'] += 1
        else:
            results['mid_thought_splits'] += 1

    return results

def analyze_statistical_distribution(chunks_dict: Dict[str, List[Dict]]) -> Dict:
    """Analyze statistical distribution of chunks across strategies"""
    results = {}

    for strategy, chunks in chunks_dict.items():
        token_counts = [chunk.get('token_count', 0) for chunk in chunks]
        source_uid_counts = [len(chunk.get('source_uids', [])) for chunk in chunks]
        chunk_lengths = [len(chunk.get('text', '')) for chunk in chunks]

        results[strategy] = {
            'total_chunks': len(chunks),
            'token_stats': {
                'mean': np.mean(token_counts),
                'median': np.median(token_counts),
                'std': np.std(token_counts),
                'min': np.min(token_counts),
                'max': np.max(token_counts),
                'percentiles': {
                    '25': np.percentile(token_counts, 25),
                    '75': np.percentile(token_counts, 75),
                    '95': np.percentile(token_counts, 95)
                }
            },
            'source_uid_stats': {
                'mean': np.mean(source_uid_counts),
                'median': np.median(source_uid_counts),
                'max': np.max(source_uid_counts),
                'distribution': dict(Counter(source_uid_counts))
            },
            'chunk_length_stats': {
                'mean': np.mean(chunk_lengths),
                'median': np.median(chunk_lengths),
                'std': np.std(chunk_lengths)
            }
        }

    return results

def find_overlapping_chunks(chunks_dict: Dict[str, List[Dict]]) -> Dict:
    """Find overlapping chunks between strategies"""
    results = {}

    for strategy, chunks in chunks_dict.items():
        uid_appearances = defaultdict(list)

        for i, chunk in enumerate(chunks):
            for uid in chunk.get('source_uids', []):
                uid_appearances[uid].append(i)

        overlapping_uids = {uid: chunk_indices for uid, chunk_indices in uid_appearances.items()
                          if len(chunk_indices) > 1}

        results[strategy] = {
            'total_overlapping_uids': len(overlapping_uids),
            'overlapping_details': overlapping_uids
        }

    return results

def generate_examples(chunks_dict: Dict[str, List[Dict]], uid_map: Dict[str, Dict]) -> Dict:
    """Generate specific examples of good and poor chunking decisions"""
    examples = {}

    for strategy, chunks in chunks_dict.items():
        good_examples = []
        poor_examples = []

        for i, chunk in enumerate(chunks):
            token_count = chunk.get('token_count', 0)
            source_uids = chunk.get('source_uids', [])
            text = chunk.get('text', '')[:300] + '...' if len(chunk.get('text', '')) > 300 else chunk.get('text', '')

            # Good example criteria: reasonable token count, natural boundaries, coherent content
            if (50 <= token_count <= 200 and
                len(source_uids) <= 5 and
                text.strip().endswith(('.', '!', '?', ':')) and
                len(good_examples) < 3):

                good_examples.append({
                    'chunk_index': i,
                    'token_count': token_count,
                    'source_uid_count': len(source_uids),
                    'text_preview': text,
                    'reason': 'Good token count, natural boundary, coherent content'
                })

            # Poor example criteria: very small/large chunks, bad boundaries, isolated content
            elif ((token_count < 20 or token_count > 500) or
                  (len(source_uids) == 1 and token_count < 30) or
                  (not text.strip() or len(text.strip()) < 10)) and len(poor_examples) < 3:

                reason = []
                if token_count < 20:
                    reason.append("too few tokens")
                if token_count > 500:
                    reason.append("too many tokens")
                if len(source_uids) == 1 and token_count < 30:
                    reason.append("isolated single block")
                if not text.strip() or len(text.strip()) < 10:
                    reason.append("empty or minimal content")

                poor_examples.append({
                    'chunk_index': i,
                    'token_count': token_count,
                    'source_uid_count': len(source_uids),
                    'text_preview': text,
                    'reason': ', '.join(reason)
                })

        examples[strategy] = {
            'good_examples': good_examples,
            'poor_examples': poor_examples
        }

    return examples

def create_visualizations(stats: Dict, output_dir: str):
    """Create visualizations for chunk analysis"""
    plt.style.use('seaborn-v0_8')

    # Token count distribution comparison
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Chunking Strategy Analysis', fontsize=16)

    # Token count distributions
    strategies = list(stats.keys())
    token_data = []
    for strategy in strategies:
        tokens = [stats[strategy]['token_stats']['mean']] * stats[strategy]['total_chunks']
        token_data.extend([(strategy, stats[strategy]['token_stats']['mean'])])

    ax1 = axes[0, 0]
    means = [stats[s]['token_stats']['mean'] for s in strategies]
    stds = [stats[s]['token_stats']['std'] for s in strategies]
    ax1.bar(strategies, means, yerr=stds, capsize=5)
    ax1.set_title('Average Token Count by Strategy')
    ax1.set_ylabel('Token Count')

    # Chunk count comparison
    ax2 = axes[0, 1]
    chunk_counts = [stats[s]['total_chunks'] for s in strategies]
    ax2.bar(strategies, chunk_counts)
    ax2.set_title('Total Chunks by Strategy')
    ax2.set_ylabel('Number of Chunks')

    # Source UID distribution
    ax3 = axes[1, 0]
    uid_means = [stats[s]['source_uid_stats']['mean'] for s in strategies]
    ax3.bar(strategies, uid_means)
    ax3.set_title('Average Source UIDs per Chunk')
    ax3.set_ylabel('Source UIDs')

    # Token count percentiles
    ax4 = axes[1, 1]
    percentiles_25 = [stats[s]['token_stats']['percentiles']['25'] for s in strategies]
    percentiles_75 = [stats[s]['token_stats']['percentiles']['75'] for s in strategies]
    percentiles_95 = [stats[s]['token_stats']['percentiles']['95'] for s in strategies]

    x = np.arange(len(strategies))
    width = 0.25
    ax4.bar(x - width, percentiles_25, width, label='25th percentile')
    ax4.bar(x, percentiles_75, width, label='75th percentile')
    ax4.bar(x + width, percentiles_95, width, label='95th percentile')
    ax4.set_xlabel('Strategy')
    ax4.set_ylabel('Token Count')
    ax4.set_title('Token Count Percentiles')
    ax4.set_xticks(x)
    ax4.set_xticklabels(strategies)
    ax4.legend()

    plt.tight_layout()
    plt.savefig(f'{output_dir}/chunking_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("Starting comprehensive chunking quality analysis...")

    # Load data
    original_data, chunks_dict = load_data()
    uid_map = extract_all_uids_from_original(original_data)

    print(f"Loaded original data with {len(uid_map)} unique UIDs")
    for strategy, chunks in chunks_dict.items():
        print(f"  {strategy}: {len(chunks)} chunks")

    # Analysis results
    analysis_results = {}

    for strategy, chunks in chunks_dict.items():
        print(f"\n=== Analyzing {strategy} strategy ===")

        # 1. UID Tracking Accuracy
        uid_accuracy = verify_uid_accuracy(chunks, uid_map)
        print(f"UID Accuracy - Missing: {len(uid_accuracy['missing_uids'])}, "
              f"Invalid Primary: {len(uid_accuracy['incorrect_primary_uids'])}, "
              f"Position Mismatches: {len(uid_accuracy['position_mismatches'])}")

        # 2. Semantic Coherence
        semantic_analysis = analyze_semantic_coherence(chunks, uid_map)
        print(f"Semantic Coherence - Hierarchy violations: {len(semantic_analysis['hierarchy_violations'])}, "
              f"Sentence breaks: {len(semantic_analysis['sentence_breaks'])}, "
              f"Context issues: {len(semantic_analysis['context_preservation'])}")

        # 3. Chunking Boundaries
        boundary_analysis = analyze_chunking_boundaries(chunks, uid_map)
        print(f"Boundaries - Natural: {boundary_analysis['natural_boundaries']}, "
              f"Mid-thought: {boundary_analysis['mid_thought_splits']}, "
              f"Orphaned: {len(boundary_analysis['orphaned_chunks'])}")

        analysis_results[strategy] = {
            'uid_accuracy': uid_accuracy,
            'semantic_coherence': semantic_analysis,
            'boundaries': boundary_analysis
        }

    # 4. Statistical Analysis
    print("\n=== Statistical Distribution Analysis ===")
    stats = analyze_statistical_distribution(chunks_dict)

    for strategy, stat in stats.items():
        print(f"{strategy}: {stat['total_chunks']} chunks, "
              f"avg tokens: {stat['token_stats']['mean']:.1f}, "
              f"avg UIDs: {stat['source_uid_stats']['mean']:.1f}")

    # 5. Overlap Analysis
    print("\n=== Overlap Analysis ===")
    overlaps = find_overlapping_chunks(chunks_dict)
    for strategy, overlap in overlaps.items():
        print(f"{strategy}: {overlap['total_overlapping_uids']} UIDs appear in multiple chunks")

    # 6. Generate Examples
    print("\n=== Generating Examples ===")
    examples = generate_examples(chunks_dict, uid_map)

    # 7. Create Visualizations
    print("\n=== Creating Visualizations ===")
    create_visualizations(stats, '/Users/sheikmeeran/roam-test/experiments')

    # Compile comprehensive report
    report = {
        'summary': {
            'total_original_uids': len(uid_map),
            'strategies_analyzed': list(chunks_dict.keys()),
            'analysis_timestamp': pd.Timestamp.now().isoformat()
        },
        'detailed_analysis': analysis_results,
        'statistical_distribution': stats,
        'overlap_analysis': overlaps,
        'examples': examples
    }

    # Save detailed report
    with open('/Users/sheikmeeran/roam-test/experiments/chunking_quality_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)

    # Generate readable summary report
    generate_summary_report(report, stats, analysis_results, examples)

    print("\n✅ Analysis complete! Check chunking_quality_report.json and chunking_summary.md for results.")

def generate_summary_report(report: Dict, stats: Dict, analysis_results: Dict, examples: Dict):
    """Generate a human-readable summary report"""

    summary = []
    summary.append("# Roam Research Semantic Chunking Quality Analysis")
    summary.append("## Executive Summary")

    # Find best strategy based on multiple criteria
    strategy_scores = {}
    for strategy in stats.keys():
        score = 0

        # Token distribution score (prefer 50-200 token range)
        mean_tokens = stats[strategy]['token_stats']['mean']
        if 50 <= mean_tokens <= 200:
            score += 3
        elif 30 <= mean_tokens <= 300:
            score += 1

        # Boundary quality score
        boundaries = analysis_results[strategy]['boundaries']
        natural_pct = boundaries['natural_boundaries'] / (boundaries['natural_boundaries'] + boundaries['mid_thought_splits'])
        score += natural_pct * 3

        # Coherence score
        semantic = analysis_results[strategy]['semantic_coherence']
        violation_pct = len(semantic['hierarchy_violations']) / semantic['total_chunks']
        score += (1 - violation_pct) * 2

        # UID accuracy score
        uid_acc = analysis_results[strategy]['uid_accuracy']
        accuracy_pct = 1 - (len(uid_acc['missing_uids']) + len(uid_acc['incorrect_primary_uids'])) / uid_acc['total_source_uids']
        score += accuracy_pct * 2

        strategy_scores[strategy] = score

    best_strategy = max(strategy_scores.keys(), key=lambda k: strategy_scores[k])

    summary.append(f"**Recommended Strategy: {best_strategy}**")
    summary.append(f"Based on comprehensive analysis across semantic coherence, boundary quality, UID accuracy, and statistical distribution.")
    summary.append("")

    # Detailed findings for each strategy
    summary.append("## Detailed Analysis by Strategy")

    for strategy, stat in stats.items():
        summary.append(f"### {strategy.title()} Strategy")
        summary.append("")

        # Statistical overview
        summary.append("#### Statistical Overview")
        summary.append(f"- **Total Chunks**: {stat['total_chunks']}")
        summary.append(f"- **Average Token Count**: {stat['token_stats']['mean']:.1f} (σ={stat['token_stats']['std']:.1f})")
        summary.append(f"- **Token Range**: {stat['token_stats']['min']} - {stat['token_stats']['max']}")
        summary.append(f"- **Median Token Count**: {stat['token_stats']['median']:.1f}")
        summary.append(f"- **Average Source UIDs per Chunk**: {stat['source_uid_stats']['mean']:.1f}")
        summary.append("")

        # Quality metrics
        analysis = analysis_results[strategy]
        summary.append("#### Quality Metrics")

        # UID Accuracy
        uid_acc = analysis['uid_accuracy']
        accuracy_rate = 1 - (len(uid_acc['missing_uids']) + len(uid_acc['incorrect_primary_uids'])) / max(uid_acc['total_source_uids'], 1)
        summary.append(f"- **UID Tracking Accuracy**: {accuracy_rate:.1%}")
        summary.append(f"  - Missing UIDs: {len(uid_acc['missing_uids'])}")
        summary.append(f"  - Incorrect Primary UIDs: {len(uid_acc['incorrect_primary_uids'])}")
        summary.append(f"  - Position Mismatches: {len(uid_acc['position_mismatches'])}")

        # Semantic Coherence
        semantic = analysis['semantic_coherence']
        summary.append(f"- **Semantic Coherence Issues**:")
        summary.append(f"  - Hierarchy Violations: {len(semantic['hierarchy_violations'])} ({len(semantic['hierarchy_violations'])/semantic['total_chunks']:.1%})")
        summary.append(f"  - Mid-sentence Breaks: {len(semantic['sentence_breaks'])} ({len(semantic['sentence_breaks'])/semantic['total_chunks']:.1%})")
        summary.append(f"  - Context Preservation Issues: {len(semantic['context_preservation'])} ({len(semantic['context_preservation'])/semantic['total_chunks']:.1%})")

        # Boundary Quality
        boundaries = analysis['boundaries']
        natural_pct = boundaries['natural_boundaries'] / (boundaries['natural_boundaries'] + boundaries['mid_thought_splits'])
        summary.append(f"- **Boundary Quality**: {natural_pct:.1%} natural boundaries")
        summary.append(f"  - Natural Boundaries: {boundaries['natural_boundaries']}")
        summary.append(f"  - Mid-thought Splits: {boundaries['mid_thought_splits']}")
        summary.append(f"  - Orphaned Chunks: {len(boundaries['orphaned_chunks'])}")
        summary.append(f"  - Reference Splits: {len(boundaries['reference_splits'])}")
        summary.append("")

        # Examples
        strategy_examples = examples[strategy]
        if strategy_examples['good_examples']:
            summary.append("#### Good Chunking Examples")
            for i, example in enumerate(strategy_examples['good_examples'][:2]):
                summary.append(f"**Example {i+1}** (Chunk {example['chunk_index']}):")
                summary.append(f"- Tokens: {example['token_count']}, Source UIDs: {example['source_uid_count']}")
                summary.append(f"- Reason: {example['reason']}")
                summary.append(f"- Preview: \"{example['text_preview'][:150]}...\"")
                summary.append("")

        if strategy_examples['poor_examples']:
            summary.append("#### Poor Chunking Examples")
            for i, example in enumerate(strategy_examples['poor_examples'][:2]):
                summary.append(f"**Example {i+1}** (Chunk {example['chunk_index']}):")
                summary.append(f"- Tokens: {example['token_count']}, Source UIDs: {example['source_uid_count']}")
                summary.append(f"- Issues: {example['reason']}")
                summary.append(f"- Preview: \"{example['text_preview'][:150]}...\"")
                summary.append("")

        summary.append("---")
        summary.append("")

    # Comparative analysis
    summary.append("## Comparative Analysis")
    summary.append("")
    summary.append("| Strategy | Chunks | Avg Tokens | Natural Boundaries | UID Accuracy | Hierarchy Violations |")
    summary.append("|----------|--------|------------|-------------------|--------------|---------------------|")

    for strategy in stats.keys():
        stat = stats[strategy]
        analysis = analysis_results[strategy]

        chunks = stat['total_chunks']
        avg_tokens = stat['token_stats']['mean']

        boundaries = analysis['boundaries']
        natural_pct = boundaries['natural_boundaries'] / (boundaries['natural_boundaries'] + boundaries['mid_thought_splits'])

        uid_acc = analysis['uid_accuracy']
        accuracy_rate = 1 - (len(uid_acc['missing_uids']) + len(uid_acc['incorrect_primary_uids'])) / max(uid_acc['total_source_uids'], 1)

        semantic = analysis['semantic_coherence']
        violation_pct = len(semantic['hierarchy_violations']) / semantic['total_chunks']

        summary.append(f"| {strategy} | {chunks} | {avg_tokens:.1f} | {natural_pct:.1%} | {accuracy_rate:.1%} | {violation_pct:.1%} |")

    summary.append("")

    # Recommendations
    summary.append("## Recommendations")
    summary.append("")
    summary.append(f"1. **Primary Recommendation**: Use the **{best_strategy}** strategy for production.")
    summary.append(f"   - Highest overall quality score: {strategy_scores[best_strategy]:.2f}")
    summary.append("")

    # Strategy-specific recommendations
    for strategy, score in sorted(strategy_scores.items(), key=lambda x: x[1], reverse=True):
        analysis = analysis_results[strategy]
        stat = stats[strategy]

        summary.append(f"2. **{strategy.title()} Strategy Improvements**:")

        if len(analysis['semantic_coherence']['hierarchy_violations']) > 0:
            summary.append("   - Address hierarchy violations by improving context preservation")

        if len(analysis['boundaries']['orphaned_chunks']) > 0:
            summary.append("   - Merge orphaned chunks with adjacent context")

        if stat['token_stats']['mean'] < 50:
            summary.append("   - Increase chunk size to improve context")
        elif stat['token_stats']['mean'] > 200:
            summary.append("   - Decrease chunk size for better embedding performance")

        summary.append("")

    summary.append("## Implementation Notes")
    summary.append("")
    summary.append("- **Optimal Token Range**: 50-200 tokens for embedding performance")
    summary.append("- **Context Preservation**: Maintain parent-child relationships in hierarchical content")
    summary.append("- **Boundary Respect**: Prioritize sentence and paragraph boundaries")
    summary.append("- **Reference Integrity**: Avoid splitting block references ((uid)) and page references [[page]]")
    summary.append("")

    # Write summary report
    with open('/Users/sheikmeeran/roam-test/experiments/chunking_summary.md', 'w') as f:
        f.write('\n'.join(summary))

if __name__ == "__main__":
    main()