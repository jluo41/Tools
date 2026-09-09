# Anti-slop adapter provenance

The Haipipe adapter intentionally keeps the external repositories in
`Tools/references` as independently updateable sources. The active adapter is
a small, reviewable port rather than a runtime import of those repositories.

## Material adapted here

| Active file | Upstream material | License |
| --- | --- | --- |
| `cli/anti_slop.py` | [`aashaexo/soundshuman`](https://github.com/aashaexo/soundshuman): rule-driven detection, pattern-density score, and prose statistics | MIT; Copyright (c) 2026 aasha |
| `cli/anti_slop.py` | [`Aboudjem/humanizer-skill`](https://github.com/Aboudjem/humanizer-skill): deterministic preservation-sensitive fact comparison | MIT; Copyright (c) 2026 Adam Boudjemaa |
| `ref/anti-slop-rules.json` | `soundshuman/rules/slop-rules.json`, which records its own adaptations from `blader/humanizer`, `hardikpandya/stop-slop`, and `brandonwise/humanizer` | MIT notices retained by the source project |

The corresponding upstream repositories and their license files remain under
`Tools/references`. The active files above preserve the upstream copyright
notices in their headers/metadata and add HAI-specific behavior: line/column
spans, Python stdlib execution, Page-safe masking, and a no-write boundary.

The copied rule data also carries the upstream notices named by
`soundshuman/LICENSE`: aasha (the adapting project), blader, Hardik Pandya,
and brandonwise. Its pattern research notes derive from Wikipedia's
[“Signs of AI writing” guide](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
maintained by WikiProject AI Cleanup, under CC BY-SA; the rule file is
therefore accompanied by this attribution rather than presented as original
HAI research. The ten screenshot repositories remain separately credited in
`Tools/references/anti-ai-writing-skills.md`.

## What was not copied into the active worker

The external `SKILL.md` instructions are comparison material, not a second
authority. Their automatic rewrite/fix commands, detector thresholds, and
voice rules are not invoked by `haipipe-writing`. A Paragraph Run may use one
audit report, then the Run worker decides whether a bounded revision is needed;
`wdiff.py` remains the only writer of the change record and the Page promoter
remains the only Page write path.

## MIT permission notice

Permission is hereby granted, free of charge, to any person obtaining a copy
of the adapted material and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the copyright notices and this permission
notice being included in copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
