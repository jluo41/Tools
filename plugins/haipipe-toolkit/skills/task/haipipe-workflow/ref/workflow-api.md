# JavaScript Workflow API · execution adapter

The Workflow tool runs resumable multi-agent JavaScript. It is an execution
adapter for a frozen Run Spec graph; it is not the Workflow ontology.

```javascript
Workflow({ scriptPath: "path/to/script.workflow.js" }, args)
```

Scripts are plain JavaScript in an async context. `meta` must be a pure literal.

## Core calls

### `agent(prompt, opts?)`

Runs one internal worker action. The caller is responsible for preserving the
owning Run Instance and receipt.

```javascript
const result = await agent('Review file X', {
  label: 'review:X',
  phase: 'REVIEW', // progress group only; never Run authority
  schema: VERDICT,
  agentType: 'code-reviewer',
})
```

### `pipeline(items, step1, step2, ...)`

Each item flows through internal callbacks. A callback is not automatically a
Run; it materializes a Run only when the frozen plan gives it a Run Spec and
the caller writes the required identity/receipt.

### `parallel(thunks)`

Awaits all independent worker calls. Parallel calls sharing one target and
close rule remain Steps in one Run. Independently closable targets materialize
separate Run Instances according to planned cardinality.

### `workflow(nameOrRef, args?)`

Invokes a sub-workflow. The caller receives only its Output and terminal
receipt summary; the callee retains its internal Run graph and identities.

### `phase(title)` and `opts.phase`

These existing API fields group progress in the UI. They are non-semantic
presentation metadata. Never use them to define target, actor, gate, route,
Run identity, receipt, or cardinality.

### `log(message)`

Emits a progress message.

## Constraints

- plain JavaScript only;
- no `Date.now()`, `Math.random()`, or `new Date()` in resumable scripts;
- no filesystem or Node APIs;
- at most 16 concurrent agents and 1000 agents per Workflow lifetime;
- at most 4096 items per `pipeline()` or `parallel()` call;
- structured Results should use JSON Schema;
- runtime receipts must be written through the owning Run dialect.

## Gate and Route pattern

```javascript
const authored = await agent('Author target', { schema: AUTHORED, phase: 'AUTHOR' })
if (!authored || authored.status !== 'complete') {
  return { route: 'HOLD', result: authored }
}

const reviewed = await agent('Review exact authored result', {
  schema: VERDICT,
  phase: 'REVIEW',
})

return {
  route: reviewed.verdict === 'pass' ? 'CLOSE' : 'author',
  result: reviewed,
}
```

The route must match the frozen Run Spec. Code branching does not authorize a
new destination absent from the graph.
