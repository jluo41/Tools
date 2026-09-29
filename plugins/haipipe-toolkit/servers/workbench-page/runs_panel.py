"""Runs beside the content (Page 0.118): one Runs panel per Space.

Each Space (Draft, Evidence, Delivery) shows its own runs in a column on the
right of its content: on top the run types that the Run cards give that Space
(`🔘 BUTTON` lines in haipipe-page-workflow/ref/run-cards.md), below them one run with its
prompt to copy, its process and its results. A selected paragraph or item
narrows the panel to that target. A panel folds to one line.

The panel starts nothing by itself: Rerun and "+ New Run" copy a prompt the
person runs in a Claude or Codex session, which records who started it.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from src.item_table import short_name
from src.run_folders import folder_for, space_of
from src import run_names

CARDS = Path(__file__).resolve().parents[2] / "skills" / "page" / "haipipe-page-workflow" / "ref" / "run-cards.md"
_CARD = re.compile(r"^## `(?P<card>[^`]+)`", re.M)
_BUTTON = re.compile(r"^🔘 BUTTON\s+(?P<label>.+?)\s+·\s+(?P<space>[A-Z][A-Za-z]+)\s+·\s+"
                     r"(?P<pattern>\S.*?)(?:\s+·\s+views\s+(?P<views>[\w ]+?))?\s*$")
_PROMPT = re.compile(r"^💬 PROMPT\s+(?P<prompt>.+?)\s*$")
_SKILL = re.compile(r"^🧩 SKILL\s+(?P<skills>.+?)\s*$")
_RUN_SKILLS = re.compile(r"(?m)^skills?:\s*(?P<skills>.+?)\s*$")
_STATE = {"done": "Closed", "held": "Held", "waiting": "Awaiting you", "running": "Running",
          "review-ready": "Awaiting you", "open": "Running"}


def _e(value) -> str:
    return html.escape(str(value or ""), quote=True)


def run_types(cards: Path = CARDS) -> list[dict]:
    """-> [{card, label, space, pattern, prompt}] from the Run cards, in card order."""
    try:
        text = cards.read_text(encoding="utf-8")
    except OSError:
        return []
    types = []
    for match in _CARD.finditer(text):
        end = text.find("\n## ", match.end())
        body = text[match.end():end if end >= 0 else len(text)]
        prompt = next((m["prompt"] for line in body.splitlines() if (m := _PROMPT.match(line))), "")
        # `🧩 SKILL a · b` is the card's; `🧩 SKILL <button label>: a · b` is one button's.
        skills, per_button = "", {}
        for line in body.splitlines():
            found = _SKILL.match(line)
            if not found:
                continue
            label, sep, names = found["skills"].partition(":")
            if sep and not label.strip().startswith("haipipe-"):
                per_button[label.strip()] = names
            elif not skills:
                skills = found["skills"]
        for line in body.splitlines():
            button = _BUTTON.match(line)
            if button:
                types.append({"card": match["card"], "label": button["label"], "space": button["space"],
                              "pattern": button["pattern"], "prompt": prompt,
                              "skills": _skill_list(per_button.get(button["label"], skills)),
                              "views": " ".join((button["views"] or "").split())})
    return types



def _skill_list(text: str) -> list[str]:
    """`haipipe-page-writing · haipipe-writing` → both names, without a leading slash."""
    return [s.strip().lstrip("/") for s in re.split(r"[·,]", text or "") if s.strip()]


def _run_skills(row: dict, kind: dict) -> list[str]:
    """The skills a run used: a `skills:` line in its ticket or runtime, else its run type's."""
    for path in (row.get("ticket"), row.get("runtime")):
        path = Path(str(path or ""))
        if path.suffix in {".md", ".yaml", ".yml"} and path.is_file():
            found = _RUN_SKILLS.search(path.read_text(encoding="utf-8", errors="replace")[:2000])
            if found:
                return _skill_list(found["skills"])
    return list(kind.get("skills") or [])


def _skills_html(skills: list[str]) -> str:
    return ('<p class=run-skill>Skill %s</p>' % " · ".join("<code>%s</code>" % _e(s) for s in skills)
            if skills else "")

def _fill(template: str, **values) -> str:
    return re.sub(r"\{(\w+)\}", lambda m: str(values.get(m.group(1), m.group(0))), template or "")


def _ticket_name(row: dict) -> str:
    ticket = row.get("ticket")
    return Path(str(ticket)).name if ticket else str(row.get("global_id") or row.get("run_id") or "")


def _run_id(row: dict) -> str:
    return str(row.get("global_id") or row.get("run_id") or "").split(" ")[-1]


def row_space(row: dict) -> str:
    ticket = row.get("ticket")
    if ticket:
        return space_of(ticket)
    folder = folder_for(_run_id(row))
    return space_of("runs/%s/x" % folder) if folder else "other"


def _targets(row: dict) -> str:
    """Addresses and Evidence Item ids a run touches (C1.P1.B2 also adds C1.P1; E40)."""
    found = set(re.findall(r"C\d+(?:\.P\d+)?(?:\.B\d+)?", str(row.get("target") or "") + " " +
                           str(row.get("_items") or "")))
    found |= set(re.findall(r"\bE\d+\b", str(row.get("_items") or "")))
    found |= set(str(row.get("_keys") or "").split())      # the Paper workbench names its own keys
    found |= {re.sub(r"\.B\d+$", "", t) for t in found}
    ticket = Path(str(row.get("ticket") or ""))
    if ticket.suffix == ".md" and ticket.is_file():
        head = ticket.read_text(encoding="utf-8", errors="replace")[:1500]
        for item in re.findall(r"(?m)^item:\s*(E\d+)(-[A-Z]+-[\w-]+)?", head):
            found |= {item[0], item[0] + item[1]}
    return " ".join(sorted(found))


def _number(row: dict) -> tuple:
    digits = re.findall(r"\d+", _run_id(row))
    return tuple(int(d) for d in digits[:1]) or (0,)


def _rel(path, base: Path) -> str:
    if not path:
        return ""
    try:
        return Path(str(path)).resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return str(path)


def _result_files(row: dict) -> list[str]:
    if not row.get("result_path"):       # Path("") is the working folder, not "no result"
        return []
    folder = Path(str(row.get("result_path")))
    if folder.is_file():
        folder = folder.parent
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir() if p.is_file() and not p.name.startswith("."))[:8]


_FORMAT = re.compile(r"^(?:rd\d+_|run-delivery-)(web|webpage|latex|word|slides?)(?:_|$)", re.I)
# What the panel calls a run (JL 260927: "just call it complete name"). The file
# names on disk keep their short prefixes; the real id shows on hover.
_DISPLAY = (
    (r"^rp-struct-(\d+)", "run-structure-%s"), (r"^rp-sec-(\d+)", "run-section-%s"),
    (r"^rp-para-(\d+)", "run-paragraph-%s"), (r"^rp-scratch-(\d+)", "run-scratch-%s"),
    (r"^rp-revise-(\d+)", "run-revise-%s"), (r"^rp-auto-(\d+)", "run-auto-write-%s"),
    (r"^rp-embed-(\d+)", "run-evidence-embed-%s"), (r"^rp-context-(\d+)", "run-context-%s"),
    (r"^rp-check-(\d+)", "run-check-%s"), (r"^re-cite-(\d+)", "run-citation-%s"),
    (r"^re-value-(\d+)", "run-value-%s"), (r"^re-display-(\d+)", "run-display-%s"),
    (r"^ridea-(\d+)", "run-idea-%s"), (r"^rclaim-(\d+)", "run-claim-%s"),
    (r"^rtask-(\d+)", "run-task-%s"), (r"^rnarra-(\d+)", "run-narrative-%s"),
)


def display_name(run_id: str) -> str:
    """`rp-struct-01` → `run-structure-01`, `rd01_latex` → `run-latex-01`; other ids as they are."""
    for pattern, name in _DISPLAY:
        match = re.match(pattern, run_id or "")
        if match:
            return name % match.group(1)
    build = re.match(r"^rd(\d+)_(web|latex|word|slides?)\b", run_id or "", re.I)
    if build:
        return "run-%s-%s" % (build.group(2).lower(), build.group(1))
    return run_id


def _card_views(row: dict) -> str:
    """The Delivery format tab a build run belongs to ("" = every tab)."""
    match = _FORMAT.match(_run_id(row))
    return {"slide": "slides", "webpage": "web"}.get(match.group(1).lower(), match.group(1).lower()) if match else ""


def _card_html(row: dict, index: int, kind: dict, base: Path, fill: dict) -> str:
    run = _run_id(row)
    state = _STATE.get(str(row.get("status") or "").lower(), str(row.get("status") or "unknown"))
    target = str(row.get("target") or "whole page")
    ticket = _rel(row.get("ticket"), base)
    result = str(row.get("result") or _rel(row.get("result_path"), base))
    folder = re.sub(r"/[^/]+\.(?:ya?ml|md|json)$", "", result)
    prompt = _fill(kind["prompt"], target=target, button=kind["label"], run=run, **fill)
    prompt = "%s\n\nContinue %s. Ticket: %s · Result: %s" % (prompt, run, ticket or "none", result or "none")
    rerun = "Rerun %s as a new %s run.\n%s" % (run, kind["label"], _fill(kind["prompt"], target=target,
                                                                       button=kind["label"], run=run, **fill))
    files = "".join("<li><code class=repo-path>%s</code></li>" % _e(f) for f in _result_files(row))
    return (
        '<article class=run-card data-type="%d" data-run="%s" data-name="%s" data-targets="%s" '
        'data-state="%s" data-views="%s" data-label="%s" hidden>'
        '<header><b title="%s">%s</b><span class="run-state st-%s">%s</span>'
        '<button type=button class=run-copy data-copy="%s">Rerun</button></header>%s'
        '<details class=run-prompt-box><summary>Prompt '
        '<button type=button class=run-copy data-copy="%s">Copy</button></summary>'
        '<pre class=run-prompt>%s</pre></details>'
        '<h4>Running process</h4><div class=run-process>%s%s</div>'
        '<h4>Results</h4><div class=run-results><code class=repo-path>%s</code><ul>%s</ul></div>'
        '</article>'
        % (index, _e(run), _e(row.get("_display") or display_name(run)), _e(_targets(row)),
           _e(state.lower().replace(" ", "-")), _e(row["_views"] if "_views" in row else _card_views(row)),
           _e(state), _e(run),
           _e(row.get("_display") or display_name(run)),
           _e(state.lower().replace(" ", "-")), _e(state), _e(rerun), _skills_html(_run_skills(row, kind)),
           _e(prompt), _e(prompt),
           _e(state), (" · " + _e(row.get("goal"))) if row.get("goal") else "",
           _e(folder or "no result yet"), files))


def _paper_run_key(run_id: str) -> str:
    """`pj02t01r01_rx_variation` or `p.j02.t01.r01` → `pj02t01r01`; other ids → ""."""
    match = re.match(r"^p[._]?j(\d+)[._]?t(\d+)[._]?r(\d+)", run_id or "", re.I)
    return "pj%st%sr%s" % match.groups() if match else ""


_KIND_WORD = {"cite": "citation", "value": "value", "display": "display",
              "citations": "citation", "values": "value", "displays": "display"}


def _ticket_item(row: dict) -> str:
    """The Evidence Item a run serves: `E25` from its ticket's `item:` line."""
    ticket = Path(str(row.get("ticket") or ""))
    if ticket.suffix == ".md" and ticket.is_file():
        match = re.search(r"(?m)^item:\s*(E\d+)", ticket.read_text(encoding="utf-8", errors="replace")[:1500])
        if match:
            return match.group(1)
    return ""


def _name_by_item(rows: list[dict]) -> None:
    """Name each evidence run by the item it serves: `run-Evalue25`, then `run-Evalue25-2`.

    An item's first run (older Paper-local runs come first) takes the plain name;
    later runs for the same item count up.
    """
    groups: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        run = _run_id(row)
        if run_names.is_run_name(run):
            continue                      # a readable name is shown as it is (JL 260928)
        served = row.get("_served") or {}
        kind = re.match(r"^re-(cite|value|display)-", run)
        word = _KIND_WORD.get(kind.group(1) if kind else served.get("tab", ""), "")
        item = served.get("item") or _ticket_item(row)
        if word and item:
            groups.setdefault((word, item), []).append(row)
    for (word, item), members in groups.items():
        members.sort(key=lambda r: (0 if _paper_run_key(_run_id(r)) else 1, _number(r)))
        for n, row in enumerate(members, 1):
            kind = {"citation": "CITE", "value": "VALUE", "display": "DISPLAY"}[word]
            row["_display"] = "run-%s%s" % (short_name(item, kind), "" if n == 1 else "-%d" % n)


_SUPPORT_PROMPT = ("/haipipe-task {run}: show its ticket, runtime and Result, and say whether the Result "
                   "still supports {target} on {page}.")
_DISCOVERY_PROMPT = ("/haipipe-discovery {run}: show its Result Card and say whether it still supports "
                     "{target} on {page}.")


def _support_rows(runs: list[dict]) -> list[dict]:
    """Supporting Runs (live.runs.supporting_task_runs) as panel rows: named by their ticket,
    selected by their address, prompted with the Evidence Items they feed."""
    out = []
    for run in runs:
        ticket = str(run.get("ticket") or "")
        refs = list(run.get("refs") or [])
        out.append(dict(run, _display=Path(ticket).stem if ticket else run.get("run_id"),
                        _keys=str(run.get("compact_id") or ""), _views="supporting",
                        target=", ".join(refs) or str(run.get("target") or "")))
    return out


def panel_html(page_src: Path, space: str, rows: list[dict], types: list[dict], *,
               plan_name: str, extra: str = "", run_tabs: dict[str, str] | None = None,
               supporting: list[dict] | None = None) -> str:
    """One Space's Runs panel: run types on the left, the selected run on the right.

    On the Evidence Space, `supporting` (the Page's Supporting Runs) is one more run
    type, shown on the Supporting Runs tab."""
    base = page_src.parent
    fill = {"page": page_src.stem, "plan": plan_name}
    mine = [t for t in types if t["space"].lower() == space]
    # A run belongs here by its folder, or by a button of this Space (the Page
    # CHECK run also shows under Delivery).
    rows = [r for r in rows if row_space(r) == space
            or any(re.search(t["pattern"], _ticket_name(r)) for t in mine)]
    if space == "delivery":
        # One Run per lane (JL 260928): the fixed run-delivery-<lane>. Older numbered
        # Delivery Runs (rdNN_*) stay on disk and in the All-runs view, not here.
        rows = [r for r in rows if not re.match(r"rd\d+_", _ticket_name(r), re.I)]
    buckets = [[] for _ in mine]
    other = []
    for row in sorted(rows, key=_number, reverse=True):
        name = _ticket_name(row)
        hit = next((i for i, t in enumerate(mine) if re.search(t["pattern"], name)), None)
        served = ((run_tabs or {}).get(_paper_run_key(_run_id(row)) or _paper_run_key(name))
                  or (run_tabs or {}).get(_run_id(row)) or (run_tabs or {}).get(Path(name).stem))
        if served:
            # An older Paper-local evidence run (pj..t..r..) joins the tab of the
            # Evidence Item it serves, and selecting that item finds it.
            row = dict(row, _items=" ".join(x for x in (served["item"], served["target"]) if x),
                       _served=served)
        if hit is None and served:
            hit = next((i for i, t in enumerate(mine) if served["tab"] in t.get("views", "").split()), None)
        (buckets[hit] if hit is not None else other).append(row)
    if space == "evidence":
        _name_by_item([row for rows_ in buckets + [other] for row in rows_])
    kinds = list(mine)
    if space == "evidence" and supporting:
        # Supporting Runs are Task runs or Discovery runs, each owned by its own skill.
        support = _support_rows(supporting)
        discovery = [r for r in support if str(r.get("family") or "").lower().startswith("discover")]
        task = [r for r in support if r not in discovery]
        kinds.append({"card": "", "label": "Task runs", "space": space, "pattern": "",
                      "views": "supporting", "prompt": _SUPPORT_PROMPT, "skills": ["haipipe-task"]})
        buckets.append(task)
        kinds.append({"card": "", "label": "Discovery runs", "space": space, "pattern": "",
                      "views": "supporting", "prompt": _DISCOVERY_PROMPT, "skills": ["haipipe-discovery"]})
        buckets.append(discovery)
    if other:
        kinds.append({"card": "", "label": "Other", "space": space, "pattern": "", "views": "",
                      "prompt": "/haipipe-page run {page} {run} again: {target}."})
        buckets.append(other)
    return panel_markup(space, kinds, buckets, base=base, fill=lambda row: fill, extra=extra,
                        named=len(mine) + (2 if space == "evidence" and supporting else 0))


def _waiting(rows) -> int:
    return sum(1 for r in rows if str(r.get("status") or "").lower() in ("waiting", "review-ready"))


def panel_markup(space: str, kinds: list[dict], buckets: list[list[dict]], *, base: Path, fill,
                 extra: str = "", whole: str = "the whole page", named: int | None = None) -> str:
    """The Runs panel HTML for run types `kinds` and their rows `buckets`.

    `fill(row)` gives the prompt placeholders of one row (`{page}`, `{plan}`, ...);
    `whole` is what "+ New Run" says when nothing is selected; the first `named`
    kinds may be the default type (an "Other" bucket after them never is).
    """
    # Open on the type that has a run waiting for the person, else the busiest one.
    named_ = list(range(min(named if named is not None else len(kinds), len(kinds)))) or list(range(len(kinds)))
    first = max(named_, key=lambda i: (_waiting(buckets[i]), len(buckets[i])), default=0)
    default_fill = fill({})
    buttons = "".join(
        '<button type=button class="run-type%s" data-type="%d" data-label="%s" data-prompt="%s" '
        'data-skills="%s" data-views="%s" data-waiting="%d" data-count="%d">'
        '%s <span class=run-count>%d</span></button>'
        % (" on" if i == first else "", i, _e(k["label"]),
           _e(_fill(k["prompt"], button=k["label"], **default_fill)), _e(" · ".join(k.get("skills") or [])),
           _e(k.get("views", "")),
           _waiting(buckets[i]), len(buckets[i]), _e(k["label"]), len(buckets[i]))
        for i, k in enumerate(kinds))
    cards = "".join(_card_html(row, i, kinds[i], base, fill(row))
                    for i, rows_ in enumerate(buckets) for row in rows_)
    waiting = sum(_waiting(rows_) for rows_ in buckets)
    return (
        '<section class=runs-panel data-space="%s" data-waiting="%d" data-whole="%s">'
        '<div class=runs-bar><button type=button class=runs-fold title="Fold or open">▸</button>'
        '<b>Runs</b>%s</div>'
        '<div class=runs-body><div class=runs-types>%s'
        '<button type=button class="run-type run-new">+ New Run</button></div>'
        '<div class=runs-detail><div class=run-list></div>%s'
        '<article class="run-card run-card-new" hidden><header><b>New run</b></header><p class=run-skill hidden></p>'
        '<details class=run-prompt-box open><summary>Prompt '
        '<button type=button class=run-copy data-copy="">Copy</button></summary>'
        '<pre class=run-prompt></pre></details></article>'
        '<div class=run-empty hidden>No runs yet.<p class=run-skill hidden></p></div>'
        '</div></div></section>'
        % (_e(space), waiting, _e(whole), extra, buttons, cards))


PANEL_CSS = """
.runs-panel button{font:600 11.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 border:1px solid var(--line);border-radius:7px;padding:3px 9px;cursor:pointer;background:var(--card);color:var(--fg)}
.run-type.on{border-color:var(--acc);color:var(--acc)}
.runs-panel{margin:14px 0 6px;border:1px solid var(--line);border-radius:10px;background:var(--card)}
.runs-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;font:13px/1.4 system-ui,sans-serif}
.runs-bar .runs-fold{padding:0 7px}
.runs-saved{padding:0 12px 10px;color:var(--mut);font:11.5px/1.5 system-ui,sans-serif}
.runs-saved code{font-size:11px} .runs-panel.folded .runs-saved{display:none}
.runs-panel.folded{cursor:pointer}
.runs-body{display:grid;grid-template-columns:minmax(150px,210px) minmax(0,1fr);gap:12px;padding:0 12px 12px}
.runs-panel.folded .runs-body{display:none}
.runs-types{display:flex;flex-direction:column;gap:6px}
.run-type{text-align:left;display:flex;justify-content:space-between}
.run-type[hidden]{display:none}
.run-type .run-count{color:var(--mut);font-weight:500}
.run-new{border-style:dashed!important}
.runs-detail{border:1px solid var(--line);border-radius:9px;padding:10px 12px;min-width:0}
.run-list{display:flex;flex-wrap:nowrap;overflow-x:auto;gap:4px;margin-bottom:8px;padding-bottom:2px}
.run-list[hidden]{display:none}
.run-list button{flex:none;font:500 11px ui-monospace,Menlo,monospace!important;padding:1px 6px!important}
.run-list button.on{border-color:var(--acc);color:var(--acc)}
.run-card header{display:flex;align-items:center;gap:8px}
.run-card header .run-copy{margin-left:auto}
.run-skill{margin:6px 0 0;color:var(--mut);font-size:12px}.run-skill code{font-size:11.5px;color:var(--fg)}
/* The prompt folds (JL 260927); Copy works while it is folded. */
.run-prompt-box>summary{display:flex;align-items:center;gap:6px;margin:10px 0 4px;cursor:pointer;
 list-style:none;font:600 12px system-ui,sans-serif;text-transform:none;letter-spacing:normal;color:var(--fg)}
.run-prompt-box>summary::-webkit-details-marker{display:none}
.run-prompt-box>summary::before{content:"▸";color:var(--acc);width:10px}
.run-prompt-box[open]>summary::before{content:"▾"}
.run-prompt-box>summary .run-copy{margin-left:auto}
.run-card h4{display:flex;align-items:center;justify-content:space-between;margin:10px 0 4px;
 font:600 12px system-ui,sans-serif}
.run-sub,.run-process{color:var(--mut);font-size:12px;line-height:1.5;overflow-wrap:anywhere}
.run-prompt{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:7px 9px;border-radius:7px;
 background:color-mix(in srgb,var(--acc) 6%,var(--card));font:12px/1.5 ui-monospace,Menlo,monospace}
.run-results ul{margin:4px 0 0;padding-left:18px;font-size:12px}
.run-state{font:600 10.5px/1.4 system-ui,sans-serif;border-radius:5px;padding:1px 6px;
 border:1px solid var(--line);color:var(--mut)}
.run-state.st-awaiting-you{color:#2b8a3e;border-color:#2b8a3e}
.run-state.st-running{color:var(--acc);border-color:var(--acc)}
.run-empty{color:var(--mut);font-size:12px}
.paragraph-group.runs-selected>summary{outline:2px solid var(--acc);outline-offset:2px;border-radius:6px}
@media (max-width:700px){.runs-body{grid-template-columns:1fr}}
"""

PANEL_JS = r"""
(function(){
 function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}
 function copy(text,btn){
  function done(){var old=btn.textContent;btn.textContent='Copied';setTimeout(function(){btn.textContent=old;},1200);}
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,function(){fallback();});}
  else fallback();
  function fallback(){var t=document.createElement('textarea');t.value=text;document.body.appendChild(t);t.select();
   try{document.execCommand('copy');done();}catch(e){}document.body.removeChild(t);}
 }
 document.addEventListener('click',function(ev){
  var b=ev.target.closest('.run-copy');if(!b)return;
  ev.preventDefault();  /* a Copy inside a folded summary copies without opening it */
  var text=b.dataset.copy||'';
  if(!text){var pre=b.closest('.run-card')&&b.closest('.run-card').querySelector('.run-prompt');text=pre?pre.textContent:'';}
  copy(text,b);
 });
 function matches(card,target){
  if(!target)return true;
  var t=(card.dataset.targets||'').split(' ');
  return t.indexOf(target)>=0||t.some(function(x){return x.indexOf(target+'.')===0;});
 }
 /* data-views="" belongs everywhere; otherwise only to the views or tabs it names.
    A run type follows the view (Draft view, Evidence tab, Delivery view); a Delivery
    build card follows the format tab. */
 function inView(el,view){var v=(el.dataset.views||'').trim();return !v||!view||v.split(' ').indexOf(view)>=0;}
 function typeShown(el,p){var v=(el.dataset.views||'').trim();if(!v)return true;
  var names=v.split(' ');return names.indexOf(p.dataset.view||'')>=0||names.indexOf(p.dataset.mode||'')>=0;}
 function skillLine(sk,src){if(!sk)return;var names=(src&&src.dataset.skills||'').split(' · ').filter(Boolean);
  sk.innerHTML=names.length?'Skill '+names.map(function(n){return '<code>'+n.replace(/[<>&"]/g,'')+'</code>';}).join(' · '):'';
  sk.hidden=!names.length;}
 function typeLabel(p,type){var b=p.querySelector('.run-type[data-type="'+type+'"]');return b?b.dataset.label:'';}
 function render(p){
  var on=p.querySelector('.run-type.on'),newMode=on&&on.classList.contains('run-new');
  var target=p.dataset.target||'',view=p.dataset.view||'',list=p.querySelector('.run-list');
  var type=newMode?p.dataset.lastType:(on?on.dataset.type:'0');
  var cards=[].slice.call(p.querySelectorAll('.run-card[data-type="'+type+'"]'))
   .filter(function(c){return matches(c,target)&&inView(c,view);});
  /* each type counts the runs of the selected target (and view), not the whole list */
  p.querySelectorAll('.run-type[data-type]').forEach(function(b){var s=b.querySelector('.run-count');if(!s)return;
   s.textContent=[].filter.call(p.querySelectorAll('.run-card[data-type="'+b.dataset.type+'"]'),
    function(c){return matches(c,target)&&inView(c,view);}).length;});
  p.querySelectorAll('.run-card').forEach(function(c){c.hidden=true;});
  list.innerHTML='';p.querySelector('.run-empty').hidden=true;
  if(newMode){
   var src=p.querySelector('.run-type[data-type="'+type+'"]'),card=p.querySelector('.run-card-new');
   var what=target||(p.dataset.space==='delivery'?p.dataset.viewLabel:'')||p.dataset.whole||'the whole page';
   card.querySelector('.run-prompt').textContent=(src?src.dataset.prompt:'').replace(/\{target\}/g,what);
   skillLine(card.querySelector('.run-skill'),src);
   card.hidden=false;return;
  }
  p.dataset.lastType=type;
  /* a type with no run yet still names the skill that does its work (JL 260929) */
  if(!cards.length){var em=p.querySelector('.run-empty');
   skillLine(em.querySelector('.run-skill'),p.querySelector('.run-type[data-type="'+type+'"]'));em.hidden=false;return;}
  function showCard(c){cards.forEach(function(x){x.hidden=true;});c.hidden=false;
}
  cards.forEach(function(c,i){var b=document.createElement('button');b.type='button';b.textContent=c.dataset.name||c.dataset.run;b.title=c.dataset.run;
   b.addEventListener('click',function(){showCard(c);
    list.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});b.classList.add('on');});
   if(i===0)b.classList.add('on');list.appendChild(b);});
  list.hidden=cards.length<2;  /* one run: its title already names it */
  showCard(cards[0]);
 }
 /* A view or tab shows only its own run types. It opens on a type with a run
    waiting for the person, else on one that has runs in this view, else on the
    first type that belongs to this view (Table opens on Structure revise). */
 function pickType(p){
  var view=p.dataset.view||'',buttons=[].slice.call(p.querySelectorAll('.run-type:not(.run-new)'));
  buttons.forEach(function(b){b.hidden=!typeShown(b,p);});
  var target=p.dataset.target||'';
  function live(b){return [].some.call(p.querySelectorAll('.run-card[data-type="'+b.dataset.type+'"]'),
   function(c){return matches(c,target)&&inView(c,view);});}
  /* a run waiting for the person first, then a type that has runs here, then a view-specific one */
  function score(b){return (+b.dataset.waiting>0?4:0)+(live(b)?2:0)+((b.dataset.views||'').trim()?1:0);}
  var best=null;
  buttons.forEach(function(b){if(!b.hidden&&(!best||score(b)>score(best)))best=b;});
  p.querySelectorAll('.run-type').forEach(function(x){x.classList.remove('on');});
  if(best)best.classList.add('on');
 }
 function setTarget(p,target){p.dataset.target=target||'';render(p);}
 function setView(p,view,label,mode){p.dataset.view=view||'';p.dataset.viewLabel=label||'';p.dataset.mode=mode||view||'';pickType(p);render(p);}
 var panels={};
 document.querySelectorAll('.runs-panel').forEach(function(p){
  var space=p.dataset.space,fold=p.querySelector('.runs-fold');panels[space]=p;
  function setFold(on){p.classList.toggle('folded',on);fold.textContent=on?'◂':'▸';store('runs-fold:'+space,on?'1':'0');}
  fold.addEventListener('click',function(ev){ev.stopPropagation();setFold(!p.classList.contains('folded'));});
  p.querySelector('.runs-bar').addEventListener('click',function(ev){
   if(p.classList.contains('folded')&&!ev.target.closest('input,button'))setFold(false);});
  if(store('runs-fold:'+space)==='1')setFold(true);
  p.querySelectorAll('.run-type').forEach(function(b){b.addEventListener('click',function(){
   p.querySelectorAll('.run-type').forEach(function(x){x.classList.remove('on');});b.classList.add('on');render(p);});});
  render(p);
 });
 document.addEventListener('space-scope',function(ev){var p=panels[ev.detail.space];if(p)setView(p,ev.detail.view,ev.detail.label,ev.detail.mode);});
 document.addEventListener('space-target',function(ev){var p=panels[ev.detail.space];if(p)setTarget(p,ev.detail.target);});
 var draft=panels.draft,lensDiv=document.getElementById('lens-div');
 if(draft&&lensDiv){
  setView(draft,lensDiv.dataset.draftMode||'table','');
  document.querySelectorAll('.draft-mode-tab').forEach(function(b){
   b.addEventListener('click',function(){setView(draft,b.dataset.draftMode,'');});});
 }
 document.addEventListener('click',function(ev){
  if(!draft||ev.target.closest('.runs-panel,button,a,input,textarea,select,[contenteditable],.structure-card'))return;
  var g=ev.target.closest('.paragraph-group[data-paragraph]');if(!g)return;
  var same=g.classList.contains('runs-selected');
  document.querySelectorAll('.paragraph-group.runs-selected').forEach(function(x){x.classList.remove('runs-selected');});
  if(!same)g.classList.add('runs-selected');
  setTarget(draft,same?'':(g.dataset.paragraph||''));
 });
})();
"""
