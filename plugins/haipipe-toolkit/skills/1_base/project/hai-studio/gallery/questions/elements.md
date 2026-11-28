# Requirements of a Question topic

The class of every topic in a Knowledge Block's Question band (s4N); s05 Block Structure: Knowledge names it. The band is the type: every topic in it has these top
buttons and left tabs. `## ` is a top button, `### ` a left tab under it; the type's right side shows the
requirement, a topic's right side shows its real page. Try explaining, Draw, Map and Slides come from the base
type; this file writes only the type's own Page tabs.

base: plugins/haipipe-toolkit/skills/1_base/project/hai-studio/base-types/learning
instances: article[id="s41-agent-text-to-a2ui"],article[id="s42-who-writes-the-json"]

## Page

### The question
what: The learner's question, as asked.
why: The answer is judged against the real question.
from: the `## The question` section; the face's **Asked:** line
must:
- the first left tab
- the learner's own words
check: by eye: matches the face's **Asked:**

### Short answer
what: The answer in a few sentences.
why: A learner who reads only one tab gets the answer.
from: the `## Short answer` section
must:
- the second left tab
- answers the question directly
check: by eye

### 〈part〉
what: One part of the full answer: a place in the system, a step, or a follow-up question.
why: The detail behind the short answer, one part at a time.
from: one `## 〈part〉` section
must:
- named by what the part covers; a follow-up reads `Follow-up: 〈question〉`
- a source link where the part states how A2UI behaves
check: by eye
