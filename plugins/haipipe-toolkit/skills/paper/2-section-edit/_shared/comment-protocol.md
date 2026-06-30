# 4-edit / shared — the comment protocol

**The load-bearing rule of `4-edit`: in Round 1 a skill never changes the prose.**
It reads, diagnoses, and leaves concise inline comments. The human reviews each
comment and replies in place. Only Round 2 applies changes, and only to comments
the human accepted.

This protocol is shared by every 4-edit sub-skill and by the `haipipe-paper-edit`
orchestrator. It is what makes safe parallel fan-out possible: a comment-only
pass cannot corrupt the draft, so many reviewers can run at once.

## The two marks

A thread is built from two marks. **Which mark** you use is your role in the
thread (raising a finding vs. responding); **who** you are is the *actor id* inside
the `{…}` (see [Actor ids](#actor-ids)). Any actor — AI tool or person — can write
either mark; by convention a reviewing tool raises findings and the author replies.

### Finding (the comment)

```
%% {<actor>-<topic>-vMMDD}: <one-line finding> | <one-line suggestion>
```

- `<actor>` — who wrote it; any short id. A reviewing AI tool stamps its own tag
  and appends the topic for fan-out traceability: `CC-content`, `CC-values`,
  `GPT-cite`, …. Drop the `-<topic>` for a single-topic pass.
- `vMMDD` — the pass date (e.g. `v0531`). New round → new date.
- `<finding> | <suggestion>` — what's wrong, then what to do, each one line.
  Keep it tight; this is a margin note, not an essay.

### Reply (same line, after the separator)

The responder appends to the **same line**, after `========>`:

```
%% {CC-content-v0531}: claim stated as causal; data is correlational. | Soften to "associated with". ========> {JL v0531}: accept
```

- `========>` — the reply separator (literal, eight `=` then `>`).
- `{<actor> vMMDD}` — responder id + reply date.
- Reply verb vocabulary: `accept` · `reject` · `modify: <how>` · `discuss: <q>` · `done`.

## Actor ids

The `{…}` token names **who** authored that line. Keep it short. One flat
namespace — use whatever ids the project recognizes:

| Kind | Examples | Note |
|------|----------|------|
| AI tool / agent | `CC` (Claude Code), `GPT`, `GEM` (Gemini), `CDX` (Codex) | reviewing tools; append `-<topic>` on findings |
| Person | `JL`, `RA`, `GG` (initials) | authors / coauthors |
| Role | `R1`, `R2`, `AC`, `ED` | numbered reviewers, area chair, editor |

- **The human actor id is asked, never assumed.** At the start of a cycle the
  skill **asks the user for their initials** (and the pass date `vMMDD`). Every
  reply slot, example, and digest then uses what the user gave. Never default to
  `JL` or any other initials — `JL`/`RA`/`GG` in this doc are illustrative only.
- A tool stamps **its own** id — Claude Code writes `CC`, another model writes its
  own tag. The agents in `agents/` run under Claude Code, so they write `CC`.
- Findings and replies share the same actor-id grammar; the **mark** (`%%` vs
  `========>`), not the actor, says whether it is a finding or a reply.
- A thread can be multi-party — an AI finding, a human reply, then another tool's
  follow-up on a new dated line:

```latex
%% {CC-content-v0531}: claim reads causal; data is correlational. | hedge. ========> {JL v0531}: modify: keep, add the n
%% {GPT-content-v0602}: still reads causal after the edit. | use "associated with". ========> {RA v0602}: accept
```

## Anchoring a comment (without mutating text)

A comment sits on its **own line, directly below the text it refers to** — never
inside the sentence.

- **One-sentence-per-line files** (like the npjDM `0-sections/`): put the comment
  on the line immediately after the target sentence's line.
  ```latex
  Agreeableness showed the strongest positive correlation ($r = 0.62$).
  %% {CC-values-v0531}: 0.62 here vs 0.747 in the table. | Reconcile against 0-displays source. ========>
  ```
- **Wrapped multi-line paragraphs**: put the comment after the paragraph's last
  line and quote a short anchor with `@"…"` so the target is unambiguous.
  ```latex
  %% {CC-content-v0531}: @"we next examined" opener is throat-clearing. | Start with the finding. ========>
  ```
- Reference the paragraph banner `[id]` when the comment is about the whole
  paragraph: `%% {CC-content-v0531}: [trait-rating.setup] two points in one para. | Split. ========>`

Multiple comments on the same target stack as separate lines (one per finding).

> **Inserting the bare `========>` tail** at the end of each comment is optional
> but recommended — it gives the author a ready slot to type the reply into.

## Comment lifecycle

```
OPEN        %% {CC-…}: finding | suggestion ========>
   │  (author appends reply)
   ▼
REPLIED     %% {CC-…}: finding | suggestion ========> {<actor> …}: accept | reject | modify: … | discuss: …
   │  (Round 2 acts on the verb)
   ▼
RESOLVED    applied (accept/modify) or dismissed (reject); comment removed or logged
```

- A skill **never** acts on an `OPEN` comment — silence is not consent.
- Multi-round threads stack; each round adds a new dated line under the old one:
  ```latex
  %% {CC-content-v0531}: vague claim. | quantify. ========> {JL v0531}: modify: use the n
  %% {CC-content-v0602}: added n=83,230; still no effect size. | add R^2. ========>
  ```

## Round invariants

| Round | A skill MAY | A skill MUST NOT |
|-------|-------------|------------------|
| **1 — review** | insert `%% {CC-…}:` comment lines | change, reorder, add, or delete any body text, banner, label, or value |
| **2 — apply** | apply changes for `accept` / `modify` replies; resolve/strip those comments | touch any `OPEN` comment; apply a `reject`; invent content beyond the reply |

Round 1 output is a **diff that adds only comment lines** — if any non-comment
line changed, the pass violated the protocol.

## Heavy sentence surgery stays in-cycle

An earlier `paper-revise` skill handled deep sentence work with its own
`%% Comments: {INITIALS}` form. **`haipipe-paper-edit` is now the single edit system;
`paper-revise` is archived at `../../_archive/paper-revise`.** Sentence-level
apply, reindex, and clean are covered by the stage agents
(`paper-edit-improver`, `paper-edit-format-checker`, `paper-edit-cleaner`). For
very heavy logic restructuring, run extra annotate → reply → improve rounds at
finer granularity rather than switching tools.

## Quick checklist (Round 1 reviewer)

- [ ] Every finding is one `%% {CC-<topic>-vMMDD}:` line, `finding | suggestion`.
- [ ] Each comment anchored on its own line below its target (or `@"quote"`).
- [ ] A trailing `========>` slot left for the author.
- [ ] **Zero** body-text changes in the diff.
