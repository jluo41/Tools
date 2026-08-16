# venue/QBt2-for-venue — the INPUT folder of a VENUE page

This folder is the venue page's 📥 INPUT: the pack a venue page reads.

🚫 ITS DESK IS INVENTED, AND THAT IS THE ONE PLACE IN THIS GROUP WHERE INVENTING
IS THE SAFE CHOICE. Every other specimen here was made real on 260807. This one
was made real, then reverted the same day, because `QBt2`'s own Opening gives
the reason and the reason holds: a venue page states what a desk REFUSES, and a
word cap or a reference style that reads as real can be followed by mistake and
cost somebody a live submission. A figure that is wrong wastes an afternoon; a
desk rule that is wrong loses a paper.

So the pack describes the Journal of Imaginary Systems, whose host is
`jis.example.invalid` under a name RFC 2606 reserves precisely so it can never
resolve. The three pack files are archived at
`_archive/260807-prose-built/venue/QBt2-for-venue/` and this file records where
the pack's SHAPE comes from.

## The shape this pack imitates

```
🏦 SHAPE  ../../../paper/venue/playbook-utd-is/     a REAL pack, imitated not quoted
            style-profile.md          the family style: MISQ · ISR · MS-IS · MS-Marketing
            MISQ/taste.md             this desk's own taste
            MISQ/MISQ-introduction/   per-section shape, one folder each
            MISQ/MISQ-methods/        …-results · …-theory · …-discussion · …-appendix
            MISQ/examples/            real accepted papers to mirror

📥 HERE   this file: which of that pack's SHAPES this one copies
📤 OUT    the blueprint, which every section page binds to
          _fixture/misq.bst, copied to the paper root and actually used
```

That split is the same one already ruled for references: the bank lives outside
and is shared, the page keeps only what it claims, and a key claimed by two
papers is stored once. See `QB6` §7.

## Which shapes this pack copies, and from where

- `playbook-utd-is/style-profile.md` · the shared IS style, which is the family
  level rather than the journal level. Claimed for its sentence rules; the
  per-journal divergences below outrank it.
- `playbook-utd-is/MISQ/taste.md` · this desk's own taste, claimed as the
  authority whenever it disagrees with the family profile.
- `misq.bst` · the ONE real artifact taken, and copied to `_fixture/`. A
  bibliography style is machinery rather than a desk rule: following it by
  mistake formats a reference list and costs nobody a submission, and the
  fixture's References really are printed through it.
- `playbook-utd-is/MISQ/examples/` · READ, not claimed. Named here so a reader
  knows it was consulted and that no sentence was lifted from it.

## What this page does NOT claim

`misqdoc.cls` is in the bank and is not copied here. The fixture compiles as
`article`, because it is not a MISQ submission and a class it does not need
would be cargo. Recorded rather than left silent: a reader comparing this folder
with the paper root would otherwise wonder which of the two is wrong.
