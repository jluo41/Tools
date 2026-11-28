"""The one table of state marks every page and the Files pane draw (hai-ui A05): one 12px circle family, drawn inline
so it looks the same on every platform, its word on hover. A row carrying a mark also carries its effect class
(`fx-<key>`, focus.css), as s07's Effects tab shows: done pops in once, running sweeps, waits for you pings, new fades
with a plus, void is struck through, not yet stays still.

Keys: the Files pane's trace states (plan, edit, done, off, kept) and a row's states (you, new, void), one drawing each.
"""
from __future__ import annotations

import re


def _mark(label: str, body: str) -> str:
    return (f'<svg class="state-mark" width="12" height="12" viewBox="0 0 12 12" role="img" aria-label="{label}" '
            f'focusable="false">{body}</svg>')


_RING = '<circle cx="6" cy="6" r="4.5" fill="none" stroke="#9a9a94" stroke-width="1.4" stroke-dasharray="2 1.6"/>'
STATE_MARKS = {
    "plan": _mark("Planned", _RING),
    "edit": _mark("Editing", '<circle cx="6" cy="6" r="4.5" fill="none" stroke="#2f6fd6" stroke-width="1.5"/>'
                             '<path d="M6 1.5a4.5 4.5 0 0 1 0 9z" fill="#2f6fd6"/>'),
    "done": _mark("Done", '<circle cx="6" cy="6" r="5" fill="#2f9e5b"/><path d="M3.6 6.2l1.6 1.6 3.2-3.3" fill="none" '
                          'stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'),
    "off": _mark("Not in plan", '<path d="M6 1l5 5-5 5-5-5z" fill="#d98a12"/>'),
    "kept": _mark("Committed", '<circle cx="6" cy="6" r="3.2" fill="#b9b9b3"/>'),
    "you": _mark("Waits for you", '<circle cx="6" cy="6" r="4.5" fill="none" stroke="#d98a12" stroke-width="1.5"/>'
                                  '<circle cx="6" cy="6" r="2" fill="#d98a12"/>'),
    "new": _mark("New", _RING + '<path d="M6 3.9v4.2M3.9 6h4.2" stroke="#9a9a94" stroke-width="1.3" stroke-linecap="round"/>'),
    "void": _mark("Void", '<circle cx="6" cy="6" r="5" fill="#d6453d"/><path d="M4.2 4.2l3.6 3.6M7.8 4.2l-3.6 3.6" '
                          'stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>'),
}
STATE_COLORS = {"plan": "#9a9a94", "edit": "#2f6fd6", "done": "#2f9e5b", "off": "#d98a12", "kept": "#b9b9b3",
                "you": "#d98a12", "new": "#9a9a94", "void": "#d6453d"}
STATE_ORDER = ("off", "edit", "plan", "done", "kept")      # a closed folder shows the first of these found inside it

_DONE = ("done", "answered", "ready", "agreed", "signed", "applied", "checked", "released", "passed", "closed",
         "complete", "verified")


def state_key(state: str) -> str:
    """A state's key in STATE_MARKS from its emoji or its words ("✅ done", "🙋 waiting for you", "In progress");
    "" for no state. Anything not done, running, waiting, new or void is not yet (plan)."""
    s = (state or "").strip()
    if not s:
        return ""
    low = s.lower()
    if s.startswith(("🆕",)) or re.match(r"new\b", low):
        return "new"
    if s.startswith(("❗", "❌")) or any(w in low for w in ("void", "fail", "superseded")):
        return "void"
    if s.startswith("🙋") or "wait" in low or "your call" in low:
        return "you"
    if s.startswith(("🏃", "⏳", "🔶")) or any(w in low for w in ("running", "progress", "partly")):
        return "edit"
    if low.startswith(("not ", "no ")):
        return "plan"
    if s.startswith(("✅", "✓")) or any(low == w or low.endswith(" " + w) for w in _DONE) or low.startswith("all done"):
        return "done"
    return "plan"


WORDS = {"plan": "not yet", "edit": "running", "done": "done", "you": "waits for you", "new": "new", "void": "void",
         "off": "not in plan", "kept": "committed"}
