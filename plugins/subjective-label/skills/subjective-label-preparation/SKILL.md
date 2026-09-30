---
name: subjective-label-preparation
description: >-
  Prepare raw transcript conversations into versioned, checked labeling items,
  reserve whole source groups for sealed test, and link an accepted package to
  a Labeling Page before Contract. Use for Data → Preparation or when a source
  is not yet a pre-unitized, safely fenced corpus.
metadata:
  version: "0.1.1"
  last_updated: "2026-09-29"
---

# /subjective-label-preparation

This is the upstream owner for Data → Preparation. Read
`$TOOLS_ROOT/plugins/subjective-label/CORPUS-PREPARATION.md` for the unit,
group, custody, and ownership rules. A preparation Run owns its Ticket and Result
under `<source-folder>/corpus-preparation/`; the Labeling Page references its
accepted package and never copies its candidate set or protected group frame.

Set `TOOLS_ROOT` to the checkout containing `plugins/subjective-label` before
using the commands below. In that checkout use `.`; in a consuming workspace
with a `Tools` link use `Tools`. Keep Page and source paths relative to the
current workspace or pass absolute paths. Set `PYTHON_BIN` to the current
workspace's interpreter (for example `.venv/bin/python`, or `python3` when
there is no project venv).

Use `engine/corpus_preparation.py` for structured transcript JSONL. Each row
needs `conversation_id` and ordered `turns` with `role` and `content`;
`split_group_id` may group related conversations. Other source formats require
an explicit normalizer that produces the same contract. Do not silently treat
one transcript row or one turn as the labeling unit.

Ask the identified preparation owner to choose `final-assistant-reply` or
`every-assistant-reply`, the earlier-context window, and the leakage group.
Record that choice with the `unit-recipe` Run. The target is the selected
assistant reply; `context_prev` contains only earlier turns. Never show
candidate or sealed text in a Page overview, prompt, embedding, or search.

Attach the source owner to the Page first so its five Run Types and live
Tickets are visible as each operation closes. Attachment is a reference, not
a Run. Use the canonical `<Page>/<Page>.md` file. If a Board still stores this
Page as a flat source, create its own Page folder with `/haipipe-page` first;
never attach to the flat group source or create a shared `labeling/` lane beside
it. Then run the five independent operations in order, passing the IDs
returned by each command to the next one:

```text
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/subjective-label/engine/corpus_preparation.py" attach \
  --owner <source-folder>/corpus-preparation --source-id <source-name> --page-file <page.md>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/subjective-label/engine/corpus_preparation.py" normalize \
  --owner <source-folder>/corpus-preparation --raw <transcripts.jsonl> --source-id <source-name>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/subjective-label/engine/corpus_preparation.py" recipe \
  --owner <source-folder>/corpus-preparation --snapshot <snapshot-id> \
  --selector <final-assistant-reply|every-assistant-reply> --accepted-by <owner>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/subjective-label/engine/corpus_preparation.py" materialize \
  --owner <source-folder>/corpus-preparation --snapshot <snapshot-id> --recipe <recipe-id>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/subjective-label/engine/corpus_preparation.py" check \
  --owner <source-folder>/corpus-preparation --snapshot <snapshot-id> --itemset <item-set-id>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/subjective-label/engine/corpus_preparation.py" reserve \
  --owner <source-folder>/corpus-preparation --snapshot <snapshot-id> --itemset <item-set-id> \
  --config <label-seed-config.yaml> --sealed-groups <count> --seed <integer> --custodian <name>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/subjective-label/engine/corpus_preparation.py" link \
  --owner <source-folder>/corpus-preparation --package <accepted-package> --page-file <page.md>
```

`--context-window <number>` on `recipe` limits prior turns; omit it to retain
all earlier turns. `reserve` assigns complete source groups using a seeded
draw. Inspect its public counts and QA receipt before linking. If a group
could expose the same target on both sides, repair the source grouping and
prepare a new snapshot. The private candidate set and protected frame stay
with the source owner. A changed source, recipe, or partition is a new
version, never an in-place edit of an accepted Result.

`--config` is the Page's proposed labeling seed configuration, with the
construct, human authority, labels, regions, and uncertainty choices. Use
`$TOOLS_ROOT/plugins/subjective-label/skills/label-building/ref/ref-config.md`
§1 for its schema; the
worker fills `corpus.path`, `id_field`, `text_field`, and `context_field` from
the accepted item set. Review those semantic choices with the responsible
human before reserving groups. The preparation owner and custodian are named
roles in the receipts; neither CLI value authenticates a person's identity.

After `attach`, Data → Preparation shows the source owner's completed Runs.
After `link`, it shows the five Runs bound to the accepted package and its
safe receipt. Data → Contract can consume the package with `engine/job.py create --source-job
<accepted-package> ...`. The Contract writer verifies the receipt and binds
the Page reference. Old pre-unitized fenced sources remain readable but do
not acquire a group-safety claim retroactively.
