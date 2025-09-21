<script>
  export let configs = [];
  export let selected = [];

  // Initialize selected with first config if empty
  $: if (selected.length === 0 && configs.length > 0) {
    selected = [configs[0]];
  }

  // Map config names to their display labels with parameters
  const configLabels = {
    'default': 'Default (t=0.6, s=1, m=50)',
    'roam_optimized': 'Roam Optimized (t=0.4, s=1, m=250)',
    'tight': 'Tight (t=0.8, s=1, m=30)',
    'loose': 'Loose (t=0.4, s=1, m=100)',
    'no_skip': 'No Skip (t=0.6, s=0, m=50)',
    'large_skip': 'Large Skip (t=0.6, s=3, m=50)'
  };

  function toggleConfig(config) {
    if (selected.includes(config)) {
      if (selected.length > 1) {
        selected = selected.filter(c => c !== config);
      }
    } else {
      if (selected.length < 3) {  // Limit to 3 for readability
        selected = [...selected, config];
      } else {
        alert('Maximum 3 configurations can be compared at once');
      }
    }
  }
</script>

<div class="config-bar">
  <span class="label">Configurations:</span>
  <div class="config-buttons">
    {#each configs as config}
      <button
        class="config-btn"
        class:active={selected.includes(config)}
        on:click={() => toggleConfig(config)}
        title="threshold={config === 'default' || config === 'no_skip' || config === 'large_skip' ? '0.6' : config === 'tight' ? '0.8' : '0.4'}, skip_window={config === 'no_skip' ? '0' : config === 'large_skip' ? '3' : '1'}, min_chunk={config === 'tight' ? '30' : config === 'loose' ? '100' : '50'}"
      >
        {configLabels[config] || config}
      </button>
    {/each}
  </div>
  <span class="hint">t=threshold, s=skip_window, m=min_chunk_size • Max 3 configs</span>
</div>

<style>
  .config-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem;
    background: white;
    border-bottom: 1px solid #e0e0e0;
  }

  .label {
    font-weight: 500;
    color: #666;
  }

  .config-buttons {
    display: flex;
    gap: 0.5rem;
  }

  .config-btn {
    padding: 0.5rem 1rem;
    border: 2px solid #ddd;
    background: white;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.9rem;
  }

  .config-btn:hover {
    background: #f5f5f5;
  }

  .config-btn.active {
    background: #4CAF50;
    color: white;
    border-color: #4CAF50;
  }

  .hint {
    margin-left: auto;
    font-size: 0.85rem;
    color: #999;
  }
</style>