"""Where the servers sit relative to the skills they present.

The servers tree is plugin-level infrastructure, a sibling of ``skills/``,
``agents/`` and ``mcp-servers/``. Its Python needs two things from the skills:
the Board/Page Markdown grammar (``src``) and the Board CLIs (``cli/build.py``).
Everything below is derived from this file's own location, so the tree works
from a workbench checkout, a marketplace symlink, or a ``~/.claude/skills`` link
that resolves back into it.

Dependency arrow: servers import skills. Skills never import servers, except
the two static builders that read the served asset bundle through
``skills/board/haipipe-board/src/assets.py`` and
``skills/page/haipipe-page/src/page_assets.py``.
"""
import sys
from pathlib import Path

HOST = Path(__file__).resolve().parent            # plugins/haipipe-toolkit/servers/_host
SERVERS = HOST.parent                              # plugins/haipipe-toolkit/servers
TOOLKIT = SERVERS.parent                           # plugins/haipipe-toolkit
WORKBENCHES = TOOLKIT.parent                           # plugins/
SKILLS = TOOLKIT / "skills"
BOARD_ENGINE = SKILLS / "board" / "haipipe-board"  # cli/build.py, src/ grammar, checks/
PAGE_ENGINE = SKILLS / "page" / "haipipe-page"     # cli/page.py, src/ grammar


def bootstrap():
    """Make the host and the skill grammar importable.

    The first importer decides which ``src`` grammar the process runs on: the
    Board server calls this before importing anything, so the Board engine's
    ``src`` (which merges Page's) comes first; a standalone Page server has
    already imported Page's ``src`` and keeps it, so the Board engine is only
    appended for ``cli.*`` helpers.
    """
    host = str(HOST)
    if host not in sys.path:
        sys.path.insert(0, host)
    engine = str(BOARD_ENGINE)
    if engine not in sys.path:
        sys.path.insert(len(sys.path) if "src" in sys.modules else 0, engine)
