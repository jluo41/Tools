---
name: haipipe-labeling-preparation
description: >-
  The one main skill of a labeling Job's items Task: read the Job's raw data
  once and fill the Data cards (describe), make the items under a recipe a
  person signs and run the item check (items), revise them from the person's
  notes into a new version (revise), and embed them under a build a person
  agrees (embed). Also prepares raw transcript conversations into versioned,
  checked labeling items, reserves whole source groups for sealed test, and
  links an accepted package to a Labeling Page before Contract. Use for an
  items Task's prompts, Data → Preparation, or a source that is not yet a
  pre-unitized, safely fenced corpus.
disable-model-invocation: true
metadata:
  version: "0.2.1"
  last_updated: "2026-10-26"
---

# /haipipe-labeling preparation

## The items Task (b15 s41-task-items-procedure)

An items Task (`task-type: items`, or the older `data`) turns its Job's raw data into the items a person labels.
This skill is its one main skill: every prompt its three tabs copy names it, and it calls any other skill itself.
The engine is `$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/items_task.py`; each step is a
hard Run in the Task's own `runs/`, run through its ticket, whose worker is the Task's `scripts/prepare.py` (a
forwarder `plan` writes).

**Start from a path** (JL 261014: "I want to run this, and make it work"). Called with only a Job or Task folder,
`/haipipe-labeling preparation <Job or Task>` (or the labeling door, `/haipipe-labeling <Job>`), first open the UI and
read where the Job stands with the labeling door's start script:

```text
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/haipipe-labeling/scripts/start.py" <path>
```

It opens the workbench in the browser on the tab of the step now (starting the SPACE's host when none runs) and
prints the Job's Tasks, the step, `who` does it, `do` what, and `open`: the full link. Tell the person in a few
lines: the steps done, the step now, and that tab, giving the full `open` link (never a bare `/_board/...` path).
Then:

1. `who: agent`: do that step now, as below, and stop at its end: after describe, say to reload 1 · Data; after
   planning items or embed, say to read the proposal in the tab and press Sign or Agree.
2. `who: person`: do nothing; say what to press, in which tab, and that the next message is the same start message.
3. Called again: the script reads the Job again; when it says `agent` and a ticket, run it, settle, say which tab to
   reload. A `note` (items made before recipes were signed, say) is said to the person as it is.

Below, `items_task.py` stands for `"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/items_task.py"`:
spell the whole command out each time, never through a shell variable (zsh does not split `$I` into words).

```text
1 describe  plan → type the config → run the ticket → settle      result/description.json: the Data cards
2 items     plan (the recipe, proposed) → a person Signs → run → settle   items-vN/ in the store; check, stats
  revise    the person's notes → plan revise (the recipe changed, `changed` typed) → Sign → run → items-vN+1
3 embed     plan (the build, proposed) → a person Agrees → run → settle   map, groups, near-duplicates, outliers
```

```text
items_task.py plan   <task> describe|items|revise|embed [--notes "<the person's notes>"] [--model <id>] [--data <path>]
items_task.py sign   <task> <rNN_run> --by <person>      the person's word; the workbench's Sign / Agree buttons write it
items_task.py settle <task>                              after a ticket: each finished Run's card takes its receipt's status
items_task.py sample <task> raw|items [--seed N]         what Draw again shows; reads, writes nothing
items_task.py status <task>
items_task.py next   <Job or Task>                       where it stands; who does the next thing, and what
bash <task>/runs/<rNN_run>/<rNN_run>.sh       the one way a step runs
```

1. **The data comes from the Job.** Its face's `dataset:` and `data:` lines name it; nothing is typed in the Task.
2. **describe:** `plan` guesses the unit, the text and the answer columns. Type what the config asks, never
   guessing a meaning: what one row is; the background from the data's SOURCE.md or paper; the column groups and
   their meanings; the answer columns (`labels: {expert: [...], rater: [...]}`); the text to label. Then run it.
3. **items:** `plan` proposes the recipe from the Data cards: the unit, the item id, the text judged (`main`), the
   context before (its column and the tags that open a turn, each named, e.g. `<TAG>: Person`), after, the
   columns kept out (every answer), the group never split, and the next free `items-vN`. Correct it, then stop:
   the worker refuses an unsigned recipe. After the person signs, run it. The item check (unique ids, one item
   per unit, nothing judged empty, no label inside) is its gate; a version is never rewritten.
4. **revise:** the person's notes come in the prompt (an image note is a file in the Task's `notes/`, its path in
   the notes). `plan revise --notes "..."` copies the last recipe; change what the notes ask, type `changed`, stop
   for the Sign. Each pass is a new Run and a new version; the notes stay in its config.
5. **embed:** `plan embed` proposes the build (a sentence-transformers model when installed, else `tfidf-svd`);
   stop for the Agree, then run it. The vectors go to `$HEAVY_DIR`, the map and groups to `result/`. A group or a
   place on the map never sets a label.
6. **Settle** after every ticket, so the Run's card says what its receipt says.

## Corpus preparation for a Labeling Page

This is the upstream owner for Data → Preparation. Read
`$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/CORPUS-PREPARATION.md` for the unit,
group, custody, and ownership rules. A preparation Run owns its Ticket and Result
under `<source-folder>/corpus-preparation/`; the Labeling Page references its
accepted package and never copies its candidate set or protected group frame.

Set `TOOLS_ROOT` to the checkout containing `plugins/haipipe-toolkit/skills/2_theme/labeling` before
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
Page as a flat source, create its own Page folder with `/haipipe-draft` first;
never attach to the flat group source or create a shared `labeling/` lane beside
it. Then run the five independent operations in order, passing the IDs
returned by each command to the next one:

```text
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/corpus_preparation.py" attach \
  --owner <source-folder>/corpus-preparation --source-id <source-name> --page-file <page.md>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/corpus_preparation.py" normalize \
  --owner <source-folder>/corpus-preparation --raw <transcripts.jsonl> --source-id <source-name>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/corpus_preparation.py" recipe \
  --owner <source-folder>/corpus-preparation --snapshot <snapshot-id> \
  --selector <final-assistant-reply|every-assistant-reply> --accepted-by <owner>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/corpus_preparation.py" materialize \
  --owner <source-folder>/corpus-preparation --snapshot <snapshot-id> --recipe <recipe-id>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/corpus_preparation.py" check \
  --owner <source-folder>/corpus-preparation --snapshot <snapshot-id> --itemset <item-set-id>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/corpus_preparation.py" reserve \
  --owner <source-folder>/corpus-preparation --snapshot <snapshot-id> --itemset <item-set-id> \
  --config <label-seed-config.yaml> --sealed-groups <count> --seed <integer> --custodian <name>
"$PYTHON_BIN" "$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/corpus_preparation.py" link \
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
`$TOOLS_ROOT/plugins/haipipe-toolkit/skills/2_theme/labeling/haipipe-labeling-building/ref/ref-config.md`
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
