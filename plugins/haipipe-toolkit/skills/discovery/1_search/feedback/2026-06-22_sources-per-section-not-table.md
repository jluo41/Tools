---
status: fixed
created: 2026-06-22
updated: 2026-07-03
occurrences: 2
context: search stage / sources.md layout
fixed_in: "2.4.0"
---

Reporter (JL): 这个source 可以让他一个source 一个section吗，不要放到一个大表里，一点都不好读
(re: discoveries/L01_personality-prescribing-landscape/01_trait-via-risk-attitude/sources.md)

The search-stage `sources.md` currently renders every citation as ONE wide
markdown table (`| id | citation/URL | role | verification |`). JL finds it
unreadable — long citations wrap badly inside narrow table cells and you cannot
scan one source at a glance. JL wants ONE SOURCE = ONE SECTION instead.

This is the same readability complaint as the probe dense-table feedback: big
tables of long-text content read as a wall.

Fix:
- Change the `sources.md` skeleton (and any search-stage template / Review
  Output Contract example) so each source is its own block:
    ### S0xx — <short descriptor>
    - Citation: <full citation>
    - URL: <locator>
    - Role: <role>   ·   Verification: VERIFIED | NEEDS-VERIFICATION
  optionally grouped under `## <cluster/theme>` headers.
- Reserve tables for short-field summaries (e.g. the group _index roll-up),
  not for per-source full citations.
- Decide in a revision pass; also retro-apply to existing sources.md files.

## Recurrences
- 2026-07-03: (JL, inline in ref/discovery-yaml-schema.md after the v2.4 rewrite reintroduced the table template) "new have this. I prefer to have a paper for one single paragraph or subsection, never never use the table to group the papers or the sources together, it is not for the human to read, get it?????"

Fix: v2.4.0 — sources.md template is now ONE SOURCE = ONE SUBSECTION (`###` heading carrying the full paper title, bullet fields, Scholar link), and the same never-a-table rule is applied across the layer: arxiv / semantic-scholar / exa-search / deepxiv result presentation, comm-lit-review literature output, novelty-check Closest Prior Work. Existing sources.md files retro-apply on next edit.
