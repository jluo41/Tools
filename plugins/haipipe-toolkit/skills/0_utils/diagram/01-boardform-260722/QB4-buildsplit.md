# Managing build.py's size

state: 🔴 OPEN
owner: JL
method: split the embedded CSS/JS out into asset files the build INLINES; the grammar stays in the skill

## Question
`build.py` is ~2,500 lines because it is three things in one file: the parser (the board's grammar), the HTML/CSS template, and the page's JavaScript (comments, chat drawer, terminal). JL 260724: "build.py is so long, could we better manage it? and should it be in the haichat-board project?"

- Why it is hard
  The length is real, but the cure must not break two Laws: the static invariant (one command, one self-contained board.html, no build toolchain) and one-grammar (`QE3`: every consumer imports the skill's parser, nobody rewrites it).
- What breaks if we leave it
  Editing 800 lines of JS inside a Python string means no syntax highlighting, no linting, and node --check only AFTER a build — the QD3 smoothness work paid that tax already.
- What it affects downstream
  Where the skill's files live, how consumers import them, and whether an offline `python3 build.py <dir>` keeps working in any SPACE with zero extra steps.

## Boundary
- ✅ This question owns
  **How build.py's code is organized and where it lives**: split or not, into what, and skill vs. haichat-board.
- ❌ This question does not own
  What the page looks like (`QA4`), what the grammar is (`QA2`/`ref/board-form.md`), or where the SPACE layer runs (`QE3` — settled).

## Diagram
```
today                                proposed split (inside the skill dir)
────────────────────────             ─────────────────────────────────────
build.py  ~2,500 lines               build.py     parser + assembly  (~1,100)
  parser        ~500                 assets/board.css   the page CSS
  CSS template  ~700                 assets/board.js    comments + drawer + terminal
  page JS       ~800                 → build.py READS and INLINES them at build
  index/render  ~500                 → output stays ONE self-contained board.html
                                     → node --check / a linter can run on board.js directly

should it move to haichat-board?  NO —
  the grammar must live where every SPACE carries it: Tools (a submodule of
  every SPACE). haichat-board is ONE consumer importing it (QE3 Law). Move it
  there and offline builds + serve.py + other SPACEs all lose their parser.
```

## Items to Finish
- [ ] JL confirms the home
      Recommendation: **build.py stays in the skill** — `QE3`'s one-grammar Law already decided this; `haichat-board/` imports it and always will.
- [ ] Split the assets out
      `assets/board.css` + `assets/board.js`, read and inlined by build.py; the emitted page stays self-contained; the strip-scripts assertion keeps running.
- [ ] Tooling on the split-out JS
      `node --check` (and optionally a linter) runs on `assets/board.js` in place, not on an extracted temp file after a build.
- [ ] A no-diff proof
      Build this board before and after the split; the two board.html files must be byte-identical (or differ only in whitespace) — the split is management, not behavior.
- [ ] Wait for a quiet window
      Two sessions are editing this skill concurrently today (19c1f361 swept one set of changes; QA4 changed mid-turn again). A file split under live concurrent edits is merge hell — schedule it, do it in one pass.

## Where we are
**Asked and answered in design; execution deliberately deferred to a quiet window.**

- The length, measured
  ~2,500 lines: parser ~500, CSS ~700, page JS ~800, index/render ~500. The JS is the part that hurts (edited blind inside a Python string).
- Why not haichat-board
  The skill travels with every SPACE via the Tools submodule; the static invariant needs `python3 build.py <dir>` to work offline in any of them. `haichat-board/` is a consumer (it imports `parse_dir`/`to_json` and serve.py's writers) — moving the grammar there would invert `QE3`'s settled Law.
- Why not now
  Concurrent sessions are live in these exact files today. The split touches every line (moving blocks); doing it while another agent edits build.py guarantees a collision.

## Files
- `build.py`
  The file being split; the parse half must keep its import surface (`parse_dir`, `to_json`, `sec`, `parse_comments`, `stinfo`) — `boards_api.py` imports exactly these.
- `assets/` (to be created)
  `board.css` + `board.js`, inlined at build time; never served separately.
- `SKILL.md` · `CHANGELOG.md`
  The shape section gains one line about assets/; version bumps on execution.

## Discussion
> JL: build.py is so long, could we better manage it? and should it in the haipipe-board project?
>> CC0724: split yes — CSS and JS out into `assets/` files that build.py inlines, output unchanged and still self-contained. Move no — the grammar must live where every SPACE carries it (the skill, via Tools); `haichat-board/` is one consumer importing it, per QE3's one-grammar Law. Deferred to a quiet window: another session is editing these files live today, and a whole-file split under concurrent edits is merge hell.

## Log
260724 1455 · Opened on JL's question; recommendation written (split into skill-local assets/, keep the home in the skill), execution parked until the concurrent-session churn quiets
