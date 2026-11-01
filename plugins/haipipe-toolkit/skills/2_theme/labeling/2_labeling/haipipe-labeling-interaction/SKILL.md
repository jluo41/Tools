---
name: haipipe-labeling-interaction
description: >-
  The labeling mode of /haipipe-interaction: a meaning loop's report as one collect Run that the person answers.
  The agent writes the loop's decision report (meaning_contracts), renders it into the form with nothing preselected,
  saves the person's paste, and reads it back as the decision record that Update applies (guideline mNN as a mind
  map, reference labels lNN, a flag per answer). For use case 2 it first draws the cards from an existing labeled
  corpus's raters' votes, with any expert key fenced out. Trigger: labeling interaction, meaning loop report,
  interaction report, decision report form, audit the existing labels, use case 2, /haipipe-labeling-interaction.
metadata:
  version: "0.1.0"
  last_updated: "2026-11-01"
---

# /haipipe-labeling-interaction · a meaning loop's report, answered

Only the 🧭 meaning Task asks the person (b15 s58-D03). Each loop asks once: one collect Run,
`runs/rNN_collect_report_mNN/`, holds the report's cards and, once answered, the person's decision record. Update
reads it, writes the next guideline and labels, and flags each answer applied (b15 s58-D08).

```text
draw (use case 2) ─▶ report.json ─▶ question_collection.md ─▶ form ─▶ 🙋 answers ─▶ decision record ─▶ Update
label_audit.py       the agent      report_form.py form       collect   collect save   report_form.py answers
```

## The rules

1. **Nothing preselected.** Every option starts blank (meaning_contracts refuses a preselected option).
2. **Blind cards first.** A random unflagged item is judged with its label hidden, before any flagged one.
3. **Train evidence only.** A card shows an item's exact excerpt; a Test item is cited by reference, never shown.
4. **One form per loop.** At most 20 cards; the form's limits hold, and a card over one is refused, not trimmed.
5. **A flag asks; it never decides.** "A flag does not establish an error" (deck v12, slide 3).

For use case 2 ("Recover a standard from existing labels"), the existing labels are evidence, read from per-rater
answers only: `label_audit.legacy_votes` raises `FenceError` for any field that is the same for every rater of an
item, such as an expert key, and the expert key stays with the score Task.

## The commands

Engine scripts sit in `skills/2_theme/labeling/engine/`; collect.py sits in
`skills/1_base/workbench/haipipe-interaction/scripts/`.

```text
label_audit.py legacy --raters <items.raters.jsonl> --answer Q_overall --groups a,b --out legacy_labels.jsonl
label_audit.py draw --legacy legacy_labels.jsonl --split split.json --seed <n> --out-dir result/
collect.py new <meaning Task> report_mNN --title "Loop N report" --for "<its sNN address>" --person <who>
report_form.py form report.json <run> --title "Loop N report" --for "<its sNN address>" --intro "<≤30 words>"
collect.py check <run> && collect.py build <run>
collect.py save <run> <the pasted text>        (then the form reopens read only)
report_form.py answers report.json <run>        (the decision record, validated)
collect.py applied <run> QN --by "<what changed, real names>"
```

The agent writes `report.json` itself: rule cards from the rules it infers, item cards from the drawn items,
`label_audit.evidence_row` for each item's excerpt. Card kinds and their option ids, which
`label_audit.apply_answers` reads:

```text
card            question_type     options
blind check     diagnostic        blind_unsafe · blind_safe · blind_cant_tell
an item         reference_label   keep · flip · change_rule (+ defer)
a tied item     reference_label   set_unsafe · set_safe · change_rule (+ defer)
a rule          define_rule       rule_holds · rule_change · rule_drop (+ defer)
```

The form's own last choice, "My own decision", is a custom answer, and its note is the comment (slide 23:
"Write another decision", "Reason and intended scope").
