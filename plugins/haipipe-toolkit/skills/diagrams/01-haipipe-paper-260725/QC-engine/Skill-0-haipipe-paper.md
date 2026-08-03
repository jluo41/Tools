# haipipe-paper · v0.4.6
state: 🟡 PARTIAL · account written; the acceptance test is open in Items
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
Why does the Paper family need one public front door, rather than asking a writer to know the lifecycle, stage, phase, delivery, and evidence workers in advance?

This page tests whether `haipipe-paper` makes the first decision correctly: which paper is in scope and which kind of work the request actually asks for.
It should make the route legible without becoming a second implementation of any specialist.

## Diagram
<!-- haipipe:skill:tree:start 31ad4899666178a5 paper/haipipe-paper -->

```
haipipe-paper/
  fn/
    digest.md          172 ln  Digest (condense the session into routed feedback)
    feedback.md        245 ln  Feedback (capture skill feedback, route at capture, fix later)
    probes.md          192 ln  Probe files (paper)
  CHANGELOG.md         270 ln  haipipe-paper — Changelog
  PREFERENCES.md        29 ln  haipipe-paper — Behavioral Preferences (portable)
  SKILL.md             611 ln  Skill: haipipe-paper (orchestrator)
```

<!-- haipipe:skill:tree:end -->

```
HUMAN REQUEST
      │  resolve paper root + intent; ask when venue is genuinely ambiguous
      ▼
haipipe-paper ──▶ lifecycle / stage / deliver / round / rebuttal
      │                    │
      │                    └── stages own their declared DPRC phases
      │
      └── probe need ──▶ haipipe-paper-probe ──▶ haipipe-probe ──▶ QA file

The front door names the next owner.  It does not write the stage artifact,
open a probe entry, run the bank, or declare a gate passed.
```

## Content
<!-- haipipe:skill:body:start 31ad4899666178a5 paper/haipipe-paper -->

**haipipe-paper** · `0.4.6` · last shipped 2026-07-30

- folder   `paper/haipipe-paper/`
- tools    Bash, Read, Write, Grep, Glob, Skill
- summary  Front door for the Board-first paper lifecycle. Each stage runs its declared phases/gates; delivery routing now includes the explicit project/projection leaf for isolated S-page candidates. History: ./CHANGELOG.md.

### SKILL.md



Skill: haipipe-paper (orchestrator)
====================================

User-facing entry for the paper lifecycle.
The paper lifecycle is a delivery owner: it owns this paper's angle, resources, claims, narrative, section map, displays, maturity, and dated work rounds.
Project-level evidence lives outside the paper in tasks and discoveries; when the paper hits a gap, record a delivery need (see "Delivery Need Routing" below) and route to the evidence worker.

This orchestrator parses intent and dispatches to stage/specialist skills via `Skill()`.
Stage skills internally drive the DPRC phase workers (`2-phase/`); users and this router never invoke phase skills directly.
Canonical structure: `../README.md` at the paper skill root (skill-tree layout, Stage to Procedure, Router Rule, Maturity Rule).

ALWAYS read and honor `PREFERENCES.md` (this skill's own folder): portable, git-tracked global behavioral preferences that survive a machine change.
`digest` / `feedback` append flagged global prefs there (merge-or-create).

The model: stages × declared phases
------------------------------------

The front door exposes STAGES, not executors.
A stage runs the ordered `phases:` list in its own `stage.md`. Most current
stages declare all four slots:

```text
   DRAFT ──▶ PROBE ──▶ REVISE ──▶ CHECK
   write &   collect    weave in    human
   raise     evidence   the answer  gate
```

PROBE is the ONLY phase that touches the bank, and it reaches it only through a probe file and a clean-context agent — the paper session never runs bank work itself.
Venue currently declares `draft → probe → check`, so its REVISE slot is shown
as `--`. Never invent a phase that the stage did not declare.
There is no generic `discover` or `task` lifecycle verb: a claim-bearing bank need goes through
PROBE, not an inline paper run. The narrow display exception is a missing, non-claim display-ready
aggregate; it is recorded in the Display request and goes to `haipipe-task-for-display`.
A standalone utility question a human wants (a quick lit scan, a data check) goes to the bank's OWN door — `/haipipe-task qa` or `/haipipe-discovery qa` — typed by a person, never proxied by the paper.


Verbs
------

One block: verb, aliases and trigger keywords, then where it goes.

```
enter | status | dashboard | preload         -> haipipe-paper-enter (open-needs console; GET-OR-CREATE: a missing path offers to create the paper first, see Dispatch notes; also "enter paper", "paper status", "create paper", "new paper folder")
venue | journal | 选刊 | any venue name       -> haipipe-paper-stage venue (recommend + pin; MISQ/ISR/Management Science/Nature/PNAS/JAMA/NEJM/Lancet/clinical/grant/patent all land here)
seed                                         -> haipipe-paper-stage seed        (also "paper seed", "why this paper")
resource | prereq | prerequisite | need      -> haipipe-paper-stage resource    (venue-FREE; what must EXIST for this paper to be testable, does it exist, can it CARRY the claim -- data, model checkpoints and producing-code alike; also "do we have the data", "does the checkpoint exist", "demand", "1-resource")
claims | claim | ledger                      -> haipipe-paper-stage claims      (also "claim gap", "supported", "GAP", "H1/H2/H3")
pitch                                        -> haipipe-paper-stage pitch       (also "cover letter", "one-minute story", "editor's chair")
narrative | story | contract                 -> haipipe-paper-stage narrative
display | figures | figures-tables           -> haipipe-paper-stage display     (also "figure plan", "gallery", "preview pdf")
section-edit | section | sec | §N            -> haipipe-paper-stage section-edit (per-section prose work)
table | figure | plot | diagram |
  illustration | figure1 | framework         -> haipipe-paper-stage display first (allocate/bind the unit); then commission the matching Display renderer
build | scaffold | restructure | conform | folder | project | projection |
  audit | review | claim-audit | reviewer | optimizer |
  polish | consistency | format | typeset |
  compile | diffpdf | overleaf | ship | deliver  -> haipipe-paper-deliver (artifact side; forwards the leaf verb to 1-build/2-audit/3-polish/4-ship; polish runs consistency→format→typeset; also "make submission-ready", "conformance", "produce the PDF")
round | rounds                               -> haipipe-paper-round (dated work rounds; also "todo", "decisions", "applied")
probe ["<question>"] | probe | probe plan | probe run [PPNN]  -> the probe pool: one 1-probes/PPNN_<topic>/ folder per topic, one QXn_<slug>.md entry file per q-executor (RAISE / SHOW / PLAN / RUN the five-step loop)
rebuttal                                     -> haipipe-paper-rebuttal (also "reply to reviewers", "reviewer comments", "OpenReview response", "R1 revision")
feedback "<text>" | feedback list|move       -> fn/feedback.md (resolve BEFORE other parsing)
digest [session] [--dry-run]                 -> fn/digest.md   (resolve BEFORE other parsing)
"<natural language>"                         -> infer via the keywords above, dispatch
```

**Phase-verb pass-through**: a trailing `draft | probe | revise | check` after any stage verb's args is a PHASE VERB — forward it verbatim through the lifecycle router to the stage skill (e.g. `/haipipe-paper edit 4-llmtrait revise` → section-edit drives its REVISE phase).
Stage skills stop only at the human gates declared in `gates:`. All current
stages declare `[check]`: DRAFT, PROBE, and (when declared) REVISE run
unattended, then CHECK asks for explicit approval. Never invent or auto-advance
a gate.

Examples:

```
/haipipe-paper enter "examples/Project-PhyPat-Simulation/papers/Paper-PhyPatSim"
/haipipe-paper enter papers/Paper-NewIdea --org jluo41    (missing path -> confirms, then creates)
/haipipe-paper venue "physician trait -> opioid prescribing; observational CMS Medicare" --no-pin
/haipipe-paper claims
/haipipe-paper display "Table 1 + STROBE flow + subgroup forest"
/haipipe-paper probe "NEED-1: expand ex ante audit to all 20 messages"
/haipipe-paper probe run PP02
```

Routing
--------

Resolution order (first match wins):

```
1. feedback / digest first-token             -> run the fn (before any other parsing)
2. first positional matches a verb/alias     -> that target
3. keyword scan over the whole phrase        -> per the trigger keywords in the Verbs block; a named journal/venue anywhere -> venue
4. no args, cwd inside a paper root          -> enter "."
5. no args, no paper root                    -> chooser (below)
6. input but target unclear                  -> ASK; NEVER silently default a venue (venue drives pitch/narrative/display/prose, expensive to redo)
```

A paper root is any directory upward containing `the S pages`, `0-lifecycle/`, `0-*.tex` + `sections/`, or `2-src/compile.sh` + `sections/`.

Venue coupling (drives two routing rules): seed + resource + claims are
venue-FREE; Venue pins the journal on
`0-lifecycle/2-venue/S-Venue-0-venue.md`; pitch/narrative/display/section-edit
are venue-ALIGNED and consult that page. Direct venue-pack reads are fallback
when it is absent, or deep dives through its `[source: ...]` tags.
So: "paper" with claims done but no venue pinned -> run `venue` before pitch.
Re-targeting ("move to another journal") -> re-run `venue`; pitch re-couples (new [primary], new RQ framing); resource and claims stay unchanged (what a paper NEEDS to exist does not depend on where you send it).

**Every lifecycle STAGE goes through one skill.** `seed · resource · claims · venue · pitch · narrative · display · section-edit` are no longer separate skills — dispatch them as `Skill("haipipe-paper-stage", args="<stage-key> <rest>")`, stage key first. The four display RENDERERS (`table · figure · diagram · illustration`) are workers and keep their own skills.

Dispatch notes (only where non-obvious; everything else is `Skill("haipipe-paper-<target>")` or `Skill("haipipe-paper-lifecycle", args="<verb> ...")`):

```
enter     Path exists -> Skill("haipipe-paper-enter", args="<path>"). Path MISSING -> get-or-create:
          CONFIRM FIRST (creating a repo is outward-facing; never create off a typo). Then resolve the
          parent project (walk up, or ask). Project-* repo -> paper is REPO-BACKED: resolve --org
          (flag or ask, NEVER assume; the paper's owner may differ from the project's), follow the
          papers-inside recipe in project/haipipe-project/fn/repo-project.md, then
          Skill("haipipe-paper-lifecycle", args="folder <paper-path>"), double-bump (paper push ->
          project pointer -> workspace pointer), and continue straight into the console.
          Plain projects: folder + scaffold, then console.
probe     Operates on the flat cross-stage pool (1-probes/PPNN_<topic>/; the README board is
          derived from it). Sub-modes are listed in the Verbs block above (raise · board · plan
          the campaign · run). It is the SAME operation at two scopes: this paper-level verb
          works the WHOLE pool (see/plan/drain every open question across all stages), while a
          stage's PROBE phase works only its own slice — the entries whose `### q-consumer`
          bullets name that stage — during that stage's declared phase turn. Both go
          through the one worker, haipipe-paper-probe, which runs the five-step loop
          MATCH-before-DISPATCH and is the ONLY thing that touches the bank; the umbrella and the
          stages never do. That worker follows the shared probe model owned by
          `probe/haipipe-probe/SKILL.md`. Anatomy + campaign + model: fn/probes.md.
```

After dispatch, capture the specialist's structured tail (status / summary / artifacts / next) and present it.

Closing Block (end every reply)
--------------------------------

THE single source of truth for the closing block (every stage / enter skill inherits this section).
This is the explicit enclosing-skill exception defined by `haipipe-board`:
Paper calls Board, but a Paper reply emits this ONE composed block rather than
also appending Board's direct-session `status.py` strip. The `board:` line below
preserves the active Board/page attachment. A direct `/haipipe-board` session
still uses Board's own strip.

**The BOARD is the paper's face; the closing block is the session's.** Ruled
2026-07-26 (design board `QA1`, `QA4`): `/haipipe-paper` is the single thing a
human types, and it CALLS `haipipe-board` to build and open `⑧`. So the closing
block stopped carrying a 9-stage strip, which was a worse copy of the board's own
spine, and now carries the URL instead.

In a paper session, END every reply with ONE fenced `text` block: a titled top
rule carrying `📄 paper · <active-stage> 🔥`, the two-line tail, a plain bottom
rule, then the board URL and the PHASE line:

```text
── 📄 paper · seed 🔥 ─────────────────────────
status:  ok · seed             (status and active stage merged on one line)
next:    <single recommended command>
──────────────────────────────────────────────
board:   http://127.0.0.1:5599/<path>/0-lifecycle/board.html#S-Seed-0-seed
phase:   draft 🔥🚀  │  probe ⬜  │  revise ⬜  │  check ⬜
```

The `board:` line is deep-linked to the page this session is working, so one
click lands on it. If the push to the browser failed, say so on that line and
print the URL anyway; never report success when only the build succeeded.

The PHASE line survives the strip's retirement, and the reason is worth stating:
it is the only thing here the board does NOT show. A page's `state:` is its
gate status, not the live DPRC progress of a run in flight. The stage line was
derivable from the board and therefore redundant; the phase line is not.

Markers: 🔥 active now · 🚀 frontier (farthest the paper has ever reached) · ✅ done · ⬜ not started · `--` skipped.
Rules: the phase line always has the four display slots
`draft | probe | revise | check` and exactly one `probe` slot. A phase omitted
from the active stage's `phases:` list is `--`, not pending. Probe entries carry
their own evidence type; the closing block never revives retired
`cite`/`val`/`disp` sub-tracks. EXACTLY one 🔥, never zero.

Gate-aware: closing a stage and advancing to the next requires an EXPLICIT approval action that the current stage is done (Stage Gate, `../../paper/route/ref/08-stage-gate.md`) -- by the human (copilot mode) or by a reviewer subagent standing in for the human (autopilot mode); once the S page carries the gate ledger, ✅ means "approved", and the ledger records who approved (human or agent).


Comment lifecycle
------------------

THE single source of truth for inline comments across ALL paper skills. Every phase worker, lifecycle stage, and orchestrator follows this convention.

**Loaded-context rule.** This section is not in context at every skill
invocation, so it cannot bind behavior by itself. Every skill that touches
working files must INLINE its binding subset: never delete/reword `> USER:`;
reply `> CC:` underneath; only the user resolves; move resolved threads
verbatim into the owning S page's `## Log`; make surgical edits only. The stage
hubs carry that block as "Comment rules (binding)".


- 0.1 · Actor ids
      The `{...}` token names **who** authored that line. Keep it short. One flat namespace:
      | Kind | Examples | Note |
      |------|----------|------|
      | AI tool / agent | `CC` (Claude Code), `GPT`, `GEM` (Gemini), `CDX` (Codex) | reviewing tools; append `-<topic>` on findings |
      | Person | initials (`AU`, `CO1`, etc.) | authors / coauthors |
      | Role | `R1`, `R2`, `AC`, `ED` | numbered reviewers, area chair, editor |
      **The human actor id is asked, never assumed.** At the start of a cycle the skill asks the user for their initials (and the pass date `vMMDD`). Never default to any specific initials.

- 0.2 · Two comment formats
      In outline `.md` files, blockquote style:
      ```markdown
      > USER: comment about this paragraph
      > CC: response to the comment
      ```
      Used in: section `.md` files, seed, claims, pitch, narrative, and `1-probes/PP*/*.md` entries.
      In `.tex` files, LaTeX comment style:
      ```latex
      %% {CC-content-v0531}: finding | suggestion ========>
      ```
      Used in: `sections/*.tex`, `4-display.tex`, rebuttal files.

- 0.3 · The two marks (tex format)
      Finding (the comment):
      ```
      %% {<actor>-<topic>-vMMDD}: <one-line finding> | <one-line suggestion>
      ```
      - `<actor>` -- who wrote it. A reviewing AI appends the topic for traceability: `CC-content`, `CC-values`, `GPT-cite`.
      - `vMMDD` -- the pass date (e.g. `v0531`). New round = new date.
      - `<finding> | <suggestion>` -- what's wrong, then what to do. One line each.
      Reply (same line, after the separator):
      ```
      %% {CC-content-v0531}: claim stated as causal. | Soften to "associated with". ========> {AU v0531}: accept
      ```
      - `========>` -- the reply separator (literal, eight `=` then `>`).
      - Reply verb vocabulary: `accept` / `reject` / `modify: <how>` / `discuss: <q>` / `done`.

- 0.4 · Anchoring (tex files)
      A comment sits on its **own line, directly below the text it refers to**:
      ```latex
      Agreeableness showed the strongest positive correlation ($r = 0.62$).
      %% {CC-values-v0531}: 0.62 here vs 0.747 in the table. | Reconcile. ========>
      ```
      For wrapped paragraphs, use `@"quote"` to anchor: `%% {CC-content-v0531}: @"we next examined" opener is throat-clearing. | Start with the finding.`

- 0.5 · The lifecycle
      Comments come from three places:
      1. **Inline in the working file**: `> USER:` comments (outline) or `%% {USER}:` comments (tex)
      2. **Session (chat)**: direction, reasoning, taste decisions -- agent writes these into the file as `> USER:` (quoting what the user said)
      3. **`> CHECK:` comments**: seeded by the CHECK worker at every flagged report
         item's exact spot. The human replies `> USER:` under each; after resolution,
         the whole thread moves into the owning S page's `## Log`. Direction is the
         reverse of `> USER:` -- agent asks, human rules.
      ```
      1. User adds comment in the .md file (or says it in session, agent writes it in)
      2. CC responds underneath
      3. Work happens, content changes
      4. User confirms resolved
      5. Comment thread MOVES to the owning S page's ## Log
         (with -> applied / -> rejected / -> deferred)
      6. Working file stays clean
      ```
      Rules:
      1. **Comments live in the working document while active.** They sit next to the content they discuss.
      2. **Agent never removes a comment.** Only the user confirming resolution triggers the move.
      3. **Resolved comments move to the owning S page's `## Log`**, grouped by
         phase and date. The comment thread is preserved verbatim.
      4. **Session comments that represent decisions** are written into the working document so they enter the same lifecycle. Ephemeral chat that is not a decision disappears with the session.
      5. **Active comments may cross internal phase boundaries.** DRAFT, PROBE, and
         REVISE are not human gates in the current stage contracts. CHECK reviews
         unresolved threads and either resolves them or restarts the appropriate
         phase.

- 0.6 · S-page `## Log` format
      Every lifecycle S page owns both its current content and history. There is no
      live `_LOG` sidecar. Insert new dated phase records directly under that page's
      `## Log` heading, newest first. If the working document is the S page itself,
      move the resolved thread from its content position down into its own `## Log`.
      **Insertion is non-destructive.** The previous newest entry stays byte-intact;
      the new entry slots between `## Log` and that entry.
      **Entry headings carry date + HH:MM**
      (`### 2026-07-05 13:29 — [PHASE] PROBE — START`), so the S page
      doubles as a coarse on-disk timeline. Legacy undated entries stay as-is.
      ```markdown
      ### 2026-07-03 10:14 — [DRAFT] resolved comments

      ### Seed Question
      > USER: don't use "discretion", too academic
      > CC: reframed to "room for judgment"
      -> applied

      ### Motivations
      > USER: lead the first motivation with a puzzle
      > CC: done, led with "the puzzle is..."
      -> applied
      ```
      Why move, not copy:
      - The working document stays readable as content, not buried in old discussion.
      - Each phase gets a clean slate.
      - The S page preserves the full reasoning chain beside the artifact it explains.
      - If a comment is reopened, it is written fresh, not resurrected from history.

- 0.7 · REVISE phase: no comment-first
      REVISE is the exception. REVISE workers apply changes directly (no comment-first round). They leave `%% {CC-<worker>}: <why>` comments explaining non-trivial changes. These comments are for CHECK to review, not for a human reply cycle. The human reviews in CHECK and can add `> USER:` comments to restart REVISE.

- 0.8 · Round invariants (tex comment-first, when used)
      | Round | A skill MAY | A skill MUST NOT |
      |-------|-------------|------------------|
      | **1 -- review** | insert `%% {CC-...}:` comment lines | change any body text, banner, label, or value |
      | **2 -- apply** | apply changes for `accept` / `modify` replies | touch any `OPEN` comment; apply a `reject` |
      Round 1 diff adds only comment lines. If any non-comment line changed, the pass violated the protocol.
      No-Arg Chooser
      ---------------
      When no paper root is found, do not fan out.
      Emit a compact chooser (one line per entry; the Verbs block carries the detail):
      ```
      📄 haipipe-paper: no paper detected. Pick an entry:
        venue       /haipipe-paper venue "<topic or paper-path>" [--no-pin]
        enter       /haipipe-paper enter "<paper-path>" [--org <owner>]   (missing path -> offers to create it)
        section-edit | rebuttal | probe    (see /haipipe-paper help text above)
      ```
      Specialist Return Contract
      ---------------------------
      Each specialist returns a tail block:
      ```
      status:    ok | blocked | failed
      summary:   2-3 sentences on what the specialist did
      artifacts: [paths created, read, or modified]
      next:      suggested next command
      ```
      Delivery Need Routing
      ----------------------
      THE single source of truth for how the paper records a gap as a need, routes it to the right evidence worker, and backfills when the answer returns. Paper-owned; the application skill keeps its own copy. There is no cross-skill shared file.
      Core rule: the paper owns the STORY and the JUDGMENT; the EXECUTORS (task and discovery) own the EVIDENCE, and the probe is the map between them.
      Paper work is demand-driven: a paragraph, claim, figure, or round todo may reveal that the next action is evidence work.
      The enter/status path surfaces those needs before recommending more writing.

- 0.9 · How paper talks to probe
      No message bus, no shared contract file. Two channels carry it, and the agent (this session) is the medium:
      ```
      1. Command   paper hits a claim gap -> the agent runs
                   /haipipe-paper probe "<question>" (opens a `## QX<n>` ENTRY in the topic's
                   probe file). PROBE owns the whole five-step loop: ① ORGANIZE the
                   `### q-executor`, ② MATCH against the bank's QA corpus, then
                   RUN FORWARD, dispatching the
                   `### q-executor` block only for the entries MATCH left as run | code | new.
      2. Disk      paper writes the need on its owning S page or claim ledger; the executor
         (async)   writes the answer as <task-folder>/QA/<n>-<slug>.md; the entry's
                   `**target**:` points at that FILE, its `### a-executor` copies the answer
                   in, and each Q-consumer's a-consumer (in the stage doc) interprets it. No
                   handshake — binding is by PATH, and the file on disk IS the state.
      ```
      Who owns which format: the paper owns the NEED (loose) and the a-consumer in its stage doc (its own vocabulary). The EXECUTOR owns the ANSWER (the QA file: `# Q` / `## Answer` / `## Caveats` / `## Not-done`, general language, anatomy in `probe/haipipe-probe/SKILL.md`). A CLAIM's status is the paper's alone, and lives in `0-lifecycle/1-work/S-Work-1-claims.md`. That is why no shared interface file is needed: each artifact's shape belongs to the layer that produces it.

- 0.10 · When to record a need
      Only when the problem is EVIDENCE, not wording. A wording/structure problem loops back inside the paper lifecycle (1-claims / 2-pitch / 3-narrative / 4-display / 5-section-edit). A need leaves the paper for an evidence worker.
      ```
      paper GAP -> a Q-consumer in the stage doc -> PROBE opens a question ENTRY in
      1-probes/ and MATCHes it -> PROBE DISPATCHes only what MATCH could not close -> the
      answering QA file -> the entry's `### a-executor` -> each Q-consumer's a-consumer ->
      the paper backfills (the claim's status flips in S-Work-1-claims.md)
      ```
      Do NOT route through a project-level narrative layer (there isn't one).

- 0.11 · Routes
      ```
      claim needs evidence / robustness / literature / a data artifact -> /haipipe-paper probe "<question>"  (an ENTRY in 1-probes/; PROBE does MATCH first, and dispatches only what MATCH cannot close)
      figure/table lacks its verified display-ready aggregate           -> /haipipe-task-for-display <need>
      figure/table has a verified aggregate and needs a paper asset     -> haipipe-paper-stage display → Intake → matching Display renderer
      settled claim status (supported|refuted|inconclusive             -> 0-lifecycle/1-work/S-Work-1-claims.md (the ONLY home of a claim's status; the
        + confidence + claim_type)                                        probe entry carries only the `### a-executor` copy of the bank's answer.
                                                                          answer)
      wording/section placement                                        -> the owning lifecycle stage skill
      standalone utility (a HUMAN, not the paper: lit scan, data check) -> /haipipe-task qa | /haipipe-discovery qa (the bank's own door)
      ```
      The entry is `/haipipe-paper probe "<need>"`: PROBE opens a question ENTRY
      (`## QX<n>`) in the right topic's probe file and owns all five steps:
      ① ORGANIZE → ② MATCH → ③ DISPATCH → ④ POINT → ⑤ INTERPRET. DRAFT only writes
      the S-page content and its Q-consumer questions.
      Two entry rules (who the delivery calls):
      - a CLAIM need (a claim's status is at stake) -> raise a question ENTRY and let the PROBE phase route it. The paper never calls a raw compute agent for a claim-bearing need, and never executes bank work inline (LAW 1).
      - a pure RENDER need (no claim at stake, e.g. re-render a figure) -> return to the Paper Display stage; it reuses the approved Intake and commissions the renderer. Call `/haipipe-task-for-display` only when the display-ready aggregate itself is missing or must change.
      ALL evidence enters through a stage's PROBE phase; the paper never calls the bank directly.
      Resolved evidence backfills into `1-claims`, `4-display`, sections, or round logs.
      Evidence workers never own the paper story.

- 0.12 · Need record
      Each open need is one row on its owning Board/S page; claim needs live on `0-lifecycle/1-work/S-Work-1-claims.md`:
      ```
      need_id      stable handle (e.g. N1, tied to a claim slot C2 or a display)
      gap          which claim slot / display / section has the gap
      kind         evidence | context | artifact | meaning
      route        the command above
      state        open | commissioned | returned      (mirrors the probe entry's derived state)
      backfill     the slot/display to update when the worker returns
      ```

- 0.13 · Backfill (the return direction)
      The answer is a FILE: the executor's `<task-folder>/QA/<n>-<slug>.md`. The probe entry's `**target**:` points at it, `### a-executor` copies its answer in (the consumer-side single source of truth), and each Q-consumer's a-consumer — its `Answer:` line in the stage doc, anchored `[source: PP<NN>]` — says what it MEANS for this paper. On backfill:
      ```
      - write the claim's status in 0-lifecycle/1-work/S-Work-1-claims.md — supported |
        refuted | inconclusive, + confidence + claim_type. THAT ledger is
        the only home of a claim's status.
      - if the evidence narrows the claim, narrow the claim wording in 1-claims
      - the executor NEVER edits paper prose: it returns a FACT, and the paper decides
        what the fact means and how to phrase it
      ```
      Multiple papers can cite the SAME QA file in discoveries/ + tasks/, each through its own entry and its own a-consumer — the FACT is shared, the JUDGMENT is not.

- 0.14 · Autonomous drain (the "keep going" loop)
      The console is a derive-from-disk, resumable loop body. To drive a delivery to done:
      ```
      LOOP until (no open needs) OR (gate hit) OR (only server-blocked left):
        1. enter    derive frontier + open needs from disk (the queue)
        2. pick     the next actionable need (skip server-blocked)
        3. route    claim -> a question ENTRY (the PROBE phase dispatches it) ;
                    missing aggregate -> task-for-display ; render -> Display → Intake → renderer ; prose -> edit
        4. execute  write the artifact locally, or wait for the dispatched QA file
        5. backfill update the slot/display/entry; mark the need returned
        6. -> 1
      ```
      State lives on disk in the Board/S pages, claim ledger, probe entries, and their target files, so a fresh session re-enters and continues.
      Server vs local: a local need (render, parse, draft, backfill) drains immediately. A need that requires a NEW server run (Stata on PHI depositing to `Report-From-CMS-Server`) is server-blocked: schedule a poll and resume when results land. A figure renders locally; it blocks only if its underlying regression is not back yet.
      Autonomy policy:
      ```
      AUTO (no asking):  local render/parse, backfill claims/displays, draft a stage tex,
                         compile previews, parse logs, status/ledger updates
      PAUSE + surface:   trigger a server/PHI run; declare a final yes/no answer;
                         settle a claim's status in S-Work-1-claims.md; compile-to-submit;
                         destructive round / git ops
      ```
      The loop runs AUTO unattended and stops at the first PAUSE gate, reporting what it hit.
      Evidence Routing Protocol
      --------------------------
      When paper-lifecycle work hits a claim or wording whose support needs NEW evidence, data/variable inspection, or an analysis that does not exist yet, the paper layer must NOT dig into data, scripts, do-files, logs, or variable definitions. Stop. Hand off. Mark the gap. Keep writing.

- 0.15 · The `\needprobe{}` macro
      When a claim lacks evidence, mark it in the `.tex` with a visible red caveat:
      ```latex
      \newcommand{\needprobe}[1]{\textcolor{red}{\textbf{[NEED PROBE]} #1}}
      ```
      Add this macro to the lifecycle preamble (or the paper's shared command file). Use it inline wherever the gap lives:
      ```latex
      \needprobe{Is the intensive margin about patients already on opioids?}
      ```
      The red flag renders in the compiled PDF so the gap is obvious to every coauthor. Remove it when the answer lands (the entry's `**target**` resolves and its `### a-executor` is written) and the claim is backfilled with supported text.

- 0.16 · Handoff protocol
      When paper work surfaces an evidence gap, do the following INSTEAD of investigating the data yourself:
      ```
      a. STOP investigating the data. Do not grep do-files, re-derive variables, or
         design the estimation.
      b. MARK the claim with \needprobe{description of what needs settling}.
      c. RECORD a delivery NEED (per Delivery Need Routing above): the claim under test
         and what an answer would have to establish.
      d. RAISE it as a Q-consumer question. The stage's PROBE phase opens the entry,
         MATCHes it against the bank, and dispatches only what MATCH cannot
         close. The paper TRIGGERS; it never runs the analysis (LAW 1).
      e. BACKFILL: when the answering QA file lands, PROBE writes the entry's
         `### a-executor`, each Q-consumer writes its a-consumer in the stage doc, the
         claim's status flips in S-Work-1-claims.md, and the \needprobe{} flag comes out.
      ```

- 0.17 · The `probe` verb
      ```
      /haipipe-paper probe <need-description>
      ```
      opens a `## QX<n>` ENTRY in the right topic's probe file at `1-probes/`. The stage's PROBE phase (`haipipe-paper-probe`) is what dispatches it — through `Agent(haipipe-probe-q-executor-agent)` to `Agent(haipipe-task-orchestrator-agent)` or `Agent(haipipe-discovery-orchestrator-agent)`, carrying the entry's `### q-executor` block and nothing else. The paper stays a story layer; the executor does the work.

- 0.18 · Heavy probes and subagent dispatch
      When a probe requires reading a lot of code/logs (e.g. cohort construction from Stata do-files), dispatch it to a BACKGROUND SUBAGENT so the main paper session keeps doing paper work:
      ```
      a. Add a beat to narrative/Methods for the topic (e.g. "Cohort construction"),
         marked \needprobe{} until the report lands.
      b. Raise the question ENTRY (/haipipe-paper probe "<need>"), then let the PROBE
         phase dispatch its `### q-executor` with run_in_background=true.
      c. When the subagent report returns, fold it into Methods + Table 1 and flip the
         beat from \needprobe{} to supported.
      ```

- 0.19 · Construction as a first-class beat
      Dataset/cohort CONSTRUCTION is a first-class narrative/Methods beat, not a one-line "Setting" aside. The narrative must account for:
      - inclusion/exclusion funnel
      - unit definition (what is one observation)
      - exposure -> outcome linkage
      - how each outcome, flag, and control variable is computed
      Each of these may trigger its own `\needprobe{}` if the paper layer has no answering QA file covering it. The EXECUTOR (not the paper) reads the do-files, inspects the data, and returns the description.
      Structure Pointers
      -------------------
      Each area's internal contract lives with its owner; consult, never restate:
      ```
      skill tree (0-enter / 1-lifecycle / 2-phase / 3-deliver / 4-respond / 5-present / venue)
                                         -> ../README.md (skill root: Skill-tree layout, Stage to Procedure, Router Rule, Maturity Rule)
      paper-folder layout                -> ../2-phase/REF/paper-folder-anatomy.md (canonical tree, prefix semantics, maturity ladder)
      lifecycle stages + venue coupling  -> ../1-lifecycle/ref/03-paper-lifecycle.md + ../1-lifecycle/ref/04-lifecycle-map.md
      rounds                             -> ../0-enter/haipipe-paper-round/SKILL.md ("Rounds contract")
      venue knowledge                    -> ../venue/playbook-<venue> packs (venue is knowledge, not a pipeline)
      ```
      Composing with Evidence Workers
      --------------------------------
      ```
      /haipipe-paper (router)
              ├─► /haipipe-paper-lifecycle    (the ARGUMENT: seed -> resource -> claims -> [venue] -> pitch -> narrative -> display -> section-edit)
              ├─► /haipipe-paper-deliver      (the ARTIFACT: build -> audit -> polish -> ship; mirror of lifecycle)
              ├─► /haipipe-paper-rebuttal     (any venue, post-review)
              │
              │   evidence path (a claim hits a gap):
              └─► 1-probes/PPNN_<topic>/QXn_<slug>.md (one file per q-executor)
                       │        PROBE runs ① ORGANIZE + ② MATCH ─────► most entries close at MATCH (T2 REUSE)
                       └─► haipipe-paper-probe (the PROBE phase worker, run inside a stage's PROBE phase)
                                ③ DISPATCH the `### q-executor` block, VERBATIM, only for what MATCH missed:
                                     Agent(haipipe-probe-q-executor-agent)          ← its clean context IS the wall
                                          ├─► Agent(haipipe-task-orchestrator-agent)
                                          └─► Agent(haipipe-discovery-orchestrator-agent)
                                ④ POINT  **target** ─► the answering QA file  tasks|discoveries/<group>/<folder>/QA/<n>-<slug>.md
                                ⑤ INTERPRET ─► `### a-executor` (harvest inline) ─► each stage doc's a-consumer

              a stage reaches the bank ONLY through its PROBE phase — no direct discover/task verb
      ```
### The other files

4 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
PREFERENCES.md      29 ln  haipipe-paper — Behavioral Preferences (portable)
fn/digest.md       172 ln  Digest (condense the session into routed feedback)
fn/feedback.md     245 ln  Feedback (capture skill feedback, route at capture, fix later)
fn/probes.md       192 ln  Probe files (paper)
```

<!-- haipipe:skill:body:end -->

## Aims
- [x] 🧭 Establish the entry boundary
      The public command resolves intent and a paper root, then dispatches to
      a named owner.  Its purpose is routing, not content generation.
- [x] 🚦 Record the non-guessing rules
      An unclear venue must be asked, not silently selected.  A phase request
      goes through its stage, and a bank need goes through PROBE rather than a
      direct task or discovery call.
- [ ] 🧪 Exercise the no-argument and ambiguous-intent branches
      A fresh-agent run should prove that the chooser, paper-root detection,
      and venue ambiguity all stop at the intended boundary.

## States
The route and its ownership boundary are now visible on the Board.
What has not yet been independently exercised here is the front door's difficult negative behavior: declining to guess an ambiguous venue or bypass a stage.

## Log
260727 · Audited against `board.md`'s decision-only rule, which says `state:` is about the DECISION and that implementation does not gate this board. Every open item here is implementation or a test, not an undecided question, so the page was reporting itself as open because code was missing. Flipped with no ruling made.
260727 1430 · Created the Paper front-door page from `paper/haipipe-paper/`.
The authored record captures route ownership; the managed spans carry the current shipped instructions and release history.

<!-- haipipe:skill:log:start 31ad4899666178a5 paper/haipipe-paper -->

Converted from the skill's own `CHANGELOG.md`: 35 releases.

260730 · `0.4.6` · explicit projection routing
      - Added `project` and `projection` to delivery routing so gated S-page content
        reaches `haipipe-paper-project` rather than an implicit submission overwrite.
260727 · `0.4.5` · Display Intake routing
      - Separates a missing display-ready aggregate (task-for-display) from a paper-facing render (Paper Display → Intake → renderer).
      - Removes the stale direct re-render-to-task route, so an existing verified aggregate is never mistaken for a paper asset.
260726 · `0.4.4` · one evidence dispatch topology
      - Synchronized the active Paper probe reference and behavioral preference with
        the runtime chain: Paper PROBE performs ORGANIZE/MATCH, the isolated
        q-executor collector performs DISPATCH/POINT, and task/discovery remain
        behind that collector.
      - Removed the last active instruction that told a Paper worker to dispatch
        directly to task/discovery.
      - Corrected active probe-entry globs to the topic-folder anatomy
        `1-probes/PP*/*.md`.
      - Removed active migration instructions for old probe sidecar paths; the Paper
        contract now exposes only the current topic-folder anatomy.
260726 · `0.4.3` · stage declarations are authoritative
      - Replaced the universal four-phase/two-gate story with each stage's
        `phases:` and `gates:` declarations; current stages gate only at CHECK and
        Venue omits REVISE.
      - Moved phase/comment history from `_LOG` sidecars into owning S pages.
      - Corrected probe ownership: DRAFT raises Q-consumers; PROBE authors entries
        and owns ORGANIZE through INTERPRET.
      - Removed the unsupported `argument-hint` frontmatter key so the user-facing
        orchestrator passes the current `skill-creator` validator.
260726 · `0.4.2` · one composed tail, one probe phase
      - Declared Paper as Board's canonical enclosing-skill case: Paper emits one
        closing block with the active Board deep link and never appends the direct
        Board `status.py` strip.
      - Restored the four-slot DPRC line (`draft | probe | revise | check`) and
        removed the retired `cite` / `val` / `disp` probe sub-tracks.
260726 · `0.4.1` · derived state has one home
      - Replaced the stale `current_layer` gate wording with the actual stage-closing approval action.
      - Removed remaining `STATUS` references from delivery routing; open needs and resumable state live on Board/S pages, the claim ledger, probe entries, and their target files.
260726 · `0.4.0` · the Closing Block carries the board URL, not a stage strip
      Implements the single-door ruling (design board `skills/diagrams/01-haipipe-paper-260725`, faces `QA1` + `QA4`, JL 2026-07-26): **`/haipipe-paper` is the single thing a human types**, and it CALLS `haipipe-board` to build and open the paper's `0-lifecycle/`. `haipipe-board` remains its own door for boards that are not inside a paper. Calling is not owning: `haipipe-board` still owns the format, the build, the filename rule, the html and the write-back.
      - **The `stage:` line and `../../application/haipipe-application/stage-strip.sh` are RETIRED.** The strip was specified in the 260622 feedback as reading `STATUS.md current_layer`, with the stated precondition that a stale value would make it lie. `STATUS.md` is retired and the board renders the spine, so the strip has neither a source nor a job. It was a worse copy of something the human already has open.
      - **A deep-linked `board:` line replaces it**, pointing at the page this session is working, so one click lands on it.
      - **The `phase:` line survives, and the reason is stated.** It is the only thing in the closing block the board does NOT show: a page's `state:` is its gate status, not the live DPRC progress of a run in flight. The stage line was derivable from the board and therefore redundant; the phase line is not.
260724 · `0.3.2`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.2.1; older entries below keep their original numbers).
260719 · `3.2.1` · vocabulary: `probe` (not "the constitution"); entry/`### a-executor` naming
      Two vocabulary rulings from JL, both dated 2026-07-19, applied across `paper/`.
      **Ruling A — the `probe` nickname.** JL: "宪法 don't use this name, just use `probe`." Every "THE CONSTITUTION" / "the constitution" / "the probe constitution" naming `probe/haipipe-probe/SKILL.md` is replaced by `probe` or by the actual path, whichever reads better at the site. A nickname already in the repo is still a nickname.
      **Ruling B — the `a-consumer:` probe-file field.** `- a-consumer:` as a FIELD IN A PROBE FILE was replaced by the entry's `### a-executor`; `check-probe-cards.sh` HARD FAILs it under the `stale-old-format` rule. The a-consumer CONCEPT is untouched and still named a-consumer: it is the per-consumer interpretation written in the STAGE DOC (station ②), anchored `[source: PP<NN>]`. Prose that said "the probe section carries its `a-consumer:`" was wrong twice over — probe files hold ENTRIES, not sections, and what an entry carries is `### a-executor`.
      Current model, for reference:
      ```
      QA file (bank)  ->  the ENTRY's `### a-executor`  (probe file: the copy, single source of truth)
                      ->  each Q-consumer's a-consumer  (STAGE DOC: what it MEANS for this consumer)
                      ->  stage content                 (REVISE weaves it in, discharges the bracket)
      ```
      Written under JL's NO TOMBSTONES rule (2026-07-19): "不需要留退役告示,直接抹除任何痕迹" then "follow this rule to do all the following changes." The docs state only the current contract; this CHANGELOG carries the history.
      ### Changed — SKILL.md
      - The `probe` verb block: "That worker follows the shared probe model (the constitution)" -> "...the shared probe model owned by `probe/haipipe-probe/SKILL.md`".
      - Same block: a stage's PROBE phase works "the sections whose `serves:` names that stage" -> "the entries whose `### q-consumer` bullets name that stage". `serves:` is one of the three strings `check-probe-cards.sh` HARD FAILs (`stale-old-format`), so the umbrella was describing a slice the checker rejects. Found during this pass, not on the reported list.
      ### Changed — fn/probes.md
      - Three "constitution" references retitled: the model owner line ("v9.5.0, the constitution" -> "v9.5.0"), the anatomy pointer ("the constitution's \"The probe file\" section" -> "`probe/haipipe-probe/SKILL.md` -> \"The probe file\""), and the loop header ("constitution v9.5.0" -> "probe v9.5.0").
      ### Unchanged (verified LIVE, ruling B)
      Every `a-consumer` in SKILL.md (7 sites) and fn/probes.md (2 sites) already named the stage-doc concept — "each Q-consumer's a-consumer (in the stage doc)", "each stage doc's a-consumer", "a-consumer in its stage doc (station ②)". This file was already on the current model; nothing was rewritten.
260719 · `3.2.0`
      Changed (JL 2026-07-19, paper/2-phase refactor — the sidecar model is retired: `1-probes/` is the only consumer-side source of truth, `_LOG_<stage>.md` the only sidecar)
      - **Retired sidecars swept out of the router.** `Used in: … _CITATION_, _VALUES_` (the two-comment-formats section) → section `.md` files and `1-probes/PP*.md` entries. `fn/probes.md` legacy-migration rule: the "Stage-owned working docs (`_CITATION_`, `_VALUES_`, `_EVIDENCE_`, `_DISPLAY_`) do NOT move" clause named four documents nobody writes; replaced with the live statement of what IS the source of truth.
      - **Dissolved lane skills swept out.** `fn/feedback.md` routed `citation, bibtex, references` to `haipipe-paper-probe-citation`; now `haipipe-paper-draft-citation` — citation holes are DRAFT's to open, not PROBE's. `fn/probes.md` step ⑤ said "the harvest lanes pay out"; harvest is INLINE in ⑤ and `### a-executor` is its only sink, so it now names what actually rides along (source anchors, values, display-unit paths).
      - **Composing with Evidence Workers diagram** redrawn to the current phase split: DRAFT authored ①ORGANIZE + ②MATCH (most entries close at MATCH, T2 REUSE); PROBE runs ③④⑤ and dispatches through `Agent(haipipe-probe-q-executor-agent)`, which fans out to the task/discovery orchestrators — the router previously showed PROBE calling those orchestrators directly, which is precisely the inline dispatch the collector exists to prevent.
      - **Evidence Routing Protocol** re-rooted: `\needprobe{}` comes out when the entry's `**target**` resolves and its `### a-executor` is written (was `target:` + `a-consumer:` — and `a-consumer:` as a probe-file field is a format `check-probe-cards.sh` HARD FAILs). Handoff step (d) attributes MATCH to DRAFT; step (e) states the real backfill chain: PROBE writes `### a-executor` → each Q-consumer writes its a-consumer in the stage doc → 1b-claims.md flips → the flag comes out.
      - **Vocabulary**: probe `SECTION` → `## QX<n>` ENTRY across the description, summary, verb line, Delivery Need Routing, and the `probe` verb; `fn/probes.md`'s no-tables rule now says a probe file holds ENTRIES.
260719 · `3.1.1`
      - WIKI RETIREMENT — three shared docs absorbed here, each now with exactly ONE home (the wiki folder is deleted; every referrer points at the section, nothing is duplicated):
        - **Comment lifecycle** (was `02-comment-lifecycle.md`, 18 referrers) — new section after the Closing Block: actor ids (never hardcode initials), the two formats (blockquote `.md` / `%% {}` tex), the two marks + `========>` reply separator, anchoring, the 6-step lifecycle + 5 rules, `_LOG` format (newest-at-top, non-destructive insert, date + HH:MM headings), the REVISE no-comment-first exception, and the round invariants table. The loaded-context rule is kept: this section is BACKGROUND, so every skill touching working files still INLINES its binding subset.
        - **Delivery Need Routing** (was `11-delivery-need.md`, 11 referrers) — MERGED into the existing section rather than added beside it: how paper talks to probe (command + disk channels), when to record a need, routes, the need-record schema, backfill, and the autonomous-drain loop with its AUTO/PAUSE autonomy policy.
        - **Evidence Routing Protocol** (was `12-evidence-routing.md`, 4 referrers) — new section directly under Delivery Need Routing: the `\needprobe{}` macro, the 5-step handoff protocol, the `probe` verb, background dispatch for heavy probes, and construction-as-a-first-class-beat.
      - Structure pointers repointed: skill tree -> `../README.md` (which absorbed `06-paper-skill-structure.md`); rounds -> `../0-enter/haipipe-paper-round/SKILL.md` (which absorbed `07-paper-rounds.md`).
260714 · `3.1.0`
      - `fn/probe-plans.md` RENAMED to `fn/probes.md` ("plans" is retired vocabulary); the verb table and Dispatch notes re-point at it.
      - Dispatch notes: "Verdicts backfill into 1-claims / sections / round logs" -> the answer lands as a section's `reading:`, and the CLAIM's status flips in `0-lifecycle/1b-claims/1b-claims.md` (the only home of a claim's status). "Buffer convention" -> "Probe-file convention".
260714 · `2.11.0`
260714 · `3.0.0`
      - The `probe` verb is re-pointed at the PROBE-FILE POOL (`1-probes/PPNN_<topic>.md`, one file per TOPIC, one SECTION per question). Before this, every `/haipipe-paper probe` invocation was routed into the dead card/stub model: the routing table sent it to `1-probe-plans/` cards, the `no args SHOW` mode derived statuses from `_ASK/` stubs (which R2 forbids from ever existing, so it would always report zero dispatches even with commissions in flight), and the diagram routed the verdict to the retired gateway.
      - `fn/probe-plans.md` REWRITTEN (legacy filename kept, same precedent as check-probe-cards.sh). It was fully pre-v8: cards in `1-probe-plans/`, the status set `planned | dispatched | verdicted` (two of which are DELETED states), and `dispatch Agent(haipipe-probe-orchestrator-agent) -- ALWAYS, no matter how small the need` — the exact opposite of R13. It now carries the 1-probes/ convention, MATCH-before-DISPATCH, and direct dispatch to the two executor orchestrators.
      - PREFERENCES.md — the highest-authority text in the bucket, loaded on every paper session — re-stated in v8 terms. It MANDATED the retired 4-step procedure and named the archived gateway agent, so a session would obey it, dispatch a nonexistent agent, fail, and (because the preference explicitly forbids substituting an inline scan) have no legal fallback. The INTENT is preserved verbatim: never fake a probe with a web scan.
      - The evidence-routing table's `settled judgment -> the PP card's ## Verdict` route now points at `0-lifecycle/1b-claims/1b-claims.md`, the ONLY home of a claim's status (R7).
      JL resource ruling (pairs with haipipe-paper-resource 1.0.0 + haipipe-paper-lifecycle 2.4.0): RESOURCE registered as a venue-FREE stage between seed and claims. New verb `resource | prereq | prerequisite | need` -> `haipipe-paper-lifecycle resource` -> `0-lifecycle/1a-resource/1a-resource.md`: what must EXIST for this paper to be testable, does it exist, and can it CARRY the claim (data, model checkpoints, and producing-code alike). The stage ASKS (Q<n>) and the probe gateway ROUTES (mints the PP, picks the type) -- so no new probe lane and no new namespace. Venue-coupling prose now reads seed + resource + claims as venue-FREE and unchanged on retarget; the closing-block stage-strip example and the Composing diagram both carry `resource`. resource SHARES the number 1 with claims (precedented: 2a-venue/ and 2b-pitch/ already share 2); nothing renumbers.
260712 · `2.10.0`
      JL routing ruling (haipipe-probe 7.8.0 companion): `probe plan` (the campaign consolidation pass) gains a ROUTE step — resolve every card's `target:` (the receiving task-folder / discovery folder; `NEW ...` when it must be created; `?` only with a stated reason). The campaign pass is the right moment because it is the only one where the whole evidence campaign is visible at once: two cards routed at the same task-folder are a hint they should merge, and a card with no plausible home is a hint the need is under-specified. DRAFT-buffered skeletons may leave `target: ?` — the paper often does not yet know what the project holds.
260712 · `2.9.0`
      JL both-banks layout ruling (pairs with haipipe-probe 7.7.0; supersedes the 2026-06-29 per-stage layout for PROBE CARDS only):
      - PPNN cards live FLAT in `1-probe-plans/PPNN_<slug>.md` beside the campaign README -- one cross-stage pool, `serves:` carries stage affinity, the whole campaign is one `ls`. The `probe "<text>"` BUFFER sub-mode files new cards there; `probe plan` reads all cards from the pool.
      - Execution-bank stubs live in `_ASK/` containers (`<receiving folder>/_ASK/PPNN_<slug>.md`), filename mirroring the card's.
      - `fn/probe-plans.md` rewritten: location + migration direction reversed (legacy per-stage `_PROBE/` cards move INTO the pool on first touch); card anatomy defers to the probe layer's SKILL.md.
260711 · `2.8.0`
      Added (JL cross-stage ruling 2026-07-11; pairs with haipipe-probe 7.5.0)
      - `probe plan` sub-mode: the CAMPAIGN consolidation pass, run after a cross-stage draft sweep — read all stage drafts + all _PROBE/ cards, merge duplicate needs (one card, many serves:), author the dispatch DAG (gating first, refutation-capable early, dependents wait, query-once) into the Campaign section of 1-probe-plans/README.md; Status board stays generated. Campaign is a HUMAN GATE like DRAFT — present and stop; the user's verb advances to "run".
260711 · `2.7.1`
      Changed (two-footed-bridge ruling, JL 2026-07-11; pairs with haipipe-probe 7.4.0)
      - `1-probe-plans/README.md` demoted everywhere it is mentioned (description, probe verb row, probe dispatch note) to a GENERATED index: the per-stage `_PROBE/` cards are the single source of truth; the index regenerates from cards + `_ASK` stubs + answering reports and is never hand-maintained; on disagreement, cards win.
260709 · `2.7.0`
      Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
      - Phase-verb pass-through documented in the routing table: trailing `draft|probe|revise|check` forwards through the lifecycle router to the stage skill; stage skills stop at their human gates and the user's verb advances them.
260708 · `2.6.0`
      Changed (venue lockfile wiring)
      - Venue coupling rule updated: venue stage compiles the pack into `0-lifecycle/2a-venue/2a-venue.md`; the venue-ALIGNED stages consult 2a-venue.md first, with direct `_venue/playbook-<venue>` reads demoted to fallback (2a-venue.md absent) or deep dives via its `[source: ...]` tags.
260704 · `2.5.0`
      Changed (probe-plan location unified, JL 2026-06-29 per-stage ruling wins over the flat buffer)
      - Probe plans live in per-stage `_PROBE/` folders; `1-probe-plans/README.md` is a thin cross-stage index (numbering authority). Verb line, dispatch note, evidence-path map, and fn/probe-plans.md all updated; PP statuses gain `read` (light probe returned, takeaways backfilled into the plan file). `_DISCOVERY_{stage}.md` retired.
      - Legacy layout migration rule (fn/probe-plans.md): flat 1-probe-plans/PPNN files move into their source_stage's _PROBE/ on first touch; legacy _DISCOVERY_ folds into the plan file + citation harvest, then deletes; the move is logged in the stage _LOG.
260703 · `2.4.1`
      Fixed
      - Marker rule tightened from "at most one 🔥 and one 🚀 per line" to EXACTLY one of each, never zero (live seed run rendered `draft 🔥` with no 🚀 anywhere). "Reached" defined as entered-not-completed, so a virgin paper's first phase renders `draft 🔥🚀`; a line with 🔥 but no 🚀 is a rendering defect.
260703 · `2.4.0`
      - create verb RETIRED, absorbed into enter as GET-OR-CREATE (JL: 直接去掉create，enter的时候没有就call create): a missing path CONFIRMS first (repo creation is outward-facing, never off a typo), then runs the same flow (org resolved per invocation, papers-inside recipe, folder scaffold, double-bump) and continues straight into the console. Verbs block, dispatch notes, examples, chooser, argument-hint updated; lifecycle + folder-skill + lifecycle-map cross-references repointed. The create flow itself is unchanged and was validated live (Paper-PhyPatSim run) before the re-homing.
260703 · `2.3.0`
      - stage-strip.sh moved from the shared-reference folder INTO this skill folder (co-located with the Closing Block spec it renders; JL: 为什么 strip 在 wiki 里有这里也有); all 8 references repointed, no strip content left outside this folder.
      - Resolved > JL: / > CC: comment threads archived below verbatim and removed from SKILL.md (comment lifecycle: working doc stays clean, resolved threads move to the log). Companion changes landed in their owners: 08-stage-gate.md Gate Modes (copilot|autopilot) + APPROVAL step + ledger Actor column + Stage Exit Invariant; haipipe-paper-check 1.4.0 (Gate Modes + invariant); haipipe-paper-probe 1.7.0 (From-buffer entry).
      ### Archived comment threads (verbatim)
      **@ Verbs / Dispatch notes**
      > CC: write/edit 的老路由目标 haipipe-paper-edit-write / edit-weaving 在重构后已不存在（对应能力并入 2-phase/2-revise workers，由 stage 内部调用）。我把 write/edit/polish 这些词全部路由到 section-edit stage 了，对吗？还是这组动词干脆退休不再出现在 Verbs 块里？
      > JL: 是的，旧词不要再出现了，省的误导
      > CC: 已退休全部旧词（write/edit/polish/draft/写初稿/整篇润色），section-edit 行只留 section-edit|section|sec|§N。
      > JL: 好，done
      **@ Closing Block (end every reply)**
      > JL: 这个应该有两层吧 一个是stage，一层是phase
      > JL: <--- 这里可以弄的再简单一些吗。比如paper root不要了，然后status和current layer放到一起。
      > JL: 我们是不是也有其他的file也在讲这个，要不把他调到这里，我们single source of truth
      > CC: 三条都已落：两层 strip（stage+phase）、tail 简化为 status·stage + next 两行、01-focus-strip-markers 语义并入本节并删除原文件（enter skill 的引用已改指这里），此节即唯一出处。
      > JL: 我想说你这个跟wiki里的strip的关系是什么，会冲突吗？
      > CC: 不再冲突：wiki 里剩的只是渲染脚本，现已把 10-stage-strip.sh 也搬进本 skill（./stage-strip.sh，与 spec 同住），8 处引用全部改指，wiki 里已无任何 strip 内容。
      **@ Gate-aware (Closing Block)**
      > JL: 你要想着我们有两个mode，一个co-pilot 在check phase的时候，人加上comments，一个是auto pilot，在check的时候，call一个subagent，然后让他给comments 你想想这个我们怎么做。但是是的，必须要有一个judgment，就是这个gate-aware，进入下一个stage要非常的明白，要有confirm，要有一个approval的动作（人或者代替人的subagent）
      > CC: 方案在 chat 里：CHECK 增加 mode=copilot|autopilot，autopilot 派 reviewer subagent 给 comments + approve/revise verdict，gate ledger 记 approval actor；你点头后我改 08-stage-gate.md + haipipe-paper-check。
      > JL: 可以的，你整吧。
      > CC: 已整：08-stage-gate.md 加 Gate Modes 节 + APPROVAL 步骤 + ledger 增 Actor 列；haipipe-paper-check 加 Gate Modes 节（autopilot 派 fresh reviewer subagent 落 > REVIEWER: comments + verdict；bibtex 等人类专属项标 DEFERRED 进 human queue，绝不静默放行）。
      **@ Composing with Evidence Workers**
      > CC: 原文这张图上游还列了 /idea-discovery /run-probe /auto-review-loop /result-to-claim 四个入口，skill 清单里已找不到，我删了。如果它们有新名字（或还想保留占位），告诉我补回。
      **@ Composing with Evidence Workers**
      > CC: 原文头部还有一处孤立引用（"读 lifecycle 参考时也读 ../1-lifecycle/haipipe-display-figure/SKILL.md"），看不出为什么单点名 figure 渲染器，我也删了。有特殊用途的话说一声。
      **@ Composing with Evidence Workers**
      > JL: 我们要不要把所有的wiki的内容也都移到这里来。然后随后把wiki的东西删掉。skill最好还是self-contained
      > CC: 建议不整体搬：共享 reference folder 本就在 paper 家族内部（家族级 self-contained），02/04/08/10 各有 5-10 个 skill 共用，搬进 umbrella 会让每次调用重新变胖；折中方案已执行 01-focus-strip-markers（并入本文件）+ 单消费者页可逐个并入唯一消费者，详见 chat。
      **@ Composing with Evidence Workers**
      > JL: 这个的话，我在想，还都是有haipipe-paper-probe 来进行probe calling？不要让haipipe-paper直接call了，他在一个stage的一个phase的阶段来call。
      > CC: 已改：umbrella 不再直连 /haipipe-probe，probe run 交给 haipipe-paper-probe（stage 的 PROBE phase worker）消费 1-probe-plans/ 再向下分发；Verbs 行、dispatch note、上图已同步。
      > JL: 好，再确认一下。
      > CC: 已确认并补齐另一端合同：haipipe-paper-probe 新增 "From-buffer entry" 节（from-buffer <paper_root> [PPNN]：读 planned 项 → reuse-before-create → 分发 /haipipe-probe → 回写 status/probe_ref → 返回 dispatch summary），两端调用签名一致。
260703 · `2.2.0`
      - JL in-file comment round applied (> JL: / > CC: threads kept in SKILL.md): (1) retired write/edit/polish/draft alias words entirely (省得误导); (2) closing block now TWO-LINE focus strip (stage + phase) with the simplified tail (status·stage merged, paper_root dropped, next only); (3) 01-focus-strip-markers ABSORBED into the Closing Block section as the single source of truth (file deleted; enter skill + 10-stage-strip.sh + the shared-reference index repointed; numbering gap kept); (4) umbrella no longer calls /haipipe-probe directly -- probe run hands 1-probe-plans/ to haipipe-paper-probe (the PROBE phase worker inside a stage's phase), composing diagram + dispatch note + description updated; (5) gate-aware line now names the two approval modes (copilot human / autopilot reviewer subagent), full design pending JL confirm (08-stage-gate.md + check skill).
260703 · `2.1.0`
      - Dedup rewrite (JL: "会有比较重复的地方吗", same treatment as discovery 2.6.0): say each thing ONCE. Command table + keyword map + positional aliases + Routing Step 2 (the same dispatch stated 4 times) merged into one Verbs block + one 6-rule Routing pass; feedback/digest full spec (written twice + fn/) reduced to one pointer section; create recipe (written twice + owner fn) reduced to one dispatch note; probe/venue-coupling/folder-tree/skill-tree restatements replaced by pointers to their owners (fn/probe-plans.md, 03-paper-lifecycle.md, paper-folder-anatomy.md, 06-paper-skill-structure.md). ~545 -> ~200 lines.
      - Stale fixes swept in: 2-claims -> 1-claims backfill refs; 3-narrative.tex -> .md; phantom top-level 2-section-edit/ dir removed from the skill tree (real homes: 1-lifecycle/5-section-edit + 2-phase/); write/edit rerouted to section-edit (old targets haipipe-paper-edit-write/-weaving no longer exist); stage list gained section-edit; "phase skills" wording corrected to stage skills (DPRC phases are internal); retired upstream workflow names dropped from the composing diagram.
      - Three open questions embedded as > CC: markers for JL review (write/edit verb fate, retired upstream workflow names, dropped display-figure reference).
260703 · `2.0.2`
      - create verb added to the front door (JL: should be /haipipe-paper create, not a sub-skill invocation): routes to haipipe-paper-lifecycle folder; repo-backed inside Project-* repos per project/haipipe-project/fn/repo-project.md papers-inside recipe; --org resolved per invocation (paper owner may differ from project owner). Retired prospectus verb/aliases removed (seed replaced it); haipipe-paper-bootstrap specialist entry replaced by haipipe-paper-folder; paper-folder contract tree fixed to current spine (1-claims, 2-pitch, 5-section-edit, .md early stages).
260703 · `2.0.1`
      - phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE; phase workers probe/ and revise/).
260622 · `2.0.0`
      - cross-cutting protocol wiring. All stage skills now reference ../1-lifecycle/ref/08-stage-gate.md (confirm-before-advance), ../1-lifecycle/ref/09-stage-illuminate.md (Socratic taste elicitation), 13-tex-quality.md (self-contained compilable tex), 12-evidence-routing.md (\needprobe macro + probe handoff). Stage strip end-of-reply convention enforced. Enter dashboard restructured (pitch summary first). 22 feedback items addressed.
260622 · `1.5.0`
      - probe buffer (1-probe-plans/). Claim-related evidence needs accumulate as probe plans during lifecycle work, then batch-dispatch to /haipipe-probe. Probe is the universal evidence gateway for claims; it calls task/discover during Gather. Direct task/discover verbs kept for non-claim utility work. See fn/probe-plans.md.
260622 · `1.4.0`
      - added probe/discover/task verbs as evidence-worker dispatchers. Paper orchestrator can now route directly to /haipipe-probe, /haipipe-discovery, /haipipe-task with project context resolved from the paper path. Paper stays story layer; evidence workers do the work.
260621 · `1.3.0`
      - renamed paper working-memory layer from feedback to rounds; added lifecycle, rounds, and skill-structure references.
260621 · `1.2.0`
      - made paper lifecycle the delivery-side owner of story/claims and routed GAP/NEED items through the shared delivery-need interface.
260621 · `1.1.0`
      - added enter/status paper-session loader routing.
260531 · `1.0.0`
      - baseline metadata added.

<!-- haipipe:skill:log:end -->
