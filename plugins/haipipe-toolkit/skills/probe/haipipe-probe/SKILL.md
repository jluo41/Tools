---
name: haipipe-probe
description: "Probe Console and claim-level evidence lifecycle. Opens a context-aware console for one active probe, then routes free-form user input through Plan -> Gather -> Read -> Judge -> Deposit. A probe is a claim-level evidence contract: it plans what claim needs evidence, gathers by calling missing task/discovery work or linking existing artifacts, reads linked evidence, judges claim support, and deposits the verdict into paper/application/insight memory. Trigger: probe, claim gap, evidence gap, hypothesis, link task, link discovery, judge claim, deposit verdict, Probe Console, /haipipe-probe."
argument-hint: "[console|plan|gather|read|judge|deposit|status] [probe_ref_or_path] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow, Task
metadata:
  version: "5.0.0"
  last_updated: "2026-07-02"
  summary: "Probe Console + lifecycle map: Plan, Gather, Read, Judge, Deposit. Full/light mode: full runs all 5 steps with insight deposit; light stops at Read for quick lookups. Section-edit gather workers route through light probes."
  changelog:
    - "5.0.0 (2026-07-02): added mode: full|light. Light probes stop at Read (no Judge, no Deposit, no insight cards). Escalation from light to full supported. Section-edit gather workers (citation, values, display) route evidence needs through light probes. Added Connection to Section-Edit section. Unwrapped hard-wrapped lines."
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

Every probe has the same lifecycle. Full-mode probes run all 5 steps; light-mode probes stop at Read.

```text
1. Plan    - define the claim and evidence needed to test it; set mode: full|light
2. Gather  - call/link task & discovery work; DONE once they have run
3. Read    - present the gathered results; the USER internalizes them
─── light probes STOP here (output → caller) ───────────────────────────
4. Judge   - decide what claim the evidence supports (full only)
5. Deposit - settle the judged verdict into durable memory / backfill the source (full only)
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
/haipipe-probe feedback "<text>"        capture skill feedback (MERGE-OR-CREATE), routed to agents/ (agent behavior) or orchestrator (everything else); `feedback list [unit]` / `feedback move <file> <unit>`
/haipipe-probe digest ["<session-name|id>"] [--dry-run]  digest a session (CURRENT, or a named/id'd PAST session): harvest feedback, dedup, confirm-gate, route to inboxes
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

Utility verbs (not lifecycle steps):

```text
fn/feedback.md   capture skill feedback, routed at capture to the unit it concerns
                 (agents/feedback/ for agent behavior, else the orchestrator
                 fallback haipipe-probe/feedback/); `feedback list [unit]` aggregates
                 across both inboxes; `feedback move <file> <unit>` re-routes
fn/digest.md     digest a session (CURRENT, or a named/id'd PAST session run from
                 a fresh context): scan the transcript for skill feedback, distill
                 + dedup discrete items, and after a MANDATORY confirm gate route
                 each through fn/feedback.md (merge-or-create). The bulk harvester
                 for feedback. Never auto-files.
```

When implementing or revising a step, use the `Probe Lifecycle Map`:

```text
ref/lifecycle-map.md
```

---

## Probe Mode: Full vs Light

Every probe has a `mode:` field set at Plan:

```text
full    Plan → Gather → Read → Judge → Deposit
        formal 3-gate judge, deposits verdict into insight KB (D/I/K/W cards),
        backfills the source that needed the evidence.

light   Plan → Gather → Read → DONE
        no formal judge, no deposit to insight KB.
        output goes directly to the caller (e.g., _CITATION_ entry, _VALUES_ entry).
        can ESCALATE to full later if the evidence turns out to need a formal verdict.
```

When to use each:

```text
full    H1/H2/H3 claims, reviewer objections, anything needing a formal verdict
        and durable knowledge in the insight KB. The probe ends with insight cards filed.

light   citation lookups ("find a paper for P2.S3"), number traces ("check this stat"),
        quick checks ("does gray2021 support this claim?"), section-edit gather needs.
        The probe ends at Read; the caller (section-edit-citation, section-edit-values)
        consumes the output directly.
```

Escalation: a light probe can continue into Judge → Deposit at any time. The user reads the evidence, decides it matters enough, and says "judge this" or "deposit this." The probe resumes from Read.

Default: `mode: full` unless the caller is a section-edit gather worker or the user says "quick check" / "just find me a paper."

## Probe Kind

Every probe has a `kind:` field set at Plan:

```text
atomic      one claim about ONE effect/comparison; single body of evidence; simple verdict
comparison  a claim ABOUT a relationship ACROSS atomic probes' verdicts; arms are atom: links
```

Heuristic: if the verdict needs "across N cohorts x M outcomes x K methods," it is a comparison sitting on TOP of atoms -- split the atoms out.

A comparison probe's `evidence_plan.required` entries should be `atom:` references to atomic probe verdicts, not raw task/discovery links.

## Probe Folder

Probe folders are flat. Do not create probe group folders.

Recommended project layout:

```text
probes/
├── _index.md
├── 0605_discretion-gradient/        ← full probe (5 files)
│   ├── probe.yaml                     mode: full
│   ├── status.md
│   ├── evidence.md
│   ├── verdict.md
│   └── deposit.md
├── 0621_trait-diabetes/             ← full probe
│   ├── probe.yaml                     mode: full
│   ├── status.md
│   ├── evidence.md
│   ├── verdict.md
│   └── deposit.md
└── 0702_lbp-discretion-cite/        ← light probe (3 files, no verdict/deposit)
    ├── probe.yaml                     mode: light
    ├── status.md
    └── evidence.md
```

File roles:

```text
probe.yaml   machine-readable contract, refs, structured result/verdict/deposit
status.md    human-readable Probe Console panel
evidence.md  Read output: gathered results presented for the user to internalize
verdict.md   Judge output: claim support, confidence, caveats (full only)
deposit.md   Deposit output: where the verdict settled (full only)
```

Light probes produce only `probe.yaml`, `status.md`, and `evidence.md`. If escalated to full, `verdict.md` and `deposit.md` are added at that point.

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
1. If first token is a v4 lifecycle verb, read fn/<verb>.md and execute that procedure.
1b. If first token is the utility verb `feedback`, read fn/feedback.md and run it
    inline (route it here before probe-ref resolution). Three sub-modes:
      - capture "<text>": infer the target UNIT -- agents (agent behavior) vs
        the orchestrator fallback (everything else). CROSS-CUTTING GUARD FIRST
        (a rule true across the whole lifecycle, or a named cross-cutting concern
        -> orchestrator fallback, overriding any agent keyword); else an agent
        keyword in the text -> agents/feedback/; else the active context from
        .probe-console.yaml; else orchestrator fallback. Write one dated file
        into THAT unit's feedback/ folder (create it + README if missing --
        agents/feedback/ is created lazily on the first agent item), then confirm
        where it landed + how it matched.
      - `feedback list [unit]`: aggregate open items across BOTH feedback/ inboxes
        under the probe skill root (agents + orchestrator), grouped by unit.
      - `feedback move <file> <unit>`: re-route a mis-filed item (unit = agents |
        orchestrator).
    Capture is MERGE-OR-CREATE: a same-topic complaint updates the existing inbox
    file (append a dated recurrence, preserve prior wording verbatim, reopen if it
    was fixed) instead of spawning a duplicate, so inboxes stay self-limiting. No
    fix on the spot.
1c. If first token is the utility verb `digest`, read fn/digest.md and run it
    inline (route it here before probe-ref resolution). RESOLVE THE SESSION FIRST:
    no arg -> the CURRENT session; a "<session-name|id>" arg -> that PAST session's
    transcript .jsonl (resolve per fn/digest.md "Resolving the target session", run
    from a fresh session for clean context). Then scan that session's transcript for
    tool/skill feedback, distill discrete items, dedup (within-batch + against
    inboxes via the same-topic test), PRESENT for a MANDATORY confirm gate, then
    route each approved item through the feedback capture (fn/feedback.md
    merge-or-create) in BATCH mode (no per-item re-confirm). Honor --dry-run
    (present only, file nothing). Flag global behavioral prefs for /remember rather
    than filing them. Never auto-files.
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
task      executes internal work (code, scripts, data processing)
discovery checks outside evidence (literature, prior art)
insight   stores judged knowledge (D/I/K/W cards)
probe     plans, gathers, reads, judges, and deposits claim-level verdicts
```

Probe may call task/discovery during `Gather`. Probe may call insight during `Deposit` (full mode only). Probe does not execute code, search literature bodies directly, or store final paper prose as its own artifact.

## Connection to Section-Edit Gather Workers

Section-edit gather workers (citation, values, display) route evidence needs through probe:

```text
section-edit-citation  →  light probe  →  discovery (search for papers)
section-edit-values    →  light probe  →  task (trace/recompute numbers)
section-edit-display   →  full probe   →  task (generate figures/tables)
```

The gather worker identifies what's needed (AUDIT phase). The probe handles the evidence lifecycle (Plan→Gather→Read). The gather worker consumes the probe's Read output (CANDIDATE/PLACE phases).

For quick lookups (single citation, number check), a light probe is sufficient. For claim-level evidence (H1 support, reviewer objection), escalate to full probe with Judge→Deposit.

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

## Feedback

`/haipipe-probe feedback "<text>"` captures a complaint / confusion / wish about
THIS skill (one dated file per item, `status: open`) to fix in a later revision
pass; it is feedback about the TOOL, not a probe verdict. Probe is the FLAT case:
capture-time routing sends each item to one of just two units. Feedback about
agent BEHAVIOR (orchestrator / creator / reviewer dispatch, monolithic collapse,
nested-agent hangs, creator/reviewer loop skipped, a reviewer's verdict enum,
broken independence) goes to `agents/feedback/`; everything else -- the lifecycle
procedures (Plan/Gather/Read/Judge/Deposit), the console/dashboard, the stage
strip, the return tail, probe id/naming/granularity, the venue editor-chair test,
compile-tex, any rule true across the whole lifecycle, or anything unclassifiable
-- falls back to the orchestrator's own `haipipe-probe/feedback/`. A CROSS-CUTTING
GUARD runs first (a lifecycle-wide rule or named cross-cutting concern -> fallback,
overriding any agent keyword). The folder IS the record of which unit it concerns;
there is no `skill:` field.

`/haipipe-probe feedback list [unit]` aggregates open items across BOTH inboxes
(unit = agents | orchestrator restricts to one); `/haipipe-probe feedback move
<file> <unit>` re-routes a mis-filed item. Capture is MERGE-OR-CREATE: a same-topic
complaint updates the existing file (append dated recurrence, preserve prior
wording verbatim, reopen if fixed) so inboxes stay self-limiting. Route a
`feedback` first-token here before probe-ref resolution. Full conventions:
`fn/feedback.md` (agent-keyword->unit map, inbox paths, cross-cutting guard,
merge-or-create, schema); fallback inbox: `feedback/README.md`; agents inbox:
`../agents/feedback/README.md`.

`/haipipe-probe digest ["<session-name|id>"] [--dry-run]` is the bulk harvester:
it digests a session -- the CURRENT one, or a named/id'd PAST session run from a
fresh context -- scanning the transcript for feedback you gave conversationally,
distilling discrete items, deduping them, and (after a mandatory confirm gate)
routing each through the same capture (in BATCH mode, no per-item re-confirm). It
files only skill-feedback; global behavioral preferences are flagged for
`/remember`, not filed. Route a `digest` first-token to it before probe-ref
resolution; resolve the target session first. Full conventions: `fn/feedback.md` (agent-keyword->unit map, inbox
paths, cross-cutting guard, merge-or-create, schema) and `fn/digest.md` (session
harvest).

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

## Behavioral Preferences (portable)

ALWAYS read and honor `PREFERENCES.md` in this skill's own folder: git-tracked
global behavioral preferences (e.g. communicate via ASCII diagrams) that survive a
machine change, unlike the machine-local `~/.claude` auto-memory. Global behavioral
prefs are kept in sync across all orchestrators by `/haipipe-paper digest`'s
global-pref fan-out (merge-or-create; one entry per topic).
