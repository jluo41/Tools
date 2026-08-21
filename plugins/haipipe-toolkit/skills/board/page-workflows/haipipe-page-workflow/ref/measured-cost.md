# What each phase actually costs, measured

Born 260820 when JL asked "could you document for each of them, how long it
takes for us?", after asking earlier the same day "why the evidence takes such
a long time?". Every row below is a real agent return from that day's two runs,
`QC1-visitlbp` and `QC2-visitcancer`, both on the CMSRegBoard. Nothing here is
an estimate.

**Read it for planning, not as a promise.** These are two pages on one board
with one model and one effort setting. The SHAPE is what transfers: which
phases are expensive, and why.

## The measurements

```text
phase                      what it did                       min    ktok  tools  s/tool
────────────────────────────────────────────────────────────────────────────────────────
② PROBE                    raise 10 cards, MATCH, dispatch   32.1   143.4     35    55.1
② PROBE repair 1           2 bank QA files                   10.2    12.9      1   610.5
② PROBE repair 2+3         3 bank QA files + cross-refs      14.1    15.5      2   422.9
③ EVIDENCE                 harvest 10 + bibex + 3 tables     36.5   390.6    152    14.4
④+⑤ DRAFT+REVISE fused     45 points, 6 divisions, the pdf   18.3   207.8     93    11.8
🖼 one display unit         rebuild an existing table          5.0    54.5     21    14.2
🖼 one display unit         3 equations, hand-authored tex     8.0    76.7     31    15.6
🖼 one display unit         4-row table with a guard column   13.4   122.6     56    14.4
🖼 one display unit         10-bar waterfall + zoom inset     16.8   148.6     71    14.2
────────────────────────────────────────────────────────────────────────────────────────
TOTAL of the rows above                                     154.5  1172.6
```

① OUTLINE is missing on purpose: both v2 and v3 were written on the FAST PATH,
in the main session, in a few minutes each. The one time it ran as a dispatched
agent (`260819-2317-QC1`) it cost roughly a full agent boot to produce a file a
person then rewrote, which is what taught the fast-path rule.

## What the numbers say

**Wall-clock tracks TOOL CALLS, not tokens.** Every row that reads files at
~14 s per call is doing the same thing: open, read, verify, write. EVIDENCE is
the longest phase because it made 152 of those calls, not because it thought
harder. So the honest answer to "why is this slow" is almost always "it is
opening a lot of files, one at a time".

**The two outliers prove the rule from the other side.** The bank-repair rows
sat at 400-600 s per tool call because each one is a full sub-agent dispatch
that runs its own lifecycle behind a single call. A tool count near zero with a
long wall-clock means work is happening one layer down.

**A display unit costs 5 to 17 minutes and scales with its INPUTS, not its
size.** The 4-row table took longer than the 3-equation tex block because it
froze six intake files from four different cards; the waterfall took longest
because it re-derived and cross-checked a thirteen-step chain. A rebuild of an
existing unit is the cheapest thing in the loop.

**Fanning out the display lane is the one real speedup available.** Four units
built in parallel on QC1 finished in the time of the slowest, 16.8 minutes,
against 43.2 minutes if they had run in sequence. EVIDENCE that builds its
units inline pays the full sum, which is what happened on QC2 when the phase
agent had no dispatch tool.

**A round is roughly 90 minutes and 750k tokens** when the page is new and the
plan is real: PROBE 32, EVIDENCE 37, DRAFT+REVISE 18, plus whatever CHECK adds
and whatever the bank needs repairing. A page whose evidence is already landed
skips most of that.

## The cost nobody plans for

Both expensive surprises this day were the same kind: **evidence that came back
WRONG and had to be argued down.** QC2's bank asserted the wrong personality
trait across five QA files, and correcting it took three dispatches and 24
minutes on top of the phase that found it. That is not overhead to remove; it
is the loop working. But it means a schedule built from the table above and
nothing else will be short by a third.
