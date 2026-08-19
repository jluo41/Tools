"""🗂 Task · the page's citations into the repo's TASK FOLDERS (QPf13).

THE FOURTH CITATION TWIN. BibEx holds a page's references into the literature,
skill into the skill tree, pagex into the repo's page tree, and this one holds
a page's references into `tasks/` — the executable folders `haipipe-task`
plans, builds, executes and reports (`plan.yaml` / `report.yaml` / `QA/*.md`).
A Q or S page argues something; the task folders behind that argument are
data, not prose, so they earn their own plugin rather than a paragraph of
paths that go stale the moment a task folder moves.

  BORROWED BY THE WHOLE FOLDER   unlike pagex (files only, to keep a page's
                                 own home safe from a ghost-page), a task
                                 folder is never itself a page: nothing under
                                 `tasks/` matches Q/S/Agent/Meeting/Design's
                                 name pattern, so linking the WHOLE directory
                                 is safe and is also the only shape that means
                                 anything — "which task" is a folder question
  MATERIALIZED AS SYMLINKS       same law as pagex: a copy ages, a link stays
                                 current, and a moved source breaks VISIBLY
  THE STORE IS THE TRUTH         task/<stem>.md is PRIMARY and ranked; the
                                 links and the status view are re-minted from
                                 it and a refresh never edits a row a person
                                 wrote
  STATUS IS READ FROM DISK       plan.yaml / report.yaml / QA/*.md presence,
                                 never a hand-typed word — the same rule
                                 plugview.py uses for display and probe
"""
import os
import re
from pathlib import Path

from live.export import _VIEW, _esc

# One row of the store, diff-friendly like pagex's and the skill map's:
#   - <repo-relative path to a task folder> · note: free text
#   - <repo-relative path> · removed                      (the ✕ tombstone)
_ROW = re.compile(r"^- (?P<path>\S+)"
                  r"(?P<removed> · removed)?"
                  r"(?: · note: (?P<note>.*))?\s*$")

_STORE_HEAD = """# task · %s
<!-- PRIMARY: the task folders this page is written about (haipipe-plugin).
     The ORDER is the person's rank: top = most load-bearing. Edit here or
     drag in the 🗂 tab. Paths are repo-relative and name a TASK FOLDER, a
     directory under some `tasks/` tree, never a single file inside one. A
     refresh re-mints the symlinks beside this file and never edits a row; a
     `removed` row is a person's ✕. -->

"""

# report.yaml's own Preview-comment convention (haipipe-task): "# O: status=X
# ...". Best-effort only — the line is free-form and not every report carries
# it (haipipe-task, 260817 vintage). A read that fails leaves state empty
# rather than guessing.
_O_STATUS = re.compile(r"^#\s*O:.*?\bstatus=(\S+)", re.M)


def _task_status(folder):
    """Read a task folder's stage from the FILES on disk, never a claim.

    Mirrors plugview.py's `_display_state`: presence, not prose, decides the
    badge. `workflow/` is haipipe-task's own nesting (Stata-dialect tasks keep
    plan.yaml and report.yaml one level down); a bare `plan.yaml` at the
    folder root is the older / non-Stata shape and is read the same way.
    """
    wf = folder / "workflow"
    base = wf if wf.is_dir() else folder
    plan = base / "plan.yaml"
    report = base / "report.yaml"
    qa_dir = folder / "QA"
    qa_n = len(list(qa_dir.glob("*.md"))) if qa_dir.is_dir() else 0
    hint = ""
    if report.is_file():
        m = _O_STATUS.search(report.read_text(encoding="utf-8", errors="replace"))
        hint = m.group(1) if m else ""
        badge, label = "✅", "reported" + (" · %s" % hint if hint else "")
        newest = report
    elif plan.is_file():
        badge, label = "📝", "planned · not yet reported"
        newest = plan
    else:
        badge, label = "❔", "no plan.yaml / report.yaml found under %s" % (
            "workflow/" if wf.is_dir() else "the folder root")
        newest = None
    age = ""
    try:
        files = [f for f in folder.rglob("*") if f.is_file()
                 and not f.name.startswith(".")]
        if files:
            import time
            newest_mtime = max(f.stat().st_mtime for f in files)
            days = int((time.time() - newest_mtime) // 86400)
            age = "today" if days <= 0 else "%dd ago" % days
    except OSError:
        pass
    return {"badge": badge, "label": label, "plan": plan.is_file(),
            "report": report.is_file(), "qa_n": qa_n, "age": age,
            "hint": hint}


class TaskMixin:

    # ---- shared ground -------------------------------------------------
    def _task_state(self, p):
        page_src, out_dir, board, err = self._export_target(p, "task")
        if err:
            return None, err
        store = out_dir / (page_src.stem + ".md")
        rows, order = {}, []
        if store.is_file():
            for line in store.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line.startswith("- "):
                    continue
                m = _ROW.match(line)
                if m and m.group("path") not in rows:
                    rows[m.group("path")] = {
                        "removed": bool(m.group("removed")),
                        "note": m.group("note") or ""}
                    order.append(m.group("path"))
        return {"page": page_src, "dir": out_dir, "stem": page_src.stem,
                "store": store, "rows": rows, "order": order,
                "board": Path(board), "ctx": self._canon_ctx(board, p)}, None

    def _task_write(self, st):
        lines = [_STORE_HEAD % st["stem"]]
        for path in st["order"]:
            r = st["rows"][path]
            line = "- %s" % path
            if r.get("removed"):
                line += " · removed"
            if r.get("note"):
                line += " · note: %s" % r["note"]
            lines.append(line + "\n")
        st["store"].write_text("".join(lines), encoding="utf-8")

    @staticmethod
    def _task_link_name(target, root):
        """Where the symlink lands: `<project>/<inner>` when the target sits
        under a `tasks/` ancestor (the repo's own convention, CLAUDE.md),
        keeping the path readable and collision-free; `<parent>/<name>`
        otherwise, the pagex fallback for anything off that convention."""
        d, stack = target, []
        while d != root and d.parent != d:
            if d.name == "tasks":
                project = d.parent.name
                inner = "/".join(reversed(stack))
                return "%s/%s" % (project, inner) if inner else project
            stack.append(d.name)
            d = d.parent
        return "%s/%s" % (target.parent.name, target.name)

    # ---- the minter ------------------------------------------------------
    def _task_mint(self, st):
        """Re-mint every live row as a relative symlink to a DIRECTORY, and
        report each row's status. THE ONE SAFETY RULE, pagex's own: this only
        ever unlinks a SYMLINK inside task/."""
        root = Path(self.root).resolve()
        base = st["dir"].resolve()
        for f in sorted(base.rglob("*"), reverse=True):
            if f.is_symlink():
                f.unlink()
            elif f.is_dir() and not any(f.iterdir()):
                f.rmdir()

        out = []
        for path in st["order"]:
            r = st["rows"][path]
            rec = {"path": path, "note": r["note"], "removed": r["removed"],
                   "link": "", "url": "", "state": "ok", "why": "",
                   "status": None}
            if r["removed"]:
                rec["state"] = "removed"
                out.append(rec)
                continue

            target = root / path.lstrip("/")
            try:
                resolved = target.resolve()
            except OSError as e:
                rec.update(state="refused", why=str(e))
                out.append(rec)
                continue

            if root not in resolved.parents and resolved != root:
                rec.update(state="refused",
                           why="resolves outside the repo root")
            elif base == resolved or base in resolved.parents:
                rec.update(state="refused",
                           why="inside this page's own task/ — a link "
                               "cannot point at the link")
            elif not resolved.exists():
                rec.update(state="dangling",
                           why="the task folder no longer exists")
            elif resolved.is_file():
                rec.update(state="refused",
                           why="a file, not a folder; task/ links whole "
                               "task folders, one row per folder")
            elif "tasks" not in resolved.parts:
                rec.update(state="refused",
                           why="no 'tasks' segment in the path — task/ only "
                               "links folders under some project's tasks/ "
                               "tree, so a wrong path fails loud, not quiet")
            else:
                link_name = self._task_link_name(resolved, root)
                link = base / link_name
                if link.exists() and not link.is_symlink():
                    rec.update(state="refused",
                               why="a real file already sits at %s; the "
                                   "minter never overwrites what it did not "
                                   "mint" % link_name)
                else:
                    link.parent.mkdir(parents=True, exist_ok=True)
                    link.symlink_to(os.path.relpath(resolved, link.parent))
                    rec["link"] = link_name
                    rec["url"] = self._url_of(link) or ""
                    rec["status"] = _task_status(resolved)
            out.append(rec)
        return out

    # ---- POST /_board/task · the refresh ---------------------------------
    def task_refresh(self, p):
        """Mint, then render. No scan-seed: unlike a page id, a task-folder
        path is not a thing this page's own prose names in a matchable
        pattern, so the store is filled by the pen alone (§🗂)."""
        st, err = self._task_state(p)
        if err:
            return None, err
        minted = self._task_mint(st)
        url = self._task_view(st, minted)
        live = [m for m in minted if m["state"] == "ok"]
        bad = [m for m in minted if m["state"] in ("dangling", "refused")]
        return {"ok": True, "url": url, "n": len(live), "bad": len(bad)}, None

    # ---- POST /_board/task-order · the drag -------------------------------
    def task_order(self, p):
        st, err = self._task_state(p)
        if err:
            return None, err
        sent = [x for x in (p.get("order") or []) if x in st["rows"]]
        st["order"] = sent + [x for x in st["order"] if x not in sent]
        self._task_write(st)
        self._task_view(st, self._task_mint(st))
        return {"ok": True, "n": len(sent)}, None

    # ---- POST /_board/task-entry · the pen --------------------------------
    def task_entry(self, p):
        """{link, note?, remove?, restore?}: the person's edits to the list.
        The field is `link`, not `path` — every view merges the board
        context `{path, file}` into its POST body (pagex's own gotcha)."""
        st, err = self._task_state(p)
        if err:
            return None, err
        many = p.get("link")
        many = many if isinstance(many, list) else [many or ""]
        many = [x.strip().lstrip("/") for x in many if x and x.strip()]
        if not many:
            return None, "no task folder path given"
        if len(many) > 1:
            for one in many:
                res, err = self.task_entry(dict(p, link=one))
                if err:
                    return None, err
            return {"ok": True, "n": len(many)}, None
        path = many[0]
        if path in st["rows"]:
            if p.get("remove"):
                st["rows"][path]["removed"] = True
            if p.get("restore"):
                st["rows"][path]["removed"] = False
            if p.get("note"):
                st["rows"][path]["note"] = p["note"].strip()
        else:
            note = (p.get("note") or "").strip()
            root = Path(self.root).resolve()
            target = root / path
            if not target.is_dir():
                return None, "%r is not a folder under the repo root" % path
            st["rows"][path] = {"removed": False, "note": note}
            st["order"].insert(0, path)
        self._task_write(st)
        self._task_view(st, self._task_mint(st))
        return {"ok": True, "path": path}, None

    # ---- the card view -----------------------------------------------------
    def _task_view(self, st, minted):
        rel_store = self._url_of(st["store"])
        shown = [m for m in minted if m["state"] != "removed"]
        removed = [m for m in minted if m["state"] == "removed"]
        bad = [m for m in shown if m["state"] != "ok"]

        rows_html = []
        for m in shown:
            title = _esc(m["path"])
            badge = {"ok": "<span class='ok'>🗂 linked</span>",
                     "dangling": "<span class='bad'>⚠ dangling</span>",
                     "refused": "<span class='bad'>⛔ refused</span>"
                     }[m["state"]]
            note = ("<div class='dsc'>%s</div>" % _esc(m["note"])
                    if m["note"] else "")
            why = ("<div class='dsc bad'>%s</div>" % _esc(m["why"])
                   if m["why"] else "")
            status_html = ""
            if m["status"]:
                s = m["status"]
                status_html = (
                    "<div class='status'>"
                    "<span class='sb'>%s %s</span>"
                    "<span class='fact'>%s plan.yaml</span>"
                    "<span class='fact'>%s report.yaml</span>"
                    "<span class='fact'>%d QA file%s</span>"
                    "<span class='fact'>%s</span>"
                    "</div>"
                    % (s["badge"], _esc(s["label"]),
                       "✅" if s["plan"] else "⬜",
                       "✅" if s["report"] else "⬜",
                       s["qa_n"], "" if s["qa_n"] == 1 else "s",
                       _esc(s["age"] or "no files")))
            link_html = ("<div class='dsc'><a href='%s' target='_blank'>"
                         "open %s/</a></div>" % (_esc(m["url"]), _esc(m["link"]))
                         if m["url"] else "")
            rows_html.append(
                "<div class='row' draggable='true' data-n='%s'>"
                "<div class='rl'><span class='grip' title='drag to rank'>⠿"
                "</span><code>%s</code> %s</div>"
                "<div class='rr'><button class='rm' data-n='%s' "
                "title='drop this task folder'>✕</button></div>"
                "%s%s%s%s</div>"
                % (_esc(m["path"]), title, badge, _esc(m["path"]),
                   status_html, note, link_html, why))
        cards = ("<div id='cards'>%s</div>" % "".join(rows_html) if rows_html
                 else "<p class='mut'>no task folder linked yet — "
                      "＋ link one below, a repo-relative path to a folder "
                      "under some project's <code>tasks/</code> tree.</p>")

        head = ("<div class='bar'><b>🗂 %s</b><span class='mut'>· %d task "
                "folder%s%s · top = most load-bearing</span>"
                "<span class='sp'></span><button id='refresh'>♻ re-mint"
                "</button><a href='%s' download>⬇ store</a></div>"
                % (_esc(st["stem"]), len(shown), "" if len(shown) == 1 else "s",
                   (" · <b class='bad'>%d need attention</b>" % len(bad))
                   if bad else "", rel_store))

        finder = ("<details open><summary class='mut'>＋ link a task folder"
                  "</summary><div class='pick'>"
                  "<input id='newpath' placeholder='repo-relative path to a "
                  "task folder, e.g. examples/Project-X/tasks/A01_group/"
                  "B02_unit' style='min-width:62%'>"
                  "<input id='newnote' placeholder='note (optional)'>"
                  "<button id='addlink'>link</button></div>"
                  "<p class='mut'>No auto-seed: a task folder is not a page "
                  "id this page's prose can be scanned for, so every row is "
                  "typed here on purpose.</p></details>")

        rmv = ""
        if removed:
            rmv = ("<details><summary class='mut'>🚫 removed · %d</summary>%s"
                   "</details>"
                   % (len(removed), "".join(
                       "<div>🚫 <code>%s</code> <button class='rst' "
                       "data-n='%s'>↩ restore</button></div>"
                       % (_esc(m["path"]), _esc(m["path"])) for m in removed)))

        script = """<script>
var CTX = {path: __PATH__, file: __FILE__};
function post(route, body) {
  Object.assign(body, CTX);
  fetch('/_board/' + route, {method: 'POST',
    headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)})
    .then(function (r) { return r.json(); })
    .then(function (j) {
      if (!j.ok) { alert('\\u26a0 ' + (j.err || route)); return; }
      location.reload();
    })
    .catch(function (e) { alert('\\u26a0 ' + e); });
}
document.addEventListener('click', function (ev) {
  var b = ev.target;
  if (b.id === 'refresh') return post('task', {});
  if (b.id === 'addlink')
    return post('task-entry', {
      link: document.getElementById('newpath').value,
      note: document.getElementById('newnote').value});
  if (!b.dataset || !b.dataset.n) return;
  if (b.className === 'rm')  return post('task-entry', {link: b.dataset.n, remove: true});
  if (b.className === 'rst') return post('task-entry', {link: b.dataset.n, restore: true});
});
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
  r.parentNode.insertBefore(drag, (ev.clientY - box.top) < box.height / 2
                                  ? r : r.nextSibling);
  moved = true;
});
document.addEventListener('drop', function (ev) { ev.preventDefault(); });
document.addEventListener('dragend', function () {
  if (!drag) return;
  drag.classList.remove('drag');
  drag = null;
  if (!moved) return;
  var out = [];
  Array.prototype.forEach.call(document.querySelectorAll('#cards .row'),
    function (r) { out.push(r.dataset.n); });
  post('task-order', {order: out});
});
</script>"""
        script = (script.replace("__PATH__", self._json(st["ctx"]["path"]))
                        .replace("__FILE__", self._json(st["ctx"]["file"])))
        css = ("<style>"
               "body{padding:12px 16px}"
               "button{cursor:pointer;border:1px solid var(--line);"
               "background:var(--card);color:var(--fg);border-radius:6px;"
               "padding:3px 9px;font:500 12.5px -apple-system,sans-serif}"
               "input{border:1px solid var(--line);border-radius:6px;"
               "padding:4px 7px;background:var(--card);color:var(--fg);"
               "font:12px ui-monospace,Menlo,monospace;max-width:62%}"
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
               ".rl code{font-size:12.5px;word-break:break-all}"
               ".rr{margin-left:auto;display:flex;gap:6px}"
               ".dsc{flex-basis:100%;line-height:1.5;font-size:12.5px}"
               ".status{flex-basis:100%;display:flex;gap:8px;flex-wrap:wrap;"
               "align-items:center;margin:2px 0}"
               ".sb{font:600 12.5px -apple-system,sans-serif}"
               ".fact{font-size:11px;color:var(--mut);border:1px solid "
               "var(--line);border-radius:999px;padding:1px 8px}"
               ".ok{color:#2c7a4b;font-size:12px}"
               ".bad{color:#c0392b;font-size:12px}"
               "summary{cursor:pointer;margin:8px 0}"
               ".pick{display:flex;gap:6px;margin-top:5px;flex-wrap:wrap}"
               "</style>")
        view = st["dir"] / (st["stem"] + "-view.html")
        view.write_text(_VIEW.format(title=_esc(st["stem"] + " · task"),
                                     body=css + head + cards + finder + rmv
                                     + script),
                        encoding="utf-8")
        return self._url_of(view)

    @staticmethod
    def _json(s):
        import json
        return json.dumps(s or "")
