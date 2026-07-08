Harvest acceptance (haipipe-paper-probe, TRANSLATE step) -- all three lanes
============================================================================

Loaded when a dispatch return carries harvestable content (a `pick_list`,
value refs, or display unit refs). Every rule here was added after a live
failure -- keep the greps LITERAL.

Lane protocol (identical for all three; JL 2026-07-07 harvester ruling)
------------------------------------------------------------------------

1. TRANSLATE writes the lane line into the PP card FIRST:
   `- pick_list: ... · harvest: OWED` / `- value_refs: ... · harvest: OWED`
   / `- unit_refs: ... · harvest: OWED`. The debt exists on disk before any
   harvest runs -- check-probe-cards.sh FAILs an OWED line, so a skipped
   harvest can never pass VERIFY or the CHECK gate.
2. Dispatch the lane's harvester subagent (cheapest tier; it READS its worker
   SKILL.md headless -- citation/values/display respectively; NEVER paraphrase
   the spec into the prompt).
3. Run the lane's mechanical acceptance below. One reject -> re-dispatch ONE
   TIER UP with the defect list (one retry); still failing -> mark the card
   `status: read (harvest DEFECTIVE)` and surface it in the stage reply.
4. On acceptance flip the card line: `harvest: accepted (<n> entries, <doc>)`.

Values lane acceptance (value_refs -> _VALUES_{stage}.md)
----------------------------------------------------------

- **count**: new `### ` entry headings == numbers named in the return.
- **source**: every entry names a source path under tasks/ (or a display CSV);
  `ls <project_root>/<path>` resolves for each.
- **number-matches-source**: for each entry, the literal value string greps in
  its named source file (`grep -F '<value>' <source>`) -- a value with no
  source hit is a REJECT (fabrication guard; the parquet/script decides).
- **no tables**: `grep -c '^|'` == 0 on the new entries.

Display lane acceptance (unit_refs -> _DISPLAY_{stage}.md + tex)
-----------------------------------------------------------------

- **count**: new registry rows == units named in the return.
- **paths**: every row's unit path exists on disk (`ls`), and any tex link
  added (`\input`/`\includegraphics`) points at that existing path.
- **need-linkage**: every row names the need/claim it serves -- an orphan unit
  row is a REJECT.

Citation lane -- dispatch + acceptance (the original, unchanged)
-----------------------------------------------------------------

Dispatch the harvest subagent
------------------------------
- Worker: `haipipe-paper-probe-citation` (harvest form), via Agent on the
  CHEAPEST model tier (`model: "haiku"`, effort low) -- harvest is pure
  transcription from sources.md; the mechanical acceptance below catches
  failures. If the one acceptance-reject retry is needed, re-dispatch ONE TIER
  UP instead of same-tier.
- The dispatch prompt tells the subagent to READ the card spec in that skill's
  SKILL.md -- NEVER paraphrase the spec into the prompt. A compressed
  re-enumeration is exactly how the identity bullet (authors/year/venue) got
  dropped in test-2-2222 (spec-drift by telephone game; the spec file is the
  single source of truth).
- The subagent expands the picked sources.md entries into `_CITATION_{stage}.md`
  cards in its own clean context. Produce and review are never the same context.

Mechanical acceptance -- RUN the commands, never eyeball
---------------------------------------------------------
(run-3 acceptance claimed "each has anchor + finding" while
`grep -c 'finding:'` returned 0.)

- **count**: new `^### ` card headings == pick_list length.
- **identity**: every new card block greps an identity bullet -- a `^- ` line
  containing a `(YYYY)` year (authors (year). venue · id). Title-only cards
  are REJECTS (test-2-2222: JL -- "title author 还有 venue 这些都没有呀").
- **fields**: every new card block greps a `- summary:` AND a `- finding:` line.
- **provenance**: a card whose S## is VERIFIED in sources.md must say
  `VERIFIED-by-discovery` on its status line (plus 🔍 for the human
  Scholar/bibtex pass, which never auto-clears). Bare "unverified" on a
  discovery-verified source is a REJECT -- it discards earned provenance.
  The grep is LITERAL: `grep -c 'VERIFIED-by-discovery'` == discovery-verified
  pick count. Semantically-equivalent wording (`retrieved ✅ (discovery, ...)`,
  `JL bibtex ⬜`) is a REJECT too -- test-123333333's harvest synonymized the
  canonical string and acceptance waved it through on "same meaning";
  meaning-judgment is exactly what mechanical acceptance exists to remove.
  Canonical strings live in the citation skill's spec (VERBATIM rule there).
- **anchors**: every new card's `source_ref` names a sources.md + S##; grep
  that S## heading in that file -- it must EXIST (the agent's fresh evidence
  landed). An unresolvable anchor is a REJECT, not a warning.
- **no bibtex**: no bibtex ENTRY on the new cards --
  `grep -cE '@(article|inproceedings|book|misc|incollection|techreport|phdthesis|conference|proceedings)\{'`
  == 0. (A bare `@` is NOT bibtex: venue names carry it, e.g. `KHD@IJCAI
  workshop` -- test-12334535 harvested a legit card with that venue and a bare
  `@` grep would false-reject it. Anchor to the entry-type-plus-brace pattern.)
- **no tables**: `grep -c '^|'` == 0 on _CITATION_ (JL standing rule --
  bullet lines only, one per source).

One reject -> re-dispatch the harvest subagent with the defect list (one
retry); still failing -> mark the PP card `status: read (harvest DEFECTIVE)`
and surface it in the stage reply.
