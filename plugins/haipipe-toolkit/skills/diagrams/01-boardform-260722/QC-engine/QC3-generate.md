# Generating a page from outside the board

state: 🟡 PARTIAL · both generators ship, routing of consequences does not
owner: JL
method: mirror `stage.py`: generate the page once, keep its managed spans in sync, and never touch what a human wrote around them

## Opening
How can the Board represent an existing skill or meeting note without becoming a stale second copy?

These sources have their own files, versions, and histories before the Board mentions them.
The difficult boundary is what the generated page may refresh and what a person must continue to own.
That choice determines whether the page stays current without erasing human judgment or discussion.
It succeeds when managed spans resync from the source and every authored line survives untouched.

**Covered elsewhere**: A skill folder → a synced Skill page: `QC3a` (`skillpage.py`). A meeting note → a board page: `QC3b` (`meetingpage.py`). Migrating the two old boards was archived 260801 (we no longer hold them). The round trip a generated page then joins: `QC4`.

## Diagram

```
   a thing that exists on disk ── generate a page, keep managed spans in sync
        │
        ├── ⚙️ skill folder   →  Skill-*.md    QC3a  skillpage.py, version + history point back
        └── 🗣  meeting note   →  a board page  QC3b  meetingpage.py, artifact vs routed consequence
```

## Content
### §1 One contract, two sources
`QC3a` turns one of 130 skill folders into one synced page, so a group of them is a roster that can be ranked, commented on, and watched over time; the page owns a snapshot and points at the live `SKILL.md`.
`QC3b` gives a meeting note a home the board can show (page discovery matches a NAME, and a dated file was invisible), then separates the artifact from its consequences: the note gets a page, and what it decided routes into the Q pages that own it.
Both mirror `stage.py`: the managed spans resync (three per generated page), everything a human wrote around them is left alone.

## Aims
- [x] 🧪 skill folder → synced page ships (QC3a)
- [x] 🧪 meeting note → board page kind ships (QC3b)
- [ ] 🧠 routing a meeting's consequences into the owning Q pages (QC3b) still to build

## States
Both page kinds generate and are live; what remains is routing a meeting note's decisions into the Q pages they change, which is the one open item on QC3b.

### Decision Now
- [ ] 🧠 JL confirms the generator family reads as one topic now that QC3a and QC3b sit under QC3

## Files
- `cli/skillpage.py` · `cli/meetingpage.py` · `cli/stage.py`
  The generators, and the model they mirror.
- `QC-engine/QC3a-skill-to-page.md` · `QC-engine/QC3b-meetingnote.md`
  The family, one source each.

## Log
- 260806 2130 · [REVISE-CC] swept to the 260806 architecture; both generators sync three managed spans (not "one managed block"), and the live skill roster is 130 after the paper family's consolidation into `paper/_old/`
260801 0140 · Full renumber QC5 -> QC3 (contiguous QC1-QC4, JL forced 260801); faces QC5a/QC5b -> QC3a/QC3b
260801 0130 · Opened as the generator-family parent overview when QC5/QC10 were regrouped into QC5a/QC5b and QC4 (migrate old boards) was archived (JL 260801)
