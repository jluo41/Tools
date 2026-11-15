"""check_common.py: the small helpers and level names every check.py module shares.
Section lookup (alias_names, section_text), fence-aware line walks, the Report levels ERROR, WARN and GAP."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))
from src.common import ALIAS  # noqa: E402
from src.feedback import SEMANTIC_SECTION_ID  # noqa: E402  · the one section-id grammar


def _plan_rel(f) -> str:
    """A plan-folder file as the reader finds it from its Page folder: `draft/records/x.md`
    (`outline/...` on a Page not yet moved to draft/)."""
    f = Path(f)
    for up in f.parents:
        if up.name in ("draft", "outline"):
            return f.relative_to(up.parent).as_posix()
    return f.name


ERROR, WARN, GAP = "ERROR", "WARN", "GAP"
# One grammar, one place: src/feedback.py's SEMANTIC_SECTION_ID (260908 it gained
# the optional section index, `S-<desk>-Main-<N>-<Title>`). This checker kept a
# private copy and so read `S-JAMA-IM-Main-1-Introduction` as a legacy stage page
# and demanded a Stage Contract from a paper section (Paper-JAMA-Board, 260908).
SEMANTIC_SECTION_PAGE = re.compile(rf"^{SEMANTIC_SECTION_ID}\.md$")


def outside_checkout(base, target):
    """True when a relative target climbs out of the git checkout `base` is in.

    A board may legitimately cite a neighbouring SPACE (`env.sh`, a platforms/
    tree) that exists on the primary machine and not in a partial checkout.
    From here such a path is UNVERIFIABLE rather than known-dead, and an ERROR
    must mean known-dead (JL 260815). Resolution is lexical: the target's
    `..` climb is compared against the checkout root without touching disk.
    """
    base = Path(base).resolve()
    root = next((p for p in (base, *base.parents) if (p / ".git").exists()), None)
    if root is None:
        return False
    try:
        candidate = (base / target).resolve()
    except OSError:
        return False
    return not str(candidate).startswith(str(root) + "/") and candidate != root


def alias_names(canon):
    """Every spelling the renderer accepts for one section name."""
    return [canon] + ALIAS.get(canon, [])


def has_section(text, canon):
    for name in alias_names(canon):
        if re.search(rf"^##\s+{re.escape(name)}\s*$", text, re.M):
            return True
    return False


def section_text(text, canon):
    """Return one section using the renderer's alias table."""
    names = "|".join(re.escape(name) for name in alias_names(canon))
    found = re.search(rf"(?ms)^##\s+(?:{names})\s*$\n?(.*?)(?=^##\s+|\Z)", text)
    return found.group(1).strip() if found else ""


def state_token(value):
    """Return the renderer's normalized four-state machine token."""
    value = value.strip()
    if not value:
        return ""
    return value.split()[0].replace("\ufe0f", "")


def strip_fences(text, prose_only=False):
    """Yield (lineno, line) for lines OUTSIDE fenced code blocks.

    Every check that reads prose has to do this. A figure legitimately contains
    long lines, em-dashes and box characters, and flagging them is how a checker
    trains people to ignore it.

    `prose_only` also skips `<!-- haipipe:… -->` MANAGED SPANS (JL 260727).
    Those hold derived content: a stage's inherited contract, a skill file, a
    changelog converted into Log lines. The board did not write that text and
    cannot fix it without falsifying a quote, so style rules about the board's
    own prose do not apply to it. Converting one skill's changelog produced 79
    such warnings in a single pass, which is exactly how a checker teaches
    people to stop reading its output.
    """
    fence, managed = False, False
    for i, ln in enumerate(text.split("\n"), 1):
        st = ln.lstrip()
        if st.startswith("```"):
            fence = not fence
            continue
        if prose_only and st.startswith("<!--") and "haipipe:" in st:
            managed = ":start" in st
            continue
        if not fence and not (prose_only and managed):
            yield i, ln
