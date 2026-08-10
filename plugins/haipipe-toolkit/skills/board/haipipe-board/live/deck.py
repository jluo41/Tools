"""🎞 Deck · write ONE board page out as a real html-ppt deck.

THE DIVISION OF LABOUR, which is the whole design.

  the reflow (70-plugin-slides.js)   decides WHAT A SLIDE IS
  this file                          decides WHAT A DECK IS

The browser already knows how to cut a board page into slides: it reads the
rendered DOM, so it sees the `div.cmp` and `div.folds` wrappers, the collapsed
`details`, and the controls the board's own scripts inject at runtime. Redoing
that here, from markdown or from the HTML on disk, would be a THIRD definition of
"what a slide is" and the three would drift. So the browser posts the slides it
already built, and this file does no parsing at all: it is a template.

WHY html-ppt OWNS THE SHELL. `assets/base.css`, `assets/themes/*.css` and
`assets/runtime.js` are a finished deck runtime: 36 themes, the T key to cycle
them, F for fullscreen, O for overview, and S for presenter mode with the
speaker cards. Reimplementing any of that in the board would be the second worst
thing here; vendoring a copy of it would be the worst, because then it stops
following the skill when the skill improves. Nothing is copied. The deck links
straight at the skill's own files by relative path, which resolves both over the
server and from a file:// open.

WHAT THIS PRODUCES IS A FILE, and that is the point of it existing at all. The
in-browser view is a projection that vanishes on Escape. This writes
`<board>/slides/<page>-deck.html`, which survives, opens on its own, and can be
sent to somebody who has never heard of the board.

WHAT IT IS NOT. It is still not an AUTHORED deck. The words are the page's own
words, so a Content division arrives as its paragraph, not as three bullets.
`page-type: slide` and its QBt9 specimen remain the authored path, where a person
writes the talk and accepts each render. This one claims nothing, so it needs no
acceptance.
"""
import os
from pathlib import Path

# The skill, by path. It lives in the display plugin because that plugin owns
# presentation; the board is only a caller and must not grow a copy.
HTML_PPT = ("Tools/plugins/haipipe-toolkit/skills/display/skills/html-ppt")

# The T key cycles this list. Kept short and legible on purpose: a board page is
# dense text, and half the gallery (cyberpunk-neon, vaporwave, y2k-chrome) makes
# dense text unreadable, so offering them here would be offering a worse deck.
THEMES = ("academic-paper", "minimal-white", "editorial-serif", "swiss-grid",
          "arctic-cool", "nord", "tokyo-night", "catppuccin-mocha")
DEFAULT_THEME = "academic-paper"

# The bridge. A slide body is the BOARD's own nodes, so it arrives wearing board
# class names that mean nothing inside a deck: `pre.asc` is a record block, `.ph`
# and `.pj` are a subdivision's heading and its parenthetical. Rather than restyle
# them, they are mapped onto html-ppt's own tokens, so a theme change moves them
# too. This is the only CSS the board contributes to the deck, and it is written
# here rather than in board.css because it applies nowhere else.
BRIDGE = """
/* THE RATIO, not the sizes. html-ppt's `.h2` is sized for a five-word slide
   title; a board division title sits above real prose, so at .58em the body read
   as a footnote under a billboard (measured 1 : 6 on QBt1). Both move toward each
   other rather than the body alone, or the title simply loses the page. */
.slide .h2 { font-size: clamp(20px, 2.1vw, 34px); line-height: 1.18;
             margin-bottom: .55em; }
.slide .kicker { font-size: .8em; }
.slide .sd-body { font-size: .80em; line-height: 1.62; }
.slide pre, .slide pre.asc {
  background: var(--surface, rgba(127,127,127,.08));
  border: 1px solid var(--line, rgba(127,127,127,.22));
  border-radius: 10px; padding: 14px 16px;
  font-size: .82em; line-height: 1.45; overflow-x: auto; white-space: pre;
}
.slide .ph { font-weight: 700; margin: 14px 0 2px; }
.slide .pj { opacity: .68; font-style: italic; margin: 0 0 8px; }
.slide .blt { margin: 0 0 6px; }
.slide .bt { font-weight: 600; }
.slide .bd { opacity: .78; }
.slide code { background: var(--surface, rgba(127,127,127,.10));
  padding: 1px 5px; border-radius: 4px; font-size: .92em; }
.slide details { margin: 0 0 8px; }
.slide summary { font-weight: 600; cursor: default; list-style: none; }
.slide summary::-webkit-details-marker { display: none; }
.slide .sd-was-link { color: var(--accent, currentColor); }
/* A board division can outrun any slide. html-ppt centres a slide and lets it
   overflow; a deck that CLIPPED page text would say something the page does not,
   which is the one thing a derived view may never do. */
.slide { overflow-y: auto; }

/* TOP, NOT MIDDLE. html-ppt centres a slide vertically, which is right for a
   five-word title and wrong for a paragraph: a short body floated in the middle
   of the screen with a third empty above and below it, and the eye had to hunt
   for where the text began. Board slides start at a fixed top edge, so every
   slide's first line is in the same place. */
.deck .slide { justify-content: flex-start; align-content: flex-start; }
.deck .slide > .kicker:first-child { margin-top: 4vh; }

/* THE ONE SLIDE A SPLIT CANNOT RESCUE. A section whose single largest child is
   already over the limit stays whole (see the reflow), so it is set smaller
   instead. Measured on QBt1: 128% of the box before, inside it after. This is
   the only place the deck trades type size for fit, and it does so on the
   slides that would otherwise lose their last lines off the bottom. */
.slide.dense { padding-top: 2vh; padding-bottom: 2vh; }
.slide.dense .sd-body { font-size: .56em; line-height: 1.45; }
.slide.dense pre, .slide.dense pre.asc { font-size: .62em; line-height: 1.3;
  padding: 8px 10px; margin: 6px 0; }
.slide.dense .h2 { font-size: clamp(16px, 1.5vw, 24px); margin-bottom: .3em; }
.slide.dense .kicker { font-size: .7em; margin-bottom: 2px; }
.slide.dense .deck-footer { font-size: .8em; }
"""

SHELL = """<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{a}/fonts.css">
<link rel="stylesheet" href="{a}/base.css">
<link rel="stylesheet" id="theme-link" href="{a}/themes/{theme}.css">
<link rel="stylesheet" href="{a}/animations/animations.css">
<style>{bridge}</style>
</head>
<body data-themes="{themes}" data-theme-base="{a}/themes/">
<div class="deck">
{slides}
</div>
<script src="{a}/runtime.js"></script>
</body>
</html>
"""

# THE NUMBER IS THE RUNTIME'S, on every slide, and the span is always empty.
# Two wrong guesses got here. First the literal went on every slide and the cover
# read "1 / 27 / 27"; then it went on all but the cover and slide 5 of QBt1 read
# "55 / 22 / 22". Both were the same mistake: html-ppt updates the ACTIVE slide's
# `.slide-number`, not the page's first, so any literal is a second writer on the
# same span. The element still has to BE there for the runtime to fill.
SLIDE = """  <section class="slide{dense}" data-title="{dt}">
{kicker}    <h2 class="h2">{title}</h2>
    <div class="sd-body">{body}</div>
    <div class="deck-footer"><span class="dim2">{foot}</span>\
<span class="slide-number" data-current="{i}" data-total="{n}"></span></div>
  </section>
"""


def _attr(s):
    return (str(s or "").replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def _text(s):
    return (str(s or "").replace("&", "&amp;")
            .replace("<", "&lt;").replace(">", "&gt;"))


class DeckMixin:

    def deck(self, f, p):
        """POST /_board/deck {path, file, slides:[{kicker,title,body}], theme}

        -> {ok, url, path, n}. The slides arrive as HTML because they ARE HTML:
        they are the page's own rendered nodes, which the browser cloned. Nothing
        is escaped on the way through for that reason, and the door is the same
        `target()` every other write uses, so a payload cannot name a file
        outside --root or a board that has no board.md.
        """
        board = p.get("_board")
        if board is None:
            got = self.target(p)
            if got[0] is None:
                return None, got[1]
            f, board = got

        slides = p.get("slides") or []
        if not isinstance(slides, list) or not slides:
            return None, "没有 slide 可写：the reflow returned nothing."

        theme = (p.get("theme") or DEFAULT_THEME).strip()
        if theme not in THEMES:
            theme = DEFAULT_THEME

        out_dir = Path(board) / "slides"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / (Path(f).stem + "-deck.html")

        # Relative, not absolute. The same href has to resolve over the server
        # AND when the file is opened straight off disk, which an absolute path
        # rooted at --root would not do.
        assets = os.path.relpath(
            (Path(self.root).resolve() / HTML_PPT / "assets"), out_dir.resolve())

        title = (p.get("title") or Path(f).stem).strip()
        foot = (p.get("foot") or Path(f).name).strip()
        n = len(slides)
        body = []
        for i, s in enumerate(slides, 1):
            k = (s.get("kicker") or "").strip()
            body.append(SLIDE.format(
                dense=(" dense" if s.get("dense") else ""),
                dt=_attr(s.get("title")),
                kicker=('    <p class="kicker">%s</p>\n' % _text(k)) if k else "",
                title=_text(s.get("title")),
                body=s.get("body") or "",
                foot=_text(foot), i=i, n=n))

        out.write_text(SHELL.format(
            theme=theme, themes=",".join(THEMES), a=assets.replace(os.sep, "/"),
            title=_text(title), bridge=BRIDGE, slides="".join(body)),
            encoding="utf-8")

        try:
            url = "/" + out.resolve().relative_to(Path(self.root).resolve()).as_posix()
        except ValueError:
            return None, "写出去的 deck 落在 --root 之外"
        return {"ok": True, "url": url, "path": str(out), "n": n,
                "theme": theme}, None
