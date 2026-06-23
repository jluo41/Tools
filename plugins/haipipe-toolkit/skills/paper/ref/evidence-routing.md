Evidence Routing Protocol
=========================

Core rule: paper owns the STORY; probe (and task/discover) own the EVIDENCE.
When paper-lifecycle work hits a claim or wording whose support needs NEW
evidence, data/variable inspection, or an analysis that does not exist yet,
the paper layer must NOT dig into data, scripts, do-files, logs, or variable
definitions. Stop. Hand off. Mark the gap. Keep writing.


The \needprobe{} macro
----------------------

When a claim lacks evidence, mark it in the .tex with a visible red caveat:

    \newcommand{\needprobe}[1]{\textcolor{red}{\textbf{[NEED PROBE]} #1}}

Add this macro to the lifecycle preamble (or the paper's shared command file).
Use it inline wherever the gap lives:

    \needprobe{Is the intensive margin about patients already on opioids?}

The red flag renders in the compiled PDF so the gap is obvious to every
coauthor. Remove it when the probe returns a verdict and the claim is
backfilled with supported text.


Handoff protocol
----------------

When paper work surfaces an evidence gap, do the following INSTEAD of
investigating the data yourself:

  a. **STOP** investigating the data. Do not grep do-files, re-derive
     variables, or design the estimation.

  b. **Mark** the claim with \needprobe{description of what needs settling}.

  c. **Record** a delivery NEED (per delivery-need.md): the claim under test,
     what the probe must decide, and the expected output/verdict.

  d. **Route** to /haipipe-probe at the appropriate time. The paper TRIGGERS
     the probe; it does not run the analysis.

  e. **Backfill**: when the probe returns a verdict, fold it into the claim
     and remove the \needprobe{} flag.


The `probe` verb in the paper orchestrator
------------------------------------------

    /haipipe-paper probe <need-description>

dispatches to /haipipe-probe with the paper's project context pre-loaded.
This is a convenience shortcut -- the paper stays a story layer; probe does
the work.


Heavy probes and subagent dispatch
----------------------------------

When a probe requires reading a lot of code/logs (e.g., cohort construction
from Stata do-files), dispatch it to a BACKGROUND SUBAGENT so the main paper
session keeps doing paper work:

  a. Add a beat to narrative/Methods for the topic (e.g., "Cohort
     construction"), marked \needprobe{} until the report lands.

  b. Open the probe (/haipipe-probe plan), then run it via
     Agent(prompt=..., run_in_background=true).

  c. When the subagent report returns, fold it into Methods + Table 1 and
     flip the beat from \needprobe{} to supported.


Construction as a first-class beat
-----------------------------------

Dataset/cohort CONSTRUCTION is a first-class narrative/Methods beat, not a
one-line "Setting" aside. The narrative must account for:

  - inclusion/exclusion funnel
  - unit definition (what is one observation)
  - exposure -> outcome linkage
  - how each outcome, flag, and control variable is computed

Each of these may trigger its own \needprobe{} if the paper layer does not
already have a probe verdict covering it. The probe (not the paper) reads the
do-files, inspects the data, and returns the description.
