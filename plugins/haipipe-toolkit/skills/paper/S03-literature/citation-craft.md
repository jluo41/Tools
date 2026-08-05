# Citation craft

Craft file for the paper family's citation lane, loaded by the DRAFT phase of any stage that declares it in its `stage.md` `craft:` list.
Source: converted from `workers/haipipe-paper-draft-citation/SKILL.md` on 2026-08-05 (thin-paper phase 2); it is DATA, not a registered skill.

One job: **no assertion leaves DRAFT owing a source to nobody.**

This lane is READ-ONLY. It walks and reports; the DRAFT phase writes the manuscript and the direct topic Q-consumer register, and PROBE alone writes nested entry pages.


What this lane does NOT do
---------------------------

- It does NOT search. Finding a paper is a question's job: the nested entry's `#### q-executor` goes to `Agent(haipipe-discovery-orchestrator-agent)`.
- It does NOT generate bibtex and NEVER touches `0-*.bib`. Generated bibtex means hallucinated authors, wrong years, wrong journals, wrong pages — the failure is silent and survives into the submitted PDF.
- It does NOT verify a source (does the DOI resolve? does the paper actually say this?). That is the check-evidence craft (`../S06-main/section-edit/check-evidence-craft.md`).
- It does NOT WRITE, anywhere. It walks and reports; the DRAFT phase writes the manuscript and Q-consumer register, PROBE writes nested S03/S04 entries, and the revise-place craft places landed keys later.


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

Only UNCITED is DRAFT's to close by raising a question. WRONG-CONTEXT and WEAK are judgments about a source you already have — flag them for the check-evidence craft and move on.


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
     → REPORT it back to the DRAFT phase as UNOWNED, naming the assertion and
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


Where the rest lives
---------------------

Phase dispatch and load order are owned by `board/page-phases/` (DRAFT loads this file last, after the type contract); the sibling lanes are `../S04-value/values-craft.md` (numbers), `../S05-display/display/draft-craft.md` (displays), `../S06-main/section-edit/revise-place-craft.md` (placement), and `../S06-main/section-edit/check-evidence-craft.md` (pre-submission verification); the probe loop that answers raised questions is `../haipipe-paper/probe/`.
