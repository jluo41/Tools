# Anti-AI writing skill references

This shelf records the ten skills shown in the external recommendation image
"AI 写的文字不能看？十大去 AI 味 Skill 推荐". It is a comparison and
provenance shelf, not a runtime bundle: do not apply all ten to one paragraph.

The Haipipe writing contract remains authoritative for the outline, evidence,
claims, reader order, Writing DNA, and the `✎` trail. An external skill may be
used as one optional surface-style audit after a draft, but it must not invent
facts, reorder the approved argument, or replace the Haipipe checkers.

## Ten-item map

| # | Screenshot label | Upstream source | Local reference | Exact skill file |
| ---: | --- | --- | --- | --- |
| 01 | `stop-slop` | [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | [`references/stop-slop`](stop-slop) | `SKILL.md` |
| 02 | `no-ai-slop` | [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) | [`references/no-ai-slop`](no-ai-slop) | `skills/no-ai-slop/SKILL.md` |
| 03 | `humanizer · blader` | [blader/humanizer](https://github.com/blader/humanizer) | [`references/humanizer-blader`](humanizer-blader) | `SKILL.md` |
| 04 | `unslop` | [cursor/plugins](https://github.com/cursor/plugins) | [`references/cursor-plugins`](cursor-plugins) | `pstack/skills/unslop/SKILL.md` |
| 05 | `slopbeth` | [ehmo/slopkit](https://github.com/ehmo/slopkit) | [`references/slopkit`](slopkit) | `skills/slopbeth/SKILL.md` |
| 06 | `humanizer · Adam` | [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | [`references/humanizer-adam`](humanizer-adam) | `skills/humanizer/SKILL.md` |
| 07 | `deslop` | [stephenturner/skills](https://github.com/stephenturner/skills) | [`references/stephenturner-skills`](stephenturner-skills) | `deslop/SKILL.md` |
| 08 | `anti-slop` | [elithrar/dotfiles](https://github.com/elithrar/dotfiles) | [`references/elithrar-dotfiles`](elithrar-dotfiles) | `.agents/skills/anti-slop/SKILL.md` |
| 09 | `humanize` | [aashaexo/soundshuman](https://github.com/aashaexo/soundshuman) | [`references/soundshuman`](soundshuman) | `SKILL.md` |
| 10 | `anti-ai-slop-writing` | [jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing) | [`references/anti-ai-slop-writing`](anti-ai-slop-writing) | `skills/anti-ai-slop-writing/SKILL.md` |

`deslop` also has a vendored comparison snapshot at
`references/auto-empirical-research-skills/skills/45-stephenturner-skill-deslop`.
The standalone submodule above is the current upstream reference; the
snapshot remains useful for historical comparisons.

## Haipipe handoff

For a paragraph Run, use this order:

1. Realize the approved outline/evidence slice with `haipipe-writing`.
2. Apply the frozen Writing DNA packet, if one was supplied.
3. Select at most one external anti-slop reference for a focused audit.
4. Preserve facts, citations, numbers, argument order, and the Haipipe `✎`
   record; then run the normal `wdiff.py`, holes, and coverage checks.

These references are not copied into the active Haipipe skills. They remain
separately updateable submodules so upstream changes do not silently change a
writing Run.
