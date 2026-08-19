# Q-consumer · PP01-keypress-double-path

## C2.P1.B4 · "Many phones also fire a `keydown` for the same character, so the PTY gets it twice"
"Many phones" is not a count and the page knows it: four sentences later it says
"One cheap test tells the two apart, and nobody has run it yet". The diagnosis is
read out of source only — the State row for A2.1 records that there is no mobile,
touch or composition handling anywhere in the terminal client or in `live/term.py`,
and adds "Not confirmed on a device".

## Stake
What this page loses: A2.1, whose Done-when is "one key press on a phone gives
exactly one character, with no reconnect banner in sight" — a measured count on a
real device, which is precisely what nobody has taken. The rule the division sets
(on a device with an IME the composer writes to the pseudo-terminal directly and
the terminal widget never owns the key press) is a build ordered against that
count.

And this page's own Lesson says why the count matters more here than elsewhere:
the same symptom was diagnosed twice before as duplicated listeners after a
reconnect, correctly both times. A third diagnosis taken from source alone is the
same mistake a third time. P2, JL typing a full turn on his own phone, cannot be
reached without it either.
