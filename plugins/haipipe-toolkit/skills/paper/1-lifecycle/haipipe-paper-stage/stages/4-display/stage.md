---
# CONTRACT — machine-readable. No `name:` field: this is DATA the router reads,
# not a registered skill.
key: display
order: "4"
title: Display
one_line: "What evidence artifacts must the reader SEE, and are they ready?"
board_family: Display
board_unit: "0"

phases: [draft, probe, revise, check]
gates: [check]             # THE HUMAN GATES THIS STAGE OPENS, declared like `phases:`.
                           # Default is ONE, at CHECK. DRAFT/PROBE/REVISE run unattended.
                           # This is safe only because PROBE cannot spend: see probe_depth.
probe_depth: 0             # THE CEILING on what PROBE may dispatch, on the bank's own ladder
                           # (task/haipipe-task/fn/qa.md:102-107), which maps 1:1 onto the
                           # consumer's `bank:` verdict:
                           #   0 READ        reuse  results already answer it   free, nothing runs
                           #   1 NEW RUN     run    old script, new config      costs
                           #   2 NEW SCRIPT  code   must write new code         costs
                           #   3 NEW FOLDER  new    open a new task-folder      costs most
                           # Rule: dispatch when depth(bank) <= probe_depth, else DEFER.
                           # At 0 the stage can only HARVEST, so a run of it is free and needs
                           # no gate. Raise it per invocation with `probe --depth N`.
runs: once
needs_paper: true
venue_aligned: true       # rewrite the display set when the paper retargets

artifact: 0-lifecycle/3-display/4-display.md          # THE BRAIN — the only hand-edited stage file
blocked_on: QB2b            # ⚠️ DECLARED DANGLING. On the MISQ pilot this file is archived: its
                           # displays were split into eleven per-unit S-Display-<n> pages, each
                           # with its own gate. Repointing `artifact:` means adopting the per-unit
                           # grain, and `runs:` below still says `once`. QB2b owns that ruling.
                           # Declared here so check-contracts.py reports this path as KNOWN
                           # rather than passing silently or failing anonymously.
generated: 0-lifecycle/3-display/4-display.tex        # gallery, rebuilt wholesale by sync; hand-editing is a defect
compiled: 0-lifecycle/3-display/4-display.pdf         # compile from the PAPER ROOT so displays/ paths resolve
inbox: 0-lifecycle/3-display/_DISPLAY_REQUEST.md      # DR rows other stages file; only THIS stage advances their status
units: displays/displayNN-<slug>/                   # README + float.tex + preview + assets/ candidates/ source/ versions/
probes: 1-probes/PPNN_<topic>/
template: template.md
support: [figure-logic.md, checklist.md]

# ── BINDING — THE DISPLAY SPLIT (JL ruling 2026-07-21) ────────────────────────────
# A display unit has TWO halves with DIFFERENT OWNERS. The same wall the probe layer
# draws between a stake-free question and a stake-aware consumer runs through every
# table and figure.
#
#   BANK side  (task-folder · stake-free · reusable · LAW 1: the executor holds the pen)
#     · source_data.csv  the numbers, one row per cell, each carrying coef/SE/p/N and
#                        the source path + line it was parsed from
#     · metrics.json     the machine digest
#     · provenance       which run, which spec, which window, which log line
#     Produced by the TASK layer (haipipe-task-for-display), never by a paper stage.
#
#   CONSUMER side (displays/<unit>/ · stake-aware · venue-bound · THIS stage)
#     · WHICH rows/columns the argument needs, in what order, what is emphasised
#     · venue formatting: caption style, column rules, width, float placement
#     · \label / \ref wiring into the manuscript
#
# THE RULE: a consumer-side unit is GENERATED FROM the bank's source_data.csv.
#           Hand-typing numbers into a unit's .tex is a DEFECT, not a shortcut.
#
# WHY BINDING — the failure it exists to prevent, observed 2026-07-21:
#   a ruling flipped §6's primary exposure from the continuous score to the binary
#   indicator. The prose was updated; table3-main-results.tex was not, because its
#   numbers were hand-authored and nothing linked them back to the bank. The table
#   silently contradicted the text it supported, and only a manual display-lane sweep
#   caught it. A GENERATED unit makes that drift mechanically detectable; a hand-typed
#   one cannot.
#
# CONSEQUENCE FOR DR ROWS: a DR names BOTH halves — `bank deliverable:` and
#   `consumer deliverable:`. A DR naming only one is incomplete and may not be accepted.
#   Structurally a DR row IS the display-flavoured q-executor: same crossing, same
#   ownership rule, a different artifact shape.
display_split: binding

exit_when: "display cannot support claim"   # the stage's own failure exit

# THE COMMISSIONING ASYMMETRY — this stage is the reason this field exists.
# Display is the ONLY stage that hands units to workers; the four renderers stay
# independently registered skills, invoked by name, and are NOT part of this contract.
commissions: [haipipe-display-table, haipipe-display-figure, haipipe-display-diagram, haipipe-display-illustration]
worker_contract: ../../../4-display/ref/paper-adapter.md
                 # RELOCATED 2026-07-20. The four renderer skills read it as ../ref/…
                 # from their own folders; all 12 paths rewritten.

# VENUE-ALIGNED. Read the pinned venue contract BEFORE proposing any display:
#   0-lifecycle/2-venue/S-Venue-0-venue.md
#     · Structural Blueprint -> per-section `Display units` rows = the venue's standard set + hero rule
#     · Writing Principles   -> the display LIMITS (figure/table caps, table format, color rules)
# The `[primary]` claim's display is the hero. Fall back to venue/playbook-<venue> `-> Display`
# ONLY when S-Venue-0-venue.md is absent; never silently re-read packs behind a pinned contract.
venue_inputs: [Structural Blueprint display units, Writing Principles display limits]

sections:                 # in order
  - Venue Set             # venue's display set + limits + the gallery config knobs
  - Display Map           # one record line per display; row order = narrative order = gallery order
  - Q-consumer
  - Render & sweep        # this stage's OWN mechanics (S0 sweep, Rn render dispatches) — NOT bank questions
  - <one group per PAPER SECTION, in narrative order>   # each opens with `venue expects:`; each display a `###` subsection
  - Parking               # kept-but-unused; never \input into the manuscript

formatting:
  title_rule: "====="
  section_rule: "-----"
  headings: "`###` per display inside its paper-section group and per Render-&-sweep item;
             Q-consumer records are checklist items under `## Items to Finish`"
  line_breaks: "one sentence per line (semantic line breaks)"
  no_pipe_tables: "BINDING (JL 2026-07-10). Every would-be table is record lines. Aligned plain text INSIDE a fenced ASCII sketch is fine — it sketches a LaTeX table, it is not doc structure."
  mirroring: "the md's group/subsection tree mirrors the generated gallery's \\section*/\\subsection* one-to-one; a display's paper section is stated ONCE, by its group header"

q_id_pattern: "- [ ] 🔎 Q-Display-<n> · <title>"
q_anchor: "[Q-Display-<n>] cited inline in the display block whose evidence the question supplies"
closed_when: "REVISE lands the numbers in the rendered unit and discharges the [Q-Display-<n>] bracket"

status_vocabulary: [planned, data-ready, candidates, rendered, input-ready, inserted, reviewed]

done_criteria:
  - "4-display.md present; Display Map consistent with units on disk — no orphans either way"
  - "every display block carries claim, takeaway, evidence source, status, caption job, fragility"
  - "no block stuck at `candidates`: a winner is promoted with a recorded why per loser, or the block is parked"
  - "4-display.tex regenerated from the md; 4-display.pdf compiles from the paper root and is current"
  - "every display referenced in S-Venue-2-narrative.md; no _DISPLAY_REQUEST.md row left `requested`"
  - "Render & sweep items all terminal (Outcome filled, or struck by the user and logged); no `✋` item run while its gating thread was unruled"
  - "every display carries an independent interrogation verdict (keep-main | keep-supplement | fix | demote | cut)"
  - "checklist.md walked and all items pass"
  - "check-probe-cards.sh <paper_root> --stage display exits 0"

upstream: [narrative]
downstream: [section-edit]
handoff: "on CHECK confirm, append the gate row to this stage's S page ## Log -> section-edit"
---

Display — the craft
===================

A display item is not a file. It is a job:

```text
What claim does this display support?
Where does the evidence come from?
What should the reader learn in FIVE SECONDS?
Where does it appear in the paper?
Is it ready to \input into the manuscript?
```

A display that cannot answer all five is not a display, it is an image lying around.

The boundary with the stages either side:

```text
NARRATIVE     which beats does the argument need?
DISPLAY       which beats must be SEEN rather than told, and can we show them?
SECTION-EDIT  the prose around the display it is already handed.
```

The one stage that COMMISSIONS
------------------------------

Every other stage that wants a figure FILES A ROW and waits. Display is the only stage with the
authority to create a display unit, dispatch a renderer, or advance a `_DISPLAY_REQUEST.md` row.

```text
another stage needs a display  -> it writes a DR row into _DISPLAY_REQUEST.md, status: requested
this stage rules on the row    -> accepted (map row + block + unit) | declined (reason written back)
this stage delivers            -> done (unit: displays/displayNN-slug/) — now the section may \input it
```

That asymmetry is why `commissions:` exists. The four renderers — table, figure, diagram,
illustration — stay separate registered skills; this stage hands each a UNIT and a candidate row,
and they write back per the unit output contract. It never renders inline, and never lets another
stage render around it.

Numbers come from a task, never from the agent
----------------------------------------------

The hard line of this stage, and the one most often crossed under deadline. A data display's
asset is RENDERED from task-produced evidence on disk — a landed QA file's anchors, a parser's
`metrics.json`, a `source_data.csv` — and the rebuild spec in the unit's `source/` points back at
that task output. `float.tex` only ever REFERENCES the asset.

Numbers typed into `float.tex` are a placeholder, not a display. The test is not "are they
correct" — it is: **when the numbers change, can this display be regenerated?** If not, it cannot
be drafted; the need goes back through the evidence route. PHI rides along: raw data stays
server-side, only aggregates land in a unit's `source/`.

Concept figures (no data) skip the evidence route — but a study-flow, provenance, or CONSORT
diagram is annotated with REAL Ns from the data description, never hand-drawn ones.

Sketches are free; renders are expensive
----------------------------------------

Steer BEFORE rendering, not after. Every non-trivial display carries 2–3 lettered candidate
lines — genuinely different forms and routes, not three shades of the same bar chart:

```text
🖼  data plot        forest · dose-response · panel · box   -> the figure renderer, from the task's CSV/JSON
📋  LaTeX table      hypothesis tests · descriptives        -> the table renderer, from the task's aggregates
📐  vector diagram   research model · design · flow         -> the diagram renderer (elbow connectors, icons)
🎨  AI illustration  the richest Figure 1                   -> the illustration renderer
```

A settled form needs only one row. The hero/architecture figure earns 3–5 framework options
(pipeline chain, hub-and-spoke, layered stack, audit loop, feedback cycle) with pros/cons and the
reviewer friction each invites. Sketch each in ASCII with real numbers where known — a sketch
costs a minute and kills a bad figure before it costs an hour. Losers are not deleted; they keep
their history, so a reversed decision stays cheap.

Figure, table, or diagram — the selection judgement
---------------------------------------------------

Deeper craft in `figure-logic.md`; the load-bearing rules:

- **One dominant claim per main figure.** A figure that cannot be summarized in one clean
  sentence must be split, partly demoted to supplement, or rewritten around a clearer claim.
- **One role per panel** (claim-evidence · method bridge · validation · benchmark · consequence ·
  case · failure mode). A panel doing three jobs does none of them.
- **A figure-bearing claim should be SHOWN.** An effect with a shape — a gradient, an interaction,
  a CI that crosses zero — belongs in a figure, not only in a typed table.
- **Main vs supplement is a claim decision, not a space decision:** the main figure keeps what
  ESTABLISHES the core claim; robustness variants and secondary ablations move.
- **Form is a real trade only when the venue's budget makes it one.** Ask then, not by default.

The md is the brain; the tex is a view
--------------------------------------

`4-display.md` is the single working surface — map, blocks, candidates, sketches, decisions,
threads. `4-display.tex` is regenerated WHOLESALE from it, `\input`s each unit's `float.tex`, and
compiles to the gallery PDF. Hand-editing the tex is a defect; so is a stale PDF.
One brain, one file: do NOT add a separate contact-sheet or `preview-all` file — **the md's ASCII
sketches ARE the contact sheet**, and the gallery is the rendered view of the same tree.

Three things must not leak downward into a unit — units stay portable, comment-free, and natively
sized, because the MANUSCRIPT, not the gallery, is their real home:

```text
commentary  preferences and threads live in the md block only, never in unit files or the tex
sizing      width caps, float pinning, spacing live in the md's gallery config -> generated preamble
captions    they belong to float.tex — a caption baked into the image PDF cannot be renumbered
```

A display fails for reasons that are not visual
-----------------------------------------------

A compiled preview is not evidence. `pdflatex` exiting 0 proves the file is well-formed, not that
the display supports its claim — so the judge is never the builder. Display sits on the seam
between story and evidence, and fails on both sides:

```text
ugly            overflow · overlap · zero-width CIs · illegible labels    -> a render problem
mute            renders fine, teaches nothing in five seconds             -> a form problem
orphaned        no claim, no producing task, no section, no map row       -> a contract problem
stale           the claim, section role, or one-minute pitch moved        -> an UPSTREAM problem
```

The last one is why display is a manuscript LAYER and not a production step. When the pitch
changes, the hero figure changes — the plot was never wrong.

Not from the display stage
--------------------------

Do not MAKE the display here — the paper layer plans, it does not plot; the renderers plot.
Do not write the prose around a display: that is section-edit's, starting from the unit this
stage hands over.
Do not park a problem in the gallery — a display that cannot support its claim exits the stage
rather than shipping at `candidates` forever.
