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

const parsed = typeof args === 'string' ? JSON.parse(args) : (args || {})
const folder = parsed.task_folder
if (!folder) { log('task-lifecycle: no task_folder in args'); return { status: 'blocked', reason: 'missing task_folder' } }
const hintType = parsed.type || null
const stages = parsed.stages || ['plan', 'build', 'execute', 'report']
const autoExecute = !!parsed.autoExecute
const maxRetries = parsed.maxRetries || 2
const runPlan = stages.includes('plan')
const runBuild = stages.includes('build')
const runExecute = stages.includes('execute') && autoExecute
const runReport = stages.includes('report')
log(`task-lifecycle: ${folder}, type=${hintType || 'auto'}, stages=[${stages}], autoExecute=${autoExecute}, maxRetries=${maxRetries}`)

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
let planResult = null
let planReview = null
let planFeedback = ''

if (!runPlan) {
  log('Plan: skipped (not in stages)')
} else {
phase('Plan')
for (let attempt = 0; attempt <= maxRetries; attempt++) {
  const retryNote = attempt > 0 ? `\n\nATTEMPT ${attempt + 1}. Reviewer feedback from previous attempt:\n${planFeedback}\nAddress these specific issues.` : ''

  planResult = await agent(
    `Stage: PLAN. Task folder: ${folder}. Type hint: ${hintType || 'auto-detect from script'}.\n\n` +
    `Create IPO-compliant workflow plan files:\n` +
    `1. Check if workflow/plan.yaml already exists — if so, READ it and IMPROVE it (do not start from scratch)\n` +
    `2. Read the main .py script to understand phases\n` +
    `3. Read type-specific sample: haipipe-task-for-<type>/ref/workflow-plan-sample.yaml\n` +
    `4. Read task-level template: haipipe-task/ref/workflow-template.yaml\n` +
    `5. Generate/update workflow/plan-script-<name>.yaml (script-level, type-specific phases)\n` +
    `6. Generate/update workflow/plan.yaml (task-level: Run/Gate1/Gate2)\n` +
    `Schema: B_project/haipipe-workflow/ref/plan-schema.md\n` +
    `Fields: label, type, required, prompt, files_in, files_out\n\n` +
    `IMPORTANT: Every plan YAML MUST start with a comment block showing the IPO tree preview:\n` +
    `# <task-name> — <purpose>\n` +
    `#\n` +
    `# I: <input files with roles>\n` +
    `# |\n` +
    `# |-- 🔧 P1: <Phase>  [S1: <step>, S2: <step>]\n` +
    `# |-- 🔨 P2: <Phase>  [S1: <step>, S2: <step> -> <output>]\n` +
    `# |-- 🔬 P3: <Phase>  [S1: <step>]\n` +
    `# |\n` +
    `# O: { status, files_out: [...] }\n` +
    `Use phase emojis: 🔧 setup, 🔨 build/train, 🔬 analysis, 📋 summary, 🚦 gate` + retryNote,
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

  if (!planReview || planReview.verdict === 'pass') break
  if (planReview.verdict === 'fail') break
  if (planReview.verdict === 'warn' && attempt > 0) break
  if (planReview.verdict === 'warn' || planReview.verdict === 'revise') {
    planFeedback = (planReview.feedback || (planReview.issues || []).join('; ')) + '\nFix the issues above. Do not leave them as warnings.'
  }
}

if (planReview && planReview.verdict === 'fail') {
  return { status: 'failed', stage: 'Plan', plan: planResult, review: planReview }
}
} // end runPlan

// ─── Stage 2: BUILD ────────────────────────────────────────────
let buildResult = null
let buildReview = null
let buildFeedback = ''
const detectedType = (planResult && planResult.type) || hintType || 'unknown'

// Template-based types use exact copies of haistepnb/ templates.
// The build stage should VERIFY structure, not rewrite code.
const TEMPLATE_TYPES = ['data', 'fit', 'endpoint']
const isTemplateBased = TEMPLATE_TYPES.includes(detectedType)

if (!runBuild) {
  log('Build: skipped (not in stages)')
} else {
phase('Build')
for (let attempt = 0; attempt <= maxRetries; attempt++) {
  const retryNote = attempt > 0 ? `\n\nATTEMPT ${attempt + 1}. Reviewer feedback from previous attempt:\n${buildFeedback}\nAddress these specific issues.` : ''

  const templateRule = isTemplateBased
    ? `\n\nIMPORTANT: This is a TEMPLATE-BASED task (type=${detectedType}).` +
      `\nThe main .py script is an EXACT COPY of a template from code/scripts/haistepnb/.` +
      `\nDo NOT modify, rename, or recreate the .py file.` +
      `\nDo NOT create a new .py file — one already exists.` +
      `\nCONFIG is overridden at runtime by papermill, NOT by editing the file.` +
      `\nOnly verify/fix the four-sister structure: configs/ runs/ results/ notebooks/ dirs exist.`
    : ''

  buildResult = await agent(
    `Stage: BUILD. Task folder: ${folder}. Type: ${detectedType}.` +
    (isTemplateBased ? ' (template-based — DO NOT modify the .py script)' : '') +
    `\n\n` +
    (isTemplateBased
      ? `Verify the task-folder structure (do NOT touch the .py script):\n` +
        `- Verify the main .py exists and is an exact template copy (DO NOT modify it)\n` +
        `- Create missing configs/<run>.yaml if needed\n` +
        `- Create missing runs/<run>.sh if needed\n` +
        `- Create missing notebooks/, results/ dirs\n` +
        `- Verify configs/<run>.yaml has all required fields for this task type\n`
      : `Fix/scaffold the task-folder structure:\n` +
        `- Add # %% cell markers at logical phase boundaries\n` +
        `- Create missing configs/<run>.yaml (extract hardcoded constants)\n` +
        `- Create missing notebooks/, workflow/ dirs\n` +
        `- Update runs/<run>.sh for papermill flow\n` +
        `- Ensure Intent docstring per ref/intent-docstring-template.py\n`
    ) +
    `\nRead: haipipe-task/ref/authoring-conventions.md\n` +
    `Read: haipipe-task-for-${detectedType}/SKILL.md` + templateRule + retryNote,
    { label: `build:create:${attempt}`, phase: 'Build', agentType: 'haipipe-task-creator-agent', schema: CREATOR_RESULT }
  )

  if (!buildResult || buildResult.status !== 'ok') {
    log(`Build creator: ${buildResult ? buildResult.status : 'null'} — stopping`)
    break
  }

  buildReview = await agent(
    `Stage: BUILD review (Gate 1). Task folder: ${folder}. Type: ${detectedType}.` +
    (isTemplateBased ? ' (template-based)' : '') +
    `\n\n` +
    `Review the task folder:\n` +
    (isTemplateBased
      ? `1. Verify the .py is an unmodified template copy (DO NOT suggest edits to template code)\n` +
        `2. Check four-sister compliance (configs/ + runs/ + results/ + notebooks/ exist)\n` +
        `3. Check that configs/<run>.yaml has all required fields\n` +
        `4. Check that runs/<run>.sh passes CONFIG correctly via papermill\n`
      : `1. Read the main .py script and its Intent docstring\n` +
        `2. Check for silent semantic bugs (scope, masking, metric units, split leaking)\n` +
        `3. Check four-sister compliance (configs + runs + results + notebooks)\n` +
        `4. Check that configs/<run>.yaml has all constants from the script\n`
    ) +
    `\nWrite CODE_REVIEW.md in the task folder.\n` +
    `Return verdict: pass, warn, revise (with feedback for creator), or fail (stop).`,
    { label: `build:review:${attempt}`, phase: 'Build', agentType: 'haipipe-task-reviewer-agent', schema: REVIEWER_RESULT }
  )

  log(`Build: attempt=${attempt}, creator=${buildResult.status}, reviewer=${buildReview ? buildReview.verdict : 'null'}`)

  if (!buildReview || buildReview.verdict === 'pass') break
  if (buildReview.verdict === 'fail') break
  if (buildReview.verdict === 'warn' && attempt > 0) break
  if (buildReview.verdict === 'warn' || buildReview.verdict === 'revise') {
    buildFeedback = (buildReview.feedback || (buildReview.issues || []).join('; ')) + '\nFix the issues above. Do not leave them as warnings.'
  }
}

if (buildReview && buildReview.verdict === 'fail') {
  return { status: 'failed', stage: 'Build', plan: planResult, build: buildResult, review: buildReview }
}
} // end runBuild

// ─── Stage 3: EXECUTE (optional) ───────────────────────────────
let runResult = null
let executeReview = null

if (!runExecute) {
  log('Execute: skipped — run manually: bash runs/<RUN>.sh')
  runResult = { status: 'skipped', note: 'run manually or set autoExecute=true' }
} else {
  phase('Execute')
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

// ─── Stage 4: REPORT ───────────────────────────────────────────
let reportResult = null
let reportReview = null
let reportFeedback = ''

if (!runReport) {
  log('Report: skipped (not in stages)')
  reportResult = { stage: 'report', status: 'skipped' }
} else {
  phase('Report')
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
      `IMPORTANT: Every report YAML MUST start with a comment block showing the IPO tree with status emojis:\n` +
      `# <task-name> — execution report\n` +
      `#\n` +
      `# I: <input files>                          ✅\n` +
      `# |\n` +
      `# |-- 🔧 P1: <Phase>  [S1: ✅, S2: ✅ -> <output>]\n` +
      `# |-- 🔨 P2: <Phase>  [S1: ✅, S2: ⏭️ skipped]\n` +
      `# |-- 🚦 G1: review   [verdict: warn]       ✅\n` +
      `# |\n` +
      `# O: { status: ok, phases: N/N, steps: X done, Y skipped }\n\n` +
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

    if (!reportReview || reportReview.verdict === 'pass') break
    if (reportReview.verdict === 'fail') break
    if (reportReview.verdict === 'warn' && attempt > 0) break
    if (reportReview.verdict === 'warn' || reportReview.verdict === 'revise') {
      reportFeedback = (reportReview.feedback || (reportReview.issues || []).join('; ')) + '\nFix the issues above. Do not leave them as warnings.'
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
