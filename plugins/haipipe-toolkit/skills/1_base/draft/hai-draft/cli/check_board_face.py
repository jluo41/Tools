"""check_board_face.py: the Board and Page face checks: board.md, its groups, each Page face.
check_board, check_face (which calls check_page_text), check_opening, the name and group-order checks."""
import re
from pathlib import Path

from cli.check_common import (ERROR, SEMANTIC_SECTION_PAGE, WARN, alias_names,  # noqa: E402
                              has_section, outside_checkout, section_text,
                              state_token, strip_fences)
from cli.check_families import _repo_root  # noqa: E402
from cli.check_page_text import (  # noqa: E402
    check_canvas_frames, check_comment_form, check_content_attribution,
    check_discussion_file, check_division_figures, check_duplicate_sections,
    check_evidence_file, check_feedback_coverage, check_fence_balance,
    check_file_paths, check_generated_block, check_group_names, check_one_canvas,
    check_page_type, check_plan_arc, check_related_board_pages,
    check_requirement_file, check_retired_blocks, check_retired_sections,
    check_section_sentences, check_section_writing_requirements,
    check_state_mirrors_aims, page_aims_text)
from src.common import (NUMBERED_GROUP, STN, aim_progress, board_kind,  # noqa: E402
                        group_stem, page_files, registered_page_source)
from src.dialect_task_block import mounted_info  # noqa: E402
from src.dialect_task_block import page_info as task_page_info  # noqa: E402
from src.page_evidence import check_page_evidence  # noqa: E402
from src.naming import (NAME_MAX_WORDS, NAME_TARGET_WORDS, ai_flavor,  # noqa: E402
                        name_words)


STATE_LABELS = {"✅": "SETTLED", "🟡": "PARTIAL", "🔴": "OPEN", "⏸": "ON HOLD"}


APPLICATION_BOARD_NAME = re.compile(
    r"^(?:(?:A\d+_)?[A-Za-z0-9][A-Za-z0-9-]*-InsightBoard|"
    r"(?:B\d+_)?[A-Za-z0-9][A-Za-z0-9-]*-DesignBoard)$"
)

# Sections a page cannot be complete without. Aliases are accepted because old
# boards still use them and ALIAS is the renderer's own table.
# `Now` (`## States`) RETIRED 260819 and merged into `Done when` (`## Aims`):
# one Aim is one row carrying its tick, its `Done when:` test and its `Now:`
# fact (`hai-draft` 0.34.0). One id written in two places was one fact with
# two owners, and it produced `aim-stated-twice` and `state-without-aim` on the
# very page that ruled it. A page that still carries `## States` keeps parsing;
# `retired-section` reports it, and this list no longer DEMANDS it.
# hai-draft 0.121: the Page Face is Opening -> Content; Aims are backstage and
# optional, so a Page with no Aims anywhere is not missing a section (JL 261001).
REQUIRED = ["Opening"]


def reader_title_words(title):
    """Return the reader-facing words in one Page H1.

    The visible purpose phrase has an eight-word ceiling. Machine identity and
    derived release metadata are useful navigation but are not the phrase a
    writer is being asked to shorten, so remove them before counting.
    """
    title = re.sub(
        r"^(?:(?:Q[A-Za-z0-9-]*\d[A-Za-z0-9-]*)|"
        r"(?:S\s+[A-Za-z]+\s+[A-Za-z0-9]+)|"
        r"(?:(?:Skill|Agent|Meeting|Design)[ -]?\d+))\s*·\s*",
        "", title, flags=re.I)
    title = re.sub(r"\s*\((?:Skill|Agent|Meeting)\b[^)]*\)\s*$", "", title,
                   flags=re.I)
    title = re.sub(r"\s*·\s*v\d[0-9A-Za-z.-]*\s*$", "", title, flags=re.I)
    return name_words(title)


def check_identity_name(value, kind, code, where, rep):
    """Report the mechanical half of the shared naming law."""
    words = name_words(value)
    if len(words) > NAME_MAX_WORDS:
        rep.add(
            WARN, code, where,
            f"{kind} has {len(words)} reader-facing words; use "
            f"{NAME_TARGET_WORDS} or fewer and never more than "
            f"{NAME_MAX_WORDS}. Rewrite around one identity; do not truncate")
    flavor = ai_flavor(value)
    if flavor:
        rep.add(
            WARN, "name-ai-flavor", where,
            f"{kind} uses generic model-like wording ({flavor!r}); name the "
            "concrete object, action, or outcome")


def check_page_title(text, name, rep):
    """Check the Page H1 against the shared six-target, eight-ceiling law."""
    match = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    if not match:
        return
    title = match.group(1)
    # Identity/version prefixes are navigation, not part of the authored name.
    visible = " ".join(reader_title_words(title))
    line = text[:match.start()].count("\n") + 1
    check_identity_name(visible, "Page title", "page-title-long",
                        f"{name}:{line}", rep)


def check_board_names(text, rep):
    """Check the Board title and Question Group names in ``board.md``."""
    title = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    if title:
        line = text[:title.start()].count("\n") + 1
        check_identity_name(title.group(1), "Board title", "board-title-long",
                            f"board.md:{line}", rep)

    names = "|".join(re.escape(n) for n in alias_names("Pages"))
    pages = re.search(rf"(?ms)^##\s+(?:{names})\s*$\n?(.*?)(?=^##\s+|\Z)", text)
    if not pages:
        return
    for match in re.finditer(
            r"^###\s+Q(?:[0-9][a-z]|[A-Z]+[a-z]*)\s*\u00b7\s*(.+?)\s*$",
            pages.group(1), re.M):
        line = text[:pages.start(1) + match.start()].count("\n") + 1
        check_identity_name(match.group(1), "Question Group title",
                            "question-group-title-long", f"board.md:{line}", rep)


def check_division_names(text, name, rep):
    """Check direct Content division names; prose and job lines are exempt."""
    block = re.search(r"(?ms)^##\s+Content\s*$\n?(.*?)(?=^##\s+|\Z)", text)
    if not block:
        return
    pattern = r"^###\s+(?:\u00a7\s*)?\d+(?:\.\d+)*\s*(?:\u00b7\s*)?(.+?)\s*$"
    for match in re.finditer(pattern, block.group(1), re.M):
        line = text[:block.start(1) + match.start()].count("\n") + 1
        check_identity_name(match.group(1), "Content division name",
                            "division-name-long", f"{name}:{line}", rep)


def declared_links(board_md):
    m = re.search(r"^## (?:Links|链接)\s*$", board_md, re.M)
    if not m:
        return {}
    tail = board_md[m.end():].split("\n## ")[0]
    out = {}
    for ln in tail.split("\n"):
        parts = ln.strip().split(None, 1)
        if len(parts) == 2 and not ln.startswith("#"):
            out[parts[0]] = parts[1].strip()
    return out


# A key's lowercase tail may be a WORD, not one letter: the paper board declares
# `### QCskill · Engine skills`, and a one-letter tail read that heading as `QCs`,
# which matched no folder. The group then vanished from the count and every folder
# after it was told it was numbered one too high.
GROUP_HEAD = re.compile(r"^###\s+Q([0-9][a-z]|[A-Z]+[a-z]*)\b", re.M)


def check_group_order(d, text, rep):
    """The group folders must read on disk in board.md's `## Pages` order.

    `## Pages` is the ONLY authority on order; the number a folder carries is
    derived from it (JL 260816). Letters carry identity and cannot carry order,
    which is how `QC-engine/` came to sort four rows above `QPs-page-structure/`
    on a board that read them the other way round.

    A board is numbered or it is not, and the middle is the only real defect: one
    numbered folder among bare ones means two orderings disagree and a reader
    cannot tell which is live. A wholly unnumbered board is the pre-260816 shape,
    reported as a WARN so it gets migrated rather than blocked.

    A folder is a GROUP folder only when its name, minus any number, starts with
    a `Q<key>` that board.md declares. That is what keeps a paper's
    `0-lifecycle/` out of this check: `0-seed/`, `1-work/` and `3-display/` are
    SUBJECT folders whose numbers carry lifecycle order, and they answer to a
    different rule entirely.
    """
    names = "|".join(re.escape(n) for n in alias_names("Pages"))
    m = re.search(rf"^##\s+({names})\s*$", text, re.M)
    if not m:
        return
    end = text.find("\n## ", m.end())
    keys = GROUP_HEAD.findall(text[m.end():end if end != -1 else len(text)])
    if not keys:
        return
    pos = {k: i + 1 for i, k in enumerate(keys)}
    # longest key first, so QAa wins over QA on `QAa-something/`
    by_len = sorted(keys, key=len, reverse=True)

    found = []                      # (folder, key, declared number or None)
    for p in sorted(d.iterdir()):
        if not p.is_dir() or p.name.startswith(("_", ".")) or p.name in ("board", "fig"):
            continue
        num = NUMBERED_GROUP.match(p.name)
        stem = group_stem(p.name)
        key = next((k for k in by_len
                    if stem == f"Q{k}" or stem.startswith(f"Q{k}-")), None)
        if key:
            found.append((p.name, key, int(num.group(1)) if num else None))
    if not found:
        return

    bare = [f for f, _, n in found if n is None]
    if len(bare) == len(found):
        rep.add(WARN, "groups-not-numbered", "board.md",
                f"{len(found)} group folders carry no reading-order number "
                f"(JL 260816); rename each to `<N>-<folder>` in ## Pages order "
                f"and rewrite the paths that cite them. regroup.py numbers a "
                f"board it is still FOLDING and cannot renumber this one")
        return
    for f in bare:
        rep.add(ERROR, "group-number-missing", f,
                "some group folders are numbered and this one is not, so the "
                "folder listing declares two different orders")
    for f, key, n in found:
        if n is None:
            continue
        want = pos[key]
        if n != want:
            rep.add(ERROR, "group-number-order", f,
                    f"numbered {n} but Q{key} is #{want} in ## Pages; "
                    f"board.md decides the order, the folder follows it")


# `### <label> · <folder>` is how `## Pages` binds a group row to a directory,
# and `servers/workbench-paper/paper.py:_GROUP_RE` reads the folder as ONE non-space token. A
# heading that spells the folder with a space (`### Ba · ManSci Main`) therefore
# matches nothing, the group vanishes, and every consumer downstream of it
# reports zero: the paper workbench showed `no S- rows in C8` and
# `0 Section page(s)` on a board whose static site had rendered all 21 pages
# correctly, because build.py groups by a different rule and never noticed
# (JL 260921). A heading that cannot bind is worse than a wrong one: nothing
# says so. This gate makes both cases loud.
PAGES_HEAD = re.compile(r"^###\s+(?P<label>.+?)\s+\u00b7\s+(?P<folder>\S+)\s*$")


def check_pages_group_folders(d, text, rep):
    """Every `### ` heading in `## Pages` must bind to a folder that exists.

    Two defects, both silent before this check:

    1. The heading does not parse as `<label> · <folder>` at all, usually
       because the folder was written with a space or the separator is a
       hyphen rather than `\u00b7`. The group is then invisible to every
       reader that uses the group regex.
    2. It parses, but the folder is not on disk, so the group is empty.

    The label carries identity and may contain spaces; the folder is the
    directory name and may not. A board with no `### ` headings under
    `## Pages` is a flat board and is left alone.
    """
    names = "|".join(re.escape(n) for n in alias_names("Pages"))
    m = re.search(rf"^##\s+({names})\s*$", text, re.M)
    if not m:
        return
    end = text.find("\n## ", m.end())
    body = text[m.end():end if end != -1 else len(text)]
    heads = [l.rstrip() for l in body.splitlines() if l.startswith("### ")]
    if not heads:
        return
    # A board that HAS a live workbench surface is broken by an unbindable heading;
    # a Task or Discovery block has no such consumer today, so the same heading
    # is a latent defect rather than a live one. Severity follows that, so the
    # gate does not block boards whose convention predates the workbench.
    dialect = re.search(r"^dialect:\s*(\S+)\s*$", text, re.M)
    plugged = (dialect and dialect.group(1).strip() == "paper") or board_kind(d) in {
        "design-board", "insight-board", "labeling-board"}
    sev = ERROR if plugged else WARN
    tail = ("" if plugged else " this board has no live workbench surface today, so"
            " nothing is broken yet; it binds to nothing the moment it gets one")
    for line in heads:
        got = PAGES_HEAD.match(line)
        if not got:
            rep.add(sev, "pages-group-unbindable", f"board.md -> {line.strip()}",
                    "a `## Pages` group heading must read `### <label> \u00b7 <folder>` "
                    "with the folder as the directory name and no spaces in it; this "
                    "one binds to nothing, so the group and every page under it "
                    "disappear from the workbench and the roster without any error."
                    + tail)
            continue
        folder = got.group("folder")
        if not (d / folder).is_dir():
            rep.add(sev, "pages-group-folder-missing",
                    f"board.md -> {folder}",
                    f"group {got.group('label')!r} names folder `{folder}`, which is "
                    f"not a directory here; rename the heading to the real folder or "
                    f"create it, or the group reads as empty." + tail)


def check_board(d, rep):
    bmd = d / "board.md"
    if not bmd.exists():
        rep.add(ERROR, "no-board-md", str(d), "no board.md: this is not a board folder")
        return {}, {}, False
    text = bmd.read_text(encoding="utf-8")
    links = declared_links(text)
    kind = board_kind(d)
    task_block = kind == "task-block"
    discovery_block = kind == "discovery-block"
    block_board = task_block or discovery_block
    if kind and kind not in {"task-block", "discovery-block", "design-board", "insight-board", "cowork-block"}:
        rep.add(ERROR, "unknown-board-kind", "board.md",
                f"board-kind {kind!r} has no Board container contract")

    if ("InsightBoard" in d.name or "DesignBoard" in d.name) and not (
        APPLICATION_BOARD_NAME.fullmatch(d.name)
    ):
        rep.add(
            WARN,
            "legacy-application-board-name",
            str(d),
            "new Application boards use subject-first names: "
            "<Subject>-InsightBoard or <Topic>-DesignBoard, with an optional "
            "A<NN>_ or B<NN>_ ordering prefix; kind-first names are readable "
            "compatibility addresses only",
        )

    if not re.search(r"^#\s+\S", text, re.M):
        rep.add(ERROR, "board-missing-title", "board.md", "no `# title` line")
    check_board_names(text, rep)
    for canon in ("Topic", "Pipeline") + (() if kind == "cowork-block" else ("Pages",)):   # cowork: its Jobs are the tree
        if not has_section(text, canon):
            shown = " / ".join(alias_names(canon))
            rep.add(ERROR, "board-missing-section", "board.md", f"no `## {shown}` section")

    check_pages_group_folders(d, text, rep)

    # Not every rule is universal. The hai-paper board rules that `state:`
    # is about the DECISION and implementation intent lives in Aims, so
    # a ✅ page there legitimately carries unticked boxes. Detected by reading
    # what the board says about itself, which is fragile: a board has no way to
    # DECLARE which rules it opts out of, and keep that gap visible in the report.
    decision_only = bool(re.search(
        r"`?state:`?[^\n]{0,80}\b(is about|means)\b[^\n]{0,40}\bDECISION\b", text, re.I))

    for key in ("spine", "close"):
        if not re.search(rf"^{key}:\s*\S", text, re.M):
            rep.add(ERROR, "board-missing-key", "board.md",
                    f"no `{key}:` line; the board cannot say what it is for or when it ends")

    # `store:` is OPTIONAL and declares where work COMMISSIONED by this board
    # writes its generated output: results and notebooks. A consumer-owned
    # Local Run records any page-serving adaptation as an immutable Result.
    # A dispatching page passes the Result store as RESULT_STORE, so
    # the executor is told a PATH and never learns which consumer it serves.
    # Absent means this board commissions nothing that produces files, and a
    # task it dispatches keeps output in its own folder (JL 260823).
    store = re.search(r"^store:\s*(\S.*?)\s*$", text, re.M)
    if store:
        target = store.group(1)
        if target.startswith("~") or ".." in target.split("/"):
            rep.add(ERROR, "board-store-path", f"board.md -> {target}",
                    "a `store:` must be repo-relative or absolute with no `..` and no "
                    "`~`; a dispatching Page resolves it once and hands the executor "
                    "an absolute path, so a climbing path resolves differently "
                    "depending on who dispatched")
    # `reads:` (JL 260824, the design family): the board's evidence whitelist.
    # Each entry is a sibling board's folder name; a direction card's grant and
    # a unit's evidence must sit inside it, so a name that resolves to nothing
    # makes the whole chain unverifiable.
    reads = re.search(r"^reads:\s*(\S.*?)\s*$", text, re.M)
    if reads:
        for entry in [e.strip() for e in reads.group(1).split("\u00b7")]:
            if not entry:
                continue
            climbs = ".." in entry.split("/")
            _root = _repo_root(d)
            inside = False
            if climbs and _root:
                try:
                    (d / entry).resolve().relative_to(_root.resolve())
                    inside = True
                except ValueError:
                    inside = False
            if entry.startswith("~") or (climbs and not inside):
                rep.add(ERROR, "board-reads-path", f"board.md -> {entry}",
                        "a `reads:` entry must be a plain sibling-board name, a "
                        "repo-relative path, or a `../` path that stays inside the "
                        "checkout (a board in another Project); never `~`")
                continue
            # repo-relative means from the CHECKOUT ROOT, never the invoker's
            # cwd: the same board must check identically from anywhere.
            _rr = _repo_root(d)
            cand = [d.parent / entry, d / entry] + ([_rr / entry] if _rr else [])
            if not any(c.is_dir() for c in cand):
                rep.add(ERROR, "board-reads-target", f"board.md -> {entry}",
                        "a `reads:` entry names no board on disk; the grant chain "
                        "(reads -> card grant -> unit evidence) starts here, so a "
                        "dead entry makes every citation under it unverifiable")

    pages = {
        (p.relative_to(d).as_posix() if (block_board and task_page_info(d, p))
         or (not block_board and mounted_info(d, p))
         or registered_page_source(p.parent) == p
         else p.name): p
        for p in page_files(d)
    }
    # `[MIAD]\d` admits the Application runtime ids (M00-meta.md, I01-<slug>.md,
    # A00-brief.md, D01-<slug>.md) that PAGENAME now discovers; without it every
    # runtime board reported all of its own pages as not-in-pages (260820).
    listed = re.findall(
        r"^((?:[QS]|[A-Z]{1,2}\d|Agent-|Meeting-|Design-)[^\s/]*\.md)\s*$", text, re.M)
    if block_board:
        listed += re.findall(
            r"^([^\s]+/t\d{2}_[a-z0-9_]+/t\d{2}_[a-z0-9_]+\.md)\s*$",
            text,
            re.M | re.I,
        )
    # Registered Pages use the same Board-relative source as parse_dir. Retain
    # its unique-basename compatibility, without guessing ambiguous filenames.
    for _, line in strip_fences(section_text(text, "Pages")):
        row = line.strip().lstrip("-*· ").strip()
        if re.fullmatch(r"[^\s]+\.md", row) and row not in listed:
            listed.append(row)
    for i, name in enumerate(listed):
        relative = next((key for key, path in pages.items()
                         if path.relative_to(d).as_posix() == name), None)
        if name not in pages and relative is not None:
            listed[i] = relative
            continue
        matches = [key for key in pages if Path(key).name == name]
        if name not in pages and len(matches) == 1:
            listed[i] = matches[0]
    for name in listed:
        if name not in pages and not (d / name).is_file():     # a Job face a cowork Block lists is on disk
            rep.add(ERROR, "pages-ghost", f"board.md -> {name}",
                    "## Pages names a file that is not on disk")
    for name in sorted(pages):
        # A Task Block's tree is the membership authority.  Its ## Pages may
        # contain group prose only; once it lists any Task explicitly, the
        # ordinary complete-registry warning applies.
        if name not in listed and kind != "cowork-block" and (not block_board or any("/t" in x for x in listed)):
            rep.add(WARN, "not-in-pages", name,
                    "on disk but not in ## Pages, so it renders under the ⚠️ group")
    if not block_board:
        check_group_order(d, text, rep)
    seen = {}
    for name in sorted(pages):
        if block_board:
            info = task_page_info(d, pages[name])
            if info:
                source = pages[name].read_text(encoding="utf-8", errors="replace")
                if discovery_block:
                    if not re.search(r"(?m)^folder-kind:\s*discovery\s*$", source):
                        rep.add(ERROR, "discovery-page-folder-kind", name,
                                "a Discovery Block Page must declare `folder-kind: discovery`")
                else:
                    if not re.search(r"(?m)^folder-kind:\s*task\s*$", source):
                        rep.add(ERROR, "task-page-folder-kind", name,
                                "a Task Block Page must declare `folder-kind: task`")
                    if not re.search(r"(?m)^task:\s*\.\s*$", source):
                        rep.add(ERROR, "task-page-self", name,
                                "a Task Page must declare `task: .` so both faces share one address")
                    if re.search(r"(?m)^page-type:\s*task\s*$", source):
                        rep.add(WARN, "task-page-legacy-type", name,
                                "`page-type: task` is a legacy key; `folder-kind: task` owns new Pages")
                continue
        m = re.match(r"([QS][A-Za-z0-9]*\d+[a-z]?)", name)
        if not m and not SEMANTIC_SECTION_PAGE.fullmatch(name):
            continue
        fid = Path(name).stem if SEMANTIC_SECTION_PAGE.fullmatch(name) else m.group(1)
        if fid in seen:
            rep.add(ERROR, "duplicate-id", name, f"id {fid} is already used by {seen[fid]}")
        seen[fid] = name

    for token, target in links.items():
        if target.startswith(("http://", "https://")):
            continue
        if not (d / target).exists():
            if outside_checkout(d, target):
                # The target climbs out of this git checkout, so from here it
                # is UNVERIFIABLE, not known-dead: on the machine that holds
                # the neighbouring SPACE the same row resolves and stays
                # checked (JL 260815). An ERROR must mean known-dead.
                rep.add(WARN, "outside-checkout", f"board.md -> {token}",
                        f"Link target lives outside this checkout: {target}")
            else:
                rep.add(ERROR, "dead-link", f"board.md -> {token}",
                        f"declared Link target does not exist: {target}")
    return pages, links, decision_only


def check_mounted_page(d, path, name, rep, seen):
    """A Task or Discovery Folder Page mounted on this Board.

    The Folder's own workflow owns the Page's status and prose grammar, so the
    Q contract (state, owner, Opening, Aims) does not apply. The Board only
    needs a unique id and an address that agrees with the path it sits on.
    """
    info = mounted_info(d, path)
    if info["id"] in seen:
        rep.add(ERROR, "duplicate-id", name,
                f"id {info['id']} is already used by {seen[info['id']]}")
    seen[info["id"]] = name
    text = path.read_text(encoding="utf-8", errors="replace")
    declared = re.search(r"(?m)^address_compact:\s*(b\d{2}j\d{2}t\d{2})\s*$", text)
    from_path = "".join(
        m.group(1).lower()
        for part in path.relative_to(d).parts[:-1]
        for m in [re.match(r"^([bjt]\d{2})(?:_|$)", part, re.I)] if m)
    if declared and re.fullmatch(r"b\d{2}j\d{2}t\d{2}", from_path) \
            and declared.group(1).lower() != from_path:
        rep.add(WARN, "mounted-address-mismatch", name,
                f"address_compact {declared.group(1)} does not match the "
                f"Folder path address {from_path}")


def check_face(path, name, rep, links, page_ids, decision_only=False):
    text = path.read_text(encoding="utf-8")
    imported_content = None
    # Only an explicitly registered base file import gets technical validation.
    # Authored Pages and declared scholarly/Task variants retain all old rules.
    if (registered_page_source(path.parent) == path
            and not re.search(r"(?m)^(?:folder-kind|page-type):\s*\S", text)):
        import tomllib  # registration already requires Python 3.11+; legacy does not
        imported_content = tomllib.loads((path.parent / "page.toml").read_text(
            encoding="utf-8")).get("content")

    title_match = re.search(r"^#\s+(\S.*?)\s*$", text, re.M)
    if not title_match:
        rep.add(ERROR, "missing-title", name, "no `# title` line")
    elif imported_content is None:
        # The shared naming law (six-word target, eight-word ceiling) replaced
        # the older six-word `title-too-long` warning.
        check_page_title(text, name, rep)
    if imported_content is None:
        check_division_names(text, name, rep)
    for canon in REQUIRED:
        # `Done when` is satisfied by the page's PLAN once the page migrated to
        # workbench-task-draft 0.16.0 and kept no copy.
        if canon == "Done when" and page_aims_text(text, path)[1]:
            continue
        if not has_section(text, canon):
            shown = " / ".join(alias_names(canon))
            rep.add(ERROR, "missing-section", name, f"no `## {shown}` section")
    # `Skill-<unit>-<slug>` is the SKILL page kind (JL 260731), not a stage: it
    # mirrors a shipped unit and has no gate, so the stage sections are not owed.
    # Stage ids are exactly what parse.py can classify as a stage: `S-<Word>-`
    # or the legacy shorthand S<d>. A bare startswith("S") also claimed
    # application families like SD00-seed and SA01-<slug> (260821), which are
    # not stages; SM/SA shorthands left parse.py the same day.
    if re.match(r"S(?:-|\d)", name) and not SEMANTIC_SECTION_PAGE.fullmatch(name):
        for canon in ("Stage Contract", "Content"):
            if not has_section(text, canon):
                shown = " / ".join(alias_names(canon))
                rep.add(ERROR, "missing-stage-section", name,
                        f"S page has no required `## {shown}` section")

    m = re.search(r"^state:\s*(.+?)\s*$", text, re.M)
    token = state_token(m.group(1)) if m else ""
    if not m:
        rep.add(ERROR, "no-state", name, "no `state:` line")
    elif token not in STN:
        rep.add(ERROR, "bad-state", f"{name}:{text[:m.start()].count(chr(10)) + 1}",
                f"state is {m.group(1)!r}; its first token must be one of "
                + " · ".join(f"{emoji} {label}" for emoji, label in STATE_LABELS.items())
                + "; an optional human-readable suffix may follow")
    elif len(m.group(0)) > 110:
        rep.add(WARN, "state-line-long", f"{name}:{text[:m.start()].count(chr(10)) + 1}",
                f"state line is {len(m.group(0))} chars; the row grammar (JL 260816, QPs1 §8) keeps it "
                "under 110: status word, what stands, then `open:` with a short list or a count; "
                "facts belong in States, reasons in Log")

    # An InsightBoard answering Page is read by the public and carries no
    # person's name (hai-insight ref/report.md § What Insight adds), so its
    # folder kind exempts it from the owner line.
    answering = re.search(r"(?m)^folder-kind:\s*(?:data|information|knowledge|wisdom)\s*$",
                          text.split("\n## ", 1)[0])
    if not answering and not re.search(r"^owner:\s*\S", text, re.M):
        rep.add(ERROR, "no-owner", name, "no `owner:` line, so nobody is named as responsible")

    if imported_content is not None:
        source = re.search(r"(?m)^source-content:[ \t]*(\S.*?)[ \t]*$", text)
        if not source or source.group(1) != imported_content:
            rep.add(ERROR, "source-content-mismatch", name,
                    "source-content must equal the registered page.toml content path")
        if not has_section(text, "Content"):
            rep.add(ERROR, "missing-section", name, "no `## Content` section")
        if not section_text(text, "Opening").strip():
            rep.add(ERROR, "opening-empty", name, "the technical wrapper needs an Opening")
        check_group_names(text, name, rep)
        check_file_paths(text, name, rep, path.parent, path=path)
        check_duplicate_sections(text, name, rep)
        check_retired_sections(text, name, rep)
        check_fence_balance(text, name, rep)
        return

    # A page id in backticks should resolve, either to a declared Link or to a
    # file on this board. Historical mentions of a retired id look identical to
    # live references today, which is why these are WARN: see the retired-id
    # convention item in the current structural contract.
    for lineno, ln in strip_fences(text, prose_only=True):
        for tok in re.findall(r"`(S-[A-Za-z0-9-]+|Q[A-Za-z]*\d+[a-z]?(?:@\w+)?)`", ln):
            if tok in links or tok in page_ids:
                continue
            rep.add(WARN, "unresolved-id", f"{name}:{lineno}",
                    f"`{tok}` is neither a page on this board nor a declared Link")

    # English-only and the em-dash ban are rules about the prose THIS TEAM
    # writes. A `Meeting-<n>` page is a mirror of a meeting that happened, in
    # whatever language it happened in, and "fixing" its wording would falsify
    # the record (QC10). Its managed spans are already skipped by strip_fences;
    # this exempts the two seeded lists as well, which are the meeting's own
    # action items and open questions and are equally quotations.
    quoted = bool(re.match(r"^Meeting-\d+-", Path(name).name))
    for lineno, ln in strip_fences(text, prose_only=True):
        if ln.lstrip().startswith(">"):
            # a sentence's comment or edit record is a quotation of what a
            # person typed, and the record rule forbids editing it; nagging
            # about a line nobody may fix is a checker defect (260815, the
            # same reasoning that exempts Meeting pages above)
            continue
        bare = re.sub(r"`[^`]*`", "", ln)   # a code span quotes the machine
        # a double-quoted span quotes a PERSON, and the board's own record
        # rules value the exact words over the prose rules (JL 260815, the
        # ruling that extended the Meeting exemption): "为啥不按序号来排?" stays
        # verbatim, and the narration around it stays English and dash-free.
        bare = re.sub(r'"[^"\n]*"|“[^”\n]*”', "", bare)
        if "—" in bare and not quoted:
            rep.add(WARN, "em-dash", f"{name}:{lineno}", "em-dash in prose (JL 260724)")
        if re.search(r"[一-鿿]", bare) and not quoted:
            rep.add(WARN, "cjk", f"{name}:{lineno}", "CJK in a board that is English-only (JL 260724)")

    # One sentence per line: the page gives every prose line its own row, so a
    # hard wrap mid-sentence becomes a broken row the reader sees.
    #
    # Only inside prose. The `state:` / `owner:` / `method:` header is lowercase
    # and unterminated by design, and a first draft of this rule flagged three
    # lines on every page for it, which is how a checker teaches people to stop
    # reading its output.
    # A `<!-- … -->` guide comment is instructions, not page prose, and its
    # wrapping is deliberate. `ref/page-template.md` is largely one long
    # comment, so counting it flagged twelve lines on every page copied from
    # the template, which is the fastest way to teach someone to ignore a
    # checker (JL 260802).
    prev_open, in_prose, in_comment = False, False, False
    for lineno, ln in strip_fences(text, prose_only=True):
        s = ln.strip()
        if "<!--" in s:
            in_comment = "-->" not in s.split("<!--", 1)[1]
            prev_open = False
            continue
        if in_comment:
            if "-->" in s:
                in_comment = False
            prev_open = False
            continue
        if s.startswith("## "):
            in_prose, prev_open = True, False
            continue
        if not in_prose:
            continue
        if (not s or s.startswith(("#", "-", ">", "|", "!", "["))
                or ln.startswith("  ") or re.match(r"^[a-z][a-z-]*:\s", s)):
            prev_open = False
            continue
        if prev_open and s[0].islower():
            rep.add(WARN, "hard-wrap", f"{name}:{lineno}",
                    "starts lowercase under an unterminated line: one sentence looks wrapped over two")
        prev_open = s[-1] not in ".?!:;)”\"`»"

    # A full-line **bold** renders as a GROUP TITLE with a 🔹 marker, so it must
    # actually lead a run of items. QA4 §3 ruled that a paragraph is never written
    # in bold; without a check the rule held nowhere, and a bold opening sentence
    # in State renders as a decorated title in front of prose.
    lines = text.split("\n")
    fence = False
    managed = False
    for i, ln in enumerate(lines):
        st = ln.lstrip()
        if st.startswith("```"):
            fence = not fence
            continue
        if st.startswith("<!--") and "haipipe:" in st:   # derived, not our prose
            managed = ":start" in st
            continue
        if fence or managed or not re.match(r"^\*\*(.+?)\*\*\s*$", ln.strip()):
            continue
        nxt = next((x for x in lines[i + 1:i + 4] if x.strip()), "")
        # A run of #### paragraph headings is a group too (JL 260801). A long
        # division groups its paragraphs rather than leaving eleven of them in
        # one flat run, and that grouping is exactly what a group title is for;
        # the rule was only ever written against `- item` runs because that was
        # the only kind of run that existed when it was made.
        if not nxt.strip().startswith(("- ", "* ", "#### ")):
            rep.add(WARN, "bold-not-a-group-title", f"{name}:{i + 1}",
                    "a whole-line **bold** renders as a group title with 🔹, but prose follows it, "
                    "not a run of items (QA4 §3)")

    aims_text, in_plan = page_aims_text(text, path)
    states_text = section_text(text, "Now")
    check_state_mirrors_aims(aims_text, states_text, name, rep)
    check_generated_block(text, name, rep, path)
    check_evidence_file(path, name, rep)
    check_discussion_file(path, name, rep)
    check_requirement_file(text, path, name, rep)
    check_section_writing_requirements(text, path, name, rep)
    check_retired_blocks(text, name, rep)

    progress = aim_progress(aims_text, states_text)
    met, total, closed = progress["met"], progress["total"], progress["closed"]
    st = token
    # Aim/state alignment is a Q ruling heuristic, not an S gate rule.
    # A lifecycle S page may pass its human gate while retaining follow-up work,
    # or show partial work before that gate. Its first emoji is authoritative.
    if not name.startswith("Q") or decision_only:
        pass          # S gate semantics, or a Q board's declared decision-only variant
    elif st == "✅" and closed != total:
        rep.add(WARN, "settled-with-open-aims", name,
                f"state is SETTLED with {total - closed} open Aim(s); on a Q every Aim must close")
    # The two staleness shapes, both real: a page that was worked on and never
    # written back reads OPEN with ticks under it (QA4a said "nothing is built
    # and nothing is decided" while the thing was running, JL 260726), and a
    # page that finished and was never closed reads PARTIAL with nothing left.
    # SKILL.md's `sync` action already requires the write-back; this is the only
    # thing that notices when a session skips it.
    elif st == "🔴" and met:
        rep.add(WARN, "open-with-met-aims", name,
                f"state is OPEN with {met}/{total} Aim(s) met; "
                "either the state is stale or the Aim State is (SKILL.md `sync`)")
    elif st == "🗂":
        # FOLDED is terminal by MERGE, not by completion, so a folded page is
        # never nagged about open Aims: its subject moved to another page and
        # its own rows will never close. Same exemption a Meeting page gets.
        pass
    elif st == "🟡" and total and closed == total:
        rep.add(WARN, "partial-with-nothing-open", name,
                "state is PARTIAL with every Aim closed; either it is SETTLED "
                "or an Aim is missing (SKILL.md `sync`)")

    check_opening(text, name, rep)
    check_feedback_coverage(path, text, name, rep)
    check_plan_arc(path, name, rep)
    check_page_type(path, text, name, rep)
    check_group_names(text, name, rep)
    check_one_canvas(text, name, rep)
    check_division_figures(text, name, rep)
    check_comment_form(text, name, rep)
    check_file_paths(text, name, rep, path.parent, path=path)
    check_related_board_pages(path, name, text, rep)
    check_canvas_frames(text, name, rep, path.parent)
    check_duplicate_sections(text, name, rep)
    check_retired_sections(text, name, rep)
    check_page_evidence(path, text, name, rep, ERROR, WARN)
    check_fence_balance(text, name, rep)
    check_content_attribution(text, name, rep)
    check_section_sentences(text, path, name, rep)


# QB4 §1 states seven rules for the Opening and NOT ONE of them was checked, so
# the same Opening was written wrong four times in one day and a second session
# wrote the same mistake back while the first was fixing it (JL 260801: "为什么
# 你不 follow 我们现在的 guideline 呢？还是我们 skill 没有强调这一点？"). Four of
# the seven are mechanical, so they belong here rather than in a reviewer's head.
# The other three (one idea, not interchangeable, reads alone) need a reader,
# which is QF1's second instrument.
# QB4 §1 sets no sentence quota: one central idea controls the length. This is
# the ceiling that catches Content leaking into the Opening, and it allows the
# bearing JL asked for on 260801 (2-3 lines placing the page) plus its stake.
OPENING_MAX_PITCH = 10
OPENING_MAX_CLAUSES = 3        # commas plus semicolons before a sentence sprawls
# The ON-STAGE paragraph is everything above ## Opening's FIRST BLANK LINE, and
# it is the only prose a reader gets without clicking. JL 260801 capped it at
# 4-5 sentences, about five lines on screen; measured on the joined render, that
# is roughly 450 characters, and this ceiling leaves a little air above it.
OPENING_MAX_STAGE_CHARS = 520


def check_opening(text, name, rep):
    """The mechanical half of QB4 §1's Opening contract."""
    body = section_text(text, "Opening")
    if not body:
        rep.add(WARN, "opening-empty", name,
                "no Opening at all; QB4 §1 says every page of every kind opens")
        return
    # strip_fences yields (lineno, line): a figure may legitimately be long
    raw = [ln.rstrip() for _, ln in strip_fences(body, prose_only=True)]
    # everything above the FIRST BLANK LINE is what the reader sees on stage,
    # MINUS the sentence apparatus. `page_question.py` composes the lead as
    # `" ".join(x for x in lead_lines if not x.startswith(">"))` and hands every
    # `>` line to `render_apparatus`, so a `> Citation:` or a `> ✎` record under
    # the lead is a lane the reader opens, never a clause in the paragraph.
    # Counting it as prose made the checker and the renderer disagree about the
    # same fact: one ✎ record on a 340-char lead reported it as 841 chars and
    # flagged the record's own diff as a stuffed sentence (found on QBv1, 260802).
    onstage = []
    for ln in raw:
        if not ln.strip():
            if onstage:
                break
            continue
        if ln.lstrip().startswith(">"):
            continue
        onstage.append(ln)
    prose = [ln for ln in raw if ln.strip() and not ln.lstrip().startswith(">")]
    if not prose:
        rep.add(WARN, "opening-empty", name, "Opening has a heading and no prose")
        return

    # 1 · the lead is an actual question, and it is the first thing on stage
    #
    # ...EXCEPT on a skill page. `Skill-<n>` and `Agent-<n>` mirror a unit that
    # ships elsewhere and DECIDE NOTHING, so `hai-page-for-skill` rules
    # the opposite: their Opening INTRODUCES the unit and may never open with a
    # question. Without this exemption the seven pages that obeyed that contract
    # each carried a WARN telling them to put the question back, and a writer
    # working the checker's list would have regressed every one of them. Found by
    # the first real dispatch of hai-block-reviewer-agent, 260802.
    lead = prose[0].strip()
    roster = name.startswith(("Skill-", "Agent-"))
    if roster:
        if lead.endswith("?"):
            rep.add(WARN, "skillpage-opening-is-a-question", f"{name}:1",
                    "a skill page decides nothing, so its Opening INTRODUCES "
                    "the unit and never asks (hai-page-for-skill); "
                    f"it reads {lead[:60]!r}")
    elif not lead.endswith("?"):
        rep.add(WARN, "opening-lead-not-a-question", f"{name}:1",
                "the Opening lead must be one actual question (QB4 §1); "
                f"it reads {lead[:60]!r}")

    # 2 · the ON-STAGE paragraph is what a reader sees, and it is capped
    #     (JL 260801). build.py splits ## Opening on its FIRST BLANK LINE:
    #     above it is the visible paragraph, below it is the More details
    #     drawer. So the budget is measured on the lines above that blank
    #     line, joined the way the renderer joins them, not on the section.
    stage_para = " ".join(x.strip() for x in onstage).strip()
    if stage_para and len(stage_para) > OPENING_MAX_STAGE_CHARS:
        rep.add(WARN, "opening-paragraph-too-long", f"{name}:1",
                f"the on-stage paragraph is {len(stage_para)} chars against a "
                f"ceiling of {OPENING_MAX_STAGE_CHARS} (QB4 §1: 4-5 sentences, "
                "about five lines on screen); move the extra below the first "
                "blank line and it lands in More details")
    # The old line-count ceiling is retired (JL 260801). It counted every prose
    # line in ## Opening, which conflates the on-stage paragraph with the More
    # details drawer; the drawer is behind a click and has no budget. The
    # on-stage character ceiling above is the rule that replaced it.

    # 3 · no attribution parentheticals: a date belongs in the Log
    for i, ln in enumerate(prose):
        if re.search(r"\((?:JL|CC)[^)]*\d{6}[^)]*\)", ln):
            rep.add(WARN, "opening-attribution", f"{name}:{i + 1}",
                    "attribution parenthetical in the Opening; QB4 §1 puts the date in the Log")

    # 4 · one idea per sentence, because a stuffed sentence is unreadable
    #     (JL 260801, on one sentence that fed the reader everything at once)
    for i, ln in enumerate(onstage or [lead]):
        for sent in re.split(r"(?<=[.?!])\s+", ln):
            n = sent.count(",") + sent.count(";") + sent.count(":")
            if n > OPENING_MAX_CLAUSES and len(sent) > 140:
                rep.add(WARN, "opening-sentence-stuffed", f"{name}:{i + 1}",
                        f"one sentence carrying {n} clauses in {len(sent)} chars; "
                        "split it, the Opening is read cold")
