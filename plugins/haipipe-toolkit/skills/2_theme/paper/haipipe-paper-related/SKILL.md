---
name: haipipe-paper-related
description: "A paper Board's closest related work: the 20 to 25 nearest papers, sorted into 3 or 4 types, mapped beside our paper (studio s10, related_map.py) and read closely in s11 to s19, so the paper can say what each leaves open and what it adds. Not the literature (haipipe-discovery) or the related/ folder (haipipe-related). Trigger: related work, closest papers, related-work map, s10, positioning, /haipipe-paper-related."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent, WebSearch, WebFetch
metadata:
  version: "0.1.1"
  last_updated: "2026-10-26"
  group-token: "s10-related-work-map"
  # version history: ./CHANGELOG.md
---

# /haipipe-paper-related · who did nearly this, and what we add

A reviewer reads a paper next to the few papers closest to it. This skill finds those papers, sorts them into
types, reads each closely, and draws where our paper sits among them. Its output is positioning, not citations.

```text
haipipe-discovery        discovery/ Paper Runs     wide: every paper we may cite, "what is known"
haipipe-related          related/related.md        storage: what came in, kept once as it came
haipipe-paper-ideation   studio/s01-ideation/      the ideas, and their novelty check (G0)
haipipe-paper-related    studio/s10-s19            narrow: the closest work, "who did nearly this"
```

Asked by JL 261019: "for the related work we can do things like s10-related-work, and after that, we have s11
s12, etc"; "it is different from the literature"; "we can use haipipe-paper-related, to find the most related
papers". The pattern is Paper-LLMRecPhy-Jama's s10 to s15, built 2026-10-13.


Related is not literature
-------------------------

```text
                 literature (haipipe-discovery)      related work (this skill)
question         what is known about X?              who asked nearly our question?
size             tens to hundreds                    about 20 to 25, in 3 or 4 types
depth            a Result card per paper             each read from its PDF, its logic
output           citations, bank.bib, evidence       one map, what each leaves open, what we add
feeds            every Section's \cite               s01 novelty (G0), Related Work, Introduction's gap
```

1. **Closest**: same question, or same subject with the same kind of design.
2. **Shared background**: a method or setting we use, not our question; a row, never a type topic.
3. **Drop**: anything else stays in Discovery; it may still be cited.
4. **★**: the one closest paper in each type, the one a reviewer names first.


The band: s10 to s19
--------------------

```text
studio/
├── s01-ideation/                         haipipe-paper-ideation: the ideas
├── s10-related-work-map/                 ① every closest paper on one map, ours as the key point
├── s11-related-work-<type>/              one type of closest work, each paper read in full
├── s12-related-work-<type>/              ...
└── s19-related-work-<type>/              at most nine types
```

1. **s10 is the map**: one main frame, small frames that explain it, as stairs.
2. **3 or 4 types**: only the most relevant papers, the studies close to us (JL 261019).
3. **s11 to s19, one per type**: a type is what its papers share (subject × design).
4. **Tag**: every topic's `**Tags:**` is `` `Related work` ``, one Studio group.
5. **Older Boards**: `related_topics.py band` moves them in, old links kept.

On a paper Board this band takes the place haipipe-studio gives "levels" (s11-s19) on a work Block; a paper Board
draws no level topics. The drawings follow excalidraw-studio's rules (one main frame, stairs, white space; JL
261013). JL 261019, on LLMRec's seven: "we might have too many related works ... merge them into three to four,
we just want to keep the most relevant, and the studies close to us". So the types tell one story (LLMRec: LLMs
already name doctors · recommenders rank for fit only · other fields split entry from order · AI answers differ
from Google), about eight papers at most each; a paper that serves one idea or one measure stays a row, cited
where it is used, and its reading moves to `studio/_archive/` with the topic it left.


The rows: related/related.md
----------------------------

The table is haipipe-related's: its six columns (`kind · date · item · link · feeds · group`), then the six a
paper row adds. A Board whose table holds only meetings and files has the six; `map` and `group` add the paper
columns at its right, every older row kept with empty cells.

```text
bears on   Closest: <type>                    the type is the s1N topic that reads it (no comma in it)
           Shared background: <what>          background, no type topic
key        ★                                  the closest in its type
venue      where it appeared                  journal, conference, or arXiv
why here   what it reports that matters       one or two sentences from its abstract or full text
read       its Discovery deep read            b01.j06.t07, or the full Run folder when that is ambiguous
source     its DOI, else arXiv or web address
feeds      s10, s1N                           written by `group`; leave it empty before
```

1. **Feeds**: `group` writes `s10, s1N` on every row of its type, so write rows first with `feeds` empty.
2. **Background rows**: `feeds` names the Section that cites them, or stays empty; s10 never draws them.
3. **PDFs**: a free copy goes in the Board's papers folder (`related/paper/`, or `papers/` where the Board has
   that), only when its license allows (haipipe-related rule 4). A copy elsewhere in the repository does not
   change the license. Without one, a paper stays a red card: "no PDF yet: its abstract only".


The workflow
------------

```text
1 find    the question from s01 → candidates          haipipe-discovery search workers, novelty-check
2 pick    closest / background / drop, ★ per type    rows in related/related.md
3 group   the closest into types (≤ 9)                related_topics.py group, one s1N each
4 read    each closest paper from its PDF             excalidraw-read, reads/pNN-<paper>/reading.yaml
5 map     s10: axes, placements, nearest, gaps        related_map.py, from the face's yaml
6 feed    s10's Open, for s01 and the Section owner   per claim: its closest work, what stays new
```

1. **Find** from the question, not the topic. Read s01's Direction and each lead Idea's claims, then search with
   haipipe-discovery's search workers (`haipipe-discovery-search-worker-agent`), `novelty-check`, and the
   `1_base/search/1_search` tools (semantic-scholar, openalex, arxiv). Follow citations both ways from the first
   closest hits. Every candidate has a real identity: a DOI, an arXiv id or a publisher page, checked.
2. **Pick** with the three questions above. Write each kept paper as a row (haipipe-related's columns: item,
   link, venue, why here, source), its `bears on` and its ★. A paper's `why here` says what its abstract or full
   text reports that matters to us, in one or two sentences, never a guess.
3. **Group** the Closest rows by what they share. Name each type in plain words, no comma ("chatbots that name
   real doctors"); the same words go after `Closest:` and become the topic's title. Then
   `related_topics.py group <board> --type '<type>' --slug <slug>` makes the next free s11-s19: the rows of that
   type in reading order, each with `says` (its first sentence of `why here`) and `ref` (title, authors (six,
   then et al.), venue, year, link; from its DOI's record at doi.org, cleaned; `--offline` leaves the authors ❓).
   It writes their `feeds`. Then write the face's `key`, `what` and `why`, and check each `says` and `ref`.
   `--background` makes a type of `Shared background: <type>` rows instead: background read in full, never on the
   map (LLMRec's s14, s16, s17). A paper whose short name starts two rows is named by its whole item.
4. **Read** each paper with `/excalidraw-read` into the type topic's `reads/pNN-<paper>/reading.yaml`: its logic,
   its key passages quoted and highlighted, and how each links to our paper (supports, threatens, we borrow).
   A reading needs a top-level `key:` (its one point), or excalidraw-studio's check fails ①. The PDF's extracted
   `paper.txt` is working material: `_WorkSpace/` or the session's scratchpad, never the Board. The most important
   papers first; a paper without a PDF stays red until one is saved.
5. **Map**: `related_topics.py map <board>` once, then fill the face's `map:` yaml (`ref/map-face.md`): two axes
   that make our gap visible, every Closest row placed, our paper as the key point; add `nearest:`, `gaps:`,
   `lessons:` and `papers:` as the reads give them something to say. Redraw with the topic's builder, then
   excalidraw-studio's `check.py` on the drawing (its limit: 200 words a frame). Steps 3 and 5 run in either order.
6. **Feed, by proposal**: s10's Open lists, per claim of the lead Idea, its closest work and what stays new, and
   one paragraph per type for the Section that positions the paper (Related Work; Literature Review at a venue
   without one, such as MISQ). The owners of s01 and of that Section write them in; this skill never edits an
   `agreed` topic or another owner's Section. In Open: one lead-in line, then one numbered item per claim; again
   for the Section, one item per type. Citations go through the Section's `draft/evidence/bibex/` (never
   `bank.bib`).

`map`, `group` and `band` redraw the Board's s00 index (haipipe-studio `block_index.py`), a generated drawing that
is never edited by hand. A `board.md` that lists the Studio topics in its own words is updated by hand.

```bash
R=Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper-related/scripts/related_topics.py
python $R map   paper/Paper-<Slug>                      # studio/s10-related-work-map/, drawn once
python $R group paper/Paper-<Slug> --type 'chatbots that name real doctors' --slug chatbots-naming-doctors
                                                        # next free s11-s19; its rows' feeds and references
python $R check paper/Paper-<Slug>                      # every Closest row placed on s10 and in one s1N
python $R feeds paper/Paper-<Slug>                      # every row's s10-s19 feeds, from the topics
python $R band  paper/Paper-<Slug> [--apply]            # an older Board's topics into s10-s19
python paper/Paper-<Slug>/studio/s10-related-work-map/build_s10_related_work_map.py      # redraw
```


Checks
------

`related_topics.py check` exits 1 on a ❌:

1. **❌ unplaced**: a Closest row with no placement on the s10 map.
2. **❌ untyped**: a Closest row in no s11-s19 topic.
3. **❌ stray**: a type topic's paper that is no row of related/related.md.
4. **❌ band**: a `Related work` topic outside s10-s19, or s10 not the map.
5. **⬜ / ⚠️ notes**: a paper not read from its PDF yet; a type with no ★; a paper in two types.

A person moves each topic's **Stage** (explore · shaping · agreed · closed); the check never does.


Rules
-----

1. **Closeness is judged, then shown**: every Closest row says in `why here` what makes it close.
2. **Read before placing**: a placement's label is a number or a few words from the paper, never invented.
3. **Quotes stay short**: a reading quotes the passages it needs, never a whole section.
4. **No private data**: a paper row and its reading carry no patient data and no unpublished co-author text.
5. **Generated drawings**: the `.excalidraw` and `.png` are drawn by the builders; change the face, then redraw.
6. **Renumber with `band`**: it moves folders, files, soft Runs (runs/run-draw-sNN/) and every mention in the
   Board's files in one pass, and writes `renamed-from: <old name>` into each face so old links still open.


Files
-----

```text
haipipe-paper-related/
├── SKILL.md                 this contract
├── CHANGELOG.md
├── ref/map-face.md          the s10 face's yaml blocks: map · nearest · gaps · lessons · papers
├── scripts/related_map.py   draws s10 from its face and the Board's Closest rows
├── scripts/related_topics.py  map · group · check · band
└── tests/test_related_topics.py
```
