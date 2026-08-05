---
# CONTRACT — machine-readable. No `name:` field: this is DATA the router reads,
# not a registered skill.
key: venue
order: "2a"
title: Venue
one_line: "Which venue does this paper target, and what does that venue REQUIRE of it?"
board_family: Open
board_unit: "Venue"
board_slug: venue          # family + unit + slug resolve the S-face filename;
                          # haipipe-board/stage.py owns that resolution (QB4@paper)

phases: [draft, probe, check]
                          # THREE phases — no REVISE. Venue produces a CONTRACT (a scored
                          # decision + a transcribed blueprint), not prose, so there is
                          # nothing for REVISE to polish. But it DOES run PROBE: it raises
                          # `## Q-Venue-<n>` questions (recent-publications, editor and
                          # competing-paper checks) as real nested S03/S04 entries, and
                          # template.md states "Answer: empty in DRAFT — PROBE
                          # fills it: the finding + [source: PP<nn>]".
                          # The invariant is only that `phases` ends with `check`.
gates: [check]             # THE HUMAN GATES THIS STAGE OPENS, declared like `phases:`.
                           # Default is ONE, at CHECK. DRAFT/PROBE/REVISE run unattended.
                           # This is safe only because PROBE cannot spend: see probe_depth.
probe_depth: 0             # THE CEILING on what PROBE may dispatch, on the bank's own ladder
                           # (task/haipipe-task/fn/qa.md:102-107), which maps 1:1 onto the
                           # consumer's `bank:` verdict:
                           #   0 READ        reuse  results already answer it   free, nothing runs
                           #   1 NEW RUN     run    old script, new config      costs
                           #   2 NEW SCRIPT  code   must write new code         costs
                           #   3 NEW FOLDER  new    open a new task-folder      costs most
                           # Rule: dispatch when depth(bank) <= probe_depth, else DEFER.
                           # At 0 the stage can only HARVEST, so a run of it is free and needs
                           # no gate. Raise it per invocation with `probe --depth N`.
runs: once
needs_paper: false        # a bare free-text topic/abstract is a valid input; no folder needed
on_rerun: diff-and-ask   # QB2c, ruled 260727. Protected on a re-run: any `> <ACTOR>:`
                         # lane, `state:`, `## States`, a settled State row, a GATE row in
                         # `## Log`. Everything else: compute the change, SHOW it, ask.
                         # Never silently overwrite. Full rule: ../CONTRACT.md.
venue_role: chooser       # NEITHER venue_free NOR venue_aligned: this is the stage that PICKS
                          # the venue, so the axis every other stage sits on is the thing this
                          # one produces. Declared rather than left blank, so a missing
                          # venue_free/venue_aligned stays a real failure everywhere else.
                          # (with no folder, run --no-pin: there is nothing to write into)

modes:
  default:    "recommend a ranked shortlist; at CHECK ask before changing the S-page `state:` line to `✅ PINNED · <venue> <year>`"
  "--no-pin": "advise only — recommend and STOP; write no file at all
               (for 'just tell me which journal', or a bare topic with no paper folder)"
  refresh:    "re-derive ONLY — keep the existing pin, re-transcribe Structural Blueprint +
               Writing Principles from current pack state, update the provenance header
               (new venue commit + derived date), log the delta. Never re-opens the choice."

artifact: 0-lifecycle/S01-opening/S-Open-Venue.md
artifact_fallback: 0-lifecycle/S01-opening/2a-venue.md
                          # papers that predate the 2026-07-25 S-face restructure carry
                          # the stage file under its old name. Use this ONLY when the
                          # resolved S face is absent, and say which one you used.
probes: 0-lifecycle/S03-literature/probes/L<n>-<topic>/ | 0-lifecycle/S04-value/probes/V<n>-<topic>/
checker: paper/haipipe-paper/probe/check-probe-cards.sh --stage venue
                          # run by CHECK before judging; path relative to the skills root
pins: 0-lifecycle/S01-opening/S-Open-Venue.md   # the pin lives on THIS stage's own S page, in its
                           # on its `state:` line: `state: ✅ PINNED · <venue> <year>`. NOT a
                           # `venue:` frontmatter key — the board's face grammar is a CLOSED
                           # whitelist (haipipe-board src/parse.py) and would not parse one.
                           # The pack slug + outlet dir go in the body's provenance header.
                           # Every reader that used to grep STATUS.md reads it here. One page owns the
                           # venue contract; a second copy could only disagree with it.
template: template.md

packs: ../../venue/        # the venue knowledge directory: playbook-*/README.md (`-> Claims`
                           # rewards), <journal>/taste.md (desk signals), <journal>/<journal>-
                           # <section>/style.md (Micro-norms), <journal>/examples/.
                           # READ BY ~13 SKILLS and NOT owned by this stage. This stage is the
                           # READER that turns a pack into a pinned contract; it NEVER edits a pack.

exit_when: "no clear fit; venue change re-runs pitch"

sections:                  # logical order; Q-consumer adapts to Board Aims
  - Venue Decision         #   (a provenance header sits above them: pack @ commit, outlet dir)
  - Relevant Files
  - Section Styles         #   the RESOLVED per-kind pack paths (style + template) — see owns_resolution
  - <one per section>      #   JL 260802 ruled B: ONE `###` division per manuscript section
                           #   (opening = title + abstract, introduction, methods, results…),
                           #   the list taken from this outlet's kinds, never fixed here
  - Writing Principles     #   the one cross-section division, prose companion to the above
  - Q-consumer

owns_resolution: |         # THIS stage resolves, ONCE, what every downstream stage would
                           # otherwise re-derive per section:
  · venue label -> pack slug         (the map in the craft body)
  · pack + outlet -> section styles + templates  (the Section Styles table in the artifact)
  Each kind row resolves TWO pack paths by parallel globs: `*-<kind>/style.md` (how it reads,
  reference) and `*-<kind>/template.md` (the skeleton section-edit drafts into, authored from
  this outlet's exemplars — the PRINCIPLE, see ../../haipipe-paper/stages/section-kinds.yml). Both, or an explicit
  `style: — blueprint-only` / `template: — generic-fallback` per missing file, so a missing
  pack file is distinguishable from an unchecked one.
  Downstream NEVER globs, finds, or spells a pack path. section-edit reads its row and stops.
  The kind vocabulary and which kinds each outlet actually has: ../../haipipe-paper/stages/section-kinds.yml
  Resolution is a GLOB (`*-<kind>`), never concatenation — the per-journal slug is arbitrary
  and sometimes multi-token (jno- · diabcare- · npjdm- · MS-IS-); concatenation works for
  MISQ and fails on six other outlets.
kinds_file: ../../haipipe-paper/stages/section-kinds.yml

formatting:
  title_rule: "====="
  section_rule: "-----"
  headings: "direct `###` divisions under Board Content; Q-consumer records are Aim records
             under `## Aims`, never Content headings"
  line_breaks: "one sentence per line (semantic line breaks); no dense paragraphs"
  fit_record: "the Venue Decision's Fit is RECORD LINES, never a pipe table"

q_id_pattern: "- P<n> · Q-Venue-<n> · <title>"
q_anchor: "[Q-Venue-<n>] cited inline in the Venue Decision sentence it rests on"
closed_when: "PROBE writes the finding + [source: <nested-entry>] into the Answer field. That is where
              the loop closes for this stage — there is no REVISE to weave it back into prose,
              because the artifact is a contract, not prose. A landed Answer that changes the
              pick re-opens DRAFT rather than being woven in."

dispatch_scope:            # venue questions are concrete LOOKUPS, never 'is this a good fit?'
  - recent-publications    # has this outlet run near-identical papers lately?
  - editor-and-competition # who handles this at the outlet; what competing papers are in flight

done_criteria:
  - "outlet named on S-Venue-0-venue.md's `state:` line (skipped under --no-pin, which writes nothing anywhere)"
  - "provenance header records pack slug @ venue commit + outlet dir"
  - "Venue Decision carries the pick, 1-2 backups, the nearest rejected + its hard disqualifier,
     the outlet's one-sentence desk test + this paper's answer, and desk-reject risks"
  - "Fit record-lines map H/claims to the venue reward each satisfies (no pipe table)"
  - "Structural Blueprint filled per section: subsections, paragraphs, sentences/paragraph,
     sentence length, citation density, results reported, display units — each [source: ...]-tagged"
  - "blueprint adapted to THIS paper's claim structure (H1/H2/H3 mapped to sections/subsections)"
  - "Writing Principles filled: tone, citation style, results presentation, display limits, abstract"
  - "Section Styles carries ONE record line per kind (kinds from ../../haipipe-paper/stages/section-kinds.yml), each line
     giving BOTH its resolved style: path and its resolved template: path — or an explicit
     `style: — blueprint-only` / `template: — generic-fallback` when the pack lacks that file, so
     'no pack file' is distinguishable from 'not checked'"
  - "at least one Q-Venue-<n> raised (the recent-publications check), and every raised Q has a real probe entry; above-ceiling work is a `deferred` entry with `**deferred**: depth-<n> · <reason>`"
  - "every <!-- RULE --> comment deleted from the filled S-Venue-0-venue.md"

upstream: [claims]         # reads Board S pages in 0-lifecycle/{0-seed,1-work} when they exist;
                           # a bare topic has none and the profile is built from the text
downstream: [pitch]
consumed_by: [pitch, narrative, display, section-edit, revise, revise-results, revise-humanizer]
                           # the venue-ALIGNED readers. S-Venue-0-venue.md is their single consumption
                           # point; the packs are a FALLBACK only when S-Venue-0-venue.md is absent.
handoff: "on CHECK confirm, write the pinned outlet onto S-Venue-0-venue.md's `state:` line
          and append the gate row to its ## Log -> pitch, which re-runs its [primary] designation,
          RQ framing, and Editor's Chair Test for this venue"
---

Venue — the craft
=================

Venue selection is the FIRST venue-coupled design decision. Seed, resource, and claims are
venue-FREE — what a paper NEEDS to exist does not depend on where you send it — and everything
after couples. So this stage answers one question in two halves: **which venue**, and **what does
that venue REQUIRE of the final paper**. The second half is the half that outlives the decision.

Profile first, packs second
---------------------------

Do not open a pack until the paper has a CONTRIBUTION PROFILE: the central contribution, the
method, the topic/domain, the evidence strength, the intended audience. From seed/claims when they
exist, from the topic text when they do not. If any of the five is unclear, ask ONE round of
questions before scoring — a profile guessed wrong makes every score downstream of it wrong too.

Then read what each pack REWARDS
--------------------------------

A pack's `README.md` carries a `-> Claims` mapping: what that venue rewards, and what it treats as
a mere enabler. That mapping — not the venue's prestige — is what the profile is matched against.

Packs are FAMILY-granular; the concrete outlet is a delta inside the family, chosen by reading each
candidate's `<journal>/taste.md` — desk-accept signals, desk-reject signals, and the one-sentence
test. A paper that passes the family and fails that test has not found its venue yet.

```text
MISQ / ISR / MS-IS / MS-Marketing              -> playbook-utd-is
NMI / Nat Comms / Nat Med / npj DM / NHB       -> playbook-nature-portfolio
PNAS                                           -> playbook-pnas
JAMA / JAMA Intern Med / JAMA Netw Open        -> playbook-jama-portfolio
Diabetes Care (specialty clinical)             -> playbook-medical-journals
grant (NSF / NSFC / KAKENHI / ERC …)           -> playbook-grant
patent (CNIPA / USPTO / EPO)                   -> playbook-patent
```

This stage OWNS that map — every other stage resolves the pinned outlet through this S page.
Write the pack slug and outlet directory in the page body's provenance header.
A named venue with no pack (NEJM, Lancet, ICLR, NeurIPS…) remains an honest
formatting target recorded in that body: say no pack exists, and let pack-specific
lifecycle wiring no-op.

Score five dimensions, High/Med/Low, one line each
--------------------------------------------------

```text
🎯 contribution-type   does the paper's strongest claim match what this venue rewards?
🔬 method              is this design one the venue publishes?
🗺  topic/domain       is the subject inside its scope?
📏 evidence-bar        does the evidence clear the bar this venue holds?
👥 audience            do the people who read it do something with it?
```

The one-line reason is not decoration — it is what makes the ranking auditable later. Record any
HARD DISQUALIFIER separately (e.g. "design science -> not ISR"); it kills a venue regardless of how
the five dimensions scored. Shortlist the top 3, each with a fit rationale, what to emphasize
there, and the main why-not. The PRIMARY is the one whose rewards the paper's strongest claim most
directly satisfies.

Transcribe the requirements; never invent them
----------------------------------------------

The blueprint is the stage's real product, and it is built by TRANSCRIPTION in this order:

```text
1  <journal>/<journal>-<section>/style.md   word budget, arc, paragraph-structure table, and the
                                            measured `## Micro-norms` block — copy these across;
                                            do not re-mine what is already measured
2  <journal>/taste.md + pack style-profile.md   the Writing Principles side
3  ONLY if a section guide is missing       count 2-3 stored exemplars in <journal>/examples/
                                            yourself; search published papers as a last resort
4  adapt to THIS paper                      H1/H2/H3 mapped onto named sections/subsections
```

Where a Micro-norms block flags a measured-vs-budget clash or a "to verify" marker, CARRY THE
CAVEAT rather than silently picking one number. Hard caps (word limits, display limits) stay caps
even when exemplars deviate from them.

The test of a finished blueprint is whether section-edit can use it without guessing:
"Introduction has 4 subsections, each 2 paragraphs, each 5-6 sentences" — not "well-structured".
The blueprint says HOW MANY sentences; Writing Principles says HOW TO WRITE them. The provenance
header exists so staleness is DETECTABLE: if `venue/` has moved past the recorded commit, run
`refresh` to re-derive without touching the pin.

The pin is a gate, not a side effect
------------------------------------

At CHECK, ask before changing the S page's `state:` line to
`✅ PINNED · <venue> <year>`, and ask again before overwriting an existing pin.
A venue change is not a metadata edit: it re-runs pitch's [primary] designation
and RQ framing, and reshapes narrative, displays, section-edit, and prose.
Claims does not move — it is venue-free.

Not from the venue
------------------

This stage recommends and pins. It does not write claims, pitch, or prose, and it never edits a
venue pack. Under `--no-pin` it writes nothing at all — recommend, stop, and offer to scaffold a
folder if the user then wants one.
