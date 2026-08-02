# Delivery Value: a number that still knows which run produced it

state: ✅ RULED
owner: JL
method: carry task-produced quantitative evidence into exact sentence-level values with provenance

## Opening

How does a number enter the paper without losing the run that produced it?

A value is a quantity stated in a sentence, such as a coefficient or a sample size. A run is the one execution of a task that computed it. Binding means the sentence points at that run, not at a file that happens to contain the same digits.

**Where this page sits**: QB2 Work commissions the computation, and QB12b specifies the value marker and its evidence card.
QB5 Display takes the numbers that are better shown than stated.
This page owns what makes a stated number trustworthy at all.

**Why the binding is to a run and not to a file**: a file with the right digits proves nothing about where they came from.
Re-run the task with one changed covariate and the file is overwritten while the sentence stays put, and now the paper asserts a number nothing produced.
A value has the shortest path to a retraction of any evidence a paper carries, because a wrong coefficient is a false claim rather than a formatting error.

**What is not yet enforced**: the projection checks currently compare markers and counts.
They do not yet compare value bindings, so today the rule is stated and only partly machine-checked.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Say "run", never "result file"**: the whole rule is the difference between those two, so the word choice is the argument.
A sentence that says a value comes from a file has already conceded the point.

**Name what must match, as a list of five**: value, definition, sample, specification, run.
A vaguer phrase like "matches the analysis" cannot be checked, and the gate is exactly this list.

**This page DESIGNS; the paper board SHOWS**: `### 2` states what a paper must carry for this concern, not what one paper happens to have today.
Where the MISQ paper differs, say so as a gap with an owner, never as the definition.

## Diagram

**The value path**: what a number carries with it, and what it must match at the end.

```text
  🧮 task RUN                     ← the one execution that computed it
        ▼
  📥 probe answer
        ▼
  🔢 value attachment             ← binds to the RUN, never to a file
        ▼
  ✍️ S-page sentence
        ▼
  📄 format projection

  🚪 the gate checks FIVE things agree with the sentence:
     value · definition · sample · specification · run
  💥 a silently re-run coefficient is a false claim, not a typo
```

## Content

### 1 · The delivery contract

**What Value owes**: a computed number in, a checkable claim out.

```text
  📥 CONSUMES                📤 PROJECTS TO           🚪 GATE
  accepted task         ━━▶  inline values      ━━▶  value · definition ·
  outputs                    the evidence card       sample · specification ·
  🚫 never a number          exposing provenance     run  ALL match the
     copied from an                                  sentence
     unbound file
```

📜 Establishes what a number must carry before a sentence may state it.

| Field | Contract |
|---|---|
| Lifecycle | After Literature and before Display. |
| Authority | The task result plus its bound sentence attachment. |
| Projects to | Inline values and the evidence card that exposes their provenance. |
| Skills | Probe, value checks, QB12b adapter behavior. |
| Consumes | Accepted task outputs; never a number copied from an unbound file. |
| Gate | Value, definition, sample, specification, and run all match the sentence. |
| Open gaps | Projection checks need to compare value bindings, not counts alone. |

#### 1.1 · Five things must agree, not one
(the digits matching is the weakest of the five, and the easiest to mistake for the whole check)
A number can be transcribed perfectly and still be wrong, because it answers a different specification or a different sample than the sentence describes.
That is why the gate names all five: the four besides the digits are where a re-run actually diverges.

### 2 · What we want on the paper board

**The group we are designing**: one Q page, no S page, and a rule that binds every sentence stating a number.

```text
  🎯 WHAT WE WANT a paper to carry for this concern
  ### Delivery · Value
        📄 QV0-value-delivery.md    a Q page: the binding rule for THIS paper
        🚫 no S page                nothing is authored per-unit here

  ⚡ this concern owns NO STAGE and produces NO manuscript text
  🔑 it binds work done elsewhere: a number stated in S-Main-6 must
     resolve to the task run that computed it
  📍 the value MARKER lives in the citing sentence, on whatever page
     states the number ── QB12b specifies it
```

🎯 Establishes what a paper board must show for this concern, and why it is the one concern with no S page at all.

#### 2.1 · A concern with no S page is still a real concern
(it owns a rule, and a rule needs a page even when it produces no prose)
`index.yml` declares no `value` stage, and no manuscript section belongs to this concern.
Every number a paper states is written on some other page, in Results or Methods or a display caption.
What this concern owns is the binding: that number resolves to a run, and `QV0-value-delivery.md` is where a paper records how its own values are bound.

#### 2.2 · The Q page is per-paper, not per-unit
(one page for the whole paper, because the rule does not vary by section)
A paper does not need a value page per section, because the five things that must agree are the same in every section.
So the group holds one Q page and grows no further, which is why it looks thin next to Display's fourteen.
Thin is correct here: the work this concern causes happens inside other pages' sentences.

#### 2.3 · Where the MISQ paper stands against this
(the page exists and the enforcement does not)
`QV0-value-delivery.md` is on the MISQ board under `Delivery · Value`, so the group is built as designed.
What is missing is machine enforcement: the projection check compares markers and counts and does not yet compare value bindings, which is QB9's deferred G3 extension.

## Aims

### A1 · 📜 The delivery contract
- A1.1 · Every stated value binds to a producing run rather than to a file.
  **Done when:** every inline value on a paper resolves to a run id through its evidence card, and a value with only a file behind it renders as visibly owed.
- A1.2 · The detailed value contract stays on QB12b rather than being restated here.
  **Done when:** this page names no marker syntax, and QB12b is the only page specifying the value chip and its bracket.

### A2 · 🎯 What we want on the paper board
- A2.1 · A paper board shows this concern as one group holding one Q page.
  **Done when:** `Delivery · Value` lists a value-delivery Q page, and no S page is created for a concern that authors no prose.

### P · 🏁 Page-level
- P1 · The binding is machine-checked, not only stated.
  **Done when:** the projection check compares value bindings and fails a candidate whose stated value no longer matches its bound run.

## States

### A1 · 📜 The delivery contract
- ✅ A1.1 · Ruled and carried in the Law: a value binds to a producing run, not to a file containing the same digits.
- ✅ A1.2 · Held. The Scope paragraph hands the marker to QB12b, and no marker syntax appears on this page.

### A2 · 🎯 What we want on the paper board
- ✅ A2.1 · Built as designed on the MISQ paper: `Delivery · Value` holds `QV0-value-delivery.md` and no S page.

### P · 🏁 Page-level
- ❄️ P1 · Held, pending QB9 A2.2. The rule is ruled and stated; enforcing it is the G3 extension the 260730 trial deferred, which QB9 owns, so P1 thaws when that check ships.

## Files

- `QB12b-sentence-value.md` · the value marker, its bracket, and the evidence card
- `QB9-build.md` · where the G3 extension that would enforce this has to land

## Law

A manuscript value binds to a producing run, not merely to a file containing the same digits.

## Glossary

- **Value binding**: the sentence-level attachment that identifies a quantitative claim's producing result.
- **Run**: one execution of a task, identified so that a later reader can tell whether the number still comes from it.

## Log

260802 · `### 2 · What we want on the paper board` added. This is the one Delivery concern with NO S page: `index.yml` declares no `value` stage and no manuscript section belongs to it, so the group holds a single Q page and the work it causes happens inside other pages' sentences. Thin is the correct shape here, and the page now says so rather than leaving a reader to wonder what is missing.
260802 · Migrated to the QB4 page contract: Writing Style added, Content numbered with a face figure and caption, Aims regrouped as A1/P with `Done when`, States mirrored per Aim.
260730 · Project trial recorded the structured-value comparison as a later G3 extension.
