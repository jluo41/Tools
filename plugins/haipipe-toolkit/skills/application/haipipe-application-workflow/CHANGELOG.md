# haipipe-application-workflow · version history

0.1.0 · 260823 · JL
- New skill, split out as the Application family's RUN head, mirroring the page family's "one folder, one head skill" pattern (haipipe-page-workflow).
- Six phases in two lanes: InsightBoard SCOPE/CLIMB/HANDOFF, DesignBoard FRAME/COMPOSE/ACCEPT, joined only at the PageX crossing.
- Three human gates, always blocking: probe release (per page, inside CLIMB), handoff signing, acceptance.
- Phase state derived from disk, shared with haipipe-application's Status verb; no status file.
- Partition-major climb order: F template first, partition groups in parallel, X group, then W pages citing the verdict.
- One-line run receipt at <application-root>/_runs/application/log.md; page receipts stay the detailed record.
