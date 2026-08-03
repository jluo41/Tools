board agents: Changelog
========================

Agent-scoped history. Versions match the agent frontmatter.
## 0.5.0 / 0.6.0 - 2026-08-03

**Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.

- **Both agents failed a correct skill page for obeying its own contract.** The creator's house rules and the reviewer's check both demanded `A<n>` ids and a one-to-one Aim-to-State map, unconditionally. `haipipe-board-page-for-skill` overrides exactly that for Skill and Agent pages, and both agents predate the override. A creator that obeyed its own step 2 then broke its own house rule; the reviewer then reported a fault on a page that was right. Both rules are now conditional on the page kind.
- **The creator could be asked to create a page it cannot create.** Its declared output was "one new Q/S page", it has no Bash tool by design, and a Skill page can only come from `skillpage.py new`; a plain `Write` over a generated page destroys its managed spans, which cost one page its Aims, States and Log on 260803. It now refuses `create-page` for `Skill-`, `Agent-` and `Meeting-`, and may still revise an Opening or write the authored half.
- The creator no longer calls `## Question` a permanent alias; it leaves it, names it in the report, and says the checker flags it.
- Both source lists reach `haipipe-board-page-for-venue`, which shipped after both agents were last dated.

## 0.5.0 / 0.4.0 - 2026-08-02

**Both agents now load `haipipe-board-page-for-skill` for a skill page.**

That variant shipped earlier the same day and neither consumer was told about it. Six writers used it only because the dispatching session named it by hand in every packet, so the next dispatch without that sentence would have judged and written `Skill-<n>` and `Agent-<n>` pages against the base contract that explicitly does not fit them.

The two Opening rules are OPPOSITE, which is why silence here is not a small gap: the base ends its Opening on what the page decides, and a skill page decides nothing, so applying the base marks correct roster prose as wrong and passes the form letter the variant exists to catch.

- `haipipe-board-reviewer-agent` 0.4.0 -> 0.5.0: source 3, loaded WHENEVER a page under review is a skill page. The list renumbers to five.
- `haipipe-board-creator-agent` 0.3.0 -> 0.4.0: source 2, with an instruction to CHECK THE FILENAME before writing a word. The list renumbers to five.

The general lesson, which cost nothing here only because a person asked: shipping a variant is not done when the variant exists. It is done when every agent that loads the base knows when to reach past it.

## [0.4.0] · 2026-08-01 · haipipe-board-reviewer-agent

- Adds a Board-order batch voice gate after page-local review.
- Detects repeated sentence stems, repeated rhetorical sequences, cosmetic
  synonym swaps, and Openings that survive a sibling-subject substitution.
- Allows a locally clear page to fail when the changed batch reads like a form
  letter.

## [0.3.0] · 2026-08-01 · haipipe-board-creator-agent

- Adds explicit `create-page` and `revise-opening` operations while preserving
  the one-agent, one-page write boundary.
- Makes the creator load `haipipe-board-page` directly, read a revision target
  completely, edit only Opening, and self-check without approving its own work.
- Keeps prose requirements in the canonical skill and reference instead of
  copying a sentence formula into each assignment packet.

## [0.3.0] · 2026-08-01 · haipipe-board-reviewer-agent

- Loads the canonical page evaluation contract and resolves base, variant,
  page-local, Stage Contract, division, and paragraph-job requirements.
- Returns one evidence-bearing `MEETS | NEEDS WORK | N/A | NOT VERIFIABLE`
  verdict per present section and Content unit.
- Reports requirement conflicts instead of silently choosing a source.

## [0.2.1] · 2026-08-01 · haipipe-board-creator-agent

- Writes the canonical plural section label `## States`; each row remains one
  singular State record for one Aim.

## [0.2.1] · 2026-08-01 · haipipe-board-reviewer-agent

- Reviews `## Aims` against the canonical plural `## States` section.

## [0.2.0] · 2026-08-01 · haipipe-board-creator-agent

- Replaced the retired Boundary and Items-to-Finish writing contract with
  Opening scope, Content-linked Aims, and one factual State row per Aim.
- Reserved Decision Now and page-level gates for the human while allowing
  evidence-backed Aim State updates.

## [0.2.0] · 2026-08-01 · haipipe-board-reviewer-agent

- Reviews the one-to-one Aim-to-State id map and distinguishes individual Aim
  status from the page-level human gate.

## [0.1.0] · 2026-07-31 · haipipe-board-creator-agent

- Added the family's second agent, and the producer half of the creator and
  reviewer pair the rest of this toolkit already uses.
- Scoped it to exactly ONE page per invocation, so the caller fans out N of
  them in parallel instead of `haipipe-board` writing pages one by one
  (JL 260731).
- Made the parallel safety structural rather than advisory: no Bash tool, so it
  cannot run `build.py`; `board.md` is off limits, so the one file every writer
  would collide on stays the caller's; and no sibling page may be read, so two
  agents cannot start duplicating each other's judgment.
- Gave it the `siblings` field in its assignment packet, which is what lets a
  page write an honest Opening scope without reading the board, and what stops
  two pages claiming the same decision.
- Left every shared write with the caller: registering in `board.md`, the lane
  block, one rebuild, one check, and dispatching the reviewer.

## [0.1.0] · 2026-07-26 · haipipe-board-reviewer-agent

- Added the Board family's first agent.
- Made the role read-only: it runs the mechanical checker, cold-reads prose,
  checks for stale claims, and returns findings without editing the Board.
- Kept Board discovery, synchronization, repair, and rebuilding with the
  original session and `haipipe-board` skill.
