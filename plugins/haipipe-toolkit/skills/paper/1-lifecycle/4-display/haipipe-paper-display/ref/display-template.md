4-display -- <paper-slug>
=========================

Date: YYYY-MM-DD
Status: DRAFT

<NO markdown pipe tables anywhere in this doc (JL 2026-07-10) -- every would-be table is a list of record lines.>


Venue Set
---------

venue: <venue> (2-venue.md @ <commit>) -- <the venue's standard display set + hero rule>.
limits: <figure/table caps, color, format>
gallery config: width_cap=<0.6\textwidth> | float=<H> | <spacing knobs> | caption=<small>


Display Map
-----------

Row order = narrative order = gallery order; each display's `@<paper section>` must match its group below (a mismatch is a defect).

1. Figure 1 = display01-<slug> @<Intro/Theory> · <research model (HERO)> · claim <C1+C3> · status: <planned>
2. <Table 1 = displayNN-<slug> @<Methods> · <descriptives> · claim <C0> · status: <data-ready>>

<status vocabulary: planned -> data-ready -> candidates -> rendered -> input-ready -> inserted -> reviewed>


Q-consumer
----------

The evidence questions this stage raises — one `##` per question: id, title, what it wants.
Numbers come from tasks/probes, never typed by the agent. Route + approver are organized at APPROVE (into the probe file); the human strikes any question at the gate first.

## Q1 · <evidence title>
<what evidence/numbers this display needs, one sentence per line; which Fig/Tab it serves.>
<gated on: the display thread that must be ruled first, if any.>

## Q2 · <evidence title>
<...>

<APPROVE adds each `→ 1-probes/PPNN_<topic>.md` pointer + derived state.>


Render & sweep — display mechanics (NOT bank questions)
-------------------------------------------------------

These are the display stage's OWN steps, not questions to the bank; PROBE runs them on the user's verb, and the user may strike any at the gate. Status: `▶ ready` · `✋ gated` · `done`.

- **S0 · cross-stage coverage sweep** — display PROBE step 0: read 3-narrative + every section md (+ its `_DISPLAY_` registry, `\input`/`\ref` uses). Outcome: the DR rows filed on each section's behalf.
- **R<n> · render dispatch** — a candidate goes to a renderer skill (`/haipipe-paper-display-figure | -table | -diagram | -illustration`); candidates land in the unit's `candidates/` (`assets/` untouched until REVISE). Serves Fig/Tab N, candidate `<letter>`. Not dispatched to the bank.


<Paper Section, e.g. Intro & Theory>
------------------------------------

venue expects: <this paper section's display units from the 2-venue.md Structural Blueprint; a mandated unit with no subsection below is a GAP -- say so here>

### Figure 1 -- display01-<slug>

claim: <C1+C3> | status: <planned>
takeaway: <what the reader learns in five seconds -- one sentence>
evidence: <source path + producing task/probe, or "concept (no data)">
candidates:
- A <AI illustration> via /haipipe-paper-display-illustration -> candidates/A-illus.png · verdict: <empty until PROBE fills it>
- B <vector diagram> via /haipipe-paper-display-diagram -> candidates/B-model.svg · verdict:
sketch:
```text
  ┌────────┐        ┌───────────┐
  │ <X>    │ ─────► │ <Y>       │   (H1: β>0)
  └────────┘        └───────────┘
```
caption job: <what the caption must explain without overclaiming>
fragility: <what could make this stale or misleading>
> USER: <verbatim user thread lines -- never deleted, reworded, or relocated by the agent>
> CC: <agent reply underneath; only the user resolves; resolved threads MOVE to _LOG verbatim>


<Paper Section, e.g. Methods>
-----------------------------

venue expects: <e.g. "variable operationalization table (MANDATORY) + descriptives">

### <Figure/Table N> -- displayNN-<slug>

<same block shape as above>

<one `-----` group per paper section, in narrative order; one `###` subsection per display, in map order.
 The md's grouping mirrors the generated gallery one-to-one: group -> \section*{...} banner, subsection -> \subsection*{Figure N. ...}.
 A display's paper section is stated ONCE, by its group header -- the block carries only claim/status.
 Aligned plain text INSIDE a fenced sketch is fine (it sketches a LaTeX table); pipe tables as doc structure are not.>


Parking
-------

- <unit or legacy asset> -- parked: <why + when to reconcile>
