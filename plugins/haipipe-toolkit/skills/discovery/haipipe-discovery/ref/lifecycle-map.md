# Discovery Lifecycle Map (v2 — two-axis, 3 types: 搜 析 创)

A discovery is one research topic stored as its own folder, a sibling of a task-folder. Discovery has the same two axes as task: a uniform lifecycle (Plan → Build(optional) → Execute → Report) crossed with a folder type. The three types follow an IPO shape — 搜 gather → 析 analyze → 创 create. This file is the CANONICAL contract for the discovery layer; do not restate it in SKILL.md or DESIGN.md, point here and edit here.

## Two axes (the model)

```
Axis 1 — LIFECYCLE (uniform; every folder runs it)   Plan → Build(opt) → Execute → Report   (English)
Axis 2 — TYPE      (what kind of folder this is)      搜 · 析 · 创                            (Chinese)
```

The type axis is named in Chinese single characters and the stage axis in English on purpose: different alphabets mean the two axes can never be mistaken for each other.

This mirrors task. Task = (Plan/Build/Execute/Report) × (data/nn/fit/...). Discovery = (Plan/Build/Execute/Report) × (搜/析/创). Every type runs every stage; the type only changes what Execute produces.

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
| **Report** | summarize results vs plan | report to a human: outcome, confidence, caveats, handoff | `discovery.yaml` report block + `status.yaml` + `site.md` |

File ownership is strict. Plan touches `discovery.yaml`. Build touches `build/`. Execute touches the work files. Report touches the report block + `status.yaml` + `site.md`.

## Axis 2 — the three types (IPO: gather → analyze → create)

| 字 | type | IPO role | Execute does | terminal | consumer |
|---|---|---|---|---|---|
| **搜** | source | INPUT | search + read source material | `sources.md` + `notes.md` | 析 / 创, and a reusable source library |
| **析** | analyze | PROCESS | judge a claim **or** map a field | `verdict.md` (判) / `landscape.md` (综) | **probe** (verdict) / **paper** (landscape) |
| **创** | create | OUTPUT | generate candidate claims | `ideas.md` | **probe-open** / **paper-seed** |

`析` is the only type whose terminal branches; `role:` decides verdict (判, a judgment) vs landscape (综, a map). `搜` merges the old search + read (they are always bound together, and the digested source set is a reusable, accumulating base). `创` stays separate because it is divergent (invent new) while 搜/析 are convergent (gather and organize what exists).

Role to type to terminal:

```
搜  source_gather, source_read                          -> sources.md (+ notes.md)
析  prior_art_check, counterevidence, novelty_check      -> verdict.md   (判, -> probe)
析  landscape_review, benchmark_landscape                -> landscape.md (综, -> paper)
创  idea_generation                                      -> ideas.md
```

## The folder = one topic, one execution

```
搜 folder                     析 folder                       创 folder
discovery.yaml (type: 搜)     discovery.yaml (type: 析, role)  discovery.yaml (type: 创)
sources.md   (search)         sources.md   (work product or   ideas.md     (Execute terminal)
notes.md     (read)           notes.md      referenced from 搜) status.yaml
status.yaml                   verdict.md | landscape.md        site.md
site.md                       status.yaml
                              site.md
```

IO mapping onto a task-folder:

| task-folder | discovery-folder |
|---|---|
| `{NN}_task.py` + `configs/<run>.yaml` | `discovery.yaml` |
| code build | `build/` (optional) |
| `results/<run>/` | `sources.md` · `notes.md` · terminal |
| `runtime.yaml` | `status.yaml` |
| `notebooks/<run>.ipynb` | `site.md` |
| `workflow/report.yaml` | `discovery.yaml` `report:` block |

## The chain — 搜 → 析 → 创

A heavy effort splits into typed folders chained by dependency, like `data-task → fit-task → eval-task`:

```
搜 folder ─sources.md+notes.md→ 析 folder ─landscape.md→ 创 folder
 (reusable source base)          (verdict/landscape)       (ideas)
```

`搜` is the reusable, accumulating source base; multiple `析` (and `创`) folders read from it. A light effort skips the standalone `搜`: an `析` folder's Execute searches + reads internally (dropping `sources.md` + `notes.md` as work products) and ends on its terminal. Build a standalone `搜` folder when the source base is reused across several analyses — exactly the reason task gives `data` its own type instead of folding it into `fit`.

## Agents (reused from task)

The task creator → reviewer loop transfers directly:

- **creator** drafts the Plan (`discovery.yaml`), runs Execute, drafts the Report.
- **reviewer** audits: search coverage, EVERY citation verified (Review Output Contract rule 5), the analysis matches the notes, claim scope not overstated.

Citation/synthesis audit is the highest-value gate in discovery (hallucinated references), and it comes for free from the task pattern.

## Parent model

```
Delivery-open (paper / application)  ->  析 (landscape / benchmark, 综) + 创 (ideas); 搜 for the source base
Probe-open                           ->  析 (verdict, 判: prior_art / counterevidence / novelty); 搜
```

## Command routing (v2)

```
/haipipe-discovery                         -> dashboard (list discovery-folders)
/haipipe-discovery open <type> <question>  -> scaffold a typed folder (type = 搜 | 析 | 创)
/haipipe-discovery plan    <discovery>     -> (re)write discovery.yaml
/haipipe-discovery build   <discovery>     -> author the optional instrument
/haipipe-discovery execute <discovery>     -> do the work, write the terminal file
/haipipe-discovery report  <discovery>     -> write report block + status + site
/haipipe-discovery <discovery>             -> run the full lifecycle on the folder
/haipipe-discovery <specialist> [args]     -> one-off bucket worker (NO folder)
```

**Retired**: the `open → search → read → review → post` verb-lifecycle. `search/read/review/idea` are no longer stage verbs. The stages are `Plan/Build/Execute/Report` (shared with task); the types are `搜/析/创`. The four capability buckets (`1_search / 2_read / 3_review / 4_idea`) remain the Execute-stage WORKERS: `搜` uses 1_search + 2_read, `析` uses 3_review, `创` uses 4_idea. Workers (4, capability) and types (3, purpose) are different axes.
