paper — open issues
=====================

Tracked here so future sessions can pick them up without re-discovering.


Roadmap: draw the plan, do not hand-write a mechanics diagram
---------------------------------------------------------------

JL 260824, on seeing the first minted `SD02-roadmap`: "roadmap 比较像是一个 plan,
能不能每次创建它的时候,都自动把那个图画好?" Deferred by JL to a later session.

- [ ] The Diagram section of a freshly minted Roadmap is currently AUTHORED BY HAND
      and shows the page type's LAP MECHANICS (Seed gap → direction row → release →
      dispatch → QA file). That picture is identical on every Roadmap ever minted, so
      it teaches the reader the contract, not the plan.
- [ ] What the reader actually wants from a plan page is THIS paper's campaign: which
      rows exist, which E-row each serves, what is released versus proposed, what is
      running, and what order the laps fall in. Every one of those facts is already a
      column on the Direction Board, so the picture is DERIVABLE — it should be
      generated from the rows, never transcribed beside them.
- [ ] Sketch of the generated shape (one row per direction, status glyph, serves-arrow
      into the Seed's E-rows):

      ```text
      SD01 §6      R1 claim novelty   ⬜ proposed   6 claim QAs
        E1 ◀────────────┤
        E2 ◀────────────┤
        E3 ◀────────────┘
        E6 ◀── R2 spread benchmark    ⬜ proposed   1 search
      ```

- [ ] Consequence for the contract: if the diagram becomes generated, the Roadmap's
      Diagram section stops being prose the author owns and becomes a DERIVED surface
      like `board/` HTML — regenerated on every build, never edited in place. Decide
      whether that belongs in `build.py` (a page-type-aware renderer) or in a small
      `haipipe-plugin-*` the page declares, and say so in the contract before writing
      any code.
- [ ] Check whether Collection wants the same treatment: its laps carry dates, rows,
      and landed paths, which is also a picture (a timeline) rather than a paragraph.
      Do not generalize past these two without a third real case.

Receipt teeth for the establish loop (260827, from the lap-L1 field test)
-------------------------------------------------------------------------

- [ ] Three grep-shaped checks, mirroring the application board's set-diff hardening:
      ① a Roadmap page containing a `▶️ released`/`🔵 running`/`✅ landed` row must have
      a Log row recording the release (the G2 receipt); ② every `landed` QA path on a
      Collection lap must exist on disk; ③ every Seed E-row cite written by a settle
      must exist on disk and match the lap's path (one string, three places).
- [ ] Placement is undecided: check.py is the generic board engine and these are
      paper-family rules — decide between a page-type-aware rule pack the checker loads
      from the contract, or a small board-local script the paper board declares.
- [ ] Each tooth must be proven to FAIL first on a known-broken sample; the 260827
      pre-repair SD02 (released rows + "Nothing released" Log) is the stored specimen
      for tooth ①.
