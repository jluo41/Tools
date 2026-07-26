# ⑤ INTERPRET · where does the answer come to rest?

state: 🟡 PARTIAL
owner: JL
method: three copies, each anchored to the one before, so a copy can never drift or be invented

## Question
An answer returns from the bank; where does it end up, and how do we know a later copy is honest?
Three stations, each a more integrated form of the same fact and each anchored to the one before it.
What turns on it is traceability: you can walk prose back to a-consumer, to a-executor, to the QA file, and see where an error entered.

Copying is normally how facts rot, and the reason it does not here is the anchor.
Station ② carries `[source: PPnn]` pointing at ①, and ① carries the target QA path pointing at the bank, so no station is free-standing and a fabricated number has nowhere to hide.
The stake never enters this chain at any station; it stays in the stage-doc Q-consumer where it belongs.

## Boundary
- ✅ Covered here
  The three places an answer lands, what form it takes at each, the anchors between them, and the precondition for harvesting at all.
- ↪ Covered elsewhere
  The read that establishes whether harvesting is legal is `QB5`; the folders the stations live in are `QA7` and `QA6`.
  Weaving the answer into prose and discharging the citation is the consumer's REVISE phase, on the paper board.

## Diagram
```
  🏦 QA file  ─▶  ① PROBE FILE          ─▶  ② Q-consumer Answer   ─▶  ③ STAGE CONTENT
  (bank ⑨)        ### a-executor            Answer: 12.9 …            "…prescribe 12.9 more
                  [→ target QA file]        [source: PPnn]             MME (N=766k)…"

  lives in:       ⑧ the wall                ⑦ the consumer           ⑦ the consumer
  form:           the copy = single truth   the per-consumer Q&A       reader-facing prose
  written at:     ⑤ INTERPRET (PROBE)       PROBE/REVISE               REVISE

  ── the precondition ─────────────────────────────────────────────
  harvest ONLY against a target that is `answered` and NOT superseded.
  a `working` target has an EMPTY ## Answer by construction, so
  harvesting one copies nothing and marks the entry `read`: a lie
  the checker names read-target-working.

  every hop is a copy ANCHORED to the last, so the chain is
  self-contained AND walkable in both directions
```

## Content
### 1 · One q-executor, several consumers, one copy
Station ① is written once per q-executor and is the consumer-side single source of truth, which is what makes T0 JOIN pay off: the MISQ paper's 27 consumer questions share 17 copies rather than keeping 27.
Each consumer then writes its own station ②, in its own words, for its own question, anchored back to the one copy.
So the interpretation is per-consumer and the fact is not, which is the same asymmetry the wall exists to protect, applied on the way back.

### 2 · The chain is walkable and not verifiable
Nothing checks that a station ② `Answer:` still matches the `### a-executor` it cites.
A hand-edited number at station ② passes every check the layer has, and the anchor makes the error findable only if someone goes looking.
That is the same shape as the board tool's own anchor-lost problem, and it is the last unchecked hop in the chain.

## Items to Finish
- [x] 🔗 Three stations defined, each anchored to the previous
- [x] 📌 Station ② carries a `[source: PPnn]` anchor
- [x] 🚦 Harvesting is legal only against an `answered`, non-superseded target
- [ ] 🧪 A broken anchor is detected rather than merely possible
      Nothing today checks that a station ② `Answer:` still matches the `### a-executor` it cites, so a hand-edited number would pass.
      This closes when the walk is checkable, which is the same shape as the board's own anchor-lost problem.

## Where we are
Defined and in use across paper and application alike.
The chain is walkable by a human; it is not yet verifiable by a machine, so a copy edited in place would go unnoticed.

## Files
- `SKILL.md`
  The three stations and their anchors.
