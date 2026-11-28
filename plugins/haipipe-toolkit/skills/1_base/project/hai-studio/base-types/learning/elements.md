# Base type: learning topic

The parts every learning Studio Type shares: the Page button and its last tab, Try explaining, and the Draw, Map and
Slides buttons. A type starts from it with `base: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/base-types/learning`
and writes only its own Page tabs; they come before Try explaining.

## Page
what: The topic's learning page, one left tab per `## ` section of `delivery/learning.md`.
why: A learner reads one part at a time, in order.
from: `sNN-〈topic〉/delivery/learning.md`, split into `delivery/page/` by `build_studios.py`
must:
- code, JSON and messages are text in code blocks, copied from the source with its license named, never a screenshot
- a screenshot is kept for a diagram; one that holds text is captured at 2x or more and never shrunk below readable size
- each tab starts with one bold sentence that answers it
- then one item per line in a list, never a paragraph that hides several items
- each item starts with its emoji, one meaning across the Block: 🆕 🧱 🔢 🗑️ opens, lays out, sets a value, removes · 👆 📤 📥 🏠 user action, sent, received, stays on the device · ✏️ 🧰 📂 what to change, which tool, where in the example · 💡 ⚠️ ✅ ❌ key idea, boundary, shows, does not show · 📖 🔗 what to read, who uses it
- a table keeps an emoji in each header cell
check: by eye on each Page tab: no picture of code; every picture's text reads at 100% zoom; a bold first line, a list instead of paragraphs, one emoji per item with the meanings above

### Try explaining
what: The learner's exercise: explain the topic back in their own words.
why: Explaining is how a learner finds what they did not understand.
from: the last `## Try explaining` of `delivery/learning.md`
must:
- always the last left tab
- one concrete task, never "summarize the topic"
check: `build_studios.py --check`: learning.md ends its sections with `## Try explaining`

## Draw
what: The topic's one drawing: the idea drawn as a pattern, not its text listed.
why: A learner sees the shape of the idea before reading it.
from: `sNN-〈topic〉/sNN-〈topic〉.excalidraw`, built by `build_studios.py`

### 〈topic title〉
what: The topic's drawing, named by the topic's title.
why: One canvas per topic keeps the drawing and the page in step.
from: `sNN-〈topic〉/sNN-〈topic〉.excalidraw`
must:
- one tab, named by the topic's title
- English labels, at least one arrow
- one concrete example carried through the whole drawing
- a picture per actor (a person, a phone, a server, a cloud for an LLM API) with its plain role in its label
- a change drawn as before and after, a flow over time as a timeline with one column per actor
- what is new is green; what stays is drawn as before
- one value traced from where it is written to what the reader sees
- one closing question the picture answers
check: `build_studios.py --check` confirms the drawing and picture files; by eye: actors have pictures, new parts are green, one value is traced

## Map
what: The topic's concept map.
why: The parts of the topic and how they connect, at a glance.
from: `sNN-〈topic〉/sNN-〈topic〉.mindmap.md`

### 〈topic title〉
what: The concept map, named by the topic's title.
why: One map per topic.
from: `sNN-〈topic〉/sNN-〈topic〉.mindmap.md`
must:
- one tab, named by the topic's title
check: the file exists and opens as a map

## Slides
what: The topic's illustrated deck, built from its drawing.
why: The same topic, ready to present.
from: `sNN-〈topic〉/delivery/deck/sNN-〈topic〉.slides.html`

### 〈topic title〉
what: The deck, named by the topic's title.
why: One deck per topic.
from: `sNN-〈topic〉/delivery/deck/sNN-〈topic〉.slides.html`
must:
- one tab, named by the topic's title
check: the html and pptx decks exist
