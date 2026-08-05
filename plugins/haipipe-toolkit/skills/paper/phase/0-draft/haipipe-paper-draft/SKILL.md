---
name: haipipe-paper-draft
description: "DRAFT phase worker (internal). Called by a paper stage to produce the first-pass S-page artifact and raise every unresolved Q-consumer question. Reads that stage's stage.md and template, writes no probe entries, and opens no human gate unless stage.md explicitly declares draft in gates. Users invoke stage skills, not this skill directly."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill
metadata:
  version: "0.6.3"
  last_updated: "2026-08-04"
  summary: "Paper-specific DRAFT worker layered on haipipe-board-page-draft: define or reopen the stage promise, write first-pass Content, and raise owned Q-consumers."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-draft (internal phase worker)
====================================================

DRAFT phase worker.
Called by stage skills (seed, resource, claims, pitch, narrative, display, section-edit) to define the first round or reopen the promise of a mature artifact.
The stage defines WHAT the result looks like (its contract at `../../../1-lifecycle/haipipe-paper-stage/stages/<order>-<key>/stage.md`).
This skill defines HOW to get there.

**LOAD THE PAGE LAYERS FIRST:** `../../../../board/page-types/haipipe-board-page-for-stage/SKILL.md`, then `../../../../board/page-phases/haipipe-board-page-draft/SKILL.md`.
Those contracts own the Stage Page shape and DRAFT authority.
This file adds only manuscript and paper-stage knowledge.

**Not user-facing.**
Users invoke stage skills:
```
/haipipe-paper seed       → seed skill calls this internally for DRAFT phase
/haipipe-paper claims     → claims skill calls this internally for DRAFT phase
/haipipe-paper section-edit §3  → section-edit skill calls this internally
```


## Rules

The DRAFT authority lives in `haipipe-board-page-draft`.
`../../../../probe/haipipe-probe/SKILL.md` supplies the Q-consumer vocabulary and evidence-wall boundary only.
On a phase conflict, the Page Phase contract wins; paper-specific additions follow:
- **EVERY HOLE IS FILLED OR OWNED, EVERY STAGE.** A hole you cannot fill leaves a placeholder carrying the id of the S page's Q-consumer question that will settle it — `\cite{TOADD} [Q-<Stage>-<n>]`, `{VAL:? <what>} [Q-<Stage>-<n>]`. A placeholder with no bracket is a defect. PROBE later turns those questions into entries.
- **Citations**: grep the paper's `.bib` FIRST — real `\citep{key}` for hits, `\cite{TOADD} [Q-<Stage>-<n>]` where none fits. A key that does not grep is invented.
- **LOCAL answers**: DRAFT may cite paper-owned registries it has actually read, but it does not author `### bank binding`; that is PROBE's MATCH work.
- **RESOURCE stage**: write `Resource Description` under `## Content` and the logical `Q-consumer` records under `## Items to Finish` on `S-Work-0-resources.md`. DRAFT describes each resource and raises the questions; PROBE opens the entries, lands the answers, and writes their source pointers. `--depth`, supplied by the human, is the spend authorization.
- One sentence per line; no markdown tables in probe files.
- ⛔ **DRAFT DOES NOT TOUCH nested entries.** It raises Q-consumer rows in the direct topic page's `### Q-consumer register` and stops. Writing a `#### q-executor`, choosing a route, judging a bank, or setting a target is PROBE's ① and ②. (They ran here until 2026-07-20, purely so one human gate could review draft + plan together; stages now declare `gates: [check]`, so that reason is gone.)
- ⛔ **DRAFT OPENS NO GATE unless the stage's contract declares one.** Read `gates:` in `stage.md`. The default is `[check]` — in that case DRAFT ends by handing straight to PROBE, with no STOP.

The steps below are the HOW-TO for these rules.

## What DRAFT means

DRAFT = define or reopen WHAT the Page promises to say, **and what it cannot yet say**.
Two outputs, both on the owning S page: first-pass Content and the Q-consumer
questions that Content could not answer. PROBE plans and runs those questions.
A draft that does not know what it does not know is not a draft.
For argument docs (seed, claims, pitch, narrative) that means content decisions in working prose.
For SECTIONS it means a REAL draft — complete academic sentences close to submission register, with real `\citep{key}` citations for keys already in the paper's .bib and `{VAL:? <what>} [Q-<Stage>-<n>]` / `\cite{TOADD} [Q-<Stage>-<n>]` placeholders for everything unverified — because the user reviews structure by reading real prose, not a skeleton.
In both cases: content-complete, unverified, unpolished (polish is REVISE's job).

Each stage has its own contract (`../../../1-lifecycle/haipipe-paper-stage/stages/<order>-<key>/stage.md`) that defines:
- What files to produce
- What content structure to follow
- What done-criteria to meet
- Which phases and gates apply

DRAFT reads that spec and produces the artifact.


## The generic drafting process

Same process for every stage, different content:

### Step 1. Identify the stage and read its artifact spec + template

Determine which stage is being drafted, then read TWO files from that stage's own folder under
`../../../1-lifecycle/haipipe-paper-stage/stages/<order>-<key>/`:

```text
stage.md      the CONTRACT (YAML frontmatter: artifact path, sections, done_criteria,
              q_id_pattern, phases, exit_when) + the CRAFT prose for that stage
template.md   the canonical skeleton — section order, placeholders, inline <!-- RULE --> comments
```

This skill carries NO templates of its own — the stage owns its format.
Resolve the folder from `../../../1-lifecycle/haipipe-paper-stage/stages/index.yml`, which maps a
stage key to its `dir`. Do NOT hardcode the mapping here; that index is the one enumerating file.

```text
seed          -> stages/0-seed/
resource      -> stages/1a-resource/
claims        -> stages/1b-claims/
venue         -> stages/2a-venue/
pitch         -> stages/2b-pitch/
narrative     -> stages/3-narrative/
display       -> stages/4-display/
section-edit  -> stages/5-section-edit/     (a section NAME, e.g. `introduction`, routes here)
```

Some stages carry EXTRA support files in the same folder; read them when the contract's
`support:` field names them. They are NOT uniform — `2b-pitch/readability.md`,
`4-display/figure-logic.md` + `checklist.md`. section-edit has none — its template is its own rulebook. Never assume a
file exists because a sibling stage has one.

⚠️ The `phases:` field in `stage.md` is AUTHORITATIVE and is not always four. `venue` declares
`[draft, probe, check]` — it has no REVISE. Run what the stage declares.

### Step 2. Consult upstream artifacts

Each stage reads from its predecessors:

| Drafting... | Read upstream |
|---|---|
| seed | nothing (seed is the root) |
| resource | Seed S page (Tentative Claim Shape + its `## Log` forward pointers) |
| claims | seed + resource |
| pitch | seed + claims + venue |
| narrative | seed + claims + pitch |
| display | narrative + claims |
| section | narrative + claims + section-type + `S-Venue-0-venue.md` |

**Venue guard.**
For venue-ALIGNED stages (pitch, narrative, display, section), resolve the venue before drafting:

1. No `venue:` pinned in `S-Venue-0-venue.md` -> **STOP with an error**.
   Report `status: blocked` and tell the user to run `/haipipe-paper venue` first.
   Never draft a venue-ALIGNED artifact against an invented venue.
2. Venue pinned and the paper's `0-lifecycle/2-venue/S-Venue-0-venue.md` exists -> **read it FIRST**: Writing Principles + the Structural Blueprint block for the artifact being drafted.
   Direct `venue/` pack reads are deep dives only, following the `[source: ...]` tags recorded there.
3. `S-Venue-0-venue.md` absent (venue stage not run) -> fall back to the pinned pack directly.
   No matching `venue/playbook-*` pack either -> **STOP with an error**.
   Name the pinned venue, list available packs, ask the user to fix the pin, add a pack, or run `/haipipe-paper venue`.
4. Fallback pack exists but lacks the per-section style file -> **proceed with a visible warning**: use the pack's general style-profile, record the missing file in the S page's `## Items to Finish` and `## Log`, and surface it again in CHECK.
   Never silently invent word budgets or structure norms.

Venue-FREE stages (seed, resource and claims) skip this guard entirely.

### Step 3. Settle structure

Present the structural plan to the user before writing content:
- **seed**: four Content divisions (Seed Question, Motivations, Landscape, Tentative Claim Shape) plus Q-consumer records in Items to Finish
- **resource**: `Resource Description` in Content (one `### Resource <n>` division, closing on `#### Serves & carries`) plus one `Q-Resource-<n>` record per unresolved existence/fitness question in Items to Finish
- **claims**: the hypothesis list and claim matrix in Content plus Q-consumer records in Items to Finish
- **pitch**: the cover letter divisions in Content plus Q-consumer records in Items to Finish
- **narrative**: the section blocks/story beats in Content plus Q-consumer records in Items to Finish
- **display**: the figure/table inventory in Content plus the Q-consumer records it implies in Items to Finish
- **section**: the paragraph skeleton/prose in Content plus Q-consumer records in Items to Finish

The stage template must declare the logical `Q-consumer` division.
On a Board-first paper S page, `create-page.py` and DRAFT materialize that
division only as recognizable checklist records under `## Items to Finish`;
they never add a literal `Q-consumer` block under `## Content`.

### Step 4. Draft content

Fill in the structure with first-pass content:
- Write to settle WHAT is being said, not HOW it sounds
- Argument docs: working prose.
  Sections: REAL prose per the stage's template (`stages/5-section-edit/template.md`, which carries its own fill rules) — complete sentences, one per line, blank line between
- Citations real, never guessed: grep the paper's .bib FIRST and write `\citep{key}` for keys that exist; `\cite{TOADD} [Q-<Stage>-<n>]` where no key fits; `{VAL:? <what>} [Q-<Stage>-<n>]` for unverified numbers.
  A key that does not grep in .bib is an invented citation.
- Never invent a number or citation to avoid a placeholder
- One idea per sentence

**Inline WebSearch/WebFetch is ALLOWED here -- as drafting fuel, NOT as evidence.**
DRAFT may search the web to orient (is this field crowded? does a dataset exist? who are the anchor names?) and to sharpen the draft.
But a seed is allowed to be intuition (seed principle 1), so what that search produces has exactly two legal destinations:
1. **PROSE** in the stage artifact (Motivations, Claim Shape, ...) -- phrased as orientation, with `\cite{TOADD} [Q-<Stage>-<n>]` slots, never as settled fact. Anything load-bearing stays a raised question.
2. **A RAISED QUESTION** -- a gap the search reveals goes through Step 4b like any other, with no special status.

FORBIDDEN in DRAFT: opening or editing a nested entry page, writing a
`#### a-executor`, or treating an inline result as landed evidence.
Real evidence lands ONLY via the PROBE phase dispatching `haipipe-paper-probe` (the single door); inline search results bind to nothing -- evidence gathered any other way means "the PROBE phase did not happen."
`check-probe-cards.sh` runs after PROBE and again at CHECK, not here, because
DRAFT has not created entries yet.

### Step 4a. 🕳️ SWEEP THE HOLES — dispatch the three lanes

Prose written: sweep it for what it could not fill. Each lane knows its own kind of hole and how to check for it. They are READ-ONLY checkers — they report, they never write — so all three can run in one batch:

```text
Skill("haipipe-paper-draft-citation", args="<stage-or-section> <paper-path>")
Skill("haipipe-paper-draft-values",   args="<stage-or-section> <paper-path>")
Skill("haipipe-paper-draft-display",  args="<stage-or-section> <paper-path>")
```

Each RETURNS a report — for every hole: WHERE it is (the sentence), WHAT it is (`\cite{TOADD}` / `{VAL:? <what>}` / a DR row), and WHO owes it (the existing `Q-<Stage>-<n>` that will produce it, or `UNOWNED` if nothing will).

**THIS HUB HOLDS THE PEN — for all of it.** The lanes do not touch the manuscript, the topic register, or nested entry pages. THIS worker takes the three reports and writes:

```
draft.md · prose        this hub, from the lane reports — insert each placeholder
                        with its [Q-<Stage>-<n>]
draft.md · Q-consumer   this hub, at Step 4b
```

One writer per file. Two lanes editing the same prose is a write race. The
display lane may write only its declared display inbox; it never writes the S
page or probe entries.

Skip a lane only when the artifact cannot carry its kind of hole (a seed has no numbers; a pitch has no displays), and log the skip.

### Step 4b. 🙋 RAISE — every question this draft cannot answer

**DRAFT is where the questions are BORN — and only born.** Raise each Q-consumer row under the direct topic page's `### Q-consumer register`, in the consumer's own words, with its paper stake and an empty entry link or return note, then STOP. Planning them (①ORGANIZE, ②MATCH) is PROBE's; see probe's phase map. This skill never opens a nested entry page.

This step is UNCONDITIONAL. It runs on every draft, whatever the question's origin: a hole Step 4a's lanes returned unowned, a question the stage typically raises (see the calling stage's `dispatch_scope:` + craft body), a gap a web search revealed, or one you simply noticed while writing.

Each question gets one DRAFT artifact: a `## Q-<Stage>-<n>` block in the S
page's Q-consumer, in the consumer's own words and carrying the STAKE. Cite its
id inline on every sentence that hangs on it. Stop at that boundary: PROBE
finds or opens the corresponding entry, strips the stake from `q-executor`,
authors the bank binding, and runs the five-step loop. Asking is cheap; the
`--depth` ceiling controls which questions may incur work.

### Step 4c. 🤖 SELF-REVIEW — check the draft before handoff

Verify mechanically that every `\cite{TOADD}` and `{VAL:?}` has a
`[Q-<Stage>-<n>]` owner and every owner resolves to a Q-consumer block in the S
page. RUN IT, do not eyeball it (JL 260801):

```text
python3 <skills>/writing/haipipe-writing/cli/holes.py <stage-doc> --dialect paper
```

It checks both directions, and the second one is the one a reader misses: a hole
carrying `[Q-Main-9]` when no `Q-Main-9` exists LOOKS owned, so nobody ever goes
looking for it. The discipline behind the check is
`writing/haipipe-writing/ref/holes.md`; the notation, the `.bib` grep, and the
topic-entry boundary stays here, because none of those generalize. Do not run the probe-entry checker yet: no entries should exist from this
phase. The sub-agent's job is semantic judgment — whether the draft says
something, follows the stage contract, and raises answerable questions.

Then, the CREATOR/REVIEWER split, so the drafter does not grade its own work. Dispatch a review sub-agent in a FRESH context (report-only; the drafter applies the fixes):

```text
Agent(general-purpose, prompt="
  Review this DRAFT phase output against the checklist. Report PASS or a numbered issue list
  (file + line + what's wrong + the fix). Do NOT edit anything — only report.

  READ:
    - the stage draft (the stage doc this run wrote/updated)
    - the calling stage's artifact spec, and probe's 'The DRAFT self-review checklist' at
      Tools/plugins/haipipe-toolkit/skills/probe/haipipe-probe/SKILL.md (repo-root-relative —
      you resolve from the repo root, not from the calling skill's folder)

  Surface A — the draft, vs the stage's artifact spec:
    - every section filled with REAL content (no unmarked placeholders)
    - one sentence per line; every \citep{} key is REAL (grep the .bib);
      gaps use {VAL:? <what>} [Q-<Stage>-<n>] / \cite{TOADD} [Q-<Stage>-<n>]
    - every Q-<Stage>-<n> is cited inline [Q-<Stage>-<n>] on the sentence it hangs on
    - COMPLETENESS, the reverse direction: every {VAL:?} and every \cite{TOADD} carries a
      [Q-<Stage>-<n>] naming a question that exists in the stage doc. A placeholder with no
      bracket is a defect — nobody owns it, so nobody will ever fill it. Either it gets a
      question or it is explicitly declined in the S page's ## Log.
    - each raised question is specific, answerable, and preserves the consumer's stake
")
```

Issues → FIX them, then re-run the review (bounded: at most 2 rounds). A
third-round residual goes into `## Items to Finish` for CHECK; never hide it.

### Step 5. Record and hand back to the stage router

Write a `[DRAFT]` summary in the owning S page's `## Log`: artifact changed,
questions raised, lanes run/skipped, and self-review verdict. Do not mark the S
page `✅`; only CHECK approval does that.

If `stage.md` includes `draft` in `gates:`, present the draft and wait. Otherwise
return immediately to the stage router, which invokes the next declared phase
(normally PROBE). Active comment threads remain inline until the user resolves
them; resolved threads move verbatim to the owning S page's `## Log`.


## Stage-specific notes

### seed
- Output: `0-lifecycle/0-seed/S-Seed-0-seed.md`
- WebSearch-to-orient: see Step 4 (the one normative home).
- Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/0-seed/stage.md` -> its `dispatch_scope:` + the craft body (the stage owns its own list; this file never restates it).
  Profiling OUR OWN data is RESOURCE-stage task work; register it as a `[FORWARD -> RESOURCE]` pointer in the Seed S page's `## Log`, do not raise it in seed.
  The RESOURCE stage is the SOLE CONSUMER of these pointers and takes them at its open (reader clause in the resource stage contract) -- an unconsumed pointer fails the RESOURCE done-criteria, not claims'.
- Short document, FIVE sections: Seed Question + Motivations + Landscape + Tentative Claim Shape + Q-consumer (Landscape and Q-consumer are not optional — the `[Q-Seed-<n>]` anchor loop hangs on Q-consumer)

### resource
- Output: `0-lifecycle/1-work/S-Work-0-resources.md`; template `template.md` (in stages/1a-resource/)
- Venue-FREE, and it sits BETWEEN seed and claims — it is stage 1a, just before claims (1b) on disk (precedented by `2a-venue/` + `2b-pitch/`).
  Nothing renumbers.
- EXACTLY TWO LOGICAL OUTPUTS: **Resource Description** in `## Content` and **Q-consumer** records in `## Items to Finish`.
  `Resource Description` has one `### Resource <n> · <name>` division per dataset, reusable model/pipeline, or producing-code resource, with `####` topic paragraphs and a closing `#### Serves & carries` naming the `H<n>` it serves and whether it carries or kills that hypothesis.
  `Q-consumer` has one checklist record per unresolved existence/fitness question, titled `Q-Resource-<n> · <title>` and carrying `Description`, `Reason`, `Probe`, and an empty `Answer` that PROBE later fills with existence, fitness, what it kills, and `[source: PP<NN>]`.
  NO Kill Conditions, NO Setup Contract, NO parallel resource ledger, NO binding table.
- On open: consume the seed's forward pointers from `S-Seed-0-seed.md`'s `## Log`.
  The grep MUST be GLYPH- AND LEGACY-TOLERANT — the live pointers on disk all say "CLAIMS" (this stage did not exist when they were written) and at least one uses a UNICODE arrow.
  Match `grep -E "\[FORWARD (->|→) (RESOURCE|CLAIMS)\]"`.
  Each pointer is consumed into the relevant resource description/topic and, where evidence is still needed, an owned `Q-Resource-<n>` block; otherwise it is explicitly DECLINED in the Resource S page's `## Log` with its reason.
  A CLAIM-STATUS pointer is not ours — leave it for claims and say so.
- The stage ASKS; it never mints a PP id, never picks a probe type or topic, and never executes (no `/haipipe-data`, `/haipipe-nn`, `/haipipe-task`, no inline store scan).
  WebSearch/glob to ORIENT is legal DRAFT fuel per Step 4 — it never lands in an `A`.
- Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/1a-resource/stage.md` -> its `probe_lanes:` + the craft body.
- PROBE (resource): one `Skill("haipipe-paper-probe", ...)` call. The worker
  authors/matches entries, dispatches only within `--depth`, and lands each Q's
  `A`. There is no DRAFT gate or `_LOG` sidecar.

### claims
- Output: `0-lifecycle/1-work/S-Work-1-claims.md`
- On open: do not re-consume Seed forward pointers. Read the Resource S page and
  its `## Log`; only pointers it explicitly declined to Claims enter this
  Q-consumer.
- Reads `S-Work-0-resources.md`: ingredients are settled there; training and
  evaluation belong to Claims.
- Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/1b-claims/stage.md` -> its `dispatch_scope:` + the craft body.
- Hypotheses are venue-neutral (H1, H2, H3)

### pitch
- Output: `0-lifecycle/2-venue/S-Venue-1-pitch.md`
- Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/2b-pitch/stage.md` -> its `dispatch_scope:` + the craft body.
- Venue-ALIGNED: reads `S-Venue-0-venue.md` (pack fallback per the venue guard)

### narrative
- Output: `0-lifecycle/2-venue/S-Venue-2-narrative.md`
- Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/3-narrative/stage.md` -> its `dispatch_scope:` + the craft body.
- Section-mirrored story with readiness tags

### display
- Resolve the current output from `stages/4-display/stage.md`; do not invent a replacement while its declared `blocked_on` remains open.
- DRAFT runs the stage's step-0 reconcile first (legacy probes/preview/tex-comments merge), then authors the md: Venue Set, Display Map, PROBE PLAN (S0/En/Rn rows, ▶ ready / ✋ gated-on-thread), one block per display with method candidates + ASCII sketch
- Open threads stay inline for CHECK; DRAFT proposes and PROBE executes within its ceiling.
- Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/4-display/stage.md` -> its `dispatch_scope:` + the craft body (the cross-stage coverage sweep is DRAFT's, not PROBE's)
- PROBE: evidence lane (tasks) + render lane (renderer skills, candidate mode) over the approved plan rows

### section-edit
- Output: the resolved Main/Appendix S page declared by the dynamic stage identity.
- Format: REAL prose per `stages/5-section-edit/template.md` (shape + rules in one file)
- Ends with the Q-consumer block: every placeholder has an owning question.
  DRAFT proposes; PROBE later binds each one to an answer.
- Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/5-section-edit/stage.md` -> its `dispatch_scope:` + the craft body.
  (citation / values / display are DRAFT's Step 4a lanes, not PROBE tracks.)
- Reads section-type norms and `S-Venue-0-venue.md`'s per-section blueprint block for style


## Where style guidance lives (NOT here)

DRAFT settles content, not style.
Style inputs come from elsewhere:

| Guidance | Lives in | Used by |
|---|---|---|
| Venue style, word budget, arc | `0-lifecycle/2-venue/S-Venue-0-venue.md` (compiled from `venue/playbook-<pack>/`; pack = fallback / deep dive) | DRAFT reads budget; REVISE applies style |
| Per-section structure norms | the paper's `S-Venue-0-venue.md` blueprint block (BINDING), deep dive `paper/venue/playbook-*/<journal>/<journal>-<kind>/style.md` (reference) | DRAFT (structure) |
| Prose quality rules | `../../REF/prose-quality.md` | REVISE |

Old venue LaTeX templates and the write-conference/scientific/systems style skills were archived to the paper-root `_archive/` (venue knowledge belongs in `venue/` packs).


## Relation to other phases

```
DRAFT (this)  →  PROBE   →  REVISE if declared  →  CHECK
settle WHAT       collect     settle     verify
to say            evidence    HOW to     everything
                              say it
```

DRAFT produces or redefines the artifact promise for one round.
If the purpose or Aims are wrong, return to DRAFT and begin a new round.
If the promise stands but its realization is weak, use REVISE.


## Who calls this skill

Stage skills call this as their DRAFT phase:

| Stage skill | What this skill drafts |
|---|---|
| seed | S-Seed-0-seed.md (5 sections) |
| resource | S-Work-0-resources.md (`Resource Description` + `Q-consumer`; PROBE later lands each Answer) |
| claims | S-Work-1-claims.md (hypothesis list + evidence matrix) |
| pitch | S-Venue-1-pitch.md (cover letter) |
| narrative | S-Venue-2-narrative.md (story beats) |
| display | the artifact declared by display/stage.md (currently blocker-aware) |
| section-edit | resolved Main/Appendix S page |

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT (this) | haipipe-paper-draft + `-citation` / `-values` / `-display` lanes | -- |
| PROBE | haipipe-paper-probe | DRAFT |
| REVISE | haipipe-paper-revise | PROBE, when declared |
| CHECK | haipipe-paper-check | the previous declared phase |

## Return contract

```
status:    ok | blocked
stage:     <stage-name>
artifact:  <path written>
questions: <count raised this run>
raised:    <one line per raised Q-consumer id + question; or "none">
review:    <the Step 4c self-review verdict, incl. any residual>
next:      the next phase declared by stage.md (normally PROBE)
```
