<!-- TEMPLATE · haipipe-page-for-task 0.9.0
     Copy to <page>/<page-id>.md and delete each RULE comment as it is satisfied.
     A RULE comment left in a shipped page is an unfinished page.
     The base frame is haipipe-page; only what a TASK page adds is templated here. -->

# <the question this task-folder was run to answer, as a statement>
state: ⬜ NOT STARTED
owner: <who>
page-type: task
task-folder: tasks/<G><NN>_<group>/<NN>_<task>/
folder-kind: task
<!-- RULE · page-type is REQUIRED. A task page wears its folder's name and 31% of
     real folders do not match {NN}_<name>, so no filename shape can mark one. -->

## Opening
<!-- RULE · the ABSTRACT. One paragraph: what this page IS and why a reader
     should care. It is NOT the Introduction -- that is division 1 below, and
     since 0.9.0 a FLAT page has one. Opening orients; Introduction argues. -->

## Diagram
```text
  raw data ─▶ input ─▶ code ─▶ results        the task's IPO shape
```

## Content
<!-- RULE · Divisions open with ONE word from the closed set, before the first ` · `:
       Introduction · Concept · Landscape · Data · Method · Result · Conclusion
     The ORDER is fixed. The MULTIPLICITY is not: Landscape, Method and Result
     may each appear several times, one division per topic. Introduction does
     not repeat and is division 1 whenever it is written.
     Landscape holds what the FIELD already established -- it is written FROM
     the discovery layer's landscape.md, and it is where a route: discovery
     probe card lands. A literature claim is not a Method.

     PICK A SHAPE — the test is one question:
       "Does a second topic need its OWN Data or its OWN Method?"
         no  → FLAT   (the words ARE the divisions)
         yes → NESTED (a topic is the division, the words sit inside as ####)

     THE ARC that orders them is NOT this template's -- it belongs to
     haipipe-page-outline §🎭, which runs it as the OUTLINE phase's first check.
     The short version: for every adjacent pair, name why N must precede N+1,
     and a reason that is a date is not a reason. -->

### 1 · Introduction · <what this folder was run to settle, and what this report claims>
<!-- RULE · three things, in this order: the question the folder was run to
     answer; what was already established before it ran; what this report will
     claim. NOT a summary of the divisions below -- that is Conclusion's job. -->

### 2 · Data · <what went in, and the one fact about it a reader must know>
<!-- RULE · Machinery names are banned at division level: Inputs, Runs,
     Provenance, Run receipts. Those go in ## Files. The material survives; the
     heading does not. -->

### 3 · Method · <what was run, AND what it was run INSTEAD OF>
<!-- RULE · A Method title with no FORK has not been written yet. Every real one
     carries `and not`, `rather than`, or `deliberately`. "Plain description,
     deliberately: no model, no test" is a fork too. -->

### 4 · Result · <what came out — the finding, not the file it lives in>
<!-- RULE · Every shown number NAMES ITS RUN. A correct number with no run is a
     defect of the page.
     RULE · BY PATH, never by copy. results/ regenerates; a pasted number goes
     stale in silence. Carry a fingerprint (row count, date range, cohort n).
     RULE · A NEW RUN IS NOT A NEW DIVISION. It is a new READING row below.
     A new division is earned only when an existing title would become a lie. -->

### 5 · Result · <what is still NOT settled>
<!-- RULE · The residual is a DIVISION, not a footnote. Its role is Result: it is
     what came out, stated as the part that came out empty. A page with no
     residual either answered everything — rare enough to say out loud — or has
     not looked. Delete this division only in the first case. -->

### 6 · Conclusion · <what it means, and what to run next>
<!-- RULE · Exactly ONE, ALWAYS LAST, ALWAYS page-level, never inside a topic.
     RULE · A Conclusion with no READING record in it is NOT WRITTEN YET (0.8.0).
     RULE · No machine writes this division and no machine moves state: to ✅. -->

READING · <date> · <who read it>
<topic>        verdict-run <run>   ⬜ unread
<topic>        verdict-run <run>   ⬜ unread
answers        <which Aims are now answered>
not answered   <what these runs did NOT settle>
next run       <the run that would settle it, or "none: the question is dead">

## Aims
<!-- RULE · one Aim per question this task must answer. -->

## States
<!-- RULE · per question: answered · needs another run · dropped. -->

## Files
<!-- RULE · ALL machinery lives here, including every QA/<n>-<slug>.md by path.
     RULE · The <NAME> token binds the four sister files and is what makes
     "every number names its run" checkable:
       configs/<NAME>.yaml · runs/<NAME>.sh · results/<NAME>/ · notebooks/<NAME>.ipynb
     RULE · NEVER copy QA prose onto the page, and never edit a QA file from it.
     Listing them by path is the whole relationship. -->

## Law

## Log
