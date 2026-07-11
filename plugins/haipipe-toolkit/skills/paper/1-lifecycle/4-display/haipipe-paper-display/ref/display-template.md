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


Probes
------

Each probe is its own sub-item, numbered within its lane: `S` sweep (coverage first), `E` evidence (numbers come from tasks/probes, never typed by the agent), `R` render (candidates land in the unit's `candidates/`; `assets/` untouched until REVISE).
DRAFT proposes; PROBE executes on the user's verb -- nothing here runs until approved at the gate.
Status: `▶ ready` (runs at `probe`) · `✋ gated` (blocked until the user rules the named thread) · `done` (Outcome written in).
The user strikes entries at the gate ("skip En/Rn"); PROBE executes only what survives, then writes each Outcome.
Separated by `---` horizontal rules.

### S0 -- cross-stage coverage sweep -- ▶ ready

Lane: sweep.
Route: display PROBE step 0 -- read 3-narrative + every section md (+ its `_DISPLAY_` registry, `\input`/`\ref` uses).
Serves: map + inbox completeness.
Outcome: <PROBE writes the DR rows filed on each section's behalf>.

---

### E1 -- <title> -- <▶ ready | ✋ gated | done>

Lane: evidence.
Route: </haipipe-probe or /haipipe-task-for-display>.
Serves: <Fig/Tab N (displayNN-slug)>.
Gated on: <omit when ready; else the gating display subsection thread>.
Outcome: <PROBE writes the artifact path + one-line takeaway>.
Detail: `_PROBE/PPNN_<slug>.md`

---

### R1 -- <title> -- <▶ ready | ✋ gated | done>

Lane: render.
Route: </haipipe-paper-display-figure | -table | -diagram | -illustration>.
Serves: <Fig/Tab N (displayNN-slug)>, candidate <letter>.
Gated on: <omit when ready; else the gating display subsection thread>.
Outcome: <PROBE writes candidates/<letter>-<form>.<ext> + one-line self-assessment>.


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
