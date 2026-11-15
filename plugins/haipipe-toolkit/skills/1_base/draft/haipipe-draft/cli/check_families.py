"""check_families.py: the checks for one kind of Board: design, insight, partition register.
Also check_workbench_roster (every page subfolder is on the workbench roster) and _repo_root."""
import re

from cli.check_common import ERROR, HERE, WARN  # noqa: E402
from src.outline_version import plan_dir, record_path  # noqa: E402
from src.folder_contract import resolved_folder_kind  # noqa: E402


CARD_FIELDS = ["state", "stance", "depth", "thesis", "expected effect",
               "grant", "released"]   # `landed:` retired 260828: the card and
                                      # its unit share a folder, so the folder
                                      # IS the binding and a pointer would only
                                      # be one more thing that can dangle
CARD_STATES = {"proposed", "released", "landed", "killed"}
UNIT_STATES = {"draft", "judged"}          # accepted@v<N> is matched separately
DEPTHS = {"copy", "copy+why", "copy+why+expectation"}


def _repo_root(d):
    """The OUTERMOST checkout root, for evidence written repo-relative.

    Not the nearest: boards live inside submodules, and a submodule carries a
    `.git` FILE that satisfies `.exists()` just as a directory does. Stopping
    at the first hit returns the submodule, whose tree has no `_WorkSpace`, so
    every result-bank citation then reads as outside the grant.
    """
    found = None
    for p in [d] + list(d.parents):
        if (p / ".git").exists():
            found = p
    return found


def _resolve_cited(raw, base, root):
    """A cited path resolves either against its own file or against the repo."""
    raw = raw.strip().strip("`").rstrip(".,;:")
    if not raw or raw.startswith(("http", "#", "~")):
        return None
    for cand in [base / raw] + ([root / raw] if root else []):
        try:
            if cand.exists():
                return cand.resolve()
        except OSError:
            pass
    return None


def _cited_paths(text):
    """Every path-looking token in a page, backticked or bare.

    The bare pattern must not be allowed to start INSIDE a path: `../../x.md`
    also matches from its second character, which yields `./../x.md`, a string
    that resolves to nothing and reads as a dead link. That false positive
    fired on twenty-three real units the first time this ran.
    """
    out = []
    for m in re.finditer(r'`([^`\s]+\.(?:md|csv|txt|parquet|json))[^`]*`', text):
        out.append(m.group(1))
    for m in re.finditer(r'(?<![`\w./])((?:\.\.?/|designs/|_WorkSpace/|examples/)'
                         r'[^\s`)\]]+\.(?:md|csv|txt|parquet|json))', text):
        out.append(m.group(1))
    return list(dict.fromkeys(out))


def _card_field(text, key):
    m = re.search(r'^' + re.escape(key) + r':[ \t]*(.*)$', text, re.M)
    return m.group(1).strip() if m else None


def check_native_design_runs(d, rep):
    """Delegate allocated native Design Runs to their worker-owned gate."""
    import importlib.util

    # Only the native Design Run grammar belongs to the Design Unit gate.
    # Page delivery Runs also use the `rdNN_<target>` prefix (for example
    # `rd01_latex`), but they are Page-owned delivery records, not Design
    # Tickets.  Matching every `results/rd*_*` folder made the shared checker
    # misclassify those valid Page Results as orphan Design Results.
    folders = set()
    for pattern in ("runs/rd*_generate_*.yaml", "runs/rd*_verify_*.yaml",
                    "runs/rd*_commission_*.yaml", "runs/rd*_adopt_*.yaml",
                    "results/rd*_generate_*", "results/rd*_verify_*",
                    "runs/run-design-*.yaml", "results/run-design-*"):   # current names (JL 261001)
        paths = d.rglob(pattern)
        folders.update(p.parent.parent for p in paths
                       if p.is_file() or p.is_dir())
    folders.update(p.parent.parent for p in d.rglob("runs/r*_design_*.yaml"))
    folders.update(p.parent.parent for p in d.rglob("results/r*_design_*")
                   if p.is_dir())
    if not folders:
        return
    checker = (next(p for p in HERE.parents if p.name == "skills") / "2_theme" / "design" /
               "haipipe-design-unit" / "scripts" / "check_unit.py")
    try:
        spec = importlib.util.spec_from_file_location("design_unit_gate", checker)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for folder in sorted(folders):
            for issue in module.audit_folder(folder):
                rep.add(ERROR, "design-run-contract", str(folder.relative_to(d)), issue)
    except (ImportError, OSError, ValueError) as exc:
        rep.add(ERROR, "design-run-checker", str(d), str(exc))


def check_design_family(d, rep):
    """The design family's laws, given teeth (JL 260824).

    Until this ran, the family had eight written laws and two checks, both of
    them about `reads:`. A session on 260824 produced four real defects and a
    human or an agent caught every one: a dispatch packet that over-quoted its
    grant, a duplicate message counted twice, a grant path one directory short,
    and a unit citing its own card through a dead link. The last of those broke
    the workbench's first law, that the wager lives on the card and the unit cites
    it, and nothing mechanical noticed. These checks are that gap closed.

    A board may declare `mode: record` on board.md. A record board holds a
    pre-contract artifact, so its cards carry a historical `released:` and may
    have no stance and no grant; the vocabulary was written after the thing it
    describes, and forcing the words would forge a provenance. Everything
    structural is still checked on a record board: files, depth, resolvable
    references, and the evidence-within-grant chain when a grant exists.
    """
    check_native_design_runs(d, rep)
    if "DesignBoard" in d.name:
        retired = set(d.rglob("design/DU*"))
        for phase_file in d.rglob("workflow/phase.yaml"):
            text = phase_file.read_text(encoding="utf-8", errors="replace")
            if re.search(r"(?m)^\s*phase:\s*D[0-5]\b", text) or re.search(
                    r"(?m)^\s*folder-kind:\s*design-(?:card|unit|verdict|division|pagedown)\b",
                    text):
                retired.add(phase_file)
        for path in sorted(retired):
            # an underscore folder (_archive/) is a person's deliberate parking
            # and stays unjudged, the same reading as check_draw_folders: the
            # record survives on disk and the board is not asked to migrate it
            parts = path.relative_to(d).parts
            if "board" in parts or any(p.startswith("_") for p in parts):
                continue
            rep.add(ERROR, "retired-design-shape", str(path.relative_to(d)),
                    "D0-D5 and design/DU* are unsupported; create a current "
                    "Design Folder and rdNN Run instead of adapting this record; "
                    "park the old record under _archive/ to keep it unjudged")
    return


INSIGHT_QUESTION_PREFIX = {
    "data": "QD",
    "information": "QI",
    "knowledge": "QK",
    "wisdom": "QW",
}


def _insight_folder_kind(md, text):
    """Resolve Page-v2 Folder kind before the legacy Page Type.

    ``workflow/folder.yaml`` is authoritative when present; the shared reader
    imports a legacy identity only when it is absent. Malformed identity or
    conflicting Markdown raises a routing error before any kind-specific check.
    """
    head = text.split("\n## ", 1)[0]
    declared = re.search(r"(?m)^folder-kind:\s*([a-z][a-z0-9-]*)\s*$", head)
    legacy = re.search(r"(?m)^page-type:\s*([a-z][a-z0-9-]*)\s*$", head)
    return resolved_folder_kind(md.parent,
                                declared=declared.group(1) if declared else "",
                                legacy=legacy.group(1) if legacy else "")


def check_insight_family(d, rep):
    """The insight family's first teeth (JL 260828, fieldtest rounds 1-2).

    Two live runs on A00 produced eighteen frictions caught by a human or a
    cold agent and none by machinery. The three mechanical ones land here:
    a Design Handoff whose signature gate has no row to test (round 1 #2),
    a refusal token spelled three ways on one board (round 2 F7/F12), and a
    settled-partial cell whose licensing sentence the cited page does not
    know it carries (round 2 F14). Each is proven to FAIL in
    tests/test_insight_family.py before being trusted.
    """
    for md in sorted(d.rglob("*.md")):
        parts = md.relative_to(d).parts
        if "board" in parts or any(pt.startswith("_") for pt in parts):
            continue
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        try:
            ptype = _insight_folder_kind(md, text)
        except ValueError as exc:
            rep.add(ERROR, "folder-identity-invalid", md.name, str(exc))
            continue
        name = md.name

        if ptype == "wisdom":
            # A deferring W page exports no handoff and owes no signature; the
            # SERVES row is the handoff's marker (for-wisdom 0.3.0).
            if re.search(r"^SERVES\b", text, re.M):
                if not re.search(r"^signed:", text, re.M):
                    rep.add(ERROR, "wisdom-handoff-no-signed-row", name,
                            "a Design Handoff carries a `signed:` row (for-wisdom "
                            "0.3.0); without one the signature gate GI5 has nothing "
                            "to test, which is how two settled cells fell back on a "
                            "version bump")
                elif re.search(r"^signed:\s*⬜", text, re.M):
                    rep.add(WARN, "wisdom-handoff-unsigned", name,
                            "the handoff's `signed:` row is ⬜ — GI5 blocks, and a "
                            "DesignBoard binding this handoff is non-conformant "
                            "until a person signs")

        if ptype == "meta":
            check_partition_register(text, name, rep)

        if ptype == "question":
            head = text.split("\n## ", 1)[0]
            current_key = re.search(r"(?m)^folder-kind:\s*question\s*$", head)
            level = re.search(
                r"(?m)^question-level:\s*(data|information|knowledge|wisdom)\s*$",
                head,
            )
            if current_key and not level:
                rep.add(ERROR, "question-level-missing", name,
                        "a Page-v2 Question Folder must declare `question-level:`; "
                        "the DIKW level and each MT00 partition derive its Question Group")
            if re.search(r"(?m)^question-group:\s*\S+", head):
                rep.add(WARN, "question-group-stored", name,
                        "Question Group is derived as partition × DIKW target from "
                        "MT00 and the register; do not store a second group state")
            if level:
                expected = INSIGHT_QUESTION_PREFIX[level.group(1)]
                for qid in re.findall(r"(?m)^(Q[DIKW]\d+)\b", text):
                    if not qid.startswith(expected):
                        rep.add(ERROR, "question-level-id-mismatch", name,
                                f"`question-level: {level.group(1)}` admits {expected}<n> "
                                f"rows, but this register contains `{qid}`; the "
                                "partition × DIKW Question Group would be ambiguous")
            for bad in re.findall(r"🚫\s?F\s?only\b|🚫F-only", text):
                rep.add(WARN, "refusal-token-legacy", name,
                        f"`{bad}` is not the token: a mark's spelling includes its "
                        "spacing and the canonical form is `🚫 F-only` "
                        "(for-question 0.4.1); a checker grepping the token misses "
                        "every legacy cell")
            lmq = re.search(r"^## Log\s*$", text, re.M)
            queue_side = text[:lmq.start()] if lmq else text
            # ## Log is excluded: a receipt QUOTING a retired token is a
            # mention, not a mark (round 4 friction 2 — the sweep's own
            # receipt tripped the rule it was satisfying).
            spaced = len(re.findall(r"[🟡🚫⬜](?=[A-Za-z])", queue_side))
            if spaced:
                rep.add(WARN, "mark-spacing-legacy", name,
                        f"{spaced} cell mark(s) run straight into a word (🟡BI03, "
                        "🚫thin, ⬜OPEN): a mark's spelling includes its spacing "
                        "(insight-workflow §Marks), and two spellings in one "
                        "column defeat the mark; re-spell in an authorized sweep "
                        "that re-pads the table")
            # One Queue row holds one cell per PARTITION COLUMN, so a single
            # line may carry several `final` cells; matching once per line
            # missed every column after the first on live A00 (QI3·C, QI7·C).
            hits = []
            for line in text.splitlines():
                lm = re.match(r"(Q[DIKW]\d+)", line)
                if lm:
                    for pid in re.findall(r"🟡\s*([A-Z]{1,3}\d{2})\s+final", line):
                        hits.append((lm.group(1), pid))
            for qid, pid in hits:
                cited = next((c for c in d.rglob(f"{pid}-*/{pid}-*.md")
                              if "board" not in c.relative_to(d).parts), None)
                if cited is None:
                    rep.add(ERROR, "partial-final-ghost-page", name,
                            f"`🟡 {pid} final` cites a page this board does not hold")
                else:
                    log_path = record_path(plan_dir(cited.parent), cited.stem, "log")
                    log = (log_path.read_text(encoding="utf-8", errors="replace")
                           if log_path.is_file() else "")
                    # WARN, not ERROR, deliberately: a missing receipt is
                    # repairable debt on a settled decision, not broken
                    # structure — but only a canonical outline-log record
                    # heading counts. A sentence on the Page is prose, not a
                    # receipt (round 3 friction 10), and Page `## Log` was
                    # retired by workbench-task-draft 0.16.1.
                    heads = [line for line in log.splitlines()
                             if re.match(r"^###\s+\d{6}(?:\s+\d{3,4})?\s+·", line)]
                    if not any(qid in line and re.search(r"\bfinal\b", line)
                               for line in heads):
                        rep.add(WARN, "partial-final-no-page-receipt", name,
                                f"`{qid}` leans on a sentence in {pid} and {pid}'s "
                                f"`draft/records/{cited.stem}-log.md` does not record "
                                "it: the flip leaves TWO receipts "
                                "(insight-workflow §Marks), because a citation "
                                "invisible from the cited end cannot carry "
                                "staleness")


PARTITION_KEYWORDS = {
    "where", "and", "or", "not", "in", "eq", "ne", "lte", "gte", "declared",
    "unfiltered", "rows", "of", "no", "its", "own", "none", "null", "true",
    "false", "template", "row", "the", "test", "partition", "that", "passed",
    "contains", "every", "below", "fails", "clause", "construction", "which",
    "exempts", "from", "seated", "yaml", "cross", "full",
}


def _partition_rows(text):
    """MT00's partition register as (letter, name, population text, percent).

    Returns [] when the register does not parse. A rule that guesses at a
    layout it does not recognise reports noise, and noise is how a checker
    gets ignored.
    """
    m = re.search(r"\*\*Partitions\*\*.*?```text\n(.*?)```", text, re.S)
    if not m:
        return []
    rows, cur = [], None
    for line in m.group(1).splitlines():
        head = re.match(r"^([A-Z])\s{2,}(\S+)\s+(.*)$", line)
        if head:
            cur = [head.group(1), head.group(2), head.group(3)]
            rows.append(cur)
        elif cur is not None and line.strip():
            cur[2] += " " + line.strip()
    out = []
    for letter, nm, body in rows:
        pm = re.search(r"·\s*([\d.]+)\s*%", body)
        out.append((letter, nm, body, float(pm.group(1)) if pm else None))
    return out


def _filter_columns(body):
    """The column identifiers a partition's population block filters on."""
    body = re.sub(r"[\d,]+ of [\d,]+ rows.*", " ", body)
    body = re.sub(r"\S+\.yaml|\S+/", " ", body)
    return {w for w in re.findall(r"\b[a-z][a-z0-9_]{2,}\b", body)
            if w not in PARTITION_KEYWORDS}


def check_partition_register(text, name, rep):
    """The partition test's clause ① made mechanical (JL 260828, a live breach).

    `haipipe-insight-workflow` calls the three admission clauses "each
    mechanically checkable" and until 260828 none of the three was checked by
    anything. A00 registered `J · minorityzip` and `L · lowincome`, ran to
    136.79% coverage across seven subgroup partitions, grew a page under one,
    and this checker stayed green for the whole window; a human reader caught
    it. Clause ① is the one with a proof that needs no judgment: disjoint
    subgroups of ONE extract cannot cover more than the extract.

    F is the template and X is the cross group, and both are excluded by the
    statute itself — F "fails ① by construction, which the test exempts it
    from", and X holds no rows of its own.
    """
    rows = [r for r in _partition_rows(text) if r[0] not in ("F", "X")]
    if len(rows) < 2:
        return

    pcts = [r[3] for r in rows if r[3] is not None]
    if len(pcts) == len(rows):
        total = sum(pcts)
        # 100.5 not 100.0: the register prints rounded percentages, and a rule
        # that fires on rounding is a rule people learn to skip.
        if total > 100.5:
            named = " + ".join(f"{r[0]}·{r[1]} {r[3]:.2f}%" for r in rows)
            rep.add(ERROR, "partition-sum-over-100", name,
                    f"registered subgroup partitions cover {total:.2f}% of the "
                    f"extract ({named}) — disjoint groups of ONE extract cannot "
                    "exceed 100%, so clause ① is broken on arithmetic alone "
                    "(insight-workflow §The partition test): a coverage gap is "
                    "legal where an overlap never is, and overlapping groups "
                    "make every X contrast double-count the people they share")

    cols = {r[0]: _filter_columns(r[2]) for r in rows}
    for letter, nm, _, _ in rows:
        mine = cols[letter]
        if not mine:
            continue
        if all(not (mine & cols[other]) for other in cols if other != letter):
            rep.add(WARN, "partition-cross-cutting", name,
                    f"`{letter} · {nm}` filters on {sorted(mine)}, a column no "
                    "sibling partition filters on: a cut sharing no axis with "
                    "its siblings slices ACROSS them, which is a COVARIATE and "
                    "belongs in an I-page column, never a group "
                    "(insight-workflow §The partition test, the covariate row)")

    # A third rule was written and DROPPED the same hour: "a filter column MT00
    # names nowhere outside its own register". It fired four times on a
    # corrected A00 over `patient_gender`, which the page discusses at length in
    # prose without ever declaring as a column, and it passed `age` only because
    # substring matching found it inside "coverage". A rule that needs prose to
    # say a column's name in one exact place reports a documentation habit, not
    # a defect — and the covariate rule above already catches the case that
    # motivated it, since an unregistered filter column is almost always a
    # column no sibling shares.


def check_workbench_roster(d, rep):
    """A page subfolder is board material only if the roster names it.

    The roster states this as its own opening law, and it has been broken three
    times: `outline/` was real storage for four days before it had a row,
    `direction/` and `design/` shipped with contracts and no row, and
    `render/` shipped a SKILL that pointed at "the row this workbench expands"
    while that row did not exist. Prose could not stop it; a scan can.
    """
    roster = HERE.parent.parent / "workbench" / "workbench" / "ref" / "roster.md"
    if not roster.is_file():
        return
    names = set(re.findall(r'^\|\s*`([a-z_]+)/`', roster.read_text(encoding="utf-8"), re.M))
    if not names:
        return
    for md in sorted(d.rglob("*.md")):
        parts = md.relative_to(d).parts
        if "board" in parts or any(p.startswith("_") for p in parts):
            continue
        page = md.parent
        if md.stem != page.name:
            continue
        # A unit inside an evidence lane (`evidence/display/S-Display-1a/…`,
        # `evidence/probe/PP01/…`)
        # also keeps a `<name>/<name>.md`, and its `assets/`, `candidates/`,
        # `source/`, `versions/` are that workbench's own anatomy, not page
        # folders. The roster governs the page's direct children only; walking
        # into a lane reported 36 false rows on the MISQ board (JL 260831).
        if any(part in names for part in parts[:-1]):
            continue
        for sub in sorted(p for p in page.iterdir() if p.is_dir()):
            if sub.name.startswith("_") or sub.name in names:
                continue
            if (sub / f"{sub.name}.md").is_file():
                continue          # a child with its own face (a Job's Task) is a Page; it is checked as one
            rep.add(WARN, "workbench-not-rostered", f"{page.name}/{sub.name}/",
                    "this subfolder is not on the workbench roster, so no surface, "
                    "writer or boundary is declared for it; add the row first")
