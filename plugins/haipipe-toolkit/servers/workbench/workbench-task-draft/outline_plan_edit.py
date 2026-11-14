"""Editing one plan bullet: add, change or drop a bullet and write the result
as the next shape version of the plan (moved verbatim from outline.py).
"""
import datetime as dt
import re

from src.outline_version import plan_dir, record_path
from src.plan_layout import from_canonical
from src.plan_shape import canonical_plan

# outline.py imports this module after it defines these two, so load it through live.outline.


def _replace_header(text, key, value):
    """Replace one plan header row, inserting it after the version when absent."""
    pat = re.compile(r"(?m)^%s:.*$" % re.escape(key))
    line = "%s: %s" % (key, value)
    if pat.search(text):
        return pat.sub(line, text, count=1)
    lines = text.splitlines()
    at = 1 if lines and lines[0].startswith("#") else 0
    lines.insert(at, line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def _working_plan_text(text, old_tag, new_tag, action, paragraph, bullet):
    """Turn an approved plan into an explicitly unapproved working Shape."""
    text = re.sub(
        r"(?m)^(#.*?\b(?:outline|draft)\s+)v\d+(?:\.\d+){0,2}(.*)$",
        lambda m: "%sv%s%s" % (m.group(1), new_tag[1:], m.group(2)),
        text,
        count=1,
    )
    key = "draft-version" if re.search(r"(?m)^draft-version:", text) else "outline-version"
    text = _replace_header(text, key, new_tag)
    text = _replace_header(
        text, "supersedes",
        "%s · working Shape copy created by the Outline Bullet editor" % old_tag,
    )
    text = _replace_header(text, "working-copy-of", old_tag)
    text = _replace_header(text, "approved", "⬜")
    text = _replace_header(text, "shape-accepted", "⬜ · pending human review")
    text = _replace_header(
        text, "date", dt.datetime.now().strftime("%y%m%d"),
    )
    text = _replace_header(
        text, "status",
        "OUTLINE · %s working Shape; Bullet %s %s pending review"
        % (new_tag, paragraph, bullet),
    )
    return text


def _plan_region(lines, paragraph):
    """Return the heading and exclusive end indexes for one C.P paragraph."""
    wanted = (paragraph or "").strip()
    if not re.fullmatch(r"C\d+\.P\d+", wanted):
        return None, "paragraph must be a C<n>.P<m> address"
    heading = re.compile(r"^###\s+%s\s*(?:·|$)" % re.escape(wanted))
    start = next((i for i, line in enumerate(lines) if heading.match(line)), None)
    if start is None:
        return None, "paragraph %s was not found in the current Shape" % wanted
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("### ") or lines[i].startswith("## "):
            end = i
            break
    return (start, end), None


def _bullet_line(line):
    return re.match(r"^(?P<prefix>-\s+B(?P<number>\d+)\s*·\s*)(?P<body>.*)$", line)


def _normalise_head(value):
    # A Bullet head is one Markdown line.  Newlines from a mobile textarea are
    # intentionally folded rather than allowed to create accidental records.
    return " ".join((value or "").replace("\r", " ").replace("\n", " ").split())


def _edit_plan_bullet(page_src, action, paragraph, bullet, head,
                      note="", evidence="", accept="", structured=False):
    """Edit/append one Bullet, preserving an approved plan byte-for-byte.

    Returns a small receipt for the Board endpoint.  The first write against an
    approved plan creates the next bounded, unapproved Shape; subsequent writes
    reuse that working file.  No generated Board HTML is touched here.
    """
    plan, old_tag = _latest_plan(page_src)
    if plan is None:
        return None, "this Page has no Outline Shape plan"
    raw_head = _normalise_head(head)
    if not raw_head:
        return None, "Bullet text is empty"
    # This legacy editor rewrites dash lines, so it works on the classic shape.
    raw_source = plan.read_text(encoding="utf-8", errors="replace")
    text = canonical_plan(raw_source)
    # Validate the address before making any working copy. A mistyped mobile
    # submission must be a no-op, including when the current plan is approved.
    pre_region, pre_err = _plan_region(text.splitlines(), paragraph)
    if pre_err:
        return None, pre_err
    if action == "edit-bullet":
        wanted = (bullet or "").strip()
        if not re.fullmatch(r"B\d+[a-z]*", wanted):
            return None, "bullet must be a B<n> address"
        if not any(
            (m := _bullet_line(line)) and "B%s" % m.group("number") == wanted
            for line in text.splitlines()[pre_region[0] + 1:pre_region[1]]
        ):
            return None, "%s was not found under %s" % (wanted, paragraph)
    elif action != "append-bullet":
        return None, "unknown Bullet action"
    approved = bool(re.search(r"(?m)^approved:\s*✅", text))
    destination = plan
    new_tag = old_tag
    created = False
    if approved:
        new_tag = _next_shape_version(old_tag)
        kind = "draft" if "-draft-v" in plan.name else "outline"
        destination = plan.parent / ("%s-%s-%s.md" % (page_src.stem, kind, new_tag))
        # Never overwrite an existing plan while resolving a concurrent request;
        # advance until a free Shape filename is found rather than ever
        # mutating an already-approved file.
        if destination.exists():
            while destination.exists():
                new_tag = _next_shape_version(new_tag)
                destination = plan.parent / ("%s-%s-%s.md" % (page_src.stem, kind, new_tag))
            text = _working_plan_text(text, old_tag, new_tag, action, paragraph, bullet)
            created = True
        else:
            text = _working_plan_text(text, old_tag, new_tag, action, paragraph, bullet)
            created = True

    lines = text.splitlines()
    region, err = _plan_region(lines, paragraph)
    if err:
        return None, err
    start, end = region
    if action == "edit-bullet":
        wanted = (bullet or "").strip()
        if not re.fullmatch(r"B\d+[a-z]*", wanted):
            return None, "bullet must be a B<n> address"
        hit = None
        for i in range(start + 1, end):
            m = _bullet_line(lines[i])
            if m and "B%s" % m.group("number") == wanted:
                hit = i
                break
        if hit is None:
            return None, "%s was not found under %s" % (wanted, paragraph)
        m = _bullet_line(lines[hit])
        slot = re.match(r"(S\d+\s*·\s*)", m.group("body"))
        if slot and not re.match(r"^S\d+\s*·\s*", raw_head):
            raw_head = slot.group(1) + raw_head
        lines[hit] = m.group("prefix") + raw_head
        changed = True
    elif action == "append-bullet":
        note = _normalise_head(note)
        evidence = _normalise_head(evidence)
        accept = _normalise_head(accept)
        # Direct callers that supply the structured fields are opting into the
        # same Note/Evidence contract as the browser form.  Keep the legacy
        # head-only helper path for internal callers and existing plans.
        structured = bool(structured or note or evidence or accept)
        if structured:
            if not note:
                return None, "a new Bullet needs a Note"
            if not re.match(
                r"^(?:none|E\d+-(?:VALUE|CITE|DISPLAY)-[a-z0-9]+(?:-[a-z0-9]+)*)\s+·\s+\S",
                evidence,
                re.I,
            ):
                return None, "Evidence must be `none · reason` or a typed E<n>-TYPE-name declaration"
            if not evidence.lower().startswith("none") and not accept:
                return None, "typed Evidence needs an Accept contract"
        numbers = []
        sentence_numbers = []
        last = None
        for i in range(start + 1, end):
            m = _bullet_line(lines[i])
            if not m:
                continue
            numbers.append(int(m.group("number")))
            sm = re.search(r"\bS(\d+)\s*·", m.group("body"))
            if sm:
                sentence_numbers.append(int(sm.group(1)))
            last = i
        number = max(numbers or [0]) + 1
        sentence = max(sentence_numbers or [0]) + 1
        raw_head = re.sub(r"^S\d+\s*·\s*", "", raw_head)
        new_line = "- B%d · S%d · %s" % (number, sentence, raw_head)
        if last is None:
            insert_at = start + 1
        else:
            insert_at = last + 1
            # Keep the new Bullet after the existing Bullet's indented Note /
            # Evidence / Result lines, while not swallowing the next heading.
            while insert_at < end:
                if lines[insert_at].startswith("  "):
                    insert_at += 1
                    continue
                if (not lines[insert_at].strip() and insert_at + 1 < end
                        and lines[insert_at + 1].startswith("  ")):
                    insert_at += 1
                    continue
                break
        # Bullets follow one another directly in a Shape file; a blank line
        # belongs only before the next heading, never between Bullets.
        additions = [new_line]
        if structured:
            additions.extend(["  Note: %s" % note, "  Evidence: %s" % evidence])
            if not evidence.lower().startswith("none"):
                additions.append("  Accept: %s" % accept)
        lines[insert_at:insert_at] = additions
        bullet = "B%d" % number
        changed = True
    else:
        return None, "unknown Bullet action"

    if not changed:
        return None, "nothing changed"
    updated = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    updated = from_canonical(raw_source, updated)  # a three-section file stays three sections
    # Atomic replace keeps a mobile double-tap from leaving a truncated plan.
    tmp = destination.with_name(destination.name + ".tmp-%d" % id(lines))
    tmp.write_text(updated, encoding="utf-8")
    tmp.replace(destination)
    log = record_path(plan_dir(page_src.parent), page_src.stem, "log")
    log.parent.mkdir(parents=True, exist_ok=True)
    if created and log.is_file():
        stamp = dt.datetime.now().strftime("%y%m%d %H%M")
        with log.open("a", encoding="utf-8") as fh:
            fh.write("\n### %s · working Shape %s created from %s\n"
                     "- **Action**: %s %s %s\n" %
                     (stamp, new_tag, old_tag, action, paragraph, bullet))
    return {
        "version": new_tag,
        "plan": str(destination),
        "created_working_shape": created,
        "approved_plan": old_tag if created else "",
        "paragraph": paragraph,
        "bullet": bullet,
    }, None


# looked up when called, never at import: the old module re-exports this file's names, so either can be imported first
def _latest_plan(*args, **kwargs):
    from live.outline import _latest_plan as real
    return real(*args, **kwargs)


def _next_shape_version(*args, **kwargs):
    from live.outline import _next_shape_version as real
    return real(*args, **kwargs)
