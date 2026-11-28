---
title: Each learning Band is one Studio Type; Connections and Applications becomes Applications
date: 2026-11-27 22:33
aim: Every b18 Band has one Studio Type in b18's own Studio Type band (s71 to s75); each topic names its type and passes type_follow check; the s3N Band reads Applications.
closed: true
plan:
- do: add
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/trace/261127/2233_band_is_studio_type.md
  what: this trace's own record, written first
- do: edit
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/board.md
  what: bands line renames s3N to Applications, adds s7N Studio Type; link titles follow
- do: edit
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/_studio_groups.txt
  what: Applications; Studio Type group last
- do: edit
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/build_studios.py
  what: Applications band; type topics s71 to s75; each topic keeps check_type; check runs type_follow
- do: edit
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/s31-use-cases-boundaries/s31-use-cases-boundaries.md
  what: title and Tags read Applications
- do: edit
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/s21-tracing-interaction/delivery/learning.md
  what: rewritten in the Methods shape, Where you start then numbered steps then Try explaining
- do: add
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/s71-studio-type-resources/
  what: Studio Type for s0N Resources (face, elements.md, generated requirement pages and views)
- do: add
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/s73-studio-type-methods/
  what: Studio Type for s2N Methods
- do: add
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/s74-studio-type-applications/
  what: Studio Type for s3N Applications
- do: add
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/s75-studio-type-questions/
  what: Studio Type for s4N Questions
- do: edit
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/sNN-*/studio-views.json
  what: every learning topic names its type (check_type); generated Page tabs rebuilt
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/knowledge/hai-knowledge/SKILL.md
  what: a learning Band is one Studio Type; five Bands incl. Questions; Applications
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/knowledge/hai-knowledge/CONSTITUTION.md
  what: new article, Band is Studio Type; A04 and A06 band names follow
- do: edit
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/ref/topic-numbering.md
  what: a theme may bind each Band to one Studio Type (Knowledge does)
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/
  what: Applications in builder, face, mind map; rebuilt drawing and structure page
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/delivery/page-spec/studio-bands-by-block-type.md
  what: Knowledge row reads Applications
- do: edit
  path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1919_english_studio.md
  what: band name sweep
- do: edit
  path: examples/Project-Ladder/knowledge/b18_a2ui_learning/trace/261127/1919_english_studio.md
  what: band name sweep
- do: edit
  path: plugins/haipipe-toolkit/skills/2_work/work/workbench-work/ref/topics.md
  what: band name sweep
---

# Each learning Band is one Studio Type

## Request

> we might want a band to be a studio type, which is much easier, how do you think?

> 🔗 Connections and Applications. I want to make this to be a Application? not Connection. let;s try to make the Band to the a studio type

> I think we might want to merge the Methods and Concepts to just Methods.

## Steps

1. Renamed the s3N Band to 🎯 Applications in every file that named it, traces included.
2. Merged Concepts into Methods. Moving s11 to s23 was refused, so s11 keeps its ID: `bands:` names s1N and
   s2N both 🧭 Methods (the Studio page groups by `bands:` before **Tags:**), and its Tags read Methods.
3. Wrote four Studio Types in b18's own s7N: s71 Resources, s73 Methods, s74 Applications, s75 Questions
   (s7K defines the s(K-1)N Band). Shared tops: Page, Draw, Map, Slides; Page ends in Try explaining.
4. Rewrote s11 and s21 in the Methods shape: Where you start, numbered steps, Try explaining.
5. `build_studios.py` writes each topic's `check_type` and Check view, and its check runs the follow check.
6. Rules: hai-knowledge SKILL.md and CONSTITUTION A07; hai-studio `ref/topic-numbering.md` allows a theme to bind
   each Band to one type. b17 s05 builder, face, mind map and studio-bands-by-block-type.md follow.

## Checks

- `build_studios.py --check`: every topic follows its Band's type.
- `type_follow.py check b18`: 7 topics ✅; a probe without `Where you start` fails as `Page: no left tab Where you start`.
- `type_requirements.py --check` on s71, s73, s74, s75 ✅; `placeholder_check.py` 0 bare slot names.
- s05 `build_structure.py --check` ✅; `skill_text_check.py` ✅.
- Live page on 5623: groups Resources, Methods (s11 s21 s22), Applications, Questions, Studio Type.

## Correction: types live in the Blueprint

> we should not have things here, becuase it is not the blueprint, only blueprint will contain the studio types, do you know? so we might still put it in b17

> I think we defiend the studio structure here. (s05 Block Structure: Knowledge)

7. Moved the four types out of b18 into b17's Studio Type band: s70 Resources, s75 Methods,
   s77 Applications, s79 Questions (the free s7N numbers, in Band order). `instances:` lists
   b18's topics by exact ID, so b17's own s01 to s04 are never marked.
8. b18 has no Studio Type band again; its topics' `check_type` point at b17. s05's Studio names each Band's type.
9. Checks: b18 `build_studios.py` ✅ (7 topics follow); s05 `--check` ✅; four `type_requirements.py --check` ✅;
   placeholder, topic titles, skill text ✅. b17's follow check still fails s01, s02, s04: already open in hai-studio A10.
   Live: b18 shows Resources, Methods, Applications, Questions; b17 Studio Type shows s70 s75 s77 s79 among the Work types.

## Correction: one run from s71, Knowledge last

> now for the s70, etc, why it is that way???? please remove the Knowledge and older it from the buttom, Don;t split them.

> wait!!!! we are starting from s71!!!!! not s70

> you can go beyong, like s80, s81, s82, etc, until s98, get it?

10. The Studio Type topics run s71 to s80 with no gaps: s71 Block Structure, s72 Block Job UI Preview, s73 Report,
    s74 UI Plugin, s75 Skills (was s76), s76 Theme Guide (was s78), s77 Resources, s78 Methods, s79 Applications,
    s80 Questions. "Knowledge" is out of the four names. Every full path was rewritten (111 files); old traces keep
    their history words.
11. Code: `studio_tabs.render` and `studio_types.element_about` treat any `sNN-studio-type-*` as Studio Type, whatever
    its decade; `topic_titles_check.py` the same; `test_studio_bands.py` pins s71 to s80 with no gaps.
12. s72's own builder (`build_type_pages.py --type-only`) regenerated its files after `type_requirements.py` had
    overwritten its views; restored from HEAD first.
13. Checks: b17 `checks/run.py` has no failure that a clean HEAD worktree lacks (six stale Skills check pages fixed);
    s72 `--check` equals HEAD (6 open preview parts); hai-studio tests: only the five failures HEAD already had;
    studio tabs tests 36 passed; titles, placeholders, skill text ✅; b18 7 topics follow; s05 `--check` ✅.
    5623 restarted (`wb.py restart`); the page lists s71 to s80 in order under Studio Type.
