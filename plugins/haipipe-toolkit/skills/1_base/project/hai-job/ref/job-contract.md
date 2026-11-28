# The Job contract

Read before creating a Job, adding a Task or naming a theme's Jobs. `hai-project/ref/ladder.md`
owns the folder hierarchy; `hai-task` owns Task execution. The Block type's contract determines
what a Job represents and whether it has a Task level. This contract owns the Job's records.

## Location

```text
bNN_〈block〉/
├── delivery/jNN_〈job〉/        this Job's published material, owned by the Block
└── jNN_〈job〉/
    ├── jNN_〈job〉.md          the face
    ├── sNN-〈topic〉/          topics serving this Job, when needed
    ├── runs/                   Job-owned Runs under hai-run
    ├── src/ · sbatch/          shared code and supervision, when needed
    └── tNN_〈task〉/           Tasks, when the owning type uses them
```

A Job that contains Tasks groups them around shared inputs, code or one question. Task code and
execution evidence stay under the Tasks. Shared code belongs in the Job's `src/`; a Job does not
hold a competing `scripts/`, `results/` or `notebooks/` tree. The Block owns delivery paths:
`delivery/jNN_〈job〉/tNN_〈task〉/〈lane〉/` selects a Task's published material. Resolve delivery
paths through `hai-delivery`; producing a file does not grant acceptance or release.

## Face

```markdown
# jNN · 〈title〉

goal: 〈what this Job delivers〉
close: 〈what must be true for it to close〉
emoji: 〈the Job's mark〉
job-type: 〈a type allowed by its Block type〉
answers: 〈Question address, when applicable〉

## Background
〈Optional context needed to understand the work〉

## Topic
〈Why this work belongs together〉

## Tasks
1. t01_〈task〉 · 〈title〉
2. t02_〈task〉 · 〈title〉

## Questions
〈The Job's own questions, when it has a register〉

## Deliverables
〈The output records this Job needs〉
```

- **Title:** use the real folder's words, with its assigned address. A theme-owned folder name uses
  that name instead of `jNN`. Rename references together when the folder's words change.
- **Goal and close:** state the intended output and its completion condition. Neither a file's
  presence nor a scaffold implies the Job is complete.
- **Emoji:** an authored mark for the Job, selected to distinguish it within its Block.
- **Type and group:** `job-type:` names the Job's declared type. The Block's `bands:` associates
  a numbered range with a group. Its group name and its use case do not determine its type;
  `code`, `doc` and `check` are example values, not a universal taxonomy.
- **Questions:** `answers:` links to a Block Question or one of its needs under `hai-report`.
  A Job may also own a question register without duplicating the Block's register.
- **Tasks:** when the Job has a Task level, `## Tasks` lists real Task folders in reading/dependency
  order. Their assigned numbers stay stable. Omit inapplicable levels rather than making dummy Tasks.
- **Background:** optional authored context. Keep data and explanation in the record; presentation
  of its text, figures and structured blocks belongs to the common workbench contract.

A theme may require additional fields and sections. The scaffold writes a skeleton: complete the
required fields from real evidence and the owning type contract before presenting the Job as ready.

## Deliverable records

`## Deliverables` holds a fenced YAML block. Each item names one output another reader uses;
its files, producing Runs and independent checks provide the evidence. The same record can name
an output that is planned but not built. Do not fabricate a file path or receipt to tick an item.

```yaml
deliverables:
- what: Reviewed summary table
  kind: table
  task: t02_summary
  means:
  - One row per included record, with the declared summary fields.
  files: t02_summary/runs/r01_summary/result/summary.csv
  run: t02_summary/runs/r01_summary
  checked_by: t03_check/runs/r01_validate
  count: 1
```

| Field | Meaning |
|---|---|
| `what` | Unique short name of the output; quote YAML text containing `:` |
| `kind` | `data`, `table`, `figure`, `card`, `check`, `site`, `view`, `code` or `doc` |
| `task` | Producing Task, when one owns the output |
| `means` | Short statements defining what the reader receives |
| `files` | File path, glob or list identifying the output |
| `count` | Required file count when the output contract specifies one |
| `run` / `runs` | Producing Run, or `{run, part}` entries whose required parts must finish |
| `checked_by` | Run that rebuilt or compared the output, separate from its maker |
| `from` | Input batches with their own `what`, `means`, `files` and `run` evidence |
| `open` | Unmet conditions, including any human acceptance still needed |
| `used_by` | Consumers that depend on the output |
| `example` | An illustrative file and selected columns |
| `browse` | Root and index for inspecting the output set |
| `opens` | Another item's `what`, when a view depends on that item's browse index |

`files` resolves from the face's folder, except `_WorkSpace/` and `code/` paths resolve from
SPACE root. `example.file` and `browse.root` resolve from SPACE root. Use exact Run addresses and
actual input/output dependencies. A Block may record outputs not owned by one Job on its own face.

An item is complete only when its declared files, producing Run gates and acceptance conditions
are satisfied. Keep an output while an active consumer still depends on it. A view's marks reflect
that evidence; the rules for presenting it belong to the common workbench owner.

`new_job.py check` validates Task-list consistency and the deliverables schema: unique `what`,
allowed `kind`, `means`, `files` or `opens`, and referenced Task/Run locations. It does not execute
Runs, verify every output's contents, enforce every theme field or grant acceptance. An output
file not built yet is a planned output, not a successful check of that output.

## Theme-owned names

A theme declares `level_patterns={"Job": 〈regex〉, "Task": 〈regex〉}` for its folder names.
A Job pattern applies directly under its Block, a Task pattern directly under its Job.
Scaffold with `--name 〈folder〉`; its face remains `〈folder〉/〈folder〉.md`.

The records are selected inside their owning Block's workbench page. Job or Task selection does
not create an independent page route or replace the Block title. UI navigation belongs to
`workbench`; this contract does not define a separate Job screen.

## Scaffold and check

```bash
S=plugins/haipipe-toolkit/skills/1_base/project/hai-job/scripts
python "$S/new_job.py" job <block> --slug <job> --title '<title>' --goal '<goal>' --close '<close>'
python "$S/new_job.py" task <job> --slug <task> --title '<title>' --kind <task-type>
python "$S/new_job.py" check <job>
```

Both creation commands accept `--nn`, `--name`, `--answers` and `--dry-run`. They refuse an occupied
folder. The Job scaffold writes title, goal, close, optional answers, Topic and Tasks; fill its
emoji, applicable type and required authored sections explicitly. The Task scaffold writes its
face and adds the entry to `## Tasks`; it creates `scripts/config/` and `runs/` for execution Tasks,
and leaves authored `draft`/`ideation` Tasks to their owner to create content and Runs when needed.
