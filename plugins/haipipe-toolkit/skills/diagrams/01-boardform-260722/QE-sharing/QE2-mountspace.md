# Mounting a SPACE

state: 🟡 PARTIAL
owner: CC
method: copy the multi-store registry `console_api.py` already proved out (`_datasets()` / `?dataset=`)

## Question
A SPACE is a repo root (`Physician-SPACE`, `WellDoc-SPACE`).
What JL wants is to mount a SPACE onto the service, then see "which boards live in this SPACE", walk into one, and open a new one.
Today `serve.py --root <repo root>` already IS "one SPACE mounted", but the layer above it is missing: no page tells you which boards exist, so you have to already know the URL to open anything.

It is not technically hard; the unclear part is how many at once.
`serve.py` takes a single `--root`, so mounting `Physician-SPACE` and `WellDoc-SPACE` together means choosing between running two processes, raising `--root` to their shared parent, or introducing a SPACE registry.
Leave it and boards can only ever be opened by someone passing you a URL, which is where half of QE1's "the second person cannot open it" really lives: not that they cannot open it, but that they do not know what is there to open.
Downstream it decides what the board list page looks like (the same visual problem as QC2's index design, one level up), whether a new board can be created from the web, and what the URLs look like.

## Boundary
- ✅ Covered here
  **The layer above a board**: how a SPACE is mounted, how many at once, how the boards in a SPACE are discovered, what the board list page shows, whether a new board can be created from the page.
- ↪ Covered elsewhere
  Whether the board is served locally or from a server, and whether it needs a login: that is `QE1`.
  Nor the Board-Webpage-Index **inside** one Board: that is `QA2b`.
  Nor which process the code runs in: that is `QE3`.

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

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QE2

## Items to Finish
- [x] Decide how many SPACEs one service mounts
      One service mounts N (the `console_api.py` registry pattern, as planned): `INLAB_SPACES` (json) > `INLAB_SPACE_STORE` (parent dir) > `INLAB_SPACE_ROOT` (single) > walking up from the service collecting `*-SPACE` dirs.
      Shipped in `boards_api.py`.
- [x] Decide how boards are discovered
      Scan for `<unit>/diagram/<NN>-<topic>/board.md` via `os.walk` with a prune list (`.git`, `node_modules`, `_WorkSpace`, the data stores…) and a depth cap of 9.
      Verified fast on `Physician-SPACE` (finds 2 boards, no cache needed yet).
- [ ] 🔴 Discovery must find boards that do not live under a `diagram/` folder
      The rule ticked above scans only for a parent folder literally named `diagram`, but the
      skill's own grammar says an existing tree can BE a board and then "the tree is called
      whatever it is called", with the paper lifecycle folder as the named example. So
      `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/`
      holds 60 pages and a `board.md` and is invisible to `_find_boards()`.
      This is the board JL asked to host on 260727, so the gap is blocking, not theoretical.
      Closes when discovery finds any pruned folder containing `board.md`, and this board appears.
- [ ] 🗺 Decide whether a mount can be NARROWER than a SPACE root
      JL 260727: run the service in Docker with only the board folder mounted, so that what can be
      read and written is enforced by the kernel rather than by path vetting.
      The complication is the 260724 ruling in the Log below: page serving was deliberately widened
      to the whole space root so a question's `## Files` links could open. A single-folder mount
      reverses that and 404s them.
      The reconciliation is a SKELETON mount: several volumes at their true relative depths, the
      board folder `rw` and the drill-through subtrees `ro`, so every `../` link that was allowed
      still resolves and everything else is absent from the filesystem.
      Closes when a mount shape is chosen and a board is served from it with its links working.
- [ ] Decide what each row of the board list shows
      v1 shipped: title · spine · ✅🟡🔴⏸ counts · question count · open-comment count · path · last modified.
      Whether that is the RIGHT set is JL's read; leave open until it has been used.
- [ ] Decide whether a new board can be opened from the web
      Not built.
      Today `open` remains a skill action from the CLI.
- [ ] Actually mount two SPACEs and open a board in each
      The mechanism ran 260724: `Physician-SPACE` (2 boards) + a scratch space mounted together, both listed, both pages served, a comment written into the scratch one.
      But the second space was a throwaway: the honest tick waits for a real second research SPACE (WellDoc-SPACE).

## Where we are
**v1 shipped in `haichat-inlab` (`boards_api.py` + the Boards view), verified end to end on 260724.**

- What runs now
  `GET /api/board/spaces` (mounted SPACEs + board counts) · `GET /api/board/boards?space=` (rows with progress) · `GET /api/board/q` (one board as JSON, same code path as `build.py --json`) · `GET /_board/page/{space}/{path}` (the real `board.html`, path-vetted) · `POST /_board/comment|discuss|resolve` (the page's own write-backs, relayed to the skill's `serve.py` functions, then rebuild).
  The console SPA gained a **Boards** page, since QE5 ② (260724) a third TOP-LEVEL entry at `/boards`, not a scoped rail view: SPACE picker → board list → the embedded page.
- What the verification showed
  Two spaces mounted; `Physician-SPACE` discovers this board and `subjective-label/diagram/02-method-260722`; a comment posted through the console landed in the scratch board's md as `- [ ] JL “…” · 260724 1315` and the html rebuilt; resolve flipped it to `[x]`; a write aimed outside a board folder was rejected; `/_board/chat` answers 501 (chat/terminal stay on the workstation, `QE3`'s Law).
- Still missing
  Create-a-board-from-the-web; the board-list row design has not been judged by a reader; a real second SPACE.
- The registry was copied as planned
  `_spaces()` in `boards_api.py` is `console_api.py`'s `_datasets()` with `dataset` renamed to `space`, nothing invented.
- What the mount already gives, read on 260727 while answering `QE1`
  The service is already containerized and already mounts rather than bakes: `haichat-board/Dockerfile`
  is `python:3.11-slim` with `fastapi` + `uvicorn` and copies only the two `.py` files, and
  `HAIChat-SPACE/docker-compose.yml` carries a `haichat-board` service on 8094 whose single volume is
  `${BOARD_SPACE_HOST:-./haichat-board/space}:/space` with `INLAB_SPACE_ROOT=/space`.
  Two properties matter for a narrow mount. `BOARD_SKILL_DIR` overrides skill discovery, so
  `build.py` and `serve.py` can be mounted from somewhere other than inside the space, which is what
  makes it possible not to mount the repo at all. And `serve.py`'s module-level imports are stdlib
  plus its own `src.common`, with `claude_agent_sdk` imported lazily inside the chat turn, so the
  slim image can import the md-writers without the SDK installed.
- Writes are already confined to a board folder in code
  `_target()` accepts a write only when the resolved path stays under the space root, sits in a
  directory that actually contains `board.md`, and has a filename matching the skill's `QNAME`.
  So "only things inside that board folder change" is already true; a narrow mount makes the same
  guarantee a second time at the kernel, which is the reason to want it rather than a reason to
  trust the code less.

## Files
- `boards_api.py`
  The shipped layer: `_spaces()` registry, `_find_boards()` discovery, board rows, page serving, write-back relay.
  Lives in the sibling project `haichat-board/` since 260724 (JL: "a separate project"); `haichat-inlab` imports it from there.
  Branch `feat/haichat-board`.
- `web/`
  `src/components/BoardsView.tsx` + the `boards` entries in `src/views.ts` / `src/types.ts` / `src/Console.tsx`.
- `build.py`
  `parse_dir()` / `to_json()`: the board list's numbers come from here, no second parser (imported by `boards_api.py`).
- `serve.py`
  The md-writers `boards_api.py` imports (`add_comment` / `add_discuss` / `resolve`), and still the whole live layer on the workstation.
- `console_api.py`
  The registry pattern this copied (`_datasets()` / `_default_dataset()` / `_scope()`).

## Glossary
SPACE: JL's term for the root of one research repo, e.g. `Physician-SPACE`, `WellDoc-SPACE`.
One SPACE holds several boards.

## Log
260727 · JL proposed running the service in Docker with only the board folder mounted, so writes are
       kernel-confined. Read the shipped container and found the mount side already built (compose
       service on 8094, `BOARD_SPACE_HOST:/space`, `BOARD_SKILL_DIR` escape hatch, slim image can
       import the md-writers because the SDK import is lazy) and writes already vetted by `_target()`.
       Two items added: discovery misses any board outside a `diagram/` folder, which hides the paper
       lifecycle board JL wants to host; and the narrow mount needs to be a skeleton so the 260724
       `## Files` widening below is not reversed.
260724 1440 · Page serving widened to ANY existing file under the space root, read-only (JL: "how could I open cms_production.do?"): `## Files` links now open through the console; source-ish suffixes (.do/.R/.sql/…) display as text instead of downloading (both here and serve.py); the third discovered board (Project-Personality-OpioidRx/01-cmsdata) verified the click end to end. `boards_api.py` rehomed to the sibling `haichat-board/` service (8094), inlab imports it; see QE3
260724 1324 · v1 shipped and verified (JL's "go ahead… as we discussed"): `boards_api.py` + Boards view in `haichat-inlab` (branch `feat/haichat-board`, commit 27e3ed6): SPACE registry, discovery, board list, embedded page, comment/discuss/resolve write-backs relayed to the skill's own writers. 🔴 → 🟡; still open: create-from-web, row-design judgment, a real second SPACE
260724 1242 · Opened: JL asked for "haichat-board mounts a SPACE, and inside it you create a new board or open an existing one". Split out as the layer above a board; where the code runs belongs to QE3
