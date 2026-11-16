"""The draft Task's Work views: each step with its facts, prompts, Runs and what it asks of a person."""
from __future__ import annotations

import html as _html
import re
from pathlib import Path
from live import draft_steps as ds
from live.frame import esc, runs_of
from live.ui_parts import GROUP_CSS, _numbered, _section
from live.focus_draft_words import ASKS, FOLD, INPUT, LAZY, PROMPT, RUN_PREFIX, SIGN, STATE_WORD, VERBS, WAITS, WORK
from live.focus_draft_assets import CSS, JS

SECTION_VERBS = {"report": "check", "work": "do", "studio": "think", "delivery": "hand over", "timeline": "look back",
                 "files": "browse", "related": "take in"}


def is_draft(folder: Path) -> bool:
    from live.frame import task_type
    return task_type(folder) == "draft"


def word(state: str, k: int = 1) -> tuple:
    """(the state's word, its class): a step's state as a word (haipipe-ui rule 5), warn when it waits on you."""
    w = STATE_WORD.get(state, state).format(k=k)
    return w, "fd-you" if state in WAITS else "fd-ok" if state == "done" else ""


def _facts(folder: Path, root: Path) -> tuple:
    from live.focus_draft_report import paragraphs
    f = ds.facts(folder, root)
    st = ds.states(f)
    # text adopted into the face (## Content) is written, though no draft holds it (r03: Status said "not started" and
    # Write "later" over "2 paragraphs, adopted"); the steps after it come next
    if st.get("2 · Write") in ("todo", "next") and any(t for _, _, t in paragraphs(folder)):
        st["2 · Write"] = "done"
        st.update({s_: "next" for s_ in ("3 · Evidence", "5 · Revise", "Delivery") if st.get(s_) == "todo"})
    w = st.get("2 · Write")
    st["2 · Draft"] = w if w in ("todo", "next", "early") else st.get("5 · Revise", w)
    k = len((f["draft"] or {}).get("previous", [])) + 1
    return f, st, k


def _prompts(op: str) -> list:
    """[(its title, prompt, tail, notes key)] of the old Operation's prompt boxes, the prompt text as draft_steps
    wrote it (one owner of every prompt)."""
    return [(re.sub(r"<[^>]+>", "", _html.unescape(t)).strip(), _html.unescape(c), _html.unescape(tail or ""),
             _html.unescape(key)) for t, c, tail, key in PROMPT.findall(op)]


def _run_rows(prompts: list) -> str:
    """The prompts as verbs: one box for your notes, then a button per prompt that copies it with them (and the line
    that sends it to the Task's session); the prompt itself shows when you rest on its button."""
    if not prompts:
        return ""
    buttons = "".join(f'<button type=button class="fd-btn fd-copy" title="{esc(prompt)}" data-copy="{esc(prompt)}"'
                      + (f' data-tail="{esc(tail)}"' if tail else "")
                      + f'>{esc(VERBS.get(key.rsplit("#", 1)[-1], "Copy prompt"))}</button>'
                      for title, prompt, tail, key in prompts)
    return (f'<div class=fd-run><textarea rows=1 data-key="{esc(prompts[0][3])}" placeholder="your notes, copied with '
            f'the prompt"></textarea><div class=fd-bar>{buttons}</div></div>')


def _ask(step: str, state: str, draft: Path | None = None, root: Path | None = None) -> str:
    """What the step waits for, one row, with Open: the draft, where the person signs."""
    ask = ASKS.get(step, {}).get(state)
    if not ask:
        return ""
    name, what = ask
    from live.frame import reader
    verb, how = SIGN.get(step, ("Open the draft", ""))
    open_ = (f'<a class=fd-btn data-pop="{esc(draft.name)}" title="{esc(how)}" href="{esc(reader(draft, root))}">{esc(verb)}</a>'
             if draft and root and draft.is_file() else "")
    return f'<div class=fd-ask role=status><span class=n>{name}</span><span class=d>{what}</span>{open_}</div>'


def _runs(folder: Path, root: Path, step: str) -> str:
    """The Task's own Runs this step makes, one row each: name, type, status."""
    rows = [r for r in runs_of(folder) if r["run"].startswith(RUN_PREFIX.get(step, ("\0",)))]
    if not rows:
        return ""
    return _section("🏃 Runs of this step", "".join(   # each row shows its own status; no tally on the bar
        f'<div class=fd-row><span class=n><code>{esc(r["run"])}</code></span><span class=d>{esc(r["type"])}</span>'
        f'<span class=w>{esc(r["status"])}</span></div>' for r in rows))


def flatten(html: str) -> str:
    """Every fold left in a step's HTML becomes a section, its summary the heading (haipipe-ui rule 4: no fold arrows);
    a drawing that loaded only when its fold opened is embedded where it stands, its heading's Open still pops it out
    (JL 261104: "why the draw is not emebeded"). `loading=lazy`, so a page of them stays quick."""
    html = LAZY.sub(lambda m: f'<iframe class="st-frame fd-draw" title="{m.group(1)}" src="{m.group(2)}" loading=lazy '
                              'referrerpolicy=no-referrer></iframe>', html)
    return FOLD.sub(lambda m: f'<section class=fd-sec><h3 class=fd-h>{m.group(1).replace(">↗</a>", ">Open ↗</a>")}</h3>'
                    f'{re.sub(r"^<div class=work-body[^>]*>(.*)</div>$", lambda b: b.group(1), m.group(2), flags=re.S)}</section>',
                    html)


def _after_first_section(html: str, extra: str) -> str:
    """`extra` placed after the first section (Scratch, a note per paragraph, right under the plan it annotates)."""
    first = html.find("<section class=fd-sec>")
    second = html.find("<section class=fd-sec>", first + 1) if first >= 0 else -1
    return html[:second] + extra + html[second:] if second > 0 else html + extra


# "Ask the agent" only where JL asked for prompts, structure and drafting (JL 261020); elsewhere it was clutter (JL
# 260927, and 261031 on 4 · Display: "I don't think we need this")
ASK_STEPS = ("1 · Plan", "2 · Write", "5 · Revise", "2 · Draft")


def step_html(folder: Path, root: Path, step: str) -> str:
    """One step, its sections in order: what waits for you, Ask the agent (the prompts as verbs), the step's Result
    cards (each a section), its Input, its Runs. Scratch (1 · Plan) is the Page's own editor, as on the old page."""
    from live.focus_draft_report import STATUS_WHAT, aims, content_read, paragraphs, responds_to, text_count
    f, st, k = _facts(folder, root)
    token = ds.FLAT.set(True)
    try:
        if step == "2 · Draft":                 # Revise's board first, then Write's examples and your own editor
            w = ds._write(f, folder, root, st["2 · Write"], editor=False)
            r = ds.STEP_VIEWS["5 · Revise"](f, folder, root, st["5 · Revise"])
            op, result = w[0] + r[0], r[1] + w[1]   # the board, the review, then Write's examples (JL 261113)
        else:
            op, result, _ = ds.STEP_VIEWS[step](f, folder, root, st[step])
        scratch = (ds._editor(folder, root, "📝 Scratch · your notes, a paragraph each", view="scratch", open_=True)
                   if step == "1 · Plan" and f["draft"] and f["draft"]["structure"] else "")
        running = ds._running(f, step)
    finally:
        ds.FLAT.reset(token)
    table = INPUT.search(op)
    report = responds_to(folder) if step == "1 · Plan" else None
    if table and report is not None:             # a response letter's plan reads the comments it answers (r02)
        from live.frame import reader
        row = ds._kv([("Comments it answers", f'<a data-pop="{esc(report.parent.name)}" href="{esc(reader(report, root))}">'
                       f'{esc(report.parent.name)}</a>')])
        row = re.search(r"<tr>.*</tr>", row, re.S).group(0)
        table = re.search(r"(?s)(.*)", table.group(1).replace("</tbody></table>", row + "</tbody></table>", 1))
    sign = re.search(r"<p class=sign-row>(.*?)</p>|<p><span class=\"st st-ok\">✓ signed</span>(.*?)</p>", op, re.S)
    signed = (f'<p class=mut>✓ signed {sign.group(2)}</p>' if sign and sign.group(2) else "")
    # Preserve the step's input, prompt and sign alongside its existing content.
    # the open forms are the view's last section, 🙋 Interaction, so this step no longer repeats them (JL 261105: "keep
    # only the bottom"); what is left is the step's own state: a Run running, its ask, its sign
    waits = running + _ask(step, st[step], (f["draft"] or {}).get("file"), root) + signed
    # each bar's state word is the step's own (JL 261106: "every closed bar shows a state word on its right"); what the
    # step waits for shows under its closed bar
    said = "running" if running else STATUS_WHAT[st[step]].format(k=k)
    ask = ASKS.get(step, {}).get(st[step])
    line = f"🙋 {ask[0]} {re.sub(r'<[^>]+>', '', ask[1])}" if ask and not running else ""
    process = _section("📌 Where this step stands", waits, said, line) if waits else ""
    boxes = quiet(boxes_of(op))                  # the shared Prompt boxes, whole; the session line rides the copy only
    n_boxes = boxes.count("<!--pb-prompt-->")      # its own word: the wait is said once, on Where this step stands (r01)
    if step == "2 · Draft":                     # your own editor, one link where the prompts are (JL 261113)
        src = ds._editor_src(folder, root, "revise")
        boxes += (f'<p><a class=fd-btn data-pop="Write it yourself" href="{esc(src.replace("&embed=1", ""))}">'
                  '✍️ Write it yourself ↗</a></p>') if src else ""
    process += _section("🤖 Ask the agent", boxes, f"{n_boxes} prompt{'s' * (n_boxes != 1)}") if step in ASK_STEPS and boxes else ""
    if step == "3 · Evidence":                  # a Section never runs evidence itself: the Board's evidence Jobs check
        from live.board_checks import checks_html    # its printed values and citations, and it reads their verdict here
        checked, cword = checks_html(folder, root)   # (JL 261113: "how do you think this to the block level evidence???")
        process += _section("✅ Checked at the Board", checked, cword) if checked else ""
    elif step != "2 · Draft":                   # Draft shows the text, its cards and the review, no Input or Runs
        process += _section("📥 Input", table.group(1) if table else "", input_word(table.group(1) if table else "")) + _runs(folder, root, step)
    results = _drop_repeats(step, _after_first_section(flatten(result), flatten(scratch)))
    if NO_TEXT in results and paragraphs(folder):   # no draft yet, but adopted Content: Write and Revise read the text
        results = results.replace(NO_TEXT, _section("📝 The adopted text", content_read(folder, root), text_count(folder)), 1)
        results = results.replace(NO_TEXT, "")          # Draft holds Write's and Revise's: the text shows once
    if step == "2 · Draft":                     # only the text with its cards, then the review (JL 261113: "these
        keep = [(a, b, t) for a, b, t in _top_sections(results)        # views are not that necessary")
                if "The text" in t or "The adopted text" in t or "Review Report" in t or "Examples" in t]
        kind = lambda t: 1 if "Review Report" in t else 2 if "Examples" in t else 0   # a pass title may say "text"
        keep.sort(key=lambda x: kind(x[2]))
        process = ""                            # no "Where this step stands", no "Ask the agent" on Draft (JL 261113:
                                                # "we don't need these two, but the 3 one should definitely be the Examples")
        assets = "".join(re.findall(r"<style\b.*?</style>|<script\b.*?</script>", results, re.S))   # the board's CSS and JS
        # three plain names (JL 261113: "1 - Drafting Workdesk, 2 - Review Report, 3 - Examples, that's all"; then "Draft
        # Lab": "why sentence? I want to call it Drafting Board? or Draft Lab", and Board is the paper's own word)
        def plain(html: str, title: str) -> str:
            html = re.sub(r"(<h3 class=fd-h>).*?(?=<span class=(?:\"?word|word)|</h3>)", lambda m: m.group(1) + title, html, count=1, flags=re.S)
            # no state word on these bars (JL 261113, of "5 cards wait for you" and "nothing yet": "no need to add this")
            html = re.sub(r"<p class=fd-wait>.*?</p>", "", html, count=1, flags=re.S)
            return re.sub(r"(<h3 class=fd-h>[^<]*)<span class=\"?word[^>]*>[^<]*</span>", r"\1", html, count=1)
        name = lambda t: ("✍️ Draft Lab", "📋 Review Report", "📚 Examples")[kind(t)]
        results = (assets + "".join(plain(results[a:b], name(t)) for a, b, t in keep)) if keep else results
        from live.draft_rubric import html as rubric_html    # 4 · Writing Rubric: tabs of rules, rules can be added
        results += _section("📏 Writing Rubric", rubric_html(folder, root))
        from live.draft_rubric import decisions_html             # 5 · Decisions: this Section, its contract, the paper, the venue
        results += _section("⚖️ Decisions", decisions_html(folder, root))
    rows = "".join(f'<div class=fd-row><span class=n>{esc(n)}</span><span class=d>{esc(v)}</span></div>' for n, v in aims(folder))
    if step == "1 · Plan" and rows:             # the aims and opening, once Plan + Results' (JL 261113: that view went)
        results = _section("🎯 What this Section must do", rows, "from its face") + results   # every bar says its state
    if step == "1 · Plan":                      # only the Structure and the Examples (JL 261115: "why we need so many,
        assets = "".join(re.findall(r"<style\b.*?</style>|<script\b.*?</script>", results, re.S))   # I think we just
        ex = lambda t: "examples" in t.lower() or "Section canvas" in t     # the canvas holds our text and the examples
        keep = [(a, b, t) for a, b, t in _top_sections(results) if "Structure" in t or ex(t)]  # need to have Structure
        keep.sort(key=lambda x: ex(x[2]))                                   # and Example, others can drop")
        name = lambda h, t: re.sub(r"(<h3 class=fd-h>)[^<]*", r"\g<1>📚 Examples", h, count=1) if ex(t) else h
        results = (assets + "".join(name(results[a:b], t) for a, b, t in keep)) if keep else results
        process = ""
    if step == "3 · Evidence":                  # the Section's own bib, one row per key, where a [key] in the text opens
        results += bib_section(folder, root)    # (r03: no .bib on Evidence or Files)
    # The focused Task uses the common Report frame. Keep its existing editors,
    # prompts and sign actions, with the material being reviewed before its actions.
    return CSS + GROUP_CSS + '<h2>📋 Review Content</h2>' + _numbered(results + process) + JS


def bib_section(folder: Path, root: Path) -> str:
    """📚 Its bib: each entry of the Section's bib (its key, paper, year, DOI), where its text cites it, and each key the
    text cites that the bib lacks; the file one Pop out away."""
    from live.focus_draft_report import bib_entries, paragraphs
    bib = bib_entries(folder)
    text = " ".join(t for _, _, t in paragraphs(folder))
    for d in sorted((folder / "draft").glob("*-draft-v*.md")) if (folder / "draft").is_dir() else []:
        text += " " + d.read_text(encoding="utf-8", errors="ignore")
    cited = list(dict.fromkeys(k.strip() for m in re.finditer(r"\\cite[pt]?\{([^}]*)\}", text) for k in m.group(1).split(",")))
    if not bib and not cited:
        return ""
    from live.frame import reader
    rows = "".join(
        f'<div class=fd-row id="bib-{esc(k)}"><span class=n><code>{esc(k)}</code></span><span class=d>'
        f'{esc(" · ".join(x for x in (e["title"], e["year"], ("DOI " + e["doi"]) if e["doi"] else "no DOI") if x))}</span>'
        f'<span class="w {"fd-ok" if k in cited else ""}">{"cited" if k in cited else "not cited"}</span></div>'
        for k, e in bib.items())
    rows += "".join(f'<div class=fd-row id="bib-{esc(k)}"><span class=n><code>{esc(k)}</code></span><span class=d>no entry in '
                    f'this Section\'s bib</span><span class="w fd-you">not in the bib</span></div>' for k in cited if k not in bib)
    files = sorted({e["file"] for e in bib.values()})
    pop = "".join(f'<p style="margin-top:8px"><a class=fd-btn data-pop="{esc(f.name)}" href="{esc(reader(f, root))}">'
                  f'Open {esc(f.name)}</a></p>' for f in files)
    missing = [k for k in cited if k not in bib]
    return _section("📚 Its bib", rows + pop, f"{len(missing)} not in the bib" if missing else f"{len(bib)} entries",
                    f"🙋 cited, not in the bib: {', '.join(missing)}" if missing else "")


NO_TEXT = "<p class=space-empty>No text yet.</p>"


def _top_sections(html: str) -> list:
    """[(start, end, title)] of the top-level `fd-sec` sections of a step's HTML."""
    out, depth, start = [], 0, 0
    for m in re.finditer(r"<section\b[^>]*>|</section>", html):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                title = re.sub(r"<[^>]+>", "", (re.search(r"<h3 class=fd-h>(.*?)</h3>", html[start:m.end()], re.S) or [None, ""])[1])
                out.append((start, m.end(), title.strip()))
        else:
            if depth == 0:
                start = m.start()
            depth += 1
    return out


def _drop_repeats(step: str, html: str) -> str:
    """A section that repeats the text-and-cards section above it goes (r01): Evidence's Open points (each is already a
    row beside its sentence), Display's one card per display (each is already beside the sentence that calls it)."""
    secs = _top_sections(html)
    if not secs or "The text and its" not in secs[0][2]:
        return html
    if step == "3 · Evidence":
        drop = [x for x in secs[1:] if x[2].startswith("❓ Open points")]
    elif step == "4 · Display":
        drop = [x for x in secs[1:] if re.match(r"(?:e?Figure|e?Table|Display)\b", x[2])]
    else:
        return html
    for start, end, _ in reversed(drop):
        html = html[:start] + html[end:]
    return html


def boxes_of(html: str) -> str:
    return "".join(re.findall(r"<!--pb-prompt-->.*?<!--/pb-prompt-->", html, re.S))


def quiet(boxes: str) -> str:
    """A Prompt box without its session line on the page (r02: "Run this in the Claude session …" in every box); the
    Copy prompt button still copies it (its data-tail)."""
    return re.sub(r"<p class=pb-sess>.*?</p>", "", boxes, flags=re.S)


def input_word(table: str) -> str:
    """The Input table's bar word: none. Each row shows its own value, muted or warned when missing; "N of M missing"
    or "all in place" is a tally (AGENTS § Page words). Kept for its callers."""
    return ""


def work_views(folder: Path, root: Path) -> tuple:
    """({key: (name, html builder)}, {key: (word, class)}, the step a bare link opens): Work's view-button-list."""
    f, st, k = _facts(folder, root)
    # a view with nothing in it does not show (haipipe-ui; JL 261031): no Display when no display is called or made
    steps = [(key, step) for key, step in WORK if key != "display" or f["displays"]]
    # Draft first, and a bare link opens it (JL 261113: Plan, Evidence and Display are made at the Board and the Job;
    # the draft is the Section's own work). The steps keep their keys; the buttons are numbered in this order.
    steps = sorted(steps, key=lambda kv: kv[0] != "draft")
    views = {key: (f"{n} · {step.split(' · ', 1)[-1]}", (lambda s=step: step_html(folder, root, s)))
             for n, (key, step) in enumerate(steps, 1)}
    words = {key: word(st[step], k) for key, step in steps}
    return views, words, "draft"
