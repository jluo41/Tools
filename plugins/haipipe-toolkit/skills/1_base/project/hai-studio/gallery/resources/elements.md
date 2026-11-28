# Requirements of a Resource topic

The class of every topic in a Knowledge Block's Resource band (s0N); s05 Block Structure: Knowledge names it. The band is the type: every topic in it has these top
buttons and left tabs. `## ` is a top button, `### ` a left tab under it; the type's right side shows the
requirement, a topic's right side shows its real page. Try explaining, Draw, Map and Slides come from the base
type; this file writes only the type's own Page tabs.

base: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/base-types/learning
instances: article[id="s01-official-sources"]

## Page

### Reading route
what: Which source to read first, and in which order.
why: A learner starts from the right page instead of the whole site.
from: the `## Reading route` section
must:
- the first left tab
- the order, and which later topic uses each source
check: by eye: every source below is placed on the route

### Resource 〈n〉 · 〈source〉
what: One source: its original link, version and exact chapter, page or time point.
why: Other topics cite this one entry, so a source has one owner.
from: one `### Resource 〈n〉 · 〈source〉` under `## Source records`
must:
- one tab per source, numbered in reading order
- the original URL, the version, the exact location; an unknown location stays unknown
- which topics use it
- the tab is named in full, `Resource 〈n〉 · 〈source〉`, never `R〈n〉`
- one official picture taken from the source itself, with one sentence on what it shows
- the picture sits in the topic's `assets/` and has a row in `assets/SOURCES.md` with its URL and license; no license, no copy
- ends with `🔍 **Look for:**` (where to look in the source) and `✅ **You know it when:**` (how the learner checks themself)
check: `build_studios.py --check`: every link opens; every file in `assets/` other than `SOURCES.md` has a row in `SOURCES.md`

### Version choice
what: Which version every topic of the Block follows, and why.
why: Sources of different versions disagree; the Block reads one.
from: the `## Version choice` section
must:
- one pinned version, named
check: by eye: the version matches the sources' versions
