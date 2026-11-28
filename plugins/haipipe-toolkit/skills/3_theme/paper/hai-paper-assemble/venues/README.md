# venues/: how to PRINT for one venue

One folder per venue (JL 261122: "for each venue, you can make a module folder"). How to WRITE for a venue (its
style, its observed patterns, its desk rules) is a different thing and lives in `skills/3_theme/paper/venue/`
(the `playbook-*` folders and the `bank/`); each venue folder here names its playbook in `profile.toml`
(`venue_pack`) when it has one.

```text
venues/<series>/
├─ profile.toml     the settings the series shares: fonts, headings, labels, citations, [latex] for the PDF,
│                   then one [journals.<journal>] table per journal holding only what that journal changes
├─ venue.py         only when a setting cannot say it: the venue's own Word shape
├─ <style>.bst      a bibliography style the venue ships (copied into the LaTeX room)
└─ test_<venue>.py  what this venue must print
```

A paper picks its folder with `[paper] venue_profile = "<series>"` or `"<series>/<journal>"` in `paper-build.toml`
(`"nature/nature-machine-intelligence"`), and may override any key in `[profile]` and `[profile.latex]`. The order is
series, then journal, then paper; a table such as `[latex]` merges key by key. One reader does it for every script:
`scripts/venue_profile.py` (JL 261123: "we might want the things to be the series").

## Rules

1. A difference a setting can express stays a setting in `profile.toml`. A new journal of a series that has a folder is
   a `[journals.<journal>]` table there, never a new folder.
2. Shared behaviour (LaTeX parsing, tables, figures, equations, references) never moves into a venue folder.
3. The shared scripts in `scripts/` never name a venue; `tests/test_venues.py` fails if one does.
4. `layout` in `profile.toml` names the folder whose `venue.py` shapes the Word file: a venue may reuse another
   venue's layout (`lancet-public-health` prints with `layout = "jama-internal-medicine"`); `"generic"` has none.

## The venue.py contract

`latex_room_to_docx.py` runs `venues/<layout>/venue.py` in its own namespace (`_load_part`), so the Word helpers
(`add_text`, `add_heading`, `add_events`, `latex_to_text`) and the paper's config are in scope. It may define:

```text
build_word(raw_master, evidence) -> (docx_path, manifest_path)   the whole Word file, in place of the generic one
```

Anything else in `venue.py` is the venue's own helper. A new hook is added here first, then called by the shared
builder as "if the venue defines it, call it, else the default", never by the venue's name.

## What the LaTeX lane reads ([latex] in profile.toml)

```text
title_block             maketitle · center   center: a \begin{center} title block that build_word parses
section_headings        ["Introduction", …]  a \section{..} added where a page has none
abstract_as_written     true · false         keep the page's own \section*{Abstract} (no abstract environment)
supplement_float_names  ["eTable", "eFigure"] supplement floats restart as eTable 1, eFigure 1
```

The other `[latex]` keys are in `ref/venue-format.md` § Venue profiles.
