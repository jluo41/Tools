---
name: paper-weaving
description: "Orchestrator for paper-revision work on a single LaTeX file. Parses intent across granularity (section / paragraph / sentence) and verb (diagnose / apply / check / write), then either runs the built-in section-diagnose workflow inline or dispatches to a specialist via Skill(). Default route (when intent is unscoped or section-level) embeds an ARC + Roles header at the top of the .tex, per-paragraph 📌 NOW / 🔧 PROPOSE blocks immediately above each `%% ---- PN.S1 ----` marker, and an optional 💭 LOGIC DISCUSSION block at the bottom — no sidecar .txt files. Three lifecycle gates: (G1) STOP after embedding the plan and ask the author to review the .tex before any prose edits; (Q) auto-fire quality check after every PROPOSE action is APPLIED — fans out via Skill() to paper-check-numeric / paper-check-reference / paper-claim-audit (configurable) plus inline cheap scans (em-dash, AI-voice patterns, sentence-length, marker monotonicity); (G2) after Gate Q passes or the author acknowledges its failures, PROMPT the author to manually delete the residual plan blocks (skill never auto-deletes). Use when the user says /paper-weaving, asks to weave / revise / diagnose / rework a section, paragraph, or sentence in a .tex file with %% Comments: {INITIALS} annotations, or wants to plan + apply edits to a paper section."
argument-hint: [granularity-or-verb] [path] [args...]
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Skill
---

Skill: paper-weaving (orchestrator)
====================================

One-stop entry for revision work on a single LaTeX file. Parses intent,
either runs the **built-in section-diagnose workflow** inline (the default
route, used to be `/paper-revise-section`) or **dispatches** to a sibling
specialist via `Skill()` when the user names a smaller granularity or
asks for a check.

The deliverable for the default route is **the .tex file itself**:
plan content (ARC, Roles, per-paragraph NOW + PROPOSE blocks) is embedded
as LaTeX `%%` comments. No sidecar `.txt`. The .tex compiles unchanged
(comments strip at build time); the plan and the prose live side by side
in one file, version-controlled together.

The skill has **three lifecycle gates** (see "Approval gates" below):

- **G1: review the plan before any prose edits.** After Step 4 inserts
  the plan blocks, STOP and ask the author to approve / redirect before
  any prose changes are applied (typically by `/paper-revise`).
- **Q: auto quality check after every PROPOSE action is APPLIED.**
  paper-weaving fans out via `Skill()` to a configurable list of sibling
  check skills (`paper-check-numeric`, `paper-check-reference`,
  optionally `paper-claim-audit`) AND runs an inline cheap scan
  (em-dash, AI-voice anti-patterns, sentence-length, marker monotonicity,
  paragraph ceiling). It aggregates a unified PASS / FAIL summary and
  presents it to the author before Gate G2.
- **G2: clean up the plan blocks after Gate Q passes.** Once Gate Q
  passes or the author acknowledges its failures, PROMPT the author to
  manually delete the residual plan blocks. The skill NEVER auto-deletes
  its own plan blocks; the author owns the cleanup decision.

---

Usage
-----

```
/paper-weaving                                -> dispatch help (lists specialists)
/paper-weaving <path>.tex                     -> default: section-level diagnose, embed in .tex
/paper-weaving section <path>.tex             -> same as above (explicit granularity)
/paper-weaving paragraph <path>.tex P<n>      -> dispatch to paper-revise-paragraph
/paper-weaving sentence <path>.tex P<n>.S<m>  -> dispatch to paper-revise-sentence
/paper-weaving check numeric <path>.tex       -> dispatch to paper-check-numeric
/paper-weaving check reference <path>.tex     -> dispatch to paper-check-reference
/paper-weaving write <path>.tex               -> dispatch to paper-write
/paper-weaving check <path>.tex               -> Gate Q on demand (runs all configured checks)
/paper-weaving cleanup <path>.tex             -> Gate G2: prompt author to delete plan blocks
/paper-weaving "<natural language>"           -> infer granularity + verb, route accordingly
```

---

Specialists
-----------

```
paper-weaving (this)         section-level diagnose + plan embedded in .tex  (DEFAULT route)
paper-revise-paragraph       paragraph-level rewrites + comment iteration
paper-revise-sentence        sentence-level edits, JL %% Comments: dialogue
paper-revise                 broader multi-pass interactive revision flow
paper-check-numeric          verify every quantitative claim against raw results
paper-check-reference        verify every citation against bib + venue metadata
paper-write                  draft a new section from PAPER_PLAN.md outline
```

`/paper-revise` is a sibling, not a child. paper-weaving routes to it
when the user asks for a broad multi-pass review rather than a single
diagnose + plan pass.

---

Routing
-------

### Step R1. Parse `$ARGUMENTS`

Pull these out of the input in any order:

- **path** — first token ending in `.tex`
- **granularity** — one of `section`, `paragraph`, `sentence`
- **verb** — one of `diagnose`, `apply`, `check` (= Gate Q on demand), `write`, `cleanup`
- **target locator** — `P<n>` or `P<n>.S<m>` if the user named a specific paragraph or sentence

### Step R2. Granularity keyword map

```
section, this section, revise this section, weave, /paper-weaving                -> section
paragraph, P<n>, this paragraph, rework P<n>, this para                          -> paragraph
sentence, S<n>, P<n>.S<n>, this line, this sentence, rewrite this                -> sentence
write, draft, from outline, /paper-write                                         -> write
```

### Step R3. Verb keyword map

```
diagnose, audit, plan, what's wrong, severity, ARC, Roles                        -> diagnose
apply, fix, rewrite, edit, apply propose                                         -> apply
check, quality check, post-apply check, run Q                                    -> check (Gate Q on demand)
check numbers, verify numbers, check stats, MAE, κ, percentages, sample size     -> check-numeric
check refs, verify citations, check bib, dead entries, BibTeX                    -> check-reference
write, draft from outline                                                        -> write
cleanup, clean up, delete plan blocks, scrub comments, ready to submit           -> cleanup (Gate G2)
```

### Step R4. Routing logic

```
Step 1. Verb = cleanup?                       -> Gate G2 prompt (see "Approval gates")
Step 2. Verb = check (Gate Q on demand)?      -> Run Gate Q substeps Q1+Q2+Q3 against path
                                                 (see "Gate Q — Auto quality check after apply")

Step 3. Resolve granularity:
  - No granularity inferred, path ends .tex     -> SECTION (default route)
  - granularity = section / unspecified         -> SECTION (default route)
  - granularity = paragraph                     -> dispatch to paper-revise-paragraph
  - granularity = sentence                      -> dispatch to paper-revise-sentence
  - granularity = write                         -> dispatch to paper-write

Step 4. If verb suggests a specific check (not generic Q), override granularity:
  - verb = check-numeric                        -> dispatch to paper-check-numeric only
  - verb = check-reference                      -> dispatch to paper-check-reference only

Step 5. Dispatch (when not SECTION):
  Skill("<specialist-name>", args="<remaining args>")

Step 6. Default SECTION route:
  Run the inline workflow in "Default route: section diagnose" below,
  STOP at Gate G1, wait for author approval.
```

If neither granularity nor a clear verb can be inferred and the input
is just a `.tex` path, **default to the SECTION route**. This matches
the prior `/paper-revise-section` behavior.

If only a verb resolves and no path is given, ask which file (don't
guess across multiple open files).

---

Default route: section diagnose
================================

This is the work the skill does inline when the SECTION route fires.
Produces a severity-ranked diagnosis (in chat) and embeds the plan
**directly into the .tex file** as LaTeX comments. Does NOT apply prose
edits — applying is gated on G1 author approval, and is typically done
by `/paper-revise` or by hand-picking actions from the embedded plan.

The point is to make the **revision plan** visible and reviewable BEFORE
any prose changes. The embedded plan IS the deliverable.

Required input format
---------------------

The target `.tex` MUST use the two-marker convention:

1. **Paragraph / sentence index headers**, one per logical unit:
   ```
   %% ---- PN.SN ----
   ```
   - `PN` = paragraph number, `SN` = sentence number
   - Numbering is **file-local**: P1 restarts at the top of every section file
   - Optional bracket note allowed: `%% ---- P2.S7 [NEW per v0517] ----`

2. **Author comments**, attached to a specific sentence:
   ```
   %% Comments: {INITIALS} v<tag>: <free-form thoughts>
   ```
   - These are the *thinking* the skill reacts to
   - **Never rewrite, translate, summarize, or compress these lines**
   - They stay verbatim across every pass

If the file does not satisfy this format, the skill stops and reports
which paragraphs are missing markers. It does not silently auto-insert.

---

What the skill does (in order)
------------------------------

### Step 1. Format check

Read the file. Verify:
- every paragraph has a `%% ---- PN.SN ----` header
- `PN` numbering starts at 1 and is monotone within the file
- at least one `%% Comments: {…}` line exists (otherwise nothing to react
  to, bail out and tell the author)

If anything fails: print a short table of what's missing and stop.

### Step 2. Read the comments

For each `%% Comments: {…}` line, extract:
- which `PN.SN` it is attached to
- the verbatim text of the author's note

Do not paraphrase them in your response. Refer to them by `PN.SN` and
quote only the relevant phrase when needed.

### Step 2.5. Scan reviewer comments (conditional)

If `1-review/A-review-content/` exists in the paper folder, scan every
`.md` inside for reviewer items whose `File:Line` target falls in the
current section, or whose free-text description references content in
the current section. For each match record:

- **item id**: `R1 W6` / `R2 Maj-5` / `Editor E.4a` / `R1 free`
- **one-line content summary**: paraphrase the reviewer's ask
- **action type**: `text-change` / `analysis` / `reframe` / `concede`
- **paragraph anchor**: which `P<n>` in the current section the item
  lands on; mark `paper-wide` if it propagates across multiple sections

This list populates the `📋 Linked reviewer items` block in the embedded
header (Step 4a). Individual items get cross-referenced as `[R<n> <id>]`
bracket tags on any PROPOSE action that implements them.

If no `1-review/A-review-content/` directory exists or no items map to
the current section, **skip this step and omit the linked-items block**.

### Step 3. Diagnosis with severity ranking (in chat)

Print a compact table to the chat:

```
| Severity | Location | Problem | Fix sketch |
| 🔴 | P3 → P4 | ... | ... |
| 🟡 | P2 | ... | ... |
| 🟡 | P1.S3 → P2.S1 | ... | ... |
| 🟢 | P5 / P6 | OK | keep |
```

Rules:
- 🔴 = hard blocker (broken logic, redundancy across paragraphs, wrong order)
- 🟡 = compression / re-anchoring needed but the paragraph still has a role
- 🟢 = leave alone
- Always include at least one row per author-commented paragraph
- Rank by severity, not by file order

Do this BEFORE editing the .tex. The author should be able to read just
this table and know whether to proceed.

### Step 4. Embed the plan into the .tex

Insert three classes of `%%`-prefixed blocks into the `.tex` file:

- **Step 4a** — section-level header block (ARC + Roles + Linked reviewer items) at the top of the file
- **Step 4b** — per-paragraph block immediately above each `%% ---- PN.S1 ----` marker
- **Step 4c** — optional 💭 LOGIC DISCUSSION block at the bottom (only when the author flagged ARC-level structural problems)

All blocks are LaTeX comments (`%%` prefix on every line). They strip
silently at compile time. The .tex remains the single source of truth.
No sidecar `.txt` is written.

Every plan-block line opens with the sentinel `%%@` (instead of bare
`%%`). Author `%% Comments: {INITIALS}` lines and existing `%% ----
PN.SN ----` markers keep their bare `%%`. The `%%@` sentinel makes
Gate G2 cleanup a trivial regex (`^%%@`) — and makes accidental
overlap with author comments impossible.

#### Step 4a. Section-level header block (top of file)

Insert this block right after the file's existing top-of-file comments
(if any), and BEFORE the first content marker `%% ---- P1.S1 ----`. For
a file wrapped in an environment (e.g. abstract uses `\begin{abstract}`),
the block goes immediately INSIDE the environment, before the first
sentence marker.

Format:

```
%%@ ═══════════════════════════════════════════════════════════════════════════════
%%@ 📜 <Section name>  v<tag>  ·  Logic + Proposed Edits   [paper-weaving plan]
%%@ ═══════════════════════════════════════════════════════════════════════════════
%%@
%%@   ARC (<N>-paragraph flow):
%%@     <emoji> P1 <2-4 word verb-phrase>  →  <emoji> P2 <verb-phrase>  →  ...  →  <emoji> P<N> <verb-phrase>
%%@
%%@   Roles per paragraph (one line per paragraph; no line breaks within a line):
%%@     <emoji> P1: This paragraph <does X>.
%%@             │
%%@             ▼
%%@     <emoji> P2: This paragraph <does Y>.
%%@             │
%%@             ▼
%%@     ...
%%@
%%@   📋 Linked reviewer items (omit if Step 2.5 did not run):
%%@     [R<n> <id>]    <one-line content + action type + paragraph anchor>
%%@     [R<n> <id>]    ...
%%@
%%@   ⏳ Status: AWAITING AUTHOR REVIEW (Gate G1) — see end-of-file cleanup hint after edits applied.
%%@ ═══════════════════════════════════════════════════════════════════════════════
```

Rules:

- **ARC line is REQUIRED.** ONE line (or 2-3 lines wrapped for 7+ paragraphs). Each `P<N>` tag is a SHORT VERB-PHRASE (2-4 words capturing the paragraph's function); NOT a single word and NOT a full sentence. Use `→` (U+2192) Unicode arrows, not ASCII `->`. Examples (good): `motivate + intro archetypes`, `report archetype profiles`, `shape-vs-level ANOVA`, `bootstrap stability check`, `interpret + future-work`. Examples (bad, single word): `motivate`, `profiles`. Examples (bad, topic keyword with no verb): `traits`, `K-means`.
- **Roles block is REQUIRED.** ONE LINE PER PARAGRAPH (no wrap, however long). Use the SAME emoji as in the ARC and as in the per-paragraph block heading below. Separator after `P<N>` is `:` (colon), NOT em-dash. Insert `│` then `▼` connector between consecutive Roles entries.
- **Linked reviewer items** stays only if Step 2.5 produced at least one match.
- **No header noise**: do NOT add icon legends, `Comments read at:` inventories, `Cross-section dependency:` blocks, or figure callouts to this header. Those belong in 💭 LOGIC DISCUSSION (Step 4c) if at all.
- If a proposed edit changes a paragraph's role, the ARC + Roles entries reflect v<new>. The block always describes the proposed (v<new>) story.

#### Step 4b. Per-paragraph block

Insert one block immediately above each `%% ---- PN.S1 ----` marker
(i.e. above the first sentence of each paragraph). Format:

```
%%@ ───────────────────────────────────────────────────────────────────────────────
%%@ <emoji> P<N> · <ROLE LABEL>                                  [<status tag>]?
%%@
%%@   📌 NOW (S1-S<k>, ~Nw):
%%@     <role-emoji> S1  <compact paraphrase>
%%@     <role-emoji> S2  <compact paraphrase>
%%@     ...
%%@
%%@   🔧 PROPOSE (<delta>):
%%@     ➕ <role-emoji> S<n> NEW  "<draft text>"  [<inline why>]
%%@        │
%%@     📝 <role-emoji> S<m> (was S<k>)  <description>  [<inline why>]
%%@        │
%%@     ➖ <role-emoji> S<j> (was S<i>)  <reason>
%%@
%%@ ───────────────────────────────────────────────────────────────────────────────

%% ---- P<N>.S1 ----
<existing first sentence of paragraph>
...
```

Rules:

- **Heading line**: `%%@ <emoji> P<N> · <ROLE LABEL>          [<status tag>]`. `<emoji>` matches the ARC + Roles entry. `<status tag>` is right-flushed in `[…]`: one of `[MAIN EDIT v<tag>]`, `[APPLIED v<tag>]`, `[no v<tag> change]`, `[NEW PARAGRAPH]`. Tag is optional; omit when keep-as-is.
- **📌 NOW**: sentence-by-sentence compact paraphrase. ONE LINE per sentence. Format: `<role-emoji> S<n>  <compact paraphrase>`. Show sentence range + approx word count in the header: `📌 NOW (S1-S5 + S7-S9, ~137w):`. When content MOVES from another paragraph, annotate provenance: `📌 NOW (currently lives in v<old>.P3; ~95w):`.
- **🔧 PROPOSE**: concrete deltas, ONE LINE per action. Format: `<action-emoji> <role-emoji> S<n> [<position-tag>]  <description>  [<inline why>]`. `<action-emoji>`: ➕ add, 📝 edit, ➖ drop, ✅ keep, 🏷 tag-as-done. `<role-emoji>` matches the corresponding NOW line so a reader can scan column-wise. `<position-tag>` optional: `NEW` (for ➕), `(was S<k>)` (for renumbered). `<description>` is either the full quoted text in double-quotes (for ➕ or 📝 full rewrite) or a brief edit instruction (for 📝 phrase-edit or ➖ drop). `[<inline why>]` is OPTIONAL one-clause rationale; skip if self-explanatory. Do NOT write `Renumber:` or `Verify:` bookkeeping; the cascade is implied by `(was S<k>)` tags.
- **`│` separator** between consecutive PROPOSE actions: a single `%%@        │` line. (Distinguish from Roles connector `│ ▼` which is two lines = flow direction.)
- **Reviewer-item bracket tags**: append `[R<n> <id>]` to any PROPOSE action that implements a Step 2.5 item. The same bracket id MUST also appear in the `📋 Linked reviewer items` header block.
- **Style**: width is FLEXIBLE. Don't break long lines; let them run. Goal: a drafted sentence reads on one line, never chopped. No em-dashes (Hard Rule 3); use `·` as the separator in the heading.

#### Step 4c. 💭 LOGIC DISCUSSION block (conditional, at bottom)

**Add only when** the author rejects sentence-level edits and asks for an
ARC-level rethink. Triggers:
- author says "rethink the story", "重新想", "不要 propose 怎么改, 先想一想", "check this again"
- author flags a transition is incoherent at the logic level (not just bad sentence)
- author proposes a different way to slice the section
- author asks for options before any rewrite

Position: at the END of the .tex file (after the last paragraph's content,
before `\end{document}` if it's a standalone file). Format:

```
%%@ ═══════════════════════════════════════════════════════════════════════════════
%%@   💭 LOGIC DISCUSSION  v<tag> · CC reply to <author> "<trigger phrase>"
%%@ ═══════════════════════════════════════════════════════════════════════════════
%%@
%%@   Status: <one-line — which JL asks were APPLIED / MID-ITERATION / DEFERRED>
%%@
%%@   Context: <short paragraph — what the author flagged, what they asked>
%%@
%%@   Author asks (verbatim):
%%@     {JL} v<tag>: <verbatim Chinese or English, no translation/compression>
%%@       CC v<tag>: <one-line reply per Hard Rule 1>
%%@     {JL} v<tag>: <verbatim>
%%@       CC v<tag>: <one-line reply>
%%@
%%@   Framing decisions needing author call (omit if none open):
%%@     (a) <short description>
%%@     (b) <short description>
%%@     (c) <short description>
%%@     Recommendation: <one-line>
```

Optional add-ons (intro-or-thesis-restructure only):

```
%%@   Gaps (author's framing):
%%@     TRAIT gap: <plain-language description with verbatim quote>
%%@     LLM gap: <description>
%%@     METHOD gap: <description>
%%@
%%@   Joint RQ (LOCK structure):
%%@     >> PRIMARY (empirical): ...
%%@     >> SUPPORTING (methodological prerequisite): ...
%%@
%%@   Proposed ARC (N paragraphs):
%%@     P1: <role label> — <one-line>
%%@     P2: <role label> — <one-line>
%%@     ...
%%@
%%@   Key structural moves vs current draft:
%%@     1. <move>
%%@     2. <move>
```

**When to STOP**: after the LOGIC DISCUSSION block is written, propose
nothing further until the author resolves the open framing decisions.
Once resolved, **rewrite the per-paragraph blocks (Step 4b) to match the
new ARC**, preserving every author comment with appropriate `(done)` /
`(old)` tags. The LOGIC DISCUSSION block stays in the file as the audit
trail. Do not delete it after the box rewrite.

---

Emoji table (used in ARC, Roles, paragraph heading, and inside NOW + PROPOSE lines)
-----------------------------------------------------------------------------------

```
Core sentence/paragraph roles:
  🎯 motivation / setup        📊 method-and-result / report
  📐 statistical test          💡 interpretation / claim
  🔮 future-work directive     ⚠️ caveat / disclaimer
  🔗 hinge / transition         🧭 mechanism
  🔁 robustness / stability    📌 topic sentence / anchor
  💬 interpret (longer-form)   📖 opener                ✅ closer

Domain-flavor emoji (paragraph-level only, when paragraph identity is dominantly about that domain):
  🏥 specialty / context       ♀♂ gender / subgroup
  🔝 high tier                 🔻 low tier             🩺 primary care
```

Same emoji must be used consistently for the same logical role across
the ARC line, the matching Roles entry, the per-paragraph heading, and
any NOW/PROPOSE line whose sentence carries that role. The reader scans
by column: if `🔮` appears in the ARC for P5, it appears on P5's Roles
line, P5's block heading, and any P5.S<n> NOW/PROPOSE line that is a
future-work directive. **Exception**: a paragraph can carry a
domain-flavor emoji at the paragraph level while its inner sentences use
core role-emoji. This keeps the ARC scannable as a domain narrative
while sentence-level emoji track function.

---

Approval gates
==============

The skill enforces **two human-in-the-loop gates** so the author always
controls when prose changes happen and when the scaffolding leaves the
file.

### Gate G1 — Review the plan before any prose edits

**Triggered**: at the end of Step 4 (default SECTION route), after all
plan blocks have been embedded into the .tex.

**Skill behavior**: STOP. Do NOT propose prose edits, do NOT call
`/paper-revise`, do NOT touch any `%% ---- PN.SN ----` content. End the
turn with a fixed end-of-turn message:

```
✅ Plan embedded in <path>.tex
   - Step 4a header block (ARC + Roles + Linked reviewer items?)
   - Step 4b × <N> per-paragraph blocks
   - Step 4c LOGIC DISCUSSION block? (only if author asked for ARC rethink)

🚦 Gate G1 — please review the embedded plan in the .tex.

   Quickest review path:
     1. Open <path>.tex
     2. Skim the `%%@ ARC` block at the top
     3. For each paragraph, read the `%%@ 📌 NOW` + `%%@ 🔧 PROPOSE` block

   When you're ready, choose one:
     (a) "approve" / "go ahead"        -> I'll start applying proposed edits
     (b) "rework P<n>"                  -> I'll revise P<n>'s block only
     (c) "rethink the story"           -> I'll add a 💭 LOGIC DISCUSSION block (Step 4c)
     (d) "abort" / "drop the plan"     -> I'll prompt cleanup (Gate G2) without applying anything
```

End the turn. Do not auto-continue. The author's next message is the
gate decision.

If the author says (a), proceed to apply edits one sentence at a time
(respecting the user memory `feedback_one_sentence_at_a_time`) — or
hand off to `/paper-revise` if the author prefers the broader workflow.

After every PROPOSE action transitions to `[APPLIED]` (i.e., the apply
round is complete), automatically fire Gate Q before offering Gate G2.

### Gate Q — Auto quality check after apply

**Triggered**:
1. Automatically, when every PROPOSE action in every per-paragraph block
   has been tagged `(applied)` or the block heading has collapsed to
   `[APPLIED v<tag>]`.
2. On demand, via `/paper-weaving check <path>.tex` (e.g., to sanity-check
   the section before submission even if no round of edits just finished).

**Skill behavior** — three substeps, run in this order:

#### Substep Q1. Inline cheap scan (no Skill() calls)

Grep the .tex prose region (everything not on a `%%` line) for cheap
quality regressions. These are O(file-size) scans, run inline by
paper-weaving without dispatching to a sibling skill:

| Check | Regex / heuristic | Fail condition |
|---|---|---|
| Em-dash (Hard Rule 3) | `[—–]` | any match |
| Sentence-length (Hard Rule 5) | tokenize each sentence | ≥35 words |
| Paragraph ceiling (Hard Rule 5) | count `%% ---- P<N>.S<n> ----` per P | ≥7 sentences in any P |
| Marker monotonicity (Hard Rule 2) | walk `%% ---- PN.SN ----` markers | non-monotone N or S within a paragraph |
| Bare `%%` comment author signature drift | `^%%[^@-]` lines without `Comments:` `{INITIALS}` or `----` | unknown bare-`%%` line (alerts author to manual edits) |
| AI-voice anti-pattern shortlist (Hard Rule 4 sample) | `\b(primarily,|specifically,|increasingly,? )\b`, `\b(agree with|claim that|suggest that)\b human|panel`, `\\emph\{[A-Z]` (italics-on-noun) | any match |

Each matched item gets reported as `🟡 inline:<check>` with `PN.SN` and
the offending substring. **Inline checks never block apply** — they
report; the author decides whether to fix before Gate G2.

#### Substep Q2. Skill fan-out (configurable)

Call sibling check skills in parallel via `Skill()`. Default check list:

```
Skill("paper-check-numeric",   args="<path>.tex")
Skill("paper-check-reference", args="<path>.tex")
```

Optional checks (run only if explicitly enabled in `paper-weaving.yml`
or requested by the author):

```
Skill("paper-claim-audit",     args="<path>.tex")   # heavy: claims-vs-evidence
Skill("paper-manual-review-values", args="<path>.tex")  # heavy: every number from raw files
Skill("citation-verifier",     args="<path>.tex")   # heavier than -reference
```

The fan-out runs in a single message so the checks execute concurrently.
Each check skill is expected to return a structured report (PASS / FAIL +
issue list). paper-weaving captures the structured tail of each report.

#### Substep Q3. Aggregate + present

Combine Q1 inline findings + Q2 skill reports into one unified
PASS/FAIL summary. Format:

```
🎯 Gate Q — Quality check after apply

Inline scan (Substep Q1):
  ✅ em-dash               (0 matches)
  🟡 sentence-length       (P3.S2 = 41w; P5.S4 = 38w)
  ✅ paragraph ceiling     (max 5 sentences, P4)
  ✅ marker monotonicity   (clean)
  🟡 AI-voice anti-pattern (P2.S3: "specifically,"; P5.S1: "\emph{Significance}")

Skill checks (Substep Q2):
  paper-check-numeric:    ✅ PASS  (12/12 numbers re-derived; report: <link>)
  paper-check-reference:  🟡 FAIL  (2 unverified refs: doe2024foo, smith2025bar)

Overall: 🟡 ATTENTION — 3 inline issues + 2 unverified refs.

Choose one:
  (a) "fix Q issues first"    -> I'll surface each issue one at a time for review
  (b) "acknowledge and continue" -> I'll proceed to Gate G2 (cleanup prompt)
  (c) "re-run Q after I fix"  -> I'll wait until you say "re-run Q"
```

If every Q check is ✅ PASS, the message collapses to:

```
🎯 Gate Q — All checks PASS. Proceeding to Gate G2.
```

…and Gate G2 fires immediately in the same turn.

#### Configuration: `paper-weaving.yml`

Optional per-paper config file at the paper folder root (sibling of
`0-sections/`). If absent, defaults above apply. Schema:

```yaml
paper-weaving:
  gate-q:
    # Inline scans (Substep Q1) — list of checks to enable; omit to enable all
    inline:
      - em-dash
      - sentence-length
      - paragraph-ceiling
      - marker-monotonicity
      - ai-voice
    # Skill fan-out (Substep Q2) — list of sibling skills to call
    skills:
      - paper-check-numeric
      - paper-check-reference
      # - paper-claim-audit          # uncomment for pre-submission rounds
      # - paper-manual-review-values
    # Skip Gate Q entirely on micro-rounds (one-sentence apply passes)
    skip-on-micro-round: true
```

If the config file is malformed, paper-weaving prints a one-line warning
and falls back to defaults.

#### When Gate Q is suppressed

Two cases skip Gate Q:

1. **Micro-round** — the apply round touched a single sentence, AND the
   config has `skip-on-micro-round: true`. Reason: running paper-check-*
   for a one-sentence edit is wasteful; the next non-trivial round will
   pick up any regression.
2. **Author override** — author typed `skip Q` during Gate G1 approval
   (e.g., `approve, skip Q`). Recorded for the current apply round only;
   the next round runs Gate Q normally.

### Gate G2 — Cleanup prompt after all edits applied

**Triggered**: invoked via `/paper-weaving cleanup <path>.tex`, OR
automatically immediately after Gate Q presents its summary (whether
PASS or 🟡 ATTENTION — the author still owns the cleanup call). Gate G2
NEVER fires directly out of the apply phase; Gate Q always runs first.

**Skill behavior**: do NOT auto-delete any `%%@` lines. The author owns
the cleanup decision. Instead, print this prompt to chat (verbatim, with
the right path substituted):

```
✅ All proposed edits in <path>.tex are now tagged APPLIED.

🧹 Gate G2 — Cleanup is your call.

   The plan blocks (every line starting with `%%@`) are scaffolding.
   They compile silently (LaTeX strips them), so leaving them in is
   harmless. But for a clean submission .tex you probably want them gone.

   I will NOT delete them automatically — past sessions have shown that
   the author sometimes wants the plan blocks retained for the NEXT
   round's audit trail, or wants to migrate some content into a sibling
   `0-sections/<file>_audit.md` before deleting.

   When you're ready, one of:

   (1) Delete in place yourself (recommended, ~3 seconds):
       In VS Code: Cmd+F → enable regex → search `^%%@.*\n?` → Replace All
       In terminal:
           sed -i.bak '/^%%@/d' <path>.tex
           (review <path>.tex.bak first; delete .bak when satisfied)

   (2) Ask me to delete them — say "/paper-weaving cleanup <path>.tex confirm-delete"
       I will then run the sed command above and show you the diff.

   (3) Keep them — say "keep plan blocks" and I won't ask again this session.

   Either way, the author `%% Comments: {INITIALS}` lines and the
   `%% ---- PN.SN ----` markers stay untouched. Only `%%@` lines (the
   skill's scaffolding) are in scope.
```

End the turn. If the author replies with option (2) (`confirm-delete`),
THEN the skill is allowed to run the sed command (or equivalent
Edit/Write operations) — but only after the author has explicitly typed
`confirm-delete`. Treat the deletion as a destructive operation: print
the diff (block count removed, line count removed) after applying so
the author can verify.

If the author replies "keep plan blocks", record that decision in the
session and skip Gate G2 prompts on subsequent apply passes against
the same file.

---

Lifecycle: applying edits
--------------------------

When the author accepts proposed actions and they get applied to the
prose, update the corresponding per-paragraph block in place:

- **Block fully consumed** (all PROPOSE actions applied): collapse to a
  single retained line preserving the heading, append the status tag:
  ```
  %%@ <emoji> P<N> · <ROLE LABEL>          [APPLIED v0519: rewrote S2-S3, dropped S4]
  ```
  Drop the `📌 NOW` / `🔧 PROPOSE` body entirely.
- **Block partially applied**: keep the block, but mark each applied
  PROPOSE line with `(applied)` at the end, and add a `[MID-ITERATION v<tag>]`
  status tag to the heading.
- **Block entirely rejected**: keep the block intact but change status
  tag to `[DEFERRED v<tag>]`.

When every per-paragraph block carries `[APPLIED v<tag>]` (collapsed
form) or `[DEFERRED v<tag>]`, fire **Gate Q** automatically (which then
hands off to Gate G2 once its summary is presented).

Author `%% Comments: {INITIALS}` lines NEVER get rewritten by this skill
(Hard Rule 1).

When a new revision round starts (v<old> → v<new>), the prior round's
collapsed `[APPLIED v<old>]` lines stay as audit trail until Gate G2 is
explicitly resolved. The new round adds fresh `📌 NOW / 🔧 PROPOSE` body
below the collapsed line, or overwrites it entirely (author chooses).

---

Author-comment preservation across the embedded plan
-----------------------------------------------------

Because the plan lives in the same file as the author's `%% Comments:`
lines, Hard Rule 1 (preserve verbatim) is more important, not less.
Rules:

- Author comments use the prefix `%% Comments: {INITIALS} v<tag>:`. The
  `{INITIALS}` signature is what distinguishes them from
  skill-generated `%%@` plan blocks.
- When marking a resolved author comment, append a status tag to the END
  of the author's verbatim line, on the SAME line:
  - `(done — <one-phrase summary>)` — original concern still resolved by current draft
  - `(old — <one-phrase summary of why superseded>)` — later structural change makes the comment irrelevant; preserved as audit trail
- Do NOT write a separate multi-line resolution block.
- When replying to an author comment with a `CC v<tag>:` tag inside the
  file, the reply MUST fit on ONE line. No multi-line bullets, no
  indented sub-points. Compress recommendation + key reason into one
  sentence. If the answer needs more, put the long version in chat and
  leave a one-line pointer in the file.

---

Step 5. STOP at Gate G1
------------------------

After embedding the plan blocks, end the turn with the fixed Gate G1
message (see "Approval gates" above). Do NOT touch the existing prose,
the `%% ---- PN.SN ----` markers, or the `%% Comments: {INITIALS}`
lines. The diagnosis in chat and the embedded `%%@` plan blocks are
the entire deliverable of this turn.

---

Hard rules (do not violate)
============================

1. **Preserve every author inline comment verbatim.** `%% Comments: {INITIALS} v<tag>:` lines stay exactly as written, in both .tex AND any prior plan block that quoted them. When the author has annotated a prior round's plan blocks and the skill is asked to regenerate (e.g. switching to a different ARC option), **do not start clean**. Read the prior plan blocks first, extract every inline annotation, and re-insert each one at the same logical location in the new blocks. No translation, no compression, no silent drop. If a note is structurally homeless (e.g. attached to a paragraph that's been merged away), park it in the 💭 LOGIC DISCUSSION block (Step 4c) under a `Preserved orphan comments` subsection rather than deleting it.

   **CC reply length**: one line, per the "Author-comment preservation" section above.

2. **PN.SN markers are file-local.** Never use cross-file continuous numbering. P1 restarts at the top of every section file.

3. **No em-dashes anywhere.** In diagnosis prose, in embedded plan blocks, in any suggested rewrites: use comma, colon, or sentence break instead.

4. **No AI-flavored prose.** Short plain academic sentences only. Anti-patterns to scrub:
   - **Parenthetical adverbs** comma-fenced mid-sentence ("We ask, *primarily,* ..."). Drop.
   - **Apposition padding** ("we use LLMs *as the measurement instrument* and ask..."). Drop.
   - **Callback constructions** ("The same X *that drives* Y *also* enables Z."). Plain.
   - **Anthropomorphic comparison verbs** (extractions "*agree with*", "*claim*", "*suggest*"). Use factual verbs ("are consistent with", "match", "track").
   - **Comma-tacked disclaimer appendages**. Give load-bearing disclaimers their own clause.
   - **Double-marked adverbs** ("*Recently*, patients *increasingly* consult..."). Pick one.
   - **Noun stacks (4+ chained nouns)**. Break the chain with a verb.
   - **Buzzword stacks** ("two-agent large language model pipeline" → "two LLM agents").
   - **Inline (i)/(ii)/(iii)** packing inside one sentence. Use a real list.
   - **Italics-on-key-nouns** (`\emph{Score}`). Use plain capitalization or none.
   - **Parenthetical name-explosions** (long trait rosters mid-sentence). Pull to a table.

   **Read-aloud test:** if a tired academic reviewer would not naturally string the clauses this way out loud, recompose.

5. **Compress, don't split (refined).** Sentence-length budget:
   - Target: 20-25 words per academic sentence.
   - 30 words: trigger compression review.
   - 35+ words: compress hard. If load-bearing content still remains AND there is a natural break point, **split into two complete sentences** (never fragments).

   **When a split happens in a marker-indexed `.tex` file**, each new sentence MUST get its own `PN.SN` marker, and downstream sentences in the same paragraph cascade-renumber. Two sentences sharing one marker violates the file-local monotonicity rule (Hard Rule 2). Example: if old `P5.S2` is split into two sentences and old `P5.S3` exists, the new ordering is new `P5.S2`, new `P5.S3` (split-tail), new `P5.S4` (was old `S3`). Mark the new marker with `[NEW v<tag>: split from old P5.S2 tail]` and the renumbered one with `[was P5.S3 in v<old>; renumbered after split]`.

   Paragraph ceiling: ≤6 sentences per paragraph.

6. **No sidecar `.txt` files.** Plan content lives in the `.tex` as `%%@` comments. If a prior round of this skill (or its predecessor `paper-revise-section`) produced a `.txt` sidecar, migrate its content into the `.tex` on the first run of the new format and PROMPT the author to delete the `.txt` (do not delete silently).

7. **No `.md` report files** as a side effect. The diagnosis table lives in the chat reply only. The .tex is the only file written by this skill.

8. **`%%@` sentinel for ALL plan lines.** Every skill-generated comment line opens with `%%@`. Bare `%%` is reserved for author comments and the `%% ---- PN.SN ----` markers. This makes Gate G2 cleanup a single regex.

9. **Never auto-delete `%%@` blocks.** Gate G2 prompts the author; the author types `confirm-delete` if they want the skill to scrub. Never delete on assumption.

10. **Never apply prose edits without Gate G1 approval.** Step 4 ends with STOP. The author's "approve" / "go ahead" message is the only valid entry to the apply phase.

11. **Gate Q always runs after apply, before Gate G2.** Exceptions: micro-round (single-sentence apply) when `skip-on-micro-round: true`, or explicit author override (`approve, skip Q`). Gate Q inline scans (Substep Q1) never block — they report; the author decides what to fix. Gate Q skill fan-out (Substep Q2) is parallel `Skill()` calls; do NOT sequentialize them.

12. **Immerse before acting.** Spend real time inside the .tex before diagnosing or proposing. Read each paragraph to the end, follow every author `%% Comments: {INITIALS}` line back to the sentence it refers to, and reread upstream paragraphs the current one depends on. A shallow read produces shallow diagnoses: missed cross-paragraph dependencies, mis-classified paragraph roles, and PROPOSE actions that contradict constraints buried elsewhere in the file. The text is the source of truth; the time spent inside it is the work, not the setup.

---

Multi-subsection workflow (pilot + parallel)
============================================

When a paper section is split into multiple `.tex` subsection files
(e.g. Results split into `02-01_*.tex` through `02-07_*.tex`), running
this skill on every subsection benefits from a **pilot + parallel**
pattern rather than 7 sequential rounds:

1. **Pilot pass (main agent, one subsection).** Pick one subsection the author knows well, or the most structurally representative one. Run the skill on it in the main conversation; embed the plan blocks. Hit Gate G1, let the author review + iterate on style choices until they approve. This `.tex` becomes the **structural benchmark** for the rest.

2. **Parallel pass (N sub-agents, remaining N-1 subsections).** Spawn one sub-agent per remaining subsection, all in a single message so they run concurrently. Each sub-agent's prompt MUST include:
   - the absolute path of the target `.tex` file
   - the absolute path of the pilot `.tex` (with embedded plan) as a structural reference ("read this FIRST to absorb the format")
   - paper-level context: shared ARC framing, RQ, lexical preferences (e.g. "consistent with" not "agree with"), any cross-section role-label vocabulary established in the pilot
   - "STOP at Gate G1; do NOT apply prose edits"
   - "Report back under 300 words: severity counts, top issues, blocks inserted (4a + 4b × N ± 4c)"

3. **Triage + iterate (main agent).** Read each sub-agent report. Subsections marked all-🟢 are in late-polish state. Subsections with 🟡 / 🔴 return to the main conversation for sequential iteration. Sub-agents can hit Gate G1 (post the prompt) but cannot iterate with the author past G1; any structurally contested subsection needs the main agent for G1 resolution and the apply phase.

**Why this pattern works:** format consistency is ~95% guaranteed by SKILL.md + memory; per-subsection content quality is ~70-80% first-cut; the pilot's role is to lock the cross-section role-label vocabulary and icon style that SKILL.md does not fully specify.

**When NOT to use:**
- Single-section files (just run the skill directly).
- Sections with fewer than ~4 subsections (sequential is simpler).
- Sections where each subsection has fundamentally different ARC needs (the pilot may not transfer cleanly).

---

When to invoke this skill vs. neighbours
========================================

| If the author wants ... | Use |
|---|---|
| diagnose one section + plan the revision, embedded in .tex | **paper-weaving** (this, default route) |
| rework a paragraph, iterate sentences inside it | `Skill(paper-revise-paragraph)` via paper-weaving |
| rewrite a single sentence | `Skill(paper-revise-sentence)` via paper-weaving |
| verify every quantitative claim against raw results | `Skill(paper-check-numeric)` via paper-weaving |
| verify every citation against bib + venue metadata | `Skill(paper-check-reference)` via paper-weaving |
| run all quality checks on demand (without an apply round) | `/paper-weaving check <path>.tex` (Gate Q) |
| clean up the embedded plan blocks before submission | `/paper-weaving cleanup <path>.tex` (Gate G2) |
| interactive multi-pass revision with sentence-level annotations + apply | `/paper-revise` (sibling, not a child) |
| draft a section from an outline | `/paper-write` |
| critique paper-wide structure, not one section | `/paper-structure-planning` |
| build a TikZ figure for the published paper | `/figure-spec` or `/diagram-drawio` |

---

Companion reference: `ref/write-principles.md`
===============================================

`ref/write-principles.md` is a condensed paper-revision rule sheet
distilled from the npjDM2025 v0516-v0519 sessions. It covers
comment-preservation conventions (Section A), anti-AI-voice prose
don't-lists (B), structural rules (C), content rules (D), verification
rules (E), the **compression-recipe catalog** F1-F7 (the operational
heart of "compress not split"), workflow rules (G), the post-iteration
code-claim audit patterns H1-H3, and a pre-save checklist (I). Skim it
before applying edits to a section that will be reviewed by external
reviewers. The skill's Hard Rules (above) and `ref/write-principles.md`
overlap intentionally — both reference the same rules from different
cuts. When they conflict, the section-specific Hard Rule wins.

---

Migration from `paper-revise-section` (legacy `.txt` sidecar format)
=====================================================================

If the workspace still has `.txt` plan files from the prior format
(e.g. `1-feedback/v0516/01_introduction_logic.txt`), do the following
on the first run of `paper-weaving` against the matching `.tex`:

1. Read the legacy `.txt`. Extract:
   - the ARC + Roles header
   - each per-paragraph block (📌 NOW + 🔧 PROPOSE)
   - any 💭 LOGIC DISCUSSION section
   - every author inline annotation embedded in the .txt
2. Embed each piece in the .tex per Step 4a / 4b / 4c, using the
   `%%@` sentinel on every line.
3. Remove the legacy "Logic + proposed edits diagram:" stub from the top
   of the .tex (the 5-line pointer block that used to point at the .txt).
4. Hit Gate G1 as usual. Once G1 + apply + G2 are resolved, PROMPT the
   author to also delete the legacy `.txt` (do not delete silently).
