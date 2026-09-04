"""🛠 Skill map · the page's citations to SKILLS, ranked by the person.

BIBEX'S TWIN, deliberately (JL 260815: "a plugin named skill, showing what
skills is related to this page, or is designed based on the content of this
page"). Evidence Citations is the page's references into the literature; this is the page's
references into the skill tree.

FLATTENED ON JL's RULING (260816: "maybe we don't need to have these concept
… we just need to show these skills and the user can drag and rank them
themselves"). The first build carried a judgment vocabulary — uses/designs
relations, an aligned ✓ with drift dates — and it came out whole. What
remains is the communication core:

  seeded, never invented   the scan only lists skill NAMES the page actually
                           writes, appended at the BOTTOM of the list
  the ORDER is the rank    top = most related; the person drags cards and
                           the store keeps exactly that order, nothing else
  ✕ is the removal         a removed name stays in the store as a tombstone
                           so a refresh can never re-seed it; ↩ restores
  MIXED, like bibex        outline/skill/<stem>.md is PRIMARY, the person's
                           ranked list; the card view beside it is derived
"""
import re
from pathlib import Path

from live.export import _VIEW, _esc


# One row of the store, diff-friendly on purpose:
#   - <name> · note: free text          (order in the file IS the rank)
#   - <name> · removed                  (the ✕ tombstone; never re-seeded)
# The pattern also swallows the pre-260816 grammar (relation/aligned fields)
# so old stores read cleanly; any write re-emits the flat form.
_ROW = re.compile(r"^- (?P<name>\S+)"
                  r"(?: · relation: (?P<rel>designs|uses|ignored))?"
                  r"(?: · aligned: \{[^}]*\})?"
                  r"(?P<removed> · removed)?"
                  r"(?: · note: (?P<note>.*))?\s*$")

_STORE_HEAD = """# skill map · %s
<!-- PRIMARY: this page's skills, ranked (haipipe-plugin).
     The ORDER is the person's rank: top = most related. Edit here or drag
     in the 🛠 tab. A refresh only APPENDS newly scanned names at the bottom;
     a `removed` row is a person's ✕ and is never re-seeded. -->

"""


class SkillmapMixin:

    # ---- the skill index ---------------------------------------------
    @staticmethod
    def _skill_roots(source=__file__):
        """Return every installed plugin's canonical ``skills/`` root.

        The Board implementation lives inside ``haipipe-toolkit``, but a Page
        may cite a skill shipped by a sibling plugin such as
        ``subjective-label``.  Falling back to the local toolkit root keeps
        the module usable when it is copied outside the normal ``plugins/``
        layout.
        """
        source = Path(source).resolve()
        plugins = next((parent for parent in source.parents
                        if parent.name == "plugins"), None)
        if plugins is not None:
            roots = sorted((plugin / "skills" for plugin in plugins.iterdir()
                            if (plugin / "skills").is_dir()),
                           key=lambda path: path.as_posix())
            if roots:
                return roots
        return [source.parents[3]]

    def _skill_index(self, roots=None):
        """name -> {dir, skillmd, agent?}, across installed plugin skills.

        Include every real SKILL.md plus agent definitions inside a skill tree
        or at a plugin's top-level ``agents/`` directory (JL 260816: "our Skill
        其实也是包括 Agent 相关的").  Archives and parked work are not offers.
        """
        roots = list(roots or self._skill_roots())
        out = {}
        agent_files = set()
        for base in roots:
            for f in base.rglob("SKILL.md"):
                parts = f.relative_to(base).parts
                if any(s.startswith("_") or s == "node_modules" for s in parts):
                    continue
                name = f.parent.name
                if "-" not in name:      # every real skill name carries one;
                    continue             # bare words would match everywhere
                out.setdefault(name, {"dir": f.parent, "skillmd": f})
            agent_files.update(base.rglob("agents/*-agent.md"))
            plugin_agents = base.parent / "agents"
            if plugin_agents.is_dir():
                agent_files.update(plugin_agents.glob("*-agent.md"))
        for f in sorted(agent_files, key=lambda path: path.as_posix()):
            if any(s.startswith("_") or s == "node_modules" for s in f.parts):
                continue
            if f.stem not in out:        # a skill name always outranks
                out[f.stem] = {"dir": f.parent, "skillmd": f, "agent": True}
        return out

    @staticmethod
    def _skill_meta(skillmd):
        # The WHOLE frontmatter block, not a byte-count guess: haipipe-board's
        # trigger-rich description outran every fixed slice and its card read
        # "v · updated ?" (JL 260815, the QPf8 screenshot).
        text = skillmd.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"(?s)\A---\s*\n(.*?)\n---", text)
        head = m.group(1) if m else text[:8000]
        def grab(key):
            m = re.search(r"(?m)^\s*%s:\s*[\"']?([^\"'\n>]+)" % key, head)
            return (m.group(1).strip() if m else "")
        desc = ""
        m = re.search(r"(?ms)^description:\s*>?-?\s*\n?((?:\s{2,}.+\n)+|.+)", head)
        if m:
            desc = " ".join(l.strip() for l in m.group(1).splitlines())
            if len(desc) > 150:
                # cut at a word, never mid-token: "…live in <p" reads broken
                desc = desc[:150].rsplit(" ", 1)[0].rstrip(",;·-") + " …"
        return {"version": grab("version"), "last_updated": grab("last_updated"),
                "description": desc}

    # ---- shared ground -----------------------------------------------
    def _skillmap_state(self, p):
        page_src, out_dir, board, err = self._export_target(p, "skill")
        if err:
            return None, err
        store = out_dir / (page_src.stem + ".md")
        rows, order, legacy = {}, [], False
        # Canonical wins.  A pre-migration sibling store is a read-only input;
        # the next refresh/edit writes the same rows to outline/skill/.
        legacy_store = page_src.parent / "skill" / (page_src.stem + ".md")
        source_store = store if store.is_file() else legacy_store
        migrated = source_store == legacy_store and legacy_store.is_file()
        if source_store.is_file():
            for line in source_store.read_text(encoding="utf-8").splitlines():
                m = _ROW.match(line.strip())
                if m and m.group("name") not in rows:
                    rel = m.group("rel")
                    if rel:
                        legacy = True    # pre-260816 grammar: migrate on write
                    rows[m.group("name")] = {
                        "removed": bool(m.group("removed")) or rel == "ignored",
                        "note": m.group("note") or ""}
                    order.append(m.group("name"))
        return {"page": page_src, "dir": out_dir, "stem": page_src.stem,
                "store": store, "rows": rows, "order": order,
                "legacy": legacy or migrated,
                "ctx": self._canon_ctx(board, p)}, None

    def _skillmap_write(self, st):
        lines = [_STORE_HEAD % st["stem"]]
        for name in st["order"]:
            r = st["rows"][name]
            line = "- %s" % name
            if r.get("removed"):
                line += " · removed"
            if r.get("note"):
                line += " · note: %s" % r["note"]
            lines.append(line + "\n")
        st["store"].write_text("".join(lines), encoding="utf-8")

    @staticmethod
    def _page_log_date(page_src):
        """The newest Page Record Log stamp, with legacy Page fallback."""
        record = (page_src.parent / "outline" /
                  (page_src.stem + "-log.md"))
        if record.is_file():
            text = record.read_text(encoding="utf-8", errors="replace")
            dates = re.findall(r"(?m)^###\s+(\d{6})", text)
            return max(dates) if dates else ""
        text = page_src.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"(?ms)^## Log\s*\n(.*)", text)
        if not m:
            return ""
        dates = re.findall(r"(?m)^-?\s*(\d{6})", m.group(1))
        return max(dates) if dates else ""

    # ---- POST /_board/skill · the refresh ----------------------------
    def skillmap_refresh(self, p):
        """Seed-append the names this page actually writes, then regenerate
        the card view. Extract-only, and modest about placement: a new name
        lands at the BOTTOM, because the order above it is the person's."""
        st, err = self._skillmap_state(p)
        if err:
            return None, err
        index = self._skill_index()
        text = st["page"].read_text(encoding="utf-8", errors="replace")
        imported = []
        for name in sorted(index):
            if name in st["rows"] or name == st["stem"]:
                continue
            # `/name` and `path/to/name` are the commonest ways a page cites a
            # skill, so a preceding slash must MATCH; only a word char or a
            # hyphen blocks, which keeps haipipe-page out of haipipe-plugin.
            if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(name), text):
                st["rows"][name] = {"removed": False, "note": ""}
                st["order"].append(name)
                imported.append(name)
        if imported or st["legacy"] or not st["store"].is_file():
            self._skillmap_write(st)
        url = self._skillmap_view(st, index)
        return {"ok": True, "url": url, "n": len(st["order"]),
                "imported": imported}, None

    # ---- POST /_board/skill-order · the drag -------------------------
    def skillmap_order(self, p):
        """{order: [names]}: the person dragged the cards; the store keeps
        exactly that order. Names the client does not send (removed rows,
        anything raced in) keep their place after the sent ones."""
        st, err = self._skillmap_state(p)
        if err:
            return None, err
        sent = [n for n in (p.get("order") or []) if n in st["rows"]]
        st["order"] = sent + [n for n in st["order"] if n not in sent]
        self._skillmap_write(st)
        self._skillmap_view(st, self._skill_index())
        return {"ok": True, "n": len(sent)}, None

    # ---- POST /_board/skill-entry · the pen --------------------------
    def skillmap_entry(self, p):
        """{name, note?, remove?, restore?}: the person's edits to the list.
        A new name must resolve to a real SKILL.md (a typo guard, not a
        judgment) and lands at the TOP, because adding by hand says "this
        matters". `remove` is the ✕ tombstone a refresh can never re-seed
        (JL 260815: "only keep the most relative ones"); `restore` undoes it."""
        st, err = self._skillmap_state(p)
        if err:
            return None, err
        name = (p.get("name") or "").strip().lstrip("/")
        index = self._skill_index()
        if name in st["rows"]:
            if p.get("remove"):
                st["rows"][name]["removed"] = True
            if p.get("restore"):
                st["rows"][name]["removed"] = False
            if p.get("note"):
                st["rows"][name]["note"] = p.get("note").strip()
        else:
            if name not in index:
                return None, ("%r resolves to no SKILL.md and no agent "
                              "definition in the toolkit tree; the pen adds "
                              "real skills and agents, not new ones" % name)
            st["rows"][name] = {"removed": False,
                                "note": (p.get("note") or "").strip()}
            st["order"].insert(0, name)
        self._skillmap_write(st)
        self._skillmap_view(st, index)
        return {"ok": True, "name": name}, None

    # ---- the index view -----------------------------------------------
    def _skillmap_view(self, st, index):
        """THE INDEX (JL 260816: "we just need to show these skills and the
        user can drag and rank them themselves"): one card per skill, in the
        person's order, with a ⠿ handle to drag a card to its rank.
        Clicking a NAME navigates the SAME frame to that skill's full view,
        whose bar carries ← ☰ → back. One tab, two depths, no
        judgments."""
        shown = [n for n in st["order"] if not st["rows"][n]["removed"]]
        removed = [n for n in st["order"] if st["rows"][n]["removed"]]
        import urllib.parse as _up
        map_rel = self._url_of(st["store"]).lstrip("/")
        rows_html = []
        for name in shown:
            r = st["rows"][name]
            known = index.get(name)
            meta = self._skill_meta(known["skillmd"]) if known else {}
            upd = meta.get("last_updated", "")
            if known and known.get("agent"):
                # an AGENT row (JL 260816): 🤖, and the door is mdview —
                # an agent is one .md, not a folder with a SKILL.md
                href = ("/_board/mdview?p=%s"
                        % _up.quote(self._url_of(known["skillmd"]).lstrip("/")))
                nm = "<a class='snm' href='%s'>\U0001f916 %s</a>" % (href,
                                                                     _esc(name))
                open_link = "<a href='%s'>open the agent</a>" % href
            elif known:
                href = ("/_board/skillview?p=%s&map=%s"
                        % (_up.quote(self._url_of(known["dir"]).lstrip("/")),
                           _up.quote(map_rel)))
                nm = "<a class='snm' href='%s'>\U0001f6e0 %s</a>" % (href,
                                                                     _esc(name))
                open_link = "<a href='%s'>open the skill</a>" % href
            else:
                nm = ("<b>\U0001f6e0 %s</b> <span class='mut'>not in the "
                      "toolkit tree</span>" % _esc(name))
                open_link = "<span class='mut'>no SKILL.md to open</span>"
            # THE CARD, the shape JL kept (260816, the QPf3 screenshot) minus
            # the judgment chrome: name, meta, the description, "open the
            # skill" beside ✕ — and ⠿, because the ORDER is
            # the judgment (JL 260816).
            if known and known.get("agent"):
                meta_line = "agent"
            else:
                meta_line = "v%s · updated %s" % (meta.get("version") or "?",
                                                  upd or "?")
            rows_html.append(
                "<div class='row' draggable='true' data-n='%s'>"
                "<div class='rl'><span class='grip' title='drag to rank'>"
                "⠿</span>%s <span class='mut'>%s"
                "</span></div>"
                "<div class='rr'><button class='rm' data-n='%s' title="
                "'remove: off the index, never re-seeded'>✕</button>"
                "</div>"
                "<div class='dsc mut'>%s</div>"
                "<div class='dsc'>%s</div>%s</div>"
                % (_esc(name), nm, _esc(meta_line), _esc(name),
                   _esc(meta.get("description", "")),
                   open_link,
                   ("<div class='dsc mut'>note: %s</div>"
                    % _esc(r["note"])) if r["note"] else ""))
        cards = ("<div id='cards'>%s</div>" % "".join(rows_html)
                 if rows_html else
                 "<p class='mut'>no skills listed yet — ↻ refresh "
                 "seeds the names this page writes.</p>")
        head = ("<div class='bar'><b>\U0001f6e0 %s</b>"
                "<span class='mut'>· %d skill%s · drag to rank · "
                "refresh appends</span><span class='sp'></span>"
                "<button id='refresh'>↻ refresh</button>"
                "<a href='%s' download>⬇ store</a></div>"
                % (_esc(st["stem"]), len(shown),
                   "" if len(shown) == 1 else "s",
                   self._url_of(st["store"])))
        add = ("<details><summary><b>＋ add a skill</b></summary>"
               "<div style='padding:8px 0'>"
               "<input id='newname' placeholder='skill name' "
               "style='width:44%'> "
               "<input id='newnote' placeholder='note (optional)' "
               "style='width:30%'> <button id='addskill'>add</button>"
               "</div></details>")
        rmv = ""
        if removed:
            rmv = ("<details><summary class='mut'>\U0001f6ab removed · "
                   "%d</summary>%s</details>"
                   % (len(removed), "".join(
                       "<div>\U0001f6ab %s <button class='rst' data-n='%s'>"
                       "↩ restore</button></div>"
                       % (_esc(n), _esc(n)) for n in removed)))
        script = """<script>
var CTX = {path: __PATH__, file: __FILE__};
function post(route, body) {
  Object.assign(body, CTX);
  fetch('/_board/' + route, {method: 'POST',
    headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})
    .then(function (r) { return r.json(); })
    .then(function (j) {
      if (!j.ok) { alert('⚠ ' + (j.err || route)); return; }
      location.reload();
    })
    .catch(function (e) { alert('⚠ ' + e); });
}
document.addEventListener('click', function (ev) {
  var b = ev.target;
  if (b.id === 'refresh') return post('skill', {});
  if (b.id === 'addskill')
    return post('skill-entry', {
      name: document.getElementById('newname').value,
      note: document.getElementById('newnote').value});
  if (!b.dataset || !b.dataset.n) return;
  if (b.className === 'rm')  return post('skill-entry', {name: b.dataset.n, remove: true});
  if (b.className === 'rst') return post('skill-entry', {name: b.dataset.n, restore: true});
});
/* drag to rank: reorder the DOM while dragging, save the order on drop */
var drag = null, moved = false;
document.addEventListener('dragstart', function (ev) {
  drag = ev.target.closest ? ev.target.closest('.row') : null;
  moved = false;
  if (drag) drag.classList.add('drag');
});
document.addEventListener('dragover', function (ev) {
  if (!drag) return;
  ev.preventDefault();
  var r = ev.target.closest ? ev.target.closest('.row') : null;
  if (!r || r === drag) return;
  var box = r.getBoundingClientRect();
  var before = (ev.clientY - box.top) < box.height / 2;
  r.parentNode.insertBefore(drag, before ? r : r.nextSibling);
  moved = true;
});
document.addEventListener('drop', function (ev) { ev.preventDefault(); });
document.addEventListener('dragend', function () {
  if (!drag) return;
  drag.classList.remove('drag');
  drag = null;
  if (!moved) return;
  var names = Array.prototype.map.call(
    document.querySelectorAll('#cards .row'),
    function (r) { return r.dataset.n; });
  post('skill-order', {order: names});
});
</script>"""
        script = (script
                  .replace("__PATH__", self._json(st["ctx"]["path"]))
                  .replace("__FILE__", self._json(st["ctx"]["file"])))
        css = ("<style>"
               "body{padding:12px 16px}"
               "button{cursor:pointer;border:1px solid var(--line);"
               "background:var(--card);color:var(--fg);border-radius:6px;"
               "padding:3px 9px;font:500 12.5px -apple-system,sans-serif}"
               "input,select{border:1px solid var(--line);border-radius:6px;"
               "padding:4px 7px;background:var(--card);color:var(--fg);"
               "font:12px ui-monospace,Menlo,monospace}"
               ".sp{flex:1}"
               ".bar{display:flex;align-items:center;gap:8px;margin:0 0 12px;"
               "flex-wrap:wrap}"
               ".bar b{font:600 15px ui-monospace,Menlo,monospace}"
               ".row{display:flex;align-items:center;gap:8px 10px;"
               "flex-wrap:wrap;padding:12px 16px;border:1px solid var(--line);"
               "border-radius:10px;margin:0 0 12px;background:var(--card)}"
               ".row.drag{opacity:.45;border-style:dashed}"
               ".grip{cursor:grab;color:var(--mut);font-size:15px;"
               "padding:0 4px;user-select:none}"
               ".rl{display:flex;align-items:center;gap:8px;flex-wrap:wrap}"
               ".rr{margin-left:auto;display:flex;gap:6px;align-items:center}"
               ".dsc{flex-basis:100%;line-height:1.5}"
               ".snm{font:600 14px ui-monospace,Menlo,monospace;"
               "text-decoration:none;color:#1f5aa8}"
               ".snm:hover{text-decoration:underline}"
               "summary{cursor:pointer;margin:8px 0}"
               "</style>")
        view = st["dir"] / (st["stem"] + "-skill.html")
        view.write_text(_VIEW.format(title=_esc(st["stem"] + " \u00b7 skill "
                                                "index"),
                                     body=css + head + cards
                                     + add + rmv + script),
                        encoding="utf-8")
        return self._url_of(view)
    @staticmethod
    def _json(s):
        import json
        return json.dumps(s or "")

    # ---- GET /_board/skillview?p=<root-relative skill dir> ------------
    # THE WHOLE SKILL, ONE PAGE (JL 260815: "just show the main content of
    # the skill? and also add its other things, like the log, etc. … one html
    # to contain all the things"). SKILL.md rendered on stage; CHANGELOG and
    # every ref/*.md as collapsed folds; everything else as a listed tree with
    # raw links. Still a live render, never a compiled copy: a copy per page
    # would drift the day the skill moves.
    def serve_skillview(self):
        import urllib.parse
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        rel = urllib.parse.unquote((q.get("p") or [""])[0]).strip("/")
        d = (Path(self.root) / rel).resolve()
        try:
            d.relative_to(Path(self.root).resolve())
        except ValueError:
            return self.send_error(400, "outside --root")
        skillmd = d / "SKILL.md"
        if not skillmd.is_file():
            return self.send_error(404, "give ?p=<a folder holding SKILL.md>")
        meta = self._skill_meta(skillmd)
        text = skillmd.read_text(encoding="utf-8", errors="replace")
        fm = re.match(r"(?s)\A---\s*\n(.*?)\n---\s*\n", text)
        body_md = text[fm.end():] if fm else text

        # ← → BETWEEN THE PAGE'S SKILLS (JL 260815: "the whole split should be
        # the skill, kind of like the display split, with ← and →"): the
        # workbench passes ?map=<the page's store>, and the bar walks the SAME
        # order the cards show — the person's rank, top first — with arrow
        # keys doing what they do in a deck. No map, no bar: standalone works.
        nav = ""
        mrel = urllib.parse.unquote((q.get("map") or [""])[0]).strip("/")
        if mrel:
            mf = (Path(self.root) / mrel).resolve()
            try:
                mf.relative_to(Path(self.root).resolve())
            except ValueError:
                mf = None
            if mf is not None and mf.is_file():
                index = self._skill_index()
                names, seen = [], set()
                for line in mf.read_text(encoding="utf-8",
                                         errors="replace").splitlines():
                    m = _ROW.match(line.strip())
                    if not m or m.group("name") in seen:
                        continue
                    seen.add(m.group("name"))
                    if m.group("removed") or m.group("rel") == "ignored":
                        continue
                    names.append(m.group("name"))
                # ← → walks SKILLS only: an agent row's door is mdview,
                # which has no map bar to walk back out of
                stops = [(n, index[n]["dir"]) for n in names
                         if n in index and not index[n].get("agent")]
                here = next((i for i, s in enumerate(stops)
                             if s[1].resolve() == d), None)
                if here is not None and len(stops) > 1:
                    def jump(i):
                        return ("/_board/skillview?p=%s&map=%s"
                                % (urllib.parse.quote(self._url_of(
                                       stops[i][1]).lstrip("/")),
                                   urllib.parse.quote(mrel)))
                    pv = (here - 1) % len(stops)
                    nx = (here + 1) % len(stops)
                    nav = (
                        "<div style='display:flex;align-items:center;gap:12px;"
                        "justify-content:space-between;padding:6px 0 10px;"
                        "border-bottom:1px solid var(--line);margin-bottom:12px'>"
                        "<a class='pv' href='%s' title='previous skill'>"
                        "← %s</a><a href='/%s' title='back to the index'>"
                        "☰ 🛠 %d / %d</a>"
                        "<a class='nx' href='%s' title='next skill'>%s →</a>"
                        "</div>"
                        "<script>document.addEventListener('keydown',"
                        "function(e){if(e.key==='ArrowLeft')"
                        "location.href=document.querySelector('a.pv').href;"
                        "if(e.key==='ArrowRight')"
                        "location.href=document.querySelector('a.nx').href});"
                        "</script>"
                        % (jump(pv), _esc(stops[pv][0]),
                           _esc(mrel[:-3] + "-skill.html?embed"),
                           here + 1, len(stops),
                           jump(nx), _esc(stops[nx][0])))

        def fold(title, inner, open_=False):
            # The embedded file lives INSIDE a sub-document frame (JL 260816,
            # the CHANGELOG screenshot): its headings demote below the fold's
            # own summary, its rhythm tightens, and a left rule marks where
            # the host page ends and the embedded file begins.
            return ("<details%s><summary><b>%s</b></summary>"
                    "<div class='sub'>%s</div></details>"
                    % (" open" if open_ else "", title, inner))

        def md_fold(title, f):
            raw = f.read_text(encoding="utf-8", errors="replace")
            # the file's own H1 repeats the fold title one line above it;
            # showing both is saying the name twice in two sizes. Both title
            # forms go: `# name` and the setext `name\n====`.
            raw = re.sub(r"\A\s*(?:#\s[^\n]*|[^\n]+\n=+)\n+", "", raw)
            cut = ""
            if len(raw) > 80000:
                raw = raw[:80000]
                cut = ("<p class='mut'>… truncated · <a href='%s'>open raw"
                       "</a></p>" % self._url_of(f))
            return fold(title, self._md_html(raw) + cut)

        # RELATED SKILLS AS CHIPS (JL 260816: "I also want to link all the
        # related skills"): every skill name this skill's own text writes
        # becomes a chip that navigates THIS view to that skill — the graph
        # is walkable in place.
        sidx = self._skill_index()
        chips = []
        for n in sorted(sidx):
            if n == d.name:
                continue
            if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(n), text):
                if sidx[n].get("agent"):
                    chips.append("<a class='chip' href='/_board/mdview?p=%s'>"
                                 "\U0001f916 %s</a>"
                                 % (self._url_of(sidx[n]["skillmd"])
                                    .lstrip("/"), _esc(n)))
                    continue
                keep_map = ("&map=" + urllib.parse.quote(mrel)) if mrel else ""
                chips.append("<a class='chip' href='/_board/skillview?p=%s%s'>"
                             "\U0001f6e0 %s</a>"
                             % (self._url_of(sidx[n]["dir"]).lstrip("/"),
                                keep_map, _esc(n)))
        chiprow = ("<div class='chips'><span class='mut'>related · </span>%s"
                   "</div>" % "".join(chips[:16])) if chips else ""

        # ONE FOLD GRAMMAR FOR EVERY FILE (JL 260816: "why you don't make the
        # skill.md to the same to these?"): SKILL.md is a fold exactly like
        # CHANGELOG.md and ref/*.md — same summary, same sub-frame — and only
        # differs in starting OPEN, because it is what the reader came for.
        parts = [nav,
                 "<div class='hcard'><h1 style='margin:2px 0 4px'>\U0001f6e0 "
                 "%s</h1><p class='mut' style='margin:0 0 6px'>v%s · updated "
                 "%s · %s · <a href='%s'>raw SKILL.md</a></p><p style='margin:"
                 "0 0 6px'>%s</p>%s</div>"
                 % (_esc(d.name), _esc(meta.get("version") or "?"),
                    _esc(meta.get("last_updated") or "?"), _esc(rel),
                    self._url_of(skillmd), _esc(meta.get("description", "")),
                    chiprow),
                 fold("\U0001f4dc SKILL.md", self._md_html(body_md),
                      open_=True)]
        chlog = d / "CHANGELOG.md"
        if chlog.is_file():
            parts.append(md_fold("📜 CHANGELOG.md", chlog))
        ref = d / "ref"
        if ref.is_dir():
            for f in sorted(ref.glob("*.md")):
                parts.append(md_fold("📚 ref/" + _esc(f.name), f))
        # the rest: LISTED with sizes and raw links, never inlined — scripts
        # and assets are for machines, and a reader who wants one gets the raw
        rows, skip = [], {"SKILL.md", "CHANGELOG.md", "ref"}
        for f in sorted(d.rglob("*")):
            r = f.relative_to(d)
            if r.parts[0] in skip or any(s.startswith((".", "_"))
                                         for s in r.parts):
                continue
            if f.is_file():
                rows.append("<div>📄 <a href='%s'>%s</a> <span class='mut'>"
                            "%.1f KB</span></div>"
                            % (self._url_of(f), _esc(str(r)),
                               f.stat().st_size / 1024))
            if len(rows) >= 200:
                rows.append("<div class='mut'>… and more; the folder is the "
                            "truth</div>")
                break
        if rows:
            parts.append(fold("🗂 the rest of the folder · %d files"
                              % len(rows), "".join(rows)))
        doc = _VIEW.format(title=_esc(d.name + " · skill"),
                           body=self.MD_CSS
                                + "<style>summary{cursor:pointer;margin:10px 0}"
                                "hr{border:0;border-top:1px solid var(--line)}"
                                "</style><div class='doc'>" + "".join(parts)
                                + "</div>")
        raw = doc.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(raw)

    # ---- GET /_board/mdview?p=<root-relative .md> ---------------------
    # RENDERED LIVE, NEVER COMPILED INTO THE PLUGIN (JL 260815: "compile it to
    # the skill html so I can see the whole content?" — the answer is a view,
    # not a copy): a per-page compiled SKILL.html would duplicate the skill
    # under every page that cites it and drift the day the skill moves. One
    # render-on-request route always shows the skill AS IT IS NOW, and stores
    # nothing anywhere.
    def serve_mdview(self):
        import urllib.parse
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        rel = urllib.parse.unquote((q.get("p") or [""])[0]).lstrip("/")
        f = (Path(self.root) / rel).resolve()
        try:
            f.relative_to(Path(self.root).resolve())
        except ValueError:
            return self.send_error(400, "outside --root")
        if not f.is_file() or f.suffix != ".md":
            return self.send_error(404, "give ?p=<a .md under --root>")
        text = f.read_text(encoding="utf-8", errors="replace")
        body = ("%s<div class='doc'><p class='mut'>%s · rendered live · "
                "<a href='/%s'>raw</a></p>%s</div>"
                % (self.MD_CSS, _esc(rel), _esc(rel), self._md_html(text)))
        html_doc = _VIEW.format(title=_esc(f.parent.name + "/" + f.name),
                                body=body)
        raw = html_doc.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(raw)

    # One typography for every rendered .md surface (JL 260815: "the
    # skill-html is not well structure, it is not good to look at"): a
    # centered measure, real paragraphs, real lists, real tables.
    MD_CSS = ("<style>"
              ".doc{max-width:900px;margin:0 auto;padding:2px 6px}"
              ".doc p{margin:0 0 10px;line-height:1.62}"
              ".doc h2{font-size:20px;margin:26px 0 10px;padding-bottom:5px;"
              "border-bottom:1px solid var(--line)}"
              ".doc h3{font-size:16.5px;margin:20px 0 7px}"
              ".doc h4{font-size:14.5px;margin:16px 0 6px}"
              ".doc h5{font-size:13.5px;margin:12px 0 5px;color:var(--mut)}"
              ".doc ul{margin:0 0 12px;padding-left:24px}"
              ".doc li{margin:3px 0;line-height:1.55}"
              ".doc .tw{overflow-x:auto;margin:0 0 14px}"
              ".doc table{border-collapse:collapse;font-size:13px;"
              "line-height:1.45}"
              ".doc th,.doc td{border:1px solid var(--line);padding:6px 10px;"
              "text-align:left;vertical-align:top}"
              ".doc th{background:var(--bg);font-weight:600}"
              ".doc blockquote{border-left:3px solid var(--line);"
              "margin:0 0 12px;padding:2px 14px;color:var(--mut)}"
              ".doc hr{border:0;border-top:1px solid var(--line);"
              "margin:18px 0}"
              ".doc pre{margin:0 0 14px}"
              # the SUB-DOCUMENT frame: an embedded file reads one size down,
              # tighter, behind a left rule — never competing with its host
              ".doc .sub{border-left:3px solid var(--line);margin:2px 0 16px;"
              "padding:2px 16px;font-size:13px}"
              ".doc .sub h2{font-size:14.5px;margin:14px 0 6px;border:0;"
              "padding:0}"
              ".doc .sub h3{font-size:13.5px;margin:11px 0 5px}"
              ".doc .sub h4,.doc .sub h5{font-size:12.5px;margin:9px 0 4px}"
              ".doc .sub p,.doc .sub li{line-height:1.5;margin:0 0 7px}"
              ".doc .sub pre{font-size:11px;padding:9px;margin:0 0 10px}"
              ".doc .sub table{font-size:12px}"
              # the three declared regions: header CARD, region BANDS, chips
              ".doc .hcard{background:var(--card);border:1px solid var(--line);"
              "border-radius:10px;padding:12px 18px;margin:8px 0 4px}"
              ".doc .band{margin:20px 0 14px;padding:8px 14px;"
              "background:var(--card);border:1px solid var(--line);"
              "border-left:4px solid #1f5aa8;border-radius:8px;"
              "font-weight:600;color:#1f5aa8}"
              ".doc .chips{margin:4px 0 0}"
              ".doc .chip{display:inline-block;border:1px solid var(--line);"
              "border-radius:999px;padding:2px 11px;margin:2px 6px 2px 0;"
              "font:12px ui-monospace,Menlo,monospace;text-decoration:none;"
              "color:#1f5aa8;background:var(--bg)}"
              ".doc .chip:hover{border-color:#1f5aa8}"
              "</style>")

    @staticmethod
    def _md_html(text):
        """Generic markdown -> READABLE html: joined paragraphs, nested
        lists, pipe tables, quotes, fences, inline code/bold/links. A
        reader's renderer, not the page grammar — SKILL.md is ordinary
        markdown and earns ordinary typography."""
        fm = ""
        m = re.match(r"(?s)\A---\s*\n(.*?)\n---\s*\n", text)
        if m:
            fm = "<details><summary class='mut'>frontmatter</summary>" \
                 "<pre>%s</pre></details>" % _esc(m.group(1))
            text = text[m.end():]

        def inline(s):
            s = _esc(s)
            s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
            s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
            s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                       r"<a href='\2' target='_blank'>\1</a>", s)
            return s

        out, para, fence, quote = [], [], None, []
        lists = []                       # open <ul> indents, a stack

        def close_lists(to=-1):
            while lists and lists[-1] > to:
                lists.pop()
                out.append("</ul>")

        def flush_para():
            if para:
                out.append("<p>%s</p>" % " ".join(inline(l) for l in para))
                para.clear()

        def flush_quote():
            if quote:
                out.append("<blockquote>%s</blockquote>"
                           % "<br>".join(inline(l) for l in quote))
                quote.clear()

        def flush_all():
            flush_para()
            flush_quote()
            close_lists()

        def table_block(rows):
            cells = [[c.strip() for c in r.strip().strip("|").split("|")]
                     for r in rows]
            sep = (len(cells) > 1
                   and all(re.fullmatch(r":?-{2,}:?", c) for c in cells[1] if c))
            html_rows = []
            body = cells[2:] if sep else cells[1:]
            if sep or len(cells) > 1:
                html_rows.append("<tr>%s</tr>" % "".join(
                    "<th>%s</th>" % inline(c) for c in cells[0]))
            else:
                body = cells
            for r in body:
                html_rows.append("<tr>%s</tr>" % "".join(
                    "<td>%s</td>" % inline(c) for c in r))
            return ("<div class='tw'><table>%s</table></div>"
                    % "".join(html_rows))

        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            if fence is not None:
                if line.startswith("```"):
                    out.append("<pre>%s</pre>" % _esc("\n".join(fence)))
                    fence = None
                else:
                    fence.append(line)
                i += 1
                continue
            if line.startswith("```"):
                flush_all()
                fence = []
                i += 1
                continue
            if line.lstrip().startswith("|") and "|" in line.lstrip()[1:]:
                flush_all()
                rows = []
                while i < len(lines) and lines[i].lstrip().startswith("|"):
                    rows.append(lines[i])
                    i += 1
                out.append(table_block(rows))
                continue
            h = re.match(r"^(#{1,4})\s+(.*)", line)
            if h:
                flush_all()
                n = min(len(h.group(1)) + 1, 5)
                out.append("<h%d>%s</h%d>" % (n, inline(h.group(2)), n))
                i += 1
                continue
            li = re.match(r"^(\s*)[-*]\s+(.*)", line)
            if li:
                flush_para()
                flush_quote()
                ind = len(li.group(1))
                # continuation lines of this item: indented deeper, not
                # themselves items, quotes, headings, or fences
                item = [li.group(2)]
                while (i + 1 < len(lines)
                       and re.match(r"^\s{%d,}\S" % (ind + 2), lines[i + 1])
                       and not re.match(r"^\s*[-*]\s+", lines[i + 1])
                       and not lines[i + 1].lstrip().startswith(("```", "|", "#", ">"))):
                    item.append(lines[i + 1].strip())
                    i += 1
                if not lists or ind > lists[-1]:
                    lists.append(ind)
                    out.append("<ul>")
                else:
                    close_lists(ind)
                    if not lists:
                        lists.append(ind)
                        out.append("<ul>")
                out.append("<li>%s</li>" % " ".join(inline(x) for x in item))
                i += 1
                continue
            if line.startswith(">"):
                flush_para()
                close_lists()
                quote.append(line.lstrip("> "))
                i += 1
                continue
            if re.fullmatch(r"\s*(-{3,}|\*{3,})\s*", line):
                flush_all()
                out.append("<hr>")
                i += 1
                continue
            if not line.strip():
                flush_all()
                i += 1
                continue
            flush_quote()
            close_lists()
            para.append(line.strip())
            i += 1
        if fence is not None:
            out.append("<pre>%s</pre>" % _esc("\n".join(fence)))
        flush_all()
        return fm + "\n".join(out)
