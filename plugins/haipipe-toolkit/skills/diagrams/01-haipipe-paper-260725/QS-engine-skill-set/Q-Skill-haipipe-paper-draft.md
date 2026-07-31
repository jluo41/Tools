# haipipe-paper-draft · v0.6.2
state: 🟡 PARTIAL · account written; the acceptance test is open in Items
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Question
How does a first draft become readable Board Markdown while making every unknown sentence-level need traceable to the question that will answer it?

This page examines the DRAFT phase's two outputs: real first-pass Content and recognizable Q-consumer records.
Its central boundary is that it asks a question but never plans, routes, or executes the evidence work.

## Diagram
<!-- haipipe:skill:tree:start 9bd3490d630514a6 paper/2-phase/0-draft/haipipe-paper-draft -->

```
haipipe-paper-draft/
  feedback/
    README.md            4 ln  haipipe-paper-draft -- Feedback Inbox
  CHANGELOG.md         221 ln  haipipe-paper-draft — Changelog
  SKILL.md             384 ln  Skill: haipipe-paper-draft (internal phase worker)
```

<!-- haipipe:skill:tree:end -->

```
stage.md + template.md + upstream + venue contract
                         │
                         ▼
                     DRAFT owns the pen
                         │
      ┌──────────────────┴──────────────────┐
      ▼                                     ▼
## Content                         ## Items to Finish
one sentence per source line        - [ ] 🔎 Q-… checklist record
real .bib key OR owned placeholder  Description · Reason · Probe · Answer
adjacent > lanes attach to sentence  ▲ same id anchors any unresolved sentence
      │                                     │
      └────────── no `1-probes/` writes ────┘
                                            ▼
                                  PROBE owns entry / route / bank / target
```

## Content
<!-- haipipe:skill:body:start 9bd3490d630514a6 paper/2-phase/0-draft/haipipe-paper-draft -->

**haipipe-paper-draft** · `0.6.2` · last shipped 2026-07-26

- folder   `paper/2-phase/0-draft/haipipe-paper-draft/`
- tools    Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent, Skill
- summary  DRAFT writes two things on the owning S page: first-pass Content and Q-consumer questions. Citation/value/display lanes report holes; this hub is the single writer that makes each hole FILLED or OWNED. PROBE alone authors entries and runs the five-step evidence loop. History: ./CHANGELOG.md.

### SKILL.md



Skill: haipipe-paper-draft (internal phase worker)
====================================================

DRAFT phase worker.
Called by stage skills (seed, resource, claims, pitch, narrative, display, section-edit) to produce the first-pass artifact.
The stage defines WHAT the result looks like (its contract at `../../../1-lifecycle/haipipe-paper-stage/stages/<order>-<key>/stage.md`).
This skill defines HOW to get there.

**Not user-facing.**
Users invoke stage skills:
```
/haipipe-paper seed       → seed skill calls this internally for DRAFT phase
/haipipe-paper claims     → claims skill calls this internally for DRAFT phase
/haipipe-paper section-edit §3  → section-edit skill calls this internally
```



- 1 · Rules (follow these — the model is haipipe-probe's)
      The DRAFT-phase rules live in `../../../../probe/haipipe-probe/SKILL.md` → **Phase rules · DRAFT phase** + **The DRAFT self-review checklist**. Follow those; on conflict, that file wins. Paper-specific additions:
      - **EVERY HOLE IS FILLED OR OWNED, EVERY STAGE.** A hole you cannot fill leaves a placeholder carrying the id of the S page's Q-consumer question that will settle it — `\cite{TOADD} [Q-<Stage>-<n>]`, `{VAL:? <what>} [Q-<Stage>-<n>]`. A placeholder with no bracket is a defect. PROBE later turns those questions into entries.
      - **Citations**: grep the paper's `.bib` FIRST — real `\citep{key}` for hits, `\cite{TOADD} [Q-<Stage>-<n>]` where none fits. A key that does not grep is invented.
      - **LOCAL answers**: DRAFT may cite paper-owned registries it has actually read, but it does not author `### bank binding`; that is PROBE's MATCH work.
      - **RESOURCE stage**: write `Resource Description` under `## Content` and the logical `Q-consumer` records under `## Items to Finish` on `S-Work-0-resources.md`. DRAFT describes each resource and raises the questions; PROBE opens the entries, lands the answers, and writes their source pointers. `--depth`, supplied by the human, is the spend authorization.
      - One sentence per line; no markdown tables in probe files.
      - ⛔ **DRAFT DOES NOT TOUCH `1-probes/`.** It raises `- [ ] 🔎 Q-<Stage>-<n>` records in the S page's `## Items to Finish` and stops. Writing a `### q-executor`, choosing a `route`, judging a `bank`, or setting a `target` is PROBE's ① and ②. (They ran here until 2026-07-20, purely so one human gate could review draft + plan together; stages now declare `gates: [check]`, so that reason is gone.)
      - ⛔ **DRAFT OPENS NO GATE unless the stage's contract declares one.** Read `gates:` in `stage.md`. The default is `[check]` — in that case DRAFT ends by handing straight to PROBE, with no STOP.
      The steps below are the HOW-TO for these rules.

- 2 · What DRAFT means
      DRAFT = settle WHAT to say, **and what you cannot yet say**.
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

- 3 · The generic drafting process
      Same process for every stage, different content:

- 3.1 · Step 1. Identify the stage and read its artifact spec + template
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

- 3.2 · Step 2. Consult upstream artifacts
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

- 3.3 · Step 3. Settle structure
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

- 3.4 · Step 4. Draft content
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
      FORBIDDEN in DRAFT: opening or editing `1-probes/`, writing a
      `### a-executor`, or treating an inline result as landed evidence.
      Real evidence lands ONLY via the PROBE phase dispatching `haipipe-paper-probe` (the single door); inline search results bind to nothing -- evidence gathered any other way means "the PROBE phase did not happen."
      `check-probe-cards.sh` runs after PROBE and again at CHECK, not here, because
      DRAFT has not created entries yet.

- 3.5 · Step 4a. 🕳️ SWEEP THE HOLES — dispatch the three lanes
      Prose written: sweep it for what it could not fill. Each lane knows its own kind of hole and how to check for it. They are READ-ONLY checkers — they report, they never write — so all three can run in one batch:
      ```text
      Skill("haipipe-paper-draft-citation", args="<stage-or-section> <paper-path>")
      Skill("haipipe-paper-draft-values",   args="<stage-or-section> <paper-path>")
      Skill("haipipe-paper-draft-display",  args="<stage-or-section> <paper-path>")
      ```
      Each RETURNS a report — for every hole: WHERE it is (the sentence), WHAT it is (`\cite{TOADD}` / `{VAL:? <what>}` / a DR row), and WHO owes it (the existing `Q-<Stage>-<n>` that will produce it, or `UNOWNED` if nothing will).
      **THIS HUB HOLDS THE PEN — for all of it.** The lanes do not touch the manuscript, the stage doc, or `1-probes/`. THIS worker takes the three reports and writes:
      ```
      draft.md · prose        this hub, from the lane reports — insert each placeholder
                              with its [Q-<Stage>-<n>]
      draft.md · Q-consumer   this hub, at Step 4b
      ```
      One writer per file. Two lanes editing the same prose is a write race. The
      display lane may write only its declared display inbox; it never writes the S
      page or probe entries.
      Skip a lane only when the artifact cannot carry its kind of hole (a seed has no numbers; a pitch has no displays), and log the skip.

- 3.6 · Step 4b. 🙋 RAISE — every question this draft cannot answer
      **DRAFT is where the questions are BORN — and only born.** Raise each `- [ ] 🔎 Q-<Stage>-<n>` record under the S page's `## Items to Finish`, in the consumer's own words, with `Description`, `Reason`, `Probe: not opened yet`, and an empty `Answer`, then STOP. Planning them (①ORGANIZE, ②MATCH) is PROBE's; see probe's PHASE MAP. This skill never opens `1-probes/`.
      This step is UNCONDITIONAL. It runs on every draft, whatever the question's origin: a hole Step 4a's lanes returned unowned, a question the stage typically raises (see the calling stage's `dispatch_scope:` + craft body), a gap a web search revealed, or one you simply noticed while writing.
      Each question gets one DRAFT artifact: a `## Q-<Stage>-<n>` block in the S
      page's Q-consumer, in the consumer's own words and carrying the STAKE. Cite its
      id inline on every sentence that hangs on it. Stop at that boundary: PROBE
      finds or opens the corresponding entry, strips the stake from `q-executor`,
      authors the bank binding, and runs the five-step loop. Asking is cheap; the
      `--depth` ceiling controls which questions may incur work.

- 3.7 · Step 4c. 🤖 SELF-REVIEW — check the draft before handoff
      Verify mechanically that every `\cite{TOADD}` and `{VAL:?}` has a
      `[Q-<Stage>-<n>]` owner and every owner resolves to a Q-consumer block in the S
      page. Do not run the probe-entry checker yet: no entries should exist from this
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

- 3.8 · Step 5. Record and hand back to the stage router
      Write a `[DRAFT]` summary in the owning S page's `## Log`: artifact changed,
      questions raised, lanes run/skipped, and self-review verdict. Do not mark the S
      page `✅`; only CHECK approval does that.
      If `stage.md` includes `draft` in `gates:`, present the draft and wait. Otherwise
      return immediately to the stage router, which invokes the next declared phase
      (normally PROBE). Active comment threads remain inline until the user resolves
      them; resolved threads move verbatim to the owning S page's `## Log`.

- 4 · Stage-specific notes

- 4.1 · seed
      - Output: `0-lifecycle/0-seed/S-Seed-0-seed.md`
      - WebSearch-to-orient: see Step 4 (the one normative home).
      - Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/0-seed/stage.md` -> its `dispatch_scope:` + the craft body (the stage owns its own list; this file never restates it).
        Profiling OUR OWN data is RESOURCE-stage task work; register it as a `[FORWARD -> RESOURCE]` pointer in the Seed S page's `## Log`, do not raise it in seed.
        The RESOURCE stage is the SOLE CONSUMER of these pointers and takes them at its open (reader clause in the resource stage contract) -- an unconsumed pointer fails the RESOURCE done-criteria, not claims'.
      - Short document, FIVE sections: Seed Question + Motivations + Landscape + Tentative Claim Shape + Q-consumer (Landscape and Q-consumer are not optional — the `[Q-Seed-<n>]` anchor loop hangs on Q-consumer)

- 4.2 · resource
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

- 4.3 · claims
      - Output: `0-lifecycle/1-work/S-Work-1-claims.md`
      - On open: do not re-consume Seed forward pointers. Read the Resource S page and
        its `## Log`; only pointers it explicitly declined to Claims enter this
        Q-consumer.
      - Reads `S-Work-0-resources.md`: ingredients are settled there; training and
        evaluation belong to Claims.
      - Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/1b-claims/stage.md` -> its `dispatch_scope:` + the craft body.
      - Hypotheses are venue-neutral (H1, H2, H3)

- 4.4 · pitch
      - Output: `0-lifecycle/2-venue/S-Venue-1-pitch.md`
      - Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/2b-pitch/stage.md` -> its `dispatch_scope:` + the craft body.
      - Venue-ALIGNED: reads `S-Venue-0-venue.md` (pack fallback per the venue guard)

- 4.5 · narrative
      - Output: `0-lifecycle/2-venue/S-Venue-2-narrative.md`
      - Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/3-narrative/stage.md` -> its `dispatch_scope:` + the craft body.
      - Section-mirrored story with readiness tags

- 4.6 · display
      - Resolve the current output from `stages/4-display/stage.md`; do not invent a replacement while its declared `blocked_on` remains open.
      - DRAFT runs the stage's step-0 reconcile first (legacy probes/preview/tex-comments merge), then authors the md: Venue Set, Display Map, PROBE PLAN (S0/En/Rn rows, ▶ ready / ✋ gated-on-thread), one block per display with method candidates + ASCII sketch
      - Open threads stay inline for CHECK; DRAFT proposes and PROBE executes within its ceiling.
      - Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/4-display/stage.md` -> its `dispatch_scope:` + the craft body (the cross-stage coverage sweep is DRAFT's, not PROBE's)
      - PROBE: evidence lane (tasks) + render lane (renderer skills, candidate mode) over the approved plan rows

- 4.7 · section-edit
      - Output: the resolved Main/Appendix S page declared by the dynamic stage identity.
      - Format: REAL prose per `stages/5-section-edit/template.md` (shape + rules in one file)
      - Ends with the Q-consumer block: every placeholder has an owning question.
        DRAFT proposes; PROBE later binds each one to an answer.
      - Question types: `../../../1-lifecycle/haipipe-paper-stage/stages/5-section-edit/stage.md` -> its `dispatch_scope:` + the craft body.
        (citation / values / display are DRAFT's Step 4a lanes, not PROBE tracks.)
      - Reads section-type norms and `S-Venue-0-venue.md`'s per-section blueprint block for style

- 5 · Where style guidance lives (NOT here)
      DRAFT settles content, not style.
      Style inputs come from elsewhere:
      | Guidance | Lives in | Used by |
      |---|---|---|
      | Venue style, word budget, arc | `0-lifecycle/2-venue/S-Venue-0-venue.md` (compiled from `venue/playbook-<pack>/`; pack = fallback / deep dive) | DRAFT reads budget; REVISE applies style |
      | Per-section structure norms | the paper's `S-Venue-0-venue.md` blueprint block (BINDING), deep dive `paper/venue/playbook-*/<journal>/<journal>-<kind>/style.md` (reference) | DRAFT (structure) |
      | Prose quality rules | `../../REF/prose-quality.md` | REVISE |
      Old venue LaTeX templates and the write-conference/scientific/systems style skills were archived to the paper-root `_archive/` (venue knowledge belongs in `venue/` packs).

- 6 · Relation to other phases
      ```
      DRAFT (this)  →  PROBE   →  REVISE if declared  →  CHECK
      settle WHAT       collect     settle     verify
      to say            evidence    HOW to     everything
                                    say it
      ```
      DRAFT produces the first-pass artifact.
      If the content is WRONG, fix it in DRAFT.
      If the content is RIGHT but sounds bad, fix it in REVISE.

- 7 · Who calls this skill
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

- 8 · Sibling phase workers
      | Phase | Worker | Called after |
      |---|---|---|
      | DRAFT (this) | haipipe-paper-draft + `-citation` / `-values` / `-display` lanes | -- |
      | PROBE | haipipe-paper-probe | DRAFT |
      | REVISE | haipipe-paper-revise | PROBE, when declared |
      | CHECK | haipipe-paper-check | the previous declared phase |

- 9 · Return contract
      ```
      status:    ok | blocked
      stage:     <stage-name>
      artifact:  <path written>
      questions: <count raised this run>
      raised:    <one line per raised Q-consumer id + question; or "none">
      review:    <the Step 4c self-review verdict, incl. any residual>
      next:      the next phase declared by stage.md (normally PROBE)
      ```
### The other files

1 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
feedback/README.md       4 ln  haipipe-paper-draft -- Feedback Inbox
```

<!-- haipipe:skill:body:end -->

## Items to Finish
- [x] ✍️ Establish DRAFT's two owned outputs
      DRAFT writes real first-pass Content and the logical Q-consumer records,
      physically represented as checklist items on the owning S page.  It does
      not duplicate a Q-consumer block under Content.
- [x] 🔗 Establish the sentence-to-question join
      A missing citation or value keeps its exact same Q id in the sentence and
      checklist record, for example:
      ```markdown
      The estimated effect is {VAL:? effect estimate} [Q-Sec0Abstract-1].
      > Value: pending the answer to Q-Sec0Abstract-1.

      - [ ] 🔎 Q-Sec0Abstract-1 · Verify the effect estimate
            **Description:** Identify the reported estimate and its source.
            **Reason:** §0 P1.S1 cannot state the estimate without it.
            **Probe:** not opened yet
            **Answer:**
      ```
- [x] 🧷 Keep Board apparatus separate from evidence ownership
      One sentence is one source line.  An adjacent typed `>` lane belongs only
      to that sentence; page-level work belongs in Items.  A candidate `> Note:`
      is REVISE's author-requested review mode, not DRAFT's normal output.
- [x] 🚧 Preserve the routing boundary
      DRAFT never creates `1-probes/` entries, selects `route` or `bank`, binds
      a target, or runs evidence work.  A missing display *unit* is a Display
      Request row, not a Q-consumer.
- [ ] 🧪 Run an end-to-end section example
      Confirm that a section's sentence ids, checklist records, Board chips,
      PROBE entry, answer, REVISE placement, and CHECK all retain one join key.

## Where we are
The DRAFT page now states the exact source grammar the Board can render and PROBE can consume.
The remaining test is a full section run in which every placeholder either reaches a matched answer or remains visibly owned at CHECK.

## Log
260727 · Audited against `board.md`'s decision-only rule, which says `state:` is about the DECISION and that implementation does not gate this board. Every open item here is implementation or a test, not an undecided question, so the page was reporting itself as open because code was missing. Flipped with no ruling made.
260727 1445 · Created the DRAFT skill page from `paper/2-phase/0-draft/haipipe-paper-draft/`.
The authored record distinguishes sentence apparatus, Q-consumer ownership, and Display Requests so they cannot be conflated in later writing work.

<!-- haipipe:skill:log:start 9bd3490d630514a6 paper/2-phase/0-draft/haipipe-paper-draft -->

Converted from the skill's own `CHANGELOG.md`: 27 releases.

260726 · `0.6.2` · Board-native question records
      - DRAFT writes stage substance only under `## Content`.
      - The logical Q-consumer now materializes as checklist records under
        `## Items to Finish`; no literal Q-consumer Content block is emitted.
260726 · `0.6.1` · Resource follows its stage contract
      - Replaced the retired Demand/Questions row schema with the authoritative
        `Resource Description` + `Q-consumer` structure.
      - Forward pointers now land in a resource topic plus an owned
        `Q-Resource-<n>`, or are explicitly declined in the S-page Log.
260726 · `0.6.0` · DRAFT raises questions; PROBE owns entries
      - DRAFT now writes only S-page Content and Q-consumer questions.
      - Removed probe-entry authoring, MATCH, and the obsolete DRAFT human gate.
      - Phase records and resolved comments now land in the owning S page's `## Log`.
260724 · `0.5.2`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 5.2.0; older entries below keep their original numbers).
260719 · `5.2.0` · Step 4c runs the checker BEFORE the sub-agent
      ### Changed
      Step 4c opened by dispatching a review sub-agent whose checklist asked, in prose, for
      placeholder ownership ("COMPLETENESS, the reverse direction: every {VAL:?} and every
      \cite{TOADD} carries a [Q-<Stage>-<n>]"). That is a regex property, and it is already tested
      deterministically by `check-probe-cards.sh` PASS 4 — which DRAFT never ran. So the phase that
      CREATES the property delegated verifying it to a model reading a document.
      It does not hold. Measured on `Paper-Personality2Opioid-MISQ2026`: 19 unowned placeholders
      across four section docs, every one written under a DRAFT self-review that reported clean.
      Step 4c now RUNS `check-probe-cards.sh <paper_root> --stage <stage>` first and states the
      DRAFT-phase pass condition explicitly — the ONLY legal FAIL is `state-planned(probe-not-run)`,
      which is what a correct DRAFT looks like (DRAFT plans the entries, PROBE runs them). Every
      other code (cite-unowned, value-unowned, dangling-owner, stale-old-format, LAW2 leak,
      sidecar-present, markdown-table) is a DRAFT defect fixed before the gate. The sub-agent keeps
      only what the checker CANNOT test: is the question answerable, was the `bank` verdict rooted in
      a folder someone actually read, does the prose say anything. Judgment, not pattern-matching.
      Requires haipipe-paper-probe >= 6.1.0 (the `--stage` filter this relies on was vacuous for
      section-edit before it).
260719 · `5.1.0` · question-raising promoted to a step of its own
      One tag for one body of work (JL: "only add it or assign the new tags until we really have the final version, not everytime, we have a new tag" / "现在直接改到5.1，但是更新并没有很多。以后代际更新要谨慎").
      From `_console/closed/260719-01-DRAFT-RAISE-QUESTIONS.md`, findings B1 B2 B4 B5 B6 · A4 A5 A8 A9 A10 · C1 C3 C4 · D1 D3 · N3 N4. JL's opening question was "把 draft 的 raise 问题's ability，也提得更重要一些" — this is that.
      **N1 — `Skill` was never declared.** `Step 4a. 🕳️ SWEEP THE HOLES` consists of exactly three `Skill()` calls — `haipipe-paper-draft-{citation,values,display}` — but `allowed-tools` listed `Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent` and never `Skill`. Every dispatch on the step's only path was undeclared. `Skill` appended. The same gap had an older, quieter instance: the `Skill("haipipe-paper-probe", …)` call in the resource stage note. That one sat in a per-stage aside; Step 4a is on the mandatory path, which is why this surfaced now.
      **B1 — RAISE + PLAN is now `Step 4b`, a top-level step.** It had been the second "legal destination" of a bulleted aside inside `**Inline WebSearch is ALLOWED here**` — nesting depth 3, scoped by its parent to "when the search reveals a gap". A question born from reading upstream, or from a `{VAL:?}` the prose could not fill, had no instructed home; the file even said so ("see Step 4 (the one normative home)"). The step is now UNCONDITIONAL and names its four origins. The WebSearch block keeps one line pointing at it.
      **B2 — the consumer-side half was never instructed.** DRAFT rule 2 in `probe` is a conjunction: raise a `## Q-<Stage>-<n>` in the stage doc's Q-consumer AND author its probe ENTRY. This file only ever taught the ENTRY, then assumed the id existed — its own self-review checked that the id was cited inline, an id nothing had told it to create. Step 4b now states both halves as ① and ②.
      **B5 — find-or-open, and T0 JOIN.** "author its ENTRY" dropped `probe`'s find-or-open, and the cost ladder's cheapest rung appeared nowhere, so a drafter opened a duplicate entry instead of adding a `### q-consumer` bullet to the one already asking.
      **N2 — the hub holds the pen, for all of it.** JL: "我以为draft会call draft-citaton, draft-values, ... 最后之后haipipe-paper-draft 再改 draft.md 和Q-consumers". Two contradictions, not one. The lanes' own SKILL.md files claimed they RAISED the Q-consumer and authored the ENTRY, while this hub said it folded them in — both claimed the pen on `1-probes/`. And the citation and values lanes each edited the manuscript prose directly, while Step 4a dispatches all three "in one batch": a sentence missing both a citation and a number is the common case, so two lanes edited the same line concurrently. Both races are gone. The lanes are READ-ONLY checkers returning one row per hole (where · what it owes · which `Q-<Stage>-<n>` owes it, or UNOWNED); this hub writes the prose placeholders, the Q-consumer, and the probe entries. The display lane keeps its pen — `_DISPLAY_REQUEST.md` has no other writer.
      **D1 / R1 — per-stage question types moved OUT.** JL: "是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？" The `PROBE:` lines in Stage-specific notes were assigning question ELICITATION to the PROBE phase, against `probe`'s PROBE rule 1 and this file's own "DRAFT is where the questions are born AND planned". Each stage skill now owns a **Questions this stage typically raises** section; this worker points at it and never restates it (one home). The display note keeps only its genuine PROBE work — the evidence and render lanes.
      **N3 — the file violated its own headline rule** in four places, writing bare `\cite{TOADD}` / `{VAL:?}` while the Rules block says "A placeholder with no bracket is a defect". Worst instance was inside the self-review checklist, where it taught the reviewer to accept them.
      **B6 — the self-review gained a COMPLETENESS surface.** It checked Q → sentence ("every `Q-<Stage>-<n>` is cited inline") and never sentence → Q. The mechanical backstop already existed — `check-probe-cards.sh` carries `cite-unowned` and `value-unowned` over the stage docs — but it runs at PROBE VERIFY and again at CHECK, long after the DRAFT gate. The self-review is where an unowned placeholder should be caught, while the drafter is still holding it.
      **A5 — the merged gate now presents all three things** it exists to review: draft, probe plan (one line per question), self-review verdict. It had presented only the draft, though the file itself says "ONE gate reviews both".
      **A4** return contract added (`status: blocked` was instructed with nothing defining it) · **A8** the single door named in FORBIDDEN · **A9** WebFetch named; load-bearing clause added · **A10** both checker run sites named · **C1** the hand-written "Status board row" dropped (it is GENERATED, and the `fn/probes.md` citation was dangling) · **C3** the self-review sub-agent gets a repo-root-relative path, since a fresh agent cannot resolve `../../../../` · **C4** "buffer rule" / "buffered probes" retired (`args="from-buffer …"` is NOT debris — it is the live argument-hint) · **D3** Q-consumer restored to the five stages missing it in Step 3 · **N4** "Probes section" → "Q-consumer".
260719 · `5.0.1` · vocabulary: `probe`, not "the constitution"
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
      ### Changed (ruling A) — four sites
      - Rules header: "The DRAFT-phase rules live in the constitution: `../../../../probe/haipipe-probe/SKILL.md`" -> "The DRAFT-phase rules live in `../../../../probe/haipipe-probe/SKILL.md`".
      - Web-search destinations: "see the probe constitution's PHASE MAP" -> "see probe's PHASE MAP".
      - Self-review READ list: "the probe constitution's 'The DRAFT self-review checklist'" -> "probe's 'The DRAFT self-review checklist'".
      - Self-review Surface B: "run the constitution's 'DRAFT self-review checklist' verbatim" -> "run probe's ... verbatim".
      No `a-consumer` sites in this skill; ruling B did not touch it.
260719 · `5.0.0` · BREAKING: the three lanes join DRAFT; every hole is FILLED or OWNED
      From the `paper/2-phase` skillset review.
      ### Changed (JL: "在 draft 的时候,就应该尽量把东西都 draft 好。比如说,如果有些东西没写出来,那就应该有一个对应的 question 或者 concern")
      DRAFT's done-state is restated: a hole is either FILLED or OWNED, and there is no third state. An OWNED hole is a placeholder carrying the id of the question that will settle it — `\cite{TOADD} [Q-<Stage>-<n>]`, `{VAL:? <what>} [Q-<Stage>-<n>]` — two markers side by side, never fused (JL: "\\cite{TOADD} [Q-XXX-N] So I want something like this."). A placeholder with no bracket is a defect: nobody owns it, so nobody will ever fill it. When no existing question would produce what the prose owes, DRAFT RAISES one — JL: "feel free to add more questions … the Q-consumer is as many as possible … if there's no one here, I think you should propose a new question."
      ### Changed — NEW Step 4a, the hole sweep
      Three lane skills join this phase and are dispatched together after the prose is written: `haipipe-paper-draft-citation` / `-values` / `-display`. They were the DRAFT halves of three skills that lived under `1-probe/` and were named probe lane workers despite containing no ③④⑤ work at all. Each lane knows its own kind of hole and its own way of checking for it (JL: "For each topic, they should be aware how to check the values and citations and displays, and raise the questions") — which is why they stay three skills rather than folding into this hub.
      ### Changed — the Rules block
      The citation rule and the sidecar rule collapse into one: EVERY HOLE IS FILLED OR OWNED, EVERY STAGE. `1-probes/` is the only consumer-side source of truth; `_LOG_<stage>.md` is the only sidecar.
      ### Changed — the seed artifact is FIVE sections, not three
      This file described `0-seed.md` as three sections in three places (Step 3, the seed stage note, and the caller table), omitting Landscape and Q-consumer. Q-consumer is where every `[Q-Seed-<n>]` anchor lives, so an agent following the old Step 3 would present a 3-section plan and fail the seed skill's own done-criterion 1.
260719 · `4.4.0` · sync to probe constitution v9.5.0 (Q-executor-entry probe-file format) + archaeology strip
      Rewrote every probe-file-anatomy reference to the new v9.5.0 shape: a probe entry is now `## QX<n>` (topic-local) with four `###` subsections — `### q-executor` (+ `Deliverable:` / `Accepted:` lines), `### q-consumer` (one bullet per Q-consumer, its stage-doc id + original question), `### bank binding` (`route` / `bank` / `target` / `state`), and `### a-executor` (the harvested copy of the QA answer). Field renames applied across the Rules block, Step 4 (probe plan), Step 4b self-review Surface B, the summary, and the frontmatter: `route:`→`route`, `match: EXISTS·<f> / NONE→NEW`→`bank: reuse | run | code | new`, `target:`→`target`, `state:`→`state`, and the probe-file `a-consumer:` (the answer copied INTO the probe file)→`### a-executor`; the `## Why` field is DROPPED — the stake stays in the stage-doc Q-consumer. Unchanged (deliberately): the stage-doc `Q-<Stage>-<n>` Q-consumer id and its `Answer:`/a-consumer (station ②) — only the probe-file entry heading and fields moved. Retired the `_VALUES_*`/`_CITATION_*` consumer-side sidecars from the T1 LOCAL registry list (1-probes/ is the only consumer-side source of truth; `_LOG` is the only kept sidecar); the `.bib`/`\citep{}`/`\cite{TOADD}`/`{VAL:?}` citation rules are untouched. Archaeology strip: dropped the dated ruling citation from the resource-stage "cut" note.
260719 · `4.3.0` · RULES block (points at haipipe-probe's DRAFT phase rules + paper deltas)
      New "## Rules (follow these)" section near the top: a short followable checklist that POINTS at the constitution's **Phase rules · DRAFT phase** + **DRAFT self-review checklist** (single source), then lists ONLY the paper-specific rules (citations/.bib, T1 LOCAL registries, RESOURCE intake, one-sentence-per-line). The detailed steps below remain the HOW-TO. No content duplicated from haipipe-probe — the worker points, not restates. Follows constitution v9.4.0 (Phase rules).
260719 · `4.2.0` · DRAFT SELF-REVIEW before the gate (Step 4b)
      New Step 4b: before the STOP gate, DRAFT dispatches a review sub-agent (`Agent(general-purpose)`, fresh context, report-only) to self-check its output — Surface A the draft vs the stage's artifact spec (real content, one sentence per line, real \citep keys, every Q-<Stage>-<n> cited inline), Surface B the probe plan vs the constitution's DRAFT self-review checklist (q-executor LAW-2-clean, answerable+specific, route set, match rooted to a specific folder, target agrees, heading id = Q-consumer id, one ## Why). Issues → the drafter fixes → re-review (bounded 2 rounds; a residual is surfaced to the human, not hidden). Creator/reviewer split: the drafter never grades its own work. `Agent` added to allowed-tools. Follows constitution v9.3.0.
260714 · `4.1.0`
      - The RAISED-QUESTIONS destination points at `haipipe-paper/fn/probes.md` (renamed from fn/probe-plans.md).
      - FORBIDDEN-in-DRAFT restated in section vocabulary: no `reading:`, no `target:`, no finding written into a probe section; the DRAFT/PROBE line is SECTION STATE.
      - resource stage note: the PROBE WORKER opens the section and writes the `-> PP<NN>` backlink (was "the gateway mints the card").
260714 · `3.10.0`
260714 · `4.0.0`
      - PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
      - DRAFT is the birthplace of the QUESTIONS: it now RAISES each gap as a `state: planned` SECTION in 1-probes/PPNN_<topic>.md (writing the `commission:` in general language, NEVER the `## Why`), instead of buffering a `status: planned` PP-card skeleton with Need/Why/Route + empty refs — a shape the rewritten checker FAILs (no-state-field / no-commission). Ports the application DRAFT worker's already-landed v1.2.
      Fixed (the RESOURCE stage was unreachable from the DRAFT worker)
      - The new venue-FREE `resource` stage (`1-lifecycle/1a-resource/haipipe-paper-resource/`) resolved NEITHER an artifact-spec row NOR a template path here, so a `resource` DRAFT had no format source at all. Added:
        - Step 1 registry row: spec `1-lifecycle/1a-resource/haipipe-paper-resource/SKILL.md`, template `ref/resource-template.md` (the template itself now exists, shipped with the stage).
        - Step 2 upstream row: `resource` reads seed (Tentative Claim Shape + `_LOG_0-seed.md` forward pointers); `claims` now reads seed + resource.
        - Step 3 "Settle structure" line: resource = the two sections (Demand `N<n>` / Questions `Q<n>` + `A`), nothing else.
        - Stage-specific notes `### resource`: output path, the two-section artifact (and the sections JL CUT), the glyph- and legacy-tolerant `[FORWARD -> RESOURCE|CLAIMS]` consume grep, "the stage ASKS -- no PP ids, no probe types, never executes", "PROBE = exactly ONE worker call per pass, never inline", "no sidecars", ends at the GATE-1 hard STOP (which approves the QUESTIONS, not the SPEND -- spend is authorized at the stage's GATE 1b, per haipipe-paper-resource 1.1.0).
        - "Who calls this skill" row for `haipipe-paper-resource`.
      - Venue guard: the venue-FREE set was stale (`seed, claims`) -- it is now `seed, resource and claims`.
      Fixed (forward-pointer DOUBLE CONSUMPTION -- companion to haipipe-paper-claims 4.5.0)
      - Stage-specific notes named CLAIMS as the consumer of seed's FORWARD pointers, while the new `### resource` note (above) named RESOURCE. Two consumers for the same 7 live pointers = a permanent deadlock at the claims CHECK gate (resource takes the pointer; the pointer LINE still sits in `_LOG_0-seed.md`, so claims' old "no unconsumed pointer" bar could never clear) -- or a double-dispatch of the same build if the agent re-materialized it as a PP entry. RESOURCE is now the SOLE consumer:
        - `### seed`: internal-data profiling forward-points to `[FORWARD -> RESOURCE]` (was `CLAIMS`); an unconsumed pointer fails the RESOURCE done-criteria, not claims'.
        - `### claims`: the "grep seed `_LOG` for `[FORWARD -> CLAIMS]`" line is GONE. Claims reads `_LOG_1a-resource.md` and picks up ONLY the pointers resource explicitly DECLINED to it.
260710 · `3.9.0`
      Changed (JL ruling: real citations from .bib in the draft)
      - Draft prose writes real `\citep{key}` for keys grep-verified in the paper's .bib (check .bib + _CITATION_ FIRST); `\cite{TOADD}` + `_CITATION_` row where no key fits. Supersedes `[CITE: <topic>]` and "(Author Year)" placeholders. A key that does not grep in .bib is an invented citation.
260709 · `3.8.0`
      Changed (JL 2026-07-09: "draft = review the section + propose what probes to do")
      - section-edit stage note: drafts end with the "Probes proposed by this draft" block per the stage template; heavier needs buffered as planned PP skeletons; the STOP presentation includes the block.
260709 · `3.7.0`
      Changed (JL ruling 2026-07-09 (LLMTrait-Section session postmortem): normalize the writing process)
      - Section drafts are REAL prose: complete sentences close to submission register, {VAL:? <what>} / [CITE: <topic>] placeholders, never invented numbers/citations. Argument docs unchanged (working prose).
      - Step 5 renamed to "STOP -- present for review, then iterate": writing done -> end the turn; the user's verb/"go" is the gate. Never start PROBE/REVISE/commit on your own.
      - Step 6 hand-off writes the [GATE] draft-review: approved line quoting the user; skips require a logged verdict.
260708 · `3.6.0`
      Changed (venue lockfile wiring)
      - Venue guard + style-source table repointed: primary venue read = the paper's `0-lifecycle/2a-venue/2a-venue.md` (Writing Principles + Structural Blueprint block); direct `_venue/` pack reads demoted to fallback (2a-venue.md absent) or deep dives via its `[source: ...]` tags; pinned-but-no-pack STOP kept in the fallback branch.
260707 · `3.5.0`
      Fixed (skillset-diagnose FIX round; findings A1/A2/A4/A6 + thread T3)
      - Template registry (A1, 🔴): all five `../ref/<stage>-template.md` rows were off by one level (resolved to nonexistent `1-lifecycle/<stage>/ref/`); now `ref/<stage>-template.md` relative to each stage skill's OWN folder, with the resolution rule spelled out.
      - Artifact-spec path (A2): `1-lifecycle/{stage}/SKILL.md` → `1-lifecycle/{stage}/haipipe-paper-{stage}/SKILL.md`.
      - Archive pointer (A4): "2-phase/_archive/" → paper-root `_archive/` (the real location).
      - Duplication (A6): the seed stage-note no longer restates the fuel-not-evidence rule; it back-references Step 4 (the one normative home).
      - FORWARD handoff (T3, JL: "同意。"): seed note now states the claims stage CONSUMES the `[FORWARD -> CLAIMS]` pointers at its open; claims stage-note gains the reader line. Reader clause itself lives in haipipe-paper-claims 4.1.0.
260707 · `3.4.0`
      Changed (DRAFT may orient via WebSearch -- validated by the Paper-CGMtoCyclePhase session where inline CGM-x-cycle search drafted the seed, then the real PROBE ran)
      - allowed-tools gains WebSearch, WebFetch.
      - Step 4: inline search is DRAFTING FUEL, not evidence -- two legal destinations (prose with (Author Year) placeholders; buffered `status: planned` PP skeletons). FORBIDDEN: findings/refs/takeaways into a PP card. The line is card state; CHECK-gate checker blocks planned/empty-ref cards from going green.
      - seed stage-note: PROBE is FEASIBILITY only (novelty + external-data-obtainable); internal-data profiling forward-points to CLAIMS via a `[FORWARD -> CLAIMS]` _LOG pointer. (Also corrected the stale "seed PROBE: n/a" line.)
260703 · `3.3.0`
      - phase spine renamed DGPC -> DPRC (GATHER->PROBE, POLISH->REVISE).
260703 · `3.2.0`
      - DRAFT-oriented cleanup. Archived leftover venue LaTeX templates (templates/) and the 3 write-* style skills to 2-phase/_archive/ (venue knowledge belongs in _venue/ packs, prose style in POLISH). Step 1 now reads the stage's template from 1-lifecycle/ via an explicit registry table; this skill carries no templates of its own. Added venue guard: venue-ALIGNED stages STOP with status: blocked when no venue is pinned or no pack matches; missing per-section style file proceeds with a flagged warning, never silently invented norms.
260703 · `3.1.0`
      - reframed as internal worker. Users invoke stage skills (seed, claims, pitch...), not this skill directly. Stage skills call this during their DRAFT phase.
260703 · `3.0.0`
      - rewritten as generic stage-aware DRAFT hub. Section-specific outline format moved to 1-lifecycle/5-section-edit/ref/outline-format.md. Draft now works for all stages (seed, claims, pitch, narrative, display, section-edit).
260702 · `2.0.0`
      - complete rewrite for section-edit outline creation.
260605 · `1.1.0`
      - renamed from paper-write to haipipe-paper-section-edit-write.
260531 · `1.0.0`
      - baseline metadata added.

<!-- haipipe:skill:log:end -->
