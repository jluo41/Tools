# Discovery BJTR Alignment Addendum

Status: active addendum to the Discovery lifecycle map (2026-09-07).

This addendum repairs a naming problem in the earlier Discovery designs. The
old 0/1/2/3 or 1/2/3/4 labels mixed skill-bank folders, Page workflow steps,
and work artifacts. They are useful historical labels, but they are not the
address of a Discovery unit. The only work address is Block–Job–Task–Run
(BJTR).

## 1. Keep the axes separate

| Axis | Canonical values | What it answers | What it does not mean |
|---|---|---|---|
| Work hierarchy | discoveries → bNN Block → jNN Job → tNN Task Page → rNN Run | Where is this work and what owns it? | Not a phase or a skill directory |
| Discovery domain | D1 SCOPE → PREPARE? → ACQUIRE ↔ SYNTHESIZE → CLOSE | When does the inquiry move? | Not b01/j01/t01/r01 numbering |
| Page workflow | 00 CONTEXT → 01 OUTLINE → 02 EVIDENCE → 03 CONTENT → 04 CHECK | How is the Task Page authored and checked? | Not a Folder level |
| Page type | source-map, source-reading, synthesis forms | What article does the Task Page promise? | Not a Run kind |
| Skill bank | 1_search, 2_review, 3_synthesize, workflow-phases, agents | Which capability or role is loaded? | Not a project path |

The work hierarchy is structural. D1 and Page workflows are temporal. Skill
folders are organizational. Page type is semantic. A name such as 2_review can
never be used to infer j02, and 01 OUTLINE can never be used to infer t01.

## 2. Canonical work shape

```text
discoveries/                                  bank; no address segment
└── b01_sleep-evidence/                       Block = Discovery Board
    ├── board.md
    └── j02_sleep-mechanisms/                 Job = inquiry/campaign group
        └── t03_circadian-review/             Task Page = one article question
            ├── t03_circadian-review.md       Page Face
            ├── discovery.yaml                Task Face manifest
            ├── outline/                      Page process and derived evidence
            ├── scripts/                      optional reusable instrument
            ├── runs/
            │   └── r01_smith2024_clock.sh    executable Run ticket
            └── results/
                └── r01_smith2024_clock/      exact same-stem Run projection
                    ├── r01_smith2024_clock.md
                    ├── facts.md
                    ├── runtime.yaml
                    └── r01_smith2024_clock.bib
```

The address is b01.j02.t03.r01 (or b01j02t03r01 in compact form). A Block can
contain several sibling Jobs; a Job can contain several Task Pages; one Task
Page can contain many Runs. One Run analyzes one admitted canonical Subject,
normally one paper. Result is the Run's readout, not a fifth level. The exact
same-stem pair runs/rNN_*.sh and results/rNN_*/ is mandatory. PDF, raw text,
and captured Trigger material are optional Result attachments.

## 3. Retrofit of the old numbered design

| Historical label | Current interpretation | Lawful owner | Never infer |
|---|---|---|---|
| 00/01/02/03/04 | Shared Page workflow records | haipipe-page-workflow and its phases | b00/b01/t01 or a Run |
| 1_search | FIND and canonical-identity capability family | D1 ACQUIRE intake | Job j01, one Run, or a phase named “1” |
| 2_review | Per-Subject review capability family | D1 ACQUIRE source review | Job j02 or one aggregate Run |
| 3_synthesize | Cross-Result synthesis capability family | D1 SYNTHESIZE and Page CONTENT | r03 or a new hierarchy level |
| 3_idea, 4_idea, or other old Idea labels | Unsupported retired labels | stop and request a new 3_synthesize Page or sibling haipipe-ideation unit | a live route, migration target, or inferred Run |
| D1 SCOPE…CLOSE | Domain lifecycle | workflow-phases/haipipe-discovery-inquiry | b/j/t/r segments |
| runs/rNN_*.sh | Level-4 executable analysis ticket | D1 ACQUIRE only | search query, API call, or synthesis pass |
| results/rNN_*/ | Paired Run readout | D1 ACQUIRE result contract | a second Run or a Page phase |

Semantic direction work leaves Discovery through the sibling haipipe-ideation
skill. It is not represented by a Discovery capability family, Page type, or
Run. No Idea compatibility route is provided.

## 4. Command-to-address crosswalk

| Command | Address affected | Durable effect |
|---|---|---|
| open-block | bNN | Create or select a Discovery Board Block and board.md |
| open-job | bNN/jNN | Create or select an inquiry/campaign Job under that Block |
| open | bNN/jNN/tNN | Create one typed Task Page with both Faces |
| scope | tNN | Freeze question, discovery_type, boundary, and admission rule |
| prepare | tNN | Optionally add a reusable script under scripts/ |
| add / acquire | tNN → rNN | Resolve Triggers, admit Subjects, allocate paired Run/Result units |
| run | rNN | Execute one already allocated Run ticket |
| synthesize | tNN | Hand accepted Results to the Page workflow; no new D1 Run |
| check / close | tNN | Check Page and reconcile Task Face/report; no new Run |

Search, resolver, reader, reviewer, checker, and Bib-builder calls are receipt
detail inside the owning cycle. They do not receive a b/j/t/r address of their
own. A URL or citation is a Trigger; after identity and admission it becomes a
Subject and receives exactly one Run address.

## 5. Legacy migration rules

The BJTR addendum is interpretive and does not mass-migrate existing folders.
For a legacy two-level bank, use scripts/migrate_bjtr.py in its no-write
preview mode first. The explicit mapping is:

```text
legacy bank       -> one bNN Block
legacy Group      -> one jNN Job under that Block
numbered leaf     -> one tNN Task Page under that Job
old source/note   -> preserved Task-side material
old paper mention -> not a Run until a new Subject is admitted and analyzed
```

The migrator never manufactures Runs from a PDF, source index, notes file, or
old status. It makes the new b/j/t address explicit. Old skill directories are
not project folders and must not be moved into discoveries/. Idea-typed legacy
manifests are rejected; they are not converted or redirected. There is no need
to rename 1_search, 2_review, or 3_synthesize to Block/Job/Task/Run directories.

## 6. Acceptance invariants

1. Every new durable Task has one complete bNN/jNN/tNN address and one
   discovery_type.
2. Every allocated Level-4 Run has a full bNN.jNN.tNN.rNN receipt, one Subject,
   an executable same-stem ticket, and an exact same-stem Result directory.
3. Only D1 ACQUIRE commissions Discovery Runs. Page phases and D1
   SYNTHESIZE/CLOSE do not mint umbrella Runs.
4. A complete Result owns its Card, facts, runtime receipt, and exactly one
   authoritative Bib entry. The Task aggregate Bib is derived from those
   Results.
5. Page Content may use many Results and one Result may support many divisions;
   hierarchy and evidence cardinality are different relationships.
6. Missing or changed evidence routes back to ACQUIRE. It is never hidden in a
   monolithic notes file or a fake 0/1/2/3 folder.
7. New semantic ideation consumes Task/Discovery evidence through
   haipipe-ideation and hands selected directions to Paper P0; Discovery keeps
   only the external evidence and cross-Result synthesis it owns.

## 7. Worked route

For “map the literature on wearable sleep timing,” the intended reader promise
is clusters, disagreements, and gaps, so select or create
b01_sleep-evidence, then j02_sleep-mechanisms, then open a
t03_circadian-review landscape-review Page. During SCOPE the question and
admission rule are frozen. ACQUIRE resolves each accepted paper and allocates
r01, r02, …; each gets its own shell ticket and Result/Bib. SYNTHESIZE uses
those Results in Page OUTLINE/CONTENT, and CHECK/CLOSE publishes the Task
outcome. If the promise is only “what do these already-selected articles say,”
use source-reading instead; if it is “what sources exist,” use source-map. A
later request to propose research directions goes to haipipe-ideation with
Result/Bib pointers; it does not turn t03 or 2_review into a new level.

This addendum is linked by the public Discovery skill, D1 workflow table,
lifecycle map, manifest schema, and agent guidance. Those files are the
operational entry points; this file is the retrofit/crosswalk when an older
numbered description is encountered. Unsupported Idea labels stop at the
boundary instead of being interpreted as compatibility.
