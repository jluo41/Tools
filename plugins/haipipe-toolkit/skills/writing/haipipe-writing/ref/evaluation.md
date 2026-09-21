# Evaluate a writing candidate

Use [evaluation-rubric.md](evaluation-rubric.md) for base-v1 criteria and
verdicts. Include the target's resolved requirements and selected evaluator
adapters. Evaluate the actual candidate version, not an imagined improved one.

## Bounded cycle

1. Identify the candidate, recoverable baseline, rubric/version/hash, relevant
   requirements and review coverage. Label the actual reviewer and mode:
   self, external, or independent. Loading an external skill in the writer's
   context is still self-review.
2. Evaluate the applicable criteria with located text and evidence. Optional
   tools run only when selected. A tool's silence proves only what it checked.
3. In draft/revise mode, repair in-scope findings within the request's
   max_revision_passes (default 1). Restore an accidental change to a protected
   claim rather than inventing support. Return plan/evidence conflicts to their
   owner. In evaluate mode, make no edits even if a repair seems obvious.
4. After any repair, evaluate the changed candidate again, including protected
   content and affected seams. Keep initial findings against the initial text
   and final findings against the final text. Even at budget exhaustion, report
   the final evaluation. Stop on no progress or a missing required input.
5. Return ready-for-review, needs-work or blocked with the unresolved findings.
   Budget exhaustion with defects is needs-work; a required missing authority
   is blocked. Readiness never means human-accepted or independent-CHECK-passed.

Ordinary feedback continues in the same Run. The cycle's method calls and
review/revision passes are internal actions, not new Steps or Runs. A local
wording turn uses a narrow self-check and the existing effective packet, not a
new whole-Page review, corpus read or subagent. A pure acceptance/navigation
Step records its disposition without rewriting, rerating unchanged text, or
creating a Before/After card.

## Compact record

Save this in the current Step's review subsection or delegated Result trace;
do not require a new file/directory for every invocation. Reuse source refs
already retained by the host. Larger selected-tool output can be linked.

```markdown
#### Writing evaluation

- Candidate: <initial/final source or journal locator, version and SHA-256>
- Baseline: <recoverable prior text/record, or first draft>
- Rubric: haipipe-writing/base-v1 · <actual content hash>
- Requirements: <resolved source identities>
- Reviewer: <actual actor> · <self/external/independent>
- Coverage: <targets and criteria checked; explicit unreviewed scope>
- Methods: <id, entry/version/hash, status/output; or none selected>

| Pass/candidate | Criterion/source | Target/quote | Verdict | Evidence/reason | Smallest fix / owner |
|---|---|---|---|---|---|
| initial or final | <axis and requirement> | <actual locator/span> | <base verdict> | <observed basis> | <repair, owner, or none> |

- Revision budget: <used>/<allowed> · <not needed/completed/exhausted/stopped>
- Final disposition: <ready-for-review/needs-work/blocked>
- Unresolved: <findings/owners or none>
- Human acceptance: <reference only if actually supplied; otherwise pending>
```

If no revision occurs, one reviewed candidate serves as initial and final;
do not fabricate a second pass or a diff. If a candidate changes after review,
the verdict cannot transfer without checking its affected criteria. Numbers
such as 8/10 may only be added under an explicitly defined rating scale; never
substitute an intuitive score for the sourced criterion rows.
