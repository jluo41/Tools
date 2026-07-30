# Boards' place in the console

state: 🟡 PARTIAL
owner: JL
method: decide the console's top level first (individual / group / boards), then move the view

## Question
The inlab console splits everything by scope: `/individual` (one patient) and `/group` (the cohort).
A board fits neither: it belongs to a SPACE, not to a patient or a cohort.
JL 260724: "board is not individual or group level, should we have individual / group and then /board at the very beginning?"
Where does Boards sit?

It is hard because the console's whole rail is scope-filtered (DATA/INSIGHT/ACTION views take the patient or the cohort as their subject), whereas boards take the workroom as their subject: park them inside a scope and the placement lies, but invent a third scope and the rail's paradigm needs a seam.
Left alone, v1 keeps Boards inside both scopes' Action group, which is findable but implies boards are patient-or-cohort work, so the first colleague who opens `/individual` → Boards and sees skill-design boards will be confused exactly the way `QA9`'s cold read warns about.
Downstream it touches the SPA's top-level routes (`/individual` · `/group` today, registered in `main.py` so refreshes work), the rail contents per scope, and where the SPACE picker lives (`QE2`'s layer).

## Boundary
- ✅ Covered here
  **Where Boards sits in the console's information architecture**: inside the scopes, a third top-level entry, or a space-level shell above the scopes.
- ↪ Covered elsewhere
  What the Boards view shows once opened: that is `QE2`.
  Nor exposure/auth: that is `QE1`.

## Diagram

```
①  today (v1)                ②  third top-level entry        ③  SPACE shell above all
   /individual                   /individual   patient           pick SPACE first
     rail: …, Boards             /group        cohort              ↓
   /group                        /boards       the workroom      individual / group / boards
     rail: …, Boards               (no patient chrome,
   boards pretend to be            SPACE picker + boards
   scoped — they are not ❌         only)  ← my recommendation
                                                                 right shape when several
   cheap, shipped, findable      honest: three subjects —        SPACEs are truly in use;
                                 patient · cohort · workroom     overkill today
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QE5

## Items to Finish
- [x] JL picks ① / ② / ③
      **②, approved 260724** ("what is your plan?
      Please go ahead", on the plan that named ② as the recommendation). ③ stays the growth path for the day WellDoc-SPACE is really mounted; ② grows into it without rework.
- [x] Implement the chosen shape
      Done 260724: `/boards` is a third top-level page (`main.tsx` routes on the pathname, `BoardsPage` = trio toggle + full-page BoardsView, no patient chrome); `main.py` serves `/boards` for refreshes; `boards` removed from `ConsoleView`/`VIEW_META`/the Action rails; the console topbar's scope toggle gained the third button `🧭 Boards`.
      SPA rebuilt; `/boards` answers 200.
- [ ] The zero-background test
      Same bar as `QA10`: a fresh reader lands on the console and finds "where the boards live" within three seconds, and nothing implies a board belongs to a patient.

## Where we are
**② is implemented: `/boards` is the third top-level entry (260724). Only the zero-background test remains.**

- The shape now
  Three entries at the very beginning: `/individual` (patient) · `/group` (cohort) · `/boards` (the workroom).
  The boards page carries the same trio toggle and nothing patient-shaped; the two scope rails no longer list Boards.
- The history in one line
  v1 (same day, earlier) parked Boards inside both scopes' Action group; JL spotted the category error within hours: a board about the board-tool listed under a patient console; moved out the same day.
- What it cost
  Exactly the predicted amount: a pathname router in `main.tsx` + `BoardsPage` + one `@app.get("/boards")` + rail cleanup.
  `boards_api.py` untouched: it was scope-free by design.

## Files
- `web/src/Console.tsx` · `web/src/views.ts` · `web/src/types.ts`
  Where the view is registered and scoped today; ② moves it out of the rail groups into the top level.
- `main.py`
  The SPA-scope routes (`/individual`, `/group`) that make refreshes work; ② adds `/boards`.
- `boards_api.py`
  Unaffected: already scope-free.

## Discussion
> JL: another question is, board is not individual or group level, how do you think? should we have a individual / group and then /board at the very beginning?
>> CC0724: agreed: a board's subject is the workroom, not a patient or a cohort, so parking it inside the scopes was a v1 convenience, not a position. My recommendation is your instinct exactly (option ②): individual / group / boards as three top-level entries. ③ (pick the SPACE first, then scope) is the fuller shape but only earns its keep once a second real SPACE is mounted; ② grows into it without rework. Your call; the fork is laid out in the Diagram.

## Log
260724 1410 · ② implemented (JL approved the plan): /boards top-level page, trio toggle everywhere, Boards out of the scope rails; SPA rebuilt, route serves. 🔴 → 🟡; zero-background test remains
260724 1350 · Opened: JL flagged that boards are neither individual- nor group-level and proposed a top-level /board entry; three options laid out, CC recommends ② (third top-level entry), decision is JL's
