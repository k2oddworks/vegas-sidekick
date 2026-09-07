/* ------------------------------------------------------------------
   Vegas Sidekick — rotating show cards
   ------------------------------------------------------------------
   Fills any grid marked with data-vs-picks using live records from
   window.VS_SHOWS (components/search-data.js), reshuffled on every load.

   It never invents markup. It clones the grid's FIRST existing card and
   rewrites the fields it recognises, so it automatically matches whatever
   card variant that page happens to use — and the cards already in the
   HTML stay as the no-JS fallback.

   Usage:
     <div class="also-grid" data-vs-picks='{"count":3,"preferCat":"auto"}'>
       ...one or more real cards, which double as the template...
     </div>

   Options (all optional):
     count        how many cards to render            default 3
     exclude      "auto" (this page) or a /shows/... path
     preferCat    "auto" (this page's category), or "magic" etc.
                  Same-category shows sort first, then everything else.
     cat          hard filter to one category
     excludeVenue lowercase substring; drops shows whose venue matches
   ------------------------------------------------------------------ */
(function () {
  "use strict";

  /* Homepage is the last legacy page with its own inline nav. Replace that
     chrome with the shared site header so / matches every interior page. */
  function installSharedHomepageHeader() {
    if (location.pathname !== "/" || document.getElementById("vs-header")) return;

    var legacy = [
      document.querySelector(".announce"),
      document.querySelector("header.site"),
      document.getElementById("scrim"),
      document.getElementById("drawer")
    ];
    legacy.forEach(function (el) { if (el && el.parentNode) el.parentNode.removeChild(el); });

    var mount = document.createElement("div");
    mount.id = "vs-header";

    var spacer = document.createElement("div");
    spacer.id = "vs-home-header-spacer";

    var progress = document.getElementById("progress-bar");
    if (progress && progress.parentNode) {
      progress.parentNode.insertBefore(mount, progress.nextSibling);
      progress.parentNode.insertBefore(spacer, mount.nextSibling);
    } else {
      document.body.insertBefore(spacer, document.body.firstChild);
      document.body.insertBefore(mount, spacer);
    }

    var style = document.createElement("style");
    style.textContent = "#vs-home-header-spacer{height:88px}@media(max-width:980px){#vs-home-header-spacer{height:54px}}";
    document.head.appendChild(style);

    var s = document.createElement("script");
    s.src = "/components/header.js?v=14";
    document.body.appendChild(s);
  }

  installSharedHomepageHeader();

  var CAT_COLOR = {
    comedy: "#ff2e7e", magic: "#7c3aed", cirque: "#0fb5c9", music: "#3b82f6",
    adult: "#c6f22e", family: "#0fb5c9", spectaculars: "#0fb5c9"
  };
  var CAT_LABEL = {
    comedy: "Comedy", magic: "Magic", cirque: "Cirque", music: "Music",
    adult: "Adult", family: "Family", spectaculars: "Spectaculars"
  };

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function catOf(url) {
    var m = /^\/shows\/([^\/]+)\//.exec(url || "");
    return m ? m[1] : "";
  }

  function here() {
    var c = document.querySelector('link[rel="canonical"]');
    var p = c ? c.getAttribute("href") : location.pathname;
    return (p || "").replace(/^https?:\/\/[^\/]+/, "");
  }

  function setTxt(node, sel, val) {
    if (val == null) return;
    var e = node.querySelector(sel);
    if (e) e.textContent = val;
  }

  /* Price: keep the card's own wrapper and prefix, swap only the figure. */
  function setPrice(node, s) {
    var e = node.querySelector(".also-price, .sc-price, .pr, .c-price, .price");
    if (!e || !s.pd) return;
    var b = e.querySelector("b, strong");
    if (b) { b.textContent = s.pd; return; }
    if (/\$\s*[\d,]+/.test(e.textContent)) {
      e.textContent = e.textContent.replace(/\$\s*[\d,]+/, s.pd);
    } else {
      e.textContent = "From " + s.pd;
    }
  }

  /* CTA: only rewrite the "See <Show Name> →" style; leave generic labels. */
  function setCta(node, s) {
    var e = node.querySelector("a.also-cta, .also-cta, a.sc-cta, .sc-cta, .cta, .c-cta, .also-btn");
    if (!e) return;
    if (e.tagName === "A" && e.getAttribute("href")) e.setAttribute("href", s.url);
    if (/^\s*See\s+.+/i.test(e.textContent) && !/^\s*See\s+(show|details|tickets)\s*/i.test(e.textContent)) {
      e.textContent = "See " + s.name + " →";
    }
  }

  function apply(node, s) {
    if (node.tagName === "A") node.setAttribute("href", s.url);

    var src = node.querySelector("source");
    if (src && src.parentNode) src.parentNode.removeChild(src);
    var img = node.querySelector("img");
    if (img) {
      img.removeAttribute("srcset");
      img.setAttribute("src", s.img);
      img.setAttribute("alt", s.name + " — Las Vegas show");
      img.setAttribute("loading", "lazy");
    }

    var cat = catOf(s.url);
    var badge = node.querySelector(".also-cat, .sc-cat, .chip");
    if (badge) {
      badge.textContent = s.cat || CAT_LABEL[cat] || "";
      if (badge.style && CAT_COLOR[cat] && badge.getAttribute("style")) {
        badge.style.background = CAT_COLOR[cat];
      }
    }

    setTxt(node, ".also-title, .also-name, .nm", s.name);
    if (!node.querySelector(".also-title, .also-name, .nm")) setTxt(node, "h3", s.name);
    setTxt(node, ".also-venue, .sc-venue, .vn", s.venue || "");
    setTxt(node, ".de, .sc-sub", s.sub || s.venue || "");
    setPrice(node, s);
    setCta(node, s);
  }

  function choose(o) {
    var all = (window.VS_SHOWS || []).filter(function (s) {
      return s && s.url && s.name && s.img;
    });
    if (o.exclude) all = all.filter(function (s) { return s.url !== o.exclude; });
    if (o.excludeVenue) {
      var keys = [].concat(o.excludeVenue);
      all = all.filter(function (s) {
        var v = (s.venue || "").toLowerCase();
        for (var i = 0; i < keys.length; i++) if (v.indexOf(keys[i]) !== -1) return false;
        return true;
      });
    }
    if (o.cat) all = all.filter(function (s) { return catOf(s.url) === o.cat; });
    shuffle(all);
    if (o.preferCat) {
      var same = [], rest = [];
      all.forEach(function (s) { (catOf(s.url) === o.preferCat ? same : rest).push(s); });
      all = same.concat(rest);
    }
    return all.slice(0, o.count || 3);
  }

  function fill(grid) {
    var o = {};
    try { o = JSON.parse(grid.getAttribute("data-vs-picks") || "{}"); } catch (e) { o = {}; }

    var self = here();
    if (o.exclude === "auto") o.exclude = self;
    if (o.preferCat === "auto") o.preferCat = catOf(self);

    var tpl = grid.firstElementChild;
    if (!tpl) return;

    var picks = choose(o);
    if (picks.length < (o.count || 3)) return;

    var frag = document.createDocumentFragment();
    picks.forEach(function (s) {
      var node = tpl.cloneNode(true);
      apply(node, s);
      frag.appendChild(node);
    });
    grid.innerHTML = "";
    grid.appendChild(frag);
  }

  function run() {
    if (!window.VS_SHOWS || !window.VS_SHOWS.length) return;
    var grids = document.querySelectorAll("[data-vs-picks]");
    for (var i = 0; i < grids.length; i++) {
      try { fill(grids[i]); } catch (e) { /* leave the static cards in place */ }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
