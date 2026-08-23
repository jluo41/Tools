# The skill set: one door, four Page Types, shared Page machinery
state: ✅ SETTLED · versions, ownership, and installed resolver verified
owner: JL

## Opening

What is the smallest Application skill set that still expresses the full system?

One public router and four owned Page Types are the product surface. Shared Page,
PageX, Probe, and output plugins supply machinery; legacy stage skills are compatibility readers rather than the target architecture.

### Writing Style

Separate public skills from shared dependencies and compatibility routes.

## Diagram

```text
haipipe-application 0.8.0
        │
        ├── haipipe-page-for-brief 0.2.0
        ├── haipipe-page-for-insight 0.3.0
        ├── haipipe-page-for-design 0.3.0        ← key renamed from intervention
        └── haipipe-page-for-meta 0.1.0          ← InsightBoard head (artifact retired)

shared: haipipe-page · page-workflow · PageX · Probe · output plugins
legacy: enter/lifecycle/ladder/phase skills → compatibility only
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

`haipipe-application` diagnoses the current frontier and routes Brief, Insight,
Design, Artifact, deploy, review, and round verbs.

#### 2 · Owned Page Types

The folder owner is the semantic owner. All four live under
`application/page-types/`; Insight retains Task-backed evidence authority.

#### 3 · Shared machinery

`haipipe-page` supplies the Page frame and phases. PageX reads accepted Pages.
Probe acquires Task/Discovery evidence only for Insight Pages. Output plugins project Design content.

#### 4 · Compatibility

Existing external Insight Pages remain valid inputs. Old Application stages may be read for migration, but no new Application copies their ladder.

## Aims

### A1 · Contract
- A1.1 · Four versions and ownership paths agree.
  **Done when:** frontmatter, changelogs, registry, and Board name the same roster.

#### A2 · Resolver
- A2.1 · Installed skill discovery points to the new Insight path.
  **Done when:** a fresh agent resolves the Application-owned skill without the
  retired Task path.

## States

### A1 · Contract
- ✅ A1.1 · Application 0.8.0; Brief/Design/Artifact 0.2.0; Insight 0.3.0.

#### A2 · Resolver
- ✅ A2.1 · Project skill links resolve the Application-owned path and both fresh agents loaded it.

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/SKILL.md`
- `../../../../application/page-types/`
- `../../../../board/haipipe-page/SKILL.md`

## Law

Application owns the Page Type because it owns the consumer and runtime placement;
Task-backed evidence rules are inherited authority, not folder ownership.

## Log

260820 · Reduced the target surface to one router plus four Application-owned
Page Types.
260820 · Refreshed project skill links and verified the moved Insight skill in two fresh contexts.
