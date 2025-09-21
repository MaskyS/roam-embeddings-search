# Semantic Chunk Visualizer

A tool to visualize and compare different semantic chunking configurations on Roam Research pages.

## Purpose

This tool helps you understand how different parameters affect semantic chunking by:
- Visualizing chunk boundaries in linearized Roam pages
- Comparing multiple configurations side-by-side
- Showing gaps when skip_window merges non-consecutive content
- Helping optimize parameters for your specific content

## Setup

### 1. Generate Chunk Data

First, generate the chunk data from your Roam graph:

```bash
cd experiments

# Install Python dependencies if needed
pip install chonkie httpx python-dotenv

# Generate chunk data from Roam
python generate_chunk_data.py --pages 3 --output chunk_data.json

# Or specify specific page UIDs
python generate_chunk_data.py --page-uids "page-uid-1" "page-uid-2" --output chunk_data.json
```

### 2. Run the Visualizer

```bash
cd chunk-viz

# Install dependencies
npm install

# Copy the generated JSON to public folder
cp ../chunk_data.json public/

# Start the dev server
npm run dev
```

Open http://localhost:5000 in your browser.

## How to Use

1. **Select a page** from the left sidebar
2. **Toggle configurations** to compare (up to 3 at once)
3. **Observe chunk boundaries**:
   - Each chunk has a colored border and `[N]` marker
   - Hover over chunks to see token/character counts
   - Yellow boxes show gaps from skip_window behavior

## Understanding the Configurations

The tool tests 5 default configurations:

- **default**: Balanced settings (threshold=0.6, skip_window=1)
- **tight**: More granular chunks (threshold=0.8)
- **loose**: Fewer, larger chunks (threshold=0.4)
- **no_skip**: No merging of non-consecutive content (skip_window=0)
- **large_skip**: Looks further for similar content (skip_window=3)

## Customizing Configurations

Edit `CHUNKER_CONFIGS` in `generate_chunk_data.py`:

```python
CHUNKER_CONFIGS = {
    "my_config": {
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "threshold": 0.7,  # 0-1, higher = more splits
        "skip_window": 2,  # 0 = no skip, >0 = merge similar non-consecutive
        "min_chunk_size": 50
    }
}
```

## Key Parameters

- **threshold**: Similarity threshold (0-1)
  - Higher (0.8+) = more splits, smaller chunks
  - Lower (0.4-) = fewer splits, larger chunks

- **skip_window**: How far to look for similar content
  - 0 = only merge consecutive sentences
  - 1+ = can merge non-consecutive similar groups

- **min_chunk_size**: Minimum tokens per chunk

## Interpreting Results

- **Contiguous chunks**: Normal flow, no gaps
- **Gaps (yellow indicators)**: Skip_window merged non-consecutive content
- **Token counts**: Shown on hover and in legend
- **Color cycling**: Colors repeat every 12 chunks

## Notes

- The sentence transformer model runs locally, no API needed
- First run may be slow as models download
- Linearization converts Roam's hierarchy to markdown-style text
- Page title becomes `# Title`, blocks become `- content` with indentation