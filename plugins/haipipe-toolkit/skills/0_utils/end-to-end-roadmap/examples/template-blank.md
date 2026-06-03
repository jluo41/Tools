---
name: project-name
description: One-line summary of the project
metadata:
  version: "1.0.0"
  start_date: "YYYY-MM-DD"
  last_updated: "YYYY-MM-DD"
  expected_completion: "YYYY-MM-DD (optional)"
---

# Roadmap: project-name

## START: [Describe your current state]

Example: "Have raw data in 5 CSV files (10GB total)"

- What data/files do you have?
- What environment is set up? (Python, dependencies, etc.)
- Any prerequisites?

| 脚本 | 输入 | 输出 | 成功率 | 状态 |
|------|------|------|--------|------|
| stage_1.py | TBD | TBD | TBD | ⬜ pending |
| stage_2.py | TBD | TBD | TBD | ⬜ pending |
| stage_3.py | TBD | TBD | TBD | ⬜ pending |

## END: [Describe your desired end state]

Example: "Have published findings (PDF report + dashboard)"

- What's the final deliverable?
- How will you measure success?
- What should the output look like?

---

## How to Fill This Template

1. **Update frontmatter:** name, description, dates
2. **Write START section:** 2-3 sentences on current state
3. **Add stages:** One row per stage in the table
   - **脚本:** Name of the script/code (e.g., "clean_data.py")
   - **输入:** What data goes in (e.g., "raw CSV")
   - **输出:** What data comes out (e.g., "cleaned parquet")
   - **成功率:** How to measure success (e.g., "0 NaN values", "98% accuracy")
   - **状态:** One of: `⬜ pending`, `⏳ running`, `✅ done`, `❌ failed`
4. **Write END section:** 2-3 sentences on desired final state
5. **Use roadmap:**
   ```bash
   # Ask Claude to analyze and report progress
   python statusline_reporter.py status <this-file>
   ```

## Example: Data Pipeline

```markdown
| 脚本 | 输入 | 输出 | 成功率 | 状态 |
|------|------|------|--------|------|
| 1_ingest.py | S3 CSV files | Pandas DataFrame | 100% of files loaded | ⏳ running |
| 2_clean.py | Raw DataFrame | Deduped, imputed | 0 NaN values | ⬜ pending |
| 3_feature_engineer.py | Clean data | Features for ML | 50+ features | ⬜ pending |
| 4_train.py | Features + labels | Trained model | 95% val accuracy | ⬜ pending |
| 5_deploy.py | Model + code | Live API endpoint | Latency <100ms | ⬜ pending |
```

## Example: Research Project

```markdown
| 脚本 | 输入 | 输出 | 成功率 | 状态 |
|------|------|------|--------|------|
| 1_lit_review.py | Scholar DB query | Annotated papers.json | 100+ papers reviewed | ✅ done |
| 2_analyze.py | papers.json | Analysis report | 5+ key findings | ⏳ running |
| 3_write_paper.py | Analysis + figures | Manuscript.tex | Draft complete | ⬜ pending |
| 4_submit.py | Manuscript + figs | Submission receipt | Submitted to venue | ⬜ pending |
```

## Tips

- **Keep metrics specific:** "done" is vague; "5/10 stages complete" or "98% accuracy" is clear
- **Update frequently:** After each stage, update the status row
- **Track blockers:** Add a "Blockers" section if you hit issues
- **Share with team:** This markdown can be version-controlled + shared

---

## Progress Notes

(Add notes as you work. E.g., "Stage 1 took 3 hours due to slow S3 access")

## Blockers / Risks

(Note any impediments here)

## Next Steps

(What should happen next?)
