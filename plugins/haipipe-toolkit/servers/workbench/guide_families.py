"""Family-owned Guide bindings. Paths are relative to the plugin repository.

Working Space rosters describe the current native presenters. The Task
question interface has its own design and writer; this registry does not
create question, progress or drawing stores for an instance.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_host"))
from host_paths import TOOLKIT as _TOOLKIT_DIR, skill_dir  # noqa: E402

TOOLKIT = "plugins/haipipe-toolkit/"
SKILLS = TOOLKIT + "skills/"


def at(name, rest=""):
    """A skill folder's path, found by its folder name (skills sit in 0_utils · 1_base · 2_theme)."""
    return TOOLKIT + skill_dir(name).relative_to(_TOOLKIT_DIR).as_posix() + "/" + rest


# The Page workbench design drawing, hand-made (JL 261003: "update your workbench design as well");
# Paper's is named in servers/workbench-paper/guide/guide.yaml.
PAGE_DESIGN = "Tools/" + TOOLKIT + "servers/workbench/task-page/studio/page-workbench-design.excalidraw"


def skill(name, role):
    return {"path": at(name, "SKILL.md"), "role": role}


FAMILIES = {
    # "paper", the Paper family's Guide, lives in servers/workbench-paper/guide/guide.yaml (261007)
    # "task", the work theme's Guide, lives in servers/workbench-work/guide/guide.yaml (261007)
    # "cowork", the CoWork Guide, lives in servers/workbench-cowork/guide/guide.yaml (261007)
    # "discovery" lives in servers/workbench-discovery/guide/guide.yaml (261007)
    # "page", the Page Task's Guide, lives in servers/workbench/task-page/guide/guide.yaml (261007)
    # "insight", the Insight family's Guide, lives in servers/workbench-insight/guide/guide.yaml (261007)
    # "design", the design theme's Guide, lives in servers/workbench-design/guide/guide.yaml (261007)
    # "labeling", the Labeling Guide, lives in servers/workbench-labeling/guide/guide.yaml (261007)
    # The Shared Workbench explains itself; it has no Board, so its folders are this server folder's files.
    # "shared", the base workbench's own Guide, lives in servers/workbench/guide/guide.yaml (261007)
}


# ── each theme's own Guide (JL 261007): servers/workbench-<theme>/guide/guide.yaml + related/ ──
# A family whose server folder carries guide/guide.yaml is read from there, and that file wins
# over its entry above; the entries above go as each theme moves its Guide home. The file holds
# the same keys as an entry. Its paths: "guide/…" or "related/…" (or a module such as
# "paper.py") are relative to the server folder; "skill:<skill>/<rest>" is a file of that skill,
# found by name; "Tools/…" is SPACE-relative (a RoadMap drawing in its design Block).
#
#   servers/workbench-<theme>/
#   ├── guide/   guide.yaml · method.md · methods.excalidraw     Description · Method · RoadMap Draw
#   └── related/ papers.md · papers/<pdf>                       Related Paper
_PATH_KEYS = ("presenter", "table", "method_doc", "method_drawing", "papers_table")


def _path(folder, value):
    if not isinstance(value, str) or value.startswith("Tools/"):
        return value
    if value.startswith("skill:"):
        name, _, rest = value[len("skill:"):].partition("/")
        return at(name, rest)
    return TOOLKIT + (folder / value).relative_to(_TOOLKIT_DIR).as_posix()


def _rows(value):
    """YAML lists back to the tuples an entry holds: a list of lists becomes a list of tuples; a
    dict (design's flow: logic, data, links lists and a repeat line) has each of its values
    treated the same way; a string stays as it is."""
    if isinstance(value, dict):
        return {k: _rows(v) for k, v in value.items()}
    if isinstance(value, list):
        return [tuple(x) if isinstance(x, list) else x for x in value]
    return value


# ── the card Guide (b03 studio/s31-guide, s31-D05 to D08) ──────────────────────────────────────
# A family whose guide.yaml declares `levels:` is drawn as the card Guide: each View in three folding
# sections, Block · Job · Task, each a stack of cards. The base's words are servers/workbench/guide/
# levels.yaml; `levels:` overrides only the words that differ; `roadmap:` lists drawings per level.
LEVEL_NAMES = ("Block", "Job", "Task")
LEVELS_FILE = Path(__file__).resolve().parent / "guide" / "levels.yaml"
# An old family key still answers, as the name it now has (the work theme was "task", 261007).
ALIASES = {"task": "work"}


def family_key(name):
    """The family a Guide request names, after its alias."""
    return ALIASES.get(name, name)


def base_levels():
    """The base's card words: {level: {"role": str, "spaces": {Space: {"is", "reads"}}}}."""
    import yaml
    try:
        return yaml.safe_load(LEVELS_FILE.read_text(encoding="utf-8")) or {}
    except OSError:
        return {}


def merge_levels(base, own):
    """The base's words with a theme's `levels:` laid over them, word by word."""
    out = {}
    for level in LEVEL_NAMES:
        b, o = base.get(level) or {}, (own or {}).get(level) or {}
        spaces = {name: dict(words) for name, words in (b.get("spaces") or {}).items()}
        for name, words in (o.get("spaces") or {}).items():
            spaces[name] = {**spaces.get(name, {}), **(words or {})}
        out[level] = {**{k: v for k, v in b.items() if k != "spaces"},
                      **{k: v for k, v in o.items() if k != "spaces"}, "spaces": spaces}
    return out


def load_guide(folder):
    """(family, entry) from <folder>/guide/guide.yaml, in the shape of an entry above."""
    import yaml
    raw = yaml.safe_load((folder / "guide" / "guide.yaml").read_text(encoding="utf-8")) or {}
    family = raw.pop("family")
    if "levels" in raw:                           # the card Guide: the base's words, then the theme's
        raw["levels"] = merge_levels(base_levels(), raw["levels"])
    if "roadmap" in raw:                          # {level: [{title, shows, board}]}; boards are Tools/… paths
        raw["roadmap"] = {level: list(raw["roadmap"].get(level) or []) for level in LEVEL_NAMES}
    entry = {k: _path(folder, v) if k in _PATH_KEYS else v for k, v in raw.items()}
    entry["skills"] = [skill(s["skill"], s.get("role", "")) for s in entry.get("skills", [])]
    for key in ("method", "spaces", "folders", "flow"):
        if key in entry:
            entry[key] = _rows(entry[key])
    entry["explain"] = {k: tuple(v) for k, v in (entry.get("explain") or {}).items()}
    entry["guide_home"] = TOOLKIT + (folder / "guide").relative_to(_TOOLKIT_DIR).as_posix()
    return family, entry


def _load_guides():
    from host_registry import workbench_folders
    for folder in workbench_folders():
        if (folder / "guide" / "guide.yaml").is_file():
            try:
                family, entry = load_guide(folder)
            except Exception as error:            # a broken file keeps the old entry, and says so
                print(f"guide_families: {folder.name}/guide/guide.yaml not loaded: {error}", file=sys.stderr)
                continue
            FAMILIES[family] = entry


_load_guides()
