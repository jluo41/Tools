export const meta = {
  name: 'haipipe-task-batch',
  description: 'Fan out N C_task specs through author -> GATE 1 -> run -> GATE 2, each task-group flowing independently (pipeline). Creators chosen per task type; the 2 reviewers shared across all.',
  phases: [
    { title: 'Author', detail: 'code-creator-for-<type>-agent per spec (parallel)' },
    { title: 'Gate1', detail: 'run-script-reviewer-agent — intent <-> impl' },
    { title: 'Run', detail: 'bash runs/<RUN>.sh (only if autoRun)' },
    { title: 'Gate2', detail: 'run-result-auditor-agent — per-run trust' },
  ],
}

// args shapes accepted:
//   [ {type, name, group, purpose, params, ...}, ... ]      // bare list of specs
//   { specs: [ ...same... ], autoRun: false }               // object form + run toggle
const specs = Array.isArray(args) ? args : ((args && args.specs) || [])
const autoRun = !!(args && !Array.isArray(args) && args.autoRun)

if (!specs.length) { log('haipipe-task-batch: no specs in args; nothing to do'); return { summary: [] } }
log(`haipipe-task-batch: ${specs.length} task-group(s), autoRun=${autoRun}`)

// Structured contracts (force the subagents to return parseable objects).
const AUTHORED = { type: 'object', required: ['status'], properties: {
  status: { type: 'string', enum: ['ok', 'blocked', 'failed'] },
  task_folder: { type: 'string' }, run_name: { type: 'string' },
  files: { type: 'array', items: { type: 'string' } },
  missing: { type: 'array', items: { type: 'string' } }, note: { type: 'string' } } }
const VERDICT = { type: 'object', required: ['verdict'], properties: {
  verdict: { type: 'string', enum: ['pass', 'warn', 'fail', 'skipped'] },
  issues: { type: 'array', items: { type: 'string' } }, sidecar: { type: 'string' } } }
const RUN = { type: 'object', required: ['status'], properties: {
  status: { type: 'string', enum: ['ok', 'failed', 'skipped'] },
  exit_code: { type: 'number' }, note: { type: 'string' } } }

const results = await pipeline(
  specs,

  // 1. AUTHOR — the per-type creator calls its skill headless, then writes <TASK>.py.
  //    Prompt is self-contained so it works even if agentType doesn't resolve;
  //    agentType picks the registered specialist when it does.
  (spec) => agent(
    `Act as code-creator-for-${spec.type}-agent (a thin C_task builder).\n` +
    `Spec:\n${JSON.stringify(spec, null, 2)}\n\n` +
    `Step 1: call Skill("haipipe-task-for-${spec.type}", "<headless scaffold from this spec — ` +
    `all params present, run SILENT, no ASK>"). It returns task_folder + run_name.\n` +
    `Step 2: read skills/C_task/haipipe-task/ref/authoring-conventions.md, then author <TASK>.py ` +
    `and fill configs/<RUN>.yaml params per the spec. Heavy artifacts -> _WorkSpace/, not results/.\n` +
    `Do NOT self-review, do NOT run. Return the structured block.`,
    { label: `author:${spec.name || spec.type}`, phase: 'Author',
      agentType: `code-creator-for-${spec.type}-agent`, schema: AUTHORED }
  ).then(a => ({ ...a, _type: spec.type, _name: spec.name || spec.type })),

  // 2. GATE 1 — run-script-reviewer (type-agnostic). Skip if authoring didn't produce a folder.
  (authored, spec) => {
    if (!authored || authored.status !== 'ok') return { ...(authored || {}), gate1: { verdict: 'skipped' } }
    return agent(
      `Act as run-script-reviewer-agent. Pre-flight review (GATE 1) of task-folder ${authored.task_folder}.\n` +
      `Audit <TASK>.py vs the run Intent (silent semantic bugs: scope, masking, dims, loss target, split). ` +
      `Write CODE_REVIEW.md. Return verdict pass|warn|fail + issues.`,
      { label: `gate1:${spec.name || spec.type}`, phase: 'Gate1',
        agentType: 'run-script-reviewer-agent', schema: VERDICT }
    ).then(v => ({ ...authored, gate1: v }))
  },

  // 3. RUN — only if autoRun AND gate1 didn't fail. Default pauses here (protect GPU / human review).
  (g1, spec) => {
    if (!g1 || g1.status !== 'ok') return g1
    if (g1.gate1 && g1.gate1.verdict === 'fail') return { ...g1, run: { status: 'skipped', note: 'gate1 fail' } }
    if (!autoRun) return { ...g1, run: { status: 'skipped', note: 'autoRun=false — paused for human approval before run.sh' } }
    return agent(
      `Execute the run for ${g1.task_folder}: bash runs/<RUN>.sh for run ${g1.run_name}. ` +
      `Report status + exit_code. Do NOT modify code.`,
      { label: `run:${spec.name || spec.type}`, phase: 'Run', schema: RUN }
    ).then(r => ({ ...g1, run: r }))
  },

  // 4. GATE 2 — run-result-auditor, only if a run actually happened.
  (ran, spec) => {
    if (!ran || !ran.run || ran.run.status !== 'ok') return ran
    return agent(
      `Act as run-result-auditor-agent. Post-run audit (GATE 2) of ${ran.task_folder} run ${ran.run_name}. ` +
      `Check runtime.status==ok, exit_code==0, git_sha real, metrics.json parseable, heavy artifacts under ` +
      `_WorkSpace/ not results/. Write RUN_AUDIT.md. Return verdict pass|warn|fail.`,
      { label: `gate2:${spec.name || spec.type}`, phase: 'Gate2',
        agentType: 'run-result-auditor-agent', schema: VERDICT }
    ).then(a => ({ ...ran, gate2: a }))
  },
)

const summary = results.filter(Boolean).map(r => ({
  name: r._name || r.run_name || null,
  type: r._type || null,
  folder: r.task_folder || null,
  authored: r.status || 'failed',
  gate1: r.gate1 ? r.gate1.verdict : null,
  run: r.run ? r.run.status : null,
  gate2: r.gate2 ? r.gate2.verdict : null,
}))

log(`haipipe-task-batch done: ${summary.length} result(s)`)
return { autoRun, summary }
