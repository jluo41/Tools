# QPf4d-chat-terminal-design · outline v1
outline-version: v1
supersedes: —
date: 260817
approved: ⬜            🚧 a person ticks this. No machine may.

Generated 260817 from this page's own divisions, face-figure captions and
sentences, so no bullet claims anything the page does not already say.
UNAPPROVED, so it is a working document: rewrite it, delete what is wrong.

## C1 · Why the phone problems all arrive at once

### C1.P1 · the four things that decide whether a form works on a device, and each device's answer
- B1 · This page works from one model: a device is not a screen size, it is four limits at once.   🖼 owed · table
- B2 · A form only works where all four hold.   ✅ have it
- B3 · The terminal has exactly one form, the raw TTY grid, and that form expects the desktop answer to every one of the four.   ✅ have it
- B4 · So the phone failures arrive together rather than one at a time.
- B5 · It is also why fixing them one at a time has not worked: each symptom is a different limit broken by the same expectation.   ✅ have it
- B6 · The four limits are also the checklist for any new form, and `## Aims` is ordered by them.   🎯 A1.1

## C2 · One press on a phone, two letters on screen

### C2.P1 · how the same key press reaches the PTY twice on a phone
- B1 · A phone keyboard is an IME: an input helper that composes, guesses and corrects while you type.   📚 citation
- B2 · Typing rides xterm's hidden textarea.   ✅ have it
- B3 · On a phone that textarea has two live paths, because the composition and `input` events are what an IME, autocorrect and predictive text all need.   🖼 owed · diagram
- B4 · Many phones also fire a `keydown` for the same character, so the PTY gets it twice.   🔢 value · PP01
- B5 · This has to be a rule, not one more patch.   🎯 A2.1
- B6 · The same symptom was found and fixed twice on `QD3`, both times as duplicated `onData` listeners after a reconnect, and that fix is present and correct today.   ✅ have it
- B7 · So a phone showing the same symptom is a third cause.
- B8 · ⚠️ 5 more sentences in this division are not planned here yet   🎯 aim

## C3 · Too narrow to read, even when the drawing is right

### C3.P1 · why a correct repaint can still be unreadable
- B1 · `QD3` closed a shredded-screen round on 260801 by nudging the width on attach.   ✅ have it
- B2 · The app then repaints at the size the browser really has, and that was the right fix for a desktop, where the true width still fits the art.   ✅ have it
- B3 · A phone does not clear that bar.
- B4 · About 390 CSS pixels at 13px metrics is roughly 46 columns, and Claude's frames are drawn for far more.   🔢 value · PP02
- B5 · So a correct repaint at the true width is still one nobody can read.   🖼 owed · figure
- B6 · This is the line the page names.   🎯 A3.1
- B7 · Above it, polishing the grid pays.   ✅ have it
- B8 · ⚠️ 2 more sentences in this division are not planned here yet   🎯 aim

## C4 · You come back, and the pane is dead

### C4.P1 · how many handlers the board registers for each direction
- B1 · A desktop tab mostly stays open, so the board could get away with tearing things down on the way out and never rebuilding them on the way back.   ✅ have it
- B2 · A phone sleeps on every app switch, and that turns the missing rebuild into the most visible failure of all.   ✅ have it
- B3 · The terminal half parks correctly, so the process stays alive.   ✅ have it
- B4 · But nothing reattaches the socket, so the reader comes back to a dead pane in front of a living process, and it never heals itself.   🎯 A4.1
- B5 · The chat half stalls instead of dying.
- B6 · A sleeping streaming `fetch` can hang without resolving or rejecting, so the `await` never returns, the `catch` never runs, and the cleanup that clears `inflight` never runs either.
- B7 · It does recover, after `QUIET_GIVEUP`, 420000 on a real send, seven minutes.   🔢 value
- B8 · ⚠️ 7 more sentences in this division are not planned here yet   🎯 aim

## C5 · If a finger cannot reach it, a phone cannot use it

### C5.P1 · each thing you can do, the gesture that reaches it on each device, and its answer
- B1 · A feature can be fully built on the server and still be out of reach, because reach belongs to the gesture, not to the feature.   🖼 owed · table
- B2 · `/_board/image` already worked on any device, and both ways in were `paste` listeners, so a phone could not put an image on the board at all.
- B3 · The whole gap was one missing button.   ✅ have it
- B4 · That one is now closed, and the fix has the shape every later one should copy.   ✅ have it
- B5 · The browser re-encodes the photo before posting, because `live/write.py` caps at 8MB and rejects HEIC.   🔢 value
- B6 · So the gesture respects what the endpoint allows, rather than the endpoint loosening for the device.   ✅ have it
- B7 · The audit also corrected one belief: the session picker was thought to be hidden in terminal view, and it is not.   ✅ have it
- B8 · ⚠️ 1 more sentences in this division are not planned here yet   🎯 aim

## C6 · Why the chat panel beside it reads so much better

### C6.P1 · what each pane can show, and which defects survive any amount of CSS
- B1 · On 260801 JL put the desktop terminal pane beside the SDK chat panel and called it the worse of the two.   🖼 owed · figure
- B2 · Reading it off the screenshot against the CSS turned one impression into five separate defects.
- B3 · The session rail takes a full-height white column for one id chip and a ＋, and the black terminal starts beside it, so the pane reads as an L-shaped gutter.   🎯 A6.2
- B4 · The pane also has three unconnected colour zones: a white header, a black body, and a white footer holding the Quick actions and Settings pills.   🎯 A6.1
- B5 · Nothing ties them together: no shared border, no shared rounded corner, no shared padding.   🎯 A6.1
- B6 · CJK runs off the right edge instead of wrapping, cutting a word in half.   ✅ have it
- B7 · That is the wcwidth defect `QD3` already names: xterm's Unicode 6 tables call a CJK cell one column while the PTY counts two.   📚 citation
- B8 · ⚠️ 9 more sentences in this division are not planned here yet   🎯 aim

