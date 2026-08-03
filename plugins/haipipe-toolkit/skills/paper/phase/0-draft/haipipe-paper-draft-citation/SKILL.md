---
name: haipipe-paper-draft-citation
description: "DRAFT-phase citation auditor (internal). Reports assertions that need sources, real existing bib keys, and every remaining hole with its owning Q-consumer id. READ-ONLY: the DRAFT hub writes the manuscript and S-page Q-consumer; PROBE alone writes 1-probes/. Never searches or writes bibtex."
allowed-tools: Bash, Read, Grep, Glob
metadata:
  argument_hint: "[stage-or-section] [paper-path]"
  version: "0.1.2"
  last_updated: "2026-07-26"
  summary: "DRAFT-phase citation auditor: find every assertion that owes a source, report the real key when the .bib already has it, and report every remaining hole with the question that owes it. READ-ONLY; the hub writes. Acquisition is a question's job, not this skill's — it never searches. History: ./CHANGELOG.md."
---

haipipe-paper-draft-citation
=============================

The citation lane of the DRAFT phase.
Called by `haipipe-paper-draft` while it drafts a stage doc or a section.

One job: **no assertion leaves DRAFT owing a source to nobody.**


What this skill does NOT do
----------------------------

- It does NOT search. Finding a paper is a question's job: the ENTRY's `### q-executor` goes to `Agent(haipipe-discovery-orchestrator-agent)`.
- It does NOT generate bibtex and NEVER touches `0-*.bib`. Generated bibtex means hallucinated authors, wrong years, wrong journals, wrong pages — the failure is silent and survives into the submitted PDF.
- It does NOT verify a source (does the DOI resolve? does the paper actually say this?). That is `haipipe-paper-check-evidence`.
- It does NOT WRITE, anywhere. It walks and reports;
  `haipipe-paper-draft` writes the manuscript and Q-consumer, PROBE writes
  `1-probes/`, and `haipipe-paper-revise-place` places landed keys later.


AUDIT — what owes a source
---------------------------

Walk the working `.md` sentence by sentence. A sentence owes a source when it is a FACTUAL ASSERTION about the world that the paper is not itself establishing:

```
owes a source        a claim about prior work · a number taken from elsewhere ·
                     a named method with an origin · a field-level generalization
                     ("X is widely used", "prior work has not tested Y")
owes nothing         this paper's own result · its own design decision ·
                     a definition it stipulates · a transition sentence
```

Three gap types, and they are not interchangeable:

```
UNCITED        the assertion has no citation at all
WRONG-CONTEXT  a citation is present but does not support THIS claim
               (the source is real, the use is wrong — the hardest kind to see,
                and the kind a reader who knows the field will catch first)
WEAK           one citation carrying a claim that needs a body of work behind it
```

Only UNCITED is DRAFT's to close by raising a question. WRONG-CONTEXT and WEAK are judgments about a source you already have — flag them for `haipipe-paper-check-evidence` and move on.


PLACE what is already there
----------------------------

Before raising anything, grep the paper's `.bib`:

```sh
grep -in "<author-surname>\|<distinctive title word>" <paper>/0-*.bib
```

A key that greps → REPORT it as `\citep{key}`, with the line it belongs on. The hub places it.
A key that does NOT grep → it does not exist. Reporting it anyway is an invented citation, and it will not be caught until compile time, or later.


ROUTE — own every remaining hole
---------------------------------

Each surviving UNCITED assertion is REPORTED as one row:

```
<line>  |  <the assertion, quoted>  |  \cite{TOADD}  |  owed by: Q-<Stage>-<n> | UNOWNED
```

The hub writes it into the prose as `\cite{TOADD} [Q-<Stage>-<n>]`.

Two markers, side by side, never fused. The `\cite{}` is the citation layer; the `[Q-...]` is the question layer; their adjacency says *this key will come from that question*.

Finding the right `[Q-<Stage>-<n>]`, cheapest first:

```
1. an EXISTING Q-consumer in this stage doc would produce it
     → reuse its id. Most citation holes land here: a novelty question, a
       landscape question, a prior-art question already asks for exactly the
       anchors the prose is missing.
2. nothing would produce it
     → REPORT it back to haipipe-paper-draft as UNOWNED, naming the assertion and
       what would settle it. The hub raises the `## Q-<Stage>-<n>`; PROBE later
       finds or opens the entry. This lane writes neither file.
```

A bare `\cite{TOADD}` with no bracket is a defect. It means no question will ever produce that key — a hole with no owner, which is exactly the state DRAFT exists to prevent.


Done criteria
--------------

- [ ] Every factual assertion is reported as carrying a real `\citep{key}`, or as owing `\cite{TOADD}`
- [ ] Every `\citep{key}` greps in the paper's `.bib`
- [ ] Every `[Q-<Stage>-<n>]` names a Q-consumer that exists in the stage doc
- [ ] WRONG-CONTEXT / WEAK flags returned for the hub to record in the owning S page's `## Items to Finish` and `## Log`
- [ ] Nothing written anywhere — the report IS the output


Siblings
---------

```
haipipe-paper-draft            the hub that calls this
haipipe-paper-draft-values     the same shape for numbers  ({VAL:?} [Q-<Stage>-<n>])
haipipe-paper-draft-display    the same shape for displays (a DR row in the 4-display inbox)
haipipe-paper-probe            answers the questions this skill raised
haipipe-paper-revise-place     puts landed keys into the prose
haipipe-paper-check-evidence   verifies the sources pre-submission
```
