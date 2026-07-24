# Mounting a SPACE

state: 🔴 OPEN
owner: CC
method: copy the multi-store registry `console_api.py` already proved out (`_datasets()` / `?dataset=`)

## Question
A SPACE is a repo root — `Physician-SPACE`, `WellDoc-SPACE`. What JL wants: mount a SPACE onto the service, then see "which boards live in this SPACE", walk into one, and open a new one. Today `serve.py --root <repo root>` already IS "one SPACE mounted", but the layer above it is missing — no page tells you which boards exist, so you have to **already know the URL** to open anything.

- Why it is hard
  Not technically hard — the unclear part is **how many at once**. `serve.py` takes a single `--root`. Mounting `Physician-SPACE` and `WellDoc-SPACE` together means choosing between running two processes, raising `--root` to their shared parent, or introducing a SPACE registry.
- What breaks if we leave it
  Boards can only ever be opened by someone passing you a URL. Half of QE1's "the second person cannot open it" is rooted here — not that they cannot open it, but that they do not know what is there to open.
- What it affects downstream
  What the board list page looks like (the same visual problem as QC2's index design, one level up), whether a new board can be created from the web, and what the URLs look like.

## Boundary
- ✅ This question owns
  **The layer above a board**: how a SPACE is mounted, how many at once, how the boards in a SPACE are discovered, what the board list page shows, whether a new board can be created from the page.
- ❌ This question does not own
  Whether the board is served locally or from a server, and whether it needs a login — that is `QE1`. Nor the index page **inside** one board — that is `QC2`. Nor which process the code runs in — that is `QE3`.

## Diagram
```
today                                  wanted
──────────────────────────────         ──────────────────────────────
serve.py --root <one repo root>        🏢 SPACE picker
  ↓                                       Physician-SPACE / WellDoc-SPACE
(this layer does not exist)  ❌            ↓
  ↓                                    📋 boards in this SPACE   ← the new layer
you must know the full URL                01-boardform-260722  15/19 ✅
  /Tools/plugins/…/01-…/board.html         02-method-260722      3/8
                                           ＋ open a new board
                                             ↓
                                       📖 board.html (already exists)

how boards are discovered: scan --root for **/diagram/*/board.md
```

## Items to Finish
- [ ] Decide how many SPACEs one service mounts
      One SPACE per process (run N of them), or one service mounting N (needs a registry plus `?space=`).
- [ ] Decide how boards are discovered
      The convention today is `<owning unit>/diagram/<NN>-<topic>-<YYMMDD>/board.md` (settled in `QC1`).
      Is scanning `**/diagram/*/board.md` enough? Does it stay fast on a large repo? Does it need a cache?
- [ ] Decide what each row of the board list shows
      Board name · spine · progress (how many ✅ out of how many) · open comment count · last modified. Enough? Too much?
- [ ] Decide whether a new board can be opened from the web
      Today `open` is a skill action (CC runs it from the command line). Doing it from a page needs an HTTP endpoint that creates the folder, writes `board.md`, and copies `ref/q-template.md`.
- [ ] Actually mount two SPACEs and open a board in each
      That is the acceptance test: not "the design supports it", but really seeing boards from two SPACEs on one page and clicking into both.

## Where we are
**The "mount one SPACE" half already runs. The "see which boards exist" half does not exist at all.**

- What already works
  `serve.py --root <repo root> --port 5599` serves the **whole repo root**, not one board — so a single process already covers every board in that SPACE, and comment write-back, chat, and terminal all work for each of them.
- What is entirely missing
  No SPACE list page, no board list page, no create-from-web. Opening any board means typing the URL or having CC push it to you.
- The multi-store registry that can be copied outright (the cheapest part)
  `_datasets()` in `console_api.py` already solved exactly this problem: three-level fallback — `INLAB_DATASETS` (json `{name: dir}`) > `INLAB_DATASET_STORE` (a parent dir whose children are auto-discovered) > `INLAB_PATIENT_STORE` (single, for backward compatibility) — plus a `?dataset=` query parameter and `_scope()` to switch. Rename `dataset` to `space` and that is this question's answer.

## Files
- `serve.py`
  What `--root` means, the routing (`do_GET` / `do_POST`), and `target()` which decides what file a request lands on. The SPACE layer goes here, or into the new router `QE3` describes.
- `build.py`
  `parse_dir()` already reads a whole board and returns data — the "how many ✅ out of how many" for the board list comes straight from it, no second parser needed.
- `console_api.py`
  The working template for multi-store registration (`_datasets()` / `_default_dataset()` / `_scope()`). Read it first when starting this.

## Glossary
SPACE: JL's term for the root of one research repo, e.g. `Physician-SPACE`, `WellDoc-SPACE`. One SPACE holds several boards.

## Log
260724 1242 · Opened: JL asked for "haichat-board mounts a SPACE, and inside it you create a new board or open an existing one". Split out as the layer above a board; where the code runs belongs to QE3
