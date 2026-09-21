# Shared work contracts
state: 🟡 PARTIAL
owner: JL

## Opening

How do Board, Page, and Run keep the toolkit's shared work traceable?

**Where this Page sits:** It defines the shared contracts used by the Jobs on this Board.

**Why it matters:** Every family can exchange work without inventing a second identity or evidence system.

## Content

### 1 · Shared owners
**Scope**: one source of truth for navigation, content, and execution.
```text
Page source ──registered by──▶ Board
human + agent ──co-write──▶ Page Writing Run
owner Skill ──executes──▶ Run ──returns──▶ Result
```

#### 1.1 · Board owns navigation
(Keep the Board as a projection of authoritative Page and Run records.)
Board owns the container, Job grouping, Page roster, navigation, and aggregate build. A Board points to Page sources and presents their state; it does not copy their authority. See `haipipe-board`.

#### 1.2 · Page owns readable content
(Keep each Page's content and lifecycle with its Page owner.)
Page owns its Folder, readable source, evidence workspace, and Page lifecycle entry. A Board registers that same Page rather than importing a second copy. See `haipipe-page`.

#### 1.3 · Run owns bounded execution
(Keep a Run's identity and Result with the skill that executes it.)
Run records one bounded commission, its Steps or attempts, and its Result. A Workflow lists Run Specs and instances with dependencies and routes. See `haipipe-run` and the `skill-structure`.

#### 1.4 · Human-AI collaboration
**Scope**: one shared Page Run, owner-native evidence Runs, and a separate acceptance decision.

#### 1.5 · Structure Run
(Co-develop the Page plan in one durable Run.)
`rp-struct-01` is a shared human-AI Run for SHAPE and SURVEY. Record participants on the Run and contributors on each Step. The person closes the structure contract before Section or paragraph writing Runs are proposed. See the `page-writing-run`.

#### 1.6 · Writing Runs
(Keep each human decision within its selected scope.)
After structure closes, use a Section Run or a fixed paragraph Run. Feedback and revision Steps stay inside that Run; the person accepts the exact scope and candidate. An independent goal gets a new Run.

#### 1.7 · Evidence and release
(Keep evidence production separate from Page writing and release.)
Code, search, data, rendering, and evidence production use their owner-native Task or Discovery Runs. Page Content adopts accepted wording after its planned Runs and required Results are ready. Page CHECK and release remain distinct gates.

#### 1.8 · Boundaries between Jobs
**Scope**: producers return Results; consumer Pages interpret and compose them.

#### 1.9 · Preserve native ownership
(Do not rename or re-home a Run at a handoff.)
Task and Discovery Results can become Supporting evidence for an Insight or Page. The consumer owns any Local Run that transforms an input for its own question. Insight, Design, Paper, and Display keep their own contracts and approval gates.

#### 1.10 · Use Run language
(Name actual Run Specs and instances, not imagined stages.)
Each Workflow is a list of Runs with explicit dependencies and routes. Controller coordinates and legacy `phase` fields are not additional Runs. The owning skill supplies exact Run names and closure rules.

## Aims
### A1 · Shared owners
- 🔨 A1.1 · The shared contracts and human-AI handoffs are explicit.
  **Done when:** Board, Page, Workflow, Run, Result, evidence, and acceptance ownership link to their current source contracts.
  **Now:** Initial map drafted from the current skill tree.
