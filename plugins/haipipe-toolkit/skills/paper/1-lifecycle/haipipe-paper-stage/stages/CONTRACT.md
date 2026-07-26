# The stage contract form

What every `stages/<order>-<key>/stage.md` must declare, and what it may.

Read this before writing a new stage or changing an existing contract. `check-contracts.py`
enforces the required core and resolves every declared path; run it after any edit.

Two files describe a stage and they carry different costs. `index.yml` is read on EVERY
invocation, including ones that turn out to be about something else, so it holds only what is
needed to RESOLVE which stage is meant: `key`, `order`, `dir`, `triggers`, `migrated`. A
`stage.md` is loaded only for the stage actually picked, so it holds everything else. Nothing
belongs in the index that a router does not need in order to choose.

## The required core

Twenty-four fields appear in all eight contracts today. That is not an accident of drafting;
each one answers a question the router or the executor asks on every run. A contract missing
any of them is incomplete.

```
 IDENTITY        key            the router's handle, matching the index row
                 order          "0" 1a 1b 2a 2b "3" "4" "5" — execution order, matching the index
                 title          human name
                 one_line       THE one question this stage answers, as a question

 BOARD           board_family   Seed | Work | Venue | Display | Main | Appendix | Submission
                 board_unit     a number, or one uppercase letter for an appendix

 EXECUTION       phases         the ordered phase list; it must end with `check`
                 gates          which phases stop for a human; the default is [check]
                 probe_depth    the ceiling PROBE may spend on, on the bank's ladder (0..3)
                 runs           `once` for a single-artifact stage, `per-unit` otherwise
                 needs_paper    whether a paper root is required to run at all

 PRODUCT         artifact       the S face this stage writes. See the resolution rule below.
                 template       the scaffold DRAFT fills
                 sections       the artifact's parts, top to bottom
                 formatting     how the artifact is written, not what it says

 EVIDENCE        probes         where this stage's probe entries live
                 q_id_pattern   `Q-<Prefix>-<n>`, the stage's own question namespace
                 q_anchor       where a raised question is recorded in the artifact

 GRAPH           upstream       which stages this one reads, by key
                 downstream     which stages consume it, by key
                 handoff        what it passes on

 CLOSING         done_criteria  what CHECK verifies
                 closed_when    what makes the gate passable
                 exit_when      the stage's own failure exit
```

`upstream` and `downstream` are craft orientation, not a dependency graph. The authoritative
dependency declaration is the S page's own `requires:` (QF2), because that one carries the
upstream page's live gate state and cannot go stale.

## How `artifact:` resolves

The stage names the DIRECTORY and the identity. Board tooling owns the FILENAME (QC2), which
it composes as `S-<board_family>-<board_unit>-<board_slug>.md`.

```
 single-artifact stage   board_slug is a required field, and
                         artifact = <stage dir>/S-<family>-<unit>-<slug>.md
                         resolved once, at contract-writing time

 per-unit stage          board_family, board_unit and board_slug are PER UNIT, not per stage,
                         so the contract declares the PATTERN and the runtime resolves it:
                         artifact = <stage dir>/{unit}/S-{board_family}-{board_unit}-{board_slug}.md
```

Never hand-spell an S filename anywhere else. If a stage's artifact cannot be resolved because a
ruling is open, declare `blocked_on: <Q page>` beside it with the reason; `check-contracts.py`
then reports that path as KNOWN rather than passing it silently or failing it anonymously.

## Conditional fields

```
 venue_free XOR venue_aligned    every stage declares exactly one. Free survives a retarget to
                                 another journal; aligned is rewritten when the venue changes.
 board_slug                      required when `runs: once`; absent when `runs: per-unit`,
                                 because the slug belongs to the unit
 unit, units_from                required when `runs: per-unit`: what a unit IS, and where the
                                 unit list comes from
 blocked_on                      present only while a declared path cannot be resolved
 venue_contract                  present when the stage reads the venue blueprint before drafting
 generated, compiled, output     present when the stage produces a build product beside its
                                 artifact. A build product is never hand-edited.
```

Everything else is stage-specific and needs no permission to exist. Forty-three such fields are
in use today across the eight contracts, from `readiness_tags` to `display_split`. A field used
by one stage belongs in that stage's contract, not here.

## Craft prose belongs in the contract

Below the frontmatter, a contract carries prose about how to do the work well. That is
deliberate and it stays. The executor that reads the machine fields is the same one that must
do the work, and a split would let the two drift. The test is not length; it is whether the
prose is ABOUT THIS STAGE. Cross-stage rules live in `../../ref/`, and template fill rules live
inline in the template as `<!-- RULE: ... -->` comments, per `../../TEMPLATES.md` C1.

## Retired fields

```
 log:      retired 2026-07-26. It declared `_LOG_<stage>.md` on all eight stages and no live
           paper ever carried one. The S face holds current state, remaining work, and history
           in a single page, which is what the log was for.
 inputs:   retired by QF2. It was a hand-maintained reading list that had gone stale on every
           stage. Its dependency half became the page's `requires:`; its ordering half survives
           as the optional `read_order:`, which states sequence and cannot create a dependency.
```
