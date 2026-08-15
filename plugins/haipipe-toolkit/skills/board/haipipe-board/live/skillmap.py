"""🛠 Skill map · the page's citations to SKILLS, worked through a workbench.

BIBEX'S TWIN, deliberately (JL 260815: "a plugin named skill, showing what
skills is related to this page, or is designed based on the content of this
page"). BibEx is the page's references into the literature; this is the page's
references into the skill tree, and it keeps the same grammar:

  seeded, never invented   the scan only lists skill NAMES the page actually
                           writes; a relation a scan cannot see is the pen's
  MIXED, like bibex        skill/<stem>.md is PRIMARY, a person's declared
                           map; the card view beside it is derived
  the tick is a judgment   ✓ means "page and skill are ALIGNED as of DATE",
                           and the card flags it stale the moment the skill's
                           own last_updated moves past the tick

WHY DRIFT IS THE CARD'S CENTER: a page rules something, a skill implements it,
then one moves without the other — the board's oldest failure mode. The card
puts the skill's last_updated beside the page's newest Log date and the
person's aligned tick, so drift is visible at a glance instead of discovered
in a review.

Two relations only: `designs` (this page rules part of that skill's contract)
and `uses` (this page leans on that skill). The seed can only claim `uses`;
`designs` is always a person's word.
"""
import datetime
import re
from pathlib import Path

from live.export import _VIEW, _esc


# One row of the store, diff-friendly on purpose:
#   - <name> · relation: designs · aligned: {JL 260815} · note: free text
_ROW = re.compile(r"^- (\S+) · relation: (designs|uses)"
                  r"(?: · aligned: \{([^}]*)\})?"
                  r"(?: · note: (.*))?\s*$")

_STORE_HEAD = """# skill map · %s
<!-- PRIMARY: this page's declared skill relations (haipipe-page-plugin).
     Edit here or through the 🛠 tab; a refresh only APPENDS newly scanned
     names and never removes a row. The seed claims `uses` at most —
     `designs` is always a person's word. -->

"""


class SkillmapMixin:

    # ---- the skill index ---------------------------------------------
    def _skill_index(self):
        """name -> {dir, name, description, version, last_updated}, from every
        SKILL.md in the toolkit tree. Archives and parked work are not offers."""
        base = Path(__file__).resolve().parents[3]
        out = {}
        for f in base.rglob("SKILL.md"):
            parts = f.relative_to(base).parts
            if any(s.startswith("_") or s == "node_modules" for s in parts):
                continue
            name = f.parent.name
            if "-" not in name:          # every real skill name carries one;
                continue                 # bare words would match everywhere
            out[name] = {"dir": f.parent, "skillmd": f}
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
        rows, order = {}, []
        if store.is_file():
            for line in store.read_text(encoding="utf-8").splitlines():
                m = _ROW.match(line.strip())
                if m and m.group(1) not in rows:
                    rows[m.group(1)] = {"relation": m.group(2),
                                        "aligned": m.group(3) or "",
                                        "note": m.group(4) or ""}
                    order.append(m.group(1))
        return {"page": page_src, "dir": out_dir, "stem": page_src.stem,
                "store": store, "rows": rows, "order": order,
                "ctx": self._canon_ctx(board, p)}, None

    def _skillmap_write(self, st):
        lines = [_STORE_HEAD % st["stem"]]
        for name in st["order"]:
            r = st["rows"][name]
            line = "- %s · relation: %s" % (name, r["relation"])
            if r.get("aligned"):
                line += " · aligned: {%s}" % r["aligned"]
            if r.get("note"):
                line += " · note: %s" % r["note"]
            lines.append(line + "\n")
        st["store"].write_text("".join(lines), encoding="utf-8")

    @staticmethod
    def _page_log_date(page_src):
        """The page's newest Log stamp: Log keeps newest first, so the first
        dated line under ## Log is the page's own 'last moved'."""
        text = page_src.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"(?ms)^## Log\s*\n(.*)", text)
        if not m:
            return ""
        d = re.search(r"(?m)^-?\s*(\d{6})", m.group(1))
        return d.group(1) if d else ""

    # ---- POST /_board/skill · the refresh ----------------------------
    def skillmap_refresh(self, p):
        """Seed-append the names this page actually writes, then regenerate
        the card view. Extract-only: a scanned row claims `uses` at most, and
        a row already in the store is never touched or removed."""
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
            # hyphen blocks, which keeps haipipe-page out of haipipe-page-plugin.
            if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(name), text):
                st["rows"][name] = {"relation": "uses", "aligned": "", "note": ""}
                st["order"].append(name)
                imported.append(name)
        if imported or not st["store"].is_file():
            self._skillmap_write(st)
        url = self._skillmap_view(st, index)
        return {"ok": True, "url": url, "n": len(st["order"]),
                "imported": imported}, None

    # ---- POST /_board/skill-verify · the human tick ------------------
    def skillmap_verify(self, p):
        """{name, who?, undo?}: ✓ = "page and skill are ALIGNED", a person's
        dated judgment on the row. The one field is all this door may touch."""
        st, err = self._skillmap_state(p)
        if err:
            return None, err
        name = (p.get("name") or "").strip()
        if name not in st["rows"]:
            return None, "no row %r in the skill map" % name
        if p.get("undo"):
            st["rows"][name]["aligned"] = ""
        else:
            who = (p.get("who") or "JL").strip()
            st["rows"][name]["aligned"] = "%s %s" % (
                who, datetime.date.today().strftime("%y%m%d"))
        self._skillmap_write(st)
        self._skillmap_view(st, self._skill_index())
        return {"ok": True, "name": name}, None

    # ---- POST /_board/skill-entry · the pen --------------------------
    def skillmap_entry(self, p):
        """{name, relation, note?, replace?}: lands a PERSON's declared
        relation. The name must resolve to a real SKILL.md (a typo guard, not
        a judgment); the relation must be one of the two words."""
        st, err = self._skillmap_state(p)
        if err:
            return None, err
        name = (p.get("name") or "").strip().lstrip("/")
        rel = (p.get("relation") or "uses").strip()
        index = self._skill_index()
        if name not in index:
            return None, ("%r resolves to no SKILL.md in the toolkit tree; "
                          "the pen lands declarations, not new skills" % name)
        if rel not in ("designs", "uses"):
            return None, "relation must be `designs` or `uses`, got %r" % rel
        if name in st["rows"] and not p.get("replace"):
            st["rows"][name]["relation"] = rel     # upgrading uses->designs is
        else:                                      # the pen's commonest move
            if name not in st["rows"]:
                st["order"].append(name)
            st["rows"][name] = {"relation": rel, "aligned": "",
                                "note": (p.get("note") or "").strip()}
        if p.get("note"):
            st["rows"][name]["note"] = p.get("note").strip()
        self._skillmap_write(st)
        self._skillmap_view(st, index)
        return {"ok": True, "name": name}, None

    # ---- the card view ------------------------------------------------
    def _skillmap_view(self, st, index):
        page_date = self._page_log_date(st["page"])
        cards = []
        for name in st["order"]:
            r = st["rows"][name]
            known = index.get(name)
            meta = self._skill_meta(known["skillmd"]) if known else {}
            upd = meta.get("last_updated", "")
            # drift: the tick's YYMMDD against the skill's own last_updated
            stale = ""
            if r["aligned"] and upd:
                tick = "20" + r["aligned"].split()[-1]          # 260815 -> 20260815
                moved = upd.replace("-", "")
                if len(tick) == 8 and len(moved) == 8 and moved > tick:
                    stale = ("<div class='mut'>⚠ drifted: the skill moved %s, "
                             "after the tick</div>" % _esc(upd))
            if r["aligned"]:
                status = ("<span class='st'><span class='ok'>✅ aligned · %s"
                          "</span> <button class='unver' data-n='%s'>undo"
                          "</button></span>" % (_esc(r["aligned"]), _esc(name)))
            else:
                status = ("<span class='st'>⬜ <button class='ver' data-n='%s'>"
                          "✓ aligned</button></span>" % _esc(name))
            link = ("<a href='%s' target='_blank'>open SKILL.md</a>"
                    % self._url_of(known["skillmd"])) if known else \
                   "<span class='mut'>not found in the toolkit tree</span>"
            rel = ("<b style='color:#1f5aa8'>[designs]</b>" if
                   r["relation"] == "designs" else "[uses]")
            cards.append(
                "<div class='card%s'>%s<b>🛠 %s</b> %s "
                "<span class='mut'>v%s · updated %s</span>"
                "<div class='mut'>%s</div><div>%s"
                "%s</div>%s%s</div>"
                % ("" if known else " miss", status, _esc(name), rel,
                   _esc(meta.get("version", "?")), _esc(upd or "?"),
                   _esc(meta.get("description", "")), link,
                   (" · <button class='mkdes' data-n='%s'>↑ designs</button>"
                    % _esc(name)) if r["relation"] == "uses" else "",
                   ("<div class='mut'>note: %s</div>" % _esc(r["note"]))
                   if r["note"] else "", stale))
        if not st["order"]:
            cards = ["<p class='mut'>no skill relations yet — ↻ refresh "
                     "seeds the names this page writes.</p>"]
        head = ("<button id='refresh' class='st'>↻ refresh</button>"
                "<h1>🛠 %s · %d skill%s</h1><p class='mut'>the page's skill "
                "map · page last moved %s · <a href='%s' download>⬇ the "
                "store</a></p>"
                % (_esc(st["stem"]), len(st["order"]),
                   "" if len(st["order"]) == 1 else "s",
                   _esc(page_date or "?"), self._url_of(st["store"])))
        add = ("<div class='card'><b>＋ declare a relation</b><div>"
               "<input id='newname' placeholder='skill name, e.g. "
               "haipipe-page-plugin' style='width:46%'> "
               "<select id='newrel'><option>uses</option><option>designs"
               "</option></select> "
               "<input id='newnote' placeholder='note (optional)' "
               "style='width:26%'> <button id='addskill'>add</button>"
               "<span class='mut' id='addnote'></span></div></div>")
        script = ("""<script>
var CTX = {path: %s, file: %s};
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
      relation: document.getElementById('newrel').value,
      note: document.getElementById('newnote').value});
  if (!b.dataset || !b.dataset.n) return;
  if (b.className === 'ver')   return post('skill-verify', {name: b.dataset.n});
  if (b.className === 'unver') return post('skill-verify', {name: b.dataset.n, undo: true});
  if (b.className === 'mkdes') return post('skill-entry', {name: b.dataset.n, relation: 'designs'});
});
</script>""" % (self._json(st["ctx"]["path"]), self._json(st["ctx"]["file"])))
        css = ("<style>button{cursor:pointer;border:1px solid var(--line);"
               "background:var(--card);color:var(--fg);border-radius:6px;"
               "padding:3px 9px;font:500 12px -apple-system,sans-serif}"
               "input,select{border:1px solid var(--line);border-radius:6px;"
               "padding:5px 8px;background:var(--card);color:var(--fg);"
               "font:12px ui-monospace,Menlo,monospace}"
               ".ok{color:#2a8a2a}.st{float:right}</style>")
        view = st["dir"] / (st["stem"] + "-skill.html")
        view.write_text(_VIEW.format(title=_esc(st["stem"] + " · skill map"),
                                     body=css + head + "".join(cards)
                                     + add + script),
                        encoding="utf-8")
        return self._url_of(view)

    @staticmethod
    def _json(s):
        import json
        return json.dumps(s or "")
