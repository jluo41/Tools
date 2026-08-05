haipipe-board-page-for-venue · Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.1.2 - 2026-08-04

- Moved under `page-types/` with the other stable Page Type variants.
- Separates the venue Page's persistent structure from its current DRAFT, PROBE, REVISE, or CHECK authority.

## 0.1.1 - 2026-08-03

**Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.

- **The section index contradicted itself eight lines apart.** `:149` ruled the index counts from ZERO so it lines up with `S-Main-<n>`; `:157` then said "the venue index counts from 1", which is the superseded rule left standing. A writer reaching `:157` first numbered every division wrong.
- The 0.1.0 changelog entry taught that same abandoned 1-based form, in the same folder at the same version, so the reader who checked the history was the one who got misled. Corrected.
- Drops "the seven sections" from the base description.

## 0.1.1 - 2026-08-03

Written from the fan-out: fourteen agents took this contract to fourteen desks the same day it shipped, and every item below is something a real desk broke rather than something anyone predicted. That is the point of releasing a contract and then running it at scale immediately.

- **🧮 Add the pack's parts up against the desk's total.** Now a required row in `Venue-Structure`, because it went 3 for 3 the first time anyone checked: JAMA IM 3,350 against 3,000, PNAS ~6,970 against ~4,000, Diabetes Care 3,950 against 4,000, and JAMA where an RCT at the pack's floor lands within 50 words of the cap. The arithmetic is systematic: a pack measures published papers section by section, and a published page is not a submission budget, so the parts were never fitted to the whole.
- **⏳ A binding rule has a WHEN.** Nature Communications is format-free at first submission and enforces its caps at revision; every Nature-family APC bites at acceptance, and npj's waiver must be requested at submission anyway. A binding row now carries at-submission, at-revision or at-acceptance.
- **🔢 `Sec-<n>` = `S-Main-<n>` is a property, not a law, and the resolver wins when they part.** Five Nature-family desks print Methods last and PNAS reads Significance first, none of which `section-kinds.yml` orders that way. The fan-out split 2-2 on which side the index should follow; ruled for the resolver, because the index exists to JOIN the S page and an index tracking the desk stops being a join key the moment the two differ.
- **🚨 The desk's section list can be longer than the resolver's, and the gap is a finding.** MISQ expects Concluding Remarks, Management Science requires a 250-word nontechnical executive summary, JAMA Network Open publishes a Research Letter: none is a declared kind, and a draft built from the resolver alone reaches the portal with a required field empty.
- **🏛 A whole section on non-journal targets**, from `QBv15-grant` and `QBv16-patent`: no resolver means no `Sec-<n>`, one target can be many desks (8 agencies, 3 patent offices), `PACK OBSERVATION` is empty where a pack holds zero funded proposals, and a non-journal rule carries its CYCLE and not just its read date. Also that the unfixable step is choosing the agency, or what the specification failed to disclose, rather than a page count.
- **🕶 Same-family rules are not the same desk's rules.** Nature Medicine's page carries neither superscript numbering, nor the et-al threshold, nor double spacing; those are *Nature*'s. A sibling rule inherited by proximity is the mirror of the pack-versus-desk error, one level in.
- **📌 nature.com does not 403.** It 303s to its SSO host and WebFetch refuses the cross-host hop; `curl -L` with a cookie jar and a desktop UA returns 200. Four Nature pages were read live because one agent worked that out. INFORMS, PNAS and ADA genuinely do 403, and Wayback snapshots of the desk's OWN url are the next-best read, stamped as such.
- **⚔️ Desks contradict THEMSELVES, and the page prints both.** ISR on anonymity and on its open-access fee, Management Science on single-blind against double-anonymous, JAMA on a 400-word against a 300-word Narrative Review abstract, Nature Communications on three separate pairs, Nature Medicine and NMI on Extended Data figures against items.

## 0.1.0 - 2026-08-03

First release. JL ruled `QBv1-misq.md` the template for the other fifteen venue pages, then asked for the rule to be written down as a skill rather than left as one page other pages are told to copy. Everything here was established on that page the same day and is lifted, not invented.

- **📖 The governing principle: a venue page is a reference, not a rulebook** (JL 260803). Almost everything on it is a measurement of what published papers did, and departing from it is a choice rather than a violation; only the desk's own published rules bind. Found through a real misreading: `QBv1` printed "120-160 words, do NOT exceed ~185" for the abstract, which is the pack's measurement of eight papers, where the desk publishes no abstract cap at all. JL ruled ~250 words fine. Every length now says whose it is, and the pack's refusals are written as the pack's.
- **🏛 The variant's reason: a venue page settles nothing.** Its subject is a desk outside the repo that publishes its own rules and rejects papers that ignore them. Three consequences drive every rule in the file: the subject is external, so facts carry provenance; there are two sources, so one has to outrank the other; and a paper is built from the page, so it owes structure and mechanics rather than taste alone.
- **⚔️ The two-source rule, and the disagreement is the asset.** The pack (`paper/venue/playbook-*/`, its own repository, READ and never written) against the desk's own published instructions. The desk wins, and the gap is written down on the page naming both readings. `QBv1` carries three: the pack's observed "40-50 published pages" against the desk's 55-page submission ceiling, no reference style recorded where the desk requires APA 7th, and none of the submission mechanics recorded at all.
- **📌 Provenance records HOW a fact was read, not just when.** Added after `misq.umn.edu` answered a direct fetch with HTTP 403 on 260803, one day after the same pages had been fetched successfully. A fact re-checked through search summaries is weaker than a fetched one and now says so on the page.
- **🖼 Three figures, in a fixed order.** Desk taste (would this desk look at my paper), Venue-Structure (what am I writing), Submission-Rules (what the portal demands). Figures ② and ③ were written on 260803 at JL's request; ① already existed on every outlet page.
- **🔗 Links are embedded twice on purpose.** Verified against `src/body.py`: a fenced block is rendered with `esc()` plus the figure linker and never the inline markdown pass, so a URL inside a figure is plain text. Bare hosts go in the figure, real markdown links go directly under it. Also records that a bare URL alone on a line in `## Diagram` is the Excalidraw canvas slot.
- **🔢 The section index rule** (JL 260803, "I want to see the index"): `### 4 · Sec-0-Abstract: ...`, with the Aims and States groups repeating the name behind their emoji. A section carries three numbers that disagree on purpose (venue index from 0, so it lines up with `S-Main-<n>`; Content division counting the judgment divisions, `S-Main-<n>` from 0), so `Venue-Structure` prints all three rather than making a reader work it out.
- **📋 This contract is filed under Contracts, not Engines** (JL 260803 asked which). The base menu's split decides it: an Engine is run and opened to change behavior, a Contract carries a rule to other pages, and a loadable spec that never executes is the second. The reference page lists this file, this file names that page, and a rule changed in one is changed in the other in the same pass.
- **📎 Two Files groups this kind adds**: `🔗 Authority`, what the desk itself publishes, and `📤 Generated`, what a tool writes between markers. Both state an action, which is the base's test for a group name. Recorded after `QBv1`'s Files section was found flat, against `QB4-overall.md` §6's action menu.
- **🎯 States the NON-override explicitly.** Unlike `haipipe-board-page-for-skill`, this variant keeps the base's Aim ids, `Done when`, and one State row per Aim. Said out loud because a reader arriving from the roster variant would otherwise assume every variant drops them.
- **❓ An unfillable slot is printed, never deleted.** `not recorded by the pack` is a finding; a missing row is a silent gap. Applies to the format-values fences and to `Submission-Rules`, which carries an open `NOT ON RECORD YET` row.
