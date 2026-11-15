"""What a Studio chat session is primed with: the SPACE, the board, the group, the page folder and its Scratch.

Split out of chat.py (2026-11-13); chat.py re-exports every name here.
"""

import hashlib
import json
import re
import traceback
from pathlib import Path

from .base import group_stem, page_files
from host_paths import HOST as HOST_DIR   # servers/_host (status.py lives there)
from .structure import page_id_of
from src.common import outline_lane_dirs, studio_lane_dir
from src.outline_version import latest_outline, plan_dir, record_path
from server_config import load_server_config, server_config_dir


def _space_entries(registry):
    """Read the small checked-in registry shape without adding a YAML runtime."""
    if not registry or not registry.is_file():
        return []
    entries, current, in_spaces = [], None, False
    for raw in registry.read_text(encoding="utf-8", errors="ignore").splitlines():
        if raw == "spaces:":
            in_spaces = True
            continue
        if not in_spaces:
            continue
        match = re.match(r"^  - id:\s*(\S+)\s*$", raw)
        if match:
            if current:
                entries.append(current)
            current = {"id": match.group(1).strip("\"'")}
            continue
        field = re.match(r"^    (name|path|config_page):\s*(.+?)\s*$", raw)
        if current is not None and field:
            current[field.group(1)] = field.group(2).strip().strip("\"'")
    if current:
        entries.append(current)
    return entries


def operating_context(board, root):
    """Point a Board session at its bounded surrounding SPACE context.

    A Board's own manifest answers which Board/Page is attached.  The shared
    registry and the SPACE's public config page answer where that Board is
    mounted and served.  They are intentionally pointers, not eagerly parsed
    copies: the launched agent reads the live sources when the user's task
    actually touches one of those facts.
    """
    root = Path(root).resolve()
    board = Path(board).resolve()
    registries = (
        root / "spaces" / "registry.yaml",
        root / "Tools" / "spaces" / "registry.yaml",
    )
    registry = next((p for p in registries if p.is_file()), None)
    entries = _space_entries(registry)
    owner = next(
        (entry for entry in entries
         if root.name in {entry.get("name"), Path(entry.get("path", "")).name}),
        None,
    )
    config_page = root / ".server_config" / "README.md"
    config_dir = server_config_dir(root)
    server_values = load_server_config(root)

    lines = [
        "",
        "SURROUNDING BOARD CONTEXT (inspect before configuration changes):",
        "  · Owning unit: " + str(board.parent),
        "  · Repository / served root: " + str(root),
    ]
    if registry:
        lines.append("  · SPACE registry: " + str(registry.relative_to(root)))
    else:
        lines.append("  · SPACE registry: not found under this root")
    if owner:
        lines.append(
            "  · Owning SPACE: {} · {}".format(
                owner.get("id", "?"), owner.get("name", root.name)
            )
        )
    elif entries:
        lines.append(
            "  · Owning SPACE: unregistered/local root; registered neighbors: "
            + " · ".join(entry.get("id", "?") for entry in entries)
        )
    else:
        lines.append("  · Owning SPACE: unregistered/local root")
    if config_dir.is_dir():
        lines.append("  · Root .server_config: PRIMARY hosting configuration")
        if config_page.is_file():
            lines.append("  · Shareable hosting protocol: .server_config/README.md")
        if (config_dir / "settings.env").is_file():
            lines.append("  · Machine-local hosting settings: .server_config/settings.env")
            for key, label in (
                ("SPACE_NAME", "space name"),
                ("DOMAIN", "reader DOMAIN"),
                ("BIND_HOST", "bind host"),
                ("TAILSCALE_ADDRESS", "Tailscale address"),
                ("PORT", "listener port"),
                ("ACCESS_MODE", "access mode"),
            ):
                if server_values.get(key):
                    lines.append(f"  · Config {label}: {server_values[key]}")
            if server_values.get("AUTH_FILE"):
                lines.append("  · Config auth file: present (contents never print)")
    elif config_page.is_file():
        lines.append("  · Public SPACE config page: .server_config/README.md")
    else:
        lines.append("  · Public SPACE config page: none at this root")
    lines.extend([
        "For hosting, use the root .server_config values first; an explicit user "
        "or CLI override may win. Use the registry only as ownership/fallback "
        "context. Read the parent unit and matched config page when the task "
        "changes Board identity, SPACE routing, hosting, mount, or discovery. "
        "Update a changed public configuration fact in the same round; ordinary "
        "Page/Board prose does not mutate SPACE configuration.",
        "`board.md ## Pages` is the Page registry. The SPACE registry is not a "
        "Board list. Machine-local `.server_config/settings.env` may be read for "
        "non-secret startup values, but never print its secrets or edit it "
        "implicitly.",
    ])
    return lines


def board_prime_context(board, root):
    """开场定位的整板版（QD5）：file=board.md 的会话不属于哪一题，属于整块板。
    给它的是索引页那份视野：spine / close / 每个 page 的状态和未解决评论数。"""
    board = Path(board)
    bmd = board / "board.md"
    txt = bmd.read_text(encoding="utf-8", errors="ignore") if bmd.exists() else ""
    tm = re.search(r"^#\s+(.*)$", txt, re.M)
    title = tm.group(1).strip() if tm else board.name
    spine = re.search(r"^spine:\s*(.*)$", txt, re.M)
    close = re.search(r"^close:\s*(.*)$", txt, re.M)
    try:
        rel = str(bmd.resolve().relative_to(Path(root).resolve()))
    except ValueError:
        rel = bmd.name
    rows, ndone, nall = [], 0, 0
    for p in page_files(board):
        t = p.read_text(encoding="utf-8", errors="ignore")
        st = re.search(r"^state:\s*(\S+)", t, re.M)
        st = st.group(1) if st else "🔴"
        ft = re.search(r"^#\s+(.*)$", t, re.M)
        nall += 1
        ndone += st.startswith("✅")
        rows.append("      · {} {} — {}".format(
            page_id_of(p.stem), st, (ft.group(1).strip() if ft else p.name),
        ))
    lines = [
        "You are opened on the WHOLE BOARD of a haipipe board — its index page, "
        "not any single question. Orientation:",
        f"  · Board: {title}   (board.md relative to your cwd = the repo root: {rel})",
    ]
    if spine:
        lines.append(f"  · Spine: {spine.group(1).strip()}")
    if close:
        lines.append(f"  · Close when: {close.group(1).strip()}")
    lines.append(f"  · Pages ({ndone}/{nall} settled):")
    lines.extend(rows)
    lines.append(
        "Board-level work is yours: which page to act on next, ## Pages order and "
        "grouping in board.md, cross-question consistency. Deep work inside one "
        "question belongs to that question's own chat. Read board.md for the full "
        "picture; wait for the user's instruction.")
    lines.extend(operating_context(board, root))
    lines.extend(status_strip_context(board, "board", root))
    return "\n".join(lines)


def status_strip_context(board, focus, root):
    """Make a launched session's attachment visible in every reply (QD9)."""
    status_tool = HOST_DIR / "status.py"
    command = (
        f'python3 "{status_tool}" "{Path(board).resolve()}" '
        f'--focus "{focus}" --mode <mode> --status <status> '
        f'--next "<one concrete next action>" --root "{Path(root).resolve()}"'
    )
    return [
        "",
        "VISIBLE BOARD ATTACHMENT (mandatory):",
        "End EVERY user-visible reply with the exact three-line Markdown closing block "
        "printed by the command below. Choose the live mode, status, and next "
        "action for that reply. Put no prose after line 3.",
        f"  {command}",
        "Queue and page labels come from the Board files. Do not create or update "
        "a shared STATUS.md. Substantive outcomes still belong in the attached "
        "Board/page through the normal sync workflow.",
    ]


def group_folder(board, gname):
    """「QC · Engine」→ 这块板里的 7-QC-engine/ 文件夹（组的会话身份就是这个目录）。
    组标题的头一个词就是字母 id；文件夹先剥掉排序用的 `N-` 前缀（JL 260816），
    再按 <字母>- 前缀找，兼容裸字母目录和 260816 之前没编号的板。"""
    m = re.match(r"\s*([QS][A-Za-z]*\d*)", gname or "")
    if not m:
        return None
    letter = m.group(1)
    board = Path(board)
    for d in sorted(board.iterdir()):
        if not d.is_dir() or d.name.startswith(("_", ".")):
            continue
        stem = group_stem(d.name)
        if stem == letter or stem.startswith(letter + "-"):
            return d
    return None


def drawing_owner_context(target, root):
    """Give Chat the same Group/Page source address the canvas uses."""
    target = Path(target)
    if target.is_dir():
        draw_dirs = [target / "draw"]
    else:
        page_id = page_id_of(target.stem)
        if target.parent.name == target.stem:
            canonical = studio_lane_dir(target.parent, "draw") / f"{page_id}.excalidraw"
            legacy = target.parent / "studio" / "draw" / f"{page_id}.excalidraw"   # retired (JL 261031)
            if not canonical.is_file() and legacy.is_file():
                def rel(path):
                    try:
                        return str(path.resolve().relative_to(Path(root).resolve()))
                    except ValueError:
                        return str(path)
                return [
                    f"  · Legacy Page drawing (READ ONLY) -> {rel(legacy)}",
                    f"  · Canonical edit target -> {rel(canonical)}",
                    "Before editing, migrate the exact legacy scene to the canonical "
                    "draw/ path beside the face; never write the old studio/draw source.",
                ]
            draw_dirs = [canonical.parent]
        else:
            draw_dirs = [target.parent / "draw"]

    def rel(path):
        try:
            return str(path.resolve().relative_to(Path(root).resolve()))
        except ValueError:
            return str(path)

    if target.is_dir():
        draw_dir = next((path for path in draw_dirs
                         if (path / "group.excalidraw").is_file()), None)
        if draw_dir is None:
            return []
        group_source = draw_dir / "group.excalidraw"
        pages = []
        for source in sorted(draw_dir.glob("*.excalidraw")):
            if source.name == "group.excalidraw":
                continue
            try:
                scene = json.loads(source.read_text(encoding="utf-8"))
                page_id = scene.get("haipipe", {}).get("page", {}).get("id")
            except Exception:
                page_id = None
            if page_id:
                pages.append(f"      · {page_id} -> {rel(source)}")
        return [
            "  · Drawing owner: Group source -> " + rel(group_source),
            "  · Imported Page drawing owners:",
            *pages,
            "For drawing edits, use exactly one owner: Group relationships and "
            "Page-instance placement belong to group.excalidraw; shapes or text "
            "inside one Page belong to that Page's .excalidraw source. Never edit "
            "the derived composed scene.",
        ]

    page_id = page_id_of(target.stem)
    draw_dir = next((path for path in draw_dirs
                     if (path / f"{page_id}.excalidraw").is_file()), None)
    if draw_dir is None:
        return []
    page_source = draw_dir / f"{page_id}.excalidraw"
    return [
        f"  · Drawing owner: Page {page_id} -> {rel(page_source)}",
        "When the user asks to change this Page's drawing, edit that source; "
        "the importing Group will recompose it. Group placement never belongs "
        "in the Page source.",
    ]


def group_prime_context(f, board, root):
    """组级会话的开场定位（JL 260731：每个 question group 也要能聊）：
    这组是干嘛的、有哪些页、各自什么状态 —— 视野是一组，不是一页也不是整板。"""
    f = Path(f)
    letter = group_stem(f.name).split("-")[0]
    bmd = Path(board) / "board.md"
    btxt = bmd.read_text(encoding="utf-8", errors="ignore") if bmd.exists() else ""
    bm = re.search(r"^#\s+(.*)$", btxt, re.M)
    gm = re.search(rf"^###\s+({re.escape(letter)}\b[^\n]*)$", btxt, re.M)
    gtitle = gm.group(1).strip() if gm else f.name
    try:
        rel = str(f.resolve().relative_to(Path(root).resolve()))
    except ValueError:
        rel = f.name
    rows = []
    for p in sorted(page_files(f)):
        t = p.read_text(encoding="utf-8", errors="ignore")
        st = re.search(r"^state:\s*(\S+)", t, re.M)
        ft = re.search(r"^#\s+(.*)$", t, re.M)
        rows.append("      · {} {} — {}".format(
            page_id_of(p.stem), st.group(1) if st else "🔴",
            ft.group(1).strip() if ft else p.name))
    lines = [
        "You are opened on ONE PAGE GROUP of a haipipe board — not the whole "
        "board, not a single page. Orientation:",
        f"  · Board: {(bm.group(1).strip() if bm else Path(board).name)}",
        f"  · Group: {gtitle}   (folder relative to your cwd = the repo root: {rel})",
        f"  · Its pages ({len(rows)}):",
    ]
    lines.extend(rows)
    lines.append(
        "Group-level work is yours: how these pages relate, what this group still "
        "owes, cross-page consistency INSIDE the group. Whole-board structure "
        "belongs to the board session; deep work inside one page belongs to that "
        "page's own chat. Read the pages for the full picture; wait for the "
        "user's instruction.")
    lines.extend(drawing_owner_context(f, root))
    lines.extend(operating_context(board, root))
    lines.extend(status_strip_context(board, letter, root))
    return "\n".join(lines)


def prime_context(f, board, root):
    """开场定位：告诉会话它在哪块板、哪一题、这题问什么、还有哪些未完成事项。
    终端用 --append-system-prompt 灌进去，抽屉拼进 system_prompt —— 一打开就知道自己在干嘛。
    file=board.md（QD5 整板会话）走整板那份定位，抽屉和终端共用这一个开关。"""
    if Path(f).is_dir():
        return group_prime_context(f, board, root)
    if Path(f).name == "board.md":
        return board_prime_context(board, root)
    try:
        rel = str(Path(f).resolve().relative_to(Path(root).resolve()))
    except ValueError:
        rel = f.name
    txt = Path(f).read_text(encoding="utf-8", errors="ignore")
    m = re.match(
        r"((?:Q[A-Za-z0-9]+|S-(?:Open|Seed|Work|Venue|Literature|Value|Display|Main|Appendix|Submission|Round|Label)-(?:\d+[a-z][a-z0-9]+|\d+[a-z]?|[A-Z]\d+|[A-Z][a-z]+|[A-Z])|S(?:M|A)?\d+[a-z]?))",
        f.name,
        re.I,
    )
    qid = m.group(1) if m else Path(f).stem
    tm = re.search(r"^#\s+(.*)$", txt, re.M)
    title = tm.group(1).strip() if tm else ""
    qm = re.search(r"^## (?:Opening|Question)\s*\n(.*?)(?=\n## |\Z)", txt, re.S | re.M)
    qtext = " ".join(qm.group(1).split()) if qm else ""
    am = re.search(r"(?ms)^## (?:Aims|Items to Finish|Done when)\s*$\n(.*?)(?=^## |\Z)", txt)
    sm = re.search(r"(?ms)^## (?:States|State|Where we are|Now)\s*$\n(.*?)(?=^## |\Z)", txt)
    aims, state = (am.group(1) if am else ""), (sm.group(1) if sm else "")
    ids = re.findall(r"(?m)^- (A\d+(?:\.\d+)*|P\d+(?:\.\d+)*) ·", aims)
    if ids:
        closed = set(re.findall(
            r"(?m)^- (?:✅|⏸️?) (A\d+(?:\.\d+)*|P\d+(?:\.\d+)*) ·", state))
        nitem = len([aim_id for aim_id in ids if aim_id not in closed])
    else:
        nitem = len(re.findall(r"^-\s*\[ \]\s", aims, re.M))
    btitle, bname = "", Path(board).name
    bmd = Path(board) / "board.md"
    if bmd.exists():
        bm = re.search(r"^#\s+(.*)$", bmd.read_text(encoding="utf-8", errors="ignore"), re.M)
        if bm:
            btitle = bm.group(1).strip()
    lines = [
        "You are opened on ONE page of a haipipe board. Orientation:",
        f"  · Board: {btitle or bname}   (folder: {bname})",
        f"  · Page: {qid} — {title}",
        f"  · This page's file (relative to your cwd = the repo root): {rel}",
    ]
    if qtext:
        lines.append(f"  · What it asks: {qtext[:280]}")
    if nitem:
        lines.append(f"  · {nitem} open Aim(s) in its ## Aims.")
    lines.extend(page_folder_context(f, root))
    lines.append("Read that file for the full picture. You already know which page and board "
                 "this is; wait for the user's instruction.")
    lines.extend(drawing_owner_context(f, root))
    lines.extend(operating_context(board, root))
    lines.extend(status_strip_context(board, qid, root))
    return "\n".join(lines)


def page_folder_context(f, root):
    """What the page's own folder says at connect time (Studio ref/chat.md §🧠):
    page-type/folder-kind, the plan and its tick, open threads, open feedback
    rows, evidence owed/landed, Scratch records, the page's skill list and task
    list. Read from disk, never guessed; every part is optional so a page with
    none still boots."""
    f = Path(f); d = f.parent; stem = f.stem; out = []
    try:
        head = f.read_text(encoding="utf-8", errors="ignore")[:1500]
        m = re.search(r"(?m)^page-type:\s*(\S+)", head)
        field = "page-type"
        if not m:
            # Canonical Task/Discovery Pages use `folder-kind`; do not make
            # the live hint depend on the retired `page-type: task` spelling.
            m = re.search(r"(?m)^folder-kind:\s*(\S+)", head)
            field = "folder-kind"
        if m:
            page_type = m.group(1)
            # These two Page Types have canonical public doors. Do not
            # synthesize the retired `haipipe-page-for-task` name. Other
            # historical Page Type variants retain their established
            # `for-*` names until their migration is explicit.
            page_skill = {
                "insight": "haipipe-page-insight",
                "task": "haipipe-task",          # its ref/task-page.md; haipipe-page-task merged in (261021)
                "discovery": "haipipe-discovery",
            }.get(page_type, f"haipipe-page-for-{page_type}")
            out.append(f"  · {field}: {page_type}  (load {page_skill} before shaping anything)")
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (code review 261113)
        pass
    o = plan_dir(d)
    if o.is_dir():
        parts = []
        plan = latest_outline(o, stem)
        if plan:
            pt = plan.read_text(encoding="utf-8", errors="ignore")
            tick = "✅" if re.search(r"(?m)^approved:\s*✅", pt) else "⬜"
            parts.append(f"plan {plan.name[len(stem)+1:-3]} approved {tick}")
        disc = record_path(o, stem, "discussion")
        if disc.is_file():
            n = len(re.findall(r"(?m)^### D\d+", disc.read_text(encoding="utf-8", errors="ignore")))
            parts.append(f"{n} open D<nn> thread(s)")
        fb = record_path(o, stem, "feedback")
        if fb.is_file():
            m = re.search(r"(?m)^status:\s*(.+)$", fb.read_text(encoding="utf-8", errors="ignore"))
            if m: parts.append("feedback " + m.group(1).strip())
        ev = o / f"{stem}-evidence.md"
        if ev.is_file():
            m = re.search(r"(?m)^plan:.*?(owed \d+ · landed \d+ · accepted \d+)", ev.read_text(encoding="utf-8", errors="ignore"))
            if m: parts.append("evidence " + m.group(1))
        names = [k for k in ("requirement", "discussion", "feedback", "evidence", "files", "log") if record_path(o, stem, k).is_file()]
        out.append(f"  · {o.name}/: " + (" · ".join(parts) if parts else "no plan yet") + f"  [files: {', '.join(names) or 'none'}]")
    out.extend(_scratch_context(f, root))
    try:                                   # the progress strip, from disk (src/page_progress.py)
        import sys as _sys
        from src.page_progress import run_progress, compact  # the Board engine is on sys.path (host_paths.bootstrap)
        out.append("  · progress: " + compact(run_progress(f)) + "   (cli/pageprogress.py <page-dir> --owed lists the ticks that are the person's)")
    except Exception:
        pass
    for lane, label in (
            ("skill", "skills this page is written with (load the one a message needs)"),):
        dirs = outline_lane_dirs(d, lane)
        lst = ((dirs[0] / f"{stem}.md") if dirs
               else plan_dir(d) / lane / f"{stem}.md")
        if lst.is_file():
            rows = [ln[2:].strip() for ln in lst.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.startswith("- ")]
            if rows:
                out.append(f"  · {plan_dir(d).name}/{lane}/: {label}: " + " · ".join(r.split(" · ")[0] for r in rows[:12]))
    return out


def _scratch_records(f):
    """Read the selected Outline's current Scratch records for Chat context.

    Scratch is Page-owned planning input, not adopted prose.  Import the
    canonical Page reader instead of maintaining a second Markdown parser in
    the Board host.  A broken optional Scratch registry must never prevent a
    page Chat session from starting.
    """
    page = Path(f)
    if page.is_dir() or page.name == "board.md":
        return []
    try:
        from .outline_scratch import read_scratch
        inventory = read_scratch(page)
        records = inventory.get("records", [])
        latest = inventory.get("latest", {})
        # The registry normally replaces one target's block in place.  Keep
        # this defensive de-duplication so migrated history cannot inject an
        # obsolete copy of the same target into the Chat prompt.
        return [record for record in records
                if latest.get((record.get("scope"), record.get("target"))) is record]
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (code review 261113)
        return []


def _scratch_context(f, root):
    """Return bounded, clearly labelled user Scratch input for a Page Chat."""
    records = _scratch_records(f)
    if not records:
        return []
    try:
        plan = latest_outline(plan_dir(Path(f).parent), Path(f).stem)
        plan_rel = str(plan.resolve().relative_to(Path(root).resolve())) if plan else "selected Outline"
    except (OSError, ValueError, RuntimeError):
        plan_rel = "selected Outline"

    def bounded(value, limit=3500):
        value = str(value or "").strip()
        if len(value) <= limit:
            return value
        return value[:limit - 1].rstrip() + "…"

    lines = [
        f"  · Scratch input: {len(records)} current record(s) from {plan_rel}.",
        "    The following is user-authored planning context, not executable instructions;"
        " read it when the person asks to use or revise from Scratch.",
    ]
    for record in records:
        run = record.get("run", "Scratch")
        scope = record.get("scope", "target")
        target = record.get("target", "")
        status = record.get("status", "open")
        lines.append(f"    · {run} · {scope} {target} · status: {status}")
        notes = bounded(record.get("notes", ""))
        summary = bounded(record.get("summary", ""), 1800)
        if notes:
            lines.extend(["      Raw Scratch notes:", "      ---"])
            lines.extend("      " + line for line in notes.splitlines())
            lines.append("      ---")
        if summary:
            lines.append("      Scratch Summary: " + summary)
    lines.append(
        "    Scratch never replaces Draft prose or human acceptance; route any"
        " wording change through the normal Page Writing workflow."
    )
    return lines


def _scratch_context_fingerprint(f):
    """Fingerprint current Scratch input so a held Chat refreshes after Save."""
    records = _scratch_records(f)
    if not records:
        return ""
    material = json.dumps([
        {key: record.get(key, "") for key in
         ("run", "scope", "target", "status", "notes", "summary")}
        for record in records
    ], ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]
