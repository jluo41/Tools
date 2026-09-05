# Task Folder Page Face

Load this reference when creating, reading, repairing, or checking the
same-stem Page inside one executable Task Folder. `haipipe-task` owns this
contract; `haipipe-page` supplies the shared Page frame and
`haipipe-page-workflow` supplies CONTEXT through CHECK.

## Ownership and identity

```text
Task Folder
├── Task Face   workflow/ · scripts/ · runs/ · generated Results
└── Page Face   <task>.md · outline/ · readable interpretation
```

The Page and Task faces name the same `bNNjNNtNN` object. A new Task Page
declares:

```yaml
folder-kind: task
task: .
```

Add the exact `task-type:` when a specialist owns the executable dialect.
`page-type: task`, `job:`, and `task-folder:` are legacy spellings accepted on
existing Pages only. Do not write them into a new Page.

Historical Log entries and immutable workflow receipts may still name the
retired `haipipe-page-for-task`. Preserve those records as provenance, but
resolve their current law to this reference; never dispatch or recreate the
retired skill.

The Page Face is not a run log. It is the technical report of what the Folder
found and what those findings mean for the Task's own question. Machinery stays
in the Task Face and is referenced by path.

## Reader promise

The Page must let a reader answer four questions without reconstructing the
execution history:

1. What question was this Task run to answer?
2. What data and method make the Result believable?
3. What did the ready Runs establish, including nulls and residuals?
4. What is the current reading, and what Run would settle what remains?

`workflow/report*.yaml`, `RUN_AUDIT.md`, metrics, and notebooks report what ran.
The Page adds the interpretation they cannot own. Do not copy those files or a
QA digest into Page prose.

## Outline grammar

SHAPE chooses one of two forms:

```text
FLAT     one topic; role words are the Content divisions
NESTED   several topics; each topic is a division and role words are paragraphs
```

Use NESTED only when another topic needs its own Data or Method. Otherwise keep
the Page FLAT even when Method, Landscape, or Result repeats.

The closed role order is:

```text
Introduction → Concept → Landscape → Data → Method → Result → Conclusion
```

- `Introduction` is optional, appears once, and is first when present.
- `Concept`, `Landscape`, and `Data` may be Page-level.
- `Landscape`, `Method`, and `Result` may repeat.
- At least one `Result` is required.
- An unresolved finding earns a Result-role division; it is not hidden in a
  footnote or Conclusion.
- `Conclusion` appears exactly once, at Page level, and is always last.

Titles state what the reader learns, not where material lives. `Inputs`,
`Runs`, `Provenance`, and `Run receipts` are Task machinery, not division
titles. A new Run adds a reading row; it creates a new Result division only
when no existing division can absorb the new message without making its title
false.

Each Content division begins with one captioned face diagram that previews the
division's argument. Do not create a separate Page-level `## Diagram` section.
The shared Page renderer generates `## Outline` from
`outline/<stem>-outline-v<N>.md`; the authored Page must not duplicate it.

For this non-Section Page, the normal realization unit is one prose paragraph
per plan Bullet; the paragraph may contain one or more sentences. Its final
source line ends with the invisible stable backlink:

```html
<!-- realizes: C<n>.P<m>.B<k> -->
```

Do not make one paragraph realize two Bullets; split it. When one Bullet needs
several paragraphs, each paragraph repeats the same backlink. Diagrams,
headings, the READING table, and Task machinery are not prose realization
units and do not carry `realizes:`.

## Evidence and Run binding

Use the shared Page evidence graph. SHAPE names typed
`E<NN>-VALUE|CITE|DISPLAY-<slug>` items and their expected ready payload.
SURVEY records the full graph; LAND executes it; EMBED folds ready Results
back into the plan:

```text
0..N Supporting Runs (Execution or Discovery)
                  ↓ validated Results
1 frozen Local Input per Evidence Item
                  ↓
1 local Page Evidence Item Run
                  ↓
1 ready typed Result
```

For this Job-backed Task dialect, the authored Evidence Item row moves through
these exact owner-native forms:

```text
SURVEY, no Ticket   Local Run: Page · Evidence Item · new-run · bNNjNNtNN
LAND, allocated     Local Run: Page · Evidence Item · registered · bNNjNNtNNrNN
LAND, ready         Local Run: Page · Evidence Item · reuse · bNNjNNtNNrNN
                              → $OUTPUT_ROOT/results/<task>/<RUNNAME>/
later same contract Local Run: Page · Evidence Item · rerun · bNNjNNtNNrNN
```

SURVEY never invents the `rNN`; LAND allocates the next real Task Run id. A
materially changed target, frozen input, or acceptance contract requires a new
Run rather than `rerun`.

`$OUTPUT_ROOT` resolves to the Job in self-serving mode and to the
consumer-owned mirrored Job root in consumer-serving mode. The Ticket remains
under the Task's `runs/` in both modes; the Page does not copy the Result back
into the Task Folder.

Every shown number names the full Run that produced it. Bind by path and
fingerprint; never paste a regenerating result as an untraceable value. A
page-local static source may enter the frozen Local Input. A cross-Folder fact
must enter through a Supporting Run Result.

The Run overview belongs to `haipipe-plugin-runs`; the evidence state belongs
to `outline/<stem>-evidence-items.md` and `outline/evidence/`. Neither becomes
a Content division.

## Reading and closure

The final Conclusion carries exactly one `<a id="reading-current"></a>` anchor
followed by one `#### READING · current` table with one stable `R<NN>` row per
independently interpreted topic or Result family:

| ID | Topic | Verdict Run | Ruling | Meaning |
|---|---|---|---|---|
| `R01` | `<topic>` | `<full-run-id>` | `✅ read · <who> · <timestamp>` | `<plain-language meaning>` |
| `R02` | `<topic>` | `<full-run-id>` | `⬜ unread` | `<meaning to establish>` |

Below the table, `answers`, `not answered`, and `next run` name the current
scope and residual.

This table is the Task owner's `page_ruling: local`; there is no separate Page
`accepted:` field. CHECK passes the owner gate only when every current row has
a person-written `✅ read · <who> · <timestamp>`, every Verdict Run resolves,
and the block's residual fields are current. Its receipt points to the durable
gate as:

```yaml
human_gate:
  required: true
  status: passed
  evidence: ["<task>.md#reading-current"]
```

The CHECK receipt's immutable Page version/hash binds that pointer to the exact
rows judged. `R<NN>` ids never renumber. When a Verdict Result changes, keep
the row id, update its Run binding if needed, and reset its Ruling to
`⬜ unread`.

A negative or null verdict may close a reading. An unbound verdict cannot.
When the named Result changes, only its dependent reading, evidence binding,
and Page version become stale; the Task identity does not change. Route the
Page back to EVIDENCE or CONTENT as appropriate, then CHECK the exact rebuilt
version. The Folder is closed only when P-B-E-R and this Page reading are both
current.

The Page's top-level `state:` is therefore a cross-face Folder state, not a
claim that one script or one Run succeeded. It may become `closed` only when
the Task Folder's current P-B-E-R records and the current READING gate above
all pass. A new or stale Run reopens the affected evidence, reading, and Page;
it does not create a new Board Page.

## QA boundary

`QA/<n>-<slug>.md` answers one outside question and is written only by the Task
QA door. The Page holds the Task's standing self-reading. Reference a QA file
by path in the Context/Files record when needed; never copy its prose into the
Page or edit it from the Page workflow.

## Template and checks

Start from `ref/task-page-template.md`, which specializes the shared Board Page
template. Then run the Page workflow and the Task tree checker. Before closure:

- the Page declares `folder-kind: task` and names the same Task as its path;
- every Content division follows the chosen FLAT or NESTED grammar;
- every Content division opens with one captioned face diagram, with no
  standalone Page-level Diagram or authored Outline section;
- every typed item has the declared Supporting/local Run graph and accepted
  Result;
- every shown number resolves to a full Run id;
- Conclusion is last; its one current READING table is the local Page ruling,
  and every stable row is current and person-read;
- machinery and QA prose remain in their owning files.
