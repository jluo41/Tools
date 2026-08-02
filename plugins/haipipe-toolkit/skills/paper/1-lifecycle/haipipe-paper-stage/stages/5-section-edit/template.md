<tpl: GENERIC FALLBACK TEMPLATE. Every (venue, section-kind) may have its own template. For a pack-having venue, section-edit uses the template resolved into S-Venue-0-venue.md's Section Styles table.>
<tpl: THIS FILE IS A TEMPLATE **and** its own rulebook. DRAFT copies it to 0-lifecycle/4-main/{section}.md and fills it in.>
<tpl: Fill every <angle-bracket> slot. DELETE every line starting with "<tpl:" as you fill — a finished .md contains ZERO of them. Mechanical gate: `grep -c '<tpl' {section}.md` must print 0 before CHECK presents the page.>
<tpl: A finished .md has FOUR parts: title + venue header, structure overview, paragraph blocks, Questions Raised. Content norms come from S-Venue-0-venue.md (BINDING) plus the style pack (REFERENCE).>

# Section <N>: <Title> -- Structure

venue: <MISQ 2026> · section-type: <methods (+results flavor)>
blueprint: 0-lifecycle/2-venue/S-Venue-0-venue.md (<methods> block)
style: <resolved venue path, e.g. venue/playbook-utd-is/MISQ/MISQ-methods/style.md · MISQ-results/style.md>   (reference only)
<tpl: DRAFT writes this header ONCE, at scaffold. The four fields:
       venue         the pin read from S-Venue-0-venue.md — an EXAMPLE above; any venue works (ISR, Nature, JAMA, a grant, a patent)
       section-type  this section's mapping (e.g. 4-llmtrait -> methods)
       blueprint     the paper's S-Venue-0-venue.md block — the authoritative digest
       style         the deep-dive pack, resolved from the blueprint's [source:] tag
     BLUEPRINT IS BINDING — word budget, ¶-per-subsection, citation density, display limits. Deviating FAILS CHECK.
     STYLE PACK IS REFERENCE ONLY — mine it for arc, signature moves, exemplar sentences; deviating is fine and never a CHECK failure.
     A HYBRID section (methods that also reports validation results) lists more than one style file, ·-separated.
     The `style:` value is COPIED from S-Venue-0-venue.md's `Section Styles` table.
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
<tpl: one Pn line per paragraph, each carrying `<n> sentences · ~<m> words`. Compare the total with S-Venue-0-venue.md. Recount after DRAFT and REVISE.>

---

## §<N>.1 <Subsection Title>

### P1. <Paragraph job headline>

(<one-line preview, ~80-120 chars: concept name + one distinguishing phrase — a scan hook, not a mini-abstract>)

<First real sentence — complete academic prose, close to submission register.>

<Second sentence; cite with a real key grep-verified in the .bib \citep{<key>}, or \cite{TOADD} [Q-Sec<unit><Slug>-<n>] when no key fits — the bracket names the question that will produce the key, side by side, never fused.>

<A sentence whose number is unverified writes it anyway: ... at {VAL:? <what the number is>} [Q-Sec<unit><Slug>-<n>] ...>

<tpl: each paragraph block = heading + preview, then prose, then any comment threads. ONE sentence per line, BLANK line between sentences (each becomes a Pn.Sn marker at sync). No S-number prefixes. No LaTeX except citation commands. Never invent a key or a number — placeholder rules are in stage.md.>
<tpl: user threads sit under the sentence they discuss and are NEVER deleted/reworded/relocated:>
> USER: <comment>
> CC: <reply — only the user resolves a thread; resolved threads MOVE to this S page's ## Log verbatim>

### P2. <Paragraph job headline>

(<one-line preview>)

<Sentences...>

---

Q-consumer
----------
<tpl: LOGICAL Q-consumer source, physically adapted into the Board S page's `## Aims`.
     A DRAFT that omits the recognizable Aim records, or duplicates them under Content,
     is INCOMPLETE and FAILS CHECK.
     DRAFT proposes the questions; PROBE authors/matches entries and fills each Answer within the invocation's depth ceiling; CHECK is the human gate.
     · STAGE-PREFIXED ID — `Q-Sec<unit><Slug>-<n>`, both halves read off this unit's S page
       filename `S-<Family>-<unit>-<slug>.md`: S-Main-0-abstract -> `Q-Sec0Abstract-<n>`,
       S-Main-6-results -> `Q-Sec6Results-<n>`, S-Appendix-A-prompts -> `Q-SecAPrompts-<n>`.
       This stage runs per-unit, so THE UNIT IS THE STAGE and its token carries the unit; a
       shared `Q-Section-<n>` collides across units (JL 2026-07-27). The id in the heading and
       the id in the inline anchor are THE SAME TOKEN, exactly as in every sibling stage.
     · ANCHORED, not detached — Reason names the exact §<N> P<x>.S<y> sentence(s) that raised it; that is how a reader jumps back.
     · EVERY {VAL:?}, every \cite{TOADD}, every heavier need becomes a numbered question. Only items resolving paper-local (a pointer the draft already sees) go into the Board page's States / Log instead.
     · A missing DISPLAY UNIT is NEVER a question — it is a DR row in 0-lifecycle/3-display/_DISPLAY_REQUEST.md. section-edit FILES display requests; it never creates displays.
     · Bullet lines, never markdown tables, anywhere in this block (JL standing rule).
     · At PROBE time heavier bank questions are DISPATCHED through 1-probes/PP<NN>_<topic>/ (executor-facing q-executor:, no stake); the harvested answer flows BACK into the Answer field here.
     · CHECK presents the Board page, so the user reviews STRUCTURE and QUESTIONS at the declared human gate.
     · PROBE fills the Answer, REVISE weaves it into the owned sentence, and CHECK verifies both the placement and its source.>

- P<n> · Q-Sec<unit><Slug>-<n> · <question title>
  **Done when:** The answer has landed, been interpreted, and been woven into Content.
  **Description:** <what the question wants to know — one sentence per line; what a good answer looks like>
  **Reason:** <which §<N> P<x>.S<y> sentence(s) cite this id, and why each matters if that assertion is wrong · serves: <claim id / stage> · track: <citation | values | display | discovery | decision | wording>>
  **Probe:** not opened yet
  **Answer:** <empty in DRAFT — PROBE fills it from the answering QA file, anchored [source: PPnn]; a pure human decision reads `JL decision`>

---

## Settled Flags (source-only guidance; materialize these in the Board page's States / Log)

- <accepted deviations / already-ruled items / placeholder rollups that resolve paper-local (e.g. `{VAL:? x} -> paper-local: the number is already on disk at <path>`) — bullet lines, never a table>

---

## My Notes & Feedback — JL
<!-- Yours. Agents never overwrite below this line. Add rulings, priorities, extra questions, corrections. -->

_(empty — add your notes here)_
<tpl: this section is MANDATORY and always present, even when empty. Agents NEVER rewrite or delete anything below its marker.>

<tpl: after filling: verify `grep -c '<tpl' {section}.md` -> 0, continue through PROBE and REVISE, then present the completed Board page at CHECK. Do not cross CHECK without the user's verb.>
