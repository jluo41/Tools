# ③ The HUMAN channel: /haipipe-board
state: 🟡 PARTIAL
owner: JL
method: one door in, ① dispatches and ③ renders, and every paper-specific behaviour stays behind one declared seam

## Opening
/haipipe-board is not part of /haipipe-paper, and half this board's rulings land in it. What is the relationship, where is its edge, and WHO DOES THE USER TYPE?
Two separate skills write the same markdown file to produce a paper and its board, and this face is how they manage that without ever colliding.

The typing question was the one that had never been answered, and the board contradicted itself about it. `QA1` drew `③` as a peer the human reaches directly and said `①` owns neither channel out. `QA2` said `①` is a thin front door that RESOLVES THE PAPER, OPENS THE BOARD, and routes. Both could not be true, and at the time this page opened the code answered a third way: `haipipe-paper-enter` (the console of that era, since retired into the one door) read `board.md` as a data file and rendered its own text dashboard, so the human had to type the second skill with the paper's `0-lifecycle/` path.

JL ruled it on 260726: `①` is the SINGLE source of entry. `/haipipe-paper enter <path>` builds and opens the paper's board, and `③` is called rather than typed.

The map pairs each thing with the board that governs it (`QA1`). This face is the middle row: `③` the tool, whose own board is `④`. What the grid alone does not show is that this one first-class family builds the entire right-hand column, its own board included. `haipipe-board` lives at `skills/board/haipipe-board/` and renders Boards across this repo, including this paper family's design and lifecycle Boards.

That earns it a place on the map, and it earns the number by the same test that excluded the evidence banks. We rule nothing about what is inside `tasks/`, so the banks are a wall rather than a room. We rule a great deal about `haipipe-board`: who composes an S filename, who creates a page, what `## Items to Finish` means, what a `>` lane binds to, and how a citation chip resolves. Nine faces on this board already rule its behaviour. A thing you rule that much is not outside the map.

The danger it creates is specific and it has already happened twice today. A ruling here can be applied to the paper skill and quietly not reach the tool, or shipped in the tool and never reflected here. Both directions were observed on 2026-07-26.
Scope: This page covers What `haipipe-board` is to this skill, which of its behaviours this board may rule, the `dialect: paper` seam, and how a ruling reaches both halves. Neighbouring pages cover What a board IS, its face grammar, where it lives on disk, and its live layer are ruled on `④`, the board tool's OWN board at `diagrams/01-boardform-260722/`, 27 faces. `③` and `④` are a thing/board pair exactly as `①` and `②` are, which is why this face may rule the contract between us and never what a board is. The two boards it renders for us are `QA3` and `QA7`. Who owns a shared page is the `QA8` group; how work is driven from a page is `QA9`. Both are now under this face, as `QA8` and `QA9`.

## Diagram
```
   TWO SKILLS, ONE FILE, TWO PRODUCTS

   ① haipipe-paper                        ③ haipipe-board
     the SUBSTANCE                          the SHELL · the RENDER
     what a stage decides and writes        · the WRITE-BACK
     paper family                           first-class Board family
              │                                        │
              └──────────────────┬─────────────────────┘
                                 │  they alternate on ONE markdown file
                                 │  and never write the same REGION
                                 ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  ⑧  0-lifecycle/…/S-<Family>-<unit>-<slug>.md               │
   │                                                               │
   │     ③ owns   the filename · the face grammar · the Pages     │
   │              row · the managed Stage Contract block ·         │
   │              anything a human types into the page             │
   │     ① owns   Opening · Content · Aims · States                │
   │              (the substance sections)                         │
   └───────────────────────────────┬──────────────────────────────┘
                                   │  ① GENERATES from it, one way
                                   ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  ⑦  sections/*.tex · displays/…/float.tex · main.pdf    │
   └──────────────────────────────────────────────────────────────┘

```

```
   ── STEP 0 · THE DOOR.  ruled 260726: ① is the SINGLE entry ────

      the user types             what actually runs
      ──────────────────────     ───────────────────────────────────
      /haipipe-paper enter   ──▶ ① resolve the paper root
        <paper-path>             ① get-or-create when the path is new
                                    └ folder: board.md + ONE Seed page
                                 ③ build.py  0-lifecycle/ → board/index.html + page files
                                 ③ serve.py  push the URL to the browser
                                 ① print ONE line + open needs + the URL
                                             │
                                             ▼
                                 the human is LOOKING at ⑧

      The user never types /haipipe-board for a paper. It stays a
      real door for the design boards that are NOT inside a paper,
      this one included: ③ must not become paper-only.

   ── why this does NOT break "① owns neither channel out" ───────
      CALLING IS NOT OWNING.
        ③ still owns the format, the build, the filename rule, the
          html, the write-back. ① renders nothing and never will.
        ① owns the ENTRY, and dispatches.

      It is the SAME relation ① already has with ⑤: a user types
      /haipipe-paper probe, never /haipipe-probe, and ① still never
      computes an answer. The old shape was ASYMMETRIC — ⑤ was
      dispatched-to, ③ was typed — and the asymmetry was an
      accident of history, not a design. This removes it.

```

```
   ── who does what, step by step ────────────────────────────────

    step             ① haipipe-paper            ③ haipipe-board
    ───────────────  ─────────────────────────  ──────────────────────────
    1 create a page  picks the stage and its    stage.py new: composes the
                     template; create-page.py   filename, writes the face,
                     is the public entry        adds the Pages row and the
                                                managed contract  ──▶ ⑧
    2 DRAFT          writes ## Content and      —
                     the Q-consumer block
    3 render         —                          build.py: md → board/ site,
                                                folds the > lanes, resolves
                                                chips against ⑦'s .bib and
                                                1-probes/
    4 a human reads  —                          serve.py: a comment, or a new
                                                > lane on a sentence, written
                                                BACK into ⑧'s markdown
    5 PROBE          asks across the wall and   —
                     records the pointer in ⑧
    6 REVISE         rewrites ⑧'s Content       —
    7 sync           owns everything else on    stage.py sync: refreshes ONLY
                     the page                   the managed block
    8 CHECK          prepares the gate          —      a HUMAN writes ✅
    9 generate       the door's build fns       —
                     read ⑧'s Content ──▶ ⑦

```

```
   ── the two asymmetries that make it work ──────────────────────
      only ③ writes ⑧ from a human's click.  ① has no UI; every
        comment, every sentence lane, every ticked box arrives
        through serve.py.
      only ① writes ⑦.  The tool never touches a manuscript file;
        it does not know what LaTeX is.

   ── the seam ───────────────────────────────────────────────────
      a board declares       dialect: paper
      and only then does ③ resolve \citep{}, {VAL:?} and [Q-X-n]
      against ⑦'s .bib and 1-probes/. A board that does not declare
      it renders byte-identical and pays nothing. That one line is
      the entire paper-specific surface of a generic tool.

```

```
   ── what the single door DELETES ───────────────────────────────
      the console's text dashboard is a SECOND renderer of the same
      S pages: a golden rule, frontier predicates, a glyph table, a
      render skeleton, and the stage strip. ⑧ renders all of it, in
      a browser, better, and with the comment lanes the terminal
      cannot have.
      What a terminal is good at is ONE line of where-we-are, the
      open needs, and the URL. The rest of that panel goes.
      → this also answers JL's 260726 question about the stage
        strip: with the board open, the strip is a worse copy of
        the board's own spine.

   ── the risk this moves ONTO the critical path ─────────────────
      the URL reaches the human over the VS Code IPC socket, :5599.
      When that push fails the board does not appear, and after
      this ruling that is EVERY paper session rather than an
      occasional one.
      enter MUST print the URL and say the push failed. A silent
      success is indistinguishable from a dead port forward, which
      is exactly how a whole session was lost on 260725.

```

```
   ── the two-way gap this face exists to close ──────────────────
      260726  chips SHIPPED in ③; four faces here still called
              them unbuilt
      260726  the round ruling landed HERE; haipipe-paper-round
              still described the layer it removed
      260726  the venue pin was ruled into S-Venue-0-venue.md
              FRONTMATTER by ①. src/parse.py:145 is a CLOSED
              whitelist — state|owner|method|session|requires|
              style-from|provides|contract-source-hash — so a
              `venue:` key is INVISIBLE to ③. The field was
              specified in 12 places and would never have parsed.
              Caught only by running the skill on a real paper.
      three the same day, both directions, none detected by anything

   ── the rule that falls out of the third one ───────────────────
      ① MAY NOT INVENT A FACE-GRAMMAR KEY. The frontmatter
      whitelist is ③'s, and ④ rules it. When ① needs to record
      something on a page, it uses a key that already parses or it
      goes to ④ and asks. The venue pin needed neither: it was
      already on the page's own `state:` line, as
      `✅ PINNED · MISQ 2026`.
```

## Content
### It has a board of its own, and that is why we may not rule it
`③` is not a bare dependency: it is the THING half of its own pair, and `④` is its board. Its rulings graduate into it the same way `②`'s graduate into `①`. That symmetry is what settles the ownership line below. A rule about board grammar belongs on `④` and would drift if restated here; a rule about the paper contract belongs here and would never be found by someone working on the tool if it were filed there.

### One door in, and why that is not a contradiction
`QA1` says `①` owns neither channel out of the paper. `QA2` says `①` is a thin front door that resolves the paper, OPENS THE BOARD and routes. Both were on the board at once, and the code answered a third way: `haipipe-paper-enter` never called `haipipe-board` at all, so a human who wanted to SEE the paper typed the second skill themselves with the `0-lifecycle/` path by hand.

JL ruled it on 260726, and the ruling outlived the console that prompted it: since 260805 the enter step is a verb of the one door itself. `①` is the SINGLE thing a human types. It calls `③` to build and open `⑧`, and it calls `⑤` to ask across the wall. **Calling is not owning**: `③` still owns the format, the build, the filename rule, the html and the write-back, and `①` renders nothing.

Two things make that safe rather than a compromise. The dependency was already there, at the write layer: `create-page.py` calls the Board's `stage.py` to compose an S filename, so `①` could never ship without `③`. And the ruling REMOVES an asymmetry rather than adding one, because `⑤` was already dispatched-to. Nobody types `/haipipe-probe` for paper work; they type `/haipipe-paper probe`, and `①` still never computes an answer. `③` alone was typed, and that was an accident of history.

The failure test is the clearest statement of it: when `serve.py` cannot reach the browser, `①` has no renderer of its own to fall back to, because it never had one. It prints the URL and says the push failed.

### One file, two writers, disjoint regions
The collaboration works because the two skills never contend for the same lines. `③` composes the filename, writes the face shell, maintains the Pages row and the managed Stage Contract block, and is the only path by which anything a human types reaches the page. `①` owns the substance: Opening, Content, Aims, States.

Two asymmetries follow, and both are load-bearing. `①` has no interface of its own, so every comment, every sentence lane and every ticked box arrives through `serve.py`. And `③` never touches a manuscript file; it does not know what LaTeX is, which is why generation into `⑦` is entirely `①`'s.

### What this board may rule about it
```
 MAY rule     the CONTRACT between paper and board
              who composes an S filename          QC3b, settled
              who creates a page                  QA8, settled
              which dependency declaration wins   QA8, settled
              what a `>` lane under a sentence means for a paper
              what a citation, value or display chip resolves against

 MAY NOT rule what a board IS, its face grammar, where it lives, how
              the live layer works. Those belong to the tool's own
              board at diagrams/01-boardform-260722/, and this one
              points at them rather than restating them.
```
The line is ownership, not politeness. A rule about the paper dialect stated only here will not be found by someone working on the tool, and a rule about board grammar stated here will drift from the version that binds.

### The seam
`dialect: paper` is the whole paper-specific surface. A board that declares it gets marker resolution at build time; a board that does not is untouched and pays nothing. Keeping the seam to one declared line is what lets a generic tool carry a domain behaviour without becoming domain-specific, and it is why `src/dialect_paper.py` can be deleted without harming the other five boards.

### Where its behaviour is implemented
```
 build.py                 md → board/ site, and the zero-script assertion
 stage.py                 stage new · sync · check · resolve
                          resolve_filename() is the ONE place an S
                          filename is composed (QC3b)
 serve.py                 the live layer: comments, sentence write-back,
                          chat and terminal per question
 src/body.py              the body grammar, the `>` lanes, the chips
 src/dialect_paper.py     the seam: .bib and 1-probes/ resolution
 create-page.py           lives in ①, and calls stage.py. The one place
                          this family reaches into the tool.
```

### How a ruling reaches both halves
It does not, today. That is the open item. A Law that graduates from `②` lands in a paper skill file by the map on `QA2`, and nothing carries it across into `③` or checks that it arrived. Both failures on 2026-07-26 were found by hand, one of them by nearly overwriting the other session's work.

## Aims
- [x] 🚪 Rule the door
      `①` is the single thing a human types; `③` is called, never typed, for a board inside a paper (JL 260726). `/haipipe-board` stays a real door for the design boards that are not inside a paper.
- [x] 🔁 Rule the three moments
      ENTER, after every write to `⑧`, and before `①` acts. The middle one is what a naive reading misses, and without it the human reads a stale board.
- [x] 🛠 Implement it
      `haipipe-paper-enter` gained an `## Open the Board` step and lost its 152-line duplicate renderer; `haipipe-paper-stage` gained the rebuild-after-write rule; the router's Closing Block carries a deep-linked board URL instead of a stage strip. (All three routers were absorbed into the one door `haipipe-paper` on 260805; the rules carried over.)
- [ ] 🧪 Prove the door with a fresh agent
      One `/haipipe-paper enter <new-path>` by an agent that did not write these skills: it should end up looking at a board without being told the word `haipipe-board`.
- [ ] 🔌 Make the push failure loud in code, not just in prose
      The rule is written in three places and enforced nowhere. A build that succeeds while the push fails currently looks identical to success.
- [x] 🖐 Name it as the fifth thing
      Not a folder beside the four: the tool the whole board column is made of (JL 260726).
- [x] 🚪 The seam is one declared line
      `dialect: paper`, opt-in, deletable, and no other board pays for it.
- [ ] 📐 State which behaviours this board may rule
      The contract half, yes; what a board IS, no. Written above as prose and not yet a checkable rule.
- [ ] 🔗 Carry a ruling into both halves
      Nothing links a graduated Law to the tool-side file that implements its other half, and nothing checks it arrived. Twice on 260726 that gap produced a page and an implementation that disagreed.
- [x] 🏷 Re-letter the relationship group under QA
      Done 260726: the five ownership seams became `QA8`, the four running-work seams became `QA9`.

## States
The relationship is real, load-bearing, named, and since 260726 it is also the only way in: `①` is the single door and calls `③`. `haipipe-board` now lives as the first-class `skills/board/` family, renders both of this family's Boards plus the other repository Boards, and keeps paper-specific behaviour behind one opt-in line.

One half of the seam gained a check on 260726. The `dialect:` line had a silent failure. A board that writes markers and forgets the two frontmatter lines rendered them as plain text, produced an EMPTY marker report, and looked completely fine, so `build.py` 0.29.0 now says so. The trigger is the board's own CONTENT rather than its folder name, because a dialect must stay deletable: code spans are stripped first, since a board that MEANS a marker writes it in prose while a board that DISCUSSES the syntax quotes it. Zero false positives across all four real boards; a real paper board with the two lines removed reports 429.

What is still missing is the mechanism connecting the two halves in the other direction. `QA2` says which skill file a group's Law lands in; nothing says which tool file, and nothing verifies either. The third gap logged in the Diagram is what that costs: a frontmatter key was specified in 12 places and could never have parsed, and only running the skill on a real paper caught it.

## Files
- `haipipe-board/`
  The tool: `cli/build.py`, `cli/stage.py`, `cli/serve.py`, `src/`.
- `../01-boardform-260722/`
  Its own board, which owns what a board IS.
- `create-page.py`
  The one place this family reaches into it.

## Law

- `①` is the SINGLE thing a human types. For a board inside a paper, `③` is CALLED, never typed. `/haipipe-board` remains its own door for boards that are not inside a paper.
- CALLING IS NOT OWNING. `③` owns the format, the build, the filename rule, the html and the write-back; `①` owns the entry and dispatches, and renders nothing.
- `①` calls `③` at THREE moments: on ENTER, after EVERY write to `⑧`, and before `①` acts (because a human's click may have changed the page underneath). A stale generated `board/` site is a defect, not an inconvenience.
- The URL push may never fail silently. Say it failed, print the URL, and never fall back to `file://`.
- `①` MAY NOT INVENT A FACE-GRAMMAR KEY. The frontmatter whitelist belongs to `③` and is ruled on `④`. When `①` needs to record something on a page it uses a key that already parses, or it goes to `④` and asks.
- `/haipipe-board` is a peer, not a part. It belongs to the first-class `skills/board/` family, and this family may rule the CONTRACT between them and never what a Board is.
- The paper session is the explicit composed-closing case. Direct Board work ends with `status.py`; when `①` calls `③`, the one Paper closing block carries the active `board:` deep link and no second Board strip is appended.
- Every paper-specific behaviour in the tool sits behind the single `dialect: paper` declaration. A board that does not declare it renders identically and pays nothing.
- A ruling that touches both halves is not graduated until it has landed in both. Applied to one side only, it produces a page and an implementation that disagree, which is a defect and not a partial success.

## Log
- 260806 0720 · [REVISE-CC] swept to the thin architecture (one door + stage data + board rental); the door ruling now names its live implementer (the enter verb of `haipipe-paper` since 260805), the S-page substance sections carry their current names, and the generate step points at the door's build fns.

260726 · closed a composition ambiguity found by a fresh reviewer: direct `③` sessions own the `status.py` strip, while an `①` session emits one Paper block containing the deep Board link; the call does not append two mutually exclusive closing blocks

260726 · Tested the door against `Paper-Personality2Opioid-MISQ2026` instead of reading it, and the venue predicate failed. Yesterday's `STATUS.md` retirement had moved the venue pin to a `venue:` frontmatter key; `haipipe-board`'s face grammar is a CLOSED whitelist at `src/parse.py:145`, so that key is invisible to `③` and was specified in 12 places that could never have parsed. The pin was already on the page's own `state:` line as `✅ PINNED · MISQ 2026`, so the fix needed no new field and no grammar change. Logged as the day's THIRD cross-package gap, and it produced the rule now in the Diagram and the Law: `①` may not invent a face-grammar key.

260726 · The `dialect:` seam's one silent failure closed in `build.py` 0.29.0. A first attempt matched marker syntax raw and false-positived on two of the four real boards, which discuss the syntax rather than mean it; stripping code fences and inline spans first separates the two cleanly.

260726 · JL ruled the door: `①` is the single source of entry, `③` is a sub-skill it calls. This face carried the contradiction and now carries the ruling, because its Boundary already claimed the contract between the two. The step table had no step 0, which is exactly the seam that was missing. Amended `QA1` (the call-flow figure replaced the peer-channel figure), `QA2`, `QA6`, `QA7`. Implemented the same day in `haipipe-paper-enter` 0.6.0, `haipipe-paper-stage` 0.8.0 and the router 0.4.0.

260726 · Created when JL asked for `/haipipe-board` to be on the map. Rebuilt around the collaboration rather than the tool: two skills, one file, disjoint regions, and the two asymmetries (only `③` writes `⑧` from a click; only `①` writes `⑦`). Absorbed the five ownership seams and four running-work seams as `QA8` and `QA9`.
