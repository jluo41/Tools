"""Where the servers sit relative to the skills they present.

The servers tree is plugin-level infrastructure, a sibling of ``skills/``,
``agents/`` and ``mcp-servers/``. Its Python needs two things from the skills:
the Page Markdown grammar (``src``) and the Page CLIs (``cli/``: ``page.py``,
``check.py``, ``draw.py``).
Everything below is derived from this file's own location, so the tree works
from a workbench checkout, a marketplace symlink, or a ``~/.claude/skills`` link
that resolves back into it.

Dependency arrow: servers import skills. Skills never import servers, except
that the Page engine reads the served asset bundle through
``skills/1_base/page/haipipe-page/src/assets.py`` and ``src/page_assets.py``.

Skills sit in three layers (``skills/0_utils``, ``skills/1_base``, ``skills/2_theme``), so a
server finds a skill or a family by its folder name (``skill_dir``), never by a fixed layer path.
"""
import functools
import sys
from pathlib import Path

HOST = Path(__file__).resolve().parent            # plugins/haipipe-toolkit/servers/_host
SERVERS = HOST.parent                              # plugins/haipipe-toolkit/servers
TOOLKIT = SERVERS.parent                           # plugins/haipipe-toolkit
WORKBENCHES = TOOLKIT.parent                           # plugins/
SKILLS = TOOLKIT / "skills"


@functools.lru_cache(maxsize=None)
def skill_dir(name):
    """The folder named ``name`` under ``skills/``: a skill (``haipipe-page``) or a family
    (``design``), nearest first, so moving a family to another layer breaks no path.
    Folders starting with ``.`` or ``_`` are skipped. When none exists the path
    ``skills/<name>`` is returned, so a missing skill fails where it is read, not at import."""
    level = [SKILLS]
    for _ in range(4):                     # layer / family / skill / sub-skill
        below = []
        for folder in level:
            try:
                children = sorted(folder.iterdir())
            except OSError:
                continue
            for child in children:
                if child.name.startswith((".", "_")) or not child.is_dir():
                    continue
                if child.name == name:
                    return child
                below.append(child)
        level = below
    return SKILLS / name


PAGE_ENGINE = skill_dir("haipipe-page")            # cli/page.py and the src/ grammar every server reads


def bootstrap():
    """Make the host and the skill grammar importable.

    The grammar is the Page engine's ``src`` and its ``cli`` helpers
    (``cli/check.py``, ``cli/draw.py``): the workbench is the one reader (JL
    261004) and the Board skill is retired (JL 261005).
    """
    host = str(HOST)
    if host not in sys.path:
        sys.path.insert(0, host)
    page = str(PAGE_ENGINE)
    if page not in sys.path:
        sys.path.insert(len(sys.path) if "src" in sys.modules else 0, page)
