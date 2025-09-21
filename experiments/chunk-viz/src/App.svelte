<script>
  import { onMount } from 'svelte';
  import PageSidebar from './components/PageSidebar.svelte';
  import ChunkedText from './components/ChunkedText.svelte';
  import ConfigSelector from './components/ConfigSelector.svelte';

  let chunkData = $state(null);
  let selectedPageIndex = $state(0);
  let selectedConfigs = $state([]);
  let loading = $state(true);
  let error = $state(null);

  // Load JSON data
  onMount(async () => {
    try {
      // In dev, load from local file; in prod, could fetch from server
      const response = await fetch('/chunk_data.json');
      if (!response.ok) throw new Error('Failed to load chunk data');
      chunkData = await response.json();
      loading = false;
    } catch (err) {
      error = err.message;
      loading = false;
    }
  });

  let currentPage = $derived(chunkData?.pages?.[selectedPageIndex]);
  let availableConfigs = $derived(chunkData?.configs ? Object.keys(chunkData.configs) : []);

  function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          chunkData = JSON.parse(e.target.result);
          selectedPageIndex = 0;
          error = null;
        } catch (err) {
          error = 'Invalid JSON file';
        }
      };
      reader.readAsText(file);
    }
  }
</script>

<main>
  <div class="container">
    {#if loading}
      <div class="loading">Loading chunk data...</div>
    {:else if error}
      <div class="error">
        <p>Error: {error}</p>
        <label class="upload-btn">
          Upload chunk_data.json
          <input type="file" accept=".json" on:change={handleFileUpload} />
        </label>
      </div>
    {:else if chunkData}
      <aside class="sidebar">
        <PageSidebar
          pages={chunkData.pages}
          bind:selectedIndex={selectedPageIndex}
        />
        <label class="upload-btn">
          + Load New Data
          <input type="file" accept=".json" on:change={handleFileUpload} />
        </label>
      </aside>

      <div class="main-content">
        <ConfigSelector
          configs={availableConfigs}
          bind:selected={selectedConfigs}
        />

        {#if currentPage}
          <div class="text-views">
            {#each selectedConfigs as configName}
              <div class="text-view" style="flex: 1;">
                <h3>{configName}</h3>
                <ChunkedText
                  page={currentPage}
                  configName={configName}
                />
              </div>
            {/each}
          </div>
        {/if}
      </div>
    {/if}
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f5f5f5;
  }

  main {
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .container {
    flex: 1;
    display: flex;
    overflow: hidden;
  }

  .sidebar {
    width: 250px;
    background: white;
    border-right: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
  }

  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .text-views {
    flex: 1;
    display: flex;
    gap: 0.5rem;
    padding: 0.5rem;
    overflow: hidden;
  }

  .text-view {
    background: white;
    border-radius: 4px;
    padding: 0.5rem;
    overflow-y: auto;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }

  .text-view h3 {
    margin-top: 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #4CAF50;
    color: #333;
  }

  .loading, .error {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 2rem;
  }

  .error {
    color: #d32f2f;
  }

  .upload-btn {
    display: block;
    padding: 0.75rem 1rem;
    background: #4CAF50;
    color: white;
    text-align: center;
    cursor: pointer;
    border: none;
    border-radius: 4px;
    margin: 1rem;
    transition: background 0.3s;
  }

  .upload-btn:hover {
    background: #45a049;
  }

  .upload-btn input {
    display: none;
  }
</style>