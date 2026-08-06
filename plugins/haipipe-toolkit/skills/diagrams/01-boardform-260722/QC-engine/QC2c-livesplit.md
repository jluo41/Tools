# serve.py: splitting the live layer
state: 🟡 PARTIAL · split shipped 260731 (gate + mixin move + thin serve.py); QD2 M1 landed in live/chat.py the same day, so what is left is retiring the serve.py shims and promoting navtest.mjs
owner: JL
method: QC2b's Law verbatim, a mechanical move under a response-identical gate; mixins so no signature changes; the areas that stopped moving go first

## Opening
How should the live server be split without creating multiple services or changing any request behavior?

One file was serving chat, terminals, drawings, activity, structure, and writes through the same handler.
The hard part is separating those jobs while they still share one root, one port, and one request context.
That boundary determines whether live features can change independently without breaking the rest of the Board.
It succeeds when focused modules assemble into the same server and a response gate proves the move.


## Diagram
```
   before the split (260731)               shipped 260731
   ─────────────────────────────           ──────────────────────────────────────
   serve.py        2938 lines              serve.py       361  thin CLI + routes
     20 routes + the terminal WS             live/chat.py         the Claude bridge
     one Handler class, 65 methods           live/term.py         PTY + WS terminus
     seven unrelated areas in one file       live/xcal.py         canvas round-trip
                                             live/write.py        sentence anchors
   src/            the RENDER half           live/activity.py     the focus-time DB
     build.py is already a thin CLI          live/structure.py    add Q · group · archive
     over 8 modules (QC2b, shipped 260724)
                                            src/common.py stays the one shared floor
   one process · one port · 5599 only       both halves, no duplication (QC2b Law)
                                            since then: home · shell · turnring joined live/
```

## Content
### 1 · What is actually in there
Counted 260731 by lines of method body: excalidraw 443, chat 414, activity 390, write-back 334, terminal 322, http plumbing 291, then image paste, HOLD and structure edits at 48, over roughly 670 more lines at module level (the four rules texts, `prime_context`, `tool_brief`, `_slugify`, `structure_op`, the PTY helpers).
The inventory and its per-area reading live on `QD2` §5, where it was gathered.
Two things in it were worth saying plainly: Claude Code was about one sixth of the file, and the largest single area was a drawing-canvas round-trip.

### 2 · One process with modules, not several servers
JL's naming ("server_excalidraw, server_xxx, and a server_main") reads two ways, and only one of them works here.
Separate SERVERS on separate ports is ruled out by the constraint `QD3` was built around: only 5599 is forwarded to the laptop, which is the entire reason the terminal is reverse-proxied rather than given its own port.
A second port would not be reachable over the tailnet or through Remote-SSH, and `QE` owns the bind address for the same reason.
The areas also share state that would have to be duplicated or synchronized across processes: one `--root`, one HOLD table (`QD1`'s Law), one rebuild path, and the same board files on disk.
So the split is MODULES, and the word for the result is a package, not a fleet.

### 3 · How you split a request-handler class
The 65 methods were not independent functions; they were methods on one `BaseHTTPRequestHandler` subclass sharing `self.root`, `self.reply()`, `self.target()`, `self.hold()`, and `self.rebuild()`.
That made the mechanism a real choice rather than a formality.

- A · mixins
  `class Handler(ChatMixin, TermMixin, XcalMixin, WriteMixin, ActivityMixin, StructureMixin, BaseHandler)`, one file per mixin, `do_POST` staying as the single routing table.
  Every method keeps its body and its `self` unchanged, so the move is textual and the gate below can actually prove it.
- B · plain modules taking an explicit context object
  Cleaner boundaries and testable without a live server, but every signature changes, so the diff stops being a move and becomes a redesign that no gate can distinguish from a rewrite.

`QC2b`'s Law rules this without needing a new one: refactors move code under a byte-identical gate, and features never ride along in the same step.
That selects A for the move, and leaves B available afterwards as its own gated step if the boundaries turn out to want it.

### 4 · Where they live and what they are called
`src/` is the render half, and its `common.py` is already shared with serve.py, so the serve modules want their own home rather than a second meaning for `src/`.
The board's own word for that half is the live layer (`QC2b`), so `live/` uses vocabulary the board already speaks.
The modules are named for what they SERVE, mirroring `QC2b`'s rule that render modules are named for what they render.
This page argued `live/excalidraw.py` because a top-level `xcal.py` script already exists, but the move shipped `live/xcal.py` anyway and the two have coexisted without confusion.
serve.py then became what build.py became on 260724: a thin CLI plus the routing table.

### 5 · What moves now, and what waits
Three areas had stopped moving and could go first: excalidraw, activity, and the write path, together 1167 lines, all shipped and stable.
Structure edits went with them.

Two areas were still moving, and moving them looked like doing the work twice.
Chat was about to become a session host (`QD2` M1), which rewrites that area, so the honest sequence looked like letting M1 land IN `live/chat.py` as that module's first version rather than moving the current code and then replacing it.
The terminal took the PTY in-house on 260731 (0.64.0) and `QD3m`'s route was still open at the time (since archived), so it was slated to move last.
In the end the `ast` slicer made the move free, chat and terminal moved with the rest, and M1 landed inside `live/chat.py` on 260731; the Aims record the inversion.

## Aims
### The mechanical split
- [x] 🧪 Build the gate before moving anything
      BUILT as `gate_live.py`: it starts a real server against a frozen throwaway copy of this board, runs 18 requests covering every route including the error paths, and hashes all 54 written files afterwards.
      Both responses and file contents pass through one narrow `norm()` so a clock or a uuid cannot fail it and a real change cannot hide in it.
      `QC2b`'s Lesson repeated itself on the first run: the gate caught `@staticmethod` decorators being dropped by the slicer, which would have shipped eight silently broken methods.
- [x] 🧱 Move the areas into `live/`
      Done as ONE mechanical pass rather than four: every method body was sliced by `ast` and copied byte for byte, so the risk that made per-area commits attractive (hand-editing) was never taken.
      `live/`: base 154 · structure 274 · write 259 · xcal 465 · activity 408 · chat 702 · term 563.
- [x] 🚪 serve.py becomes a thin CLI plus the routing table
      2933 lines to 361: the imports, the mixin assembly, `do_GET`, `do_HEAD`, `do_POST`, the daemon, and the console's re-exports.

### Follow-up work
- [x] 🔌 Land `QD2` M1 inside `live/chat.py`
      The reasoning inverted once the move turned out to be free: chat moved with the rest at zero hand-editing cost, so M1 landed in a module that holds only chat instead of inside a 2933-line file.
      That was the point of moving it early rather than an argument against it.
      LANDED 260731 (`QD2` A4.1): a daemon thread owns one asyncio loop plus the per-question client registry, and chat.py has grown 702 to 1332 lines around it.
- [ ] 🧹 Retire the shims once JL has clicked through
      `serve.py` re-exports `structure_op`, `prime_context`, `tool_brief`, `MODELS` and friends so the console keeps importing them from `serve` (QE3's Law).
      They can point at `live.*` directly once the console is confirmed working.

### The standing checklist (JL 260731: "checklist 就是 item to finish — 要时刻保证它们永远是被 check 的")
- [x] 📋 `checks/` built (0.89.0): the executable half of every hard item
      Two tiers. `checks/run.py` = smoke: the LIVE server, seconds, read-only — tree serves, the server's own python imports the SDK (asked through the new `GET /_board/health`, because ps shows the venv symlink RESOLVED and re-running that binary loses the venv: the 3.9 trap), tree `_assets` current, watch.py alive, claude and node present.
      `checks/run.py --full` = real turns on a THROWAWAY fixture board with its own server and Chrome: `pty_e2e.py` ①–⑦ (a real CLI turn through the PTY), one scoped SDK chat turn (CHATOK), and `termnav.mjs` (⌨ follows the tree router, park-not-held, paste — 12 browser checks). The fixture strips every page's `session:` header (a fixture must never `--resume` a real session) and answers the fresh-cwd trust dialog; both were found by the battery's own first runs.
      Board items each check guards: `QD3` ⑤ park/reattach → termnav T9c/T9d + pty ⑥; `QD3` own-PTY → pty ①–⑦; `QD1` one-window → termnav T9b; `QD2` chat answers → the SDK turn + smoke's venv check; paste → termnav T9b′.
- [ ] 📥 Promote SDK-Talk's `navtest.mjs` (💬 follows the router) into `checks/` once its harness settles
      It was mid-iteration when the battery shipped; copying an in-flight file would freeze a flaky version.

## States
The split is shipped: the mixin modules under `live/`, a thin serve.py, and the `checks/` battery standing guard; `QD2` M1 landed inside `live/chat.py` the same day, so only the shim retirement and the navtest.mjs promotion remain.
The question was opened by JL on 260731 ("could we separate them? I don't think it is good to put all the things in one"), and the inventory that motivated it was gathered the same day on `QD2` §5.

- 260731 CC · 📋 The one-off batteries became a standing checklist (`checks/`, 0.89.0)
  JL's ruling made it explicit: a ticked hard item must stay CHECKED, not remembered — today one did not (`follow()` on the tree silently stopped enforcing `QD1`'s one-window law and no tick moved).
  The scattered scratchpad suites (pty_e2e, termnav) are now checked in under `checks/` with a two-tier runner; the full tier runs on a throwaway fixture so a standing check never rewrites a real page's `session:` header or leaves rows in a real registry (gate_live's shape, extended to real turns).
  First runs earned their keep: smoke caught the live server predating the health route, and the fixture caught its own two bugs (a fixture that `--resume`s the real board's sessions; the fresh-cwd trust dialog blocking the TUI).
  Both tiers green as of 260731 1934: smoke 6/6 on the live 5599, full = pty ①–⑦ + CHATOK + termnav 12/12 on the fixture.
- 260731 CC · 🔎 Independent check of the shipped split, one crasher found and fixed
  A second session verified the move: all eight files compile, the Handler MRO assembles the six mixins in order, and the console's re-export surface (`structure_op`, `prime_context`, `MODELS`, the rules texts) still imports from serve.
  The check then caught what the response gate could not: `POST /_board/term` crashed every terminal open, because `USE_TTYD` stayed behind as a serve.py global while `terminal()` moved to `live/term.py`; the gate never spawns claude, so the one uncovered route was the one that broke.
  The fix took two rounds, and the second is the lesson: reading `base.USE_TTYD` still crashed, because `terminal()`'s local `base = f"/_term/{key}"` shadows the module import; the module is now aliased `_base`, and the runtime flag is read through it so `--ttyd` keeps working.
  After the fix the full seven-step terminal e2e passed against the split server (spawn, handshake, boot, a real PTYOK turn, resize, second-client ring replay, clean release).
  A flag set by main() into another module's namespace is exactly the shared-state seam §3 warned about; worth a line in `live/base.py`'s docstring when the page closes.
  The full battery then ran against the split server on the repo venv: terminal e2e three times back-to-back, one scoped SDK chat turn ("BATTERY-OK", $0.009), the session picker on a page and on board.md, the excalidraw scene route, all three assets, and the write path (comment, discuss, image, add_question) on a throwaway fixture board that was deleted after; `resolve` needs the legacy `- [ ] CC「quote」` shape by design, unchanged from before the split.
  The battery also caught an intermittent: a respawn within a second of a release races the dying claude for the same session and exits at once; `kill_term` now registers the pid in `DYING` and the next spawn waits up to 2s for it (`wait_dying`), after which three zero-spacing e2e runs pass in a row.
  One operational rule rediscovered the hard way: serve.py must run on the repo's `.venv` python, or `/_board/chat` answers "no claude_agent_sdk" while everything else works.
- 260731 CC · 🩹 Fresh evidence for the order: the terminal area moved again today
  The black-pane defect (a release-then-respawn race double-closing a recycled fd) was found and fixed in the PTY area hours after 0.64.0 shipped it: cleanup is now single-owner (`pty_pump` alone closes its fd; kill paths only signal) and the fix was verified by re-running the respawn scenario live.
  An area that needed a same-day correctness patch is still forming, which is exactly the §5 test; it confirms terminal-last rather than changing the plan.
- 260731 CC · 🧭 This is QC2b's deferred half, and its Law already governs it
  `QC2b` shipped the render split on 260724 and recorded that it left the live layer alone on purpose, because that layer was still forming.
  So this page inherits rather than invents: the mechanical-move rule, the gate-before-features rule, and the "common.py is the one shared floor, never duplicated" rule all apply verbatim.
  What this page adds is the part `QC2b` could not answer at the time: which areas have since stopped forming, and how a handler class splits when its methods share `self`.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [x] 🧩 Rule modules against servers (JL 260731: "server_excalidraw, server_xxx, and a server_main")
      DECIDED 260731 by JL ("go ahead with the split"): A, one process, one port, modules.
      A · one process, one port, several modules under `live/`, which keeps one HOLD table, one root, and one rebuild path together.
      B · several servers on their own ports, fronted by serve.py, which breaks the single-forwarded-port constraint `QD3` was built around.
      → CC's proposal: A; B breaks the single-forwarded-port constraint `QD3` was built around, and would split one HOLD table, one root, and one rebuild path across processes.
- [x] 🔧 Rule the split mechanism
      DECIDED 260731 by JL with the same go: A, mixins, the textual move the gate can prove.
      A · mixins, a pure textual move the gate can prove, so the refactor moves code and nothing rides along.
      B · plain modules taking an explicit context, which reads cleaner but changes every signature and becomes a redesign.
      → CC's proposal: A now and B never as one step; `QC2b`'s Law says a refactor moves code and features never ride along, and B changes every signature.
- [x] ⏱ Rule the order
      DECIDED 260731 by JL with the same go: A, the settled four now; chat arrives via QD2 M1, terminal last.
      A · move the four settled areas now and let `QD2` M1 land directly in `live/chat.py`, which avoids writing chat twice.
      B · split all seven at once and do M1 afterwards, which means writing the chat half twice.
      C · wait for M1 and `QD3m`, then split everything, which stalls the parts that are already still.
      → CC's proposal: A; it avoids writing chat twice without stalling the parts that are already still.
- [x] 🏷 Rule the naming, in JL's own words against the board's
      DECIDED 260731 by JL: "use live/".
      JL said "server_excalidraw, server_xxx, and a server_main"; §4 argued `live/` instead, and that translation should be ruled, not assumed.
      A · a `live/` package (`live/chat.py`), which mirrors the shape `QC2b` shipped for the render half and keeps the skill root at its current 9 scripts.
      B · flat `server_*.py` files beside serve.py, exactly as JL named them, which costs nothing if the flat names read better.
      → CC's proposal: A; it is the same shape `QC2b` shipped for the render half, and the root stays scannable, but B costs nothing if the flat names read better to JL.

## Files
### Engines
- `../../board/haipipe-board/cli/serve.py`
  The file this page split; 2938 lines then, 496 today: imports, the mixin assembly, and the routing table.
- `../../board/haipipe-board/live/`
  Where the split landed: ten modules today (the moved six plus base, with home, shell, and turnring grown since).
- `../../board/haipipe-board/src/common.py`
  The shared floor both halves import, and the one file this split must not duplicate.
- `../../board/haipipe-board/cli/build.py`
  What a thin CLI looks like after the same treatment, 164 lines over `src/`.

### Related work
- `QC-engine/QC2b-srcsplit.md`
  The render-side split, its Law, and the sentence that deferred this one.

## Log
- 260806 2129 · [REVISE-CC] swept to the 260806 architecture; QD2 M1 ticked as landed in live/chat.py (260731, QD2 A4.1), the drawing module corrected to the shipped live/xcal.py, the States "Nothing is built" opener replaced with the shipped split, and serve.py's Files row brought from 2938 to today's 496 lines
260801 0130 · Reindexed QC8 -> QC2c under the new QC2 code-shape parent (JL 260801)
260731 2358 · The venv rule became code (0.90.0): the checklist's next run caught 5599 on system 3.9 a THIRD time (three restarts, three hands, same trap), so `main()` now re-execs itself onto `<--root>/.venv/bin/python` when the SDK is missing — proven by starting under `/usr/bin/python3` and getting `python 3.13.14 · sdk true` from `/_board/health`; the 1830 "maybe a Decision Now row" is thereby closed as built, per JL's no-decisions rule. Same lap re-ran `checks/run.py --full` against SDK-Talk's assets split + router queue: full tier green, the 0.86 follow() fix intact in `assets/js/10-drawer/40-follow.js`, ledger sequential — the two sessions are aligned, and the checklist is what proved it
260731 1934 · `checks/` shipped (0.89.0) on JL's ruling that the checklist IS the items-to-finish, kept checked: smoke tier (live server, read-only, incl. the new `GET /_board/health` venv probe) + full tier (fixture board, real CLI turn, real SDK turn, 12 browser checks); both tiers green first time after the battery fixed its own two fixture bugs
260731 1830 · 5599 found running on system python 3.9 after a 1751 restart — 💬 SDK chat 400s under 3.9 ("no claude_agent_sdk", needs 3.10+) while ⌨ and the static pages look fine, so the breakage is invisible until someone sends a chat turn; no live PTY children, so killed and relaunched on `.venv/bin/python` (sdk import verified); this is the second time — serve.py's docstring and the venv memory both say it, a re-exec guard in main() may be worth a Decision Now row
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Battery passed end to end on the split (term e2e ×3, chat turn, picker, xcal, writes on a fixture); DYING grace-wait added for rapid respawn; 5599 restarted on the repo venv
260731 · Naming row added (JL's `server_*.py` against `live/`, ruled not assumed) and the same-day PTY race fix recorded as evidence for terminal-last
260731 · Opened from JL's ask ("could we separate them?"), inheriting QC2b's Law; modules-not-servers, mixins, and the settled-areas-first order proposed as three Decision Now rows
