#!/usr/bin/env python3
"""create_section_sessions.py · one named Claude session and one named Codex
thread per Section Page, paired.

`/haipipe-paper sessions` runs this once the Story's C8 Section Narrative has
fixed the Section structure. Contract: ../ref/section-sessions.md.

    python create_section_sessions.py <paper-root> --prefix <Short>            # plan only
    python create_section_sessions.py <paper-root> --prefix <Short> --apply    # create
        [--providers claude,codex] [--appendix one|each] [--pages <page id> ...]
        [--replace] [--keep-running] [--codex-map FILE] [--wait 900]

A unit is what one session owns: each Main Section Page, and the whole
Appendix group as one unit (--appendix one, the default: appendix pages are
small and share letters, table numbers and cross-appendix rulings; --appendix
each gives every appendix page its own). For each unit:
  1. Claude: start `claude --bg -n <Short>-<unit>` from the repository root
     with a read-only first turn scoped to that unit, write its UUID into each
     page header's `session:` line, and `claude stop` it once that turn is idle,
     because `/resume` refuses a session still running in the background;
  2. Codex: start a thread through `codex app-server` (so it is interactive-
     sourced and shows in the Codex app), name it `<Short>-<unit>-Codex`
     with `thread/name/set`, run the same first turn, and write its id into the
     page header's `codex-session:` line;
  3. register an identity-only call-peer pair `<Short>-<unit>` binding the
     two. --codex-map binds existing Codex threads instead of creating new ones.

Without --apply it prints the plan and changes nothing. A provider whose
header line already names an existing session is skipped unless --replace.
"""
import argparse
import itertools
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAIR_SYNC = HERE.parents[2] / "0_utils" / "call-peer" / "scripts" / "pair_sync.py"


def repo_root(start):
    for p in [start, *start.parents]:
        if (p / "pyproject.toml").exists() and (p / "Tools").exists():
            return p
    sys.exit(f"no repository root (pyproject.toml + Tools/) above {start}")


def claude_title(sid):
    """The session's saved name, or None when no transcript exists. A page copied
    from a predecessor paper keeps that paper's `session:`; only a session whose
    name is this unit's name is treated as the unit's owner."""
    home = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
    for f in (home / "projects").glob(f"*/{sid}.jsonl"):
        title = ""
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if '"custom-title"' in line:
                try:
                    title = json.loads(line).get("customTitle", title)
                except ValueError:
                    pass
        return title
    return None


def board_prefix(paper):
    return header_value(paper / "board.md", "session-prefix")


def record_prefix(paper, prefix):
    """Keep the chosen prefix in board.md so every later run names sessions the same way."""
    md = paper / "board.md"
    lines = md.read_text(encoding="utf-8").split("\n")
    head = range(min(25, len(lines)))
    after = next((i for key in ("dialect:", "paper-root:", "source:") for i in head
                  if lines[i].startswith(key)), None)
    if after is None:
        after = next((i for i in head if lines[i].startswith("# ")), 0)
    lines.insert(after + 1, f"session-prefix: {prefix}")
    md.write_text("\n".join(lines), encoding="utf-8")


def codex_live(tid):
    return codex_name(tid) is not None


def codex_name(tid):
    """The thread's latest name in the Codex session index, "" when unnamed, None when absent."""
    index = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "session_index.jsonl"
    try:
        text = index.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    name = None
    for line in text.splitlines():
        if f'"{tid}"' in line:
            try:
                name = json.loads(line).get("thread_name") or ""
            except ValueError:
                name = name or ""
    return name


def appendix_pair(unit_name, page_id):
    """`<Short>-Appendix-<letter>` for `S-<desk>-Appendix-<letter>-<slug>`, else `<Short>-Appendix-<page id>`."""
    m = re.search(r"-Appendix-([A-Z])(?:-|$)", page_id)
    return f"{unit_name}-{m.group(1) if m else page_id}"


def paired_codex(root, sid):
    """The Codex thread already paired to this Claude session in a call-peer
    manifest for this workspace (exact id match), else ("", "")."""
    pairs = Path(os.environ.get("HAIPIPE_PAIRS_DIR", Path.home() / ".config" / "haipipe" / "pairs"))
    for f in sorted(pairs.glob("*.json")) if sid else []:
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(j, dict):
            continue
        prov = j.get("providers") or {}
        if j.get("cwd") == str(root) and (prov.get("claude") or {}).get("session_id") == sid:
            cx = prov.get("codex") or {}
            return cx.get("session_id", ""), cx.get("session_name", "")
    return "", ""


def compile_order(paper):
    """Section ids in the Story's `haipipe:compile-order` block, in order."""
    for story in sorted(paper.glob("A1-Story/Story*/Story*.md")):
        text = story.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<!-- haipipe:compile-order:start -->(.*?)<!-- haipipe:compile-order:end -->", text, re.S)
        if m:
            return story, re.findall(r"^\s*-\s*(S-[\w-]+)\s*$", m.group(1), re.M)
    return None, []


def section_pages(paper):
    """Every S- page folder in a Main or Appendix group: (id, <group>/<id>/<id>.md, group, is_appendix)."""
    out = []
    for group in sorted(paper.glob("B?-*-Main")) + sorted(paper.glob("B?-*-Appendix")):
        for d in sorted(group.glob("S-*")):
            md = d / f"{d.name}.md"
            if md.is_file():
                out.append((d.name, md, group, group.name.endswith("-Appendix")))
    return out


def build_units(pages, appendix):
    """A unit is what one session owns: one Main page, or with --appendix one
    (the default) the whole Appendix group, whose pages are small and coupled
    (shared letters, table numbers and cross-appendix rulings)."""
    units, appx, appx_group = [], [], None
    for pid, md, group, is_appx in pages:
        if is_appx and appendix == "one":
            appx.append((pid, md))
            appx_group = group
        else:
            units.append({"key": pid, "pages": [(pid, md)], "folder": md.parent})
    if appx:
        units.append({"key": "Appendix", "pages": appx, "folder": appx_group})
    return units


def unit_header(unit, key):
    """The unit's current id for `key`: the one value every page carries, else ""."""
    vals = {header_value(md, key) for _, md in unit["pages"]}
    return vals.pop() if len(vals) == 1 else ""


def header_value(md, key):
    for line in md.read_text(encoding="utf-8", errors="replace").splitlines()[:25]:
        if line.startswith(key + ":"):
            return line.split(":", 1)[1].strip()
    return ""


def write_header(md, key, value):
    """Replace the header's `<key>:` line, or add it after `session:` / `method:` / `owner:`."""
    lines = md.read_text(encoding="utf-8").split("\n")
    head = range(min(25, len(lines)))
    hit = [i for i in head if lines[i].startswith(key + ":")]
    if hit:
        lines[hit[0]] = f"{key}: {value}"
    else:
        after = next((idx for anchor in ("session:", "method:", "owner:")
                      for idx in [i for i in head if lines[i].startswith(anchor)][:1]), None)
        if after is None:
            raise RuntimeError(f"{md}: no header `method:` or `owner:` line to anchor `{key}:`")
        lines.insert(after + 1, f"{key}: {value}")
    md.write_text("\n".join(lines), encoding="utf-8")


def first_prompt(root, paper, unit, story):
    rel = lambda p: p.relative_to(root)
    if len(unit["pages"]) == 1 and unit["key"] != "Appendix":
        page_id, md = unit["pages"][0]
        head = f"""You are the owning session for ONE Section Page of the paper {paper.name}.

Your page: {rel(md)}
Your folder: {rel(unit['folder'])}/  (draft/, results/, runs/, delivery/ are yours)
Your brief: the row for {page_id} in the Section Narrative (C8) of {rel(story)}"""
        own, first = "your own page folder", "read your page, its Story C8 row, and the newest file in draft/"
        line1 = "this page's state in one line"
    else:
        listed = "\n".join(f"  - {rel(md)}" for _, md in unit["pages"])
        head = f"""You are the owning session for the WHOLE APPENDIX of the paper {paper.name}: every Section Page in one group.

Your pages:
{listed}
Your folder: {rel(unit['folder'])}/  (each page's draft/, results/, runs/, delivery/ are yours)
Your brief: the Appendix rows of the Section Narrative (C8) of {rel(story)}; its compile-order block says which appendices print"""
        own, first = "the Appendix group folder", "read each appendix page, its Story C8 row, and the newest file in its draft/"
        line1 = "the Appendix's state in one line"
    return f"""{head}
Paper map: {rel(paper / 'board.md')}

Scope rules:
1. Write only inside {own}. Other pages' problems: list them, never fix them.
2. Never edit Tools/, code/, the Story page, or the paper-level delivery/ unless the author asks.
3. Never start a compute or regression Run unasked.
4. Before any edit, load the haipipe-paper-section skill (and haipipe-page for the page contract).
5. While the author has a Run open, edit only the Draft file draft/<stem>-draft-v<N>.md; Page Content, logs, receipts, results/ and delivery wait for the Run's close.

First turn, READ ONLY: {first}. Then reply: line 1 = {line1}; then a numbered list of what is done, what is open, and the one next step. Then stop and wait."""


# ---------------------------------------------------------------- Claude
def agents():
    try:
        out = subprocess.run(["claude", "agents", "--json"], capture_output=True, text=True, timeout=60).stdout
        return json.loads(out or "[]")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return []


def claude_launch(root, name, prompt):
    r = subprocess.run(["claude", "--bg", "-n", name, prompt], cwd=root,
                       capture_output=True, text=True, timeout=120)
    m = re.search(r"backgrounded\s*·\s*([0-9a-f]{8})", r.stdout + r.stderr)
    if not m:
        raise RuntimeError(f"{name}: claude --bg gave no session id:\n{(r.stdout + r.stderr)[-400:]}")
    short = m.group(1)
    for _ in range(30):
        full = next((a.get("sessionId") for a in agents() if a.get("id") == short), None)
        if full:
            return short, full
        time.sleep(1)
    raise RuntimeError(f"{name}: session {short} not listed by `claude agents --json`")


def claude_stop_when_idle(shorts, deadline):
    """Stop each background session once its first turn is idle; return those still busy."""
    left = set(shorts)
    while left and time.time() < deadline:
        live = {a.get("id"): a for a in agents()}
        for s in list(left):
            a = live.get(s)
            if a is None:
                left.discard(s)
            elif a.get("kind") == "background" and a.get("status") == "idle":
                subprocess.run(["claude", "stop", s], capture_output=True, timeout=60)
                left.discard(s)
        if left:
            time.sleep(15)
    return left


# ---------------------------------------------------------------- Codex
class CodexAppServer:
    """Minimal JSON-RPC client over `codex app-server` stdio. A thread started
    here is app-server sourced, so the Codex app lists it; `codex exec` threads
    are not listed and cannot be named from the CLI."""

    DECLINE = {"item/commandExecution/requestApproval": {"decision": "decline"},
               "item/fileChange/requestApproval": {"decision": "decline"},
               "execCommandApproval": {"decision": "denied"},
               "applyPatchApproval": {"decision": "denied"}}

    def __init__(self, root):
        self.p = subprocess.Popen(["codex", "app-server"], cwd=root, stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
        self.ids, self.q, self.done = itertools.count(1), queue.Queue(), {}
        threading.Thread(target=self._read, daemon=True).start()
        self.call("initialize", {"clientInfo": {"name": "haipipe-paper-sessions", "version": "1.4.0"}})
        self._send({"method": "initialized"})

    def _read(self):
        for line in self.p.stdout:
            try:
                self.q.put(json.loads(line))
            except ValueError:
                continue

    def _send(self, msg):
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()

    def _handle(self, m):
        if "method" in m and "id" in m:          # a server request: this first turn is read-only
            reply = self.DECLINE.get(m["method"])
            self._send({"id": m["id"], "result": reply} if reply else
                       {"id": m["id"], "error": {"code": -32601, "message": "declined by haipipe-paper sessions"}})
        elif m.get("method") == "turn/completed":
            self.done[(m.get("params") or {}).get("threadId")] = True

    def call(self, method, params, timeout=120):
        rid = next(self.ids)
        self._send({"id": rid, "method": method, "params": params})
        end = time.time() + timeout
        while time.time() < end:
            try:
                m = self.q.get(timeout=1)
            except queue.Empty:
                continue
            if m.get("id") == rid and ("result" in m or "error" in m):
                if "error" in m:
                    raise RuntimeError(f"codex {method}: {m['error']}")
                return m["result"]
            self._handle(m)
        raise RuntimeError(f"codex {method}: no reply in {timeout}s")

    def new_thread(self, root, name, prompt):
        tid = self.call("thread/start", {"cwd": str(root)})["thread"]["id"]
        self.call("thread/name/set", {"threadId": tid, "name": name})
        self.call("turn/start", {"threadId": tid, "input": [{"type": "text", "text": prompt}]})
        return tid

    def wait_turns(self, tids, deadline):
        left = set(tids) - set(self.done)
        while left and time.time() < deadline:
            try:
                self._handle(self.q.get(timeout=2))
            except queue.Empty:
                pass
            left = set(tids) - set(self.done)
        return left

    def close(self):
        try:
            self.p.stdin.close()
            self.p.wait(timeout=20)
        except Exception:
            self.p.kill()


def register_pair(root, pair, sid, name, tid, tname):
    cmd = [sys.executable, str(PAIR_SYNC), "register", "--pair-name", pair, "--cwd", str(root),
           "--caller-provider", "claude", "--caller-session-id", sid, "--caller-session-name", name,
           "--callee-provider", "codex", "--callee-session-id", tid]
    if tname:
        cmd += ["--callee-session-name", tname]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode:
        raise RuntimeError(f"{pair}: pair registration failed: {r.stderr.strip()[-300:]}")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", help="the paper root (the folder holding board.md)")
    ap.add_argument("--prefix", help="short paper name; sessions are named <prefix>-<unit>."
                                     " Default: board.md `session-prefix:`; --apply records it there")
    ap.add_argument("--providers", default="claude,codex", help="claude, codex, or claude,codex (default)")
    ap.add_argument("--pages", nargs="*", default=None, help="only these page ids")
    ap.add_argument("--apply", action="store_true", help="create the sessions (default: print the plan)")
    ap.add_argument("--replace", action="store_true", help="create new sessions even where the page names live ones")
    ap.add_argument("--keep-running", action="store_true", help="do not stop Claude sessions after their first turn")
    ap.add_argument("--appendix", choices=["one", "each"], default="one",
                    help="one session for the whole Appendix group (default) or one per appendix page")
    ap.add_argument("--codex-map", help="bind existing Codex threads: '<unit> <thread id> [thread name]' lines;"
                                        " a unit is a page id, or Appendix")
    ap.add_argument("--wait", type=int, default=900, help="seconds to wait for first turns")
    a = ap.parse_args()

    providers = {x.strip() for x in a.providers.split(",") if x.strip()}
    if not providers or providers - {"claude", "codex"}:
        sys.exit("--providers takes claude, codex, or claude,codex")
    paper = Path(a.paper).resolve()
    if not (paper / "board.md").is_file():
        sys.exit(f"{paper}: no board.md; pass the paper root")
    root = repo_root(paper)
    recorded = board_prefix(paper)
    if a.prefix and recorded and a.prefix != recorded:
        sys.exit(f"board.md records session-prefix: {recorded}; use it, or edit board.md first")
    a.prefix = a.prefix or recorded
    if not a.prefix:
        sys.exit("pass --prefix <Short>: two or three words naming this paper, unused by other papers")
    story, order = compile_order(paper)
    if not story or not order:
        sys.exit("no Story `haipipe:compile-order` block: settle the Section structure (Story C8) first")
    pages = section_pages(paper)
    if a.pages:
        wanted = set(a.pages)
        pages = [p for p in pages if p[0] in wanted]
        missing = wanted - {p[0] for p in pages}
        if missing:
            sys.exit("no Section Page folder for: " + ", ".join(sorted(missing)))
    mapped = {}
    if a.codex_map:
        for line in Path(a.codex_map).read_text(encoding="utf-8").splitlines():
            parts = line.split(None, 2)
            if len(parts) >= 2 and not line.lstrip().startswith("#"):
                mapped[parts[0]] = (parts[1], parts[2].strip() if len(parts) > 2 else "")

    plan = []
    for unit in build_units(pages, a.appendix):
        key = unit["key"]
        name = f"{a.prefix}-{key}"
        sid, tid = unit_header(unit, "session"), unit_header(unit, "codex-session")
        title = claude_title(sid) if sid else None
        c_live = title == name                      # owned: this unit's name, not a copied-in session
        foreign = f"  (is '{title or 'unnamed'}', not this unit)" if sid and title is not None and not c_live else ""
        if foreign:
            tid = ""                                # a foreign session's Codex line is not this unit's
        # an Appendix unit may keep one older Codex thread per page; then its Codex side is present
        page_tids = {header_value(md, "codex-session") for _, md in unit["pages"]}
        per_page = not foreign and len(page_tids) > 1 and all(t and codex_live(t) for t in page_tids)
        if c_live and not tid and not per_page and key not in mapped and not a.replace:
            ptid, pname = paired_codex(root, sid)
            if ptid:                                 # already paired: bind it, do not create a second
                mapped[key] = (ptid, pname)
        x_live = per_page or (bool(tid) and codex_live(tid))
        mk_claude = "claude" in providers and (a.replace or not c_live)
        mk_codex = "codex" in providers and key not in mapped and (a.replace or not x_live)
        plan.append((unit, sid, tid, mk_claude, mk_codex, per_page))
        note = "" if key == "Appendix" or key in order else "  (not in compile order)"
        pages_line = "".join(f"\n   · {pid}{'' if pid in order else '  (not in compile order)'}"
                             for pid, _ in unit["pages"]) if key == "Appendix" else ""
        print(f"{a.prefix}-{key}{note}{pages_line}\n"
              f"   claude {'create' if mk_claude else 'keep  '}  session: {sid[:8] or '-'}{' (live)' if c_live else foreign}\n"
              f"   codex  {'create' if mk_codex else ('bind  ' if key in mapped else 'keep  ')}"
              f"  codex-session: {'one per page' if per_page else (mapped.get(key, (tid,))[0] or '-')[:8]}"
              f"{' (live)' if x_live else ''}")

    todo = sum(p[3] + p[4] for p in plan) + sum(1 for p in plan if p[0]["key"] in mapped)
    if not a.apply:
        print(f"\nplan only · {todo} to create or bind · rerun with --apply")
        return
    for tool in (["claude"] if any(p[3] for p in plan) else []) + (["codex"] if any(p[4] for p in plan) else []):
        if subprocess.run([tool, "--version"], capture_output=True).returncode:
            sys.exit(f"the `{tool}` CLI is not on PATH")

    if not recorded:
        record_prefix(paper, a.prefix)
        print(f"board.md · session-prefix: {a.prefix}")
    deadline_for = lambda: time.time() + a.wait
    shorts, threads, codex = [], [], None
    try:
        for unit, sid, tid, mk_claude, mk_codex, per_page in plan:
            key = unit["key"]
            name, prompt = f"{a.prefix}-{key}", first_prompt(root, paper, unit, story)
            if mk_claude:
                short, sid = claude_launch(root, name, prompt)
                for _, md in unit["pages"]:
                    write_header(md, "session", sid)
                shorts.append(short)
                print(f"claude  {name} · {sid}")
            tname = f"{name}-Codex"
            if key in mapped:
                tid, tname = mapped[key][0], mapped[key][1] or tname
                for _, md in unit["pages"]:
                    write_header(md, "codex-session", tid)
                print(f"codex   {name} · bound {tid}")
            elif mk_codex:
                codex = codex or CodexAppServer(root)
                tid = codex.new_thread(root, tname, prompt)
                for _, md in unit["pages"]:
                    write_header(md, "codex-session", tid)
                threads.append(tid)
                print(f"codex   {tname} · {tid}")
            if sid and tid and (mk_claude or mk_codex or key in mapped):
                register_pair(root, name, sid, name, tid, tname)
                print(f"pair    {name} · claude {sid[:8]} ↔ codex {tid[:8]}")
            elif sid and per_page and mk_claude and key not in mapped:
                # an Appendix keeping one older Codex thread per page: one pair per page
                for pid, md in unit["pages"]:
                    ptid = header_value(md, "codex-session")
                    pair = appendix_pair(name, pid)
                    register_pair(root, pair, sid, name, ptid, codex_name(ptid) or "")
                    print(f"pair    {pair} · claude {sid[:8]} ↔ codex {ptid[:8]}")
        deadline = deadline_for()
        if codex and threads:
            busy = codex.wait_turns(threads, deadline)
            print(f"codex first turns done: {len(threads) - len(busy)}/{len(threads)}"
                  + (f"; still running: {' '.join(t[:8] for t in busy)}" if busy else ""))
    finally:
        if codex:
            codex.close()
    if shorts and not a.keep_running:
        busy = claude_stop_when_idle(shorts, deadline_for())
        print(f"claude stopped after first turn: {len(shorts) - len(busy)}/{len(shorts)}"
              + (f"; still busy: {' '.join(sorted(busy))} (run `claude stop <id>` before /resume)" if busy else ""))


if __name__ == "__main__":
    main()
