# Project and utilities
state: 🟡 PARTIAL
owner: JL

## Opening

How do project and utility skills help the rest of the toolkit get configured and operated?

**Where this Page sits:** These skills provide shared setup and local operations for the other Jobs.

**Why it matters:** Maintainers can find environment and helper tools without treating them as hidden workflow stages.

## Content

### 1 · Support families
**Scope**: project setup and utilities are supporting capabilities.
```text
project setup / utility ──▶ owner Job Runs
                                      │
                                      ▼
                            configured work + Results
```

#### 1.1 · Project setup
(Use Project skills to establish or maintain a workspace.)
The Project family contains 2 `SKILL.md` files under `project-family`. It owns project-container setup and related workspace operations.

#### 1.2 · Shared utilities
(Choose a utility by the concrete input or operation.)
The utility family contains 10 `SKILL.md` files under `utility-family`. These include table workflows, notebook support, connectors, formatting, and other cross-cutting helpers.

#### 1.3 · Workflow and Run ownership
**Scope**: support work keeps the contract of the skill that executes it.

#### 1.4 · Do not invent a shared lifecycle
(A utility can be used inside a Job without becoming a Run owner.)
Use the selected utility's own instructions and return shape. When it performs a bounded commission with a Run contract, preserve that Run identity and Result. Otherwise treat it as a helper, not an invented workflow unit.

#### 1.5 · Keep setup separate from research evidence
(Project scaffolding prepares a workspace; it does not prove a research result.)
Project setup supports the user and the other Jobs. Evidence, interpretation, design, and Paper acceptance remain with their domain owners.

## Aims
### A1 · Support families
- 🔨 A1.1 · Project and utility responsibilities are distinct from research Jobs.
  **Done when:** All support skill roots link to their canonical instructions and any native Run/Result contract is preserved.
  **Now:** Both skill families are mapped.
