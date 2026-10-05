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

    const variants = Array.isArray(item.variants) ? item.variants : [];
    const pages = Array.isArray(item.referencePages) ? item.referencePages : [];
    const search = normalize(filters.search);
    if (search) {
      const haystack = [
        item.filename,
        item.path,
        item.publicUrl,
        item.show,
        item.venue,
        ...(item.usage || []),
        ...variants.flatMap((variant) => [
          variant.filename,
          variant.path,
          variant.publicUrl,
          variant.variantRole,
          ...(variant.usage || [])
        ]),
        ...pages.flatMap((page) => [page.title, page.url])
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

  function uniqueBy(values, keyFn) {
    const seen = new Set();
    return values.filter((value) => {
      const key = keyFn(value);
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  function groupItems(items) {
    const buckets = new Map();
    items.forEach((item) => {
      const key = item.visualGroupKey || item.path;
      if (!buckets.has(key)) buckets.set(key, []);
      buckets.get(key).push(item);
    });

    return [...buckets.entries()].map(([key, variants]) => {
      variants.sort((a, b) => {
        const score = (value) => value.variantRole === "Hero" ? 0 : value.variantRole === "OG/social" ? 1 : value.referenced ? 2 : 3;
        return score(a) - score(b) || a.filename.localeCompare(b.filename);
      });
      const representative = variants[0];
      const usage = [...new Set(variants.flatMap((item) => item.usage || []))];
      const duplicateHints = [...new Set(variants.flatMap((item) => item.duplicateHints || []))];
      const referenceFiles = [...new Set(variants.flatMap((item) => item.referenceFiles || []))];
      const referencePages = uniqueBy(
        variants.flatMap((item) => item.referencePages || []),
        (page) => page.url
      ).sort((a, b) => String(a.title || "").localeCompare(String(b.title || "")));
      return {
        ...representative,
        visualGroupKey: key,
        variants,
        variantCount: variants.length,
        referenced: variants.some((item) => item.referenced),
        referenceCount: referenceFiles.length,
        referenceOccurrences: variants.reduce((sum, item) => sum + Number(item.referenceOccurrences || 0), 0),
        referenceFiles,
        referencePages,
        usage,
        duplicateHints,
        show: variants.map((item) => item.show).find(Boolean) || null,
        venue: variants.map((item) => item.venue).find(Boolean) || null,
        relatedShowUrl: variants.map((item) => item.relatedShowUrl).find(Boolean) || null,
        relatedVenueUrl: variants.map((item) => item.relatedVenueUrl).find(Boolean) || null
      };
    });
  }

  function attachCopy(button, value) {
    button.addEventListener("click", async () => {
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
    const referenceModal = document.getElementById("reference-modal");
    const referenceModalTitle = document.getElementById("reference-modal-title");
    const referenceModalCount = document.getElementById("reference-modal-count");
    const referenceModalList = document.getElementById("reference-modal-list");
    const referenceModalClose = document.getElementById("reference-modal-close");
    let lastReferenceTrigger = null;

    function makeReferenceLink(page) {
      const link = document.createElement("a");
      link.href = page.url;
      link.target = "_blank";
      link.rel = "noopener";

      const title = document.createElement("strong");
      title.textContent = page.title || page.url;
      link.appendChild(title);

      const path = document.createElement("span");
      path.textContent = page.url;
      link.appendChild(path);
      return link;
    }

    function closeReferenceModal() {
      if (!referenceModal || referenceModal.hidden) return;
      referenceModal.hidden = true;
      document.body.classList.remove("reference-modal-open");
      if (lastReferenceTrigger) {
        lastReferenceTrigger.setAttribute("aria-expanded", "false");
        lastReferenceTrigger.focus({ preventScroll: true });
      }
      lastReferenceTrigger = null;
    }

    function openReferenceModal(item, trigger) {
      if (!referenceModal) return;
      const pages = item.referencePages || [];
      referenceModalTitle.textContent = item.filename || "Referenced pages";
      referenceModalCount.textContent = pages.length + (pages.length === 1 ? " public page" : " public pages");
      referenceModalList.replaceChildren(...pages.map(makeReferenceLink));
      referenceModalList.scrollTop = 0;
      lastReferenceTrigger = trigger || null;
      if (lastReferenceTrigger) lastReferenceTrigger.setAttribute("aria-expanded", "true");
      referenceModal.hidden = false;
      document.body.classList.add("reference-modal-open");
      window.requestAnimationFrame(() => referenceModalClose?.focus({ preventScroll: true }));
    }

    referenceModal?.querySelectorAll("[data-reference-close]").forEach((node) => {
      node.addEventListener("click", closeReferenceModal);
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && referenceModal && !referenceModal.hidden) closeReferenceModal();
    });

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

    const files = payload.images;
    const items = groupItems(files);
    let category = "all";
    let renderLimit = 60;

    const showNames = [...new Set(files.map((item) => item.show).filter(Boolean))].sort((a, b) => a.localeCompare(b));
    const venueNames = [...new Set(files.map((item) => item.venue).filter(Boolean))].sort((a, b) => a.localeCompare(b));

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
      ["Image files", summary.totalImages ?? files.length],
      ["Visual cards", items.length],
      ["Used files", summary.usedImages ?? files.filter((item) => item.referenced).length],
      ["No references", summary.unreferencedImages ?? files.filter((item) => !item.referenced).length],
      ["Exact dup groups", summary.exactDuplicateGroups ?? 0]
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

    function makeVariantRow(variant) {
      const row = document.createElement("div");
      row.className = "variant-row";

      const header = document.createElement("div");
      header.className = "variant-head";
      const name = document.createElement("strong");
      name.textContent = variant.filename;
      header.appendChild(name);
      if (variant.variantRole) {
        const role = document.createElement("span");
        role.className = "variant-role";
        role.textContent = variant.variantRole;
        header.appendChild(role);
      }
      row.appendChild(header);

      const details = document.createElement("div");
      details.className = "variant-details";
      const dimension = variant.width && variant.height ? variant.width + " × " + variant.height : "Dimensions in browser";
      details.textContent = dimension + " · " + String(variant.fileType || "").toUpperCase() + " · " + formatBytes(variant.sizeBytes);
      row.appendChild(details);

      const code = document.createElement("code");
      code.className = "variant-path";
      code.textContent = variant.path;
      row.appendChild(code);

      const actions = document.createElement("div");
      actions.className = "variant-actions";
      const copyUrl = document.createElement("button");
      copyUrl.type = "button";
      copyUrl.textContent = "Copy URL";
      attachCopy(copyUrl, variant.publicUrl);
      actions.appendChild(copyUrl);

      const copyPath = document.createElement("button");
      copyPath.type = "button";
      copyPath.textContent = "Copy path";
      attachCopy(copyPath, variant.path);
      actions.appendChild(copyPath);

      const open = document.createElement("a");
      open.href = variant.publicUrl;
      open.target = "_blank";
      open.rel = "noopener";
      open.textContent = "Open";
      actions.appendChild(open);
      row.appendChild(actions);
      return row;
    }

    function cardFor(item) {
      const card = template.content.firstElementChild.cloneNode(true);
      const thumb = card.querySelector(".thumb");
      const thumbLink = card.querySelector(".thumb-link");
      const thumbFrame = card.querySelector(".thumb-frame");
      const previewFallback = card.querySelector(".preview-fallback");
      const previewErrorBadge = card.querySelector(".preview-error-badge");
      const filename = card.querySelector(".filename");
      const path = card.querySelector(".path");
      const publicUrl = card.querySelector(".public-url");
      const metadata = card.querySelector(".metadata");
      const categoryBadge = card.querySelector(".category-badge");
      const referenceBadge = card.querySelector(".reference-badge");
      const variantCount = card.querySelector(".variant-count");
      const variantList = card.querySelector(".variant-list");
      const usageBadges = card.querySelector(".usage-badges");
      const showRow = card.querySelector(".show-row");
      const showValue = card.querySelector(".show-value");
      const venueRow = card.querySelector(".venue-row");
      const venueValue = card.querySelector(".venue-value");
      const referenceValue = card.querySelector(".reference-value");
      const usedOn = card.querySelector(".used-on");
      const usedOnSummary = card.querySelector(".used-on-summary");
      const duplicateNote = card.querySelector(".duplicate-note");
      const mainActions = card.querySelector(".actions");
      const openImage = card.querySelector(".open-image");
      const openShow = card.querySelector(".open-show");

      card.dataset.path = item.path;
      thumb.alt = item.filename;
      thumbLink.href = item.publicUrl;
      filename.textContent = item.filename;

      const previewCandidates = uniqueBy(
        (item.variants && item.variants.length ? item.variants : [item]).filter((variant) => variant && variant.path),
        (variant) => variant.path
      );
      let previewIndex = 0;

      function loadPreviewCandidate(index) {
        const candidate = previewCandidates[index];
        if (!candidate) return false;
        thumb.src = candidate.path;
        thumbLink.href = candidate.publicUrl || candidate.path;
        return true;
      }

      thumb.addEventListener("error", () => {
        previewIndex += 1;
        if (previewIndex < previewCandidates.length && loadPreviewCandidate(previewIndex)) return;
        thumb.hidden = true;
        previewFallback.hidden = false;
        previewErrorBadge.hidden = false;
        thumbFrame.classList.add("preview-failed");
        thumbLink.href = item.publicUrl;
      });

      loadPreviewCandidate(0);
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

      if (item.variantCount > 1) {
        variantCount.hidden = false;
        variantCount.textContent = item.variantCount + " variants";
        path.hidden = true;
        publicUrl.hidden = true;
        metadata.hidden = true;
        variantList.hidden = false;
        item.variants.forEach((variant) => variantList.appendChild(makeVariantRow(variant)));
        mainActions.querySelectorAll("[data-copy], .open-image").forEach((node) => { node.hidden = true; });
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
        ? item.referenceCount + (item.referenceCount === 1 ? " site file" : " site files")
        : "0 site files";

      const referencePages = item.referencePages || [];
      if (referencePages.length === 1) {
        usedOn.hidden = false;
        const link = makeReferenceLink(referencePages[0]);
        link.classList.add("used-on-direct");
        const title = link.querySelector("strong");
        if (title) title.textContent = "Used on 1 page →";
        usedOnSummary.appendChild(link);
      } else if (referencePages.length > 1) {
        usedOn.hidden = false;
        const button = document.createElement("button");
        button.type = "button";
        button.className = "used-on-trigger";
        button.textContent = "Used on " + referencePages.length + " pages →";
        button.setAttribute("aria-haspopup", "dialog");
        button.setAttribute("aria-expanded", "false");
        button.addEventListener("click", () => openReferenceModal(item, button));
        usedOnSummary.appendChild(button);
      } else if (item.referenced) {
        usedOn.hidden = false;
        const note = document.createElement("div");
        note.className = "used-on-note";
        note.textContent = "Referenced by site assets or runtime files; no public page link detected.";
        usedOnSummary.appendChild(note);
      }

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
        const type = button.dataset.copy;
        const value = type === "url" ? item.publicUrl : type === "path" ? item.path : item.filename;
        attachCopy(button, value);
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

      const matchingFiles = filtered.reduce((sum, item) => sum + item.variantCount, 0);
      count.textContent = "Showing " + visible.length + " of " + filtered.length + " visual assets · " + matchingFiles + " files";
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
    window.VSMediaLibrary = { start, matchesFilters, formatBytes, groupItems };
  }
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { matchesFilters, formatBytes, groupItems };
  }
})();
