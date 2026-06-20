# Write Principles — Paper Revision Reference

A condensed rule reference for any `.tex` paper-revision pass driven by `paper-revise-section` or its companion `paper-revise`. Distilled from the npjDM2025 v0516-v0519 sessions. Rules in this file SUPERSEDE skill defaults when they conflict. Hard-rule recaps are intentional: this is the single sheet to scan before applying edits. Project-specific items (canonical terminology, reviewer-id schema) live in each paper's own `1-feedback/v<tag>/` folder, not here.

---

## A. Comment preservation (audit trail)

| Rule | Spec |
|---|---|
| **A1** | JL's `%% Comments: {JL} v<DATE>:` lines are IMMUTABLE. Never compress, summarize, paraphrase, translate, or replace them. Recap of SKILL.md Hard Rule 1. |
| **A2** | Mixed CN/EN inside a JL comment is INTENTIONAL. Never translate the Chinese portion. |
| **A3** | One commenter, one line. Use a fresh `%% Comments: {INITIALS} v<DATE>:` line per author per round; never overwrite another author's line. |
| **A4** | Same-day roundtrips use `v<DATE>-N` suffix: `v0517` → `v0517-2` → `v0517-3`. Stable, parseable, follows the dialogue thread. |
| **A5** | Bracket notes inside index headers stay brief and use `--` (double-hyphen) NOT em-dash. Format: `%% ---- P1.S3 [NEW per v0517 -- short reason] ----`. |

**Reply-block canonical format**:

```
%% ---- P1.S2 ----
Active sentence here.
%% Comments: {CC} v0517: short audit note.
%% Comments: {JL} v0517: user feedback verbatim, mixed CN/EN as written.
%% Comments: {CC} v0517-2: response to JL; what changed and why.
%% Comments: {JL} v0517-3: follow-up if any.
%% Comments: {CC} v0517-3: final response.
```

CC chains MAY extend on one line via `========>` only when the chain is CC-only (no JL line being chained over). Single-line CC replies preferred (skill memory rule).

---

## B. Anti-AI-voice prose

Recap of SKILL.md Hard Rule 4 + concrete don't-lists.

| Category | Drop these |
|---|---|
| Buzzwords | "demonstrated", "exhibited", "leveraging", "novel", "unprecedented", "comprehensive", "powerful", "remarkable", "state-of-the-art" |
| Throat-clearing | "In this study", "Interestingly", "It is worth noting that", "Importantly", "Notably" |
| Verbs | Prefer plain: "scored", "ranked", "had", "is". Avoid: "demonstrated", "exhibited", "achieved", "manifested". |
| Em-dashes | Never (`—`, U+2014). Use comma, colon, semicolon, "which" clause, or two sentences. |
| Italics on plain nouns | Only for genuine load-bearing contrast or established convention (statistical symbols, figure-panel labels). |
| Parenthetical name-explosions | After first definition, use the abbreviation or short form. Don't repeat the trait roster five times. |
| Framing around numbers | Numbers and CIs stay verbatim. Drop "achieved", "exhibited", "remarkable", "substantial" wrapping them. |

**Read-aloud test**: if a tired reviewer would not naturally string the clauses this way out loud, recompose.

---

## C. Structural rules

| Rule | Spec |
|---|---|
| **C1** | ≤6 sentences per paragraph (hard ceiling). 7+ → COMPRESS, don't split into more paragraphs. |
| **C2** | Compress, don't split. Trigger at >30 words; nearly mandatory at >35. Drop adjectives, parentheticals, hedging, AI-voice tails (Section F recipes) FIRST. Only split when two genuinely distinct facts cannot be compressed without losing data. **Caveat: long-but-clear beats short-but-broken.** If dropped words carry load-bearing context (logical contrast X vs Y, methodological qualifier, disambiguation from related concept), KEEP the sentence. Recap of SKILL.md Hard Rule 5. |
| **C3** | One sentence per `%% ---- Pn.Sm ----` block. Splits get their own block (`Sxa`/`Sxb` or cascade-renumber). Two sentences sharing one marker violates file-local monotonicity. |
| **C4** | No orphan 1-sentence preview paragraphs. If a 1-sentence paragraph announces "we will benchmark and then apply", merge it into the downstream paragraph that does the work. |
| **C5** | Each paragraph has one logical role. Don't mix prompt-design with output-processing, or model-selection with model-evaluation, in one paragraph. |
| **C6** | Narrate, don't preview. Order is: design → evaluate → results → selection. No upfront roadmap paragraph. |

**Paragraph-numbering (file-local, recap of SKILL.md Hard Rule 2)**:

- Each `0-sections/0X-YY_*.tex` restarts at `P1.S1`. No continuous numbering across files.
- Paragraph splits during work-in-progress (Phase 2) MAY use `P20a, P20b, ...` as transient labels; clean-up phase (Phase 3) renumbers to sequential `P3, P4, P5, ...`.
- Sentence splits within a paragraph stay at `Sxa`/`Sxb` PERMANENTLY; don't renumber across split sentences within one paragraph.

---

## D. Content rules

| Rule | Spec |
|---|---|
| **D1** | No duplicate facts across sentences or paragraphs. Before adding a fact, scan for nearby restatement. A schema (e.g. "score / evidence / consistency / sufficiency") should be described ONCE. |
| **D2** | Separate epistemic layers explicitly. Template: name (a) the directly observed signal, (b) the latent construct the signal proxies, (c) the unobservable ground truth the construct is sometimes confused with. Claim validation only for (a)↔(b), not access to (c). |
| **D3** | Paragraph-purpose alignment. If a paragraph exists to "support why we chose model X", every sentence supports that claim; don't derail into adjacent results. |
| **D4** | Highlight load-bearing entities by ordering. In a list of N options where one is the paper's final choice, put that one FIRST. |
| **D5** | Keep reproducibility detail, drop implementation flavor. Keep: anchor levels, rating scales, panel sizes, MAE values, judge identity, hyper-parameters that affect results. Drop: "structured XML output", "JSON-formatted", "schema-validated", "via the OpenAI API". |
| **D6** | No internal codebase paths in paper-visible text. Never put `\texttt{tasks/...}`, `code/...`, or any other build-system path into figure captions, table captions, section prose, or any rendered text. Provenance breadcrumbs belong in (i) the rebuttal letter, (ii) Data/Code Availability statement, (iii) the project's revision checklist. `\includegraphics{../../tasks/...}` source paths are fine — they don't render. |

---

## E. Verification rules

| Rule | Spec |
|---|---|
| **E1** | Numbers must be source-anchored. Before citing `n = 226,999` or `MAE = 0.0949`, check the source CSV / parquet / SUMMARY.md and confirm the value matches the claim. Different cohorts have different n's; pick the one that matches the claim. |
| **E2** | Don't make completed work sound unfinished. If all 5 annotators completed all 200 cases, the paper says "complete hard-case panel (200 cases, 5 annotators)", not "160 returned so far". |
| **E3** | Verify external URLs before citing. Vendor product landing pages drift (model URLs change as new versions ship). Prefer stable documentation roots over product landing pages. |
| **E4** | Verify `\label{sec:foo}` exists before writing `\ref{sec:foo}`. Grep the repo; if missing, either add the label or revise the reference. |
| **E5** | When the user comment has a typo on a number, USE the verified value (not the typo); flag the discrepancy in the CC audit line. |

---

## F. Compression recipes (apply in order, cheapest first)

The operational heart of "compress, don't split". Each recipe is a concrete pattern caught in v0518-v0519 passes.

| Recipe | Pattern | Example |
|---|---|---|
| **F1** | Drop AI-voice tails | "...natural groupings of physicians by their overall trait profiles, yielding distinct archetypes with implications for patient care" → drop the "yielding... implications for..." tail. |
| **F2** | Drop redundant qualifier labels in numeric lists | After first `($|d|$ = 0.177, 95\% CI [0.167, 0.186])`, subsequent items drop the labels: `0.164 [0.154, 0.175]`. The pattern carries; provenance lives in one footnote sentence. |
| **F3** | Compress 3-4 item parenthetical lists by collapsing modifiers | "stigma around mental health treatment" → "mental-health stigma". "the emotional complexity of psychiatric encounters" → "encounter complexity". Each item drops the `[head] [of/around X]` frame. |
| **F4** | Eliminate word repetition | If a key word ("evaluation", "physicians", "patient") appears 3+ times in one sentence, restructure. One occurrence usually becomes implicit from context. |
| **F5** | Drop nested sub-explanations | "creating more challenging evaluation contexts (particularly relevant for Psychiatry, where patients with mental health conditions may have different evaluation patterns)" → "creating more difficult evaluation contexts (notably Psychiatry)". |
| **F6** | Drop qualifiers implicit from section context | "one-way ANOVA over specialty" → "one-way ANOVA" when the paragraph is about specialty. Same for throat-clearing like "as we have shown above". |
| **F7** | Compress 4-item subject/object lists by trimming the longest modifier | "rater behavior, contextual expectations, language asymmetry in patient descriptions of physicians, or genuine differences in behavior" → "rater behavior, contextual expectations, or genuine behavioral differences". Trim the longest item when remaining items still name the load-bearing alternatives. |

**Stop-rule for compression**: after applying recipes, if remaining words encode a logical contrast, methodological qualifier, or disambiguation, STOP. Long-but-clear beats short-but-broken (C2 caveat).

---

## G. Workflow rules

| Rule | Spec |
|---|---|
| **G1** | Diagnose-first for sections with >5 paragraphs. Produce a 🔴/🟡/🟢 severity-ranked table BEFORE editing. User reviews diagnosis; edits proceed in severity order. Recap of `paper-revise-section` Step 3. |
| **G2** | Paste-as-merge convention. When the user pastes a `% commented-out` index header next to a different paragraph block, the intent is MERGE the two sentences/paragraphs into one. |
| **G3** | User-pasted edit = authoritative. When the user pastes their own draft and says "follow", apply their structure; don't argue for a different one unless asked. |
| **G4** | Comment hygiene after structural change. After paragraph rename/split/merge: (a) DROP "was Pn.Sm" provenance notes (git diff captures them); (b) DROP forward-looking labels in comments ("P20a = omnibus framing") since the new header already states the role; (c) DROP bracket annotations on headers once their content has been consumed into the prose, especially any containing em-dashes (B violation). |
| **G5** | Reviewer-id tag in CC comments (when applicable). Format: `%% Comments: {CC} v<DATE>: R2 M5 -- short reason.`. Use the project's reviewer-id schema (e.g. `R1 W7`, `R2 M5`, `Editor E.4a`). Multi-point sentences chain: `R1 W1 + R2 M5 -- ...`. The project's `1-feedback/v<tag>/` defines the schema. |
| **G6** | Per-section reports and revision-checklist files are PROJECT-SPECIFIC. Some projects forbid per-section `.md` reports during revision (npjDM2025 does); some forbid checklist updates during per-section audits. Check the project's `1-feedback/v<tag>/INSTRUCTIONS.md` (or equivalent) for the project rule. |

---

## H. Post-iteration code-claim audit

These patterns kick in AFTER iterative editing has converged on a section, before submission or co-author handoff. They catch drift that per-section iteration does not.

| Pattern | Trigger | Mechanism |
|---|---|---|
| **H1 — Bidirectional code-claim audit** | After methods section converges; within 2 weeks of submission. | (a) **Phantom-hunt**: for every procedure claimed in methods, grep the analysis scripts under `tasks/`. Zero hits → phantom. Drop, run, or soften the claim. (b) **Gap-hunt**: read results section; for every reported number, verify methods describes the procedure that produced it. If absent, add a short procedure sentence. |
| **H2 — Cargo-culted numbers** | Anytime a specific n / range / statistic appears in methods. | For every n / range / statistic, find the source CSV or Python output. If methods cites a number it cannot defend with provenance, replace with a qualitative descriptor (e.g. "complete-case sample"). |
| **H3 — Fresh-agent audit** | After per-section iteration converges; iterative author is blind to own drift. | Spawn a fresh-context auditor (Agent tool, `subagent_type=general-purpose`, empty context). Prompt template: scope files (methods + cross-check results + relevant `tasks/*.py`); list recent edits + known-deferred; ask for severity-ranked diagnosis with code-grep evidence cited; stipulate READ-ONLY; word budget ~800. Catches cross-file drift, terminology inconsistency, and the auditor's own misclassifications that single-file iteration misses. |

---

## I. Pre-save checklist

Before committing a section-file edit:

- [ ] All JL `%% Comments:` lines preserved verbatim, no translation or compression?
- [ ] New CC line added on its OWN line (not overwriting JL's)?
- [ ] No em-dash (`—`) in active sentence or bracket annotations?
- [ ] No buzzwords from Section B?
- [ ] Each `%% ---- Pn.Sm ----` block holds exactly ONE sentence?
- [ ] Paragraph ≤6 sentences total?
- [ ] No sentence >30 words without justification (compression recipes Section F applied)?
- [ ] Numbers source-anchored against a file under `tasks/.../results/` (E1)?
- [ ] No duplicate fact with a nearby sentence (D1)?
- [ ] Citations exist in the bib for every named model/paper?
- [ ] No internal codebase path leaked into paper-visible text (D6)?
- [ ] Reviewer-id tag in CC comment if the edit addresses a reviewer point (G5)?
- [ ] P-numbers are file-local; this file starts from `P1` (Hard Rule 2)?

---

## Where the rules live (cross-reference map)

| Topic | Authoritative source |
|---|---|
| Em-dash ban, JL verbatim preservation, file-local PN.SN, compress-not-split ceiling, ASCII-only diagrams, no `.md` reports | SKILL.md Hard Rules 1-7 |
| AI-voice anti-pattern checklist (read-aloud test, parenthetical adverbs, callbacks, etc.) | SKILL.md Hard Rule 4 |
| Logic-diagram format (ARC, Roles, boxes, role-emoji, action format) | SKILL.md Step 4 |
| Compression recipes (sentence-level patterns) | This file Section F |
| Comment preservation conventions (A1-A5, reply-block format) | This file Section A |
| Post-iteration code-claim audit | This file Section H |
| Per-project canonical terminology / reviewer-id schema | `<paper>/1-feedback/v<tag>/INSTRUCTIONS.md` and project memory |
| Per-project rebuttal-letter format (`\paperedit{}`, etc.) | `<paper>/1-feedback/v<tag>/INSTRUCTIONS.md` |
