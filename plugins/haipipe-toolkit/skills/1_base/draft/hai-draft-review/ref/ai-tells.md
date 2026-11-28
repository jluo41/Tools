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

- **Inflated significance**: "marking a pivotal moment", "a testament to"
- **`-ing` tails that fake depth**: "…, highlighting the importance of…"
- **Promotional or figurative language**: "rich", "vibrant", "groundbreaking"
- **Vague attribution**: "experts argue", with nobody named
- **AI vocabulary**: *delve, underscore, intricate, tapestry, testament,
  landscape (abstract), pivotal, showcase, foster, leverage (as filler), realm,
  seamless*
- **Copula avoidance**: "serves as" where "is" was the word
- **Negative parallelism**: "not just X, but Y"
- **Rule-of-three padding**: three items where the third carries nothing
- **Elegant variation**: cycling synonyms for one referent, so the reader cannot
  tell whether two names are one thing
- **Filler**: "it is worth noting that", "in order to"
- **Overlong, clause-stacked sentences**: inspect reading burden; split only
  when meaning and the host's sentence/Bullet mapping permit it
- **Em-dashes**: remove entirely; recast with commas, colons, parentheses, or a
  new sentence (JL 260724, and this repo's own hard rule)

**Before**: *The method has the ability to capture higher-order dependencies.*

**After**: *The method can capture higher-order dependencies.*

The example changes expression only. No comparator, result, table or citation
may be added to make a sentence more specific without supplied authority.

## 2 · The tells this repo produced on its own

Found in this codebase's prose rather than inherited from the catalogue.
`cli/score.py` matches exactly these, and no others:

- `X is not the thing being traded away: it is Y`: the reversal flourish
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

The guardrails below are adapted from Adam Boudjemaa's humanizer (MIT) and
stephenturner's deslop (MIT); rows in [anti-slop-attribution.md](anti-slop-attribution.md).

**Do not flag:**

- **One tell alone.** One "crucial", one three-item list, one tidy sentence is how
  people write too. Flag a cluster in the same passage, never an isolated hit; the
  rules JSON already weights tier 2 and tier 3 words this way.
- **Clean grammar.** Correct punctuation and a consistent Oxford comma are a careful
  writer or a copy editor, not a machine.
- **Anything inside quotes, titles, headings, code, or a quoted example.** A watched
  word in a citation title, a variable name, or a pasted sample under critique stays
  exactly as written; `cli/anti_slop.py` masks these spans before it scans.
- **Deliberate repetition of a technical term.** Technical prose repeats the exact
  term on purpose. Varying it for elegance is the elegant-variation tell in reverse.
- **Formulaic consistency by itself.** Low sentence-length variance is the natural
  voice of many writers, including autistic and ADHD writers; burstiness alone never
  raises a finding.
- **Formal or non-native English.** A stiff, textbook register is often a
  second-language writer's honest voice, and detectors over-flag it
  (Liang et al., arXiv:2304.02819).
- **Short samples.** Under about 40 words there is no signal; the scanner reports
  `short_sample` instead of a verdict.

**Preserve when found:**

- hard-to-fabricate specifics: dates, amounts, file paths, names, measured numbers;
- admitted uncertainty and a stated bias;
- a fragment, a tangent, a self-correction, an ending that simply stops;
- text written before late 2022, which predates the tools being looked for.

**Do not dilute.** An anti-slop pass removes filler; it never flattens a specific
into a generality, softens a claim the evidence supports, or restates one point in
several ways to fill space. If the pass left the passage vaguer, the pass was wrong.

## 4 · Match the register

A finding is judged against the register the host declared, not against one house
voice. In a Page, note, or README the reader is in the room: "you" over "people",
specifics over abstractions, no narrator speaking from a distance. In a paper,
thesis, or proposal, formality stays: "we" for the authors' own work, named authors
instead of "researchers have shown", and neither the distant "it has long been
recognized that" nor the blog voice. The catalog carries this as `register:` on each
evaluator entry (`humanizer` for the general register, `academic-humanizer` for the
academic one), and [plain-rules.md](plain-rules.md) §2 keeps its own ruling: a
defined technical term is kept and explained, never traded for a common word that
loses precision.

## 5 · Hard to read: what senior readers flag (JL 261110)

Two senior co-authors of an IS paper called its prose machine-written, sentence by sentence and in a meeting
(2026-11-08 to 261110). What they flagged, as tells any reviewer checks, with the published reason behind each:

1. **The room metaphor**: "settles the decision", "leaves the choice open", "room to enter", "move it much".
   Name the construct (discretion, latitude, ambiguity) instead of a picture of space. AI text overuses a small
   set of words and readers now spot them (Kobak et al. 2025, Science Advances; Liang et al. 2024).
2. **Things as subjects**: "Three control sets enter in steps", "the pooled model lets every control vary",
   "the score reads", "Table 4 reports". Reverse it: a person does the verb ("We introduced three sets of controls
   in sequence"). Clark, Martin and Mahowald (2026, arXiv 2610.29162) find all nine frontier models use more
   inanimate subjects with animate verbs than people do, plus more low-frequency word combinations, longer
   subject-verb distances, stacked nouns ("patient-request pressure") and reduced object relatives: text packed
   for density, not for a reader.
3. **Definition stacks**: "X identifies …. Y captures …. Z is the pathway …. W determines …". One sentence that
   relates the constructs; each definition where it is first used. A list of constructs is not theory
   (Sutton and Staw 1995; Whetten 1989).
4. **Self-narration**: section roadmaps ("This section describes …, and ends with …"), "Having tested H1, we
   turn to H2", a summary the next section repeats, a number said twice (Hyland 1998 on metadiscourse).
5. **Procedural over-defense**: "We fix this ranking from clinical sources before examining any estimate";
   cite where the choice comes from instead, and answer the worry once, in Methods.
6. **Self-praise**: "It resolves the opening tension", "data rarely available together", "the gap is specific:".
7. **A theory as one cited line**: a bridge sentence ("Studies of X show why this room matters.") then a
   one-line definition with a citation. Develop it: the claim, its evidence, why the setting fits, the prediction.
8. **Granular openings**: a Section opens on its biggest meaning, then the finding, then the numbers.
9. **Loose verbs**: "map" reviews to a trait when the method scores or extracts it; use the exact verb.
10. **Fragmented sentences** (JL 261111): after a "one idea per sentence" pass, a paragraph turns into a string of
   short sentences, each half of a topic ("Their error in predicting age group dropped by 13.0%. Next-day time in
   range barely changed."). One topic per sentence, one or two points: merge the halves back (`plain-rules.md` §3).
   The ScalingGlucose Abstract went from 8 to 13 sentences in 150 words (11.5 words each) and read as a list; four
   Nature Machine Intelligence abstracts run 5 to 9 sentences of 20 to 30 words.
11. **Half a count** (JL 261111, blind round r06): "a larger model helped in only 1 of 28 comparisons" hides that it
   hurt in 9. When a count has two directions, give both ("helped in 1 of 28 comparisons and hurt in 9"); "only" does
   not replace the other half. The same holds for a split result: a number for one group implies the other group
   behaved alike unless the sentence says otherwise.
12. **A data set sized only in people** (JL 261111: "should say the glucose size as well. not just the human"): give
   the amount of data in its own unit (57.5 million readings, 547 patient-years) beside the number of people.

A co-author's own sentences keep their register ("attributes … largely to", "conjecture", "ceteris paribus",
"; however,"). A rewrite we write still follows the house rules: no semicolons, no transition set off by commas, no
longer than what it replaces. Run `cli/anti_slop.py audit` on the rewrites before they are proposed (JL 261110).

