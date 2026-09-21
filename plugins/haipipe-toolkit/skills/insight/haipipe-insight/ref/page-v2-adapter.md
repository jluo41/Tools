# Page v2 adapter · Insight semantics over the shared Page lifecycle

Every Application Insight Folder is a Page, but the two workflows answer
different questions:

```text
Page workflow     is this one Page ready and closed?
Insight workflow  may this Page's epistemic authority advance its register cell?
```

## Nested lifecycle

For Page work, the Insight dispatcher resolves the declared Folder owner and
the selected native Run targets, then delegates bounded Page coordination:

```text
CONTEXT → OUTLINE → EVIDENCE → CONTENT → CHECK → CLOSE
                                                    │
                                                    ▼
                                              test GI<n>
                                                    │
                                                    ▼
                                             update Question Queue
```

Only Page CHECK may emit Page `CLOSE`. A Page Run such as
`rp-struct-01` or `rp-para-01_P01` records a selected human-feedback unit;
closing it never closes the Page and never advances a GI gate. An Insight
dispatch does not allocate a Page Run unless the person actually selected an
interactive Page-writing goal.

This diagram describes Page control dependencies. Resume the current native
Run or the Page authority that owns the remaining work; it does not require a
full controller pass for a wording Step. Index actual RP/RE/RD/native Runs in
the Insight Runtime and keep Page control receipts separate.

## Evidence and semantic lineage are different edges

Actual values, citations, and displays use the shared Page evidence graph:

```text
Supporting Run Result(s)
        ↓
one frozen Local Input per Evidence Item
        ↓
one local Page Evidence Run
        ↓
typed VALUE | CITE | DISPLAY Result
```

Cross-Folder evidence never enters through a new PageX binding. A related Page
link is navigation or context until an accepted Supporting Run Result supplies
the evidence. A governed page-local static source may be frozen directly in
Local Input under the Page contract.

Insight also needs a semantic edge between rows. That edge records how a child
row interprets already-authorized parents; it neither invents a Run nor replaces
the evidence graph underneath those parents. Use one Folder-owned `PARENTS` row
beside each I/K/W finding:

```text
PARENTS  <exact Page path>@<Page version>#sha256:<hash> · <row-id>[, <row-id>...]
```

The child additionally records its own operation (`DERIVATION`, claim test, or
applicability judgment). A parent change reopens only the rows and Queue cells
that cite it. The two legal same-rung exceptions remain X Information from
mirrored I rows and the pooling-verdict K row from the heterogeneity K row.

A missing calculation needed to finish an existing cell is an Evidence Item of
that cell's owning Page, even when a reusable Task supplies its Supporting Run.
Do not register a second QD/QI/QK/QW row merely to commission the method. Add a
new question only when the desired Result answers a distinct epistemic ask or
changes the target rung/scope; implementation reuse alone is not a new question.
A rung change allocates the destination register's next legal id, with reciprocal
`supersedes` / `superseded-by` links under the Question contract. Never move a QI
id into a Knowledge register or carry its completed cells into the successor.

For a Task-side Insight RF bridge, the Supporting Run pins the exact
instance/item/execution-version/Result path/hash, while `PARENTS` names the
exact D/I/K/W/RF rows inside that Result. The local Wisdom Page still owns
applicability, counsel, forbidden overreach, `serves:`, and the human signature.

## Cross-board handoff

A signed W handoff is a frozen Application input, not a synthetic Run and not a
new PageX lane. Design pins the exact handoff path, Page version, content hash,
signature, and the Question GI6 settlement receipt in its Context/Evidence input. It
may consume the handoff but may not reopen upstream computation from Design.
Record current eligibility using [handoff-record.md](../../haipipe-insight-workflow/ref/handoff-record.md);
a historical signature by itself cannot establish current eligibility.

## Migration

Existing PageX and `probe/` material remains readable migration history. New or
reopened work follows these rules:

- do not bulk-rewrite settled historical pages;
- `OWE-ON-NEXT-TOUCH` for the Page v2 evidence/lineage record;
- preserve historical Queue marks and add an owed migration finding rather
  than flipping them backward;
- migrate an old PageX evidence edge to an accepted Supporting Run Result, or
  to a governed Local Input only when it is genuinely page-local static input;
- never select `latest`; preserve exact historical path/version/hash;
- the requirement for a person signature applies immediately and is never
  grandfathered; current eligibility still requires exact payload/dependency
  pins and GI5/GI6 owner records.

New pages declare `folder-kind:` on the Page; a separately governed identity
record uses `workflow/folder.yaml current.folder-kind`. Neither records execution
progress. See `../../haipipe-insight-workflow/ref/migration.md` for old identity
files and skill paths. Legacy `page-type:` is a read-only compatibility key.
