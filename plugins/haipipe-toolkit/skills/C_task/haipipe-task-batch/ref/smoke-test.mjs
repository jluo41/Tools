// Token-free smoke test for batch-pipeline.workflow.js.
//
// Runs the REAL workflow body with the harness primitives (agent/pipeline/
// parallel/log) STUBBED — so it exercises control flow, stage chaining, the
// autoRun branch, the gate1-fail branch, and the summary mapping WITHOUT
// spawning a single agent or spending tokens.
//
//   node skills/C_task/haipipe-task-batch/ref/smoke-test.mjs
//
// Exit 0 = wiring good. Non-zero = a stage chain / branch regressed.
// This is the cheap pre-check; the live `Workflow({scriptPath}, args)` run is
// the true end-to-end test (opt-in, costs tokens).

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const HERE = dirname(fileURLToPath(import.meta.url))
const SCRIPT = join(HERE, 'batch-pipeline.workflow.js')

// ── Stubbed harness primitives ─────────────────────────────────────────────
let SCENARIO = null
const logs = []
const log = (m) => logs.push(String(m))
const phase = () => {}
const budget = { total: null, spent: () => 0, remaining: () => Infinity }
const workflow = async () => { throw new Error('nested workflow not used') }

// Faithful pipeline: each item flows through ALL stages independently; a
// throwing stage drops that item to null.
async function pipeline(items, ...stages) {
  return Promise.all(items.map(async (item, i) => {
    let acc = item
    for (const stage of stages) {
      try { acc = await stage(acc, item, i) } catch { return null }
    }
    return acc
  }))
}
async function parallel(thunks) {
  return Promise.all(thunks.map(async (t) => { try { return await t() } catch { return null } }))
}

// agent() canned returns, keyed by phase + the active scenario.
async function agent(_prompt, opts = {}) {
  const { phase: ph, label } = opts
  if (ph === 'Author') return SCENARIO.author(label)
  if (ph === 'Gate1')  return SCENARIO.gate1(label)
  if (ph === 'Run')    return { status: 'ok', exit_code: 0 }
  if (ph === 'Gate2')  return { verdict: 'pass' }
  return {}
}

// ── Load the real workflow body into an async function ──────────────────────
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const src = readFileSync(SCRIPT, 'utf8').replace('export const meta', 'const meta')
const run = new AsyncFunction('agent', 'pipeline', 'parallel', 'log', 'phase', 'args', 'budget', 'workflow', src)
const exec = (args) => run(agent, pipeline, parallel, log, phase, args, budget, workflow)

// ── Tiny assert harness ─────────────────────────────────────────────────────
let failures = 0
const check = (name, cond) => { console.log(`${cond ? '✓' : '✗ FAIL'}  ${name}`); if (!cond) failures++ }
const byName = (summary, n) => summary.find((s) => s.name === n)

const specs = (types) => types.map((t, i) => ({ type: t, name: `run_${t}_${i}`, group: 'A01', purpose: `smoke ${t}`, params: {} }))

// ── Scenario A: autoRun=false → pause after GATE 1, no run, no gate2 ─────────
SCENARIO = { author: (l) => ({ status: 'ok', task_folder: `/fake/${l}`, run_name: l, files: ['f'] }),
             gate1: () => ({ verdict: 'pass' }) }
{
  const out = await exec({ specs: specs(['training', 'data', 'eval']), autoRun: false })
  check('A: 3 results', out.summary.length === 3)
  check('A: all authored ok', out.summary.every((s) => s.authored === 'ok'))
  check('A: all gate1 pass', out.summary.every((s) => s.gate1 === 'pass'))
  check('A: run SKIPPED (autoRun=false)', out.summary.every((s) => s.run === 'skipped'))
  check('A: gate2 not run', out.summary.every((s) => s.gate2 === null))
}

// ── Scenario B: autoRun=true, one gate1=fail → that one not run ─────────────
SCENARIO = { author: (l) => ({ status: 'ok', task_folder: `/fake/${l}`, run_name: l, files: ['f'] }),
             gate1: (l) => ({ verdict: l.includes('data') ? 'fail' : 'pass' }) }
{
  const out = await exec({ specs: specs(['training', 'data', 'eval']), autoRun: true })
  const data = out.summary.find((s) => s.type === 'data')
  const others = out.summary.filter((s) => s.type !== 'data')
  check('B: gate1=fail spec NOT run', data.run === 'skipped' && data.gate2 === null)
  check('B: passing specs ran ok', others.every((s) => s.run === 'ok'))
  check('B: passing specs gate2 pass', others.every((s) => s.gate2 === 'pass'))
}

// ── Scenario C: author returns blocked → gate1 skipped, no run ───────────────
SCENARIO = { author: (l) => (l.includes('training')
               ? { status: 'blocked', missing: ['purpose'] }
               : { status: 'ok', task_folder: `/fake/${l}`, run_name: l, files: ['f'] }),
             gate1: () => ({ verdict: 'pass' }) }
{
  const out = await exec({ specs: specs(['training', 'eval']), autoRun: true })
  const blocked = out.summary.find((s) => s.type === 'training')
  check('C: blocked author surfaced', blocked.authored === 'blocked')
  check('C: blocked spec gate1 skipped', blocked.gate1 === 'skipped')
  check('C: blocked spec not run', blocked.run === null || blocked.run === 'skipped')
}

// ── Scenario D: empty specs → clean empty result ────────────────────────────
SCENARIO = { author: () => ({}), gate1: () => ({}) }
{
  const out = await exec({ specs: [], autoRun: false })
  check('D: empty specs → empty summary', Array.isArray(out.summary) && out.summary.length === 0)
}

console.log(`\n${failures === 0 ? 'PASS' : 'FAIL'} — ${failures} failing check(s)`)
process.exit(failures === 0 ? 0 : 1)
