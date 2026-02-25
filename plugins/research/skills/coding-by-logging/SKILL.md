Skill: coding-by-logging
========================

A structured approach to code review and iterative improvement through
documented discussions between human and AI.

---

Overview
========

This skill enables session-based code review where:

1. Claude writes findings to a log file (not just verbal feedback)
2. User reviews and adds comments with instructions
3. Claude executes changes and documents responses
4. All decisions are tracked for future reference

The log file becomes a living document of code evolution.

**CRITICAL: Keep it CONCISE and READABLE**
- Purpose: Facilitate communication between human and Claude
- NOT exhaustive documentation - just key findings and decisions
- Focus on actionable items, not verbose explanations
- Use tables and bullet points to reduce text
- Each session MUST have a timestamp for tracking

The structure is basically Session and Session's issues.

---

When to Use
===========

- Code reviews
- Refactoring sessions
- Bug fixing with multiple issues
- Architecture discussions
- Any multi-step code changes that benefit from documentation

---

File Structure
==============

**Key Rule**: One level 1 heading (`===`) per SESSION. Multiple sessions can exist in same document.

```
Session 1: {Description} ({YYYY-MM-DD HH:MM})
===============================================

Location: {file/folder path}
Status: {status indicator}

Overview
--------

{Brief overview of what this session covers}

**Severity Legend**:
- [CRITICAL] - Must fix, causes runtime errors
- [HIGH] - Should fix, causes confusion or maintenance burden
- [MEDIUM] - Consider fixing, code quality improvement
- [LOW] - Nice to have, minor improvement

Issue 1: {Issue Title}
----------------------

**Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
**Location**: `{file_path}:{line_number}`
**Problem**: {Description of what's wrong}
**Impact**: {What breaks or suffers}
**Recommendation**: {Suggested fix}

> JL: {User's instruction or feedback}
>> CC: {Claude's response and action taken}

Issue 2: {Issue Title}
----------------------

...

Changes Made
------------

**Files Modified:**
- `path/to/file1.py` - {what changed}
- `path/to/file2.py` - {what changed}

**Files Deleted:**
- `path/to/old_file.py` - {reason}

Unsolved Items
--------------

| # | Issue | Status | Notes |
|---|-------|--------|-------|
| 3 | {title} | DEFERRED | {reason} |
| 5 | {title} | TODO | {user note} |

Session 2: {Description} ({YYYY-MM-DD HH:MM})
===============================================

Overview
--------

{New issues discovered or follow-up work}

Issue 3: {Issue Title}
----------------------

...

Changes Made
------------

...
```

---

Hierarchy Rules
===============

| Element | Underline | Usage |
|---------|-----------|-------|
| Session Header | `===` | One per session (level 1) |
| Section Headers | `---` | Overview, Issues, Changes, etc. (level 2) |
| Issue Headers | `---` | Issue 1, Issue 2, etc. (level 2) |
| Subsections | **Bold** | Within issues (Severity, Location, etc.) |

**Key Pattern**:
- Each SESSION starts with `Session N: Description (Date)` underlined with `===`
- All content within a session uses `---` for sections (level 2)
- No level 3 headings - use **bold** labels instead

---

Comment Conventions
===================

**CRITICAL REQUIREMENT**: After executing ANY user comment, Claude MUST reply with `>> CC:` response.
- ALWAYS respond to every `> JL:` comment
- Responses should be BRIEF but informative (1-2 sentences)
- Include what was done AND the outcome
- Never leave a user comment without a response

**User Comments (after reviewing Claude's write-up):**

```
> JL: please do
> JL: keep as-is, I prefer this approach
> JL: let's defer this to next sprint
> JL: can you explain why this is a problem?
```

**Claude Responses (after executing):**

```
>> CC: DONE. Deleted the file and updated all imports.
>> CC: DEFERRED. This requires a larger refactor. Recommend doing separately.
>> CC: KEPT AS-IS. The current approach is acceptable because {reason}.
>> CC: {Brief answer explaining why this is a problem}
```

**Response Format**:
- Start with status marker (DONE/DEFERRED/KEPT AS-IS)
- Add 1-2 sentence explanation of what changed or why
- Be concise but complete

**Follow-up Exchanges:**

```
> JL2: What about performance impact?
>> CC2: Minimal impact. The serialization is <1ms per call.

> JL3: TODO: revisit this later
```

---

Status Markers
==============

Use these in `>> CC:` responses:

| Marker | Meaning |
|--------|---------|
| `DONE` | Change completed successfully |
| `DEFERRED` | Will do later (include reason) |
| `KEPT AS-IS` | Decided not to change (include reason) |
| `TODO` | User marked for future work |
| `UNDECIDED` | Needs more discussion |

---

Session Workflow
================

```
SESSION N
=========

Step 1: Claude Reviews
----------------------
- Claude examines code
- Writes issues to log file with:
  - Severity level
  - File location
  - Problem description
  - Recommendation

Step 2: User Reviews Log
------------------------
- User reads each issue
- Adds "> JL:" comment with instruction:
  - "please do" → execute the fix
  - "skip" or "keep as-is" → don't change
  - "defer" → mark for later
  - Question → Claude will answer

Step 3: Claude Executes
-----------------------
- Claude reads all "> JL:" comments
- Executes requested changes
- **REQUIRED**: Adds ">> CC:" response to EVERY user comment:
  - DONE + what was changed (brief, 1-2 sentences)
  - DEFERRED + why (include reason)
  - KEPT AS-IS + explanation
  - Answer to questions (concise but complete)
- **Never skip responding** - every user comment deserves acknowledgment

Step 4: Verify
--------------
- Run tests/imports to confirm changes work
- If new issues found → document in same session or start new session

Step 5: Summarize
-----------------
- List all changes made
- List unsolved/deferred items
- Session complete

         │
         ▼ (if more work needed)

SESSION N+1
===========
...
```

---

Formatting Rules
================

1. **No markdown headers** - Use `===` and `---` underlines instead of `#`, `##`, `###`

2. **Numbered issues** - Use `Issue 1:`, `Issue 2:` not `### Issue 1`

3. **Bold for labels** - Use `**Location**:`, `**Problem**:` etc.

4. **Code blocks** - Use triple backticks for code examples

5. **Tables** - Use for structured data (status summaries, etc.)

6. **Separators** - Use `---` on its own line between issues

---

Example Session Start
=====================

**Note:** This is a simplified example. Keep your actual sessions even more concise.

```
Session 1: Initial Review - Authentication Module (2026-01-14 14:30)
=====================================================================

Location: auth/login.py
Status: 🔍 Review in progress

Overview
--------

Reviewed the authentication module for security issues and code quality.
Found 5 issues ranging from CRITICAL to LOW severity.

**Overall Assessment**: Good foundation, needs security fixes

**Severity Legend**:
- [CRITICAL] - Must fix, causes runtime errors
- [HIGH] - Should fix, causes confusion or maintenance burden
- [MEDIUM] - Consider fixing, code quality improvement
- [LOW] - Nice to have, minor improvement

Issue 1: SQL Injection Vulnerability
-------------------------------------

**Severity**: [CRITICAL]
**Location**: `auth/login.py:45`
**Problem**: User input passed directly to SQL query without sanitization.
**Impact**: Attackers can execute arbitrary SQL commands.
**Recommendation**: Use parameterized queries.

> JL: please fix immediately
>> CC: DONE. Replaced string formatting with parameterized query using cursor.execute(sql, params).

Issue 2: Hardcoded Secrets
---------------------------

**Severity**: [HIGH]
**Location**: `auth/config.py:12`
**Problem**: API key stored in source code.
**Impact**: Security risk if code is leaked.
**Recommendation**: Move to environment variables.

> JL: defer to next sprint
>> CC: DEFERRED. Added to backlog for security sprint next week.

Changes Made
------------

**Files Modified:**
- `auth/login.py:45` - Fixed SQL injection using parameterized queries

**Files Deferred:**
- `auth/config.py` - Secret management (next sprint)
```

---

Balancing Detail and Readability
=================================

**General Guidance:**

| Task Complexity | Session Length | Detail Level |
|----------------|----------------|--------------|
| Simple bug fix | 50-100 lines | Minimal - just issue + fix |
| Feature review | 100-300 lines | Medium - key issues + decisions |
| Large refactor | 300-500 lines | Higher - but use tables/diagrams |
| Multi-phase project | 500+ lines | Only for complex projects like the example |

**What to Include:**
- ✅ Issue severity, location, problem statement
- ✅ User decisions (`> JL:` comments)
- ✅ Claude actions (`>> CC:` responses - brief!)
- ✅ Summary tables (changes made, unsolved items)

**What to Minimize:**
- ❌ Verbose explanations of obvious changes
- ❌ Repeated background information
- ❌ Implementation details unless critical
- ❌ Long code blocks (use file references instead)

**Remember:** If the log is too long to review in 5 minutes, it's too detailed.

---

Tips for Effective Use
======================

**PRIORITY: Keep Logs Readable and Concise**

1. **ALWAYS add timestamps** - Every session MUST have `(YYYY-MM-DD HH:MM)` in header

2. **ALWAYS respond to user comments** - Every `> JL:` gets a `>> CC:` response (1-2 sentences max)

3. **Use tables, not paragraphs** - Tables are faster to scan than long text

4. **Be brief but informative** - 1-2 sentences: what happened + outcome. No fluff.

5. **Be specific in locations** - Include `file_path:line_number` for easy navigation

6. **Focus on decisions and actions** - Not implementation details unless critical

7. **Use consistent naming** - Same user marker (JL, USER, etc.) throughout session

8. **Summarize at end** - Always list what's done and what's remaining (use tables)

9. **Avoid excessive detail** - If it's obvious from the code change, don't explain it

10. **Purpose reminder** - This log is for COMMUNICATION, not exhaustive documentation

---

Real Example
============

See `cc-logging-example.md` in this same directory for a DETAILED example of this skill
applied to a complex multi-phase refactoring project.

**IMPORTANT NOTE:** That example is VERY DETAILED (2000+ lines) because it documents
a large-scale I/O abstraction refactoring across 6 sessions. For most tasks, your
logs should be MUCH MORE CONCISE (100-500 lines per session).

**Summary of that example (6 sessions):**

- **Session 1 (2026-01-18 10:00)**: I/O operations audit
  - Inventoried 33+ filesystem operations across core files
  - Documented with tables (not verbose paragraphs)

- **Session 2 (2026-01-18 14:00)**: Storage abstraction design
  - Proposed 4-file solution with diagrams
  - User feedback integrated via `> JL:` / `>> CC:` exchanges

- **Session 3 (2026-01-18 13:45)**: Implementation Phase 1 & 2
  - Created 4 new files, refactored 4 existing files
  - Verification confirmed imports work

- **Session 4-6**: Testing, design fixes, and final implementation

**Key patterns demonstrated:**

1. **Timestamps in every session header** - tracks when work happened
2. **Tables and diagrams** - reduces text, improves readability
3. **Concise `>> CC:` responses** - 1-2 sentences, not paragraphs
4. **Clear status tracking** - DONE/TODO/DEFERRED at a glance
5. **Session continuity** - each builds on previous work

**For YOUR tasks:** Use this as a reference for structure, but keep content
much shorter. Focus on decisions and actions, not detailed explanations.

---

End of Skill Definition
