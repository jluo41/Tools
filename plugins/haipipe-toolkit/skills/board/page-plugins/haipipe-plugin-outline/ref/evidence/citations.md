# Citations and Bib authority

This reference is loaded by `haipipe-plugin-outline` when work reads or
writes citation entries, verifies a source, builds a citation workbench, or
aggregates Discovery Result Bibs. The parent skill remains the only Plugin.

## One law

A machine may copy a BibTeX entry verbatim from a trusted publisher/index or
a person, subset existing entries, validate them, deduplicate exact entries,
and stable-sort them. It MUST NOT invent or complete title, author, venue,
year, pages, DOI, or key from model memory.

A person supplying citation metadata is not the same as supplying a complete
BibTeX entry. Formatting supplied fields into BibTeX is composition; only a
complete supplied entry may land through the person route.

## Authority mode A · ordinary Page

```text
<page>/outline/evidence/bibex/
├── <stem>.bib           PRIMARY · the Page's own person/workflow material
└── <stem>-bib.html      DERIVED · citation workbench
```

Refresh may subset entries from a trusted seed Bib. A person-supplied complete
entry may land verbatim. The workbench regenerates freely.

## Authority mode B · Discovery aggregate

```text
<task>/results/<RUNNAME>/<RUNNAME>.bib  PRIMARY · one verified Subject entry
                         │
                         ├── validate complete Result
                         ├── reject key/DOI conflicts
                         ├── deduplicate exact entries
                         └── stable key sort
                         ↓
<task>/outline/evidence/bibex/<task>.bib        DERIVED · Page Evidence Bib
<task>/outline/evidence/bibex/<task>-bib.html   DERIVED · citation workbench
```

Only Results whose runtime says `status: complete` enter the union. Every
source Result Bib contains exactly one entry, and its key equals the Result
Card's `cite: @Key`. Planned, running, blocked, unresolved, and superseded
Results are excluded.

The derived Task Bib is never the correction target. Verification or metadata
repair lands in the owning Result Bib first, then the aggregate and workbench
are rebuilt. A key or DOI conflict hard-fails instead of choosing silently.

Citation content and verification judgment are separate authorities. Never add
local verification fields to a verbatim BibTeX entry. Discovery persists the
person judgment beside that primary entry in the owning Result receipt:

```yaml
# results/<RUNNAME>/runtime.yaml
bib:
  source: <trusted export URL or supplied-entry receipt>
  mode: verbatim_copy
  verification:
    status: verified        # pending | verified
    by: <person identifier>
    at: <ISO-8601 timestamp>
```

Missing `verification` means `pending`; a machine may never write
`status: verified`. For an ordinary Page, the authoritative CITE Evidence Item
stores `verified: ✅` beside that item and its workflow receipt records person
and timestamp. The HTML workbench only presents these judgments and is never
their authority.

The exact Paper Run contract lives in
`../../../../discovery/haipipe-discovery/ref/paper-run-contract.md`.

## Legal writers

```text
ordinary refresh        subset trusted seed entries; rebuild workbench
ordinary human entry    land a person-supplied complete entry verbatim
Discovery Result        copy one authoritative entry into the Result Bib
Discovery build-bib     validate/union Result Bibs; rebuild derived Page Bib
human verification      record the judgment beside the owning primary authority
```

The Discovery builder is deterministic code, not citation authoring.

## Surface and gate

The 📚 Citations segment renders one row per entry with status, DOI/URL/Scholar
links, verification controls, and the owning Result link in Discovery mode.
Deterministic validation proves shape and identity consistency; `verified`
remains a person's judgment. Discovery reads it from
`runtime.yaml#bib.verification`; ordinary Pages read the owning CITE gate.

During category-folder migration, a legacy flat `bibex/` lane and
`outline/evidence/bibex/` are the same logical citation storage lane.
