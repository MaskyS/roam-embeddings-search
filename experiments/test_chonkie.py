#!/usr/bin/env python3
"""
Test Chonkie with the granite embedding model
"""

from chonkie import SemanticChunker
import time

print("Testing Chonkie with granite embedding model...")

# Sample text to chunk
sample_text = """
# Introduction to Machine Learning

Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves.

## Types of Machine Learning

There are three main types of machine learning:

1. **Supervised Learning**: The algorithm learns from labeled training data, helping to predict outcomes for unforeseen data. Common examples include classification and regression problems.

2. **Unsupervised Learning**: The algorithm learns patterns from unlabeled data. The system tries to learn without a teacher. Examples include clustering and dimensionality reduction.

3. **Reinforcement Learning**: The algorithm learns through trial and error by interacting with an environment. It receives rewards or penalties for its actions and learns to maximize the reward.

## Applications

Machine learning has numerous applications across various industries:

- Healthcare: Disease diagnosis, drug discovery, personalized medicine
- Finance: Fraud detection, risk assessment, algorithmic trading
- Transportation: Autonomous vehicles, route optimization
- Retail: Recommendation systems, demand forecasting
- Technology: Natural language processing, computer vision, speech recognition

## Getting Started

To begin with machine learning, you should have a good foundation in:
- Mathematics (linear algebra, calculus, statistics)
- Programming (Python is most popular)
- Data manipulation and visualization
- Understanding of algorithms and data structures

The journey into machine learning is exciting and constantly evolving with new techniques and applications emerging regularly.
"""

print(f"Sample text length: {len(sample_text)} characters\n")

# Test the chunker
print("Initializing SemanticChunker with granite model...")
start = time.time()

try:
    chunker = SemanticChunker(
        embedding_model="ibm-granite/granite-embedding-small-english-r2",
        threshold=0.6,
        skip_window=1,
        min_chunk_size=50
    )
    init_time = time.time() - start
    print(f"✓ Chunker initialized in {init_time:.2f} seconds\n")

    # Perform chunking
    print("Chunking text...")
    chunk_start = time.time()
    chunks = chunker.chunk(sample_text)
    chunk_time = time.time() - chunk_start

    print(f"✓ Chunking completed in {chunk_time:.2f} seconds\n")
    print(f"Number of chunks created: {len(chunks)}\n")

    # Display chunks
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")
        print(f"Start: {chunk.start_index}, End: {chunk.end_index}")
        print(f"Tokens: {chunk.token_count}")
        print(f"Text preview: {chunk.text[:100]}..." if len(chunk.text) > 100 else f"Text: {chunk.text}")
        print()

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\nTotal time: {time.time() - start:.2f} seconds")