---
name: haipipe-paper-venue
description: "Recommend the best-fit venue for a paper or topic, then pin it. Produces 0-lifecycle/2-venue/2-venue.md with venue choice, writing principles (section structure, length norms, citation density, results conventions, display limits), fit assessment, and probes. Writes the choice into STATUS.md. This is the venue-first front door: run it before pitch (claims is venue-free). Trigger: venue, which journal, where to submit, venue fit, recommend journal, journal selection, pick venue, 投哪个期刊, 选刊, 期刊推荐, /haipipe-paper-venue."
argument-hint: "[paper-path | free-text topic/abstract] [--no-pin]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "3.0.0"
  last_updated: "2026-07-07"
  summary: "Venue stage orchestrator. Recommends + pins the best-fit venue, produces 2-venue.md with writing principles, structural blueprint (per-section quantitative norms), and probes. Downstream stages (pitch, narrative, display, section-edit) all read the Structural Blueprint and Writing Principles sections."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# Paper Venue: recommend + pin the best-fit venue

## Overview

Venue selection is the FIRST venue-coupled design decision. Pitch (the cover letter), narrative, displays, and prose all couple to the venue, so the venue must be chosen before pitch. Claims is venue-FREE and does NOT need a venue. The lifecycle order is: seed (FREE) -> claims (FREE) -> [venue pinned here] -> pitch (ALIGNED) -> narrative (ALIGNED) -> display (ALIGNED) -> section-edit (ALIGNED).

This skill analyzes a paper or a bare topic against every venue pack in `../../_venue/playbook-*`, recommends a ranked shortlist, pins the choice in `STATUS.md`, and produces a stage document (`2-venue.md`) with the venue profile, writing principles, and probes.

The venue packs are knowledge, not skills; this skill is the READER that turns them into a recommendation. It never edits a pack.

## Artifact Spec

**Files produced:**
- `0-lifecycle/2-venue/2-venue.md` -- venue stage document (venue choice + writing principles + probes)
- `0-lifecycle/2-venue/_LOG_2-venue.md` -- phase progress journal
- `0-lifecycle/2-venue/_PROBE/` -- probe plans (recent publications, editor, competing papers)
- `STATUS.md` -- `venue:` field pinned

**Content structure (2-venue.md):**

```text
2-venue: <paper title>
=======================

Venue Choice            which venue, one-line why, backup options
Venue Profile           audience, scope, what this venue rewards
Structural Blueprint    per-section quantitative norms (THE construction spec)
Writing Principles      prose-level specs (tone, citation style, language)
Fit Assessment          how H1/H2/H3 match the venue's scope
Probes                  venue-level investigation needs
```

**Structural Blueprint section (the key downstream contract):**

The structural blueprint is a per-section quantitative spec derived from exemplar papers at this venue. Every section gets its own block with:

```text
Section: <name> (<role in the paper>)
  Subsections: <count> (<subsection names>)
  Paragraphs per subsection: <count or range>
  Sentences per paragraph: <count or range>
  Avg sentence length: <words>
  Citation density: <citations per sentence>
  Results reported: <yes/no>
  Results detail: <what kind: coefficients, p-values, effect sizes, none>
  Display units: <which figures/tables belong here>
```

This section is the single source of truth for paper structure. Pitch reads it to frame the contribution. Narrative reads it to allocate story beats. Section-edit reads it to know how many paragraphs each section gets and what each paragraph does.

**How to derive the blueprint:**
1. Read the venue playbook (`../../_venue/playbook-<venue>/`) for general norms.
2. Read stored exemplars (`../../_venue/playbook-<venue>/exemplars/`) for real section structures.
3. If exemplars are sparse, read 2-3 published papers at this venue (via the paper's own `0-extra/` or by searching) and count: sections, subsections, paragraphs, sentences, sentence length, citations per sentence, where results appear.
4. Synthesize into the per-section spec above.
5. Adapt the generic blueprint to THIS paper's claim structure (e.g., H1/H2/H3 map to specific theory subsections).

The blueprint is venue-ALIGNED: retargeting to a different venue rewrites the blueprint.

**Writing Principles section (prose-level specs):**
- Language/tone: formal vs accessible, jargon level, hedging conventions
- Citation style: in-text format, bibliography conventions
- Results presentation: tables vs figures, statistical reporting, effect size conventions
- Display limits: max figures, max tables, format requirements
- Abstract conventions: word limit, structure (prose vs labeled), arc

Writing Principles is the prose companion to the Structural Blueprint. The blueprint says HOW MANY sentences; Writing Principles says HOW TO WRITE them.

**Formatting:**
- Heading style: `=====` for the document title, `-----` for sections. No `#`/`##`/`###`.
- One sentence per line (semantic line breaks).

**Done-criteria:**
- [ ] Venue pinned in STATUS.md
- [ ] Structural Blueprint section filled with per-section quantitative norms (every section has: subsection count, paragraphs, sentences/paragraph, sentence length, citation density, results reported, display units)
- [ ] Writing Principles section filled with prose-level specs (tone, citation style, abstract conventions)
- [ ] Fit Assessment maps H/claims to venue scope
- [ ] At least one probe planned or done (recent publications check)
- [ ] Blueprint adapted to THIS paper's claim structure (H1/H2/H3 mapped to specific sections/subsections)

## Modes

```text
default     recommend a shortlist, then ASK before writing STATUS venue (you confirm the pin)
--no-pin    advisory only: recommend and stop; never write any file
            (for "just tell me which journal" / a bare topic with no folder)
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
venue packs        ../../_venue/playbook-*/README.md   ("-> Claims" rewards + fit signals)
venue index        ../../_venue/README.md              (family map + IS selection table)
```

## Procedure

1. **Build the paper's contribution profile.** From the seed/claims (or the topic text), extract: the central contribution, the method, the topic/domain, the evidence strength, and the intended audience. If these are unclear, ask one round of questions before scoring.
2. **Read the candidate packs.** For each `../../_venue/playbook-<venue>/README.md`, read the `-> Claims` mapping (what it rewards, contribution vs enabler) and the fit signals; read `../../_venue/README.md` for the family map and IS selection table.
3. **Score each venue** on five dimensions, each High/Med/Low with a one-line reason: contribution-type match, method match, topic/domain match, evidence-bar match, audience match. Record any hard disqualifier (e.g. "design science -> not ISR").
4. **Rank and shortlist** the top 3. For each: a fit rationale, what to emphasize for that venue, and the main why-not / risk.
5. **Recommend ONE primary** + 1-2 backups. The primary is the one whose rewards the paper's strongest claim most directly satisfies.
6. **Pin it (unless `--no-pin`).** In default mode, ASK the user, then write `venue: <pack-slug>` (plus an optional `venue_outlet:` for the concrete journal) into `STATUS.md`. With `--no-pin`, stop after step 5 and write nothing. Pinning is the handoff to pitch (the cover letter), which re-runs its [primary] claim designation, RQ framing, and Editor's Chair Test for the new venue.
7. **Derive the structural blueprint.** After pinning, build the per-section quantitative spec:
   a. Read the venue playbook's style-profile and exemplars.
   b. If exemplars exist, count real structures: sections, subsections, paragraphs per subsection, sentences per paragraph, average sentence length, citations per sentence, where results are reported and how.
   c. If exemplars are sparse, search for 2-3 published papers at this venue in the same contribution type (theory-forward empirical, causal, design science, etc.) and count the same metrics.
   d. Synthesize into the Structural Blueprint section of 2-venue.md: one block per section, adapted to THIS paper's claim structure.
   e. The blueprint must be concrete enough that section-edit can use it without further guessing: "Introduction has 4 subsections, each 2 paragraphs, each 5-6 sentences" not "Introduction should be well-structured."

## Output contract

A recommendation table, then the STATUS write on confirm:

```text
venue            fit   why (one line)                         emphasize / why-not
playbook-jama-portfolio    HIGH  patient-safety opioid outcome, obs.    Table1+STROBE; assoc-not-causal
playbook-utd-is    LOW   thin IS theory contribution            would need a theory pivot
...
PRIMARY: playbook-jama-portfolio (outlet: JAMA Internal Medicine)   BACKUP: playbook-clinical-medicine
-> write STATUS.md: venue: jama / venue_outlet: JAMA Internal Medicine ?
```

## Topic-only example (no paper folder yet)

`/haipipe-paper-venue "physician agreeableness, scored by an LLM from online reviews,
predicts higher opioid prescribing; observational, CMS Medicare 2015-2020" --no-pin`

1. Build the profile from the text (no seed/claims to read): contribution = a clinical prescribing-safety association; method = the LLM trait measure (an enabler); design = observational; audience = clinical / policy.
2-5. Score the packs, shortlist, recommend (here: `playbook-jama-portfolio` -> JAMA Internal Medicine primary, `playbook-clinical-medicine` backup).
6. `--no-pin`, so report only and stop; offer to scaffold a paper folder and pin if the user then wants one.

## Venue label -> pack resolution

A human venue name maps to one pack (family granularity; the concrete outlet is a delta inside the pack). This skill owns the map:

```text
MISQ / ISR / Management Science (IS) [UTD-IS]-> playbook-utd-is   (pick the outlet via the in-pack delta)
Nature / Nature Methods / Nature Biotech      -> playbook-nature-portfolio
PNAS                                          -> playbook-pnas
JAMA / JAMA Internal Medicine / JAMA Netw Open-> playbook-jama-portfolio
NEJM / Lancet / Annals / BMJ (clinical)       -> playbook-clinical-medicine
grant (NSF / NSFC / KAKENHI / ERC / ...)      -> playbook-grant
patent (CNIPA / USPTO / EPO)                   -> playbook-patent
```

When `STATUS.md venue:` is a human label, every stage resolves it through this map to find `../../_venue/playbook-<slug>`. Prefer writing the pack slug into STATUS directly.

## Boundaries

```text
this skill   recommends a venue and PINS it (STATUS venue); owns label->pack resolution
claims       venue-FREE evidence inventory (does NOT read the venue)
pitch        venue-ALIGNED cover letter; couples to the pinned venue (Editor's Chair, [primary], RQ framing)
narrative    venue-ALIGNED arc; expands the pitch for this venue
_venue/*     knowledge packs, read-only here
```

It recommends and pins; it does not write claims, pitch, or prose. Venue-first.
After pinning, the next step is pitch (not claims -- claims is venue-free).

## Gate

Ask before overwriting an existing `STATUS.md venue:` (a venue change re-runs the pitch's [primary] designation and RQ framing, and reshapes narrative, displays, section-edit, and prose). Claims stays unchanged because it is venue-free.
