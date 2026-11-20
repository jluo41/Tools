# A01 · A topic about real work is a manual too

> "make the studio like a things like manual to show how things work. we can help people to understand what is the progress/" (JL 261118, a note-sync setup)

## 1. Need
JL set up a note sync (a database on one machine, a tunnel, three devices). He wanted one
Studio topic that a newcomer opens to learn how a note travels between devices and how far the setup is.

## 2. Now
`haipipe-studio/SKILL.md` § "First principle: a Studio is never a report" says "No bookkeeping on screen:
decided, started, counts and dates belong in a round's record and in Report". `five_parts.py` draws Idea,
Now, Design, Process, Delivery; Now lists the delivery's parts, decided and open lines from the face. The
first LiveSync drawing (`s01-how-livesync-works.png`, 261118 15:37) showed the flow but no step states.

## 3. Gap
The First principle forbids progress on a Studio, and `five_parts.now()` had no input for it. A topic about
running work (a service, a setup) therefore had no allowed place to say where the work stands.

## 4. Methods
1. Leave progress to a Report page: keeps the principle, but JL reads the Studio, not a separate report; rejected.
2. A constitution exception: a topic about running work is a manual and shows its state; the principle
   stays for idea topics. Chosen: smallest change, matches what JL asked.
3. Fix only the LiveSync drawing by hand: the next setup topic repeats the problem; rejected.

## 5. Update
- `haipipe-studio/CONSTITUTION.md`: A01, wins over the First principle for running work
- `s01-how-livesync-works/`: Design A draws the real path; 10 progress steps

Cases: ✅ b01_livesync s01 (A7) · ⬜ other Studio topics about a service or setup, not audited.
Run: `grep` for sync.example.test, notes_vault and "progress, live" in the s01 canvas; `constitution.py --check` ✅ (261118).

## 6. Never again
The constitution line at the top of `haipipe-studio/SKILL.md` makes every agent read A01 before the First
principle. Open risk: the Run line checks only s01; an unaudited running-work topic can still lack progress
until a reviewer reads it.
