# QA Issue Template

### Q{N}: {short title}

- **Severity**: BLOCKER | WARN | INFO
- **Where**: {file}:{line}
- **What**: {one sentence}
- **Why it matters**: {impact if not fixed}
- **Evidence**:
```
{3-10 lines of the actual code or data}
```
- **Suggested fix**: {concrete edit}
- **Status**: OPEN | FIXED | SKIPPED | DISCUSSED
- **Resolution**: {what was done, or why skipped}


# Severity Guide

| Level | Meaning | Example |
|-------|---------|---------|
| BLOCKER | Will crash or produce wrong results on real data | _ever date binarized as flag; variable not found in regression |
| WARN | Silent data quality issue or maintenance risk | stale comment; config drift between synth/full |
| INFO | Style, convention, or documentation gap | missing header comment; verbose runner |
