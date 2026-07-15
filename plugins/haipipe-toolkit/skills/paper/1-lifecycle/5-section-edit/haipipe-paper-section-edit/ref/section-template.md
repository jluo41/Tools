<tpl: THIS FILE IS A TEMPLATE. DRAFT copies it to 0-lifecycle/5-section-edit/{section}/{section}.md and fills it in.>
<tpl: Fill every <angle-bracket> slot. DELETE every line starting with "<tpl:" as you fill — a finished .md contains ZERO of them. Mechanical gate: `grep -c '<tpl' {section}.md` must print 0 before the ⛔ STOP presentation.>
<tpl: Rules live in ref/outline-format.md (read it once per session). This file is only the SHAPE. Content norms come from the venue blueprint (2-venue.md block, BINDING) + section-type/section-<type>/SKILL.md (structure norms) + the style pack file(s) (REFERENCE ONLY).>

# Section <N>: <Title> -- Structure

venue: <MISQ 2026> · section-type: <methods (+results flavor)>
blueprint: 0-lifecycle/2-venue/2-venue.md (<methods> block)   <- BINDING: budget, structure, density
style: <resolved _venue path, e.g. _venue/playbook-utd-is/MISQ/MISQ-methods/style.md · MISQ-results/style.md>   (reference only)
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

## Q-consumer proposed by this draft

<tpl: derived FROM the prose — every {VAL:?} and \cite{TOADD} above appears here with its EXPECTED source. Pointer-following first: if the draft already sees the pointer in the paper's own registries, say `-> paper-local: <file>` and PROBE closes it `answered-local` — nothing is dispatched.>

values:    {VAL:? <what>}                       -> <expected source: paper-local _VALUES_/metrics.json | tasks/ run>
citation:  \cite{TOADD} @ P<n>.S<n> (<topic>)   -> <check prior stages' _CITATION_ / .bib first | discovery sweep (buffered: PP<NN>)>
display:   P<n> wants <display>                 -> 0-displays/ unit exists? LINK : DR request (4-display inbox)
heavier:   <need requiring a new task run / lit sweep>  (raised: PP<NN>, state: planned)
<tpl: heavier needs -> a `state: planned` question SECTION in `1-probes/PP<NN>_<topic>.md` (one file per TOPIC; the section carries serves:/target:/state:/q-executor:, with an EMPTY a-consumer:) + its Status board row in `1-probes/README.md`. EXCEPTION: a missing display unit is never a probe section — it is a DR row for the 4-display inbox (PROBE files it; section-edit never creates displays).>
<tpl: index row = a BULLET LINE, never a markdown table (JL standing rule: no tables in probe documents). Shape — append verbatim, one per PP:>
<tpl: - PP<NN> · <stage/section> · <status> · <one-line need> · card: <path>              >
<tpl: after filling: verify `grep -c '<tpl' {section}.md` -> 0, then present structure + the questions raised and ⛔ STOP for the user's review. Do not advance without the user's verb.>
