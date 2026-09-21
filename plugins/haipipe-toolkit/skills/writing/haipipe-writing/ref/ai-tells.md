# AI tells: the general catalogue

Migrated 2026-08-01 from Layer 1 of the retired HAI humanizer's pattern catalog,
which was itself vendored from `AIScientists-Dev/academic-humanizer @ 02281d8` (MIT).
Retained provenance and license: [method-attribution.md](method-attribution.md).

**Why it moved.** That file's Layers 2 to 6 are academic: over-claiming verbs,
citation dumping, venue voice, funding-proposal register. Layer 1 is not. It
describes how a machine writes in any register, and it was reachable only by
loading a paper skill. The standalone HAI humanizer is now retired. Academic
checks can be selected through the external evaluation adapter; this catalog
contributes diagnostic findings, never an AI-origin verdict.

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
- **Overlong, clause-stacked sentences** — inspect reading burden; split only
  when meaning and the host's sentence/Bullet mapping permit it
- **Em-dashes** — remove entirely; recast with commas, colons, parentheses, or a
  new sentence (JL 260724, and this repo's own hard rule)

**Before**: *The method has the ability to capture higher-order dependencies.*

**After**: *The method can capture higher-order dependencies.*

The example changes expression only. No comparator, result, table or citation
may be added to make a sentence more specific without supplied authority.

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
claim-evidence discipline, is enforced by the shared Writing request and
[academic evaluator adapter](methods/academic-humanizer.md).
