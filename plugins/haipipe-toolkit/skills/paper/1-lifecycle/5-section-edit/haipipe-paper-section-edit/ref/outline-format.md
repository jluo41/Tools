# Section .md Format Spec (the working document)

The section `.md` is the primary working document for section-edit. **Scaffold it by copying `ref/section-template.md`** (the fill-in skeleton; this file is its rulebook) — fill the `<slots>`, delete the `<tpl:` guidance lines, and gate on `grep -c '<tpl' = 0`. It lives at `0-lifecycle/5-section-edit/{section}/{section}.md`. DRAFT creates it with REAL prose, PROBE fills its placeholders' sources, REVISE polishes its sentences and syncs to tex, CHECK verifies everything matches.

**The .md holds real paper prose** (JL ruling 2026-07-09, supersedes the "lean plan" model): complete academic sentences the user can review as a paper — not telegraphic notes, not a skeleton. The `.tex` is GENERATED from it by sync; tex prose is never edited directly.

## File structure

```markdown
# Section N: Title -- Structure

venue: MISQ 2026 · section-type: methods (+results flavor)
blueprint: 0-lifecycle/2-venue/2-venue.md (methods block)   <- BINDING: budget, structure, density
style: _venue/playbook-utd-is/MISQ/MISQ-methods/style.md · MISQ-results/style.md   (reference only)

\```
§N.1 Subsection Title (K paragraphs)
  P1. Short paragraph job description                        5 sentences · ~110 words
  P2. Short paragraph job description                        5 sentences · ~120 words
  P3. Short paragraph job description                        4 sentences · ~95 words

§N.2 Subsection Title (K paragraphs)
  P4. Short paragraph job description                        5 sentences · ~105 words

total: 4 ¶ · 19 sentences · ~430 words   (venue budget for this section: ~500)
\```

---

## §N.1 Subsection Title

### P1. Why LLM scoring is credible here

(enabler framing; cites companion pipeline paper)

We score each review with the pipeline validated in \citep{authors2025npjdm}.

The model recovers human-perceived agreeableness at MAE {VAL:? cross-model MAE}.

Agreement with human annotators falls within the human-human range.

> USER: this claim feels strong, soften?
> CC: softened to "closely tracks" — will land in REVISE.

---

### P2. What this paragraph does

(Preview of key points.)

First real sentence of the paragraph.

Second real sentence, citing prior work as \citep{wang2022reviews} when the key is already in the .bib, or \cite{TOADD} when it is not.
```

## Three elements per paragraph

1. **Heading + preview**: what this paragraph does and why it's here (preview = ONE short line, ~80-120 chars, a scan hook)
2. **Prose sentences**: REAL draft prose, one sentence per line, blank line between sentences
3. **Comments**: `> USER:` / `> CC:` threads under the sentence they discuss (preserved verbatim; see binding rules)

## Rules

- **Venue header under the H1** (written ONCE at scaffold by DRAFT): `venue:` (the pin from STATUS.md), `section-type:` (this section's mapping, e.g. 4-llmtrait → methods), `blueprint:` (the paper's 2-venue.md block — the authoritative digest), `style:` (the deep-dive pack file, resolved from the blueprint's `[source:]` tag). Resolve the pack path layout-agnostically — installed skills flatten the tree: `VEN=$(find ~/.claude/skills "$CLAUDE_PLUGIN_ROOT" -type d -path '*skills/paper/_venue' 2>/dev/null | head -1)` — and record the RESOLVED path so later phases (and the user) follow the link instead of re-deriving it. Pack file absent → write `style: (pack missing — blueprint only)` and flag for CHECK. **The blueprint is BINDING** (word budget, ¶ structure, citation density, display limits); **the style file(s) are REFERENCE ONLY** — mine them for arc, signature moves, and exemplar sentences, but deviation is fine and never a CHECK failure. A hybrid section (e.g., a methods section that reports validation results) lists MORE THAN ONE style reference, `·`-separated.
- **Structure overview at top** (update whenever structure changes)
- **Counts in the overview**: each `Pn` line carries `N sentences · ~M words` (approximate, `~`); a `total:` line closes the block with ¶ / sentence / word totals against the venue budget from `2-venue.md`. Recount whenever the block is updated (draft, and after REVISE); over budget → flag it, don't silently trim.
- `##` for subsections, `###` for paragraphs
- **Sentences are REAL prose**: complete academic sentences close to submission register. Content-complete; verification and polish come later. If a sentence can't be written because a fact is missing, write it anyway with a placeholder.
- **One sentence per line, blank line between sentences** (each becomes a `Pn.Sn` marker when synced to tex). Never prefix sentences with numbers (`S1.` etc.) — Pn.Sn indexing lives only in tex.
- **Citations are REAL, placeholders greppable, nothing guessed** (JL ruling 2026-07-10, supersedes `[CITE: <topic>]` + parenthetical "(Author Year)"; legacy `[CITE:]` markers in old drafts are treated as `\cite{TOADD}`):
  - `{VAL:? <what the number is>}` — a number that PROBE/values must trace to a source
  - `\citep{key}` / `\citet{key}` — a real citation whose key EXISTS in the paper's .bib. Grep the .bib (and `_CITATION_`) FIRST; writing a key that does not grep in .bib is inventing a citation
  - `\cite{TOADD}` — a citation slot with no suitable .bib key yet. EVERY `\cite{TOADD}` is paired with a `_CITATION_` row naming the topic + expected source (the prose stays clean; the map carries the topic). `grep -c TOADD` = open slots; a TOADD surviving into compiled tex fails CHECK (broken-\cite check)
- **Target 5-6 sentences per paragraph** (MISQ/ISR norm; consult section-type for venue-specific)
- **USER comments as `> USER:` text**, CC responses as `> CC:` text, directly under the sentence discussed
- **Comment lifecycle (binding)**: the agent NEVER deletes, rewords, or relocates a `> USER:` comment; it replies underneath; only the user declares a thread resolved; resolved threads MOVE to `_LOG` verbatim; each phase starts with a clean file
- **Surgical edits only**: change the specific lines under discussion. A full-file rewrite of a .md carrying `> USER:` comments is forbidden.
- **Never a tex mirror**: no LaTeX markup EXCEPT citation commands (`\citep`/`\citet`/`\cite{TOADD}` — the one construct that syncs to tex verbatim), no `%%` markers, no agent monologue in the .md

## Draft prose is NOT

- NOT verified (that's PROBE: `{VAL:?}` and `\cite{TOADD}` stay until traced)
- NOT venue-polished (that's REVISE: humanizer, sentence economy, weave)
- NOT LaTeX (that's sync-to-tex after REVISE)
- NOT the agent's scratchpad (analysis and options belong in the session, not the file)

DRAFT prose settles WHAT each sentence says, in real sentences. REVISE settles HOW it sounds. If a sentence says the wrong thing, fix it in the .md during DRAFT (or restart DRAFT). If it says the right thing but sounds bad, REVISE fixes it — in the .md first, then sync to tex.

## Probe proposal (the draft's last block)

The draft ENDS by proposing the probe work it just created. DRAFT proposes; PROBE executes (after the gate). The block is the last section of the .md:

```markdown
---

## Q-Paper proposed by this draft

values:    {VAL:? cross-model MAE}            -> expected source: npjDM Table 2 / tasks/ run
           {VAL:? mean agreeableness}         -> paper-local: 0-displays/table1-.../source/metrics.json
citation:  \citep{authors2025npjdm}           -> key in .bib, verify placement only
           \cite{TOADD} @ P2.S1 (ML trait-measurement priors) -> _CITATION_ row #4; needs discovery sweep (buffered: PP12)
display:   P2 wants the trait-distribution figure -> 0-displays/ unit exists? LINK : DR request (4-display inbox)
heavier:   case-mix robustness needs a NEW task run (buffered: PP13)
```

Rules:
- Derived from the prose: every `{VAL:?}` and `\cite{TOADD}` placeholder appears here with its EXPECTED source (pointer-following first); `\citep{key}` citations appear only if placement needs verifying. When the draft already SEES the pointer in the paper's own registries, say so — `-> paper-local: _VALUES_6-results.md` / `0-displays/<unit>/source/metrics.json` — and PROBE closes it with nothing dispatched (`answered-local`).
- Display needs are stated per paragraph.
- Anything heavier than pointer-following (a new task run, a lit sweep) is RAISED as a `state: planned` question SECTION in `1-probes/PP<NN>_<topic>.md` (one file per TOPIC) + a Status board row. The section carries serves: / target: / state: / q-executor: (the question in GENERAL language — no claim ids, no stake), and an EMPTY a-consumer: — DRAFT proposes, it never executes.
- **Board rows are bullet lines, never markdown tables** (JL standing rule — no tables in probe documents; the checker enforces it inside probe files). Append one line per probe file to `1-probes/README.md`:
  `- PP<NN> · <stage/section> · <state> · <one-line need> · file: <path>` EXCEPTION: a missing DISPLAY UNIT never becomes a question SECTION — it becomes a DR row in `0-lifecycle/4-display/_DISPLAY_REQUEST.md` (section-edit never creates displays; the display stage solves requests).
- The ⛔ STOP presentation shows this block, so the user reviews the STRUCTURE and the QUESTIONS RAISED at the same gate.

## Populating from existing tex (backward fill)

When the section already has prose in `0-sections/*.tex`:

1. Read the tex file
2. Extract paragraph structure (from `% Para [id]` banners or `%% ---- Pn.Sn ----` markers)
3. For each paragraph: create the heading + preview, then copy the sentences as prose lines (one per line, blank-line separated, markers stripped)
4. Preserve any existing `> USER:` comments from prior editing rounds exactly where they were
5. Present the populated .md to the user for review

This is a BACKWARD FILL: tex -> .md, done ONCE at scaffold time. From then on the .md is the source and tex is sync output.

## Inputs for section drafting

1. **z-structure**: `0-lifecycle/5-section-edit/z-structure/z-structure.md` (paper-level architecture)
2. **Narrative**: `0-lifecycle/3-narrative/3-narrative.md` (the story beats)
3. **Existing tex**: `0-sections/NN_section.tex` (if the section already has prose)
4. **Section-type**: `section-type/section-{type}/SKILL.md` (structure norms for this section type)
5. **Venue contract**: `0-lifecycle/2-venue/2-venue.md` (blueprint + writing principles; `_venue/` packs = fallback / deep dive)
6. **Claims**: `0-lifecycle/1-claims/1-claims.md` (what claims this section needs to support)

## Done-criteria for section DRAFT

- [ ] `grep -c '<tpl' {section}.md` = 0 (template fully instantiated, no guidance residue)
- [ ] Every paragraph has a heading, preview, and real prose sentences
- [ ] Structure overview matches the paragraph blocks
- [ ] Every unverified number is a `{VAL:?}`; every citation gap a `\cite{TOADD}` + `_CITATION_` row; every `\citep{key}` greps to a real .bib entry (nothing invented)
- [ ] "Q-Paper proposed by this draft" block at the end covers every placeholder + display need; heavier needs buffered as planned PP skeletons in `1-probes/` + Status board row
- [ ] ⛔ The user has reviewed the STRUCTURE + the QUESTIONS RAISED and approved (no open structural `> USER:` questions)
- [ ] _LOG has a `[GATE] draft-review: approved` entry quoting the user

## _LOG entry format for DRAFT

```markdown
## YYYY-MM-DD #N ~HH:MM [GATE] draft-review: approved
> USER: "looks good, go"

## YYYY-MM-DD #N ~HH:MM [DRAFT]
> USER: original comment
> CC: response
-> applied / rejected / deferred
- Created section .md with N paragraphs, M sentences, K {VAL:?} + J \cite{TOADD} slots, L \citep{} keys from .bib
- Key decisions: [structural choices from resolved comments]
```

## Relation to REVISE

```
DRAFT                                  REVISE
-----                                  ------
settle WHAT to say                     settle HOW to say it
real prose, one sentence per line      venue-quality prose, humanized
\citep{key} from .bib + \cite{TOADD}   verified values; TOADD resolved to real keys
content decisions                      sentence economy, voice, flow
writes the .md                         revises the .md, THEN syncs to tex
```

The draft prose is the INPUT to REVISE. Both phases work the `.md`; only sync touches tex.
