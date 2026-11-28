# What to change next

for: b42-s01:paper_workbench_review @ what_to_change

<!-- One card per question: ## QN · title, one short why, at most one ```text sketch``` or ![picture](f.png),
     **the question?**, then - [x] A · my pick and - [ ] B · another, then Why A: one line.
     collect.py check holds the limits; collect.py build renders the form. -->

## Q1 · Design page

Draft Lab grew from 89 dated corrections and was never written down, so a fault fixed in one view came back in another.

**Write a one-page Draft Lab design before more code?**

- [x] A · Yes: each element and when it shows, then code follows it.
- [ ] B · No: keep changing it from feedback as now.

Why A: one written design stops the same fault returning in the next view.

## Q2 · One owner

Several sessions edited the same Draft Lab files at once and broke a host and the Story view.

**Who may change Draft Lab code?**

- [x] A · One owning session; others send it requests.
- [ ] B · Any session, inside an announced window.

Why A: one writer means no collisions and one place that knows the design.

## Q3 · Release times

Shared hosts were restarted while files were half edited, so pages broke or showed old code.

**When do shared hosts pick up new code?**

- [x] A · At set times, after a private walk and the must-check gate.
- [ ] B · Whenever a session finishes a change, as now.

Why A: you only ever see code that was checked whole.

## Q4 · Lowercase s

The converter is ready and every parser reads both cases. Real drafts still mix S and s.

**When do the real drafts move to lowercase s?**

- [ ] A · Now, each Section session converting its own drafts.
- [x] B · After the AITC LOI is sent on 11-16.
- [ ] C · Never: keep reading both cases.

Why B: no risk to the AITC send; one sweep right after.

## Q5 · Gate script

The must-check rules marked auto are checked by hand or by scattered scripts today.

**Build must_check.py to run every auto rule at once?**

- [x] A · Yes, now: the gate becomes one command.
- [ ] B · Later, after the design page.

Why A: a gate nobody can run in one step gets skipped.

## Q6 · Clean-up

Two copies of the citation name lookup, 83 Draft Lab files, and 89 dated comments make the code hard to follow.

**Hold a weekly clean-up pass?**

- [x] A · Yes: merge duplicates, move dated comments into the design page.
- [ ] B · Only when something breaks.

Why A: duplicates are where fixes get missed.

## Q7 · Global rules

Eighteen of your working-style rules live only in per-SPACE memories, so a new project starts without them.

**Add them to your global CLAUDE.md?**

- [x] A · Yes, after you approve the list.
- [ ] B · No, keep them per SPACE.

Why A: every session in every project then reads them.

## Q8 · Feedback in use

While using a page you often feel "this should be different". Today it is lost or said in a chat. /hai-project feedback already files it by skill and counts repeats.

```text
💬 on the page ─▶ <skill>/feedback/ (page, element, your words) ─▶ triage ─▶ must-check row or design page
```

**How do you leave feedback while using a page?**

- [ ] A · A 💬 Feedback button on every page, saved with the page and element.
- [ ] B · Say it in any session's chat; it runs /hai-project feedback.
- [x] C · Both, into the same inbox, triaged into rules the same day.

Why C: the button catches it in the moment; chat catches the rest.
