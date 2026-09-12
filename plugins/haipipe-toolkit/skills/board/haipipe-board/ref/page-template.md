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

Keep the current Page Face:
  Opening → generated Outline → Content → Aims

Title rule: use a short, objective label naming the Page's subject and the
work or deliverable it owns. Keep it to three to five visible words. Do not
encode a joke, marketing phrase, surprise, accusation, or unqualified finding
in the title.

Do not author ## Outline or ## Diagram. The current versioned plan under
outline/ produces the Outline projection. Drawings live in studio/draw/.

Do not create Page-level States, Files, Discussion, or Log sections. Use the
matching records under outline/, including outline/<stem>-files.md and
outline/<stem>-log.md.

Q may omit Content. S must contain Content and may carry a Stage Contract.
Delete every guide comment before the Page is ready.
-->

## Opening
<One Page-specific paragraph that defines the subject, states the stake, and names what this Page owns.>

**Where this Page sits:** <the closest upstream or neighbouring Page and what it owns.>

**Why it matters:** <the consequence in reader language.>

## Stage Contract
<!-- S only. Delete this whole section on a Q Page. stage.py owns the managed blocks. -->

<!-- haipipe:contract:start sha256=... -->
### Required Inputs
<generated from explicit requires metadata>

### Venue
<generated from explicit style-from metadata>
<!-- haipipe:contract:end -->

### Provides
<short observable output handed downstream>

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

## Aims
### A1 · First division
- ⬜ A1.1 · <durable target>
  **Done when:** <observable test>
  **Now:** <one current fact>

### A2 · Second division
- ⬜ A2.1 · <durable target>
  **Done when:** <observable test>
  **Now:** <one current fact>

### P · Page-level
- ⬜ P1 · <target that genuinely crosses divisions>
  **Done when:** <whole-Page test>
  **Now:** <one current fact>

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
