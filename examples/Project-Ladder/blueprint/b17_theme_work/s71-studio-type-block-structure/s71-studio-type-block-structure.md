s71 · Studio Type: Block Structure
==================================
view: overview
emoji: 🧱
band: s0N
name: Block Structure

**Stage:** shaping

**Holds:** The Folder, the Job-Task and the Studio of one Block type.

**Title:** `sNN · Block Structure: <Block type>`

**Examples:** s01 · s02 · s03 · s04; b11 s01 · s02 · s03 (Insight Board, Question Book, DataPrep)

**Topic:** This type defines the content of its Studio instances. Shared Blueprint bands are defined by `delivery/page-spec/studio-bands.json`. Other Work Blocks (Blueprint) reference this definition when they use this type and define only their own additional types.

**Feeds:** none


Definition
----------

1. **Views:** every Block Structure topic has Structure, Draw and Skills; Examples is optional (s05 has none, its example Block shows in s15). Structure and Draw each hold Folder, Job-Task and Studio.
2. **Rule, not a real folder:** Structure and Draw show the type's rule: naming patterns with 〈placeholders〉, never a real folder. Each line's purpose shows on hover.
3. **Examples and Skills:** Examples show the type's example Block read live (its real Folder, Jobs and Studio topics, then the Block itself). Skills lists the skills that own the type.
4. **Job / Task levels:** at most four: Job group → Job name → Task group → Task name, drawn as a folder tree like Folder: a ◇ for each level, the level's name small after it, one colour per level, the same colour for the same level in every Block type (b11: purple Job group, blue Job name, green Task group, orange Task name, each with a dark-mode variant; the values are in b11's `delivery/structure/structure.css`).
5. **Only the levels the type needs:** a level the type never needs is left out, not shown empty. "optional" stays only where real Blocks of the type differ, as Work's groups do. Insight: a Question Book Job is itself a question version, so it has no Job group; DataPrep steps are names, so it has no Task group.
6. **Runs:** a Task's Runs go on the Task's hover only when a Run means something structural (Insight Board: `rNN_〈segment〉`, one per segment, plus `rNN_cross`). Work Runs are tries, so they stay off the tree.
7. **Checks:** the rule tree names no real path; the levels match the type; titles start with "Block Structure:".

Worked examples: b11 s01-s03 (`examples/Project-Ladder/blueprint/b11_theme_insight/delivery/structure/build_structure.py` and `check_structure.py`). The Insight Board's tree: 〈question-vN〉 → jNN · 〈data-vM〉 · 〈prep-vK〉 → Prep | Data | Information | Knowledge | Wisdom | Executive → tNN 〈L〉NN 〈question〉.


Decided
-------

- s71-D01 · Each Studio type is its own topic in the s7N Studio Type band (JL 261127: "I want each type of the studio should be a sperate markdown. and I want to put them as a group of studio in studio as well.")
