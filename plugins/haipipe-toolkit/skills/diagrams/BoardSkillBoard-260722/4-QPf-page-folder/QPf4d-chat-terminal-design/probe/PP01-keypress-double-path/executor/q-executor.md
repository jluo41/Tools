# Q · how many characters one key press delivers on a touch keyboard

A browser terminal built on xterm.js takes typing through a hidden textarea. On a
device with an on-screen keyboard — an input method that composes, autocorrects
and predicts — that textarea can fire a `keydown` AND an `input` /
`compositionend` for the same character.

On at least one real touch device (iOS Safari and Android Chrome if both are
reachable), type single characters into such a terminal and report:

- how many characters arrive at the pseudo-terminal per key press
- which event path delivered each one: `keydown`, `input`, or `compositionend`
- whether the doubling starts at the very first key press, or only after a
  reconnect notice has appeared
- the device, the operating system version and the browser version

A minimal xterm.js page attached to a local pseudo-terminal is enough to
reproduce the paths if no larger application is at hand. Desktop browser mobile
emulation does not answer this: it does not use the device's input method.

Deliverable: a QA digest plus the captured event log for a few key presses.
Accepted: a per-press count with the delivering event named | no touch device
could be reached, stated as such.
