---
name: haipipe-paper-deliver
description: "Orchestrator for the paper delivery group (3-deliver) — everything downstream of the written argument. Routes the four verb-intent sub-groups to their leaf skills: build (structure the folder), audit (read-only findings), polish (mutate the draft), ship (produce & move the artifact). The artifact-side mirror of haipipe-paper-lifecycle (which owns the argument). Routing only; each leaf owns its own workflow. Trigger: build, scaffold, restructure, conform, audit, review, claim-audit, reviewer, optimizer, submission preflight, polish, consistency, format, typeset, ship, compile, diffpdf, overleaf, deliver, /haipipe-paper-deliver."
argument-hint: "[build|audit|polish|ship | <leaf-verb>] [paper-path-or-args...]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.0.1"
  last_updated: "2026-07-19"
  summary: "Router for 3-deliver, the artifact side of the paper. Four sub-groups by verb-intent: 1-build (scaffold/restructure/conform/folder — structure, zero prose), 2-audit (claim-audit/reviewer/optimizer — read-only findings), 3-polish (polish: consistency→format→typeset — mutate the draft), 4-ship (compile/diffpdf/to-overleaf — produce & move). Also THE home of the Lifecycle TeX Quality Standard (self-contained preamble, real prose, Pn.Sm tags, compile-after-every-mutation). Mirror of haipipe-paper-lifecycle; the top router delegates delivery intents here. History: ./CHANGELOG.md."
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

Lifecycle TeX Quality Standard
-------------------------------

THE single source of truth for the quality bar every compiled paper `.tex` must meet. Any skill that WRITES or EDITS one of those files — inside this group or upstream in `1-lifecycle/` — meets it at write time and edit time.

Scope: this standard applies to the DISPLAY stage (`0-lifecycle/4-display/4-display.tex`) and the section files (`0-sections/*.tex`) ONLY. All other lifecycle stages are markdown (`<stage>.md` + `_LOG_<stage>.md`) and do not compile.

Every compiled paper `.tex` (the display stage `4-display.tex` and `0-sections/*.tex`) is a **deliverable**, not a fragment or draft.

### Rules

**SELF-CONTAINED** -- every `.tex` has its own preamble and compiles directly to a same-name `.pdf`. No shell wrappers, no `\input`-fragment indirection.

Minimal preamble:

```latex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{parskip}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{xcolor}
\newcommand{\needprobe}[1]{\textcolor{red}{\textbf{[NEED PROBE]} #1}}
\title{N-stage: PaperName (Venue)}
\date{}
\begin{document}
\maketitle
...
\end{document}
```

The `\needprobe{}` macro marks claims lacking evidence with a visible red flag in the compiled PDF (see the Evidence Routing Protocol in `../../haipipe-paper/SKILL.md`). Remove it when the probe returns a verdict.

**REAL PROSE** -- content is rendered LaTeX prose with `\section*` headers, not `%%` comment blocks. A `.tex` that compiles to a blank page is a defect.

**SENTENCE-INDEXED** -- every sentence carries `%% ---- Pn.Sm ----` tags per `../../2-phase/REF/sentence-format.md`. Paragraph banners use the 3-line format:

```latex
% =========
% Para [file-slug.para-slug] Role -- point
% =========
```

`Pn` restarts per file, `Sm` restarts per paragraph. Tables (tabularx) get a banner but no per-sentence tags.

### Compile rule

After writing or editing a display or section `.tex`, compile it:

```sh
pdflatex -interaction=nonstopmode -output-directory <stage-dir> <stage.tex>
```

Run twice when cross-references or citations are present. Then clean aux:

```sh
rm -f <stage-dir>/*.aux <stage-dir>/*.log <stage-dir>/*.out
```

A stale PDF (tex newer than pdf) is a defect. The skill -- not the user -- is responsible for compiling after every tex mutation.

### .gitignore note

The display PDF is a **tracked deliverable**. `0-lifecycle/**/*.pdf` is NOT gitignored. Committing the refreshed PDF after a tex change is expected.

Return Contract
---------------

Capture the leaf's tail and present it:

```
status:    ok | blocked | failed
summary:   what the leaf did (2-3 sentences)
artifacts: [paths created, read, or modified]
next:      suggested next command
```
