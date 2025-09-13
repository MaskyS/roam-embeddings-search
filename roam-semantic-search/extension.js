// Roam Semantic Search Extension - Depot Compatible Version
// Follows official Roam Depot extension guidelines

let extensionAPI;
let searchState = {
  isOpen: false,
  query: '',
  results: [],
  selectedIndex: 0,
  loading: false,
  error: null,
  abortController: null,
  commands: [] // Track commands for cleanup
};

// Configuration - will be moved to settings panel
const DEFAULT_CONFIG = {
  backendURL: 'http://localhost:8001',
  searchLimit: 20,
  debounceDelay: 300
};

let config = { ...DEFAULT_CONFIG };

// API Client
class SearchAPI {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }
  
  async checkConnection() {
    try {
      const response = await fetch(this.baseURL);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('[Semantic Search] Connection error:', error);
      throw error;
    }
  }
  
  async search(query, signal) {
    try {
      const url = `${this.baseURL}/search?q=${encodeURIComponent(query)}&limit=${config.searchLimit}`;
      const response = await fetch(url, { signal });
      
      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log('[Semantic Search] Request cancelled');
        return null;
      }
      console.error('[Semantic Search] Search error:', error);
      throw error;
    }
  }
}

let searchAPI;

// Helper functions
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text || '';
  return div.innerHTML;
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Modal management with proper CSS prefixes
function createModal() {
  // Check if modal already exists
  if (document.getElementById('rss-modal')) {
    return;
  }
  
  const modalHTML = `
    <div id="rss-modal" class="rss-modal">
      <div class="rss-backdrop"></div>
      <div class="rss-container">
        <div class="rss-header">
          <h3 class="rss-title">🔍 Semantic Search</h3>
          <button class="rss-close bp3-button bp3-minimal">×</button>
        </div>
        <div class="rss-search">
          <input type="text" class="rss-input bp3-input" placeholder="Enter search query..." />
        </div>
        <div class="rss-status"></div>
        <div class="rss-results"></div>
      </div>
    </div>
  `;
  
  // Add styles
  addStyles();
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  // Get elements
  const modal = document.getElementById('rss-modal');
  const backdrop = modal.querySelector('.rss-backdrop');
  const closeBtn = modal.querySelector('.rss-close');
  const input = modal.querySelector('.rss-input');
  
  // Event listeners
  backdrop.addEventListener('click', closeModal);
  closeBtn.addEventListener('click', closeModal);
  input.addEventListener('input', debouncedSearch);
  document.addEventListener('keydown', handleKeydown);
  
  // Focus input
  input.focus();
  
  searchState.isOpen = true;
}

function closeModal() {
  // Cancel any pending requests
  if (searchState.abortController) {
    searchState.abortController.abort();
  }
  
  // Remove event listeners
  document.removeEventListener('keydown', handleKeydown);
  
  // Remove DOM element
  const modal = document.getElementById('rss-modal');
  if (modal) {
    modal.remove();
  }
  
  // Reset state
  searchState.isOpen = false;
  searchState.selectedIndex = 0;
  searchState.results = [];
}

function handleKeydown(event) {
  if (!searchState.isOpen) return;
  
  if (event.key === 'Escape') {
    closeModal();
  } else if (event.key === 'ArrowDown') {
    event.preventDefault();
    selectNext();
  } else if (event.key === 'ArrowUp') {
    event.preventDefault();
    selectPrevious();
  } else if (event.key === 'Enter') {
    event.preventDefault();
    if (searchState.selectedIndex >= 0 && searchState.results[searchState.selectedIndex]) {
      const result = searchState.results[searchState.selectedIndex];
      handleResultClick(result.uid, event);
    }
  }
}

function selectNext() {
  if (searchState.results.length > 0) {
    searchState.selectedIndex = Math.min(searchState.selectedIndex + 1, searchState.results.length - 1);
    updateSelection();
  }
}

function selectPrevious() {
  if (searchState.results.length > 0) {
    searchState.selectedIndex = Math.max(searchState.selectedIndex - 1, 0);
    updateSelection();
  }
}

function updateSelection() {
  const results = document.querySelectorAll('.rss-result');
  results.forEach((el, index) => {
    if (index === searchState.selectedIndex) {
      el.classList.add('rss-selected');
    } else {
      el.classList.remove('rss-selected');
    }
  });
}

function showLoading() {
  const statusEl = document.querySelector('.rss-status');
  if (statusEl) {
    statusEl.innerHTML = '<div class="rss-loading">Searching...</div>';
  }
}

function showError(message) {
  const statusEl = document.querySelector('.rss-status');
  if (statusEl) {
    statusEl.innerHTML = `<div class="rss-error">⚠️ ${escapeHtml(message)}</div>`;
  }
}

function clearStatus() {
  const statusEl = document.querySelector('.rss-status');
  if (statusEl) {
    statusEl.innerHTML = '';
  }
}

function renderResults(results) {
  const resultsEl = document.querySelector('.rss-results');
  if (!resultsEl) return;
  
  if (!results || results.length === 0) {
    resultsEl.innerHTML = '<div class="rss-no-results">No results found</div>';
    return;
  }
  
  searchState.results = results;
  searchState.selectedIndex = 0;
  
  const resultsHTML = results.map((result, index) => {
    const similarity = result.similarity || 0;
    const percentage = (similarity * 100).toFixed(0);
    const blockText = result.block?.text || 'No text available';
    const parentText = result.block?.parent_text || '';
    
    return `
      <div class="rss-result ${index === 0 ? 'rss-selected' : ''}" data-uid="${result.uid}" data-index="${index}">
        <div class="rss-result-text">${escapeHtml(blockText)}</div>
        ${parentText ? `<div class="rss-result-context">${escapeHtml(parentText)}</div>` : ''}
        <div class="rss-result-similarity">
          <div class="rss-similarity-bar">
            <div class="rss-similarity-fill" style="width: ${percentage}%;"></div>
          </div>
          <span class="rss-similarity-value">${similarity.toFixed(2)}</span>
        </div>
      </div>
    `;
  }).join('');
  
  resultsEl.innerHTML = resultsHTML;
  
  // Add click handlers
  resultsEl.querySelectorAll('.rss-result').forEach(el => {
    el.addEventListener('click', (event) => {
      const uid = el.dataset.uid;
      handleResultClick(uid, event);
    });
  });
}

function handleResultClick(uid, event) {
  if (event.shiftKey) {
    // Open in sidebar
    window.roamAlphaAPI.ui.rightSidebar.addWindow({
      window: { type: 'block', 'block-uid': uid }
    });
  } else {
    // Navigate to block in main view
    window.roamAlphaAPI.ui.mainWindow.openBlock({
      block: { uid: uid }
    });
  }
  closeModal();
}

async function performSearch() {
  const input = document.querySelector('.rss-input');
  if (!input) return;
  
  const query = input.value.trim();
  if (!query) {
    const resultsEl = document.querySelector('.rss-results');
    if (resultsEl) resultsEl.innerHTML = '';
    clearStatus();
    return;
  }
  
  // Cancel previous request
  if (searchState.abortController) {
    searchState.abortController.abort();
  }
  
  // Create new abort controller
  searchState.abortController = new AbortController();
  
  showLoading();
  
  try {
    const response = await searchAPI.search(query, searchState.abortController.signal);
    
    if (response && response.results) {
      renderResults(response.results);
      clearStatus();
      
      if (response.count > 0) {
        const statusEl = document.querySelector('.rss-status');
        if (statusEl) {
          statusEl.innerHTML = `<div class="rss-success">Found ${response.count} results</div>`;
        }
      }
    }
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error('[Semantic Search] Search error:', error);
      showError(error.message.includes('fetch') 
        ? 'Cannot connect to backend. Is it running?'
        : error.message);
      renderResults([]);
    }
  }
}

const debouncedSearch = debounce(performSearch, 300);

// Add CSS styles
function addStyles() {
  // Check if styles already added
  if (document.getElementById('rss-styles')) return;
  
  const styles = `
    <style id="rss-styles">
      .rss-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      
      .rss-backdrop {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
      }
      
      .rss-container {
        position: relative;
        background: var(--bg-color, white);
        border-radius: 8px;
        width: 600px;
        max-height: 80vh;
        display: flex;
        flex-direction: column;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
      }
      
      .rss-header {
        padding: 16px 20px;
        border-bottom: 1px solid var(--border-color, #e5e7eb);
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      
      .rss-title {
        margin: 0;
        font-size: 18px;
        color: var(--text-color, #202020);
      }
      
      .rss-close {
        font-size: 24px;
      }
      
      .rss-search {
        padding: 16px 20px;
        border-bottom: 1px solid var(--border-color, #e5e7eb);
      }
      
      .rss-input {
        width: 100%;
      }
      
      .rss-status {
        padding: 0 20px;
        min-height: 20px;
      }
      
      .rss-loading {
        padding: 8px 0;
        color: #6b7280;
      }
      
      .rss-error {
        padding: 8px 0;
        color: #dc2626;
      }
      
      .rss-success {
        padding: 8px 0;
        color: #059669;
        font-size: 12px;
      }
      
      .rss-results {
        flex: 1;
        overflow-y: auto;
        padding: 16px 20px;
      }
      
      .rss-no-results {
        padding: 20px;
        text-align: center;
        color: #6b7280;
      }
      
      .rss-result {
        padding: 12px;
        margin-bottom: 8px;
        border: 1px solid var(--border-color, #e5e7eb);
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.2s;
      }
      
      .rss-result:hover {
        background-color: var(--hover-bg, #f9fafb);
      }
      
      .rss-result.rss-selected {
        background-color: var(--selected-bg, #eff6ff);
        border-color: var(--selected-border, #3b82f6);
      }
      
      .rss-result-text {
        font-size: 14px;
        margin-bottom: 4px;
        color: var(--text-color, #202020);
      }
      
      .rss-result-context {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 4px;
      }
      
      .rss-result-similarity {
        display: flex;
        align-items: center;
        gap: 8px;
      }
      
      .rss-similarity-bar {
        flex: 1;
        height: 4px;
        background: #e5e7eb;
        border-radius: 2px;
      }
      
      .rss-similarity-fill {
        height: 100%;
        background: #3b82f6;
        border-radius: 2px;
      }
      
      .rss-similarity-value {
        font-size: 11px;
        color: #6b7280;
      }
      
      /* Dark mode support */
      .roam-body-main.bp3-dark .rss-container {
        background: #2f3136;
      }
      
      .roam-body-main.bp3-dark .rss-title,
      .roam-body-main.bp3-dark .rss-result-text {
        color: #dcddde;
      }
      
      .roam-body-main.bp3-dark .rss-header,
      .roam-body-main.bp3-dark .rss-search,
      .roam-body-main.bp3-dark .rss-result {
        border-color: #4a4d52;
      }
      
      .roam-body-main.bp3-dark .rss-result:hover {
        background-color: #393c43;
      }
      
      .roam-body-main.bp3-dark .rss-result.rss-selected {
        background-color: #404449;
        border-color: #5a9fd4;
      }
    </style>
  `;
  
  document.head.insertAdjacentHTML('beforeend', styles);
}

// Settings panel configuration
function createSettingsPanel() {
  return {
    tabTitle: "Semantic Search",
    settings: [
      {
        id: "backend-url",
        name: "Backend URL",
        description: "URL of the semantic search backend service",
        action: {
          type: "input",
          placeholder: "http://localhost:8001",
          onChange: (e) => {
            const newUrl = e.target.value;
            if (newUrl) {
              config.backendURL = newUrl;
              extensionAPI.settings.set("backend-url", newUrl);
              searchAPI = new SearchAPI(newUrl);
              console.log('[Semantic Search] Backend URL updated:', newUrl);
            }
          }
        }
      },
      {
        id: "search-limit",
        name: "Result Limit",
        description: "Maximum number of search results to display",
        action: {
          type: "input",
          placeholder: "20",
          onChange: (e) => {
            const limit = parseInt(e.target.value);
            if (limit > 0 && limit <= 100) {
              config.searchLimit = limit;
              extensionAPI.settings.set("search-limit", limit);
            }
          }
        }
      },
      {
        id: "debounce-delay",
        name: "Search Delay (ms)",
        description: "Delay before searching after typing stops",
        action: {
          type: "input",
          placeholder: "300",
          onChange: (e) => {
            const delay = parseInt(e.target.value);
            if (delay >= 100 && delay <= 1000) {
              config.debounceDelay = delay;
              extensionAPI.settings.set("debounce-delay", delay);
            }
          }
        }
      },
      {
        id: "test-connection",
        name: "Test Connection",
        description: "Test the connection to the backend",
        action: {
          type: "button",
          onClick: async () => {
            try {
              const data = await searchAPI.checkConnection();
              window.roamAlphaAPI.ui.showToast({
                message: `✅ Connected! Graph: ${data.roam_graph_name}, Documents: ${data.chroma_collection_count}`,
                intent: "success"
              });
            } catch (error) {
              window.roamAlphaAPI.ui.showToast({
                message: `❌ Connection failed: ${error.message}`,
                intent: "danger"
              });
            }
          }
        }
      }
    ]
  };
}

// Main extension export following Roam Depot guidelines
export default {
  onload: ({ extensionAPI: api }) => {
    console.log('[Semantic Search] Extension loading...');
    extensionAPI = api;
    
    // Load saved settings
    config.backendURL = extensionAPI.settings.get("backend-url") || DEFAULT_CONFIG.backendURL;
    config.searchLimit = extensionAPI.settings.get("search-limit") || DEFAULT_CONFIG.searchLimit;
    config.debounceDelay = extensionAPI.settings.get("debounce-delay") || DEFAULT_CONFIG.debounceDelay;
    
    // Initialize API client
    searchAPI = new SearchAPI(config.backendURL);
    
    // Create settings panel
    extensionAPI.settings.panel.create(createSettingsPanel());
    
    // Add main search command using extensionAPI
    extensionAPI.ui.commandPalette.addCommand({
      label: 'Semantic Search',
      callback: () => {
        if (searchState.isOpen) {
          closeModal();
        } else {
          createModal();
        }
      }
    });
    
    // Add test command for debugging
    extensionAPI.ui.commandPalette.addCommand({
      label: 'Semantic Search: Test Connection',
      callback: async () => {
        try {
          const data = await searchAPI.checkConnection();
          alert(`✅ Connected to backend!\n\nGraph: ${data.roam_graph_name}\nDocuments: ${data.chroma_collection_count}`);
        } catch (error) {
          alert(`❌ Connection failed!\n\nMake sure the backend is running at ${config.backendURL}\n\nError: ${error.message}`);
        }
      }
    });
    
    console.log('[Semantic Search] Extension loaded successfully!');
  },
  
  onunload: () => {
    console.log('[Semantic Search] Extension unloading...');
    
    // Close modal if open
    if (searchState.isOpen) {
      closeModal();
    }
    
    // Cancel any pending requests
    if (searchState.abortController) {
      searchState.abortController.abort();
    }
    
    // Remove styles
    const styles = document.getElementById('rss-styles');
    if (styles) {
      styles.remove();
    }
    
    // Commands are automatically cleaned up by extensionAPI
    
    // Reset state
    searchState = {
      isOpen: false,
      query: '',
      results: [],
      selectedIndex: 0,
      loading: false,
      error: null,
      abortController: null,
      commands: []
    };
    
    console.log('[Semantic Search] Extension unloaded.');
  }
};