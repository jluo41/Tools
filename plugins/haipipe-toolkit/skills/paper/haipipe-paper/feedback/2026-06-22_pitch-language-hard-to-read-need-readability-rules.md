---
status: fixed
created: 2026-06-22
context: haipipe-paper-pitch skill (1-lifecycle/haipipe-paper-pitch); felt reading 1-pitch.tex on Paper-Personality-Opioid-MedJournal
fixed_in: "haipipe-paper-pitch 1.3.0"
---
I want to mkae sure what shoulod be the language style used in the pitch, from time to time, the writign in the pitch is very hard to read, we want to read them as soon as easier as possible. Pleas think about it. add this a a feedback, could you pull codex to think about how to update the skill related by adding the template and ref the examples, maybe we can also give some rules for in that skills to follow as well.

Distilled ask:
- The pitch must be readable as FAST and EASILY as possible. It is the one-minute, skim-it-in-one-screen artifact; if a reader has to slow down to parse a sentence, the pitch has failed.
- The current pitch skill states "one minute or it failed" and "hook is a question", but gives NO concrete language/readability rules. The result: prose that is sometimes hard to read.
- Three concrete updates wanted in haipipe-paper-pitch:
  1. Add explicit READABILITY RULES the skill must follow (sentence length, plain words, lead with the point, one idea per sentence, no jargon stacks, concrete numbers, no AI-flavored prose).
  2. Add / refine the TEMPLATE so the rules are baked into the per-section guidance, not just stated abstractly.
  3. REFERENCE worked EXAMPLES (good vs hard-to-read pitch prose, ideally drawn from the real ProjB pitch) so the skill shows, not just tells.
- The user asked to pull Codex in to think about the skill update before/while implementing.

Why this matters:
- The pitch is the highest-traffic, lowest-patience artifact in the lifecycle (it is what a busy reader skims first). Hard-to-read pitch prose defeats its only job.
- It connects to standing house-style guidance the user has given repeatedly: no AI voice, one idea per sentence, compress don't split, use verified numbers, no manual line wrap. The pitch skill should encode these as enforceable rules.

Proposed solution (Codex-assisted, then implemented):
1. New ref doc, e.g. ref/pitch-readability.md: a short ranked rule list + a few before/after worked examples (hard-to-read -> easy), keyed to the pitch sections.
2. Updated template in SKILL.md (and/or ref/pitch-template.tex) with per-section readability cues inline (e.g. Hook: one sharp question, <= ~20 words; Surprise: state the turn in the first sentence).
3. SKILL.md Principles section gains an explicit "Readability rules" subsection that points at ref/pitch-readability.md and is checked as part of the pitch done-gate.
4. Repoint the dangling `../../3-write-edit/_shared/sentence-format.md` reference (the _shared layout doc was removed) to a skill-local layout note while doing this pass.

Where it touches:
- new ref/pitch-readability.md (rules + worked examples) under haipipe-paper-pitch/.
- haipipe-paper-pitch/SKILL.md: add Readability rules subsection, bake cues into the template, fix the dangling _shared ref.
- ties to [pitch-skill-no-structure-gate]: readability becomes part of the pitch exit/done criteria.

Fix: Implemented in haipipe-paper-pitch 1.3.0 (Codex-assisted design). Added ref/pitch-readability.md (8 global language rules + a per-section cue table + 3 before/after rewrites quoting the real ProjB pitch + a reviewer checklist + done-gate use). SKILL.md gained Principle 7 ("read it in one minute or rewrite it", pointing at the ref) and the template now carries a one-line `% Cue:` in every section banner. The `../../3-write-edit/_shared/sentence-format.md` reference was checked and is VALID (that file exists), so it was left as-is — proposed-fix item 4 was moot. Refinement (same day, per user): the One-Minute Pitch cue changed from "one repeatable sentence <=25 words" to "a short plain-language paragraph (~4-6 short sentences) for a NEWCOMER who understands it and feels interested" — a single terse kernel read as too short for a newcomer. ref/pitch-readability.md gained a "The One-Minute Pitch is for a newcomer" subsection; the SKILL template's One-Minute Pitch now scaffolds P1.S1-S4 (context -> question -> surprising finding -> why it matters).
