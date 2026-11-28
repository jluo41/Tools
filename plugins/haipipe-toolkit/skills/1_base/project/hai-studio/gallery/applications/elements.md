# Requirements of a Application topic

The class of every topic in a Knowledge Block's Application band (s3N); s05 Block Structure: Knowledge names it. The band is the type: every topic in it has these top
buttons and left tabs. `## ` is a top button, `### ` a left tab under it; the type's right side shows the
requirement, a topic's right side shows its real page. Try explaining, Draw, Map and Slides come from the base
type; this file writes only the type's own Page tabs.

base: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/base-types/learning
instances: article[id="s31-use-cases-boundaries"]

## Page

### A decision to explore
what: The real decision: when to use the thing, and when not.
why: An application is a choice with a boundary, not a feature list.
from: the `## A decision to explore` section
must:
- the first left tab
- both sides: where it helps and where it does not
check: by eye: a boundary is named

### Connect the topics
what: Which Resources and Methods topics the decision draws on.
why: The application is built from what the learner already read.
from: the `## Connect the topics` section
must:
- a link to each topic it uses
check: `build_studios.py --check`: every link opens

### A bounded practice proposal
what: A small practice that would test the decision, as a plan.
why: A learner sees how to try it without a Job being implied.
from: the `## A bounded practice proposal` section
must:
- marked as a plan; no Run or result is implied
check: by eye: no receipt or result is claimed

### What that practice could establish
what: What the practice would show, and what it would not.
why: The limit of a practice is decided before running it.
from: the `## What that practice could establish` section
must:
- what it shows and what it cannot show
check: by eye
