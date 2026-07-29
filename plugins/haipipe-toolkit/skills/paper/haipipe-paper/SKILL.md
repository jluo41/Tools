---
name: haipipe-paper
description: "Run any paper-lifecycle work: parse intent (venue + stage) and route to the stage specialists. Each stage runs the ordered phases declared by its stage.md and stops only at its declared gates; evidence enters ONLY through PROBE, which turns the S page's Q-consumer questions into probe entries and runs them through clean agents. `enter`/`status` open the paper's first-class Board. Trigger: paper, enter paper, paper status, venue, seed, resource, claims, pitch, narrative, display, section-edit, round, rebuttal, probe, evidence, 写论文, 论文流程, /haipipe-paper."
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "0.4.5"
  last_updated: "2026-07-27"
  summary: "Front door for the Board-first paper lifecycle. Each stage runs the phases and gates declared by its stage.md; current stages use one CHECK gate, and Venue intentionally omits REVISE. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

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
build | scaffold | restructure | conform | folder |
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

Gate-aware: closing a stage and advancing to the next requires an EXPLICIT approval action that the current stage is done (Stage Gate, `../1-lifecycle/ref/08-stage-gate.md`) -- by the human (copilot mode) or by a reviewer subagent standing in for the human (autopilot mode); once the S page carries the gate ledger, ✅ means "approved", and the ledger records who approved (human or agent).


Comment lifecycle
------------------

THE single source of truth for inline comments across ALL paper skills. Every phase worker, lifecycle stage, and orchestrator follows this convention.

**Loaded-context rule.** This section is not in context at every skill
invocation, so it cannot bind behavior by itself. Every skill that touches
working files must INLINE its binding subset: never delete/reword `> USER:`;
reply `> CC:` underneath; only the user resolves; move resolved threads
verbatim into the owning S page's `## Log`; make surgical edits only. The stage
hubs carry that block as "Comment rules (binding)".

### Actor ids

The `{...}` token names **who** authored that line. Keep it short. One flat namespace:

| Kind | Examples | Note |
|------|----------|------|
| AI tool / agent | `CC` (Claude Code), `GPT`, `GEM` (Gemini), `CDX` (Codex) | reviewing tools; append `-<topic>` on findings |
| Person | initials (`AU`, `CO1`, etc.) | authors / coauthors |
| Role | `R1`, `R2`, `AC`, `ED` | numbered reviewers, area chair, editor |

**The human actor id is asked, never assumed.** At the start of a cycle the skill asks the user for their initials (and the pass date `vMMDD`). Never default to any specific initials.

### Two comment formats

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

### The two marks (tex format)

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

### Anchoring (tex files)

A comment sits on its **own line, directly below the text it refers to**:

```latex
Agreeableness showed the strongest positive correlation ($r = 0.62$).
%% {CC-values-v0531}: 0.62 here vs 0.747 in the table. | Reconcile. ========>
```

For wrapped paragraphs, use `@"quote"` to anchor: `%% {CC-content-v0531}: @"we next examined" opener is throat-clearing. | Start with the finding.`

### The lifecycle

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

### S-page `## Log` format

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

### REVISE phase: no comment-first

REVISE is the exception. REVISE workers apply changes directly (no comment-first round). They leave `%% {CC-<worker>}: <why>` comments explaining non-trivial changes. These comments are for CHECK to review, not for a human reply cycle. The human reviews in CHECK and can add `> USER:` comments to restart REVISE.

### Round invariants (tex comment-first, when used)

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

### How paper talks to probe

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

### When to record a need

Only when the problem is EVIDENCE, not wording. A wording/structure problem loops back inside the paper lifecycle (1-claims / 2-pitch / 3-narrative / 4-display / 5-section-edit). A need leaves the paper for an evidence worker.

```
paper GAP -> a Q-consumer in the stage doc -> PROBE opens a question ENTRY in
1-probes/ and MATCHes it -> PROBE DISPATCHes only what MATCH could not close -> the
answering QA file -> the entry's `### a-executor` -> each Q-consumer's a-consumer ->
the paper backfills (the claim's status flips in S-Work-1-claims.md)
```

Do NOT route through a project-level narrative layer (there isn't one).

### Routes

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

### Need record

Each open need is one row on its owning Board/S page; claim needs live on `0-lifecycle/1-work/S-Work-1-claims.md`:

```
need_id      stable handle (e.g. N1, tied to a claim slot C2 or a display)
gap          which claim slot / display / section has the gap
kind         evidence | context | artifact | meaning
route        the command above
state        open | commissioned | returned      (mirrors the probe entry's derived state)
backfill     the slot/display to update when the worker returns
```

### Backfill (the return direction)

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

### Autonomous drain (the "keep going" loop)

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

### The `\needprobe{}` macro

When a claim lacks evidence, mark it in the `.tex` with a visible red caveat:

```latex
\newcommand{\needprobe}[1]{\textcolor{red}{\textbf{[NEED PROBE]} #1}}
```

Add this macro to the lifecycle preamble (or the paper's shared command file). Use it inline wherever the gap lives:

```latex
\needprobe{Is the intensive margin about patients already on opioids?}
```

The red flag renders in the compiled PDF so the gap is obvious to every coauthor. Remove it when the answer lands (the entry's `**target**` resolves and its `### a-executor` is written) and the claim is backfilled with supported text.

### Handoff protocol

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

### The `probe` verb

```
/haipipe-paper probe <need-description>
```

opens a `## QX<n>` ENTRY in the right topic's probe file at `1-probes/`. The stage's PROBE phase (`haipipe-paper-probe`) is what dispatches it — through `Agent(haipipe-probe-q-executor-agent)` to `Agent(haipipe-task-orchestrator-agent)` or `Agent(haipipe-discovery-orchestrator-agent)`, carrying the entry's `### q-executor` block and nothing else. The paper stays a story layer; the executor does the work.

### Heavy probes and subagent dispatch

When a probe requires reading a lot of code/logs (e.g. cohort construction from Stata do-files), dispatch it to a BACKGROUND SUBAGENT so the main paper session keeps doing paper work:

```
a. Add a beat to narrative/Methods for the topic (e.g. "Cohort construction"),
   marked \needprobe{} until the report lands.
b. Raise the question ENTRY (/haipipe-paper probe "<need>"), then let the PROBE
   phase dispatch its `### q-executor` with run_in_background=true.
c. When the subagent report returns, fold it into Methods + Table 1 and flip the
   beat from \needprobe{} to supported.
```

### Construction as a first-class beat

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
