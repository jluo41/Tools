# Deleting studio folders

for: b35-s01:studio @ studio_skill

Your Q2: each loose drawing becomes an sNN, then studio/ goes. 267 folders, 122 drawings. Four things would be lost or break first.

## Q1 · Untracked files

1,911 files in studio/ folders are not in git, so deleting them loses them for good. Most are old session folders in WellDoc and Knowledge's workspace map.

```text
WellDoc-SPACE     1,389   cowork/studio/01-lmft-postrain-260820/, legacy/, _pngs/
Knowledge-SPACE     493   studio/workspace-map/ (46 MB)
other SPACEs         29
```

**What happens to files git does not keep?**

- [x] A · Pack each SPACE's into one .tar.zst in its _WorkSpace, then delete.
- [ ] B · Delete them too; they are old.
- [ ] C · Leave those studio/ folders until their Projects' sessions look.

Why A: No studio/ left, and nothing is lost for good.

## Q2 · Question maps

Nine Blocks keep studio/question-map.excalidraw, written by the question-map code (workbench-work, haipipe-insight). Deleted, it comes back on the next build.

**Where does a Block's question map go?**

- [x] A · Its own sNN, sNN-question-map; the code writes there.
- [ ] B · Beside board.md, as question-map.excalidraw.

Why A: Every drawing is an sNN, as your note says.

## Q3 · Past the limit

A Block holds at most 9 sNN. Two would pass it: b10_project_workbench (14 now, 3 more) and Paper-TestToLearn-MS2026 (11 now, 1 more).

**May these two Blocks go past 9?**

- [x] A · Yes; the new sNN are listed for their owner to merge.
- [ ] B · No; fold each drawing into the closest existing sNN.

Why A: Nothing is lost; merging needs the owner's reading.

## Q4 · Above a Block

14 studio/ folders sit where no Block is: a Project's cowork/, Knowledge-SPACE's root, a paper Section, a server folder. They hold 9 drawings.

**Where do their drawings go?**

- [x] A · Each to its Project or Block as an sNN; the rest packed, as Q1.
- [ ] B · Pack them all, drawings too, then delete.

Why A: A drawing stays where people look; the rest is kept safely.
