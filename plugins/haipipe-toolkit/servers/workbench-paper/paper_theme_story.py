"""The Idea and Story views of a paper Board: idea cards and maps, the venue map, §3 question blocks, the data and story trees.
Moved from paper_theme.py, which re-exports every name here so `from live.paper_theme import _story_sections` keeps working."""
from __future__ import annotations

import re
from pathlib import Path

from live import paper as P
from live.frame import esc
from live.paper_theme_work import _cols, _first_sentence, _folded, _idea_groups, _items, _key, _line, _mini, _section


def _idea_card(x, words=None, mark=""):
    """One idea, folded to its one line (its short question, verdict and state), opened as its drawing card is: why it
    matters in the key box, its data beside its method, what each finding would mean, now and next; then the face's
    full question, closest work and risk (JL 261020: "让它的 layout 跟我们 draw 里面长得比较相似一些")."""
    w = words or {}
    sub = {k.lower(): " ".join(v) for k, v in x.get("substance") or []}
    status = {k.lower(): re.sub(r"\s*\(.*?\)", "", v) for k, v in x.get("fields") or []}
    call = _first_sentence(sub.get("recommendation", ""), 12)
    short = w.get("short") or _first_sentence(sub.get("research question") or x.get("title", ""), 18)
    meta = " · ".join(esc(v) for v in ([x.get("verdict") or "⬜ open"] + [f"{k} {status[k]}" for k in ("novelty", "pilot")
                                                                         if status.get(k)] + ([call] if call else [])))
    why = w.get("why") or _first_sentence(sub.get("hypothesis", ""))
    results = "<br>".join(f'{P.inline(r.get("find", ""))} <span class=mut>→</span> {P.inline(r.get("means", ""))}'
                          for r in w.get("results") or [])
    rows = [("Question", P.inline(sub.get("research question") or x.get("title", ""))),
            ("Why it matters" if w.get("why") else "Hypothesis", P.inline(why)),
            ("Data", " · ".join(P.inline(i) for i in w.get("data") or [])),
            ("Method", "<br>".join(f"{k}. {P.inline(i)}" for k, i in enumerate(w.get("method") or [], 1))
             or P.inline(_first_sentence(sub.get("method", "")))),
            ("If we find", results + (' <span class=mut>(drafted)</span>' if results and w.get("drafted") else "")),
            ("Now", P.inline(w.get("now", ""))), ("Next", P.inline(w.get("next") or _first_sentence(sub.get("next evidence action", "")))),
            ("Closest work", P.inline(_first_sentence(sub.get("discovery basis", "")))), ("Risk", P.inline(_first_sentence(sub.get("risk", ""))))]
    body = ["".join(_line(k, v) for k, v in rows if v)]
    return _folded(f'{esc(mark)} <b>{esc(x["id"])} · {P.inline(short)}</b>', meta, "".join(body), f"idea-{x['id']}")


def _drawing_words(page):
    """The topic's drawing words (`<topic>-drawing.yaml`), {} when it has none."""
    import yaml
    if not page:
        return {}
    f = Path(page.get("path") or "")
    try:
        return yaml.safe_load(f.read_text(encoding="utf-8")) or {} if f.is_file() else {}
    except Exception:
        return {}


def _idea_map(ideas, direction, shorts=None):
    """The ideas as a map: the direction in the root, each idea a branch (its verdict mark and its question), and a leaf
    for each of its hypothesis, method, smallest experiment, novelty and recommendation, cut to their first sentence."""
    labels = (("Hypothesis", "hypothesis"), ("Method", "method"), ("Minimum Experiment", "experiment"),
              ("novelty", "novelty"), ("Recommendation", "verdict"))
    branches = []
    for x in ideas:
        sub = {k.lower(): v for k, v in x.get("substance") or []}
        sub["novelty"] = [v for k, v in x.get("fields") or [] if k.lower() == "novelty"]   # its short mark, not the table
        leaves = []
        for label, tag in labels:
            said = " ".join(sub.get(label.lower()) or [])
            if said and not said.lstrip().startswith("|"):
                first = _first_sentence(said)
                leaves.append(_leaf("", tag, P.inline(first if len(first) <= 110 else first[:107].rsplit(" ", 1)[0] + " …"), note=said))
        mark = (x.get("verdict") or "").split()[0] if (x.get("verdict") or "")[:1] in "✅🔶⬜❗🟡❌" else ""
        # the drawing's short title when it has one (the full question shows on the card below and on hover)
        branches.append((f"{esc(mark)} {esc(x['id'])}", P.inline((shorts or {}).get(x["id"]) or x.get("title", "")), leaves, "",
                         f"idea-{x['id']}"))
    return _map("💡 The direction", P.inline(direction), branches) if branches else ""


def _idea_cards(d):
    """The Ideation topic as its drawing reads: the question in the key box, the setting folded, then each group of
    ideas (a card each, folded), then the path to G0."""
    i = d.get("ideation") or {}
    ideas = {x["id"]: x for x in i.get("ideas") or []} if i.get("present") else {}
    if not ideas:
        return ""
    page = P.ideation_topic(d["board"])
    text = page["text"] if page else ""
    words = _drawing_words({"path": str(d["board"] / Path(page["rel"]).parent / f'{page["stem"]}-drawing.yaml')} if page else None)
    asked = re.search(r"(?ms)^## Opening\s*\n+(.*?)\n", text)
    index = words.get("index") or {}
    out = []
    roster = words.get("roster") or {}
    if roster:
        flow = " → ".join(P.inline(x) for x in [roster.get("start", ""), roster.get("roster", ""),
                                                 " / ".join(roster.get("google", [])), " / ".join(roster.get("agent", [])), roster.get("end", "")] if x)
        rows = ([("Question", P.inline(asked.group(1).strip()))] if asked else []) + \
               [("Pool", P.inline(index.get("key", ""))), ("Flow", flow), ("Reading", P.inline(roster.get("reading", "")))] + \
               [(n.get("big", ""), P.inline(n.get("tag", ""))) for n in roster.get("numbers") or []]
        out.append(_folded(f'🔑 {P.inline(roster.get("title", "The setting")).lstrip("①").strip()}', P.inline(roster.get("key", "")),
                           "".join(_line(k, v) for k, v in rows if v)))
    groups = [(g.get("name", ""), g.get("line", ""), g.get("ideas") or []) for g in words.get("groups") or []] or \
             [(f"{m} {n}", note, ids) for m, n, note, ids in _idea_groups(text)]
    sketch = {k: m for m, _n, _note, ids in _idea_groups(text) for k in ids}
    shown = set()
    for name, line, ids in groups:
        cards = [_idea_card(ideas[k], (words.get("ideas") or {}).get(k), sketch.get(k, "")) for k in ids if k in ideas and k not in shown]
        shown.update(ids)
        if cards:
            out.append(_section(name, line, "".join(cards)))
    rest = [_idea_card(x, (words.get("ideas") or {}).get(k)) for k, x in ideas.items() if k not in shown]
    if rest:
        out.append(_section("Other ideas", "", "".join(rest)))
    # the ideas also drawn as the draft's §1 mind map (JL 261022: "for the idea and for the story ... I want something
    # like this"): the direction in the root, each idea a branch in the drawing's order, its hypothesis, method,
    # experiment, novelty and recommendation the leaves; the cards follow under their own subsection
    order = [k for _n, _l, ids in groups for k in ids if k in ideas] + [k for k in ideas if k not in shown]
    direction = re.search(r"(?m)^\*\*The direction\*\*:\s*(.*)$", text)
    shorts = {k: v.get("short") for k, v in (words.get("ideas") or {}).items() if isinstance(v, dict) and v.get("short")}
    tree = _idea_map([ideas[k] for k in dict.fromkeys(order)], direction.group(1) if direction else (asked.group(1).strip() if asked else ""),
                     shorts)
    if tree:
        out = [_sub("The ideas"), tree, _sub("Each idea")] + out
    path = words.get("path") or {}
    if path.get("steps"):
        rows = [(st.get("title", ""), "<br>".join(P.inline(l) for l in st.get("lines") or [])) for st in path["steps"]]
        rows += [("Also", P.inline(path.get("also", "")))] + [("Open", P.inline(q)) for q in path.get("open") or []]
        out.append(_folded(f'🧭 {P.inline(path.get("title", "From here to G0")).lstrip("⑲").strip()}', P.inline(path.get("key", "")),
                           "".join(_line(k, v) for k, v in rows if v)))
    return "".join(out)


def _division(text, title):
    """The body of a face's `### N · <title>` division, up to the next division or setext heading."""
    m = re.search(r"(?ms)^### \d+ · %s[^\n]*\n(.*?)(?=^### \d+ · |^\S[^\n]*\n-{3,}\n|\Z)" % re.escape(title), text or "")
    return m.group(1) if m else ""


def _fields(body):
    """`**Label**: words` paragraphs and `- **Label**: words` or `1. **Label**: words` items → [(label, words)]."""
    out = []
    for par in re.split(r"\n\s*\n", body or ""):
        for item in (_items(par) or [" ".join(par.split())]):
            m = re.match(r"^\*\*(.+?)\*\*\s*:?\s*(.*)$", item.strip())
            if m:
                out.append((m.group(1).strip().rstrip(":"), m.group(2).strip()))
    return out


def _table(body, first):
    """The rows of a division's Markdown table whose first cell matches `first`, each a list of cells."""
    rows = [[c.strip() for c in line.strip().strip("|").split("|")] for line in (body or "").splitlines() if line.startswith("|")]
    return [r for r in rows if re.fullmatch(first, r[0])]


def _rq_blocks(body):
    """§3's `#### 3.N · Question N · RQn` blocks: (id, fields, {group: [item]}), an item a dict of its code, its
    `Name: sentence`, its other ` · ` parts and its indented `- **Label**: words` lines (a claim's Now, If it fails)."""
    out = []
    for m in re.finditer(r"(?ms)^#### [\d.]+ · Question \d+ · (RQ\d+)\s*\n(.*?)(?=^#### |\Z)", body or ""):
        fields, groups, group, last = [], {}, None, None
        for line in m.group(2).splitlines():
            g = re.match(r"^\*\*(Theories|Hypotheses|Potential claims|Potential contributions|Potential work|Tasks)\*\*\s*$", line.strip())
            if g:
                group, last = g.group(1), None
                groups[group] = []
                continue
            nested = re.match(r"^\s+- \*\*(.+?)\*\*\s*:\s*(.*)$", line)
            if nested and last is not None:
                last["more"][nested.group(1).strip().lower()] = nested.group(2).strip()
                continue
            item = re.match(r"^- \*\*(.+?)\*\*\s*(?::|·)\s*(.*)$", line)
            if not item:
                continue
            if group is None:
                fields.append((item.group(1), item.group(2).strip()))
                continue
            parts = [x.strip() for x in item.group(2).strip().split(" · ")]
            code = next((x for x in parts if re.fullmatch(r"C\d+", x)), item.group(1))
            said = next((x for x in parts if ":" in x), parts[-1] if parts else "")
            last = {"code": code, "said": said, "parts": parts, "more": {}}
            groups[group].append(last)
        out.append((m.group(1), fields, groups))
    return out


def _sub(title):
    """A subsection of a step's Result: a small grey heading over its folded cards (JL 261022: "for the results, should
    we also have the subsection as well? ... venue will be on subsection of the results")."""
    return (f'<h4 style="margin:20px 0 6px;font:600 12.5px system-ui,sans-serif;color:var(--mut);'
            f'letter-spacing:.04em;text-transform:uppercase">{esc(title)}</h4>')


def _map(root_title, root_text, branches):
    """A tree drawn as the draft's §1 mind map (JL 261022, of the Story and the Idea: "I want something like this"): the
    root box, each branch box with the line it hands to the next on the arrow below it, each leaf a code, a grey tag,
    its words and its evidence chips. Read-only, but it answers a click (JL 261023: "我点击这个 button 的时候，它就会 show
    more information"): a leaf opens its whole sentence under it, a branch opens its card below and scrolls to it. A
    branch is (id, title, [leaf html], hand-on) or (id, title, [leaf html], hand-on, the id of its card)."""
    from live.draft_steps import _mapview          # §1's look, shared by hai-mindmap's mapview.py
    PLAN_CSS, PLAN_JS = _mapview().CSS, _mapview().JS
    paras = []
    for k, b in enumerate(branches):
        bid, title, leaves, handon = b[:4]
        opens = f' data-open="{esc(b[4])}" title="open its card"' if len(b) > 4 and b[4] else ""
        paras.append(f'<div class=pm-para><div class="pm-node pm-pnode"{opens}><span class=pm-id>{bid}</span><b>{title}</b></div>'
                     f'<ul class=pm-leaves>{"".join(leaves)}</ul></div>'
                     + (f'<div class=pm-q>↓ {handon}</div>' if handon and k < len(branches) - 1 else ""))
    return (PLAN_CSS + MAP_RO + '<div style="overflow-x:auto;margin:4px 0 10px"><div class="pm pm-ro"><svg class=pm-wires aria-hidden=true></svg>'
            f'<div class="pm-node pm-root"><b>{root_title}</b>' + (f'<p>{root_text}</p>' if root_text else "")
            + f'</div><div>{"".join(paras)}</div></div></div>' + PLAN_JS)


# a read-only map's clicks: a leaf shows its whole text under it (click again to close), a branch opens its card
MAP_RO = """<style>.pm-ro .pm-leaves li[title]{cursor:pointer}.pm-ro .pm-leaves li[title]:hover .pm-t{color:var(--acc)}
.pm-ro .pm-pnode[data-open]{cursor:pointer}.pm-ro .pm-pnode[data-open]:hover{border-color:var(--acc)}
.pm-more{white-space:normal;max-width:680px;margin:3px 0 7px 38px;padding:6px 10px;border-left:2px solid var(--acc);
 background:var(--wash);color:var(--fg);font-size:13px;line-height:1.55;border-radius:0 6px 6px 0;cursor:auto}</style>
<script>(function(){if(window.__pmRo)return;window.__pmRo=1;
 document.addEventListener('click',function(e){var t=e.target;if(!t.closest)return;
  var n=t.closest('.pm-ro .pm-pnode[data-open]');
  if(n){var d=document.getElementById(n.dataset.open);if(d){d.open=true;d.scrollIntoView({behavior:'smooth',block:'start'});}return;}
  if(t.closest('.pm-more'))return;
  var li=t.closest('.pm-ro .pm-leaves li[title]');if(!li)return;
  var m=li.querySelector(':scope>.pm-more');
  if(m)m.remove();else{m=document.createElement('div');m.className='pm-more';m.textContent=li.getAttribute('title');li.appendChild(m);}
  if(window.pmDraw)window.pmDraw();});})();</script>"""


def _leaf(code, tag, words, chips="", note=""):
    """One leaf of a map: its code, a grey tag, its words, its chips; the whole sentence on hover."""
    return (f'<li{(" title=" + chr(34) + esc(note) + chr(34)) if note else ""}><span class=pm-s>{esc(code)}</span>'
            + (f'<span class=pm-role>{esc(tag)}</span>' if tag else "")      # no empty tag box (JL 261023: "干净一些")
            + f'<span class=pm-w><span class=pm-t>{words}</span>{chips}</span></li>')


VENUE_BRANCHES = (("The call", ("call", "editors", "window", "scope")),
                  ("What it asks", ("what it asks", "topics", "methods", "read first")),
                  ("The format", ("length", "words", "our budget", "submission", "same as")))


def _venue_map(venue_div, venues, held):
    """The target venue as a map: the venue in the root; its first frame split into the call, what it asks and the
    format (by each point's label), and each further frame (how the paper meets the call, why it is doable) a branch of
    its own; each point a leaf, its label the tag, its evidence rows as chips, the whole point on hover."""
    from live.draft_steps import INK

    def chip(e):
        state = held.get(e, "absent")
        ink = INK["need"] if state == "absent" else INK["cite"] if e.lower().startswith("ecite") else INK["value"]
        return f' <span class=pm-card style="color:{ink};border-color:{ink}66">{esc(e)}</span>'

    def leaf(point):
        label, _, words = point.partition(":") if re.match(r"^[^:]{1,80}:", point) else ("", "", point)
        words = re.sub(r"\s*\((?:E\w*\d+(?:, )?)+\)", "", words).strip()
        tag = " ".join(re.sub(r"\([^)]*\)|[\"“”]", "", label).replace(",", " ").split()[:2])
        return _leaf("", _clip(tag, 18), P.inline(_clip(words, 64)), _chips(re.findall(r"E(?:work|cite)\d+", point), chip), point)

    frames = list(re.finditer(r"(?ms)^#### (V\d+) · ([^\n]+)\n(.*?)(?=^#### |\Z)", venue_div))
    branches = []
    for k, m in enumerate(frames):
        points = _items(m.group(3))
        if k == 0:
            left = list(points)
            for name, keys in VENUE_BRANCHES:
                mine = [x for x in left if x.split(":", 1)[0].strip().lower().startswith(keys)]
                left = [x for x in left if x not in mine]
                if mine:
                    branches.append((esc(m.group(1)), esc(name), [leaf(x) for x in mine], ""))
            if left:
                branches.append((esc(m.group(1)), "More", [leaf(x) for x in left], ""))
        elif points:
            branches.append((esc(m.group(1)), P.inline(m.group(2).strip()[:1].upper() + m.group(2).strip()[1:]), [leaf(x) for x in points], ""))
    v = venues[0]
    root = f"🧭 {P.inline(v[1])}" if len(v) > 1 else "🧭 The venue"
    return _map(root, P.inline(v[3]) if len(v) > 3 else "", branches) if branches else ""


def _clip(text, n):
    """At most n characters, cut at a word; the whole text stays on the leaf's hover."""
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= n else text[:n - 1].rsplit(" ", 1)[0].rstrip(",;:") + " …"


# a hypothesis's theory said in one short word on its tag, as the draft map's roles are (JL 261023, of the draft's map:
# "为什么别人的就是看起来那么的干净 ... 你能够做得干净一些吗？")
SHORT_THEORY = (("consideration", "consideration"), ("institutional", "logics"), ("bias in", "bias in/out"),
                ("copy of", "bias in/out"), ("cumulative", "cumulative"), ("safety", "safety"), ("long tail", "long tail"),
                ("superstar", "superstars"), ("four ways", "regulation"), ("oversight", "oversight"),
                ("many hands", "many hands"), ("remedial", "remedial"), ("equality", "fairness"), ("availability", "availability"))


def _short_tag(text):
    low = (text or "").lower()
    found = sorted((low.find(key), short) for key, short in SHORT_THEORY if key in low)   # the theory named first wins
    hit = found[0][1] if found else ""
    return hit or _clip(re.sub(r"[\"()]", "", text or "").split(";")[0], 16)


def _chips(codes, chip, keep=3):
    """At most `keep` evidence chips on a leaf, then a grey +n."""
    codes = list(dict.fromkeys(codes))
    more = f' <span class=mut style="font-size:11px">+{len(codes) - keep}</span>' if len(codes) > keep else ""
    return "".join(chip(e) for e in codes[:keep]) + more


def _outline(body):
    """A nested Markdown list as a tree: [(text, [children])], two spaces of indent a level."""
    root, stack = [], [(-1, None)]
    for line in (body or "").splitlines():
        m = re.match(r"^(\s*)- (.*\S)", line)
        if not m:
            continue
        depth, node = len(m.group(1)) // 2, (m.group(2), [])
        while stack and stack[-1][0] >= depth:
            stack.pop()
        (stack[-1][1][1] if stack[-1][1] else root).append(node)
        stack.append((depth, node))
    return root


def _tree_map(root_title, root_text, nodes):
    """A mind map of any depth (JL 261023, of the data flow: "You can make more layers of the mindmap tree"): a node
    with children is a box wired to them, a node without is a leaf; a line `title · note` puts its note grey beside it,
    `code · title · note` adds a code, and a leading ✅ 🔶 ⬜ 🙋 ❗ marks its state. A click opens a leaf's whole line."""
    from live.draft_steps import _mapview          # §1's look, shared by hai-mindmap's mapview.py
    PLAN_CSS = _mapview().CSS

    def split(text):
        parts = [x.strip() for x in text.split(" · ")]
        code = parts.pop(0) if len(parts) > 2 and len(parts[0]) <= 14 else ""
        return code, parts[0], " · ".join(parts[1:])

    def leaf(text):
        code, title, note = split(text)
        mark = note[:1] if note[:1] in "✅🔶⬜🙋❗" else ""          # its state first, as the story's RQ boxes show theirs
        note = note[1:].strip() if mark else note
        # "n of m folds" as a badge beside the name (JL 261023: "能把这个 n of n folds 变得显眼一些？")
        # and "n of m runs" the same way (JL 261024, the ScalingGlucose data flow: "I want you to make things like this")
        folds = re.search(r"(\d+) of (\d+) (folds|runs)[;:,]?\s*", note)
        badge = ""
        if folds:
            n, m = int(folds.group(1)), int(folds.group(2))
            ink = "#2b8a3e" if n == m else "#e8590c" if n else "#adb5bd"
            badge = (f' <span style="display:inline-block;margin:0 4px;padding:0 8px;border-radius:10px;background:{ink};'
                     f'color:#fff;font:700 12px/1.6 system-ui,sans-serif">{n} / {m} {folds.group(3)}</span>')
            note = (note[:folds.start()] + note[folds.end():]).strip(" ;,:")
        return _leaf(code, "", (f"{mark} " if mark else "") + _tree_title(title, 48) + badge + (f' <span class=mut style="font-size:12px">{P.inline(_clip(note, 70))}</span>' if note else ""),
                     note=_TREE_LINK.sub(r"\1", text.split(" · ")[0]) + text[len(text.split(" · ")[0]):])

    def row(text, kids):
        code, title, note = split(text)
        boxes = "".join(row(t, k) for t, k in kids if k)
        leaves = "".join(leaf(t) for t, k in kids if not k)
        return (f'<div class=tr-row><div class="pm-node tr-box"{(" title=" + chr(34) + esc(note) + chr(34)) if note else ""}>'
                + (f'<span class=pm-id>{esc(code)}</span>' if code else "") + f'<b>{_tree_title(title, 200)}</b>'
                + (f'<span class=tr-note>{P.inline(_clip(note, 60))}</span>' if note else "")
                + f'</div><div class=tr-kids>{boxes}' + (f'<ul class=pm-leaves>{leaves}</ul>' if leaves else "") + '</div></div>')

    body = "".join(row(t, k) for t, k in nodes)
    return (PLAN_CSS + MAP_RO + TREE_CSS + '<div style="overflow-x:auto;margin:4px 0 10px"><div class="tr pm-ro"><svg class=tr-wires aria-hidden=true></svg>'
            f'<div class=tr-row><div class="pm-node pm-root tr-box"><b>{root_title}</b>' + (f'<p>{root_text}</p>' if root_text else "")
            + f'</div><div class=tr-kids>{body}</div></div></div></div>' + TREE_JS)


TREE_CSS = """<style>.tr{position:relative;width:max-content;min-width:100%;padding:8px 4px;box-sizing:border-box}
.tr-wires{position:absolute;left:0;top:0;pointer-events:none;overflow:visible}.tr-wires path{fill:none;stroke:var(--mut);stroke-opacity:.45;stroke-width:1.4}
.tr-row{display:grid;grid-template-columns:auto auto;gap:0 44px;align-items:center;margin:5px 0}
.tr-kids{display:flex;flex-direction:column;justify-content:center}
.tr-box{padding:8px 12px;font-size:14px;line-height:1.35;max-width:230px}.tr-box.pm-root{max-width:250px}
.tr-note{display:block;font-size:11.5px;color:var(--mut);margin-top:2px}
@media(max-width:1000px){.tr,.tr-row{display:block;width:auto}.tr-wires{display:none}.tr-kids{padding-left:14px;border-left:2px solid var(--line);margin:4px 0}}</style>"""
TREE_JS = """<script>(function(){if(window.__trMap)return;window.__trMap=1;
 function wire(a,b,o,leaf){var p=a.getBoundingClientRect(),q=b.getBoundingClientRect();
  var x1=p.right-o.left,y1=p.top+p.height/2-o.top,x2=q.left-o.left-6,y2=(leaf?q.top+12:q.top+q.height/2)-o.top,m=(x1+x2)/2;
  return '<path d="M'+x1+','+y1+' C'+m+','+y1+' '+m+','+y2+' '+x2+','+y2+'"/>';}
 function draw(){document.querySelectorAll('.tr').forEach(function(t){var svg=t.querySelector('.tr-wires');
  if(!t.offsetParent||getComputedStyle(svg).display==='none')return;var o=t.getBoundingClientRect(),d='';
  svg.setAttribute('width',o.width);svg.setAttribute('height',o.height);
  t.querySelectorAll('.tr-row').forEach(function(r){var box=r.querySelector(':scope>.tr-box'),k=r.querySelector(':scope>.tr-kids');
   k.querySelectorAll(':scope>.tr-row>.tr-box').forEach(function(c){d+=wire(box,c,o);});
   k.querySelectorAll(':scope>ul>li').forEach(function(l){d+=wire(box,l,o,true);});});
  svg.innerHTML=d;});}
 window.addEventListener('resize',draw);window.addEventListener('load',draw);setTimeout(draw,60);
 document.addEventListener('toggle',function(){setTimeout(draw,0);},true);document.addEventListener('click',function(){setTimeout(draw,0);});
 window.trDraw=draw;})();</script>"""


TREE_ROUTE = "/_board/workbench"   # live.frame.ROUTE: a folder's workbench page
_TREE_LINK = re.compile(r"^\[([^\]]+)\]\(([^)\s]+)\)$")


def _tree_title(title, n):
    """A tree node's title, clipped to n characters; a title written `[words](url)` is a link on its clipped words."""
    m = _TREE_LINK.match(title.strip())
    if not m:
        return P.inline(_clip(title, n))
    return f'<a href="{esc(m.group(2))}" target="_top">{P.inline(_clip(m.group(1), n))}</a>'


def _expand_csv(nodes, root):
    """A tree line `@csv <path from the SPACE root> · <column>=<value> · <label column> · <value column>` becomes one leaf
    per matching row, `label · value`, read now, so a count in the tree is never typed (JL 261023: "我们 fold00 到 fold09
    到底跑了几个了，你也要说明一下"). An optional fifth part names a column holding a folder from the SPACE root; a row
    that has one gets its label as a link, `[label](<that folder's workbench page>)`, which the tree opens (JL 261101,
    the PaperFlow tree: "update the link for it")."""
    import csv as _csv
    from urllib.parse import urlencode
    out = []
    for text, kids in nodes:
        if not text.startswith("@csv "):
            out.append((text, _expand_csv(kids, root)))
            continue
        parts = [x.strip() for x in text[5:].split(" · ")]
        path = (Path(root) / parts[0]) if root else Path(parts[0])
        if len(parts) < 4 or not path.is_file():
            out.append((f"❗ {path.name} · not on disk", []))
            continue
        key, _, want = parts[1].partition("=")
        with path.open(encoding="utf-8") as fh:
            rows = list(_csv.DictReader(fh))
        for r in rows:
            if r.get(key.strip()) == want.strip():
                label, to = r.get(parts[2], ""), (r.get(parts[4], "") if len(parts) > 4 else "").strip()
                if to:
                    label = f"[{label}]({TREE_ROUTE}?{urlencode({'path': to})})"
                out.append((f"{label} · {r.get(parts[3], '')}", []))
    return out


def _flow_sections(text, root=None, division="Data tree", head="The data, as a tree"):
    """A Plan topic's tree division drawn as a many-layered mind map: the DataFlow topic's "Data tree", or the
    PaperFlow topic's "Paper tree" (JL 261024: the paper flow drawn as the data flow is)."""
    tree = _expand_csv(_outline(_division(text, division)), root)
    if not tree:
        return ""
    (root, kids), rest = tree[0], tree[1:]
    title, _, note = root.partition(" · ")
    return _sub(head) + _tree_map(P.inline(title), P.inline(note), kids + rest)


def _story_map(text):
    """§3 drawn as a mind map: the paper's question in the root, each research question a branch (its state and name),
    its hypotheses and claims the leaves (a hypothesis tagged with its theory and chipped with the evidence rows that
    test it: violet a row from our own Runs, blue a cited paper, red a row still absent), and on the arrow between two
    questions what the paper can say once the first is answered (the narrative)."""
    from live.draft_steps import INK
    rqs = _division(text, "Research Questions")
    asked = next((v for k, v in _fields(rqs.split("####")[0]) if k.lower().startswith("the paper's question")), "")
    held = {r[0]: r[-1].lower() for r in _table(_division(text, "Evidence Basis and Boundaries"), r"E\w*\d+")}
    story = re.search(r"(?ms)^\*\*The narrative, if the questions are answered\*\*.*?\n\n(.*?)(?:\n\s*\n(?=\S)(?!\d+\. )|\Z)", rqs)
    said = {}
    for line in _items(story.group(1)) if story else []:
        for rq in re.findall(r"\((RQ\d+)", line):
            said.setdefault(rq, re.split(r"(?<=\w)[:;]|, yet |, but ", line, maxsplit=1)[0].strip())

    def chip(e):
        state = held.get(e, "absent")
        ink = INK["need"] if state == "absent" else INK["cite"] if e.lower().startswith("ecite") else INK["value"]
        return f' <span class=pm-card style="color:{ink};border-color:{ink}66">{esc(e)}</span>'

    branches = []
    for rq, fields, groups in _rq_blocks(rqs):
        f = {k.lower(): v for k, v in fields}
        state = f.get("answer state", "")
        mark = state.split()[0] if state[:1] in "✅🔶⬜❗🟡" else ""
        leaves = []
        # its theories first (JL 261023: "You have C, I think you also need the Theory as well"): code, role, name;
        # short, as the draft map is, with the whole sentence and its test on hover
        for t in groups.get("Theories", []):
            # tagged "theory", as a claim is tagged "claim" (JL 261023: "is the mechanism you mean the theory? could you
            # name it to 'theory'?"); its role for this question (core, rival, ...) opens with its sentence on a click
            role = t["parts"][0] if len(t["parts"]) > 1 and ":" not in t["parts"][0] else ""
            name = re.sub(r"\s*\([^()]*\d{4}[^()]*\)", "", t["said"].split(":", 1)[0]).split(", with ")[0].strip()
            note = (f"Role here: {role} · " if role else "") + " · ".join(x for x in t["parts"] if x != role)
            leaves.append(_leaf(t["code"], "theory", f"<i>{P.inline(_clip(name, 44))}</i>", note=note))
        for h in groups.get("Hypotheses", []):
            name = h["said"].split(":", 1)[0]
            theory = re.search(r"\(([^()]*)\)\s*$", h["said"].split(" · tested by")[0])
            tested = next((x for x in h["parts"] if x.startswith("tested by")), "")
            leaves.append(_leaf(h["code"], _short_tag(theory.group(1)) if theory else "", P.inline(_clip(name, 44)),
                                _chips(re.findall(r"E\w*\d+", tested), chip), " · ".join(x for x in (h["said"], tested) if x)))
        for c in groups.get("Potential claims", []):
            leaves.append(_leaf(c["code"], "claim", f'<b>{P.inline(_clip(c["said"].split(":", 1)[0], 44))}</b>', note=c["said"]))
        branches.append((f"{esc(mark)} {esc(rq)}", P.inline(f.get("name", "")), leaves, "", f"story-{rq.lower()}"))
    # on the arrow, the question the next research question asks, short, as the draft's "why should physicians care?"
    branches = [(b, n, l, (branches[k + 1][1][:1].lower() + branches[k + 1][1][1:]) if k + 1 < len(branches) else "", a)
                for k, (b, n, l, _h, a) in enumerate(branches)]
    return _map("📖 The paper's question", P.inline(asked), branches) if branches else ""


def _story_sections(text):
    """A Story topic's face laid out as its drawing (JL 261020: "让它的 layout 跟我们 draw 里面长得比较相似一些"): the
    paper's question in the key box, then a folded card per research question, opened as the drawing's row (the question
    → what we expect, and why → what the paper can say), then the narrative, stakes, what we will not claim, the evidence,
    the work and where it could go, each folded (hai-paper-story §1 to §9)."""
    out = []
    ident, pitch, rqs = _fields(_division(text, "Identity")), _fields(_division(text, "Pitch")), _division(text, "Research Questions")
    asked = next((v for k, v in _fields(rqs.split("####")[0]) if k.lower().startswith("the paper's question")), "")
    one = next((v for k, v in ident if k.lower() == "one sentence"), "")
    bounds = _division(text, "Evidence Basis and Boundaries")
    ev = _table(bounds, r"E\w*\d+")
    held = {r[0]: r[-1].lower() for r in ev}
    if asked or one or pitch:
        out.append(_folded("📖 The paper's question", P.inline(asked), "".join(_line(k, P.inline(v)) for k, v in
                                                                         [("In a sentence", one)] + pitch if v)))
    cards = []
    for rq, fields, groups in _rq_blocks(rqs):
        f = {k.lower(): v for k, v in fields}
        state = f.get("answer state", "")
        chip = state.split()[0] if state[:1] in "✅🔶⬜❗🟡" else ""
        asked_rq = re.sub(r"\s*\(RQ\d+[a-z]:.*$", "", f.get("research question", ""))
        col1 = (_key(f"<b>Why it matters</b> · {P.inline(_first_sentence(f.get('why it matters', '')))}")
                + "".join(_key(f"<b>{k}</b> · {P.inline(_first_sentence(v))}") for k, v in (("How", f.get("question", "")),
                          ("Now", re.sub(r"^\S+\s+", "", state) if chip else state)) if v))
        hyps, in_hand = [], 0
        for h in groups.get("Hypotheses", []):
            tested = next((x for x in h["parts"] if x.startswith("tested by")), "")
            rows = [held.get(e.strip()) for e in re.findall(r"E\w*\d+", tested)]
            mark = "✅" if rows and all(r == "established" for r in rows) else "🔶" if any(r in ("established", "provisional") for r in rows) else "⬜"
            in_hand += mark == "✅"
            hyps.append(_mini(f"{mark} {esc(h['code'])} · {P.inline(h['said'].split(':', 1)[0])}",
                              P.inline(h["said"].split(":", 1)[1].strip() if ":" in h["said"] else ""), esc(tested)))
        n = len(hyps)
        theories = [_mini(f"{esc(t['code'])} · {P.inline(t['said'].split(':', 1)[0])}",
                          P.inline(t["said"].split(":", 1)[1].strip() if ":" in t["said"] else ""),
                          " · ".join(esc(x) for x in t["parts"] if x != t["said"]))
                    for t in groups.get("Theories", [])]
        col2 = ((_key(f"{len(theories)} theor{'y' if len(theories) == 1 else 'ies'}") + "".join(theories) if theories else "")
                + ((_key(f"{n} hypothes{'is' if n == 1 else 'es'}: {in_hand} with evidence in hand, {n - in_hand} waiting for a Run")
                    + "".join(hyps)) if hyps else "")) or '<span class=mut>none yet</span>'
        claims = [_mini(f"{esc(c['code'])} · {P.inline(c['said'].split(':', 1)[0])}",
                        P.inline(c["said"].split(":", 1)[1].strip() if ":" in c["said"] else ""),
                        " · ".join(f"{esc(k.capitalize())}: {P.inline(v)}" for k, v in c["more"].items() if k in ("now", "if it fails")))
                  for c in groups.get("Potential claims", [])]
        col3 = (_key(P.inline(_first_sentence(f.get("if answered", "")))) if f.get("if answered") else "") + "".join(claims)
        work = " · ".join(esc(w["code"]) for w in groups.get("Potential work", []))
        body = (_cols([("❓ The question", col1), ("🔮 Theory, and what we expect", col2), ("📣 What the paper can say", col3 or "—")])
                + (f'<p class=mut style="font-size:12.5px;margin:8px 0 0">Work: {work}</p>' if work else ""))
        cards.append(_folded(f'{esc(chip)} <b>{esc(rq)} · {esc(f.get("name", ""))}</b>', P.inline(asked_rq), body, f"story-{rq.lower()}"))
    out = [_sub("The questions"), _story_map(text)] + out + cards
    story = re.search(r"(?ms)^\*\*The narrative, if the questions are answered\*\*.*?\n\n(.*?)(?:\n\s*\n(?=\S)(?!\d+\. )|\Z)", rqs)
    lines = _items(story.group(1)) if story else []
    more = []
    if lines:
        more.append(_folded("<b>📜 The narrative, if the questions are answered</b>", f"{len(lines)} steps",
                            "".join(_line(str(k), P.inline(x)) for k, x in enumerate(lines, 1))))
    stakes = _fields(_division(text, "Stakes"))
    if stakes:
        more.append(_folded("<b>🎯 Stakes</b>", " · ".join(esc(k) for k, _v in stakes), "".join(_line(k, P.inline(v)) for k, v in stakes)))
    nots = _items(bounds.split("**We will not claim**", 1)[1]) if "**We will not claim**" in bounds else []
    if nots:
        more.append(_folded("<b>🚫 What we will not claim</b>", f"{len(nots)} boundaries",
                            '<ul style="margin:0;padding-left:18px">' + "".join(f"<li>{P.inline(x)}</li>" for x in nots) + "</ul>"))
    if ev:
        more.append(_folded("<b>🧾 The evidence</b>", "",   # each row shows its own state; no "N established" tally
                            "".join(_line(r[0], f"{P.inline(r[1])} <span class=mut>· {esc(r[-1])}</span>") for r in ev)))
    work = _table(_division(text, "Task Roadmap"), r"T\d+")
    if work:
        more.append(_folded("<b>🛠 The work</b>", "",       # each row shows its own state; no "N done" tally
                            "".join(_line(r[0], f"{P.inline(r[1])} <span class=mut>· {esc(r[3] if len(r) > 3 else '')}</span>") for r in work)))
    venue_div = _division(text, "Venues")
    venues = _table(venue_div, r"V\d+")
    if venues:
        # the venue drawn as the questions' map (JL 261023: "could you make this to be the layout like this as well?"),
        # inside its own card, under the venue list ("this should be within the section, not out of the section")
        more.append(_folded("<b>🧭 Where the story could go</b>", f"{len(venues)} venues · {esc(venues[0][1])} first",
                            "".join(_line(r[0], f"<b>{P.inline(r[1])}</b> <span class=mut>· {esc(r[2])} · leads with "
                                               f"{esc(r[4] if len(r) > 4 else '')}</span>") for r in venues)
                            + _venue_map(venue_div, venues, held)))
    # each venue's frames (the call, how the paper meets it, why it is doable) are read in the map only; their bullet
    # cards were dropped (JL 261023: "I don't need this ... otherwise, this is very hard to read")
    # the Result in subsections (JL 261022): the questions, the narrative, why it matters, the evidence, the venue
    groups = [("The narrative", ("📜",)), ("Why it matters, and its limits", ("🎯", "🚫")),
              ("The evidence and the work", ("🧾", "🛠")), ("The venue", ("🧭",))]
    for title, marks in groups:
        mine = [c for c in more if any(f"<b>{mk}" in c for mk in marks)]
        if mine:
            out += [_sub(title)] + mine
    return "".join(out)
