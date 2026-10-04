(() => {
  const CATEGORY_LABELS = {
    "product-photos": "Product photos",
    "seating-charts": "Seating charts",
    "venue-photos": "Venue photos",
    "news": "News / Dispatch",
    "good-to-know": "Good to Know",
    "brand-site": "Brand / site assets",
    "other": "Other"
  };

  function normalize(value) {
    return String(value || "").trim().toLowerCase();
  }

  function matchesFilters(item, filters) {
    const category = filters.category || "all";
    if (category !== "all" && item.category !== category) return false;

    const search = normalize(filters.search);
    if (search) {
      const haystack = [
        item.filename,
        item.path,
        item.publicUrl,
        item.show,
        item.venue,
        ...(item.usage || [])
      ].map(normalize).join(" ");
      if (!haystack.includes(search)) return false;
    }

    const show = normalize(filters.show);
    if (show && !normalize(item.show).includes(show)) return false;

    const venue = normalize(filters.venue);
    if (venue && !normalize(item.venue).includes(venue)) return false;

    if (filters.unusedOnly && item.referenced) return false;
    if (filters.duplicatesOnly && !(item.duplicateHints || []).length) return false;
    return true;
  }

  function formatBytes(bytes) {
    const value = Number(bytes || 0);
    if (value < 1024) return value + " B";
    if (value < 1024 * 1024) return (value / 1024).toFixed(value < 10240 ? 1 : 0) + " KB";
    return (value / (1024 * 1024)).toFixed(1) + " MB";
  }

  function formatDate(value) {
    if (!value) return "";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return "Generated " + new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit"
    }).format(date);
  }

  function copyText(value) {
    if (navigator.clipboard?.writeText) return navigator.clipboard.writeText(value);
    const temp = document.createElement("textarea");
    temp.value = value;
    temp.setAttribute("readonly", "");
    temp.style.position = "fixed";
    temp.style.opacity = "0";
    document.body.appendChild(temp);
    temp.select();
    document.execCommand("copy");
    temp.remove();
    return Promise.resolve();
  }

  let started = false;

  async function start() {
    if (started) return;
    started = true;

    const grid = document.getElementById("media-grid");
    const empty = document.getElementById("empty-state");
    const template = document.getElementById("media-card-template");
    const search = document.getElementById("media-search");
    const showFilter = document.getElementById("show-filter");
    const venueFilter = document.getElementById("venue-filter");
    const unusedFilter = document.getElementById("unused-filter");
    const duplicateFilter = document.getElementById("duplicate-filter");
    const loadMore = document.getElementById("load-more");
    const count = document.getElementById("results-count");
    const generatedAt = document.getElementById("generated-at");
    const stats = document.getElementById("media-stats");
    const categoryFilters = document.getElementById("category-filters");
    const reset = document.getElementById("reset-filters");

    let payload;
    try {
      const response = await fetch("/hq/media-library/media-library.json", { cache: "no-store" });
      if (!response.ok) throw new Error("Inventory unavailable");
      payload = await response.json();
      if (!Array.isArray(payload.images)) throw new Error("Invalid inventory");
    } catch (error) {
      grid.innerHTML = '<div class="empty-state">Media inventory is unavailable. The deploy workflow must generate <code>hq/media-library/media-library.json</code>.</div>';
      count.textContent = "Inventory unavailable";
      return;
    }

    const items = payload.images;
    let category = "all";
    let renderLimit = 60;

    const showNames = [...new Set(items.map((item) => item.show).filter(Boolean))].sort((a, b) => a.localeCompare(b));
    const venueNames = [...new Set(items.map((item) => item.venue).filter(Boolean))].sort((a, b) => a.localeCompare(b));

    const fillDatalist = (id, values) => {
      const list = document.getElementById(id);
      const fragment = document.createDocumentFragment();
      values.forEach((value) => {
        const option = document.createElement("option");
        option.value = value;
        fragment.appendChild(option);
      });
      list.replaceChildren(fragment);
    };

    fillDatalist("show-options", showNames);
    fillDatalist("venue-options", venueNames);

    const summary = payload.summary || {};
    const statRows = [
      ["All images", summary.totalImages ?? items.length],
      ["Used on site", summary.usedImages ?? items.filter((item) => item.referenced).length],
      ["No references", summary.unreferencedImages ?? items.filter((item) => !item.referenced).length],
      ["Exact dup groups", summary.exactDuplicateGroups ?? 0],
      ["Format pairs", summary.sameBasenameFormatGroups ?? 0]
    ];
    stats.innerHTML = statRows.map(([label, value]) =>
      '<div class="stat"><div class="number">' + String(value) + '</div><div class="label">' + label + '</div></div>'
    ).join("");
    generatedAt.textContent = formatDate(payload.generatedAt);

    function filters() {
      return {
        category,
        search: search.value,
        show: showFilter.value,
        venue: venueFilter.value,
        unusedOnly: unusedFilter.checked,
        duplicatesOnly: duplicateFilter.checked
      };
    }

    function cardFor(item) {
      const card = template.content.firstElementChild.cloneNode(true);
      const thumb = card.querySelector(".thumb");
      const thumbLink = card.querySelector(".thumb-link");
      const filename = card.querySelector(".filename");
      const path = card.querySelector(".path");
      const publicUrl = card.querySelector(".public-url");
      const metadata = card.querySelector(".metadata");
      const categoryBadge = card.querySelector(".category-badge");
      const referenceBadge = card.querySelector(".reference-badge");
      const usageBadges = card.querySelector(".usage-badges");
      const showRow = card.querySelector(".show-row");
      const showValue = card.querySelector(".show-value");
      const venueRow = card.querySelector(".venue-row");
      const venueValue = card.querySelector(".venue-value");
      const referenceValue = card.querySelector(".reference-value");
      const duplicateNote = card.querySelector(".duplicate-note");
      const openImage = card.querySelector(".open-image");
      const openShow = card.querySelector(".open-show");

      card.dataset.path = item.path;
      thumb.src = item.path;
      thumb.alt = item.filename;
      thumbLink.href = item.publicUrl;
      filename.textContent = item.filename;
      path.textContent = item.path;
      publicUrl.textContent = item.publicUrl;
      categoryBadge.textContent = CATEGORY_LABELS[item.category] || "Other";

      referenceBadge.classList.add(item.referenced ? "used" : "unused");
      referenceBadge.textContent = item.referenced ? "Used on site" : "No current references";

      const dimension = item.width && item.height ? item.width + " × " + item.height : "Dimensions loading";
      metadata.innerHTML =
        '<span class="dimension">' + dimension + '</span>' +
        '<span>' + String(item.fileType || "").toUpperCase() + '</span>' +
        '<span>' + formatBytes(item.sizeBytes) + '</span>';

      if (!item.width || !item.height) {
        thumb.addEventListener("load", () => {
          const target = metadata.querySelector(".dimension");
          if (target && thumb.naturalWidth && thumb.naturalHeight) {
            target.textContent = thumb.naturalWidth + " × " + thumb.naturalHeight;
          }
        }, { once: true });
      }

      (item.usage || []).forEach((label) => {
        const badge = document.createElement("span");
        badge.className = "usage-badge";
        badge.textContent = label;
        usageBadges.appendChild(badge);
      });

      if (item.show) showValue.textContent = item.show;
      else showRow.hidden = true;

      if (item.venue) venueValue.textContent = item.venue;
      else venueRow.hidden = true;

      referenceValue.textContent = item.referenceCount
        ? item.referenceCount + (item.referenceCount === 1 ? " file" : " files")
        : "0 files";

      if ((item.duplicateHints || []).length) {
        duplicateNote.hidden = false;
        duplicateNote.textContent = item.duplicateHints.join(" · ");
      }

      openImage.href = item.publicUrl;
      if (item.relatedShowUrl) {
        openShow.hidden = false;
        openShow.href = item.relatedShowUrl;
      }

      card.querySelectorAll("[data-copy]").forEach((button) => {
        button.addEventListener("click", async () => {
          const type = button.dataset.copy;
          const value = type === "url" ? item.publicUrl : type === "path" ? item.path : item.filename;
          const original = button.textContent;
          try {
            await copyText(value);
            button.textContent = "Copied";
            button.classList.add("copied");
            window.setTimeout(() => {
              button.textContent = original;
              button.classList.remove("copied");
            }, 1200);
          } catch (_) {
            button.textContent = "Copy failed";
            window.setTimeout(() => { button.textContent = original; }, 1200);
          }
        });
      });

      return card;
    }

    function render() {
      const current = filters();
      const filtered = items.filter((item) => matchesFilters(item, current));
      const visible = filtered.slice(0, renderLimit);
      const fragment = document.createDocumentFragment();
      visible.forEach((item) => fragment.appendChild(cardFor(item)));
      grid.replaceChildren(fragment);

      count.textContent = "Showing " + visible.length + " of " + filtered.length + " matching images";
      empty.hidden = filtered.length !== 0;
      loadMore.hidden = visible.length >= filtered.length;
    }

    function resetLimitAndRender() {
      renderLimit = 60;
      render();
    }

    search.addEventListener("input", resetLimitAndRender);
    showFilter.addEventListener("input", resetLimitAndRender);
    venueFilter.addEventListener("input", resetLimitAndRender);
    unusedFilter.addEventListener("change", resetLimitAndRender);
    duplicateFilter.addEventListener("change", resetLimitAndRender);

    categoryFilters.addEventListener("click", (event) => {
      const button = event.target.closest("[data-category]");
      if (!button) return;
      category = button.dataset.category;
      categoryFilters.querySelectorAll("[data-category]").forEach((node) => {
        node.classList.toggle("active", node === button);
      });
      resetLimitAndRender();
    });

    reset.addEventListener("click", () => {
      category = "all";
      search.value = "";
      showFilter.value = "";
      venueFilter.value = "";
      unusedFilter.checked = false;
      duplicateFilter.checked = false;
      categoryFilters.querySelectorAll("[data-category]").forEach((node) => {
        node.classList.toggle("active", node.dataset.category === "all");
      });
      resetLimitAndRender();
    });

    loadMore.addEventListener("click", () => {
      renderLimit += 60;
      render();
    });

    render();
  }

  if (typeof window !== "undefined") {
    window.VSMediaLibrary = { start, matchesFilters, formatBytes };
  }
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { matchesFilters, formatBytes };
  }
})();
