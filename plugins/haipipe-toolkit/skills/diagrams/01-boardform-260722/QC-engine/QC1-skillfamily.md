# The skill family as a deliverable

state: 🟡 PARTIAL · what SKILL.md must say and which units ship are both still forming
owner: JL
method: SKILL.md stays as short as possible and is the only export channel for settled rules; the roster is ruled by JL, and a shipped unit follows settled decisions, never precedes them

## Opening
What should the Board family ship, and how should its settled decisions reach a future agent with no memory of this work?

The family needs one clear public door without hiding the contracts that make it usable.
The hard part is separating essential operating guidance from units that deserve their own entry points.
That choice controls what every Board session loads and which parts can evolve independently.
It succeeds when a newcomer can name each shipped unit and find every settled rule once.

**Covered elsewhere**: What SKILL.md must say and where it draws the cut to `ref/`: `QC1a`. The sub-skill roster and its one test: `QC1b`. One synced page per shipped unit: `Skill-0`..`Skill-5`. The agents below the skills: `Agent-1`, `Agent-2`.

## Diagram

```
   skills/board/  ── one family, several doors
        │
        ├── 📜 SKILL.md  · the only export channel for settled rules   QC1a
        ├── 🧱 the roster · which units are their own door             QC1b
        └── 🪞 one synced Skill-*/Agent-* page per shipped unit        Skill-0..5 · Agent-1..2
```

## Content
### §1 The two ends of one question

**Two faces, one deliverable**: what each face rules, and where its answer lands.

```
📜 QC1a  what SKILL.md says   ──▶  the cut line to ref/    ──▶  SKILL.md
🧱 QC1b  which units exist    ──▶  the roster + one test   ──▶  skills/board/
🪞 Skill-* · Agent-*          ──▶  one synced mirror page per shipped unit
```
📌 Both faces answer "what does this family ship", one from inside a unit and one from above the set.

`QC1a` rules what SKILL.md says and what it leaves to `ref/`: the cut line needs a rule, not a feel, because SKILL.md is the skill's entry point and its only graduation channel.
`QC1b` names every subskill candidate and applies one test to each: is it its own door, or a section of the manual?
The roster took its shape on 260731: one door, the board+group altitude, two loadable SPECs, and the write-back VERB; `digest` is named and unshipped.

## Aims
- [ ] 🧠 SKILL.md's cut line is written as a rule (QC1a)
- [x] 🧱 the roster ruled: five of six units ship, digest is named and unbuilt (QC1b, JL 260731)
- [ ] ⚠️ resolve the overlap: does the subskill roster live here (QC1b) or in the Skill-* pages?

## States
The roster is ruled and five of its six units ship (`haipipe-board` 0.104.0, `-index` 0.2.1, `-page` 0.6.0, `-sentence` 0.1.1, `-routing` 0.6.0; `-digest` is named and unbuilt); SKILL.md's cut line is still described more by feel than by rule; and the skill page overlaps the Skill-* roster it points at, which is the open item.

### Decision Now
- [ ] ⚠️ JL rules whether QC1b (the roster argument) and the Skill-* pages (the roster itself) should stay separate or merge

## Files
- `haipipe-board/SKILL.md`
  The door and the export channel.
- `QC-engine/QC1a-skillmd.md` · `QC-engine/QC1b-subskills.md`
  The family, one face each.

## Log
260801 0130 · Opened as the skill-family parent overview when QC1/QC6 were regrouped into QC1a/QC1b; flagged the QC1b vs Skill-* overlap as the open decision (JL 260801)
