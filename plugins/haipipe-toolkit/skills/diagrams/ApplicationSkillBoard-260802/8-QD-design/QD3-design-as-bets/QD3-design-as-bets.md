# Design as bets: the card, the unit, and the grant that binds them

state: ✅ SETTLED · the design family shipped 260824 · 23 checker rules enforce it
owner: JL

## Opening

What stops a designed message from being a guess that nobody can later argue with?

A bet written down before the artifact exists. Since 260824 a Design Page proposes strategy CARDS carrying a stance, a thesis and an expected effect with its falsification line; a person releases each card; one agent realizes each released card as one artifact UNIT; a judge checks the unit; a person accepts the division. The card is the bet and the unit is the wager paid, and keeping them in separate files is what makes the terms unable to drift.

### Writing Style

Name the failure each rule exists to prevent. A design law with no recorded failure behind it is a preference that found a rulebook.

## Diagram

```text
📇 direction/DR<NN>.md          🎨 design/DU<NN>-<slug>/
   the BET, before any copy        the WAGER PAID, one folder
   ├── stance                      ├── README.md   kind → venue pack
   ├── thesis                      ├── spec.md     COMPILED, never invented
   ├── expected effect ─────┐      ├── evidence.md ⊆ the card's grant
   │   + falsification line │      └── content/    the artifact itself
   ├── grant ───────────────┼──────────▶ the agent may quote ONLY this
   ├── released: ✋ a person │
   └── landed: DU<NN> ──────┴──────▶ cited, NEVER restated in the unit
```

## Content

### 1 · The two lives of a direction

**Why two files**: what each holds, and the failure that splitting them prevents.

```text
lives here            because
─────────────────────────────────────────────────────────────────────────
the card, at PROPOSAL  the artifact folder does not exist yet, a killed bet
                       still needs a tombstone, and the release gate must be
                       visible on disk
the unit, at REALIZATION  it cites the card back; changing the terms means
                       returning to the card for re-release, never editing
                       them inside the unit
```

A designed message is a bet, and a bet placed after seeing the outcome is not a bet. The card exists so the stance, the move and the wager are written and released BEFORE any copy exists. Its two precedents are both in the family: probe cards give it its lifecycle, proposed then human-released then dispatched; the retired stage ladder gives it its reason, because arms were invented ad hoc and nobody could later say why there were thirteen.

#### 2 · The Reads Law, a four-level narrowing chain

Authority to cite evidence narrows at every level, and each level sits inside the one above:

```text
① board.md   reads: A00                 the board whitelist, set at scaffold
② BR00       born-of: A00·W01           the Brief's birth, ⊆ ①
③ DR card    grant: <paths>             the bet's evidence, ⊆ ①
④ DU unit    evidence.md rows           what the artifact cites, ⊆ ③
```

Enforcement is two-sided: at dispatch the agent's packet contains only granted evidence, so it cannot wander; at judge the set-differences are checked. A packet handed to one agent once quoted two figures the granted section did not contain; the agent refused them and recorded the exclusion, which is the chain working against the person who wrote the packet.

#### 3 · Warrant and grant are different acts

This distinction was conflated in four documents until the sweep recorded in the Log, and every card contradicted them:

```text
WARRANT   why a division may EXIST      rides on the card's stance; moves to a
                                        principle page only when promoted
GRANT     what an agent may QUOTE       names InsightBoard pages by path, because
                                        an agent cannot be handed a rule and asked
                                        to quote a rate
```

An exploration card is the clearest case: it exists to resolve a named uncertainty, and that uncertainty lives on a K row no principle restates.

#### 4 · One card, one agent, one folder

Fan-out is safe because the unit folder is the agent's write boundary, the shape the display family proved first. An agent may touch nothing outside its folder except the card's `landed:` pointer, may never write `released:` or `accepted:`, and refuses a card still at `proposed`, because realizing an unreleased card would pass a person's gate mechanically.

#### 5 · The gates a machine may not open

```text
✋ release     a card at `proposed` blocks its own fan-out and nothing else,
               so proposing is always safe
✋ accept      the person's row on the division names reviewer, unit and render
               version, and the render must EXIST first, because a person accepts
               a version they have seen
```

No expected effect, no release. A card that cannot say what it is for and what would falsify it is not a bet, and an `ignore` card states `baseline, calibrates` rather than leaving the field empty.

#### 6 · Record mode, for artifacts older than the vocabulary

A board holding a PRE-CONTRACT slate declares `mode: record` on `board.md`. It relaxes the WORDS and nothing structural: a card may carry a historical `released:` instead of a person's tick, may have no stance, and a unit may sit at `state: historical-record`, while files, depth, resolvable references and evidence-within-grant are still checked. Forcing the current words onto a 2025 artifact would forge a provenance, which is the one thing a record board must not do.

## Aims

### A1 · The two lives of a direction
- A1.1 · The wager exists in exactly one place and cannot drift.
  **Done when:** the unit cites the card and no unit restates an expected effect.

#### A2 · Reads Law
- A2.1 · Every citation is inside a grant that is inside the board's `reads:`.
  **Done when:** the three set-differences are checkable without reading prose.

#### A5 · Gates
- A5.1 · Release and acceptance are a person's, mechanically.
  **Done when:** a machine writing either field is a reported error, not a convention.

## States

### A1 · The two lives of a direction
- ✅ A1.1 · `unit-dead-reference` fires when a unit's pointer to its card does not resolve, written after one did not on 260824 and left the wager unreachable while every self-check reported clean.

#### A2 · Reads Law
- ✅ A2.1 · `card-grant-outside-reads` and `unit-evidence-outside-grant` check two of the three; the third is the board's own `reads:` resolution.

#### A5 · Gates
- ✅ A5.1 · `card-released-unsigned` and `card-proposed-signed` catch both directions; `card-released-no-wager` refuses a release with no falsifiable claim.

## Files

### 📋 Contracts
- `../../../../application/haipipe-design/SKILL.md`
  The design door: the Reads Law, the two births, the verbs.
- `../../../../board/page-plugins/haipipe-plugin-design/SKILL.md`
  The card grammar and release gate (§card, absorbed from the deleted haipipe-plugin-direction 260828), the unit anatomy, the compiled spec, and the kind routing.
- `../../../../application/haipipe-design/agents/haipipe-designer-agent.md`
  The realizer's packet, procedure and refusals.

## Law

The wager lives on the card. A unit cites it and never restates it, and no machine writes `released:` or `accepted:`.

## Log

260824 · The design family shipped: two page plugins, one agent, one door, and three declarations (`reads:`, `born-of:`, `stance:`). The board layer invented nothing else.

260824 · The laws gained teeth. Twenty-three checker rules over `direction/` and `design/`, each proven to FAIL on a board broken exactly that one way before being trusted, after a run in which four real defects were caught by a human or an agent and none by the machinery.
260828 · One thread, one folder (JL: "no need to have a new direction folder"): the card moved into its unit as card.md, direction/ retired, DR/DU numbering collapsed to DU, both pointer fields died with the folder split, and release-before-realize became a checker ERROR (unit-realized-before-release, proven to FAIL). B00 migrated same day, 0 error.
