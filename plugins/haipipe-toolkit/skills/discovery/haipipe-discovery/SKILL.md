---
name: haipipe-discovery
description: "External-evidence layer. One research topic = one discovery-folder running Plan -> Build(opt) -> Execute -> Report, typed Search | Review | Idea; buckets 1_search/2_review/3_idea are the Execute workers, 1:1 with the types. Trigger: discover, find paper, lit review, 找idea, 查新, source, verdict, landscape, /haipipe-discovery."
argument-hint: "[verb|type] [discovery] [args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "2.6.0"
  last_updated: "2026-07-03"
  summary: "Two-axis discovery: uniform Plan/Build/Execute/Report lifecycle x 3 folder types (Search/Review/Idea), mirroring task. Each type has a specialist skill (haipipe-discovery-search/-review/-idea) heading its bucket. Self-contained folders (no parent field); contract = discovery.yaml + evidence files only."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-discovery (orchestrator)
======================================

Single entry for the discovery layer: what the outside world already knows (`Search` gather, `Review` analyze) and the new angles drawn from it (`Idea` create). Discovery is **external evidence work**, not a task execution stage. Durable evidence lives under `discoveries/`; whoever needs it references it from their own side — this layer never references upward.

Verbs
-----

```
/haipipe-discovery                              -> dashboard: render this verb list + the Model line, suggest the likely next command
/haipipe-discovery <discovery>                  -> run full lifecycle on a folder
/haipipe-discovery <discovery-group>            -> iterate/summarize children
/haipipe-discovery status [path]                -> read-only status
/haipipe-discovery open <type> <question>       -> scaffold a typed discovery-folder (type = Search | Review | Idea)
/haipipe-discovery open-group <slug>            -> ensure discovery-group dir
/haipipe-discovery plan <discovery>             -> (re)write discovery.yaml
/haipipe-discovery build <discovery>            -> author the optional instrument (build/)
/haipipe-discovery execute <discovery>          -> do the work, write the terminal file
/haipipe-discovery report <discovery>           -> append the report block + log event
/haipipe-discovery feedback "<text>" | list [unit] | move <file> <unit>   -> skill-feedback inbox (see Feedback)
/haipipe-discovery digest ["<session-name|id>"] [--dry-run]               -> harvest a session's feedback (see Feedback)

/haipipe-discovery <specialist> [args]          -> one-off worker dispatch (NO folder)
/haipipe-discovery "<natural language>"         -> infer + dispatch (Routing)
```

The Model
---------

Two axes, same as task: LIFECYCLE `Plan -> Build(opt) -> Execute -> Report` (uniform, process verbs) × TYPE `Search · Review · Idea` (folder kinds; each type maps 1:1 to its bucket). The type only changes what Execute produces:

```
Search   INPUT     search + read source material      -> sources.md + notes.md (reusable source base)
Review   PROCESS   judge a claim OR map a field       -> verdict.md (judge) / landscape.md (synthesize), role: picks
Idea     OUTPUT    generate ideas OR check novelty    -> ideas.md (idea_generation) / verdict.md (novelty_check)
```

The CANONICAL contract lives in ONE place — per-stage IO and the chain: `ref/lifecycle-map.md`; fields, roles, terminal templates: `ref/discovery-yaml-schema.md`. Do not restate them here. A one-off capability call does NOT create a folder; the discovery-folder is only for durable, project-tracked topics — the same split as a quick script vs a scaffolded task-folder.

Hierarchy
---------

```
discoveries/<GROUP>/<NN>_<topic>/   -> one research topic per folder, e.g.:

├── L01_personality-prescribing-landscape/  (landscape / context work)
│   ├── 01_empathy-agreeableness-outcomes/   (Review, landscape_review -> landscape.md)
│   └── 02_trait-signal-novelty/             (Idea, novelty_check -> verdict.md)
└── P01_trait-opioid-prior-art/             (claim evidence)
    ├── 01_trait-rx-source-base/             (Search -> sources.md + notes.md)
    └── 02_agreeableness-rx-prior-art/       (Review, prior_art_check -> verdict.md)
```


Group letters are purpose hints, not the source of truth (`type:`/`role:` in discovery.yaml are authoritative). Three purposes, one routing question each:

```
S  source base        just building a pile of sources?           (mostly Search)
L  landscape          understanding a field / context?           (mostly Review synthesize, Idea)
P  proof / prior art  testing a specific claim against outside?  (mostly Review judge, Search)
```

Buckets (Execute-stage workers)
-------------------------------

Three buckets, 1:1 with the types, each HEADED by a type-specialist skill that owns that type's Execute procedure and output contracts (the Review Output Contract lives in haipipe-discovery-review) and picks among the workers beside it:

```
1_search   /haipipe-discovery-search   fetch AND read -> sources.md + notes.md
  arxiv (preprints) · semantic-scholar (venues+citations) · exa-search (broad web)
  alphaxiv (fast read) · deepxiv (section read) · paper-analyzer (deep note)

2_review   /haipipe-discovery-review   judge -> verdict.md, synthesize -> landscape.md
  research-lit (default) · comm-lit-review (comms domain) · academic-researcher (cross-discipline)

3_idea     /haipipe-discovery-idea     generate -> ideas.md, novelty_check -> verdict.md
  idea-creator (brainstorm + rank) · novelty-check (查新)
```

Bucket aliases: `1|search`, `2|review`, `3|idea|novelty`. (Reading is part of searching — no separate `read` alias.)

Routing
-------

```
1. First positional is a lifecycle verb (open / open-group / plan / build / execute / report / status)
     -> durable operation on the folder. `feedback` and `digest` route to fn/feedback.md /
        fn/digest.md BEFORE any other parsing; neither scaffolds a folder.
2. First positional is an existing path: discovery-folder -> run requested stage or full
     lifecycle; discovery-group -> iterate/summarize children.
3. `open <type>` where type ∈ {Search, Review, Idea} -> scaffold that typed folder.
4. First positional is a specialist name -> dispatch that worker (one-off, NO folder).
5. arXiv ID / URL in args -> a 1_search read worker:
     "summarize|explain" -> alphaxiv ; "section|layered" -> deepxiv ; "analyze|claims" -> paper-analyzer
     bare ID, no verb -> alphaxiv
6. First positional is a bucket alias -> use that bucket.
7. Keyword scan (pick a worker for a one-off, or infer a folder type):
     "preprint|arxiv"                          -> arxiv            (Search)
     "IEEE|ACM|venue|citation"                 -> semantic-scholar (Search)
     "web|blog|news|exa"                       -> exa-search       (Search)
     "review|survey|landscape|map the field|related work" -> research-lit (Review synthesize)
     "prior art|is X known|does X exist|already done"     -> Review judge (verdict)
     "novelty|is this idea new|查新"            -> novelty-check    (Idea, role novelty_check)
     "brainstorm|find idea|找idea|propose"      -> idea-creator     (Idea)
8. Bucket resolved, specialist unresolved -> bucket default
     (1_search: arxiv to find, alphaxiv to read one paper | 2_review: research-lit | 3_idea: idea-creator).
9. Nothing resolves -> ask: Search (gather) / Review (judge or map) / Idea (generate or check)?
```

Dispatch: `Skill(<specialist>, args="...")`; do not auto-chain. Type-level work goes to the type specialists — they pick workers and carry the output contracts.

Protocol (durable project work)
-------------------------------

Walk the lifecycle stages; never hand-place a completed discovery package.

```
Step 0  Resolve project root = nearest ancestor with tasks/, paper/, applications/, probes/, or _haipipe/.
        If ambiguous, ask (AUTO -> blocked).
Step 1  Resolve scope: folder (has discovery.yaml) -> run stage(s); group -> iterate;
        open-group -> create container; open <type> <question> -> scaffold; specialist -> one-off.
Step 2  Group: purpose letter (S/L/P) + next free two-digit id (no renumbering).
Step 3  Folder: next free NN_<slug>/ in the group. One topic per folder; slug names the TOPIC.
Step 4  Run the stages (each owns its files):
        Plan     write discovery.yaml (type + role + question + sources + expected_outputs);
                 NO parent field — self-contained; append discovery.opened to _haipipe/project.log.jsonl
        Build    (optional) author the instrument under build/; set status building
        Execute  dispatch the TYPE SKILL — Search -> haipipe-discovery-search,
                 Review -> haipipe-discovery-review, Idea -> haipipe-discovery-idea;
                 inspect local project evidence first unless fresh web search was asked; set status executing
        Report   APPEND the report: block (absent until now; outcome != lifecycle status);
                 set top-level status (ok / inconclusive / blocked);
                 append discovery.completed to the project log
        Handoff  return the terminal path to the caller; the CALLER records the link on its
                 own side and appends discovery.consumed — the discovery records nothing upward
Step 5  Return: {status, discovery_group, discovery_folder, type, files_written, next}.
```

Feedback
--------

`feedback` / `digest` are utility verbs about THIS skill (not about discovery findings); capture-only — fixing is a later revision pass. Full contract: `fn/feedback.md` + `fn/digest.md`; fallback inbox: `feedback/README.md`.

```
capture  feedback "<text>"   -> route to the unit's feedback/ inbox: cross-cutting guard first
                                (lifecycle/type-field/schema-wide -> THIS folder's feedback/),
                                else keyword -> unit, else active context, else fallback.
                                Units: 1_search · 2_review · 3_idea · agents. MERGE-OR-CREATE:
                                same-topic items update the existing file (dated recurrence,
                                verbatim history, reopen if fixed), never duplicate.
list     feedback list [unit] -> aggregate open items across ALL inboxes, grouped by unit.
move     feedback move <file> <unit> -> re-route a mis-filed item (pure file move).
digest   digest [session] [--dry-run] -> scan a session transcript (past by name/id, else current)
                                for conversational feedback; distill, dedup, MANDATORY confirm
                                gate, then route each item through capture. Global behavioral
                                prefs go to /remember, not inboxes.
```

Behavioral Preferences (portable)
---------------------------------

ALWAYS read and honor `PREFERENCES.md` in this skill's folder: git-tracked global behavioral preferences that survive a machine change, kept in sync across orchestrators by `/haipipe-paper digest`'s global-pref fan-out.
