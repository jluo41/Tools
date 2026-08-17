---
name: haipipe-page-for-value
description: >-
  The VARIANT contract for a VALUE DISPLAY Page: an inward evidence page declaring `route: inward` and `display: companion`, whose questions face produced results. Each E division owns a QA-probe and a same-numbered Value Display companion, so a bound result becomes a managed candidate table or figure before Narrative decides whether it belongs in the paper. It adds the inward route's binding rule: number, run provenance, claim update, and candidate-display disposition. Trigger: value display, value table, analysis display, value topic, task route, value binding, run provenance, claim ledger, number evidence, /haipipe-page-for-value.
metadata:
  version: "0.5.0"
  last_updated: "2026-08-10"
  summary: "Value Display update (JL 260810): each probe has a same-numbered display companion, turning every bound result into a candidate table or figure with an explicit disposition before Narrative selects paper material."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-value · Value Display: what this project produces and can show

**LOAD TWO THINGS FIRST.** `haipipe-page` gives the frame; `haipipe-board/ref/topic-entry-contract.md` gives the E-division and QA-probe anatomy, which both evidence routes share and neither restates (`QB6 §4`, JL 260805). A QA-probe is a hidden source record named `<n>-<slug>.md`, never a board page (JL ruling B, 260806); it is the paper's stub that points at the QA-bank, the original. What this file adds is the inward route alone. Inward means the answer does not exist yet: the project must RUN something to make it, so every rule here is about chaining a produced number to the run that made it and to the claim that needs it.

**The kind this variant covers**: an evidence page whose questions face INWARD.

```
kind     resolved by                          closes when
─────────────────────────────────────────────────────────────────────
Value    the REQUIRED `route: inward`         every E<n> division's consumers
evidence line in the metadata head            are BOUND, DEFERRED, or
         (base, type resolution step ②)       WITHDRAWN, AND E0 is empty
```

"Value" names a DIRECTION, not a paper section: any family may ask for a number its own work must produce. The paper family's projection files these pages as `S-Value-<n>-<topic>` with `V<n>` probe folders; those letters are family vocabulary and stay in the paper projection. `route: inward` is the REQUIRED head key; it is what separates a page that must produce numbers from one that searches for papers.

## 🧬 The page organizes BY EXECUTOR

One `### E<n> · <the executor question>` Content division per Q-executor conversation; one division owns exactly one QA-probe. `### E0 · incoming` is the collect queue: a Q-consumer born on ANY page is COLLECTED into the owning topic's E0 first, and EVIDENCE later promotes it into a new E<n> and opens its QA-probe. The division's `#### consumers` block holds the collected Q-consumers, one row each: source page id, the stake in one line, then the A-consumer interpretation and the row state. Its `#### answer digest` is 2-3 lines from the A-executor; the full text stays in the QA-probe record. The anatomy is the core's; this route only says what its rows mean.

## 🗣 What a legal consumer row carries HERE

A Value Q-consumer carries a CLAIM DEPENDENCY: which claim rests on the number, and what specification would count as producing it.

```
✅  "H2 states high-dose prescribing rises with the trait score.
     It needs the LBP-cohort estimate, its CI, and the spec that made it."
🚫  "Get the regression results."                    no claim named · a chore
🚫  "Produce an estimate near 0.3."                  the answer ordered in advance
```

The stake stays on this page. The QA-probe's Q-executor asks for the computation in neutral terms, and the bank that runs it never learns which claim would be rescued (`page-workflows/haipipe-page-evidence` owns that wall).

## 📥 What a returned answer must BECOME: the value binding

An answer that stays in the QA-probe's `#### A-executor` is not yet a number the page may print. The consumer row's write-back is a typed record with three parts:

```
1  the value           with its uncertainty, exactly as the run reported it
2  the run provenance  which run, which specification, which QA file · BY PATH
3  the claim update    which claim consumed it, and what its status became:
                       supported · weakened · unresolved
```

🚫 A number whose provenance line is missing is a HOLE, not a result. It reads exactly like a real one, which is why the record, not the prose, is what CHECK audits.

## 🖼 Every probe gets a Value Display companion

After EVIDENCE returns, the result has two distinct products: a binding that says what the paper may claim, and a candidate display that makes the result inspectable.
The page declares `display: companion` in its metadata head.
Every nonzero E division therefore carries one `🖼 Display:` pointer to `display/<topic page>/<n>-<slug>.md`, sharing its QA-probe's number and stem.

```text
QA-probe        the neutral question, run, answer, and provenance
Value Display   the possible table or figure, its five-second takeaway,
                its narrative role, and its disposition
```

`not-displayable` is a valid disposition, never an omission.
A candidate becomes a formal Paper Display unit only when Narrative selects it and files a Display request.
The companion never owns a final caption, render acceptance, or manuscript placement; those remain `haipipe-page-for-display`'s job.
Use `haipipe-board/ref/topic-display-card.md` for its exact shape.

## 🚪 When the page closes

The core owns the terminal row states and the rule that the human gate reads the E divisions, not the QA-probes. The close rule on this route: every E<n> division's consumers are terminal AND `E0 · incoming` is empty. What BOUND takes here is a run you can walk to: the consumer row carries the number together with its run, specification, and QA file, each named by path. A number typed from memory binds nothing. Until the provenance paths exist the row stays open, however right the number looks in the prose.

**The template.** `template.md`, beside this file. ONE template serves every page of this type: two pages of it differ in what they say, never in what shape they are, so nothing has to be resolved before writing one. Copy it, fill every `<slot>`, and delete each RULE comment as you satisfy it.

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work** (`QB6` §7). A value page reads a producing run and hands on the parsed result its consumers read.

```text
 📥 INPUT   <stage>/QA-probe/<page name>/            one folder per PAGE NAME
              <n>-<slug>.md              the record: the question, and the ONE
                                         place its numbers are typed
              <n>-<slug>.data/source/    the producing run, or an extract script
 📤 OUTPUT  <n>-<slug>.data/*.csv        🤖 parsed FROM the record's own fence
              ▶ never retyped, and the parse is strict: a malformed row exits
                non-zero rather than writing a short table
            <stage>/display/<page name>/<n>-<slug>.md
                                          candidate Value Display companion
```

`route:` says where the answer came from. `local` means it was produced here and this record IS the original. `task` or `discovery` means the answer lives in that tree, a `- bank:` path names it, and this record holds only the binding and a digest. **The bank is never copied into the paper.**

An answered record that no consumer wants is a VISIBLE OPEN ROW, not a silent success: it keeps its division with an unbound consumer line until a consumer appears or the record is retired.

## 📂 Files

```
haipipe-page-for-value/
├── SKILL.md            this route dictionary
├── template.md         the page skeleton to copy, plus the QA-probe record shape
└── CHANGELOG.md        version history
```

Nothing executable ships here. The E-division, QA-probe, and Display companion shapes belong to `haipipe-board/ref/topic-entry-contract.md`, enforced by `haipipe-board/src/topic_entry_contract.py`; the wall a computation request crosses is owned by `page-workflows/haipipe-page-evidence`. A question about what is already published goes to `haipipe-page-for-literature`. The paper family projects this shape at `paper/haipipe-paper/probe/topic-entry-contract.md`.
