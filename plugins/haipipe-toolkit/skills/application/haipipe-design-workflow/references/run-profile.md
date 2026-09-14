# Design Run Profile · v4

ALLOWED: family `design`; operations `generate` and `verify`. `compose`,
`brainstorm`, `theory-driven`, `challenge`, and
`revise` are generation modes; revise pins frozen base + feedback.

TARGET: one independently closable unit (single, sequence, or candidate set),
or one independently closable verification over named DUs. Count N generation
+ J verification Runs. Do not count an umbrella, signature, render, Page Run,
workflow pass, model call, or internal draft.

TICKET: caller-authored
`<DS>/runs/<rdNN_generate|verify_slug>.yaml`, conforming to the unit worker's
`references/unit-contract.md`. `haipipe.design-ticket/v2` is the only accepted
schema. A YAML Ticket is a declared agent dialect, never a shell script.

INPUTS: the Ticket pins config, immutable release receipt, and exact file
references/hashes. Defaults are compiled before freeze. New v2 configs include
one `design_intent` bet. A source role does not elevate authority. A static
Brief, signed W handoff, or template has no invented Supporting Run id.
A real upstream Run retains its complete native identity. An `rpNN` Page Run is
never Design evidence or authority; preserved candidate feedback from it may be
pinned only with role `feedback` to a new revise Run.

WORKER: `haipipe-design-unit`, loaded by path
`../../haipipe-design-unit/SKILL.md` from this reference's
directory. The existing designer agent is a thin dispatcher into that worker.

RESULT: `<DS>/results/<Ticket-stem>/result.yaml`, `checks.yaml`, operation
payload, and caller-owned `runtime.yaml`. v2 Tickets produce v2 Results.
An allocated Ticket immediately owes planned runtime. New Result paths are
otherwise empty unless truthfully resuming one incomplete attempt. Completed
Results are immutable.

ACCEPT: Ticket gate + Result integrity + substantive commissioned checks.
Generate requires pass. Verify requires complete coverage; pass or fail may be
an honest completed judgment, unresolved is not. Self-check is never
independent verification.

PROMOTION: the caller records human adoption of exact DU/member hashes,
independent verification Results, preview manifest, and handoff versions. The
Design Page's owner gate consumes this same receipt; Page CHECK verifies the
projection and never duplicates the candidate decision. Selection, adoption,
Page release, and ordinary rendering mint no Design Run.

REOPEN: changed config, source, criteria, candidate content, target, or feedback
gets a new Run and may name `supersedes`. Preserve the old Result and decision.
An unchanged failed attempt may resume with an append-only attempt trail.

## Caller runtime receipt

```yaml
run: rd01_generate_sms
family: design
operation: generate
target: One SMS
status: complete
ticket: runs/rd01_generate_sms.yaml
result: results/rd01_generate_sms/
inputs:
  - {path: scripts/config/rd01_generate_sms.yaml, sha256: <config-hash>}
  - {path: outline/decisions/release-01.yaml, sha256: <release-hash>}
ticket_sha256: <hash-of-ticket>
worker: {kind: skill, name: haipipe-design-unit, actor: designer-context-01}
started_at: <ISO timestamp>
finished_at: <ISO timestamp>
failure: null
supersedes: null
```

`inputs` covers config, release, all declared inputs, and target manifests.
Actor/context provenance must be honest. Pin an immutable decision receipt,
not a growing log. The worker cannot advance runtime or human authority.

Audit a native Folder with:

```bash
python3 <haipipe-design-unit>/scripts/check_unit.py --folder <DS>
```

The Runs presenter projects Design identities under the Task Run lane. It does
not rename them Paper Runs or consume the Page's `rpNN` sequence.

The profile rejects v1 Ticket/Result schemas, `rNN_design_*`, D0–D5 folders,
`design/DU*/`, and PageX. There is no compatibility or migration route.
