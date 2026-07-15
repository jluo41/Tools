Evidence Routing Protocol
=========================

Core rule: the paper owns the STORY and the JUDGMENT; the EXECUTORS (task and
discovery) own the EVIDENCE, and the probe is the map between them.
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
coauthor. Remove it when the answer lands (the section's `target:` resolves and its
`a-consumer:` is written) and the claim is backfilled with supported text.


Handoff protocol
----------------

When paper work surfaces an evidence gap, do the following INSTEAD of
investigating the data yourself:

  a. **STOP** investigating the data. Do not grep do-files, re-derive
     variables, or design the estimation.

  b. **Mark** the claim with \needprobe{description of what needs settling}.

  c. **Record** a delivery NEED (per delivery-need.md): the claim under test and
     what an answer would have to establish.

  d. **Raise** it as a question SECTION (`/haipipe-paper probe "<need>"`). The
     stage's PROBE phase MATCHes it against the bank, and dispatches only what
     MATCH cannot close. The paper TRIGGERS; it never runs the analysis (LAW 1).

  e. **Backfill**: when the answering QA file lands, write the section's
     `a-consumer:`, flip the claim's status in 1-claims.md, and remove the
     \needprobe{} flag.


The `probe` verb in the paper orchestrator
------------------------------------------

    /haipipe-paper probe <need-description>

opens a question SECTION in the right topic's probe file at `1-probes/`. The stage's
PROBE phase (haipipe-paper-probe) is what dispatches it — to
`Agent(haipipe-task-orchestrator-agent)` or `Agent(haipipe-discovery-orchestrator-agent)`,
carrying the section's `q-executor:` block and nothing else. The paper stays a story
layer; the executor does the work.


Heavy probes and subagent dispatch
----------------------------------

When a probe requires reading a lot of code/logs (e.g., cohort construction
from Stata do-files), dispatch it to a BACKGROUND SUBAGENT so the main paper
session keeps doing paper work:

  a. Add a beat to narrative/Methods for the topic (e.g., "Cohort
     construction"), marked \needprobe{} until the report lands.

  b. Raise the question SECTION (/haipipe-paper probe "<need>"), then let the
     PROBE phase dispatch its `q-executor:` with run_in_background=true.

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

Each of these may trigger its own \needprobe{} if the paper layer has no answering
QA file covering it. The EXECUTOR (not the paper) reads the do-files, inspects the
data, and returns the description.
