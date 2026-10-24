# Changelog · haipipe-paper-related

## [0.1.0] · 2026-10-19 · The closest work, in the s10-s19 band

JL 261019: "for the related work we can do things like s10-related-work, and after that, we have s11 s12, etc";
"should we have haipipe-paper-related? ... it is different from the literature"; "we can use
haipipe-paper-related, to find the most related papers".

- New skill. A paper Board's related work is the 10 to 30 papers closest to ours, sorted into at most nine
  types: `studio/s10-related-work-map/` maps them all beside our paper; s11 to s19 read one type each, paper by
  paper, with excalidraw-read.
- `scripts/related_map.py`: the s10 drawing, generalized from Paper-LLMRecPhy-Jama's s05 builder (2026-10-13). Every
  frame but the map is optional; a Closest row the face does not place is drawn red.
- `scripts/related_topics.py`: `map` and `group` scaffold the topics with forwarding builders; `check` names
  every Closest row not placed or not typed; `band` moves an older Board's related-work topics into s10-s19 in
  one pass (folders, files, soft Runs, every mention, `renamed-from:`).
- `ref/map-face.md`: the s10 face's yaml blocks, from the LLMRec example.
- First Board moved: Paper-LLMRecPhy-Jama, s05 to s10 became s10 to s15.
- First new Board: Paper-AgreeablePrescriptionDiscretion (MISQ), by a fresh agent: 14 closest papers in 3
  types (s11-s13), all placed, check exit 0. Its 14 notes, fixed before release:
  - `map` and `group` add the six paper columns to a six-column table (`ensure_columns`); the SKILL lists them.
  - `group` writes `feeds` (`s10, s1N`) on its rows, so rows are written first with `feeds` empty.
  - `group` writes each paper's `ref` (authors from its DOI's record at doi.org, arXiv too; `--offline`).
  - `says` is the first sentence, never cut at U.S., e.g. or an initial, no trailing semicolon.
  - A type name with a comma is refused (`bears on` is split on commas).
  - s10 names its acts (Act 1 · Where our paper sits; Act 2 · Up close; Act 3 · Each type), so check.py's ③ passes.
  - `map`, `group` and `band` redraw the s00 index (generated, never hand-edited).
  - Feed is a proposal in s10's Open: never an edit to an agreed s01 or another owner's Section; Literature
    Review stands for Related Work at a venue without one.
  - `read` takes the full Run folder when a short address is ambiguous; background rows feed their Section;
    `paper.txt` stays out of the Board; a reading needs a top-level `key:`; a repo copy does not change a license.
- A second fresh agent (a scratch copy of the MISQ Board) ran map, group, check and the Feed again: exit 0, the
  Feed written as proposals in s10's Open. Fixed from it: the map's across axis now clears a crowded top left;
  a DOI record is cleaned (&amp;, "Dr.", a footnote mark); `ref` keeps six authors, then et al. (the docs said
  every author); the limit is check.py's 200 words; a face names the Section that positions the paper, not always
  Related Work.
- LLMRec done first (JL 261019: "It's first do the LLMRec"), which added: `group --background` (a read type of
  Shared background rows, never on the map); `feeds` (every row's s10-s19 feeds, from the topics; `check` warns
  when they drift); a paper whose short name starts two rows is named by its whole item (two Chen et al. 2026);
  `band` also moves a range's second end (s06-s10 had become s11-s10).
- Three or four types (JL 261019: "merge them into three to four, we just want to keep the most relevant, and the
  studies close to us"): LLMRec's seven became s11-s14, 42 papers in topics became 24, readings renumbered with their
  papers, the old topics and seven readings kept in `studio/_archive/`. `check` keys papers by their whole item, so two
  Chen et al. 2026 papers in two types are not one paper in two types.
