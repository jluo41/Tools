# Probe Lifecycle Map

The Probe Lifecycle Map connects each lifecycle verb to its skill procedure,
questions, actions, file ownership, external calls, human output, machine state,
and stop gates.

## Map

| Step | Skill Procedure | Question | Action | Reads | Writes | External Calls | Human Output | Machine State | Stop / Gate |
|---|---|---|---|---|---|---|---|---|---|
| `Console` | `fn/console.md` | Which probe is active, and what can happen next? | Load context, render panel, route free-form input | `probe.yaml`, lifecycle files, linked refs | `.probe-console.yaml`, `status.md` | none | `status.md` / console panel | `.probe-console.yaml` | missing or ambiguous probe |
| `Plan` | `fn/plan.md` | What claim is being tested, and what evidence would settle it? | Intake input, resolve existing/new probe, define claim/evidence contract | user input, source refs, nearby probes | `probe.yaml`, `status.md` | none by default | `status.md` | `probe.yaml` | duplicate, unfalsifiable, unclear source |
| `Gather` | `fn/gather.md` | Is needed evidence missing or already present? | Call/Link/Extract evidence; emit participant roster when done | `probe.yaml`, candidate task/discovery/insight artifacts | `probe.yaml`, `status.md`, optional `gather.md` | `haipipe-task`, `haipipe-discovery` | `status.md`, participant roster, optional `gather.md` | `probe.yaml.evidence_refs`, `probe.yaml.calls` | costly/PHI work, ambiguous link, approval needed; DONE = all participants finished running |
| `Read` | `fn/read.md` | What did gathered evidence say? (STOP gate — user internalizes) | Present evidence legibly; STOP for user reaction; no verdict language | linked tasks/discoveries/insights, `probe.yaml` | `evidence.md`, `probe.yaml.result`, `status.md` | none | `evidence.md` (the internalize panel) | `probe.yaml.result` | Gather incomplete, missing evidence, malformed artifacts, ALWAYS stop after writing |
| `Judge` | `fn/judge.md` | What claim does the evidence honestly support? | Structural check, integrity audit, semantic verdict | `probe.yaml`, `evidence.md`, linked raw artifacts | `verdict.md`, `probe.yaml.verdict`, `status.md` | reviewer agents / Codex when available | `verdict.md` | `probe.yaml.verdict` | integrity fail, overclaim, insufficient evidence |
| `Deposit` | `fn/deposit.md` | Where should this verdict go? | Backfill source, file memory, or emit next need | `verdict.md`, `probe.yaml`, return target | `deposit.md`, `probe.yaml.deposit`, `status.md` | optional `haipipe-insight-*`; paper/application edits only with approval | `deposit.md` | `probe.yaml.deposit` | no target, user approval needed |

## File Principles

Use a minimal, flat probe folder:

```text
probe.yaml
status.md
evidence.md
verdict.md
deposit.md
```

Optional:

```text
gather.md
INTEGRITY_AUDIT.md
CLAIMS_FROM_RESULTS.md
```

Do not create probe group folders. Use tags and `_index.md` for organization.

Project root is the nearest directory containing `probes/`. Console state
`.probe-console.yaml` is written there, not necessarily at the repository root.

Artifact-first link requests must apply `ref/probe-attach.md` before editing
`probe.yaml.evidence_refs`.

## Command Routing

```text
/haipipe-probe <probe>          -> Console
/haipipe-probe console <probe>  -> Console
/haipipe-probe plan ...         -> Plan
/haipipe-probe gather ...       -> Gather
/haipipe-probe read <probe>     -> Read
/haipipe-probe judge <probe>    -> Judge
/haipipe-probe deposit <probe>  -> Deposit (alias: return)
/haipipe-probe "<free text>"    -> active Console router, else Plan
```

Legacy aliases:

```text
design   -> plan
bridge   -> gather call
dispatch -> gather call
harvest  -> read
post     -> read + judge
resume   -> read + judge
review   -> judge
file     -> gather link / plan
return   -> deposit (renamed 4.0.1)
```
