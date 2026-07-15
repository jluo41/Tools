# Discovery Lifecycle Map (v2 — two-axis, 3 types: Search Review Idea)

A discovery is one research topic stored as its own folder, a sibling of a task-folder. Discovery has the same two axes as task: a uniform lifecycle (Plan → Build(optional) → Execute → Report) crossed with a folder type. The three types follow an IPO shape — Search (gather) → Review (analyze) → Idea (create). This file is the CANONICAL contract for the discovery layer; do not restate it in SKILL.md or DESIGN.md, point here and edit here.

## Two axes (the model)

```
Axis 1 — LIFECYCLE (uniform; every folder runs it)   Plan → Build(opt) → Execute → Report   (process verbs)
Axis 2 — TYPE      (what kind of folder this is)      Search · Review · Idea                  (folder kinds)
```

The two axes use non-overlapping vocabularies on purpose: the four phases are process verbs every folder runs (Plan/Build/Execute/Report); the three types name the kind of folder (Search/Review/Idea). No word appears in both lists, so the two axes can never be mistaken for each other. Each type maps 1:1 to its Execute bucket: Search → 1_search, Review → 2_review, Idea → 3_idea.

This mirrors task. Task = (Plan/Build/Execute/Report) × (data/nn/fit/...). Discovery = (Plan/Build/Execute/Report) × (Search/Review/Idea). Every type runs every stage; the type only changes what Execute produces.

One simplification versus task: a task-folder holds MANY runs (`configs/<run>`, `results/<run>`, `notebooks/<run>`); a discovery-folder holds ONE execution per topic — one Plan, one Execute, one Report.

## Hierarchy (unchanged)

```
task:       tasks/{G}{NN}_group/   ⊃  {NN}_taskname/   (one runnable unit)
discovery:  discoveries/<GROUP>/   ⊃  <NN>_<topic>/    (one research topic)
```

## Axis 1 — the lifecycle (uniform)

| stage | task meaning | discovery meaning | writes |
|---|---|---|---|
| **Plan** | design the IPO contract | declare `type` + question + scope + which sources + intended terminal | `discovery.yaml` |
| **Build** *(optional)* | write the code | author the instrument: query strategy / extraction schema / synthesis rubric. SKIP for a quick lookup | `build/` artifact |
| **Execute** | run the script | do the work — gather / analyze / create | the work bundle + the terminal file |
| **Report** | summarize results vs plan | report to a human: outcome, confidence, caveats, handoff | `discovery.yaml` `report:` block (appended; absent before) + log event |

File ownership is strict. Plan writes `discovery.yaml`. Build touches `build/`. Execute writes the evidence files. Report appends the `report:` block. There are no other bookkeeping files.

## Axis 2 — the three types (IPO: Search → Review → Idea)

The types × roles × terminals table is owned by `ref/discovery-yaml-schema.md` (one home; do not restate). In one line: Search = find + read (sources.md + notes.md); Review = judge (verdict.md) or synthesize (landscape.md); Idea = generate (ideas.md) or novelty_check (verdict.md); `role:` picks the terminal within the type.

## The folder = one topic, one execution

```
Search folder                      Review folder                            Idea folder
discovery.yaml (type: Search)      discovery.yaml (type: Review, role)      discovery.yaml (type: Idea, role)
sources.md   (search)              sources.md  (work product, or            ideas.md | verdict.md
notes.md     (read)                notes.md     referenced from a Search)     (terminal, by role)
                                   verdict.md | landscape.md
```

IO mapping onto a task-folder:

| task-folder | discovery-folder |
|---|---|
| `{NN}_task.py` + `configs/<run>.yaml` | `discovery.yaml` |
| code build | `build/` (optional) |
| `results/<run>/` | `sources.md` · `notes.md` · terminal |
| `workflow/report.yaml` | `discovery.yaml` `report:` block |

## The chain — Search → Review → Idea

A heavy effort splits into typed folders chained by dependency, like `data-task → fit-task → eval-task`:

```
Search folder ─sources.md+notes.md→ Review folder ─landscape.md→ Idea folder
 (reusable source base)          (verdict/landscape)       (ideas)
```

`Search` is the reusable, accumulating source base; multiple `Review` (and `Idea`) folders read from it. A light effort skips the standalone `Search`: a `Review` folder's Execute searches + reads internally, WRITING `sources.md` + `notes.md` into its own folder as work products (they appear in `expected_outputs` alongside the terminal, but they are not terminals), and ends on its terminal. Build a standalone `Search` folder when the source base is reused across several analyses — exactly the reason task gives `data` its own type instead of folding it into `fit`.

## Agents (reused from task)

The task creator → reviewer loop transfers directly:

- **creator** drafts the Plan (`discovery.yaml`), runs Execute, drafts the Report.
- **reviewer** audits: search coverage, EVERY citation verified (Review Output Contract rule 5), the analysis matches the notes, claim scope not overstated.

Citation/synthesis audit is the highest-value gate in discovery (hallucinated references), and it comes for free from the task pattern.

## Self-contained by design

A discovery knows nothing outside its own folder: no `parent` field, no consumer tracking, no reference to any upper layer. It answers its question, writes its terminal, and stops. Whoever needs the terminal records the link on THEIR side; that is entirely their business, not this layer's.

## Command routing (v2)

```
/haipipe-discovery                         -> dashboard (list discovery-folders)
/haipipe-discovery open <type> <question>  -> scaffold a typed folder (type = Search | Review | Idea)
/haipipe-discovery plan    <discovery>     -> (re)write discovery.yaml
/haipipe-discovery build   <discovery>     -> author the optional instrument
/haipipe-discovery execute <discovery>     -> do the work, write the terminal file
/haipipe-discovery report  <discovery>     -> write report block + status + site
/haipipe-discovery <discovery>             -> run the full lifecycle on the folder
/haipipe-discovery <specialist> [args]     -> one-off bucket worker (NO folder)
```

**Retired**: the `open → search → read → review → post` verb-lifecycle. `search/read/review/idea` are no longer stage verbs. The stages are `Plan/Build/Execute/Report` (shared with task); the types are `Search/Review/Idea`. The three buckets (`1_search / 2_review / 3_idea`) are exactly one per type, each headed by a TYPE SPECIALIST skill (haipipe-discovery-search / -review / -idea, since v2.5.0) that Execute dispatches; the specialist picks among the capability workers beside it (the old 2_read bucket merged into 1_search in v2.3.0; novelty_check became an Idea role in v2.4.0).
