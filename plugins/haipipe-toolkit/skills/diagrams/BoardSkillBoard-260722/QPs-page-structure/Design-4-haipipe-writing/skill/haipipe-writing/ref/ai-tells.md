# AI tells: the general catalogue

Migrated 2026-08-01 from `paper/2-phase/2-revise/haipipe-paper-revise-humanizer/ref/pattern-catalog.md`
Layer 1, which was itself vendored from `AIScientists-Dev/academic-humanizer @ 02281d8` (MIT).

**Why it moved.** That file's Layers 2 to 6 are academic: over-claiming verbs,
citation dumping, venue voice, funding-proposal register. Layer 1 is not. It
describes how a machine writes in any register, and it was reachable only by
loading a paper skill. The humanizer keeps Layers 2 to 6 and cites this file for
Layer 1, so there is one catalogue and it lives where any prose can reach it.

## 1 · The catalogue

- **Inflated significance** — "marking a pivotal moment", "a testament to"
- **`-ing` tails that fake depth** — "…, highlighting the importance of…"
- **Promotional or figurative language** — "rich", "vibrant", "groundbreaking"
- **Vague attribution** — "experts argue", with nobody named
- **AI vocabulary** — *delve, underscore, intricate, tapestry, testament,
  landscape (abstract), pivotal, showcase, foster, leverage (as filler), realm,
  seamless*
- **Copula avoidance** — "serves as" where "is" was the word
- **Negative parallelism** — "not just X, but Y"
- **Rule-of-three padding** — three items where the third carries nothing
- **Elegant variation** — cycling synonyms for one referent, so the reader cannot
  tell whether two names are one thing
- **Filler** — "it is worth noting that", "in order to"
- **Overlong, clause-stacked sentences** — split them
- **Em-dashes** — remove entirely; recast with commas, colons, parentheses, or a
  new sentence (JL 260724, and this repo's own hard rule)

**Before**: *Additionally, an enduring testament to the method's value is its
ability to delve into intricate dependencies, showcasing a seamless integration
that underscores its pivotal role.*

**After**: *The method also captures higher-order dependencies, which the
baselines miss (Table 2).*

## 2 · The tells this repo produced on its own

Found in this codebase's prose rather than inherited from the catalogue.
`cli/score.py` matches exactly these, and no others:

- `X is not the thing being traded away: it is Y` — the reversal flourish
- `…, which is why …` bolted onto an already-finished sentence
- `not only … but also`
- the four-slot house skeleton: `This page defines X` / `The hard part is` /
  `Without that` / `It succeeds when`. On one 53-page board, 37 pages ended on
  "succeeds when" and 22 opened on "This page", so the pages differed by one noun.

## 3 · What NOT to over-correct

A tell is a tell in context. Neutral and precise IS the human voice in technical
writing, so do not inject opinion, humour, or first-person personality to prove a
human wrote it. The academic-specific version of this caution, with its
claim-evidence discipline, stays in the humanizer's Layer 3.
