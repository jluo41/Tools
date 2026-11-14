"""5 · Revise of the draft Task: a person's comments on the text (note cards, note_act) and their actions on a
Revise card (card_act); draft_step_revise.py re-exports them."""
from __future__ import annotations

import datetime
import re
from pathlib import Path

from live.frame import esc, face
from live.draft_steps_common import _inline
from live.draft_step_revise_cards import _before_passes, _change, _first_pass_title, _revise_passes


# ── a person's comments on the text, answered by each Revise pass ────────────────────────────────────────────────
# a sentence numbered within its paragraph has the full address C1.P2.S2 (S1-S3 repeat across paragraphs, JL 261112)
NOTE_TARGET = re.compile(r"^(S\d+[a-z]*|C\d+|C\d+\.P\d+|C\d+\.P\d+\.S\d+[a-z]*)$")


def _comments_path(revise: Path) -> Path:
    """`draft/records/<stem>-comments.md`, beside the cards file `<stem>-revise.md`."""
    return revise.with_name(revise.name.replace("-revise.md", "-comments.md"))


def _comments(path: Path) -> list:
    """A person's comments on the text (JL 261021: "我选中一个句子 ... 点个加号就能加注释 ... 放到 Revise 的那一栏里面"), one
    `### Comment <n> · <S or paragraph>` block each: `Quote:` the words selected, `State:` open (waiting for a pass),
    answered (a pass replied) or done (the person closed it), then the thread, `- Note · <time>: …` from the person and
    `- Reply · <time>: …` from the pass that answered it."""
    if not path.is_file():
        return []
    out = []
    for m in re.finditer(r"(?ms)^### Comment (\d+) · ([^\n]+?)[^\S\n]*\n(.*?)(?=^### |^## |\Z)",
                         path.read_text(encoding="utf-8", errors="replace")):
        body = m.group(3)
        field = lambda k: (re.search(r"(?m)^" + k + r":[^\S\n]*(.*)$", body) or [None, ""])[1].strip()
        out.append({"n": m.group(1), "target": m.group(2).strip(), "quote": field("Quote"),
                    "state": (field("State").split() or ["open"])[0].lower(),
                    "thread": re.findall(r"(?m)^- (Note|Reply) · (.+?): (.*)$", body)})
    return out


def _answered_by(revise: Path) -> dict:
    """{comment number: the heads of the newest pass's cards that answer it (`Answers: Comment <n>`)}."""
    out = {}
    for head, c in (_revise_passes(revise)[:1][0][1] if revise.is_file() and _revise_passes(revise) else []):
        for n in re.findall(r"Comment (\d+)", (re.search(r"(?m)^Answers:[^\S\n]*(.*)$", c.get("body", "")) or [None, ""])[1]):
            out.setdefault(n, []).append(head)
    return out


def _who(w: str, t: str) -> tuple:
    """Who wrote a message: (name, named or not, the round mark's letters). A co-author's comment carries their name after
    its time, `- Note · 2026-11-10 11:20 · Ritu Agarwal: …` (JL 261113: "we should collect the co-author's comments as
    well"); a line with no name is the person's (You) or a pass's reply (AI)."""
    name = t.split(" · ", 1)[1].strip() if " · " in t else ""
    if not name:
        return ("AI", False, "AI") if w == "Reply" else ("You", False, "You")
    return name, True, "".join(p[0] for p in name.split()[:2]).upper()


def _note_card(c: dict, by: list) -> str:
    """One comment, in the column of Revise cards beside its sentence, as a thread (JL 261021: "回复的时候，不应该有个
    AI Reply 吗？ ... 很不像一个 modern 的 UI 设计"): the sentence and its state on top, the words it is on, then each
    message with a round mark for who wrote it (You, or AI for a pass's reply), the cards that answer it, and small text
    actions: Reply (it opens again), Resolve once answered, Reopen, or Delete while no pass has replied."""
    st, replied = c["state"], any(w == "Reply" for w, _, _ in c["thread"])
    when = lambda t: t[5:] if re.match(r"\d{4}-", t) else t            # 2026-10-21 14:32 → 10-21 14:32
    msgs = "".join(
        f'<div class="nt-msg{" nt-ai" if w == "Reply" else " nt-co" if _who(w, t)[1] else ""}"><span class=nt-av>{esc(_who(w, t)[2])}</span>'
        f'<div><div class=nt-who><b>{esc(_who(w, t)[0])}</b> <span>{esc(when(t.split(" · ")[0]))}</span></div>'
        f'<div class=nt-text>{_inline(x, {})}</div></div></div>' for w, t, x in c["thread"])
    cards = (f'<div class=nt-cards>↳ {" · ".join(esc(h) for h in by)}</div>' if by else "")
    acts = (["reply", "delete"] if st == "open" and not replied else ["reply"] if st == "open"
            else ["done", "reply"] if st == "answered" else ["reopen"])
    label = {"reply": "Reply", "done": "✓ Resolve", "reopen": "Reopen", "delete": "Delete"}
    buttons = ('<div class=nt-acts>'
               + "".join(f'<button type=button class="nt-btn nt-st{" nt-danger" if a == "delete" else ""}" '
                         f'data-note-act={a}>{label[a]}</button>' for a in acts)
               + '<button type=button class="nt-btn nt-w nt-send" data-note-act=save>Send</button>'
               '<button type=button class="nt-btn nt-w" data-note-act=cancel>Cancel</button>'
               '<span class="rv-msg mut"></span></div>')
    on_p = bool(re.match(r"C\d+\.P\d+$", c["target"]))           # a comment on a whole paragraph sits at its heading
    return (f'<div class="rv-card rv-note" data-n="{esc(c["n"])}" data-s="{esc(c["target"])}"'
            + (f' data-p="{esc(c["target"])}"' if on_p else "") + f' data-state="{esc(st)}">'
            f'<div class=nt-head><span class="nt-s rv-handle">{esc(c["target"])}</span> <span class="nt-state nt-{esc(st)} rv-handle">'
            f'{NOTE_LABEL.get(st, esc(st))}</span>'
            + (f'<span class=rv-peek style="flex:1;min-width:0">{esc(_who(*c["thread"][-1][:2])[0])}: '
               f'{esc(c["thread"][-1][2])}</span>' if c["thread"] else "") + '</div>'
            + (f'<div class=nt-quote>“{esc(c["quote"])}”</div>' if c["quote"] else "")
            + msgs + cards
            + '<textarea class=nt-box rows=2 placeholder="Reply…"></textarea>' + buttons + '</div>')


NOTE_LABEL = {"open": "Open", "answered": "AI replied", "done": "Resolved"}


def _write_sentence(path: Path, sid: str, orig: str, new: str) -> tuple:
    """Put `new` in place of sentence `sid` in the current Draft's §3 text: (the Draft, "") when written or already
    there, (the Draft or None, why not) when the sentence is no longer `orig`."""
    from live.draft_steps_common import read_draft
    draft = Path(read_draft(path.parents[2]).get("file") or "")
    if not draft.is_file():
        return None, "no current Draft"
    dt = draft.read_text(encoding="utf-8")
    head, mark, tail = dt.partition("## 3 ·")
    if not mark:
        head, tail = "", dt
    line = re.search(r"(?m)^(- B\d+[a-z]* · " + re.escape(sid) + r" · )(.*)$", tail)
    said = " ".join(line.group(2).split()) if line else ""
    cut = new.strip() == "(cut)"                        # a card that removes the sentence (`Expected: (cut)`)
    if (said == " ".join(new.split())) or (cut and not line):
        return draft, ""
    if not line or said != " ".join(orig.split()):
        return draft, f"{sid} is no longer the reviewed sentence; reload"
    tail = tail.replace(line.group(0) + "\n", "", 1) if cut else tail.replace(line.group(0), line.group(1) + new, 1)
    draft.write_text(head + mark + tail, encoding="utf-8")
    return draft, ""


def _adopt(path: Path, p: dict) -> tuple:
    """✓ Use this on a reviewer's suggested sentence (JL 261113: "I think this is good, how could I accept it?"): a new
    Edit card at the end of the cards file, the reviewer's words as its Expected, accepted now; the pass that applies
    accepted cards writes it into the text."""
    sid, orig, new = (str(p.get(k) or "").strip() for k in ("s", "original", "expected"))
    if not re.fullmatch(r"S\d+[a-z]*", sid) or not new:
        return 400, {"ok": False, "err": "a sentence and its new words"}
    text = path.read_text(encoding="utf-8")
    if f"Expected: {new}\n" in text:
        return 409, {"ok": False, "err": "already a card with these words; reload"}
    when = f"{datetime.datetime.now():%Y-%m-%d %H:%M}"
    # the sentence changes now, in the current Draft (JL 261114: "When I click this, will it just update the
    # sentence?"), so the text, its 🕘 history and its card agree; refused when the sentence is no longer the original
    draft, err = _write_sentence(path, sid, orig, new)
    if err:
        return 409 if draft else 404, {"ok": False, "err": err}
    card = (f"\n\n### Edit · {sid} · the reviewer's suggestion\nBy: AI\n"
            f"Why: the blind review's suggested sentence, taken by the person with ✓ Use this.\n"
            f"Original: {orig}\nExpected: {new}\nState: written · {when} · JL, into {draft.name}\n")
    path.write_text(_into_newest_pass(text, card), encoding="utf-8")
    return 200, {"ok": True, "state": "written"}


def _into_newest_pass(text: str, card: str) -> str:
    """The cards file with `card` at the end of its newest "## Pass" part (above the next "## " heading), so it shows in
    the current Pass and never inside an older hidden "## Round" part below it; with no Pass, above the first Round."""
    passes = list(re.finditer(r"(?m)^## Pass\b", text))
    if passes:
        nxt = re.search(r"(?m)^## ", text[passes[-1].end():])
        at = passes[-1].end() + nxt.start() if nxt else len(text)
    else:
        rnd = re.search(r"(?m)^## Round\b", text)
        at = rnd.start() if rnd else len(text)
    head, tail = text[:at].rstrip("\n"), text[at:]
    return head + card + ("\n" + tail if tail else "")


def card_act(root: Path, p: dict, read_only: bool = False) -> tuple:
    """A person's ✓ Accept, ✗ Reject, ↺ Undo or edited Expected on one Revise card (b32 s41-D32): writes only that card's
    `State:` (with the time) and, for an edit, its `Expected:` in `draft/records/<stem>-revise.md`. The text itself is
    changed by the pass that applies the accepted cards. Refused when the card changed on disk since the page showed
    it (`was`), so a person never writes over an agent's new pass."""
    if read_only:
        return 403, {"ok": False, "err": "this host is read-only"}
    root = Path(root).resolve()
    folder = (root / str(p.get("task") or "").strip("/")).resolve()
    md = face(folder) if folder.is_dir() and root in folder.parents else None
    if md is None:
        return 400, {"ok": False, "err": "no such Task"}
    path = folder / "draft" / "records" / f"{md.stem}-revise.md"
    state, head, title = str(p.get("state") or ""), str(p.get("card") or ""), str(p.get("pass") or "")
    if not path.is_file():
        return 404, {"ok": False, "err": f"no {path.name}"}
    if p.get("act") == "adopt":
        return _adopt(path, p)
    if state not in ("proposed", "accepted", "rejected"):
        return 400, {"ok": False, "err": "a card is proposed, accepted or rejected"}
    text = path.read_text(encoding="utf-8")
    start, end = 0, len(text)
    sec = re.search(r"(?m)^## " + re.escape(title) + r"[^\S\n]*$", text) if title else None
    if sec:
        nxt = re.search(r"(?m)^## ", text[sec.end():])
        start, end = sec.end(), sec.end() + nxt.start() if nxt else len(text)
    elif title == _first_pass_title(text):       # the cards above the first `## Pass` heading
        end = len(_before_passes(text))
    else:
        return 409, {"ok": False, "err": "the pass changed on disk; reload"}
    seg = text[start:end]
    found = list(re.finditer(r"(?ms)^### " + re.escape(head) + r"[^\S\n]*\n(.*?)(?=^### |^## |\Z)", seg))
    if len(found) != 1:
        return 409, {"ok": False, "err": "the card changed on disk; reload"}
    body = found[0].group(1)
    cur = re.search(r"(?m)^State:[^\S\n]*(\S*)", body)
    now = (cur.group(1).lower() if cur and cur.group(1) else "proposed")
    if p.get("was") and str(p["was"]) != now:
        return 409, {"ok": False, "err": f"it is {now} on disk now; reload", "state": now}
    line = "State: proposed" if state == "proposed" else f"State: {state} · {datetime.datetime.now():%Y-%m-%d %H:%M}"
    body = re.sub(r"(?m)^State:.*$", line, body, count=1) if cur else body.rstrip("\n") + f"\n{line}\n\n"
    change = None
    if p.get("expected") is not None:
        words = " ".join(str(p["expected"]).split())
        if not words:
            return 400, {"ok": False, "err": "the new words are empty"}
        body = (re.sub(r"(?m)^Expected:.*$", lambda m: "Expected: " + words, body, count=1)
                if re.search(r"(?m)^Expected:", body) else body.rstrip("\n") + f"\nExpected: {words}\n\n")
        orig = re.search(r"(?m)^Original:[^\S\n]*(.*)$", body)
        change = _change(head, orig.group(1) if orig else "", words)
        opt = str(p.get("option") or "")
        if re.fullmatch(r"[A-Z]", opt):
            body = (re.sub(r"(?m)^Chosen:.*$", "Chosen: " + opt, body, count=1) if re.search(r"(?m)^Chosen:", body)
                    else body.rstrip("\n") + f"\nChosen: {opt}\n\n")
    # ✓ Accept writes the chosen words into the text now, as ✓ Use this does (JL 261114: "why the proposed
    # suggestions are gone?": an accepted card folded away while its sentence stayed the old one)
    sm, note = re.search(r"(?<![\w.])S\d+[a-z]*\b", head), ""      # "Edit · S41 · C1.P8.B4 · …"
    sid = sm.group(0) if sm else ""
    exp, orig = (re.search(r"(?m)^" + k + r":[^\S\n]*(.*)$", body) for k in ("Expected", "Original"))
    if state == "accepted" and re.fullmatch(r"S\d+[a-z]*", sid) and exp and orig and exp.group(1).strip():
        draft, err = _write_sentence(path, sid, orig.group(1).strip(), exp.group(1).strip())
        if draft and not err:
            body = re.sub(r"(?m)^State:.*$", f"State: written · {datetime.datetime.now():%Y-%m-%d %H:%M} · JL, into {draft.name}",
                          body, count=1)
            state = "written"
        else:
            note = err
    seg = seg[:found[0].start(1)] + body + seg[found[0].end(1):]
    path.write_text(text[:start] + seg + text[end:], encoding="utf-8")
    return 200, {"ok": True, "state": state, "change": change, "note": note}


def _checked_path(revise: Path) -> Path:
    """`draft/records/<stem>-checked.md`, beside the cards file."""
    return revise.with_name(revise.name.replace("-revise.md", "-checked.md"))


def checked(revise: Path) -> dict:
    """{S: the sentence's words when the person checked it}: a sentence they passed (JL 261113: "a button, which means
    check ... this sentence passed my judgment, ... no need to modify it"). A check holds while the words are the same."""
    path = _checked_path(revise)
    if not path.is_file():
        return {}
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"(?m)^- (S\d+[a-z]*) · [^·]+ · (.*)$",
                                                                path.read_text(encoding="utf-8", errors="replace"))}


def _check_act(folder: Path, md: Path, revise: Path, p: dict) -> tuple:
    """✓ a sentence (it passed the person's judgment: no pass edits or rescores it while its words stay) or take the ✓
    back. The line keeps the sentence's words, so a check on words that later change no longer holds."""
    sid = str(p.get("s") or "").split(".")[-1]
    if not re.fullmatch(r"S\d+[a-z]*", sid):
        return 400, {"ok": False, "err": "a check is on a sentence (S<n>)"}
    from live.draft_steps_common import read_draft
    now = {m.group(1): m.group(2).strip() for _, b in read_draft(folder).get("text", [])
           for m in re.finditer(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · (.*)$", b)}
    if sid not in now:
        return 400, {"ok": False, "err": f"{sid} is not a sentence of the current Draft"}
    words = " ".join(now[sid].split())
    path = _checked_path(revise)
    head = (f"# {md.stem} · checked sentences\n\nSentences the person passed. A Revise pass, a review and a rescoring "
            "leave a checked sentence as it is, while its words are the ones below.\n\n")
    lines = [l for l in (path.read_text(encoding="utf-8").splitlines() if path.is_file() else []) if l.startswith("- ")]
    lines = [l for l in lines if not l.startswith(f"- {sid} · ")]
    if p.get("act") == "check":
        lines.append(f"- {sid} · {datetime.datetime.now():%Y-%m-%d %H:%M} · {words}")
    key = lambda l: [int(x) if x.isdigit() else x for x in re.findall(r"\d+|[a-z]", l.split(" · ")[0][3:])]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(head + "\n".join(sorted(lines, key=key)) + "\n", encoding="utf-8")
    return 200, {"ok": True, "checked": p.get("act") == "check"}


def note_act(root: Path, p: dict, read_only: bool = False) -> tuple:
    """A person's comment on the text in 5 · Revise (JL 261021: "我选中一个句子 ... 点个加号就能加注释"), written in
    `draft/records/<stem>-comments.md`: `add` a comment on a sentence (with the words selected, if any), `reply` (a
    new note, so it waits on a pass again), `done`, `reopen`, or `delete` while no pass has replied. A pass answers a
    comment by appending its Reply and setting `State: answered`; the person closes it. Returns the comment's card,
    "" once deleted. Refused when its state changed on disk since the page showed it (`was`)."""
    if read_only:
        return 403, {"ok": False, "err": "this host is read-only"}
    root = Path(root).resolve()
    folder = (root / str(p.get("task") or "").strip("/")).resolve()
    md = face(folder) if folder.is_dir() and root in folder.parents else None
    if md is None:
        return 400, {"ok": False, "err": "no such Task"}
    revise = folder / "draft" / "records" / f"{md.stem}-revise.md"
    if str(p.get("act") or "") in ("check", "uncheck"):
        return _check_act(folder, md, revise, p)
    path = _comments_path(revise)
    act, n = str(p.get("act") or ""), str(p.get("n") or "")
    words = " ".join(str(p.get("text") or "").split())
    now = f"{datetime.datetime.now():%Y-%m-%d %H:%M}"
    text = path.read_text(encoding="utf-8") if path.is_file() else (
        f"# {md.stem} · comments\n\nA person's comments on the text, left in 5 · Revise; each Revise pass answers the "
        "open ones (a Reply line, `State: answered`), and the person closes them.\n")
    if act == "add":
        target = str(p.get("s") or "")
        if not NOTE_TARGET.match(target):
            return 400, {"ok": False, "err": "a comment is on a sentence (S<n>), a paragraph (C<n>.P<n>) or the Section (C<n>)"}
        if not words:
            return 400, {"ok": False, "err": "the comment is empty"}
        n = str(max([int(c["n"]) for c in _comments(path)] or [0]) + 1)
        quote = " ".join(str(p.get("quote") or "").split())[:400]
        text = (text.rstrip("\n") + f"\n\n### Comment {n} · {target}\n" + (f"Quote: {quote}\n" if quote else "")
                + f"State: open\n- Note · {now}: {words}\n")
    else:
        found = list(re.finditer(r"(?ms)^### Comment " + re.escape(n) + r" · [^\n]*\n(.*?)(?=^### |^## |\Z)", text))
        if not n or len(found) != 1:
            return 409, {"ok": False, "err": "the comment changed on disk; reload"}
        body = found[0].group(1)
        cur = (re.search(r"(?m)^State:[^\S\n]*(\S*)", body) or [None, "open"])[1].lower() or "open"
        if p.get("was") and str(p["was"]) != cur:
            return 409, {"ok": False, "err": f"it is {cur} on disk now; reload"}
        if act == "delete":
            if re.search(r"(?m)^- Reply · ", body):
                return 409, {"ok": False, "err": "a pass has replied; mark it done instead"}
            rest = text[found[0].end():].lstrip("\n")
            path.write_text(text[:found[0].start()].rstrip("\n") + ("\n\n" + rest if rest.strip() else "\n"),
                            encoding="utf-8")
            return 200, {"ok": True, "html": ""}
        if act == "reply":
            if not words:
                return 400, {"ok": False, "err": "the reply is empty"}
            body = body.rstrip("\n") + f"\n- Note · {now}: {words}\n"
            state = "open"
        elif act in ("done", "reopen"):
            state = "done" if act == "done" else "open"
        else:
            return 400, {"ok": False, "err": "add, reply, done, reopen or delete"}
        line = f"State: {state}" + (f" · {now}" if state == "done" else "")
        body = re.sub(r"(?m)^State:.*$", line, body, count=1) if re.search(r"(?m)^State:", body) else line + "\n" + body
        if not body.endswith("\n\n") and text[found[0].end():].strip():
            body = body.rstrip("\n") + "\n\n"
        text = text[:found[0].start(1)] + body + text[found[0].end(1):]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    c = next(c for c in _comments(path) if c["n"] == n)
    return 200, {"ok": True, "n": n, "state": c["state"], "html": _note_card(c, _answered_by(revise).get(n, []))}
