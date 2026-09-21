# External evidence work
state: 🟡 PARTIAL
owner: JL

## Opening

How does Discovery find and assess external evidence while keeping each source traceable to its Run?

**Where this Page sits:** Discovery is an independent evidence-producing Job.

**Why it matters:** A consumer can tell what was searched, which source was reviewed, and which finding came from that Run.

## Content

### 1 · Discovery ownership
**Scope**: external source work stays with Discovery.
```text
source scope ──▶ Search / Review / Synthesize Runs
                       │
                       ▼
                evidence Result ──▶ consumer Job
```

#### 1.1 · Family inventory
(Keep search, source review, and synthesis under their Discovery owners.)
The Discovery family contains 16 `SKILL.md` files under `discovery-family`. `haipipe-discovery` routes work to its search, review, and synthesis specialists.

#### 1.2 · Results remain traceable
(A consumer cites the exact source Run and Result.)
Discovery returns owner-native Run Results. A consumer Page may bind one as Supporting evidence and create a Local Run when it needs page-specific extraction or normalization. Discovery does not write consumer prose.

#### 1.3 · Workflow and Runs
**Scope**: each Run has an owner, source scope, and observable Result.

#### 1.4 · Follow the Discovery owner
(Use the current Run Specs and stop rules.)
The Discovery workflow owner defines which Runs are needed, their dependencies, and when the evidence is sufficient. The labels Search, Review, and Synthesize describe capability families; the actual Workflow lists the bounded Runs chosen for a commission.

#### 1.5 · Route findings to consumers
(Pass evidence with provenance, not a detached summary.)
Task can supply internal analyses; Discovery can supply external literature or source checks. Insight and Ideation may consume accepted Results, while Page and Paper bind evidence to their own claims.

## Aims
### A1 · Discovery ownership
- 🔨 A1.1 · Discovery inputs, Run ownership, and Result handoffs are clear.
  **Done when:** The Discovery router, Run owner, and consumer evidence boundary all resolve to canonical source files.
  **Now:** Family root and handoff are mapped.
