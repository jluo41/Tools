---
name: haipipe-paper-deliver
description: "Orchestrator for the paper delivery group (3-deliver) — everything downstream of the written argument. Routes the four verb-intent sub-groups to their leaf skills: build (structure the folder), audit (read-only findings), polish (mutate the draft), ship (produce & move the artifact). The artifact-side mirror of haipipe-paper-lifecycle (which owns the argument). Routing only; each leaf owns its own workflow. Trigger: build, scaffold, restructure, conform, audit, review, claim-audit, reviewer, optimizer, submission preflight, polish, consistency, format, typeset, ship, compile, diffpdf, overleaf, deliver, /haipipe-paper-deliver."
argument-hint: "[build|audit|polish|ship | <leaf-verb>] [paper-path-or-args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-07-17"
  summary: "Router for 3-deliver, the artifact side of the paper. Four sub-groups by verb-intent: 1-build (scaffold/restructure/conform/folder — structure, zero prose), 2-audit (claim-audit/reviewer/optimizer — read-only findings), 3-polish (polish: consistency→format→typeset — mutate the draft), 4-ship (compile/diffpdf/to-overleaf — produce & move). Mirror of haipipe-paper-lifecycle; the top router delegates delivery intents here. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-deliver (orchestrator)
============================================

User-facing entry for **paper artifact work** — everything downstream of the written argument: turn the plan into a physical folder, then get the draft submission-ready.
This is the artifact-side mirror of `haipipe-paper-lifecycle` (which owns the argument). The two together split the paper: **decide/write** the argument, **produce/deliver** the artifact.

The orchestrator owns routing only.
Each leaf specialist owns its own workflow, inputs, and outputs.
The orchestrator never scaffolds, audits, polishes, or compiles itself.

The four sub-groups (by verb-intent)
------------------------------------

```
1-build/    structure the folder, ZERO prose
   scaffold        plan → conforming empty skeleton (tex + dirs + 1-compile.sh)
   restructure     non-conforming paper → gold layout, prose byte-identical
   conform         conformance audit, report-only
   folder          minimal container (README + STATUS + dirs); the get-or-create bootstrap

2-audit/    read-only, produce findings (no mutation)
   claim-audit         every number/claim traces to raw results
   reviewer            formal reviewer-side evaluation
   optimizer           claim/evidence/terminology drift review + late-stage venue preflight

3-polish/   mutate the draft, whole-paper passes
   polish          one skill, three ordered passes: consistency → format → typeset

4-ship/     produce & move the artifact
   compile         LaTeX → PDF, diagnose & fix errors
   diffpdf         tracked-changes PDF (latexdiff style)
   to-overleaf     two-way Overleaf Git sync
```

Verbs
-----

Group verb (no leaf) opens that sub-group's chooser; a leaf verb dispatches straight through.

```
/haipipe-paper-deliver                                 -> dashboard (the four groups + their leaves)
/haipipe-paper-deliver build [<leaf>] <args>           -> 1-build/*   (leaf: scaffold | restructure | conform | folder)
/haipipe-paper-deliver audit [<leaf>] <args>           -> 2-audit/*   (leaf: claim-audit | reviewer | optimizer)
/haipipe-paper-deliver polish <args>                   -> 3-polish/haipipe-paper-polish (consistency → format → typeset)
/haipipe-paper-deliver ship [<leaf>] <args>            -> 4-ship/*    (leaf: compile | diffpdf | to-overleaf)
/haipipe-paper-deliver scaffold|restructure|conform|folder <args>       -> the named 1-build leaf
/haipipe-paper-deliver claim-audit|reviewer|optimizer <args>          -> the named 2-audit leaf
/haipipe-paper-deliver polish <args>                                 -> haipipe-paper-polish
/haipipe-paper-deliver compile|diffpdf|to-overleaf <args>             -> the named 4-ship leaf
/haipipe-paper-deliver "<natural language>"            -> infer the leaf, dispatch
```

Dispatch is `Skill("haipipe-paper-<leaf>")` (the leaf name, never a path). Every leaf name is unique across the group.

Routing
-------

Resolution order (first match wins):

```
1. first positional is a LEAF verb (scaffold, compile, ...)   -> that leaf
2. first positional is a GROUP verb (build|audit|polish|ship) -> if a second token names a leaf in that group, that leaf; else the group chooser
3. keyword scan over the phrase                               -> the most-specific leaf (a named skill wins over its group)
4. no args                                                    -> dashboard
5. input but target unclear                                   -> ASK; never guess a mutating leaf (restructure, polish change files)
```

Invariants (state them, do not re-implement — the leaves enforce them)
----------------------------------------------------------------------

- `1-build/` changes **no prose** (scaffold writes no sentences; restructure gates on prose + compile parity; conform writes nothing).
- `2-audit/` is **read-only** — it reports, never edits.
- `3-polish/` is where the draft is mutated; `4-ship/` produces and moves artifacts.
- Prose itself is written upstream, in `1-lifecycle/5-section-edit` (DRAFT/REVISE) — never here.

Return Contract
---------------

Capture the leaf's tail and present it:

```
status:    ok | blocked | failed
summary:   what the leaf did (2-3 sentences)
artifacts: [paths created, read, or modified]
next:      suggested next command
```
