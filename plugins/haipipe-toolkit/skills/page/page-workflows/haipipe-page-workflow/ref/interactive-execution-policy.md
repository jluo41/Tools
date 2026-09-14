# Page interactive execution policy

This policy keeps human-feedback Steps responsive. It applies between Steps,
between Page Runs, and while preparing the next review packet.

## Two-minute foreground target

An ordinary wording-feedback Step is a small interactive edit with a target of
under two minutes. Its normal write set is the current Version journal,
`working.md`, `runtime.yaml`, and the candidate preview only when the live
Bullet Workspace needs that projection. A wording-only Step does not touch the
Page source, outline plan, evidence-item contracts, delivery, receipts,
changelogs, or skills. Make one bounded patch and do not create or wait for a
sub-agent in this path.

If the target slice or its current record cannot be found immediately, stop and
return one named blocker. Do not widen the read, invoke a full controller, or
repair unrelated state during the person's waiting time.

## Default foreground work

The default action is record-first and lightweight:

- read the Run resume view, the latest saved Result, the selected paragraph
  slice, its dependent Bullets, and the frozen Mermaid Structure description;
- save the verbatim feedback, the complete candidate, affected planning text,
  `working.md`, and `runtime.yaml`;
- perform one bounded file patch and one narrow hash, scope, or evidence check;
- return the review packet and stop for the person's next decision.

Do not silently add a build, export, browser session, full-page reread, broad
analysis, or background worker to this foreground path.

## Heavy work needs explicit approval

Before starting any non-trivial work between a Step and the next Step or Run,
show a short approval request with the exact action, reason, expected outputs,
and the files or external services it will touch. Wait for an explicit yes.

Heavy work includes:

- adopting Page Content or generating Web, LaTeX, Word, PDF, or other delivery;
- rebuilding the full Outline, Mermaid projection, Board, or phase controller;
- running the full test suite, broad browser verification, or an export audit;
- starting Discovery, citation search, figure production, rendering, data,
  computation, or any other delegated Task Run;
- launching post-run preference or feedback analysis that uses a sub-agent,
  background worker, or substantial model/tool budget.

An acceptance or a request for the next Run is not approval for any of these
actions. A prior approval is scoped to the named action and does not authorize
later work. If the person declines or does not answer, record the action as
`awaiting-approval` or `deferred`; it must not block the next lightweight
review packet.

The approval request should be concrete:

```text
Heavy action proposed: <one action>
Why now: <dependency or reason>
Will produce: <named Result or files>
Touches: <paths, services, or Task Run family>
Proceed?
```

## Post-run analysis

After a Page Run closes, prepare one analysis proposal from the immutable
Version hash. Do not dispatch it automatically when it is heavy. Ask for
approval using the same packet, then launch it as an output-only Task Run if
approved. The next Page Run may start immediately, and analysis never edits a
closed Version, accepted prose, Shape, shared policy, or delivery.

## Statuses

Use `deferred` when the action is not needed yet, `awaiting-approval` when the
person must decide, `running` only after approval, and `complete` or `failed`
after the named output is checked. A missing approval is not a failure.
