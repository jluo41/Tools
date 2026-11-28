"""Track changes for a Revise Run: the before and after text drawn as word and
sentence insertions and deletions (moved verbatim from runs.py).
"""
from __future__ import annotations

import difflib
import html
import re

# runs.py imports this module after it defines these helpers, so load it through live.runs.


def _token_track_changes(before: str, after: str) -> str:
    """Render one paired span with document-like lexical replacements."""
    # Bind leading space to its lexical token. Treating whitespace as an
    # independent match makes a replaced phrase alternate old/new word by word,
    # which is technically granular but visually unlike document Track Changes.
    token = re.compile(r"\s*(?:[\w]+(?:['’\-][\w]+)*|[^\w\s])", re.UNICODE)
    old = token.findall(before.strip())
    new = token.findall(after.strip())
    output = []
    for operation, a1, a2, b1, b2 in difflib.SequenceMatcher(
            None, old, new, autojunk=False).get_opcodes():
        old_text = html.escape("".join(old[a1:a2]))
        new_text = html.escape("".join(new[b1:b2]))
        if operation == "equal":
            output.append(old_text)
        elif operation == "delete":
            output.append(f"<del>{old_text}</del>")
        elif operation == "insert":
            output.append(f"<ins>{new_text}</ins>")
        else:
            output.append(f"<del>{old_text}</del><ins>{new_text}</ins>")
    return "".join(output)


def _track_sentences(value: str) -> list[str]:
    """Keep sentence whitespace so inserted/deleted sentences read naturally."""
    return [match.group(0) for match in re.finditer(
        r".*?(?:[。！？]+|[.!?]+(?=\s|$))(?:\s+|$)|.+$", value.strip(), re.S
    ) if match.group(0)]


def _sentence_similarity(left: str, right: str) -> float:
    token = re.compile(r"[\w]+(?:['’\-][\w]+)*|[^\w\s]", re.UNICODE)
    matcher = difflib.SequenceMatcher(
        None, token.findall(left.lower()), token.findall(right.lower()),
        autojunk=False,
    )
    longest_anchor = max((block.size for block in matcher.get_matching_blocks()),
                         default=0)
    return longest_anchor + matcher.ratio()


def _word_track_changes(before: str, after: str) -> str:
    """Render safe Track Changes: whole sentences, then word-level edits."""
    old_sentences = _track_sentences(before)
    new_sentences = _track_sentences(after)
    if len(old_sentences) == 1 and len(new_sentences) > 1:
        paired = max(range(len(new_sentences)),
                     key=lambda index: _sentence_similarity(
                         old_sentences[0], new_sentences[index]))
        if _sentence_similarity(old_sentences[0], new_sentences[paired]) >= 1.3:
            return "".join(
                _token_track_changes(old_sentences[0], sentence)
                if index == paired else f"<ins>{html.escape(sentence)}</ins>"
                for index, sentence in enumerate(new_sentences)
            )
    if len(new_sentences) == 1 and len(old_sentences) > 1:
        paired = max(range(len(old_sentences)),
                     key=lambda index: _sentence_similarity(
                         old_sentences[index], new_sentences[0]))
        if _sentence_similarity(old_sentences[paired], new_sentences[0]) >= 1.3:
            return "".join(
                _token_track_changes(sentence, new_sentences[0])
                if index == paired else f"<del>{html.escape(sentence)}</del>"
                for index, sentence in enumerate(old_sentences)
            )
    return _token_track_changes(before, after)


def _track_change_html(section: str) -> str:
    saved = _section_body(section, "Saved result")
    track_section = _subsection_body(saved, "Track changes")
    matches = list(re.finditer(r"^#####[ \t]+(.+?)[ \t]*$", track_section, re.M))
    cards = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(track_section)
        body = track_section[match.end():end].strip()
        before = _level_heading_body(body, 6, "Before")
        after = _level_heading_body(body, 6, "After")
        # A Track Changes card represents an actual text transition. Lifecycle,
        # navigation, and presenter-only feedback belongs in the ordinary
        # Changes record and must not create an empty visual diff.
        if not before or not after or before == after:
            continue
        why = _level_heading_body(body, 6, "Why")
        decision = _level_heading_body(body, 6, "Decision")
        preference = _level_heading_body(body, 6, "Inferred preference")
        analysis = _level_heading_body(body, 6, "Analysis status")
        status = _level_heading_body(body, 6, "Preference status")
        title = match.group(1).strip()
        title_parts = [part.strip() for part in title.split("·", 1)]
        identifier = title_parts[0]
        feedback_match = re.fullmatch(r"F0*(\d+)", identifier, re.I)
        display_identifier = (
            f"Feedback {int(feedback_match.group(1))}"
            if feedback_match else identifier
        )
        kind = title_parts[1] if len(title_parts) > 1 else "Unclassified change"
        cards.append(
            '<section class=track-card><h4>%s</h4><p class=track-kind>%s</p>'
            '<div class=track-legend><span class=removed>Deleted</span>'
            '<span class=added>Added</span></div><div class=track-diff>%s</div>%s%s%s%s%s</section>' % (
                html.escape(display_identifier), html.escape(kind),
                _word_track_changes(before, after),
                ('<p class=why><b>Why</b><br>%s</p>' % _inline_markdown(why)) if why else "",
                ('<p class=track-decision><b>Decision</b><br>%s</p>' % _inline_markdown(decision)) if decision else "",
                ('<p class=preference><b>Inferred preference</b><br>%s</p>' %
                 _inline_markdown(preference)) if preference else "",
                ('<p class=track-status>%s</p>' % _inline_markdown(status)) if status else "",
                ('<p class=track-status><b>Analysis</b><br>%s</p>' %
                 _inline_markdown(analysis)) if analysis else "",
            )
        )
    return "".join(cards)


# looked up when called, never at import: the old module re-exports this file's names, so either can be imported first
def _inline_markdown(*args, **kwargs):
    from live.runs import _inline_markdown as real
    return real(*args, **kwargs)


def _level_heading_body(*args, **kwargs):
    from live.runs import _level_heading_body as real
    return real(*args, **kwargs)


def _section_body(*args, **kwargs):
    from live.runs import _section_body as real
    return real(*args, **kwargs)


def _subsection_body(*args, **kwargs):
    from live.runs import _subsection_body as real
    return real(*args, **kwargs)
