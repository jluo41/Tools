export const meta = {
  name: 'haipipe-page-lifecycle',
  description: 'Route one Page through CONTEXT, OUTLINE, EVIDENCE, CONTENT, and an independent CHECK.',
  phases: [
    { title: 'Produce', detail: 'a phase-scoped producer performs any phase except CHECK' },
    { title: 'Snapshot', detail: 'rebuild, run mechanical checks, and identify the exact Page version' },
    { title: 'Check', detail: 'a fresh read-only judge evaluates and routes that version' },
  ],
}

const parsed = typeof args === 'string' ? JSON.parse(args) : (args || {})
const board = parsed.board
// `page` MUST be stored BOARD-RELATIVE. Run 260805-0216-QB8e stored an ABSOLUTE
// path; the 260816 regroup added a `<N>-` prefix to every group folder and the
// receipt stopped auditing, on a page that had not changed. A relative path also
// survives a clone, a rename of the checkout, and a second working copy.
const page = (() => {
  const raw = String(parsed.page || '')
  if (!raw || !board) return raw
  const b = String(board).replace(/\/+$/, '')
  return raw.startsWith(b + '/') ? raw.slice(b.length + 1) : raw
})()
// The RECEIPT stores the relative path; every AGENT is handed the absolute one,
// because an agent runs in a fresh context with no idea what `board` was.
const pageAbs = page && board && !page.startsWith('/') ? `${String(board).replace(/\/+$/, '')}/${page}` : page
// The auditor's own packet-run-mismatch invariant requires packet.page === run.page
// (both board-relative). Without this line the echoed packet kept the raw absolute
// input while the top-level `page` was normalized, so every audit failed on its own
// receipt (found 260818 auditing run 260818-1510-QPw00).
parsed.page = page
const runId = parsed.run_id
const intent = parsed.intent
let startPhase = String(parsed.start_phase || '').toUpperCase()
const limits = parsed.limits || {}
const maxSteps = limits.max_steps || 12
const maxRounds = limits.max_rounds || 3
// ── COPILOT | AUTO (260821) ──────────────────────────────────────────────
// Not two rule sets — ONE, read two ways. The selected plugin ticks and any
// owner RULING are the same in both; what changes is what happens while one is
// UNANSWERED:
//
//   copilot   the human half BLOCKS. A person is here; wait for them.
//   auto      the human half DEFERS. The loop keeps moving and the debt
//             accumulates on the ledger (`cli/pagephase.py --owed`), which is
//             handed over together at the end instead of interrupting once
//             per selected tick.
//
// This is JL's 260818 ruling made executable: "human not to approve, they to
// break" — the RUN proceeds on `checked: ✅` alone, and a plan nobody objected
// to is not blocked. It defers plugin ticks and obeys the phase-owned RULING
// policy below.
const mode = String(parsed.mode || 'copilot').toLowerCase()
if (!['copilot', 'auto'].includes(mode)) {
  log(`page-lifecycle: unknown mode=${mode}`)
  return { status: 'blocked', reason: `unknown mode ${mode}; use copilot | auto`, receipts: [] }
}

// OWNER RULING IS PHASE-OWNED. `page_ruling` is resolved from the Folder's
// phase contract before dispatch: `none` adds no Page gate; `domain-gate`
// reuses the owning workflow gate; `local` adds a Page-local gate. Missing
// metadata means a legacy Page: preserve the historical behavior in which
// AUTO hardens a local gate while COPILOT honors the caller's declaration.
// Plugin ticks (`approved:` `verified` `read:` `accepted:`) remain selected by
// actual artifacts and may be deferred onto the owed ledger.
const pageRuling = String(parsed.page_ruling || 'legacy-default').toLowerCase()
if (!['none', 'domain-gate', 'local', 'legacy-default'].includes(pageRuling)) {
  log(`page-lifecycle: unknown page_ruling=${pageRuling}`)
  return { status: 'blocked', reason: `unknown page_ruling ${pageRuling}; use none | domain-gate | local`, receipts: [] }
}
const declaredGate = parsed.human_gate || { required: false, rule: '' }
const phaseWaivesOwnerGate = pageRuling === 'none'
const phaseOwnsGate = !phaseWaivesOwnerGate && (pageRuling === 'domain-gate' || pageRuling === 'local')
const legacyAutoGate = pageRuling === 'legacy-default' && mode === 'auto'
const hardenOwnerGate = !declaredGate.required && (phaseOwnsGate || legacyAutoGate)
const ownerGateLabel = pageRuling === 'domain-gate'
  ? 'phase-owned domain gate'
  : pageRuling === 'local'
    ? 'phase-owned local RULING'
    : pageRuling === 'legacy-default'
      ? 'legacy Page RULING'
      : 'declared human gate'
const humanGate = hardenOwnerGate
  ? { ...declaredGate, required: true,
      rule: (declaredGate.rule ? declaredGate.rule + '; ' : '') +
            `${ownerGateLabel} cannot be waived` }
  : declaredGate
// Written back for the SAME reason `parsed.page` is normalized above:
// src/page_lifecycle.py asserts every receipt's human_gate.required equals the
// packet's. A hardened gate that the echoed packet did not know about would
// fail the audit on its own receipt.
parsed.human_gate = humanGate
parsed.page_ruling = pageRuling
if (!board || !page || !runId || !intent || !parsed.start_phase) {
  log('page-lifecycle: missing board, page, run_id, intent, or start_phase')
  return { status: 'blocked', reason: 'missing required raw-material packet field', receipts: [] }
}
if (startPhase === 'PROBE') startPhase = 'EVIDENCE' // retired 260901; old packets still parse
if (['DRAFT', 'REVISE', 'COMPILE'].includes(startPhase)) startPhase = 'CONTENT'
parsed.start_phase = startPhase
if (!['CONTEXT', 'OUTLINE', 'EVIDENCE', 'CONTENT', 'CHECK'].includes(startPhase)) {
  log(`page-lifecycle: unknown start_phase=${startPhase}`)
  return { status: 'blocked', reason: `unknown start_phase ${startPhase}`, receipts: [] }
}

const ROUTES = ['CONTEXT', 'OUTLINE', 'EVIDENCE', 'CONTENT', 'CHECK', 'CLOSE', 'HOLD']
const PHASE_CYCLES = {
  CONTEXT: ['PREPARE'],
  OUTLINE: ['SHAPE', 'SURVEY'],
  EVIDENCE: ['LAND', 'EMBED'],
  CONTENT: ['WRITE'],
  CHECK: ['CHECK'],
}
const legalNextCycle = (route, nextCycle) =>
  ['CLOSE', 'HOLD'].includes(route) ||
  ((PHASE_CYCLES[route] || []).includes(String(nextCycle || '').toUpperCase()))
// CURRENT grammar comes first. The DRAFT/REVISE/COMPILE rows and edges remain
// below only so the Python auditor can verify immutable historical receipts.
const LEGAL = {
  CONTEXT: ['CONTEXT', 'OUTLINE', 'HOLD'],
  OUTLINE: ['CONTEXT', 'OUTLINE', 'EVIDENCE', 'CONTENT', 'DRAFT', 'HOLD'],
  EVIDENCE: ['CONTEXT', 'EVIDENCE', 'OUTLINE', 'HOLD'],
  CONTENT: ['CONTEXT', 'CONTENT', 'OUTLINE', 'EVIDENCE', 'CHECK', 'HOLD'],
  DRAFT: ['DRAFT', 'OUTLINE', 'REVISE', 'CHECK', 'HOLD'],
  REVISE: ['REVISE', 'COMPILE', 'OUTLINE', 'EVIDENCE', 'DRAFT', 'CHECK', 'HOLD'],
  COMPILE: ['COMPILE', 'CHECK', 'REVISE', 'HOLD'],
  CHECK: ['CLOSE', 'CONTEXT', 'OUTLINE', 'EVIDENCE', 'CONTENT', 'DRAFT', 'REVISE', 'HOLD'],
}

// A deterministic failure returns to the phase that owns the broken artifact.
// In particular, OUTLINE-part phases cannot jump to REVISE, which owns existing
// Page prose rather than outlines, item rows, or evidence bindings.
const MECHANICAL_REPAIR_ROUTE = {
  CONTEXT: 'CONTEXT',
  OUTLINE: 'OUTLINE',
  EVIDENCE: 'EVIDENCE',
  CONTENT: 'CONTENT',
  DRAFT: 'REVISE',
  REVISE: 'REVISE',
  COMPILE: 'REVISE',
  CHECK: 'CONTENT',
}

const PRODUCER_RESULT = {
  type: 'object',
  required: ['actor', 'status', 'phase', 'cycle', 'route', 'reason', 'reopens_promise', 'artifacts', 'evidence'],
  properties: {
    actor: { type: 'string' },
    status: { type: 'string', enum: ['ok', 'blocked', 'failed'] },
    phase: { type: 'string', enum: ['CONTEXT', 'OUTLINE', 'EVIDENCE', 'CONTENT'] },
    cycle: { type: 'string', enum: ['PREPARE', 'SHAPE', 'SURVEY', 'LAND', 'EMBED', 'WRITE'] },
    route: { type: 'string', enum: ROUTES },
    next_cycle: { type: 'string', enum: ['PREPARE', 'SHAPE', 'SURVEY', 'LAND', 'EMBED', 'WRITE', 'CHECK'] },
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
    route: { type: 'string', enum: ROUTES },
    next_cycle: { type: 'string', enum: ['PREPARE', 'SHAPE', 'SURVEY', 'LAND', 'EMBED', 'WRITE', 'CHECK'] },
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
    `Board: ${board}\nPage: ${pageAbs}\nPage (board-relative, for the receipt): ${page}\nSnapshot label: ${label}\n\n` +
    `1. Run haipipe-board/cli/build.py on the Board.\n` +
    `2. Run haipipe-board/cli/check.py on the Board, then keep ONLY the lines whose\n` +
    `   first field is this Page's file name. mechanical_errors and mechanical_warnings\n` +
    `   are PAGE-SCOPED counts, never board-scoped: a board-scoped count makes CLOSE\n` +
    `   unreachable for every page whenever any OTHER page has an error.\n` +
    `   Use: python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board> | grep '^<page-file-name>'\n` +
    `   Report the exact matching lines in findings, and 0 when there are none.\n` +
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

log(`page-lifecycle: run=${runId}, page=${page}, start=${startPhase}, mode=${mode}, maxSteps=${maxSteps}, maxRounds=${maxRounds}`)

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
// One producer agent per current producing phase. CHECK has its own fresh,
// read-only judge and therefore does not appear here.
const PRODUCER_AGENTS = {
  CONTEXT: 'haipipe-page-context-agent',
  OUTLINE: 'haipipe-page-outline-agent',
  EVIDENCE: 'haipipe-page-evidence-agent',
  CONTENT: 'haipipe-page-content-agent',
}

// CONTEXT, OUTLINE, and CHECK inherit the session tier. EVIDENCE and CONTENT
// execute an approved plan and use the bounded high tier.
const PHASE_EFFORT = {
  EVIDENCE: 'high',
  CONTENT: 'high',
}

for (let step = 1; step <= maxSteps; step++) {
  if (current === 'CHECK') {
    phase('Check')
    const review = await agent(
      `Perform CHECK on exactly one Board Page in a fresh, read-only context.\n\n` +
      `Board: ${board}\nPage: ${pageAbs}\nPage (board-relative, for the receipt): ${page}\nExpected version: ${currentVersion.version_id}\n` +
      `Intent: ${intent}\nMode: ${mode}\nHuman gate: ${JSON.stringify(humanGate)}\n\n` +
      `Load the canonical chain: haipipe-page, haipipe-page-workflow, haipipe-page-check, the Folder-owning workflow, the exact Page Type, then its family checker. ` +
      `Run the Board's read-only checker, compute the same source:render SHA-256 identity, and HOLD if it differs from the expected version. ` +
      `Judge mechanics, function, evidence, readability, the local closing rule, and any human gate. ` +
      `Do not edit, rebuild, or cure a finding. Route to CLOSE, CONTEXT, OUTLINE, EVIDENCE, CONTENT, or HOLD, and name next_cycle when routing to a Page phase. ` +
      `CLOSE requires verdict=pass and durable evidence for every required human gate.`,
      {
        label: `check:r${round}:s${step}`,
        phase: 'Check',
        // ⑦ since 260819: the page-scoped judge; haipipe-board-reviewer-agent
        // is its base and keeps whole-board reviews. Pre-260819 receipts
        // naming the reviewer as CHECK actor stay auditable.
        agentType: 'haipipe-page-check-agent',
        schema: REVIEW_RESULT,
      }
    )

    if (!review) {
      const receipt = {
        step,
        round,
        phase: 'CHECK',
        cycle: 'CHECK',
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
        next_cycle: '',
        reopens_promise: false,
        reason: 'independent reviewer unavailable',
        artifacts: [],
        evidence: [],
        findings: ['reviewer returned no receipt'],
        human_gate: gateShape(null),
      }
      receipts.push(receipt)
      return { status: 'blocked', run_id: runId, board, page, mode, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts }
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
    if (!legalNextCycle(route, review.next_cycle)) {
      route = 'HOLD'
      reviewStatus = 'blocked'
      verdict = 'blocked'
      reason = `${reason}; reviewer omitted or mismatched next_cycle for its Page-phase route`
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
    if (route === 'CLOSE' && verdict !== 'pass') {
      route = 'HOLD'
      reviewStatus = 'blocked'
      verdict = 'blocked'
      reason = `${reason}; CLOSE requires verdict=pass`
    }
    if (route === 'CLOSE' && review.human_gate.required && (review.human_gate.status !== 'passed' || !review.human_gate.evidence.length)) {
      route = 'HOLD'
      // In AUTO this can be a DESIGNED terminal rather than a failure: the
      // loop ran end to end and stopped at the required owner or caller gate.
      // Say which authority owns it; `--owed` lists what is left.
      reason = mode === 'auto'
        ? `${reason}; AUTO reached CHECK and stopped at the required ` +
          `${ownerGateLabel}. Everything mechanical passed. See the ` +
          `owed ticks: cli/pagephase.py <page-dir> --owed`
        : `${reason}; required human gate lacks durable passed evidence`
    }
    if (step === maxSteps && !['CLOSE', 'HOLD'].includes(route)) {
      route = 'HOLD'
      reason = `${reason}; max_steps=${maxSteps} reached before another phase could run`
    }

    const receipt = {
      step,
      round,
      phase: 'CHECK',
      cycle: 'CHECK',
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
      next_cycle: review.next_cycle || '',
      reopens_promise: false,
      reason,
      artifacts: [],
      evidence: review.evidence,
      findings: review.findings,
      human_gate: review.human_gate,
    }
    receipts.push(receipt)

    if (route === 'CLOSE' || route === 'HOLD') {
      return { status: terminalStatus(route, reviewStatus === 'blocked' ? 'blocked' : 'hold'), run_id: runId, board, page, mode, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts }
    }
    parsed.cycle = review.next_cycle
    current = route
    continue
  }

  phase('Produce')
  const phaseSkill = current.toLowerCase()
  const producer = await agent(
    `Perform exactly one ${current} phase for one Board Page.\n\n` +
    `Board: ${board}\nPage: ${pageAbs}\nPage (board-relative, for the receipt): ${page}\n` +
    `Assignment packet: ${JSON.stringify(parsed)}\nCurrent round: ${round}\nCurrent version: ${currentVersion.version_id}\n\n` +
    `Read the ⚡ Brief at the top of haipipe-page-${phaseSkill} first; then load the canonical chain: haipipe-page, haipipe-page-workflow, the current phase, the Folder-owning workflow, the exact Page Type, phase policy, any selected Run workers, and the presenter. ` +
    `Follow the phase boundary. CONTEXT, OUTLINE, and EVIDENCE share haipipe-plugin-outline but may write only their own records. ` +
    `Do not rebuild, run CHECK, approve the result, touch board.md, or alter a human gate. ` +
    (mode === 'auto'
      ? `MODE: auto — nobody is watching this run. A tick that is a person's ` +
        `(approved: · verified · read: · accepted:) is DEFERRED, never waited on: ` +
        `route FORWARD on the machine half (checked:, agents/approve-rules/) and ` +
        `record the owed tick, per JL 260818 "human not to approve, they to break". ` +
        `HOLD only for a MISSING INPUT you cannot obtain or a person's standing 🛑 — ` +
        `never for an unticked gate alone. You still may not write a person's tick. `
      : `MODE: copilot — a person is attending. An unticked person-reserved gate is ` +
        `a legitimate HOLD; stop and name which tick and which file. `) +
    `Return one phase receipt and suggest the next legal route. CONTENT owns Draft, Revise, Build, and Pre-check as internal WRITE movements, not separate phases.`,
    {
      label: `${current.toLowerCase()}:r${round}:s${step}`,
      phase: 'Produce',
      agentType: PRODUCER_AGENTS[current] || 'haipipe-page-creator-agent',
      effort: PHASE_EFFORT[current],
      schema: PRODUCER_RESULT,
    }
  )

  if (!producer) {
    const receipt = {
      step,
      round,
      phase: current,
      cycle: '',
      actor: PRODUCER_AGENTS[current] || 'haipipe-page-creator-agent',
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
      next_cycle: '',
      reopens_promise: false,
      reason: 'phase producer unavailable',
      artifacts: [],
      evidence: [],
      findings: ['producer returned no receipt'],
      human_gate: gateShape(null),
    }
    receipts.push(receipt)
    return { status: 'blocked', run_id: runId, board, page, mode, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts }
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
  } else if (!legalNextCycle(route, producer.next_cycle)) {
    status = 'failed'
    route = 'HOLD'
    reason = `${reason}; producer omitted or mismatched next_cycle for its Page-phase route`
    findings = findings.concat(['producer next_cycle violated the lifecycle grammar'])
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
    route = MECHANICAL_REPAIR_ROUTE[current] || 'HOLD'
    reason = `${reason}; deterministic checker found ${afterSnapshot.mechanical_errors} error(s)`
    findings = findings.concat(afterSnapshot.findings || [])
  }
  if (step === maxSteps && !['CLOSE', 'HOLD'].includes(route)) {
    route = 'HOLD'
    reason = `${reason}; max_steps=${maxSteps} reached before another phase could run`
  }

  const receipt = {
    step,
    round,
    phase: current,
    cycle: producer.cycle,
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
    next_cycle: producer.next_cycle || '',
    reopens_promise: false,
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
    return { status: status === 'blocked' ? 'blocked' : status === 'failed' ? 'failed' : 'hold', run_id: runId, board, page, mode, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts }
  }
  parsed.cycle = producer.next_cycle
  current = route
}

return { status: 'hold', run_id: runId, board, page, mode, packet: parsed, limits: { max_steps: maxSteps, max_rounds: maxRounds }, final_version: currentVersion.version_id, receipts, reason: 'loop exhausted without terminal route' }
