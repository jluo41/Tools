# s22 · Word lane speed: ideas

The open ideas of this topic, one per slide.

## Is Word slow, or stuck?
- 28 minutes: 14 displays, each 2 minutes, almost to the second
- 2 minutes is AppleScript's timeout, and the placement then failed
- Word's main thread sits on a lock at 0% CPU

## What must stay
- each display at the top of the page after its citation
- real Word for what goes to co-authors
- does a draft need it too?

## It was stuck
- 28 minutes on the stuck Word
- 40 to 80 seconds on a working Word, displays at page tops
- so builds now take turns, and a stuck Word costs 30 seconds and says so

## Five ways to go faster
- a Word queue, so builds take turns: built
- a draft that skips measuring
- one Word session for all displays
- reuse the last placement when the text before did not change
- ask Word for the next page in place of searching for it
