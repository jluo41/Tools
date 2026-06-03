---
name: end-to-end-roadmap
description: Template skill to document and track any multi-stage E2E project
metadata:
  version: "1.0.0"
  last_updated: "2026-06-02"
  use_case: "progress tracking, status reporting, milestone planning"
---

# Skill: end-to-end-roadmap

A meta-skill template for documenting any END-TO-END project with clear START state, N stages (milestones), and END goal. Includes roadmap generation, Claude-based status reporting, and structured progress tracking.

## When to Use

- You have a multi-stage project (3+ stages)
- Each stage has: a script/tool, inputs, outputs, success metrics
- You want: repeatable documentation + automated progress reporting
- Examples: data pipeline, ML training, research project, feature rollout

Trigger phrases:
- "document E2E roadmap"
- "track project progress"
- "show where we are in the pipeline"

## Structure

Every E2E roadmap follows:

```
# Roadmap: {Project Name}

## START: {What we have now}
(Current state, input data, prerequisites)

| 脚本 | 输入 | 输出 | 成功率 | 状态 |
|------|------|------|--------|------|
| stage_1.py | X | Y | metric | ✅ done |
| stage_2.py | Y | Z | metric | ⏳ running |
| stage_N.py | ... | ... | metric | ⬜ pending |

## END: {What we want to achieve}
(Final deliverable, success criteria)
```

## Commands

### Create new roadmap
```bash
python roadmap_generator.py create "project-name" \
  --start "have raw data files (csv, json)" \
  --stages "clean,analyze,visualize,report" \
  --end "published findings (PDF report + dashboard)"
```

Creates: `_WorkSpace/project-name/roadmap.md`

### Show status (ask Claude to analyze)
```bash
python statusline_reporter.py status _WorkSpace/project-name/roadmap.md
```

Claude analyzes the markdown and returns:
- Current phase (which stage we're in)
- Progress % (how many stages done)
- Next action (what to do next)
- Blockers (if any marked in roadmap)

### Update stage status
```bash
python roadmap_generator.py update _WorkSpace/project-name/roadmap.md \
  --stage 2 \
  --status "done" \
  --metric "98.5% accuracy"
```

## Example: Food-to-Description Roadmap

See `examples/food-to-nutrition-roadmap.md` for a filled example using the food-to-description skill.

```markdown
# Roadmap: food-to-description

## START: Have Shanghai diet.parquet (3,470 meals)

| 脚本 | 输入 | 输出 | 成功率 | 状态 |
|------|------|------|--------|------|
| 1_decompose.py | FoodName (free text) | (food, amount_g) tuples | 2,018 unique components | ✅ done |
| 2_retrieve.py | food_name | Top-10 USDA candidates | 62.8% rank-1 match | ✅ done |
| 3_llm_rerank.py | food + candidates | Best fdc_id (WEAK/MISS only) | ~90-95% expected | ⏳ running |
| 4_aggregate.py | fdc_id + amount | Nutrition (Cal/Carbs/Pro/Fat/Fib) | 3,470 rows filled | ⬜ pending |

## END: Output parquet with filled nutrition columns

(Calories, Carbs, Protein, Fat, Fiber)
```

## Roadmap Format Details

### Frontmatter (YAML)
```yaml
---
name: project-name
description: One-line summary
metadata:
  version: "1.0.0"
  start_date: "2026-06-02"
  last_updated: "2026-06-02"
  expected_completion: "2026-06-10"
---
```

### START Section
Describe current state:
- What data/files you have
- Environment setup (Python version, dependencies)
- Known prerequisites

### Stage Table
Each row = one stage:
- **脚本** (Script): Which file/command runs this stage
- **输入** (Input): What data flows in
- **输出** (Output): What data flows out
- **成功率** (Success Metric): How to measure success (%, count, coverage)
- **状态** (Status): One of:
  - ✅ done
  - ⏳ running
  - ❌ failed
  - ⬜ pending

### END Section
Describe desired final state:
- Output deliverables
- Success criteria
- Timeline target

## Status Reporting (Claude)

Running `/statusline_reporter.py status <roadmap.md>` triggers Claude to:
1. Parse the roadmap markdown
2. Extract: START, stages, END, current status
3. Analyze: which stage is active, what's next
4. Report back with:
   - 📊 Emoji dashboard showing progress
   - 📝 Prose summary (current phase, blockers, next action)
   - 💾 Suggested updates to markdown

Example output:
```
📊 Roadmap Progress: food-to-description

Current Phase: Stage 3 (LLM Rerank)
Progress: 3/4 stages started, 2 complete
Next Action: Continue Stage 3 (1,676 calls, ~45 calls/min ETA)
Blockers: None
Expected Completion: 2026-06-02 ~3 hours

Dashboard:
📥 Stage 1: ✅ done (2,018 components)
📊 Stage 2: ✅ done (62.8% rank-1)
🧠 Stage 3: ⏳ running (150/1,676 reranked)
📤 Stage 4: ⬜ pending (waiting for stage 3)
```

## Reusable Template

Use `examples/template-blank.md` as a starting point for any new project:

```bash
cp examples/template-blank.md _WorkSpace/my-project/roadmap.md
# Edit: fill in START, stages, END
python statusline_reporter.py status _WorkSpace/my-project/roadmap.md
```

## Implementation Details

### Files
- `roadmap_generator.py` — Create/update roadmap markdown files
- `statusline_reporter.py` — Ask Claude to analyze roadmap + report status
- `examples/food-to-nutrition-roadmap.md` — Filled example (food-to-description)
- `examples/template-blank.md` — Blank template for new projects
- `examples/tutorial.md` — Step-by-step guide

### Design

1. **Markdown as source of truth:** Human-readable, version-controllable, Claude-readable
2. **Claude for analysis:** Natural language understanding of progress, blocker detection, next-step reasoning
3. **Extensible:** Works with any pipeline, any stage count, any metrics

## Troubleshooting

### "Claude fails to parse my roadmap"
- Ensure frontmatter is valid YAML (`---` delimiters, proper indentation)
- Table must have exactly 5 columns: 脚本, 输入, 输出, 成功率, 状态
- Status must be emoji + word: `✅ done`, `⏳ running`, `❌ failed`, `⬜ pending`

### "I want to track more columns"
- Add extra columns after "状态" (they'll be ignored by Claude)
- Or create a custom reporter (roadmap_generator.py is extensible)

### "How do I integrate with CI/CD?"
- Run `/statusline_reporter.py status` in a cron job
- Parse output, send to Slack/email
- Or write custom webhook to update status

## See Also

- `food-to-description` skill: Real example using this roadmap template
- DIKW framework skills: Plan → Design → Implement → Verify

---

**Specialist tail:**

```
status:    ok
summary:   "end-to-end-roadmap v1.0: template + generator for any E2E project"
artifacts: [roadmap_generator.py, statusline_reporter.py, examples/]
next:      Use food-to-description skill as reference implementation; create new roadmap for your project
```
