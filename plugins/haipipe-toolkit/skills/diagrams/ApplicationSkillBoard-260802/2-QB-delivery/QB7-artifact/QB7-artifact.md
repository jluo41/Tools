# Delivery Artifact: the shipped draft and its one source

state: 🔴 OPEN
owner: JL
method: read the artifact and section-edit skills, mirror the ruling shape of QB6@paper, and put the binding question to JL

## Opening
What file does an intervention actually ship, and what stands behind its words?
The shipped file is an artifact: one markdown deliverable at `0-artifacts/<slug>-v{N}.md`, written by the `draft` verb.
Its content restates what already lives upstream, so a hand edit to the shipped file quietly forks the source.
This page pins what an artifact is and puts one ruling to JL: whether the paper board's one-source projection rule binds here too.

**What the words mean**: an artifact is the deliverable itself, such as `0-artifacts/refill-reminder-v1.md` for an sms venue.
The evidence ladder is the venue-free chain 1a-descriptions to 1d-advice that supplies the content an artifact restates.
A venue profile is the folder `venue/venue-<name>/` carrying the template, constraints, style-profile, and exemplars for one channel.
A projection is QB6@paper's word for a generated file whose contents are reproducible from its authored source.

**Where this page sits**: on the sister paper board, QB6@paper owns this same delivery concern for manuscripts and ruled that one S page is authored while every manuscript file is a projection of it, checked by regenerating and comparing byte for byte.
This page is the application family's counterpart, and it must say whether that ruling transfers.

**Covered elsewhere**: the step-by-step composing procedure belongs to the artifact skill, and the per-section prose cycle for report-like venues belongs to the section-edit skill.
This page owns only the identity of the shipped file and the ruling on its source.

**Why it matters**: the failure QB6@paper names never announces itself here either.
Someone fixes a typo in the shipped draft because it is the file in front of them, the next re-draft discards the fix, and from then on the artifact and the 1c ledger can disagree about a number with nothing reporting it.

## Writing Style

How this page must be written, so the next editor edits to the same rules.

**The direction is fixed in every sentence**: lifecycle content flows into the artifact, never back, so a sentence that has the artifact correcting the ledger is wrong even as shorthand.

**Name the precedent as QB6@paper**: a bare QB6 on this board reads as this board's own QB6, which is a different page.

**Do not pre-empt the ruling**: until JL answers the Decision Now row, describe today's skill behavior as behavior, never as law.

## Diagram

**From lifecycle to shipped file**: what the draft verb reads and the one file it writes.

```text
  🪜 ladder            1c claims · 1d advice ──┐
  🎭 venue profile     template · style ───────┼──▶ ✍️ draft verb
  🧭 when required     narrative · display ────┘         │
  📄 sectioned only    0-sections/ prose ────────────────┤
                                                         ▼
  📦 the artifact      0-artifacts/<slug>-v{N}.md
  ❓ open ruling       projection of its inputs · or · authored assembly
```

## Content

### 1 · The shipped file

**The artifact at a glance**: address, versioning, and the delta from the paper family.

```text
  📦 file          0-artifacts/<slug>-v{N}.md
  🔢 version       N bumps on re-draft · old versions kept for diff
  🏷 frontmatter   venue · audience · adopted_A · declined_A · status
  🆚 paper family  authored S pages projecting TeX · here plain markdown
```
📌 This part settles what the deliverable physically is, and where the application family deliberately departs from the paper family.

An artifact is one markdown file in `0-artifacts/`, named `<slug>-v{N}.md`, and it is the only thing the draft verb writes.
Its frontmatter names the pinned venue, the audience, the intent, and every advice id it adopted or declined, with a one-line why per declined id.
Version N increments on each re-draft after round feedback, and previous versions are kept for diff rather than overwritten.
The markdown format is a deliberate delta from the paper family, where QB6@paper's units project TeX section files from authored S pages; an intervention's deliverable is markdown end to end, and even its sectioned venues stage their prose as files under `0-sections/`.

### 2 · How it is composed

**Two composing routes**: simple venues fill slots, sectioned venues assemble parts.

```text
  ✉️ simple     sms · push · reminder    1d advice ──▶ venue template slots
  📊 sectioned  report · dashboard      venue structure + narrative arc
                                        + display elements + 0-sections/ prose
  🔁 both       COMPOSE ▸ PROBE ▸ REVISE ▸ CHECK
```
📌 This part settles where an artifact's words come from, on both routes the artifact skill defines.

The draft verb blocks without a pinned venue, then loads the venue profile, the venue's Artifact Principles, the 1d advice, and the 1c ledger, plus narrative and display when the venue required those stages.

**2.1 · The two routes**
- A simple venue (sms, push, reminder) composes directly: adopted advice entries fill the venue template's slots, and the advice-to-slot mapping happens here rather than in the ladder.
- A sectioned venue (report, dashboard spec) first runs the section-edit stage, which drafts, probes, revises, and checks one section at a time into `0-sections/`; the artifact is then an assembly with connective text, and new claims never appear in it.

Both routes end in the same DPRC pass: COMPOSE fills the template or assembly, PROBE traces every number to its anchor and flags what does not trace, REVISE applies the style-profile and audience rules, and CHECK runs the venue self-review before the human gate writes the `draft` Gate Ledger row.

### 3 · The one-source question

**The open relationship**: what the precedent ruled, and what is still unruled here.

```text
  📜 paper ruling   one authored S page · files regenerate byte for byte
  📦 here today     numbers must trace · connective wording born in REVISE
  ❓ unruled        which of the two the artifact must be
```
📌 This part states the one ruling this page exists to obtain, and why today's skill text does not already contain it.

QB6@paper settled the manuscript side: exactly one file is authored per unit, every manuscript file is a projection, and the check is mechanical, regenerate and compare byte for byte.
The artifact skill already leans that way without saying so: new claims never appear in an artifact, every number must trace through the 1c ledger to a resolvable anchor, and a composition problem that traces upstream becomes a loopback suggestion rather than an inline fix.
But it also does what a pure projection forbids: the REVISE step rewrites the artifact's own wording for tone, length, and reading level, so the shipped file carries venue-shaped text that exists nowhere upstream, and versions are diffed rather than regenerated.
So the artifact today is traceable but not reproducible, and whether that is the intended end state or an interim habit is genuinely JL's call; the Decision Now row in `## States` carries the options.

## Aims

### A1 · 📦 The shipped file
- A1.1 · Every shipped draft is one addressable markdown file whose frontmatter names its venue, audience, and every adopted or declined advice id.
  **Done when:** an intervention's current draft resolves to `0-artifacts/<slug>-v{N}.md` and its frontmatter carries venue, audience, adopted_A, and declined_A.

### A2 · 🔁 How it is composed
- A2.1 · No artifact becomes a second evidence source: every number and adopted advice id in it traces through the 1c ledger to a resolvable anchor.
  **Done when:** the DPRC PROBE step reports zero unflagged inventions on the current draft.

### A3 · ❓ The one-source question
- A3.1 · The artifact's relationship to its upstream content is ruled rather than inherited by habit.
  **Done when:** JL answers the Decision Now row, the ruling lands in `## Law` with the rejected options, and the artifact skill's text is updated to match.

## States

### Decision Now
- [ ] 🗣 Does the paper board's one-source ruling bind the intervention artifact?
      📍 `Part` 3 · The one-source question
      🔔 `Why now` the application family is shipping its first artifacts while QB6@paper has already ruled the manuscript side, so every new draft deepens whichever habit wins.
      `A ·` full projection: the artifact must regenerate byte for byte from the ladder, the narrative, and the venue's Artifact Principles, and a hand edit to `0-artifacts/` is forbidden.
      ⭐ `B ·` traceability only: every number and adopted advice id must trace to an upstream anchor, but REVISE owns the connective wording, so the artifact stays authored and versioned rather than regenerated; CC recommends B because the DPRC pass already writes venue-shaped wording that exists nowhere upstream, and byte regeneration would outlaw the skill's own REVISE step.
      `C ·` split by venue: sectioned venues bind fully because their prose already lives in `0-sections/` and the artifact is an assembly, while simple venues bind traceability only.
      🛑 `Blocks` this page's Law row and A3.1; composing itself continues under the current skill text.
      🤖 `If nobody answers` B stays in effect, because it is what the artifact skill does today.

### A1 · 📦 The shipped file
- 🧠 A1.1 · The rule is written in the artifact skill's frontmatter spec and Definition of done; verification waits on the first real intervention draft inspected from this board.

### A2 · 🔁 How it is composed
- 🧠 A2.1 · The PROBE step that would prove this is specified in the skill; no draft has yet been traced from this board.

### A3 · ❓ The one-source question
- 🧠 A3.1 · Waiting on JL; the Decision Now row above carries the ask, three options, and CC's default.

## Files

### ⚙️ Engines
- `../../application/3-deliver/haipipe-application-artifact/SKILL.md`
  The draft verb; JL's ruling lands here as changed COMPOSE and REVISE rules, so open it first when the ruling arrives.
- `../../application/1-lifecycle/5-section-edit/haipipe-application-section-edit/SKILL.md`
  The sectioned-venue prose lane into `0-sections/`; opened only if the ruling splits by venue.

### 📥 Input files
- `../PaperSkillBoard-260725/2-QB-delivery/QB6-main/QB6-main.md`
  The precedent this page reads, cited in prose as QB6@paper: one authored source, every manuscript file a projection of it.

## Glossary

- 📦 **Artifact**: the shipped markdown deliverable at `0-artifacts/<slug>-v{N}.md`, written by the draft verb.
- 🪞 **Projection**: QB6@paper's term for a generated file whose contents are reproducible from its authored source.
- 🎭 **Venue profile**: the folder `venue/venue-<name>/` carrying one channel's template, constraints, style-profile, and exemplars.
- 🪜 **Evidence ladder**: the venue-free stages 1a-descriptions through 1d-advice that supply the content an artifact restates.
- 🔁 **DPRC**: the artifact skill's composing pass, COMPOSE then PROBE then REVISE then CHECK.

## Log

260802 · Page created from the artifact and section-edit skills and the QB6@paper precedent; the one-source ruling opened for JL as a Decision Now row.
