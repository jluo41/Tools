#!/usr/bin/env python3
"""A collection Run: a person's answers to a few questions, asked in Markdown and picked in a form (haipipe-interaction,
its first kind of interaction: request and record the human input a page's work needs; renamed from haipipe-collect).

    python collect.py new   <page> <slug> --title T --for F [--person P] [--feeds a,b]
                                            runs/rNN_collect_<slug>/ under the page: run.yaml, question_collection.md
    python collect.py check <run>           the questions' problems, one per line; nothing written
    python collect.py build <run>           question_collection.md rendered into the form rNN_collect_<slug>.html
    python collect.py save  <run> [file]    the pasted picks (a file, or stdin) into result/answer_collection.md
    python collect.py close <run>           finish a save that stopped halfway (its answers stay as they are)
    python collect.py applied <run> Q1 [Q2 ...] --by "..." [--state "in progress"]
                                            what applied each answer, in applied.md: its flag on the form

JL 261031: "so it will be a run of collection"; "it will just be the rNN under that page"; "in that run, you generate
a question_collection.md in that run folder, and this could be rendered into the html and we can make the selection
on it"; "for each question you asked, try to make it as compact as possible". The Markdown is the source a person
can read anywhere; the form is generated from it; the answers come back as the same Markdown with the person's
picks ticked and their notes added.

question_collection.md, one card per question:

    # Report and Delivery
    for: b17-s04:theme_work @ workbench_page_structure
    One line of intro (optional).

    ## Q1 · Report or Delivery
    One short why.
    ```text
    an optional sketch (or one picture: ![caption](file.png))
    ```
    **Where does a delivery show?**
    - [x] A · In the Report; Delivery leaves the right rail.
    - [ ] B · In both.
    Why A: One thing in one place.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "project" / "haipipe-run" / "scripts"))
from soft_run import read_card, space_root, write_card  # noqa: E402  the one Run card, written the one way

QUESTIONS = "question_collection.md"
ANSWERS = "result/answer_collection.md"
# what the answers changed, one line per question, written by whoever applied them, beside run.yaml and never in
# result/, so the Result stays closed (JL 261031: "if we already fix them, then give them the flags")
APPLIED = "applied.md"
APPLIED_STATES = ("applied", "in progress")
APPLIED_LINE = re.compile(r"^(Q\d+) · (applied|in progress) · (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) · (.+?)\s*$")
RUN_NAME = re.compile(r"^r(\d{2,})_collect_[a-z0-9]+(?:_[a-z0-9]+)*$")
SLUG = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
LIMITS = {                      # the compact card (JL 261031)
    # one theme's questions in one set, not many short sets (JL 261031): up to 20 questions
    "questions": 20, "options": 4, "intro": 30, "why": 40, "ask": 12, "option": 14, "because": 16, "sketch": 6,
}
QHEAD = re.compile(r"^##\s+(Q\d+)\s*[·:-]\s*(.+?)\s*$")
OPTION = re.compile(r"^-\s*\[( |x|X)\]\s*([A-Z])\s*[·:.)-]\s*(.+?)\s*$")
ASK = re.compile(r"^\*\*(.+?)\*\*$")
WHY_PICK = re.compile(r"^Why\s+([A-Z]):\s*(.+)$")
FOR = re.compile(r"^for:\s*(.+)$")
IMAGE = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)$")
# an option's own preview, the line under it: a live page [preview](option-a.html) or a picture ![A](option-a.png)
# (JL 261031: "for the UI, you have differen options, you can also make the option's preview results, liek the hmtl
# to be embeded here")
PREVIEW = re.compile(r"^\[preview\]\(([^)\s]+\.html?)\)$")
# The copied text's first line names its Run; a form built before the rename (JL 261031) wrote the old words.
HEADS = ("haipipe-interaction answers", "haipipe-collect feedback")
# QN · title: K · option text[ (changed from M)], or QN · title: (no option picked)
PASTE_PICK = re.compile(r"^(Q\d+) · (.*?): (?:([A-Z]) · (.*?)(?: \(changed from [A-Z]\))?|\(no option picked\)|(my own decision))\s*$")
OWN = "own"        # every question's last choice, the person's own decision; its words are the note (JL 261031: "like I
                   # will add my decisions")
PASTE_NOTE = re.compile(r"^\s*note:\s?(.*)$")             # any indent: a note that lost its spaces still counts


class SpecError(Exception):
    """Questions that cannot be read, said in one line."""


def words(text) -> int:
    return len(str(text or "").split())


def run_folder(path: Path) -> Path:
    """The Run folder from a path to it or to a file in it."""
    path = path.resolve()
    return path.parent if path.is_file() else path


# ── question_collection.md ⇄ the questions ──────────────────────────────────────────────────────
def parse(text: str, name: str = QUESTIONS) -> dict:
    """The questions from their Markdown: title, for, intro, and one card per `## QN · title`."""
    spec = {"title": "", "for": "", "intro": "", "questions": [], "stray": []}
    q, fence, comment, intro = None, None, False, []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if comment:                                          # an <!-- note to the writer --> is never content
            comment = "-->" not in line
            continue
        if fence is not None:
            if line.startswith("```"):
                if q is not None:
                    q.setdefault("show", []).append({"sketch": "\n".join(fence)})
                fence = None
            else:
                fence.append(raw.rstrip())
            continue
        if line.startswith("<!--"):
            comment = "-->" not in line
            continue
        if line.startswith("```"):
            fence = []
            continue
        if not line:
            continue
        if line.startswith("# ") and not spec["title"] and q is None:
            spec["title"] = line[2:].strip()
            continue
        m = QHEAD.match(line)
        if m:
            q = {"id": m.group(1), "title": m.group(2), "why": "", "ask": "", "options": [], "line": n}
            spec["questions"].append(q)
            continue
        if q is None:
            m = FOR.match(line)
            if m:
                spec["for"] = m.group(1).strip()
            else:
                intro.append(line)
            continue
        m = OPTION.match(line)
        if m:
            q["options"].append({"key": m.group(2), "text": m.group(3), **({"pick": True} if m.group(1) in "xX" else {})})
            continue
        m = PREVIEW.match(line) or (IMAGE.match(line) if q["options"] and not q.get("because") else None)
        if m and q["options"] and raw[:1].isspace():                 # indented under its option: that option's preview
            q["options"][-1]["preview"] = m.group(m.lastindex)
            continue
        m = WHY_PICK.match(line)
        if m and q["options"]:
            q["because"], q["because_key"] = m.group(2).strip(), m.group(1)
            continue
        m = ASK.match(line)
        if m and not q["options"]:
            q["ask"] = m.group(1).strip()
            continue
        m = IMAGE.match(line)
        if m and not q["ask"]:
            q.setdefault("show", []).append({"image": m.group(2), "caption": m.group(1)})
            continue
        if not q["ask"] and not q["options"]:
            q["why"] = f'{q["why"]} {line}'.strip()
        else:
            spec["stray"].append(f"{q['id']}: line {n} is not part of its card")
    if fence is not None:
        raise SpecError(f"{name}: a ``` block is never closed")
    spec["intro"] = " ".join(intro)
    return spec


def markdown(spec: dict, answers: dict | None = None) -> str:
    """The questions back as Markdown; with answers, the person's picks ticked and their notes added."""
    out = [f"# {spec['title']}" + (" · answers" if answers is not None else ""), ""]
    if spec.get("for"):
        out += [f"for: {spec['for']}", ""]
    if spec.get("intro"):
        out += [spec["intro"], ""]
    for q in spec["questions"]:
        out += [f"## {q['id']} · {q['title']}", "", q["why"], ""]
        for item in q.get("show") or []:
            out += (["```text", item["sketch"].rstrip(), "```", ""] if "sketch" in item
                    else [f"![{item.get('caption', '')}]({item['image']})", ""])
        mine = next((o["key"] for o in q["options"] if o.get("pick")), "")
        given = (answers or {}).get(q["id"], {})
        ticked = given.get("pick", "") if answers is not None else mine
        out += [f"**{q['ask']}**", ""]
        for o in q["options"]:
            out.append(f"- [{'x' if o['key'] == ticked else ' '}] {o['key']} · {o['text']}")
            if o.get("preview"):
                out.append(f"  [preview]({o['preview']})" if o["preview"].endswith((".html", ".htm"))
                           else f"  ![{o['key']}]({o['preview']})")
        out += [""]
        if mine and q.get("because"):
            out += [f"Why {mine}: {q['because']}", ""]
        if answers is not None:
            if ticked == OWN:                          # the person's own decision, in their words
                out += ["Answer: my own decision.", "", "> decision: " + given.get("note", "").replace("\n", "\n> "), ""]
                continue
            if not ticked:
                said = "Answer: none picked."
            elif not mine:                             # nothing was preselected: no "changed from my pick" (b15 261101)
                said = f"Answer: {ticked}."
            else:
                said = f"Answer: {ticked}, " + ("my pick." if ticked == mine else f"changed from my pick {mine}.")
            out += [said + (" Where the note below says otherwise, the note wins." if given.get("note") else ""), ""]
            if given.get("note"):
                out += ["> note: " + given["note"].replace("\n", "\n> "), ""]
    return "\n".join(out).rstrip() + "\n"


# the Studio topic an interaction is attached to (JL 261031: "the interaction page should be attached to one studio as
# well"): the sNN at the head of its for: address, b17-s04 or b16.j01.t03-s38
# a Block's bNN, or a paper Board's own folder name, which has no bNN (Paper-X-s04, Paper-X.j11-s05)
TOPIC = re.compile(r"\s*((?:b\d+|Paper-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*?)(?:\.[jt]\d+)*-s\d+)\b")
EXAMPLE_FOR = "b17-s04:theme_work @ workbench_page_structure"


def topic_of(about: str) -> str:
    m = TOPIC.match(about or "")
    return m.group(1) if m else ""


def problems(spec: dict, run: Path) -> list[str]:
    """What is wrong with a Run's questions, one line each; empty when it builds."""
    out = list(spec.get("stray") or [])
    if not RUN_NAME.match(run.name):
        out.append(f"{run.name}: a collection Run is named rNN_collect_<slug>")
    title = spec.get("title", "")
    if not title:
        out.append("title: missing (the first # line)")
    elif not 2 <= words(title) <= 4:
        out.append("title: two to four words")
    if not topic_of(spec.get("for", "")):
        out.append(f"for: names no Studio topic; an interaction is attached to one sNN (for: {EXAMPLE_FOR})")
    if words(spec.get("intro")) > LIMITS["intro"]:
        out.append(f"intro: at most {LIMITS['intro']} words")
    questions = spec.get("questions") or []
    if not questions:
        return out + ["questions: at least one (## Q1 · title)"]
    if len(questions) > LIMITS["questions"]:
        out.append(f"questions: at most {LIMITS['questions']} per Run; the rest go in the next Run")
    seen = set()
    for q in questions:
        where = q["id"]
        if where in seen:
            out.append(f"{where}: used twice")
        seen.add(where)
        if not 1 <= words(q["title"]) <= 3:
            out.append(f"{where}: title, one to three words")
        if not q["why"]:
            out.append(f"{where}: why missing (a short paragraph under the ## line)")
        elif words(q["why"]) > LIMITS["why"]:
            out.append(f"{where}: why has {words(q['why'])} words; at most {LIMITS['why']}")
        if not q["ask"]:
            out.append(f"{where}: the question is missing (**…?** before the options)")
        else:
            if not q["ask"].endswith("?"):
                out.append(f"{where}: the question ends with ?")
            if words(q["ask"]) > LIMITS["ask"]:
                out.append(f"{where}: the question, at most {LIMITS['ask']} words")
        options = q["options"]
        if not 2 <= len(options) <= LIMITS["options"]:
            out.append(f"{where}: options, two to {LIMITS['options']} (- [ ] A · text)")
        keys = [o["key"] for o in options]
        if len(set(keys)) != len(keys):
            out.append(f"{where}: every option needs its own key")
        for o in options:
            if words(o["text"]) > LIMITS["option"]:
                out.append(f"{where}: option {o['key']} has {words(o['text'])} words; at most {LIMITS['option']}")
        picks = [o["key"] for o in options if o.get("pick")]
        if len(picks) > 1:
            out.append(f"{where}: tick at most one option, my pick")
        if picks and not q.get("because"):
            out.append(f"{where}: Why {picks[0]}: missing, one line on why my pick wins")
        if picks and q.get("because_key") and q["because_key"] != picks[0]:
            out.append(f"{where}: Why {q['because_key']} names another option than my pick {picks[0]}")
        if words(q.get("because")) > LIMITS["because"]:
            out.append(f"{where}: Why, at most {LIMITS['because']} words")
        shows = q.get("show") or []
        if len(shows) > 1:
            out.append(f"{where}: at most one detail, a sketch or a picture")
        for o in q["options"]:
            if o.get("preview") and not (run / o["preview"]).is_file():
                out.append(f"{where}: option {o['key']}'s preview not found: {o['preview']}")
        for item in shows:
            if "image" in item and not (run / item["image"]).is_file():
                out.append(f"{where}: picture not found: {item['image']}")
            if "sketch" in item and len(item["sketch"].rstrip().splitlines()) > LIMITS["sketch"]:
                out.append(f"{where}: sketch, at most {LIMITS['sketch']} lines")
    return out


def load(run: Path) -> dict:
    source = run / QUESTIONS
    if not source.is_file():
        raise SpecError(f"{run.name}: no {QUESTIONS}")
    return parse(source.read_text(encoding="utf-8"), f"{run.name}/{QUESTIONS}")


# ── the form ────────────────────────────────────────────────────────────────────────────────────
def inline(text: str) -> str:
    """Escape, then `code` and **bold**."""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)


def show_html(item: dict) -> str:
    """The one detail: a text sketch as is, or a picture (a path relative to the Run folder)."""
    if "sketch" in item:
        return f'<pre class="sketch">{html.escape(item["sketch"].rstrip())}</pre>'
    return f'<img class="pic" src="{html.escape(item["image"])}" alt="{html.escape(item.get("caption", ""))}">'


def preview_html(qid: str, o: dict) -> str:
    """One option's preview, side by side with the others: the live page (or picture) at half size; a click picks the
    option, Open shows it full size in a new tab."""
    key, src = html.escape(o["key"]), html.escape(o["preview"])
    pick = (f"var r=document.querySelector('input[name=\\'{qid}\\'][value=\\'{key}\\']');"
            "r.checked=true;r.dispatchEvent(new Event('change',{bubbles:true}))")
    body = (f'<iframe src="{src}" title="option {key}" tabindex="-1"></iframe>'
            if src.endswith((".html", ".htm")) else f'<img src="{src}" alt="option {key}">')
    return (f'<figure class="pv" data-q="{qid}" data-key="{key}"><figcaption><b>{key}</b>'
            f'<a href="{src}" target="_blank" rel="noopener">Open ↗</a></figcaption>'
            f'<div class="pv-frame" onclick="{pick}">{body}<span class="pv-hit"></span></div></figure>')


def card(q: dict) -> str:
    qid = html.escape(q["id"])
    options = []
    for o in q["options"]:
        key = html.escape(o["key"])
        checked = " checked" if o.get("pick") else ""
        rec = '<span class="rec">my pick</span>' if o.get("pick") else ""
        options.append(f'<label class="opt"><input type="radio" name="{qid}" value="{key}"{checked}>'
                       f'<span><b>{key}</b> {inline(o["text"])}{rec}</span></label>')
    options.append(f'<label class="opt own"><input type="radio" name="{qid}" value="{OWN}">'
                   '<span><b>✍</b> My own decision</span></label>')   # its words go in the note, then required
    pick = next((o for o in q["options"] if o.get("pick")), None)
    because = (f'<p class="because">Why {html.escape(pick["key"])}: {inline(q["because"])}</p>'
               if pick and q.get("because") else "")
    shown = [o for o in q["options"] if o.get("preview")]
    previews = ('<div class="previews">' + "".join(preview_html(qid, o) for o in shown) + "</div>") if shown else ""
    return (f'<section class="card" id="{qid}"><h2><span class="qid">{qid}</span>{inline(q["title"])}'
            f'<span class="state" id="state-{qid}"></span><span class="applied" id="applied-{qid}"></span></h2>'
            f'<p class="applied-by" id="applied-by-{qid}" hidden></p>'
            f'<p class="why">{inline(q["why"])}</p>{"".join(show_html(i) for i in q.get("show") or [])}'
            f'<fieldset><legend class="ask">{inline(q["ask"])}</legend>{"".join(options)}</fieldset>'
            f'{previews}{because}<textarea class="note" id="note-{qid}" rows="1" placeholder="Note (optional)"></textarea>'
            "</section>")


CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--mut:#6f6f6b;--faint:#9aa0a6;--line:#e3e3e6;--on:#1864ab;--wash:#e7f5ff;--soft:#f6f6f7;--prop:#b35c00;--ok:#2b8a3e;--red:#c92a2a}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161719;--fg:#e8e8e6;--mut:#a0a09c;--faint:#7c828a;--line:#2c2e33;--on:#91caff;--wash:#253749;--soft:#1d1f22;--prop:#e4bd62;--ok:#8ce99a;--red:#ff8787}}
:root[data-theme="dark"]{--bg:#161719;--fg:#e8e8e6;--mut:#a0a09c;--faint:#7c828a;--line:#2c2e33;--on:#91caff;--wash:#253749;--soft:#1d1f22;--prop:#e4bd62;--ok:#8ce99a;--red:#ff8787}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14.5px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:var(--on)}
code{font:12.5px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--soft);border-radius:4px;padding:0 4px}
.wrap{max-width:760px;margin:0 auto;padding:20px 16px 24px}
.wrap:has(.previews){max-width:1180px}
.previews{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin:8px 0}
.pv{margin:0;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.pv figcaption{display:flex;justify-content:space-between;padding:4px 10px;font-size:12.5px;border-bottom:1px solid var(--line)}
.pv-frame{position:relative;height:300px;overflow:hidden;cursor:pointer;background:#fff}
.pv-frame iframe{width:200%;height:200%;border:0;transform:scale(.5);transform-origin:0 0;pointer-events:none}
.pv-frame img{width:100%;display:block}
.pv-hit{position:absolute;inset:0}
.pv.on{border-color:var(--on);box-shadow:0 0 0 2px var(--wash)}
.label{font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--red);margin:0 0 4px;font-weight:600;overflow-wrap:anywhere}
h1{font-size:22px;margin:0 0 4px}
.lead{color:var(--mut);margin:0 0 16px}
.card{border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:0 0 12px}
.card h2{font-size:16px;margin:0 0 4px;display:flex;gap:8px;align-items:baseline}
.card h2 .qid{color:var(--on)}
.card h2 .state{margin-left:auto;font-size:12px;color:var(--prop);font-weight:600}
.card h2 .applied{font-size:12px;color:var(--ok);font-weight:600;white-space:nowrap}
.card h2 .applied.wip{color:var(--prop)}
.applied-by{margin:0 0 6px;font-size:12.5px;color:var(--ok)}
.why{margin:0 0 8px;color:var(--mut)}
pre.sketch{background:var(--soft);border-radius:8px;padding:8px 10px;overflow-x:auto;font:12px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;margin:0 0 8px}
img.pic{max-width:100%;max-height:220px;border:1px solid var(--line);border-radius:8px;margin:0 0 8px}
fieldset{border:0;margin:0;padding:0}
.ask{font-weight:600;padding:0;margin:0 0 6px}
.opt{display:flex;gap:8px;align-items:baseline;padding:5px 10px;border:1px solid var(--line);border-radius:8px;margin:0 0 4px;cursor:pointer}
.opt:has(input:checked){border-color:var(--on);background:var(--wash)}
.opt .rec{font-size:11px;color:var(--ok);border:1px solid var(--ok);border-radius:6px;padding:0 5px;margin-left:8px;white-space:nowrap}
.because{font-size:13px;color:var(--mut);margin:4px 0 6px}
textarea{width:100%;font:inherit;font-size:13.5px;padding:5px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg);resize:vertical}
textarea.note{min-height:32px;field-sizing:content}
#out{min-height:120px;font:12px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--soft)}
.send{position:sticky;bottom:0;background:var(--bg);border-top:1px solid var(--line);padding:8px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;justify-content:center}
button{font:inherit;font-size:14px;border:1px solid var(--on);background:var(--on);color:var(--bg);border-radius:8px;padding:6px 16px;cursor:pointer}
button.quiet{background:transparent;color:var(--on)}
#copied{font-size:13px;color:var(--ok)}
details.box{margin:4px 0 0;color:var(--mut);font-size:13px}
"""

JS = r"""
(function(){
  var FORM = JSON.parse(document.getElementById('form-data').textContent);
  var KEY = 'haipipe-interaction:' + location.pathname, OLD = 'haipipe-collect:' + location.pathname;   // OLD: answers kept before the rename
  function load(){ try { return JSON.parse(localStorage.getItem(KEY) || localStorage.getItem(OLD) || '{}'); } catch (e) { return {}; } }
  var ANS = FORM.answered;                       /* answered: the person's own picks, read only */
  function save(s){ if (ANS) return; try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }
  function picked(q){ var c = document.querySelector('input[name="' + q.id + '"]:checked'); return c ? c.value : ''; }
  function note(q){ return document.getElementById('note-' + q.id).value; }
  function option(q, key){ for (var i = 0; i < q.options.length; i++) { if (q.options[i].key === key) return q.options[i]; } return null; }
  function stamp(){
    var d = new Date(); function p(n){ return (n < 10 ? '0' : '') + n; }
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
  }
  function text(){
    var out = ['haipipe-interaction answers · ' + FORM.run + ' · ' + FORM.title + ' · ' + stamp(),
               'form: ' + decodeURIComponent(location.pathname)];
    if (FORM.built) out.push('built: ' + FORM.built);          // which build of the form these picks were made on
    FORM.questions.forEach(function(q){
      var key = picked(q), o = option(q, key), line = q.id + ' · ' + q.title + ': ';
      line += key === 'own' ? 'my own decision' : o ? key + ' · ' + o.text : '(no option picked)';
      if (o && q.pick && key !== q.pick) line += ' (changed from ' + q.pick + ')';
      out.push(line);
      var n = note(q).trim();
      if (n) out.push('   note: ' + n.split('\n').join('\n         '));
    });
    return out.join('\n') + '\n';
  }
  function refresh(){
    var s = {};
    FORM.questions.forEach(function(q){
      var o = option(q, picked(q)); s[q.id] = {pick: picked(q), text: o ? o.text : '', note: note(q)};
      var words = [];
      if (q.pick && s[q.id].pick && s[q.id].pick !== q.pick) words.push(s[q.id].pick === 'own' ? 'my decision' : 'changed');
      var box = document.getElementById('note-' + q.id);
      box.placeholder = s[q.id].pick === 'own' ? 'Your decision (required)' : 'Note (optional)';
      if (s[q.id].note.trim()) words.push('note');
      document.getElementById('state-' + q.id).textContent = words.join(' · ');
    });
    save(s);
    document.getElementById('out').value = text();
    document.getElementById('copied').textContent = '';
  }
  function restore(){
    if (ANS) {
      FORM.questions.forEach(function(q){
        var a = ANS.picks[q.id] || {};
        document.querySelectorAll('input[name="' + q.id + '"]').forEach(function(r){ r.checked = r.value === a.pick; r.disabled = true; });
        var n = document.getElementById('note-' + q.id); n.value = a.note || ''; n.readOnly = true;
      });
      document.querySelector('.send').style.display = 'none';
      return;
    }
    var s = load();
    FORM.questions.forEach(function(q){
      var a = s[q.id]; if (!a) return;
      var key = a.text ? (q.options.filter(function(o){ return o.text === a.text; })[0] || {}).key : a.pick;   // by its text
      var r = key && document.querySelector('input[name="' + q.id + '"][value="' + key + '"]');
      if (r) r.checked = true;
      if (a.note) document.getElementById('note-' + q.id).value = a.note;
    });
  }
  function done(ok){ document.getElementById('copied').textContent = ok ? 'Copied: paste it into the chat' : 'Open the text below, select it and copy'; }
  window.haipipeAnswers = text;      /* the combined page reads every form's answer through this (bundle) */
  function copy(){
    var box = document.getElementById('out'); box.value = text();
    function fallback(){ box.closest('details').open = true; box.focus(); box.select(); var ok = false; try { ok = document.execCommand('copy'); } catch (e) {} done(ok); }
    if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(box.value).then(function(){ done(true); }, fallback); }
    else { fallback(); }
  }
  function reset(){
    try { localStorage.removeItem(KEY); localStorage.removeItem(OLD); } catch (e) {}
    FORM.questions.forEach(function(q){
      document.querySelectorAll('input[name="' + q.id + '"]').forEach(function(r){ r.checked = r.value === q.pick; });
      document.getElementById('note-' + q.id).value = '';
    });
    refresh();
  }
  restore(); refresh();
  document.addEventListener('change', refresh);
  /* the chosen option's preview is outlined, as its radio is */
  function lightPreviews(){document.querySelectorAll('.pv').forEach(function(f){
    var r=document.querySelector('input[name="'+f.dataset.q+'"][value="'+f.dataset.key+'"]');f.classList.toggle('on',!!(r&&r.checked));});}
  document.addEventListener('change', lightPreviews); lightPreviews();
  /* the part that differs between a question's previews gets a box (JL 261031: "highlight the part that are different
     by using the box"): a preview's own class="diff" marks it; otherwise the pages are compared, node by node, and the
     smallest block that differs is boxed in every option; each preview then scrolls to its first box */
  var DIFF_CSS = '.ix-diff{outline:5px solid #e8590c!important;outline-offset:4px;border-radius:4px}';
  function own(n){ return Array.prototype.filter.call(n.childNodes, function(c){ return c.nodeType === 3; })
    .map(function(c){ return c.textContent.trim(); }).join('|'); }
  function box(ns){ ns.forEach(function(n){ n.classList.add('ix-diff'); }); }
  function kidsOf(n){ return Array.prototype.filter.call(n.children, function(c){ return !/^(STYLE|SCRIPT)$/.test(c.tagName); }); }
  function lcs(x, y){                    /* which children are the same in both pages, kept in order */
    var m = x.length, n = y.length, L = [];
    for (var i = 0; i <= m; i++) { L.push(new Array(n + 1).fill(0)); }
    for (i = m - 1; i >= 0; i--) for (var j = n - 1; j >= 0; j--)
      L[i][j] = x[i].outerHTML === y[j].outerHTML ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1]);
    var keepX = [], keepY = []; i = 0; j = 0;
    while (i < m && j < n) { if (x[i].outerHTML === y[j].outerHTML) { keepX[i] = keepY[j] = true; i++; j++; }
      else if (L[i + 1][j] >= L[i][j + 1]) i++; else j++; }
    return [x.filter(function(_, k){ return !keepX[k]; }), y.filter(function(_, k){ return !keepY[k]; })];
  }
  function walk(a, b){                   /* two pages' nodes: box what one has and the other has not */
    if (a.outerHTML === b.outerHTML) return;
    var root = /^(BODY|MAIN)$/.test(a.tagName);
    if (!root && (own(a) !== own(b) || a.className !== b.className)) { box([a, b]); return; }
    var d = lcs(kidsOf(a), kidsOf(b)), x = d[0], y = d[1];
    if (!x.length && !y.length) { if (!root) box([a, b]); return; }
    var paired = x.length === y.length && x.every(function(c, i){ return c.tagName === y[i].tagName; });
    if (!paired) { box(x.concat(y)); return; }
    if (!root && x.length > 2) { box([a, b]); return; }
    x.forEach(function(c, i){ if (c.outerHTML === y[i].outerHTML) box([c, y[i]]); else walk(c, y[i]); });   /* the same block, moved */
  }
  function diffQuestion(q){
    var frames = Array.prototype.slice.call(document.querySelectorAll('.pv[data-q="' + q + '"] iframe'));
    var docs = frames.map(function(f){ try { return f.contentDocument; } catch (e) { return null; } });
    if (frames.length < 2 || docs.some(function(d){ return !d || d.readyState !== 'complete' || !d.body ||
        d.URL === 'about:blank'; })) return;   /* every page loaded, not the blank one an iframe starts with */
    if (docs.some(function(d){ return d.documentElement.dataset.ixDiffed; })) return;
    docs.forEach(function(d){ d.documentElement.dataset.ixDiffed = '1'; });
    docs.forEach(function(d){ var s = d.createElement('style'); s.textContent = DIFF_CSS; d.head.appendChild(s); });
    var marked = docs.some(function(d){ return d.querySelector('.diff'); });
    if (marked) docs.forEach(function(d){ box(Array.prototype.slice.call(d.querySelectorAll('.diff'))); });
    else {                             /* the page itself, never what a browser add-on puts in the body */
      var top = function(d){ return d.querySelector('main') || d.body; };
      docs.slice(1).forEach(function(d){ walk(top(docs[0]), top(d)); });
    }
    docs.forEach(function(d){ var first = d.querySelector('.ix-diff'); if (!first) return;
      var y = first.getBoundingClientRect().top + d.defaultView.scrollY;
      if (y > 420) d.defaultView.scrollTo(0, y - 80); });
  }
  document.querySelectorAll('.pv iframe').forEach(function(f){
    var q = f.closest('.pv').dataset.q;
    f.addEventListener('load', function(){ diffQuestion(q); });
    if (f.contentDocument && f.contentDocument.readyState === 'complete') diffQuestion(q);
  });
  /* a question already applied carries its flag (JL 261031: "if we already fix them, then give them the flags"):
     applied.md beside the form, written by collect.py applied, read each time the form opens */
  if (window.fetch) fetch('applied.md', {cache: 'no-store'}).then(function(r){ return r.ok ? r.text() : ''; })
    .then(function(text){ text.split('\n').forEach(function(line){
      var m = /^(Q\d+) · (applied|in progress) · (\d{4}-\d{2}-\d{2}) \d{2}:\d{2} · (.+?)\s*$/.exec(line);
      var flag = m && document.getElementById('applied-' + m[1]), by = m && document.getElementById('applied-by-' + m[1]);
      if (!flag) return;
      flag.textContent = (m[2] === 'applied' ? '✅ applied ' : '⏳ in progress ') + m[3];
      flag.classList.toggle('wip', m[2] !== 'applied');
      by.textContent = (m[2] === 'applied' ? 'Applied: ' : 'In progress: ') + m[4]; by.hidden = false;
    }); }).catch(function(){});
  document.addEventListener('input', function(e){ if (e.target.classList.contains('note')) refresh(); });
  document.querySelectorAll('[data-copy]').forEach(function(b){ b.addEventListener('click', copy); });
  document.getElementById('reset').addEventListener('click', reset);
})();
"""


def lead_words(data: dict) -> str:
    if data.get("answered"):
        return (f'Answered {html.escape(data["answered"]["received"])}: your picks and notes are shown, read only; a flag '
                f'on a question says whether it is applied or in progress. The answers: <a href="{ANSWERS}">{ANSWERS}</a>.')
    if not any(q.get("pick") for q in data.get("questions") or []):     # a labeling report: options never preselected
        return "Nothing is picked for you: choose one option per question, or ✍ My own decision, then Copy feedback and paste it to me."
    return "My pick is selected; change any, then Copy feedback and paste it to me."


def page(spec: dict, run: Path, built: str = "") -> str:
    """The form, rendered from the questions; `built` is its build stamp (a time, never a hash), which the copied text
    repeats so `save` can tell a paste from an older build of the form."""
    data = {"run": run.name, "title": spec["title"], "built": built,
            "questions": [{"id": q["id"], "title": q["title"],
                           "pick": next((o["key"] for o in q["options"] if o.get("pick")), ""),
                           "options": [{"key": o["key"], "text": o["text"]} for o in q["options"]]}
                          for q in spec["questions"]]}
    answered = run / ANSWERS                          # an answered form shows the person's own picks and notes, read
    if answered.is_file():                            # only, from the paste its answer file keeps (JL 261031)
        text = answered.read_text(encoding="utf-8")
        kept_paste = KEPT_PASTE.search(text.replace("\r\n", "\n"))
        got = picks(kept_paste.group(1))[0] if kept_paste else {}
        when = re.search(r"(?m)^received:\s*(.+?)\s*$", text)
        data["answered"] = {"received": when.group(1) if when else "",
                            "picks": {q: {"pick": a["pick"], "note": a["note"]} for q, a in got.items()}}
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    label = "Questions for you · " + html.escape(run.name) + (f' · {html.escape(spec["for"])}' if spec.get("for") else "")
    intro = inline(spec.get("intro", ""))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="haipipe-built" content="{html.escape(built)}">
<title>{html.escape(spec["title"])}</title>
<!-- GENERATED FILE by haipipe-interaction scripts/collect.py from this Run's {QUESTIONS}: change the questions there
     and build again, never this page. -->
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<p class="label">{label}</p>
<h1>{html.escape(spec["title"])}</h1>
<p class="lead">{intro + " " if intro else ""}{lead_words(data)}
The questions as Markdown: <a href="{QUESTIONS}">{QUESTIONS}</a>.</p>
{"".join(card(q) for q in spec["questions"])}
<details class="box"><summary>The text Copy feedback sends</summary><textarea id="out" readonly></textarea></details>
</div>
<div class="send"><button type="button" data-copy>Copy feedback</button><button type="button" class="quiet" id="reset">Back to my picks</button><span id="copied"></span></div>
<script type="application/json" id="form-data">{payload}</script>
<script type="text/markdown" id="haipipe-questions">{markdown(spec).replace("</", "<\\/")}</script>
<script>{JS}</script>
</body>
</html>
"""


# ── the Run ─────────────────────────────────────────────────────────────────────────────────────
def where(path: Path) -> str:
    """A SPACE-relative path for the card, never an absolute one: from the SPACE (env.sh), else its git root."""
    path = path.resolve()
    root = space_root(path) or next((p for p in [path, *path.parents] if (p / ".git").exists()), None)
    return path.relative_to(root).as_posix() if root else path.name


def new(page_dir: Path, slug: str, title: str, for_: str = "", person: str = "", feeds: list[str] | None = None) -> Path:
    """Allocate the next rNN under the page; write its card and the start of question_collection.md."""
    if not page_dir.is_dir():
        raise SystemExit(f"{page_dir}: no such folder")
    if not SLUG.match(slug):
        raise SystemExit(f"slug {slug!r}: lower-case words joined by _")
    runs = page_dir / "runs"
    here = [p.name for p in runs.iterdir()] if runs.is_dir() else []
    if any(name.endswith(f"_collect_{slug}") for name in here):
        raise SystemExit(f"a collection Run for {slug!r} is already under {page_dir.resolve().name}: a new round is a new slug")
    # every interaction is attached to one Studio topic, its sNN (JL 261031), whose card shows it
    if not topic_of(for_):
        raise SystemExit(f"--for {for_!r}: an interaction is attached to one Studio topic; name its sNN, as "
                         f"--for '{EXAMPLE_FOR}' (no topic fits: start one first, haipipe-studio)")
    # one waiting Run per sNN its for: names (JL 261031: a button on each Studio row, "it will pop out and I can do
    # the selection here"), so answers never cross; an older Run that names none still holds its page
    waiting = [name for name in here if "_collect_" in name and (runs / name / "run.yaml").is_file()
               and read_card(runs / name).get("status") == "waiting"
               and topic_of(read_card(runs / name).get("target", "")) in ("", topic_of(for_))]
    if waiting:
        raise SystemExit(f"{page_dir.resolve().name} already waits on {waiting[0]} for the same sNN: one waiting collection Run "
                         "per sNN, so answers never cross; add the question there, or ask when it comes back")
    nums = [int(m.group(1)) for name in here for m in [re.match(r"^r(\d+)_", name)] if m]
    run = runs / f"r{(max(nums) + 1 if nums else 1):02d}_collect_{slug}"
    run.mkdir(parents=True)
    write_card(run, {"run": run.name, "kind": "hard", "type": "collect", "scope": where(page_dir), "target": for_ or title,
                     "ticket": f"{run.name}.html", "skill": "haipipe-interaction", "agent": person or None, "signs": None,
                     "status": "planned", "passes": [], "writes": [ANSWERS], "feeds": feeds or []})
    (run / QUESTIONS).write_text(
        f"# {title}\n\n" + (f"for: {for_}\n\n" if for_ else "")
        + "<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),\n"
          "     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.\n"
          "     collect.py check holds the limits; collect.py build renders the form. -->\n",
        encoding="utf-8")
    return run


def build(run: Path) -> Path:
    try:
        spec = load(run)
    except SpecError as err:
        raise SystemExit(str(err))
    found = problems(spec, run)
    if found:
        raise SystemExit("\n".join(f"{run.name}: {p}" for p in found))
    ticket = run / f"{run.name}.html"
    before = ticket.read_text(encoding="utf-8") if ticket.is_file() else ""
    # the same questions keep the same stamp, whatever the template (b17 261031): a tab already open still copies a
    # stamp save accepts, and only a changed question makes earlier copies stale
    kept = QUESTIONS_IN_FORM.search(before) if before else None
    same = bool(before) and ((kept.group(1).replace("<\\/", "</") == markdown(spec)) if kept else
                             (card_words(before) == card_words(page(spec, run, form_built(before)))))
    if (run / ANSWERS).exists() and not same:          # its Result is closed: so are its questions (tester k6d, k6e)
        raise SystemExit(f"{run.name}: answered, so its questions stay as they were answered; a changed question "
                         "is a new Run (collect.py new)")
    fresh = page(spec, run, form_built(before) if same else datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    if fresh != before:                                # a new template (its applied flags) or new questions
        ticket.write_text(fresh, encoding="utf-8")
    if (run / ANSWERS).exists():
        return ticket                                  # answered: the card stays done
    card_ = read_card(run)
    if card_.get("status") in (None, "planned"):
        card_["status"] = "waiting"                  # the form exists: it waits on its person
        write_card(run, card_)
    return ticket


def applied(run: Path, qids: list[str], by: str, state: str = "applied", now: datetime | None = None) -> Path:
    """Record that answers were applied: one line per question in applied.md, replacing that question's earlier line.
    Only an answered Run, only its own questions; the time from the clock."""
    if not (run / ANSWERS).is_file():
        raise SystemExit(f"{run.name}: not answered yet, so nothing can be applied ({ANSWERS} is missing)")
    if state not in APPLIED_STATES:
        raise SystemExit(f"--state {state!r}: one of " + ", ".join(APPLIED_STATES))
    by = " ".join(by.split())
    if not by:
        raise SystemExit("--by: say what changed, with real names (a file, a decision)")
    ids = {q["id"] for q in load(run)["questions"]}
    unknown = [q for q in qids if q not in ids]
    if unknown or not qids:
        raise SystemExit(f"{run.name}: no such question {', '.join(unknown) or '(none given)'}; its questions are "
                         + ", ".join(sorted(ids)))
    path = run / APPLIED
    lines = {}
    if path.is_file():
        for ln in path.read_text(encoding="utf-8").splitlines():
            m = APPLIED_LINE.match(ln)
            if m:
                lines[m.group(1)] = ln
    when = (now or datetime.now()).strftime("%Y-%m-%d %H:%M")
    for q in qids:
        lines[q] = f"{q} · {state} · {when} · {by}"
    order = sorted(lines, key=lambda q: int(q[1:]))
    path.write_text(f"# Applied · {run.name}\n\nWhat the answers changed, one line per question, written by whoever "
                    "applied them; the answers stay in result/.\n\n" + "\n".join(lines[q] for q in order) + "\n",
                    encoding="utf-8")
    return path


def picks(pasted: str) -> tuple[dict, list, list]:
    """({QN: {pick, title, text, note}}, the lines it could not read, the QN given twice) from the copied text: its
    first line, `form:`, `built:` and `for:` are the header; a `note:` line belongs to the question above it, and
    every line after it, at any indent and empty lines too, continues the note until the next question line."""
    answers, current, odd, twice, in_note = {}, None, [], [], False
    for i, line in enumerate(pasted.strip().splitlines()):
        if i == 0 or line.startswith(("form:", "for:", "built:")):
            continue
        if not line.strip():
            if in_note and current:                    # a note's empty line: a paragraph break, kept
                answers[current]["note"] += "\n"
            continue
        m = PASTE_PICK.match(line)
        if m:
            current, in_note = m.group(1), False
            if current in answers:
                twice.append(current)
            answers[current] = {"pick": m.group(3) or (OWN if m.group(5) else ""), "title": m.group(2).strip(),
                                "text": (m.group(4) or "").strip(),
                                "note": ""}
            continue
        m = PASTE_NOTE.match(line)
        if m and current:
            answers[current]["note"], in_note = m.group(1).strip(), True
            continue
        if in_note and current:                        # a note's later line, whatever its indent (JL's chat may strip it)
            answers[current]["note"] += "\n" + line.strip()
            continue
        odd.append(line)
    for given in answers.values():
        given["note"] = re.sub(r"\n{3,}", "\n\n", given["note"]).strip()
    return answers, odd, twice


def run_chain(here: Path) -> tuple:
    """The folders a form's path must end with to name this Run: from its Project (a `Project-*` folder; else its
    Block, `bNN_*` or `Paper-*`; else its page) down to the Run. Hosts serve a SPACE root, so a host's path holds them."""
    above = [here, *here.parents]
    anchor = (next((p for p in above if p.name.startswith("Project-")), None)
              or next((p for p in above if re.match(r"^(b\d{2,}_|Paper-)", p.name)), None)
              or here.parent.parent)                   # the page that holds runs/
    return here.relative_to(anchor.parent).parts


def form_names_run(form: str, run: Path) -> bool:
    """Whether the paste's `form:` path is this Run's own form: the browser's path to it (on a host, from the SPACE
    root; opened as a file, its disk path) must end with this Run's folders from its Project down, then its ticket.
    A path naming no page, or another page's same-named Run, does not (Codex review 261031). A folder in that chain
    reached through a link is followed on disk, from a folder at or above the chain's top."""
    parts = tuple(x for x in form.strip().split("/") if x)
    if not parts or parts[-1] != f"{run.name}.html":
        return False
    mine = (run / f"{run.name}.html").resolve()
    for here in dict.fromkeys([run.absolute(), run.resolve()]):
        chain = run_chain(here)
        if len(parts) > len(chain) and parts[-len(chain) - 1:-1] == chain:
            return True
        top = here.parents[len(chain) - 2] if len(chain) >= 2 else here
        for base in [Path("/"), *top.parents]:
            found = base.joinpath(*parts)
            if found.is_file() and found.resolve() == mine:
                return True
    return False


QUESTIONS_IN_FORM = re.compile(r'<script type="text/markdown" id="haipipe-questions">(.*?)</script>', re.S)


def card_words(form_text: str) -> str:
    """The words a person reads in a form's question cards, without its markup: how a form built before its questions
    were embedded (0.6.1) is compared, so a template change alone never makes it stale."""
    start, end = form_text.find('<section class="card"'), form_text.find('<details class="box">')
    region = form_text[start:end] if start >= 0 and end > start else ""
    region = re.sub(r'<label class="opt own">.*?</label>', "", region, flags=re.S)   # the standard last choice
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", region)).split())


def form_built(form_text: str) -> str:
    m = re.search(r'<meta name="haipipe-built" content="([^"]*)">', form_text)
    return html.unescape(m.group(1)) if m else ""


def checked(run: Path, pasted: str) -> tuple:
    """Every check `save` makes, before anything is written: (questions, picks, unread lines, form: line), or a
    refusal that names what is wrong."""
    lines = pasted.strip().splitlines()
    if not lines:
        raise SystemExit(f"{run.name}: nothing saved: the paste is empty")
    first = lines[0]
    if not any(first.startswith(f"{head} · ") for head in HEADS):
        raise SystemExit(f"{run.name}: nothing saved: its first line should start 'haipipe-interaction answers · {run.name} ·', "
                         f"and reads {first[:120]!r}")
    named = first.split(" · ")[1].strip() if len(first.split(" · ")) > 1 else ""
    if named != run.name:
        raise SystemExit(f"{run.name}: nothing saved: the paste is {named or '(no Run)'}'s, not this Run's")
    out = run / ANSWERS
    done = str(read_card(run).get("status")) == "done"
    if out.exists():                                   # an interrupted save left its answers: the Result is closed
        raise SystemExit(f"{run.name}: nothing saved: {ANSWERS} is already saved and closed. A changed mind is a new "
                         "Run (collect.py new), never a rewrite of a closed Result"
                         + ("" if done else "; its card still says waiting, so an earlier save stopped halfway: "
                                            "collect.py close finishes it"))
    if done and not out.exists():
        raise SystemExit(f"{run.name}: nothing saved: its card says done but {ANSWERS} is missing; look at the Run by hand")
    form_file = run / f"{run.name}.html"
    if not form_file.is_file():
        raise SystemExit(f"{run.name}: nothing saved: it has no form yet (collect.py build)")
    try:
        spec = load(run)
    except SpecError as err:
        raise SystemExit(f"{run.name}: nothing saved: {err}")
    form_text = form_file.read_text(encoding="utf-8")
    built = form_built(form_text)
    kept = QUESTIONS_IN_FORM.search(form_text)        # the questions the form was built from, or (before 0.6.1) its cards
    stale = (kept.group(1).replace("<\\/", "</") != markdown(spec)) if kept else \
        (card_words(form_text) != card_words(page(spec, run, built)))
    if stale:                                          # its questions changed after the build; a new template never counts
        raise SystemExit(f"{run.name}: nothing saved: the form no longer matches {QUESTIONS} (it changed after the "
                         "build), so these answers may be to other questions; build the form again, reload it, ask again")
    errors = []
    form = next((ln[5:].strip() for ln in lines if ln.startswith("form:")), None)
    wrong_page = form is not None and not form_names_run(form, run)
    if wrong_page:
        errors.append(f"its form: is {form}; this Run's own form ends with {'/'.join(run_chain(run.absolute()))}/{run.name}.html")
    given_built = next((ln[6:].strip() for ln in lines if ln.startswith("built:")), "")
    if built and given_built != built and not wrong_page:
        errors.append(f"it was copied from {'the build of ' + given_built if given_built else 'a form without a build stamp'}"
                      f"; this Run's form now is the build of {built}: reload this Run's form and copy again "
                      "(a paste from another Run's form is refused the same way)")
    head = first.split(" · ")
    if len(head) < 4 or head[2].strip() != spec["title"]:
        errors.append(f"its first line names the title {head[2].strip() if len(head) > 2 else '(none)'!r}; "
                      f"the questions say {spec['title']!r} (a form built from older questions?)")
    answers, odd, twice = picks(pasted)
    asked = {q["id"]: q for q in spec["questions"]}
    errors += [f"{qid} is answered twice (if one of those lines belongs to a note, indent it)" for qid in dict.fromkeys(twice)]
    for qid, given in answers.items():
        q = asked.get(qid)
        if q is None:
            errors.append(f"{qid} is not one of this Run's questions ({', '.join(asked)})")
            continue
        if given["title"] != q["title"]:
            errors.append(f"{qid} is titled {given['title']!r}; the questions say {q['title']!r} (an older form?)")
        if given["pick"] == OWN:
            if not given["note"].strip():
                errors.append(f"{qid}: my own decision has no words; write the decision in its note")
        elif given["pick"]:
            option = next((o for o in q["options"] if o["key"] == given["pick"]), None)
            if option is None:
                errors.append(f"{qid}: {given['pick']} is not one of its options ({', '.join(o['key'] for o in q['options'])})")
            elif given["text"] != option["text"]:
                errors.append(f"{qid} {given['pick']} reads {given['text']!r}; the questions say {option['text']!r} (an older form?)")
    missing = [qid for qid in asked if qid not in answers]
    if missing:
        errors.append(f"no line for {', '.join(missing)}")
    if errors:
        unread = f"\n  lines not read as a pick or a note: {' | '.join(odd)}" if odd else ""
        raise SystemExit(f"{run.name}: nothing saved:\n  " + "\n  ".join(errors) + unread)
    return spec, answers, odd, form


DECISIONS = "decisions.yaml"        # a chat record's own list, one entry per decision, in order


def record_decisions(run: Path) -> list:
    """A chat record's decisions [{title, decision, said, when, applied_by}], from its decisions.yaml, else read back
    from the files an older record wrote (its questions' Said line, its answers' decision line, its applied.md)."""
    import yaml
    f = run / DECISIONS
    if f.is_file():
        return yaml.safe_load(f.read_text(encoding="utf-8")) or []
    spec, out = load(run), []
    text = (run / ANSWERS).read_text(encoding="utf-8") if (run / ANSWERS).is_file() else ""
    got = re.search(r"(?m)^received:\s*(.+)$", text)
    flags = {m.group(1): m.group(4) for m in (APPLIED_LINE.match(x) for x in ((run / APPLIED).read_text(encoding="utf-8").splitlines()
             if (run / APPLIED).is_file() else [])) if m}
    for q in spec["questions"]:
        block = re.search(rf"(?ms)^## {q['id']} · .*?(?=^## |\Z)", text)
        dec = re.search(r"(?m)^> decision:\s*(.+)$", block.group(0)) if block else None
        said = re.match(r'Said in the chat: "(.*)"$', q.get("why", ""), re.S)
        out.append({"title": q["title"], "decision": dec.group(1).strip() if dec else "", "said": said.group(1) if said else q.get("why", ""),
                    "when": got.group(1).strip() if got else "", "applied_by": flags.get(q["id"], "")})
    return out


def _write_record(run: Path, title: str, for_: str, items: list, now: datetime) -> None:
    import yaml
    spec = {"title": title, "for": for_, "intro": "Decided in the chat, not on a form; this topic's decisions, in the order they were made.",
            "questions": [{"id": f"Q{i}", "title": d["title"], "why": f'Said in the chat: "{d["said"]}"',
                           "ask": textwrap_short(d["decision"]), "options": []} for i, d in enumerate(items, 1)]}
    answers = {f"Q{i}": {"pick": OWN, "note": d["decision"]} for i, d in enumerate(items, 1)}
    said = "\n".join([f"decided in the chat · {run.name} · {title} · {now:%Y-%m-%d %H:%M}"] + [
        f"Q{i} · {d['title']}: my own decision\n   note: {d['decision']}\n   said: {d['said']}" for i, d in enumerate(items, 1)])
    (run / QUESTIONS).write_text(markdown(spec), encoding="utf-8")
    (run / ANSWERS).parent.mkdir(exist_ok=True)
    (run / ANSWERS).write_text(answer_file(spec, answers, f"{now:%Y-%m-%d %H:%M}", said), encoding="utf-8")
    (run / DECISIONS).write_text(yaml.safe_dump(items, allow_unicode=True, sort_keys=False, width=200), encoding="utf-8")
    (run / f"{run.name}.html").write_text(record_page(run, title, for_, items), encoding="utf-8")   # what See answers opens
    lines = [f"Q{i} · applied · {d.get('applied_at') or d.get('when') or f'{now:%Y-%m-%d %H:%M}'} · {d['applied_by']}"
             for i, d in enumerate(items, 1) if d.get("applied_by")]
    if lines:
        (run / APPLIED).write_text(f"# Applied · {run.name}\n\nWhat the answers changed, one line per question, written by whoever "
                                   "applied them; the answers stay in result/.\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def record_page(run: Path, title: str, for_: str, items: list) -> str:
    """A chat record, read only, in the forms' look: each decision as a card, the person's words under it, its flag
    (JL 261031: "the UI here doesn't good", on See answers opening raw Markdown). GENERATED by collect.py."""
    cards = "".join(
        f'<section class="card"><h2><span class="qid">Q{i}</span>{html.escape(d["title"])}'
        + (f'<span class="flag">✅ applied {html.escape((d.get("applied_at") or d.get("when") or "")[:10])}</span>' if d.get("applied_by") else "")
        + f'</h2><p class="dec">{html.escape(d["decision"])}</p><p class="said">“{html.escape(d["said"])}”</p>'
        + f'<p class="meta">{html.escape(d.get("when") or "")}' + (f' · {html.escape(d["applied_by"])}' if d.get("applied_by") else "") + '</p></section>'
        for i, d in enumerate(items, 1))
    return f"""<!doctype html><!-- GENERATED by collect.py record; never edit, rerun it -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<style>:root{{color-scheme:light dark;--ink:light-dark(#1c1c1c,#e8e8e6);--muted:light-dark(#6f6f6b,#a0a09c);--line:light-dark(#e3e3e6,#2c2e33);
--bg:light-dark(#f6f6f7,#161719);--paper:light-dark(#fff,#1b1c1f);--ok:light-dark(#2b8a3e,#8ce99a)}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:860px;margin:auto;padding:24px 16px 48px}}.kicker{{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
h1{{font-size:24px;margin:4px 0 6px}}.lead{{color:var(--muted);margin:0 0 18px}}
.card{{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:0 0 12px}}
.card h2{{font-size:16px;margin:0 0 6px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}}.qid{{color:var(--muted);font-weight:600}}
.flag{{margin-left:auto;font-size:12.5px;font-weight:600;color:var(--ok)}}.dec{{font-size:16px;margin:0 0 8px}}
.said{{margin:0 0 6px;padding-left:10px;border-left:3px solid var(--line);color:var(--muted);font-style:italic}}.meta{{font-size:12px;color:var(--muted);margin:0}}
</style></head><body><main><div class="kicker">✍ Decided in the chat · {html.escape(run.name)} · {html.escape(for_)}</div>
<h1>{html.escape(title)}</h1><p class="lead">This topic's decisions, in the order they were made, each with the words that made it.</p>
{cards}</main></body></html>
"""


def textwrap_short(s: str, n: int = 90) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def record(page_dir: Path, slug: str, title: str, for_: str, decisions: list, applied_by: str = "",
           now: datetime | None = None) -> Path:
    """A decision the person made in the chat, not on a form, kept as an interaction like any answered form (JL
    261031: "the big decisions like this should also be recorded ... to be consistent in the future"). One theme, one
    set (JL 261031: "each question set should have a things like theme ... we don't want to have some many short
    questions list"): a topic's chat decisions all go into its one record under the page, appended in order; a new
    record Run is made only for a topic that has none. `decisions` is [(title, what was decided, their own words)].
    Each question's line on the workbench is the decision itself; `applied_by` flags the new ones applied."""
    if not page_dir.is_dir():
        raise SystemExit(f"{page_dir}: no such folder")
    if not SLUG.match(slug):
        raise SystemExit(f"slug {slug!r}: lower-case words joined by _")
    if not topic_of(for_):
        raise SystemExit(f"--for {for_!r}: a decision belongs to one Studio topic; name its sNN, as --for '{EXAMPLE_FOR}'")
    if not decisions or any(not (d[0].strip() and d[1].strip() and d[2].strip()) for d in decisions):
        raise SystemExit("each --decision is 'title :: what was decided :: the person\'s own words', all three filled")
    now = now or datetime.now()
    runs = page_dir / "runs"
    here = sorted(x for x in runs.iterdir() if x.is_dir()) if runs.is_dir() else []
    mine = [x for x in here if "_collect_" in x.name and (x / "run.yaml").is_file()
            and read_card(x).get("source") == "chat" and topic_of(read_card(x).get("target", "")) == topic_of(for_)]
    new = [{"title": d[0].strip(), "decision": d[1].strip(), "said": d[2].strip(), "when": f"{now:%Y-%m-%d %H:%M}",
            "applied_by": applied_by} for d in decisions]
    if mine:                                       # the topic's record: append, keep its name and title
        run = mine[0]
        card = read_card(run)
        items = record_decisions(run) + new
        _write_record(run, load(run)["title"], card.get("target") or for_, items, now)
        nums = [int(m.group(1)) for x in (run / "passes").iterdir() for m in [re.match(r"^p(\d+)-", x.name)] if m] if (run / "passes").is_dir() else []
        folder = run / "passes" / f"p{(max(nums) + 1 if nums else 1):02d}-{now:%m%d}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "pass.md").write_text(f"# {folder.name} · decided in the chat\n\nrecorded: {now:%Y-%m-%d %H:%M}; "
                                        f"{len(new)} decision(s) added to {ANSWERS}.\n", encoding="utf-8")
        card["passes"] = sorted(set(card.get("passes") or []) | {folder.name})
        write_card(run, card)
        return run
    if any(x.name.endswith(f"_collect_{slug}") for x in here):
        raise SystemExit(f"a collection Run for {slug!r} is already under {page_dir.resolve().name}: use a new slug")
    nums = [int(m.group(1)) for x in here for m in [re.match(r"^r(\d+)_", x.name)] if m]
    run = runs / f"r{(max(nums) + 1 if nums else 1):02d}_collect_{slug}"
    run.mkdir(parents=True)
    _write_record(run, title, for_, new, now)
    folder = run / "passes" / f"p01-{now:%m%d}"
    folder.mkdir(parents=True)
    (folder / "pass.md").write_text(f"# {folder.name} · decided in the chat\n\nrecorded: {now:%Y-%m-%d %H:%M}; {ANSWERS} holds "
                                    "the decisions and the person's words.\n", encoding="utf-8")
    write_card(run, {"run": run.name, "kind": "hard", "type": "collect", "scope": where(page_dir), "target": for_,
                     "ticket": None, "skill": "haipipe-interaction", "agent": None, "signs": None, "status": "done",
                     "source": "chat", "passes": [folder.name], "writes": [ANSWERS], "feeds": []})
    return run


def _theme(for_: str) -> str:
    """A topic's theme in words, from its address: `… @ paper_tree_concept` → "Paper tree concept"."""
    slug = (for_.split("@", 1)[1] if "@" in for_ else "").strip()
    words = slug.replace("_", " ").capitalize() if slug else "This topic"
    return re.sub(r"\bui\b", "UI", words)


def audit(top: Path, fix: bool = False) -> list:
    """Check every question set (collection Run) at or below `top` (JL 261031: "make it to check all the interaction
    question sets"): one theme, one set. Lists, per page and topic: chat records split over several Runs (--fix merges
    them into the first, renamed rNN_collect_<theme>_decisions, the others removed), more than one waiting form, an
    old record whose lines read "What was decided?" (--fix rewrites it), and a set that names no Studio topic."""
    found, groups = [], {}
    for card_f in sorted(top.rglob("runs/r*_collect_*/run.yaml")):
        run = card_f.parent
        if "_archive" in run.parts:
            continue
        card = read_card(run)
        q = run / QUESTIONS
        text = q.read_text(encoding="utf-8", errors="ignore") if q.is_file() else ""
        for_ = (re.search(r"(?m)^for:\s*(.+?)\s*$", text) or [None, card.get("target") or ""])[1]
        topic = topic_of(for_)
        if not topic:
            found.append((run, "names no Studio topic (for:); give it its sNN"))
            continue
        kind = "chat" if card.get("source") == "chat" else card.get("status") or "planned"
        groups.setdefault((run.parent.parent, topic, kind), []).append(run)
        if kind == "chat" and "**What was decided?**" in text:
            found.append((run, "an old record: its lines read \"What was decided?\""))
            if fix:
                _write_record(run, load(run)["title"], card.get("target") or for_, record_decisions(run), datetime.now())
    short = {}                                     # waiting sets of one or two questions, by the Job above them
    for (page, topic, kind), runs in groups.items():
        if kind == "waiting":
            job = next((d for d in [page, *page.parents] if re.match(r"^j\d+_", d.name)), page)
            short.setdefault(job, []).extend(r for r in runs if len(load(r)["questions"]) <= 2)
    for job, runs in short.items():
        if len(runs) >= 3:
            found.append((job, f"{len(runs)} short waiting sets (one or two questions each): answer them on one page "
                               "(collect.py bundle), and ask the next round as one set per theme"))
    for (page, topic, kind), runs in groups.items():
        if kind == "waiting" and len(runs) > 1:
            found.append((page, f"{topic}: {len(runs)} waiting sets; one theme, one set: " + ", ".join(r.name for r in runs)))
        if kind == "chat" and len(runs) > 1:
            found.append((page, f"{topic}: chat decisions split over " + ", ".join(r.name for r in runs)))
            if fix:
                found.append((page, f"{topic}: merged into {merge_records(runs).name}"))
    return found


def merge_records(runs: list) -> Path:
    """One topic's chat records under one page, merged into the first, in order: its decisions all in one set, named
    by the theme (rNN_collect_<theme>_decisions); the others' folders removed; links to their old names are updated
    in the page's own Markdown (and its Board's) by the caller's sweep."""
    import shutil
    runs = sorted(runs, key=lambda r: r.name)
    first, card = runs[0], read_card(runs[0])
    for_ = card.get("target") or ""
    items = [d for r in runs for d in record_decisions(r)]
    theme = (for_.split("@", 1)[1].strip() if "@" in for_ else "topic")
    name = f"{first.name.split('_collect_')[0]}_collect_{re.sub(r'[^a-z0-9]+', '_', theme.lower()).strip('_')}_decisions"
    target = first.parent / name
    if target != first:
        first.rename(target)
    for r in runs[1:]:
        shutil.rmtree(r)
    card = read_card(target)
    card["run"] = target.name
    write_card(target, card)
    _write_record(target, f"{_theme(for_)} decisions"[:60], for_, items, datetime.now())
    old = [r.name for r in runs if r.name != target.name]
    board = next((d for d in target.parents if (d / "board.md").is_file()), target.parent.parent)
    for md in board.rglob("*.md"):
        if "_archive" in md.parts or md.name == "answer_collection.md":
            continue
        s = md.read_text(encoding="utf-8", errors="ignore")
        n = s
        for o in old:
            n = n.replace(o, target.name)
        if n != s:
            md.write_text(n, encoding="utf-8")
    return target


BUNDLE = "answer_all.html"


def waiting_runs(page_dir: Path) -> list:
    """Every waiting collection Run at this page or below, in path order."""
    return sorted(r.parent for r in page_dir.rglob("runs/r*_collect_*/run.yaml")
                  if read_card(r.parent).get("status") == "waiting" and (r.parent / f"{r.parent.name}.html").is_file())


def bundle(page_dir: Path) -> Path:
    """One page that answers every waiting form under `page_dir` at once (JL 261031: "should actively think about
    combine the different interactions in to one page"): each form in place, one under the other, and one Copy that
    joins all their answers; save-all splits the paste back to each Run. Written to <page>/runs/answer_all.html
    (GENERATED; never edited by hand; rerun bundle)."""
    runs = waiting_runs(page_dir)
    out = page_dir / "runs" / BUNDLE
    out.parent.mkdir(parents=True, exist_ok=True)
    items = []
    for run in runs:
        spec = load(run)
        src = os.path.relpath(run / f"{run.name}.html", out.parent)
        items.append(f'<section class="b-item"><h2>🙋 {html.escape(spec["title"])}</h2>'
                     f'<p class="b-meta">{html.escape(spec.get("for", ""))} · <code>{html.escape(run.name)}</code> · '
                     f'<a href="{html.escape(src)}" target="_blank" rel="noopener">Open alone ↗</a></p>'
                     f'<iframe class="b-form" src="{html.escape(src)}" title="{html.escape(spec["title"])}"></iframe></section>')
    body = "".join(items) or '<p class="b-meta">Nothing waits for you here.</p>'
    out.write_text(f"""<!doctype html><!-- GENERATED by collect.py bundle {page_dir.name}; never edit, rerun it -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Answer all · {html.escape(page_dir.name)}</title><style>
:root{{color-scheme:light dark;--ink:light-dark(#1c1c1c,#e8e8e6);--muted:light-dark(#6f6f6b,#a0a09c);--line:light-dark(#e3e3e6,#2c2e33);
--bg:light-dark(#f6f6f7,#161719);--paper:light-dark(#fff,#1b1c1f);--accent:light-dark(#1864ab,#91caff)}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:980px;margin:auto;padding:24px 16px 120px}}h1{{font-size:24px;margin:0 0 4px}}.lead{{color:var(--muted);margin:0 0 20px}}
.b-item{{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:0 0 16px}}
.b-item h2{{font-size:17px;margin:0 0 2px}}.b-meta{{color:var(--muted);font-size:12.5px;margin:0 0 8px}}
.b-form{{width:100%;border:0;min-height:300px}}
.b-bar{{position:fixed;left:0;right:0;bottom:0;background:var(--paper);border-top:1px solid var(--line);padding:10px 16px;
display:flex;gap:12px;justify-content:center;align-items:center}}.b-bar button{{font:inherit;font-weight:600;border:0;border-radius:8px;
padding:9px 18px;background:var(--accent);color:#fff;cursor:pointer}}.b-bar span{{color:var(--muted);font-size:13px}}
#all{{position:absolute;left:-9999px}}</style></head><body><main>
<h1>Answer all · {html.escape(page_dir.name)}</h1>
<p class="lead">Every form that waits for you here, in one page. Pick in each, then press Copy all answers once and paste it back.</p>
{body}</main><div class="b-bar"><button type="button" id="copy">Copy all answers</button><span id="said"></span></div>
<textarea id="all" readonly></textarea><script>
(function(){{
  var frames = Array.prototype.slice.call(document.querySelectorAll('.b-form'));
  function fit(f){{ try {{ var d = f.contentDocument; f.style.height = (d.documentElement.scrollHeight + 8) + 'px';
    d.querySelectorAll('[data-copy], #reset').forEach(function(x){{ x.style.display = 'none'; }});   /* one Copy, below */
    d.querySelectorAll('.bar, .actions, #copy-bar').forEach(function(x){{ x.style.position = 'static'; }}); }} catch (e) {{}} }}
  frames.forEach(function(f){{ f.addEventListener('load', function(){{ fit(f); setInterval(function(){{ fit(f); }}, 1500); }}); }});
  document.getElementById('copy').addEventListener('click', function(){{
    var parts = frames.map(function(f){{ try {{ return f.contentWindow.haipipeAnswers(); }} catch (e) {{ return ''; }} }}).filter(Boolean);
    var box = document.getElementById('all'); box.value = parts.join('\\n\\n');
    var said = document.getElementById('said');
    function done(ok){{ said.textContent = ok ? 'Copied: paste it back in one message.' : 'The browser blocked copying: the text is shown, copy it by hand.';
      if (!ok) {{ box.style.cssText = 'position:fixed;left:16px;right:16px;bottom:64px;height:40vh;z-index:9'; box.focus(); box.select(); }} }}
    if (navigator.clipboard && window.isSecureContext) {{ navigator.clipboard.writeText(box.value).then(function(){{ done(true); }}, function(){{ box.select(); done(document.execCommand('copy')); }}); }}
    else {{ box.select(); var ok = false; try {{ ok = document.execCommand('copy'); }} catch (e) {{}} done(ok); }}
  }});
}})();
</script></body></html>
""", encoding="utf-8")
    return out


def save_all(pasted: str, root: Path, now: datetime | None = None) -> list:
    """One paste from the combined page, split at each form's first line, each saved to its own Run by its form:
    path (from the SPACE root); a block that does not save is named, the others still save."""
    heads = re.compile(r"(?m)^(?=(?:%s) · )" % "|".join(re.escape(h) for h in HEADS))
    blocks = [b.strip() + "\n" for b in heads.split(pasted) if b.strip()]
    done, failed = [], []
    for b in blocks:
        form = re.search(r"(?m)^form:\s*(\S+)", b)
        run = (root / form.group(1).lstrip("/")).parent if form else None
        if run is None or not (run / "run.yaml").is_file():
            failed.append(b.splitlines()[0][:80] + " : its form: path does not lead to a Run")
            continue
        try:
            done.append(save(run, b, now))
        except SystemExit as err:
            failed.append(f"{run.name}: {err}")
    for f in failed:
        print("not saved: " + f, file=sys.stderr)
    return done


def save(run: Path, pasted: str, now: datetime | None = None) -> Path:
    """The person's picks into result/answer_collection.md (the same Markdown, their picks ticked), the pasted text
    kept word for word below it; one pass; the card says done. Every check runs first (checked)."""
    spec, answers, odd, form = checked(run, pasted)
    if form is None:
        print(f"{run.name}: the paste has no form: line; matched by its first line and its build stamp", file=sys.stderr)
    if odd:                                                    # kept word for word below either way
        print(f"{run.name}: lines not read as a pick or a note: " + " | ".join(odd), file=sys.stderr)
    now = now or datetime.now()
    out = run / ANSWERS
    out.parent.mkdir(exist_ok=True)
    part = out.with_name(out.name + ".part")                   # whole or not at all: written aside, then moved in
    part.write_text(answer_file(spec, answers, f"{now:%Y-%m-%d %H:%M}", pasted), encoding="utf-8")
    os.replace(part, out)
    done = close(run, now)
    if (run / f"{run.name}.html").is_file():           # the form reopens read only, its stamp kept (b15 261101: an
        build(run)                                     # answered form still showed Copy feedback until rebuilt)
    return done


def answer_file(spec: dict, answers: dict, received: str, pasted: str) -> str:
    """The answer file: the questions' Markdown with the person's picks ticked, when it came, the paste word for word."""
    body = markdown(spec, answers).split("\n", 1)
    return (f"{body[0]}\n\nreceived: {received}\n{body[1]}\n## The pasted text\n\n"
            f"```text\n{pasted.strip()}\n```\n")


KEPT_PASTE = re.compile(r"(?s)\n## The pasted text\n\n```text\n(.*)\n```\n?$")


def close(run: Path, now: datetime | None = None) -> Path:
    """Finish a save: the round's pass and `status: done` on the card, once its answer file is there. `save` ends with
    it; on its own it finishes a save that stopped halfway. It first runs save's checks on the paste the answer file
    keeps, so a file that is not a saved answer is never closed; it never touches the answers, and it reuses a pass
    an interrupted save already wrote."""
    out = run / ANSWERS
    card_ = read_card(run)
    if not out.is_file():
        raise SystemExit(f"{run.name}: its card says done but {ANSWERS} is missing; look at the Run by hand"
                         if card_.get("status") == "done" else f"{run.name}: no {ANSWERS} to close; save the person's answers first")
    if card_.get("status") == "done":
        return out
    text = out.read_text(encoding="utf-8", errors="ignore")
    kept = KEPT_PASTE.search(text)
    got = re.search(r"(?m)^received:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", text)
    if not kept or not got:
        raise SystemExit(f"{run.name}: {ANSWERS} holds no pasted text and time, so it is not a saved answer; "
                         "look at the Run by hand")
    pasted = kept.group(1)
    first = pasted.strip().splitlines()[0] if pasted.strip() else ""
    if not any(first.startswith(f"{head} · {run.name} ·") for head in HEADS):
        raise SystemExit(f"{run.name}: the paste kept in {ANSWERS} is not this Run's; look at the Run by hand")
    flat = lambda t: t.replace("\r\n", "\n").rstrip("\n")   # a Windows line end or a trimmed last line is no edit (k6b2)
    try:                                               # the body is exactly what save writes from that paste (k6b)
        same = flat(answer_file(load(run), picks(pasted)[0], got.group(1), pasted)) == flat(text)
    except SpecError:
        same = False
    if not same:
        raise SystemExit(f"{run.name}: {ANSWERS} is not what save writes from the paste it keeps (edited by hand, or "
                         f"its {QUESTIONS} changed since); look at the Run by hand")
    now = now or (datetime.strptime(got.group(1), "%Y-%m-%d %H:%M") if got else datetime.fromtimestamp(out.stat().st_mtime))
    passes = run / "passes"
    written = sorted(x.name for x in passes.iterdir() if (x / "pass.md").is_file()
                     and "the answers came back" in (x / "pass.md").read_text(encoding="utf-8", errors="ignore")) if passes.is_dir() else []
    if not written:                                    # no pass yet: this round's
        nums = [int(m.group(1)) for x in passes.iterdir() for m in [re.match(r"^p(\d+)-", x.name)] if m] if passes.is_dir() else []
        folder = passes / f"p{(max(nums) + 1 if nums else 1):02d}-{now:%m%d}"
        folder.mkdir(parents=True)
        (folder / "pass.md").write_text(f"# {folder.name} · the answers came back\n\nreceived: {now:%Y-%m-%d %H:%M}; "
                                        f"{ANSWERS} holds them.\n", encoding="utf-8")
        written = [folder.name]
    card_.update({"status": "done", "passes": sorted(set(card_.get("passes") or []) | set(written)), "writes": [ANSWERS]})
    write_card(run, card_)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new", help="allocate a collection Run under a page")
    n.add_argument("page", type=Path)
    n.add_argument("slug")
    n.add_argument("--title", required=True)
    n.add_argument("--for", dest="for_", required=True, help=f"its Studio topic, as '{EXAMPLE_FOR}'")
    n.add_argument("--person", default="")
    n.add_argument("--feeds", default="")
    for name, text in (("check", "list the questions' problems"), ("build", "render the form")):
        s = sub.add_parser(name, help=text)
        s.add_argument("run", type=Path)
    s = sub.add_parser("save", help="keep the pasted picks")
    s.add_argument("run", type=Path)
    s.add_argument("file", nargs="?", type=Path)
    c = sub.add_parser("close", help="finish a save that stopped halfway")
    c.add_argument("run", type=Path)
    r = sub.add_parser("record", help="keep a decision made in the chat as an answered interaction")
    r.add_argument("page", type=Path)
    r.add_argument("slug")
    r.add_argument("--title", required=True)
    r.add_argument("--for", dest="for_", required=True, help=f"its Studio topic, as '{EXAMPLE_FOR}'")
    r.add_argument("--decision", action="append", required=True,
                   help="'title :: what was decided :: the person's own words'; once per decision")
    r.add_argument("--applied-by", default="", help="what already applied them, with real names: flags them applied")
    au = sub.add_parser("audit", help="check every question set: one theme, one set")
    au.add_argument("top", type=Path)
    au.add_argument("--fix", action="store_true", help="merge split chat records; rewrite old records")
    bu = sub.add_parser("bundle", help="one page answering every waiting form under a page")
    bu.add_argument("page", type=Path)
    sa = sub.add_parser("save-all", help="save a paste from the combined page, each form to its Run")
    sa.add_argument("file", nargs="?", type=Path)
    sa.add_argument("--root", type=Path, default=None, help="the SPACE root the form: paths start from (default: found)")
    a = sub.add_parser("applied", help="record that answers were applied: their flags on the form")
    a.add_argument("run", type=Path)
    a.add_argument("questions", nargs="+", help="Q1 Q2 ...")
    a.add_argument("--by", required=True, help="what changed, with real names")
    a.add_argument("--state", default="applied", choices=APPLIED_STATES)
    args = ap.parse_args(argv)
    if args.cmd == "new":
        feeds = [f.strip() for f in args.feeds.split(",") if f.strip()]
        print(new(args.page, args.slug, args.title, args.for_, args.person, feeds))
        return 0
    if args.cmd == "audit":
        found = audit(args.top, args.fix)
        for where_, what in found:
            print(f"{where_}: {what}")
        print("ok" if not found else f"{len(found)} finding(s)")
        return 0
    if args.cmd == "bundle":
        print(bundle(args.page))
        return 0
    if args.cmd == "save-all":
        pasted = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
        root = args.root or space_root(Path.cwd())
        for out in save_all(pasted, Path(root)):
            print(out)
        return 0
    if args.cmd == "record":
        parts = [[x.strip() for x in d.split("::")] for d in args.decision]
        if any(len(x) != 3 for x in parts):
            raise SystemExit("each --decision is 'title :: what was decided :: the person's own words'")
        print(record(args.page, args.slug, args.title, args.for_, [tuple(x) for x in parts], args.applied_by))
        return 0
    run = run_folder(args.run)
    if args.cmd == "check":
        try:
            found = problems(load(run), run)
        except SpecError as err:
            found = [str(err)]
        print("\n".join(found) if found else "ok")
        return 1 if found else 0
    if args.cmd == "build":
        print(build(run))
        return 0
    if args.cmd == "close":
        print(close(run))
        return 0
    if args.cmd == "applied":
        print(applied(run, args.questions, args.by, args.state))
        return 0
    pasted = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
    print(save(run, pasted))
    return 0


if __name__ == "__main__":
    sys.exit(main())
