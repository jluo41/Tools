# Insight and handoffs
state: 🟡 PARTIAL
owner: JL

## Opening

How does Insight turn accepted Results into a signed interpretation that another Job can use?

**Where this Page sits:** Insight consumes evidence from Task and Discovery and can hand signed Wisdom to Design.

**Why it matters:** Interpretation, evidence provenance, and a person's decision stay visible as separate records.

## Content

### 1 · Insight ownership
**Scope**: resources and interpretations belong to Insight.
```text
Task + Discovery Results ──▶ Insight questions and Runs
                                   │
                                   ▼
signed Wisdom ──▶ Design Brief
```

#### 1.1 · Family inventory
(Keep Insight separate from the families that consume its handoff.)
The Insight family contains 8 `SKILL.md` files under `insight-family`. `haipipe-insight` owns the domain entry; `insight-workflow` owns its selected Run graph, Results, receipts, and signed handoff settlement.

#### 1.2 · Evidence and questions
(Tie every interpretation to its source Run and registered question.)
Insight records resource scope, questions, partitions, evidence dependencies, and DIKW resources. It consumes exact Supporting Run identities and creates owner-native Results for its own interpretations.

#### 1.3 · Design handoff
**Scope**: Insight settles the evidence-led handoff; Design owns its Brief.

#### 1.4 · Person-signed Wisdom
(The person settles the handoff before Design consumes it.)
Insight records a signed, versioned Wisdom handoff. Design consumes that exact signed version as input and owns its own design Brief, Commission, Generate, and Verify Runs.

#### 1.5 · Preserve the boundary
(Do not turn Design into an Insight step or combine the Jobs.)
Insight does not produce design artifacts. Design does not rewrite the evidence interpretation. Each family retains its own Run identities, Results, and acceptance rules.

#### 1.6 · Workflow and Runs
**Scope**: the Insight controller coordinates owner-native Runs without renaming them.

#### 1.7 · Follow the current graph
(Read the Run workflow contract for concrete dispatch and closure.)
The current controller defines bounded Run Specs, dependencies, receipts, and completion rules. See `insight-run-workflow` and the shared `haipipe-run`.

## Aims
### A1 · Insight ownership
- 🔨 A1.1 · Insight and Design remain separate first-class families.
  **Done when:** Insight's exact signed handoff and Design's independent Run owner are linked and checked against their current contracts.
  **Now:** Ownership and direction are mapped.
