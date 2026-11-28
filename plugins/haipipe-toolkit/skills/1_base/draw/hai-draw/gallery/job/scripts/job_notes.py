"""② of a Job drawing: the words it uses, how sure, what would close each open point. Small, it explains ①.
Moved out of job_ladder.py, which re-exports it."""
from __future__ import annotations

from job_ladder import NW, T_RES, TERMS, Drawing, canvas, jd, words, GREY, INK, RED  # noqa: F401


def has_notes(cfg: dict) -> bool:
    return bool(cfg.get("terms") or cfg.get("sure") or cfg.get("later") or
                any(isinstance(o, dict) and o.get("closer") for o in cfg.get("open") or []))


def notes_frame(d: Drawing, info: dict, cfg: dict, mark: str = "②") -> dict | None:
    """Asked by the reader review of 261013 ("neither one defines its terms … or says how to close what is open"): the
    face's `terms`, `sure` and `open` (with each `closer`), in a small frame stepped below and right of the staircase
    (canvas.explains), so its short labels decode."""
    if not has_notes(cfg):
        return None
    rest = "what is open" if cfg.get("open") else "what waits for later" if cfg.get("later") else "what is open"
    f = d.frame(f"{mark} 📖 {info['id']}: the words it uses, how sure, {rest}", NW)
    Drawing.room(f)
    d.text(40, 22, "📖 Words to know", 40)
    d.icon("document", f"{info['id']}_notes_doc", NW - 150, 24, "ok", w=80, h=104)   # vivid first: a picture
    y = 140
    terms = [t for t in cfg.get("terms") or [] if (t.get("term") if isinstance(t, dict) else t)]
    for t in terms[:TERMS]:
        term, means = (t.get("term"), t.get("means")) if isinstance(t, dict) else (str(t), "")
        y = d.para(40, y, str(term), NW - 80, T_RES) + 2
        y = d.para(70, y, words(means, 25), NW - 110, 24) + 14 if means else y + 10
    if len(terms) > TERMS:                  # never drop a term silently (found on OpioidRx b02, 261013)
        y = d.para(40, y, f"… {jd.n_of(len(terms) - TERMS, 'more term')} in the face", NW - 80, 24, GREY) + 14
    if cfg.get("sure"):
        y += 24
        d.text(40, y, "🎯 How sure", 34)
        h = Drawing.height(words(cfg["sure"], 50), NW - 140, 24) + 40
        d.key(40, y + 60, NW - 80, h)
        y = d.para(70, y + 80, words(cfg["sure"], 50), NW - 140, 24) + 30
    opens = [o for o in cfg.get("open") or [] if o]
    if opens:
        y += 24
        d.text(40, y, "❓ What is open, and what would close it", 34, RED)
        y += 66
        for o in opens:
            item = o.get("item", "") if isinstance(o, dict) else str(o)
            y = d.para(40, y, f"❓ {words(item, 25)}", NW - 80, 24, RED) + 2
            if isinstance(o, dict) and o.get("closer"):
                y = d.para(70, y, f"→ close by: {words(o['closer'], 25)}", NW - 110, 24, INK)
            y += 14
    later = [o for o in cfg.get("later") or [] if o]
    if later:                               # an agreed topic's open points, moved to Later: plain, never red (the
        y += 24                             #   stage contract: agreed = no red ? and no open point; b31 s06-D07)
        d.text(40, y, "⏳ Later, and what would start it", 34)
        y += 66
        for o in later:
            item = o.get("item", "") if isinstance(o, dict) else str(o)
            y = d.para(40, y, f"⏳ {words(item, 25)}", NW - 80, 24, INK) + 2
            if isinstance(o, dict) and o.get("closer"):
                y = d.para(70, y, f"→ when: {words(o['closer'], 25)}", NW - 110, 24, GREY)
            y += 14
    canvas.explains(f)                    # small on purpose: it explains the staircase (JL 261013)
    f["height"] = max(y + 40, 600)
    if f["height"] > canvas.FRAME_MAX[1]:   # a list read top to bottom: only its width must fit
        canvas.reads_down(f)
    return f
