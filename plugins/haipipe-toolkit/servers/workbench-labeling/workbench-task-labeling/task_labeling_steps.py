"""The items Task's three steps: their state from disk, what we have, the proposal to sign, the prompt that takes
notes, and the steps as views on the focus page every level shares."""
from __future__ import annotations

import re
from pathlib import Path
from live.frame import Space, esc, face, rel
from live import labeling_theme as T
from live.ui_parts import plural_word
from live.labeling_theme import NOTES, _block_of, _engine_job

from live.task_labeling_read import (IT, OLD_RESULT, RESULTS, _cell, _config, _embedding_state, _face_part,
                                     _item_runs, _items_facts, _kv, _not_yet, _op, _open_run, _raw_card, _runs_of,
                                     _signs, _status, _yaml_file)
from live.task_labeling_cards import _data_cards, _embed_runs, _embedding_cards, _items_cards, _run_link, data_point


# ── the steps: state from disk, what we have, the proposal to sign, the prompt that takes notes ───────
ITEM_STEPS = (
    ("raw", "📥 Step 1 · Data", "describe", _data_cards),
    ("make", "🧱 Step 2 · Items", "items", _items_cards),
    ("embed", "🗺 Step 3 · Embedding", "embed", _embedding_cards),
)
SKILL = "haipipe-labeling-preparation"


def _step_states(task: Path, root: Path, job: dict | None, block: Path | None) -> dict:
    lane, emb, _ = _embedding_state(job, block)
    builds = (emb or {}).get("builds") or [] if isinstance(emb, dict) else []
    done = {"raw": _raw_card(task)[1] is not None,                  # each step done by its own Run only
            "make": bool(_items_facts(task, root)["done"]),
            "embed": bool(builds) or any(r[2] for r in _embed_runs(task))}
    states, nexted = {}, False
    for key, _, op, _ in ITEM_STEPS:                                 # the first step not done is next
        states[key] = "done" if done[key] else ("next" if not nexted else "todo")
        nexted = nexted or not done[key]
        if states[key] == "todo" and key == "embed" and done["make"]:
            states[key] = "next"                                       # items made before Data cards existed
        if states[key] != "todo":
            open_ = _open_run(task, op)
            if open_ is not None and op in ("items", "embed"):
                states[key] = "ready" if _signs(open_) else "sign"       # a proposal waits for the person
    return states


def _prompt(key: str, state: str, task: Path, root: Path, again: bool = False) -> str:
    t = rel(task, root)
    op = {"raw": "describe", "make": "items", "embed": "embed"}[key]
    open_ = _open_run(task, op)
    if again:
        f = _items_facts(task, root)
        version = Path(str(f["metrics"].get("store") or f["manifest"].get("store") or "the items")).name
        return f"/{SKILL} {t} revise: read my notes on {version}, plan the revised recipe, and stop for my Sign."
    if key == "raw":
        return f"/{SKILL} {t} describe: plan and run the describe Run, then fill the Data cards. No items."
    if state in ("sign", "ready") and open_ is not None:
        word = "Sign" if op == "items" else "Agree"
        return (f"/{SKILL} {t} {op}: " + (f"I {word} {open_.name} on the screen first; then " if state == "sign" else "")
                + f"run {open_.name} and settle it.")
    if key == "make":
        return f"/{SKILL} {t} items: plan the items Run from the Data cards, and stop for my Sign."
    return f"/{SKILL} {t} embed: plan the embedding Run, and stop for my Agree."


def _what_we_have(key: str, task: Path, root: Path, job) -> str:
    if key == "raw":
        data = IT.job_data(task, root) if IT else {"dataset": "", "data": ""}
        files = IT.data_files(root, data["data"]) if IT and data["data"] else []
        rows = [("Dataset", esc(data["dataset"] or "—")),
                ("Folder", f'<code>{esc(data["data"])}</code>' if data["data"] else
                 '<span class=mut>no <code>data:</code> line in the Job</span>'),
                ("Files", " · ".join(f"<code>{esc(p.name)}</code> {p.stat().st_size / 1e6:.1f} MB" for p in files)
                 or '<span class="st st-warn">not found</span>')]
        return _kv(rows)
    if key == "make":
        run, card = _raw_card(task)
        if not card:
            return _not_yet("Step 1 first.")
        t, proof = card.get("table") or {}, (card.get("grain") or {}).get("proof") or {}
        unit = (card.get("grain") or {}).get("unit")
        return _kv([("Data", f"the Data cards, from <code>{esc(run.name)}</code>"),
                                ("Rows", esc(f'{t.get("rows", 0):,} rows' + (f' · {proof.get("distinct_" + unit, 0):,} '
                                                                            + unit.removesuffix("_id") + "s" if unit else ""))),
                                ("Kept out", esc(" · ".join(lb["column"] for lb in card.get("labels") or []) or "—"))])
    f = _items_facts(task, root)
    if not f["done"]:
        return _not_yet("Step 2 first.")
    return _kv([("Items", f'<code>{esc(f["metrics"].get("store") or f["manifest"].get("store"))}</code> · '
                                      f'{esc(f["manifest"].get("items", "—"))} items, from <code>{esc(f["run"].name)}</code>'),
                            ("Text", esc(str(f["manifest"].get("item") or "—")))])


def _sign_box(task: Path, root: Path, run: Path, word: str) -> str:
    s = _signs(run)
    if s:
        return f'<p><span class="st st-ok">✓ {esc(word)}</span> · {esc(s.get("at", ""))}</p>'
    body = esc('{"action": "sign", "task": "%s", "run": "%s"}' % (rel(task, root), run.name))
    # a sign needs no name (settled 5; round 4: the "name (optional)" box went): the host records "a person"
    return (f'<p class=sign-row><button type=button class=work-act data-post="/_board/labeling/items" '
            f'data-body="{body}">{"Agree" if word == "agreed" else "Sign"}</button></p>')


def _speakers(turns: dict) -> str:
    """The recipe's turn names in words (round 4: "turns: Person → Person"): a speaker kept as it is is named once, a
    renamed one says what it is shown as."""
    words = [str(k) if str(k) == str(v) else f"{k} shown as {v}" for k, v in turns.items()]
    return ("speaker: " if len(words) == 1 else "speakers: ") + ", ".join(words)


def _proposal(key: str, task: Path, root: Path) -> str:
    """The recipe (Step 2) or the build (Step 3) the agent proposed, for a person to sign or agree."""
    op = {"make": "items", "embed": "embed"}.get(key)
    run = _open_run(task, op) if op else None
    if run is None:
        return _as_signed(key, task, root)
    c = _config(task, run)
    if op == "items":
        r = c.get("recipe") or {}
        cb = r.get("context_before") or {}
        rows = [("One item", esc(f"one {r.get('unit')}") + f" · id <code>{esc(r.get('item_id'))}</code>"),
                ("Judged", f"<code>{esc(r.get('main'))}</code>"),
                ("Before", (f"<code>{esc(cb.get('column'))}</code>" + (" · " + esc(_speakers(cb["turns"]))
                                                                        if cb.get("turns") else ""))
                 if cb else "none"),
                ("After", f"<code>{esc((r.get('context_after') or {}).get('column'))}</code>"
                 if r.get("context_after") else "none"),
                ("Kept out", esc(plural_word(len(r.get('keep_out') or []), "column", "columns") + ": "
                                 + ", ".join((r.get("keep_out") or [])[:6])
                                 + (f" and {len(r['keep_out']) - 6} more" if len(r.get("keep_out") or []) > 6 else ""))),
                ("Group", esc(f"the {r.get('group')}, never split" if r.get("group") else "—")),
                ("Writes", f"<code>{esc(c.get('out'))}</code>")]
        if c.get("revise_of"):
            rows.insert(0, ("Revises", f"<code>{esc(c['revise_of'])}</code>"))
            ch = str(c.get("changed") or "")
            rows.append(("Changed", '<span class="st st-warn">not typed yet</span>' if not ch or ch.startswith("<typed")
                         else esc(ch)))
        title, word = f"Recipe · {run.name}", "signed"
    else:
        rows = [("Model", esc(c.get("model"))), ("Embeds", esc("the judged text alone" if c.get("input") == "main"
                                                             else "the judged text with its turns before")),
                ("Map", esc(str(c.get("map") or "").upper())), ("Groups", esc(c.get("groups") or "chosen by fit")),
                ("Items", f"<code>{esc(c.get('items'))}</code>")]
        title, word = f"Build · {run.name}", "agreed"
    if c.get("notes"):
        rows.append(("Your notes", _cell(c["notes"])))
    failed = _status(run) == "failed"
    return (f'<div class="topic work-task"><div class=work-body><h4>{esc(title)}</h4>'
            + _kv(rows) + _sign_box(task, root, run, word)
            + (f'<p class="st st-warn">✗ failed: <code>{esc(rel(run / "result" / "runtime.yaml", root))}'
               '</code></p>' if failed else "") + "</div></div>")


def _as_signed(key: str, task: Path, root: Path) -> str:
    """A done step's recipe or build, as the person signed it; an older Run's from the face's Method part."""
    if key == "make":
        f = _items_facts(task, root)
        if not f["run"]:
            return ""
        c = _config(task, f["run"])
        s = _signs(f["run"])
        r = c.get("recipe")
        rows = ([("One item", esc(f"one {r.get('unit')}") + f" · id <code>{esc(r.get('item_id'))}</code>"),
                 ("Judged", f"<code>{esc(r.get('main'))}</code>"),
                 ("Before", f"<code>{esc((r.get('context_before') or {}).get('column'))}</code>"
                  if r.get("context_before") else "none"),
                 ("Kept out", esc(plural_word(len(r.get('keep_out') or []), "column", "columns")))] if isinstance(r, dict)
                else [("one item", esc(f["manifest"].get("item") or "—"))])
        rows += [("script", " · ".join(f'<code>{esc(x.relative_to(task).as_posix())}</code>' for x in f["scripts"]))
                 ] if f["scripts"] else []
        rows += [("signed", esc(str(s.get("at", "") or "yes")) if s else '—'),
                 ("its settings", f'<code>{esc(rel(f["config"], root))}</code>' if f["config"] and f["config"].is_file()
                  else "—")]
        return (f'<h4>Recipe, signed · {esc(f["run"].name)}</h4>' + _kv(rows)
                + _face_part(task, "Method"))
    if key == "embed":
        built = [r for r in _embed_runs(task) if r[2]]
        if not built:
            return ""
        run = built[-1][0]
        c, s = _config(task, run), _signs(run)
        return (f'<h4>Build, agreed · {esc(run.name)}</h4>' + _kv([
            ("model", esc(c.get("model") or _yaml_file(run / "result" / "manifest.yaml").get("model") or "—")),
            ("agreed", esc(str(s.get("at", "") or "yes")) if s else '<span class=mut>—</span>')]))
    return ""


PROMPT_HEAD = {"raw": ("Data", "describe the raw file"), "make": ("Items", "make the items"),
               "embed": ("Embedding", "embed the items"), "again": ("Items", "make the items again")}


def _session(task: Path) -> str:
    """The chat session a Task's prompts run in: the Task face's `session:`, else its Job's, else the Task's name."""
    for md in (face(task), face(task.parent)):
        text = md.read_text(encoding="utf-8", errors="ignore")[:3000] if md else ""
        m = re.search(r"(?m)^session:\s*(\S.*?)\s*$", text)
        if m:
            return m.group(1)
    return task.name


def _prompt_box(prompt: str, task: Path, root: Path, key: str, open_: bool = True) -> str:
    """The step's prompt in the Prompt box every theme shares (servers/workbench/ui_parts.prompt_box; JL 261101, b15
    s58 C1): the prompt, one notes row copied with it (kept in this browser; a pasted image kept in the Task's notes/,
    s41-D14), and the line that sends it to the Task's session. `open_` is kept for the callers: a done step folds."""
    from live.ui_parts import prompt_box
    step, asks = PROMPT_HEAD.get(key, (key.title(), ""))
    return prompt_box(prompt, (("your notes", "notes, a row, an image"),), _session(task), step=step, asks=asks,
                      key=f"notes:{rel(task, root)}#{key}", upload=(rel(task, root), "/_board/labeling/notes"))


# each step's state word on its bar (JL 261106: "every closed bar shows a state word on its right")
CHIPS = {"done": '<span class="st st-ok">✓ done</span>', "next": '<span class="st st-warn">→ next</span>',
         "sign": '<span class="st st-warn">✍ waits for your sign</span>',
         "ready": '<span class="st st-warn">→ signed, ready to run</span>', "todo": '<span class=st>· later</span>'}
WAIT_STYLE = "margin:2px 0 10px;font-size:13.5px;color:light-dark(#b35c00,#ffc078)"


def _waiting_form(task: Path, run: Path | None) -> Path | None:
    """A 🙋 form beside the steps that waits for the person and feeds `run` (its run.yaml `feeds:`): the questions the
    step's sign rests on (the walkthrough's items Task: the recipe's choices, asked before the recipe is signed)."""
    if run is None:
        return None
    for r, card in reversed(_item_runs(task)):
        feeds = card.get("feeds") or []
        feeds = feeds if isinstance(feeds, list) else [feeds]
        if "_collect_" in r.name and str(card.get("status") or "") == "waiting" and run.name in map(str, feeds):
            return r
    return None


def _form_title(form: Path) -> str:
    """A form's title, the first heading of its question_collection.md; its Run's name when it has none."""
    md = form / "question_collection.md"
    head = next((ln[2:].strip() for ln in (md.read_text(encoding="utf-8", errors="ignore").splitlines()
                                            if md.is_file() else []) if ln.startswith("# ")), "")
    return head or form.name


def _wait_line(task: Path, op: str, state: str) -> tuple:
    """(the one line that waits on the person, under the step's bar; the form it waits on, or None): only while the
    step's proposal waits for a Sign (the recipe) or an Agree (the build), and the form first when one feeds it."""
    if state != "sign" or op not in ("items", "embed"):
        return "", None
    what, verb = ("recipe", "Sign") if op == "items" else ("build", "Agree")
    form = _waiting_form(task, _open_run(task, op))
    if form is not None:
        return f"🙋 Answer {_form_title(form)} first, then read the {what} below and press {verb}", form
    return f"✍️ Read the {what} below and press {verb}", None


def _step_box(i: int, task: Path, root: Path, job, state: str) -> str:
    from live.frame import _file_url
    key, title, op, _ = ITEM_STEPS[i]
    wait, form = _wait_line(task, op, state)
    page = form / f"{form.name}.html" if form is not None else None
    ask = (f'<p class=items-form>🙋 <b>{esc(_form_title(form))}</b> waits for your answers: its choices are what your '
           f'{"Sign" if op == "items" else "Agree"} rests on. <a class=chip data-pop="{esc(form.name)}" '
           f'href="{esc(_file_url(page, root))}">Answer</a></p>' if page is not None and page.is_file() else "")
    body = ("<h4>Input</h4>" + _what_we_have(key, task, root, job) + ask + _proposal(key, task, root)
            + _prompt_box(_prompt(key, state, task, root), task, root, key, open_=state != "done"))
    return (f'<details class="topic work-task items-step"{"" if state == "done" else " open"}><summary>'
            f'<span class=related-head><b>{esc(title)}</b> {CHIPS[state]}</span></summary>'
            + (f'<p class=items-wait style="{WAIT_STYLE}">{esc(wait)}</p>' if wait else "")
            + f'<div class=work-body>{body}</div></details>')


def _again_box(task: Path, root: Path) -> str:
    """Step 2 again (s41-D14): the items as they are, and the revise prompt that takes the person's notes."""
    f = _items_facts(task, root)
    version = Path(str(f["metrics"].get("store") or f["manifest"].get("store") or "")).name
    body = (_kv([("Items", esc(f"{version} · {f['manifest'].get('items', '—')} items")),
                             ("Recipe", esc(str(f["manifest"].get("item") or "—")))])
            + _prompt_box(_prompt("make", "done", task, root, again=True), task, root, "again"))
    return (f'<details class="topic work-task items-step"><summary><span class=related-head><b>🧱 Revise the items</b>'
            f'</span></summary><div class=work-body>{body}</div></details>')


def _items_spaces(folder: Path, root: Path, sub: str) -> dict:
    from live.frame import href
    job, block = _engine_job(folder, root), _block_of(folder)
    r_sub = OLD_RESULT.get(sub, sub)
    r_sub = r_sub if r_sub in RESULTS else RESULTS[0]
    i = RESULTS.index(r_sub)
    states = _step_states(folder, root, job, block)
    key = ITEM_STEPS[i][0]
    state = states[key]
    cards = (_not_yet("The steps before first.") if state == "todo"
             else ITEM_STEPS[i][3](folder, root, job, block))
    again = _again_box(folder, root) if key == "make" and state in ("done",) else ""
    after = (f'<p><a class=chip href="{esc(href(folder, root, T.THEME, "Work Details", RESULTS[i + 1]))}">next: '
             f'{esc(ITEM_STEPS[i + 1][1])} →</a></p>' if i + 1 < len(ITEM_STEPS) else
             '')
    steps = tuple({"label": f"run-{op}-<task>", "doing": title.split(" · ", 1)[-1],
                   "prompt": _prompt(k, states[k], folder, root), "skills": [SKILL]} for k, title, op, _ in ITEM_STEPS)
    # page=True: these views are the whole row; the base's Draft, Evidence and Value views stay off (an items Task
    # has no Draft plan; JL 261014: "we don't need draft")
    # two parts (JL 261014): Operation, what a person does (the step, its prompt; the revise box), then Result,
    # what the step made (the cards)
    part = lambda name: f'<h3 style="margin:18px 0 6px">{name}</h3>'
    operation = part("Operation") + _step_box(i, folder, root, job, state) + again
    result = part("Result") + cards
    return {"Audience Report": Space(html=result, subspaces=RESULTS, open=r_sub, page=True,
                                     note="Results only."),
            "Work Details": Space(html=operation + result + after,
                                  subspaces=RESULTS, open=r_sub, run_types=steps, page=True),
            "Description": Space(note=NOTES["items"])}


# ── the items Task on the focus page every level shares (round 2 of the b15 review: the items Task kept an older
# single-section layout). Its views are its steps, Data · Items · Embedding; each is ⚙️ Process (the step: its input,
# the recipe or build it proposes with its Sign or Agree, then its prompt) and 📊 Results (what the step made), each
# section closed with its state word, then 🙋 Interaction last with the forms that step's sign rests on. Report shows
# the Results and the Interaction only. The same parts as _items_spaces, so the two layouts read the same files. ──
ITEM_VIEWS = (("data", "Data", "the raw table: what it holds, and rows drawn from it"),
              ("items", "Items", "the items a person labels, made under a signed recipe"),
              ("embedding", "Embedding", "the items mapped into groups, under an agreed build"))
ITEM_PROCESS = ("📥 Describe the raw table", "🧱 Make the items", "🗺 Embed the items")
ITEM_RESULTS = ("🗂 Data cards", "🧱 Items", "🗺 Embedding map")
OP_VIEW = {"describe": "data", "items": "items", "embed": "embedding"}
STEP_WORD = {"done": ("done", "ok"), "next": ("next", ""), "sign": ("waits for your sign", "you"),
             "ready": ("signed, ready to run", "run"), "todo": ("later", "")}
BUTTON_WORD = {"done": ("done", "ok"), "next": ("next", ""), "sign": ("your sign", "you"), "ready": ("ready to run", ""),
               "todo": ("later", "")}                 # every button says where its step stands (round 4: Embedding)


def items_states(task: Path, root: Path) -> dict:
    """{view: the step's state (done, next, sign, ready, todo)}."""
    states = _step_states(task, root, _engine_job(task, root), _block_of(task))
    return {view: states[key] for (key, *_), (view, *_) in zip(ITEM_STEPS, ITEM_VIEWS)}


def items_words(task: Path, root: Path) -> dict:
    """{view: (its button's word, ok | you | "")}."""
    return {view: BUTTON_WORD[state] for view, state in items_states(task, root).items()}


def items_default(task: Path, root: Path) -> str:
    """Where Work opens: the step that waits for a sign, else the next one, else the last."""
    states = items_states(task, root)
    return (next((v for v, s in states.items() if s == "sign"), "")
            or next((v for v, s in states.items() if s in ("ready", "next")), "") or ITEM_VIEWS[-1][0])


def item_forms(task: Path, root: Path, view: str) -> list:
    """The collection Runs this step's 🙋 Interaction shows: those that feed one of its Runs (run.yaml `feeds:`), else
    the step named in the form's own name (_collect_items_…, _collect_embed_…); any other form goes to Items."""
    from live import focus_page as F

    def home(r) -> str:
        for fed in r.get("feeds") or []:
            run = task / "runs" / Path(str(fed)).name
            if run.is_dir() and _op(task, run) in OP_VIEW:
                return OP_VIEW[_op(task, run)]
        slug = r["run"].split("_collect_", 1)[-1]
        return next((v for word, v in (("describe", "data"), ("data", "data"), ("embed", "embedding"))
                     if slug.startswith(word)), "items")
    return [r for r in F.interactions(task, root) if Path(r["page"]) == task and home(r) == view]


def _results_word(key: str, task: Path, root: Path, state: str) -> str:
    """A Results bar's word, read from the step's own files: Data's its point, "600 rows · 30 chats · 20 raters"."""
    if state == "todo":
        return "later"
    if key == "raw":
        return data_point(task) or "not described yet"
    if key == "make":
        f = _items_facts(task, root)
        n = f["manifest"].get("items") if f["done"] else None
        return f"{n} items" if n not in (None, "") else "made" if f["done"] else "not made yet"
    return "built" if state == "done" else "not built yet"


RUN_WORD = {"complete": "done", "completed": "done", "done": "done", "ok": "done", "waiting": "waits for you",
            "planned": "planned", "signed": "signed", "failed": "failed", "running": "running"}


def _step_runs(task: Path, root: Path, op: str) -> str:
    """The step's own Runs, each opening its card and receipt in the pop-out, with its state (round 4: "open
    r01_describe's receipt: no view links it"). A form that feeds them is the view's 🙋 Interaction, never here
    (settled 3)."""
    links = []
    for run in _runs_of(task, op):
        links.append(_run_link(task, root, run) + f' <small>{esc(RUN_WORD.get(_status(run), _status(run)))}</small>')
    return _kv([("Runs", " · ".join(links) or '<span class=mut>no Run yet</span>')])


def _side_parts(eid: str, parts: list, top: str) -> str:
    """A step's cards as side tabs, the one kind of tabs (settled 4; round 4: Data opened onto seven bare folds), its
    tiles above them."""
    from live.ui_parts import _side_tabs
    if not parts:
        return top
    return top + _side_tabs(eid, [(t, w) for t, w, _ in parts], [b for _, _, b in parts])


def items_view(task: Path, root: Path, section: str, view: str) -> str:
    """One step of an items Task, in the shared shape (see above): its Process one closed bar holding its input, its
    Runs, the recipe or build with its Sign or Agree, and its prompt (round 4: the prompt sat open under the bar)."""
    from live import focus_page as F, interaction_section as IX
    from live.ui_parts import _numbered
    from live.labeling_step_parts import _section
    from live.labeling_steps import quiet_prompt
    i = [v for v, *_ in ITEM_VIEWS].index(view)
    key, _, op, cards_of = ITEM_STEPS[i]
    job, block = _engine_job(task, root), _block_of(task)
    state = _step_states(task, root, job, block)[key]
    forms = item_forms(task, root, view)
    wait, _ = _wait_line(task, op, state)
    if wait:                       # the waiting item itself, the first open question as its 🙋 Interaction says it, else
        run = _open_run(task, op)  # the sign (round 4: "Answer … in 🙋 Interaction below, then …" read as a chore list)
        what, verb = ("recipe", "Sign") if op == "items" else ("build", "Agree")
        wait = IX.state_word(forms)[1] or f"✍️ The {what} {run.name if run else ''} waits for your {verb}".replace("  ", " ")
    prompt = quiet_prompt(_prompt_box(_prompt(key, state, task, root), task, root, key))
    step = _section(ITEM_PROCESS[i], "<h4>Input</h4>" + _what_we_have(key, task, root, job) + _step_runs(task, root, op)
                    + _proposal(key, task, root) + prompt, STEP_WORD[state][0], wait)
    process = step
    if key == "make" and state == "done":               # Step 2 again (s41-D14): the items as they are, and their revise
        f = _items_facts(task, root)
        version = Path(str(f["metrics"].get("store") or f["manifest"].get("store") or "")).name
        process += _section("🧱 Revise the items", _kv([("Items", esc(f"{version} · {f['manifest'].get('items', '—')} items")),
                                                       ("Recipe", esc(str(f["manifest"].get("item") or "—")))])
                            + quiet_prompt(_prompt_box(_prompt("make", "done", task, root, again=True), task, root, "again")),
                            "when you need it")
    if state == "todo":
        cards = _not_yet("The steps before first.")
    else:
        parts, top = cards_of(task, root, job, block, as_parts=True)
        cards = _side_parts(f"it{key}", parts, top) or cards_of(task, root, job, block)   # else its own "not yet" line
    results = _section(ITEM_RESULTS[i], cards or _not_yet("Nothing to show yet."), _results_word(key, task, root, state))
    body = _numbered(process + results)  # Work retired (JL 261111): one list, no Process/Results heading
    body += IX.view_section(forms, root, IX.next_number(body), lambda r: F.interaction_where(r, task, root))
    if i + 1 < len(ITEM_VIEWS):
        nxt, name, _ = ITEM_VIEWS[i + 1]
        body += f'<p class=ls-next><a href="{esc(F.page_url(task, root, "report", nxt))}">next: {esc(name)} →</a></p>'
    return f'<div class="ls-view lf-items">{body}</div>'
