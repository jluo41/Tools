Harvest acceptance (haipipe-application-probe, INTERPRET step) -- venue-scaled lanes
=====================================================================================

Loaded when an answering QA file carries harvestable content (value anchors, source anchors, or display unit refs) for a lane the pinned venue fires (`values:` always; `sources:` sectioned venues only; `displays:` display-unit venues only -- see SKILL.md "Venue-hook contract"). Every rule here was added after a live failure -- keep the greps LITERAL.

The harvest reads the ANSWER, not the bank
-------------------------------------------

A harvest hook follows the anchors the QA file names (`[→ results/<file>]`, `[→ sources.md#S02]`) and transcribes what they point at. It does NOT search, does NOT sweep, does NOT open the task-folder and go looking. Finding is the EXECUTOR's job, and it is reached by DISPATCH, never by reading around.

```
   QA/<n>-<slug>.md   ## Answer   ... [→ results/summary.csv]  [→ sources.md#S02]
                                        │                        │
                        the ONLY things a hook may follow  ──────┘
```

Lane protocol (identical for all lanes)
-----------------------------------------

1. INTERPRET writes the lane line into the SECTION first: `- values: ... · harvest: OWED` / `- sources: ... · harvest: OWED` / `- displays: ... · harvest: OWED`. The debt exists on disk before any harvest runs -- `check-probe-cards.sh` FAILs an OWED line, so a skipped harvest can never pass VERIFY or the CHECK gate.
2. Dispatch the lane's harvester hook as a subagent (cheapest tier). Application has NO probe sub-worker skills: the dispatch prompt binds the subagent to the paper family's sub-worker contract -- pointer-following only, no search (no WebSearch, no Semantic Scholar), transcribe ONLY what the QA file's anchors name. For the citation lane, point the subagent at the `_CITATION_` card format spec in `../../../../../paper/2-phase/1-probe/haipipe-paper-probe-citation/SKILL.md` (single source of truth; the doc shape is family-shared, application adds no fork). NEVER paraphrase a spec into the prompt -- spec-drift by telephone game is the named paper-side failure mode.
3. Run the lane's mechanical acceptance below. One reject -> re-dispatch ONE TIER UP with the defect list (one retry); still failing -> mark the section `state: read (harvest DEFECTIVE)` and surface it in the stage reply.
4. On acceptance flip the lane line: `harvest: accepted (<n> entries, <doc>)`.

(NOTE: "card" below refers ONLY to a `_CITATION_` entry -- the citation doc's own unit, which keeps its name. A probe file holds SECTIONS, never cards.)

Values lane acceptance (values: -> _VALUES_{stage}.md; ALWAYS eligible)
-------------------------------------------------------------------------

- **count**: new `### ` entry headings == numbers named in the QA file's Answer.
- **source**: every entry names a source path under `tasks/` (or a display CSV); `ls <project_root>/<path>` resolves for each.
- **number-matches-source**: for each entry, the literal value string greps in its named source file (`grep -F '<value>' <source>`) -- a value with no source hit is a REJECT (fabrication guard; the parquet/script decides, never the prose).
- **no tables**: `grep -c '^|'` == 0 on the new entries.

Display lane acceptance (displays: -> _DISPLAY_{stage}.md + artifact links; display-unit venues only)
-------------------------------------------------------------------------------------------------------

- **count**: new registry entries == units named in the QA file.
- **paths**: every entry's unit path exists on disk (`ls`), and any artifact link added (markdown image/link in `0-artifacts/` or a section file) points at that existing path.
- **need-linkage**: every entry names the question/claim it serves -- an orphan unit entry is a REJECT.

Citation lane acceptance (sources: -> _CITATION_{stage}.md; sectioned venues only)
------------------------------------------------------------------------------------

Mechanical acceptance -- RUN the commands, never eyeball (paper run-3: acceptance claimed "each has anchor + finding" while `grep -c 'finding:'` returned 0).

- **count**: new `^### ` card headings == the number of source anchors named.
- **identity**: every new card block greps an identity bullet -- a `^- ` line containing a `(YYYY)` year (authors (year). venue · id). Title-only cards are REJECTS.
- **fields**: every new card block greps a `- summary:` AND a `- finding:` line.
- **provenance**: a card whose S## is VERIFIED in `sources.md` must say `VERIFIED-by-discovery` on its status line (plus 🔍 for the human verification pass, which never auto-clears). The grep is LITERAL: `grep -c 'VERIFIED-by-discovery'` == the discovery-verified count. Semantically-equivalent wording is a REJECT -- meaning-judgment is exactly what mechanical acceptance exists to remove.
- **anchors**: every new card's `source_ref` names a `sources.md` + S##; grep that S## heading in that file -- it must EXIST. An unresolvable anchor is a REJECT, not a warning.
- **no bibtex**: no bibtex ENTRY on the new cards -- `grep -cE '@(article|inproceedings|book|misc|incollection|techreport|phdthesis|conference|proceedings)\{'` == 0. (A bare `@` is NOT bibtex: venue names carry it, e.g. `KHD@IJCAI workshop`; anchor to the entry-type-plus-brace pattern.)
- **no tables**: `grep -c '^|'` == 0 on `_CITATION_` (JL standing rule -- bullet lines only, one per source).

One reject -> re-dispatch the harvest subagent with the defect list (one retry); still failing -> mark the section `state: read (harvest DEFECTIVE)` and surface it in the stage reply.

What a hook may NEVER do
-------------------------

- Write anything under `tasks/` or `discoveries/`. The probe layer CAUSES bank files; the EXECUTOR authors them (CC-8). A hook that "just adds a note" to a leaf has broken LAW 1.
- Search. If an anchor is missing, that is a REJECT and (if the content is genuinely needed) a NEW question -- a new section, a new commission, a new dispatch. It is never a quick lookup.
- Generate bibtex, or touch a `.bib`.
