# `verdict` · drive the X group to its pooling verdict

Partition-major boards only. X is the one group allowed to compare, and every
W page on the board is CONDITIONED on X's verdict (`ref/partition.md` §The
pooling verdict conditions every W page). Rung-major boards have no X group
and no verdict; `chain` opens their W pages directly.

1. Resolve the board and check the precondition: the template F and every
   registered partition group have settled the K mirror of the questions the
   verdict will compare, one `chain` per cell. A mirror a partition cannot
   carry is a registered refusal (`🚫` with a reason) on the owning register,
   never a silent gap; a refusal is a legal input to the verdict.
2. Register the X questions if absent, through `question`, each with column
   X only: one Information contrast ("how large is the gap between the
   partitions?") and one Knowledge verdict ("pool or serve them separately?"),
   optionally a Knowledge heterogeneity question between them. On A00 these
   are `QI14 → XI01`, `QK15 → XK01`, `QK16 → XK02`.
3. Open the X pages with `chain`, in this order and one page per step:

   ```text
   XI01  the contrast       derives the between-partition differences from the
                            partitions' own settled I rows · no data of its own
   XK01  heterogeneity      claims whether the partitions genuinely differ, with
                            strength, unresolved rivals and boundary
   XK02  the verdict        states exactly POOL or SPLIT as an exchangeability
                            claim, citing XK01, naming every compared partition
   ```

4. Run each page through the Page workflow to CHECK/CLOSE. GI4 on the verdict
   page is per-column-set: it passes only when the verdict word is exactly one
   of the two and every compared partition is named with its strength.
5. Settle the three X cells on their registers (`settle`), then apply the
   verdict to the W pages:

   ```text
   POOL    every non-template W page DEFERS, explicitly and by id, to F's W
           page, and exports no handoff; F's W page carries the one counsel
   SPLIT   the differing partition's W page may counsel its own action and
           cites XK02 as the birth certificate a child board must also cite
   ```

Nothing before XK02 may say "pool" or "split"; a per-partition page that
compares is a violation of `ref/partition.md` rule 3, not a shortcut. A
partition newly registered after the verdict reopens XK02, because the
verdict names the partitions it covers.

Return the X page paths, the verdict word, the partitions it covers and their
strengths, and which W pages are now unlocked under which rule.
