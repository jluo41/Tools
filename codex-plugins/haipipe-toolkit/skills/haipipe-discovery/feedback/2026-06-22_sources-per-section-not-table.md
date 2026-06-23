---
status: open
created: 2026-06-22
context: search stage / sources.md layout
fixed_in: ""
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
