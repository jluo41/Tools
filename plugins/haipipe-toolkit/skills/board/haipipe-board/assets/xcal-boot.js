/* Injected by serve.py into the proxied Excalidraw app (QA4a).
 *
 * WHY THIS EXISTS
 * The open-source app has no "save to a server": it loads a scene from `#url=`
 * and saves to the browser. That is two failures at once (JL 260726): what you
 * draw never reaches `fig/board.excalidraw`, and opening another page's frame
 * shows a "Replace my content" dialog that throws the drawing away.
 *
 * Both come from the same place, the browser's localStorage, so this script
 * takes that over:
 *     read  : the app is handed an IN-MEMORY localStorage, seeded from the file
 *     write : in the one editing tab, the real localStorage is watched and
 *             pushed back to the file
 * With no `#url=` there is no external scene to confirm, so the dialog is gone.
 *
 * WHY READ AND WRITE ARE DIFFERENT MODES
 * A board page carries ONE iframe per page and they all share one origin, so
 * every embedded editor would write the same localStorage key and then read
 * each other's drawing back as its own. An embed is therefore view-only and
 * persists nothing; editing happens in the tab opened by "✏️ Edit", and a lock
 * keeps that to one tab at a time. The FILE is what they share, which is what
 * makes one excalidraw per board work at all.
 */
(function () {
  // The app's own module script was held back by the proxy so that seeding can
  // finish first: localStorage is synchronous, but IndexedDB (where the IMAGES
  // live) is not, and an app that boots mid-seed renders grey placeholders.
  function start() {
    if (!window.__haipipeApp) return;
    var s = document.createElement("script");
    s.type = "module"; s.crossOrigin = "anonymous"; s.src = window.__haipipeApp;
    document.head.appendChild(s);
    window.__haipipeApp = null;
  }

  /* Excalidraw keeps pasted images in IndexedDB `files-db` / `files-store`,
   * keyed by the element's fileId, NOT in localStorage. So the scene's bytes
   * have to be put there before the app looks, and read back out on save. */
  function idb(mode, fn) {
    return new Promise(function (res) {
      var req;
      try { req = indexedDB.open("files-db"); } catch (e) { return res(null); }
      req.onupgradeneeded = function () {
        try { req.result.createObjectStore("files-store"); } catch (e) {}
      };
      req.onerror = function () { res(null); };
      req.onsuccess = function () {
        var db = req.result, out = null;
        if (!db.objectStoreNames.contains("files-store")) { db.close(); return res(null); }
        var tx;
        try { tx = db.transaction("files-store", mode); } catch (e) { db.close(); return res(null); }
        try { out = fn(tx.objectStore("files-store")); } catch (e) {}
        tx.oncomplete = function () { db.close(); res(out); };
        tx.onerror = tx.onabort = function () { db.close(); res(null); };
      };
    });
  }
  function put_files(files) {
    var ids = Object.keys(files || {});
    if (!ids.length) return Promise.resolve(0);
    return idb("readwrite", function (store) {
      ids.forEach(function (id) { store.put(files[id], id); });
      return ids.length;
    });
  }
  function get_files(ids) {
    if (!ids.length) return Promise.resolve({});
    return idb("readonly", function (store) {
      var out = {};
      ids.forEach(function (id) {
        var r = store.get(id);
        r.onsuccess = function () { if (r.result) out[id] = r.result; };
      });
      return out;
    }).then(function (o) { return o || {}; });
  }
  function image_ids(els) {
    var seen = {};
    els.forEach(function (e) { if (e.type === "image" && e.fileId) seen[e.fileId] = 1; });
    return Object.keys(seen);
  }

  var q = new URLSearchParams(location.search);
  var board = q.get("board");
  if (!board) return start();               // not our URL: leave the app alone
  var frame = q.get("frame") || "";
  var edit = q.get("edit") === "1";
  var K_EL = "excalidraw", K_ST = "excalidraw-state";
  var LOCK = "haipipe-xcal-edit", LOCK_MS = 6000;
  var SAVE = "/_board/excalidraw-save";
  var scene_url = "/" + board.replace(/^\/+/, "") +
                  (frame ? "?frame=" + encodeURIComponent(frame) : "");
  var me = String(Math.floor(performance.now() * 1000)) + location.search;

  function lock_held_by_other() {
    try {
      var l = JSON.parse(localStorage.getItem(LOCK) || "null");
      return l && l.id !== me && (Date.now() - l.t) < LOCK_MS ? l : null;
    } catch (e) { return null; }
  }
  var blocked = edit ? lock_held_by_other() : null;
  if (blocked) edit = false;                // another tab owns the pen

  /* ---- 1. seed, synchronously: the app reads storage the moment it boots -- */
  var x = new XMLHttpRequest();
  x.open("GET", scene_url, false);
  try { x.send(null); } catch (e) {}
  var scene = null;
  if (x.status === 200) { try { scene = JSON.parse(x.responseText); } catch (e) {} }
  if (!scene) {
    console.error("[haipipe] could not load " + scene_url + " (HTTP " + x.status + ")");
    return start();
  }
  var els = (scene.elements || []).filter(function (e) { return !e.isDeleted; });

  // The app filters stored appState through a per-key table, and `viewModeEnabled`
  // is one of the keys it REFUSES to restore, so the obvious way to make an embed
  // read-only does not work. `activeTool` and `zenModeEnabled` do restore, and
  // between them they do the job better: the hand tool pans and zooms but cannot
  // draw, and zen mode takes the editing chrome off a figure nobody is editing.
  var st = { viewBackgroundColor: "#ffffff", zenModeEnabled: !edit };
  if (!edit) st.activeTool = { type: "hand", customType: null, locked: true,
                               lastActiveTool: null, fromSelection: false };
  // Without `#url=` nothing scrolls to content, so a frame at x=4000 would open
  // on empty canvas. Fit whatever we were asked for, frame or whole board.
  var box = null;
  els.forEach(function (e) {
    if (frame && e.type !== "frame") return;   // fit the FRAME, not its contents
    var b = [e.x, e.y, e.x + (e.width || 0), e.y + (e.height || 0)];
    box = box ? [Math.min(box[0], b[0]), Math.min(box[1], b[1]),
                 Math.max(box[2], b[2]), Math.max(box[3], b[3])] : b;
  });
  if (box) {
    var vw = innerWidth || 1200, vh = innerHeight || 800, pad = 48;
    var z = Math.min(1, (vw - 2 * pad) / Math.max(1, box[2] - box[0]),
                        (vh - 2 * pad) / Math.max(1, box[3] - box[1]));
    z = Math.max(0.1, z);
    st.zoom = { value: z };
    st.scrollX = (vw / z - (box[2] - box[0])) / 2 - box[0];
    st.scrollY = (vh / z - (box[3] - box[1])) / 2 - box[1];
  }

  if (edit) {
    localStorage.setItem(K_EL, JSON.stringify(els));
    localStorage.setItem(K_ST, JSON.stringify(st));
    localStorage.setItem(LOCK, JSON.stringify({ id: me, frame: frame, t: Date.now() }));
    setInterval(function () {
      localStorage.setItem(LOCK, JSON.stringify({ id: me, frame: frame, t: Date.now() }));
    }, 2000);
    addEventListener("beforeunload", function () { localStorage.removeItem(LOCK); });
  } else {
    // An embed must not touch the real storage: 28 of them share this origin.
    var mem = {};
    mem[K_EL] = JSON.stringify(els);
    mem[K_ST] = JSON.stringify(st);
    var shim = {
      getItem: function (k) { return k in mem ? mem[k] : null; },
      setItem: function (k, v) { mem[k] = String(v); },
      removeItem: function (k) { delete mem[k]; },
      clear: function () { mem = {}; },
      key: function (i) { return Object.keys(mem)[i] || null; }
    };
    Object.defineProperty(shim, "length", { get: function () { return Object.keys(mem).length; } });
    try {
      Object.defineProperty(window, "localStorage", { value: shim, configurable: true });
    } catch (e) {
      console.error("[haipipe] could not shim localStorage; not seeding", e);
    }
  }

  /* ---- 1b. the images, then let the app boot ------------------------- */
  // Nothing above this point is async, so the app is held for exactly as long
  // as the image seed takes, and not one frame longer.
  put_files(scene.files).then(start, start);

  /* ---- 2. the badge: saving is invisible otherwise -------------------- */
  var pill;
  function say(text, tone) {
    if (!pill) {
      pill = document.createElement("div");
      pill.setAttribute("style",
        "position:fixed;left:12px;bottom:12px;z-index:2147483647;font:12px/1.5 " +
        "ui-monospace,Menlo,monospace;padding:5px 10px;border-radius:999px;" +
        "pointer-events:none;box-shadow:0 1px 4px rgba(0,0,0,.25)");
      (document.body || document.documentElement).appendChild(pill);
    }
    pill.textContent = text;
    pill.style.background = tone === "bad" ? "#c0392b" : tone === "busy" ? "#8a6d3b" : "#2d6a4f";
    pill.style.color = "#fff";
  }
  function ready() {
    if (!document.body) return setTimeout(ready, 60);
    if (blocked) {
      say("👁 read-only · another tab is editing " + (blocked.frame || "the board"), "bad");
    } else if (!edit) {
      say("👁 read-only · pan and zoom · ✏️ Edit on the page to draw");
    } else {
      say("✏️ editing " + (frame || "the whole board") + " · saves to the repo");
    }
  }
  ready();

  /* ---- 3. write back, from the editing tab only ---------------------- */
  if (!edit) return;
  // Compare on CONTENT, not on the raw JSON. Excalidraw rewrites `version`,
  // `versionNonce` and `updated` on every element the moment it loads a scene,
  // so a raw comparison reports a change the instant the editor opens and the
  // file gets rewritten by merely being looked at (found 260726 in headless
  // Chrome: "✓ saved" one second after load, nothing drawn). Key order differs
  // between our writer and the app's, so it is normalised here too.
  var VOLATILE = { version: 1, versionNonce: 1, updated: 1 };
  function sig(list) {
    return JSON.stringify(list.map(function (e) {
      var o = {};
      Object.keys(e).sort().forEach(function (k) { if (!VOLATILE[k]) o[k] = e[k]; });
      return o;
    }));
  }

  var last = sig(els), busy = false;
  var sent = {};                            // fileIds the server already has
  Object.keys(scene.files || {}).forEach(function (id) { sent[id] = 1; });
  function flush(unloading) {
    var now = localStorage.getItem(K_EL);
    if (!now || busy) return;
    var live;
    try { live = JSON.parse(now).filter(function (e) { return !e.isDeleted; }); }
    catch (e) { return; }
    var body = sig(live);
    if (body === last) return;
    if (unloading) {
      // No time for IndexedDB on the way out, so this carries elements only.
      // Safe: the server MERGES the files map, so images saved by an earlier
      // tick stay. Only an image pasted in the last second or so can be lost.
      if (navigator.sendBeacon)
        navigator.sendBeacon(SAVE, new Blob(
          [JSON.stringify({ board: board, frame: frame, elements: live })],
          { type: "application/json" }));
      return;
    }
    busy = true;
    say("… saving", "busy");
    // Only images this tab has not already stashed: re-sending a screenshot
    // every 1.5 seconds would make a megabyte-per-tick save loop.
    var owed = image_ids(live).filter(function (id) { return !sent[id]; });
    get_files(owed).then(function (files) {
      var n = Object.keys(files).length;
      return fetch(SAVE, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board: board, frame: frame, elements: live, files: files })
      }).then(function (r) { return r.json(); }).then(function (r) {
        busy = false;
        if (r && r.ok) {
          last = body;
          Object.keys(files).forEach(function (id) { sent[id] = 1; });
          say("✓ saved " + new Date().toTimeString().slice(0, 8) +
              (n ? " · " + n + " image" + (n > 1 ? "s" : "") : ""));
        } else { say("✗ " + ((r && r.err) || "refused"), "bad"); }
      });
    }).catch(function (e) { busy = false; say("✗ " + e, "bad"); });
  }
  setInterval(flush, 1500);
  addEventListener("beforeunload", function () { flush(true); });
})();
