---
name: chronicle-email
description: Index emails from MS365 Outlook into organized monthly markdown files. Use when the user wants to chronicle, index, or archive emails by month, or when they say /chronicle-email.
---

# Chronicle Email

Index and chronicle emails from MS365 Outlook (junjieluo.jhu@outlook.com) into organized monthly markdown index files with daily sections, reimbursement tracking, and structured formatting.

**Method**: MS365 MCP integration + structured markdown generation
**Location**: `~/Desktop/jluo41-repo/3-Chronile/Emails/MonthIndex/`

## Index Format

Monthly email indexes follow a standardized format with:
- **Header**: Total count, period coverage, reimbursement note
- **Pre-month section**: Older email threads filed into the month folder
- **Daily sections**: Organized by date with table format (Date | From | Subject)
- **Reimbursement summary**: Expense-related emails at the end

## Entry Format Example

```markdown
# 2026-01 Email Index

**Total**: 604 emails in folder `2026_01`
**Period**: Full month (Jan 1-31, 2026)

> Emails marked with **[$]** are reimbursement/receipt/expense-related.

---

## Pre-January (older threads filed into this folder)

| Date | From | Subject |
|------|------|---------|
| 2025-09-23 | Gordon Gao | Re: HBR Pitch on the Collapse and Future of Telehealth Platforms (x7) |
| 2025-12-17 | Risa Wolf | Re: Clinical-decision support for AID systems (x2) |

---

## Jan 1

| Date | From | Subject |
|------|------|---------|
| 01-01 | LinkedIn | You appeared in 30 searches |
| 01-01 | **[$]** Amazon Web Services | **Amazon Web Services Invoice Available [Account: 415909850145]** |

## Jan 2

| Date | From | Subject |
|------|------|---------|
| 01-02 | BlueStar | Let's get back on track: your weekly challenge |
| 01-02 | New York Times | Inside the unraveling U.S.-Ukraine partnership |

---

## Reimbursement & Expenses Summary

| Date | From | Subject | Notes |
|------|------|---------|-------|
| 2026-01-01 | Amazon Web Services | Amazon Web Services Invoice Available [Account: 415909850145] | AWS monthly invoice |
| 2026-01-15 | jhubillingadmin@jhu.edu | [sis-bill-notification] JHU Monthly eBill Broadcast | JHU monthly billing statement |
```

## Implementation Steps

### 1. Parameter Gathering
- **Required**: Month (e.g., "2026-01", "January 2026", or "2026_01")
- **Default**: Use previous month if not specified

### 2. MS365 Connection
```
Use mcp__ms365__login to authenticate
Use mcp__ms365__verify-login to check status
```

### 3. Locate Email Folder
Navigate folder structure to find the target month:
```
Inbox → jluo41-{YEAR} → {YEAR}_{MONTH}
Example: Inbox → jluo41-2026 → 2026_01
```

Folder naming convention:
- Parent: `jluo41-{YEAR}` (e.g., "jluo41-2026")
- Monthly: `{YEAR}_{MONTH}` (e.g., "2026_01")

### 4. Retrieve All Emails
Use `mcp__ms365__list-mail-folder-messages` with:
- `mailFolderId`: The folder ID from step 3
- `select`: `["subject", "from", "receivedDateTime"]`
- `orderby`: `["receivedDateTime asc"]`
- `fetchAllPages`: `true`

**Important**: Handle pagination properly. Monthly folders typically contain 300-600+ emails.

### 5. Process and Format Emails

**Grouping**:
- Separate pre-month emails (before first day of target month)
- Group by day for the target month
- Track duplicates (same sender + same subject on same day)

**Date Formatting**:
- Pre-month: Use `YYYY-MM-DD` format
- Target month: Use `MM-DD` format for daily sections
- Section headers: Use "Jan 1", "Feb 15" style (month abbreviation + day)

**Reimbursement Detection**:
Mark emails with **[$]** if subject or sender contains keywords:
- Financial: `invoice`, `receipt`, `billing`, `payment`, `order confirmation`, `reimbursement`
- Vendors: `Amazon Web Services`, `AWS`, `Uber`, `cybersource`, `expense`
- JHU: `ebill`, `billing statement`

**Duplicate Handling**:
When same sender sends multiple emails with identical subject on same day:
- First occurrence: Show normally
- Subsequent: Add `(x2)`, `(x3)`, etc. suffix to subject

### 6. Write Output File

**File path**: `~/Desktop/jluo41-repo/3-Chronile/Emails/MonthIndex/{YEAR}-{MONTH}-index.md`

**File structure**:
1. Header with total count and period
2. Reimbursement note
3. Horizontal rule `---`
4. Pre-month section (if applicable)
5. Horizontal rule `---`
6. Daily sections for each day with emails
7. Horizontal rule `---`
8. Reimbursement & Expenses Summary

### 7. Context Optimization

To save context tokens:
- Use Task/general-purpose agent for email retrieval and processing
- Process data in background agents when dealing with 500+ emails
- Only load final formatted output into main conversation

## Writing Style Guidelines

**Subject Lines**:
- Preserve original subject exactly as received
- Bold entire subject line for reimbursement emails
- Add duplicate count suffix when applicable

**Sender Names**:
- Use `from.emailAddress.name` field (display name)
- If display name is empty, use email address prefix

**Table Formatting**:
- Keep columns aligned with pipes `|`
- Use consistent spacing
- No line breaks within table rows

## Error Handling

- If MS365 not logged in, authenticate first
- If folder not found, check folder structure and year
- If no emails in period, create minimal index noting "0 emails"
- If partial month, note date range in period field

## Reimbursement Summary Guidelines

For each expense-related email, provide:
- **Date**: Full `YYYY-MM-DD` format
- **From**: Sender name or organization
- **Subject**: Full subject line (without **[$]** markers)
- **Notes**: Brief categorization (e.g., "AWS monthly invoice", "Uber ride receipt")

## Usage Examples

**User request**: "Chronicle emails for January 2026"
**Action**:
1. Connect to MS365
2. Find `2026_01` folder
3. Retrieve all emails
4. Generate index at `3-Chronile/Emails/MonthIndex/2026-01-index.md`

**User request**: "/chronicle-email 2025-12"
**Action**: Process December 2025 emails from `2025_12` folder

**User request**: "Update my email chronicle for last month"
**Action**: Auto-detect previous month and process accordingly

## Tags Strategy

No tags needed for this skill (unlike logseq-cc-records). The Chronicle system uses folder-based organization.

## Output Confirmation

After successful indexing, report to user:
- Total emails indexed
- Number of expense-related emails
- File location
- Date range covered
