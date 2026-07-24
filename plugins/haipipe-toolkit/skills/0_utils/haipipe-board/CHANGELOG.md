haipipe-board — Changelog
=========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.

**v0-series rule (JL, 2026-07-23):** this skill stays on `0.x.x` — **it never goes to 1.0.0 without JL's explicit say-so.** Everything here is provisional: the board form, the Q template, the generator's output. Ship `0.MINOR.PATCH` freely; `1.0.0` is a decision, not a milestone that arrives on its own.


## [0.9.2] — 2026-07-24

**The terminal self-heals, and its columns stop lying.** JL's screenshot (QD3's Lesson) showed reconnect banners knocking six times on a terminal that had been RELEASED — reconnecting cannot revive a dead ttyd — over a TUI mangled by drifting column math.

- after 2 failed reconnects the drawer now respawns the terminal through `/_board/term` (`--resume` restores the session) instead of knocking to 6 and giving up.
- `fitTerm` reads xterm's real rendered cell size (fallback to the old constants) and refits 350ms after connect — the pty and the pane agree on width, claude repaints clean.

## [0.9.1] — 2026-07-24

**No button closes the chatbot anymore.** JL clicked the drawer's "↻ Reload to see the result" and lost the drawer — that button predated live refresh and did a hard `location.reload()`, which tears down everything the scripts built. All four reload sites (the drawer's post-write button, the drawer's ↻, the dock panel's ↻, the discussion-add success) now call `window.__boardRefresh` — the QD6 in-place swap, run immediately — so content updates under you and the drawer stays open mid-conversation. Labels renamed to "↻ Refresh in place" / "↻ Refresh". First edit made directly in `assets/board.js` since the QB4 split — checked with `node --check` on the real file.

## [0.9.0] — 2026-07-24

**Live refresh, an honest wait line, and the QB4 split.** Three JL asks in one afternoon of drawer-testing.

- **live in-place refresh (QD6).** "When the chat changed something, refresh automatically — and my chat interface is still there." The page HEAD-polls its own URL every 4s (both servers send Last-Modified; the console's page route gained HEAD) and, on change, swaps ONLY `div.wrap`: content updates under you, scroll restored, "↻ board updated" toast, held while text is selected. The chat drawer (mid-stream included), terminal, and comment dock hang off `<body>` and never notice. No Node, no reload, drawer survives — that requirement decided the design.
- **the wait line tells the truth (QD2).** serve.py emits `stage` events ("booting claude — the full tier loads the whole skill registry…", "session up — sending your message") so the drawer shows real progress instead of a static "…thinking"; the collapsed thinking block is labeled `💭 Thinking (N chars — click to reopen)`. Verified along the way: resumed sessions DO stream thinking now (the explicit `thinking={enabled}` option cured yesterday's loose end ②).
- **build.py split into assets (QB4).** 2,488 → 850 lines: the page's JS and CSS now live as REAL files — `assets/board.js` (1,173 lines, `node --check`s in place) and `assets/board.css` (465 lines) — read and inlined at build, output still ONE self-contained board.html. Byte-identical proven on a frozen board (split vs. mechanically re-joined build), a proof that caught two wrapper-newline slips before they shipped. The grammar's home stays the skill; `haichat-board/` keeps importing it.

## [0.8.0] — 2026-07-24

**The gate shows the change (duplicating the VS Code extension, step 1).** JL: "what is the backend of the vscode claude plugin? I want to duplicate it." The backend is the `claude` binary over the stream-JSON agent protocol — exactly what the drawer already drives through `claude_agent_sdk`; the visible delta was the gate.

- serve.py's permission ask events now carry `detail`: Edit → old/new strings; Write → the file's current content vs. the proposed; MultiEdit → per-edit pairs (capped at 6); Bash → the command. Truncated (4k/edit) — a gate preview, not a diff viewer.
- the drawer renders it: − red blocks, + green blocks, commands verbatim, above Allow once / Always / Deny. Strip-scripts invariant unaffected (the gate only exists in the live layer).
- honest status: emitted JS node-checked; a live gate-pop E2E is still owed (full-tier boots load the ~150-skill registry and outran the test window).
- next duplication step (QD2 ④): one persistent claude process per session, like the extension — also the cure for those slow boots.

## [0.7.1] — 2026-07-24

**`## Files` links actually open.** JL clicked `cms_production.do` on the CMS board and nothing usable happened — the link machinery (`resolve()`'s walk-up + `## Links`) was fine; the serving side wasn't.

- `EXT` widened: `.do .R .sql .tex .bib .toml .csv .tsv .ps1 .log` now count as path-like, so backticked references to them resolve (existence-checked, as always).
- `serve.py` serves source-ish suffixes as `text/plain` — they display in the browser instead of downloading (default mimetypes made `.do` an octet-stream).
- The first consumer moved: `boards_api.py` now lives in HAIChat-SPACE's **`haichat-board/`** sibling project (own service on 8094; `haichat-inlab` imports the same router). Its page serving widened to any existing file under the space root, read-only, matching serve.py — that is what makes a `## Files` click work in the console.

## [0.7.0] — 2026-07-24

**English output + the parser as a service.** JL: "put all the things in English, no Chinese anymore — in the board html or markdown."

- **the emitted page is fully English.** All user-visible chrome strings in `build.py` translated (index labels, tooltips, comment badges, the CLI summary line); `<html lang="en">`; comment quotes render as `“…”`. New `scrub_cjk_comments()` drops CJK-bearing CSS/JS comments from the **emitted** page only — the source keeps its comments for developers; the build asserts the page still reads with scripts stripped, as before.
- **comment grammar widened to curly quotes.** `CM_HEAD` (build.py) and `resolve` (serve.py) accept `“…”` alongside `「…」`/`"…"`, and `serve.py`'s writer now writes `“…”`. Found the hard way: an English board written with curly quotes parsed to zero comments — they silently vanished from the page (~19k chars of body reappeared after the fix).
- **`build.py <dir> --json`** — the parser half exposed as a service (the boardform board's QE3: one grammar, two render paths). Emits meta + per-question `{state, owner, done/total, comments_open/total, sections}` from the same code the HTML is built from, so JSON and HTML cannot disagree (asserted in the consumer's tests).
- **first external consumer: `haichat-inlab`'s `boards_api.py`** (HAIChat-SPACE, branch `feat/haichat-board`) imports `build.py`/`serve.py` from this skill dir — SPACE mounting, board discovery, page serving, and the comment/discuss/resolve write-backs, none of it re-implemented. Design record: the boardform board's QE2/QE3.
- **terminal smoothness (QD3 ①–④):** the drawer terminal now auto-reconnects with backoff (the xterm survives, scrollback intact; the post-auth resize makes claude repaint), sends a same-size resize op every 30s as keepalive, refits via ResizeObserver when the pane resizes, and pre-warms the xterm assets on ⌨ hover (assets only — never `POST /_board/term`, which takes HOLD).
- the skill's own board (`diagram/01-boardform-260722/`, 23 questions) fully translated to English — body, JL quotes, comments, logs.

## [0.6.0] — 2026-07-23

**The question page was reordered so a stranger can read it.** JL: "currently it is very very hard for a fresh eye to understand." The diagnosis was ordering, not wording — the page gave you *what we did* before *what we're deciding and why*.

- **on-stage order is now fixed: intent first, state second.** `Question → Boundary → Diagram → Items to Finish → Where we are → Files`. Previously `Now` sat above `Done when`, so a reader hit a wall of implementation detail before learning the goal, and `Why here` — the single most orienting paragraph — was buried fifth.
- **`## Question` became a lede plus bullets.** It renders through `body()` now: the first paragraph is the 21px lede, and 2–4 bullets carry *why it's hard / what breaks if we don't decide / what it affects downstream*. The acceptance bar is stated in QA4's `## Law`: **read this one section and a zero-context reader knows what the question is.**
- **new `## Boundary` section** (`.bnd`, grey rule) — what the question covers and, more importantly, what it does **not**, naming the question that owns the excluded part. Without it readers bring another question's expectations to this one. Optional but strongly recommended.
- **new `## Files` section** (`.fls`, blue rule, last on stage) — which files this question touches, and what each one's role is. Read the question, then know where to go; change a file, then know which question to write back to. Paths in backticks become clickable through `board.md`'s `## Links`. Optional but strongly recommended.
- **`## Done when` → `## Items to Finish`, `## Now` → `## Where we are`.** Plainer names for a fresh reader.
- **`## Why here` retired** — its job moved into `## Question`'s bullets. Boards that still carry the section parse fine; it renders in the bottom folds, so no content is lost.
- **no board breaks.** `ALIAS` now maps one slot to many names, so `Done when`/`Items to Finish`, `Now`/`Where we are` and the old Chinese names all resolve. Every existing question file rebuilt untouched.
- **QA2 and QA4 reopened (`✅ → 🟡`).** The layout and the template were both settled under the old structure — this change invalidates them. QA4 carries the new `## Law` and a `## Lesson` worth keeping: *it was closed ✅ that same morning and reopened by one sentence from JL, because the finish line never included "a stranger can read it."* Every one of the board's questions was then converted to the new shape — Question as lede-plus-bullets, plus `## Boundary` and `## Files`, with `## Why here` folded in and removed (18/18, verified against the *rendered* page rather than the markdown, because a substring check gets fooled by headings that appear inside ascii fences — QA2 lost a whole section to exactly that). Still owed: the fresh-agent cold read.

## [0.5.0] — 2026-07-23

- 新增 **view** 动作：「打开 <板文件夹>」= 看已有的板，不是开新板。
  之前只有 open（开新板），第 5 步还只写「打开 board.html 给用户看」而没给命令，
  新 agent 会去跑 `open board.html` —— 那是在**服务器**桌面上开，用户（Remote-SSH，
  浏览器在自己笔记本上）什么都看不到。现在写明唯一有效的方式：
  通过 VS Code IPC socket + `browser.sh` 把 `http://127.0.0.1:5599/<板>/board.html` 推过去。
- frontmatter 的 description 补上「打开这块板」触发词，并写明 view ≠ open、禁用 `open`/`file://`。
- open 第 6 步改成「按 view 那节推到用户的 VS Code 浏览器」。
- 清掉写死的「14 题」（板的题数会变，写死必过期）。

## [0.4.3] — 2026-07-23

A compose box in every question's Discussion — write a thought in bulk, it lands in `## Discussion`.

- **`## Discussion` gets a textarea.** Inside each question's Discussion fold there is now a box + signer dropdown + "➕ Add to discussion". Type a thought — a whole block, *not* pinned to a sentence the way a comment is — pick a signer, press Add: serve.py appends it as `> WHO: …` to that question's `## Discussion` and rebuilds; a reload shows it. Reuses the existing write path (new `/_board/discuss`, sibling of `/_board/comment`) and is fence-aware like the comment fix, so it never lands in a `## Discussion` line shown inside a code example. With serve.py not running the button says to hand-write it instead. The box is inert static HTML without the script, so the invariant (strip every `<script>`, the prose survives) still holds. Decided the simple way (JL): into `## Discussion`, not a new section — reuses the free-form thread that already exists.

## [0.4.2] — 2026-07-23

A third level of hierarchy inside a section — the **group topic** — plus the comment-writer bug that surfaced it.

- **a whole-line-bold `**…**` becomes a group topic.** A line that is entirely bold is no longer just a bold paragraph; it renders as a 🔹-marked, slightly-larger heading that leads a cluster of items — sitting between the section heading (`.ch`, underlined, 📍/🎯/💡) and the item names (`.bt`, `▸`). Three visible levels now: 📍 section ＞ 🔹 group ＞ ▸ item. The 🔹 is the default marker; write an emoji at the start of the bold line (`**🎨 …**`) and it becomes the marker instead — the icon is *authored*, never guessed by the generator (build.py has no LLM, and guessing an emoji from keywords is exactly the kind of machine-guess the writing rules forbid). Mixed-bold lines (`**a** b`) are untouched — only fully-bold lines convert. Documented across `ref/q-template.md` (the `## Now` example), `ref/board-form.md` §5 (syntax table) and §8 (on-stage hierarchy). QA4 asked for it — recorded through the board's own comment layer.
- **the Question block shows its name.** Every other section renders a label (📍 Now, 🎯 Done when, 💡 Why here); the question line carried only a bare `❓`. It now has a small `❓ Question` eyebrow (`.ql`, accent, above the question text), matching the rest. QA4's remaining open comment asked for exactly this — resolved and re-anchored on close (the `❓` moved into the label, so the quote moved to the question text).
- **serve.py no longer writes comments into fenced examples.** `add_comment` matched the *first* `## Comments` heading in the file — including the one inside QA4's `md 段落→页面位置` code fence — so a comment on that slide landed in the example, not the real section. It now skips ``` fences when locating `## Comments` / `## Log`. The stray comment was moved back to QA4's real `## Comments`. (A running serve.py must be restarted to pick this up.)

## [0.4.1] — 2026-07-23

Doc-consistency pass out of the first fresh-agent acceptance read (the QB2 known-gap): a new agent, given only `SKILL.md` + `ref/`, opened a real board, built it, and the build.py-invocation drift it hit got fixed across the ref spec. `SKILL.md`'s open/build sections had already been corrected; `ref/board-form.md` had been left stale — exactly the cross-file drift this skill warns about.

- **`ref/board-form.md` synced to the `<skill>/build.py` call.** §7 still showed the bare `python3 build.py <folder>`, which fails if you `cd` into the board folder (the script lives in the skill dir, not the board). It now reads `python3 <skill>/build.py <board 文件夹>` with the same "don't cd in" note the SKILL.md open/build sections carry. The last bare shorthand in SKILL.md's `sync` section was corrected too.
- **`ref/board-form.md` §2 gains the slug + default-state rules.** `-<slug>` is short lowercase English, parser-ignored; a freshly-opened Q is always `state: 🔴 OPEN`. Both were in SKILL.md's open steps but missing from the "full spec".
- **`ref/board-form.md` §3 marks board.md's required vs optional sections.** The Q-file spec (§4) already listed 必填/选填; board.md did not — `## Topic` / `## Pipeline` / `## Roster` required, `source:` / `## Links` optional, now stated.
- **known-gap surfaced, not folded in.** The acceptance read hit a question the current model has no home for — where a note that is off the board's `spine` but worth keeping should go (not ⏸️ ON HOLD, which is on-topic-deferred; not a forced Q). Drafted as a question for the skill's own board; left off SKILL.md per the graduation rule (undecided stays out of the manual). Distinct from the existing `QB3` (migrate the two older boards).

## [0.4.0] — 2026-07-23

The single-Q slide layout (QA4) is settled and closed. The focus-mode slide got the polish that finally answered its last open fork — *what belongs on stage vs. folded* — and the rule graduated into the spec.

- **section headings gain a line + an `expand all`.** Each of 📍 Now / 🎯 Done when / 💡 Why here now has an underline and, when it holds collapsible items, a right-aligned `expand all` that opens/collapses every item and code block in that section at once. Pure enhancement (`.secall` + a delegated click handler): strip the script and each item is still individually openable, all text stays in the DOM.
- **code blocks fold by default.** A ```` ``` ```` block in the prose renders as a one-line `</> code · N 行` disclosure, revealed on click or via `expand all`; `## Diagram` (the headline picture) is the one that stays open (`body(txt, fold_code=False)`). So a slide's first glance is a clean column of item names + the diagram, not walls of code.
- **the big title copies with a space.** `<span class="hid">QA4 </span>…` — the id and title were glued on copy (`QA4Single…`) because the gap was CSS `margin`, not a character; a real space now sits inside the badge so the heading copies as `QA4 Single-Q slide layout`.
- **QA4's `## Law` graduated into `ref/board-form.md §8`**, not SKILL.md — display spec stays in the spec doc, keeping SKILL.md lean (QB1's rule). The on-stage/folded rule, up-down `Now`/`Done when` stacking, long-Q scrolling (no truncate/split), no-16:9-lock, and the copyable-title note all live there now. Graduated list: `QA2 · QA4 · QA6 · QC1`.

## [0.3.0] — 2026-07-23

The graduation mechanism — SKILL.md is now defined as the board's settled questions, distilled. Plus the live layer (serve.py) gets a foothold in the manual.

- **板 ↔ SKILL.md, written down.** New SKILL.md section: this file is the crystallisation of the skill's own board (`diagram/01-boardform-260722/`). A question that reaches `✅ SETTLED` graduates its `## Law` into SKILL.md; questions still `🟡/🔴` do NOT enter the manual — so a "just-decided" rule never gets written as iron law (QD1's permission rule was written hard, then overturned — the cautionary case). SKILL.md is therefore always *the sum of settled rulings, no more*. The rule lives in QB1's `## Law`.
- **serve.py enters the manual.** New `serve` action: one server serves the whole repo root (`serve.py --root <root>`), giving every board live commenting-to-disk plus chat/terminal per question. The old `comment` text ("stage in localStorage → Sync to md") was stale — QA6 shipped Save-immediately-writes-to-disk; the section now says so, with the browser Sync/Copy path demoted to the serve.py-not-running fallback.
- **chat / terminal held as provisional.** The QD group (drawer via claude_agent_sdk, terminal via ttyd) is real and running but still `🟡` — SKILL.md carries only a pointer to it, not rules, per the graduation mechanism.
- **actions regrouped** — offline (`open · add · build · sync · link · close`, needs only build.py) vs live (`serve · comment`, needs serve.py).

## [0.2.0] — 2026-07-23

`SKILL.md` written. Comments become first-class. The zero-script promise is restated as what it actually protects.

- **`SKILL.md` + three `ref/` files** — the skill is now readable by someone who was not in the room: `ref/q-template.md` (copy this to add a question), `ref/board-form.md` (full spec: folder, numbering, section↔page map, syntax table), `ref/writing-rules.md` (how to write it so people understand, plus the cold-read prompt and its convergence test). `ref/board-example.md` was replaced — it still held the pre-0.1 single-file `[BOARD]`/`[Qn]` form.
- **`## Comments`** — inline comments pinned to a sentence, each with its own state: `- [ ] JL 「quoted sentence」 · 260723 1100` plus an indented body; `[x]` marks it solved. Open comments highlight their sentence in the prose and force the fold open; solved ones grey out and strike through. A quote that no longer matches the prose is flagged **⚠ anchor lost** on the item and in the fold label — a comment can never silently detach. `## Discussion` stays as the free-form thread.
- **in-page commenting** — select a sentence, press 💬, write, Save. Comments stage in `localStorage` and go to the md in one shot via "Sync to md" (File System Access API) or "Copy". Any 1–4 letter initials work, not just JL/RA/CC; new names are added from the dropdown and remembered, and each gets a stable colour.
- **`watch.py`** — rebuilds on any `.md` change, so "Sync to md" → refresh is a closed loop with no Claude Code in it.
- **topic/explanation bullets** — `- heading` plus indented lines renders as a bolded lead with its explanation underneath; `## Done when` items take the same shape. Long passages stop being walls of sentences.
- **`## Log` takes a time** — `260723 1030 · what changed`; the time is optional.
- **titles are phrases, ≤14 chars** — the full question belongs in `## Question`. The board's own ten titles went from 43 chars at worst down to 8–15.
- **the invariant replaced the rule.** 0.1.0 asserted "zero `<script>` in the output". That became false the moment commenting shipped, and it was never the real guarantee anyway. What is asserted now: **strip every `<script>` and each question plus the full prose is still there** (checked on every build). Scripts may only enhance.

Known gaps (tracked on the board at `0_utils/diagram/01-boardform-260722/`): "Sync to md" has never been run end to end (QA6), no fresh-agent acceptance run (QB2), the two older boards are not migrated (QB3), and comments already written into md have no check for a broken anchor after the prose is edited.

## [0.1.0] — 2026-07-22

First working version. Board = a folder; `build.py` turns it into one static page.

- **board form** — `<unit>/diagram/<NN>-<topic>-<YYMMDD>/` holds `board.md` (title · `spine:` · `close:` · `## Topic` · `## Pipeline` · `## Roster`) plus one `Q<A><n>-<slug>.md` per question, plus generated `board.html` and `fig/`.
- **binding is by PATH** — every `Q*.md` in the folder is on the board; `## Roster` only sets order and grouping. An unlisted file still renders (under ⚠️) and warns on stderr — a missed roster entry can never drop a question.
- **Q file sections in English** — `## Question / Diagram / Done when / Now / Why here / Glossary / Discussion / Log`. Chinese section names still parse, so older boards build unchanged.
- **`## Done when` is a checklist** — `- [ ]` / `- [x]`, with an auto count (`3/5`) in the panel header.
- **`## Diagram`** — a fenced ASCII diagram per question, readable in the md and rendered as-is in the page.
- **`## Log`** — dated one-line history per question (`260722 · what changed`).
- **state labels** — `✅ SETTLED / 🟡 PARTIAL / 🔴 OPEN / ⏸️ ON HOLD`.
- **zero `<script>` in the output, asserted at build time.** Every question is a real `<section>`; collapsibles are native `<details>`; navigation is plain anchors. The page cannot render blank.
- **focus mode is pure CSS** — `:target` + `:has()` show one question full-screen, unbounded (no card border/radius/fill), 38px title, prev/next/index links. Same file serves both reading and projecting; there is no separate `deck.html`.

Known gaps (tracked on the board at `0_utils/diagram/01-boardform-260722/`): `SKILL.md` is not written (QB1), no fresh-agent acceptance run (QB2), the two older boards are not migrated (QB3), inline comments are half-built (QA6 — the md syntax parses, the CSS does not exist yet).
