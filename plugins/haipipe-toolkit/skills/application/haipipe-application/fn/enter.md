# `enter` · open an Application, or scaffold it from nothing

The verb every session starts with. It reports state and never changes a Page.

## Resolve

1. Take the path given, or the current directory. Walk up until a folder holds at least one `*-InsightBoard/` or `*-DesignBoard/`; that folder is the Application root.
2. If none is found, this is not an Application yet. Offer to scaffold (below) and stop until the operator answers.
3. List every board by kind: `ls -d *-InsightBoard *-DesignBoard`. Report each board's subject, taken from the folder name.

## Report, derived from disk and never from stored status

```text
board                           head page        pages    open
──────────────────────────────────────────────────────────────────────────
SmsClickR4-InsightBoard         MT00-meta ✅     I01 ✅ I02 🔨   QI3 unanswered
YoungMaleRefill-DesignBoard     BR00-brief ✅    DS01 🔨         R3 unaccepted
```

For each board report, in this order:

1. Whether the head page exists and whether it closed. A board with no head page is the first thing to fix.
2. One row per Page, with its `state:` line.
3. **InsightBoard only**: register Queue rows with no answering page (read the wisdom register's rollup), and any source whose as-of date is older than a dependent Page's reading.
4. **DesignBoard only**: divisions with no `accepted:` row, and rows cleared by a handoff that has since moved.
5. Stale PageX bindings on either board, by comparing the bound version against the target's current one.

Then state the frontier and maturity from the vocabulary in `SKILL.md` §Status, and name the single next command.

## Scaffold, only on an explicit yes

Ask for two subjects and one layout before creating anything, because a board's folder name says its subject and renaming one later breaks every PageX binding into it, and the InsightBoard's layout is made once, at scaffold.

```text
what data will this read?      → <DataSubject>   PascalCase   SmsClickR4
what is being designed?        → <DesignTopic>   PascalCase   YoungMaleRefill
one story or several?          → layout          rung-major (default) | partition-major
```

The layout ask decides the InsightBoard's group tree and nothing else. Rung-major is the default and the tree below; a subgroup that is at most a column inside an I page has not earned the other layout. Partition-major is for subgroup analysis as first-class, the same ladder per subgroup under shared thresholds: consult `ref/partition.md`, scaffold `1-F-full/` and `X-cross/` (index-free: letters sort after digits, so X seats itself last and later partitions rename nothing) in place of the four rung groups, let MT00 carry the partition register and the shared-threshold rule, and give every register Queue one column per partition (`haipipe-page-for-question` 0.2.1). The layout is never stored as a key; the group names on disk ARE the record.

Create both boards with their head pages, then stop:

```text
<root>/<DataSubject>-InsightBoard/board.md
<root>/<DataSubject>-InsightBoard/0-MT-meta/MT00-meta/MT00-meta.md                            page-type: meta
<root>/<DataSubject>-InsightBoard/0-MT-meta/MT01-question-data/MT01-question-data.md          page-type: question
<root>/<DataSubject>-InsightBoard/0-MT-meta/MT02-question-information/…                        page-type: question
<root>/<DataSubject>-InsightBoard/0-MT-meta/MT03-question-knowledge/…                          page-type: question
<root>/<DataSubject>-InsightBoard/0-MT-meta/MT04-question-wisdom/…                             page-type: question
<root>/<DesignTopic>-DesignBoard/board.md
<root>/<DesignTopic>-DesignBoard/0-BR-brief/BR00-brief/BR00-brief.md                          page-type: brief
```

Create no chain page and no Design Page: both need a subject nobody has named yet. Never infer an audience, behavior, or venue. An InsightBoard whose Meta Page is written and whose four registers are empty is a complete state, so scaffolding may legitimately stop with one board usable and the other only framed.

Return the Application root, one line per board, the frontier, and the next command.
