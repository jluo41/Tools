// haipipe-workflow Run Spec graph template.
// `meta.phases` and opts.phase are engine progress labels only.

export const meta = {
  name: 'WORKFLOW_NAME',
  description: 'PURPOSE — one line, shown in permission dialog',
  phases: [
    { title: 'AUTHOR', detail: 'progress group for Run Spec author' },
    { title: 'REVIEW', detail: 'progress group for Run Spec review' },
  ],
}

const specs = Array.isArray(args) ? args : (args && args.specs || [])
if (!specs.length) { log('no inputs; nothing to do'); return { runs: [] } }

const AUTHOR_RESULT = {
  type: 'object',
  required: ['status', 'result', 'receipt'],
  properties: {
    status: { type: 'string', enum: ['complete', 'blocked', 'failed'] },
    result: { type: ['string', 'null'] },
    receipt: { type: 'string' },
  }
}

const REVIEW_RESULT = {
  type: 'object',
  required: ['verdict', 'route', 'receipt'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'warn', 'fail', 'blocked'] },
    route: { type: 'string', enum: ['CLOSE', 'author', 'HOLD'] },
    receipt: { type: 'string' },
  }
}

const runs = await pipeline(
  specs,
  (spec, _, idx) => agent(
    `Run Spec author for ${JSON.stringify(spec)}`,
    { label: `author:${spec.name || idx}`, phase: 'AUTHOR', schema: AUTHOR_RESULT }
  ),
  (authored, spec, idx) => {
    if (!authored || authored.status !== 'complete') return authored
    return agent(
      `Independently review ${authored.result}`,
      { label: `review:${spec.name || idx}`, phase: 'REVIEW', schema: REVIEW_RESULT }
    ).then(review => ({ authored, review }))
  },
)

return { runs: runs.filter(Boolean) }
