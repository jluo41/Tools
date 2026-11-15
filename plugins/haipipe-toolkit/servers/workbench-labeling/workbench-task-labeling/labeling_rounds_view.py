"""The Labeling Space: a round's draw, the chat prompts, the label definitions, the rounds and the
guideline versions."""
from __future__ import annotations

import json
import re
from pathlib import Path

from live.labeling_job import _canonical_job_module, _read_json
from live.labeling_hold import _calibration_module, _definition_module
from live.labeling_model import (_card, _clean_keywords, _current_policy, _esc, _job_tasks_card, _job_where, _later,
    _load_mapping, _md_inline, _md_table, _round_words, _row, _space_mapping_ref, _unsure_words, _when)
from live.labeling_embedding_view import _build_label, _engine_command, _group_color, _repo_relative
from live.labeling_data_view import _meaning_gate


def _round_draw(root: Path, round_id: str) -> dict:
    """What the draw froze for one round: how it was drawn, and which items it picked."""
    module = _calibration_module()
    path = root / "rounds" / round_id
    draw: dict = {"items": [], "card": {}, "manifest": {}}
    if module is None or not path.is_dir():
        return draw
    try:
        manifest = _load_mapping(path / "manifest.yaml")
        card = {}
        if (path / "card.md").is_file():
            for line in (path / "card.md").read_text(encoding="utf-8").splitlines():
                if ": " in line and not line.startswith(("#", "-", " ")):
                    key, value = line.split(": ", 1)
                    card[key.strip()] = value.strip()
        states = module._item_states(path)
        config = _load_mapping(root / "config.yaml")
        corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
        text_field = str(corpus.get("text_field") or "text")
        context_field = str(corpus.get("context_field") or "context_prev")
        rows = {str(r.get("item_id")): r for r in module._corpus_rows(root)}
        notes: dict = {}
        for note in module._read_jsonl(path / "sessions" / "feedback.jsonl"):
            notes.setdefault(str(note.get("item_id")), []).append(note)
        items = []
        for row in module._read_jsonl(path / "human_batch.jsonl"):
            item_id = str(row.get("item_id"))
            entry = states.get(item_id) or {}
            final = entry.get("final")
            shown = "show" in (entry.get("kinds") or [])
            source = rows.get(item_id) or {}
            items.append({
                "item_id": item_id, "order": row.get("order"),
                "probability": row.get("selection_probability"),
                "label": ((final or {}).get("payload") or {}).get("class_label") or ("unresolved" if final else None),
                "first": ((entry.get("first") or {}).get("payload") or {}).get("class_label"),
                "state": "labeled" if final else ("answered" if entry.get("first") else "waiting"),
                # text only once the person has been shown the item, so the table never shows it first
                "text": str(source.get(text_field) or "") if shown else None,
                "context": str(source.get(context_field) or "") if shown else None,
                "feedback": notes.get(item_id, []),
            })
        draw.update({"items": items, "card": card, "manifest": manifest})
    except Exception:  # the page must still render
        return draw
    return draw


def _turns_html(context: str) -> str:
    """Earlier conversation turns, one line per speaker, folded under an item's text."""
    out = []
    for line in str(context or "").splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z][A-Za-z_ ]{0,20}):\s?(.*)$", line)
        who, body = (m.group(1), m.group(2)) if m else ("", line)
        if who.strip().lower() in {"lamda", "assistant", "bot", "chatbot", "ai", "model", "gpt", "claude"}:
            who = "AI"
        out.append(f'<div class=turn>{f"<b>{_esc(who)}</b>" if who else ""}<span>{_esc(body)}</span></div>')
    return "".join(out)


def _draw_sentence(draw: dict, pool) -> str:
    parts = [f'{draw.get("method") or "random"} draw']
    if pool:
        parts.append(f"from the {pool} items to label")
    if draw.get("seed") is not None:
        parts.append(f'seed {draw["seed"]}')
    return ", ".join(parts)


def _policy_words(version) -> str:
    """'G_00' -> 'G_00, the first draft'; later versions keep their number."""
    version = str(version or "")
    return f"{version}, the first draft" if version == "G_00" else version


def _map_groups(vm: dict) -> tuple[dict, dict, str]:
    """Each item's group in the newest embedding build, each group's keywords, and the build's name."""
    builds = ((vm.get("embedding") or {}).get("builds")) or []
    if not builds:
        return {}, {}, ""
    newest = builds[-1]
    groups = {str(row.get("item_id")): row.get("group") for row in newest.get("map") or []}
    keywords = {int(g["group"]): " · ".join(_clean_keywords(g.get("keywords"))[:4])
                for g in (newest.get("groups") or {}).get("groups") or []}
    return groups, keywords, _build_label(newest["manifest"]["model"]["id"], newest["manifest"].get("settings"))


def _items_table(draw: dict, groups: dict, keywords: dict) -> str:
    """One row per drawn item: # · Item · Text · Group · State · Feedback."""
    records = []
    for item in draw["items"]:
        group = groups.get(item["item_id"])
        if item["state"] == "labeled":
            pill = f'<span class="pill ok">{_esc(item["label"])}</span>'
        elif item["state"] == "answered":
            pill = f'<span class="pill acc">first: {_esc(item["first"])}</span>'
        else:
            pill = '<span class="pill mut">waiting</span>'
        group_tag = (f'<span class="pill mut" title="{_esc(keywords.get(int(group), ""))}">'
                     f'<i class=dot style="background:{_group_color(group)}"></i>'
                     f'G{int(group) + 1}</span>') if group is not None else ""
        if item.get("text") is None:
            text_cell = '<span class=mut>not opened yet</span>'
        else:
            text_cell = (f'<div class=reply>{_esc(item["text"])}</div>'
                         + (f'<details class=ctx><summary>conversation before it</summary>'
                            f'<div class=convo>{_turns_html(item["context"])}</div></details>' if item.get("context") else ""))
        notes_cell = "".join(
            f'<div class=fb><b>{"Model" if n.get("author") == "model" else "You"}</b> {_esc(n.get("text"))}</div>'
            for n in item.get("feedback") or [])
        records.append(
            f'<tr><td class=num>#{_esc((item.get("order") or 0) + 1)}</td><td class=nowrap>item {_esc(item["item_id"])}</td>'
            f'<td>{text_cell}</td><td>{group_tag}</td><td>{pill}</td><td>{notes_cell}</td></tr>'
        )
    return ('<div class=scroll><table class=items><thead><tr><th>#</th><th>Item</th><th>Text</th><th>Group</th><th>State</th>'
            '<th>Feedback</th></tr></thead>'
            f'<tbody>{"".join(records)}</tbody></table></div>')


def _chat_prompt(vm: dict, current: dict, draw: dict, *, run: dict | None = None) -> str:
    """The text to paste into a Claude chat to go on labeling this round; it writes nothing."""
    root, config = vm["root"], vm.get("config") or {}
    round_id = str(current.get("round_id") or "")
    page = vm.get("page_candidate") or vm.get("page_src") or root.parent / f"{root.parent.name}.md"
    board = next((folder / "board.md" for folder in page.parent.parents
                  if (folder / "board.md").is_file()), None)
    run_id = str((run or {}).get("run") or current.get("calibration_run") or "")
    matching = run or next((r for r in vm.get("runs") or [] if r.get("run") == run_id), None)
    run_state = str(matching.get("status") or "unknown") if matching else ("not started" if not run_id else "recorded")
    skills = _run_type_skills().get("human-calibration") or []
    card = draw.get("card") or {}
    released_card = bool(card.get("released_at") and card.get("released_by")
                         and (root / "rounds" / round_id / "card.md").is_file())
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = (config.get("labels") or {}).get("values") if isinstance(config.get("labels"), dict) else None
    human = ((config.get("authority") or {}) if isinstance(config.get("authority"), dict) else {}).get("human_id") or "me"
    tag = lambda i: f'#{(i.get("order") or 0) + 1} item {i["item_id"]}'
    finals = [f'{tag(i)} (first: {i["first"]})' for i in draw["items"] if i["state"] == "answered"]
    todo = [tag(i) for i in draw["items"] if i["state"] == "waiting"][:5]
    lines = [
        f'Continue labeling {_round_words(current.get("round_id"))} of {root.parent.name} with me ({human}).',
        f'Board: {_repo_relative(board) if board else "none (standalone Page)"}',
        f'Page: {_repo_relative(page)}',
        f'Folder: {_repo_relative(root.parent)}',
        f"Job folder: {_job_where(vm)}",
        f'Run Type: human-calibration · target: {round_id}',
        f'Declared Skills: {" · ".join(skills) if skills else "see Run Type map"}',
        f'Run: {run_id or "none yet"} · status: {run_state}',
        f'Prerequisite: G0 {"passed" if (vm.get("canonical") or {}).get("g0_passed") else "not verified"}; '
        f'released Card {"verified" if released_card else "not verified"}.',
        f'Question: {construct.get("question") or construct.get("name") or ""}'
        + (f'  Labels: {" · ".join(str(v) for v in labels)}' if labels else ""),
        f'Progress: {current.get("finals", 0)} of {current.get("batch_size", len(draw["items"]))} labeled.',
    ]
    if finals:
        lines.append("Waiting for my final: " + ", ".join(finals))
    if todo:
        lines.append("Next items: " + ", ".join(todo))
    lines += [
        "",
        'Follow /haipipe-labeling-rounds, JUDGE "By chat" (engine/calibration.py):',
        "1. Call open_item for the next unfinished item, even if it was shown earlier. Show me its conversation and AI reply.",
        "2. Record only what I say: record_first for my first answer, then show any available reference observations and your view.",
        "3. record_final when I keep or change; add_feedback for a note about an item.",
        "If first or lock was already recorded, open_item finishes a missing reveal; never repeat record_first.",
        "Never show reference observations or your view before my first answer is recorded.",
    ]
    return "\n".join(lines)


def _meaning_prompt(vm: dict, run: str | None = None) -> str:
    """The definition-discussion prompt: start a new discussion, or resume ``run``. It writes nothing itself."""
    config = vm.get("config") or {}
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    human = authority.get("human_id") or "me"
    values = [str(v) for v in labels.get("values") or []]
    meanings = labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {}
    where = _job_where(vm)
    tool = _engine_command("definition_discussion.py", "start", "--job-root", where,
                           "--human-id", human)
    lines = [
        f"Discuss what the labels of {vm['root'].parent.name} mean with me ({human}), one label at a time. "
        "I decide what each label means; you ask and propose.",
        f"Job folder: {where}",
        f'Question: {construct.get("question") or construct.get("name") or ""}',
    ]
    rule = " ".join(str(x) for x in (construct.get("seed"), construct.get("scope")) if x)
    if rule:
        lines.append(f"Rule: {rule}")
    lines.append("Labels now:")
    lines += [f"- {v}: {meanings.get(v) or ''}" for v in values]
    module = _definition_module()
    state = module.state(vm["root"], run) if (module and run) else None
    if state:
        settled = [f'{r["label"]} ({r["decision"]})' for r in state["labels"] if r["decision"]]
        lines.append(f"Run: {run} (open). Settled: {', '.join(settled) or 'none yet'}. "
                     f"Open: {', '.join(state['open']) or 'none'}.")
    else:
        lines.append("Start the Run: " + tool)
    lines += [
        "",
        "How (engine/definition_discussion.py):",
        "1. Take the next open label. Ask me one question at a time: what makes a response this label and not "
        "its neighbour? Propose clearer wording, one made-up example, and one made-up counterexample.",
        "2. Never use an item from a round as an example, and never say how you would label one.",
        "3. Keep the talk with say: --author model for your questions and proposals, --author human for my words.",
        "4. When I settle a label, record only my decision with decide: --keep, or --meaning with my wording, "
        "plus --reason in my words.",
        "5. When every label is settled, run close (add --open-question for anything we left open). "
        "If a wording changed, I press Confirm meaning again in Labeling > Definition.",
    ]
    return "\n".join(lines)


def _label_definitions(vm: dict) -> str:
    """Labeling → Definition: what each label means; discussing them is the definition-discussion Run."""
    config = vm.get("config") or {}
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    uncertainty = config.get("uncertainty") if isinstance(config.get("uncertainty"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    values = [str(v) for v in labels.get("values") or []]
    if not values:
        return _card("Label definitions", "<p class=mut>No labels are written in config.yaml yet.</p>")
    meanings = labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {}
    region_meanings = regions.get("meanings") if isinstance(regions.get("meanings"), dict) else {}
    between = [str(r) for r in regions.get("values") or [] if len(str(r)) > 1]
    receipt = authority.get("meaning_receipt") if isinstance(authority.get("meaning_receipt"), dict) else {}
    still_valid = (vm.get("canonical") or {}).get("meaning_receipt_valid", True)  # a stale receipt is no confirmation
    confirmed = (f'by {_esc(receipt.get("human_id"))}, {_esc(_when(receipt.get("confirmed_at")))}'
                 if receipt.get("confirmed_at") and still_valid else "")
    rows = "".join(
        f'<tr><td class=nowrap><b>{_esc(v)}</b></td><td>{_esc(meanings.get(v) or "")}</td></tr>' for v in values)
    between_rows = "".join(
        f'<tr><td class=nowrap><code>{_esc(r)}</code></td><td>'
        + (_esc(region_meanings[r]) if region_meanings.get(r) else '<span class=mut>not defined yet</span>')
        + '</td></tr>' for r in between)
    return _card("Label definitions", "".join([
        _row("question", _esc(construct.get("question") or construct.get("name") or "")),
        _row("judge", _esc(construct.get("seed"))) if construct.get("seed") else "",
        _row("scope", _esc(construct.get("scope"))) if construct.get("scope") else "",
        _row("confirmed", confirmed),
        '<div class=scroll><table class=defs><thead><tr><th>Label</th><th>What it means</th></tr></thead>'
        f'<tbody>{rows}</tbody></table></div>',
        ('<h3 class=sub>In-between cases</h3>'
         '<div class=scroll><table class=defs><thead><tr><th>Case</th><th>What it means</th></tr></thead>'
         f'<tbody>{between_rows}</tbody></table></div>') if between else "",
        (f'<p class=mut>How sure: {_esc(" · ".join(_unsure_words(v) for v in uncertainty["levels"]))} unsure. '
         f'{_esc(uncertainty.get("meaning") or "")}</p>') if uncertainty.get("levels") else "",
    ]))


def _discussion_view(vm: dict) -> str:
    """Each definition-discussion Run: every label before and after, and what stayed open.

    Starting or resuming a discussion is the Runs panel's `+ New Run` / `Resume` (JL 260927); this view
    shows what the discussions decided. The newest shows; picking a run in the panel shows that one.
    """
    module = _definition_module()
    runs = [r for r in vm.get("runs") or [] if r["operation"] == "definition-discussion"]
    records = []
    for i, run in enumerate(reversed(runs)):  # newest first, shown
        try:
            state = module.state(vm["root"], run["run"]) if module else None
        except (OSError, ValueError, KeyError):
            state = None
        if not state:
            continue
        rows = "".join(
            f'<tr><td class=nowrap><b>{_esc(r["label"])}</b></td><td>{_esc(r["before"])}</td>'
            f'<td class="{"changed" if r["decision"] == "change" else "mut"}">'
            f'{_esc(r["after"] if r["decision"] == "change" else ("kept" if r["decision"] else ""))}</td>'
            f'<td>{_esc(r["reason"])}</td></tr>' for r in state["labels"])
        questions = "".join(f"<li>{_esc(q)}</li>" for q in state["open_questions"])
        records.append(
            f'<div class=discrec data-target="{_esc(run.get("target") or "")}"{" hidden" if i else ""}>'
            '<div class=scroll><table class=defs><thead><tr><th>Label</th><th>Before</th><th>After</th>'
            f'<th>Why</th></tr></thead><tbody>{rows}</tbody></table></div>'
            + (f'<h3 class=sub>Still open</h3><ul>{questions}</ul>' if questions else "") + '</div>')
    return _card("Discussion", "".join(records)) if records else ""


def _rounds_view(vm: dict) -> str:
    cal, root = vm["cal"] or {}, vm["root"]
    rounds = cal.get("rounds") or []
    if not rounds:
        return _card("Rounds", "<p class=mut>No round yet.</p>")
    groups, keywords, model_name = _map_groups(vm)
    current = cal.get("current_round") or {}
    labeling_now = bool(current) and not (vm.get("canonical") or {}).get("hold")
    cards = []
    for r in reversed(rounds):
        draw = _round_draw(root, r["round_id"])
        is_current = labeling_now and r["round_id"] == current.get("round_id")
        manifest, card = draw["manifest"], draw["card"]
        drew = manifest.get("draw") if isinstance(manifest.get("draw"), dict) else {}
        pool = manifest.get("development_pool_size")
        probability = next((i["probability"] for i in draw["items"] if i.get("probability")), None)
        state_words = {"judging": "you are labeling", "judged": "all labeled; waiting to be closed",
                       "released": "ready to label"}.get(str(r["state"]), str(r["state"]))
        rows = [
            _row("state", _esc(state_words)),
            _row("started", _esc(", ".join(x for x in (card.get("released_by"), _when(card.get("released_at"))) if x)))
            if card.get("released_by") else "",
            _row("how drawn", _esc(_draw_sentence(drew, pool))) if drew or pool else "",
            _row("each item's chance", _esc(f'{probability * 100:.1f}% (1 in {round(1 / probability)})'))
            if isinstance(probability, (int, float)) and probability else "",
            _row("guideline", _esc(_policy_words(manifest.get("policy_version") or card.get("policy"))))
            if manifest.get("policy_version") or card.get("policy") else "",
        ]
        seen_groups = {int(groups[i["item_id"]]) for i in draw["items"] if groups.get(i["item_id"]) is not None}
        coverage = ""
        if groups and seen_groups:
            total_groups = len({g for g in groups.values() if g is not None})
            coverage = f'<p class=mut>map groups {len(seen_groups)} / {total_groups} · {_esc(model_name)}</p>'
        started_at = _when(card.get("released_at")) if card.get("released_at") else ""
        cards.append(
            f'<details class=roundbox data-target="{_esc(str(r["round_id"]).replace("_", "-"))}"{" open" if is_current else ""}><summary><b>{_esc(_round_words(r["round_id"]).capitalize())}</b>'
            f'<span>{_esc(r["finals"])} of {_esc(r["batch_size"])} labeled</span>'
            f'<span class=mut>{_esc(state_words)}{" · started " + _esc(started_at) if started_at else ""}</span></summary>'
            f'{"".join(rows)}'
            f'<h3 class=sub>The items this round drew · {len(draw["items"])}</h3>'
            f'{_items_table(draw, groups, keywords)}'
            f'{coverage}</details>'
        )
    return "".join(cards)


def _guideline_html(text: str) -> str:
    """Headings, bullet lists, paragraphs, bold and code; the leading # title is the card's own title."""
    out: list[str] = []
    para: list[str] = []
    items: list[str] = []

    def flush() -> None:
        if para:
            out.append(f'<p>{_md_inline(" ".join(para))}</p>')
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{_md_inline(i)}</li>" for i in items) + "</ul>")
            items.clear()

    for n, raw in enumerate(text.splitlines()):
        line = raw.rstrip()
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        bullet = re.match(r"^\s*[-*]\s+(.*)$", line)
        if heading:
            flush()
            if not (len(heading.group(1)) == 1 and not out):
                out.append(f"<h3>{_md_inline(heading.group(2))}</h3>")
        elif bullet:
            if para:
                flush()
            items.append(bullet.group(1))
        elif not line.strip():
            flush()
        elif items and raw.startswith("  "):
            items[-1] += " " + line.strip()
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    return "".join(out)


def _labeling_space(vm: dict) -> dict[str, str]:
    root = vm["root"]
    cal = vm["cal"] or {}
    label = _label_definitions(vm)
    labeling_now = cal.get("current_round") and not (vm["canonical"] or {}).get("hold")
    app = "" if labeling_now else '<div id=label-app aria-live=polite><p class=mut>Loading…</p></div>'
    current = (root / "policy" / "current")
    policy = current.read_text(encoding="utf-8").strip() if current.is_file() else ""
    guideline = root / "policy" / "versions" / policy / "guideline.md" if policy else None
    if guideline and guideline.is_file():
        text = guideline.read_text(encoding="utf-8", errors="replace")[:20000]
        guide = _card(f"Guideline {policy}", f'<div class=guide>{_guideline_html(text)}</div>')
    else:
        guide = _card("Guideline", "<p class=mut>No guideline version is readable yet.</p>")
    return {"definition": label + _discussion_view(vm) + _meaning_gate(vm) + _meaning_history(vm),
            "rounds": app + _rounds_summary(vm) + (_rounds_view(vm) if cal.get("rounds") else ""),
            "guideline": _guideline_versions(vm) + guide}


def _quality_space(vm: dict) -> dict[str, str]:
    root, sealed = vm["root"], vm["sealed"]
    frame = sealed.get("frame") if isinstance(sealed.get("frame"), dict) else {}
    if sealed:
        test = _card("Held-back test items", "".join([
            _row("items", _esc(sealed.get("n_items"))),
            _row("how drawn", _esc(frame.get("rule"))),
            _row("keeper", _esc(sealed.get("custodian"))),
            _row("state", _esc({"reserved-and-unexposed": "kept aside, never shown"}.get(str(sealed.get("status")), sealed.get("status")))),
            _row("locked for scoring", "yes" if (root / "test" / "final" / "lock.json").is_file() else "not yet"),
        ]))
    else:
        test = _later("P0 Contract")
    evaluation = (_card("Evaluation", _row("registry", "present")) if (root / "evaluation" / "registry.yaml").is_file()
                  else _later("P3 Test"))
    audits = sorted((root / "audit").glob("final_*")) if (root / "audit").is_dir() else []
    audit = _card("Audit", _row("audits", _esc(len(audits)))) if audits else _later("P5 Audit")
    return {"test": test, "evaluation": evaluation, "audit": audit,
            "gold": _job_tasks_card(vm, "gold", "External gold")}


def _run_type_skills() -> dict[str, list[str]]:
    """Run Type -> declared Skills from ref-space-mapping.md; these do not prove historical usage."""
    ref = _space_mapping_ref()
    headers, rows = _md_table(ref.read_text(encoding="utf-8"), "Run Type skills") if ref else ([], [])
    col = {h.lower(): i for i, h in enumerate(headers)}
    if "run type" not in col or "declared skills" not in col:
        return {}
    out: dict[str, list[str]] = {}
    for cells in rows:
        if max(col["run type"], col["declared skills"]) >= len(cells):
            continue
        op = cells[col["run type"]].strip().strip("`")
        if op:
            out[op] = re.findall(r"`([^`]+)`", cells[col["declared skills"]])
    return out


def _meaning_history(vm: dict) -> str:
    """Labeling → Definition: every recorded change to the label meanings, newest first."""
    module = _canonical_job_module()
    try:
        revisions = module.meaning_revisions(vm["root"]) if module is not None else []
    except Exception:  # the page must still render
        revisions = []
    g0 = _read_json(vm["root"] / "gates" / "g0" / "receipt.json")
    rows = []
    for rev in reversed(revisions):
        before = rev.get("before") if isinstance(rev.get("before"), dict) else {}
        after = rev.get("after") if isinstance(rev.get("after"), dict) else {}
        changed = [k for k in sorted(set(before) | set(after)) if before.get(k) != after.get(k)]
        rows.append(f'<tr><td class=num>{_esc(rev.get("seq"))}</td><td>{_esc(_when(rev.get("revised_at")))}</td>'
                    f'<td>{_esc(rev.get("human_id"))}</td><td>{_esc(", ".join(changed) or "none")}</td>'
                    f'<td><code>{_esc(rev.get("run") or "")}</code></td></tr>')
    confirmed = (f'<p class=mut>Meanings confirmed (G0) {_esc(_when(g0.get("confirmed_at") or g0.get("created_at")))}'
                 f'{" by " + _esc(g0.get("human_id")) if g0.get("human_id") else ""}.</p>') if g0 else ""
    if not rows:
        return _card("Meaning history", "<p class=mut>No change since the Contract.</p>" + confirmed)
    return _card("Meaning history", '<div class=scroll><table class=steptable><thead><tr><th>#</th><th>When</th>'
                 '<th>By</th><th>Labels changed</th><th>Run</th></tr></thead>'
                 f'<tbody>{"".join(rows)}</tbody></table></div>' + confirmed)


def _round_events(root: Path, round_id: str) -> list[dict]:
    path = root / "rounds" / round_id / "sessions" / "events.jsonl"
    if not path.is_file():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict):
            out.append(event)
    return out


def _rounds_summary(vm: dict) -> str:
    """Labeling → Rounds: all rounds in one table, then how the final labels fall (counts only)."""
    root, cal, config = vm["root"], vm["cal"] or {}, vm["config"] or {}
    rounds = cal.get("rounds") or []
    if not rounds:
        return ""
    values = [str(v) for v in ((config.get("labels") or {}).get("values") or [])]
    table, spread = [], []
    for r in rounds:
        rid = r.get("round_id") or ""
        manifest = _load_mapping(root / "rounds" / rid / "manifest.yaml")
        draw = manifest.get("draw") if isinstance(manifest.get("draw"), dict) else {}
        finals = [e for e in _round_events(root, rid) if e.get("kind") == "final"]
        changed = sum(1 for e in finals if str((e.get("payload") or {}).get("change_type") or "none") != "none")
        state = {"judging": "labeling", "judged": "all labeled"}.get(str(r.get("state")), str(r.get("state") or ""))
        how = " · ".join(x for x in (str(draw.get("method") or ""), f'seed {draw["seed"]}' if draw.get("seed") is not None else "") if x)
        table.append(
            f'<tr><td>{_esc(_round_words(rid))}</td><td>{_esc(state)}</td>'
            f'<td class=num>{_esc(r.get("finals", 0))} of {_esc(r.get("batch_size", 0))}</td>'
            f'<td class=num>{_esc(changed)}</td>'
            f'<td>{_esc(how)}</td>'
            f'<td>{_esc(manifest.get("policy_version") or "")}</td></tr>')
        counts = {v: 0 for v in values}
        for e in finals:
            label = str((e.get("payload") or {}).get("class_label") or "")
            counts[label] = counts.get(label, 0) + 1
        spread.append(f'<tr><td>{_esc(_round_words(rid))}</td>'
                      + "".join(f'<td class=num>{_esc(counts.get(v, 0))}</td>' for v in values)
                      + f'<td class=num>{_esc(len(finals))}</td></tr>')
    head = "".join(f"<th>{_esc(v)}</th>" for v in values)
    return _card("All rounds", (
        '<div class=scroll><table class=steptable><thead><tr><th>Round</th><th>State</th><th>Labeled</th>'
        '<th>Changed after the reveal</th><th>How drawn</th><th>Guideline</th></tr></thead>'
        f'<tbody>{"".join(table)}</tbody></table></div>'
        '<h3 class=sub>How the final labels fall</h3>'
        f'<div class=scroll><table class=steptable><thead><tr><th>Round</th>{head}<th>All</th></tr></thead>'
        f'<tbody>{"".join(spread)}</tbody></table></div>'))


def _guideline_versions(vm: dict) -> str:
    """Labeling → Guideline: every version, which rounds used it, the current one marked."""
    root, cal = vm["root"], vm["cal"] or {}
    base = root / "policy" / "versions"
    if not base.is_dir():
        return ""
    current = _current_policy(root)
    used: dict[str, list[str]] = {}
    for r in cal.get("rounds") or []:
        manifest = _load_mapping(root / "rounds" / str(r.get("round_id")) / "manifest.yaml")
        if manifest.get("policy_version"):
            used.setdefault(str(manifest["policy_version"]), []).append(_round_words(r.get("round_id")))
    rows = []
    for folder in sorted(p for p in base.iterdir() if p.is_dir() and not p.is_symlink()):
        manifest = _load_mapping(folder / "manifest.yaml")
        status = str(manifest.get("status") or "")
        rows.append(f'<tr><td><code>{_esc(folder.name)}</code>{" <b class=ok>current</b>" if folder.name == current else ""}</td>'
                    f'<td>{_esc(status.replace("-", " "))}</td><td>{_esc(manifest.get("parent") or "none")}</td>'
                    f'<td>{_esc(manifest.get("created_by") or "")}</td><td>{_esc(", ".join(used.get(folder.name, [])) or "none")}</td></tr>')
    return _card("Versions", '<div class=scroll><table class=steptable><thead><tr><th>Version</th><th>Status in its manifest</th>'
                 '<th>From</th><th>Made by</th><th>Used by</th></tr></thead>'
                 f'<tbody>{"".join(rows)}</tbody></table></div>')
