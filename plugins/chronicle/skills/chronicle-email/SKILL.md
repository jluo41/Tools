---
name: chronicle-email
description: Two modes for MS365 Outlook emails. (1) monthly-index — chronicle a full month into a markdown index file. (2) recent-window — pull last N days as a compact summary (default 7), used as input to chronicle-day-plan Phase 1. Mailbox is junjieluo.jhu@outlook.com via Softeria ms-365-mcp-server. Trigger: "/chronicle-email", "chronicle emails", "last week's emails", "summarize this week's inbox".
---

# Chronicle Email

Index emails from MS365 Outlook (`junjieluo.jhu@outlook.com`) via the
Softeria `ms-365-mcp-server` MCP. Two modes — pick by user intent.

```
mode = monthly-index   →  full month → markdown index file        (existing)
mode = recent-window   →  last N days → compact summary in-chat   (NEW)
                          (used by chronicle-day-plan Phase 1)
```

**Server**: `ms-365-mcp-server` (Softeria), launched with `--preset mail --read-only`.
Tool namespace: `mcp__ms365__*`. Token cached in macOS Keychain after one-time
device-code login (`mcp__ms365__login` → phone OAuth).

**Output locations**:
- monthly-index: `~/Desktop/jluo41-repo/3-Chronile/Emails/MonthIndex/`
- recent-window: returned in-chat (no file written by default)

## Mode: recent-window (last N days)

Pulls the last N days (default 7) of inbox messages and summarizes
in-chat. The PRIMARY consumer is `chronicle-day-plan` Phase 1 — it
asks "anything overnight needing a real reply?" and uses this as fuel.

### Verified call (confirmed working 2026-04-28)

```
tool:    mcp__ms365__list-mail-messages
filter:  receivedDateTime ge {YYYY-MM-DD}T00:00:00Z   ← last N days = today − N
orderby: receivedDateTime desc
select:  id,subject,from,receivedDateTime,bodyPreview,isRead,hasAttachments
top:     15            ← start small; raise to 30 only if days are dense
```

⚠️ Microsoft Graph rule: **do not combine `$filter` and `$search`**.
Use one or the other. For date-window pulls, `$filter` is correct.

### Response shape (what to expect)

```json
{
  "value": [
    {
      "id": "...",
      "receivedDateTime": "2026-04-28T08:34:19Z",
      "subject": "Re: ...",
      "bodyPreview": "...",
      "isRead": true,
      "hasAttachments": false,
      "from": { "emailAddress": { "name": "...", "address": "..." } }
    }
  ],
  "@odata.nextLink": "..."   // present iff more pages
}
```

### Pagination

For >15 emails, follow `@odata.nextLink` ONCE; refuse to fetch all
pages unless the user explicitly says so (avoid huge context blobs).
Or set `fetchAllPages: true` to merge — but only when user wants a
complete export, not a daily summary.

### Summarization rules (the part that goes back to the caller)

```
For each message, classify into ONE of:
  ⭐ needs-reply    real correspondence; from a known human; awaits response
  📋 fyi-internal   meeting cancellations, schedule notices, internal admin
  💸 financial      invoices, receipts, billing — flag with [$]
  📰 newsletter     bulk mail, marketing, digest — drop unless explicit ask
  🔒 security       account-security notices — drop unless they're flagging risk

Return groups in priority order (needs-reply → fyi-internal → financial),
with newsletters/security counted but not enumerated.
```

### Compact in-chat output template

```
📨 Last 7 days · N emails · M after filter

⭐ NEEDS REPLY (count)
  · 04-28  Ed Bunker         — Re: About the Dissertation Proposal
  · 04-28  Heller, Carol     — Re: Wharton poster prep
  · 04-27  Susanne Muehlsch. — Undergrad student project inclusion?
  · 04-27  attorneys@chen…   — EB-1A Evaluation

📋 FYI / INTERNAL (count)
  · 04-27  Minghong Xu       — AI Agent Lab weekly meeting (cancelled)

💸 FINANCIAL (count)
  · (none worth flagging)

(N newsletters · M security notices — dropped)
```

This compact form is what chronicle-day-plan Phase 1 uses as a SEED
for sharp prompts ("you've got 4 emails awaiting real replies — which
one needs your brain today?"). **It is not the plan output itself.**

### Anti-patterns

- ❌ Returning raw bodyPreview unfiltered → too noisy for a day plan
- ❌ Including "External Email" warning lines in summaries → strip them
- ❌ Pulling more than 15 emails for the day-plan use case → context bloat
- ❌ Persisting to a markdown file → recent-window is in-chat only;
  monthly-index is the persistent mode

---

## Mode: monthly-index (full month → markdown file)

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
- `select`: `"subject,from,receivedDateTime"`              (comma-separated string)
- `orderby`: `"receivedDateTime asc"`                      (single string)
- `fetchAllPages`: `true`

**Important**: Handle pagination properly. Monthly folders typically contain 300-600+ emails.

**Server constraint**: Cannot combine `$filter` and `$search` in the same call.
For monthly-index, no filter is needed (the folder is already scoped); for
date-windowed pulls (recent-window mode), use `$filter` only.

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
