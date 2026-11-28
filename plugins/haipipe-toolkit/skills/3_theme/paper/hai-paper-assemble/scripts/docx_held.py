"""docx_held.py: displays held for the top of a page in Word, measured by Microsoft Word (word_page_boundaries,
place_held). latex_room_to_docx.py runs this file inside its own namespace (_load_part), so the Word helpers come
from there; it moved out whole when the placement rule changed (261122)."""
from __future__ import annotations


# ---- full-page displays held for the next page (0.12.0) -------------------------------------------------------
# Word cannot hold a display back while the text keeps filling the page, the way LaTeX does with a [p] float. So a
# display that needs a whole page is left out at first; Microsoft Word lays the document out and reports where the
# page that holds the citing paragraph ends; the display is then put at that boundary on a page of its own, splitting
# the paragraph that crosses it, and the text goes on after it. Without Word (no Mac, a test) it prints at once.
MSWORD_APP = Path("/Applications/Microsoft Word.app")
WORD_BOX = Path.home() / "Library" / "Containers" / "com.microsoft.Word" / "Data" / "Documents" / "hai-measure"
HELD: dict[int, list[dict]] = {}


_WORD_FREE: bool | None = None


def word_can_measure() -> bool:
    if os.environ.get("HAIPIPE_WORD_DRAFT") == "1":   # build.py --word-draft (JL 261104): floats, no measuring; Word sets
        return False                                  # each display at the top of the page its citing text reaches
    if not (sys.platform == "darwin" and MSWORD_APP.exists() and os.environ.get("HAIPIPE_WORD_PREVIEW") != "html"
            and "PYTEST_CURRENT_TEST" not in os.environ):
        return False
    global _WORD_FREE
    if _WORD_FREE is None:                 # asked once a build: a person's open Word is never used (261122)
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from word_lock import word_in_use
        _WORD_FREE = not word_in_use()
        if not _WORD_FREE:
            print("Word has your documents open: displays go right after their citing paragraphs, not at page tops. "
                  "Close Word, or set HAIPIPE_WORD_PREVIEW=word, and build again.", file=sys.stderr)
    return _WORD_FREE


def element_text(el) -> str:
    return "".join(node.text or "" for node in el.iter(qn("w:t")))


def last_text_paragraph(doc: Document):
    for el in reversed(body_children(doc)):
        if el.tag == qn("w:p") and len(element_text(el).strip()) >= 25:
            return el
    return None


def _squash(text: str) -> tuple[str, list[int]]:
    """the text without whitespace, and for each kept character its index in the original"""
    keep = [(c, i) for i, c in enumerate(text) if not c.isspace()]
    return "".join(c for c, _ in keep), [i for _, i in keep]


def _applescript_string(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def word_running() -> bool:
    return subprocess.run(["pgrep", "-x", "Microsoft Word"], capture_output=True).returncode == 0


WORD_STUCK = "Word did not answer"     # build_delivery.py finds this line in the step's output and warns


def word_answers(wait: int = 30) -> bool:
    """A quick question only a working Word can answer. A stuck Word (b16.j02-s22, 261104: its main thread on a lock, 0%
    CPU) let every display wait out AppleScript's 120 seconds and still fall back, about 28 minutes a paper, in silence."""
    script = f'with timeout of {wait} seconds\ntell application "Microsoft Word" to get name of documents\nend timeout'
    try:
        return subprocess.run(["osascript", "-e", script], capture_output=True, timeout=wait + 10).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def word_page_boundaries(path: Path, anchors: list[str]) -> list[str | None]:
    """For each anchor ("E|text": the page the text ends on; "S|text": the page it starts on), the ~120 characters
    Word lays out just before the end of that page (paragraph marks as <P>, cell marks as <C>), or None."""
    WORD_BOX.mkdir(parents=True, exist_ok=True)
    copy = WORD_BOX / path.name
    shutil.copy2(path, copy)
    # "E|3|text": the 3rd match of text (the Abstract repeats Results phrases, so the first match can be wrong)
    finds = ", ".join(_applescript_string(a.split("|", 2)[0] + "|" + a.split("|", 2)[1] + "|"
                                          + a.split("|", 2)[2].replace("^", "^^")) for a in anchors)
    script = f"""
on rep(t, a, b)
  set AppleScript's text item delimiters to a
  set xs to text items of t
  set AppleScript's text item delimiters to b
  set r to xs as text
  set AppleScript's text item delimiters to ""
  return r
end rep
tell application "Microsoft Word"
  set d to open file name "{copy}"
  repaginate d
  set n to end of content of text object of d
  set out to ""
  repeat with a in {{{finds}}}
   try
    home key selection move unit a story
    set q to a as text
    set AppleScript's text item delimiters to "|"
    set parts to text items of q
    set mode to item 1 of parts
    set k to (item 2 of parts) as integer
    set q to (items 3 thru -1 of parts) as text
    set AppleScript's text item delimiters to ""
    set ok to false
    repeat with i from 1 to k
      if i > 1 then set selection start of selection to (selection end of selection)
      set ok to (execute find (find object of selection) find text q match case true wrap find find stop with match forward)
      if not ok then exit repeat
    end repeat
    if ok then
      if mode is "S" then
        set fe to selection start of selection
      else
        set fe to selection end of selection
      end if
      set pe to ((get range information (create range d start fe end fe) information type active end page number) as integer)
      set lo to fe
      set hi to n
      if ((get range information (create range d start (hi - 1) end (hi - 1)) information type active end page number) as integer) > pe then
        repeat while hi - lo > 1
          set m to (lo + hi) div 2
          if ((get range information (create range d start m end m) information type active end page number) as integer) > pe then
            set hi to m
          else
            set lo to m
          end if
        end repeat
        set s to hi - 120
        if s < 0 then set s to 0
        set bt to content of (create range d start s end hi)
        set bt to my rep(my rep(bt, return, "<P>"), (ASCII character 7), "<C>")
        set out to out & "OK" & tab & bt & linefeed
      else
        set out to out & "END" & linefeed
      end if
    else
      set out to out & "MISS" & linefeed
    end if
   on error e
    set out to out & "ERR " & e & linefeed
   end try
  end repeat
  close d saving no
end tell
return out
"""
    try:
        r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=600)
    finally:
        copy.unlink(missing_ok=True)
    if r.returncode != 0:
        print(f"Word could not lay out {path.name}: {r.stderr.strip()[:300]}", file=sys.stderr)
        return [None] * len(anchors)
    lines = [ln for ln in r.stdout.split("\n") if ln.strip()]
    for ln in lines:
        if not ln.startswith("OK\t"):
            print(f"Word page end for {path.name}: {ln[:200]}", file=sys.stderr)
    found = [ln.split("\t", 1)[1] if ln.startswith("OK\t") else None for ln in lines]
    return (found + [None] * len(anchors))[:len(anchors)]


def set_page_break_before(el) -> None:
    if el is None:
        return
    if el.tag == qn("w:p"):
        pPr = el.find(qn("w:pPr"))
        if pPr is None:
            pPr = OxmlElement("w:pPr"); el.insert(0, pPr)
        if pPr.find(qn("w:pageBreakBefore")) is None:
            pPr.insert(0, OxmlElement("w:pageBreakBefore"))
        return
    para = OxmlElement("w:p"); pPr = OxmlElement("w:pPr"); pPr.append(OxmlElement("w:pageBreakBefore")); para.append(pPr)
    el.addprevious(para)


def split_paragraph(p_el, offset: int):
    """Split a body paragraph after `offset` characters of its text; the second part carries on the same paragraph
    (no first-line indent) and is returned."""
    new_p = OxmlElement("w:p")
    pPr = p_el.find(qn("w:pPr"))
    if pPr is not None:
        new_pPr = deepcopy(pPr)
        ind = new_pPr.find(qn("w:ind"))
        if ind is None:
            ind = OxmlElement("w:ind"); new_pPr.append(ind)
        ind.set(qn("w:firstLine"), "0")
        if ind.get(qn("w:hanging")) is not None:
            del ind.attrib[qn("w:hanging")]
        new_p.append(new_pPr)
    else:
        new_pPr = OxmlElement("w:pPr"); ind = OxmlElement("w:ind"); ind.set(qn("w:firstLine"), "0")
        new_pPr.append(ind); new_p.append(new_pPr)
    count, moving = 0, False
    for child in [c for c in p_el if c.tag != qn("w:pPr")]:
        if moving:
            new_p.append(child)
            continue
        text = element_text(child)
        if count + len(text) <= offset:
            count += len(text)
            continue
        k = offset - count
        if child.tag == qn("w:r") and 0 < k < len(text):
            tail = deepcopy(child)
            ts, tail_ts = child.findall(qn("w:t")), tail.findall(qn("w:t"))
            if len(ts) == 1:
                ts[0].text = text[:k]
                tail_ts[0].text = text[k:].lstrip()
                for node in (ts[0], tail_ts[0]):
                    node.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                new_p.append(tail)
                moving = True
                continue
        new_p.append(child)   # the split falls at this child's start
        moving = True
    p_el.addnext(new_p)
    return new_p


def boundary_target(anchor, before: str | None):
    """The body element a held display goes in front of, splitting a paragraph when the page ends inside it."""
    if anchor is None or before is None:
        return None
    following = [anchor]
    while following[-1].getnext() is not None and following[-1].getnext().tag != qn("w:sectPr"):
        following.append(following[-1].getnext())
    at_par_start = before.endswith("<P>") or before.endswith("<C>")
    segments = [s for s in re.split(r"<P>|<C>", before) if s.strip()]
    if not segments:
        return None
    seg, _ = _squash(segments[-1])
    if len(seg) < 8:
        return None
    for el in following:
        squashed, index = _squash(element_text(el))
        if at_par_start:
            if el.tag == qn("w:p") and squashed.endswith(seg):
                return el.getnext()
        elif el.tag == qn("w:p"):
            pos = squashed.find(seg)
            if pos >= 0:
                end = index[pos + len(seg) - 1] + 1
                full = element_text(el)
                if end >= len(full.rstrip()):
                    return el.getnext()
                # split only where a sentence ends, never inside one (JL 261028: a display cut a sentence in two);
                # the page then ends on a full stop and the display opens the next page, as LaTeX does. When the
                # page ends inside the paragraph's first sentence, the display goes in front of the paragraph.
                stops = [m.end() for m in re.finditer(r"[.?!][)\]\"”’]*\s+", full) if m.end() <= end]
                if not stops:
                    return el
                return split_paragraph(el, stops[-1])
    return None


def is_heading1(p_el) -> bool:
    """A paragraph set in the Heading 1 style: a main Section or an Appendix opens here."""
    pPr = p_el.find(qn("w:pPr"))
    style = pPr.find(qn("w:pStyle")) if pPr is not None else None
    return style is not None and style.get(qn("w:val")) in {"Heading1", "Heading 1", "Subtitle"}   # Subtitle: a template's REFERENCES, APPENDIX


def _body_index(el) -> int:
    body = el.getparent()
    return list(body).index(el) if body is not None else -1


def save_docx(doc: Document, path: Path) -> None:
    """Save; then place each held display, in order, at the top of the page after the one its citing paragraph ends
    on, as Microsoft Word lays the document out, and save again. A display cited before the end of the one placed
    just before it goes to the page after that one, so the order of the displays and their citations holds."""
    doc.save(path)
    held = HELD.pop(id(doc), [])
    if not held:
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from word_lock import word_turn
    with word_turn() as turn:      # builds take turns in Word, for the whole document (b16.j02-s22)
        place_held(doc, path, held, turn)


def place_held(doc: Document, path: Path, held: list, turn: bool) -> None:
    was_running, placed, last = word_running(), 0, None
    answers = turn and word_answers()
    if not answers:
        print(f"{WORD_STUCK} in 30 seconds: {Path(path).name}'s {len(held)} display(s) go right after their citing "
              "paragraphs, not at page tops. Restart Word and build again.", file=sys.stderr)
    try:
        for h in held:
            anchor, mode = h["anchor"], "E"
            target, measured = None, False
            if last is not None and (anchor is None or _body_index(anchor) < _body_index(last)):
                anchor, mode = last.getnext(), "S"     # after the display placed just before
                while anchor is not None and not (anchor.tag == qn("w:p") and (len(element_text(anchor).strip()) >= 25 or is_heading1(anchor))):
                    anchor = anchor.getnext()
                if anchor is not None and anchor.tag == qn("w:p") and is_heading1(anchor):
                    # the next Section or Appendix starts here: the display stays in front of it, never under it
                    # (Pp-AgreeableRx 261122: Tables C2 to C5 printed under Appendix D's heading and first paragraph)
                    target, anchor = anchor, None
            if anchor is not None:
                text = element_text(anchor).strip()
                snippet = text[:50] if mode == "S" else text[-60:]
                # which match is the anchor's own: count the matches in the body up to and including it
                k = 0
                for el in body_children(doc):
                    k += element_text(el).count(snippet)
                    if el is anchor:
                        break
                doc.save(path)
                before = word_page_boundaries(Path(path), [f"{mode}|{max(k, 1)}|{snippet}"])[0] if answers else None
                target = boundary_target(anchor, before)
                placed += target is not None
                measured = target is not None
                if target is None:                   # Word could not say: right after the citing paragraph
                    target = anchor.getnext()
                # a display never crosses into the next Section or Appendix: if a Heading 1 lies between its citing
                # paragraph and the measured page, it goes in front of that heading, as LaTeX's \clearpage flushes
                # floats before the next appendix (261101: Table B1 printed under Appendix C, Table C2 under D)
                el = anchor.getnext()
                while el is not None and el is not target and el.tag != qn("w:sectPr"):
                    if el.tag == qn("w:p") and is_heading1(el):
                        target = el
                        break
                    el = el.getnext()
            start = len(body_children(doc))
            display = h["display"]
            if display.kind == "table":
                add_table(doc, display, h["title"], compact=h["compact"])
            else:
                add_figure(doc, display, h["title"], compact=h["compact"], max_height=6.4 if h["full_page"] else None)
            moved = body_children(doc)[start:]
            pars = [el for el in moved if el.tag == qn("w:p")]
            if pars:   # a clear gap under the legend, so it never reads as the body text that follows (JL 261028)
                Paragraph(pars[-1], doc._body).paragraph_format.space_after = Pt(18)
                no_contextual_spacing(pars[-1])
            if target is not None and target.tag != qn("w:sectPr"):
                for el in moved:
                    target.addprevious(el)
                # a figure that fills its page sends the text on to the next page; after a table, or a short
                # figure, the text goes on below it
                if h["full_page"] and display.kind != "table":
                    set_page_break_before(target)
            # a display placed at a page Word measured starts that page; one placed by the fallback (Word could not
            # find its citing paragraph) stays right after it with no break, so it never strands a page of two lines
            if measured or h["full_page"]:
                set_page_break_before(moved[0])
            last = moved[-1]
    finally:
        if not was_running and word_running():
            try:   # never with a document open: a person may have opened one during the build
                subprocess.run(["osascript", "-e", 'tell application "Microsoft Word" to if (count of documents) is 0 then quit saving no'],
                               capture_output=True, timeout=30)
            except subprocess.TimeoutExpired:
                pass
            for _ in range(40):   # wait until Word has gone, or the preview step takes it for the user's own Word
                if not word_running():
                    break
                import time; time.sleep(0.25)
    doc.save(path)
    print(f"{Path(path).name}: {len(held)} display(s) placed at the top of a page; {placed} where Word ended the page")
