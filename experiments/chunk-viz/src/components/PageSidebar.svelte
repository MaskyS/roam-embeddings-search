<script>
  export let pages = [];
  export let selectedIndex = 0;
</script>

<div class="page-list">
  <h3>Pages</h3>
  {#each pages as page, i}
    <button
      class="page-item"
      class:selected={selectedIndex === i}
      on:click={() => selectedIndex = i}
    >
      <span class="page-title">{page.title}</span>
      <span class="page-info">{page.text_length} chars</span>
    </button>
  {/each}
</div>

<style>
  .page-list {
    flex: 1;
    padding: 0.5rem;
  }

  h3 {
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .page-item {
    display: block;
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 0.25rem;
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s;
  }

  .page-item:hover {
    background: #f5f5f5;
    transform: translateX(2px);
  }

  .page-item.selected {
    background: #e8f5e9;
    border-color: #4CAF50;
    border-width: 2px;
  }

  .page-title {
    display: block;
    font-weight: 500;
    color: #333;
    margin-bottom: 0.25rem;
  }

  .page-info {
    display: block;
    font-size: 0.85rem;
    color: #999;
  }
</style>