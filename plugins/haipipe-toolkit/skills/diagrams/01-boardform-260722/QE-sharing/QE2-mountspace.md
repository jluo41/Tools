# Mounting a SPACE

state: 🟡 PARTIAL
owner: CC
method: copy the multi-store registry `console_api.py` already proved out (`_datasets()` / `?dataset=`)
session: 9d892e06-11a4-4808-b251-c36157d20d61
## Opening
How should one service mount a research SPACE, find every board inside it, and give people one place to open them?
A SPACE is the root folder of one research repo, such as `Physician-SPACE`; to mount one is to hand the service that folder to read and write in.
The hard part is that a board's links reach files outside its own folder, so a mount narrow enough to be safe can break them.
This page decides how wide the mount is and how boards are found.

**Why it matters**: Nobody should have to know a board's path before they can find it.
This board sits 78 characters below the repo root, which is not something a person types from memory or pastes into a reply.
So the service has to be the part that knows where boards are, and the person only picks one.

**Why the mount is the hard half**: A board folder is not self-contained.
A question's `## Files` list points at real code elsewhere in the repo, and on 260724 page serving was widened to the whole SPACE root so those links would open.
A mount that carries only the board folder takes that back and answers 404.
The shape this page keeps returning to is a skeleton mount: the board folder writable, the few drill-through subtrees read-only at their true depths, and nothing else present in the filesystem at all.

**How boards are found**: The service walks the mounted SPACE looking for a `board.md`, rather than reading a registry someone has to keep up to date.
A registry drifts the moment a board is added or moved; a walk cannot.
What the walk is allowed to match is still open, because today it only matches a folder named `diagram`, and a paper lifecycle tree is named whatever it is named.

**What a good answer produces**: A reader picks a SPACE, sees every board in it with its progress, and opens one.
The files that board is allowed to reach still open, and nothing else in the repo is visible to the process at all.

**Covered elsewhere**: Whether the board is served locally or from a server, and whether it needs a login: that is `QE1`.
Nor the Board-Webpage-Index **inside** one Board: that is `QB2`.
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

## Aims
### The mount: how many SPACEs, and how narrow
- [x] Decide how many SPACEs one service mounts
      One service mounts N (the `console_api.py` registry pattern, as planned): `INLAB_SPACES` (json) > `INLAB_SPACE_STORE` (parent dir) > `INLAB_SPACE_ROOT` (single) > walking up from the service collecting `*-SPACE` dirs.
      Shipped in `boards_api.py`.
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
- [ ] Actually mount two SPACEs and open a board in each
      The mechanism ran 260724: `Physician-SPACE` (2 boards) + a scratch space mounted together, both listed, both pages served, a comment written into the scratch one.
      But the second space was a throwaway: the honest tick waits for a real second research SPACE (WellDoc-SPACE).

### Board discovery inside a SPACE
- [x] Decide how boards are discovered
      Scan for `<unit>/diagram/<NN>-<topic>/board.md` via `os.walk` with a prune list (`.git`, `node_modules`, `_WorkSpace`, the data stores…) and a depth cap of 9.
      Verified fast on `Physician-SPACE` (finds 2 boards, no cache needed yet).
- [x] SPACE Board Home: discover → see → open (JL 260801)
      The direct Board service now exposes the human-facing route `/boards`, not an internal `/_board/*` route. It scans every non-hidden, non-archived `board.md` below its mounted SPACE, groups cards as Task Board · Paper Board · Skill Board, then shows title · path · spine · settled-page progress and links to that Board's own `board/index.html`. Every Board top bar links back with `🏠 Boards`.
      Task Board is the default. A board under `plugins/*/skills/diagrams/` is a Skill Board (even if its topic says paper); a paper lifecycle tree is a Paper Board. This is a location rule, not a registry.
      `/_board/*` remains reserved for live implementation endpoints such as chat and health; the singular `board/` remains each Board's generated folder, so `/board` would be ambiguous.
- [ ] 🔴 Discovery must find boards that do not live under a `diagram/` folder
      The rule ticked above scans only for a parent folder literally named `diagram`, but the
      skill's own grammar says an existing tree can BE a board and then "the tree is called
      whatever it is called", with the paper lifecycle folder as the named example. So
      `examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026/0-lifecycle/`
      holds 60 pages and a `board.md` and is invisible to `_find_boards()`.
      This is the board JL asked to host on 260727, so the gap is blocking, not theoretical.
      Closes when discovery finds any pruned folder containing `board.md`, and this board appears.

### The Boards page surface
- [ ] Decide what each row of the board list shows
      v1 shipped: title · spine · ✅🟡🔴⏸ counts · question count · open-comment count · path · last modified.
      Whether that is the RIGHT set is JL's read; leave open until it has been used.
- [ ] Decide whether a new board can be opened from the web
      Not built.
      Today `open` remains a skill action from the CLI.

## States
**v1 shipped in `haichat-inlab` (`boards_api.py` + the Boards view), verified end to end on 260724.**

- The short route is BUILT, and option A of the URL-length row is what was built
  JL ruled it in chat on 260802 and the row below is closed with that answer recorded, under the same-day rule that a machine closes a row the person has already answered. `/b/<slug>[/<page-id>]` answers 302 with the real generated file, and the strip's link went from 131 characters to 42.
  `live/home.py` owns it: `board_slug()` strips the `NN-` ordinal and the `-YYMMDD` date, and `resolve_short()` walks the same `_manifests()` discovery the Home page already uses, so there is no second registry. `HomeMixin.short_request()` matches only `/b/<slug>` and `/b/<slug>/<id>`, and `serve_short()` redirects rather than serving the bytes, so the address bar lands on the canonical URL and every relative asset and write-back path inside the page keeps working.
  `status.py` prints the short form whenever the anchor resolves to a generated file, and keeps the long URL when it does not, because the route answers 404 there and a long working link beats a short dead one. It imports `board_slug` rather than copying the rule.
  Driven on a second server on port 5601, leaving the live one untouched: `/b/boardform` → the Index, `/b/boardform/QE2` and `/b/boardform/QD6` → their pages, `/b/boardform/QE` → the group page, and following the redirect ends on a 200. `/b/boardform/NOPE` and `/b/nosuchboard/QE2` both 404 rather than redirecting somewhere plausible. All 10 boards in this SPACE produce distinct slugs, so nothing is ambiguous today. 5 new tests in `tests/test_home.py`; the suite is 87 green.
  LIVE on 5599 since 260802, after JL restarted the server himself. Re-checked against the real host, not the spare port: `/b/boardform/QE2` answers 302 and following it lands on 200, `/b/boardform` answers 302 to the Index, and both `/b/boardform/NOPE` and `/b/nosuchboard/QE2` answer 404.
  A restart is what it costs to pick this up, because `live/term.py`'s `kill_all_terms` is registered `atexit` and `reap_stale_terms` clears whatever survived, so an attached terminal cannot be carried across. Three `claude` sessions were attached when this was built, each resumable by its own session id.

- The long URL still works, and that is a property worth keeping
  Nothing was moved, renamed, or redirected away: a page is still served from its real path, and `/Tools/plugins/…/board/QE/QE2-mountspace.html` was re-checked at 200 on the live server. The short form is a 302 whose destination IS that path, so the long URL is the canonical target rather than a deprecated alias, and every link already written into a page, a commit message or a chat log keeps resolving.
  The one way the short route could take something away is by shadowing: it claims `/b/<one>/<two>`, so a real folder named `b` at the SPACE root would disappear behind it. There is none, checked 260802. A SPACE that grows one would need the route renamed, which is the reason to record this rather than assume it.

- Direct Board service home, shipped 260801
  One mounted SPACE now has a lightweight, read-only `/boards` entry page in `serve.py`: 10 current Board source folders are discovered by `live/home.py`, grouped into Task Boards (the default), Paper Boards (paper lifecycle trees), and Skill Boards (`plugins/*/skills/diagrams/`). Each card opens its own generated Board Index. This is not another Board and writes no registry or `board.md`; it is a fresh discovery view. It does not solve multi-SPACE mounting, which remains this page's open design work.

- What runs now
  `GET /api/board/spaces` (mounted SPACEs + board counts) · `GET /api/board/boards?space=` (rows with progress) · `GET /api/board/q` (one board as JSON, same code path as `build.py --json`) · `GET /_board/page/{space}/{path}` (the real `board.html`, path-vetted) · `POST /_board/comment|discuss|resolve` (the page's own write-backs, relayed to the skill's `serve.py` functions, then rebuild).
  The console SPA gained a **Boards** page, since QE5 ② (260724) a third TOP-LEVEL entry at `/boards`, not a scoped page list view: SPACE picker → board list → the embedded page.
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

### Decision Now
- [x] 🗣 How does a board's URL get short enough to sit in a reply?
      ✅ `A`, ruled by JL 260802 ("go head, I want you to update" and then "It works Good"), built and live on 5599 the same day. Ticked by CC under the 260802 rule that a machine closes a row the human has already answered.
      📍 `Part` the mount layer this page owns; `/Tools/plugins/haipipe-toolkit/skills/diagrams/…` is the long half
      🔔 `Why now` JL 260802, of the strip's link: "I feel the URL here is too long". Today's page URL is 131 characters and 78 of them are the path from the repo root down to the board folder. `QD6`'s Law already hides the address behind the label, but a chat renderer expands `[label](url)` back into `label (url)`, so on that surface the length shows no matter what the strip does. This page's own Opening says people should not need to know a board's full path.
      ⭐ `A ·` a short redirect route, `/b/<board-slug>/<page-id>`, answering 302 with the real file. 42 characters, a 68% cut. `live/home.py` already discovers every board folder and `status.py` already computes a short board name, so this is a lookup against a list that exists rather than a new registry.
      `B ·` a shorter host: the tailnet MagicDNS name in place of the raw IP. 123 characters, a 6% cut. Nearly free, and on its own it fixes nothing.
      `C ·` mount the diagrams tree at a short prefix, `/boards/<board-folder>/board/…`. 92 characters, a 30% cut. No redirect indirection to keep honest, but it needs a mount table maintained and still carries the whole `board/QD/QD6-session-status-strip.html` tail.
      🛑 `Blocks` nothing; the strip works at any length.
      🤖 `If nobody answers` A takes effect, with B applied alongside it when MagicDNS is available, which together give 34 characters.
- [ ] 🗺 Choose the mount shape for the Docker service
      A single board-folder mount reverses the 260724 page-serving widening and 404s a question's `## Files` drill-through links; a SKELETON mount (the board folder `rw`, the drill-through subtrees `ro` at their true relative depths) keeps every allowed `../` link resolving.
      The reconciliation this page records is the skeleton mount; a tick here also closes the 🗺 row in Items to Finish.

## Files
### The short route, shipped 260802
- `live/home.py`
  `board_slug()`, `resolve_short()`, and the `HomeMixin.short_request()` / `serve_short()` pair. The single owner of what a board is called in a URL.
- `cli/serve.py`
  Two lines, in `do_GET` and `do_HEAD`, placed above the static handler so `/b/...` is recognised before anything tries to read it off disk.
- `status.py`
  `board_url()` prints the short form; it imports `board_slug` rather than restating the rule.
- `tests/test_home.py`
  `ShortRouteTest`: the slug rule, index/page/group resolution, the full folder name as an alias, misses that stay misses, and the route matcher's shape.

### The shipped service
- `boards_api.py`
  The shipped layer: `_spaces()` registry, `_find_boards()` discovery, board rows, page serving, write-back relay.
  Lives in the sibling project `haichat-board/` since 260724 (JL: "a separate project"); `haichat-inlab` imports it from there.
  Branch `feat/haichat-board`.
- `web/`
  `src/components/BoardsView.tsx` + the `boards` entries in `src/views.ts` / `src/types.ts` / `src/Console.tsx`.

### Imported from the skill
- `live/home.py` · `cli/serve.py` · `src/page_board.py`
  The direct-service `/boards` route, its read-only discovery/rendering, and the return link present on every generated Board page.
- `cli/build.py`
  `parse_dir()` / `to_json()`: the board list's numbers come from here, no second parser (imported by `boards_api.py`).
- `cli/serve.py`
  The md-writers `boards_api.py` imports (`add_comment` / `add_discuss` / `resolve`), and still the whole live layer on the workstation.

### The pattern it copied
- `console_api.py`
  The registry pattern this copied (`_datasets()` / `_default_dataset()` / `_scope()`).

## Glossary
SPACE: JL's term for the root of one research repo, e.g. `Physician-SPACE`, `WellDoc-SPACE`.
One SPACE holds several boards.

## Log
260802 1410 · Opening rewritten to the `/haipipe-board-page` contract: the four visible sentences now sit above the first blank line (they were below it, so the page rendered as one bare question), the question's own words `SPACE` and `mount` are defined in it with a real example, and the drawer became labelled parts (Why it matters · Why the mount is the hard half · How boards are found · What a good answer produces · Covered elsewhere) instead of a prose wall
260802 · Live on 5599 after JL restarted it, and re-checked against the real host rather than the spare port: short 302 then 200, index 302, both bad-name cases 404. JL asked whether the old URL still works; it does, it was checked at 200, and the answer is now on the page as its own record rather than only in a session
260802 · Built option A the same round, after JL said go ahead: `/b/<slug>[/<page-id>]` as a 302 in `live/home.py`, routed from `cli/serve.py`, printed by `status.py`, 131 characters down to 42. Driven on a spare port so the live server kept its attached terminals; 6 routes checked including both 404 cases, 10 boards with no slug collision, 5 tests added, suite 87 green. The running 5599 still needs a restart to serve it
260802 · JL: "I feel the URL here is too long" of the status strip's link. The strip is `QD6`'s and the path shape is this page's, so the row landed here: 131 characters today, 78 of them the path from the repo root to the board folder, with a short redirect route measured at 42 and recommended
260801 · Added the Space Home taxonomy JL proposed: Task Board by default, then Paper Board, then Skill Board. Classification is inferred from the owning path, with Skill taking precedence over a topic word such as “paper”; `/boards` now shows grouped cards, and focused discovery/rendering tests cover all three kinds.
260801 · JL ruled that the SPACE-level human route is `/boards`; `/_board/*` remains the private live-API namespace, while each Board keeps its own generated `board/` folder. Shipped `live/home.py` discovery + cards and the `🏠 Boards` return link on every generated Board page; local discovery/escaping/navigation tests passed.
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
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
