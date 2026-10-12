"""Small, shared rules for reader-facing identity names.

Names are addresses, not explanations.  The prose contract lives in
``ref/writing-rules.md``; this module owns only the mechanical edge that the
checker and live creation routes must agree on.
"""

import re


NAME_TARGET_WORDS = 6
NAME_MAX_WORDS = 8
NAME_WORD = re.compile(
    r"[A-Za-z]+(?:['’][A-Za-z]+)*(?:-[A-Za-z0-9]+)*|[\u3400-\u9fff]"
)

# These are narrow title scaffolds, not a general banned-word list.  A term
# such as "framework" or "robust" may be exact technical language; these
# phrases usually add posture without helping a reader distinguish one item
# from its sibling.
AI_FLAVOR = (
    (re.compile(r"^\s*(?:a\s+)?comprehensive\b", re.I), "comprehensive"),
    (re.compile(r"^\s*(?:a\s+)?holistic\b", re.I), "holistic"),
    (re.compile(r"\bseamless(?:ly)?\b", re.I), "seamless"),
    (re.compile(r"\bcutting-edge\b", re.I), "cutting-edge"),
    (re.compile(r"\bnext-generation\b", re.I), "next-generation"),
    (re.compile(r"\bbest-in-class\b", re.I), "best-in-class"),
    (re.compile(r"\bultimate guide\b", re.I), "ultimate guide"),
    (re.compile(r"\bdeep dive\b", re.I), "deep dive"),
    (re.compile(r"^\s*(?:understanding|exploring|unlocking|reimagining)\b", re.I),
     "generic opening"),
)


def name_words(text):
    """Return reader-facing English words or individual Han characters."""
    return NAME_WORD.findall(text or "")


def ai_flavor(text):
    """Return the first generic title scaffold, or an empty string."""
    for pattern, label in AI_FLAVOR:
        if pattern.search(text or ""):
            return label
    return ""


def name_problem(text, kind="name"):
    """Return the mechanical reason an authored identity name is rejected."""
    words = name_words(text)
    if len(words) > NAME_MAX_WORDS:
        return (f"the {kind} has {len(words)} reader-facing words; use "
                f"{NAME_TARGET_WORDS} or fewer and never more than "
                f"{NAME_MAX_WORDS}")
    flavor = ai_flavor(text)
    if flavor:
        return (f"the {kind} uses generic model-like wording ({flavor!r}); "
                "name the concrete object, action, or outcome")
    return ""


def compact_name(text, maximum=NAME_MAX_WORDS):
    """Bound an automatically derived fallback name without cutting a token.

    Authored names are rejected by :func:`name_problem` and must be rewritten.
    This helper is only for the session picker fallback derived from the first
    user message, where no authored name exists yet.
    """
    text = " ".join((text or "").split())
    matches = list(NAME_WORD.finditer(text))
    if len(matches) <= maximum:
        return text
    return text[:matches[maximum - 1].end()].rstrip(" ,.;:-")
