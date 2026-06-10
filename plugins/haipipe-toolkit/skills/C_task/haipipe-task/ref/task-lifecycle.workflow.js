export const meta = {
  name: 'haipipe-task-lifecycle',
  description: 'Four-stage lifecycle for a task folder: Plan → Build → Execute → Report. Each stage uses a creator-reviewer loop.',
  phases: [
    { title: 'Plan', detail: 'creator drafts plan.yaml → reviewer checks → loop if revise' },
    { title: 'Build', detail: 'creator writes/fixes code → reviewer checks → loop if revise' },
    { title: 'Execute', detail: 'run the task → reviewer audits results (optional)' },
    { title: 'Report', detail: 'creator drafts report.yaml → reviewer checks → loop if revise' },
  ],
}

const folder = args && args.task_folder
if (!folder) { log('task-lifecycle: no task_folder in args'); return { status: 'blocked', reason: 'missing task_folder' } }
const hintType = (args && args.type) || null
const autoExecute = !!(args && args.autoExecute)
const autoReport = !!(args && args.autoReport)
const maxRetries = (args && args.maxRetries) || 2
log(`task-lifecycle: ${folder}, type=${hintType || 'auto'}, autoExecute=${autoExecute}, autoReport=${autoReport}, maxRetries=${maxRetries}`)

const CREATOR_RESULT = {
  type: 'object', required: ['stage', 'status'],
  properties: {
    stage: { type: 'string' },
    status: { type: 'string', enum: ['ok', 'blocked', 'failed'] },
    type: { type: 'string' },
    plan_path: { type: 'string' },
    script_plans: { type: 'array', items: { type: 'string' } },
    task_folder: { type: 'string' },
    files: { type: 'array', items: { type: 'string' } },
    report_path: { type: 'string' },
    phases: { type: 'number' },
    steps: { type: 'number' },
    verdict: { type: 'string' },
  }
}

const REVIEWER_RESULT = {
  type: 'object', required: ['verdict'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'warn', 'fail', 'revise'] },
    issues: { type: 'array', items: { type: 'string' } },
    feedback: { type: 'string' },
    sidecar: { type: 'string' },
  }
}

const RUN_RESULT = {
  type: 'object', required: ['status'],
  properties: {
    status: { type: 'string', enum: ['ok', 'failed', 'skipped'] },
    note: { type: 'string' },
  }
}

// ─── Stage 1: PLAN ─────────────────────────────────────────────
phase('Plan')
let planResult = null
let planReview = null
let planFeedback = ''

for (let attempt = 0; attempt <= maxRetries; attempt++) {
  const retryNote = attempt > 0 ? `\n\nATTEMPT ${attempt + 1}. Reviewer feedback from previous attempt:\n${planFeedback}\nAddress these specific issues.` : ''

  planResult = await agent(
    `Stage: PLAN. Task folder: ${folder}. Type hint: ${hintType || 'auto-detect from script'}.\n\n` +
    `Create IPO-compliant workflow plan files:\n` +
    `1. Read the main .py script to understand phases\n` +
    `2. Read type-specific sample: haipipe-task-for-<type>/ref/workflow-plan-sample.yaml\n` +
    `3. Read task-level template: haipipe-task/ref/workflow-template.yaml\n` +
    `4. Generate workflow/plan-script-<name>.yaml (script-level, type-specific phases)\n` +
    `5. Generate workflow/plan.yaml (task-level: Run/Gate1/Gate2)\n` +
    `Schema: B_project/haipipe-workflow/ref/plan-schema.md\n` +
    `Fields: label, type, required, prompt, files_in, files_out` + retryNote,
    { label: `plan:create:${attempt}`, phase: 'Plan', agentType: 'haipipe-task-creator-agent', schema: CREATOR_RESULT }
  )

  if (!planResult || planResult.status !== 'ok') {
    log(`Plan creator: ${planResult ? planResult.status : 'null'} — stopping`)
    break
  }

  planReview = await agent(
    `Stage: PLAN review. Task folder: ${folder}.\n\n` +
    `Review the plan files just created:\n` +
    `- workflow/plan.yaml\n` +
    `- workflow/plan-script-*.yaml\n\n` +
    `Check:\n` +
    `1. Does the plan follow B_project/haipipe-workflow/ref/plan-schema.md? (Header/I/P[S]/O)\n` +
    `2. Are all step fields canonical? (label, type, required, prompt, files_in, files_out)\n` +
    `3. Do phases match the type-specific sample for this task type?\n` +
    `4. Are files_in/files_out accurate (check actual _WorkSpace paths)?\n` +
    `5. Is the task-level plan wired correctly (Run → Gate1 → Gate2)?\n\n` +
    `Return verdict: pass (advance), warn (advance with notes), revise (loop back with feedback), fail (stop).`,
    { label: `plan:review:${attempt}`, phase: 'Plan', agentType: 'haipipe-task-reviewer-agent', schema: REVIEWER_RESULT }
  )

  log(`Plan: attempt=${attempt}, creator=${planResult.status}, reviewer=${planReview ? planReview.verdict : 'null'}`)

  if (!planReview || planReview.verdict === 'pass' || planReview.verdict === 'warn') break
  if (planReview.verdict === 'fail') break
  if (planReview.verdict === 'revise') {
    planFeedback = planReview.feedback || planReview.issues.join('; ')
  }
}

if (planReview && planReview.verdict === 'fail') {
  return { status: 'failed', stage: 'Plan', plan: planResult, review: planReview }
}

// ─── Stage 2: BUILD ────────────────────────────────────────────
phase('Build')
let buildResult = null
let buildReview = null
let buildFeedback = ''
const detectedType = (planResult && planResult.type) || hintType || 'unknown'

for (let attempt = 0; attempt <= maxRetries; attempt++) {
  const retryNote = attempt > 0 ? `\n\nATTEMPT ${attempt + 1}. Reviewer feedback from previous attempt:\n${buildFeedback}\nAddress these specific issues.` : ''

  buildResult = await agent(
    `Stage: BUILD. Task folder: ${folder}. Type: ${detectedType}.\n\n` +
    `Fix/scaffold the task-folder structure:\n` +
    `- Rename script to {NN}_{task_name}.py if needed\n` +
    `- Add # %% cell markers at logical phase boundaries\n` +
    `- Create missing configs/<run>.yaml (extract hardcoded constants)\n` +
    `- Create missing notebooks/, workflow/ dirs\n` +
    `- Update runs/<run>.sh for papermill flow\n` +
    `- Ensure Intent docstring per ref/intent-docstring-template.py\n\n` +
    `Read: haipipe-task/ref/authoring-conventions.md\n` +
    `Read: haipipe-task-for-${detectedType}/SKILL.md` + retryNote,
    { label: `build:create:${attempt}`, phase: 'Build', agentType: 'haipipe-task-creator-agent', schema: CREATOR_RESULT }
  )

  if (!buildResult || buildResult.status !== 'ok') {
    log(`Build creator: ${buildResult ? buildResult.status : 'null'} — stopping`)
    break
  }

  buildReview = await agent(
    `Stage: BUILD review (Gate 1). Task folder: ${folder}.\n\n` +
    `Review the code for intent-vs-implementation bugs:\n` +
    `1. Read the main .py script and its Intent docstring\n` +
    `2. Check for silent semantic bugs (scope, masking, metric units, split leaking)\n` +
    `3. Check four-sister compliance (configs + runs + results + notebooks)\n` +
    `4. Check that configs/<run>.yaml has all constants from the script\n\n` +
    `Write CODE_REVIEW.md in the task folder.\n` +
    `Return verdict: pass, warn, revise (with feedback for creator), or fail (stop).`,
    { label: `build:review:${attempt}`, phase: 'Build', agentType: 'haipipe-task-reviewer-agent', schema: REVIEWER_RESULT }
  )

  log(`Build: attempt=${attempt}, creator=${buildResult.status}, reviewer=${buildReview ? buildReview.verdict : 'null'}`)

  if (!buildReview || buildReview.verdict === 'pass' || buildReview.verdict === 'warn') break
  if (buildReview.verdict === 'fail') break
  if (buildReview.verdict === 'revise') {
    buildFeedback = buildReview.feedback || buildReview.issues.join('; ')
  }
}

if (buildReview && buildReview.verdict === 'fail') {
  return { status: 'failed', stage: 'Build', plan: planResult, build: buildResult, review: buildReview }
}

// ─── Stage 3: EXECUTE (optional) ───────────────────────────────
phase('Execute')
let runResult = null
let executeReview = null

if (!autoExecute) {
  log('Execute: skipped (autoExecute=false — run manually, then re-invoke with autoReport=true)')
  runResult = { status: 'skipped', note: 'autoExecute=false' }
} else {
  runResult = await agent(
    `Stage: EXECUTE. Task folder: ${folder}.\n` +
    `Run the task via runs/<RUN>.sh. Report status. Do NOT modify code.`,
    { label: 'execute:run', phase: 'Execute', schema: RUN_RESULT }
  )

  if (runResult && runResult.status === 'ok') {
    executeReview = await agent(
      `Stage: EXECUTE review (Gate 2). Task folder: ${folder}.\n\n` +
      `Audit the run results:\n` +
      `1. All expected outputs exist per workflow/plan.yaml\n` +
      `2. metrics.json well-formed\n` +
      `3. runtime.yaml consistent\n` +
      `4. No heavy artifacts in results/ (should be in _WorkSpace/)\n\n` +
      `Write RUN_AUDIT.md. Return verdict.`,
      { label: 'execute:review', phase: 'Execute', agentType: 'haipipe-task-reviewer-agent', schema: REVIEWER_RESULT }
    )
    log(`Execute: run=${runResult.status}, review=${executeReview ? executeReview.verdict : 'null'}`)
  } else {
    log(`Execute: run=${runResult ? runResult.status : 'null'}`)
  }
}

// ─── Stage 4: REPORT (optional) ────────────────────────────────
phase('Report')
let reportResult = null
let reportReview = null
let reportFeedback = ''

if (!autoReport && !autoExecute) {
  log('Report: skipped (autoReport=false)')
  reportResult = { stage: 'report', status: 'skipped' }
} else {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const retryNote = attempt > 0 ? `\n\nATTEMPT ${attempt + 1}. Reviewer feedback:\n${reportFeedback}\nAddress these issues.` : ''

    const context = [
      `Plan review: ${planReview ? planReview.verdict : 'null'}`,
      `Build review: ${buildReview ? buildReview.verdict : 'null'}`,
      `Execute: ${runResult ? runResult.status : 'null'}`,
      `Execute review: ${executeReview ? executeReview.verdict : 'null'}`,
    ].join(', ')

    reportResult = await agent(
      `Stage: REPORT. Task folder: ${folder}.\n\n` +
      `Generate report files mirroring the plan:\n` +
      `1. Read workflow/plan.yaml and workflow/plan-script-*.yaml\n` +
      `2. Read execution evidence: results/, CODE_REVIEW.md, RUN_AUDIT.md\n` +
      `3. Mirror plan structure with status/output/note per step\n` +
      `4. Follow B_project/haipipe-workflow/ref/plan-schema.md Report schema\n\n` +
      `Lifecycle context: ${context}` + retryNote,
      { label: `report:create:${attempt}`, phase: 'Report', agentType: 'haipipe-task-creator-agent', schema: CREATOR_RESULT }
    )

    if (!reportResult || reportResult.status !== 'ok') break

    reportReview = await agent(
      `Stage: REPORT review. Task folder: ${folder}.\n\n` +
      `Check the report files:\n` +
      `1. Does report mirror plan structure exactly (same phases, same steps)?\n` +
      `2. Is every step status accurate (done/skipped/failed matches reality)?\n` +
      `3. Are file existence claims correct?\n` +
      `4. Does summary.verdict reflect the gate verdicts?\n\n` +
      `Return verdict: pass, warn, revise, or fail.`,
      { label: `report:review:${attempt}`, phase: 'Report', agentType: 'haipipe-task-reviewer-agent', schema: REVIEWER_RESULT }
    )

    log(`Report: attempt=${attempt}, creator=${reportResult.status}, reviewer=${reportReview ? reportReview.verdict : 'null'}`)

    if (!reportReview || reportReview.verdict === 'pass' || reportReview.verdict === 'warn') break
    if (reportReview.verdict === 'fail') break
    if (reportReview.verdict === 'revise') {
      reportFeedback = reportReview.feedback || reportReview.issues.join('; ')
    }
  }
}

// ─── Output ────────────────────────────────────────────────────
return {
  task_folder: folder,
  type: detectedType,
  stages: {
    plan:    { creator: planResult ? planResult.status : null, reviewer: planReview ? planReview.verdict : null },
    build:   { creator: buildResult ? buildResult.status : null, reviewer: buildReview ? buildReview.verdict : null },
    execute: { run: runResult ? runResult.status : null, reviewer: executeReview ? executeReview.verdict : null },
    report:  { creator: reportResult ? reportResult.status : null, reviewer: reportReview ? reportReview.verdict : null },
  },
}
