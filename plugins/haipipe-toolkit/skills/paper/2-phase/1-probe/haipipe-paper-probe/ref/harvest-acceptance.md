Citation harvest acceptance (haipipe-paper-probe, TRANSLATE step)
===================================================================

Loaded on demand when a dispatch return carries a `pick_list`. Every rule here
was added after a live failure -- keep the greps LITERAL.

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
- **no bibtex**: `grep -c '@'` == 0 on the new cards.
- **no tables**: `grep -c '^|'` == 0 on _CITATION_ (JL standing rule --
  bullet lines only, one per source).

One reject -> re-dispatch the harvest subagent with the defect list (one
retry); still failing -> mark the PP card `status: read (harvest DEFECTIVE)`
and surface it in the stage reply.
