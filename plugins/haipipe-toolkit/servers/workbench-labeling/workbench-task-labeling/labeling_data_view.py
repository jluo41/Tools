"""The Data Space: the raw corpus, the items, the preparation steps, and the meaning gate."""
from __future__ import annotations

import importlib.util
import json
import re
from functools import lru_cache
from pathlib import Path

from live.labeling_job import _canonical_job_module, _read_json
from live.labeling_model import (_card, _esc, _g0_repair_request, _g0_retroactive_block, _hold_words,
    _imported_reference_only, _job_tasks_card, _job_where, _meaning_allowed, _meaning_list, _next_step,
    _open_definition_run, _row, _when)
from live.labeling_embedding_view import _embedding_summary, _embedding_view


def _data_space(vm: dict) -> dict[str, str]:
    config, manifest, sealed, imported = vm["config"], vm["manifest"], vm["sealed"], vm["imported"]
    preparation = vm.get("preparation") or {}
    if not (vm["root"] / "config.yaml").is_file():
        if not vm.get("page_ready", True):
            contract = _card("Labeling Contract", "<p>Create this Page's own folder, then "
                             "complete and link Corpus Preparation before Contract.</p>")
        elif preparation.get("linked") and not preparation.get("error"):
            package = (preparation.get("reference") or {}).get("package") or ""
            contract = _card("Labeling Contract", "".join([
                "<p>The Corpus Preparation package is accepted. Create this Page's "
                "Labeling Contract through the Runs panel.</p>",
                _row("accepted package", f"<code>{_esc(package)}</code>"),
            ]))
        else:
            contract = _card("Labeling Contract", "<p>Complete and link Corpus "
                             "Preparation before creating this Page's Contract.</p>")
        return {"preparation": _job_tasks_card(vm, "data", "Job data") + _preparation_view(vm),
                "contract": contract, "embedding": _embedding_view(vm)}
    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    n_items = manifest.get("n_items")
    n_sealed = manifest.get("n_sealed", sealed.get("n_items"))
    n_dev = manifest.get("n_eligible")
    if n_dev is None and isinstance(n_items, int) and isinstance(n_sealed, int):
        n_dev = n_items - n_sealed

    corpus = _card("Data", "".join([
        _row("source", _esc(source.get("name") or (config.get("corpus") or {}).get("source") or "")),
        _row("items", _esc(n_items)),
        _row("to label", _esc(n_dev)),
        _row("held back", _esc(f"{n_sealed} items for the final test; you never see them" if n_sealed is not None else "none")),
        _row("embedding", _embedding_summary(vm.get("embedding"))),
    ]))
    imported_rows = []
    for key, value in imported.items():
        if isinstance(value, dict) and value.get("field") and isinstance(value.get("values"), dict):
            counts = " · ".join(f"{_esc(k)} {_esc(v)}" for k, v in value["values"].items())
            imported_rows.append(_row(str(value["field"]), counts))
    schema = ""
    if imported_rows:
        unit = imported.get("unit") if isinstance(imported.get("unit"), dict) else {}
        schema += _card("Imported labels (other people's labels, not the right answer)", "".join(imported_rows) + (
            f'<p class=mut>Counted per {_esc(unit.get("row") or "source row")}.</p>'))
    reveal = (config.get("reveal") or {}).get("reference_observations") if isinstance(config.get("reveal"), dict) else None
    if isinstance(reveal, dict):
        schema += _card("What you see after you lock an answer", "".join([
            _row("from", _esc(reveal.get("label"))),
            _row("vote counts", ", ".join(f"<code>{_esc(f)}</code>" for f in reveal.get("count_fields") or [])),
            _row("other fields", ", ".join(f"<code>{_esc(f)}</code>" for f in reveal.get("item_fields") or [])),
        ]))
    return {"preparation": _job_tasks_card(vm, "data", "Job data") + _preparation_view(vm),
            "contract": _contract_detail(vm) + corpus + schema, "embedding": _embedding_view(vm)}


@lru_cache(maxsize=16)
def _corpus_shape(items: str, mtime_ns: int, size: int, text_field: str,
                  context_field: str) -> dict:
    """Word counts over the items to label only; held-back text is never read."""
    from statistics import median  # noqa: PLC0415
    text_words, context_words, meta = [], [], {}
    try:
        with open(items, encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(row, dict) or row.get("population_status") != "eligible":
                    continue
                if not meta and isinstance(row.get("source_metadata"), dict):
                    meta = row["source_metadata"]
                text_words.append(len(str(row.get(text_field) or "").split()))
                if context_field:
                    context_words.append(len(str(row.get(context_field) or "").split()))
    except OSError:
        return {}

    def spread(words: list[int]) -> str:
        return f"{median(words):g} words median, {min(words)} to {max(words)}" if words else ""

    return {"n": len(text_words), "text": spread(text_words), "context": spread(context_words),
            "no_context": sum(1 for n in context_words if n == 0), "meta": meta}


def _day_words(value) -> str:
    """'2026-09-16...' -> '16 Sep 2026'."""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(value or ""))
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    return f"{int(m.group(3))} {months[int(m.group(2)) - 1]} {m.group(1)}" if m else str(value or "")


def _bytes_words(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return ""


def _corpus_view_module():
    """Load the subjective-label corpus reader (``corpus_view``)."""
    job_module = _canonical_job_module()
    if job_module is None:
        return None
    candidate = Path(job_module.__file__).with_name("corpus_view.py")
    if not candidate.is_file():
        return None
    spec = importlib.util.spec_from_file_location("haipipe_subjective_label_corpus_view", candidate)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _corpus_source(vm: dict) -> dict:
    config, manifest = vm.get("config") or {}, vm.get("manifest") or {}
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    packaged = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    described = corpus.get("source") if isinstance(corpus.get("source"), dict) else {}
    return {**packaged, **{k: v for k, v in described.items() if v}}


def _code_popup(vm: dict) -> str:
    """The script that made the items, read-only in a pop-out: `corpus.source.code` names it,
    relative to the SPACE root (the nearest folder above the job holding env.sh)."""
    rel = str(_corpus_source(vm).get("code") or "").strip()
    if not rel or rel.startswith("/") or ".." in Path(rel).parts or Path(rel).suffix not in {".py", ".yaml", ".sh", ".md"}:
        return ""
    space = next((p for p in Path(vm["root"]).parents if (p / "env.sh").is_file()), None)
    path = space / rel if space else None
    if path is None or not path.is_file():
        return f' <span class=mut>· code: <code>{_esc(rel)}</code> (not found on this host)</span>'
    try:
        text = path.read_text(encoding="utf-8")[:200_000]
    except OSError:
        return ""
    return (f' <button type=button class="pill tog" data-code-open>View code</button>'
            f'<dialog class=codepop data-code-dialog><header><code>{_esc(rel)}</code>'
            f'<button type=button class="pill tog" data-code-close>Close</button></header>'
            f'<pre><code>{_esc(text)}</code></pre></dialog>')


def _data_card(vm: dict) -> str:
    """What data this job labels, said first: the dataset, what it is, one item, its size,
    any ground truth kept apart, and the Run that made it. A missing fact says what to add."""
    config, manifest = vm.get("config") or {}, vm.get("manifest") or {}
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    source = _corpus_source(vm)
    name = _esc(source.get("name") or "")
    if name and source.get("uri"):
        name = f'<a href="{_esc(source["uri"])}" target=_blank rel=noopener>{name}</a>'
    name = " · ".join(x for x in (name, _esc(source.get("version") or ""), _esc(source.get("license") or "")) if x)
    population = manifest.get("population")
    pop = population if isinstance(population, dict) else {}
    unit = (corpus.get("population") or pop.get("definition")
            or (population if isinstance(population, str) else ""))
    n_dev = manifest.get("n_eligible", manifest.get("n_items"))
    if not isinstance(n_dev, int):   # the package does not say: count the items file
        items = vm["root"] / (manifest.get("items_file") or "corpus/items.jsonl")
        try:
            stat = items.stat()
            n_dev = _corpus_shape(str(items), stat.st_mtime_ns, stat.st_size,
                                  manifest.get("text_field") or corpus.get("text_field") or "text",
                                  manifest.get("context_field") or corpus.get("context_field") or "").get("n")
        except OSError:
            n_dev = None
    n_sealed = manifest.get("n_sealed", (vm.get("sealed") or {}).get("n_items"))
    size = " · ".join(x for x in (
        f"{n_dev:,} to label" if isinstance(n_dev, int) else "",
        f"{n_sealed:,} held back for the test, never shown" if isinstance(n_sealed, int) and n_sealed else "") if x)
    missing = lambda key, what: (f'<span class=warn>not described yet</span> <span class=mut>· add '
                                 f'<code>corpus.source.{key}</code> ({what})</span>')
    rows = [
        _row("dataset", name or missing("name", "its name, link and license")),
        _row("what it is", _esc(source.get("description") or "") or missing("description", "one sentence: whose text, how much, from where")),
        _row("one item", _esc(unit)) if unit else "",
        _row("size", _esc(size)) if size else "",
        _row("ground truth", _esc(source.get("ground_truth"))
             + ' <span class=mut>· kept apart, never shown while you label</span>') if source.get("ground_truth") else "",
        _row("made by", _esc(source.get("made_by")) + _code_popup(vm)) if source.get("made_by") else "",
        _row("stored at", f'<code>{_esc(source.get("store"))}</code>') if source.get("store") else "",
    ]
    return _card("The data", "".join(rows))


def _raw_corpus_card(vm: dict) -> str:
    """The raw source as a folder, and which raw column became which item field; no row values."""
    config, manifest = vm.get("config") or {}, vm.get("manifest") or {}
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
    if not source and isinstance(corpus.get("source"), dict):
        source = corpus["source"]
    name = _esc(source.get("name") or "")
    if name and source.get("uri"):
        name = f'<a href="{_esc(source["uri"])}" target=_blank rel=noopener>{name}</a>'
    if name and source.get("license"):
        name += f' · {_esc(source["license"])}'
    module = _corpus_view_module()
    try:
        raw = module.raw_source(vm["root"]) if module else {}
    except (OSError, ValueError) as error:
        return _card("Raw corpus", _row("source", name) + f'<p class=warn>{_esc(error)}</p>')
    if not raw:
        return ""   # no raw-folder record: "The data" above already names the dataset
    folder = _row("folder", f'<code>{_esc(raw["folder"])}/</code>'
                  + ("" if raw["found"] else ' <span class=warn>not found on this machine</span>'))
    file_rows = []
    for f in raw["files"]:
        n_rows = f"{f['rows']:,}" if "rows" in f else ""
        file_rows.append(
            f'<tr><td><code>{_esc(f["path"])}</code></td><td class=num>{_esc(_bytes_words(f["bytes"]))}</td>'
            f'<td class=num>{_esc(n_rows)}</td><td class=num>{_esc(len(f.get("columns") or []) or "")}</td>'
            f'<td class=num>{_esc(f.get("keys") or "")}</td></tr>')
    files = "".join(file_rows)
    files_table = ('<div class=scroll><table class=items><thead><tr><th>File</th><th>Size</th><th>Rows</th>'
                   f'<th>Columns</th><th>Items</th></tr></thead><tbody>{files}</tbody></table></div>'
                   if files else "")
    main = next((f for f in raw["files"] if f["path"] == raw["file"]), {})
    used = raw["fields"]
    mapping = "".join(
        f'<tr><td><code>{_esc(col)}</code></td><td>→</td><td><code>{_esc(field)}</code></td></tr>'
        for col, field in used.items())
    others = [c for c in main.get("columns") or [] if c not in used]
    rows = [
        folder,
        files_table,
        _row("one row is", _esc(raw["one_row_is"])) if raw["one_row_is"] else "",
        _row("one item is", f'all rows with the same <code>{_esc(raw["item_key"])}</code>'
             + (f' ({_esc(main["keys"])} items)' if main.get("keys") else "")) if raw["item_key"] else "",
        _row("raw column → item field", f'<table class=map><tbody>{mapping}</tbody></table>') if mapping else "",
        (f'<details class=ctx><summary>other columns ({len(others)}), never shown before you label</summary>'
         f'<p class=mut>{", ".join(f"<code>{_esc(c)}</code>" for c in others)}</p></details>') if others else "",
        _row("built", _esc(" · ".join(x for x in (_day_words(raw["built_on"]), raw["built_by"]) if x)))
        if raw["built_on"] or raw["built_by"] else "",
    ]
    return _card("Raw corpus", "".join(rows))


def _items_card(vm: dict) -> str:
    """The items to label: what one item is, the counts, and a table you can page through."""
    config, manifest = vm.get("config") or {}, vm.get("manifest") or {}
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    population = manifest.get("population")
    pop = population if isinstance(population, dict) else {}
    text_field = manifest.get("text_field") or corpus.get("text_field") or "text"
    context_field = manifest.get("context_field") or corpus.get("context_field") or ""
    items = vm["root"] / (manifest.get("items_file") or "corpus/items.jsonl")
    try:
        stat = items.stat()
        shape = _corpus_shape(str(items), stat.st_mtime_ns, stat.st_size, text_field, context_field)
    except OSError:
        shape = {}
    context = ""
    if context_field and shape.get("context"):
        context = f'<code>{_esc(context_field)}</code> · {_esc(shape["context"])}'
        if shape.get("no_context"):
            n = shape["no_context"]
            context += f' · {_esc(n)} {"item has" if n == 1 else "items have"} none'
    table = ""
    if shape.get("n") and not (vm.get("state") or {}).get("authority_hold"):
        table = ('<div class=actions><button type=button class=primary data-items-show>Show items</button></div>'
                 '<div data-items-box hidden><div class=itemfilter data-items-filter></div><div data-items-note></div>'
                 '<div class=scroll><table class="items itemgrid"><thead><tr><th>Item id</th><th>Item text</th>'
                 '<th>State</th></tr></thead>'
                 '<tbody data-items-rows></tbody></table></div></div><div data-items-more></div>')
    return _card("Items to label", "".join([
        _row("text", f'<code>{_esc(text_field)}</code> · {_esc(shape["text"])}') if shape.get("text") else "",
        _row("context", context) if context else "",
        _row("kept together", "no encounter is split across the held-back test")
        if pop.get("encounter_straddle_across_seal") == [] else "",
        table,
    ]))


_PREP_STEPS = (
    ("source-normalize", "Read the transcripts", "accept each conversation, set malformed ones aside"),
    ("unit-recipe", "Choose what one item is", "which reply is labeled, and how much conversation comes with it"),
    ("unit-materialize", "Make the items", "one item per chosen reply"),
    ("unit-check", "Check the items", "unique ids, context cut before the reply, nothing missing"),
    ("initial-group-reserve", "Hold back a test set", "whole conversations set aside, never shown while labeling"),
)


def _items_flow_card(vm: dict) -> str:
    """For a job made from ready items: corpus → items_transform → items → held back → this job."""
    manifest = vm.get("manifest") or {}
    source = _corpus_source(vm)
    n_dev = manifest.get("n_eligible", manifest.get("n_items"))
    n_sealed = manifest.get("n_sealed", (vm.get("sealed") or {}).get("n_items"))
    total = n_dev + n_sealed if isinstance(n_dev, int) and isinstance(n_sealed, int) else None
    steps = [
        ("Corpus", source.get("name") or "the dataset"),
        ("items_transform", source.get("made_by") or "the script that decides what one item is"),
        ("Items", f"{total:,} items" if total else "one item per unit to label"),
        ("Hold back a test set", f"{n_sealed:,} items, never shown while you label" if isinstance(n_sealed, int) else ""),
        ("This job", f"{n_dev:,} items to label" if isinstance(n_dev, int) else ""),
    ]
    rows = "".join(f'<li class=done><span class=mark>{"↓" if i else "●"}</span><b>{_esc(a)}</b>'
                   f'<span class=mut>{_esc(b)}</span></li>' for i, (a, b) in enumerate(steps))
    return _card("From corpus to items", f'<ol class=prepsteps>{rows}</ol>')


def _prep_steps(prep: dict) -> str:
    """The five Preparation steps and the link, in order: done, next, or not yet."""
    done = {run.get("operation") for run in prep.get("runs") or [] if run.get("status") == "complete"}
    linked, rows, next_set = bool(prep.get("linked")), [], False
    for op, words, what in _PREP_STEPS + (("link", "Link to this job", "the accepted items become this job's corpus"),):
        ok = linked or op in done
        cls = "done" if ok else ("next" if not next_set else "todo")
        next_set = next_set or not ok
        mark = {"done": "✓", "next": "→", "todo": "·"}[cls]
        rows.append(f'<li class={cls}><span class=mark>{mark}</span><b>{_esc(words)}</b>'
                    f'<span class=mut>{_esc(what)}</span></li>')
    return f'<ol class=prepsteps>{"".join(rows)}</ol>'


def _preparation_view(vm: dict) -> str:
    prep = vm.get("preparation") or {}
    has_job = (vm["root"] / "config.yaml").is_file()
    if not vm.get("page_ready", True) and not has_job:
        source = vm["page_src"]
        target = vm["page_candidate"]
        prompt = (f"Use /hai-draft to create the canonical Page folder for {source}. "
                  f"The Page file should be {target}. Preserve the Board source and its "
                  "existing content. Return to Data → Preparation after the Page folder exists.")
        return _card("Page folder needed", "".join([
            "<p>Corpus Preparation needs this Page's own folder. The current Board source "
            "is flat, so it cannot own an isolated <code>labeling/</code> lane yet.</p>",
            _row("Page file to create", f"<code>{_esc(target)}</code>"),
            f'<div class=actions><button type=button class=primary data-copy="{_esc(prompt)}">'
            "Copy Page-folder request</button></div>",
        ]))
    data = _data_card(vm) if has_job else ""
    rest = _raw_corpus_card(vm) + _items_card(vm) if has_job else ""
    corpus = data + rest
    if prep.get("error"):
        return data + _card("Corpus Preparation", f'<p class=warn>{_esc(prep["error"])}</p>') + rest
    if not prep.get("linked"):
        if not prep.get("attached"):
            if corpus:
                return data + _items_flow_card(vm) + rest
            prompt = ("Use /hai-labeling-preparation for the Page whose labeling folder is at "
                      f"{_job_where(vm)}. Identify the transcript JSONL and source owner, attach "
                      "that owner to this Page, then work through the five Corpus Preparation "
                      "Run Types in order. Link the accepted package before creating a Labeling Contract.")
            return _card("Corpus Preparation", "<p>Attach a source preparation owner to this Page, "
                         "then use the Run Types on the right in order.</p>"
                         f'<div class=actions><button type=button class=primary data-copy="{_esc(prompt)}">'
                         "Copy setup request</button></div>")
        owner_ref = prep["owner_reference"]
        return data + _card("Corpus Preparation", "".join([
            _prep_steps(prep),
            _row("next", _esc(_next_step(vm)[0])),
            '<details class=ctx><summary>ids</summary>'
            + _row("source", f'<code>{_esc(owner_ref["source_id"])}</code>')
            + _row("owner", f'<code>{_esc(owner_ref["owner"])}</code>') + '</details>',
        ])) + rest
    receipt = prep["receipt"]
    ref = prep["reference"]
    rows = [
        _prep_steps(prep),
        _row("result", f'<span class=ok>accepted</span> · {_esc(receipt["n_eligible"])} items to label · '
             f'{_esc(receipt["n_sealed"])} held back · whole conversations kept together'),
        '<details class=ctx><summary>ids</summary>'
        + _row("source", f'<code>{_esc(receipt["snapshot_id"])}</code>')
        + _row("recipe", f'<code>{_esc(receipt["recipe_id"])}</code>')
        + _row("item set", f'<code>{_esc(receipt["item_set_id"])}</code>')
        + _row("partition", f'<code>{_esc(receipt["partition_id"])}</code>')
        + _row("owner", f'<code>{_esc(ref["owner"])}</code>') + '</details>',
    ]
    return data + _card("Corpus Preparation", "".join(rows)) + rest


def _meaning_gate(vm: dict) -> str:
    """Confirm meaning (G0): the gate on the label meanings, so it sits in Labeling › Definition."""
    config, state, canonical = vm.get("config") or {}, vm.get("state"), vm.get("canonical") or {}
    if not state:
        return ""
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    if _imported_reference_only(vm):
        # The header carries the single source-only status. This job has no
        # local meaning gate to confirm, so don't repeat it as an alarm card.
        gate = ""
    elif state["authority_hold"]:
        gate = _card("Meaning", f'<p class=warn>Read-only: {_esc(_hold_words(canonical.get("hold_reason") or state["authority_reason"]))}.</p>'
                     '<p class=mut>Method state: <code>HOLD</code>.</p>'
                     '<p class=mut>No one can confirm a meaning or label on this job.</p>')
    elif canonical and canonical.get("meaning_receipt_valid") and canonical.get("g0_receipt_valid"):
        receipt = authority.get("meaning_receipt") if isinstance(authority.get("meaning_receipt"), dict) else {}
        gate = _card("Meaning confirmed ✓", f'<p class=ok>Caller attested as {_esc(receipt.get("human_id"))}, {_esc(_when(receipt.get("confirmed_at")))}.</p>')
    elif _g0_retroactive_block(vm):
        gate = _card("Meaning confirmation unavailable", '<p class=warn>A round was released '
                     'without a valid earlier meaning confirmation. G0 cannot be confirmed '
                     'retroactively for that round. Keep this job as history and start a new '
                     'job for new labels.</p>')
    elif _open_definition_run(vm) and _meaning_allowed(vm):
        gate = _card("Meaning discussion open", '<p>Finish the open discussion in the Runs '
                     'panel before confirming the meanings.</p>')
    elif canonical.get("meaning_definitions_missing") and not canonical.get("g0_retroactive_block"):
        names = ", ".join(str(value) for value in canonical["meaning_definitions_missing"])
        gate = _card("Define label meanings first", f'<p>These labels still need meanings: {_esc(names)}. '
                     'Use the Definition discussion Run to decide their wording before confirming G0.</p>')
    elif _g0_repair_request(vm) or (canonical and canonical.get("first_blocked_frontier") == "G0 · human meaning confirmation"):
        repair = _g0_repair_request(vm)
        region_meanings = regions.get("meanings") if isinstance(regions.get("meanings"), dict) else {}
        gate = _card("Restore G0 receipt" if repair else "Confirm the meaning", (
            ("<p>An intact earlier human confirmation already records these meanings. "
             "Restore its missing G0 receipt; this does not create a new semantic decision.</p>"
             if repair else
             "<p>Confirming records your attestation that these classes, boundary regions, "
             "and unsure levels match your intended meaning. The Workbench does not authenticate identity.</p>") +
            '<details><summary>boundary regions</summary>'
            f'{_meaning_list([str(v) for v in regions.get("values") or []], region_meanings)}</details>'
            '<label class=attest><input type=checkbox data-confirm-attest> '
            'These meanings are what I mean.</label>'
            f'<div class=actions><button class=primary type=button data-confirm-meaning disabled>{"Restore G0 receipt" if repair else "Confirm meaning"}</button>'
            '<span class=msg role=status data-confirm-msg></span></div>'
        ), "focus")
    else:
        gate = _card("Meaning", f'<p class=mut>{_esc(state["first_failed"])}</p>')

    return gate


def _code_spans(text: str) -> str:
    """`a` · `b` from the map, as code, everything else escaped."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", _esc(text))


def _contract_detail(vm: dict) -> str:
    """Data → Contract: the job itself and its labels, from config.yaml and the P0 receipt."""
    root, config, canonical = vm["root"], vm["config"] or {}, vm["canonical"] or {}
    if not (root / "config.yaml").is_file():
        return ""
    construct = config.get("construct") if isinstance(config.get("construct"), dict) else {}
    authority = config.get("authority") if isinstance(config.get("authority"), dict) else {}
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    regions = config.get("regions") if isinstance(config.get("regions"), dict) else {}
    uncertainty = config.get("uncertainty") if isinstance(config.get("uncertainty"), dict) else {}
    receipt = _read_json(root / "gates" / "p0-contract" / "receipt.json")
    contract_runs = [r for r in vm["runs"] if r["operation"] == "corpus-contract"]
    mode = {"single_human_semantic_authority": "one person decides every label",
            "external_annotation_import": "imported labels, for reference only"}.get(
        str(authority.get("mode") or ""), str(authority.get("mode") or ""))
    job = _card("The job", "".join([
        _row("job", f'<code>{_esc(receipt.get("job_id") or "")}</code>') if receipt.get("job_id") else "",
        _row("target", f'<code>{_esc(construct.get("name") or "")}</code>'),
        _row("question", _esc(construct.get("question") or "")),
        _row("labels decided by", _esc(" · ".join(x for x in (authority.get("human_id"), mode) if x))),
        _row("test kept by", _esc(canonical.get("sealed_custodian") or (vm["sealed"] or {}).get("custodian") or "")),
        _row("created", _esc(_when(receipt.get("created_at")))) if receipt.get("created_at") else "",
        _row("by Run", f'<code>{_esc(contract_runs[-1]["name"])}</code>') if contract_runs else "",
        _row("contract check", '<span class=ok>valid</span>' if canonical.get("p0_contract_integrity_valid")
             else '<span class=warn>' + _esc("; ".join(canonical.get("p0_integrity_errors") or ["not valid"])) + '</span>'),
    ]))
    values = [str(v) for v in labels.get("values") or []]
    scheme = _card("Labels", "".join([
        _row("labels", _esc(" · ".join(values))) if values else "",
        _row("kind", _esc(" · ".join(x for x in (labels.get("type"), f'none = {labels["none_value"]}'
                                                  if labels.get("none_value") else "") if x))),
        _row("regions", _esc(" · ".join(str(r) for r in regions.get("values") or []))) if regions.get("values") else "",
        _row("how sure", _esc(" · ".join(str(u) for u in uncertainty.get("levels") or []))) if uncertainty.get("levels") else "",
        _row("meanings", "in Labeling → Definition"),
    ])) if values else ""
    return job + scheme
