---
name: haipipe-design-workflow
description: >-
  Native Design workflow inside one stable Design Folder: write and release a
  bounded Commission, generate immutable candidate Results, independently
  verify them, render reviewable previews, and record a person's exact adoption.
  Coordinates with—but never impersonates—the Folder's Page workflow.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-13"
---

# /haipipe-design-workflow · commission bets, adopt exact results

## Version governance

This Design family remains pre-1.0. Only explicit user approval may authorize
`1.0.0` or any higher major version. Architecture size, clean breaks, and
field-test repairs do not independently authorize a major-version jump.

Load `haipipe-design`, `haipipe-folder`, `haipipe-run`, and
[run-profile.md](references/run-profile.md). The stable DS Folder owns both
faces. These stages create no Card, Unit, Verdict, Division, or round Folder.

## Design phase map

| Phase | Work object | Allowed Runs | Gate | Terminal evidence |
|---|---|---|---|---|
| Commission | written bet + frozen config | none | person releases exact version | immutable release receipt |
| Generate | one released unit/set/sequence | `Design.generate` | Result integrity + full self-check pass | N generation Results or truthful non-success |
| Verify | named generation Results | `Design.verify` | fresh independent context + complete coverage | J review Results; pass or fail is honest completion |
| Adopt | exact verified members + preview | none | person chooses/declines exact versions | immutable adoption receipt |

Expected Design Run count is `N + J`, not messages, drafts, tool calls,
renders, Page Runs, or stage-controller passes. A renderer/model call inside a
worker is not another Run. A separately commissioned Display task keeps its own
native identity.

## Commission and release

1. Resolve the current Brief, audience × job × venue, Folder owner, and Board
   `reads:`. Reject non-current Design shapes instead of migrating them.
2. Write the Commission under `outline/` and compile defaults into one frozen
   per-Run config under `scripts/config/`. Include `design_intent`, exact input
   roles/hashes, target, output scope, criteria, mode, and iteration budget.
3. Check that the bet is honest for its mode. Grant is permission, not warrant:
   release cannot turn inspiration, a forecast, or unsigned material into
   evidence.
4. Present the exact existing set. Only a person may release it. A changed term
   requires a new immutable receipt/config version.
5. After release, allocate the next monotonic `rdNN_*` Ticket plus planned
   `runtime.yaml`. Proposals and unreleased rows receive no Run id.

## Generate and verify

1. Validate Ticket inputs with the unit checker; hold only dependent work.
2. Record running/start time, then dispatch `haipipe-design-unit generate` or
   `verify`. Independent verification uses a genuinely fresh context whose
   actor differs from every target producer.
3. Validate the returned envelope, hashes, artifact count, check coverage, and
   substantive observations before recording terminal runtime.
4. Generate completes only on pass. Verify may complete with pass or fail when
   every check is settled; unresolved means blocked.
5. Preserve immutable completed Results. Changed candidate content, criteria,
   input, target, or feedback creates a new generation Run. `revise` pins exact
   base and feedback; it never edits the old DU.

## Render and adopt

Create a recipient-view preview in `delivery/render/` from exact DU/member
hashes. Rendering is review preparation, not adoption, Page release, shipping,
or a Design Run by default. If a preview is hand-edited, preserve it as feedback
and open a new revise Run; never promote the edited derivative over its source.

Present candidate differences, independent findings, preview, source scope,
and open gaps. A person may adopt a subset. The adoption receipt pins:

```text
DU Result + selected member hashes + verification Result(s)
+ render manifest/version + signed handoff versions + person's words/time
```

Review pass cannot adopt. Silence cannot adopt. Later changes stale only the
affected current binding and never erase the historical decision. Stop Design
work once the requested adoption/decline is recorded.

## Page interlock

The Design workflow and Page workflow share the Folder, not a phase machine:

| Change/request | Route | Why |
|---|---|---|
| candidate content or behavior | new Design generate/revise Run | changes the designed thing |
| independent candidate judgment | Design verify Run | judges immutable DU |
| Page structure or explanatory prose | `rp00` / paragraph Page Run | changes how the Folder explains |
| adopt candidate | Design adoption receipt | domain authority |
| publish Page projection | Page release → CONTENT | one adoption of accepted Page text |
| judge current Page projection | fresh Page CHECK | verifies projection/currentness |

`rp00_mermaid-structure` is mandatory for the Page sequence but never a Design
ideation stage. Page Runs cannot satisfy Commission release, generate/verify a
DU, or act as Design evidence. Conversely, a Design Result appears in the Page
surface under the Task Run lane with its native identity; it does not consume
an `rpNN` number.

The adoption receipt satisfies the Folder owner's `domain-gate`. Page CHECK
reuses it and must not solicit duplicate candidate acceptance. Page release
waits for any Design Result the Page promises to show, but an open Page Run does
not block unrelated released Design work.

## Evidence, recovery, and stop rules

- Design empirical authority pins a signed contextual W handoff. Do not invent
  an Insight Run id or launch upstream work from a Design Folder.
- Factual Page claims use `outline/evidence/`. PageX is not a valid Design
  address. A `rpNN` identity is never an evidence Run id.
- A failed/blocked attempt may resume only with unchanged inputs and append-only
  attempts. Material change allocates a new Run and may name `supersedes`.
- Never overwrite complete Results, hide rejected candidates, exceed the
  released budget, send, allocate traffic, or measure effectiveness.

## Status

Report two independent frontiers:

```text
design: <commission> · <Run/result/verdict> · <adoption/freshness> · next
page:   <rp00/rpNN/release/CHECK> · <projection freshness> · next
```

Then report the exact blocker or next bounded action. Do not compress them into
one scalar or count planned rows as Runs.

## Clean break

Only Commission → Generate → Verify → Adopt is routable. Reject D0–D5/GD0–GD6,
`design/DU*/`, PageX, v1 Ticket/Result schemas, and `rNN_design_*` identities.
Do not reinterpret, migrate, or continue them inside this workflow. Unsupported
Design bytes are not readable history, migration inputs, fallback evidence, or
compatibility surfaces. Stop content inspection after a decisive unsupported
marker; leaving unrelated files unchanged during an audit is not compatibility.
