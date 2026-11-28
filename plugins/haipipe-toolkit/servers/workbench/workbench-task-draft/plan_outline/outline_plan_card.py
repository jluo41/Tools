"""📃 Page · the Draft table (plan_card): the plan's Bullets beside their Draft, Reading and Revise rows, with evidence chips.

Moved out of outline.py (the 600-line rule); outline re-exports every name here.
"""
import re
from urllib.parse import quote

from src.plan_shape import canonical_plan, iter_plan_bullets, presentation_point
from src.evidence_labels import collect_result_labels
from live.outline_preview import read_drafts, bullet_token, record_token
from live.outline_scratch import (read_scratch, scratch_assets_html, scratch_control_html,
                                  scratch_flag_html, scratch_heading_attr)
from live.outline_revise import (revise_rows_html, sentence_id as revise_sentence_id,
                                 assets_html as revise_assets_html)
from live.outline_state import (_disk_state, LANDED, _pstate, _asset_url, _aim_rows, _live,
                                _count_landed, _count_accepted, _bundle_state)
from live.outline_plan_read import (_MARK, _latest_plan, _typed_item_review, _paragraph_display,
                                    _source_realizations, _join_wrapped)
from live.outline_plan_html import (_e, _scratch_run_meta, _opening_preview_card,
                                    _outline_cycle_strip, _typed_item_chip, _preview_reader_html,
                                    _bundle_row_html)


def plan_card(page_src, root=None, path_q="", file_q="", read_only=False,
              minimal=False):
    """-> the read-only Draft table, or '' when no outline file exists.

    `path_q`/`file_q` are the Board route the live Outline was opened with; they
    keep Bullet permalinks stable. `read_only` remains an API compatibility
    argument; this reader is now always read-only.
    """
    f, ver = _latest_plan(page_src)
    if f is None:
        return ""
    outline_url = ("/_board/draft?path=%s&file=%s" % (quote(path_q), quote(file_q))
                   if path_q and file_q else "")
    txt = canonical_plan(f.read_text(encoding="utf-8", errors="replace"))
    # The Page paragraph index is global across Content divisions. The
    # historical Shape kept per-division P numbers, so translate those local
    # addresses only in this live presentation layer: source prose, Evidence
    # records, and append-only Run history remain address-stable underneath.
    paragraph_display = _paragraph_display(txt)

    def display_address(address):
        match = re.match(r"^(C\d+\.P\d+)(\.B\d+[a-z]*)$", address)
        if not match:
            return paragraph_display.get(address, address)
        return paragraph_display.get(match.group(1), match.group(1)) + match.group(2)

    preview_blocks = {b["address"]: b for b in iter_plan_bullets(txt)}
    preview_records = read_drafts(page_src)
    evidence_bindings = collect_result_labels(page_src.parent)
    approved = bool(re.search(r"^approved:\s*✅", txt, re.M))
    cards, units, keys, serves, display_serves = _disk_state(page_src)
    page_text = page_src.read_text(encoding="utf-8", errors="replace")
    typed = _typed_item_review(page_src, f, txt, approved)
    preview_item_by_id = {item["id"]: item for item in typed["items"]}
    try:
        scratch_latest = read_scratch(page_src)["latest"]
    except (OSError, ValueError):
        scratch_latest = {}
    # The page is the Aims' home (JL 260831, QPf12 row 2: "In the Page as well,
    # and should map to the content"); a plan that still carries Aim rows only
    # fills ids the page does not have.
    aims = {k: v for k, v in _aim_rows(txt).items() if v[0]}
    aims.update(_aim_rows(page_text))
    source_realizations, scaffolds = _source_realizations(page_text)

    # A card names the bullets it SERVES, so the plan never has to be edited
    # to carry an id that did not exist when it was frozen. Many-to-many: PP04
    # answers three bullets, and a bullet may need two cards.
    by_bullet = {}
    for pid, addrs in serves.items():
        for a in addrs:
            by_bullet.setdefault(a, []).append(pid)
    display_by_bullet = {}
    for did, addrs in display_serves.items():
        for a in addrs:
            display_by_bullet.setdefault(a, []).append(did)
    unserved = sorted(pid for pid, a in serves.items() if not a)


    # A bullet may WRAP, and its mark often sits on the continuation line.
    # Reading line-by-line called those bare, which is a false 🕳 on a bullet
    # the author did mark (found by driving it, 260817).
    joined = _join_wrapped(txt)

    # One bullet = one planned SENTENCE ANCHOR. Its address is its position
    # (C3.P1.S2 = section 3, paragraph 1, sentence anchor 2), the same grammar
    # hai-draft-writing uses on the rendered page. DRAFT may expand that anchor
    # into several scaffolds (`realizes: C3.P1.B2`); the outline surface keeps
    # the stable Point join and does not pretend to own those later splits.
    rows, tally, cited, bundle_rows = [], {}, set(), []
    opening_card = _opening_preview_card(page_src, path_q, file_q, evidence_bindings)
    if opening_card:
        rows.append(opening_card)
    paragraph_bullets = []
    paragraph_reading = []
    paragraph_revise = []
    current_paragraph = ""
    current_paragraph_title = ""
    current_section = ""

    def _flush_paragraph():
        """Close one paragraph group, keeping all its Bullets inside it."""
        nonlocal paragraph_bullets, paragraph_reading, paragraph_revise, current_paragraph, current_paragraph_title
        if not current_paragraph:
            return
        display_paragraph = paragraph_display.get(current_paragraph, current_paragraph)
        reading_body = "".join(paragraph_reading)
        if not reading_body:
            reading_body = (
                '<div class=reading-line><span class=reading-address>—</span>'
                '<div class=reading-copy><span class=preview-placeholder>'
                'Not drafted</span></div></div>'
            )
        revise_body = revise_rows_html(current_paragraph, display_paragraph, paragraph_revise,
                                       read_only=read_only, path_q=path_q, file_q=file_q)
        rows.append(
            '<details class="paragraph-group" open data-paragraph="%s" id="group-%s">'
            '<summary class="prow"%s><span class=addr>%s</span>'
            '<span class=mut>%s</span>%s%s</summary>'
            '<div class=paragraph-scratch>%s</div>'
            '<div class=paragraph-bullets><div class=preview-columns>'
            '<span>Bullet</span><span>Draft</span></div>%s</div>'
            '<div class=paragraph-reading>%s</div>'
            '<div class=paragraph-revise>%s</div>'
            '</details>'
            % (_e(current_paragraph), re.sub(r"[^A-Za-z0-9_-]", "-", current_paragraph),
               scratch_heading_attr("paragraph", current_paragraph,
                                    read_only=read_only),
               _e(display_paragraph),
               _e(re.sub(r"\s*·\s*[Ss]\d+\s+to\s+[Ss]\d+\s*$", "", current_paragraph_title)),
               _scratch_run_meta(scratch_latest.get(("paragraph", current_paragraph))),
               scratch_flag_html("paragraph", current_paragraph,
                                 scratch_latest.get(("paragraph", current_paragraph)),
                                 read_only=read_only),
               scratch_control_html("paragraph", current_paragraph,
                                    scratch_latest.get(("paragraph", current_paragraph)),
                                    read_only=read_only, path_q=path_q,
                                    file_q=file_q),
               "".join(paragraph_bullets), reading_body, revise_body)
        )
        paragraph_bullets = []
        paragraph_reading = []
        paragraph_revise = []
        current_paragraph = ""
        current_paragraph_title = ""

    cn = pn = sn = nid = 0
    for line in joined:
        # A `## ` that is NOT `## C<n>` ENDS the plan's divisions. The plan's
        # own trailing sections (## Aims, ## Notes for DRAFT) were falling
        # through into the last paragraph, so its 26 `- A1.1 ·` rows rendered
        # as bullets B5..B30 of C15.P2 (JL 260819: "there are 32 points for one
        # paragraph"). Counting only `## C<n>` as a division was half the fix;
        # stopping at the first other `## ` is the other half.
        if line.startswith("## ") and not re.match(r"^## C\d+\b", line):
            if cn:
                _flush_paragraph()
                break
            continue
        division_match = re.match(r"^## C(\d+)\b", line)
        if division_match:
            _flush_paragraph()
            cn = int(division_match.group(1)); pn = 0
            current_section = "C%d" % cn
            division_title = re.sub(r"^C\d+\s*·\s*", "", line[3:].strip())
            rows.append('<div class="row division-title"%s title="%s" id="division-C%d">'
                        '<span class="addr sec">C%d</span><b>%s</b>%s%s</div>'
                        '<div class=section-scratch>%s</div>'
                        % (scratch_heading_attr("section", current_section,
                                                read_only=read_only),
                           _e(division_title), cn, cn,
                           _e(division_title.split(" · ")[0]),
                           _scratch_run_meta(scratch_latest.get(("section", current_section))),
                           scratch_flag_html("section", current_section,
                                             scratch_latest.get(("section", current_section)),
                                             read_only=read_only),
                           scratch_control_html("section", current_section,
                                                scratch_latest.get(("section", current_section)),
                                                read_only=read_only, path_q=path_q,
                                                file_q=file_q)))
            continue
        if line.startswith("### "):
            _flush_paragraph()
            paragraph_match = re.match(r"^### C(\d+)\.P(\d+)\b", line)
            if paragraph_match:
                cn = int(paragraph_match.group(1))
                pn = int(paragraph_match.group(2))
            else:
                pn += 1
            sn = 0
            # The paragraph row carries its OWN address in the same column the
            # bullets use (JL 260819, on reading a paragraph title as a broken
            # bullet: "how do you think we can add the Cx.Px to the paragraph
            # sentence as well"). The address was in the file all along; the
            # renderer used to strip it.
            current_paragraph = "C%d.P%d" % (cn, max(pn, 1))
            current_paragraph_title = re.sub(
                r"^C\d+\.P\d+\s*·\s*", "", line[4:].strip()
            )
            continue
        if not line.startswith("- "):
            continue
        sn += 1
        # The editor addresses the Bullet the file NAMES (`- B3 ·`); the
        # position counter is only the fallback for an unnumbered plan.
        explicit = re.match(r"^-\s+B(\d+)[a-z]*\s*·", line)
        bullet_id = "B%s" % explicit.group(1) if explicit else "B%d" % sn
        body = re.sub(r"^[SsB]\d+\s*·\s*", "", line[2:].strip())
        # The FULL address on every row. It was shortened to P<n>.B<n> once
        # (JL 260817: "为什么还要保留 C1") and JL reversed it on 260819
        # ("could you add back the C? like P2.B1 to C1.P2.B1, so we can know
        # the exact index"): a row is quoted OUT of the pane — in chat, in a
        # card's serves:, in a receipt — and there the C is the part that
        # says where it lives.
        # B, not S. At OUTLINE time a bullet is a POINT, and one point
        # becomes ONE OR MORE sentences when it is drafted (JL 260817:
        # "我们能一句话把一个 point 讲完吗?"). C3.P2 is shared with the
        # sentence address, so the link survives; only the last token
        # differs, and it differs because the units differ.
        # Evidence/feedback joins use the Bullet identity written in the plan,
        # not a renderer position.  Preserve explicit B numbers even when a
        # legacy plan has a gap or uses a non-sequential slot label.
        full_addr = "C%d.P%d.%s" % (cn, max(pn, 1), bullet_id)
        addr = full_addr
        display_addr = display_address(full_addr)
        parsed_block = preview_blocks.get(full_addr)
        if parsed_block is not None:
            # Draft is embedded in the same Outline Markdown.  The parsed
            # plan body deliberately excludes the Draft field, so evidence
            # marks and Bullet presentation never scan candidate prose.
            body = parsed_block["body"]

        # New typed Evidence Items are the current contract.  Their short
        # inline tags keep the Shape readable; each is a route to the item's
        # Evidence Space row, where the whole Survey graph (supports,
        # local Run, Result, and human Decide) is shown once.
        typed_chips = []
        for item in typed["by_target"].get(full_addr, []):
            nid += 1
            typed_chips.append(_typed_item_chip(item, outline_url))
        none_reason = typed.get("none_by_target", {}).get(full_addr, "")

        def _backlink(exclude=()):
            """The ↩ tag: cards that name THIS bullet in their `serves:`.
            It is skipped for a card the row already prints as a chip, because
            `🧮 PP01 answered 1` then `↩ PP01 ✓` is one fact twice on one line
            (JL 260817, screenshot). It is the ONLY thing that speaks when the
            plan's mark is bare, which is the normal case: the plan is frozen
            before the card exists, so the CARD names the bullet."""
            b = [x for x in by_bullet.get(full_addr, []) if x not in exclude]
            if not b:
                return ""
            # One chip PER card, each opening the card's own popover — the
            # same evidence-card treatment the forward chips got. A bare
            # <span> here meant the one chip that usually speaks for a bullet
            # was the one chip nobody could open (JL 260819: "why the probe
            # PP01 here we cannot click and see it?").
            out = []
            for x in b:
                st = _pstate(cards.get(x, ("?", 0, ""))[0])
                ok = st in LANDED
                cls = "ok" if ok else "mut"
                label = "↩ %s %s" % (_e(x), "✓" if ok else _e(st))
                _c, _n, detail = _live("probe", x, cards, units, keys, aims)
                if not detail:
                    out.append('<span class="evtag %s">%s</span>' % (cls, label))
                    continue
                pid = "bl-%s-%s" % (full_addr.replace(".", "-"), _e(x))
                out.append(
                    '<button class="evchip %s" popovertarget="%s">%s</button>'
                    '<div id="%s" popover class="chipcard %s">'
                    '<div class=cch><b>%s</b><span class=cck>🧮 probe card</span></div>'
                    '<div class=ccb><p>%s</p></div></div>'
                    % (cls, pid, label, pid, cls, _e(x), _e(detail)))
            return " ".join(out)

        # THE MARK IS THE LAST EMOJI ON THE LINE, inside the end-anchored
        # window. A first-hit substring scan read C1.P2.B1 — whose PROSE
        # mentions 📚 and 🧮 mid-sentence before ending `🖼 Display4` — as a
        # citation bullet, so Display4 landed on the orphan row of the very
        # plan that cites it (JL 260819: "Why you still didn't solve this
        # problem? you should cite it."). Same 64-char window as
        # plan_shape.check_coverage, one law in two readers.
        hit, hit_at = None, -1
        for emo, kind in _MARK.items():
            at = body.rfind(emo)
            if at > hit_at and at >= 0 and len(body) - at <= 64:
                hit, hit_at = (emo, kind), at
        def _bullet_row(head_raw, chips_html, bullet_id, _edit_value=None,
                        evidence_none_reason=""):
            """Render one static Bullet/Draft row without changing its source."""
            point = presentation_point(
                head_raw, number=int(re.search(r"\d+", bullet_id).group(0))
            )
            statement = point["statement"] or "—"
            record = preview_records.get(addr)
            block = preview_blocks.get(addr)
            value = block.get("draft", "") if block else (record or {}).get("text", "")
            # The Revise box starts from what the reader sees: the Draft field,
            # or the Page's own realized sentence when no Draft exists yet (JL
            # 260922: "put the sentences there, so we can modify, not writing
            # from the scratch"). A Save writes the Draft field either way.
            paragraph_revise.append({
                "address": addr, "bullet_id": bullet_id,
                "sid": revise_sentence_id(block["head"]) if block else "",
                "text": value or " ".join(source_realizations.get(addr, [])),
                "bullet_token": bullet_token(block) if block else "",
                "record_token": record_token(record),
            })
            if not value:
                # A realized Page sentence is a useful read-only fallback for
                # a legacy/minimal Outline that has no embedded Draft field.
                # It never becomes a new Draft authority or an editor value.
                value = " ".join(source_realizations.get(addr, []))
            if value:
                copy = _preview_reader_html(value, preview_item_by_id, evidence_bindings)
            else:
                copy = '<span class=preview-placeholder>Not drafted</span>'
            # The reader is a projection of the same Draft value, not a second
            # source. Keep one lightweight line per Bullet so the source join
            # remains visible without bringing Point/Evidence metadata along.
            paragraph_reading.append(
                '<div class="reading-line" data-point="%s">'
                '<span class=reading-address>%s</span>'
                '<div class=reading-copy>%s</div></div>'
                % (_e(addr), _e(bullet_id), copy)
            )
            preview = (
                '<div class=point-preview><div class=preview-copy>%s</div></div>'
                % copy
            )
            focus_id = "bullet-" + re.sub(r"[^A-Za-z0-9_-]", "-", addr)
            permalink = "%s&lens=div&focus=%s" % (outline_url, quote(display_addr))
            evidence = (
                '<span class=point-evidence aria-label="Evidence routes">%s</span>'
                % chips_html
                if chips_html else ""
            )
            evidence_state = "none" if evidence_none_reason else (
                "routed" if chips_html else "missing"
            )
            evidence_attrs = ' data-evidence-state="%s"' % evidence_state
            if evidence_none_reason:
                evidence_attrs += ' data-evidence-reason="%s"' % _e(
                    evidence_none_reason
                )
            return ('<div id="%s" class=point-group data-point="%s" data-display-point="%s">'
                    '<div class=point-plan><div class=point-head%s>'
                    '<a class=point-address href="%s" data-outline-lens="div" '
                    'data-outline-focus="%s" title="Open %s">%s</a>'
                    '<span class=point-label>[%s]</span>'
                    '<span class=point-statement>%s</span>%s</div></div>%s</div>'
                    % (_e(focus_id), _e(addr), _e(display_addr), evidence_attrs,
                       _e(permalink),
                       _e(display_addr), _e(display_addr), _e(bullet_id),
                       _e(point["role"]), _e(statement), evidence, preview))

        if hit is None:
            # A plain sentence is the NORMAL case, not a defect. Requiring a
            # tag on every line was wrong (JL 260817) and made the plan
            # unreadable: the plan is prose, the notes are the exception.
            tally["plain point"] = tally.get("plain point", 0) + 1
            edit_head = re.split(
                r"\s+(?=(?:Note|Evidence|Accept|Answered|Drawn|Routed|More):)",
                body,
                maxsplit=1,
            )[0]
            edit_head = re.sub(r"\s+\u241e.*$", "", edit_head).strip()
            plain_chips = [chip for chip in [_backlink(), *typed_chips] if chip]
            paragraph_bullets.append(
                _bullet_row(body, " ".join(plain_chips), bullet_id, edit_head,
                            none_reason)
            )
            continue
        emo, kind = hit
        tally[kind] = tally.get(kind, 0) + 1
        # Split at the WINNING occurrence, not the first: the prose before an
        # end mark may legally mention any glyph.
        raw_said = body[:hit_at].strip()
        after = body[hit_at + len(emo):]
        pat = {"probe": r"(?<![A-Za-z0-9-])(PP\d+)", "value": r"(?<![A-Za-z0-9-])(PP\d+(?:\.v\d+)?)",
               "display": r"(Display\d+)",
               # [A-Za-z]* after the year, not [a-z]?: author-year-WORD keys
               # (`luo2026eventglucose`) were truncated to `luo2026e`, and the
               # chip then reported not-in-bibex for a key nobody wrote.
               "cite": r"(QB\d+|[A-Za-z][\w:-]*\d{4}[A-Za-z]*|[A-Za-z][\w-]*[_:][\w:-]+|[A-Z][A-Z0-9-]{3,})",
               "aim": r"(?<![A-Za-z0-9.\-])(A\d+\.\d+|P\d+)"}.get(kind)
        # ALL of them, not the first. "📚 Dowell2016 · Dowell2022" registered
        # only Dowell2016, so the second key appeared as an orphan on the very
        # reverse-join row built to catch orphans (found 260817 by driving it).
        refs = re.findall(pat, after) if pat else []
        # LEGACY TOLERANCE for multi-chip tails (`📚 Gray2021 · 🧮 proof`):
        # the ROW shows only the LAST mark, but the orphan join must credit
        # every kind named anywhere in the end window — Gray2021 printed as
        # an orphan of the very plan that cites it (260819 smoke, QC1).
        _tail = body[-64:]
        for _emo, _kind in _MARK.items():
            _at = _tail.rfind(_emo)
            _p = {"probe": r"(?<![A-Za-z0-9-])PP\d+", "value": r"(?<![A-Za-z0-9-])PP\d+(?:\.v\d+)?",
                  "display": r"Display\d+",
                  "cite": r"QB\d+|[A-Za-z][\w:-]*\d{4}[A-Za-z]*|[A-Za-z][\w-]*[_:][\w:-]+|[A-Z][A-Z0-9-]{3,}"}.get(_kind)
            if _at >= 0 and _p:
                cited.update(re.findall(_p, _tail[_at:]))
        # A BARE mark whose bullet already has a card is RAISED, and saying
        # "not raised yet" beside a ↩ chip that names the card is one fact
        # contradicted twice on one line (JL 260819: "why here you didn't
        # raise a probe here? I don't understand"). The plan is frozen before
        # the card exists, so bare is the NORMAL case and the backlink is the
        # only thing that knows: let it speak alone.
        # A BARE mark whose bullet already has a card is RAISED, so the chip
        # is suppressed and the ↩ backlink speaks alone. It must NOT skip the
        # Evidence Bundle row below: doing that dropped four rows from the
        # derived bundle, caught by checks/outline.py minutes after I wrote it.
        bare_served = not refs and bool(by_bullet.get(full_addr))
        chips = []
        for ref in (refs or [""]):
            if ref:
                cited.add(ref)
            cls, note, detail = _live(kind, ref, cards, units, keys, aims)
            label = " ".join(x for x in (emo, _e(ref), _e(note)) if x)
            if not detail:
                chips.append('<span class="evtag %s">%s</span>' % (cls, label))
                continue
            # THE EVIDENCE CARD, the board's own one (JL 260817: "我想让它有点
            # 像那个 evidence card 一样"). A chip in the line, a panel beside
            # it holding the THING itself — the reference as printed, the
            # card's own question, the unit's own claim — never a description
            # of it (hai-draft-writing §🃏). Native popover, no script: the
            # panel is real body text, so deleting every <script> leaves it.
            nid += 1
            pid = "ev%d" % nid
            media = ""
            if kind == "display":
                u = _asset_url(units, ref, root)
                if u:
                    media = ('<object class=evfig data="%s"></object>' % _e(u)
                             if u.endswith(".pdf")
                             else '<img class=evfig src="%s" alt="">' % _e(u))
            kindname = {"probe": "probe card", "value": "value",
                        "display": "display unit",
                        "cite": "citation", "aim": "aim"}.get(kind, kind)
            chips.append(
                '<button class="evchip %s" popovertarget="%s">%s</button>'
                '<div id="%s" popover class="chipcard %s">'
                '<div class=cch><b>%s</b><span class=cck>%s %s</span></div>'
                '<div class=ccb>%s<p>%s</p></div></div>'
                % (cls, pid, label, pid, cls, _e(ref or "—"), emo, kindname,
                   media, _e(detail)))
        if bare_served:
            chips = [_backlink()]
        else:
            bl = _backlink(exclude=refs)
            if bl:
                chips.append(bl)
        chips.extend(typed_chips)
        if kind in {"probe", "value", "display", "cite"}:
            bundle = _bundle_state("value" if kind == "probe" else kind,
                                   refs, full_addr, by_bullet,
                                   display_by_bullet, cards, units, keys,
                                   scaffolds)
            bundle_rows.append(_bundle_row_html(full_addr, kind, bundle))
        # Keep the Bullet statement and its compact Evidence routes together in
        # the left pane. The routes follow the statement inline and wrap only
        # when the column itself needs to wrap.
        edit_head = re.split(
            r"\s+(?=(?:Note|Evidence|Accept|Answered|Drawn|Routed|More):)",
            body,
            maxsplit=1,
        )[0]
        edit_head = re.sub(r"\s+\u241e.*$", "", edit_head).strip()
        paragraph_bullets.append(
            _bullet_row(raw_said, " ".join(chips), bullet_id, edit_head,
                        none_reason)
        )

    _flush_paragraph()
    rows.append(scratch_assets_html(path_q, file_q)) if not read_only else None
    rows.append(revise_assets_html(read_only=read_only))

    # ── the join runs BOTH ways ────────────────────────────────────────
    # Bullet → disk catches "we promised a display and built none". Disk →
    # bullet catches the opposite: evidence sitting on the page that no plan
    # line uses. The contract claimed both from the start and only the first
    # was built (found 260817 by checking the file against its own code).
    # Typed Evidence Items are the current contract. Their links are rendered
    # from the typed bundle above, while `cited` is populated only by the
    # legacy icon-mark grammar. Running the legacy disk→bullet orphan check in
    # typed mode therefore flags every valid current citation as unused.
    if not minimal and not typed["items"]:
        on_disk = [("🧮", k) for k in cards] + [("🖼", k) for k in units] \
            + [("📚", k) for k in keys]
        orphan = [(e, k) for e, k in on_disk
                  if k not in cited and not serves.get(k)]
        if orphan:
            rows.append('<div class=row style="margin-top:11px"><b>🎈 on disk, '
                        'cited by no bullet</b></div>')
            for emo, k in sorted(orphan, key=lambda x: (x[0], x[1])):
                rows.append('<div class=row><span class=addr></span>'
                            '<span class=warn>%s %s</span>'
                            '<span class=mut> — evidence nobody is using, or a '
                            'citation that got lost</span></div>' % (emo, _e(k)))

    source_map = ""  # the Draft Space's Reads line names the plan (JL 260927: concise)
    if minimal:
        return '<div class="card plan-card minimal-plan">%s%s</div>' % (
            source_map, "".join(rows)
        )

    # Three counts, computed INDEPENDENTLY. A folder existing is not a landed
    # answer, and a landed answer is not an accepted one; collapsing them into
    # one number is how "declared" got read as "done".
    owed = sum(tally.get(k, 0) for k in ("probe", "value", "display", "cite"))
    landed = _count_landed(txt, cards, units, keys)
    accepted = _count_accepted(txt, cards, units)
    head = "%s plan %s" % ("🔒" if approved else "✍️", _e(ver))
    gate = ('<span class=ok>approved: ✅</span>' if approved
            else '<span class=mut>approved: ⬜</span>')
    # The counts run through _e(), so an `&nbsp;` written into the STRING is
    # escaped and printed as the five literal characters (seen in the 260817
    # screenshot: "0 accepted &nbsp; aim 9"). Separators belong in the markup.
    if typed["items"]:
        item_n = len(typed["items"])
        # a state word, never a tally (AGENTS.md Page words, JL 261113)
        counts = ("decided" if typed["decided"] == item_n else
                  "decisions open" if typed["decided"] else "not decided yet")
    else:
        counts = ("accepted" if owed and accepted >= owed else "landing" if landed
                  else "owed" if owed else "")
    bundle = ""
    if bundle_rows:
        bundle = ('<details class=bundles><summary>🔗 Evidence Bundles</summary>%s</details>'
                  % "".join(bundle_rows))
    cycle_strip = _outline_cycle_strip(typed["cycle"])
    return ('<div class="card plan-card"><details class=plan-details><summary>%s · %s</summary>'
            '%s<div class=planmeta>%s</div>%s</details>%s%s</div>'
            % (head, gate, cycle_strip, _e(counts), bundle, source_map,
               "".join(rows)))
