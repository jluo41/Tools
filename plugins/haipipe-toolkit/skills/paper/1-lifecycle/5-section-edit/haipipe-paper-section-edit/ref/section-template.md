<tpl: THIS FILE IS A TEMPLATE. DRAFT copies it to 0-lifecycle/5-section-edit/{section}/{section}.md and fills it in.>
<tpl: Fill every <angle-bracket> slot. DELETE every line starting with "<tpl:" as you fill — a finished .md contains ZERO of them. Mechanical gate: `grep -c '<tpl' {section}.md` must print 0 before the ⛔ STOP presentation.>
<tpl: Rules live in ref/outline-format.md (read it once per session). This file is only the SHAPE. Content norms come from the venue blueprint (2a-venue.md block, BINDING) + section-type/section-<type>/SKILL.md (structure norms) + the style pack file(s) (REFERENCE ONLY).>

# Section <N>: <Title> -- Structure

venue: <MISQ 2026> · section-type: <methods (+results flavor)>
blueprint: 0-lifecycle/2a-venue/2a-venue.md (<methods> block)   <- BINDING: budget, structure, density
style: <resolved venue path, e.g. venue/playbook-utd-is/MISQ/MISQ-methods/style.md · MISQ-results/style.md>   (reference only)
<tpl: resolve the pack path layout-agnostically (find over ~/.claude/skills + $CLAUDE_PLUGIN_ROOT), record the RESOLVED path; pack absent -> `style: (pack missing — blueprint only)` + flag for CHECK. Hybrid sections list multiple style files ·-separated.>

```
§<N>.1 <Subsection Title> (<K> paragraphs)
  P1. <Short paragraph job description>                       <n> sentences · ~<m> words
  P2. <Short paragraph job description>                       <n> sentences · ~<m> words

§<N>.2 <Subsection Title> (<K> paragraphs)
  P3. <Short paragraph job description>                       <n> sentences · ~<m> words

total: <p> ¶ · <s> sentences · ~<w> words   (venue budget for this section: <from blueprint>)
```
<tpl: one Pn line per paragraph; recount after every structure change; over budget -> flag it, never silently trim.>

---

## §<N>.1 <Subsection Title>

### P1. <Paragraph job headline>

(<one-line preview, ~80-120 chars: concept name + one distinguishing phrase — a scan hook, not a mini-abstract>)

<First real sentence — complete academic prose, close to submission register.>

<Second sentence; cite with a real key grep-verified in the .bib \citep{<key>}, or \cite{TOADD} when no key fits (+ a _CITATION_ row naming the topic).>

<A sentence whose number is unverified writes it anyway: ... at {VAL:? <what the number is>} ...>

<tpl: ONE sentence per line, BLANK line between sentences (each becomes a Pn.Sn marker at sync). No S-number prefixes. No LaTeX except citation commands. Never invent a key or a number.>
<tpl: user threads sit under the sentence they discuss and are NEVER deleted/reworded/relocated:>
> USER: <comment>
> CC: <reply — only the user resolves a thread; resolved threads MOVE to _LOG verbatim>

### P2. <Paragraph job headline>

(<one-line preview>)

<Sentences...>

---

## Questions Raised by This Draft

<tpl: MANDATORY last block (JL 2026-07-18, BINDING — full spec in ref/outline-format.md). One `###` subsection PER question, each with all four labelled fields. EVERY {VAL:?}/\cite{TOADD}/display-need/heavier-need becomes a numbered question. Bullet lines, never tables. Then a Settled Flags section, then a user-owned notes section.>

Each question is a Q_consume: it links back to the sentence that raised it, and its Answer is filled later by the probe group (the bank).

### §<N>-Q1 · <short title>
<tpl: index = the stage/section TAG + Q<n> so it is globally unique — `§<N>-Q<n>` for a manuscript section (§1-Q1, §6-Q2; §0 = abstract), `<stage>-Q<n>` for a lifecycle stage (seed-Q1, claims-Q1).>
- **Question.** <one clear line — the consumer question>
- **Links to.** §<N> P<x>.S<y>  ·  serves: <claim id / stage>  ·  track: <citation | values | display | discovery | decision | wording>
- **Description.** <2-4 short sentences: what is uncertain, why it matters, what a good answer looks like>
- **Answer (from the group).** _pending — filled by PROBE_

<tpl: repeat ### Q<n> for EVERY placeholder / display need / heavier need. At PROBE-run time, heavier bank questions are DISPATCHED via `1-probes/PP<NN>_<topic>.md` (executor-facing q-executor:, no stake) + a `1-probes/README.md` bullet row (`- PP<NN> · <stage/section> · <state> · <one-line need> · file: <path>`); the harvested answer flows BACK into that question's Answer field. A missing display unit is never a question — it is a DR row for the 4-display inbox (section-edit never creates displays).>

---

## Settled Flags (not open questions — logged, no action)

- <accepted deviations / already-ruled items / placeholder rollups that resolve paper-local (e.g. `{VAL:? x} -> paper-local: _VALUES_...`) — bullet lines, never a table>

---

## My Notes & Feedback — JL
<!-- Yours. Agents never overwrite below this line. Add rulings, priorities, extra questions, corrections. -->

_(empty — add your notes here)_

<tpl: after filling: verify `grep -c '<tpl' {section}.md` -> 0, then present structure + the questions raised and ⛔ STOP for the user's review. Do not advance without the user's verb.>
