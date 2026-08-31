# The design layer: what the DesignBoard owns, and where it stops

state: ✅ SETTLED · the ACCEPTED cut ruled 260820
owner: JL

## Opening

What does the DesignBoard own, and at which point does the work stop being its own?

It owns everything between a settled insight and an accepted version: the audience strategy, the design principles, the message divisions, and the rails that hold them together. It stops at accepted. Building the thing, shipping it, running the experiment, and collecting what came back are task-layer work, and the folders that used to hold them on this board are gone.

### Writing Style

Say what the board owns before saying what it refuses. A boundary page that leads with exclusions reads as a complaint rather than a contract.

## Diagram

```text
🎨 DESIGN BOARD                          │  NOT THE DESIGN BOARD
─────────────────────────────────────────┼──────────────────────────────────
📌 brief    what we are building         │  🔧 implementation · build and ship
🎨 design   the messages, the rails      │  🧪 experiment     · run the A/B
✅ accept   "this exact version may go"  │  📊 collection     · gather the result
                                         │
        the board's LAST act ────────────┤  all three owned by the task layer
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

The DesignBoard takes one Brief and a set of settled Design Handoffs bound through PageX, and returns accepted divisions. It reaches no finding of its own and inspects no source.

#### 2 · Why acceptance is the right cut

Deciding that an exact version may go is a design judgment: it weighs the audience, the venue, the rails, and the evidence the design leaned on, all of which live on this board. Everything after that decision is execution against a fixed target, and execution already has an owner.

#### 3 · What left, and where it went

The board carries no `4-deploy/` and no `5-rounds/`. Both existed while the public door already said `deployment log → Task Folder P-B-E-R → Application Insight refresh`, so the folders held work that sentence had given away. Removing them makes the contract agree with itself.

#### 4 · The loop still closes

Cutting deploy does not orphan feedback. A shipped version produces data, a task folder collects it, an Insight Page re-reads it into a new handoff version, and the stale PageX binding reopens the dependent Design division. The cycle crosses boards rather than looping inside this one.

#### 5 · Before minting an experiments board

The task layer already carries two surfaces: P-B-E-R for execution and a Task Board for reading results. An A/B run is a task folder, its result reading is a task page, and its synthesis is an Insight Page. Check that shape before proposing a fourth board family for measurement.

## Aims

### A1 · Contract
- ✅ A1.1 · The board's last act is acceptance, and nothing downstream lives here.
  **Done when:** no deploy record, shipment log, or measurement round can be written to a Design Page.
  **Now:** `4-deploy/` and `5-rounds/` removed in Application 0.9.0; the `deploy` and `iterate` verbs are gone and Design Page Type 0.3.0 forbids the records.


#### A2 · Closure
- ✅ A2.1 · The feedback loop closes without a stage on this board.
  **Done when:** the documented return path runs task → Insight → stale binding → reopened division.
  **Now:** The public door's Iteration section is now a handoff diagram, not a stage.


## Discussion

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/SKILL.md`
  The public door, its verb list, and the two-board runtime map.
- `../../../../application/page-types/haipipe-page-for-design/SKILL.md`
  The Design Page contract and its closing checks.

## Law

The DesignBoard ends at ACCEPTED. It never owns SHIPPED and never owns MEASURED.

## Log

260820 · Cut the board at acceptance and removed `4-deploy/` and `5-rounds/` (JL: "you just stop at designing, the implementation is another thing").

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0