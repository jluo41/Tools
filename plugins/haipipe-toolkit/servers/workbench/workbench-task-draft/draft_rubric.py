"""4 · Writing Rubric on a draft Task's Draft view (JL 261113: "add 4. Writing Rubric, to add the writing principles or
the rules we set. I want it to be the left tab and right content, left tab can be different types of topics, and right
content could be a list of rules, and we can add it as well").

Each tab reads the one file where its rules already live, so nothing is copied:
  This Section   the page's authored W rules (<stem>-requirement.md) and the author's rulings R1, R2 …
                 (<stem>-revise-rules.md), both in draft/records/                                     ✚ add
  Coauthors      the paper Board's writing-patterns.md (the co-authors' patterns)                  ✚ add
  Venue          the same requirement file's generated venue rules (V blocks)
  Plain English  haipipe-draft-review ref/plain-rules.md (its section headings)
  Anti-AI        haipipe-draft-review ref/ai-tells.md (its section headings)
Skill rules serve every project, so they are read here and changed in the skill. An added rule is written by
`rule_act` (POST /_board/draft-rule) into its tab's file, dated from the clock.
"""
from __future__ import annotations

import datetime
import re
from pathlib import Path

from live.frame import esc

SKILLS = Path(__file__).resolve().parents[3] / "skills" / "1_base" / "draft" / "haipipe-draft-review" / "ref"


def _req(folder: Path) -> Path:
    return folder / "draft" / "records" / f"{folder.name}-requirement.md"


def _patterns(folder: Path) -> Path:
    return folder.parent.parent / "writing-patterns.md"          # tNN_<section> / jNN_<version> / Paper-X


def _blocks(text: str, prefix: str) -> list:
    """[(title, rule)] of `### W1 · title` / `### V2 · title` blocks: every `- **Rule**:` line, or the title alone."""
    out = []
    for m in re.finditer(r"(?ms)^### (" + prefix + r"\d+) · ([^\n]*)\n(.*?)(?=^### |^# ---|\Z)", text):
        rules = re.findall(r"(?m)^- \*\*Rule\*\*: (.*)$", m.group(3))
        title = m.group(2).strip()
        out += [(f"{m.group(1)} · {title}", "" if r.strip().rstrip(".") == title.rstrip(".") else r.strip()) for r in rules] \
            or [(f"{m.group(1)} · {title}", "")]                  # a short rule shows once (JL 261113: "hard to read")
    return out


def _headings(path: Path, level: str = "##") -> list:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    return [(re.sub(r"^\d+[a-z]? · ", "", h).strip(), "") for h in re.findall(r"(?m)^" + level + r" (.+)$", text)
            if not re.match(r"(?i)\d+ · (the test|what no rule)", h)]


def _rules(path: Path) -> list:
    """The skill file's own rules, not its chapter titles (JL 261113, of a tab listing "The catalogue": "I don't
    understand about this"): each `- **Name**: detail` line, and each paragraph that opens on a **bold rule.**"""
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    out = []
    for m in re.finditer(r"(?m)^- \*\*([^*]+)\*\*:?\s*(.*(?:\n  +.*)*)", text):        # - **Filler**: "in order to"
        out.append((m.group(1).strip().rstrip(":"), " ".join(m.group(2).split())))
    for m in re.finditer(r"(?m)^\*\*([^*]{8,}?[.!?\)])\*\*[ \t]*(.*(?:\n(?!\s*\n).+)*)", text):   # **One reader move.** …
        para = " ".join(m.group(2).split())
        first = re.split(r"(?<=[.!?])\s", para, maxsplit=1)[0] if para else ""
        out.append((" ".join(m.group(1).split()), first))
    seen = set()
    return [x for x in out if not (x[0] in seen or seen.add(x[0])) and not x[0].lower().startswith(("before", "after"))]


def tabs(folder: Path) -> list:
    """[(key, name, rules [(title, text)], source path, can add)] in the order the rail shows them."""
    req = _req(folder)
    rtext = req.read_text(encoding="utf-8", errors="replace") if req.is_file() else ""
    authored = rtext.split("# --- writing:begin", 1)[1] if "# --- writing:begin" in rtext else ""
    venue = rtext.split("# --- requirement:end", 1)[0]
    pat = _patterns(folder)
    ptext = pat.read_text(encoding="utf-8", errors="replace") if pat.is_file() else ""
    coauthors = [(m.group(2).strip(), (re.search(r"(?m)^- \*\*Fix\*\*: (.*)$", m.group(3)) or [None, ""])[1].strip())
                 for m in re.finditer(r"(?ms)^### (\d+)\. ([^\n]*)\n(.*?)(?=^### |\Z)", ptext)]
    rr = folder / "draft" / "records" / f"{folder.name}-revise-rules.md"          # the author's rulings, R1, R2 …
    rulings = [(f"{m.group(1)} · {m.group(2)}", m.group(3).strip()) for m in
               re.finditer(r"(?m)^- (R\d+) · ([^·]+?) · (.*)$", rr.read_text(encoding="utf-8")) ] if rr.is_file() else []
    return [("section", "This Section", _blocks(authored, "W") + rulings, req, True),
            ("coauthors", "Coauthors", coauthors, pat, True),
            ("venue", "Venue", _blocks(venue, "V"), req, False),
            ("plain", "Plain English", _rules(SKILLS / "plain-rules.md"), SKILLS / "plain-rules.md", False),
            ("ai", "Anti-AI", _rules(SKILLS / "ai-tells.md"), SKILLS / "ai-tells.md", False)]


CSS = """<style>
.rb{display:grid;grid-template-columns:150px minmax(0,1fr);gap:18px;align-items:start}
.rb-tabs{display:flex;flex-direction:column;gap:2px;position:sticky;top:8px}
.rb-tab{font:inherit;font-size:13.5px;text-align:left;padding:6px 10px;border:0;border-radius:6px;background:transparent;
 color:var(--muted,#6f6f6b);cursor:pointer}
.rb-tab span{float:right;font-size:12px;opacity:.7}.rb-tab:hover{background:var(--wash)}
.rb-tab[aria-selected=true]{background:var(--soft,#e7f5ff);color:var(--ink);font-weight:600}
.rb-pane[hidden]{display:none}.rb-list{list-style:none;margin:0;padding:0 6px 0 0;counter-reset:rb;max-height:min(60vh,520px);overflow-y:auto;scrollbar-width:thin}   /* a long list scrolls in place (JL 261113) */
.rb-list li{counter-increment:rb;padding:8px 0 8px 30px;border-bottom:1px solid var(--line);position:relative;
 font-size:14.5px;line-height:1.5}
.rb-list li::before{content:counter(rb);position:absolute;left:4px;top:8px;font-size:12px;color:var(--muted)}
.rb-list li:has(.rb-tag){padding-left:4px}.rb-list li:has(.rb-tag)::before{content:none}   /* one number: the tag */
.rb-list b{font-weight:600}.rb-tag{font:500 11px/1 system-ui,sans-serif;color:var(--muted);margin-right:8px}.rb-list .rb-t{display:block;color:var(--muted);font-size:13.5px}
.rb-src{font-size:12px;color:var(--muted);margin:6px 0 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rb-src a{color:var(--muted)}.rb-src a:hover{color:var(--accent,#1864ab)}
.rb-add{display:flex;align-items:center;gap:6px;margin:6px 0 0}
.rb-add input{flex:1;min-width:0;font:inherit;font-size:13px;padding:3px 8px;border:1px solid var(--line);border-radius:5px;
 background:transparent;color:var(--ink)}
.rb-add button{font:inherit;font-size:12.5px;padding:3px 10px;border:1px solid var(--line);border-radius:5px;background:transparent;
 color:var(--accent,#1864ab);cursor:pointer}.rb-msg:empty{display:none}.rb-msg{font-size:12px;color:var(--muted)}
.rb-add .rb-src{margin:0 0 0 4px;max-width:40%}
@media(max-width:700px){.rb{grid-template-columns:minmax(0,1fr)}.rb-tabs{flex-direction:row;flex-wrap:wrap;position:static}}
</style>"""

JS = """<script>(function(){if(window.__rb)return;window.__rb=1;
 document.addEventListener('click',function(e){var t=e.target.closest&&e.target.closest('.rb-tab');if(t){e.preventDefault();
  var b=t.closest('.rb');b.querySelectorAll('.rb-tab').forEach(function(x){x.setAttribute('aria-selected',x===t);});
  b.querySelectorAll('.rb-pane').forEach(function(p){p.hidden=p.dataset.k!==t.dataset.k;});return;}
  var a=e.target.closest&&e.target.closest('.rb-add button');if(!a)return;e.preventDefault();
  var f=a.closest('.rb-add'),i=f.querySelector('input'),m=f.querySelector('.rb-msg'),v=i.value.trim();if(!v){m.textContent='write the rule first';return;}
  a.disabled=true;m.textContent='saving…';
  fetch('/_board/draft-rule',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({task:f.dataset.task,tab:f.dataset.k,text:v})}).then(function(r){return r.json();}).then(function(j){
   a.disabled=false;if(!j.ok){m.textContent=j.err||'not saved';return;}
   var li=document.createElement('li');li.innerHTML='<b></b>';li.firstChild.textContent=v;
   f.parentNode.querySelector('.rb-list').appendChild(li);i.value='';m.textContent='saved to '+j.file;})
  .catch(function(err){a.disabled=false;m.textContent=String(err);});});
})();</script>"""


def _open(src: Path, root: Path) -> str:
    """The tab's markdown file, one click away (JL 261113: "will we have the writing-rubric markdown things here?")."""
    from live.frame import reader
    path = src if str(src).startswith(str(root)) else root / "Tools" / src.relative_to(SKILLS.parents[6])
    if not path.is_file():
        return f"from {esc(src.name)}"
    try:
        href = reader(path, root)
    except ValueError:                           # a skill file lies outside the SPACE (Tools/ is a link), and the page
        return f"from {esc(path.name)} (haipipe-draft-review)"    # server opens no file outside it: named, not linked
    return f'<a data-pop="{esc(path.name)}" href="{esc(href)}">📄 {esc(path.name)} ↗</a>'


def html(folder: Path, root: Path, ts: list | None = None, word: str = "a rule") -> str:
    """The section's body: tabs on the left, the open tab's rules on the right, an add box on writable tabs."""
    task = folder.relative_to(root).as_posix()
    ts = tabs(folder) if ts is None else ts
    nav = "".join(f'<button type=button class=rb-tab data-k="{k}" aria-selected={"true" if i == 0 else "false"}>'
                  f'{esc(n)}<span>{len(rules)}</span></button>' for i, (k, n, rules, _, _) in enumerate(ts))
    panes = ""
    for i, (k, n, rules, src, add) in enumerate(ts):
        tag = lambda t: (lambda m: f'<span class=rb-tag>{esc(m.group(1))}</span>{esc(m.group(2))}' if m else esc(t))(
            re.match(r"([WVRDS]\d+[a-z]?|PP\d+|open) · (.*)$", t))
        items = "".join(f'<li><b>{tag(t)}</b>' + (f'<span class=rb-t>{esc(x)}</span>' if x else "") + '</li>' for t, x in rules)
        where = src.relative_to(root).as_posix() if src.is_file() and str(src).startswith(str(root)) else src.name
        panes += (f'<div class=rb-pane data-k="{k}"{"" if i == 0 else " hidden"}><ol class=rb-list>{items}</ol>'
                  + (f'<div class=rb-add data-k="{k}" data-task="{esc(task)}"><input placeholder="＋ {esc(word)}…">'
                     f'<button type=button>Add</button><span class=rb-msg></span><span class=rb-src>{_open(src, root)}</span></div>'
                     if add else f'<p class=rb-src>{_open(src, root)}</p>') + '</div>')
    return CSS + f'<div class=rb><div class=rb-tabs role=tablist>{nav}</div><div>{panes}</div></div>' + JS


DEC_HEAD = """# {title} · decisions

What has been decided here, one line each: the decision, who decided and when. Open questions stay in their
discussion record until someone rules; then the ruling is a line here. (JL 261113: "maybe a new section for decision?")

## Decided
"""


def _dec_files(folder: Path) -> dict:
    """{tab: its decisions.md}: this Section's, the paper's (the Board) and its venue's."""
    board = folder.parent.parent
    face = folder / f"{folder.name}.md"
    venue = (re.search(r"(?m)^venue:\s*(\S+)", face.read_text(encoding="utf-8")) or [None, ""])[1] if face.is_file() else ""
    out = {"dec-section": folder / "draft" / "records" / f"{folder.name}-decisions.md", "dec-paper": board / "decisions.md"}
    if venue and (board / "venues" / venue).is_dir():
        out["dec-venue"] = board / "venues" / venue / "decisions.md"
    return out


def _dec_lines(path: Path) -> list:
    if not path.is_file():
        return []
    decided = path.read_text(encoding="utf-8").split("## Decided", 1)[-1]
    decided = re.split(r"(?m)^## ", decided, maxsplit=1)[0]        # stop at the next heading (an "## Open" list)
    return [(m.group(1).strip(), (m.group(2) or "").strip()) for m in    # a line with no " — " has no why
            re.finditer(r"(?m)^- (.+?)(?: — (.*))?$", decided)]


def decision_tabs(folder: Path) -> list:
    """[(key, name, items, file, can add)]: This Section (its open D questions first), its Contract, the Paper, the Venue."""
    files = _dec_files(folder)
    disc = folder / "draft" / "records" / f"{folder.name}-discussion.md"
    open_ = [(f"open · {m.group(1)} {m.group(2).strip()}", "") for m in
             re.finditer(r"(?m)^### (D\d+) · (.*)$", disc.read_text(encoding="utf-8"))] if disc.is_file() else []
    face = folder / f"{folder.name}.md"
    ft = face.read_text(encoding="utf-8") if face.is_file() else ""
    field = lambda k: (re.search(r"(?m)^" + k + r":\s*(.*)$", ft) or [None, ""])[1]
    contract = [(f"Must establish: {x.strip()}", "") for x in re.split(r";\s*|,\s*(?=H\d)", field("must-establish")) if x.strip()]
    contract += [("Must refuse: " + field("must-refuse"), "")] if field("must-refuse") else []
    tabs_ = [("dec-section", "This Section", open_ + _dec_lines(files["dec-section"]), files["dec-section"], True),
             ("dec-contract", "Contract", contract, face, False),
             ("dec-paper", "Paper", _dec_lines(files["dec-paper"]), files["dec-paper"], True)]
    if "dec-venue" in files:
        tabs_.append(("dec-venue", "Venue", _dec_lines(files["dec-venue"]), files["dec-venue"], True))
    return tabs_


def decisions_html(folder: Path, root: Path) -> str:
    return html(folder, root, decision_tabs(folder), "a decision")


def rule_act(root: Path, p: dict, read_only: bool = False) -> tuple:
    """Write one added rule into its tab's file: This Section → the next W rule; Coauthors → the next pattern."""
    if read_only:
        return 403, {"ok": False, "err": "read-only server"}
    text = " ".join(str(p.get("text") or "").split())
    folder = (root / str(p.get("task") or "")).resolve()
    if not text or len(text) > 600 or root.resolve() not in folder.parents or not folder.is_dir():
        return 400, {"ok": False, "err": "a rule needs words and a draft Task"}
    now = datetime.datetime.now().strftime("%y%m%d %H%M")
    if p.get("tab") == "section":
        f = _req(folder)
        if not f.is_file():
            return 404, {"ok": False, "err": "no requirement record on this page"}
        s = f.read_text(encoding="utf-8")
        n = max([int(x) for x in re.findall(r"(?m)^### W(\d+) ", s)] or [0]) + 1
        title = text if len(text.split()) <= 14 else " ".join(text.split()[:8]) + " …"   # a short rule is its own title
        block = (f"\n### W{n} · {title}\n- **Rule**: {text}\n- **Applies**: {folder.name} · Content\n"
                 f"- **Source**: JL {now} (workbench, 4 · Writing Rubric)\n")
        s = s.replace("# --- writing:end ---", block.lstrip("\n") + "# --- writing:end ---", 1) if "# --- writing:end ---" in s \
            else s.rstrip("\n") + "\n" + block
    elif p.get("tab") == "coauthors":
        f = _patterns(folder)
        if not f.is_file():
            return 404, {"ok": False, "err": "no writing-patterns.md on this paper Board"}
        s = f.read_text(encoding="utf-8")
        n = max([int(x) for x in re.findall(r"(?m)^### (\d+)\. ", s)] or [0]) + 1
        block = f"### {n}. {' '.join(text.split()[:8])}\n\n- **Fix**: {text}\n- **From**: JL {now} (workbench)\n\n"
        cut = re.search(r"(?m)^### (?!\d+\.)", s)
        s = s[:cut.start()] + block + s[cut.start():] if cut else s.rstrip("\n") + "\n\n" + block
    elif str(p.get("tab", "")).startswith("dec-") and p.get("tab") in _dec_files(folder):
        f = _dec_files(folder)[p["tab"]]
        title = {"dec-section": folder.name, "dec-paper": f.parent.name, "dec-venue": f.parent.name}[p["tab"]]
        s = f.read_text(encoding="utf-8") if f.is_file() else DEC_HEAD.format(title=title)
        s = s.rstrip("\n") + f"\n- {text} — JL {now} (workbench)\n"
    else:
        return 400, {"ok": False, "err": "this tab's rules live in a skill"}
    f.write_text(s, encoding="utf-8")
    return 200, {"ok": True, "file": f.resolve().relative_to(root.resolve()).as_posix()}
