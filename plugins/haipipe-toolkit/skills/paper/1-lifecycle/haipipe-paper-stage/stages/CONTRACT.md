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
                 on_rerun       what a SECOND run does to a page a human has edited.
                                Default and only currently legal value: `diff-and-ask`.
                                See "The second run" below. QB2c.

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

`sections:` describes the stage's LOGICAL product.
On a Board-first paper S page, every ordinary section becomes a direct `###`
division under `## Content`, while the logical `Q-consumer` section is adapted
into recognizable `- P<n> · Q-<Stage>-<n>` Aim records under
`## Aims`.
It is never emitted as a second `## Q-consumer` content block.
`create-page.py` enforces this adapter.

`upstream` and `downstream` are craft orientation, not a dependency graph. The authoritative
dependency declaration is the S page's own `requires:` (QF2), because that one carries the
upstream page's live gate state and cannot go stale.

## The second run

Every stage is run more than once. A venue change re-runs pitch, a returned probe answer re-runs
revise, a reviewer round reopens whole families. So `on_rerun:` answers the question that matters
most about a stage, which is not what its first run produces but what its second run does to a page
a human has already read, argued with, and commented on.

Ruled 2026-07-27 (QB2c). Before this field existed, the behaviour had nowhere to be declared, so it
was patched into eight separate places across seven files, in five shapes, and each patch was
invisible to the next author. Those eight are superseded by this section. **A local re-run rule that
survives it will contradict it later, so remove it rather than leave it.**

**Two things a re-run does. Both are binding.**

```
 ① PROTECTED — a re-run may not rewrite these AT ALL
      > <ACTOR>:                any comment lane, whoever wrote it
      state:                    a value a human set at a gate
      ## States                 written after that gate, about that gate
      a settled State row       in ## States
      a GATE row in ## Log      the one thing on the page that CANNOT be
                                re-derived from disk if it is overwritten

 ② EVERYTHING ELSE — diff and ask, never silently overwrite
      compute what would change, SHOW it, then ask keep / change / reframe.
      This was already the written rule in `ref/09-stage-illuminate.md:25`
      and had never been built.
```

⚖️ **The protection is keyed to the LANE SHAPE, `> <ACTOR>:`, and never to one actor id.** This is
the operative half of the ruling, because the previous attempts failed on exactly this point. Two
rules already protected `> USER:`, the canonical actor id here; every human comment line on the MISQ
paper reads `> JL:`, an alias `2-phase/USAGE.md:53` tolerates when reading. Measured 2026-07-27: 47
such lines across 8 of 40 S pages, and `> USER:` on none of them. So the rule that ran most often
guarded a string that was not there. Matching the shape closes that gap without editing a single
human comment line, which is the one edit `haipipe-board`'s own law forbids.

The hand-drawn `<!-- Agents never overwrite below this line -->` in `5-section-edit/template.md` and
its 95 venue copies is superseded, not implemented: `create-page.py :: template_divisions()` emits
only `###` division titles and drops HTML comments, so the guard sat in 96 files and reached 0 of
the 40 live pages. Protection now keys to constructs that are actually on the page, so no marker has
to survive compilation for it to hold.

## How `artifact:` resolves

The stage names the DIRECTORY and the identity. Board tooling owns the FILENAME (QB4@paper), which
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

## The paper-folder paths a contract may name

Ruled 2026-07-26 on the design board (QA6). **The number is the delete test**: `rm -rf 0-* 1-* 2-*`
must leave a paper that still compiles and still submits. A contract that names a path decides where
a file actually lands, so these are bindings, not prose.

```
 0-lifecycle/<family>/S-<Family>-<n>-<slug>.md   the artifact. One family, one folder
 1-probes/PPnn_<topic>/                          the near side of the wall
 2-src/compile.sh                                how the deliverable is BUILT

 sections/ · appendices/                         GENERATED prose. UNNUMBERED: a journal gets it
 displays/displayNN-<slug>/                      the unit. THE ONLY home of an asset
 <paper>.tex · .bib · .pdf                       the deliverable. UNNUMBERED
```

Never name these, in any field or any comment:

```
 ✗ 0-sections/ · 0-displays/     the old numbered deliverable. A prefix here fails the delete test
 ✗ figures/ · Figure/ · Table/   a second home for an asset. It lives in its unit's assets/
 ✗ 1-compile.sh                  the build script is 2-src/compile.sh
 ✗ STATUS.md                     RETIRED. See below
```

## STATUS.md is retired

`STATUS.md` was the stored frontier: `current_layer`, `maturity`, the venue pin, and the Gate Ledger.
Every part of it now has a better home, and the file itself is no longer created.

```
 current_layer · maturity   DERIVED, from each S page's own `state:` and from disk. The enter
                            console had already stopped reading the stored value; a stored
                            frontier can only go stale, and a stale one is a third answer to
                            "where is this paper" that disagrees with the other two.
 the venue pin              S-Venue-0-venue.md's `state:` line, e.g. `✅ PINNED · MISQ 2026`.
                            NOT a `venue:` frontmatter key: the board's face grammar is a
                            CLOSED whitelist (haipipe-board src/parse.py) and would not see
                            one. One page owns the venue contract;
                            a second copy could only disagree with it.
 Gate Ledger                the S page's own `## Log`, one row on the page whose gate it was.
                            This is the one part that is HISTORY and cannot be derived, so it
                            needed a home rather than a deletion, and the reader is already
                            standing on that page when they want it.
```

A `handoff:` therefore reads `on CHECK confirm, append the gate row to this stage's S page ## Log
-> <next>`. It never advances a frontier, because there is no stored frontier to advance. That also
dissolves the loopback problem: re-running an early stage on a paper whose frontier is further along
records its gate and changes nothing else.
