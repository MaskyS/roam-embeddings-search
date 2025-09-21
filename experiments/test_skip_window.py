#!/usr/bin/env python3
"""
Test skip_window behavior in Chonkie's SemanticChunker.
Based on the example from the docs - let's see what ACTUALLY happens.
"""

from chonkie import SemanticChunker
import json

# Text with clearly alternating topics (AI and Finance)
text = """Neural networks process information through interconnected nodes.
The stock market experienced significant volatility this quarter.
Deep learning models require substantial training data for optimization.
Economic indicators point to potential recession risks ahead.
GPU acceleration has revolutionized machine learning computations.
Federal reserve policies impact global financial markets.
Transformer architectures dominate modern NLP applications.
Cryptocurrency markets show correlation with traditional assets.
Natural language processing enables machines to understand human text.
Interest rates affect bond yields and equity valuations significantly."""

print("="*60)
print("TESTING SKIP_WINDOW BEHAVIOR")
print("="*60)
print("\nOriginal text (alternating AI/Finance topics):")
print("-"*40)
sentences = text.strip().split('\n')
for i, sent in enumerate(sentences):
    topic = "AI" if i % 2 == 0 else "Finance"
    print(f"{i+1}. [{topic}] {sent[:60]}...")

# Test different skip_window values
configs = [
    {"name": "No skip (window=0)", "skip_window": 0},
    {"name": "Skip 1 (window=1)", "skip_window": 1},
    {"name": "Skip 2 (window=2)", "skip_window": 2},
    {"name": "Skip 3 (window=3)", "skip_window": 3},
]

for config in configs:
    print("\n" + "="*60)
    print(f"CONFIG: {config['name']}")
    print("="*60)

    chunker = SemanticChunker(
        embedding_model="ibm-granite/granite-embedding-small-english-r2",
        threshold=0.65,  # Moderate threshold
        chunk_size=512,
        skip_window=config['skip_window'],
        min_chunk_size=50,
        similarity_window=3
    )

    chunks = chunker.chunk(text)

    print(f"\nNumber of chunks: {len(chunks)}")
    print("\nChunk details:")
    print("-"*40)

    for i, chunk in enumerate(chunks):
        # Identify which sentences are in this chunk
        chunk_text = chunk.text
        included_sentences = []

        for j, sent in enumerate(sentences):
            if sent[:50] in chunk_text:
                topic = "AI" if j % 2 == 0 else "Finance"
                included_sentences.append(f"S{j+1}[{topic}]")

        print(f"\nChunk {i+1}:")
        print(f"  Range: [{chunk.start_index}:{chunk.end_index}] ({chunk.end_index - chunk.start_index} chars)")
        print(f"  Sentences: {', '.join(included_sentences)}")
        print(f"  Preview: {chunk.text[:80]}...")

        # Check if this chunk has non-consecutive content
        if len(included_sentences) > 1:
            # Parse sentence numbers
            sent_nums = []
            for s in included_sentences:
                num = int(s.split('[')[0][1:])
                sent_nums.append(num)

            # Check for gaps
            is_consecutive = all(sent_nums[i+1] - sent_nums[i] == 1 for i in range(len(sent_nums)-1))
            if not is_consecutive:
                print(f"  ⚠️  NON-CONSECUTIVE CONTENT DETECTED! Sentence gaps: {sent_nums}")

print("\n" + "="*60)
print("KEY OBSERVATIONS:")
print("="*60)
print("""
1. Does skip_window actually MERGE non-consecutive text?
   - If yes: We should see chunks with gaps (e.g., S1, S3, S5 in one chunk)
   - If no: It just affects boundary decisions but keeps text contiguous

2. How does skip_window affect the chunking?
   - Look at how AI vs Finance sentences are grouped
   - Are similar topics pulled together across gaps?

3. What would "gaps" in the output actually mean?
   - Our detect_gaps function looks for chunk.end_index != next_chunk.start_index
   - But if skip_window merges non-consecutive text, how is that represented?
""")

# Additional test: Very dissimilar content
print("\n" + "="*60)
print("TEST 2: VERY DISSIMILAR CONTENT")
print("="*60)

dissimilar_text = """Machine learning algorithms process vast amounts of data.
Banana bread requires ripe bananas and flour.
Neural networks consist of interconnected layers.
The weather today is sunny with mild temperatures.
Deep learning models can recognize complex patterns.
Cats typically sleep for 12-16 hours per day.
Natural language processing enables text understanding.
Pizza originated in Naples, Italy centuries ago."""

print("\nTesting with very dissimilar alternating content...")
chunker = SemanticChunker(
    embedding_model="ibm-granite/granite-embedding-small-english-r2",
    threshold=0.65,
    chunk_size=512,
    skip_window=3,  # Aggressive skip window
    min_chunk_size=50
)

chunks = chunker.chunk(dissimilar_text)
print(f"\nWith skip_window=3 and dissimilar content:")
print(f"Number of chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    lines_in_chunk = chunk.text.count('\n') + 1
    print(f"\nChunk {i+1}: {lines_in_chunk} lines")
    print(f"  Preview: {chunk.text[:100]}...")