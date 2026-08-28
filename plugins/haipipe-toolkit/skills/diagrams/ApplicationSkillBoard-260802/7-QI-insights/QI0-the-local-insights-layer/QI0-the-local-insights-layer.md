# The Insights layer: its own board, Task-backed authority

state: ✅ SETTLED · placement and evidence authority separate · one open ruling
owner: JL

## Opening

Where should the understanding work live when it exists specifically to serve an Application?

On its own board. A `<DataSubject>-InsightBoard` holds one Meta Page saying what data exists and one Insight Page per raised need. Evidence authority does not move with the folder: Task rules still govern source identity, run binding, staleness, human reading, and Probe. Placement says who keeps the file; it never says who may judge the evidence.

### Writing Style

Always name which side owns placement and which side owns evidence. Never collapse the two into the vague statement that an Insight is simply "a Task" or simply "part of Design."

## Diagram

**The two authorities**: what the Application decides, and what it may not.

```text
Application authority                         Task-backed authority
────────────────────────────                  ───────────────────────────
📁 the InsightBoard owns placement            🧾 source + run identity
🎯 the Brief owns the need                    ⏳ staleness + refresh rules
🧠 W serves the application context           🔬 Probe into Task/Discovery
📤 Design Handoff serves PageX                👤 human reads evidence result
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

An Insight Page is opened because a Brief or Design Page has a bounded decision that cannot be made from its current accepted inputs. A separate board exposes that dependency instead of burying it beside the design that waits on it.

#### 2 · Why a board of its own

The halves have different readers. Whoever checks whether the evidence holds is asking a different question from whoever signs off that a message may reach a patient, and one board gives them one queue. An Application is therefore a `<DataSubject>-InsightBoard` and a `<DesignTopic>-DesignBoard`, and PageX crosses between them unchanged because it binds by path.

#### 3 · What remains Task-backed

D, I, and K must be traceable to accepted Task/Discovery outputs or accepted existing Pages. Any new Probe follows the shared Task-backed source/run/staleness contract. Application cannot weaken those rules, and moving the file into an Application folder did not move that authority.

#### 4 · What Application adds

W is explicitly contextual: it says what the evidence permits, discourages, or leaves unresolved for this Application. Division 8 packages that judgment as a Design Handoff rather than a generic finding.

#### 5 · The two scopes

`page-type: insight` carries `scope: task | application`, because both layers create it. A `scope: application` Page lives here and serves a named need. A `scope: task` Page is consumer-neutral, lives on the Task/Insights Board, and is where dataset-first exploration goes when no Brief has raised anything yet. An Application borrows one through PageX rather than reopening the same question locally.

#### 6 · Compatibility

Existing consumer-neutral Insight Pages on another Board remain valid PageX inputs. They are not moved automatically; a local Page may reference them and add only the Application-specific W and handoff that are genuinely needed.

## Aims

### A1 · Contract
- A1.1 · Placement and evidence authority are separate and explicit.
  **Done when:** the public door, Page Type, and Board all state the same split.

#### P · Runtime
- P1 · Application insights have one canonical home.
  **Done when:** the runtime map uses `<DataSubject>-InsightBoard/1-I-insights/` and no current Application procedure routes new work to an external Task Board by default.
- P2 · Both scopes resolve to one contract with no collision.
  **Done when:** `scope:` is required and each scope's required fields are stated.

## States

### A1 · Contract
- ✅ A1.1 · Shipped in Application 0.10.0 and Insight Page Type 0.5.0.

#### P · Runtime
- ✅ P1 · The public router and Insight procedure use `<DataSubject>-InsightBoard/1-I-insights/`; the worked specimen builds clean at 2 pages, 0 error.
- ✅ P2 · `scope: task | application` is required and the resolution table names it.

### Decision Now
- [ ] 🗣 Which skill set owns `haipipe-page-for-insight`, now that both layers create the Page Type?
      It ships under `application/page-types/` while its `parent:` is `haipipe-page-for-task` and the task layer creates `scope: task` Pages against it. `haipipe-page` §🧬 says the folder a variant sits in names its owner, so today the folder says Application owns a contract Task also depends on.
      A · leave it in `application/page-types/`. Nothing breaks, both layers resolve it by name, and the folder simply stops being a reliable ownership signal.
      B · move it to `task/page-types/` beside its parent. The folder tells the truth again, and evidence authority and contract home finally agree.
      → CC recommends B, because the contract's own text says evidence discipline is Task's and a reader who trusts the folder rule is currently misled. It is a folder move plus a symlink refresh, not a rewrite.

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/SKILL.md`
  The public ownership and runtime contract.
- `../../../../application/haipipe-insight/SKILL.md`
  The InsightBoard's own law door since 260827: one dataset, the Climb Law, the three pens.
- `../../../../task/page-types/haipipe-page-for-insight/SKILL.md`
  The Insight Page contract, both scopes.

### 🔗 Related Board Pages
- `reads · DRAFT` · [QI2 §1](7-QI-insights/QI2-insight-to-design-handoff/QI2-insight-to-design-handoff.md)
  How a settled handoff crosses to the DesignBoard.

## Law

Application owns the **placement and consumer** of its Insight Pages; Task owns their **evidence discipline**. A folder move never moves an authority.

## Log

260820 · Moved the live Insight Page Type into `application/page-types/` and retained Task-backed Probe/source/run/staleness rules.
260820 · Split the Application into two boards, so this layer became the `<DataSubject>-InsightBoard` rather than a `1-insights/` folder inside one board.
260820 · Added `scope: task | application` after the single-contract collision surfaced, and raised the ownership ruling above.
260827 · The layer gained its own law door, `/haipipe-insight`, symmetric to `/haipipe-design`: the one-dataset law, the Climb Law and the three pens in one place, the workflow keeping only order and gates. The reused slash name is disclaimed in the door itself: the KB layer retired 260717 held evidence; this door holds none.
