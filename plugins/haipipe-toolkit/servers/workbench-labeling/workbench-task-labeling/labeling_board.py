"""The Board level: every labeling job on one Board."""
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote, urlparse

from live.labeling_job import (PHASES, _board_pages, _labeling_lane, _page_folder_candidate, is_labeling_corpus_page,
    is_labeling_surface_page)
from live.labeling_hold import _labeling_job
from live.labeling_model import (_esc, _g0_repair_request, _g0_retroactive_block, _meaning_allowed, _next_step,
    _open_definition_run, _round_words, _row, _view_model)
from live.labeling_page import _CSS


# ── Board level: every labeling job on one Board (zoom out) ───────────────────


def _board_root_url(path_q: str) -> str:
    path = urlparse(path_q or "").path
    return path[: -len("/board.md")] if path.endswith("/board.md") else path.rsplit("/", 1)[0]


def _job_urls(path_q: str, page: dict) -> tuple[str, str]:
    """(page-level Labeling URL, generated Board page URL) for one Board page."""
    root = _board_root_url(path_q)
    page_url = "/_board/page?path=" + quote(f"{root}/{page.get('file') or ''}", safe="/")
    labeling_url = "/_board/labeling?path=%s&file=%s&page=%s" % (
        quote(path_q), quote(page.get("file") or ""), quote(page_url))
    return labeling_url, page_url


def _job_row(page_src: Path, page: dict, path_q: str) -> dict:
    vm = _view_model(page_src)
    state, canonical, cal, config = vm["state"], vm["canonical"], vm["cal"] or {}, vm["config"]
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    manifest, sealed = vm["manifest"], vm["sealed"]
    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    rounds = cal.get("rounds") or []
    current = cal.get("current_round")
    labeled = sum(int(r.get("finals") or 0) for r in rounds)
    n_items = manifest.get("n_items")
    n_sealed = manifest.get("n_sealed", sealed.get("n_items"))
    n_dev = manifest.get("n_eligible")
    if n_dev is None and isinstance(n_items, int) and isinstance(n_sealed, int):
        n_dev = n_items - n_sealed
    prep = vm.get("preparation") or {}
    if prep.get("error"):
        kind, badge, rank = "repair", "Needs repair", 4
    elif prep.get("attached") and not (vm["root"] / "config.yaml").is_file():
        kind, badge, rank = ("preparing", "Create Contract" if prep.get("linked") else "Prepare corpus", 1)
        receipt = prep.get("receipt") or {}
        source = {"name": (prep.get("owner_reference") or {}).get("source_id")
                  or receipt.get("snapshot_id") or ""}
        n_dev, n_sealed = receipt.get("n_eligible"), receipt.get("n_sealed")
    elif state["authority_hold"]:
        kind, badge, rank = "hold", "Read-only", 5
    elif _g0_retroactive_block(vm):
        kind, badge, rank = "repair", "Invalid G0", 4
    elif _g0_repair_request(vm):
        kind, badge, rank = "confirm", "Restore G0", 1
    elif state["canonical_integrity_errors"]:
        kind, badge, rank = "repair", "Needs repair", 4
    elif _open_definition_run(vm) and _meaning_allowed(vm):
        kind, badge, rank = "confirm", "Discuss meanings", 1
    elif canonical.get("meaning_definitions_missing"):
        kind, badge, rank = "confirm", "Define meanings", 1
    elif canonical and canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation":
        kind, badge, rank = "confirm", "Confirm meaning", 1
    elif cal.get("phase") == "P1" and current:
        kind, badge, rank = "labeling", f"Labeling {current['finals']}/{current['batch_size']}", 0
    elif (cal.get("phase") == "P1" and rounds and rounds[-1]["state"] == "judged"
          and rounds[-1].get("calibration_status") == "running"):
        kind, badge, rank = "labeling", "Finish Run", 1
    elif cal.get("phase") == "P1" and rounds and rounds[-1]["state"] == "judged":
        kind, badge, rank = "judged", f"{_round_words(rounds[-1]['round_id'])} done", 3
    elif cal.get("phase") == "P1":
        kind, badge, rank = "ready", "Start round 1", 2
    else:
        kind, badge, rank = "other", str(canonical.get("phase") or "P0"), 4
    next_line, _ = _next_step(vm)
    labeling_url, page_url = _job_urls(path_q, page)
    return {
        "id": (vm.get("job") or {}).get("id") or page.get("id"), "title": page.get("title"),
        "file": page.get("file"),
        "target": construct.get("name") or "", "question": construct.get("question") or "",
        "source": source.get("name") or "", "n_dev": n_dev, "n_sealed": n_sealed,
        "human": authority.get("human_id") or "", "kind": kind, "badge": badge, "rank": rank,
        "labeled": labeled, "current": current, "rounds": len(rounds),
        "phase": " ".join(x for x in (str(canonical.get("phase") or ""), dict(PHASES).get(str(canonical.get("phase") or ""), "")) if x),
        "g0": bool(canonical.get("g0_passed")) if canonical else None,
        "runs": len(vm["runs"]) + len(prep.get("runs") or []),
        "next": next_line, "labeling_url": labeling_url, "page_url": page_url,
    }


def board_jobs(board_dir: Path, path_q: str, probe: bool = False) -> dict:
    """Every Page on the Board that owns a labeling/ job, plus the ones that do not."""
    pages = _board_pages(Path(board_dir))
    jobs, empty = [], []
    for page in pages:
        page_src = Path(board_dir) / (page.get("file") or "")
        if not is_labeling_surface_page(page_src):
            continue
        lane, _ = _labeling_lane(page_src)
        if (not (lane / "config.yaml").is_file()
                and not (lane / "preparation-ref.yaml").is_file()
                and not (lane / "preparation-owner.yaml").is_file()):
            if is_labeling_corpus_page(page_src):
                labeling_url, _ = _job_urls(path_q, page)
                candidate = _page_folder_candidate(page_src)
                ready = candidate.is_file() and not candidate.is_symlink()
                job = _labeling_job(page_src)
                empty.append({"id": (job or {}).get("id") or page.get("id"), "title": page.get("title"),
                              "labeling_url": labeling_url + "&space=data&view=preparation",
                              "badge": "Prepare corpus" if ready else "Create Page folder"})
            continue
        if probe:
            jobs.append({"id": page.get("id")})
            continue
        try:
            jobs.append(_job_row(page_src, page, path_q))
        except Exception as error:  # one broken job must not hide the others
            labeling_url, page_url = _job_urls(path_q, page)
            jobs.append({"id": page.get("id"), "title": page.get("title"), "kind": "repair",
                         "badge": "Needs repair", "rank": 4, "next": type(error).__name__,
                         "labeling_url": labeling_url, "page_url": page_url})
    jobs.sort(key=lambda j: (j.get("rank", 9), str(j.get("id"))))
    return {"jobs": jobs, "empty": empty}


def render_board(board_dir: Path, path_q: str) -> str:
    data = board_jobs(board_dir, path_q)
    jobs = data["jobs"]
    waiting = [j for j in jobs if j["kind"] in {"labeling", "confirm", "ready", "preparing"}]
    if not jobs:
        headline = "No Page on this Board has a labeling job yet."
    elif waiting:
        headline = f"{len(waiting)} of {len(jobs)} jobs wait for you. Start with {waiting[0]['id']}: {waiting[0]['badge'].lower()}."
    else:
        headline = f"{len(jobs)} jobs. None is waiting for you right now."
    def record(job: dict) -> str:
        pill = {"preparing": "acc", "confirm": "acc", "labeling": "acc", "ready": "acc", "judged": "ok",
                "hold": "mut", "repair": "warn"}.get(job["kind"], "mut")
        data_bits = [x for x in (
            job.get("source") or "",
            f"{job['n_dev']} to label" if job.get("n_dev") is not None else "",
            f"{job['n_sealed']} held back for the test" if job.get("n_sealed") is not None else "",
            f"{job['labeled']} labeled" if job.get("labeled") else "",
        ) if x]
        rows = [
            _row("Target", f"<code>{_esc(job.get('target') or '')}</code>") if job.get("target") else "",
            _row("Data", _esc(" · ".join(data_bits))) if data_bits else "",
            _row("Labeler", _esc(job.get("human"))) if job.get("human") else "",
            _row("Phase", _esc(job.get("phase"))) if job.get("phase") else "",
            _row("Meanings", '<span class=ok>confirmed (G0)</span>' if job.get("g0") else "not confirmed")
            if job.get("g0") is not None else "",
            _row("Rounds", _esc(f'{job["rounds"]} · {job["labeled"]} labeled')) if job.get("rounds") else "",
        ]
        rows.append(_row("Next", _esc(job["next"])))
        return (
            f'<a class="rec job {_esc(job["kind"])}" href="{_esc(job["labeling_url"])}" data-job="{_esc(job["id"])}">'
            f'<div class=rh><span class=rid>{_esc(job["id"])}</span>'
            f'<span class=rt>{_esc(job.get("question") or job.get("title") or job.get("target"))}</span>'
            f'<span class="pill {pill}">{_esc(job["badge"])}</span></div>'
            f'<div class=rrows>{"".join(rows)}</div></a>'
        )

    groups = ""
    if waiting:
        groups += '<div class=rgrp>Waiting for you</div>' + "".join(record(j) for j in waiting)
    others = [j for j in jobs if j not in waiting]
    if others:
        groups += '<div class=rgrp>Other jobs</div>' + "".join(record(j) for j in others)
    if not jobs:
        groups = f'<p class=mut>{_esc(headline)}</p>'
    empty = ""
    if data["empty"]:
        links = "".join(
            f'<a class="rec job" href="{_esc(e["labeling_url"])}">'
            f'<div class=rh><span class=rid>{_esc(e["id"])}</span>'
            f'<span class=rt>{_esc(e.get("title") or e["id"])}</span>'
            f'<span class="pill mut">{_esc(e["badge"])}</span></div></a>'
            for e in data["empty"]
        )
        empty = f'<div class=card><h2>Pages before Contract</h2>{links}</div>'
    name = Path(board_dir).name
    tally = f'{len(waiting)} waiting · {len(jobs)} jobs'
    # The shared shell (servers/README.md "Adding a workbench", rule 1): title, band, then the
    # Space row with Guide first; this level has one Space, its jobs, in one box.
    document = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>Labeling · {_esc(name)}</title><style>{_CSS}{_BOARD_CSS}</style></head><body>'
        '<h1>🏷 Labeling · all jobs</h1>'
        f'<div class=wb-band>{_esc(tally)} · <b>Next:</b> {_esc(headline)}</div>'
        '<nav class=spaces role=tablist aria-label="Labeling Spaces">'
        '<button class="space on" type=button role=tab aria-selected=true data-space=jobs>Jobs</button></nav>'
        '<section class="panel board-jobs" data-space=jobs><div class=space-main>'
        '<div class=card><h2>Labeling jobs</h2>'
        f'{groups}</div>{empty}</div></section>'
        '</body></html>'
    )
    from live.workbench_guide import mount_guide
    return mount_guide(document, "labeling", {"path": path_q, "file": "board.md"},
                       "nav.spaces", "section.panel")


_BOARD_CSS = """
a.rec{display:block;color:var(--fg);text-decoration:none;border-radius:6px;margin:0 -6px;padding:8px 6px 6px}
a.rec:hover,a.rec:focus-visible{background:color-mix(in srgb,var(--acc) 6%,var(--card));outline:none}
.rgrp:first-of-type{margin-top:4px}
.board-jobs>.space-main{border:1px solid var(--line);border-radius:10px;padding:12px 16px 16px}
.board-jobs>.space-main>.card:first-child{border-top:0;padding-top:0}
"""
