"""Each workbench button's Run name, read off the server code (JL 261007-08: a button is named by the soft
Run it makes, `run-<type>-<target>`; haipipe-run rule 6). The drawings name their buttons through
name_of(), so a screen in s11 · s12 · s13 shows what the live frame shows.

Read from each theme's run cards (skills/**/run-cards.md: 🔘 BUTTON … then 🏷 RUN …), and from servers/: each theme's RUN_NAMES ({its words: the Run}), the frame's PAGE_RUN_NAMES, every
run_type("run-…", "what it does", …) call and every {"label": "run-…", "doing": "…"} kind. A phrase
with no Run name stays as it is.
"""
import re
from functools import lru_cache
from pathlib import Path

TOOLKIT = Path(__file__).resolve().parents[4] / "plugins" / "haipipe-toolkit"
SERVERS = TOOLKIT / "servers"
_CARD = re.compile(r"🔘 BUTTON\s+(.+?)\s+·[^\n]*\n(?:[^\n]*\n){0,3}?🏷 RUN\s+(\S+)")         # a run card's button and its Run
# the base's Idea Studio button is one Run for three words (haipipe-run rule 6), and the plain "Run"
ALIASES = {"add a topic": "run-draw-<sNN>", "redraw a topic": "run-draw-<sNN>", "redraw": "run-draw-<sNN>",
           "save this session": "run-draw-<sNN>", "draw": "run-draw-<sNN>", "run": "run-<type>-<target>"}
# the drawings' own words for a button the server already names (261008): the same Run, other words
DRAWN = {"add topic": "run-draw-<sNN>", "release": "run-release-<target>", "rank and keep": "run-rank-t99", "keep this chat": "run-draw-<sNN>", "draw the logic": "run-draw-<sNN>", "build a map": "run-labeling-embedding-<job>",
         "redraw the section map": "run-draw-<sNN>", "draw the report": "run-figures-<qNN>",
         "structure the report": "run-structure-<slug>", "build the report": "run-delivery-<target>",
         "build a delivery": "run-delivery-<target>", "build the article": "run-delivery-<target>",
         "export bibtex": "run-delivery-<target>", "edit the spine": "run-face-<bNN>",
         "update the dikw level": "run-face-<jNN>", "update the inquiry": "run-face-<jNN>",
         "set up a job": "run-add-<jNN>", "set up the job": "run-labeling-contract-<job>", "open a dikw level": "run-add-<jNN>",
         "add a task": "run-add-<tNN>", "plan its tasks": "run-plan-<tNN>", "launch all": "run-launch-<jNN>",
         "add design tasks": "run-add-job-j<NN>", "add an item": "run-add-related-<slug>",
         "find related work": "run-add-related-<slug>", "record the extract": "run-add-version-<d>vM",
         "release the job's output": "run-release-j<NN>", "passed review": "run-release-j<NN>",
         "generate": "run-generate-d<NN>", "revise one": "run-revise-d<NN>",
         "create the job": "run-labeling-open-<job>", "freeze the handoff": "run-labeling-handoff-<job>",
         "publish final labels": "run-labeling-final-<job>", "start a round": "run-labeling-round-<NN>",
         "prepare a round": "run-labeling-round-<NN>", "label the round": "run-labeling-round-<NN>",
         "close the round": "run-labeling-round-<NN>", "learn the guideline": "run-labeling-guideline-<job>",
         "measure": "run-labeling-round-<NN>", "score executors": "run-labeling-evaluation-<job>"}
_PAIR = re.compile(r'"([^"\n]{2,60})":\s*"((?:run-|rNN_)[^"\n]+)"')                  # "Plan a Task": "run-plan-<tNN>"
_CALL = re.compile(r'run_type\(\s*f?"((?:run-|rNN_)[^"\n]+)",\s*"([^"\n]+)"')         # run_type("run-…", "doing", …)
_KIND = re.compile(r'"label":\s*f?"((?:run-|rNN_)[^"\n]+)",\s*"doing":\s*"([^"\n]+)"')  # {"label": "run-…", "doing": "…"}


def _clean(name: str) -> str:
    """An f-string's {tag} / {folder.name…} as a placeholder: run-face-{tag} -> run-face-<tag>."""
    return re.sub(r"\{[^}]*\}", "<id>", name).replace("<id>", "<tag>") if "{" in name else name


@lru_cache(maxsize=1)
def table() -> dict:
    """{a button's words, lower case: its Run name}."""
    out = dict(ALIASES, **DRAWN)
    for cards in sorted(TOOLKIT.glob("skills/**/run-cards.md")):    # a theme's run cards (paper, design, …)
        for words, run in _CARD.findall(cards.read_text(encoding="utf-8", errors="ignore")):
            out.setdefault(words.strip().lower(), _clean(run))
    for py in sorted(SERVERS.glob("workbench*/*.py")):
        src = py.read_text(encoding="utf-8", errors="ignore")
        for words, run in _PAIR.findall(src):
            if "_" not in words and not run.endswith("-"):     # a button's words, not a dict key (run_id)
                out.setdefault(words.lower(), _clean(run))
        for run, doing in _CALL.findall(src) + _KIND.findall(src):
            out.setdefault(doing.lower(), _clean(run))
    return out


def name_of(label: str) -> str:
    """The Run a button makes, or the label itself when it names none (a ↗ link, a view)."""
    if label.startswith(("run-", "rNN_")):
        return label
    return table().get(label.strip().lstrip("+").strip().lower(), label)


def named(label: str) -> bool:
    """Whether the button has a Run name yet (a drawing shows the others in red, open)."""
    return name_of(label).startswith(("run-", "rNN_"))
