"""A throwaway board the browser drive can write into.

WHY THE DRIVE MAY NOT USE A REAL BOARD (learned the hard way, 260802). The
first version of `drive_sentence.py` drove QB5, the page it was testing. Two
things went wrong at once and both are fatal to a test: it left five cards on
a real page that a person then had to clean up by hand, and its SECOND run
found the sentences already carrying what the first run wrote, so a passing
step and a broken step became indistinguishable.

So the drive builds this instead: a two-page board in a temp folder, with
sentences shaped for each gesture, thrown away when the run ends. Writing into
it is the point, and nothing outside it can notice.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent.parent

BOARD_MD = """# Drive fixture: a board the browser test may write into

spine: Two pages of ordinary sentences, so a real browser can comment on them, put cards on their words, and edit them, without touching a board anyone reads.
close: Never. This board is rebuilt from scratch by every run of tests/drive_sentence.py.

## Topic
A fixture, not a document. Each sentence below exists to be a target for one gesture.

## Pipeline
Built by tests/fixture_board.py, driven by tests/drive_sentence.py, deleted after.

## Pages
### QA · Targets
Sentences shaped for the gestures the drive performs.
QA1-targets.md
QA2-plain.md
"""

QA1 = """# Sentences the drive writes onto
state: 🔴 OPEN
owner: CC
method: one paragraph per gesture, each with words long enough to select

## Opening
What does a sentence look like when a test is about to write on it?
It looks like any other sentence, which is the whole point of the fixture.
Each paragraph below is a target for one gesture the drive performs.
Nothing here is read by a person, so the prose only has to be ordinary.
This page exists so the real pages never have to be written on by a machine.

## Diagram

**The fixture's shape**: one paragraph per gesture the drive has to prove.

```
1  a bare sentence          -> a card is written onto its words
2  a sentence with a card   -> clicking those words opens it
3  a sentence with lanes    -> the drawer holds them, shut
4  a sentence for a comment -> a remark lands under it
5  the same sentence twice  -> every write on it must refuse
```

## Content
### 1 · Targets
**One paragraph per gesture**: what the drive does to each.

```
📄 FOUR TARGETS · one gesture each
   1.1  bare        write a card on these words
   1.2  carded      click the words, the panel opens
   1.3  laned       three lanes, folded under it
   1.4  comment     a remark lands beneath it
   1.5  twinned     identical twice, so a write cannot choose
   1.6  both       a card in the words AND lanes under the line
   1.7  broken     a card naming words that are not there
   1.8  two cards  two spans on one sentence
   1.9  multiline  a card body of three lines
   1.10 edited     double-click, replace, one record
```
📌 Establishes the targets, so the drive never has to search a real page.

#### 1.1 · A bare sentence
(nothing is attached, so a card written here proves the whole write path)
The pooled coefficient reached a stable value in the third quarter of the year.

#### 1.2 · A sentence that already carries a card
(the card is written in the source, so the drive can click it without writing first)
The estimate was drawn from the clustered specification rather than the naive one.
> Card clustered specification: The fixture's own card. Clicking these words opens this panel, which is what the drive checks first.

#### 1.3 · A sentence with three lanes
(the drawer holds them and stays shut until the sentence is clicked)
Three separate records are filed underneath this particular sentence of prose.
> Citation: A fixture citation, standing in for a real one.
> Value: 3 lanes are filed here, which is what the badge counts.
> Note: The drawer opens on a click and never on load.

#### 1.4 · A sentence waiting for a remark
(the drive selects part of it and writes a comment under it)
Someone should say whether this number was measured or merely assumed here.

#### 1.5 · A sentence written twice, on purpose
(a writer cannot tell these two apart, so every write on them must refuse)
This exact sentence is written twice on this page.
This exact sentence is written twice on this page.

#### 1.6 · A sentence carrying BOTH surfaces at once
(a card on its words and lanes under the line, which must not interfere)
The revised figure was redrawn from the second panel of the appendix table.
> Card second panel: Both surfaces on one sentence. This card sits in the words while the lanes below sit under the line.
> Citation: A lane filed under the same sentence that carries the card.
> Note: The badge counts the lanes and never counts the card.

#### 1.7 · A sentence whose card names words it does not contain
(a broken binding must be loud, because a miss nobody can see is the failure this grammar may not have)
Nothing in this sentence matches what the record below claims to point at.
> Card purple monkey dishwasher: This card names words that are not in the sentence above, so it must render as a visible row rather than disappear.

#### 1.8 · A sentence carrying two cards at once
(two spans, two panels, and neither may swallow the other)
The first estimate and the second estimate disagreed by a wide margin.
> Card first estimate: The earlier of the two, which is the one the abstract quotes.
> Card second estimate: The later of the two, computed after the sample was widened.

#### 1.9 · A card whose body runs to several lines
(a record is a run, not a line, so continuations must stay inside the panel)
The measurement was repeated under three separate conditions during the trial.
> Card three separate conditions: The first condition held the sample fixed.
> The second widened it.
> The third dropped the outliers.

#### 1.10 · A sentence the drive edits
(double-click replaces the source line and leaves one change record beside it)
This sentence will be rewritten by the drive and should keep one change record.

## Aims
### A1 · 📄 Targets
- A1.1 · Every gesture the drive performs has a sentence shaped for it.
  **Done when:** The drive reaches all four paragraphs and each one answers.

## States
### A1 · 📄 Targets
- ✅ A1.1 · Four targets, one per gesture.

## Files
### ⚙️ Engines · what RUNS this subject
- `tests/fixture_board.py`
  Writes this board into a temp folder and builds it.
"""

QA2 = """# A second page, so the board is not one page long
state: 🔴 OPEN
owner: CC
method: one ordinary page, so the index and the sidebar have something to list

## Opening
Why does the fixture need a second page at all?
A board with one page hides every defect that only appears when pages are listed.
The sidebar, the index roster, and the group page all need more than one row.
So this page holds ordinary prose and is never written on.
It exists to make the fixture shaped like a board rather than like a document.

## Diagram

**Why a second page**: what a one-page board cannot show.

```
one page   index roster of 1 · sidebar of 1 · no group page worth opening
two pages  the shapes a real board actually renders
```

## Content
### 1 · Ordinary prose
**Nothing special**: this page is scenery.

```
📄 scenery · never written on by the drive
```
📌 Establishes that the board has more than one page.

#### 1.1 · A paragraph
(plain sentences, so the page renders like any other)
This page carries no records and the drive never selects anything on it.
It is here so the index, the sidebar, and the group page have two rows to draw.

## Aims
### A1 · 📄 Ordinary prose
- A1.1 · The board renders with more than one page.
  **Done when:** The index lists two pages.

## States
### A1 · 📄 Ordinary prose
- ✅ A1.1 · Two pages.

## Files
### ⚙️ Engines · what RUNS this subject
- `tests/fixture_board.py`
  Writes this page.
"""


def build(root=None):
    """-> (board_dir, page_url_path). Caller owns the cleanup."""
    d = pathlib.Path(root or tempfile.mkdtemp(prefix="board-drive-"))
    grp = d / "QA-targets"
    grp.mkdir(parents=True, exist_ok=True)
    (d / "board.md").write_text(BOARD_MD, encoding="utf-8")
    (grp / "QA1-targets.md").write_text(QA1, encoding="utf-8")
    (grp / "QA2-plain.md").write_text(QA2, encoding="utf-8")
    r = subprocess.run([sys.executable, str(HERE / "cli" / "build.py"), str(d)],
                       capture_output=True, text=True)
    if r.returncode:
        shutil.rmtree(d, ignore_errors=True)
        raise SystemExit("fixture build failed:\n" + r.stdout + r.stderr)
    return d, "board/QA/QA1-targets.html"


if __name__ == "__main__":
    d, page = build(sys.argv[1] if len(sys.argv) > 1 else None)
    print(d)
    print(d / page)
