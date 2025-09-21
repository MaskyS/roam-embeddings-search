// Roam Semantic Search Extension - Depot Compatible Version
// Follows official Roam Depot extension guidelines

let extensionAPI;
let searchState = {
  isOpen: false,
  query: "",
  results: [],
  selectedIndex: 0,
  loading: false,
  error: null,
  abortController: null,
  commands: [], // Track commands for cleanup
  hidePages: false, // Toggle to filter out page results
};

// Configuration - will be moved to settings panel
const DEFAULT_CONFIG = {
  backendURL: "http://localhost:8002", // Changed to semantic backend port
  searchLimit: 20,
  debounceDelay: 300,
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
      console.error("[Semantic Search] Connection error:", error);
      throw error;
    }
  }

  async search(query, signal, excludePages = false) {
    try {
      // Simplified URL for the new semantic-only backend
      const url = `${this.baseURL}/search?q=${encodeURIComponent(query)}&limit=${config.searchLimit}&exclude_pages=${excludePages}`;
      const response = await fetch(url, { signal });

      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      if (error.name === "AbortError") {
        console.log("[Semantic Search] Request cancelled");
        return null;
      }
      console.error("[Semantic Search] Search error:", error);
      throw error;
    }
  }
}

let searchAPI;

// Helper functions
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text || "";
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
  if (document.getElementById("rss-modal")) {
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
        <div class="rss-filters">
          <label class="bp3-control bp3-switch rss-filter-switch">
            <input type="checkbox" class="rss-hide-pages-toggle" ${searchState.hidePages ? 'checked' : ''} />
            <span class="bp3-control-indicator"></span>
            Blocks only
          </label>
        </div>
        <div class="rss-status"></div>
        <div class="rss-results"></div>
      </div>
    </div>
  `;

  // Add styles
  addStyles();

  document.body.insertAdjacentHTML("beforeend", modalHTML);

  // Get elements
  const modal = document.getElementById("rss-modal");
  const backdrop = modal.querySelector(".rss-backdrop");
  const closeBtn = modal.querySelector(".rss-close");
  const input = modal.querySelector(".rss-input");

  // Event listeners
  backdrop.addEventListener("click", closeModal);
  closeBtn.addEventListener("click", closeModal);
  input.addEventListener("input", debouncedSearch);
  document.addEventListener("keydown", handleKeydown);

  // Add toggle listener
  const toggleCheckbox = modal.querySelector(".rss-hide-pages-toggle");
  if (toggleCheckbox) {
    toggleCheckbox.addEventListener("change", (e) => {
      searchState.hidePages = e.target.checked;
      // Save preference
      if (extensionAPI) {
        extensionAPI.settings.set("hide-pages", searchState.hidePages);
      }
      // Re-run search with new filter setting
      performSearch();
    });
  }

  // Focus input with a small delay to ensure DOM is ready
  setTimeout(() => {
    input.focus();
    input.select(); // Also select any existing text for easy replacement
  }, 400);

  searchState.isOpen = true;
}

function closeModal() {
  // Cancel any pending requests
  if (searchState.abortController) {
    searchState.abortController.abort();
  }

  // Remove event listeners
  document.removeEventListener("keydown", handleKeydown);

  // Clean up rendered blocks before removing modal
  // This is important to prevent memory leaks from Roam's renderBlock
  const resultsEl = document.querySelector(".rss-results");
  if (resultsEl) {
    // Clear all rendered blocks
    resultsEl.innerHTML = "";
  }

  // Remove DOM element
  const modal = document.getElementById("rss-modal");
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

  if (event.key === "Escape") {
    closeModal();
  } else if (event.key === "ArrowDown") {
    event.preventDefault();
    selectNext();
  } else if (event.key === "ArrowUp") {
    event.preventDefault();
    selectPrevious();
  } else if (event.key === "Enter") {
    event.preventDefault();
    if (
      searchState.selectedIndex >= 0 &&
      searchState.results[searchState.selectedIndex]
    ) {
      const result = searchState.results[searchState.selectedIndex];
      handleResultClick(result.uid, event);
    }
  }
}

function selectNext() {
  if (searchState.results.length > 0) {
    searchState.selectedIndex = Math.min(
      searchState.selectedIndex + 1,
      searchState.results.length - 1,
    );
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
  const results = document.querySelectorAll(".rss-result");
  results.forEach((el, index) => {
    if (index === searchState.selectedIndex) {
      el.classList.add("rss-selected");
      // Scroll the selected element into view
      el.scrollIntoView({
        behavior: "smooth",
        block: "nearest",
        inline: "nearest",
      });
    } else {
      el.classList.remove("rss-selected");
    }
  });
}

function showLoading() {
  const statusEl = document.querySelector(".rss-status");
  if (statusEl) {
    statusEl.innerHTML = '<div class="rss-loading">Searching...</div>';
  }
}

function showError(message) {
  const statusEl = document.querySelector(".rss-status");
  if (statusEl) {
    statusEl.innerHTML = `<div class="rss-error">⚠️ ${escapeHtml(message)}</div>`;
  }
}

function clearStatus() {
  const statusEl = document.querySelector(".rss-status");
  if (statusEl) {
    statusEl.innerHTML = "";
  }
}

function renderResults(results) {
  const resultsEl = document.querySelector(".rss-results");
  if (!resultsEl) return;

  if (!results || results.length === 0) {
    resultsEl.innerHTML = searchState.hidePages
      ? '<div class="rss-no-results">No block results found (try disabling "Blocks only" filter)</div>'
      : '<div class="rss-no-results">No results found</div>';
    return;
  }

  searchState.results = results;
  searchState.selectedIndex = 0;
  resultsEl.innerHTML = ""; // Clear previous results

  results.forEach((result, index) => {
    const similarity = result.similarity || 0;
    const percentage = (similarity * 100).toFixed(0);
    const pageTitle = result.page_title || "Untitled Page";
    const parentText = result.parent_text || "";
    const isPage = result.document_type === "page";

    // Pages don't need breadcrumbs, chunks show their context
    let breadcrumbHtml = "";
    if (!isPage) {
      const breadcrumb = parentText ?
        `${escapeHtml(pageTitle)} > ${escapeHtml(parentText)}` :
        escapeHtml(pageTitle);
      breadcrumbHtml = `<div class="rss-result-breadcrumb">${breadcrumb}</div>`;
    }

    // The backend now sends pre-formatted text with ^^highlight^^ syntax
    let chunkTextWithHighlights = result.chunk_text_preview || "";

    // For pages, format as [[Page Name]]
    if (isPage) {
      // Remove any existing highlights and add page reference brackets
      const cleanPageName = chunkTextWithHighlights.replace(/\^\^/g, '');
      chunkTextWithHighlights = `[[${cleanPageName}]]`;
    }

    const resultDiv = document.createElement("div");
    resultDiv.className = `rss-result ${index === 0 ? "rss-selected" : ""} ${isPage ? "rss-page-result" : ""}`;
    resultDiv.dataset.uid = result.uid;
    resultDiv.dataset.index = index;

    resultDiv.innerHTML = `
      ${breadcrumbHtml}
      <div class="rss-chunk-container" id="rss-chunk-${result.uid}-${index}">
        <!-- Fallback content in case renderString fails -->
        ${escapeHtml(chunkTextWithHighlights.replace(/\^\^/g, ''))}
      </div>
      <div class="rss-result-similarity">
        <div class="rss-similarity-bar">
          <div class="rss-similarity-fill" style="width: ${percentage}%;"></div>
        </div>
        <span class="rss-similarity-value">${percentage}% match${isPage ? ' (page)' : ''}</span>
      </div>
    `;

    resultDiv.addEventListener("click", (event) => {
      handleResultClick(result.uid, event);
    });

    resultsEl.appendChild(resultDiv);

    const chunkContainer = document.getElementById(`rss-chunk-${result.uid}-${index}`);
    if (chunkContainer) {
      try {
        // renderString will now handle the ^^highlight^^ syntax automatically
        window.roamAlphaAPI.ui.components.renderString({
          el: chunkContainer,
          string: chunkTextWithHighlights,
        });
      } catch (e) {
        console.error("[Semantic Search] renderString failed:", e);
        // The fallback text is already in the container
      }
    }
  });
  updateSelection();
}

function handleResultClick(uid, event) {
  if (event.shiftKey) {
    // Open in sidebar
    window.roamAlphaAPI.ui.rightSidebar.addWindow({
      window: { type: "block", "block-uid": uid },
    });
  } else {
    // Navigate to block in main view
    window.roamAlphaAPI.ui.mainWindow.openBlock({
      block: { uid: uid },
    });
  }
  closeModal();
}

async function performSearch() {
  const input = document.querySelector(".rss-input");
  if (!input) return;

  const query = input.value.trim();
  if (!query) {
    const resultsEl = document.querySelector(".rss-results");
    if (resultsEl) resultsEl.innerHTML = "";
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
    const response = await searchAPI.search(
      query,
      searchState.abortController.signal,
      searchState.hidePages
    );

    if (response && response.results) {
      renderResults(response.results);
      clearStatus();

      if (response.count > 0) {
        const statusEl = document.querySelector(".rss-status");
        if (statusEl) {
          statusEl.innerHTML = `<div class="rss-success">Found ${response.count} results</div>`;
        }
      }
    }
  } catch (error) {
    if (error.name !== "AbortError") {
      console.error("[Semantic Search] Search error:", error);
      showError(
        error.message.includes("fetch")
          ? "Cannot connect to backend. Is it running?"
          : error.message,
      );
      renderResults([]);
    }
  }
}

const debouncedSearch = debounce(performSearch, 300);

// Add CSS styles
function addStyles() {
  // Check if styles already added
  if (document.getElementById("rss-styles")) return;

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
        overflow: hidden;
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
      .rss-close { font-size: 24px; }
      .rss-search {
        padding: 16px 20px;
      }
      .rss-input { width: 100%; }
      .rss-filters {
        padding: 8px 20px 12px 20px;
        border-bottom: 1px solid var(--border-color, #e5e7eb);
        background: var(--bg-color, white);
        position: relative;
        z-index: 1;
      }
      .rss-filter-switch {
        margin: 0;
        font-size: 13px;
        display: flex;
        align-items: center;
      }
      .rss-status { padding: 0 20px; min-height: 20px; }
      .rss-loading, .rss-error, .rss-success { padding: 8px 0; }
      .rss-error { color: #dc2626; }
      .rss-success { color: #059669; font-size: 12px; }
      .rss-results {
        flex: 1;
        overflow-y: auto;
        padding: 16px 20px;
        max-height: calc(80vh - 200px);
        position: relative;
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
      .rss-result-breadcrumb {
        font-size: 11px;
        color: #6b7280;
        margin-bottom: 8px;
        padding: 4px 6px;
        background: #f3f4f6;
        border-radius: 3px;
        display: inline-block;
      }
      .rss-chunk-container {
        font-size: 14px;
        line-height: 1.5;
        color: var(--text-color, #202020);
      }
      .rss-result-similarity {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 8px;
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
      .roam-body-main.bp3-dark .rss-container { background: #2f3136; }
      .roam-body-main.bp3-dark .rss-title,
      .roam-body-main.bp3-dark .rss-chunk-container { color: #dcddde; }
      .roam-body-main.bp3-dark .rss-header,
      .roam-body-main.bp3-dark .rss-search,
      .roam-body-main.bp3-dark .rss-filters,
      .roam-body-main.bp3-dark .rss-result { border-color: #4a4d52; }
      .roam-body-main.bp3-dark .rss-result:hover { background-color: #393c43; }
      .roam-body-main.bp3-dark .rss-result.rss-selected {
        background-color: #404449;
        border-color: #5a9fd4;
      }
      .roam-body-main.bp3-dark .rss-result-breadcrumb {
        color: #9ca3af;
        background: #374151;
      }
      .roam-body-main.bp3-dark .rss-filters {
        background: #2f3136;
      }
    </style>
  `;

  document.head.insertAdjacentHTML("beforeend", styles);
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
              console.log("[Semantic Search] Backend URL updated:", newUrl);
            }
          },
        },
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
          },
        },
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
          },
        },
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
                message: `✅ Connected! Graph: ${data.roam_graph_name}, Documents: ${data.collection_count}`,
                intent: "success",
              });
            } catch (error) {
              window.roamAlphaAPI.ui.showToast({
                message: `❌ Connection failed: ${error.message}`,
                intent: "danger",
              });
            }
          },
        },
      },
    ],
  };
}

// Main extension export following Roam Depot guidelines
export default {
  onload: ({ extensionAPI: api }) => {
    console.log("[Semantic Search] Extension loading...");
    extensionAPI = api;

    // Load saved settings
    config.backendURL =
      extensionAPI.settings.get("backend-url") || DEFAULT_CONFIG.backendURL;
    config.searchLimit =
      extensionAPI.settings.get("search-limit") || DEFAULT_CONFIG.searchLimit;
    config.debounceDelay =
      extensionAPI.settings.get("debounce-delay") ||
      DEFAULT_CONFIG.debounceDelay;

    // Load filter preference
    searchState.hidePages = extensionAPI.settings.get("hide-pages") || false;

    // Initialize API client
    searchAPI = new SearchAPI(config.backendURL);

    // Create settings panel
    extensionAPI.settings.panel.create(createSettingsPanel());

    // Add main search command using extensionAPI
    extensionAPI.ui.commandPalette.addCommand({
      label: "Semantic Search",
      callback: () => {
        if (searchState.isOpen) {
          closeModal();
        } else {
          createModal();
        }
      },
    });

    // Add test command for debugging
    extensionAPI.ui.commandPalette.addCommand({
      label: "Semantic Search: Test Connection",
      callback: async () => {
        try {
          const data = await searchAPI.checkConnection();
          alert(
            `✅ Connected to backend!\n\nGraph: ${data.roam_graph_name}\nDocuments: ${data.collection_count}`,
          );
        } catch (error) {
          alert(
            `❌ Connection failed!\n\nMake sure the backend is running at ${config.backendURL}\n\nError: ${error.message}`,
          );
        }
      },
    });

    console.log("[Semantic Search] Extension loaded successfully!");
  },

  onunload: () => {
    console.log("[Semantic Search] Extension unloading...");

    // Close modal if open
    if (searchState.isOpen) {
      closeModal();
    }

    // Cancel any pending requests
    if (searchState.abortController) {
      searchState.abortController.abort();
    }

    // Remove styles
    const styles = document.getElementById("rss-styles");
    if (styles) {
      styles.remove();
    }

    // Commands are automatically cleaned up by extensionAPI

    // Reset state
    searchState = {
      isOpen: false,
      query: "",
      results: [],
      selectedIndex: 0,
      loading: false,
      error: null,
      abortController: null,
      commands: [],
      hidePages: false,
    };

    console.log("[Semantic Search] Extension unloaded.");
  },
};
