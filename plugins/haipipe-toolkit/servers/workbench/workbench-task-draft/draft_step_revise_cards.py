"""5 · Revise of the draft Task: the Revise passes read from `<stem>-revise.md` and each proposed card drawn
(old and new, by sentence, review chips, options); draft_step_revise.py re-exports them."""
from __future__ import annotations

import difflib
import re
from pathlib import Path

from live.frame import _table, esc
from live.sentence_id import sid as _sid
from live.draft_steps_common import _inline


def _revise_passes(path: Path) -> list:
    """`draft/records/<stem>-revise.md` as its passes, newest first: [(title, [(head, {why, original, expected,
    state})])]. A Revise run rewrites the file as one `## Pass <k> · …` part, the latest only (JL 261020: "always keep
    the latest version"); an older file may still hold several, and only the newest shows. A file with none is one pass, named by its "Pass <k>,
    on draft v<N>" line (JL 261020: "everytime to run you will have many things new")."""
    text = path.read_text(encoding="utf-8", errors="replace")

    def cards(body: str) -> list:
        return [(m.group(1).strip(), {**{k.lower(): v.strip() for k, v in re.findall(
                    r"(?m)^(?:[-*][^\S\n]+)?(Why|Original|Expected|State|By):[^\S\n]*(.*)$", m.group(2))},
                 "body": m.group(2)})                     # "State: …" or "- State: …" (most records write the dash)
                for m in re.finditer(r"(?ms)^### ([^\n]+)\n(.*?)(?=^### |^## |\Z)", body)]
    parts = [(t.strip(), b) for t, _, b in (x.partition("\n") for x in re.split(r"(?m)^## ", text)[1:])
             if t.strip().lower().startswith("pass")]
    head = _before_passes(text)                  # cards above the first `## Pass` are a pass of their own, never lost
    if head.strip() and re.search(r"(?m)^### ", head):
        parts = [(_first_pass_title(text), head)] + parts
    passes = [(t, cards(b)) for t, b in parts]
    num = lambda t: int(re.search(r"\d+", t).group(0)) if re.search(r"\d+", t) else 0
    return sorted(passes, key=lambda x: -num(x[0]))


def _proposed_cards(path: Path) -> int:
    """How many cards of the newest pass still read `State: proposed` (a card with no State line is proposed; a
    review report is not a card)."""
    passes = _revise_passes(path) if path.is_file() else []
    return sum(re.sub(r"\W+$", "", (c.get("state") or "proposed").split()[0].lower()) == "proposed"
               for h, c in passes[0][1] if not _is_report(h)) if passes else 0


def _before_passes(text: str) -> str:
    """The part of a cards file above its first `## Pass` heading (the whole file when it has none)."""
    m = re.search(r"(?m)^## Pass", text)
    return text[:m.start()] if m else text


def _first_pass_title(text: str) -> str:
    """The name of the cards above the first `## Pass` heading: from its "Pass <k>, on draft v<N>" line, else Pass 1."""
    m = re.search(r"Pass (\d+), on draft (v\d+(?:\.\d+)*)", _before_passes(text))
    return f"Pass {m.group(1)} · on draft {m.group(2)}" if m else "Pass 1"


STATE_CHIP = {"proposed": '<span class="st st-warn">🔶 proposed</span>', "accepted": '<span class="st st-ok">✓ accepted</span>',
              "written": '<span class="st st-ok">✓ written</span>', "rejected": '<span class=st>✗ rejected</span>',
              "applied": '<span class="st st-ok">✓ applied</span>'}


def _old_new(old: str, new: str) -> str:
    """Original → Expected as one run of words: the words taken out struck in red, the words put in green."""
    a, b = old.split(), new.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if op == "equal":
            out.append(esc(" ".join(a[i1:i2])))
        if op in ("delete", "replace"):
            out.append(f'<del style="color:#c92a2a;background:#fff5f5">{esc(" ".join(a[i1:i2]))}</del>')
        if op in ("insert", "replace"):
            out.append(f'<ins style="color:#2b8a3e;background:#ebfbee;text-decoration:none">{esc(" ".join(b[j1:j2]))}</ins>')
    return " ".join(out)


def _paragraph_plan(text: str):
    """A Section question's paragraph plan, "4 paragraphs, about 400 words: P1 the shift (S1 to S4) · P2 …", as (lead,
    {P1: its job}, note after it); None when it names fewer than two paragraphs."""
    m = re.match(r"^([^:]{0,80}):\s*(?=P\d+\s)", text)
    lead, rest = (m.group(1).strip(), text[m.end():]) if m else ("", text)
    items = [list(x) for x in re.findall(r"(?:^|·)\s*(P\d+)\s+(.*?)(?=\s*·\s*P\d+\s|$)", rest.strip())]
    if len(items) < 2:
        return None
    note, cut = "", re.search(r"\.\s+(?=[A-Z])", items[-1][1])     # a sentence after the last paragraph is a note
    if cut:
        note, items[-1][1] = items[-1][1][cut.end():].strip(), items[-1][1][:cut.start()]
    return lead, {k: v.strip().rstrip(".") for k, v in items}, note


def _plan_cell(text: str, changed: bool) -> str:
    if not text:
        return '<span class=mut>—</span>'
    body = re.sub(r"\(([Ss]\d+[^)]*)\)", r'<span class=mut>(\1)</span>', esc(text))     # its sentences, quiet
    return f'<span style="background:#ebfbee;border-radius:3px;padding:0 3px">{body}</span>' if changed else body


def _change(head: str, original: str, expected: str) -> str:
    """A card's change: an Edit's or Review's words old → new; a Section question's paragraph plans side by side, a row
    per paragraph, now against proposed, the changed ones tinted (JL 261020: "You can make it like the table?"); a
    question that names no paragraphs keeps its now and proposed lines."""
    if head.lower().startswith("section question"):
        now, new = _paragraph_plan(original), _paragraph_plan(expected)
        if now and new:
            keys = sorted(set(now[1]) | set(new[1]), key=lambda k: int(k[1:]))
            rows = [(f"<b>{esc(k)}</b>", _plan_cell(now[1].get(k, ""), False),
                     _plan_cell(new[1].get(k, ""), new[1].get(k, "") != now[1].get(k, ""))) for k in keys]
            heads = ("", "now" + (f" · {now[0]}" if now[0] else ""), "proposed" + (f" · {new[0]}" if new[0] else ""))
            notes = "".join(f'<p class=mut style="margin:4px 0">{esc(n)}</p>' for n in (now[2], new[2]) if n)
            return _table(tuple(esc(h) for h in heads), rows) + notes
        return (f'<p style="margin:4px 0"><span class=mut>now</span> {esc(original)}</p>'
                f'<p style="margin:4px 0"><span class=mut>proposed</span> {_listed(expected)}</p>')
    rows = _by_sentence(head, original, expected)
    return rows or f'<p style="margin:4px 0;line-height:1.6">{_old_new(original, expected)}</p>'


def _by_sentence(head: str, original: str, expected: str) -> str:
    """A change over several sentences, sentence by sentence (JL 261020: "I think this should be sentence by sentence"):
    a row per old sentence, its s id, its words old → new. Each new sentence goes to the old one it reads most like; an
    old one that gets none shows struck, with the sentence it went into. "" when the change holds one old sentence."""
    from live.outline_revise import split_sentences
    old, new = split_sentences(original), split_sentences(expected)
    if len(old) < 2:
        return ""
    m = re.search(r"\b[Ss](\d+)(?:\s*(?:to|–|-)\s*[Ss]?(\d+))?", head)
    first = int(m.group(1)) if m else None
    labels = ([f"s{first + i}" for i in range(len(old))] if m and m.group(2) and int(m.group(2)) - first + 1 == len(old)
              else [f"s{first}" if m and i == 0 else "" for i in range(len(old))])
    words = lambda t: [w.strip(".,;:()[]{}\"'“”").lower() for w in t.split()]
    like = [[difflib.SequenceMatcher(None, words(o), words(n)).ratio() for n in new] for o in old]
    # each new sentence's old one: the earliest that reads nearly as much like it as the best does, so sentences joined
    # into one stay at the first of them (S6 to S8 → S6); never before the one the sentence above went to, so the rows
    # keep reading order (a short new sentence split off S10 is not drawn back to S7 by a few shared words)
    home, at = [], 0
    for j in range(len(new)):
        best = max(like[k][j] for k in range(at, len(old)))
        at = min(i for i in range(at, len(old)) if like[i][j] >= 0.6 * best)
        home.append(at)
    rows = []
    for i, o in enumerate(old):
        mine = [new[j] for j in range(len(new)) if home[j] == i]
        if mine:
            change = _old_new(o, " ".join(mine))
        else:
            j = max(range(len(new)), key=lambda j: like[i][j]) if new else None
            went = (f'→ into {labels[home[j]] or "the sentence above"}' if j is not None and like[i][j] >= 0.15
                    else "→ taken out")
            change = (f'<del style="color:#c92a2a;background:#fff5f5">{esc(o)}</del> '
                      f'<span class=mut>{esc(went)}</span>')
        rows.append(f'<tr data-s="{esc(labels[i])}"><td class=mut style="white-space:nowrap;width:1%;padding:4px 8px 4px 0;'
                    f'vertical-align:top">{esc(labels[i] or "·")}</td><td style="padding:4px 0;line-height:1.6">{change}</td></tr>')
    return ('<table class=rv-rows style="border-collapse:collapse;width:100%;margin:4px 0">'
            + "".join(rows).replace("<tr", '<tr style="border-top:1px solid var(--line)"') + "</table>")


def _listed(text: str) -> str:
    """A proposal of several parts, "a new paragraph of 3 sentences after P1: S5 as its opener · "…" · "…"", as its lead
    and then one part a line, so each proposed sentence reads on its own."""
    lead, sep, rest = text.partition(": ")
    parts = [x.strip() for x in (rest if sep else text).split(" · ") if x.strip()]
    if len(parts) < 2:
        return esc(text)
    return ((esc(lead) + ":" if sep else "") + '<ul style="margin:4px 0 0;padding-left:20px">'
            + "".join(f'<li style="margin:2px 0">{esc(x)}</li>' for x in parts) + "</ul>")



# who made a change (JL 261113: "by" badges): JL, the coauthors, or the AI. A card's own `By:` line wins (`By: RA` or
# `By: Ritu Agarwal`); otherwise its Why names the person whose words it carries; a card naming no one was the AI's.
BY_NAME = {"JL": "Junjie Luo", "RA": "Ritu Agarwal", "GG": "Gordon Gao", "AI": "an AI session (Claude or Codex)"}
BY_WORDS = (("RA", r"\bRitu\b|\bRA\b"), ("GG", r"\bGordon\b|\bGG\b"), ("JL", r"\bJL\b|\bJunjie\b"))


def _by(c: dict) -> list:
    """[initials] of who made this change, from its `By:` line, else the people its Why opens on."""
    own = c.get("by", "")
    if own:
        got = [k for k, n in BY_NAME.items() if re.search(rf"\b{k}\b|{n.split()[0]}", own)]
        if got:
            return got
    why = re.split(r"(?<=[.:;])\s", c.get("why", ""), maxsplit=1)[0]
    return [k for k, rx in BY_WORDS if re.search(rx, why)] or ["AI"]


def _decided_by(c: dict) -> list:
    """[initials] of the person who decided the card, named on its State line (`accepted · JL 261113`)."""
    st = c.get("state", "")
    if not st or st.split()[0].lower().startswith("proposed"):
        return []
    return [k for k, rx in BY_WORDS if re.search(rx, st)]


def _by_badges(who: list, decided: list = ()) -> str:
    """who made the change, then ✓ who decided it, when that is someone else"""
    return ("".join(f'<span class="by by-{k.lower()}" title="by {esc(BY_NAME.get(k, k))}">{esc(k)}</span>' for k in who)
            + "".join(f'<span class="by by-{k.lower()} by-dec" title="decided by {esc(BY_NAME.get(k, k))}">✓{esc(k)}</span>'
                      for k in decided if k not in who))

def _revise_card(head: str, c: dict, task: str, title: str, at: str = "") -> str:
    """One Revise card a person acts on (JL 261020: "我想要那种可以交互的感觉"): its kind, sentence and job, its state;
    why; the change; then ✓ Accept · ✗ Reject · ✎ Edit, or ↺ Undo once decided. Hovering it lights its sentence in the
    text above. A click writes only the card's State (or its edited Expected) in the cards file (card_act)."""
    state = re.sub(r"\W+$", "", c.get("state").split()[0].lower()) if c.get("state") else "proposed"
    if state in ("jl's", "jl"):   # "State: JL's call" waits on the person like proposed (JL 261114: the waiting cards were folded away)
        state = "proposed"
    target = _sid((re.match(r"[^·]+·\s*((?:C\d+\.P\d+\.)?[Ss]\d+[a-z]*)\b", head) or [None, ""])[1])   # s3 or C2.P1.s3
    para = (re.match(r"[^·]+·\s*(C\d+\.P\d+)\b", head) or [None, ""])[1] or at   # a whole part's card: its first paragraph
    # a card is a choice (JL 261021: "这个 edit 你能不能自动把这几个（比如 A、B、C）都列出来 ... D 是 drop it ... 点击确认 button
    # 就可以了"): every option listed, A, B, C (one, "this change", when the card has no options), then the next letter,
    # drop it and keep the original; a radio picks one and Confirm writes it (card_act: the option's words, accepted,
    # or the card rejected)
    choice = head.lower().startswith(("edit", "review"))
    buttons = ('<p class=rv-acts style="margin:6px 0 0">'
               + ('<button type=button class="work-act rv-confirm" data-card-act=confirm>Confirm</button> ' if choice else
                  '<button type=button class=work-act data-card-act=accept>✓ Accept</button> '
                  '<button type=button class=work-act data-card-act=reject>✗ Reject</button> ')
               + '<button type=button class=work-act data-card-act=edit>✎ Edit</button> '
               '<button type=button class=work-act data-card-act=undo>↺ Undo</button> '
               '<button type=button class=work-act data-card-act=save>Save the words</button> '
               '<button type=button class=work-act data-card-act=cancel>Cancel</button> '
               '<span class="rv-msg mut"></span></p>')
    # a card made for a person's comment names it (`Answers: Comment 3`), so the comment and its change read together
    answers = re.findall(r"Comment (\d+)", (re.search(r"(?m)^Answers:[^\S\n]*(.*)$", c.get("body", "")) or [None, ""])[1])
    link = "".join(f' <span class="st nt-link">💬 answers Comment {esc(n)}</span>' for n in answers) + _review_chips(c)
    opts = _options(c)
    rows = opts or [("A", "this change", c.get("expected", ""))]
    chosen = _chosen(c, opts) or "A"
    pick = "drop" if state == "rejected" else chosen
    group = "pick-" + re.sub(r"\W+", "-", head)
    drop = chr(ord("A") + len(rows))
    orig = c.get("original", "")
    # how much of the sentence stays (JL 261113: a big change needs a solid reason, otherwise do not make it)
    same = (round(100 * difflib.SequenceMatcher(None, orig, c.get("expected", "")).ratio())   # a sentence edit only: a
            if orig and c.get("expected") and head.lower().startswith("edit") else None)       # record card has no sentence
    sim = (f' <span class="sx-sim{" low" if same < 60 else " mut"}" title="similarity to the original sentence">{same}% same</span>'
           if same is not None else "")
    choices = ("" if not choice else '<div class=rv-choices>' + "".join(
        f'<label class="rv-choice{" sel" if k == pick else ""}" data-opt="{esc(k)}" data-text="{esc(text)}">'
        f'<input type=radio name="{esc(group)}" value="{esc(k)}"{" checked" if k == pick else ""}> <b>{esc(k)}</b> '
        f'<span class=mut>{esc(why)}</span>'
        + (' <span class="st st-ok">✓ in the text</span>' if state == "written" and k == chosen else "")
        + f'<div class=rv-opt-text><span class=rv-opt-diff>{_old_new(orig, text)}</span>'
        f'<span class=rv-opt-plain>{_inline(text, {})}</span></div></label>' for k, why, text in rows)
        + f'<label class="rv-choice rv-drop{" sel" if pick == "drop" else ""}" data-opt="drop">'
        f'<input type=radio name="{esc(group)}" value="drop"{" checked" if pick == "drop" else ""}> <b>{drop}</b> '
        f'<span class=mut>drop it: keep the original</span>'
        f'<div class=rv-opt-text>{_inline(orig, {}) if orig else "<span class=mut>no sentence: the new one goes</span>"}</div>'
        '</label></div>')
    # each item its own card, one light box (JL 261020: "I still want each of them to have a card"), and no box around
    # the pass, so never a box in a box ("I don't want this", of the cards inside the pass's frame)
    return (f'<div class="rv-card{" has-opts" if opts else ""}{" has-choice" if choice else ""}" data-task="{esc(task)}" '
            f'data-pass="{esc(title)}" data-card="{esc(head)}" data-state="{esc(state)}" data-s="{esc(target)}" '
            f'data-p="{esc(para)}" data-chosen="{esc(chosen)}">'
            f'<div><b class=rv-handle title="{esc(head)}">{esc(_short_head(head))}</b> {_by_badges(_by(c), _decided_by(c))} <span class=rv-chip>{STATE_CHIP.get(state, esc(state))}</span>'
            + (sim if same is not None and same < 100 else "") + f'{link}</div>'
            f'<p class=mut style="margin:4px 0">{esc(c.get("why", ""))}</p>'
            + (choices if choice else f'<div class=rv-change>{_change(head, orig, c.get("expected", ""))}</div>')
            + f'<div class=rv-edit contenteditable=true spellcheck=false>{esc(c.get("expected", ""))}</div>'
            f'{buttons}</div>')


def _short_head(head: str) -> str:
    """A card's title as its row shows it (JL 261113: "the Edit box is too wordy"): ✏️ and what the change is about; the
    sentence id and Bullet address go, the row already names them, and a Review reads as an Edit."""
    kind, _, rest = head.partition("·")
    rest = re.sub(r"^\s*(?:[Ss]\d+[a-z]*|C\d+(?:\.P\d+)?(?:\.B\d+[a-z]?)?)\s*·\s*", "", rest.strip())
    rest = re.sub(r"^(?:[Ss]\d+[a-z]*|C\d+(?:\.P\d+)?(?:\.B\d+[a-z]?)?)\s*·\s*", "", rest)
    k = kind.strip().lower()
    icon = "✏️ " if k in ("edit", "review") else ""
    return (icon + rest) if rest else (icon + kind.strip())


def _review_chips(c: dict) -> str:
    """A card's sentence review beside its state (JL 261110: the per-sentence review and the easier-to-read verdict beside
    each card): its `Score: <n>/10` and its `Readable:` line, the blind A/B readers' verdict (haipipe-paper-draft,
    Co-authors' patterns): rewrite easier and the same meaning, green; the original easier or the meaning changed, amber;
    no gain, grey. The whole line shows on hover."""
    body = c.get("body", "")
    score = re.search(r"(?m)^(?:[-*][^\S\n]+)?Score:[^\S\n]*(\d+(?:\.\d+)?)\s*/\s*10", body)
    read = re.search(r"(?m)^(?:[-*][^\S\n]+)?Readable:[^\S\n]*(.+)$", body)
    out = f' <span class=st title="sentence review score">{esc(score[1])}/10</span>' if score else ""
    if read:
        line = read[1].strip()
        low = line.lower()
        if re.search(r"chang\w* (?:the )?meaning|meaning differs|same[_ ]meaning: no|meaning: no", low):
            chip = ("st st-warn", "📖 changes the meaning")
        elif "original easier" in low:
            chip = ("st st-warn", "📖 original easier")
        elif "no gain" in low or re.search(r"\beasier: same\b", low):
            chip = ("st", "📖 no gain")
        elif re.search(r"rewrite easier|keep rewrite", low):
            chip = ("st st-ok", "📖 easier to read")
        else:
            chip = ("st", "📖 " + line[:40])
        out += f' <span class="{chip[0]}" title="{esc(line)}">{esc(chip[1])}</span>'
    return out


def _options(c: dict) -> list:
    """A card's options, [(letter, the approach, the sentence)], from its `Option A (<approach>): <sentence>` lines."""
    return [(k, (why or "").strip(), text.strip()) for k, why, text in
            re.findall(r"(?m)^Option ([A-Z])(?: \(([^)\n]*)\))?:[^\S\n]*(.*)$", c.get("body", ""))]


def _chosen(c: dict, opts: list) -> str:
    """The option the card holds: its `Chosen:` letter, else the option whose words are its Expected."""
    m = re.search(r"(?m)^Chosen:[^\S\n]*([A-Z])\b", c.get("body", ""))
    if m:
        return m.group(1)
    return next((k for k, _, t in opts if " ".join(t.split()) == " ".join(c.get("expected", "").split())), "")


def _is_report(head: str) -> bool:
    return head.lower().startswith(("revise review report", "current draft review report"))
