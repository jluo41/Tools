"""Bridge to the browser assets, which live with the servers.

The JS/CSS parts a rendered Board page loads are owned and assembled by
``plugins/haipipe-toolkit/servers`` (``_host/host_assets.py``): every server
folder contributes ``assets/js/**`` and ``assets/css/**`` parts, concatenated in
sorted relative order. The static build in this skill writes the same bundle
into ``board/_assets/``, so this module re-exports that assembler instead of
keeping a second copy of the parts.
"""
import pathlib
import sys

_HOST = pathlib.Path(__file__).resolve().parents[4] / "servers" / "_host"
if str(_HOST) not in sys.path:
    sys.path.insert(0, str(_HOST))
import host_assets as _host_assets  # noqa: E402

CSS_CHARSET = _host_assets.CSS_CHARSET
BOARD_MARK = _host_assets.BOARD_MARK
board_mark = _host_assets.board_mark
parts = _host_assets.parts
js = _host_assets.js
css = _host_assets.css
verify = _host_assets.verify
