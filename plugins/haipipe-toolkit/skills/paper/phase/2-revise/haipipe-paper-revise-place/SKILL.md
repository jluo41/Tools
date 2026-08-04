---
name: haipipe-paper-revise-place
description: "REVISE-phase placement worker (internal). Runs FIRST in the revise chain: for every placeholder whose owed answer has landed, substitute the real thing into the prose — `\\cite{TOADD} [Q-X-n]` → `\\citep{key}`, `{VAL:? value} [Q-X-n]` → the number, a done DR row → `\\input` + `\\ref`. Leaves untouched, and flags, every placeholder whose answer has not landed. Never verifies, never searches, never invents. Users invoke stage skills, not this skill directly."
allowed-tools: Bash, Read, Edit, Grep, Glob
metadata:
  argument_hint: "[stage-or-section] [paper-path]"
  version: "0.1.2"
  last_updated: "2026-07-26"
  summary: "REVISE-phase placement worker: substitute landed answers into the prose and discharge their brackets. Runs BEFORE content and humanizer, so those workers see final text rather than placeholders. A placeholder whose answer has not landed stays put and is flagged. History: ./CHANGELOG.md."
---

haipipe-paper-revise-place
===========================

> **Where this grammar was ruled.** This worker implements three rulings on the
> paper design board, and it may not drift from them without that board changing
> first: `QC1@paper` the citation (and its HUMAN-ONLY `.bib` boundary, which is
> why this worker may place a key and may never write one), `QC2@paper` the value
> (a number binds to the RUN that produced it, not to a path), `QC3@paper` /
> `QC4@paper` the Display (a stable unit id, projected as `\ref{}`). The bracket
> `[Q-X-n]` is ONE join key shared by all of them, ruled once on `QC2@paper`, and
> it sits BESIDE its marker and is never fused into it.

The first worker in the REVISE chain.

DRAFT marked the holes and named their owners. PROBE brought the answers back into each entry's `#### a-executor`. This worker does the one remaining mechanical step: **put the landed answer where the placeholder is, and discharge the bracket.**


Why it runs FIRST
------------------

```
place → content → humanizer → results
```

Content and humanizer rewrite sentences. If placement ran after them, every substituted key and number would land in prose those workers had already closed — re-opening sentences the humanizer just finished, and forcing a second pass over text that was already final. Running de-AI over `{VAL:? held-out accuracy}` and then swapping in `0.87` afterwards means the sentence was never actually reviewed in the form that ships.

So: substitute first, then let the prose workers see the real text.


What this worker does NOT do
-----------------------------

- It does NOT verify. Whether the DOI resolves, whether the paper says what the sentence claims, whether the number re-derives — none of that is here. That is the pre-submission evidence check.
- It does NOT search, and does NOT re-run anything. If the answer has not landed, the hole stays a hole.
- It does NOT invent. There is no case where this worker writes a value or a key that it did not read out of a landed `#### a-executor` or the `.bib`.


The three substitutions
------------------------

For each placeholder in the working `.md`, resolve its `[Q-<Stage>-<n>]` through the direct topic register to the nested entry, and read that entry's `#### a-executor`.

```
CITATION   \cite{TOADD} [Q-X-n]
             ↓ the entry is `read` AND the key now greps in the paper's .bib
           \citep{key}                       ← bracket discharged
             ↓ the entry is `read` but no key is in the .bib yet
           leave it, flag it: the source landed but the .bib entry is owed

VALUE      {VAL:? mean MME difference, LBP cohort} [Q-X-n]
             ↓ the entry is `read` and its a-executor carries the number
           12.9 [Q-X-n]                      ← bracket KEPT, and a lane added
           > Value: <what the number is> · probe=<entry path> · run=<run id>
                    · state=verified
           Write the number at the precision the SOURCE states. Do not round
           to make a sentence read better; rounding is a claim about precision.

DISPLAY    a need whose DR row is `done` with its unit path filled
             ↓
           \input{displays/displayNN-slug/float.tex} + \ref{fig:...}
             ↓ the DR row is still `requested` or `accepted`
           leave it 📨 pending, flag it. NEVER pre-place a \ref for a unit that
           does not exist — it compiles to `??` and nothing downstream re-checks
           a reference that is already written.
```


The discharge rule
-------------------

A CITATION's bracket comes off; a VALUE's does not, and the two are asymmetric for a reason
that is mechanical rather than stylistic.

`\cite{TOADD} [Q-X-n]` → `\citep{key}` removes both markers together, because `\citep{key}` is
SELF-CHECKING: the key either greps in the paper's `.bib` or it does not, forever, with no
bracket needed. That is why a page of settled citations still reports every one of them.

A NUMBER has no such property. `12.9` is just digits, and the ONLY thing that ties it to the run
that produced it is the bracket, which is why `body.py` checks a prose number only on a sentence
that carries one. Discharging a value's bracket therefore does not tidy up a finished sentence,
it makes a verified number unverifiable, and the board goes dark on the work that is MOST
finished. Measured on MISQ 260727: `S-Main-0`'s headline `12.90` had been placed under the old
rule and reports nothing, while `S-Main-6`, which still carries its brackets, reports 41 markers.
The signal was inverted — brightest where least was done.

So a placed value keeps its bracket AND gains a `> Value:` lane naming the entry, the run and
`state=verified`. That is `QC0`'s S4 exactly, which is the worked example of a FINISHED sentence
and not of a pending one, and it is why `QC0` reports 3 numbers `ok`.

A bracket left standing over an unfilled placeholder is not a failure either — it is an accurate
statement that the hole is still open. Removing a bracket while leaving the placeholder is the
failure: the hole becomes unowned, and nothing will ever fill it.


Order of operations
--------------------

Edit the working `.md`, never the `.tex`. The `.md` is the document the human reads and comments in; tex follows at sync. This holds even though citation commands are the one LaTeX construct the `.md` legitimately carries.


Comments
---------

Leave `%% {CC-place}:` on any substitution that is not self-evident — a number whose precision was chosen, a key picked between two plausible candidates, a display placed against a claim it only partly covers. A pure `TOADD → \citep{key}` swap needs no comment.

Never touch a `> USER:` comment.


Done criteria
--------------

- [ ] Every placeholder whose entry is `read` and whose answer landed has been substituted, bracket discharged
- [ ] Every placeholder whose answer has NOT landed is untouched, bracket intact, and flagged in the `[REVISE]` entry in the owning S page's `## Log`
- [ ] No `\ref` written for a display unit that does not exist
- [ ] Every number written at its source's precision
- [ ] Every `\citep{key}` greps in the paper's `.bib`
- [ ] Working `.md` edited; `.tex` untouched until sync


Siblings
---------

```
haipipe-paper-revise             the hub that dispatches this first
haipipe-paper-revise-content     runs next — WHAT the sentences say
haipipe-paper-revise-humanizer   then — HOW they sound
haipipe-paper-revise-results     then — results narration
haipipe-paper-draft-{citation,values,display}   marked these holes and named their owners
haipipe-paper-probe              landed the answers into each `#### a-executor`
```
