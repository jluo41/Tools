# The local Insights layer: Application placement, Task-backed authority
state: ✅ SETTLED · ownership and runtime placement shipped
owner: JL

## Opening

Where should the understanding work live when it exists specifically to serve an Application?

It lives inside the Application at `1-insights/`. This placement keeps the Brief, the missing premise, the DIKW reasoning, and every downstream Design Handoff in one inspectable system. Evidence authority does not move: Task rules still govern source identity, run binding, staleness, human reading, and Probe.

### Writing Style

Always name which side owns placement and which side owns evidence. Never collapse the two into the vague statement that an Insight is simply “a Task” or simply
“part of Design.”

## Diagram

```text
Application authority                         Task-backed authority
────────────────────────────                  ───────────────────────────
📁 1-insights/ owns placement                 🧾 source + run identity
🎯 Brief/Design owns the need                 ⏳ staleness + refresh rules
🧠 W serves the application context           🔬 Probe into Task/Discovery
📤 Design Handoff serves PageX                👤 human reads evidence result
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

An Insight Page is opened because a Brief or Design Page has a bounded decision that cannot be made from its current accepted inputs. Local placement exposes that dependency without copying raw evidence into Design.

#### 2 · What remains Task-backed

D, I, and K must be traceable to accepted Task/Discovery outputs or accepted existing Pages. Any new Probe follows the shared Task-backed source/run/staleness contract. Application cannot weaken those rules.

#### 3 · What Application adds

W is explicitly contextual: it says what the evidence permits, discourages, or leaves unresolved for this Application. Division 8 packages that judgment as a
Design Handoff rather than a generic finding.

#### 4 · Compatibility

Existing consumer-neutral Insight Pages on another Board remain valid PageX inputs. They are not moved automatically; a local Page may reference them and add only the Application-specific W and handoff that are genuinely needed.

## Aims

### A1 · Contract
- A1.1 · Placement and evidence authority are separate and explicit.
  **Done when:** the public door, Page Type, and Board all state the same split.

#### A2 · Runtime
- A2.1 · New Application insights have one canonical home.
  **Done when:** the runtime map uses `1-insights/<insight-id>/` and no current
  Application procedure routes new work to an external Task Board by default.

## States

### A1 · Contract
- ✅ A1.1 · Shipped in Application 0.8.0 and Insight Page Type 0.3.0.

#### A2 · Runtime
- ✅ A2.1 · The public router and Insight procedure now use `1-insights/`.

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/SKILL.md`
  The public ownership and runtime contract.
- `../../../../application/page-types/haipipe-page-for-insight/SKILL.md`
  The local Insight Page contract.

## Law

Application owns the **placement and consumer** of its Insight Pages; Task owns their **evidence discipline**.

## Log

260820 · Moved the live Insight Page Type into `application/page-types/` and retained Task-backed Probe/source/run/staleness rules.
