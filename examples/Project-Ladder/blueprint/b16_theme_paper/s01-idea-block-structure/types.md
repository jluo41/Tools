# Types of an Idea Block

The shared Block Structure contract owns these four lists. Names in 〈 〉 are proposed semantic contracts, not registered execution values. The `for:` and `holds:` lines give the scope and owner; they do not migrate existing records.

example: examples/Project-Ladder/paper/Idea-Example

## Job group type

### 〈Research topic〉
for: Organize a portfolio by a bounded research question.
holds: Multiple candidate Idea Jobs in one direction; a Job has one primary group and may reference related candidates.

## Job type

### Idea Job
for: Develop one candidate idea.
holds: One canonical Idea Card, evidence pointers, assessments and selection. hai-ideation recognizes ideation.yaml kind: ideation-unit and layout: idea-job; there is no asserted job-type: idea field.

## Task group type

### 〈Framing〉
for: Sharpen the candidate question.
holds: Bounded question, hypothesis and alternatives.

### 〈Assessment〉
for: Evaluate the candidate.
holds: Novelty, feasibility and fit questions; skills are methods inside these Tasks.

### 〈Decision〉
for: Prepare the human selection.
holds: Comparative evidence and development recommendation, followed by the original human selection receipt.

## Task type

### ideation
for: Develop or assess an Idea.
holds: A bounded assessment question, source-linked evidence and review receipts; owned by hai-ideation.

### draft
for: Write a separately commissioned prose Page.
holds: A Page with the shared draft contract; it does not replace the Idea Card or scientific selection.
