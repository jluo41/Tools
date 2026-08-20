#!/usr/bin/env python3
"""Check every stage contract against stages/CONTRACT.md, and against a real paper.

Two things go wrong with a contract and neither shows up until a stage runs:
a required field goes missing, or a declared path stops existing on the paper the
stage would write to. This checks both.

    python3 check-contracts.py                      # form only
    python3 check-contracts.py <paper-root>         # form + resolve every path there

Exit 1 on any missing required field, any filename that disagrees with the
board's resolution rule, or any dangling path that is not declared `blocked_on:`.
"""

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAGES = HERE / "stages"

# The S filename rule belongs to Board tooling (QC2). Import it rather than
# re-spelling it here, so a checker can never disagree with the creator.
_spec = importlib.util.spec_from_file_location(
    "board_stage", HERE.parents[1] / "board" / "haipipe-board" / "cli" / "stage.py")
board_stage = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(board_stage)
resolve_filename = board_stage.resolve_filename

REQUIRED = [
    "key", "order", "title", "one_line",
    "board_family", "board_unit",
    "phases", "gates", "probe_depth", "runs", "needs_paper",
    "artifact", "template", "sections", "formatting",
    "probes", "q_id_pattern", "q_anchor",
    "upstream", "downstream", "handoff",
    "done_criteria", "closed_when", "exit_when",
]
FAMILIES = {"Open", "Seed", "Work", "Venue", "Literature", "Value", "Display", "Main",
            "Appendix", "Submission", "Round", "Label"}
PATH_FIELD = re.compile(
    r"^\s*([a-z][a-z0-9_]*):\s+"
    r"(0-lifecycle/\S+|0-sections/\S+|0-displays/\S+)"
)
RETIRED_PATH_PREFIXES = ("0-sections/", "0-displays/")
RETIRED = {"log": "retired 2026-07-26; the S face carries the history",
           "inputs": "retired by QF2; use the page's requires: and optional read_order:"}
ON_DEMAND_PATHS = {"archive", "display_request", "inbox"}


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def fields(fm):
    out = {}
    for line in fm.splitlines():
        m = re.match(r"^([a-z][a-z0-9_]*):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).split(" #", 1)[0].strip().strip('"\'')
    return out


def main():
    paper = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    if paper and not paper.is_dir():
        sys.exit(f"not a paper root: {paper}")

    problems, notes = [], []
    # FOLLOW index.yml's `dir:` values, never the stages/ folder listing
    # (260803). The stage contracts moved out to their delivery group,
    # `S01-opening/seed/` and so on, and a glob over `stages/` then found
    # nothing while still reporting "form ok".
    import re as _re
    _txt = (STAGES / "index.yml").read_text(encoding="utf-8")
    dirs = []
    for _d in _re.findall(r"dir:\s*([^,\s}]+)", _txt):
        _p = (STAGES / _d).resolve()
        if _p.is_dir():
            dirs.append(_p)
    dirs = sorted(set(dirs))
    if not dirs:
        sys.exit("FAIL: index.yml resolved ZERO stage dirs; a checker that looks "
                 "at nothing must not report ok (each dir: is relative to stages/)")

    for d in dirs:
        contract = d / "stage.md"
        fm = frontmatter(contract.read_text(encoding="utf-8"))
        f = fields(fm)
        where = f"{d.name}"

        for key in REQUIRED:
            if key not in f:
                problems.append(f"{where}: missing required field `{key}`")
        for key, why in RETIRED.items():
            if key in f:
                problems.append(f"{where}: retired field `{key}` is back ({why})")
        for line in fm.splitlines():
            m = PATH_FIELD.match(line)
            if m and m.group(2).startswith(RETIRED_PATH_PREFIXES):
                problems.append(
                    f"{where}: `{m.group(1)}` names retired deliverable path "
                    f"`{m.group(2)}`; use unnumbered `sections/` / `displays/`"
                )

        if f.get("board_family") not in FAMILIES and "or" not in f.get("board_family", ""):
            problems.append(f"{where}: board_family `{f.get('board_family')}` is not a family")

        axis = [k for k in ("venue_free", "venue_aligned", "venue_role") if f.get(k)]
        if len(axis) != 1:
            problems.append(f"{where}: must declare exactly one of venue_free / venue_aligned / "
                            f"venue_role, found {axis or 'none'}")

        # the filename must be what board tooling would compose
        if f.get("runs") == "once":
            if "blocked_on" in f:
                notes.append(f"{where}: filename resolution deferred, blocked on {f['blocked_on']}")
            elif "board_slug" not in f:
                problems.append(f"{where}: runs: once but no board_slug, so the S filename "
                                f"cannot be resolved")
            else:
                want = resolve_filename(f["board_family"], f["board_unit"],
                                        f["board_slug"])[0]
                got = f["artifact"].rsplit("/", 1)[-1]
                if got != want:
                    problems.append(f"{where}: artifact filename `{got}` disagrees with the "
                                    f"resolution rule (`{want}`)")
        elif f.get("runs") == "per-unit":
            for key in ("unit", "units_from"):
                if key not in f:
                    problems.append(f"{where}: runs: per-unit but no `{key}`")

        if not paper:
            continue

        # A stage that has not run on this paper declares nothing but intentions:
        # its inputs are not there yet because it was never asked for them. Only a
        # stage whose artifact (or legacy fallback) is on disk can have its declared
        # paths judged. Otherwise "not reached yet" reads as "contract is broken".
        declared = [m.group(2).split("#")[0].strip()
                    for m in (PATH_FIELD.match(l) for l in fm.splitlines()) if m]
        ran = any((paper / p).exists() for p in declared
                  if not any(c in p for c in "{<*"))
        if not ran:
            notes.append(f"{where}: not run on {paper.name}; declared paths not judged")
            continue

        for line in fm.splitlines():
            m = PATH_FIELD.match(line)
            if not m:
                continue
            field, path = m.group(1), m.group(2).split("#")[0].strip()
            if field in RETIRED:
                continue
            # A fallback is the path used when the artifact is ABSENT, so on a
            # migrated paper it is absent by design. The pair is checked below.
            if field == "artifact_fallback":
                continue
            if any(c in path for c in "{<*"):
                # A pattern cannot be resolved without a unit. What IS checkable is that the
                # container it will be created in exists: everything up to the first templated
                # segment. Deeper directories (a pitch archive, a new section folder) are
                # created on demand, so a missing one is information, not a defect.
                parts = path.split("/")
                fixed = [p for i, p in enumerate(parts)
                         if not any(c in p for c in "{<*")
                         and all(not any(c in q for c in "{<*") for q in parts[:i])]
                if len(fixed) >= 2 and not (paper / "/".join(fixed[:2])).exists():
                    problems.append(f"{where}: {field}: {path} — container "
                                    f"`{'/'.join(fixed[:2])}` does not exist")
                elif fixed and not (paper / "/".join(fixed)).exists():
                    notes.append(f"{where}: {field}: {path} — `{'/'.join(fixed)}` "
                                 f"not created yet")
                continue
            if (paper / path).exists():
                continue
            if field in ON_DEMAND_PATHS:
                notes.append(f"{where}: {field}: {path} — created only when work is filed")
                continue
            if field == "artifact" and "artifact_fallback" in f \
                    and (paper / f["artifact_fallback"]).exists():
                notes.append(f"{where}: {field}: {path} — absent; this paper predates the "
                             f"S-face restructure, so the run uses artifact_fallback "
                             f"`{f['artifact_fallback']}`")
                continue
            if "blocked_on" in f and field == "artifact":
                notes.append(f"{where}: {field}: {path} — DECLARED dangling, "
                             f"blocked on {f['blocked_on']}")
            else:
                problems.append(f"{where}: {field}: {path} — does not exist on {paper.name}")

    print(f"checked {len(dirs)} stage contracts against {STAGES.parent.name}/stages/CONTRACT.md")
    if paper:
        print(f"resolved declared paths against {paper}")
    for n in notes:
        print(f"  KNOWN   {n}")
    for p in problems:
        print(f"  FAIL    {p}")
    if problems:
        print(f"\n{len(problems)} problem(s)")
        return 1
    print(f"\nform ok" + (f"; every path resolves ({len(notes)} declared blocked)" if paper else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
