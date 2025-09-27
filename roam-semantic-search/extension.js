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
  hidePages: true, // Toggle to filter out page results
  searchAlpha: 0.5, // Balance between keyword (0) and semantic (1) search
  useRerank: true, // Toggle for VoyageAI reranking
};

const syncState = {
  pollInterval: null,
  lastStatus: null,
};

function isJobActive(status) {
  const st = status?.status || status?.summary?.status;
  return st === "running" || st === "cancelling";
}

function updateSyncStatusDisplay(status) {
  const container = document.querySelector('.rss-sync-status-setting');
  if (!container) return;
  const input = container.querySelector('input');
  if (!input) return;
  const message = renderSyncStatusMessage(status || { status: "idle" });
  input.value = message;
  input.setAttribute("readonly", "readonly");
  input.classList.add("rss-sync-status-input");
  const description = container.querySelector('.rm-settings-panel__description');
  if (description) {
    description.textContent = message;
  }
}

// Configuration - will be moved to settings panel
const DEFAULT_CONFIG = {
  backendURL: "http://localhost:8002", // Changed to semantic backend port
  searchLimit: 20,
  debounceDelay: 300,
  syncLimit: 50,
};

let config = { ...DEFAULT_CONFIG };

// API Client
class SearchAPI {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async checkConnection() {
    try {
      return await this.request("/");
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

  async startSync(body) {
    return await this.request("/sync/start", {
      method: "POST",
      body: JSON.stringify(body || {}),
    });
  }

  async getSyncStatus() {
    return await this.request("/sync/status");
  }

  async cancelSync() {
    return await this.request("/sync/cancel", {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  async clearDatabase() {
    return await this.request("/sync/clear", {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  async request(path, options = {}) {
    const url = path.startsWith("http") ? path : `${this.baseURL}${path}`;
    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };

    const response = await fetch(url, { ...options, headers });
    const text = await response.text();

    if (!response.ok) {
      let detail = text || response.statusText;
      try {
        const parsed = JSON.parse(text);
        if (parsed && typeof parsed === "object") {
          detail = parsed.detail || parsed.message || detail;
        }
      } catch (err) {
        // swallow JSON parse errors
      }
      throw new Error(detail);
    }

    if (!text) {
      return null;
    }

    try {
      return JSON.parse(text);
    } catch (err) {
      return text;
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

function showToast(message, intent = "primary") {
  if (extensionAPI && extensionAPI.ui && typeof extensionAPI.ui.showToast === "function") {
    extensionAPI.ui.showToast({ message, intent });
    return;
  }
  if (window.roamAlphaAPI && window.roamAlphaAPI.ui && typeof window.roamAlphaAPI.ui.showToast === "function") {
    window.roamAlphaAPI.ui.showToast({ message, intent });
    return;
  }
  window.alert(message);
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
          <div class="rss-filters-group">
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
          </div>
          <div class="rss-search-type">
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

    const accentIntensity = Math.max(0, Math.min(similarity, 1));
    const accentAlpha = Math.max(0.18, Math.min(0.45, 0.2 + accentIntensity * 0.4));
    const baseColor = "59, 130, 246";
    const accentColor = `rgba(${baseColor}, ${accentAlpha.toFixed(2)})`;
    resultDiv.style.setProperty("--rss-accent-color", accentColor);

    let headerHtml = "";
    const chipText = `${percentage}% Match`;
    const scoreChip = `<span class="rss-score-chip">${chipText}</span>`;
    const chunkFallback = escapeHtml(chunkTextWithHighlights.replace(/\^\^/g, ""));

    let pageTextId = null;

    if (isPage) {
      pageTextId = `rss-page-text-${result.uid}-${index}`;
      resultDiv.innerHTML = `
        <div class="rss-page-line">
          <span class="rss-page-text" id="${pageTextId}">${chunkFallback}</span>
          ${scoreChip}
        </div>
      `;
    } else {
      if (breadcrumbHtml) {
        headerHtml = `<div class="rss-result-header">${breadcrumbHtml}${scoreChip}</div>`;
      } else {
        headerHtml = `<div class="rss-result-header">${scoreChip}<span class="rss-header-label">Match</span></div>`;
      }

      resultDiv.innerHTML = `
        ${headerHtml}
        <div class="rss-chunk-container" id="rss-chunk-${result.uid}-${index}">
          <!-- Fallback content in case renderString fails -->
          ${chunkFallback}
        </div>
      `;
    }

    resultDiv.addEventListener("click", (event) => {
      // Navigate to parent_uid if available, otherwise page_uid, fallback to primary uid
      const navUid = result.parent_uid || result.page_uid || result.uid;
      handleResultClick(navUid, event);
    });

    resultsEl.appendChild(resultDiv);

    if (isPage && pageTextId) {
      const pageTextEl = resultDiv.querySelector(`#${pageTextId}`);
      if (pageTextEl) {
        try {
          pageTextEl.innerHTML = "";
          window.roamAlphaAPI.ui.components.renderString({
            el: pageTextEl,
            string: chunkTextWithHighlights,
          });
        } catch (e) {
          console.error("[Semantic Search] renderString failed for page result:", e);
          pageTextEl.textContent = chunkTextWithHighlights.replace(/\^\^/g, "");
        }
      }
    }

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

    if (!isPage) {
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

function stopSyncPolling() {
  if (syncState.pollInterval) {
    clearInterval(syncState.pollInterval);
    syncState.pollInterval = null;
  }
}

function startSyncPolling() {
  if (syncState.pollInterval) {
    return;
  }
  syncState.pollInterval = setInterval(() => {
    fetchAndNotifyStatus(false).catch((error) =>
      console.error("[Semantic Search] Sync status polling error", error),
    );
  }, 5000);
}

function renderSyncStatusMessage(status) {
  const jobStatus = status?.status || status?.summary?.status || "idle";
  const parts = [`Sync status: ${jobStatus}`];
  if (status?.mode) {
    parts.push(`mode: ${status.mode}`);
  }

  const summary = status?.summary || {};
  const stats = summary.stats || {};
  const params = status?.params || {};
  const progress = status?.progress || summary.progress || {};

  const totalPages = summary.total_pages ?? summary.total_target_pages ?? progress.total;
  if (typeof progress.processed === "number" && typeof progress.total === "number") {
    parts.push(`processed: ${progress.processed}/${progress.total}`);
    if (typeof progress.percent === "number") {
      parts.push(`progress: ${progress.percent.toFixed(1)}%`);
    }
  } else if (typeof totalPages === "number") {
    parts.push(`total pages: ${totalPages}`);
  }

  if (stats) {
    const docs = stats.documents_added ?? stats.docs ?? 0;
    const updated = stats.pages_updated ?? 0;
    const skipped = stats.pages_skipped ?? 0;
    const failed = stats.pages_failed ?? 0;
    parts.push(`docs: ${docs}, updated: ${updated}, skipped: ${skipped}, failed: ${failed}`);
  }

  if (typeof summary.elapsed_seconds === "number") {
    parts.push(`elapsed: ${summary.elapsed_seconds.toFixed(2)}s`);
  }

  if (summary.started_at) {
    parts.push(`started: ${summary.started_at}`);
  }

  if (params.since) {
    parts.push(`since: ${params.since}`);
  }
  if (params.limit) {
    parts.push(`limit: ${params.limit}`);
  }

  const failures = (summary.failures || status?.failures || []).filter(Boolean);
  if (failures.length) {
    const latest = failures.slice(-2).join("; ");
    parts.push(`failures: ${latest}`);
  }

  if (summary.error || status?.error) {
    parts.push(`error: ${summary.error || status.error}`);
  }
  return parts.join(" | ");
}

function showSyncToast(status, intentOverride) {
  const jobStatus = status?.status || status?.summary?.status || "idle";
  let intent = intentOverride;
  if (!intent) {
    if (jobStatus === "success") {
      intent = "success";
    } else if (jobStatus === "failed") {
      intent = "danger";
    } else if (jobStatus === "cancelled") {
      intent = "warning";
    } else {
      intent = "primary";
    }
  }
  showToast(renderSyncStatusMessage(status), intent);
}

async function fetchAndNotifyStatus(showToast = false) {
  try {
    const status = await searchAPI.getSyncStatus();
    syncState.lastStatus = status;
    updateSyncStatusDisplay(status);

    const jobStatus = status?.status || status?.summary?.status || "idle";
    const isActive = { running: true, cancelling: true }.hasOwnProperty(jobStatus);
    if (showToast) {
      showSyncToast(status);
    }

    if (!isActive) {
      const shouldNotify = showToast || syncState.pollInterval !== null;
      stopSyncPolling();
      if (shouldNotify) {
        showSyncToast(status);
      }
    }

    return status;
  } catch (error) {
    stopSyncPolling();
    showToast(`Sync status error: ${error.message}`, "danger");
    throw error;
  }
}

async function triggerSyncStart(params) {
  if (isJobActive(syncState.lastStatus)) {
    showToast("A sync job is already running", "warning");
    return;
  }
  try {
    const response = await searchAPI.startSync(params);
    syncState.lastStatus = response;
    const modeLabel = params?.mode || "full";
    showToast(`Sync started (${modeLabel})`, "primary");
    startSyncPolling();
    updateSyncStatusDisplay(response);
  } catch (error) {
    showToast(`Sync start failed: ${error.message}`, "danger");
    throw error;
  }
}

async function triggerSyncCancel() {
  if (!isJobActive(syncState.lastStatus)) {
    showToast("No running sync to cancel", "warning");
    return;
  }
  try {
    const response = await searchAPI.cancelSync();
    syncState.lastStatus = response;
    showToast("Cancel requested", "warning");
    startSyncPolling();
    updateSyncStatusDisplay(response);
  } catch (error) {
    showToast(`Cancel failed: ${error.message}`, "danger");
    throw error;
  }
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
      .rss-search .rss-input { width: 100%; }
      .rss-filters {
        padding: 6px 20px;
        background: rgba(148, 163, 184, 0.08);
        border-bottom: 1px solid rgba(148, 163, 184, 0.25);
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 12px;
        border-radius: 4px;
        margin: 0 20px;
      }
      .rss-filters-group {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
      }
      .rss-filter-switch {
        margin: 0;
        font-size: 11px;
        display: flex;
        align-items: center;
        color: #9aa5b6;
        gap: 5px;
      }
      .rss-filter-switch input[type="checkbox"] {
        accent-color: rgba(148, 163, 184, 0.45);
        width: 13px;
        height: 13px;
      }
      .rss-filter-switch .bp3-control-indicator {
        background-color: rgba(148, 163, 184, 0.1);
        border: 1px solid rgba(148, 163, 184, 0.4);
        box-shadow: none;
        transition: background-color 0.2s ease, border-color 0.2s ease;
      }
      .rss-filter-switch .bp3-control-indicator::before {
        background: rgba(71, 85, 105, 0.8);
        box-shadow: none;
      }
      .rss-filter-switch input:checked ~ .bp3-control-indicator {
        background-color: rgba(59, 130, 246, 0.22);
        border-color: rgba(59, 130, 246, 0.35);
      }
      .rss-filter-switch input:checked ~ .bp3-control-indicator::before {
        background: rgba(59, 130, 246, 0.95);
      }
      .rss-search-type {
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 6px;
        color: #9aa5b6;
        font-size: 11px;
      }
      .rss-alpha-slider {
        width: 80px;
        height: 3px;
        cursor: pointer;
        margin: 0;
        flex-shrink: 0;
        background: rgba(59, 130, 246, 0.18);
        border-radius: 999px;
      }
      .rss-alpha-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: rgba(59, 130, 246, 0.85);
        border: 1px solid rgba(59, 130, 246, 0.45);
      }
      .rss-alpha-slider::-moz-range-thumb {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: rgba(59, 130, 246, 0.85);
        border: 1px solid rgba(59, 130, 246, 0.45);
      }
      .rss-slider-label {
        color: #a8b4c4;
        font-weight: 500;
        font-size: 11px;
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
        border-left: 3px solid var(--rss-accent-color, rgba(59, 130, 246, 0.25));
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.2s, border-color 0.2s;
      }
      .rss-result:hover {
        background-color: var(--hover-bg, #f9fafb);
        border-left-color: var(--rss-accent-color, rgba(59, 130, 246, 0.45));
      }
      .rss-result.rss-selected {
        background-color: var(--selected-bg, #eff6ff);
        border-color: var(--selected-border, #3b82f6);
        border-left-color: var(--rss-accent-color, rgba(59, 130, 246, 0.55));
      }
      .rss-result.rss-page-result {
        padding: 10px;
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
      .rss-result-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
        min-height: 18px;
      }
      .rss-score-chip {
        font-size: 9px;
        font-weight: 500;
        color: #6b7280;
        padding: 0 4px;
        margin-left: 0;
        white-space: nowrap;
      }
      .rss-result-header .rss-result-breadcrumb {
        margin-bottom: 0;
      }
      .rss-header-label {
        font-size: 11px;
        color: #6b7280;
      }
      .rss-page-line {
        display: flex;
        align-items: baseline;
        gap: 6px;
        font-size: 15px;
        font-weight: 600;
        color: var(--text-color, #202020);
      }
      .rss-page-text {
        display: inline-block;
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
        color: #d1d5db;
        background: #374151;
      }
      .roam-body-main.bp3-dark .rss-score-chip {
        color: #d1d5db;
        border-color: rgba(148, 163, 184, 0.45);
      }
      .roam-body-main.bp3-dark .rss-result {
        border-left-color: var(--rss-accent-color, rgba(59, 130, 246, 0.4));
      }
      .roam-body-main.bp3-dark .rss-filters {
        background: rgba(55, 65, 81, 0.35);
        border-bottom-color: rgba(55, 65, 81, 0.55);
      }
      .roam-body-main.bp3-dark .rss-block-bullet {
        color: #6b7280;
      }
      .roam-body-main.bp3-dark .rss-page-line {
        color: #dcddde;
      }
      .rss-alpha-slider {
        width: 80px !important;
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
        id: "sync-status",
        name: "Current Sync Status",
        description: "Idle",
        className: "rss-sync-status-setting",
        action: {
          type: "input",
          placeholder: "Idle",
          onChange: () => {},
        },
      },
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
        id: "sync-limit",
        name: "Sync Test Page Limit",
        description: "Used when running limited sync",
        action: {
          type: "input",
          placeholder: `${config.syncLimit}`,
          onChange: (e) => {
            const value = parseInt(e.target.value, 10);
            if (Number.isInteger(value) && value > 0) {
              config.syncLimit = value;
              extensionAPI.settings.set("sync-limit", value);
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
          label: "Test Connection",
          content: "Test Connection",
          onClick: async () => {
            try {
              const data = await searchAPI.checkConnection();
              showToast(
                `✅ Connected! Graph: ${data.roam_graph_name}, Documents: ${data.collection_count}`,
                "success",
              );
            } catch (error) {
              showToast(`❌ Connection failed: ${error.message}`, "danger");
            }
          },
        },
      },
      {
        id: "sync-recent",
        name: "Sync Recently Edited Pages",
        description: "Uses the last successful run's edit time when available.",
        action: {
          type: "button",
          label: "Sync Recently Edited Pages",
          content: "Sync Recently Edited Pages",
          onClick: async () => {
            try {
              await triggerSyncStart({ mode: "since" });
            } catch (error) {
              console.error("[Semantic Search] Sync since failed", error);
            }
          },
        },
      },
      {
        id: "sync-full",
        name: "Full Sync (All Pages)",
        description: "Runs a complete sync of the graph.",
        action: {
          type: "button",
          label: "Full Sync",
          content: "Full Sync",
          onClick: async () => {
            const confirmed = window.confirm(
              "Run a full sync? This may take a long time on large graphs.",
            );
            if (!confirmed) return;
            try {
              await triggerSyncStart({ mode: "full" });
            } catch (error) {
              console.error("[Semantic Search] Full sync failed", error);
            }
          },
        },
      },
      {
        id: "clear-database",
        name: "Clear Semantic Database",
        description:
          "Deletes all objects from Weaviate. Run a sync afterwards to repopulate.",
        action: {
          type: "button",
          label: "Clear Database",
          content: "Clear Database",
          onClick: async () => {
            const confirmed = window.confirm(
              "This will permanently delete all synced data. Continue?",
            );
            if (!confirmed) return;
            try {
              await searchAPI.clearDatabase();
              showToast(
                "Semantic database cleared. Run a sync to repopulate.",
                "warning",
              );
              await fetchAndNotifyStatus(true);
            } catch (error) {
              console.error("[Semantic Search] Clear database failed", error);
              showToast(`Clear database failed: ${error.message}`, "danger");
            }
          },
        },
      },
      {
        id: "sync-limited",
        name: "Sync Limited Pages",
        description: "Runs a limited sync using the configured page count.",
        action: {
          type: "button",
          label: "Sync Limited Pages",
          content: "Sync Limited Pages",
          onClick: async () => {
            try {
              await triggerSyncStart({ mode: "limit", limit: config.syncLimit });
            } catch (error) {
              console.error("[Semantic Search] Limited sync failed", error);
            }
          },
        },
      },
      {
        id: "sync-cancel",
        name: "Cancel Sync",
        description: "Request cancellation of the running sync job.",
        action: {
          type: "button",
          label: "Cancel Sync",
          content: "Cancel Sync",
          onClick: async () => {
            try {
              await triggerSyncCancel();
            } catch (error) {
              console.error("[Semantic Search] Cancel sync failed", error);
            }
          },
        },
      },
      {
        id: "sync-status-refresh",
        name: "Refresh Sync Status",
        description: "Fetch the current sync job status and display it.",
        action: {
          type: "button",
          label: "Refresh Sync Status",
          content: "Refresh Sync Status",
          onClick: async () => {
            try {
              await fetchAndNotifyStatus(true);
            } catch (error) {
              console.error("[Semantic Search] Refresh status failed", error);
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
    config.syncLimit =
      extensionAPI.settings.get("sync-limit") || DEFAULT_CONFIG.syncLimit;

    // Load filter preferences
    const hidePagesSetting = extensionAPI.settings.get("hide-pages");
    const hidePagesUnset = hidePagesSetting === undefined || hidePagesSetting === null;
    searchState.hidePages = hidePagesUnset ? true : hidePagesSetting;
    if (hidePagesUnset) {
      extensionAPI.settings.set("hide-pages", searchState.hidePages);
    }
    const alphaSetting = extensionAPI.settings.get("search-alpha");
    const alphaUnset = alphaSetting === undefined || alphaSetting === null;
    searchState.searchAlpha = alphaUnset ? 0.5 : alphaSetting;
    if (alphaUnset) {
      extensionAPI.settings.set("search-alpha", searchState.searchAlpha);
    }
    const rerankSetting = extensionAPI.settings.get("use-rerank");
    const rerankUnset = rerankSetting === undefined || rerankSetting === null;
    searchState.useRerank = rerankUnset ? true : rerankSetting;
    if (rerankUnset) {
      extensionAPI.settings.set("use-rerank", searchState.useRerank);
    }

    // Initialize API client
    searchAPI = new SearchAPI(config.backendURL);

    // Create settings panel
    extensionAPI.settings.panel.create(createSettingsPanel());
    setTimeout(() => updateSyncStatusDisplay(syncState.lastStatus), 100);

    // Resume polling if a job is already running
    fetchAndNotifyStatus(false)
      .then((status) => {
        const jobStatus = status?.status || status?.summary?.status;
        if (jobStatus === "running" || jobStatus === "cancelling") {
          startSyncPolling();
        }
      })
      .catch(() => {
        // ignore initial status errors
      });

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

    stopSyncPolling();

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
