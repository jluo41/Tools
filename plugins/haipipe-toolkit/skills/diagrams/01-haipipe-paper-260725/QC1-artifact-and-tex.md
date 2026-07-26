# The artifact is the paper; the tex is a build product
state: 🟡 PARTIAL
owner: JL
method: keep the .md as the record; rule what generates the tex from it

## Question
What does a stage write, and where does the compiled manuscript come from?

The settled half is a strong rule: the `.md` is the paper and the `.tex` is a build product. Prose authored into the tex sits outside the record a human reviews, and sync will either overwrite it or silently keep it, which are both defects. The unsettled half is the mechanism: what exactly sync reads, and by what rule it turns a page into tex.

## Boundary
- ✅ Covered here
  What a stage writes, and the direction of generation.
- ↪ Covered elsewhere
  How many artifacts a stage writes is `QB4`; what they are called is `QC2`; projection into LaTeX, Word, and HTML is `QC3`.

## Content
### The rule, and why it is not negotiable
Two writable copies of the same prose is the oldest failure in this system. Whichever one a human edits, the other is silently wrong, and the human cannot tell which they are reading. So exactly one direction is allowed: markdown to tex, never back.

### What sync must read, once the grain is ruled
The section pages carry a shape contract: divisions at `###` numbered for depth, paragraphs at `####`, sentence apparatus as `>` lines. That makes extraction mechanical rather than interpretive:
```
 ### §6.1 <Title>   →  a subsection
 #### P1. <job>     →  a paragraph break; the heading is scaffolding, not prose
 (job line)         →  dropped: it describes the paragraph, it is not in it
 > any lane         →  dropped: apparatus, never manuscript
 plain sentences    →  the prose, as authored, one per line
```

### The open edge
An artifact that is not prose at all. The pitch stage's real output has been a `.tex`, and the display stage's output is a rendered asset plus a float file. "The .md is the paper" is exact for section-edit and needs restating for the stages whose product is not a section.

## Items to Finish
- [x] 📜 One direction only: md to tex
      Stated in the section-edit contract, with the reason.
- [ ] 🧠 Rule what sync reads
      The page's `## Content`, with the extraction rule above written into the contract so two implementations cannot disagree.
- [ ] 🧪 Round-trip one section
      Generate a section's tex from its page and diff against the shipped file; differences are either rule bugs or drift the tex accumulated. This is a parity test, not permission to make TeX a second source.
- [ ] 📐 Restate the rule for non-prose artifacts
      Display and pitch produce things that are not sections. Say what "the artifact" means for them.

## Where we are
The rule holds and is stated. The generator's input is currently a path that no longer exists on the one paper using it, so the rule is true and unexecutable at the same time.

## Files
- `stages/5-section-edit/stage.md`
  Carries the law and the dead path.
- `0-lifecycle/2a-venue/S-Venue-0-venue.md`
  The section shape contract extraction can rely on.
