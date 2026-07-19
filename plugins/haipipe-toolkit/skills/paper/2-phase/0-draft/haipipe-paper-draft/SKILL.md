---
name: haipipe-paper-draft
description: "DRAFT phase worker (internal). Called by stage skills to produce the first-pass artifact. Reads the stage's artifact spec (from 1-lifecycle/) to know WHAT the result should look like, then runs the generic drafting process: consult upstream → settle structure → draft content → iterate with user → confirm. Users invoke stage skills (seed, claims, pitch...), not this skill directly."
argument-hint: "[stage-or-section] [paper-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
metadata:
  version: "4.3.0"
  last_updated: "2026-07-19"
  summary: "DRAFT phase worker (internal): produce the first-pass artifact for any stage -- consult upstream, settle structure, draft real prose per the stage's template ({VAL:?} placeholders, real \\citep{} keys from the .bib), iterate with the user, then SELF-REVIEW the draft + probe plan via a fresh-context sub-agent before the STOP gate. Inline WebSearch is drafting fuel only, never durable evidence. Raises what it cannot answer as question SECTIONS in 1-probes/ AND authors their probe plan (q-executor + route + match + target — DRAFT runs the loop's ①ORGANIZE + ②MATCH); never writes an answer (a-consumer) into one. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-draft (internal phase worker)
====================================================

DRAFT phase worker.
Called by stage skills (seed, resource, claims, pitch, narrative, display, section-edit) to produce the first-pass artifact.
The stage defines WHAT the result looks like (artifact spec in `1-lifecycle/`).
This skill defines HOW to get there.

**Not user-facing.**
Users invoke stage skills:
```
/haipipe-paper seed       → seed skill calls this internally for DRAFT phase
/haipipe-paper claims     → claims skill calls this internally for DRAFT phase
/haipipe-paper section-edit §3  → section-edit skill calls this internally
```


## Rules (follow these — the model is haipipe-probe's)

The DRAFT-phase rules live in the constitution: `../../../../probe/haipipe-probe/SKILL.md` → **Phase rules · DRAFT phase** + **The DRAFT self-review checklist**. Follow those; on conflict, that file wins. Paper-specific additions:
- **Citations**: grep the paper's `.bib` (+ `_CITATION_`) FIRST — real `\citep{key}` for hits, `\cite{TOADD}` (+ a `_CITATION_` row) where none fits, `{VAL:? <what>}` for unverified numbers. A key that does not grep is invented.
- **T1 LOCAL**: a question answered by the paper's OWN registries (`_CITATION_*` / `_VALUES_*` / `_EVIDENCE_*` / `read` sections / `0-displays/` / `.bib`) roots `match:` there, marked `answered-local` (no bank dispatch). A display-shaped need reroutes to `0-lifecycle/4-display/_DISPLAY_REQUEST.md`.
- **RESOURCE stage**: read `1a-resource.md`'s GATE-1-approved `Q<n>`, open one `serves: resource` section each, and write the `-> PP<NN>` backlink into `1a-resource.md`.
- One sentence per line; no markdown tables in probe files.

The steps below are the HOW-TO for these rules.

## What DRAFT means

DRAFT = settle WHAT to say.
The first pass at producing a stage's artifact.
For argument docs (seed, claims, pitch, narrative) that means content decisions in working prose.
For SECTIONS it means a REAL draft — complete academic sentences close to submission register, with real `\citep{key}` citations for keys already in the paper's .bib and `{VAL:?}` / `\cite{TOADD}` placeholders for everything unverified — because the user reviews structure by reading real prose, not a skeleton.
In both cases: content-complete, unverified, unpolished (polish is REVISE's job).

Each stage has its own artifact spec (in `1-lifecycle/{stage}/haipipe-paper-{stage}/SKILL.md`) that defines:
- What files to produce
- What content structure to follow
- What done-criteria to meet
- Which DPRC phases apply

DRAFT reads that spec and produces the artifact.


## The generic drafting process

Same process for every stage, different content:

### Step 1. Identify the stage and read its artifact spec + template

Determine which stage is being drafted, then read TWO things from `1-lifecycle/`: the stage's SKILL.md artifact spec (WHAT to produce, done-criteria) and the stage's canonical template (section order, placeholders).
This skill carries NO templates of its own -- the stage owns its format.

| Stage | Artifact spec | Template |
|---|---|---|
| seed | `1-lifecycle/0-seed/haipipe-paper-seed/SKILL.md` | `ref/seed-template.md` |
| resource | `1-lifecycle/1a-resource/haipipe-paper-resource/SKILL.md` | `ref/resource-template.md` |
| claims | `1-lifecycle/1b-claims/haipipe-paper-claims/SKILL.md` | `ref/claims-template.md` |
| pitch | `1-lifecycle/2b-pitch/haipipe-paper-pitch/SKILL.md` | `ref/pitch-template.md` |
| narrative | `1-lifecycle/3-narrative/haipipe-paper-narrative/SKILL.md` | `ref/narrative-template.md` |
| display | `1-lifecycle/4-display/haipipe-paper-display/SKILL.md` | `ref/display-template.md` (unit contracts live in the same `ref/`) |
| section name (e.g. `introduction`) | `1-lifecycle/5-section-edit/haipipe-paper-section-edit/SKILL.md` | `ref/outline-format.md` |

(Template paths are relative to each stage skill's OWN folder — the same folder as its SKILL.md, e.g. `1-lifecycle/0-seed/haipipe-paper-seed/ref/seed-template.md`.)

### Step 2. Consult upstream artifacts

Each stage reads from its predecessors:

| Drafting... | Read upstream |
|---|---|
| seed | nothing (seed is the root) |
| resource | seed (Tentative Claim Shape + `_LOG_0-seed.md` forward pointers) |
| claims | seed + resource |
| pitch | seed + claims + venue |
| narrative | seed + claims + pitch |
| display | narrative + claims |
| section | z-structure + narrative + claims + section-type + venue (2a-venue.md) |

**Venue guard.**
For venue-ALIGNED stages (pitch, narrative, display, section), resolve the venue before drafting:

1. No `venue:` pinned in STATUS.md -> **STOP with an error**.
   Report `status: blocked` and tell the user to run `/haipipe-paper venue` first.
   Never draft a venue-ALIGNED artifact against an invented venue.
2. Venue pinned and the paper's `0-lifecycle/2a-venue/2a-venue.md` exists -> **read it FIRST** (the venue stage's compiled doc): Writing Principles + the Structural Blueprint block for the artifact being drafted.
   Direct `venue/` pack reads are deep dives only, following the `[source: ...]` tags recorded there.
3. `2a-venue.md` absent (venue stage not run) -> fall back to the pinned pack directly.
   No matching `venue/playbook-*` pack either -> **STOP with an error**.
   Name the pinned venue, list available packs, ask the user to fix the pin, add a pack, or run `/haipipe-paper venue`.
4. Fallback pack exists but lacks the per-section style file -> **proceed with a visible warning**: use the pack's general style-profile, flag the missing file in the draft output and `_LOG`, and surface it again in the CHECK report.
   Never silently invent word budgets or structure norms.

Venue-FREE stages (seed, resource and claims) skip this guard entirely.

### Step 3. Settle structure

Present the structural plan to the user before writing content:
- **seed**: the three sections (question, motivations, claim shape)
- **resource**: the two sections — the Demand rows (one `N<n>` per hypothesis) and the Questions (`Q<n>` + its `A`); nothing else
- **claims**: the hypothesis list and claim matrix layout
- **pitch**: the cover letter sections (hook, finding, so-what, editor's chair)
- **narrative**: the section blocks and story beats
- **display**: the figure/table inventory (+ the Probes rows it implies)
- **section**: the paragraph skeleton (how many subsections, how many paragraphs, what job each does)

### Step 4. Draft content

Fill in the structure with first-pass content:
- Write to settle WHAT is being said, not HOW it sounds
- Argument docs: working prose.
  Sections: REAL prose per the stage's template (`ref/outline-format.md`) — complete sentences, one per line, blank line between
- Citations real, never guessed: grep the paper's .bib (and `_CITATION_`) FIRST and write `\citep{key}` for keys that exist; `\cite{TOADD}` (+ a `_CITATION_` row naming the topic) where no key fits; `{VAL:? <what>}` for unverified numbers.
  A key that does not grep in .bib is an invented citation
- Never invent a number or citation to avoid a placeholder
- One idea per sentence

**Inline WebSearch is ALLOWED here -- as drafting fuel, NOT as evidence.**
DRAFT may search the web to orient (is this field crowded? does a dataset exist? who are the anchor names?) and to sharpen the draft.
But a seed is allowed to be intuition (seed principle 1), so what that search produces has exactly two legal destinations:
1. **PROSE** in the stage artifact (Motivations, Claim Shape, ...) -- phrased as orientation, with `\cite{TOADD}` slots, never as settled fact.
2. **RAISED QUESTIONS + THEIR PLAN** -- when the search reveals a gap the paper must later verify, RAISE IT AS A QUESTION and PLAN it.
   **DRAFT is where the questions are born AND planned** — the probe plan is authored here, beside the draft, so ONE gate reviews both (see the probe constitution's PHASE MAP: ①ORGANIZE + ②MATCH run at DRAFT).
   For each one, write a SECTION in the right topic's probe file at `1-probes/PPNN_<topic>.md` + a Status board row, per `../../../haipipe-paper/fn/probes.md`, carrying the full plan:
   - `q-executor:` — the question in GENERAL language (no claim ids, no stake, no hint of which answer is wanted); NEVER write the `## Why` into a q-executor — the stake never leaves the probe file.
   - `route:` — the dispatch door, `task | discovery` (AUTHORITATIVE).
   - `match:` — root it to a SPECIFIC bank folder (a read-only bank grep is legal — LAW 1 bans the pen and the run, not the eye): `EXISTS · <folder>` (→ link) or `NONE → propose NEW <folder>`.
   - `target:` — the existing QA path (EXISTS) or `NEW <path>` (NONE).
   This HANDS the plan to the PROBE phase, which RUNS IT FORWARD (③ dispatch the `NEW` ones, ⑤ harvest); it does not answer it here.

FORBIDDEN in DRAFT: writing an `a-consumer:` (the ANSWER — that is PROBE's ⑤ harvest), or treating an inline result as landed evidence.
Inline search results bind to nothing -- evidence gathered any way other than the PROBE phase's dispatch means "the PROBE phase did not happen."
The DRAFT/PROBE line is no longer an empty `target:` (DRAFT now writes the `target:` plan) — it is `a-consumer:` / `state:`: DRAFT leaves a section at `planned` (a `NEW` target awaiting dispatch) or `answered` (an EXISTS target already answered, awaiting harvest), never `read`; only PROBE's harvest writes `a-consumer:` and reaches `read`.
The CHECK gate runs `check-probe-cards.sh` and cannot go green over a `planned` section -- so DRAFT search can never masquerade as evidence.

### Step 4b. 🤖 SELF-REVIEW — check the draft + probe plan before the gate

Before the STOP gate, self-review the DRAFT output — a CREATOR/REVIEWER split, so the drafter does not grade its own work. Dispatch a review sub-agent in a FRESH context (report-only; the drafter applies the fixes):

```text
Agent(general-purpose, prompt="
  Review this DRAFT phase output against the checklist. Report PASS or a numbered issue list
  (file + line + what's wrong + the fix). Do NOT edit anything — only report.

  READ:
    - the stage draft (the stage doc this run wrote/updated)
    - the probe plan (the 1-probes/PPNN_*.md files touched this run)
    - the calling stage's artifact spec, and the probe constitution's
      'The DRAFT self-review checklist' (../../../../probe/haipipe-probe/SKILL.md)

  Surface A — the draft, vs the stage's artifact spec:
    - every section filled with REAL content (no unmarked placeholders)
    - one sentence per line; every \citep{} key is REAL (grep the .bib); gaps use {VAL:?} / \cite{TOADD}
    - every Q-<Stage>-<n> is cited inline [Q-<Stage>-<n>] on the sentence it hangs on

  Surface B — the probe plan (run the constitution's 'DRAFT self-review checklist' verbatim):
    LAW-2-clean q-executor · answerable+specific · route set · match ROOTED to a specific folder
    (candidate READ + judged on the answer) · target agrees with match · heading id = Q-consumer id ·
    one ## Why per file, stake never leaked into a q-executor
")
```

Issues → FIX them, then re-run the review (bounded: at most 2 rounds; a 3rd-round residual is SURFACED to the human at the gate, never hidden). The self-review PRECEDES the human gate — it never replaces it; its verdict is presented at Step 5.

### Step 5. ⛔ STOP — present for review, then iterate

Writing done → STOP and end the turn: present the draft (structure + where the placeholders are) and hand the floor to the user.
The user reviews STRUCTURE and adds `> USER:` comments.
Respond with `> CC:` underneath each (never delete or reword a user comment).
Iterate until the user advances.
Do NOT start PROBE, REVISE, or any commit on your own — the user's verb/"go" is the gate.

### Step 6. Confirm and hand off

When the user approves:
1. Move resolved comment threads to `_LOG` (if applicable)
2. Write a draft phase summary entry to `_LOG` + the `[GATE] draft-review: approved` line quoting the user
3. Mark draft ✅
4. Hand off to PROBE (or skip to REVISE if PROBE is n/a for this stage — logged verdict required)


## Stage-specific notes

### seed
- Output: `0-lifecycle/0-seed/0-seed.md`
- WebSearch-to-orient + buffer rule: see Step 4 (the one normative home); seed's buffered probes are the FEASIBILITY pair (novelty + external-data-obtainable).
- PROBE (seed): FEASIBILITY only -- "can this paper exist at all?" (is it novel? does the external labeled data exist?).
  Profiling OUR OWN data is RESOURCE-stage task work; register it as a `[FORWARD -> RESOURCE]` pointer in `_LOG`, do not dispatch it in seed.
  The RESOURCE stage is the SOLE CONSUMER of these pointers and takes them at its open (reader clause in haipipe-paper-resource SKILL) -- an unconsumed pointer fails the RESOURCE done-criteria, not claims'.
- Short document: seed question + motivations + tentative claim shape

### resource
- Output: `0-lifecycle/1a-resource/1a-resource.md`; template `ref/resource-template.md`
- Venue-FREE, and it sits BETWEEN seed and claims — it is stage 1a, just before claims (1b) on disk (precedented by `2a-venue/` + `2b-pitch/`).
  Nothing renumbers.
- EXACTLY TWO SECTIONS: **Demand** (one `**N<n> (H<n>)**` per prerequisite the seed's Tentative Claim Shape implies -- keyed on H, never C) and **Questions** (one `**Q<n> (N<n>)**`, its `-> PP<NN>` backlink once the PROBE worker opens the section, and its `A:` when the answer lands).
  NO Kill Conditions, NO Setup Contract, NO Resource Ledger, NO Binding table — JL cut them 2026-07-14.
- On open: consume the seed's forward pointers out of `_LOG_0-seed.md`.
  The grep MUST be GLYPH- AND LEGACY-TOLERANT — the live pointers on disk all say "CLAIMS" (this stage did not exist when they were written) and at least one uses a UNICODE arrow.
  Match `grep -E "\[FORWARD (->|→) (RESOURCE|CLAIMS)\]"`.
  Each pointer becomes an N row, a Q, or is explicitly DECLINED in `_LOG` with its reason; a CLAIM-STATUS pointer is not ours — leave it for claims and say so.
- The stage ASKS; it never mints a PP id, never picks a probe type or topic, and never executes (no `/haipipe-data`, `/haipipe-nn`, `/haipipe-task`, no inline store scan).
  WebSearch/glob to ORIENT is legal DRAFT fuel per Step 4 — it never lands in an `A`.
- PROBE (resource): EXACTLY ONE worker call per pass — `Skill("haipipe-paper-probe", args="from-buffer <paper_root>")`, never evidence inline.
  The worker picks up the human-approved Q's, opens a SECTION for each in the right topic's probe file, writes the `-> PP<NN>` backlink into the Q, MATCHes, dispatches only what MATCH cannot close, and lands the answer back as the Q's `A`.
  It runs in TWO passes (SCAN, then — after the stage's GATE 1b spend authorization — BUILD); the pass split is the stage's business, not DRAFT's.
- NO SIDECARS: no `_VALUES_`, no `_CITATION_`, no `_RESOURCE_` satellite.
- Ends at the hard STOP: GATE 1, where the human approves the DEMAND, the QUESTIONS (which Q's are worth asking) and the SCOPE CUTS.
  Asking is cheap, so GATE 1 approves the QUESTIONS, not the SPEND — spend is authorized later, at the stage's GATE 1b, once the SCAN answers have landed.

### claims
- Output: `0-lifecycle/1b-claims/1b-claims.md`
- On open: do NOT grep seed's `_LOG` for forward pointers — RESOURCE is their sole consumer, and re-consuming one it already took DOUBLE-DISPATCHES the same build.
  Read `_LOG_1a-resource.md` instead: only the pointers resource explicitly DECLINED to claims become PP entries in the Probes section (or are declined again in `_LOG`)
- Reads the resource stage's `1a-resource.md`: the ingredients (data / reusable model / code) are settled there, but training this paper's model (fit) + eval are claims' own experiment; a claim whose ingredients are missing is marked BLOCKED-ON-RESOURCE, not re-asked
- PROBE: link evidence sources, spawn probes for GAPs
- Hypotheses are venue-neutral (H1, H2, H3)

### pitch
- Output: `0-lifecycle/2b-pitch/2b-pitch.md`
- PROBE: citation audit for anchor papers
- Venue-ALIGNED: reads the venue stage's 2a-venue.md (pack fallback per the venue guard)

### narrative
- Output: `0-lifecycle/3-narrative/3-narrative.md`
- PROBE: citation + display needs per beat
- Section-mirrored story with readiness tags

### display
- Output: `0-lifecycle/4-display/4-display.md` (the BRAIN; `4-display.tex` is GENERATED from it by sync at REVISE — never drafted by hand); template `ref/display-template.md`
- DRAFT runs the stage's step-0 reconcile first (legacy probes/preview/tex-comments merge), then authors the md: Venue Set, Display Map, PROBE PLAN (S0/En/Rn rows, ▶ ready / ✋ gated-on-thread), one block per display with method candidates + ASCII sketch
- The ⛔ STOP presentation = the open threads + the Probes section; the user rules on threads and strikes rows; DRAFT proposes, PROBE executes after the gate (the display twin of section-edit's "Probes proposed by this draft" block)
- PROBE: step-0 cross-stage coverage sweep, then evidence lane (tasks/probes) + render lane (renderer skills, candidate mode) over the approved plan rows

### section-edit
- Output: `0-lifecycle/5-section-edit/{section}/{section}.md`
- Format: REAL prose per `ref/outline-format.md` in section-edit hub
- Ends with the "Questions raised by this draft" block: every {VAL:?}/\cite{TOADD} rolled up with its expected source, display needs per paragraph, heavier needs (new task run, lit sweep) RAISED as `state: planned` question SECTIONS in `1-probes/PPNN_<topic>.md` + Status board row.
  DRAFT proposes; PROBE binds each one to an answer after the gate.
  The STOP presentation includes this block.
- PROBE: citation + values + display (three parallel tracks)
- Reads section-type norms and 2a-venue.md's per-section blueprint block for style (pack fallback per the venue guard)


## Where style guidance lives (NOT here)

DRAFT settles content, not style.
Style inputs come from elsewhere:

| Guidance | Lives in | Used by |
|---|---|---|
| Venue style, word budget, arc | `0-lifecycle/2a-venue/2a-venue.md` (compiled from `venue/playbook-<pack>/`; pack = fallback / deep dive) | DRAFT reads budget; REVISE applies style |
| Per-section structure norms | `1-lifecycle/5-section-edit/section-type/` | DRAFT (structure) |
| Prose quality rules | `2-phase/REF/prose-quality.md` | REVISE |

Old venue LaTeX templates and the write-conference/scientific/systems style skills were archived to the paper-root `_archive/` (venue knowledge belongs in `venue/` packs).


## Relation to other phases

```
DRAFT (this)  →  PROBE   →  REVISE  →  CHECK
settle WHAT       collect     settle     verify
to say            evidence    HOW to     everything
                              say it
```

DRAFT produces the first-pass artifact.
If the content is WRONG, fix it in DRAFT.
If the content is RIGHT but sounds bad, fix it in REVISE.


## Who calls this skill

Stage skills call this as their DRAFT phase:

| Stage skill | What this skill drafts |
|---|---|
| haipipe-paper-seed | 0-seed.md (3 sections) |
| haipipe-paper-resource | 1a-resource.md (2 sections: Demand N\<n\> + Questions Q\<n\> with their A) |
| haipipe-paper-claims | 1b-claims.md (hypothesis list + evidence matrix) |
| haipipe-paper-pitch | 2b-pitch.md (cover letter) |
| haipipe-paper-narrative | 3-narrative.md (story beats) |
| haipipe-paper-display | 4-display.md (display map + Probes section + per-display blocks with candidates) |
| haipipe-paper-section-edit | {section}.md (paragraph outline) |

## Sibling phase workers

| Phase | Worker | Called after |
|---|---|---|
| DRAFT (this) | haipipe-paper-draft | -- |
| PROBE | haipipe-paper-probe | DRAFT |
| REVISE | haipipe-paper-revise | PROBE |
| CHECK | haipipe-paper-check | REVISE |
