Harvest acceptance (haipipe-application-probe, ⑤ INTERPRET) -- venue-scaled lanes
==================================================================================

Loaded when an answering QA file carries harvestable content (value anchors, source anchors, or display unit links) for a lane the pinned venue fires (_VALUES_ always; _CITATION_ sectioned venues only; _DISPLAY_ display-unit venues only -- see SKILL.md "Venue-hook contract"). Adapted from paper's harvest-acceptance.md; every rule there was added after a live failure -- keep the greps LITERAL.

Lane protocol (identical for all lanes; JL 2026-07-07 harvester ruling)
------------------------------------------------------------------------

1. ⑤ INTERPRET writes the lane line into the probe SECTION FIRST: `- values: <path> · harvest: OWED` / `- sources: S01,S02 · harvest: OWED` / `- displays: <unit> · harvest: OWED`. The debt exists on disk before any harvest runs -- check-probe-cards.sh FAILs an OWED line, so a skipped harvest can never pass VERIFY or the CHECK gate.
2. Dispatch the lane's harvester hook as a subagent (cheapest tier). Application has NO sub-worker skills: the dispatch prompt binds the subagent to paper's sub-worker contract -- pointer-following only, no search (no WebSearch, no Semantic Scholar; finding is the bank's monopoly), transcribe ONLY what the return's pointers name. For the citation lane, point the subagent at the _CITATION_ card format spec in `../../../../../paper/2-phase/1-probe/haipipe-paper-probe-citation/SKILL.md` (single source of truth; the card shape is family-shared, application adds no fork). NEVER paraphrase a spec into the prompt -- spec-drift by telephone game is the named paper-side failure mode.
3. Run the lane's mechanical acceptance below. One reject -> re-dispatch ONE TIER UP with the defect list (one retry); still failing -> leave the section at `state: read` with `harvest: DEFECTIVE` and surface it in the stage reply.
4. On acceptance flip the lane line: `harvest: accepted (<n> entries, <doc>)`.

Values lane acceptance (the section's values: lane -> _VALUES_{stage}.md; ALWAYS eligible)
------------------------------------------------------------------------------------------

- **count**: new `### ` entry headings == numbers named in the return.
- **source**: every entry names a source path under tasks/ (or a display CSV); `ls <project_root>/<path>` resolves for each.
- **number-matches-source**: for each entry, the literal value string greps in its named source file (`grep -F '<value>' <source>`) -- a value with no source hit is a REJECT (fabrication guard; the parquet/script decides).
- **no tables**: `grep -c '^|'` == 0 on the new entries.

Display lane acceptance (the section's displays: lane -> _DISPLAY_{stage}.md + artifact links; display-unit venues only)
-----------------------------------------------------------------------------------------------------------------------

- **count**: new registry rows == units named in the return.
- **paths**: every row's unit path exists on disk (`ls`), and any artifact link added (markdown image/link in 0-artifacts/ or a section file) points at that existing path.
- **need-linkage**: every row names the need/claim it serves -- an orphan unit row is a REJECT.

Citation lane acceptance (the section's sources: lane -> _CITATION_{stage}.md; sectioned venues only)
------------------------------------------------------------------------------------------------------

Mechanical acceptance -- RUN the commands, never eyeball (paper run-3: acceptance claimed "each has anchor + finding" while `grep -c 'finding:'` returned 0).

- **count**: new `^### ` card headings == the sources named in the return.
- **identity**: every new card block greps an identity bullet -- a `^- ` line containing a `(YYYY)` year (authors (year). venue · id). Title-only cards are REJECTS.
- **fields**: every new card block greps a `- summary:` AND a `- finding:` line.
- **provenance**: a card whose S## is VERIFIED in sources.md must say `VERIFIED-by-discovery` on its status line (plus 🔍 for the human verification pass, which never auto-clears). The grep is LITERAL: `grep -c 'VERIFIED-by-discovery'` == discovery-verified pick count. Semantically-equivalent wording is a REJECT -- meaning-judgment is exactly what mechanical acceptance exists to remove. Canonical strings live in the paper citation skill's spec (VERBATIM rule there).
- **anchors**: every new card's `source_ref` names a sources.md + S##; grep that S## heading in that file -- it must EXIST (the agent's fresh evidence landed). An unresolvable anchor is a REJECT, not a warning.
- **no bibtex**: no bibtex ENTRY on the new cards -- `grep -cE '@(article|inproceedings|book|misc|incollection|techreport|phdthesis|conference|proceedings)\{'` == 0. (A bare `@` is NOT bibtex: venue names carry it, e.g. `KHD@IJCAI workshop`; anchor to the entry-type-plus-brace pattern.)
- **no tables**: `grep -c '^|'` == 0 on _CITATION_ (JL standing rule -- bullet lines only, one per source).

One reject -> re-dispatch the harvest subagent with the defect list (one retry); still failing -> leave the section at `state: read` with `harvest: DEFECTIVE` and surface it in the stage reply.
