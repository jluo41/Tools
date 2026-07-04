// ─── haipipe-workflow template ───────────────────────────────────
// Copy this file, rename, and fill in the blanks.
// See: skills/flow/haipipe-workflow/ref/workflow-api.md
// See: skills/flow/haipipe-workflow/ref/concepts.md

export const meta = {
  name: 'WORKFLOW_NAME',
  description: 'PURPOSE — one line, shown in permission dialog',
  phases: [
    { title: 'P1_TITLE', detail: 'what this phase does' },
    { title: 'P2_TITLE', detail: 'what this phase does' },
    // add more phases as needed
  ],
}

// ─── I: Input ───────────────────────────────────────────────────
// args shape: array of specs, or object with fields
const specs = Array.isArray(args) ? args : (args && args.specs || [])
if (!specs.length) { log('no specs; nothing to do'); return { summary: [] } }
log(`${meta.name}: ${specs.length} item(s)`)

// ─── Schemas (contracts between phases) ─────────────────────────
const P1_RESULT = {
  type: 'object',
  required: ['status'],
  properties: {
    status: { type: 'string', enum: ['ok', 'blocked', 'failed'] },
    // add fields
  }
}

const P2_RESULT = {
  type: 'object',
  required: ['verdict'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'warn', 'fail'] },
    issues:  { type: 'array', items: { type: 'string' } },
  }
}

// ─── P: Phases ──────────────────────────────────────────────────
const results = await pipeline(
  specs,

  // P1 — first phase (one Step per item, fan=pipeline)
  (spec, _, idx) => agent(
    `P1 prompt for item ${idx}: ${JSON.stringify(spec)}`,
    {
      label: `p1:${spec.name || idx}`,
      phase: 'P1_TITLE',
      schema: P1_RESULT,
      // agentType: 'my-specialist-agent',
    }
  ),

  // P2 — second phase (gate: skip if P1 failed)
  (p1, spec) => {
    if (!p1 || p1.status !== 'ok') return { ...p1, p2: { verdict: 'skipped' } }
    return agent(
      `P2 prompt: review result of ${spec.name || 'item'}`,
      {
        label: `p2:${spec.name || 'item'}`,
        phase: 'P2_TITLE',
        schema: P2_RESULT,
      }
    ).then(v => ({ ...p1, p2: v }))
  },
)

// ─── O: Output ──────────────────────────────────────────────────
const summary = results.filter(Boolean).map(r => ({
  name:    r.name || null,
  status:  r.status || 'failed',
  verdict: r.p2 ? r.p2.verdict : null,
}))

log(`${meta.name} done: ${summary.length} result(s)`)
return { summary }
