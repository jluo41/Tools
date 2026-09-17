---
name: haipipe-design-unit
description: >-
  Generate, revise, or verify one bounded Design Unit from a frozen caller
  ticket. Returns a DU Result or a separate verification Result. Use for one
  message, sequence, candidate set, or UI unit; not for Board management,
  adoption, shipping, or measurement.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-13"
---

# /haipipe-design-unit · one commission, one inspectable result

Version governance: this Design skill stays at `0.4.0`. Only explicit user approval may authorize `1.0.0`.

## Version governance

This Design family remains pre-1.0. Only explicit user approval may authorize
`1.0.0` or any higher major version. Architecture size, clean breaks, and
field-test repairs do not independently authorize a major-version jump.

This is a worker like a display renderer, not a Folder/phase owner. The caller
owns the `rdNN_*` Run identity, input authority, release, scheduling, and
adoption.

Read [unit-contract.md](references/unit-contract.md) on every invocation.
Read [modes.md](references/modes.md) only for the selected mode. The caller
compiles and pins relevant venue rules; load only the selected venue pack
when a rule needs interpretation, never every venue or the entire Board.

## Entry

The logical operations are `generate <ticket>` and `verify <ticket>`.
These are skill instructions, not shell commands. Revision is generate with a
frozen base and feedback. A model/tool call is not
a Run by itself: the caller supplies a real Ticket and runtime receipt under
`haipipe-run`.

Resolve checker paths from this skill's directory, not the Design Folder.
Validate with `python3 scripts/check_unit.py --ticket <ticket>`. Read the
ticket's exact config and source files. Missing, stale, contradictory, or
unapproved inputs return a named hold. Never discover replacement evidence,
execute an upstream producer, or infer approval. A brief-only commission is
legal when explicitly configured and cannot claim measured effectiveness.
For every Ticket, read `design_intent` before creating content: it is the
commissioned bet, not evidence or permission to exceed the source boundary.

## Generate

1. Resolve what one DU contains: one message, a complete sequence, or an
   explicitly commissioned candidate set. Files, variants, internal drafts,
   and retries do not create extra Run identities.
2. Work only in the ticket's paired Result directory. Use the frozen config's
   goal, source roles, output contract, and criteria; never invent a passing
   rubric after seeing the output. For revision, read the exact base and
   feedback but do not edit the base.
3. Produce the selected mode's content in service of the frozen move. Treat
   evidence, inspiration, reference material, and avoid lists according to
   their roles. An intuition or forecast is not an observed finding. Do not
   back-fill `design_intent` after seeing the candidate.
4. Check the actual artifacts against every criterion. Use deterministic
   checks when possible. For visual criteria inspect the actual render.
   Semantic judgments name observable evidence; merely compiling a file or
   writing "pass" is not verification.
5. Iterate within the explicit budget. Preserve useful alternatives and check
   outcomes, not private chain-of-thought. If criteria conflict or the budget
   is exhausted, return the unmet criteria and leave a truthful partial Result.
6. Write the result envelope and checks defined by the contract; validate with
   `python3 scripts/check_unit.py --ticket <ticket> --result <result.yaml>`.
   Return exact paths, verdict, coverage, and gaps. The caller, not this worker,
   writes runtime lifecycle state and decides whether the Run is complete.

Self-checking belongs to this Run and never claims independent review.
Once complete, the DU is immutable. Later feedback requires a new Run.

## Verify

Read each target DU's pinned result manifest and its hash-bound artifacts.
Do not rewrite the targets, their checks, runtime, Page, or adoption record.
The verification output directory must be disjoint from every target.

Write a separate check for every target artifact × criterion pair, with
`pass | fail | unresolved`, observed evidence, and actionable findings.
A fully performed review may complete with a fail verdict; unresolved
required checks keep the review incomplete. Neither verdict means adopted.

For `review_mode: independent`, use an actual fresh reviewer context with an
identity distinct from each producer. A changed actor label alone is not
independence. The generator's self-check cannot satisfy this request.

## Boundaries

- The caller releases work, allocates Tickets, resolves upstream sources,
  records runtime, manages the Page, and adopts results. This worker does none
  of those invisibly.
- Page Runs never dispatch this worker and never become its evidence. Candidate
  feedback returns through a new revise Ticket; explanatory Page edits remain
  in the Page workflow.
- Write only the current output directory, never inputs or completed Results.
- Verification methods may be shared with generation, while independent
  reviewers remain independent executions.
- Never send, deploy, allocate traffic, or measure effectiveness here.
- Return operation, Run id, Result path, verdict, criterion coverage, and gaps.
  Structural validation alone is not a semantic or safety endorsement.

## Clean break

Accept only `haipipe.design-ticket/v2` with an `rdNN_generate_*` or
`rdNN_verify_*` identity. Reject v1, `rNN_design_*`, D0–D5 records,
`design/DU*/`, and PageX. They cannot be bases, references, verification
targets, or implicit authority for this worker. Unsupported Design bytes are
not readable history, migration inputs, fallback evidence, or compatibility
surfaces.
