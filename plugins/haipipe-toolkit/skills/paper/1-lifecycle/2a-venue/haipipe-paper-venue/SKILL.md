---
name: haipipe-paper-venue
description: "Recommend the best-fit venue for a paper or topic, then pin it. Produces 0-lifecycle/2a-venue/2a-venue.md with the venue decision, relevant files, and requirements (structural blueprint + writing principles: section structure, length norms, citation density, results conventions, display limits), plus a Q-consumer. Writes the choice into STATUS.md. This is the venue-first front door: run it before pitch (claims is venue-free). Trigger: venue, which journal, where to submit, venue fit, recommend journal, journal selection, pick venue, 投哪个期刊, 选刊, 期刊推荐, /haipipe-paper-venue."
argument-hint: "[paper-path | free-text topic/abstract] [--no-pin]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.4.1"
  last_updated: "2026-07-19"
  summary: "Venue stage orchestrator: recommends + pins the best-fit venue and produces 2a-venue.md (template ref/venue-template.md) -- the venue decision, relevant files, and requirements (structural blueprint transcribed from pack Micro-norms + writing principles), plus a Q-consumer. 2a-venue.md is the single consumption point for the venue-ALIGNED stages (pitch, narrative, display, section-edit). Venue questions are SECTIONS in 1-probes/. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper Venue: recommend + pin the best-fit venue

## Overview

It answers one question: **which venue does this paper target, and what does that venue REQUIRE of the final paper?**

Venue selection is the FIRST venue-coupled design decision.
Pitch (the cover letter), narrative, displays, and prose all couple to the venue, so the venue must be chosen before pitch.
Resource and claims are venue-FREE and do NOT need a venue (what a paper NEEDS to exist does not depend on where you send it).
The lifecycle order is: seed (FREE) -> resource (FREE) -> claims (FREE) -> [venue pinned here] -> pitch (ALIGNED) -> narrative (ALIGNED) -> display (ALIGNED) -> section-edit (ALIGNED).

This skill analyzes a paper or a bare topic against every venue pack in `../../../venue/playbook-*`, recommends a ranked shortlist, pins the choice in `STATUS.md`, and produces a stage document (`2a-venue.md`) with the venue decision, relevant files, requirements (blueprint + writing principles), and a Q-consumer.

The venue packs are knowledge, not skills; this skill is the READER that turns them into a recommendation.
It never edits a pack.

## Artifact Spec

**Files produced:**
- `0-lifecycle/2a-venue/2a-venue.md` -- venue stage document; full fill-in skeleton: `ref/venue-template.md`
- `0-lifecycle/2a-venue/_LOG_2a-venue.md` -- phase progress journal
- `1-probes/PPNN_<topic>.md` -- the probe FILES; a venue question becomes an ENTRY (recent publications, editor, competing papers), its `### q-consumer` bullet naming the `Q-Venue-<n>` it serves
- `STATUS.md` -- `venue:` field pinned

**Content structure (2a-venue.md)** -- four sections; full skeleton + fill rules (inline `<!-- RULE -->` comments) in `ref/venue-template.md`; cross-stage charter in `../../TEMPLATES.md`:

```text
2a-venue: <paper title>
========================
Provenance header       pack slug @ venue commit, outlet dir

Venue Decision          which venue + WHY, ranked suggestion (backups, nearest rejected), audience,
                        desk test + this paper's answer, desk-reject risks, and which claim hits
                        which reward -- as RECORD LINES, never a pipe table
Relevant Files          the packs/guides this rests on (taste.md, section style.md, exemplars)
Requirements            what the final paper MUST do -- Structural Blueprint (per-section norms,
                        transcribed + source-tagged) + Writing Principles (tone, citation, results, hard caps)
Q-consumer              venue-fit questions, uniform ## Q-Venue-<n> (Description/Reason/Answer)
```

**Structural Blueprint section (the key downstream contract):**

One block per manuscript section, fields per the template: subsections, paragraphs, sentences/paragraph, avg sentence length, citation density, results reported + detail, display units, this-paper adaptation, and a `[source: ...]` tag naming the guide each number came from.

This section is the design contract for paper structure: the venue-aligned stages (pitch for framing, narrative for beat allocation, display for exhibit budgets, section-edit for paragraph counts) read it here rather than re-deriving from the packs.
The provenance header makes staleness detectable: if `venue` has moved past the recorded commit, re-derive the blueprint without changing the pin.

**How to derive the blueprint (source priority):**
1. Read the pinned outlet's per-section guides (`../../../venue/playbook-<venue>/<journal>/<journal>-<section>/style.md`).
   Each carries word budget, arc, paragraph-structure table, and a measured `## Micro-norms` block (paragraphs, sentences per paragraph, words per sentence, citation density) -- TRANSCRIBE these into the spec above; do not re-mine what is already measured.
2. Read `<journal>/taste.md` (desk signals) and the pack `style-profile.md` for the Writing Principles side.
3. ONLY if the outlet has no section guides (or a section is missing): count 2-3 stored exemplars from `<journal>/examples/` yourself (sections, paragraphs, sentences, sentence length, citations per sentence, where results appear), or search published papers as a last resort.
4. Adapt the generic blueprint to THIS paper's claim structure (e.g., H1/H2/H3 map to specific theory subsections).
5. Where a Micro-norms block flags a measured-vs-budget clash or a "to verify" marker, carry that caveat into the blueprint rather than silently picking one number.

The blueprint is venue-ALIGNED: retargeting to a different venue rewrites the blueprint.

**Writing Principles section (prose-level specs):**
- Language/tone: formal vs accessible, jargon level, hedging conventions
- Citation style: in-text format, bibliography conventions
- Results presentation: tables vs figures, statistical reporting, effect size conventions
- Display limits: max figures, max tables, format requirements
- Abstract conventions: word limit, structure (prose vs labeled), arc

Writing Principles is the prose companion to the Structural Blueprint.
The blueprint says HOW MANY sentences; Writing Principles says HOW TO WRITE them.

**Formatting:** per `ref/venue-template.md` (`=====` title, `-----` sections, no `#` headings, one sentence per line).

**Done-criteria:**
- [ ] Venue pinned in STATUS.md
- [ ] Structural Blueprint section filled with per-section quantitative norms (every section has: subsection count, paragraphs, sentences/paragraph, sentence length, citation density, results reported, display units)
- [ ] Writing Principles section filled with prose-level specs (tone, citation style, abstract conventions)
- [ ] Venue Decision's Fit record-lines map H/claims to venue scope (no pipe table)
- [ ] At least one Q-Venue-<n> question raised or answered (recent publications check)
- [ ] Every `<!-- RULE -->` comment deleted from the filled 2a-venue.md
- [ ] Blueprint adapted to THIS paper's claim structure (H1/H2/H3 mapped to specific sections/subsections)

## Modes

```text
default     recommend a shortlist, then ASK before writing STATUS venue (you confirm the pin)
--no-pin    advisory only: recommend and stop; never write any file
            (for "just tell me which journal" / a bare topic with no folder)
refresh     re-derive ONLY: keep the existing pin, re-transcribe the Structural Blueprint +
            Writing Principles from the current pack state, update the provenance header
            (new venue commit + derived date), and log the delta in _LOG_2a-venue.md.
            Use when venue has moved past the recorded commit (pack norms improved) or
            when 2a-venue.md predates the provenance header. Never re-opens the venue choice.
```

## When to use

- "Which journal for this?", "where should I submit?", venue fit, before pitch.
- A new paper whose venue is undecided, or a topic with no folder yet.
- Reconsidering venue after a reject, a scope change, or a reviewer signal.
  (On retarget: claims stays unchanged; pitch, narrative, display, and section-edit rewrite with new [primary], RQ framing, and Editor's Chair Test.)

## Inputs

```text
paper root         reads 0-lifecycle/{0-seed,1-claims,2-pitch} for the contribution profile
   or topic text   a free-text topic / abstract when there is no folder yet
venue packs        ../../../venue/playbook-*/README.md   ("-> Claims" rewards + fit signals)
outlet taste       ../../../venue/playbook-*/<journal>/taste.md   (desk-accept/reject signals + one-sentence test)
section norms      ../../../venue/playbook-*/<journal>/<journal>-<section>/style.md   (quantitative norms + Micro-norms)
venue index        ../../../venue/README.md              (family map + IS selection table)
```

## Procedure

1. **Build the paper's contribution profile.**
   From the seed/claims (or the topic text), extract: the central contribution, the method, the topic/domain, the evidence strength, and the intended audience.
   If these are unclear, ask one round of questions before scoring.
2. **Read the candidate packs.**
   For each `../../../venue/playbook-<venue>/README.md`, read the `-> Claims` mapping (what it rewards, contribution vs enabler) and the fit signals; read `../../../venue/README.md` for the family map and IS selection table.
   A pack is family-granular; to pick the OUTLET inside a family, read each candidate `<journal>/taste.md` and score the paper against its desk-accept/desk-reject signals and one-sentence test.
3. **Score each venue** on five dimensions, each High/Med/Low with a one-line reason: contribution-type match, method match, topic/domain match, evidence-bar match, audience match.
   Record any hard disqualifier (e.g. "design science -> not ISR").
4. **Rank and shortlist** the top 3.
   For each: a fit rationale, what to emphasize for that venue, and the main why-not / risk.
5. **Recommend ONE primary** + 1-2 backups.
   The primary is the one whose rewards the paper's strongest claim most directly satisfies.
6. **Pin it (unless `--no-pin`).**
   In default mode, ASK the user, then write `venue: <pack-slug>` (plus an optional `venue_outlet:` for the concrete journal) into `STATUS.md`.
   With `--no-pin`, stop after step 5 and write nothing.
   Pinning is the handoff to pitch (the cover letter), which re-runs its [primary] claim designation, RQ framing, and Editor's Chair Test for the new venue.
7. **Derive the structural blueprint.**
   After pinning, build the per-section quantitative spec:
   a. Read the pinned outlet's `<journal>-<section>/style.md` guides; transcribe each guide's word budget, paragraph-structure table, and measured Micro-norms block (paragraphs, sentences/paragraph, words/sentence, citation density) into the per-section spec.
   b. Read `<journal>/taste.md` + the pack `style-profile.md` for Writing Principles (tone, citation style, abstract conventions).
   c. ONLY where section guides are missing: count 2-3 stored exemplars in `<journal>/examples/` yourself, or search published papers at this venue in the same contribution type, and measure the same metrics.
   d. Synthesize into the Structural Blueprint section of 2a-venue.md: one block per section, adapted to THIS paper's claim structure; carry over any measured-vs-budget clash or "to verify" caveat the guides flag.
   e. The blueprint must be concrete enough that section-edit can use it without further guessing: "Introduction has 4 subsections, each 2 paragraphs, each 5-6 sentences" not "Introduction should be well-structured."

## Output contract

A recommendation table, then the STATUS write on confirm:

```text
venue            fit   why (one line)                         emphasize / why-not
playbook-jama-portfolio    HIGH  patient-safety opioid outcome, obs.    Table1+STROBE; assoc-not-causal
playbook-utd-is    LOW   thin IS theory contribution            would need a theory pivot
...
PRIMARY: playbook-jama-portfolio (outlet: JAMA Internal Medicine)   BACKUP: jama-netopen (same pack)
-> write STATUS.md: venue: playbook-jama-portfolio / venue_outlet: jama-im ?
```

## Topic-only example (no paper folder yet)

`/haipipe-paper-venue "physician agreeableness, scored by an LLM from online reviews,
predicts higher opioid prescribing; observational, CMS Medicare 2015-2020" --no-pin`

1. Build the profile from the text (no seed/claims to read): contribution = a clinical prescribing-safety association; method = the LLM trait measure (an enabler); design = observational; audience = clinical / policy.
2-5. Score the packs, shortlist, recommend (here: `playbook-jama-portfolio` -> JAMA Internal Medicine primary, `jama-netopen` in the same pack as backup).
6. `--no-pin`, so report only and stop; offer to scaffold a paper folder and pin if the user then wants one.

## Venue label -> pack resolution

A human venue name maps to one pack (family granularity; the concrete outlet is a delta inside the pack).
This skill owns the map:

```text
MISQ / ISR / MS-IS / MS-Marketing [UTD-IS]     -> playbook-utd-is          (journals: MISQ, ISR, MS-IS, MS-Marketing)
NMI / Nat Comms / Nat Med / npj DM / NHB       -> playbook-nature-portfolio (journals: NMI, nature-communications, nature-medicine, npj-digital-medicine, nature-human-behaviour)
PNAS                                           -> playbook-pnas            (journal: pnas)
JAMA / JAMA Internal Medicine / JAMA Netw Open -> playbook-jama-portfolio  (journals: jama-flagship, jama-im, jama-netopen)
Diabetes Care (specialty clinical)             -> playbook-medical-journals (journal: diabetes-care; extension point for more)
grant (NSF / NSFC / KAKENHI / ERC / ...)       -> playbook-grant           (agency deltas in README, no journal dirs)
patent (CNIPA / USPTO / EPO)                   -> playbook-patent          (jurisdiction deltas in README, no journal dirs)
```

A named venue with no pack (NEJM, Lancet, ICLR, NeurIPS, ...) stays a bare `venue_outlet:` formatting target: recommend honestly, note no pack exists, and the lifecycle wiring no-ops.

When `STATUS.md venue:` is a human label, every stage resolves it through this map to find `../../../venue/playbook-<slug>`.
Prefer writing the pack slug into STATUS directly.

## Boundaries

```text
this skill   recommends a venue and PINS it (STATUS venue); owns label->pack resolution
claims       venue-FREE evidence inventory (does NOT read the venue)
pitch        venue-ALIGNED cover letter; couples to the pinned venue (Editor's Chair, [primary], RQ framing)
narrative    venue-ALIGNED arc; expands the pitch for this venue
display      venue-ALIGNED exhibit set; reads the blueprint's display units and limits
section-edit venue-ALIGNED prose; reads the blueprint's per-section paragraph/sentence spec
venue/*     knowledge packs, read-only here
```

It recommends and pins; it does not write claims, pitch, or prose.
Venue-first.
After pinning, the next step is pitch (not claims -- claims is venue-free).

## Gate

Ask before overwriting an existing `STATUS.md venue:` (a venue change re-runs the pitch's [primary] designation and RQ framing, and reshapes narrative, displays, section-edit, and prose).
Claims stays unchanged because it is venue-free.
