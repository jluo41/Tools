"""The state of each plan mark read from disk: sibling workbench folders, bundle
backlinks, and how many of a bullet's cards have landed (moved verbatim from outline.py).
"""
import pathlib
import re

from src.common import evidence_lane_dirs


def _disk_state(page_src):
    """Read sibling workbench folders, including the bundle backlinks.

    The result is still a live projection: no status or bundle is written.
    ``serves`` belongs to Probe cards and ``display_serves`` belongs to Display
    units; keeping the maps separate prevents the two workbench state ladders from
    being mistaken for one another.
    """
    base = page_src.parent
    cards, units, serves, display_serves = {}, {}, {}, {}
    seen_cards = set()
    for pd in evidence_lane_dirs(base, "probe"):
        for d in sorted(pd.iterdir()):
            if d.name in seen_cards:
                continue
            seen_cards.add(d.name)
            c = d / "card.md"
            if not c.is_file():
                continue
            t = c.read_text(errors="replace")
            st = (re.search(r"^state:\s*(\w+)", t, re.M) or [None, "?"])[1]
            # `proof/` is the historical Probe-card name; `answer/`
            # was 0.3.0's and real cards on disk still use it. Read BOTH: a
            # renamed contract must not make an existing card read as empty.
            n = 0
            for name in ("proof", "answer"):
                dd = d / name
                if dd.is_dir():
                    n += len([f for f in dd.glob("*")
                              if f.is_file() and f.name != "manifest.yaml"])
            why_empty = bool(re.search(r"^why_empty:\s*\S+", t, re.M))
            sv = (re.search(r"^serves:\s*(.+)$", t, re.M) or [None, ""])[1]
            serves.setdefault(d.name.split("-")[0], []).extend(
                [re.sub(r"\.S(\d+)$", r".B\1", a) for a in re.findall(r"C\d+\.P\d+\.[BS]\d+", sv)])
            q = (re.search(r"^question:\s*(.+)$", t, re.M) or [None, ""])[1]
            if not q:
                q = (re.search(r"^#\s*\S+\s*\n+(.+)$", t, re.M) or [None, ""])[1]
            # The `## Values` rows, keyed v1/v2/…, kept verbatim: the 🧮
            # chip's evidence card must show THE NUMBER and its proof
            # binding, not just the card's question (JL 260819: "why the
            # value '7' is not get the evidence card? is it the PP01.v1??").
            vals = {}
            vb = re.search(r"(?ms)^## Values\s*\n(.*?)(?=^## |\Z)", t)
            if vb:
                for row in re.finditer(r"(?m)^-\s*(v\d+)\s*·\s*(.+?)\s*$",
                                        vb.group(1)):
                    vals[row.group(1)] = row.group(2)
            cards[d.name.split("-")[0]] = (st, n, q.strip(), why_empty, vals)
    seen_units = set()
    for dd in evidence_lane_dirs(base, "display"):
        for d in sorted(dd.iterdir()):
            if d.name in seen_units:
                continue
            seen_units.add(d.name)
            m = re.search(r"-(Display\d+)-", d.name)
            if not d.is_dir() or not m:
                continue
            r = d / "README.md"
            txt = r.read_text(errors="replace") if r.is_file() else ""
            # ONE parser, shared with the checker. `src/page_evidence.py:60`
            # recorded this exact blind spot and named this file: both read
            # README rows, this one required a leading bullet, and every unit
            # writing a bare `claim: ...` came back with NO claim, NO kind and
            # NO acceptance. A tab and a checker disagreeing about what a ROW
            # is, is how a reader learns to trust neither.
            rows = {}
            for k, v in re.findall(
                    r"^\s*(?:[-*]\s*)?\*{0,2}([A-Za-z][\w -]{0,24}?)"
                    r"\*{0,2}\s*:\s*\*{0,2}\s*(.*?)\s*$", txt, re.M):
                rows.setdefault(k.strip().lower(), v.strip())
            acc = rows.get("accepted", "").startswith("✅")
            rendered = (d / "preview.pdf").is_file() and any(
                (d / "assets").glob("*")) if (d / "assets").is_dir() else False
            claim = re.sub(r"\s+", " ", rows.get("claim")
                           or rows.get("what it shows")
                           or rows.get("shows") or "")
            # A rendered PDF is not yet EVIDENCE. The current Display contract
            # also requires a frozen intake and an explicit renderer row; keep
            # those inputs in the live tuple so the bundle cannot call a bare
            # preview complete.
            intake_ready = (d / "intake").is_dir() and bool(
                rows.get("intake") or rows.get("evidence")
                or rows.get("source") or (d / "intake" / "inputs").is_dir())
            renderer = bool(rows.get("renderer"))
            # THE FIGURE ITSELF, not a description of it (JL 260818: "why
            # here the Displays are not embedded in the outline's content").
            # A 🖼 chip that opens a panel holding only the claim makes a
            # reader leave the tab to see the one thing the mark is about.
            # PNG first because a browser draws it inline with no workbench;
            # the PDF is the fallback and rides in an <object>.
            asset = None
            for cand in ("assets/figure.png", "assets/figure.svg",
                         "assets/figure.pdf", "preview.pdf"):
                if (d / cand).is_file():
                    asset = d / cand
                    break
            units[m.group(1)] = (rendered, acc, claim.strip(),
                                 intake_ready and renderer, renderer, asset)
            sv = (re.search(r"^serves:\s*(.+)$", txt, re.M) or [None, ""])[1]
            display_serves[m.group(1)] = re.findall(
                r"C\d+\.P\d+\.[BS]\d+", sv
            )
    # The KEY alone says the citation resolves; the reader also wants to see
    # WHAT it is without leaving the tab (JL 260817: "我点它之后，它把这个内容
    # 就直接出现了"). So the entry's own fields come back with it.
    keys = {}
    seen_bibs = set()
    for bx in evidence_lane_dirs(base, "bibex"):
        for f in bx.glob("*.bib"):
            if f.name in seen_bibs:
                continue
            seen_bibs.add(f.name)
            for ent in re.split(r"\n(?=@)", f.read_text(errors="replace")):
                m = re.match(r"@\w+\{\s*([^,\s]+)", ent.strip())
                if not m:
                    continue
                def fld(name):
                    g = re.search(r"\b%s\s*=\s*[{\"]" % name, ent, re.I)
                    if not g:
                        return ""
                    i, depth, out = g.end(), 1, []
                    while i < len(ent) and depth:
                        ch = ent[i]
                        if ch == "{":
                            depth += 1
                        elif ch == "}":
                            depth -= 1
                            if not depth:
                                break
                        out.append(ch)
                        i += 1
                    # {CDC} protects capitalisation in BibTeX and is not
                    # part of the title. Stripping only the ENDS left a stray
                    # closing brace mid-string ("CDC} Guideline", 260817).
                    return re.sub(r"\s+", " ",
                                  re.sub(r"[{}]", "", "".join(out))).strip(' "')
                keys[m.group(1)] = {"title": fld("title"), "author": fld("author"),
                                    "year": fld("year"),
                                    "venue": fld("journal") or fld("booktitle") or fld("publisher"),
                                    "verified": bool(re.search(
                                        r"verified:\s*✅", ent, re.I))}
    return cards, units, keys, serves, display_serves


# THE PROBE STATE LADDER, and it is the workbench's, not this file's.
# The retired Probe contract removed the invented raised/working/bound ladder
# for haipipe-probe's own words. This file counted on `bound`, a word no card
# carries any more, so four cards on QC1-visitlbp read `⬜` and their bullets
# read `0 of 1 bound` while two of them were ANSWERED (found 260817 by asking
# whether the thing was ready to use). The old words stay readable because a
# renamed contract must not make an existing card read as empty.
LEGACY_STATE = {"raised": "planned", "working": "commissioned", "bound": "answered"}


# has the number LANDED? (a proof/ is expected with it)
LANDED = ("answered", "answered-local", "read")


# is a human DONE with it? the strip's one-line verdict
READ = ("read",)


STUCK = ("deferred", "failed", "concern")


def _pstate(st):
    """-> the protocol word, whatever vintage the card was written in."""
    st = (st or "").lower()
    return LEGACY_STATE.get(st, st)


def _short_authors(a):
    """`Dowell, Deborah and Haegerich, Tamara M. and Chou, Roger` -> `Dowell et al.`
    One surname is enough in a panel whose title bar already prints the key."""
    if not a:
        return ""
    people = [x.strip() for x in re.split(r"\s+and\s+", a) if x.strip()]
    first = people[0].split(",")[0].strip()
    return first if len(people) == 1 else first + " et al."


def _tex_dash(s):
    """BibTeX writes `---` for a dash. Printing the three hyphens raw is what
    the panel was doing. An EN dash, never an em dash (JL's standing rule)."""
    return re.sub(r"-{2,3}", "\u2013", s or "")


def _asset_url(units, ref, root):
    """-> a URL the browser can fetch for this unit's winning asset, or None.

    The tab is served from the SAME process that serves the tree, so a path
    made relative to `--root` is fetchable as-is. Outside the root there is no
    URL to give, and a broken <img> is worse than no image."""
    got = units.get(ref)
    asset = got[5] if got and len(got) > 5 else None
    if not asset or not root:
        return None
    try:
        return "/" + asset.resolve().relative_to(
            pathlib.Path(root).resolve()).as_posix()
    except ValueError:
        return None


def _aim_rows(page_text):
    """-> {aim id: (aim sentence, state emoji, state sentence)}.

    One id ties three places: the outline bullet says what a sentence will
    establish, `## Aims` says what must become true, `## States` says whether
    it has (workbench-task-draft §📐). Only the first two were ever joined."""
    def _sec(name):
        m = re.search(r"(?m)^## %s\b[^\n]*$(.*?)(?=^## |\Z)" % name, page_text, re.S)
        return m.group(1) if m else ""
    want, got = {}, {}
    # Since workbench-task-draft 0.16.0 the Aims live in the PLAN, and a plan
    # row is `- [ ] A1.1 · target` (a person's box) with its state on the
    # folded `**Now:** …` line, because `## States` is retired. Reading only
    # the bare `- A1.1 ·` form made a migrated page's 🧭 tab say "this page
    # lists no aims yet" while ten Aims sat in its plan (JL 260830, SM08).
    aims_txt = _sec("Aims")
    # The merged-States row is `- ⬜ A1.1 · …` (tick before the id, the set
    # src/common.py AIM_RE reads); without the tick group every 🎯 mark read
    # "not on the page yet" while the row sat on the page (MISQ-Board, 260831).
    for m in re.finditer(r"(?m)^-\s+(?:\[([ xX])\]\s+)?(?:(⬜|🔨|🧠|✅|❄️?|🟡|🟠|⏸️?)\s+)?(A\d+\.\d+|P\d+)\s*·\s*(.+?)\s*$",
                         aims_txt):
        box, tick, aid, sentence = m.group(1), m.group(2), m.group(3), m.group(4)
        want.setdefault(aid, sentence)
        tail = aims_txt[m.end():]
        nxt = re.search(r"(?m)^-\s+", tail)
        block = tail[:nxt.start()] if nxt else tail
        now = re.search(r"\*\*Now:\*\*\s*(.+)", block)
        if now:
            fact = now.group(1).strip()
            em = re.match(r"([⬜🔨🧠✅❄️🟡🟠⏸])\s*", fact)
            emoji = em.group(1) if em else (tick or ("✅" if (box or "").lower() == "x" else "⬜"))
            got.setdefault(aid, (emoji, fact[em.end():].strip() if em else fact))
        elif tick is not None:
            got.setdefault(aid, (tick, ""))
        elif box is not None:
            got.setdefault(aid, ("✅" if box.lower() == "x" else "⬜", ""))
    for m in re.finditer(r"(?m)^-\s+(\S+)\s+(A\d+\.\d+|P\d+)\s*·\s*(.+?)\s*$",
                         _sec("States")):
        got.setdefault(m.group(2), (m.group(1), m.group(3)))
    return {k: (want.get(k, ""), got.get(k, ("", ""))[0], got.get(k, ("", ""))[1])
            for k in set(want) | set(got)}


def _live(mark, ref, cards, units, keys=(), aims=None):
    """One bullet's LIVE half: what the folders say about what it owes."""
    if mark == "probe":
        if not ref:
            return "mut", "needs a probe · not raised yet", ""
        st, n, q, why_empty, _vals = cards.get(ref, (None, 0, "", False, {}))
        if st is None:
            return "warn", "🚨 no card", ""
        body, st = q, _pstate(st)
        if st in STUCK:
            return "warn", "🚨 " + st, body
        if st in LANDED and not n and not why_empty:
            # ANSWERED with an empty proof/ is the one shape that lies: the
            # card says the number came back and nothing on disk carries it.
            return "warn", "🚨 %s, proof/ empty" % st, body
        # "📮 PP01 answered 1" read as "the answer is 1" (JL 260819: "why
        # the answer is 1???") — the bare number was the proof/ FILE count.
        # Say what is counted, and prefer the count a reader wants: how
        # many values the card holds.
        nv = sum(1 for r in _vals.values() if "NOT HERE" not in r.upper())
        got = ("%d value%s" % (nv, "s" if nv != 1 else "")) if nv \
            else ("proof/ %d file%s" % (n, "s" if n != 1 else ""))
        # An answered ask's card SHOWS its values (JL 260819: "how could we
        # later convert this into the value evidence card?" — no conversion:
        # the card already holds them; quoting is 🧮's job, one id per use).
        if _vals:
            vrows = " · ".join(
                "%s.%s = %s (%s)" % (ref, k,
                                     (r.split("·")[1].strip() if "·" in r else r),
                                     r.split("·")[0].strip())
                for k, r in sorted(_vals.items()))
            body = "%s\n\nValues: %s" % (body, vrows)
        if st in READ:
            return "ok", "read · %s" % got, body
        if st in LANDED:
            return "ok", "%s · %s" % (st, got), body
        return "mut", st or "?", body
    if mark == "value":
        # 🧮 quotes ONE number: PP<NN>.v<n>. The card's lifecycle is 📮's
        # job; this chip answers only "is the quoted id real and landed".
        # checks/values.py owns re-computing the number itself.
        if not ref:
            return "mut", "owes its value id · PP<NN>.v<n>", ""
        card_id = ref.split(".")[0]
        st, n, q, why_empty, vals = cards.get(card_id,
                                              (None, 0, "", False, {}))
        if st is None:
            return "warn", "🚨 no card behind %s" % ref, ""
        body, st = q, _pstate(st)
        if "." not in ref:
            return "mut", "names the card, owes the .v id", body
        # The evidence behind a 🧮 chip is THE VALUES ROW — the number, its
        # meaning and its proof binding — with the card's question after it
        # for context. Showing only the question made the reader ask where
        # the 7 lives (JL 260819).
        row = vals.get(ref.split(".", 1)[1])
        if row is None:
            return ("warn", "🚨 %s names no row in %s's ## Values"
                    % (ref, card_id), body)
        parts = [p.strip() for p in row.split("·")]
        num = parts[1] if len(parts) > 1 else ""
        label = parts[0] if parts else row
        bind = " · ".join(parts[2:])
        body = "%s = %s · %s%s · state %s. The card asks: %s" % (
            ref, num or "?", label,
            (" · bound to " + bind) if bind else "", st, q)
        if num.upper() == "NOT HERE":
            return "warn", "🚨 allocated elsewhere · %s" % row, body
        if st in STUCK:
            return "warn", "🚨 " + st, body
        if st in READ or st in LANDED:
            return "ok", "= %s · %s" % (num, st), body
        return "mut", "%s · value not landed yet" % (st or "?"), body
    if mark == "display":
        if not ref:
            return "mut", "needs a figure · not built yet", ""
        got = units.get(ref)
        if got is None:
            return "warn", "🚨 no unit", ""
        rendered, acc, claim = got[:3]
        if not rendered:
            return "mut", "not rendered", claim
        return ("ok", "rendered ✓", claim) if acc \
            else ("mut", "rendered, unaccepted", claim)
    if mark == "cite":
        # A 📚 must name a REAL published work in this page's own bibex, not a
        # sibling board page. QB1/QB2/QB3 were board pages wearing the citation
        # mark, and the page's bibex held zero entries (JL 260817).
        if not ref:
            return "mut", "needs a bib key · not landed yet", ""
        if re.match(r"^QB?\d+$", ref):
            return "warn", "🚨 board page, not a citation", ""
        e = keys.get(ref)
        if not e:
            return "warn", "🚨 not in bibex/", ""
        # A CARD, not a bibliography entry. The full author list is what made
        # a 📚 card twice the height of a 🧮 one (JL 260817: "evidence card
        # 太大了"), and nobody reads six names in a popover: the citation KEY
        # already carries the first author, so the panel says "et al.".
        bits = [b for b in (_short_authors(e["author"]), e["year"]) if b]
        detail = _tex_dash(e["title"]) + ((" · " + " · ".join(bits)) if bits else "")
        if e["venue"]:
            detail += " · " + e["venue"]
        return "ok", "", detail

    if mark == "aim":
        # An empty cell is a STATUS, never a blank. A 🎯 bullet with no Aim id
        # is an intention nobody is tracking, and that must SHOW (JL 260817).
        # With an id the note stays EMPTY: the chip already prints the id, and
        # "→ %s" printed it a second time, so the chip read `🎯 A4.2 → A4.2`
        # (seen in the 260817 screenshot).
        #
        # 🎯 WAS THE ONE MARK THAT NEVER OPENED (JL 260818: "why the evidence
        # card here are not clickable?"). It returned an empty detail whether
        # the id resolved or not, so twenty tracked targets rendered as dead
        # grey tags. The material was on the page the whole time: the workbench's
        # own id grammar ties the bullet to `## Aims` and `## States` by that
        # id (§📐), and the panel is where the other three marks already show
        # the THING itself.
        if not ref:
            return "mut", "no Aim id", ""
        row = (aims or {}).get(ref)
        if row is None:
            # NOT an error. At OUTLINE time the plan names Aims that DRAFT has
            # not created yet, so an unresolved id is the normal forward case;
            # 🚨 here would fire on every well-formed new plan.
            return "mut", "not on the page yet", ""
        aim, emo, state = row
        detail = aim or "named in ## States, with no row in ## Aims"
        if state:
            detail += "  ·  " + (emo + " " if emo else "") + state
        return ("ok" if emo == "✅" else "mut"), "", detail

    return "mut", "", ""


def _count_landed(txt, cards, units, keys):
    """How many owed things EXIST. Not how many are finished."""
    n = 0
    for m in re.finditer(r"🧮[^\n]*?(?<![A-Za-z0-9-])(PP\d+)", txt):
        st = _pstate(cards.get(m.group(1), (None, 0, ""))[0])
        n += st in LANDED
    for m in re.finditer(r"🖼[^\n]*?(Display\d+)", txt):
        n += bool(units.get(m.group(1)))
    for m in re.finditer(r"📚[^\n]*?([A-Za-z][\w:-]*\d{4}[a-z]?)", txt):
        n += m.group(1) in keys
    return n


def _count_accepted(txt, cards, units):
    """How many carry a HUMAN yes: a display's `accepted: ✅` and, since the
    probe workbench's 0.7.0 ladder, a card's `state: read`. The two are the same
    act (a person looked at the thing itself and said yes), so counting only
    the display half under-reported every page that answers with numbers."""
    n = 0
    for m in re.finditer(r"🖼[^\n]*?(Display\d+)", txt):
        got = units.get(m.group(1))
        n += bool(got and got[1])
    for m in re.finditer(r"🧮[^\n]*?(?<![A-Za-z0-9-])(PP\d+)", txt):
        n += _pstate(cards.get(m.group(1), (None, 0, ""))[0]) in READ
    return n


def _bundle_state(kind, refs, address, by_bullet, display_by_bullet,
                  cards, units, keys, scaffolds=None):
    """Return one complete/incomplete roll-up for a marked Outline Point.

    This deliberately returns data rather than HTML so the plan surface and a
    future API can share the same Evidence Bundle semantics. The bundle is
    keyed by the frozen Point address; workbench folders and typed Evidence Item
    states remain the authorities. The bundle does not mint another status
    vocabulary.
    """
    probes = sorted(set(by_bullet.get(address, [])))
    displays = sorted(set(display_by_bullet.get(address, [])))
    displays += [r for r in refs if r.startswith("Display") and r in units
                 and r not in displays]
    citations = [r for r in refs if r in keys]
    sentences = sorted(set((scaffolds or {}).get(address, [])))
    feedback = []
    for pid in probes:
        st = _pstate(cards.get(pid, ("", 0, ""))[0])
        if st in READ:
            feedback.append("%s: read" % pid)
        elif st in STUCK:
            feedback.append("%s: %s" % (pid, st))
    for did in displays:
        got = units.get(did, (False, False, "", False, ""))
        if got[1]:
            feedback.append("%s: accepted" % did)
    for cite in citations:
        feedback.append("%s: %s" % (
            cite, "verified" if keys.get(cite, {}).get("verified")
            else "unverified"))

    if kind in ("value", "probe"):
        landed = [p for p in probes
                  if _pstate(cards.get(p, ("", 0, "", False))[0]) in LANDED
                  and (cards.get(p, ("", 0, "", False))[1] > 0
                       or cards.get(p, ("", 0, "", False))[3])]
        summary = "complete" if probes and len(landed) == len(probes) \
            else "incomplete"
        return {"probes": probes, "displays": [], "citations": [],
                "sentences": sentences, "feedback": feedback, "summary": summary,
                "have": len(landed), "need": max(1, len(probes))}
    if kind == "display":
        rendered = [d for d in displays if units.get(d, (False, False, "", False, ""))[0]]
        intake = [d for d in displays if units.get(d, (False, False, "", False, ""))[3]]
        summary = "complete" if displays and len(rendered) == len(displays) \
            and len(intake) == len(displays) \
            else "incomplete"
        return {"probes": probes, "displays": displays, "citations": [],
                "sentences": sentences, "feedback": feedback,
                "summary": summary, "have": len(rendered),
                "need": max(1, len(displays))}
    if kind == "cite":
        summary = "complete" if refs and len(citations) == len(refs) \
            else "incomplete"
        return {"probes": probes, "displays": displays,
                "citations": citations, "sentences": sentences,
                "feedback": feedback, "summary": summary,
                "have": len(citations), "need": max(1, len(refs))}
    return {"probes": probes, "displays": displays,
            "citations": citations, "sentences": sentences,
            "feedback": feedback,
            "summary": "complete",
            "have": 1, "need": 1}
