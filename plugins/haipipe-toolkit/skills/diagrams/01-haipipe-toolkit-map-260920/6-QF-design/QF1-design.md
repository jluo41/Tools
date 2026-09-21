# Design production
state: 🟡 PARTIAL
owner: JL

## Opening

How does Design turn signed Insight into a verified creative artifact?

**Where this Page sits:** Design receives person-signed Wisdom from Insight and can pass visual work to Display or a consuming Page.

**Why it matters:** Creative choices have their own owner, evidence, and acceptance record.

## Content

### 1 · Design ownership
**Scope**: a Brief and Design Folder own the creative work.
```text
signed Insight ──▶ Brief ──▶ Commission ──▶ Generate ──▶ Verify
                                                                   │
                                                                   ▼
                                                            accepted artifact
```

#### 1.1 · Family inventory
(Route design work to its own Brief and workflow owners.)
The Design family contains 4 `SKILL.md` files under `design-family`. `haipipe-design` routes the request; `design-workflow` owns the Run workflow.

#### 1.2 · Native Runs
(Commission, generate, and verify work under Design identities.)
The current shared Run catalogue describes Design Runs for Commission, Generate, and Verify. The Design owner defines exact scope, inputs, dependencies, Results, and closure. The Brief is the owner record, not an extra Run unless commissioned as one.

#### 1.3 · Insight boundary
**Scope**: signed evidence handoff flows into an independently owned design task.

#### 1.4 · Consume exact Wisdom
(Use the signed version selected by Insight.)
Design consumes its exact signed Wisdom input. It records how that input shaped the Brief and resulting artifact; it does not alter the Insight interpretation or substitute a newer version silently.

#### 1.5 · Verify before handoff
(Preserve Design acceptance and downstream Display work.)
Design verifies its generated unit against the declared Brief and acceptance conditions. Display can format or assemble accepted units but does not become the Design decision-maker.

## Aims
### A1 · Design ownership
- 🔨 A1.1 · Insight-to-Design handoff and Design Run ownership are traceable.
  **Done when:** A Brief, Commission, Generate, and Verify route resolves to the current Design contract and exact accepted inputs.
  **Now:** Family ownership is mapped.
