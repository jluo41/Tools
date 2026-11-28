---
name: hai-insight-workflow
description: 'Read the Insight ladder gates and route the next Run to its owning skill and agent. Covers question
  releases, prep code and Board execution. Trigger: insight workflow, next Run, run card, gate, /hai-insight
  workflow.'
disable-model-invocation: true
metadata:
  version: 3.1.0
  last_updated: '2026-11-27'
---

# /hai-insight workflow

Load `hai-insight` and `hai-run`. This skill routes work; each Run is performed by the skill and agent named on its card and signed only where that card requires a person.

## Sources

- `ref/run-cards.md`: Run labels, routing classification, patterns, owner, agent, signature and prompt.
- `scripts/run_cards.py`: the single card reader. `--check` validates the card and scaffold owners.
- `scripts/next_run.py <folder>`: read-only next-operation advice from current files.
- `hai-insight/ref/insight-ladder.md`: Block, version, member and execution contract.
- `hai-insight/ref/dataprep.md`: preparation code and the consuming Board's execution.

Card classifications describe routing. Current Studio top views and live Block navigation come from the shared workbench, not from the card's classification strings. Before dispatch, compare the card's prompt with the target's owning contract. Record any conflict and do not dispatch inconsistent instructions. Change a card through its owner and regenerate dependent output, then rerun the check.

For a DataPrep step, `hai-insight/ref/dataprep.md` governs the interface: expose `run(ctx)`, read declared context inputs and write only its allowed outputs. Do not introduce step-owned dataset configs or execute data inside the code step. The consuming Board's prep Task runs the chain.

## Determine what is next

Read the exact target, pins, reviews and Run records before recommending an operation. The next_run helper is advisory; compare its output with the file-backed gates, especially preparation pins and retained release members.

| Scope | What to check |
|---|---|
| Question Book | open proposals and the current version; triage a batch, then open or amend a version |
| Question version | complete release membership; needs agreed independently; compute scripts reviewed; question review; signed segments; person's release signature |
| Question definition | neutral ask → evidence plan → independent review → script where required → independent review |
| DataPrep version | ordered steps and declared interfaces → independent step reviews → signature and pinned hash |
| Insight Board | frozen data version, signed question/prep versions, distinct version combination and allowed single-version change |
| Board Job | prep ready output where required → Run tickets and power checks → readings → pages → CHECK → comparison → person's close |
| Answer Task | its required segment Runs or cited inputs, then answer, CHECK and alignment |

A refused Run with an evidenced reason is a completed computational outcome, not a missing Run. This does not waive page review or a human signature. A question with no compute need receives no artificial hard ticket.

## Gates

Commands check only their implemented conditions. Inspect the prerequisite evidence as well: independent review verdicts, segment consent and the person's explicit release decision. A successful command or completed review Run does not prove all gates passed; a returned review needs revision, and a placeholder collection is not a person's decision.

A question's needs and script are reviewed independently. Segments are fixed before outcome inspection. Signed question/prep versions are frozen and hashed. Data versions are frozen. A Board Job uses the named signed versions, a new combination and the allowed change from its predecessor. Preparation must produce ready output before dependent question Runs.

Power checks precede contrasts. A page is CHECKed independently. Closing requires the recorded reviews and required comparison, then the person's signature. Design receives only a signed handoff. A timer, loop or author's self-review cannot satisfy these gates.

## Dispatch

| Responsibility | Actor |
|---|---|
| asks, plans, writes and proposes | hai-insight-agent |
| reviews questions, evidence and alignment | hai-insight-reviewer-agent |
| CHECKs prose | hai-draft-check-agent |
| reviews scripts | hai-task-reviewer-agent |
| launches execution tickets | hai-task-orchestrator-agent |
| writes code | hai-task-creator-agent |
| signs segments, releases, prep, close and handoff | a person |

Follow the individual card when choosing its owner; the table explains responsibilities, not permission to run all work. A judge must not be the maker of what is judged.

## Return

Name the target, the exact unmet gate, supporting file, next operation and its owning card. For work status use the shared response-format Block map and actual Tasks/Runs. Keep Job/Task navigation inside the owning Block. Separate any action waiting on a person from work an agent can already do.
