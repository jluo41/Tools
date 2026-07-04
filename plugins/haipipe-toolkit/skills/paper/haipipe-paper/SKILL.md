---
name: haipipe-paper
description: "Run any paper-lifecycle work. Use `/haipipe-paper enter <paper-path>` or `/haipipe-paper status [paper-path]` to preload an open-needs paper dashboard from STATUS.md, 0-lifecycle, 1-rounds, 0-displays, 0-sections, and git state. Paper lifecycle owns paper-specific story, angle, claims, narrative, displays, maturity, and dated work rounds; open GAP/NEED items accumulate as probe plans in 1-probe-plans/ and batch-dispatch to /haipipe-probe (the universal evidence gateway for claims; probe calls task/discover during Gather). Direct task/discover verbs available for non-claim utility work. Also parses intent (venue + stage) and dispatches to specialists for writing/revising/rebutting papers. Trigger: paper, enter paper, paper status, open needs, claim gap, figure table gap, round, paper round, work round, write paper, paper pipeline, paper writing, draft paper, revise paper, polish tex, rebuttal, reply to reviewers, probe, probe run, discover, task, evidence, 写论文, 论文流程, /haipipe-paper."
argument-hint: "[create|enter|status|venue|stage] [paper-path-or-args...]"
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "2.1.0"
  last_updated: "2026-07-03"
  summary: "Front door for the paper lifecycle: one verbs block, one routing pass, closing block, pointers to owners."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper (orchestrator)
====================================

User-facing entry for the paper lifecycle. The paper lifecycle is a delivery owner: it owns this paper's angle, claims, narrative, section map, displays, maturity, and dated work rounds. Project-level evidence lives outside the paper in probes, discoveries, tasks, and insights; when the paper hits a gap, record a delivery need (`../wiki/11-delivery-need.md`) and route to the evidence worker.

This orchestrator parses intent and dispatches to stage/specialist skills via `Skill()`. Stage skills internally drive the DPRC phase workers (`2-phase/`); users and this router never invoke phase skills directly. Canonical structure: `README.md` at the paper skill root + `../wiki/06-paper-skill-structure.md`.

ALWAYS read and honor `PREFERENCES.md` (this skill's own folder): portable, git-tracked global behavioral preferences that survive a machine change. `digest` / `feedback` append flagged global prefs there (merge-or-create).

Verbs
------

One block: verb, aliases and trigger keywords, then where it goes.

```
enter | status | dashboard | preload         -> haipipe-paper-enter (open-needs console; also "enter paper", "paper status", "aware mode")
create | folder                              -> create the paper folder (see Dispatch notes; also "create paper", "new paper folder", "scaffold paper folder")
venue | journal | 选刊 | any venue name       -> haipipe-paper-venue (recommend + pin; MISQ/ISR/Management Science/Nature/PNAS/JAMA/NEJM/Lancet/clinical/grant/patent all land here)
seed                                         -> haipipe-paper-lifecycle seed        (also "paper seed", "why this paper")
claims | claim | ledger                      -> haipipe-paper-lifecycle claims      (also "claim gap", "supported", "GAP", "H1/H2/H3")
pitch                                        -> haipipe-paper-lifecycle pitch       (also "cover letter", "one-minute story", "editor's chair")
narrative | story | contract                 -> haipipe-paper-lifecycle narrative
display | figures | figures-tables           -> haipipe-paper-lifecycle display     (also "figure plan", "gallery", "preview pdf")
section-edit | section | sec | §N            -> haipipe-paper-lifecycle section-edit (also write, edit, polish, draft, 写初稿, 整篇润色, "walk sections")
table | figure | plot | diagram |
  illustration | illustration-gemini |
  figure1 | framework                        -> haipipe-paper-lifecycle <renderer verb> (display renderer family; 做表/画图/架构图)
round | rounds                               -> haipipe-paper-round (dated work rounds; also "todo", "decisions", "applied")
probe ["<need>"] | probe | probe run [PPNN]  -> probe-plan buffer (BUFFER / SHOW / DISPATCH; also "evidence gap", "verify claim", "hypothesis")
discover ["<question>"]                      -> /haipipe-discovery (non-claim utility; also "lit review", "find papers", "related work")
task ["<contract>"]                          -> /haipipe-task (non-claim utility; also "run analysis", "compute", "implement")
rebuttal                                     -> haipipe-paper-rebuttal (also "reply to reviewers", "reviewer comments", "OpenReview response", "R1 revision")
feedback "<text>" | feedback list|move       -> fn/feedback.md (resolve BEFORE other parsing)
digest [session] [--dry-run]                 -> fn/digest.md   (resolve BEFORE other parsing)
"<natural language>"                         -> infer via the keywords above, dispatch
```

Examples:

```
/haipipe-paper create Paper-PhyPatSim --org jluo41
/haipipe-paper enter "examples/Project-PhyPat-Simulation/papers/Paper-PhyPatSim"
/haipipe-paper venue "physician trait -> opioid prescribing; observational CMS Medicare" --no-pin
/haipipe-paper claims
/haipipe-paper display "Table 1 + STROBE flow + subgroup forest"
/haipipe-paper probe "NEED-1: expand ex ante audit to all 20 messages"
/haipipe-paper probe run PP02
/haipipe-paper discover "AI-assisted precision nudging in IS literature"
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

A paper root is any directory upward containing `STATUS.md`, `0-lifecycle/`, `0-*.tex` + `0-sections/`, or `1-compile.sh` + `0-sections/`.

Venue coupling (drives two routing rules): seed + claims are venue-FREE; venue pins the journal in STATUS.md between claims and pitch; pitch/narrative/display/section-edit are venue-ALIGNED and consult `_venue/playbook-<venue>`. So: "paper" with claims done but no venue pinned -> run `venue` before pitch. Re-targeting ("move to another journal") -> re-run `venue`; pitch re-couples (new [primary], new RQ framing); claims stays unchanged.

Dispatch notes (only where non-obvious; everything else is `Skill("haipipe-paper-<target>")` or `Skill("haipipe-paper-lifecycle", args="<verb> ...")`):

```
create    Resolve the parent project (walk up from cwd, or ask). Project-* repo -> paper is REPO-BACKED:
          resolve --org FIRST (flag or ask, NEVER assume; the paper's owner may differ from the project's),
          follow the papers-inside recipe in project/haipipe-project/fn/repo-project.md, then
          Skill("haipipe-paper-lifecycle", args="folder <paper-path>"), then double-bump
          (paper push -> project pointer -> workspace pointer). Plain projects: just the folder + scaffold.
probe     Three sub-modes -- "<text>" BUFFER a plan file in 1-probe-plans/, no args SHOW the buffer,
          "run [PPNN]" DISPATCH planned probes via Skill("haipipe-probe", args="plan from-paper ...").
          The paper layer never runs probes itself; verdicts backfill into 1-claims / sections / round logs.
          Full buffer convention: fn/probe-plans.md.
discover  Resolve the project root, Skill("haipipe-discovery", args="<args> --project <project_root>").
task      Resolve the project root, Skill("haipipe-task", args="<args> --project <project_root>").
```

After dispatch, capture the specialist's structured tail (status / summary / artifacts / next) and present it.

> CC: write/edit 的老路由目标 haipipe-paper-edit-write / edit-weaving 在重构后已不存在（对应能力并入 2-phase/2-revise workers，由 stage 内部调用）。我把 write/edit/polish 这些词全部路由到 section-edit stage 了，对吗？还是这组动词干脆退休不再出现在 Verbs 块里？

Closing Block (end every reply)
--------------------------------

In a paper session, END every reply with ONE fenced `text` block: a titled top rule, the return-contract tail, a plain bottom rule, then the stage strip as the very last line. Marker semantics (🔥 = session's active stage, 🚀 = overall frontier, 🔥🚀 collapse) are owned by `../wiki/01-focus-strip-markers.md`; render the strip DETERMINISTICALLY with the helper, never hand-type it:

```sh
sh "$CLAUDE_SKILL_DIR/../wiki/10-stage-strip.sh" <paper-dir> [<session-stage>]
```

```text
── 📄 paper · claims 🔥 ───────────────────────
status:        ok|blocked|failed
paper_root:    <path>
current_layer: <layer>
next:          <single recommended command>
──────────────────────────────────────────────
seed ✅  claims 🚀  pitch ⬜  narrative ⬜  display ⬜  →  section-edit ⬜  →  review ⬜
```

Gate-aware: advancing `current_layer` requires an EXPLICIT user confirm that the current stage is done (Stage Gate, `../wiki/08-stage-gate.md`); once STATUS.md carries the gate ledger, ✅ means "user-confirmed". Every stage / enter skill inherits this closing block.

No-Arg Chooser
---------------

When no paper root is found, do not fan out. Emit a compact chooser (one line per entry; the Verbs block carries the detail):

```
📄 haipipe-paper: no paper detected. Pick an entry:
  create      /haipipe-paper create "<Paper-Name>" [--org <owner>]
  venue       /haipipe-paper venue "<topic or paper-path>" [--no-pin]
  enter       /haipipe-paper enter "<paper-path>"
  section-edit | rebuttal | probe | discover | task    (see /haipipe-paper help text above)
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

Paper work is demand-driven: a paragraph, claim, figure, or round todo may reveal that the next action is evidence work. The enter/status path surfaces those needs before recommending more writing. Need record schema: `../wiki/11-delivery-need.md`; paper/evidence boundary + `\needprobe{}`: `../wiki/12-evidence-routing.md`.

```
claim needs a verdict / robustness / literature / data artifact  -> /haipipe-paper probe "<need>"  (buffer first; probe gathers via task+discover, deposits verdicts)
figure/table needs materialized output (not claim-gated)         -> /haipipe-task-for-display <need>
closed evidence needs reusable meaning/caveat                    -> /haipipe-insight <artifact>
wording/section placement                                        -> the owning lifecycle stage skill
non-claim utility work (lit scan, data check)                    -> /haipipe-paper discover|task
```

For claim-related evidence, ALWAYS route through the probe buffer; direct discover/task verbs are for non-claim utility only. Resolved evidence backfills into `1-claims`, `4-display`, sections, or round logs. Evidence workers never own the paper story.

Structure Pointers
-------------------

Each area's internal contract lives with its owner; consult, never restate:

```
skill tree (0-enter / 1-lifecycle / 2-phase / 3-build-submit / 4-respond / 5-present / components / wiki)
                                   -> README.md (skill root) + ../wiki/06-paper-skill-structure.md
paper-folder layout                -> ../3-build-submit/_shared/paper-folder-anatomy.md (canonical tree, prefix semantics, maturity ladder)
lifecycle stages + venue coupling  -> ../wiki/03-paper-lifecycle.md + ../wiki/04-lifecycle-map.md
rounds                             -> ../wiki/07-paper-rounds.md
venue knowledge                    -> ../_venue/playbook-<venue> packs (venue is knowledge, not a pipeline)
```

Composing with Evidence Workers
--------------------------------

```
/haipipe-paper (router)
        ├─► /haipipe-paper-lifecycle    (seed -> claims -> [venue] -> pitch -> narrative -> display -> section-edit)
        ├─► /haipipe-paper-rebuttal     (any venue, post-review)
        │
        │   evidence workers (dispatched when a claim hits a gap):
        ├─► /haipipe-probe      (claim verdict; calls task/discover in its Gather, deposits to insight)
        ├─► /haipipe-discovery  (outside literature / context)
        └─► /haipipe-task       (run analysis / compute artifact)
            └── verdicts/artifacts backfill into 1-claims, sections, round logs
```

> CC: 原文这张图上游还列了 /idea-discovery /run-probe /auto-review-loop /result-to-claim 四个入口，skill 清单里已找不到，我删了。如果它们有新名字（或还想保留占位），告诉我补回。

> CC: 原文头部还有一处孤立引用（"读 lifecycle 参考时也读 ../1-lifecycle/haipipe-paper-display-figure/SKILL.md"），看不出为什么单点名 figure 渲染器，我也删了。有特殊用途的话说一声。

Feedback & Digest
------------------

`/haipipe-paper feedback "<text>"` captures a complaint/wish about THIS skill family, capture-time-routed into the concerned sub-skill's `feedback/` inbox (folder = the record; orchestrator inbox is the fallback), MERGE-OR-CREATE so inboxes stay self-limiting; `feedback list [skill]` aggregates, `feedback move <file> <skill>` re-routes. `/haipipe-paper digest [session] [--dry-run]` harvests a session transcript into discrete feedback items (dedup, mandatory confirm gate, then the same capture; global behavioral prefs fan out to every orchestrator's PREFERENCES.md instead of the inboxes). Full spec: `fn/feedback.md` + `fn/digest.md`; this section is a pointer, not the spec.
