---
name: haipipe-probe
description: "Probe Console and claim-level evidence lifecycle. Opens a context-aware console for one active probe, then routes free-form user input through Plan -> Gather -> Read -> Judge -> Deposit. A probe is a claim-level evidence contract: it plans what claim needs evidence, gathers by calling missing task/discovery work or linking existing artifacts, reads linked evidence, judges claim support, and deposits the verdict into paper/application/insight memory. Trigger: probe, claim gap, evidence gap, hypothesis, link task, link discovery, judge claim, deposit verdict, Probe Console, /haipipe-probe."
argument-hint: "[console|plan|gather|read|judge|deposit|status] [probe_ref_or_path] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow, Task
metadata:
  version: "4.3.0"
  last_updated: "2026-06-23"
  summary: "Probe Console + lifecycle map: Plan, Gather, Read, Judge, Deposit."
  changelog:
    - "4.3.0 (2026-06-23): feedback-driven revision pass (14 items). (1) Plan: kind: field (atomic|comparison); comparison arms must be atom: links. (2) Gather: link+extract lightweight variant; fan-out model (1 probe : N discoveries : N tasks); naming rule (topic not verb); done-predicate strengthened (actual items, not evidence_plan); participant roster at Gather->Read boundary. (3) Read: elevated to stop-and-internalize gate (most participatory step); verdict-language ban in evidence.md. (4) Deposit: output readability template. (5) stage-strip.sh: fixed Gather false-positive (evidence_plan was Plan artifact, not Gather). (6) Dashboard: no-args view trimmed to compact glance. (7) Orchestrator agent: Write/Edit removed from tools (structural anti-monolith enforcement); dispatch prompts use coordinator language. (8) probe-yaml-schema: kind field, deposited status, deposit block heading."
    - "4.2.0 (2026-06-22): completed the Return->Deposit rename (artifact deposit.md, fn/deposit.md, probe.yaml deposit:/status: deposited/deposited_at/deposit_target; stage-strip predicate + accepts deposited|returned|closed). LEAN-ATOM MODE: a leaf probe declaring parent: logs Read/Judge/Deposit as yaml blocks (result:/verdict:/deposit:) and the strip reads them (yaml is disk). Deposit step now ALWAYS proposes the /haipipe-insight review handoff in next: (loop no longer implicit)."
    - "4.1.0 (2026-06-22): source-type letter in the probe ref. P.D<MMDD> discovery-sourced, P.T<MMDD> task-sourced (other source.type derives the letter from the primary evidence_plan kind). Folder becomes probes/<LETTER><MMDD>_<slug>/. Resolver accepts lettered + legacy letterless refs; existing letterless probes migrate lazily. See ref/probe-yaml-schema.md."
    - "4.0.1 (2026-06-22): rename lifecycle step Return -> Deposit (settle the judged verdict into durable memory); legacy command alias return kept; Read reframed as a present-and-internalize stop; Gather-done = participating tasks/discoveries have run, closed by a participant manifest."
    - "4.0.0 (2026-06-22): reframe probe around Probe Console and the concise lifecycle Plan/Gather/Read/Judge/Deposit; flat probe folders; group folders removed."
    - "3.3.0 (2026-06-21): delivery-need inputs from paper/application and verdict backfill."
    - "3.1.0 (2026-06-19): sandwich lifecycle around discoveries/tasks."
---

# Skill: haipipe-probe

`haipipe-probe` owns the **Probe Console** and the claim-level evidence
lifecycle.

A probe is not an execution unit. A probe is a claim-level evidence contract.
Tasks run code. Discoveries inspect outside evidence. Insights preserve judged
knowledge. The probe asks:

```text
Does the available evidence support this claim, under what scope, and with what caveats?
```

Read first:

```text
../PHILOSOPHY.md
ref/lifecycle-map.md
```

---

## Probe Console

`/haipipe-probe <probe>` opens a Probe Console: a context-aware working session
for one active probe.

The console:

```text
1. resolves the active probe
2. loads probe.yaml and lifecycle artifacts
3. renders status.md / a console panel
4. records active state in .probe-console.yaml
5. routes later free-form user input through the lifecycle
```

Console state is session state, not research evidence. Store active probe state
at the **project root**, defined as the nearest directory containing `probes/`
(for example `examples/ProjB-PhyTrait-OpioidRx/`, not necessarily the repo
root):

```text
.probe-console.yaml
```

Use `status.md` inside each probe folder for the human-readable panel.

---

## Lifecycle

Every probe has the same lifecycle:

```text
1. Plan   - define the claim and evidence needed to test it
2. Gather - call/link task & discovery work; DONE once they have run
3. Read   - present the gathered results; the USER internalizes them
4. Judge   - decide what claim the evidence supports
5. Deposit - settle the judged verdict into durable memory / backfill the source
```

`Plan` absorbs intake/framing. Users may enter a paper claim gap, application
question, task path, discovery note, insight card, or loose idea.

`Gather` has two internal actions, and a crisp done-line:

```text
Call    - create missing task/discovery work
Link    - attach existing task/discovery/insight artifacts
Extract - link + run a small extraction script (lighter than a full task; heavier
          than a plain link; reviewer spot-checks the output)
DONE    - every participating task AND discovery has FINISHED RUNNING (and every
          linked artifact resolves). Not "declared a ref" - actually ran.
```

One probe legitimately references N discoveries AND N tasks (fan-out model).
When Gather spans multiple sub-questions, split into N topic-folders (one
question per folder). Name folders by TOPIC, never by verb.

`Gather` closes by naming its participant roster: which tasks/discoveries
actually ran. That manifest is the handoff line into `Read`.

`Read` and `Judge` must stay separate, and `Read` is a STOP, not a silent summary:

```text
Read  = present the gathered results legibly; the USER internalizes them.
        The user's reaction is the input to Judge. (Most participatory step.)
Judge = what claim can we honestly make?
```

`Deposit` is not `Report`, and is distinct from `Judge`. Report makes a result
inspectable; `Judge` makes the claim; `Deposit` lets the judged verdict settle
into durable memory (insight KB) and backfills the source that needed it, so the
knowledge accrues. (Canonical verb `deposit`; legacy alias `return`.)

---

## Commands

```text
/haipipe-probe <probe>                  open Probe Console for probe
/haipipe-probe console <probe>          explicit console open
/haipipe-probe                          project-level probe dashboard / active console resume

/haipipe-probe plan <args...>           Plan: create or revise claim/evidence contract
/haipipe-probe gather <probe> <args...> Gather: call/link/check evidence
/haipipe-probe read <probe>             Read: present gathered results for the user to internalize
/haipipe-probe judge <probe>            Judge: structural + integrity + claim verdict
/haipipe-probe deposit <probe>          Deposit: settle verdict into memory / backfill source (alias: return)

/haipipe-probe status [<probe>]         render status panel
/haipipe-probe link <artifact>          alias: gather link in active console
/haipipe-probe call <kind> <need>       alias: gather call task|discovery
/haipipe-probe feedback "<text>"        capture skill feedback to feedback/ (fix later); `feedback list` shows open items
/haipipe-probe "<free text>"            route through active Probe Console if present
```

Legacy aliases remain valid:

```text
design   -> plan
bridge   -> gather call
dispatch -> gather call
harvest  -> read
post     -> read + judge
resume   -> read + judge
review   -> judge
file     -> gather link / plan, depending on input
return   -> deposit (lifecycle step renamed in 4.0.1; command alias kept)
```

---

## Skill Procedures

Each lifecycle verb has one procedure file:

```text
fn/console.md   Probe Console entrypoint and router
fn/plan.md      define/revise the claim and evidence contract
fn/gather.md    call missing work, link existing artifacts, check readiness
fn/read.md      present gathered results; the user internalizes them
fn/judge.md     decide claim support through independent gates
fn/deposit.md    Deposit: settle verdict into durable memory / backfill source
```

Legacy verbs (`design`/`bridge`/`harvest`/`dispatch`/`post`/`resume`/`review`/
`file`) have no separate files: the router maps them to the v4 procedures above
via the alias table in Commands, then reads that procedure.

Utility verb (not a lifecycle step):

```text
fn/feedback.md   capture skill feedback into feedback/ ; `feedback list` reviews open items
```

When implementing or revising a step, use the `Probe Lifecycle Map`:

```text
ref/lifecycle-map.md
```

---

## Probe Kind

Every probe has a `kind:` field set at Plan:

```text
atomic      one claim about ONE effect/comparison; single body of evidence; simple verdict
comparison  a claim ABOUT a relationship ACROSS atomic probes' verdicts; arms are atom: links
```

Heuristic: if the verdict needs "across N cohorts x M outcomes x K methods,"
it is a comparison sitting on TOP of atoms — split the atoms out.

A comparison probe's `evidence_plan.required` entries should be `atom:`
references to atomic probe verdicts, not raw task/discovery links.

## Probe Folder

Probe folders are flat. Do not create probe group folders.

Recommended project layout:

```text
probes/
├── _index.md
├── 0605_discretion-gradient/
│   ├── probe.yaml
│   ├── status.md
│   ├── evidence.md
│   ├── verdict.md
│   └── deposit.md
└── 0621_trait-diabetes/
    ├── probe.yaml
    ├── status.md
    ├── evidence.md
    ├── verdict.md
    └── deposit.md
```

File roles:

```text
probe.yaml  machine-readable contract, refs, structured result/verdict/deposit
status.md   human-readable Probe Console panel
evidence.md Read output: gathered results presented for the user to internalize
verdict.md  Judge output: claim support, confidence, caveats
deposit.md   Deposit output: where the verdict settled or should
```

**Lean atoms.** A leaf probe of a comparison decomposition (one that declares
`parent: <comparison-probe>`) may log its lifecycle COMPACTLY inside `probe.yaml`
(a `result:` block for Read, a `verdict:` block for Judge, a `deposit:` block for
Deposit) instead of writing separate `evidence.md`/`verdict.md`/`deposit.md`
files. The stage strip reads those yaml blocks for `parent:` atoms (yaml is still
disk). Full / comparison probes keep the human `.md` artifacts.

Optional:

```text
gather.md              only for complex call/link decisions
INTEGRITY_AUDIT.md     long independent integrity audit, when useful
CLAIMS_FROM_RESULTS.md claim-verifier output (Judge gate 3)
```

No code, notebooks, raw literature bodies, heavy result artifacts, or plots live
in probe folders. Those belong to task, discovery, or insight and are linked by
reference.

---

## Routing

Route arguments in this order:

```text
0. Resolve legacy-verb aliases to their v4 verb first (Commands alias table):
   design->plan, bridge/dispatch->gather, harvest->read, post/resume->read+judge,
   review->judge, file->gather/plan. There are no fn/<legacy>.md files.
1. If first token is a v4 lifecycle verb (or the utility verb `feedback`), read fn/<verb>.md and execute that procedure.
2. If first token resolves to a probe, open fn/console.md for that probe.
3. If active console exists and input is free text, route via fn/console.md.
4. If no active console exists and input is free text, route to fn/plan.md.
5. If no args, render project-level probe dashboard and active console state.
```

Resolver accepts (letter encodes source kind: D=discovery, T=task):

```text
P.D0622                          # lettered ref (current convention)
D0622                            # bare lettered id
probes/D0622_identity-concordance-steering/
P.0605 / 0605 / probes/0605_*/   # legacy letterless, still resolvable
```

Resolve relative to the active project root. If the current working directory is
inside a nested project, prefer that project's `probes/`. If multiple project
roots contain a matching probe ref, ask the user to choose.

If a probe ref appears only in `probes/FILING.md` as a proposal such as
`P.06xx_trait-diabetes`, do not treat it as an existing probe. Ask whether to
create/select the actual probe before linking artifacts.

---

## Boundaries

```text
task      executes internal work
discovery checks outside evidence
insight   stores judged knowledge
probe     plans, gathers, reads, judges, and deposits claim-level verdicts
```

Probe may call task/discovery during `Gather`. Probe may call insight during
`Deposit`. Probe does not execute code, search literature bodies directly, or
store final paper prose as its own artifact.

For artifact-first inputs, `Gather` must apply `ref/probe-attach.md` before
editing `evidence_refs`. If the artifact does not strongly match the active
probe, propose an existing/new probe and ask before changing anything.

---

## Copilot Policy

Default mode is `copilot`.

The Probe Console may automatically:

```text
read files
summarize status
classify user input
suggest link targets
detect missing evidence
draft evidence/verdict/deposit text
```

It must ask before:

```text
creating costly tasks
running PHI/full-data work
changing the claim target
declaring a final yes/no verdict
editing paper/application text
filing insight memory as accepted knowledge
```

Auto mode should be implemented later as a policy on the same lifecycle, not as
a separate workflow.

---

## Return Contract

Every procedure returns a short tail:

```text
status:    ok | blocked | failed
summary:   1-3 sentences
artifacts: [paths read/written/created]
next:      suggested next command or question
```

### Closing stage strip

Like the paper console, every reply in an active Probe Console session CLOSES
with the lifecycle stage strip as the VERY LAST line, AFTER the return-contract
tail above. Render it deterministically with the helper, never hand-typed:

```sh
sh "$CLAUDE_SKILL_DIR/ref/stage-strip.sh" probes/<probe>
```

It prints 1-2 lines, e.g.
`Plan ✅ ─ Gather ▶️ ─ Read ⬜ ─ Judge ⬜ ─ Deposit ⬜   ⚠ drift` plus a
`← here <step>: <why>` frontier reason. This is derive-from-disk: a step is ✅
only when its artifact resolves on disk, and a stale linked ref shows `⚠ drift`,
so the strip surfaces drift the stored `probe.yaml` would hide. The strip closes
EVERY reply in the session, not just the first console open. (`fn/console.md`
step 8 also pastes it as the `status.md` panel header; both placements use this
same helper output.)
