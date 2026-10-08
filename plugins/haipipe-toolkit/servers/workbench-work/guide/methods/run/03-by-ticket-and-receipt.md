By ticket and receipt
=====================

One Run method card. The Task workbench shows it in the shared Guide › Method, under the
Run methods; its papers are the rows of `../../../related/papers.md` whose `group` is
`by ticket and receipt`. A claim names its source in brackets; "(ours)" marks the
workbench's own judgment.

family: Run: How is each Result made, and can it be made again?
move: Every Result is written by one Ticket that runs one config, and the Ticket writes a
  receipt of what it ran; a wrong Result is fixed by changing the worker or config and
  rerunning the Ticket, never by editing the Result.
comes from: Sandve et al. 2013, ten simple rules; Moreau & Missier 2013, PROV; Pimentel et
  al. 2019, provenance from scripts
reads: the Ticket · its config · the worker
returns: one Result folder and its receipt
test now: T3 receipt
test in use: T4 generated


What the literature says
------------------------

rationale: Recording how every result was produced and keeping the exact scripts is what
  lets a result be made again [Sandve 2013]; a record of entity, activity and agent says
  which Run made which Result and who ran it [Moreau 2013]; provenance can be captured from
  scripts as they run [Pimentel 2019 provenance].
context: Reproducible computational research and provenance standards [Sandve 2013;
  Moreau 2013; Pimentel 2019 provenance].
steps: 1. The Ticket names its config and worker. 2. It runs them and writes the Result.
  3. It writes the receipt: status, start, finish, inputs and outputs. 4. A gate checks the
  required files.
strengths: Any Result can be traced to the exact code and config that wrote it, and
  rerun (ours).
limitations: A receipt records what ran, not whether it was right; that is the review's and
  the report's job (ours).


Applied to AI
-------------

agent: haipipe-task-orchestrator-agent runs the Ticket; it does not edit the Result.
steps: 1. Run the Ticket. 2. Read its receipt. 3. On a failure, route to Build, not to the
  Result.
returns: the Result folder and its complete receipt.
verify: The receipt is complete and every required Result file exists (T3); no Result
  file changed after the Ticket wrote it (T4).
risk: An agent may patch a wrong number in a Result to save a rerun (ours).
evidence on ai: No study tests receipt-gated runs by agents (ours).
skill: haipipe-task
