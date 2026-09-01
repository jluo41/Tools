---
name: haipipe-plugin-bibex
description: >-
  Bibex plugin for a Board Page: owns the citation workbench and two lawful
  authority modes. A normal Page owns a primary Page Bib; a
  Discovery Topic derives that Page Bib by validating and unioning the
  exactly-one-entry Bib owned by each completed Paper Result. BibTeX may be
  copied/subset/deduplicated but never composed from model memory. Trigger:
  bibex plugin, page bib, Discovery evidence bib, aggregate result bibs,
  citation workbench, verify citation, /haipipe-plugin-bibex.
metadata:
  version: "0.2.0"
  last_updated: "2026-09-01"
---

# /haipipe-plugin-bibex · citation authority without composition

LOAD haipipe-plugin first. It owns plugin storage, surface, writer, and
boundary. This file owns Bibex's delta.

## One law

A machine may copy a BibTeX entry verbatim from a trusted publisher/index or a
person, subset existing entries, validate them, deduplicate exact entries, and
stable-sort them. It MUST NOT invent or complete title, author, venue, year,
pages, DOI, or key from model memory.

A person supplying citation metadata is not the same as supplying a BibTeX
entry. Formatting fields into BibTeX is composition; only a complete supplied
entry may land through the person route.

## Authority mode A · ordinary Page

~~~text
<page>/evidence/bibex/
├── <stem>.bib           PRIMARY · the Page's own person/workflow material
└── <stem>-bib.html      DERIVED · citation workbench
~~~

Refresh may subset entries from a trusted seed Bib. A person-supplied entry may
land verbatim. The workbench regenerates freely.

## Authority mode B · Discovery Topic aggregate

~~~text
<topic>/results/<RUNNAME>/<RUNNAME>.bib   PRIMARY · one verified Subject entry
                 │
                 ├── validate complete Result
                 ├── reject key/DOI conflicts
                 ├── deduplicate exact entries
                 └── stable key sort
                 ▼
<topic>/evidence/bibex/<topic>.bib        DERIVED · Page Evidence Bib
<topic>/evidence/bibex/<topic>-bib.html   DERIVED · citation workbench
~~~

The workflow phase selects this mode because the Folder is a Discovery Topic;
there is no separate configuration-folder skill. The exact Run/Result contract
lives in haipipe-discovery/ref/paper-run-contract.md.

Only Results whose runtime says status: complete enter the union. Every source
Result Bib contains exactly one entry, and its key equals the Result Card's
cite: @Key. Blocked, unresolved, planned, running, and superseded Results are
excluded.

The derived Topic Bib is never the correction target. Verification or metadata
repair lands in the owning Result Bib first, then the aggregate and workbench
are rebuilt. If two Results disagree on a key or DOI, aggregation hard-fails
instead of choosing silently.

## Writers

~~~text
ordinary refresh        subset trusted seed entries; rebuild workbench
ordinary human entry    land person-supplied entry verbatim
Discovery Result        copy one authoritative entry into the Result Bib
Discovery build-bib     validate/union Result Bibs; rebuild derived Page Bib
human verification      record the person's verification at the owning primary
~~~

The Discovery builder is deterministic code, not citation authoring.

## Surface

The citation workbench renders one row per entry with status, DOI/URL/Scholar
links, verification controls, and the owning Result link in Discovery mode.
Verification marks remain a person's judgment; deterministic validation proves
shape and identity consistency, not scholarly correctness.

## Files

- haipipe-board/live/export.py — ordinary Page routes and workbench builder.
- haipipe-discovery/scripts/paper_runs.py — Discovery validator/aggregate
  builder.
- haipipe-plugin/ref/roster.md — plugin roster row.

During category-folder migration, a legacy flat bibex lane and
evidence/bibex/ are the same logical lane.
