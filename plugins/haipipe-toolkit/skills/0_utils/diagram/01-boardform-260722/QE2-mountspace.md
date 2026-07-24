# Mounting a SPACE

state: 🟡 PARTIAL
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
shipped 260724 (boards_api.py + Boards view)          still missing
──────────────────────────────────────────            ─────────────────────
🏢 SPACE picker  /api/board/spaces                     ＋ open a new board
   Physician-SPACE (2) · Scratch-SPACE (1)               from the web  ❌
     ↓
📋 boards in this SPACE  /api/board/boards?space=      a real 2nd SPACE
   🧭 01-boardform-260722   ✅5 🟡9 🔴8 · 💬0            (WellDoc)  ❌
   🧭 02-method-260722      ✅2 🟡4 🔴5 ⏸2 · 💬12
     ↓ click
📖 the real board.html   /_board/page/{space}/{path}
   comments/discuss/resolve write back to the md
   (chat/terminal → 501, workstation-only, QE3 Law)

how boards are discovered: scan the space root for <unit>/diagram/*/board.md
(os.walk + prune list + depth cap — no cache needed yet)
```

## Items to Finish
- [x] Decide how many SPACEs one service mounts
      One service mounts N (the `console_api.py` registry pattern, as planned): `INLAB_SPACES` (json) > `INLAB_SPACE_STORE` (parent dir) > `INLAB_SPACE_ROOT` (single) > walking up from the service collecting `*-SPACE` dirs. Shipped in `boards_api.py`.
- [x] Decide how boards are discovered
      Scan for `<unit>/diagram/<NN>-<topic>/board.md` via `os.walk` with a prune list (`.git`, `node_modules`, `_WorkSpace`, the data stores…) and a depth cap of 9. Verified fast on `Physician-SPACE` (finds 2 boards, no cache needed yet).
- [ ] Decide what each row of the board list shows
      v1 shipped: title · spine · ✅🟡🔴⏸ counts · question count · open-comment count · path · last modified. Whether that is the RIGHT set is JL's read — leave open until it has been used.
- [ ] Decide whether a new board can be opened from the web
      Not built. Today `open` remains a skill action from the CLI.
- [ ] Actually mount two SPACEs and open a board in each
      The mechanism ran 260724: `Physician-SPACE` (2 boards) + a scratch space mounted together, both listed, both pages served, a comment written into the scratch one. But the second space was a throwaway — the honest tick waits for a real second research SPACE (WellDoc-SPACE).

## Where we are
**v1 shipped in `haichat-inlab` (`boards_api.py` + the Boards view), verified end to end on 260724.**

- What runs now
  `GET /api/board/spaces` (mounted SPACEs + board counts) · `GET /api/board/boards?space=` (rows with progress) · `GET /api/board/q` (one board as JSON, same code path as `build.py --json`) · `GET /_board/page/{space}/{path}` (the real `board.html`, path-vetted) · `POST /_board/comment|discuss|resolve` (the page's own write-backs, relayed to the skill's `serve.py` functions, then rebuild). The console SPA gained a **Boards** page — since QE5 ② (260724) a third TOP-LEVEL entry at `/boards`, not a scoped rail view: SPACE picker → board list → the embedded page.
- What the verification showed
  Two spaces mounted; `Physician-SPACE` discovers this board and `subjective-label/diagram/02-method-260722`; a comment posted through the console landed in the scratch board's md as `- [ ] JL “…” · 260724 1315` and the html rebuilt; resolve flipped it to `[x]`; a write aimed outside a board folder was rejected; `/_board/chat` answers 501 (chat/terminal stay on the workstation, `QE3`'s Law).
- Still missing
  Create-a-board-from-the-web; the board-list row design has not been judged by a reader; a real second SPACE.
- The registry was copied as planned
  `_spaces()` in `boards_api.py` is `console_api.py`'s `_datasets()` with `dataset` renamed to `space` — nothing invented.

## Files
- `boards_api.py`
  The shipped layer: `_spaces()` registry, `_find_boards()` discovery, board rows, page serving, write-back relay. Lives in the sibling project `haichat-board/` since 260724 (JL: "a separate project"); `haichat-inlab` imports it from there. Branch `feat/haichat-board`.
- `web/`
  `src/components/BoardsView.tsx` + the `boards` entries in `src/views.ts` / `src/types.ts` / `src/Console.tsx`.
- `build.py`
  `parse_dir()` / `to_json()` — the board list's numbers come from here, no second parser (imported by `boards_api.py`).
- `serve.py`
  The md-writers `boards_api.py` imports (`add_comment` / `add_discuss` / `resolve`), and still the whole live layer on the workstation.
- `console_api.py`
  The registry pattern this copied (`_datasets()` / `_default_dataset()` / `_scope()`).

## Glossary
SPACE: JL's term for the root of one research repo, e.g. `Physician-SPACE`, `WellDoc-SPACE`. One SPACE holds several boards.

## Log
260724 1440 · Page serving widened to ANY existing file under the space root, read-only (JL: "how could I open cms_production.do?") — `## Files` links now open through the console; source-ish suffixes (.do/.R/.sql/…) display as text instead of downloading (both here and serve.py); the third discovered board (Project-Personality-OpioidRx/01-cmsdata) verified the click end to end. `boards_api.py` rehomed to the sibling `haichat-board/` service (8094), inlab imports it — see QE3
260724 1324 · v1 shipped and verified (JL's "go ahead… as we discussed"): `boards_api.py` + Boards view in `haichat-inlab` (branch `feat/haichat-board`, commit 27e3ed6) — SPACE registry, discovery, board list, embedded page, comment/discuss/resolve write-backs relayed to the skill's own writers. 🔴 → 🟡; still open: create-from-web, row-design judgment, a real second SPACE
260724 1242 · Opened: JL asked for "haichat-board mounts a SPACE, and inside it you create a new board or open an existing one". Split out as the layer above a board; where the code runs belongs to QE3
