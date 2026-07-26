# How a sentence becomes a vector
state: ✅ SETTLED
owner: CC
method: `lib/embed.py` wraps sentence-transformers and OpenAI; swapping the model changes one line of config

## Question
How does one review sentence turn into a string of numbers (a vector), so that the work done by distance (picking hard cases, de-duplicating, covering the full corpus) means anything: which model produces it, how the cache is stored, and is it allowed to decide a label?

JL asked this one directly: how does a sentence become an embedding.
It is also the lowest foundation under the "does the code already do it" half of the spine, because QB1's hard-case picking, Tier 0 of the cascade in QD2, and QB2's de-duplication all stand on it.
If it is not written down, the "pick by position" in those questions above is empty talk.
The other half of the question is a guard rail rather than a build order: a vector is close to another vector for reasons that have nothing to do with the label, so letting distance decide a label would quietly corrupt every set that was picked by distance.

## Boundary
- ✅ Covered here
  The embedding layer itself: which model turns a sentence into a vector, how the cache is keyed, and the standing rule that a vector never decides a label.
- ↪ Covered elsewhere
  How the cascade splits the work and uses this layer as its Tier 0 is QD2; hunting hard cases by distance to grow the gallery is QB1; deciding a label is the panel's job, which is QA2 for labeling independently and QA3 for putting a weak model through the exam.

## Diagram
```
  one review  ──►  lib/embed.py  ──►  [0.02, -0.31, …]  384-dim vector
                                       sentences close in meaning → close in coordinates

  ⚖️ one iron rule: embedding is a SPEED tool, not a JUDGMENT tool
       it only does: find candidates · de-duplicate · cover the full corpus        it never decides a label
       labels come only from panel reasoning, because four traps wait otherwise:
         semantic inversion ("I feel alive" vs "I feel nothing" sit close together, opposite labels)
         irony / genre imitation looks like the target in vector space
         ordinal collapse ("extremely high" vs "very high" squash into one blob)
         no explanation (when a label is wrong you cannot point at the word that caused it)
```

## Items to Finish
- [x] 🎯 The default model is fixed, and so is the way to swap it
      The default is `all-MiniLM-L6-v2`, and changing model means editing the `model` and `dim` lines in the config, nothing else.
      `all-MiniLM-L6-v2` is 22M parameters, 384 dimensions, roughly 2K sentences per second on CPU, and free, which covers anything under 100K English items with no reason to deliberate.
      For better quality or a large corpus the alternative is OpenAI `text-embedding-3-small`; for medical text it is `biobert`.
      The swap stays a one-line edit because the choice lives in the `embedding:` block of `config.yaml` and nowhere else in the code.
- [x] 🗄 The cache layout is fixed
      Vectors are stored under a `sha1(model+text)` hash, so the cache is keyed by the pair `(model, text)`.
      Because the model name is part of the key, switching models does not invalidate what is already cached.
      A new model only recomputes on its first use, and the old entries stay usable if the choice is reverted.
- [x] ⚖️ The principle is nailed down: embedding finds candidates and never decides a label
      Its three jobs are finding candidates, de-duplicating, and covering the full corpus; the label itself always comes from panel reasoning.
      `ref/ref-embeddings.md` records the four failure modes behind the rule.
      Semantic inversion: "I feel alive" and "I feel nothing" sit close in coordinates and carry opposite labels.
      Irony and genre imitation look like the target in vector space.
      Ordinal collapse: "extremely high" and "very high" squash into one blob.
      And there is no explanation: when a label comes out wrong you cannot point at the word that caused it.

## Where we are
One module, one agent, and one block of config, all three settled.
`lib/embed.py` is the only place in the whole system that touches Hugging Face, OpenAI, or sentence-transformers, and everything else reaches it through the embedder agent, which offers embed, index, nearest, cluster, and stratified-sample.
Nothing here is waiting on a decision: the model choice, the cache layout, and the rule that a vector never decides a label were all fixed in `ref/ref-embeddings.md` before this face was written, and this face only pins them where they can be read.

## Files
- `lib/embed.py`
  The single module behind this face, and the only one allowed to talk to Hugging Face, OpenAI, or sentence-transformers, so any change to the embedding layer starts here.
- `ref/ref-embeddings.md`
  The document this face was copied from: the model choice, the cache layout, and the four failure modes behind the iron rule.
- `ref/ref-config.md`
  Carries the `embedding:` block, which is the one place a model swap is edited.

## Law
- Embedding only finds candidates, de-duplicates, and covers the full corpus, and **never decides a label** (labels come only from panel reasoning).
- Swapping the embedding model touches only `model` and `dim` in `config.yaml`; the cache is keyed by the `(model, text)` hash, so a swap does not invalidate it.
- One module (`lib/embed.py`), one agent (embedder), one block of config (`embedding:`): do not start a second place that touches Hugging Face.

## Glossary
embedding / vector: mapping a sentence to a string of numbers, where sentences close in meaning get numbers that are close.
cosine similarity: a number measuring how closely two vectors point the same way, 1 = same direction, 0 = unrelated, used to judge how alike two sentences are.
faiss: a library that finds nearest neighbors by vector, `faiss-flat` (under 100K items) or `faiss-ivf` (larger).
panel: the set of model labelers, whose reasoning is the only thing that decides a label.

## Discussion
> CC0723: This face is the foundation under QB1 (hunting hard cases) and QD2 (Tier 0 of the cascade). Everything in it comes from `ref/ref-embeddings.md`, which was fixed long ago, so this face went straight to ✅: a board does not only hold the undecided questions, it also pins the settled engine facts where they can be seen.

## Log
260725 · rewritten to the current face format in English
260723 1600 · created: pulled the model choice, the cache layout, and the iron rule out of `ref/ref-embeddings.md` onto the board and marked it ✅ (already fixed)
