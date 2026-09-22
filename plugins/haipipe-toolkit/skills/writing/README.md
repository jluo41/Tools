# writing

The prose layer: draft from an approved plan and evidence, revise existing
writing within its authorized scope, or evaluate a candidate. Return readable
prose, located findings and genuine changes in the host's record format.

```
writing/
├── haipipe-writing/              🚪 the door, and the only writer: draft · revise · evaluate → methods → review → host return
│   └── ref/external/README.md    📚 the anti-AI writing shelf: what we call, what we only read
├── 1_style/
│   └── writing-dna-skill/        ✍️ vendored · distills an author corpus into a frozen Writing DNA (role: style)
└── 2_evaluate/
    ├── academic-humanizer/       🎓 vendored · papers, theses, rebuttals, NSF/NIH proposals (role: evaluator)
    └── humanizer/                🧹 vendored · blader's general-register humanizer (role: evaluator)
```

Two treatments for external skills, the same rule `discovery/` uses for its
search and review workers. A skill we **call** is an adapted copy in a numbered
folder, named in `haipipe-writing/ref/writing-methods.yaml`, with its LICENSE
and a CHANGELOG that stamps the upstream commit. A skill we only **read** stays
in `references/` and is digested in `haipipe-writing/ref/external/README.md`;
what we wanted from it is already in `haipipe-writing/ref/anti-slop-rules.json`, `haipipe-writing/ref/ai-tells.md`,
or `haipipe-writing/cli/anti_slop.py`.

There is no `1_write/` folder. The writer is the door itself: `haipipe-writing`
drafts and applies every edit under its surgical-revision rule, and no external
skill is allowed to write. Upstream, both humanizers are rewriters; here they are
bound as evaluators that return findings, and Writing decides what changes.
`1_style/` shapes the voice before the draft (a frozen Writing DNA is an input to
the writer, not a writer), and `2_evaluate/` judges after it. The numbers follow
that stage order around the door.

**Scope.** Writing provides prose work for Paper, Page, Insight, Design and
standalone files. The host owns its plan, Evidence, Run state and acceptance.
Writing owns the scoped candidate, genuine change trace and evaluation.

When a host already has an approved outline and evidence, read
`haipipe-writing/ref/realize-from-plan.md`. The host keeps ownership of the
outline, claims, and evidence; this worker turns one bounded plan slice into
reviewable prose and applies the shared change-record contract.

**Page integration.** Section and Paragraph Runs use the same
[Writing request](haipipe-writing/ref/writing-request.md), with their actual
scope and existing Run/Version/Step. Their host stores clean Before/After and
the review; method calls never allocate additional Runs.

**External capabilities.** Select writers, style inputs or evaluators through
[the method adapter contract](haipipe-writing/ref/method-adapter-contract.md)
and [catalog](haipipe-writing/ref/writing-methods.yaml). A vendored entry resolves
to its numbered folder; a frozen-profile entry resolves from the supplied packet;
the catalog never installs or launches anything. Missing required methods block;
optional ones are visibly skipped.
