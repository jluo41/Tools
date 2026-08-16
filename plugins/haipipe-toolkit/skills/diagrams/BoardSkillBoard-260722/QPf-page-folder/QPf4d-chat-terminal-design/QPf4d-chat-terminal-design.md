# Chat · the terminal's form on the device holding it

state: 🗂 FOLDED · into QPf4-chat §6 the form per device (JL 260815) · the full record stays here
owner: JL
method: design the terminal's FORM against a device's four constraints: how many columns it has, how a keystroke arrives, what a pointer can do, and whether the page is allowed to stay awake
session: 63917036-5db1-4fb5-9d55-a1edfc554596

## Opening
How do we design one TUI that keeps working as the device under it changes?
A device is four things at once: its width, how a keystroke arrives, what a finger can do, and whether the page may stay awake.
A phone breaks all four: 46 columns, an IME that types each letter twice, no hover, suspended on every app switch.
The terminal has one form, drawn for the desktop answer to all four, so this page rules what the phone's pane, composer and return path become instead.

**What the four constraints are**: Width in columns, the path a keystroke travels, what a pointer can do, and whether the page is allowed to stay awake.
A desktop answers about 87 columns, one hardware key path, hover plus click, and a tab that stays open.
A phone answers about 46 columns, an IME with two live input paths, a thumb with no hover, and a suspend on every app switch.
A form is only usable where all four of its assumptions hold, which is why the phone failures arrive together rather than one at a time.

**Where this page sits**: `QD3` owns the engine: the PTY, the 5599 proxy, keys, HOLD, reaping, the security line.
It has no design half, so the form question fell between pages until JL hit it on a phone.
This page is that half, and it stops at the form: where typing happens, what the pane shows, which gestures exist, and what the page owes a reader who leaves and returns.
The desktop pane sits here too for now, because the gap between it and the SDK drawer is a question about form rather than about the process, and whether it stays is the 🧭 row in `## States`.
`QD5` decides whether the board becomes panes at all, so anything about that container is not argued here.

**What a ruling per device buys**: The phone stops being a special case that waits for the desktop form to be patched one symptom at a time.
Each device is handed the form its own four constraints allow, so the composer, the session view, and the return path are each chosen by whichever constraint that device breaks.

**What the alternative costs**: One form everywhere means each symptom gets fixed where it shows rather than where it comes from.
The doubled keystroke was diagnosed and fixed twice on `QD3` as duplicated listeners, correctly both times, and a phone still doubles, because the third cause is a different constraint.

**How it is judged**: Someone completes and resumes a turn on the device in hand, and never has to know which form they were given.

**Covered elsewhere**: The engine is `QD3`: the PTY, the 5599 proxy, keys, HOLD, reaping, the security line. A defect in the process is that page; a defect in the form is this one. Rendering the session as chat rather than as a screen is `QD3`'s 🪄 smooth pane (route D), and it may turn out to BE the answer here, which is why this page must not decide it alone. The SDK chat box is `QD2`; the session rules are `QD1`; whether the board becomes panes at all is `QD5`.

## Diagram

**One form, two devices**: what the terminal assumes, against what each device actually offers.

```
  ONE FORM TODAY                              WHAT EACH DEVICE ACTUALLY OFFERS
  ──────────────────────────────              ─────────────────────────────────────
  the raw TTY grid, everywhere                 desktop              phone
  ┌────────────────────────────┐              ┌──────────────┐    ┌──────────────┐
  │ 87 cols x 29 rows          │              │ ~87 columns  │    │ ~46 columns  │
  │ claude's box art fits      │              │ hardware kbd │    │ IME keyboard │
  │ input via hidden textarea  │              │ hover + mouse│    │ thumb, no    │
  │ hover pre-warms the assets │              │ stays open   │    │ hover at all │
  └────────────────────────────┘              └──────────────┘    │ SUSPENDED on │
             │                                        ▲           │ every switch │
             ├── drawn for this ──────────────────────┘           └──────────────┘
             └── and handed unchanged to this ────────────────────────────▲
```

**Four failures, two causes**: which assumption each symptom breaks, and where the cause sits.

```
  A · the form assumes a big screen and a pointer
      · one keypress types two   ← the phone keyboard delivers the character on
                                    the composition path AND the keydown path;
                                    xterm listens to both, the PTY gets it twice
      · the frames shred         ← 80-column box art repainted into ~46 columns
      · the keyboard will not open ← focus() runs after the async start returns,
                                    which iOS need not accept as the user's tap

  B · the form assumes the page never goes away
      · switch away and back →   the page has three EXIT handlers; the chat half
        the terminal is frozen   now rejoins on visibilitychange and focus, but
                                 nothing reattaches the terminal socket. see States.
```

## Content
### 1 · A device is four constraints, and the terminal was drawn for one set of them
**The four properties**: what decides whether a form is usable on a device, with each device's answer.

```
📱 vs 🖥  the four properties that decide a form
   ┌──────────────┬──────────────────┬──────────────────┐
   │              │ 🖥 desktop        │ 📱 phone          │
   ├──────────────┼──────────────────┼──────────────────┤
   │ 📏 width      │ ~87 columns      │ ~46 columns      │
   │ ⌨️ keyboard    │ hardware, 1 path │ IME, 2 paths     │
   │ 🖱 pointer    │ hover + click    │ thumb, no hover  │
   │ ⏳ lifetime   │ stays open       │ suspended often  │
   └──────────────┴──────────────────┴──────────────────┘
   the terminal assumes the LEFT column in all four, everywhere
```
This page works from one model: a device is not a screen size, it is four constraints at once, and a form is only usable where all four hold.
The terminal has exactly one form, the raw TTY grid, and that form assumes the desktop value of every one of the four.
That is why the phone failures arrive together rather than one at a time, and why fixing them one at a time has not worked: each symptom is a different constraint being violated by the same assumption.
The four properties are also the checklist for any proposed form, which is what `## Aims` is ordered by.

### 2 · Where typing happens, and why a phone types every letter twice
**Two paths, one character**: how the same keypress reaches the PTY twice on a phone.

```
⌨️ ONE keypress, TWO paths into the PTY
   👆 press "a"
      ├─① keydown ─────────▶ xterm evaluateKeyboardEvent ──▶ "a"
      └─② input/composition ▶ xterm textarea handler ──────▶ "a"
   🖥 desktop: ① only          ➜ "a"
   📱 phone:   ① and ② both    ➜ "aa"   ❌
   ✅ the fix: a composer that writes to the PTY, bypassing xterm's input entirely
```
Typing rides xterm's hidden textarea, and on a phone that textarea has two live paths because the composition and `input` events are what IME, autocorrect and predictive text all require, while many devices additionally fire a `keydown` for the same character.
Board history shows why this must be stated as a rule rather than patched again: this exact symptom was diagnosed and fixed twice on `QD3`, both times as duplicated `onData` listeners after a reconnect, and that fix is present and correct today.
A phone reporting the same symptom is therefore a third cause, and the lesson is that the symptom is not diagnostic; the input PATH is.
The distinguishing test is cheap and still unrun: doubling from the very first keystroke with no `[connection lost…]` banner ever shown points at the composition path, while doubling that begins only after a reconnect banner points back at the listener cause.
The rule this page establishes: on a device with an IME, the composer writes to the PTY directly and the terminal widget never owns the keystroke.

### 3 · Below some width, the grid stops being a rendering choice
**The same repaint at two widths**: why a correct repaint can still be unreadable.

```
📏 the same repaint, two widths
   🖥 87 cols  ┌─ Claude's box art ─────────────┐   ✅ reads
   📱 46 cols  ┌─ Claude's box a…│rt ───────┐    ❌ wraps into itself
   ⚠️ a CORRECT repaint at the true width is still unreadable
```
`QD3` closed a shredded-screen round on 260801 by nudging the width on attach so the app repaints at the size the browser really has, and that was the right fix for a desktop, where the true width still fits the art.
A phone does not clear that bar: about 390 CSS pixels at 13px metrics is roughly 46 columns, and Claude's frames are drawn for far more, so a correct repaint at the true width is still an unreadable one.
This is the boundary the page names: above it, polishing the grid pays; below it, the grid itself is the defect and only a reflowing rendering fits.
It is also why the smooth pane stops being an alternative rendering and becomes the only one available.

### 4 · A page that can be suspended owes the reader an entry handler
**Leaving against returning**: how many handlers the board registers for each direction.

```
🚪 the board handles LEAVING three times and RETURNING for the chat only
   pagehide ──▶ 80-restore.js   save the view
            ──▶ 50-activity.js  end the activity span
            ──▶ 30-terminal.js  park:true, drop the WebSocket
   pageshow ──▶ 20-live-refresh.js   poll speed only, not the socket or the turn
   visibilitychange / focus ──▶ 20-chat/10-sessions.js   rejoin a live turn
   📱 result: dead terminal pane in front of a live process · a hung send still
              holds the chat busy for up to 7 min
```
A desktop tab mostly stays open, so the board could get away with tearing down on the way out and never rebuilding on the way back; a phone suspends on every app switch, which turns that omission into the most visible failure of all.
The terminal half parks correctly, which keeps the process alive, but nothing reattaches the socket, so the reader returns to a dead pane in front of a living process and it never self-heals.
The chat half stalls instead of dying: a suspended streaming `fetch` can hang without resolving or rejecting, so the `await` never returns, the `catch` never runs, and the cleanup that clears `inflight` never runs either.
It does recover, after `QUIET_GIVEUP`, 420000 on a real send, seven minutes; the watchdog meant to rescue it is a `setInterval`, which is exactly what a backgrounded page throttles.
The chat half has since grown a return path: `10-sessions.js` calls `chatRejoin()` on `visibilitychange` and `focus`, attaching to a live turn through `/_board/attach` and falling back to a transcript sync, so a finished turn is recovered rather than lost; the rejoin refuses to run while `inflight` is set, so the hung send above still waits out the watchdog, and the terminal socket has no entry handler at all.
The rule: every teardown registered on the way out owes a matching rebuild on the way back, and a timer is not a rebuild.

### 5 · Every desktop gesture needs a touch twin, or an explicit desktop-only ruling
**The gesture audit**: each capability, the gesture that reaches it on each device, and its answer.

```
👆 gesture audit
   paste an image   🖥 clipboard event   📱 none  ──▶ 🖼 file input   ✅ SHIPPED 260801
   pre-warm assets  🖥 hover             📱 none  ──▶ open
   pick a session   🖥 tab + click       📱 works ──▶ 🗂 Sessions tab, already there
   type            🖥 hardware kbd      📱 IME   ──▶ division 2
```
A capability can be fully built on the server and still be unreachable, because reachability is a property of the gesture and not of the feature.
Images proved it: `/_board/image` was already device-agnostic and both entry points were `paste` listeners, so a phone could not put an image on the board at all, and the whole gap was one missing button.
That one is now closed, and the shape of the fix is the general one: the browser re-encodes before posting, because `live/write.py` caps at 8MB and rejects HEIC, so the gesture must respect the endpoint's constraints rather than the endpoint loosening for the device.
The audit also corrected an assumption: the session picker was believed hidden in terminal view and is not, which is recorded in `## States` because being wrong in that direction is worth keeping.

### 6 · The pane renders a screen; the drawer beside it renders a document
**The same reply in two panes**: what each surface can show, and which defects survive any amount of CSS.

```
🪟 the SAME answer, two surfaces
   🖥 SDK drawer   markdown ▶ headings · bullets · bold · clickable links
                   one bubble per turn, reflows to any width
   ⌨ terminal      a grid of cells the CLI repaints
                   a heading is bold-ish text · a URL is bare characters
   ────────────────────────────────────────────────────────────────────
   🎨 cheap        one surface · page list reclaimed · notice inside the pane
   🌏 elsewhere    CJK clipped at the right edge      ──▶ QD3's wcwidth
   🧱 structural   a URL that is not a link           ──▶ document renderer
```
On 260801 JL put the desktop terminal pane beside the SDK drawer and called it the worse of the two, and reading it off the screenshot against the CSS turned one impression into five separate defects.
The session rail takes a full-height white column for one id chip and a ＋, and the black terminal starts beside it, so the pane reads as an L-shaped gutter instead of a surface.
Three unconnected colour zones stack up: a white header, a black body, and a white footer carrying the Quick actions and Settings pills, with no shared frame, radius or padding tying them together.
CJK runs off the right edge instead of wrapping, clipping a word in half, which is the wcwidth defect `QD3` already names: xterm's Unicode 6 tables call a CJK cell one column while the PTY counts two.
The reload notice is positioned against the VIEWPORT, since `#ctoast` is `position:fixed` at `left:50%`, so inside a narrower pane it lands half outside the left edge and cannot be read.
The status strip's URL wraps as bare characters across two lines, because a TTY has no links.
The comparison itself is the finding: the two panes are not rendering the same KIND of thing, so no amount of CSS closes the gap, which is exactly what the archived `QD3m` argued and what `QD3`'s 🪄 smooth-pane items own.
The work therefore splits cleanly: the layout defects are cheap and true whatever else happens, the CJK one belongs to `QD3`'s wcwidth item, and the URL closes only when the pane renders a document rather than a screen.

## Aims

### A1 · 📐 A device is four constraints, and the terminal was drawn for one set of them
- A1.1 · The phone has a ruled form, chosen against its own four constraints rather than patched symptom by symptom.
  **Done when:** JL has ticked one option on the 📐 Decision Now row, and that choice is written into Content 1 as the form this page hands a phone.

### A2 · ⌨️ Where typing happens, and why a phone types every letter twice
- A2.1 · Typing on a phone stops riding xterm's hidden textarea.
  **Done when:** the composer writes to the PTY directly, and one keypress on a phone produces exactly one character with no reconnect banner involved.
  **Plan:** run the distinguishing test first, since a first-keystroke double with no banner confirms the composition path before anything is built.

### A3 · 📏 Below some width, the grid stops being a rendering choice
- A3.1 · The page names what 80-column art does on a 46-column screen.
  **Done when:** Content 3 carries the width below which the raw grid is abandoned rather than shrunk, and names the rendering that replaces it.

### A4 · 🚪 A page that can be suspended owes the reader an entry handler
- A4.1 · Returning to the board rebuilds what leaving tore down.
  **Done when:** a `pageshow` handler reattaches the parked terminal's socket and settles a chat turn whose stream died while suspended, without waiting out `QUIET_GIVEUP`.

### A5 · 👆 Every desktop gesture needs a touch twin, or an explicit desktop-only ruling
- A5.1 · Every gesture the board offers is reachable on a phone, or is recorded as desktop-only on purpose.
  **Done when:** the audit in Content 5 has a row per gesture and no row reads "none" without a decision beside it.
- A5.2 · An image can be put on the board from a phone.
  **Done when:** a photo picked on a real phone lands in `fig/` and its path reaches whichever view is showing.
- A5.3 · A session can be picked while the terminal is showing.
  **Done when:** the picker is reachable from the terminal view without a second chooser being added.

### A6 · 🪟 The pane renders a screen; the drawer beside it renders a document
- A6.1 · The pane reads as ONE surface rather than three colour zones.
  **Done when:** header, body and footer share a frame, a radius and a padding.
- A6.2 · The pane's content is the full width of the pane.
  **Done when:** the session rail no longer holds a full-height column for one chip, and the surface is not L-shaped.
- A6.3 · A notice inside the pane is positioned to the PANE, not to the window.
  **Done when:** `#ctoast` and every other in-pane affordance are positioned against their pane's box rather than the viewport.
- A6.4 · The terminal pane is not visibly the worse of the two panes.
  **Done when:** one identical answer is rendered in both panes and compared side by side, and JL does not call the terminal pane the worse one.

### P · Page-level
- P1 · This page's ownership boundary with `QD3` is settled.
  **Done when:** the 🧭 Decision Now row is ticked and the losing side is written into the Opening's `Covered elsewhere`.
- P2 · JL completes and resumes a turn on the device in hand without knowing which form he was given.
  **Done when:** JL types a full turn on his own phone with no doubled character, no shredded frame and no chasing the keyboard, and switches away and back mid-turn without the drawer freezing.

## States

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🗣 What is the phone's form?
      📍 `Part` 1, the four-constraint model every other part is read against
      🔔 `Why now` the terminal is unusable on JL's phone today, and every item below reads differently depending on the answer
      `A ·` composer plus a read-only pane: the TUI stays a screen but stops taking keystrokes on a phone, and a plain native input under it writes whole lines to the PTY. Smallest change, keeps one engine, and the pane is still 46 columns of art nobody can read.
      ⭐ `B ·` the phone gets the smooth pane, which is `QD3`'s route D and already the plan of record there: the session renders as chat, reflows to any width by construction, and the raw grid stays one toggle away for the moments only it can serve, such as permission dialogs and pickers. CC recommends B with A shipped first as the stopgap, because A is a few hours and unblocks the phone this week while B is the form that actually fits the device.
      `C ·` keep the raw grid everywhere and fix only the input. Cheapest, and it leaves the width problem standing, so the terminal stays readable only on a tablet and up.
      🛑 `Blocks` A1.1 and A3.1, and everything under A6 that assumes the pane keeps rendering a screen
      🤖 `If nobody answers` A ships as the stopgap and B stays on `QD3`'s roadmap

- [ ] 🗣 How far do we close the gap with the SDK drawer, on the DESKTOP?
      📍 `Part` 6, the two-surfaces comparison JL asked for
      🔔 `Why now` JL called the pane the worse of the two on 260801, and the cheap half and the structural half have different owners
      ⭐ `A ·` fix the layout defects only: one surface, the page list reclaimed, notices positioned to the pane. Cheap, lands this week, and the pane still shows a screen, so headings stay bold-ish text and URLs stay characters. CC recommends A now and B next, because A is cheap and true under every future.
      `B ·` fix the layout AND render the session as a document, the archived `QD3m` route owned as `QD3`'s 🪄 smooth pane: tail the session's jsonl and draw markdown bubbles, keeping the PTY as the engine and the raw TTY one toggle away. The only version that can actually match the drawer, and the larger build.
      `C ·` drop the terminal pane on the desktop and let the SDK drawer be the one chat surface, keeping the TUI for the phone or for a real CLI window.
      🛑 `Blocks` A6.1 through A6.4
      🤖 `If nobody answers` A is built, since every option contains it

- [ ] 🗣 Does this page own the desktop form too, or only the phone?
      📍 `Part` 6, which is desktop material sitting on a page whose Opening leads with the phone
      🔔 `Why now` Content 6 and the 🎨 row above are both desktop, so the page is already acting as if the answer is A
      ⭐ `A ·` this page owns the terminal's form on every device, and `QD3` keeps strictly to the engine. CC recommends A, because `QD3`'s smoothness items are already half form and half engine, and splitting on that seam is what let the phone fall through both pages until JL hit it.
      `B ·` this page is the phone question alone, and desktop polish stays in `QD3`'s 🚧 smoothness items.
      🛑 `Blocks` P1, and the home of Content 6
      🤖 `If nobody answers` the page keeps behaving as A and the Opening stays as written

### A1 · 📐 A device is four constraints, and the terminal was drawn for one set of them
- 🧠 A1.1 · Waiting on JL. The model and the four constraints are written, the options are costed, and nothing under them should be built until the 📐 row is ticked.

### A2 · ⌨️ Where typing happens, and why a phone types every letter twice
- ⬜ A2.1 · Not started. The diagnosis stands on a code read: there is no mobile, touch or composition handling anywhere in the terminal client or in `live/term.py`, so the phone path was never in scope rather than having been handled and broken. Not confirmed on a device, and the distinguishing test in Content 2 has not been run.

### A3 · 📏 Below some width, the grid stops being a rendering choice
- 🧠 A3.1 · Waiting on the 📐 ruling. The measurement is in: about 390 CSS pixels at 13px metrics is roughly 46 columns, which is below the width Claude's own frames are drawn for.

### A4 · 🚪 A page that can be suspended owes the reader an entry handler
- 🔨 A4.1 · Half built, on the chat side: `10-sessions.js` now calls `chatRejoin()` on `visibilitychange` and `focus`, attaching to a live turn through `/_board/attach` with a quiet giveup (`QUIET_GIVEUP = attach ? 6000 : 420000`) and falling back to a transcript sync; it refuses while `inflight` is set, so a send whose suspended stream hung still waits out the seven minutes. The terminal half is untouched: `pagehide` still parks in `30-terminal.js`, nothing reattaches the socket, and the one `pageshow` under `assets/js/` is `20-live-refresh.js`, which only snaps the refresh poll back to fast. Read from source; not yet confirmed on a device.

### A5 · 👆 Every desktop gesture needs a touch twin, or an explicit desktop-only ruling
- 🔨 A5.1 · Images and the session picker are both surveyed and closed below. Hover pre-warming of the assets is still open and has no touch answer and no desktop-only ruling.
- ✅ A5.2 · Built 260801: `assets/js/10-drawer/35-imagepick.js` plus one button in the drawer header; the server was already device-agnostic and was not touched. The button sits in the HEADER because that is the one strip `termView()` leaves alone, so it is reachable from the TUI, and it routes by view, writing a bare repo-root-relative path into the PTY when the terminal is showing and `![image](path)` into the composer when the chat is. It re-encodes through a canvas before posting, since `live/write.py` caps at 8MB and rejects the HEIC an iPhone shoots, and it passes a small PNG through untouched because re-encoding a screenshot to JPEG blurs the text it was taken to show. Verified in JL's own Chrome over CDP on both branches: a 4000x3000 JPEG went in at 188KB and landed in `fig/` at 12KB, the terminal branch put the path on the CLI prompt line, and the chat branch inserted the full repo-root-relative markdown; test files were removed afterwards. Confirmation on a real phone is P2, not this row.
- ✅ A5.3 · Nothing to build. The drawer has THREE tabs, `🗂 Sessions · ✨ Quick actions · ⚙ Settings`, and the picker is `.spick` / `.spl` inside the 🗂 Sessions tab, not `.sid` inside ⚙ Settings; `.sid` is only a session-id readout. `termView()` hides `.sfocus .bd .acts .cfg .sid .ft .tip` and does NOT hide `.sessions` or `.spick`, so the picker is reachable while the terminal is showing. Verified in JL's own Chrome over CDP: the tab strip reads exactly those three labels, clicking 🗂 leaves `.utility` at `open show-sessions`, `.sessions` computes to `display:block`, and the list rendered two session rows.

### A6 · 🪟 The pane renders a screen; the drawer beside it renders a document
- 🧠 A6.1 · Not started, and it waits on the 🎨 row only for sequencing: one surface is true under options A and B alike.
- 🧠 A6.2 · Not started. The page list is a full-height white column for one id chip and a ＋, so the surface is L-shaped; same sequencing as A6.1.
- ⬜ A6.3 · Not started. `#ctoast` is `position:fixed` at `left:50%`, and every other in-pane affordance has the same bug latent.
- 🧠 A6.4 · Waiting on the 🎨 row. This is the acceptance test for A6.1 through A6.3 and it is JL's own standard from 260801: render one identical answer in both panes and compare them side by side.

### P · Page-level
- 🧠 P1 · Waiting on the 🧭 row. Content 6 is desktop material on a phone-led page, so the page is already acting as if the answer is A.
- 🧠 P2 · Waiting on JL and on a real phone. CC cannot close this row: there is no phone here, and every earlier round of the doubling bug was called fixed on a desktop and was not.

## Files

### ⚙️ Engines
- `assets/js/10-drawer/30-terminal.js`
  The whole terminal front end: xterm construction, `fitTerm`, the WS protocol, input binding, paste, the ⌨ toggle, and the `pagehide` park beacon. Every option in the 📐 ruling lands here, and so does A2.1.
- `assets/js/10-drawer/20-chat/50-prefs-paste.js`
  The chat send loop: the streaming reader, `inflight`, `chatBusy`, and the `watchdog` whose `QUIET_GIVEUP` is the seven-minute stall in A4.1.
- `assets/js/80-restore.js`
  Already records which half the drawer was showing and restores it on load, which makes it the natural home for the entry handler A4.1 asks for.
- `assets/js/10-drawer/35-imagepick.js`
  The 🖼 button and its canvas re-encode; the worked example of a gesture given a touch twin, and the pattern A5.1 follows for whatever it closes next.
- `assets/js/10-drawer/20-chat/10-sessions.js`
  The session picker `.spick` / `.spl` that A5.3 found already reachable; open it before adding any second chooser. It also holds the chat's return path now: `syncNow()` rejoins a live turn on `visibilitychange` and `focus`, which is the built half of A4.1.
- `live/term.py`
  `spawn_pty`, the `/_term/<key>/ws` terminus, and `park`. A composer that writes whole lines still arrives through this socket.
- `live/write.py`
  The 8MB cap and the png/jpeg/gif/webp allowlist that any image gesture has to respect rather than ask to be loosened.

## Lesson
- 🔁 A SYMPTOM IS NOT DIAGNOSTIC; THE INPUT PATH IS. The doubled keystroke was diagnosed and fixed twice on `QD3` as duplicated `onData` listeners after a reconnect, correctly both times, and a phone still doubles because the third cause is a different constraint. Fixing what the symptom looks like rather than which path delivered it is what made the same bug arrive three times.
- 🔍 A CLAIM READ OUT OF SOURCE IS A HYPOTHESIS. CC read `.sid` in `termView()`'s hide list, concluded that `.sid` was the session picker and that the terminal hid it, and both halves were false. The file had also changed under CC mid-session, which is the second time this board has been bitten by another session editing the same files. Driving JL's own Chrome over CDP settled it in minutes and re-reading never would have.
- 🚪 REACHABILITY IS A PROPERTY OF THE GESTURE, NOT OF THE FEATURE. `/_board/image` was device-agnostic the whole time and a phone still could not put an image on the board, because both entry points were `paste` listeners. A survey of `assets/js/` found no file input, no `capture` attribute and no drop handler, so the whole gap was one missing button.
- ⏱ EVERY TEARDOWN OWES A REBUILD, AND A TIMER IS NOT A REBUILD. The board registered `pagehide` three times and `pageshow` not once when this was read, and the watchdog meant to rescue the resulting stall is a `setInterval`, which is exactly what a backgrounded page throttles. The rescue is suspended by the same event that caused the failure.

## Log
- 260806 2143 · [REVISE-CC] swept to the 260806 architecture; the A4 exit-only story was stale: `20-live-refresh.js` now registers a `pageshow` (poll speed only) and `10-sessions.js` rejoins a live turn on `visibilitychange`/`focus` through `/_board/attach`, so the Diagram, Content 4, A4.1 (⬜→🔨) and the ⏱ Lesson now say only the terminal socket lacks an entry handler; drawer tab order in A5.3 corrected to `🗂 Sessions · ✨ Quick actions · ⚙ Settings` per `20-chat/00-open.js`
260802 · Brought to the page contract: `## Aims` became six A-groups plus P, keyed by id and name to the six Content divisions, with a testable `Done when` on every row; `## States` became one State row per Aim with `### Decision Now` first; the seven dated narrative entries that were doing States' job moved down here and into `## Lesson`, since their substance is now in Content. Added Content 6 for the desktop pane against the SDK drawer, which was the one cluster of Aims and one Decision Now row with no division to sit under. Captions added above all eight figures, the Diagram split into its two real figures, `## Items to Finish` and `## Where we are` renamed where the prose still cited them, JL's quotes translated on the English-only board, and `## Files` grouped under ⚙️ Engines with the three files the page names but never listed
260802 0117 · Opening rebuilt to QB4 §1. The old version put the whole rationale BELOW the first blank line, so the stage showed one bare question and the four sentences that explained it were hidden in `More details` (QB4 §1.1.2 names this exact failure by example). The visible paragraph is now 4 sentences, about 455 characters, and follows the required shape: the question, what its own words mean with a real value for each, why that is hard, what this page decides. `More details` was one prose block and is now five bold-labelled parts per QB4 §1.3.1, including the bearing on `QD3` and `QD5` that QB4 §1.2.2 requires and the Opening did not have
260801 · JL compared the desktop terminal pane with the SDK drawer and called it the uglier of the two, asking directly for the comparison. Five defects recorded and now held in Content 6: the L-shaped session rail, three unjoined colour zones, CJK clipped at the right edge, a viewport-positioned notice landing outside the pane, and a URL wrapping as bare characters. Split into the cheap layout items, `QD3`'s wcwidth item, and the structural one: the drawer renders a document and the terminal renders a screen, which is the 🎨 Decision Now row
260801 · JL, on the Opening: "I want the opening to say how we design this TUI so that it works on the configuration in front of it." Right, and the rewrite was measured against QB4 line 28 rather than taste. The old lead asked what the terminal should BECOME and then listed breakage, so it named the problem and never the design, which fails "name what this page GIVES the reader". It now leads on how one TUI is designed to survive a changing device, states the four-part contract as the ONE central idea, and ends on the crisp test. `method:` was carrying only three of the four constraints and now matches the Opening and Content
260801 · JL: "why does this page have no content?" Correct, and it was a real defect: the page had no `## Content` at all, so every piece of substance was sitting in dated State bullets, which makes a LOG rather than a design page (QB4: "Substance found in Opening moves to Content"). Added five Content divisions, each opening with a face figure per QB4: the four-constraint device model, where typing happens, the width below which the grid itself is the defect, what a suspendable page owes on return, and the gesture audit
260801 · JL, switching away and back: "why does the whole chat pane feel frozen after I shift away and come back?" Read from source: `pagehide` is registered in `80-restore.js`, `50-activity.js` and `10-drawer/30-terminal.js`, and `pageshow` in no file at all, so every switch-away tears things down and nothing rebuilds them. The terminal side parks correctly and keeps the PTY alive, but nothing reattaches the WebSocket; the chat side stalls instead of dying, because a suspended streaming `fetch` can hang without resolving or rejecting, so the cleanup that clears `inflight` never runs and the send button stays a stop button until `QUIET_GIVEUP` gives up at seven minutes. Now A4.1
260801 · 🖼 BUILT and verified in Chrome on both branches: `35-imagepick.js` plus a header button; the terminal branch writes the path to the PTY, the chat branch inserts markdown, and the canvas re-encode respects the 8MB cap and HEIC. Phone confirmation still owed under P2
260801 · CC's reading of the session picker was wrong in both halves and the correction is kept as a Lesson: `.sid` is a session-id readout, the picker is `.spick` / `.spl` in a 🗂 Sessions tab that had already shipped, and `termView()` hides neither `.sessions` nor `.spick`. Caught by driving JL's own Chrome over CDP rather than by re-reading the file, which had also changed under CC mid-session. The item became A5.3, closed with nothing to build
260801 · JL asked for a session button in the Quick actions strip. The first answer, that it existed one tab over under ⚙ Settings and was hidden by `termView()`, was recorded and then found to be wrong the same day; it was also noted that adding a second chooser would re-break JL's own "one chooser, not two" ruling that removed the tab strip
260801 · JL asked how to upload an image from a phone; the answer is that there is no way. Both entry points are `paste` listeners and `assets/js/` has no file input, `capture`, or drop handler, while `/_board/image` is already device-agnostic. Recorded with the two `live/write.py` constraints the gesture must respect, the 8MB cap and the absence of HEIC
260801 · JL, on a phone: "I type one letter and two come out." `QD3` records this symptom twice already, both times traced to `connectWS()` binding a fresh `termT.onData(...)` on every reconnect without dropping the old one, and that fix is present and correct today. So a phone reporting it is a THIRD cause: the hidden textarea has two live paths on a device with an IME. Supporting it, there is no mobile, touch or composition handling anywhere in the terminal client or in `live/term.py`
260801 · CC recorded that the narrow width is the shredded screen one device further on: `QD3`'s width nudge on attach was right for a desktop, where the true width still fits the art, and a phone at roughly 46 columns does not clear that bar, so a correct repaint is still an unreadable one
260801 · Opened from JL after the terminal proved hard to use on a phone: `QD3` owns the engine and has no design half, so the form question gets its own page. Carries the third-cause diagnosis for the doubled keystroke, the width argument that a correct repaint is still unreadable at ~46 columns, the exit-handler-without-entry-handler diagnosis for the freeze on returning, and the phone-form ruling for JL
