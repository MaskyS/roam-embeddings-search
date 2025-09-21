<script>
  import { getChunkColor } from '../utils/colors.js';
  import Markdown from 'svelte-exmarkdown';

  export let page;
  export let configName;

  $: config = page?.configs?.[configName];
  $: chunks = config?.chunks || [];
  $: gaps = config?.gaps || [];
  $: text = page?.linearized_text || '';

  // Force segments to recompute when any dependency changes
  $: chunks, gaps, text, segments = renderTextWithChunks();

  let segments = [];

  function renderTextWithChunks() {
    if (!chunks || !chunks.length || !text) {
      return [];
    }

    const newSegments = [];
    let lastEnd = 0;

    chunks.forEach((chunk, i) => {
      // Check if there's a gap before this chunk
      const gap = gaps.find(g => g.after_chunk === i - 1);

      if (gap && gap.gap_start > lastEnd) {
        // Add skipped indicator
        newSegments.push({
          type: 'gap',
          content: `↓ ... ${gap.gap_size} chars skipped ... ↓`
        });
      }

      // Use chunk.text directly instead of substring
      newSegments.push({
        type: 'chunk',
        id: chunk.id,
        content: chunk.text,  // Use the text from chunk directly
        color: getChunkColor(i),
        tokens: chunk.token_count,
        length: chunk.length
      });

      lastEnd = chunk.end_index;
    });

    return newSegments;
  }

  let hoveredChunk = null;
</script>

<div class="chunked-text">
  {#if config?.error}
    <div class="error">Error: {config.error}</div>
  {:else}
    <div class="text-container">
      {#each segments as segment}
        {#if segment.type === 'gap'}
          <div class="gap-indicator">
            {segment.content}
          </div>
        {:else if segment.type === 'chunk'}
          <div
            class="chunk"
            style="--chunk-color: {segment.color};"
            on:mouseenter={() => hoveredChunk = segment.id}
            on:mouseleave={() => hoveredChunk = null}
          >
            <!-- <sup class="chunk-marker">{segment.id}</sup> -->
            <span class="chunk-text"><Markdown md={segment.content} /></span>
            {#if hoveredChunk === segment.id}
              <div class="chunk-tooltip">
                Chunk {segment.id} • {segment.tokens} tokens • {segment.length} chars
              </div>
            {/if}
          </div>
        {/if}
      {/each}
    </div>

    {#if chunks && chunks.length > 0}
      <div class="legend">
        {#each chunks.slice(0, 12) as chunk, i}
          <span class="legend-item" style="color: {getChunkColor(i)};">
            [{chunk.id}] {chunk.token_count}tok
          </span>
        {/each}
        {#if chunks.length > 12}
          <span class="legend-item">... +{chunks.length - 12} more</span>
        {/if}
      </div>
    {/if}
  {/if}
</div>

<style>
  .chunked-text {
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .text-container {
    flex: 1;
    overflow-y: auto;
    padding: 0.5rem;
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace;
    font-size: 0.85rem;
    line-height: 1.5;
  }

  .chunk {
    display: inline;
    position: relative;
    transition: opacity 0.2s;
    color: var(--chunk-color);
  }

  .chunk:hover {
    opacity: 0.9;
  }

  /* .chunk-marker {
    font-size: 0.65rem;
    font-weight: bold;
    opacity: 0.7;
    margin-right: 2px;
    vertical-align: super;
  } */

  .chunk-text {
    display: inline;
    color: var(--chunk-color);
  }

  /* No spacing between chunks - they flow naturally */

  /* Markdown styling within chunks - inherit chunk color */
  .chunk-text :global(h1),
  .chunk-text :global(h2),
  .chunk-text :global(h3),
  .chunk-text :global(p),
  .chunk-text :global(li),
  .chunk-text :global(blockquote) {
    color: inherit;
  }

  .chunk-text :global(h1) {
    font-size: 1.5rem;
    margin: 0.5rem 0;
    font-weight: bold;
  }

  .chunk-text :global(h2) {
    font-size: 1.3rem;
    margin: 0.4rem 0;
  }

  .chunk-text :global(h3) {
    font-size: 1.1rem;
    margin: 0.3rem 0;
  }

  .chunk-text :global(p) {
    margin: 0.5rem 0;
  }

  .chunk-text :global(ul),
  .chunk-text :global(ol) {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
  }

  .chunk-text :global(li) {
    margin: 0.25rem 0;
  }

  .chunk-text :global(code) {
    background: rgba(0,0,0,0.05);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
    font-size: 0.9em;
    opacity: 0.9;
  }

  .chunk-text :global(pre) {
    background: rgba(0,0,0,0.05);
    padding: 0.5rem;
    border-radius: 4px;
    overflow-x: auto;
  }

  .chunk-text :global(blockquote) {
    border-left: 3px solid currentColor;
    margin: 0.5rem 0;
    padding-left: 1rem;
    opacity: 0.8;
  }

  .chunk-text :global(strong) {
    font-weight: bold;
  }

  .chunk-text :global(em) {
    font-style: italic;
  }

  .chunk-text :global(a) {
    color: inherit;
    text-decoration: underline;
    opacity: 0.9;
  }

  .chunk-text :global(a:hover) {
    opacity: 1;
  }

  .chunk-text :global(img) {
    max-width: 200px;
    max-height: 200px;
    object-fit: contain;
    display: block;
    margin: 0.5rem 0;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    cursor: pointer;
    transition: transform 0.2s;
  }

  .chunk-text :global(img:hover) {
    transform: scale(1.05);
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }

  .chunk-tooltip {
    position: absolute;
    top: -25px;
    right: 0;
    background: #333;
    color: white;
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    font-size: 0.75rem;
    white-space: nowrap;
    z-index: 10;
    pointer-events: none;
  }

  .chunk-tooltip::after {
    content: '';
    position: absolute;
    top: 100%;
    right: 20px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #333;
  }

  .gap-indicator {
    margin: 1rem 0;
    padding: 0.5rem;
    background: #fff3cd;
    border: 1px dashed #ffc107;
    border-radius: 4px;
    text-align: center;
    color: #856404;
    font-style: italic;
  }

  .legend {
    padding: 0.5rem;
    border-top: 1px solid #e0e0e0;
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem;
    font-size: 0.7rem;
  }

  .legend-item {
    padding: 0.2rem 0.5rem;
    background: #f5f5f5;
    border-radius: 3px;
    font-weight: 500;
  }

  .error {
    padding: 1rem;
    color: #d32f2f;
  }
</style>