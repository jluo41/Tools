"""The design views' small parts in the base's look: the run cards, status words, folds, ids and a Job's cost
(split from design_views.py, which re-exports every name here)."""
from __future__ import annotations

import re
from pathlib import Path

from host_paths import skill_dir
from live import design_reader as R
from live.frame import esc, pop, reader, rel, table


GUIDE_METHOD = "/_board/guide?family=design&view=method"
OK = ("passed", "closed", "released", "answered", "ok", "kept", "yes", "✓", "✅")
WARN = ("verify", "revise", "open", "failed", "waiting", "draft")


# ── the run cards (b12 s21: each Run's skill, agent, sign and prompt live on its card) ────────────
CARDS = skill_dir("haipipe-design-workflow") / "references" / "run-cards.md"
_CARD_LINE = re.compile(r"^🔘 BUTTON\s+(.+?) · (Block|Job|Task) › (.+?) · (\^run-\S+)(?: · views (.+))?$")
_ALIAS = {}                                     # older spellings of a Run, mapped to its card (none left, 261007)
_cache: dict = {}


def ladder_cards(path: Path = CARDS) -> list:
    """The ladder's run cards: [{label, level, space, pattern, views, skill, agent, signs, prompt}], in file order.
    The older board's cards (one-word Spaces) never match a `<Level> › <Space>` line, so they are left out."""
    try:
        stamp = path.stat().st_mtime
    except OSError:
        return []
    if _cache.get("stamp") == (path, stamp):
        return _cache["cards"]
    out, card = [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _CARD_LINE.match(line)
        if m:
            card = {"label": m.group(1), "level": m.group(2), "space": m.group(3), "pattern": m.group(4),
                    "views": (m.group(5) or "").split(), "skill": "", "agent": "", "signs": "", "prompt": ""}
            out.append(card)
        elif line.startswith("🔘 BUTTON") or line.startswith("## "):
            card = None
        elif card is not None:
            for mark, key in (("🧩 SKILL", "skill"), ("🤖 AGENT", "agent"), ("✍️ SIGNS", "signs"), ("💬 PROMPT", "prompt")):
                if line.startswith(mark):
                    card[key] = line[len(mark):].strip()
    _cache.update(stamp=(path, stamp), cards=out)
    return out


def card_for(label: str, level: str | None = None) -> dict | None:
    """The run card of a Runs-panel entry named as its Run (run-<type>-<target>), its own level's first."""
    name = re.sub(r"^(\?\s*)?t(?:00|NN|99|\d\d) › ", "", label.strip())
    name = _ALIAS.get(name, name).replace("run-freeze-prediction-", "run-freeze-predictions-")
    sample = re.sub(r"<[^>]+>", "x01", name)
    found = [c for c in ladder_cards() if re.match(c["pattern"], sample)]
    return next((c for c in found if c["level"] == level), found[0] if found else None)


# ── small parts in the base's look ───────────────────────────────────────────────────────────
def _kind(label: str, prompt: str, *skills: str, rows=(), level: str | None = None) -> dict:
    """A Runs-panel entry, named as its Run; its card (if any) gives the skill, the agent, the sign and the prompt."""
    card = card_for(label, level)
    if card:
        prompt = card["prompt"]
        if card["agent"] and card["agent"] != "none":
            prompt = f'Run with {card["agent"]}. {prompt}'
        if card["signs"] and card["signs"] != "none":
            prompt += f' I sign {card["signs"]}.'
        skills = (card["skill"],) if card["skill"] else skills
    return {"label": label, "prompt": prompt, "skills": list(skills), "rows": list(rows)}


def _rows(rs: list, root: Path, *types: str) -> list:
    return [{"run_id": r["run"], "status": r["status"], "target": r["target"], "result": rel(r["result"], root)}
            for r in rs if not types or r["type"] in types]


def _st(state) -> str:
    s = str(state if state not in (None, "") else "—")
    low = s.lower()
    cls = "st-ok" if any(low.startswith(o) for o in OK) else "st-warn" if any(low.startswith(w) for w in WARN) else "mut"
    return f"<span class={cls}>{esc(s)}</span>"


def _fold(title: str, meta: str, body: str = "", opened: bool = False, missing: bool = False, mono: bool = False) -> str:
    t = f"<code>{esc(title)}</code>" if mono else esc(title)
    inner = f'<div style="padding:8px 14px">{body}</div>' if body else ""
    return (f'<details class="topic{" missing" if missing else ""}"{" open" if opened else ""}><summary><b>{t}</b>'
            f'<span class=topic-meta>{meta}</span></summary>{inner}</details>')


def _pairs(rows) -> str:
    return table(("", ""), [(f"<span class=mut>{esc(k)}</span>", v) for k, v in rows])


def _open(path: Path, root: Path, label: str, text: str = "") -> str:
    return pop(reader(path, root), label, text or label) if path.exists() else esc(text or label)


def _ideas_text(j: dict) -> dict:
    return {str(i.get("id", "")): str(i.get("idea", "")) for i in j["ideas"]}


def _id(value: str, words: str = "") -> str:
    """An id as plain text: mono, its words after it (no chip; b03 s32-D09)."""
    return f"<code>{esc(value)}</code>" + (f" {esc(words)}" if words else "")


# the review's checks by their Guide names (guide/method.md: T0 Rules · T1 Fidelity · T2 Critique · T3 Pretest · T4 Exp);
# the T-number only on hover, since "T0" reads as a ticket
TESTS = {"T0": "rules", "T1": "fidelity", "T2": "critique", "T3": "pretest", "T4": "Exp"}


def _test(t: str) -> str:
    return f'<span title="{esc(t)}">{esc(TESTS.get(str(t), str(t)))}</span>'


def _qrow(a: str, b: str, c: str) -> str:
    return f"<div class=q-row><div>{a}</div><div>{b}</div><div>{c}</div></div>"


def _qhead(a: str, b: str, c: str) -> str:
    return f"<div class='q-row q-head-row'><div>{esc(a)}</div><div>{esc(b)}</div><div>{esc(c)}</div></div>"


def _mins(v) -> str:
    return "—" if v is None else f"{v:.0f} min"


def _job_link(href, j: dict, label: str = "") -> str:
    return f'<a href="{esc(href("", "", j["path"]))}">{esc(label or j["name"])}</a>'


def _live(designs: list) -> list:
    return [d for d in designs if d["state"] != "dropped"]


def _pred(p: dict, mode: str = "full") -> str:
    """A predicted effect with its basis: against what, by whom and why, because a bare number
    makes its reader ask where it came from. full: the reason shown; fold: folded under the number; cell: on hover."""
    p = p if isinstance(p, dict) else {}
    num, why = str(p.get("predicted") or ""), str(p.get("why") or "")
    if not num:
        return "<span class=mut>—</span>"
    if mode == "cell":
        return (f'<span title="{esc(why)}" style="border-bottom:1px dotted">{esc(num)}</span>' if why else esc(num))
    head = (f'{esc(num)} <span class=mut>against {esc(p.get("against") or "the control")}'
            + (f' · by {esc(p["by"])}' if p.get("by") else "") + "</span>")
    if not why:
        return head
    if mode == "fold":
        return head + f'<details class=q-more><summary>› why</summary><p class=mut>{esc(why)}</p></details>'
    return head + f'<p class=mut>why: {esc(why)}</p>'


def _passed(designs: list) -> list:
    return [d for d in designs if d["state"] in ("passed", "kept", "released")]   # kept comes after passed


def _cost(j: dict) -> dict:
    """What a Job spent: every Run of the Job and its Tasks (generate, verify, revise, t00, t99)."""
    rs = list(j["runs"]) + [r for d in j["designs"] for r in d["runs"]]
    rs += [r for t in (j["t00"], j["t99"]) if t for r in R.runs(t)]
    live = _live(j["designs"])
    mins = [r["minutes"] for r in rs if r["minutes"] is not None]
    toks = [r["tokens"] for r in rs if r["tokens"] is not None]
    n = max(len(live), 1)
    passed = len(_passed(live))
    return {"minutes": sum(mins), "per_design": sum(mins) / n if mins else None,
            "tokens": f"{sum(toks) / n / 1000:.0f}k" if toks else "—",
            "rounds": sum(len(d["drafts"]) for d in live) / n, "first": sum(d["first_try"] for d in live),
            "n": len(live), "passed": passed, "per_passed": sum(mins) / passed if mins and passed else None}
