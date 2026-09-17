# `question` · register one question the person asked in plain words

The person types a question and nothing else. This verb decides everything
the row needs, which register faces it, which partitions it runs on, where it
grew out of, then writes ONE row. It never answers the question.

Input: `/haipipe-insight application <root> question "<text>"`
(the Insight Board's Ask box produces exactly this line).

1. Resolve the InsightBoard. Read `0-MT-meta/MT00-meta/MT00-meta.md` for the
   Partition Register (letter, name, filter per group) and the four registers
   `MT01-question-data` to `MT04-question-wisdom` for the questions already
   asked. If the same ask is already a row, return that id; never mint a twin.
2. Decide the LEVEL from the kind of answer the words want, the lowest rung
   that can answer it:

   ```text
   D  Data          "what is in", "how many", "which fields", "who was sent"     observe
   I  Information   "how does X vary", "rate", "over time", "by group", "gap"    derive
   K  Knowledge     "does X matter", "is it true that", "can we", "works best"   claim
   W  Wisdom        "what should we do", "which to send", "recommend", "next"    counsel
   ```

   A W or K question the board cannot yet warrant is still registered at its
   own level; `chain` opens the missing rungs beneath it one at a time.
3. Decide the PARTITIONS, and say why for each:
   - F always, because F is the template ladder every group mirrors;
   - the named group(s) when the words name an audience the register has a
     column for (an age band, a gender, a region);
   - every registered column when the words ask whether groups DIFFER;
   - X alone when the ask is "do the partitions differ" or "pool or split",
     because X is the only group allowed to compare;
   - never a partition the register has no column for: name the missing
     column and stop, so a person adds it first.
4. Find the LINEAGE:
   - origin `need-driven` when a Brief, a decision or the person's stated need
     raised it; `curiosity-driven` when a Result on this board raised it;
   - parent: the row that raised it, found by searching the ask's nouns
     through the I/K pages' Null and Contradiction divisions and their dated
     log lines, written as page id and row id (`FI08 · I3`), or a Brief need
     (`BR00 A6.1`), or an earlier question (`QI9`); otherwise `new`.
5. Write the row with the board tool, run from
   `Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/`:

   ```text
   python3 -m live.insightboard ask <board-folder> <D|I|K> <F,B,C> "<text>" \
       --origin <curiosity-driven|need-driven> --parent "<FI08 · I3 | QI9 | BR00 A6.1 | new>"
   ```

   It appends the row to the right register with `⬜ open` in each chosen
   column and `·` elsewhere, writes one dated receipt line carrying origin and
   parent into the register's log (`outline/<register-stem>-log.md` when the
   board keeps one, else the register page's own Log division), and refuses
   what it cannot do (an empty ask, a missing column).
   For W the tool refuses, because `MT04` keeps a transposed grid: add the
   row by hand, one `QW<n>` line in the left column and one `⬜ open` per
   partition row, then the same receipt line.
6. Report the id, the level with its reason, the partitions with their
   reasons, origin and parent, and the next command:
   `/haipipe-insight application <root> chain <id> <first partition>`.

Ask only. A question phrased so that only one answer is admissible is
rewritten before registration so that "do nothing" is a legal answer
(`haipipe-insight-question` §Writing Style). The row carries the ask, its
partitions and its provenance; the answer lives on the chain pages.

Return the register path, the new id, the cells opened, the parent, and the
next verb.
