"""The Embedding view: the map of the items, its build settings, and the command that builds it."""
from __future__ import annotations

import shlex
import sys
from pathlib import Path

from live.labeling_hold import _calibration_module, _embedding_module
from live.labeling_model import _card, _clean_keywords, _esc, _md_inline, _row, _script_json, _when


_GROUP_COLORS = ("#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948",
                 "#b07aa1", "#ff9da7", "#9c755f", "#a0cbe8", "#d37295", "#bab0ac")
_LABEL_COLORS = ("var(--warn)", "var(--acc)", "var(--ok)", "#b07aa1", "#9c755f")


def _group_color(group) -> str:
    try:
        return _GROUP_COLORS[int(group) % len(_GROUP_COLORS)]
    except (TypeError, ValueError):
        return "var(--mut)"


def _model_name(model_id) -> str:
    return str(model_id or "").rsplit("/", 1)[-1]


def _thousands(value) -> str:
    return f"{value:,}" if isinstance(value, int) else str(value)


def _embedding_summary(emb: dict | None) -> str:
    builds = (emb or {}).get("builds") or []
    if not builds:
        return '<span class=mut>not built</span>'
    labels = _unique_labels([(b["manifest"]["version"], b["manifest"]["model"]["id"], b["manifest"].get("settings"))
                             for b in builds])
    names = "<br>".join(_esc(labels[b["manifest"]["version"]]) for b in builds)
    return f'{names}<br><span class=mut>{len(builds)} built</span>'


def _item_marks(root: Path) -> dict[str, dict]:
    """Which round drew each item, and its final label once the human gave one."""
    module = _calibration_module()
    marks: dict[str, dict] = {}
    if module is None:
        return marks
    try:
        for round_path in module._round_dirs(root):
            states = module._item_states(round_path)
            for row in module._read_jsonl(round_path / "human_batch.jsonl"):
                item_id = str(row.get("item_id"))
                final = (states.get(item_id) or {}).get("final")
                label = None
                if final:
                    label = (final.get("payload") or {}).get("class_label") or "unresolved"
                marks[item_id] = {"round": round_path.name, "final": label}
    except Exception:  # marks are decoration; the map renders without them
        return {}
    return marks


def _repo_relative(path: Path) -> str:
    for parent in path.resolve().parents:
        if (parent / "pyproject.toml").is_file() and (parent / "code").is_dir():
            return str(path.resolve().relative_to(parent))
    return str(path)


_SHORT_MODELS = {
    "all-MiniLM-L6-v2": "MiniLM", "all-mpnet-base-v2": "mpnet", "bge-m3": "bge-m3",
    "multilingual-e5-large-instruct": "e5-large", "Qwen3-Embedding-0.6B": "Qwen3 0.6B",
    "Qwen3-Embedding-4B": "Qwen3 4B", "Qwen3-Embedding-8B": "Qwen3 8B",
}
_TEXT_WORDS = {"reply_context": "reply + context", "reply": "reply only", "context": "context only"}


def _build_label(model_id, settings: dict | None, full: bool = True) -> str:
    """A build's name: model, which text, instruction; `full` adds groups, map, and seed when not default."""
    settings = settings or {}
    name = _model_name(model_id)
    tags = [_SHORT_MODELS.get(name, name), _TEXT_WORDS.get(settings.get("input") or "reply_context", "reply + context")]
    if settings.get("instruction"):
        tags.append("instruction")
    if not full:
        return " · ".join(tags)
    if settings.get("groups"):
        tags.append(f'{settings["groups"]} groups')
    if settings.get("map") == "pca":
        tags.append("PCA")
    if int(settings.get("seed") or 0):
        tags.append(f'seed {settings["seed"]}')
    return " · ".join(tags)


_STATE_PILL = {"built": ("ok", "built"), "building": ("acc", "building…"),
               "failed": ("warn", "failed"), "stopped": ("warn", "stopped")}


def _embedding_view(vm: dict) -> str:
    emb = vm.get("embedding")
    if emb is None:
        return _card("Embedding", "<p class=mut>The subjective-label embedding engine is not available here.</p>")
    if emb.get("error"):
        return _card("Embedding", f'<p class=warn>Could not read the embeddings: {_esc(emb["error"])}</p>')
    builds, status = emb["builds"], emb["status"]

    names = _unique_labels([(b["manifest"]["version"], b["manifest"]["model"]["id"], b["manifest"].get("settings"))
                            for b in builds])
    chips = "".join(
        f'<button class="pill tog" type=button data-emb-show="{_esc(b["manifest"]["version"])}" '
        f'title="{_esc(b["manifest"]["model"]["id"])}: {_esc(_settings_text(b["manifest"].get("settings")))}">'
        f'{_esc(names[b["manifest"]["version"]])}</button>' for b in builds
    )
    catalog = [r for r in status if not r.get("variant") and r.get("params")]
    options = "".join(
        f'<option value="{_esc(r["id"])}" data-instruct="{"1" if r.get("instruct") else ""}"'
        f'{" selected" if r.get("recommended") else ""}>{_esc(_SHORT_MODELS.get(_model_name(r["id"]), _model_name(r["id"])))} · {_esc(r.get("download"))}'
        f'{" · recommended" if r.get("recommended") else ""}</option>'
        for r in catalog
    )
    model_info = {r["id"]: f'{r["id"]} · {r.get("note") or ""}' for r in catalog}
    form = (
        '<div class=embform data-emb-form>'
        '<div class=line><span class=lbl>Model</span><select data-emb-field=model>' + options + '</select>'
        '<button class=primary type=button data-emb-run>Run embedding</button></div>'
        '<p class="mut modelinfo" data-emb-modelinfo></p>'
        '<details class=embmore><summary>More settings</summary>'
        '<div class=line title="Which part of each item the model reads"><span class=lbl>Text</span>'
        '<button class="pill tog on" type=button data-emb-input=reply_context>Reply + context</button>'
        '<button class="pill tog" type=button data-emb-input=reply>Reply only</button>'
        '<button class="pill tog" type=button data-emb-input=context>Context only</button></div>'
        '<div class=line title="Qwen3 and e5-instruct only: tells the model what similar should mean">'
        '<span class=lbl>Instruction</span>'
        '<input class=reason data-emb-field=instruction maxlength=300 placeholder="optional"></div>'
        '<div class=line title="Leave empty and the engine picks the count"><span class=lbl>Number of groups</span>'
        '<input class="reason num" type=number min=2 max=20 data-emb-field=groups placeholder="auto"></div>'
        '<div class=line title="How the numbers are drawn flat"><span class=lbl>Map style</span>'
        '<button class="pill tog on" type=button data-emb-map=tsne>t-SNE</button>'
        '<button class="pill tog" type=button data-emb-map=pca>PCA</button></div>'
        '<div class=line title="Change it to get a different layout of the same items"><span class=lbl>Layout seed</span>'
        '<input class="reason num" type=number min=0 max=99999 value=0 data-emb-field=seed></div>'
        '</details>'
        '<p class=msg role=status data-emb-msg></p>'
        f'<script type=application/json class=embcatalog>{_script_json(model_info)}</script>'
        '</div>'
    )
    tried = []
    order = {b["manifest"]["version"]: i for i, b in enumerate(builds)}
    row_names = _unique_labels([(r["version"], r["id"], r.get("settings")) for r in status if (r.get("state") or "none") != "none"])
    for r in sorted(status, key=lambda r: order.get(r["version"], len(order))):
        state = r.get("state") or "none"
        if state in {"none", "built"}:  # a finished build is listed in the Runs panel; only builds that need you stay here
            continue
        cls, text = _STATE_PILL.get(state, ("mut", state))
        button = (f'<button class=ghost type=button data-emb-show="{_esc(r["version"])}">Show</button>'
                  if state == "built" else "")
        started, started_cls = _started_text(r.get("started")) if r.get("started") else ("", "")
        problem = ""
        if state in {"failed", "stopped"}:
            detail = " · ".join([str(r.get("failure") or "the build process ended early"), *(r.get("log_tail") or [])])
            problem = f'<div class=warn>{_esc(detail)}</div>'
        state_cell = ("" if state == "built" else
                      f'<span class="pill {cls} state">{_esc(text)}</span>')
        tried.append(
            f'<tr data-emb-row="{_esc(r["version"])}" data-state="{_esc(state)}">'
            f'<td title="{_esc(r.get("settings_summary") or "")}"><b>{_esc(row_names.get(r["version"]) or "")}</b>'
            f'{problem}<div class=mut><code>{_esc(r.get("run") or "")}</code></div></td>'
            f'<td class="{started_cls}">{_esc(started)}</td>'
            f'<td>{state_cell}</td><td>{button}</td></tr>'
        )
    runs_table = ('<div class=scroll><table class=runtable><thead><tr><th>Build</th><th>Started</th><th></th>'
                  '<th></th></tr></thead><tbody>' + "".join(tried) + '</tbody></table></div>') if tried else ""
    picker = (
        f'<div class="card{"" if builds else " focus"}"><h2>Embedding model<span class=tally>{len(builds)} built</span></h2>'
        + (f'<div class=line><span class=lbl>Showing</span>{chips}</div>' if builds else
           '<p>No embedding yet.</p>')
        + f'<div class=runbox data-emb-formbox><h3>Run a new embedding</h3>{form}</div>'
        + runs_table
        + '</div>'
    )
    started = {r["version"]: r.get("started") for r in status}
    panes = "".join(
        f'<div class=embpane data-emb="{_esc(b["manifest"]["version"])}"{"" if i == len(builds) - 1 else " hidden"}>'
        f'{_embedding_build_view(vm, {**b, "started": started.get(b["manifest"]["version"])})}</div>'
        for i, b in enumerate(builds)
    )
    return picker + panes


def _unique_labels(entries: list[tuple[str, str, dict | None]]) -> dict[str, str]:
    """key -> short build name; two builds that would read the same get their full names."""
    short = {key: _build_label(model, settings, full=False) for key, model, settings in entries}
    counts: dict[str, int] = {}
    for label in short.values():
        counts[label] = counts.get(label, 0) + 1
    return {key: (label if counts[label] == 1 else _build_label(model, settings))
            for (key, model, settings), label in zip(entries, short.values())}


def _settings_text(settings: dict | None) -> str:
    """The engine's plain sentence for a build's settings; older builds had the defaults."""
    module = _embedding_module()
    if module is None:
        return ""
    return module.settings_summary(settings or dict(module.DEFAULT_SETTINGS))


def _started_text(started: dict | None) -> tuple[str, str]:
    """Who asked for a build, in words, and the row class: a build nobody asked for is flagged."""
    started = started or {}
    person, note = started.get("person"), started.get("note")
    if started.get("via") == "run button":
        return (f"{person}, with the Run embedding button" if person
                else "with the Run embedding button (who pressed it was not recorded yet)"), ""
    if person:
        return f"from the terminal, for {person}" + (f" ({note})" if note else ""), ""
    return "from the terminal; no person's request is recorded", "warn"


_POOLING_WORDS = {
    "mean": "Average all word-piece vectors into one vector of {dim} numbers for the whole item.",
    "cls": "Keep the vector of the first word piece, where the model was trained to put a summary "
           "of the whole input: one vector of {dim} numbers.",
    "lasttoken": "Keep the vector of the last word piece, which has read the whole input: "
                 "one vector of {dim} numbers.",
}




def _piece(text) -> str:
    """A word piece as shown: a newline becomes ↵ and a bare space ␣, so no chip looks empty."""
    text = str(text).replace("\n", "↵")
    return text if text.strip() else "␣"


def _settings_flags(settings: dict) -> str:
    """The CLI flags that rebuild exactly these settings; defaults are left out."""
    flags = []
    if settings.get("input") and settings["input"] != "reply_context":
        flags.append(f'--input {shlex.quote(str(settings["input"]))}')
    if settings.get("instruction"):
        flags.append(f'--instruction {shlex.quote(str(settings["instruction"]))}')
    if settings.get("groups"):
        flags.append(f'--groups {int(settings["groups"])}')
    if settings.get("map") and settings["map"] != "tsne":
        flags.append(f'--map {shlex.quote(str(settings["map"]))}')
    if int(settings.get("seed") or 0):
        flags.append(f'--seed {int(settings["seed"])}')
    return "".join(" " + f for f in flags)


def _engine_command(script: str, *args: str) -> str:
    """Build a replay command from this installed package and host Python."""
    from host_paths import skill_dir
    path = skill_dir("labeling") / "engine" / script
    return " ".join(shlex.quote(part) for part in (sys.executable, str(path), *map(str, args)))


def _embedding_build_view(vm: dict, emb: dict) -> str:
    root, config = vm["root"], vm["config"]
    m = emb["manifest"]
    model_id = str(m["model"]["id"])
    model_name = model_id.rsplit("/", 1)[-1]
    settings = m.get("settings") or {}
    command = (_engine_command("embedding_build.py", "build", "--job-root", _repo_relative(root),
                               "--started-by", "<your name>", "--model", model_id)
               + _settings_flags(settings))
    dim = m["model"]["dim"]
    pre = m.get("preprocessing") or {}
    enc = m.get("encoder") or {}
    pop = m.get("population") or {}
    corpus = config.get("corpus") if isinstance(config.get("corpus"), dict) else {}
    text_field = pre.get("text_field") or "text"
    context_field = pre.get("context_field") or "context"
    n = pop.get("eligible_embedded")

    steps = [
        ("Item", f'<code>{_esc(text_field)}</code> is the response to judge; '
                 f'<code>{_esc(context_field)}</code> is the conversation before it.'
                 + (f' <span class=mut>One item is {_esc(corpus.get("population"))}.</span>'
                    if corpus.get("population") else "")),
        ("Input", {"reply": "Use the reply only; the context is left out.",
                   "context": "Use the context only; the reply is left out."}.get(
                       pre.get("input"), "Join them: the response, a blank line, then the context. "
                                         "The response goes first, so a cut can never remove it.")),
    ]
    if pre.get("prompt"):
        steps.append(("Instruction", f'Put <code>{_esc(pre["prompt"])}</code> in front of every input, '
                                     'so the model reads each item with that task in mind.'))
    modules = {step.get("module"): step for step in enc.get("steps") or []}
    if enc.get("max_tokens"):
        cut = enc.get("items_cut") or 0
        steps.append(("Word pieces", (
            f'The tokenizer splits the input into word pieces. The model reads at most '
            f'{_esc(_thousands(enc["max_tokens"]))}. ' + (
                f'{_esc(cut)} of {_esc(n)} items are longer (longest {_esc(_thousands(enc.get("longest_tokens")))}), '
                'so the end of their context is cut.' if cut else 'No item is longer than that.'))))
    params = m["model"].get("params")
    steps.append(("Model", f'<code>{_esc(model_name)}</code>' + (f' ({_esc(params)} parameters)' if params else "")
                           + f' reads all word pieces together and gives each one {_esc(_thousands(dim))} numbers.'))
    if "Pooling" in modules:
        mode = str(modules["Pooling"].get("mode") or "mean")
        words = _POOLING_WORDS.get(mode, "Combine the word-piece vectors (" + mode + ") into one vector of {dim} numbers.")
        steps.append(("Pooling", _esc(words.format(dim=_thousands(dim)))))
    if "Normalize" in modules or pre.get("normalize") == "l2":
        steps.append(("Length 1", "Scale the vector to length 1, so the similarity of two items "
                                  "(0 unrelated, 1 the same) is a plain dot product."))
    steps.append(("Saved", f'Row r of <code>vectors.npy</code> ({_esc(n)} × {_esc(_thousands(dim))}) is row r of '
                           '<code>rows.jsonl</code> (item id, text hash, word-piece count).'))
    recipe_rows = "".join(_row(f"{i} · {name}", body) for i, (name, body) in enumerate(steps, start=1))
    recipe = (
        f'<div class="card"><h2>From item to vector<span class=tally>{_esc(model_name)} · {_esc(_thousands(dim))} numbers</span></h2>'
        f'{recipe_rows}'
        f'<p class=mut>held back, not embedded: {_esc(pop.get("sealed_excluded", 0))}</p></div>'
    )

    ex = m.get("example") or {}
    example = ""
    if ex.get("input"):
        pieces = ex.get("word_pieces") or []
        numbers = ", ".join(f"{v:.4f}" for v in ex.get("vector_first") or [])
        example = (
            f'<div class="card"><h2>Worked example<span class=tally>made up, not a corpus item</span></h2>'
            + _row("1 · input", f'<code>{_esc(ex["input"])}</code>')
            + (_row(f"2 · {len(pieces)} word pieces",
                    '<span class=pieces>' + "".join(f'<code class=wp>{_esc(_piece(t))}</code>' for t in pieces) + '</span>')
               if pieces else "")
            + _row("3 · vector", f'<code>[{_esc(numbers)}, …]</code> '
                                 f'<span class=mut>first 8 of {_esc(_thousands(ex.get("dim")))} numbers</span>')
            + _row("4 · length", f'<code>{_esc(ex.get("length"))}</code>')
            + '</div>'
        )

    groups = emb.get("groups") or {}
    group_rows = groups.get("groups") or []
    points = emb.get("map") or []
    marks = _item_marks(root)
    schema_labels = [str(v) for v in ((config.get("labels") or {}).get("values") or [])] \
        if isinstance(config.get("labels"), dict) else []
    label_color = {v: _LABEL_COLORS[i % len(_LABEL_COLORS)] for i, v in enumerate(schema_labels)}
    label_color["unresolved"] = "var(--fg)"
    width, height, pad = 1000, 600, 16
    circles = []
    for point in points:
        item_id = str(point.get("item_id"))
        mark = marks.get(item_id) or {}
        x = pad + float(point.get("x") or 0) * (width - 2 * pad)
        y = pad + float(point.get("y") or 0) * (height - 2 * pad)
        g = point.get("group")
        final = mark.get("final")
        lc = label_color.get(final, "var(--mut)") if final else "var(--mut)"
        cls = "pt" + (" drawn" if mark else "") + (" done" if final else "")
        tip = f'item {item_id} · G{int(g) + 1 if isinstance(g, int) else "?"}'
        if mark:
            tip += f' · {mark["round"]}' + (f' · final: {final}' if final else " · not labeled yet")
        circles.append(
            f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="7" data-item="{_esc(item_id)}" '
            f'data-group="{_esc(g)}" style="--gc:{_group_color(g)};--lc:{lc}"><title>{_esc(tip)}</title></circle>'
        )
    drawn = sum(1 for p in points if str(p.get("item_id")) in marks)
    done = sum(1 for p in points if (marks.get(str(p.get("item_id"))) or {}).get("final"))
    group_legend = "".join(
        f'<button class=leg type=button data-group-pick="{int(r["group"])}">'
        f'<i class=dot style="background:{_group_color(r["group"])}"></i>G{int(r["group"]) + 1} '
        f'<span class=kw>{_esc(" · ".join(_clean_keywords(r.get("keywords"))[:2]))}</span></button>'
        for r in group_rows
    )
    pane_data = {
        "version": m.get("version"),
        "groups": {str(int(r["group"])): {"name": f'G{int(r["group"]) + 1}', "color": _group_color(r["group"]),
                                          "keywords": _clean_keywords(r.get("keywords")), "size": r.get("size")}
                   for r in group_rows},
        "marks": {item: {"round": mk.get("round"), "final": mk.get("final")} for item, mk in marks.items()},
        "label_colors": label_color,
        "points3d": [[str(r.get("item_id")), r.get("x"), r.get("y"), r.get("z"),
                      next((pt.get("group") for pt in points if str(pt.get("item_id")) == str(r.get("item_id"))), None)]
                     for r in emb.get("map3d") or []],
    }
    has3d = bool(pane_data["points3d"])
    label_legend = "".join(
        f'<span><i class=dot style="background:{c}"></i>{_esc(v)}</span>' for v, c in label_color.items()
        if v != "unresolved" or any((mk.get("final") == "unresolved") for mk in marks.values())
    ) + '<span><i class="dot faint"></i>not labeled</span>'
    mapcard = (
        f'<div class="card mapwrap" data-color=group><h2>Map<span class=tally>{_esc(len(points))} items · '
        f'{_esc(groups.get("k"))} groups</span></h2>'
        '<div class=line><span class=lbl>Color by</span>'
        '<button class="pill tog on" type=button data-map-color=group>Group</button>'
        '<button class="pill tog" type=button data-map-color=label>Your labels</button></div>'
        '<div class=line><span class=lbl>Show</span>'
        '<button class="pill tog on" type=button data-map-show=all>All items</button>'
        f'<button class="pill tog" type=button data-map-show=round title="Only the items a round picked for you to label">Picked for labeling ({_esc(drawn)})</button>'
        '<span class=zoomctl>'
        + ('<button class="pill tog on" type=button data-map-dim=2d>2D</button>'
           '<button class="pill tog" type=button data-map-dim=3d>3D</button>'
           '<button class="pill tog" type=button data-spin hidden>Spin</button>' if has3d else '')
        + '<button class="pill tog" type=button data-zoom=in aria-label="Zoom in" title="Zoom in (or pinch)">+</button>'
        '<button class="pill tog" type=button data-zoom=out aria-label="Zoom out" title="Zoom out">−</button>'
        '<button class="pill tog" type=button data-zoom=reset>Reset</button></span></div>'
        f'<svg class=map viewBox="0 0 {width} {height}" role=img title="Drag to move" '
        f'aria-label="Map of {_esc(len(points))} development items"><g class=zoom><g class=links></g>'
        f'{"".join(circles)}</g></svg>'
        + (f'<canvas class=map3d hidden role=img aria-label="3D map of {_esc(len(points))} development items"></canvas>'
           if has3d else '')
        + f'<div class="legend group">{group_legend}</div>'
        f'<div class="legend label">{label_legend}</div>'
        '<div class=pick data-pick hidden></div>'
        f'<p class=mut>◯ picked {_esc(drawn)} · labeled {_esc(done)}</p>'
        f'<script type=application/json class=embdata>{_script_json(pane_data)}</script></div>'
    )

    records = []
    for r in group_rows:
        g = int(r["group"])
        ids = [str(p.get("item_id")) for p in points if p.get("group") == g]
        in_round = [marks[i] for i in ids if i in marks]
        finals = [mk["final"] for mk in in_round if mk.get("final")]
        tally = " · ".join(f"{v} {finals.count(v)}" for v in [*schema_labels, "unresolved"] if finals.count(v))
        records.append(
            f'<tr class=grp data-group-pick="{g}" tabindex=0>'
            f'<td><span class=rid><i class=dot style="background:{_group_color(g)}"></i>G{g + 1}</span></td>'
            f'<td><b>{_esc(" · ".join(_clean_keywords(r.get("keywords"))) or "no distinctive words")}</b>'
            f'<div class=exbox data-no-light><button class="pill tog" type=button data-ex-group="{g}">'
            f'Show typical items</button></div></td>'
            f'<td class=num data-label=items>{_esc(r.get("size"))}</td><td class=num data-label=picked>{len(in_round)}</td>'
            f'<td class=num data-label=labeled>{len(finals)}{f" <span class=mut>({_esc(tally)})</span>" if tally else ""}</td></tr>'
            f'<tr class=exrow hidden><td colspan=5 data-no-light><div class=exs data-ex-list="{g}"></div></td></tr>'
        )
    clarity = _group_clarity(groups)
    groupcard = (
        '<div class="card"><h2>Groups<span class=tally>k-means on the vectors</span></h2>'
        + clarity
        + '<div class=scroll><table class=grptable><thead><tr><th>Group</th><th>Keywords</th><th>Items</th>'
        '<th>Picked</th><th>Labeled</th></tr></thead><tbody>' + "".join(records) + '</tbody></table></div>'
        '</div>'
    )

    files = ", ".join(f'<code>{_esc(f.get("path"))}</code>' for f in m.get("files") or [])
    scores = groups.get("silhouette_by_k") or {}
    started_words, started_cls = _started_text(emb.get("started"))
    record = _card("Build record", "".join([
        _row("run", f'<code>{_esc(m.get("run"))}</code>'),
        _row("built", _esc(_when(m.get("created_at")))),
        _row("started", _esc(started_words), started_cls),
        _row("model", f'<code>{_esc(model_id)}</code> · {_esc(m["model"].get("device"))} · '
                      f'{_esc(m["model"].get("dtype") or "float32")}'
                      + (f' · {_esc(m["model"]["license"])}' if m["model"].get("license") else "")),
        _row("folder", f'<code>{_esc(_repo_relative(emb["folder"]))}/</code>'),
        _row("files", f'<code>manifest.json</code>, {files}'),
        _row("map", f'{_esc((m.get("map") or {}).get("method"))}, seed {_esc((m.get("map") or {}).get("seed"))}'),
        _row("groups", f'k = {_esc(groups.get("k"))}, set in the run settings' if settings.get("groups") else
                       f'k = {_esc(groups.get("k"))}, the best of k = {_esc(min(scores, key=int) if scores else "?")} '
                       f'to {_esc(max(scores, key=int) if scores else "?")} by silhouette'),
        _row("rebuild", f'<code>{_esc(command)}</code>'),
    ]))
    who = (emb.get("started") or {}).get("person")
    built_line = f'built {_when(m.get("created_at"))}' + (f' by {who}' if who else "")
    return (mapcard + groupcard
            + f'<details class=fold><summary>How the map is made: from text to numbers</summary>{recipe}{example}</details>'
            + f'<details class=fold><summary>Technical details · {_esc(built_line)}</summary>{record}</details>')


def _group_clarity(groups: dict) -> str:
    """How separated the groups really are, in words: a weak split must not read as real categories."""
    scores = groups.get("silhouette_by_k") or {}
    best = scores.get(str(groups.get("k")))
    if not isinstance(best, (int, float)):
        return ""
    if best >= 0.5:
        words, cls = "clear", "ok"
    elif best >= 0.25:
        words, cls = "some separation", "mut"
    else:
        words, cls = "weak", "warn"
    return f'<p class="{cls}">groups: {_esc(words)} <span class=mut>(score {best:.2f})</span></p>'


def _wf_cell(text: str) -> str:
    """'start + shows · Embedding' with the verbs bold; '—' (nothing in this Space) is left blank."""
    text = str(text or "").strip()
    if text in {"", "—"}:
        return ""
    verbs, _, where = text.partition(" · ")
    verbs_html = " + ".join(f"<b>{_esc(v.strip())}</b>" for v in verbs.split("+"))
    return verbs_html + (f" · {_md_inline(where)}" if where else "")
