# Task and engineering
state: 🟡 PARTIAL
owner: JL

## Opening

How do Task and engineering skills produce internal work that consumers can reuse and trace?

**Where this Page sits:** It is the internal evidence producer in the toolkit graph.

**Why it matters:** Consumer Pages can cite a completed Result without taking ownership of the producer's code or run history.

## Content

### 1 · Family boundary
**Scope**: task execution and its engineering specializations.
```text
internal commission
      │
      ▼
owner-native Run ──▶ Result ──▶ consumer Page or Insight
```

#### 1.1 · Task umbrella
(Use Task for bounded internal execution.)
The Task family plans, builds, executes, and reports internal work. Its current tree contains 49 `SKILL.md` files under `task-family`. The main entry is `haipipe-task`; specialized families cover data, neural networks, endpoints, individual inference, and supporting methods.

#### 1.2 · Owner-native Results
(A Task Run returns a Result that a consumer can trace.)
Each Run keeps its Task identity, declared inputs, execution record, and Result. A Page or Insight consumer records the exact source Run as Supporting evidence and commissions a Local Run only for consumer-specific transformation.

#### 1.3 · Workflow and Runs
**Scope**: the owner defines the Run graph; the Board only presents it.

#### 1.4 · Resolve actual Run Specs
(Read the Task workflow contract before naming work.)
Task workflow definitions list bounded Run Specs with dependencies, routes, and completion rules. Read the `run-catalog` and `task-hierarchy` for the exact family contracts. This map does not convert Plan, Build, Execute, or Report labels into Runs by assumption.

#### 1.5 · Handoffs to consumers
(Transfer receipts without copying producer ownership.)
Discovery and Task are sibling evidence producers. Both return the shared Run/Result shape. The consumer records the source Run id, selected evidence, and any local transformation in its own workspace.

#### 1.6 · Source links
**Scope**: canonical skill files remain the maintained source.

#### 1.7 · Start with the owning skill
(Use the specialist selected by the requested work.)
Open `haipipe-task` for dispatch and the `task-family` for specialists. The `haipipe-run` owns identity and Result rules.

## Aims
### A1 · Family boundary
- 🔨 A1.1 · Task and engineering skill ownership is clear.
  **Done when:** Each specialist family and its actual Run contract can be reached from this Page without copying the source instructions.
  **Now:** Family root and canonical links are mapped.
