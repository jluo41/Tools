# Insight Playbook

Start here if you do not know what the insight folder is for.

First look at the workflow image:

[00_workflow_image.md](00_workflow_image.md)

The short version:

```text
finished work -> review -> INSIGHT_REVIEW.yaml -> apply -> insight cards
```

`insights/` is not a place to dump everything. It is the project's permanent
memory: small, reusable cards that future narratives, applications, and papers
can cite.

## The Two Commands

```bash
/haipipe-insight review <folder>
```

Use this when you have a completed task, probe, narrative, discovery note, or
application ask session. It asks: "What here is worth keeping?"

It writes:

```text
INSIGHT_REVIEW.yaml
```

Then:

```bash
/haipipe-insight apply <INSIGHT_REVIEW.yaml>
```

Use this after the review checklist looks right. It writes or updates the real
cards under `insights/`.

## What To Read

Read these files in order:

1. `00_workflow_image.md` shows the whole review/apply workflow as one picture.
2. `01_plain_mental_model.md` explains the idea without haipipe jargon.
3. `02_toy_walkthrough.md` walks through a fake project from source material to cards.
4. `03_INSIGHT_REVIEW.example.yaml` shows the review checklist.
5. `04_cards_after_apply.md` shows what gets written after apply.
6. `05_when_to_update_cards.md` explains merge, update, supersede, and change logs.

## The Rule Of Thumb

Do not ask "Which folder should this go in?"

Ask:

```text
Is this a reusable thing future work should cite?
```

If yes, review it. If no, leave it in the task, probe, narrative, or application
folder where it was produced.
