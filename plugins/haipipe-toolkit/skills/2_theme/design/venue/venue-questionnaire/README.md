# Venue: Questionnaire

Questions a reader answers in their own words before a meeting with someone who will read the answers (a pre-visit
questionnaire, JL 261011: "it is not message"). Not a message: nobody sends it as text, the reader writes, and the
answers come back. Not a checklist: an item is a question with an answer box, never a tick.


## Constraints

- **Items:** 3-12 questions (a goal may narrow it, e.g. 5 to 8)
- **Item format:** one question, in plain words; it may open with one plain sentence of what was observed, then asks
- **Answer kind:** every question names how it is answered: `sentence`, `sentences`, `time`, `yes-no`,
  or `choice: <a> / <b> / <c>`
- **One ask per item:** a question that asks two things is two questions
- **Neutral:** no leading question, no advice, no cause given; the reader's account, not a test
- **Order:** the reader's day or the order the meeting will take them


## Design profile

```yaml
design_profile:
  evidence_bar: medium
  narrative: optional
  display: none
  section_edit: none
```


## Output grammar

`design.md`, word for word as the reader sees it; the answer line is drawn as the box, not as words:

```text
# <title>
<one optional line: why these questions, for whom they are>

1. <question>
   answer: sentence
2. <question>
   answer: time
3. <question>
   answer: choice: <a> / <b> / <c>

Done when: <what finished looks like>
```

The design workbench draws it as numbered questions, each with its answer box (servers/workbench-design
`design_views.questionnaire_card`); a missing answer line is drawn as a `sentence` box.


## Venue template

```yaml
template:
  - slot: title
    job: name the meeting the answers are for
    claim_source: the signed goal (board.md ## Goals) and the shared rules (design-goal.md)
  - slot: questions
    job: each question asks one thing the reader alone can tell, with its answer kind
    claim_source: the pinned goal · method version · inputs version (a finding it opens with comes through a signed Wisdom handoff in the fence)
  - slot: completion
    job: what finished looks like
    claim_source: venue convention, non-load-bearing
```


## Run guidance

### Inputs and generate ③

Each question maps through the Job's inputs/ fence (its manifest). A question that opens with an observed finding
names that finding's file and row as its `from`; a question with no finding behind it says so. If a question needs
a premise the fence lacks, return a named gap; do not ask from Design.

### verify ④ (another agent)

Each item: one question, one answer kind that fits it (a "when" question gets `time`, a "did you" question gets
`yes-no` or `sentence`), plain words, no advice, no cause, no leading word. A tick box, a to-do or two asks in one
item fails. If a preview is needed, render the exact questions inside the current Run's result/.

A passed verify ④, then t99's rank ⑤ and a person's release, put that exact questionnaire in delivery/.
