"""Guide's shared base: its paths, Views, URLs, a family's profile and declared sources.

Every other guide_* module and workbench_guide.py read these; nothing here renders a page.
"""

import html
import json
from pathlib import Path
from urllib.parse import urlencode

from live.guide_families import FAMILIES, family_key

HERE = Path(__file__).resolve().parents[1]          # servers/workbench, above its home/ page/ studio/ guide/
REPOSITORY = HERE.parents[3]
STUDIO_INDEX = "/?view=radial&measure=studios"
VIEWS = (("description", "Description", "What does this Workbench do?"),
         ("method", "Method", "How does this family reach a supported answer or product?"),
         ("roadmap-draw", "RoadMap Draw", "Space · View · Run type · Agent & Skill, in one drawing"),
         ("related-paper", "Related Paper", "Which papers does this Workbench build on?"))
DRAW_NAMES = {"roadmap-draw": "RoadMap"}
# Earlier View keys (a saved link, a family's `explain` entry) and the View that now holds them.
OLD_VIEWS = {"skill-set": "roadmap-draw", "methods": "method", "workbench": "roadmap-draw", "folder-map": "roadmap-draw"}


def esc(value):
    return html.escape(str(value), quote=True)


def url(**values):
    return "/_board/guide?" + urlencode(values)


# A family's declared drawings, view only, through Guide's own route (JL 261003: a `--only
# labeling` host refuses /_excalidraw/, so the methods canvas and the Workbench design came up
# 404). `method` is the entry's method_drawing; `explain-<view>` is the board an `explain`
# drawing names. Only these declared files are served, never an arbitrary path.
def family_drawing(profile, key):
    if key == "method":
        return profile.get("method_drawing") or None
    if key.startswith("roadmap-"):                  # roadmap-<level>-<n>: a drawing guide.yaml roadmap: names
        level, _, n = key[len("roadmap-"):].partition("-")
        rows = (profile.get("roadmap") or {}).get(level) or []
        board = str(rows[int(n)].get("board", "")) if n.isdigit() and int(n) < len(rows) else ""
        return board[len("Tools/"):] if board.startswith("Tools/") else None
    if key.startswith("explain-"):
        explain = (profile.get("explain") or {}).get(key[len("explain-"):])
        if explain and explain[0] == "/_excalidraw/":
            board = str(explain[1].get("board", ""))
            return board[len("Tools/"):] if board.startswith("Tools/") else None
    return None


def drawing_url(family, key, file=""):
    # `file` names the declared drawing, so the address says which file it shows; Guide checks it
    return url(mode="drawing", guide="1", board=url(mode="drawing-scene", family=family, drawing=key).lstrip("/"),
               family=family, drawing=key, file=file)


def script_json(value):
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


def family_profile(family, context):
    profile = FAMILIES[family]
    if family == "design" and context.get("file") not in (None, "", "board.md"):
        return dict(profile, presenter="plugins/haipipe-toolkit/servers/workbench-design/design.py",
                    spaces=[("Board › Design Tasks", "One row per Design page: its task, method, N designs and how many are ready"),
                            ("Design Goal", "The task once: Aim · Venue · Rules · Resources (the starting text and its named elements) · Leave out"),
                                     ("Design", "The element matrix, then one card per design: Design · Rationale · Evaluation, its runs folded inside"),
                                     ("Delivery", "Every design whose independent Verify passed, word for word, and the csv")],
                    folders=[("Design Goal", "Design Page owner", "<same-stem Page>.md", "*.md"),
                             ("Design items", "Design Folder owner", "draft/<stem>-design-items.md", "draft/*-design-items.md"),
                             ("Runs", "Design Run owner", "runs/", "runs"),
                             ("Results and element records", "Design Run owner", "results/<run>/ (content, checks, elements.yaml)", "results"),
                             ("Delivery", "Design delivery owner", "delivery/", "delivery")])
    return profile


def instance(context):
    """Whether a Guide request names an instance whose paths it can resolve."""
    return bool(context.get("path") or context.get("file"))


def mount_guide(document, family, context, nav, native):
    """Attach one Guide button to a native Space row; retain its own layout."""
    family = family_key(family)
    if family not in FAMILIES or not (instance(context) or FAMILIES[family].get("standalone")):
        return document
    config = dict(family=family, context=context, nav=nav, native=native)
    styles = (HERE / "assets/guide-mount.css").read_text(encoding="utf-8")
    javascript = (HERE / "assets/guide-mount.js").read_text(encoding="utf-8")
    insertion = (f'<style>{styles}</style><script type="application/json" id="wb-guide-mount">'
                 f'{script_json(config)}</script><script>{javascript}</script>')
    return document.replace("</body>", insertion + "</body>", 1)


def contract_path(family, index, context=None):
    profile = family_profile(family, context or {})
    paths = ([item["path"] for item in profile["skills"]] + [profile["presenter"],
             "plugins/haipipe-toolkit/servers/workbench/guide/guide_families.py",
             "plugins/haipipe-toolkit/servers/workbench/guide/workbench_guide.py"])
    if index < 0 or index >= len(paths):
        raise ValueError("Unknown Guide source")
    candidate = (REPOSITORY / paths[index]).resolve()
    candidate.relative_to(REPOSITORY.resolve())
    if not candidate.is_file():
        raise FileNotFoundError(paths[index])
    return candidate


def folder_matches(root, source, family, row, context, allowed=None):
    """Resolve declared patterns inside the instance, with the static boundary."""
    from host_registry import static_path_allowed
    allowed = allowed or (lambda candidate: static_path_allowed(root, candidate))
    folders = family_profile(family, context)["folders"]
    if row < 0 or row >= len(folders):
        raise ValueError("Unknown folder mapping")
    pattern = folders[row][3]
    base = source.parent
    matches = []
    for candidate in base.glob(pattern):
        if allowed(candidate):
            matches.append(candidate)
            if len(matches) >= 80:
                break
    return sorted(matches)

