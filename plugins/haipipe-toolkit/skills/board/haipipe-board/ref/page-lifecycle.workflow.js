export const meta = {
  name: 'haipipe-board-page-lifecycle',
  description: 'Route one Page through bounded DRAFT, PROBE, REVISE, and independent CHECK loops.',
  phases: [
    { title: 'Produce', detail: 'a phase-scoped producer performs DRAFT, PROBE, or REVISE' },
    { title: 'Snapshot', detail: 'rebuild, run mechanical checks, and identify the exact Page version' },
    { title: 'Check', detail: 'a fresh read-only judge evaluates and routes that version' },
  ],
}

const parsed = typeof args === 'string' ? JSON.parse(args) : (args || {})
const board = parsed.board
const page = parsed.page
const runId = parsed.run_id
const intent = parsed.intent
const startPhase = String(parsed.start_phase || '').toUpperCase()
const limits = parsed.limits || {}
const maxSteps = limits.max_steps || 12
const maxRounds = limits.max_rounds || 3
const humanGate = parsed.human_gate || { required: false, rule: '' }

if (!board || !page || !runId || !intent || !parsed.start_phase) {
  log('page-lifecycle: missing board, page, run_id, intent, or start_phase')
  return { status: 'blocked', reason: 'missing required raw-material packet field', receipts: [] }
}
if (!['DRAFT', 'PROBE', 'REVISE', 'CHECK'].includes(startPhase)) {
  log(`page-lifecycle: unknown start_phase=${startPhase}`)
  return { status: 'blocked', reason: `unknown start_phase ${startPhase}`, receipts: [] }
}

const ROUTES = ['DRAFT', 'PROBE', 'REVISE', 'CHECK', 'CLOSE', 'HOLD']
const LEGAL = {
  DRAFT: ['DRAFT', 'PROBE', 'REVISE', 'CHECK', 'HOLD'],
  PROBE: ['PROBE', 'REVISE', 'DRAFT', 'CHECK', 'HOLD'],
  REVISE: ['REVISE', 'PROBE', 'DRAFT', 'CHECK', 'HOLD'],
  CHECK: ['CLOSE', 'REVISE', 'PROBE', 'DRAFT', 'HOLD'],
}

const PRODUCER_RESULT = {
  type: 'object',
  required: ['actor', 'status', 'phase', 'route', 'reason', 'reopens_promise', 'artifacts', 'evidence'],
  properties: {
    actor: { type: 'string' },
    status: { type: 'string', enum: ['ok', 'blocked', 'failed'] },
    phase: { type: 'string', enum: ['DRAFT', 'PROBE', 'REVISE'] },
    route: { type: 'string', enum: ROUTES },
    reason: { type: 'string' },
    reopens_promise: { type: 'boolean' },
    artifacts: { type: 'array', items: { type: 'string' } },
    evidence: { type: 'array', items: { type: 'string' } },
    findings: { type: 'array', items: { type: 'string' } },
    open_questions: { type: 'array', items: { type: 'string' } },
  },
}

const SNAPSHOT_RESULT = {
  type: 'object',
  required: ['actor', 'status', 'version_id', 'source_sha256', 'render_sha256', 'mechanical_errors', 'mechanical_warnings', 'evidence'],
  properties: {
    actor: { type: 'string' },
    status: { type: 'string', enum: ['ok', 'failed'] },
    version_id: { type: 'string' },
    source_sha256: { type: 'string' },
    render_sha256: { type: 'string' },
    mechanical_errors: { type: 'number' },
    mechanical_warnings: { type: 'number' },
    evidence: { type: 'array', items: { type: 'string' } },
    findings: { type: 'array', items: { type: 'string' } },
  },
}

const REVIEW_RESULT = {
  type: 'object',
  required: ['actor', 'status', 'verdict', 'route', 'reason', 'checked_version', 'reopens_promise', 'findings', 'evidence', 'human_gate'],
  properties: {
    actor: { type: 'string' },
    status: { type: 'string', enum: ['pass', 'revise', 'blocked'] },
    verdict: { type: 'string', enum: ['pass', 'revise', 'blocked'] },
    route: { type: 'string', enum: ['CLOSE', 'REVISE', 'PROBE', 'DRAFT', 'HOLD'] },
    reason: { type: 'string' },
    checked_version: { type: 'string' },
    reopens_promise: { type: 'boolean' },
    findings: { type: 'array', items: { type: 'string' } },
    evidence: { type: 'array', items: { type: 'string' } },
    human_gate: {
      type: 'object',
      required: ['required', 'status', 'evidence'],
      properties: {
        required: { type: 'boolean' },
        status: { type: 'string', enum: ['not-required', 'pending', 'passed'] },
        evidence: { type: 'array', items: { type: 'string' } },
      },
    },
  },
}

async function snapshot(label) {
  return agent(
    `You are the mechanical builder for one Board Page. You do not edit Markdown or make a semantic judgment.\n\n` +
    `Board: ${board}\nPage: ${page}\nSnapshot label: ${label}\n\n` +
    `1. Run haipipe-board/cli/build.py on the Board.\n` +
    `2. Run haipipe-board/cli/check.py --strict and preserve the target Page findings.\n` +
    `3. Locate the rendered HTML for this Page.\n` +
    `4. Compute SHA-256 for the Markdown source and rendered HTML.\n` +
    `5. Return version_id exactly as <source_sha256>:<render_sha256>.\n` +
    `Do not change the Page, board.md, another source file, or a human gate.`,
    { label: `snapshot:${label}`, phase: 'Snapshot', schema: SNAPSHOT_RESULT }
  )
}

function terminalStatus(route, fallback) {
  if (route === 'CLOSE') return 'closed'
  if (route === 'HOLD') return fallback || 'hold'
  return 'running'
}

function gateShape(result) {
  return result && result.human_gate
    ? result.human_gate
    : { required: !!humanGate.required, status: humanGate.required ? 'pending' : 'not-required', evidence: [] }
}

log(`page-lifecycle: run=${runId}, page=${page}, start=${startPhase}, maxSteps=${maxSteps}, maxRounds=${maxRounds}`)

phase('Snapshot')
let currentVersion = await snapshot('initial')
if (!currentVersion || currentVersion.status !== 'ok') {
  return {
    status: 'failed',
    run_id: runId,
    board,
    page,
    packet: parsed,
    limits: { max_steps: maxSteps, max_rounds: maxRounds },
    final_version: currentVersion ? currentVersion.version_id : null,
    receipts: [],
    reason: 'initial build or version snapshot failed',
  }
}

let current = startPhase
let round = parsed.round || 1
let receipts = []
let producerActors = {}

for (let step = 1; step <= maxSteps; step++) {
  if (current === 'CHECK') {
    phase('Check')
    const review = await agent(
      `Perform CHECK on exactly one Board Page in a fresh, read-only context.\n\n` +
      `Board: ${board}\nPage: ${page}\nExpected version: ${currentVersion.version_id}\n` +
      `Intent: ${intent}\nHuman gate: ${JSON.stringify(humanGate)}\n\n` +
      `Load haipipe-board-page, the matching Page Type, and haipipe-board-page-check. ` +
      `Run the Board's read-only checker, compute the same source:render SHA-256 identity, and HOLD if it differs from the expected version. ` +
      `Judge mechanics, function, evidence, readability, the local closing rule, and any human gate. ` +
      `Do not edit, rebuild, or cure a finding. Route to CLOSE, REVISE, PROBE, DRAFT, or HOLD. ` +
      `DRAFT requires reopens_promise=true because purpose or Aims must change. ` +
      `CLOSE requires verdict=pass and durable evidence for every required human gate.`,
      {
        label: `check:r${round}:s${step}`,
        phase: 'Check',
        agentType: 'haipipe-board-reviewer-agent',
        schema: REVIEW_RESULT,
      }
    )

    if (!review) {
      const receipt = {
        step,
        round,
        phase: 'CHECK',
        actor: 'workflow-controller',
        role: 'controller',
        builder_actor: currentVersion.actor,
        status: 'blocked',
        version_before: currentVersion.version_id,
        version_after: currentVersion.version_id,
        checked_version: currentVersion.version_id,
        source_sha256: currentVersion.source_sha256,
        render_sha256: currentVersion.render_sha256,
        mechanical_errors: currentVersion.mechanical_errors,
        mechanical_warnings: currentVersion.mechanical_warnings,
        verdict: 'blocked',
        route: 'HOLD',
        requested_route: 'HOLD',
        reopens_promise: false,
        reason: 'independent reviewer unavailable',
        artifacts: [],
        evidence: [],
        findings: ['reviewer returned no receipt'],
        human_gate: gateShape(null),
      }
      receipts.push(receipt)
      return { status: 'blocked', run_id: runId, board, page, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts }
    }

    let route = review.route
    let reason = review.reason
    let reviewStatus = review.status
    let verdict = review.verdict
    if (!LEGAL.CHECK.includes(route)) {
      route = 'HOLD'
      reviewStatus = 'blocked'
      verdict = 'blocked'
      reason = `${reason}; reviewer returned an illegal CHECK route`
    }
    if (review.checked_version !== currentVersion.version_id) {
      route = 'HOLD'
      reviewStatus = 'blocked'
      verdict = 'blocked'
      reason = `${reason}; checked version differs from the current snapshot`
    }
    if (producerActors[currentVersion.version_id] === review.actor) {
      route = 'HOLD'
      reviewStatus = 'blocked'
      verdict = 'blocked'
      reason = `${reason}; producer and CHECK actor are identical for this version`
    }
    if (currentVersion.actor === review.actor) {
      route = 'HOLD'
      reviewStatus = 'blocked'
      verdict = 'blocked'
      reason = `${reason}; builder and CHECK actor are identical for this version`
    }
    if (route === 'DRAFT' && !review.reopens_promise) {
      route = 'HOLD'
      reviewStatus = 'blocked'
      verdict = 'blocked'
      reason = `${reason}; DRAFT route did not name a reopened purpose or Aim`
    }
    if (route === 'CLOSE' && verdict !== 'pass') {
      route = 'HOLD'
      reviewStatus = 'blocked'
      verdict = 'blocked'
      reason = `${reason}; CLOSE requires verdict=pass`
    }
    if (route === 'CLOSE' && review.human_gate.required && (review.human_gate.status !== 'passed' || !review.human_gate.evidence.length)) {
      route = 'HOLD'
      reason = `${reason}; required human gate lacks durable passed evidence`
    }
    if (step === maxSteps && !['CLOSE', 'HOLD'].includes(route)) {
      route = 'HOLD'
      reason = `${reason}; max_steps=${maxSteps} reached before another phase could run`
    }
    if (route === 'DRAFT' && review.reopens_promise && round >= maxRounds) {
      route = 'HOLD'
      reason = `${reason}; max_rounds=${maxRounds} prevents another DRAFT round`
    }

    const receipt = {
      step,
      round,
      phase: 'CHECK',
      actor: review.actor,
      role: 'judge',
      builder_actor: currentVersion.actor,
      status: reviewStatus === 'blocked' ? 'blocked' : 'ok',
      version_before: currentVersion.version_id,
      version_after: currentVersion.version_id,
      checked_version: review.checked_version,
      source_sha256: currentVersion.source_sha256,
      render_sha256: currentVersion.render_sha256,
      mechanical_errors: currentVersion.mechanical_errors,
      mechanical_warnings: currentVersion.mechanical_warnings,
      verdict,
      route,
      requested_route: review.route,
      reopens_promise: route === 'DRAFT' && review.reopens_promise,
      reason,
      artifacts: [],
      evidence: review.evidence,
      findings: review.findings,
      human_gate: review.human_gate,
    }
    receipts.push(receipt)

    if (route === 'CLOSE' || route === 'HOLD') {
      return { status: terminalStatus(route, reviewStatus === 'blocked' ? 'blocked' : 'hold'), run_id: runId, board, page, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts }
    }
    if (route === 'DRAFT' && review.reopens_promise) round += 1
    current = route
    continue
  }

  phase('Produce')
  const producer = await agent(
    `Perform exactly one ${current} phase for one Board Page.\n\n` +
    `Assignment packet: ${JSON.stringify(parsed)}\nCurrent round: ${round}\nCurrent version: ${currentVersion.version_id}\n\n` +
    `Load haipipe-board-page, the matching Page Type, haipipe-board-page-${current.toLowerCase()}, and any family worker. ` +
    `Follow the phase boundary. Work only on the target Page and a declared probe surface when PROBE requires one. ` +
    `Do not rebuild, run CHECK, approve the result, touch board.md, or alter a human gate. ` +
    `Return one phase receipt and suggest the next legal route. DRAFT from a non-DRAFT phase must explain the changed purpose or Aim and set reopens_promise=true.`,
    {
      label: `${current.toLowerCase()}:r${round}:s${step}`,
      phase: 'Produce',
      agentType: 'haipipe-board-creator-agent',
      schema: PRODUCER_RESULT,
    }
  )

  if (!producer) {
    const receipt = {
      step,
      round,
      phase: current,
      actor: 'haipipe-board-creator-agent',
      role: 'producer',
      builder_actor: currentVersion.actor,
      status: 'blocked',
      version_before: currentVersion.version_id,
      version_after: currentVersion.version_id,
      checked_version: '',
      source_sha256: currentVersion.source_sha256,
      render_sha256: currentVersion.render_sha256,
      mechanical_errors: currentVersion.mechanical_errors,
      mechanical_warnings: currentVersion.mechanical_warnings,
      verdict: '',
      route: 'HOLD',
      requested_route: 'HOLD',
      reopens_promise: false,
      reason: 'phase producer unavailable',
      artifacts: [],
      evidence: [],
      findings: ['producer returned no receipt'],
      human_gate: gateShape(null),
    }
    receipts.push(receipt)
    return { status: 'blocked', run_id: runId, board, page, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts }
  }

  const before = currentVersion.version_id
  let afterSnapshot = currentVersion
  if (producer.status === 'ok') {
    phase('Snapshot')
    afterSnapshot = await snapshot(`r${round}:s${step}:${current.toLowerCase()}`)
  }

  let route = producer.route
  let reason = producer.reason
  let status = producer.status
  let findings = producer.findings || []
  if (status !== 'ok') {
    route = 'HOLD'
  } else if (producer.phase !== current || !LEGAL[current].includes(route) || route === 'CLOSE') {
    status = 'failed'
    route = 'HOLD'
    reason = `${reason}; producer returned a phase or route outside ${current} authority`
    findings = findings.concat(['producer phase or route violated the lifecycle grammar'])
  } else if (route === 'DRAFT' && current !== 'DRAFT' && !producer.reopens_promise) {
    status = 'blocked'
    route = 'HOLD'
    reason = `${reason}; DRAFT route did not name a reopened purpose or Aim`
    findings = findings.concat(['DRAFT route requires reopens_promise=true'])
  } else if (!afterSnapshot || afterSnapshot.status !== 'ok') {
    status = 'failed'
    route = 'HOLD'
    reason = `${reason}; build or version snapshot failed`
    findings = findings.concat(['build or version snapshot failed'])
    afterSnapshot = currentVersion
  } else if (afterSnapshot.actor === producer.actor) {
    status = 'failed'
    route = 'HOLD'
    reason = `${reason}; producer and mechanical builder actor are identical`
    findings = findings.concat(['producer and builder must be separate actors'])
  } else if (afterSnapshot.mechanical_errors > 0) {
    route = 'REVISE'
    reason = `${reason}; deterministic checker found ${afterSnapshot.mechanical_errors} error(s)`
    findings = findings.concat(afterSnapshot.findings || [])
  }
  if (step === maxSteps && !['CLOSE', 'HOLD'].includes(route)) {
    route = 'HOLD'
    reason = `${reason}; max_steps=${maxSteps} reached before another phase could run`
  }
  if (route === 'DRAFT' && current !== 'DRAFT' && producer.reopens_promise && round >= maxRounds) {
    route = 'HOLD'
    reason = `${reason}; max_rounds=${maxRounds} prevents another DRAFT round`
  }

  const receipt = {
    step,
    round,
    phase: current,
    actor: producer.actor,
    role: 'producer',
    builder_actor: afterSnapshot.actor,
    status,
    version_before: before,
    version_after: afterSnapshot.version_id,
    checked_version: '',
    source_sha256: afterSnapshot.source_sha256,
    render_sha256: afterSnapshot.render_sha256,
    mechanical_errors: afterSnapshot.mechanical_errors,
    mechanical_warnings: afterSnapshot.mechanical_warnings,
    verdict: '',
    route,
    requested_route: producer.route,
    reopens_promise: route === 'DRAFT' && current !== 'DRAFT' && producer.reopens_promise,
    reason,
    artifacts: producer.artifacts,
    evidence: producer.evidence.concat(afterSnapshot.evidence || []),
    findings,
    human_gate: gateShape(null),
  }
  receipts.push(receipt)
  currentVersion = afterSnapshot
  if (status === 'ok' && currentVersion.version_id !== before) {
    producerActors[currentVersion.version_id] = producer.actor
  }

  if (route === 'HOLD') {
    return { status: status === 'blocked' ? 'blocked' : status === 'failed' ? 'failed' : 'hold', run_id: runId, board, page, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts }
  }
  if (route === 'DRAFT' && current !== 'DRAFT' && producer.reopens_promise) round += 1
  current = route
}

return { status: 'hold', run_id: runId, board, page, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts, reason: 'loop exhausted without terminal route' }
