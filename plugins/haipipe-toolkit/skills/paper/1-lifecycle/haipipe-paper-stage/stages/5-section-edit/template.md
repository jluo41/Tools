<tpl: GENERIC FALLBACK TEMPLATE. PRINCIPLE (JL 2026-07-20): every (venue, section-kind) has its OWN template, summarized from that outlet's exemplars. This file is used ONLY when the venue has no pack, or the pack has no template.md for this kind. For a pack-having venue, section-edit copies the venue-specific template resolved into 2a-venue.md's Section Styles table instead of this one. See stage.md `template:` and ../section-kinds.yml.>
<tpl: THIS FILE IS A TEMPLATE **and** its own rulebook. DRAFT copies it to 0-lifecycle/5-section-edit/{section}/{section}.md and fills it in.>
<tpl: Fill every <angle-bracket> slot. DELETE every line starting with "<tpl:" as you fill — a finished .md contains ZERO of them. Mechanical gate: `grep -c '<tpl' {section}.md` must print 0 before the ⛔ STOP presentation.>
<tpl: A finished .md has FOUR parts, top to bottom: (1) title + venue header, (2) structure overview, (3) paragraph blocks, (4) Questions Raised block. Content norms come from the venue blueprint (2a-venue.md block, BINDING) + the style pack (REFERENCE ONLY). Craft rules — what DRAFT prose is, the placeholder forms, the comment lifecycle — are in stage.md.>

# Section <N>: <Title> -- Structure

venue: <MISQ 2026> · section-type: <methods (+results flavor)>
blueprint: 0-lifecycle/2a-venue/2a-venue.md (<methods> block)   <- BINDING: budget, structure, density
style: <resolved venue path, e.g. venue/playbook-utd-is/MISQ/MISQ-methods/style.md · MISQ-results/style.md>   (reference only)
<tpl: DRAFT writes this header ONCE, at scaffold. The four fields:
       venue         the pin read from STATUS.md — an EXAMPLE above; any venue works (ISR, Nature, JAMA, a grant, a patent)
       section-type  this section's mapping (e.g. 4-llmtrait -> methods)
       blueprint     the paper's 2a-venue.md block — the authoritative digest
       style         the deep-dive pack, resolved from the blueprint's [source:] tag
     BLUEPRINT IS BINDING — word budget, ¶-per-subsection, citation density, display limits. Deviating FAILS CHECK.
     STYLE PACK IS REFERENCE ONLY — mine it for arc, signature moves, exemplar sentences; deviating is fine and never a CHECK failure.
     A HYBRID section (methods that also reports validation results) lists more than one style file, ·-separated.
     The `style:` value is COPIED from 2a-venue.md's `Section Styles` table — the row whose kind matches this section. The VENUE stage resolved it; this stage never globs a pack path, never runs find, never spells a per-journal slug (jno · diabcare · npjdm · natcomm · MS-IS all use slugs a consumer cannot derive).
     Row reads `— blueprint-only` -> write `style: (no pack for this kind — blueprint only)`; the blueprint alone is enough to draft.
     No Section Styles table at all -> the venue stage has not been run or is stale: STOP and say so.>

```
§<N>.1 <Subsection Title> (<K> paragraphs)
  P1. <Short paragraph job description>                       <n> sentences · ~<m> words
  P2. <Short paragraph job description>                       <n> sentences · ~<m> words

§<N>.2 <Subsection Title> (<K> paragraphs)
  P3. <Short paragraph job description>                       <n> sentences · ~<m> words

total: <p> ¶ · <s> sentences · ~<w> words   (venue budget for this section: <from blueprint>)
```
<tpl: one Pn line per paragraph, each carrying `<n> sentences · ~<m> words` (approximate — keep the ~). The total: line closes the block against the venue budget from 2a-venue.md. Recount at draft AND after REVISE. Over budget -> FLAG it, never silently trim. Headings: ## for subsections, ### for paragraphs.>

---

## §<N>.1 <Subsection Title>

### P1. <Paragraph job headline>

(<one-line preview, ~80-120 chars: concept name + one distinguishing phrase — a scan hook, not a mini-abstract>)

<First real sentence — complete academic prose, close to submission register.>

<Second sentence; cite with a real key grep-verified in the .bib \citep{<key>}, or \cite{TOADD} [Q-Section-<n>] when no key fits — the bracket names the question that will produce the key, side by side, never fused.>

<A sentence whose number is unverified writes it anyway: ... at {VAL:? <what the number is>} [Q-Section-<n>] ...>

<tpl: each paragraph block = heading + preview, then prose, then any comment threads. ONE sentence per line, BLANK line between sentences (each becomes a Pn.Sn marker at sync). No S-number prefixes. No LaTeX except citation commands. Never invent a key or a number — placeholder rules are in stage.md.>
<tpl: user threads sit under the sentence they discuss and are NEVER deleted/reworded/relocated:>
> USER: <comment>
> CC: <reply — only the user resolves a thread; resolved threads MOVE to _LOG verbatim>

### P2. <Paragraph job headline>

(<one-line preview>)

<Sentences...>

---

Q-consumer
----------
<tpl: MANDATORY last block (JL 2026-07-18, BINDING). A DRAFT that omits it, or writes it as freeform prose, is INCOMPLETE and FAILS the gate — no exceptions.
     The draft PROPOSES the questions; PROBE, after the gate, FILLS each Answer. This is what the user reviews at the DRAFT gate and what the PROBE run drains.
     · STAGE-PREFIXED ID — `Q-Section-<n>`. The id in the heading and the id in the inline anchor are THE SAME TOKEN, exactly as in every sibling stage.
     · ANCHORED, not detached — Reason names the exact §<N> P<x>.S<y> sentence(s) that raised it; that is how a reader jumps back.
     · EVERY {VAL:?}, every \cite{TOADD}, every heavier need becomes a numbered question. Only items resolving paper-local (a pointer the draft already sees) go under Settled Flags instead.
     · A missing DISPLAY UNIT is NEVER a question — it is a DR row in 0-lifecycle/4-display/_DISPLAY_REQUEST.md. section-edit FILES display requests; it never creates displays.
     · Bullet lines, never markdown tables, anywhere in this block (JL standing rule).
     · At PROBE-run time heavier bank questions are DISPATCHED via 1-probes/PP<NN>_<topic>.md (executor-facing q-executor:, no stake) + a 1-probes/README.md bullet row (`- PP<NN> · <stage/section> · <state> · <one-line need> · file: <path>`); the harvested answer flows BACK into the Answer field here.
     · The ⛔ STOP presentation shows this block, so the user reviews STRUCTURE and QUESTIONS at the same gate.
     · closes at CHECK, not REVISE: PROBE FLAGS, it does not place; the human verifies at CHECK and the agent places afterward.>

## Q-Section-<n> · <question title>
Description: <what the question wants to know — one sentence per line; what a good answer looks like>
Reason: <which §<N> P<x>.S<y> sentence(s) cite this id, and why each matters if that assertion is wrong · serves: <claim id / stage> · track: <citation | values | display | discovery | decision | wording>>
Answer: <empty in DRAFT — PROBE fills it from the answering QA file, anchored [source: PPnn]; a pure human decision reads `JL decision`>

---

## Settled Flags (not open questions — logged, no action)

- <accepted deviations / already-ruled items / placeholder rollups that resolve paper-local (e.g. `{VAL:? x} -> paper-local: the number is already on disk at <path>`) — bullet lines, never a table>

---

## My Notes & Feedback — JL
<!-- Yours. Agents never overwrite below this line. Add rulings, priorities, extra questions, corrections. -->

_(empty — add your notes here)_
<tpl: this section is MANDATORY and always present, even when empty. Agents NEVER rewrite or delete anything below its marker.>

<tpl: after filling: verify `grep -c '<tpl' {section}.md` -> 0, then present structure + the questions raised and ⛔ STOP for the user's review. Do not advance without the user's verb.>
