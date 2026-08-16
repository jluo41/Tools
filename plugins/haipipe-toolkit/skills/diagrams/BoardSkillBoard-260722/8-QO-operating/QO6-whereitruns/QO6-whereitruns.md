# Where the board runs

state: ✅ SETTLED
owner: JL
method: decide whether the static half survives first: that one answer determines everything else

## Opening
Which process should own the board's static pages and live actions without creating a second implementation of its Markdown grammar?

The board needs a portable HTML artifact and a service that can mount SPACEs, write comments, and embed the result in the console.
Moving everything into a new stack could ease deployment while quietly breaking offline reading or duplicating the parser.
That choice determines where the code lives and which later sharing features can be built safely.
The design works when both surfaces use one grammar and each degrades honestly when the live half is unavailable.

**Covered elsewhere**: Who may access it and whether it needs a login: that is `QE1`. Nor how a SPACE is mounted and what the board list looks like: that is `QE2`. Nor whether the body text is editable in the page: that is `QE4`. Nor which address the listener actually binds to: that is `QE6`.


## Diagram

```
two candidates; the difference is what comes free and what it costs
─────────────────────────────────────────────────────────────────
① stay in serve.py (Tools repo)
   Python SimpleHTTPRequestHandler · cli/serve.py, 496 lines today
   binds 127.0.0.1 by default; --host can widen it (that address is QE6)
   ✅ the static half survives by default   ✅ smallest change; SPACE layer could ship tomorrow
   ❌ no auth, no multi-user, no deploy     ❌ cannot embed in HAI-Chat

② move into haichat-inlab as one more router (HAIChat-SPACE repo)
   main.py mounts two today: console_api · haichat_api
   (four when this was drawn; labeling_api.py and tasks_api.py are no longer
    in the repo, checked 260806)
   both have the same shape: an env var injects a repo path -> render what is
   already on disk, read-only -> one narrow write-back path.
   The board has exactly that shape.
   ✅ per-thread iframe embed comes free    ✅ docker-compose deploy comes free
   ✅ web/ is already React + TS + Vite
   ❌ no _datasets() registry on disk, so QE2 has to write one, not copy one
   ❌ must wire auth / multi-user (couples to QE1)   ❌ touches both repos

Should the front end use Node: yes, but **the one that already exists** —
haichat-inlab/web/ is already React + TypeScript + Vite.
Do not rewrite the back end: build.py's parse_* is not rendering code, it is
    **the board's grammar**. Rewriting it in Node means two parsers to keep in
    sync forever, and the Python one cannot be deleted (SKILL.md's hard
    invariant: strip every <script> from the page and every question and all
    body text is still there).
```


## Aims
### The rulings JL approved on 260724
- [x] Decide: does `build.py` producing a static page stay an invariant?
      **Kept** (JL 260724, approving the discussed plan: "as we discussed, don't stop to ask me").
      `build.py` stays alive and gained `--json`: two render paths, one grammar.
      The give-a-colleague-one-file and offline-projection properties survive.
- [x] Decide: stay in `serve.py` or move into `haichat-inlab`?
      **Both, split by layer** (the discussed hybrid, approved 260724): the grammar (`build.py`) and the md-writers (`serve.py`) stay in the skill; `haichat-inlab` gained `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/boards_api.py`, a fifth router that IMPORTS them: SPACE mounting, board discovery, page serving, comment/discuss/resolve write-backs.
      Chat/terminal (`QD2`/`QD3`) stay on the workstation's `serve.py`; the console answers them 501.
- [x] Decide whether to branch, and in which repo
      **`feat/haichat-board` in `HAIChat-SPACE`** (created, first commit 27e3ed6); **no branch in `Tools`**: its two changes (`--json`, English chrome) are small and additive, and a Tools branch only adds submodule-ref churn in `Physician-SPACE`.
      As of 260806 that branch is not in `HAIChat-SPACE` any more: it holds `main`, `align-mm-server-to-agent`, and `inlab-databricks-ui`, and `27e3ed6` is not a valid object there. The ruling stands; the code it named no longer exists.

### build.py --json, shipped and cross-checked
- [x] Ship `build.py --json`
      Shipped (skill v0.7.0): meta + per-question `{state, owner, done/total, comments_open/total, sections}` from the same parse the HTML uses.
- [x] Verify once: for the same board, the API's JSON and the static HTML agree
      Verified 260724 on this board: 22 question ids match the HTML sections exactly; comment counts match (`QB1 0 open / 7`); the console's `/api/board/q` returns byte-identical JSON because it calls the same `to_json`.

## States
Settled 260724: JL approved the discussed plan ("you just go ahead… as we discussed"), and v1 was built, verified, and committed on `feat/haichat-board`.

Checked against disk 260806: the skill half is alive and has grown; the SPACE half is not on disk anywhere. There is no `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/boards_api.py` in `HAIChat-SPACE`, no sibling `haichat-board/` project, nothing on port 8094, and no `feat/haichat-board` branch. The layer split ruled in `## Law` still stands as the plan; only the skill half of it has shipped.

The static half survived in a new shape. A Board folder now builds the `board/` tree (an index, one file per group, one file per page), and `build.py` deletes a leftover single-file `board.html` after generating it (JL 260731, recorded on `QC4`). The scripts-off assertion still runs on every build, now against the largest generated page instead of the monolith.

**🐍 This half today (`serve.py`, Tools repo)**

- What already works
  Comment write-back (`/_board/comment`) · discussion (`/_board/discuss`) · resolving (`/_board/resolve`) · chat (`/_board/chat`, Claude Agent SDK with per-call Allow/Deny) · a real terminal (`/_board/term`, ttyd behind a reverse proxy) · a per-file `HOLD` lock.
  Every write calls `build.py` to rebuild immediately.
- The hard limit
  No auth of any kind, single user.
  It binds `127.0.0.1` by default, and `--host` can widen that to a tailnet address or to `0.0.0.0`.
  That is not an oversight: it can write files and spawn terminals, so binding it outward hands both of those to the network (`QE1` spells this out; `QE6` picks the address).

**⚛️ The other half (`haichat-inlab`, HAIChat-SPACE repo)**

- Its shape is identical to the board's
  `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/main.py` mounts two routers on 260806, `console_api` and `haichat_api`, each one "an env var injects a repo path → render what is already on disk, read-only → one narrow write-back path": `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/console_api.py` takes `INLAB_PATIENT_STORE`, `INLAB_ENDPOINT_STORE`, and `INLAB_REGISTRY`, and serves the records and packaged endpoints it finds under them.
  The two other routers this page cited in 260724, `tasks_api.py` and `labeling_api.py`, are no longer in the repo, so the count is two, not four; the shape argument is unchanged.
  The board wants precisely this shape.
- Three things that come free, and one that no longer does
  HAI-Chat renders any URL as a per-thread iframe (the board embeds into a conversation naturally) · `docker-compose.yml` already has a `haichat-inlab` service · `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/web/` is React + TypeScript + Vite already.
  The fourth is gone: `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/console_api.py` has no `_datasets()` on 260806, so the multi-SPACE registry `QE2` needs has to be written rather than copied.

**🔍 What the "mature options" actually are, honestly**

- Static site generators (Astro / Docusaurus / VitePress)
  Read-only, render at build time, and **give you no write-back**.
  Write-back is the hard part of a board.
- Git-backed CMS (TinaCMS / Decap)
  The closest match: markdown as source of truth plus a React editor.
  But their model is "make a commit", and a board wants write-to-disk-now plus an immediate rebuild (which is how it works today, and why "there is no such thing as an unsynced comment").
- Conclusion
  Nothing off the shelf replaces `serve.py` outright.
  There is exactly one mature component worth bringing in, and it belongs to `QE4`: Yjs, for when two people edit the same question at once.

## Files
### The skill half (Tools repo)
All of these sit under `Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/` (`haipipe-board` 0.124.0).
- `cli/serve.py`
  Candidate ① itself.
  496 lines; routing in `do_GET` / `do_POST`, and the handler mixes in the `live/` package: the write paths `add_comment` / `add_discuss` / `resolve` are in `live/write.py`, the live layer is `live/chat.py` and `live/term.py`, and the `HOLD` lock is in `live/base.py`.
- `cli/build.py`
  A 164-line entry now.
  The parse half is `src/parse.py` (`split_sections` / `parse_q` / `parse_file` / `parse_dir`); the render half and `to_json` are `src/page_board.py`; `--json` goes between the two.
  `parse_comments` no longer exists.
- `SKILL.md`
  Holds the hard invariant, worded there as "delete every `<script>` in the page and every question and all of the prose is still there", which `cli/build.py` asserts on every build.
  Dropping the static half means editing this first.

### The haichat-inlab half (HAIChat-SPACE repo)
- `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/main.py`
  Candidate ②'s mount point, holding two routers on 260806.
- `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/console_api.py`
  The env-var-injects-a-path shape the board wants, read from `INLAB_PATIENT_STORE` / `INLAB_ENDPOINT_STORE` / `INLAB_REGISTRY`.
  The `_datasets()` / `_scope()` registry `QE2` planned to copy is not in this file, so there is nothing to copy yet.

## Law
- The static half is an invariant
  `build.py` → a self-contained `board.html` stays, whatever else is built on top.
  Give a colleague one file; project offline.
  The no-JS assertion keeps running on every build.
- One grammar, never two parsers
  `build.py`'s parse half is the board's grammar; every consumer (serve.py, boards_api.py, anything later) IMPORTS it or calls `--json`.
  Rewriting it in another language is forbidden while the invariant above stands.
- One writer, never two
  The md-editing functions (`add_comment` / `add_discuss` / `resolve`) live in the skill's `serve.py`; `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/boards_api.py` imports them.
  A second implementation of "how a comment is written into md" must not exist.
- The layer split
  Skill (Tools repo) = grammar + static build + workstation live layer (chat/terminal).
  The SPACE layer (mounting + discovery + serving + relayed write-backs) = `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/boards_api.py`.
  Anything mounting it degrades honestly (501/502) where the workstation half is required.
- The SPACE layer's home is the sibling project `haichat-board/` (JL 260724)
  Its own service (port 8094, zero-build server-rendered index, own Dockerfile + compose entry); `haichat-inlab` imports the SAME router from that directory for its `/boards` page: one implementation, two fronts.
  Same repo, same branch, so "merge back later" is an ordinary `git merge`, not a transplant.

## Glossary
router: a FastAPI `APIRouter`, a group of endpoints under a shared prefix.
`haichat-inlab/main.py` uses `include_router()` to compose its routers into one service, two of them on 260806; the board's `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/boards_api.py` would be one more and has not been written yet. per-thread iframe: HAI-Chat embedding any URL as a page alongside one conversation thread.
`haichat-inlab`'s README describes itself exactly this way.

## Discussion
> JL: I might want to use the mature way, like using the nodejs, etc. How do you think?
>> CC0724: Node belongs on the front end, and it is **already there**: `haichat-inlab/web/` is React + TypeScript + Vite; the board should be a view inside it rather than a new app. Do not rewrite `build.py` in Node: those ~490 lines are the board's grammar, so rewriting means two parsers to keep in sync forever, and the Python one cannot be deleted while the static-page invariant stands. So the real decision is "does the static half survive", not "Node or not".
> JL: so you mean here we are going to the haichat-inlab, right? do we want to have a new branch for this purpose?
>> CC0724: Only partly. Of the five steps, the first two (`build.py --json`, the SPACE index on `serve.py`) stay in `Tools`; the last three (`../../../../../../platforms/HAIChat-SPACE/haichat-inlab/boards_api.py`, the `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/web/` view, in-page editing) go to `HAIChat-SPACE`. On branching: yes for `HAIChat-SPACE` (`feat/haichat-board`, a multi-day feature in a repo whose `haichat-inlab` service others run), no for `Tools` (both changes are small and additive, and branching there only adds submodule-ref churn in `Physician-SPACE`).

## Log
- 260806 2203 · [REVISE-CC] swept to the 260806 architecture; the SPACE half is presented as planned, not shipped: no `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/boards_api.py`, no sibling `haichat-board/`, nothing on 8094, and `feat/haichat-board` is gone from `HAIChat-SPACE`. Skill-half facts re-measured on disk: `cli/serve.py` 496 lines with the writers and live layer in `live/`, `cli/build.py` a 164-line entry over `src/parse.py` + `src/page_board.py`, `parse_comments` retired, the `board/` tree replacing the single-file `board.html`, and `haichat-inlab/main.py` mounting two routers with no `_datasets()`.
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260724 1440 · JL: a separate project for haichat-board, merged back later → `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/boards_api.py` moved to the sibling `haichat-board/` (standalone on 8094: server-rendered index, Dockerfile, compose entry); inlab imports the same router from there. Law amended; still ✅, the decision deepened, nothing reversed
260724 1324 · SETTLED. JL approved the discussed plan ("go ahead… as we discussed, don't stop to ask me"): static invariant KEPT (`build.py --json` shipped, skill v0.7.0); hybrid layer split (grammar+writers in the skill, SPACE/discovery/serving in `haichat-inlab`'s new `../../../../../../platforms/HAIChat-SPACE/haichat-inlab/boards_api.py`, chat/terminal workstation-only via 501); branch `feat/haichat-board` created in HAIChat-SPACE (commit 27e3ed6), no branch in Tools. JSON≡HTML verified on this board (22 ids, comment counts). `## Law` written
260724 1242 · Opened: JL asked "should we use a mature stack like nodejs / should we branch". Split "where it runs + does the static invariant survive" into its own question; the SPACE layer is QE2 and in-page editing is QE4
