"""The browser assets, assembled from parts across every server folder.

Each server folder (``_host``, ``haipipe-board``, ``haipipe-page``,
``workbench-*``, and sibling workbenches' ``servers/workbench-*``) keeps its own
parts under ``assets/js/**`` and ``assets/css/**``. They are gathered here and
concatenated in sorted RELATIVE path order, so a part's numeric prefix still
says where it goes no matter which folder owns it, and the assembled file is
byte-identical to the one the single ``assets/`` tree used to produce.

JL 260731: "把所有东西都写到一个 board.js 吗? 能不能像 live 一样分成不同的
part... 现在又是到了那种牵一发而动全身的窘境."

board.js had grown to 3509 lines and board.css to 1565, so every edit read as a
risk to everything else. They are now written as topic files under `assets/js/`
and `assets/css/`, and assembled here into the single file each page loads.

The assembly rule is deliberately the dumbest one that can work: CONCATENATE
EVERY PART IN SORTED PATH ORDER. No manifest to keep in sync, no import graph,
no build step a reader has to learn. The numeric prefixes ARE the order, and a
new part is a new file whose name says where it goes.

Order is load-bearing for JS, because the parts are fragments of top-level
IIFEs: `10-drawer/00-open.js` opens a closure that `10-drawer/50-structure.js`
closes, and everything between shares its scope. That is the same reason the
live layer's mixins compose in a fixed order (QC8). Splitting a shared closure
across files only stays safe while the concatenation is exact, so `verify()`
below is the gate: it is called on every load, and a part that does not
reassemble into balanced JavaScript fails the build rather than the browser.
"""
import pathlib
import sys

_HOST = pathlib.Path(__file__).resolve().parent
if str(_HOST) not in sys.path:
    sys.path.insert(0, str(_HOST))
from host_paths import SERVERS  # noqa: E402
from host_registry import asset_roots  # noqa: E402

BOARD_MARK = SERVERS / "haipipe-board" / "assets" / "board-mark.svg"


def board_mark():
    """The Board mark, embedded as favicon by the renderer and the shell."""
    return BOARD_MARK.read_text(encoding="utf-8").strip()


def _join(folder, suffix):
    found = parts(folder, suffix)
    if not found:
        raise RuntimeError(f"no {suffix} parts under any server assets/{folder}")
    return "\n".join(p.read_text(encoding="utf-8") for p in found)


def js():
    """assets/js/**.js concatenated in sorted path order."""
    return _join("js", ".js")


def css():
    """assets/css/**.css concatenated in sorted path order."""
    return _join("css", ".css")


# A stylesheet does NOT inherit the HTML document's encoding. When the server
# sends `Content-Type: text/css` with no charset parameter, which is exactly
# what Python's own `mimetypes` sends, the browser falls back to its LOCALE
# default: windows-1252 on most machines. Every non-ASCII glyph in a `content:`
# rule then mojibakes, and the one that shows is the fold marker on each
# section header: `▸` (UTF-8 e2 96 b8) renders as `â–¸` (JL 260819, screenshot
# of Outline / Content / Aims / States / Files).
#
# This is the half of the fix that travels WITH the file, so it also holds
# under `file://` and under any server that is not `servers/_host/serve.py`. It must be
# the first bytes of the stylesheet: a comment or even a blank line in front of
# it makes the browser ignore the rule. It is prepended at WRITE time rather
# than inside `css()`, because `css()` is also inlined into a `<style>` element
# by the legacy single-file build, and `@charset` is not valid there.
CSS_CHARSET = '@charset "utf-8";\n'


def parts(folder="js", suffix=".js"):
    """The part files from every server folder, in the order they are concatenated.

    Sorted by the path relative to each folder's ``assets/<folder>/``; two
    folders may not claim the same relative name, because then the order (and
    the file) would depend on which folder was scanned first.
    """
    found = {}
    for root in asset_roots(folder):
        for p in root.rglob(f"*{suffix}"):
            rel = p.relative_to(root).as_posix()
            if rel in found:
                raise RuntimeError(f"duplicate asset part {folder}/{rel}: {found[rel]} and {p}")
            found[rel] = p
    return [found[rel] for rel in sorted(found)]


def verify():
    """Fail loudly if the parts no longer assemble into one sound file.

    Really parses the assembled JavaScript, because that is the failure this
    split introduces: a part renamed out of its order now closes a closure
    before it opens, and counting brackets cannot see that (they never balance
    anyway, since strings and regexes are full of them). Node is the parser
    when it is on PATH; without it this check is skipped rather than faked.
    Returns a list of complaints; empty means sound.
    """
    import shutil
    import subprocess
    import tempfile

    node = shutil.which("node")
    if not node:
        return []
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(js())
        path = fh.name
    try:
        # `new Function` parses the whole text as a function body, which is how
        # the browser will read it: top-level `return` is the only difference,
        # and this file has none.
        r = subprocess.run(
            [node, "-e",
             "new Function(require('fs').readFileSync(process.argv[1],'utf8'))",
             path],
            capture_output=True, text=True)
    finally:
        pathlib.Path(path).unlink(missing_ok=True)
    if r.returncode:
        tail = (r.stderr or r.stdout).strip().split("\n")
        why = next((x for x in tail if "Error" in x), tail[-1] if tail else "?")
        return [f"assets/js does not parse once assembled: {why[:160]}"]
    return []
