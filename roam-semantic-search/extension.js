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
  searchAlpha: 0.5, // Balance between keyword (0) and semantic (1) search
  useRerank: false, // Toggle for VoyageAI reranking
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

  async search(
    query,
    signal,
    excludePages = false,
    alpha = 0.5,
    rerank = false,
  ) {
    try {
      // URL with alpha parameter for hybrid search balance and reranking option
      const url = `${this.baseURL}/search?q=${encodeURIComponent(query)}&limit=${config.searchLimit}&exclude_pages=${excludePages}&alpha=${alpha}&rerank=${rerank}`;
      console.log("[Semantic Search] API Request:", url, "Rerank:", rerank);
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
            <input type="checkbox" class="rss-hide-pages-toggle" ${searchState.hidePages ? "checked" : ""} />
            <span class="bp3-control-indicator"></span>
            Blocks only
          </label>
          <label class="bp3-control bp3-switch rss-filter-switch">
            <input type="checkbox" class="rss-rerank-toggle" ${searchState.useRerank ? "checked" : ""} />
            <span class="bp3-control-indicator"></span>
            Rerank
          </label>
          <div class="rss-search-type-slider">
            <span class="rss-slider-label">Keyword</span>
            <input type="range" class="rss-alpha-slider"
              min="0" max="1" step="0.1" value="${searchState.searchAlpha}"
              title="${Math.round(searchState.searchAlpha * 100)}%" />
            <span class="rss-slider-label">Semantic</span>
          </div>
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

  // Add toggle listeners
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

  const rerankToggle = modal.querySelector(".rss-rerank-toggle");
  if (rerankToggle) {
    rerankToggle.addEventListener("change", (e) => {
      searchState.useRerank = e.target.checked;
      // Save preference
      if (extensionAPI) {
        extensionAPI.settings.set("use-rerank", searchState.useRerank);
      }
      // Re-run search with new rerank setting
      performSearch();
    });
  }

  // Add alpha slider listener
  const alphaSlider = modal.querySelector(".rss-alpha-slider");
  if (alphaSlider) {
    alphaSlider.addEventListener("input", (e) => {
      searchState.searchAlpha = parseFloat(e.target.value);
      // Update tooltip to show current value
      const percentage = Math.round(searchState.searchAlpha * 100);
      e.target.title = `${percentage}%`;
      // Save preference
      if (extensionAPI) {
        extensionAPI.settings.set("search-alpha", searchState.searchAlpha);
      }
      // Re-run search with new alpha setting
      debouncedSearch();
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
      // Navigate to parent_uid if available, otherwise page_uid, fallback to primary uid
      const navUid = result.parent_uid || result.page_uid || result.uid;
      handleResultClick(navUid, event);
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

// Parse linearized chunk text into individual blocks
function parseLinearizedChunk(text) {
  const lines = text.split("\n");
  const rawBlocks = [];
  let currentBlock = null;

  for (const line of lines) {
    // Check if this line starts a new block (spaces followed by "- ")
    const blockMatch = line.match(/^(\s*)- (.*)$/);

    if (blockMatch) {
      // Save previous block if exists
      if (currentBlock) {
        rawBlocks.push(currentBlock);
      }

      currentBlock = {
        indent: blockMatch[1].length,
        text: blockMatch[2],
      };
    } else if (currentBlock) {
      // This is a continuation line of the current block
      if (line.trim()) {
        // Non-empty continuation line
        currentBlock.text += "\n" + line.trimStart();
      } else {
        // Empty line within a block - preserve it for paragraph breaks
        currentBlock.text += "\n";
      }
    }
  }

  // Don't forget the last block
  if (currentBlock) {
    rawBlocks.push(currentBlock);
  }

  if (rawBlocks.length === 0) {
    return [];
  }

  // Normalize indentation so the first block becomes level 0 even if the
  // snippet started partway through a Roam hierarchy.
  const indentLevels = [...new Set(rawBlocks.map((block) => block.indent))].sort(
    (a, b) => a - b,
  );
  const indentToLevel = new Map(
    indentLevels.map((indent, index) => [indent, index]),
  );

  return rawBlocks.map((block) => ({
    level: indentToLevel.get(block.indent) ?? 0,
    text: block.text,
  }));
}

// Render multi-block chunk with proper hierarchy
function renderMultiBlockChunk(container, chunkText, preParsedBlocks) {
  const blocks = Array.isArray(preParsedBlocks)
    ? preParsedBlocks
    : parseLinearizedChunk(chunkText);

  if (blocks.length === 0) {
    // No blocks found, fallback to simple render
    window.roamAlphaAPI.ui.components.renderString({
      el: container,
      string: chunkText,
    });
    return;
  }

  if (blocks.length === 1 && blocks[0].level === 0) {
    // Single top-level block - use simple render
    window.roamAlphaAPI.ui.components.renderString({
      el: container,
      string: blocks[0].text,
    });
    return;
  }

  // Multiple blocks or nested structure - create hierarchical display
  const blockList = document.createElement("div");
  blockList.className = "rss-block-list";

  blocks.forEach((block) => {
    // Create container for this block
    const blockWrapper = document.createElement("div");
    blockWrapper.className = "rss-block-wrapper";
    blockWrapper.style.marginLeft = `${block.level * 20}px`;

    const blockItem = document.createElement("div");
    blockItem.className = "rss-block-item";
    blockItem.style.display = "flex";
    blockItem.style.alignItems = "flex-start";

    // Add bullet for all blocks
    const bullet = document.createElement("span");
    bullet.className = "rss-block-bullet";
    bullet.textContent = "•";
    bullet.style.marginRight = "8px";
    bullet.style.flexShrink = "0";
    bullet.style.marginTop = "2px";
    bullet.style.color = "#9ca3af";

    // Container for the actual block content
    const blockContent = document.createElement("div");
    blockContent.className = "rss-block-content";
    blockContent.style.flex = "1";

    blockItem.appendChild(bullet);
    blockItem.appendChild(blockContent);
    blockWrapper.appendChild(blockItem);
    blockList.appendChild(blockWrapper);

    // Render the block text with Roam formatting
    try {
      window.roamAlphaAPI.ui.components.renderString({
        el: blockContent,
        string: block.text,
      });
    } catch (e) {
      // Fallback to plain text
      blockContent.textContent = block.text;
    }
  });

  container.appendChild(blockList);
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

  // Sort results by similarity score (highest first)
  const sortedResults = [...results].sort((a, b) => {
    const scoreA = a.similarity || 0;
    const scoreB = b.similarity || 0;
    return scoreB - scoreA; // Descending order
  });

  searchState.results = sortedResults;
  searchState.selectedIndex = 0;
  resultsEl.innerHTML = ""; // Clear previous results

  sortedResults.forEach((result, index) => {
    const similarity = result.similarity || 0;
    const percentage = (similarity * 100).toFixed(0);
    const pageTitle = result.page_title || "Untitled Page";
    const parentText = result.parent_text || "";
    const isPage = result.document_type === "page";

    // Pages don't need breadcrumbs, chunks show their context
    let breadcrumbHtml = "";
    let breadcrumbConfig = null;
    if (!isPage) {
      // Don't show duplicate if parent_text is the same as page_title
      const showParent = parentText && parentText !== pageTitle;
      const breadcrumbId = `rss-breadcrumb-${result.uid}-${index}`;
      const parentMarkup = showParent
        ? '<span class="rss-breadcrumb-separator"> &gt; </span><span class="rss-breadcrumb-parent"></span>'
        : "";
      breadcrumbHtml = `
        <div class="rss-result-breadcrumb" id="${breadcrumbId}">
          <span class="rss-breadcrumb-page"></span>
          ${parentMarkup}
        </div>
      `.trim();
      breadcrumbConfig = {
        id: breadcrumbId,
        page: pageTitle,
        parent: showParent ? parentText : null,
      };
    }

    // The backend now sends pre-formatted text with ^^highlight^^ syntax
    let chunkTextWithHighlights = result.chunk_text_preview || "";

    // For pages, format as [[Page Name]]
    if (isPage) {
      // Remove any existing highlights and add page reference brackets
      const cleanPageName = chunkTextWithHighlights.replace(/\^\^/g, "");
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
        ${escapeHtml(chunkTextWithHighlights.replace(/\^\^/g, ""))}
      </div>
      <div class="rss-result-similarity">
        <div class="rss-similarity-bar">
          <div class="rss-similarity-fill" style="width: ${percentage}%;"></div>
        </div>
        <span class="rss-similarity-value">${percentage}% match${isPage ? " (page)" : ""}</span>
      </div>
    `;

    resultDiv.addEventListener("click", (event) => {
      // Navigate to parent_uid if available, otherwise page_uid, fallback to primary uid
      const navUid = result.parent_uid || result.page_uid || result.uid;
      handleResultClick(navUid, event);
    });

    resultsEl.appendChild(resultDiv);

    if (breadcrumbConfig) {
      const breadcrumbContainer = document.getElementById(breadcrumbConfig.id);
      if (breadcrumbContainer) {
        const pageContainer = breadcrumbContainer.querySelector(
          ".rss-breadcrumb-page",
        );
        if (pageContainer) {
          try {
            pageContainer.innerHTML = "";
            window.roamAlphaAPI.ui.components.renderString({
              el: pageContainer,
              string: breadcrumbConfig.page,
            });
          } catch (e) {
            pageContainer.textContent = breadcrumbConfig.page;
          }
        }

        if (breadcrumbConfig.parent) {
          const parentContainer = breadcrumbContainer.querySelector(
            ".rss-breadcrumb-parent",
          );
          if (parentContainer) {
            try {
              parentContainer.innerHTML = "";
              window.roamAlphaAPI.ui.components.renderString({
                el: parentContainer,
                string: breadcrumbConfig.parent,
              });
            } catch (e) {
              parentContainer.textContent = breadcrumbConfig.parent;
            }
          }
        }
      }
    }

    const chunkContainer = document.getElementById(
      `rss-chunk-${result.uid}-${index}`,
    );
    if (chunkContainer) {
      try {
        // Clear the fallback text before rendering
        chunkContainer.innerHTML = "";

        const parsedBlocks = parseLinearizedChunk(chunkTextWithHighlights);
        const needsHierarchy =
          parsedBlocks.length > 1 ||
          parsedBlocks.some((block) => block.level > 0);

        if (needsHierarchy) {
          // Multi-block chunk - render with normalized hierarchy
          renderMultiBlockChunk(
            chunkContainer,
            chunkTextWithHighlights,
            parsedBlocks,
          );
        } else {
          // Single block or simple text - use standard renderString
          window.roamAlphaAPI.ui.components.renderString({
            el: chunkContainer,
            string: chunkTextWithHighlights,
          });
        }
      } catch (e) {
        console.error("[Semantic Search] renderString failed:", e);
        // Restore fallback text on error
        chunkContainer.innerHTML = escapeHtml(
          chunkTextWithHighlights.replace(/\^\^/g, ""),
        );
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
      searchState.hidePages,
      searchState.searchAlpha,
      searchState.useRerank,
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
        width: 650px;
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
        display: flex;
        align-items: center;
        gap: 16px;
      }
      .rss-filter-switch {
        margin: 0;
        font-size: 13px;
        display: flex;
        align-items: center;
      }
      .rss-search-type-slider {
        display: flex;
        align-items: center;
        font-size: 12px;
        margin-left: auto;
        flex-shrink: 0;
      }
      .rss-alpha-slider {
        width: 80px;
        height: 4px;
        cursor: pointer;
        margin: 0 12px;
        flex-shrink: 0;
      }
      .rss-slider-label {
        color: #9ca3af;
        font-weight: 500;
        font-size: 12px;
        white-space: nowrap;
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

      /* Multi-block chunk styles */
      .rss-block-list {
        padding: 0;
        margin: 0;
      }
      .rss-block-wrapper {
        margin-bottom: 4px;
      }
      .rss-block-item {
        display: flex;
        align-items: flex-start;
        line-height: 1.5;
      }
      .rss-block-bullet {
        color: #9ca3af;
        margin-right: 8px;
        margin-top: 2px;
        flex-shrink: 0;
        font-size: 12px;
      }
      .rss-block-content {
        flex: 1;
        min-width: 0;
        word-wrap: break-word;
      }
      .rss-block-content p {
        margin: 0 0 8px 0;
      }
      .rss-block-content p:last-child {
        margin-bottom: 0;
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
      .roam-body-main.bp3-dark .rss-block-bullet {
        color: #6b7280;
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

    // Load filter preferences
    searchState.hidePages = extensionAPI.settings.get("hide-pages") || false;
    searchState.searchAlpha = extensionAPI.settings.get("search-alpha") || 0.5;
    searchState.useRerank = extensionAPI.settings.get("use-rerank") || false;

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
      searchAlpha: 0.5,
      useRerank: false,
    };

    console.log("[Semantic Search] Extension unloaded.");
  },
};
