# Short objective purpose title
state: 🔴 OPEN
owner: CC
method: <optional one-line method; delete when unused>

<!-- S-only metadata. Delete on a Q Page. Use stage.py when dependencies exist.
requires: S-Work-1
style-from: S-Venue-1
provides: <observable downstream handoff>
-->

<!--
Create a Q Page as Q<group><number>-<slug>.md.
Create an S Page as S-<Family>-<unit>-<slug>.md, preferably with stage.py.

Keep the reader-facing Page Face minimal:
  Opening → Content

Outline, Aims, Stage Contract, Files, Discussion, Log, and other process
records belong to the Page Folder and their owning Spaces. They may remain in
legacy Page Faces for compatibility, but they are not reader-facing Page
areas and should not be added to new Page source files.

Title rule: use a short, objective label naming the Page's subject and the
work or deliverable it owns. Keep it to three to five visible words. Do not
encode a joke, marketing phrase, surprise, accusation, or unqualified finding
in the title.

Do not author ## Outline or ## Diagram. The current versioned plan under
outline/ produces the Outline projection. Drawings live in studio/draw/.

Do not create Page-level States, Files, Discussion, or Log sections. Use the
matching records under outline/, including outline/<stem>-files.md and
outline/<stem>-log.md.

Q may omit Content. S must contain Content. Stage contracts, requirements,
and targets are backstage records, not additional Page Face sections.
Delete every guide comment before the Page is ready.
-->

## Opening
<One Page-specific paragraph that defines the subject, states the stake, and names what this Page owns.>

**Where this Page sits:** <the closest upstream or neighbouring Page and what it owns.>

**Why it matters:** <the consequence in reader language.>

## Content
<!-- S required; Q optional. Number divisions and paragraphs all the way down.
Each planned Cn.Pm paragraph realizes its own approved Bullets; keep sentence-
level realizes backlinks. Interactive writing co-develops Bullets and candidate
prose; CONTENT adopts explicitly accepted paragraphs without another drafting
Run. The owner still defines sentence-slot requirements. -->

### 1 · First division
**Division map:** what the diagram previews.

```text
📥 input
   │
   ▼
🧭 argument
   │
   ▼
📤 outcome
```

#### 1.1 · First paragraph
(the job this paragraph performs)
<Write the paragraph in plain English, one sentence per source line.>

### 2 · Second division
**Division map:** what the diagram previews.

```text
📥 input
   │
   ▼
🧭 argument
   │
   ▼
📤 outcome
```

#### 2.1 · First paragraph
(the job this paragraph performs)
<Continue with the next coherent part.>

<!-- Page targets and completion facts live in the Page Folder's requirement,
     Context, Run, and CHECK records. They are not copied into the reading
     Page as a second content stream. -->

<!-- Optional current folds: Law, Lesson, Glossary. Add only when earned.

## Law
- ⚖️ <current durable rule>
  <meaning and boundary>

## Lesson
- 🧪 <specific reusable lesson>
  <what future work should do differently>

## Glossary
- 📖 **<term>**: <plain definition>
-->
