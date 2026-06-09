Claude Code Workflow API — cheat sheet
=======================================

The Workflow tool runs deterministic, resumable multi-agent scripts.
Scripts are plain JavaScript (NOT TypeScript). The script body runs
in an async context — use `await` directly.


Invocation
----------

From a skill or assistant message:

```javascript
Workflow({
  scriptPath: "path/to/script.workflow.js"
}, args)
```

Or inline (for one-off):

```javascript
Workflow({
  script: `export const meta = { ... }; ...`
}, args)
```

Resume a prior run:

```javascript
Workflow({
  scriptPath: "...",
  resumeFromRunId: "wf_abc123"
})
```


Script structure
-----------------

Every script has two parts: **meta** (pure literal) + **body** (async JS).

```javascript
export const meta = {
  name: 'my-workflow',
  description: 'One-line description shown in permission dialog',
  phases: [
    { title: 'Discover', detail: 'grep for X across repo' },
    { title: 'Fix',      detail: 'one agent per finding' },
  ],
}

// Body starts here — async context, use await directly
phase('Discover')
const findings = await agent('Find all X', { schema: FINDINGS })
// ...
```


Core functions
---------------

### agent(prompt, opts?) → Promise<any>

Spawn a subagent. The fundamental Step.

```javascript
const result = await agent(
  'Review file X for bugs',
  {
    label: 'review:X',           // display label in progress UI
    phase: 'Review',             // group under this phase (use inside pipeline/parallel)
    schema: VERDICT,             // force structured output (JSON Schema)
    model: 'sonnet',             // override model (omit to inherit)
    agentType: 'code-reviewer',  // use registered specialist agent
    isolation: 'worktree',       // git worktree isolation (expensive)
  }
)
```

- Without `schema`: returns final text as string.
- With `schema`: returns validated object (subagent retries on mismatch).
- Returns `null` if user skips or agent dies on terminal error.


### pipeline(items, stage1, stage2, ...) → Promise<any[]>

**DEFAULT fan-out.** Each item flows through all stages independently.
No barrier between stages — item A can be in stage 3 while item B is
still in stage 1.

```javascript
const results = await pipeline(
  specs,
  (spec) => agent(`Author ${spec.name}`, { phase: 'Author', schema: AUTHORED }),
  (authored, spec) => agent(`Review ${authored.folder}`, { phase: 'Review', schema: VERDICT }),
  (reviewed, spec) => {
    if (reviewed.verdict === 'fail') return reviewed
    return agent(`Run ${reviewed.folder}`, { phase: 'Run', schema: RUN })
  },
)
```

Stage callback signature: `(prevResult, originalItem, index)`

A stage that throws drops that item to `null` and skips remaining stages.


### parallel(thunks) → Promise<any[]>

**Barrier fan-out.** Awaits ALL thunks before returning.

```javascript
const all = await parallel([
  () => agent('Search by content', { schema: FINDINGS }),
  () => agent('Search by filename', { schema: FINDINGS }),
  () => agent('Search by git log',  { schema: FINDINGS }),
])
```

A thunk that throws resolves to `null`. Use `.filter(Boolean)` on results.

**Use parallel only when you genuinely need ALL results together**
(dedup, merge, early-exit). Otherwise use pipeline.


### phase(title) → void

Start a new phase. Subsequent `agent()` calls group under this title
in the progress display.

```javascript
phase('Discover')
const findings = await agent(...)
phase('Fix')
const fixes = await parallel(findings.map(f => () => agent(...)))
```


### log(message) → void

Emit a progress message (shown as narrator line above progress tree).

```javascript
log(`Found ${bugs.length} bugs, verifying...`)
```


Context objects
----------------

### args: any

The value passed as the Workflow tool's second argument. Pass
arrays/objects as actual JSON, NOT stringified.

```javascript
const specs = Array.isArray(args) ? args : (args.specs || [])
```


### budget: { total, spent(), remaining() }

Token budget from user's "+500k" directive.

```javascript
while (budget.total && budget.remaining() > 50_000) {
  const result = await agent('Find more bugs', { schema: BUGS })
  bugs.push(...result.bugs)
}
```

- `budget.total`: number | null (null = no target)
- `budget.spent()`: output tokens used this turn (shared across workflows)
- `budget.remaining()`: max(0, total - spent()), or Infinity if no target


### workflow(nameOrRef, args?) → Promise<any>

Run another workflow inline as a sub-step. One level of nesting only.


Constraints
-----------

- Plain JavaScript only (no TypeScript syntax)
- No `Date.now()`, `Math.random()`, `new Date()` (breaks resume)
- No filesystem or Node.js API access
- Max 16 concurrent agents (excess queues)
- Max 1000 total agents per workflow lifetime
- Max 4096 items per pipeline()/parallel() call
- `meta` must be a pure literal (no variables, no function calls)


Schema pattern
--------------

Define schemas as constants; reference in `agent()` opts:

```javascript
const FINDINGS = {
  type: 'object',
  required: ['bugs'],
  properties: {
    bugs: {
      type: 'array',
      items: {
        type: 'object',
        required: ['file', 'line', 'desc'],
        properties: {
          file: { type: 'string' },
          line: { type: 'number' },
          desc: { type: 'string' },
          severity: { type: 'string', enum: ['low', 'medium', 'high'] },
        }
      }
    }
  }
}
```


Common patterns
----------------

### Gate chain (Author → Review → Run → Audit)

```javascript
const results = await pipeline(specs,
  (spec) => agent(`Author ${spec.name}`, { schema: AUTHORED }),
  (a, spec) => {
    if (a.status !== 'ok') return a
    return agent(`Review ${a.folder}`, { schema: VERDICT }).then(v => ({...a, gate: v}))
  },
  (r, spec) => {
    if (r.gate?.verdict === 'fail') return r
    return agent(`Run ${r.folder}`, { schema: RUN }).then(x => ({...r, run: x}))
  },
)
```

### Adversarial verify (N skeptics per finding)

```javascript
const votes = await parallel(
  Array.from({ length: 3 }, () => () =>
    agent(`Try to refute: ${claim}`, { schema: VERDICT })
  )
)
const survives = votes.filter(Boolean).filter(v => !v.refuted).length >= 2
```

### Loop-until-dry (unknown-size discovery)

```javascript
const seen = new Set()
let dry = 0
while (dry < 2) {
  const found = await agent('Find bugs', { schema: BUGS })
  const fresh = found.bugs.filter(b => !seen.has(b.key))
  if (!fresh.length) { dry++; continue }
  dry = 0
  fresh.forEach(b => seen.add(b.key))
  results.push(...fresh)
}
```
