# Where the board runs

state: 🔴 OPEN
owner: JL
method: decide whether the static half survives first — that one answer determines everything else

## Question
The board runs inside `serve.py` today — a 976-line Python `SimpleHTTPRequestHandler` bound to `127.0.0.1`, single user. JL wants to make it a real thing and asked whether to move to a mature stack such as Node. The decision that actually matters is not the language: it is **which process the board moves into, and whether `build.py` producing a static page stays an invariant**.

- Why it is hard
  The board has two halves with opposite requirements. The **static half** (`build.py` → `board.html`) is valuable precisely because it has zero dependencies: hand an RA one file, project it in a meeting, read it offline. The **live half** (comment write-back, chat, terminal) must run on the machine the files are on. Moving into a service makes it very easy to kill the static half by accident.
- What breaks if we leave it
  Both `QE2` (the SPACE layer) and `QE4` (in-page editing) need to know which codebase they are written in before anyone can start. Until this is decided, those two can only be speculated about.
- What it affects downstream
  Which of the two repos the code lives in, whether to branch, the fate of `build.py`'s ~490-line parser, and whether the board can be embedded in a HAI-Chat thread.

## Boundary
- ✅ This question owns
  **Which process and which repo the board's code runs in**: stay in `serve.py`, or move into `haichat-inlab` as a fifth router; whether the front end should reuse the `haichat-inlab/web/` React SPA; whether `build.py` producing a static page remains an invariant.
- ❌ This question does not own
  Who may access it and whether it needs a login — that is `QE1`. Nor how a SPACE is mounted and what the board list looks like — that is `QE2`. Nor whether the body text is editable in the page — that is `QE4`.

## Diagram
```
two candidates; the difference is what comes free and what it costs
─────────────────────────────────────────────────────────────────
① stay in serve.py (Tools repo)
   Python SimpleHTTPRequestHandler · 976 lines · bound to 127.0.0.1 only
   ✅ the static half survives by default   ✅ smallest change; SPACE layer could ship tomorrow
   ❌ no auth, no multi-user, no deploy     ❌ cannot embed in HAI-Chat

② move into haichat-inlab as a fifth router (HAIChat-SPACE repo)
   main.py mounts four today: console_api · haichat_api · labeling_api · tasks_api
   every one has the same shape: an env var injects a repo path -> render what is
   already on disk, read-only -> one narrow write-back path.
   The board has exactly that shape.
   ✅ per-thread iframe embed comes free    ✅ docker-compose deploy comes free
   ✅ web/ is already React + TS + Vite     ✅ _datasets() multi-store registry (QE2 needs it)
   ❌ must wire auth / multi-user (couples to QE1)   ❌ touches both repos

Should the front end use Node: yes, but **the one that already exists** —
haichat-inlab/web/ is already React + TypeScript + Vite.
Do not rewrite the back end: build.py's parse_* is not rendering code, it is
    **the board's grammar**. Rewriting it in Node means two parsers to keep in
    sync forever, and the Python one cannot be deleted (SKILL.md's hard
    invariant: strip every <script> from the page and every question and all
    body text is still there).
```

## Items to Finish
- [ ] Decide: does `build.py` producing a static page stay an invariant?
      **Keep it** → `build.py` stays alive, gains a `--json` output, two render paths (JSON for the API, HTML for the static page).
      **Drop it** → a full Node rewrite becomes coherent, but the board can no longer be handed over as one file or projected offline.
      Decide this one first; everything else follows from it.
- [ ] Decide: stay in `serve.py` or move into `haichat-inlab`?
      A two-step path is also available: build `QE2`'s SPACE layer on `serve.py` first (usable immediately), then move.
- [ ] Decide whether to branch, and in which repo
      `Tools` (`jluo41/Tools`) and `HAIChat-SPACE` (`JHU-CDHAI/HAIChat-SPACE`) are two independent repos, both mounted as submodules of `Physician-SPACE`. `haichat-inlab` is a **plain directory** inside `HAIChat-SPACE`, not a submodule.
- [ ] Ship `build.py --json`
      `parse_dir()` / `parse_file()` / `parse_q()` are already the clean parsing half and `render()` the rendering half. Adding an output does not require a refactor.
- [ ] Verify once: for the same board, the API's JSON and the static HTML agree
      Two render paths must not tell different stories.

## Where we are
**Not decided. What follows is verified fact, not conclusion.**

**🐍 This half today (`serve.py`, Tools repo)**

- What already works
  Comment write-back (`/_board/comment`) · discussion (`/_board/discuss`) · resolving (`/_board/resolve`) · chat (`/_board/chat`, Claude Agent SDK with per-call Allow/Deny) · a real terminal (`/_board/term`, ttyd behind a reverse proxy) · a per-file `HOLD` lock. Every write calls `build.py` to rebuild immediately.
- The hard limit
  Bound to `127.0.0.1` only, no auth, single user. That is not an oversight — it can write files and spawn terminals, so binding it outward hands both of those to the network (`QE1` spells this out).

**⚛️ The other half (`haichat-inlab`, HAIChat-SPACE repo)**

- Its shape is identical to the board's
  `main.py` mounts four routers, each one "an env var injects a repo path → render what is already on disk, read-only → one narrow write-back path": `tasks_api.py` takes `INLAB_PROJECTS_ROOT` and scans the task-folders of `Project-*`; `labeling_api.py` takes `INLAB_LABEL_STORE`, and its "only write" is the researcher's own decision appended to `human_decisions.jsonl`. The board wants precisely this shape.
- Four things that come free
  HAI-Chat renders any URL as a per-thread iframe (the board embeds into a conversation naturally) · `docker-compose.yml` already has a `haichat-inlab` service · `web/` is React + TypeScript + Vite already · `console_api.py`'s `_datasets()` is the multi-SPACE registry `QE2` needs.

**🔍 What the "mature options" actually are, honestly**

- Static site generators (Astro / Docusaurus / VitePress)
  Read-only, render at build time, and **give you no write-back**. Write-back is the hard part of a board.
- Git-backed CMS (TinaCMS / Decap)
  The closest match — markdown as source of truth plus a React editor. But their model is "make a commit", and a board wants write-to-disk-now plus an immediate rebuild (which is how it works today, and why "there is no such thing as an unsynced comment").
- Conclusion
  Nothing off the shelf replaces `serve.py` outright. There is exactly one mature component worth bringing in, and it belongs to `QE4`: Yjs, for when two people edit the same question at once.

## Files
- `serve.py`
  Candidate ① itself. 976 lines; routing in `do_GET` / `do_POST`, write paths in `add_comment` / `add_discuss` / `resolve`, live layer in `chat` / `terminal`.
- `build.py`
  Parsing half `parse_dir` / `parse_file` / `parse_q` / `split_sections` / `parse_comments`; rendering half `render`. `--json` goes between the two.
- `SKILL.md`
  Holds the hard invariant (strip every `<script>` and the body is still there), which `build.py` asserts on every build. Dropping the static half means editing this first.
- `main.py`
  Candidate ②'s mount point, currently holding four routers.
- `console_api.py`
  The multi-store registry template (`_datasets()` / `_scope()`) — the thing `QE2` would copy.

## Glossary
router: a FastAPI `APIRouter`, a group of endpoints under a shared prefix. `haichat-inlab/main.py` uses `include_router()` to compose four into one service; the board would be the fifth.
per-thread iframe: HAI-Chat embedding any URL as a page alongside one conversation thread. `haichat-inlab`'s README describes itself exactly this way.

## Discussion
> JL: I might want to use the mature way, like using the nodejs, etc. How do you think?
>> CC0724: Node belongs on the front end, and it is **already there** — `haichat-inlab/web/` is React + TypeScript + Vite; the board should be a view inside it rather than a new app. Do not rewrite `build.py` in Node: those ~490 lines are the board's grammar, so rewriting means two parsers to keep in sync forever, and the Python one cannot be deleted while the static-page invariant stands. So the real decision is "does the static half survive", not "Node or not".
> JL: so you mean here we are going to the haichat-inlab, right? do we want to have a new branch for this purpose?
>> CC0724: Only partly. Of the five steps, the first two (`build.py --json`, the SPACE index on `serve.py`) stay in `Tools`; the last three (`boards_api.py`, the `web/` view, in-page editing) go to `HAIChat-SPACE`. On branching: yes for `HAIChat-SPACE` (`feat/haichat-board` — a multi-day feature in a repo whose `haichat-inlab` service others run), no for `Tools` (both changes are small and additive, and branching there only adds submodule-ref churn in `Physician-SPACE`).

## Log
260724 1242 · Opened: JL asked "should we use a mature stack like nodejs / should we branch". Split "where it runs + does the static invariant survive" into its own question; the SPACE layer is QE2 and in-page editing is QE4
