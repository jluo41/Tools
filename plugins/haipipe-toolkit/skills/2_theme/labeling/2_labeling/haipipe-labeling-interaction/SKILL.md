---
name: haipipe-labeling-interaction
description: >-
  The 🧭 meaning Task of a labeling Job, step by step: Frame, then loops of Report → Preferences → Update. The only
  Task that asks the person: each loop writes one interaction report (cards drawn from the corpus, nothing
  preselected) as a /haipipe-interaction form, saves the person's answers, and Update turns them into reference
  labels lNN and guideline mNN, a mind map whose rules cite their cards; the person signs mNN before expression runs.
  It runs the prompts the workbench's meaning page copies. For use case 2 the cards come from an existing labeled
  corpus's raters' votes, any expert key fenced out. Trigger: meaning loop, frame the task, interaction report,
  report-NN, save my answers, Update, approve mNN, audit the existing labels, use case 2,
  /haipipe-labeling-interaction.
metadata:
  version: "0.2.0"
  last_updated: "2026-11-01"
  # version history: ./CHANGELOG.md
---

# /haipipe-labeling-interaction · the meaning loop, one step per prompt

Only the 🧭 meaning Task asks the person (b15 s58-D03; JL 261101: "we hope that the interaction is only available in
the meaning loop task"). Its page (Work: Frame · Report · Preferences · Update) copies one prompt per step into the
Task's chat session; each prompt below names its step, and this skill does exactly that step, then replies with the
page's link and nothing else (the form is the conversation).

```text
Frame ─▶ Loop 1: Report ─▶ 🙋 Preferences ─▶ Update ─▶ ✍️ your sign m01 ─▶ 🛠 expression
                Loop 2: Report (with expression's round report) ─▶ … ─▶ m02
```

## The layout (engine/meaning_versions.py reads it; the page and these steps agree)

```text
<meaning Task>/                          task-type: labeling-meaning
├── runs/rNN_collect_frame_decisions/    Frame: what to judge, which standard, who decides (a record or a form)
├── runs/rNN_draw_report_mNN/            Loop NN's draw: result/draws.json, signals.jsonl (use case 2)
├── runs/rNN_rules_report_mNN/           Loop NN's cards: result/report.json (+ rules.md, issue_groups.json)
├── runs/rNN_collect_report_mNN/         Loop NN's form (collect.py), report.json beside it, applied.md
├── runs/rNN_update_mNN/                 result/labels.jsonl (labels lNN), changes.md, decision_record.json
└── meaning/mNN.mindmap.md               guideline mNN; mNN.approved.yaml is your sign
```

Loop NN makes mNN: every Run of the loop ends in `_mNN`. `meaning_versions.py loops <Task>` says where each loop
stands. Scripts: engine `E = skills/2_theme/labeling/engine/`; `collect.py` is
`skills/1_base/workbench/haipipe-interaction/scripts/collect.py`; run them with the SPACE's `.venv/bin/python`.

## 1 · Frame: "step Frame"

1. Read the items Task (its items, their context) and any old labels' sources the Job's `schema.yaml` names. List the
   assumptions in the person's rough idea (the prompt's Goal, Use cases and Constraints rows).
2. Ask the three frame questions on one form: what to judge, which standard (a new one from the person's judgment, or
   recover an existing one), who decides. `collect.py new <Task> frame_questions --title "Frame questions" --for
   "<the Task's sNN address>"`, write `question_collection.md` (your assumptions in each why), `check`, `build`.
   When the person already decided in the chat, `collect.py record <Task> frame_decisions …` instead.
3. Once answered: `collect.py save`, write the Task face's `goal:` and the Job's `schema.yaml` (the label values) from
   the answers, then `collect.py applied` on each. Reply: the Task's Work › Frame link.

## 2 · Report: "Loop N: prepare interaction report-0N"

1. `meaning_versions.py loops <Task>`: Loop N's Runs so far. A planned Run with a ticket is the person's to press.
2. Draw the cases into `runs/rNN_draw_report_mNN/result/`:
   - use case 2 (existing labels): `E/label_audit.py legacy …` then `E/label_audit.py draw --legacy … --split … --seed
     <n> --out-dir …`: hard (flagged: split, tie, Unsure, a group gap), random (unflagged, label hidden), typical;
   - use case 1 (a new standard): typical items from the items Task's corpus map, hard ones at its boundaries, random
     ones by seed. Never a Test item's text.
3. Write `report.json` (meaning_contracts' report): blind cards first, then rule cards, then the hard items;
   `E/label_audit.py`'s `evidence_row` for each excerpt; options never preselected. A rule card's `current_rule` quotes
   its mind-map rule word for word, so the page tags that rule with the card. Any expression round report since the
   last loop (its `round_report.md`) becomes cards too: a wrong label is an item card, a rule gap a rule card.
4. The form: `collect.py new <Task> report_mNN --title "Loop N report" --for "<sNN address>"`, then
   `E/report_form.py form report.json <the Run> --title … --for … --intro "<≤30 words>"`; keep `report.json` beside
   the form; `collect.py check <Run>` and `collect.py build <Run>`.
5. Reply: the Task's Work › Preferences link only.

## 3 · Preferences: "save my answers to report-0N … then start Update"

The page embeds the form; its Copy prompt carries the prompt, the person's notes, the session line, then the form's
answer block (from its `haipipe-interaction answers` line to the end).

1. `collect.py save <the Run> <that block>`; the form reopens read only. A refusal (an older form, a wrong Run) is
   said as it is; never edit the paste to pass.
2. The notes go into Update's decisions; then do 4 · Update at once.

## 4 · Update: "step Update, Loop N"

1. Labels: `E/meaning_update.py labels --report <report.json> --form <the collect Run> --previous <labels>
   --version lNN --out runs/rNN_update_mNN/result`, where `<labels>` is the last Update's `labels.jsonl` (Loop 1: the
   existing labels, l00). It writes `labels.jsonl`, `changes.md` (each changed label, then the rule answers the
   guideline must take) and `decision_record.json`.
2. Guideline: write `meaning/mNN.mindmap.md` from m(N-1) (Loop 1: the frame's question as the root, the label values
   as branches). Apply each rule answer in `changes.md`; a changed or new rule's note reads `from rNN QN: <what>`; a
   deferred card's rule stays, its note `open: rNN QN deferred to Loop N+1`. Check it with /haipipe-mindmap.
3. Flags: `collect.py applied <the collect Run> QN --by "<what changed, real names>"` for each applied answer;
   `--state "in progress" --by "Loop N+1's report: …"` for a deferred one.
4. Never sign. The person signs on the page (Update: Approve mNN), which writes `meaning/mNN.approved.yaml` through
   `meaning_versions.approve`; expression runs only on a signed mNN. Reply: the Task's Work › Update link.

## The rules

1. **Nothing preselected.** Every option starts blank (meaning_contracts refuses a preselected option).
2. **Blind cards first.** A random unflagged item is judged with its label hidden, before any flagged one.
3. **Train evidence only.** A card shows an item's exact excerpt; a Test item is cited by reference, never shown.
4. **One form per loop.** At most 20 cards; a card over a limit is refused, never trimmed.
5. **A flag asks; it never decides.** "A flag does not establish an error" (deck v12, slide 3).
6. **Only the person signs.** No agent writes `mNN.approved.yaml`; an unclear answer becomes Loop N+1's card.

For use case 2 ("Recover a standard from existing labels"), the existing labels are evidence, read from per-rater
answers only: `label_audit.legacy_votes` raises `FenceError` for any field that is the same for every rater of an
item, such as an expert key, and the expert key stays with the score Task.

## Card kinds

Their option ids, which `label_audit.apply_answers` (through `meaning_update.py`) reads:

```text
card            question_type     options
blind check     diagnostic        blind_unsafe · blind_safe · blind_cant_tell
an item         reference_label   keep · flip · change_rule (+ defer)
a tied item     reference_label   set_unsafe · set_safe · change_rule (+ defer)
a rule          define_rule       rule_holds · rule_change · rule_drop (+ defer)
```

The form's own last choice, "My own decision", is a custom answer, and its note is the comment (slide 23: "Write
another decision", "Reason and intended scope").

A worked example that runs every step with these tools on synthetic chats:
`servers/workbench-labeling/tests/labeling_example.py` (its output is Tools'
`blueprints/Project-Ladder/labeling/b01_labeling_example`).
