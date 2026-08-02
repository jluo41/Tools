# Design the terminal for the device holding it

state: 🟡 PARTIAL
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
`QD5` decides whether the board becomes panes at all, so anything about that container is not argued here.

**What a ruling per device buys**: The phone stops being a special case that waits for the desktop form to be patched one symptom at a time.
Each device is handed the form its own four constraints allow, so the composer, the session view, and the return path are each chosen by whichever constraint that device breaks.

**What the alternative costs**: One form everywhere means each symptom gets fixed where it shows rather than where it comes from.
The doubled keystroke was diagnosed and fixed twice on `QD3` as duplicated listeners, correctly both times, and a phone still doubles, because the third cause is a different constraint.

**How it is judged**: Someone completes and resumes a turn on the device in hand, and never has to know which form they were given.

**Covered elsewhere**: The engine is `QD3`: the PTY, the 5599 proxy, keys, HOLD, reaping, the security line. A defect in the process is that page; a defect in the form is this one. Rendering the session as chat rather than as a screen is `QD3`'s 🪄 smooth pane (route D), and it may turn out to BE the answer here, which is why this page must not decide it alone. The SDK chat box is `QD2`; the session rules are `QD1`; whether the board becomes panes at all is `QD5`.

## Diagram

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

  FOUR FAILURES, TWO CAUSES
  ─────────────────────────────────────────────────────────────────────────────
  A · the form assumes a big screen and a pointer
      · one keypress types two   ← the phone keyboard delivers the character on
                                    the composition path AND the keydown path;
                                    xterm listens to both, the PTY gets it twice
      · the frames shred         ← 80-column box art repainted into ~46 columns
      · the keyboard will not open ← focus() runs after the async start returns,
                                    which iOS need not accept as the user's tap

  B · the form assumes the page never goes away
      · switch away and back →   the page has EXIT handlers and no ENTRY handler.
        everything is frozen     `pagehide` is registered in three files;
                                 `pageshow` in none. see Where we are.
```

## Content
### 1 · A device is four constraints, and the terminal was drawn for one set of them
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
The four properties are also the checklist for any proposed form, which is what `## Items to Finish` is ordered by.

### 2 · Where typing happens, and why a phone types every letter twice
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
The rule this page establishes: on a device with an IME, the composer writes to the PTY directly and the terminal widget never owns the keystroke.

### 3 · Below some width, the grid stops being a rendering choice
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
```
🚪 the board handles LEAVING three times and RETURNING zero times
   pagehide ──▶ 80-restore.js   save the view
            ──▶ 50-activity.js  end the activity span
            ──▶ 30-terminal.js  park:true, drop the WebSocket
   pageshow ──▶ (nothing anywhere in assets/js/)
   📱 result: dead pane in front of a live process · chat busy for up to 7 min
```
A desktop tab mostly stays open, so the board could get away with tearing down on the way out and never rebuilding on the way back; a phone suspends on every app switch, which turns that omission into the most visible failure of all.
The terminal half parks correctly, which keeps the process alive, but nothing reattaches the socket, so the reader returns to a dead pane in front of a living process and it never self-heals.
The chat half stalls instead of dying: a suspended streaming `fetch` can hang without resolving or rejecting, so the `await` never returns, the `catch` never runs, and the cleanup that clears `inflight` never runs either.
It does recover, after `QUIET_GIVEUP = 420000`, seven minutes, and the turn is lost; the watchdog meant to rescue it is a `setInterval`, which is exactly what a backgrounded page throttles.
The rule: every teardown registered on the way out owes a matching rebuild on the way back, and a timer is not a rebuild.

### 5 · Every desktop gesture needs a touch twin, or an explicit desktop-only ruling
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
The audit also corrected an assumption: the session picker was believed hidden in terminal view and is not, which is recorded in `## Where we are` because being wrong in that direction is worth keeping.

## Aims
- [ ] 🧹 The pane becomes ONE surface instead of three colour zones
      White header, black body, white footer with the Quick actions and Settings pills, none of them sharing a frame, radius or padding.
      Cheap, true under every option in the ruling below, and the single biggest reason the pane reads as unfinished beside the drawer.
- [ ] 📐 The session rail stops taking a full-height column for one chip
      A whole white gutter is spent on an id and a ＋, and the terminal starts beside it, so the surface is L-shaped.
      Closes when the picker is a header control or a collapsed strip and the pane's content is the full width of the pane.
- [ ] 📍 A notice inside the pane is positioned to the PANE, not the window
      `#ctoast` is `position:fixed` at `left:50%`, so the reload notice lands half outside a narrower pane's left edge.
      Every in-pane affordance has this bug latent, not only this toast.
- [ ] 🪄 Judge the pane against the SDK drawer on the SAME reply
      Acceptance for all of the above: render one identical answer in both panes and compare them side by side.
      It closes as ✅ only when the terminal pane is not visibly the worse of the two, which is the standard JL applied on 260801.
- [ ] 📐 Rule what the phone's form actually is
      The whole page turns on this, and it is JL's call, so it sits in Decision Now below.
      Every item under it reads differently depending on the answer, which is why nothing else here should be built first.
- [ ] 🔄 Give the page an entry handler, not just exit handlers
      Cause B above, and the one item that is true under every option in the ruling and helps the desktop too.
      On return the page must re-establish what leaving tore down: reattach the terminal it parked, and settle a chat turn whose stream died while suspended, rather than waiting out a seven-minute watchdog.
- [ ] ⌨ Typing on a phone stops riding xterm's hidden textarea
      Also true under every option, because the doubling comes from that textarea having two live input paths on a phone.
      Whatever the pane becomes, the composer writes to the PTY directly rather than through the terminal widget's own input handling.
- [ ] 📏 Decide what 80-column art does on a 46-column screen
      Shrinking the font buys columns and costs legibility, and at some width claude's own frames stop being drawable at all.
      This is where the smooth pane stops being an alternative rendering and starts being the only one that fits.
- [ ] 👆 Every gesture has a touch equivalent
      Hover pre-warms the assets, the ⌨ toggle and the session picker are pointer targets, and paste is a desktop clipboard event.
      A phone has none of those, so each needs its own answer or an explicit decision that it is desktop-only.
      The first one surveyed is images, and it turned out to be missing outright rather than merely awkward; it has its own item below.
- [x] 🖼 Images have a phone gesture: a 🖼 button in the drawer header (BUILT 260801)
      `assets/js/10-drawer/35-imagepick.js` plus one button in the header; the server was already device-agnostic and was not touched.
      It sits in the HEADER because that is the one strip `termView()` leaves alone, so it is reachable from the TUI, which is where a phone reader wants to hand Claude a screenshot; it then routes by view, writing a bare repo-root-relative path into the PTY when the terminal is showing and `![image](path)` into the composer when the chat is.
      It re-encodes through a canvas before posting, since `live/write.py` caps at 8MB and rejects the HEIC an iPhone shoots, and passes a small PNG through untouched because re-encoding a screenshot to JPEG blurs the text it was taken to show.
      Verified in JL's own Chrome over CDP on both branches: a 4000x3000 JPEG went in at 188KB and landed in `fig/` at 12KB, the terminal branch put the path on the CLI prompt line, and the chat branch inserted the full repo-root-relative markdown. Test files removed afterwards.
      Still owed: JL confirming it on a real phone, where the photo library and camera actually appear. That is part of the 🧪 item.
- [x] 🎛 Nothing to build: the session picker is already a tab and already survives the terminal
      Corrected on 260801 after driving the real page; the first version of this item was wrong and is kept below as the Where we are entry that recorded it.
      The drawer has THREE tabs, `✨ Quick actions · 🗂 Sessions · ⚙ Settings`, and the picker is `.spick` / `.spl` inside the 🗂 Sessions tab, not `.sid` inside ⚙ Settings; `.sid` is only a session-id readout.
      `termView()` hides `.sfocus .bd .acts .cfg .sid .ft .tip` and does NOT hide `.sessions` or `.spick`, so the picker is reachable while the terminal is showing.
      Verified in JL's own Chrome over CDP: the tab strip reads exactly those three labels, clicking 🗂 leaves `.utility` at `open show-sessions`, `.sessions` computes to `display:block`, and the list rendered two session rows.
- [ ] 🧪 Verified by JL on a real phone
      Acceptance is JL typing a full turn on his own phone without a doubled character, without a shredded frame, without chasing the keyboard, and switching away and back mid-turn without the drawer freezing.
      CC cannot close this item: no phone here, and every earlier round of the doubling bug was called fixed on a desktop and was not.

## States
**Nothing built. This page was opened on 260801 from JL's report that the terminal is hard to use on a phone.**

- 260801 JL · 🎨 On the DESKTOP the pane is uglier than the SDK drawer, and the gap is structural rather than cosmetic
  JL: "你这个界面也没有合页好，非常的难看。你跟那个 SDK 的 UI 比比啊?"
  Read off the screenshot and confirmed against the CSS, so this is five separate defects rather than one impression.
  ① The session rail takes a full-height white column for one id chip and a ＋, and the black terminal starts beside it, so the pane reads as an L-shaped gutter instead of a surface.
  ② Three unconnected colour zones stack up: a white header, a black body, and a white footer carrying the Quick actions and Settings pills, with no shared frame, radius or padding tying them together.
  ③ CJK runs off the right edge instead of wrapping, clipping "读者分不" mid-word, which is the wcwidth defect `QD3` already names: xterm's Unicode 6 tables call a CJK cell one column while the PTY counts two.
  ④ The reload notice is positioned against the VIEWPORT (`#ctoast` is `position:fixed` at `left:50%`), so inside a narrower pane it lands half outside the left edge and cannot be read.
  ⑤ The status strip's URL wraps as bare characters across two lines, because a TTY has no links.
  The comparison JL asked for IS the finding: the SDK drawer renders a DOCUMENT, so markdown becomes headings, bullets, bold and clickable links, each turn in its own bubble; the terminal renders a SCREEN, a grid of cells the CLI repaints, where a heading is bold-ish text and a URL is characters.
  No amount of CSS closes that, because the two panes are not rendering the same kind of thing, which is exactly what the archived `QD3m` argued (render the session's jsonl as web chat and keep the PTY as the engine) and what `QD3`'s 🪄 smooth-pane items own.
  So the work splits cleanly: ① ② and ④ are layout defects worth fixing whatever else happens and are cheap; ③ belongs to `QD3`'s wcwidth item; ⑤ closes only when the pane renders a document rather than a screen.

- 260801 JL · ❄️ Switching away and back freezes the drawer, because the page has exit handlers and no entry handler
  JL: "为什么我一 shift away 再 back，感觉整个聊天界面就卡住了?"
  Leaving is handled three times over and returning is handled nowhere: `pagehide` is registered in `80-restore.js`, `50-activity.js` and `10-drawer/30-terminal.js`, while `pageshow` appears in no file in `assets/js/`.
  So every switch-away tears things down and nothing rebuilds them on the way back.
  On the terminal side `pagehide` beacons `park:true`, which is correct and deliberate, since it keeps the PTY alive; but the WebSocket is gone and nothing reattaches it, so the reader returns to a dead pane in front of a living process. That never self-heals.
  On the chat side the damage is a stall rather than a death: a suspended page's streaming `fetch` can hang without either resolving or rejecting, so `await rd.read()` never returns, the `catch` never runs, and the cleanup line after it that clears `inflight` and `chatBusy(false)` never runs either.
  The drawer therefore stays busy and the send button stays a stop button. It is not permanent: `watchdog` gives up at `QUIET_GIVEUP = 420000`, so it recovers after SEVEN MINUTES, and the turn is lost when it does.
  Worse, the watchdog is a `setInterval`, which is exactly what a backgrounded page throttles, so the timer meant to rescue the stall is suspended by the same event that caused it.
  Nothing here is confirmed on a device yet; it is read from the code, and the check is cheap, because a stall that clears in about seven minutes and a `pageshow` that never fires are both directly observable.

- 260801 JL · 📱 On a phone, one letter still arrives as two, and the recorded cause does not explain it
  JL: "我打一个字母，它出来两个字母."
  `QD3` records this symptom twice already, both times traced to `connectWS()` binding a fresh `termT.onData(...)` on every reconnect without dropping the old one, so each drop doubled the sends.
  That fix is present and correct in `assets/js/10-drawer/30-terminal.js` today: the previous pair is disposed before the next is bound, and the listeners send through the current socket.
  So a phone reporting the same symptom is a THIRD cause, not a regression of the second.
  The reading that fits: a phone keyboard delivers a character through the hidden textarea's composition and input events, which is the path IME, autocorrect and predictive text all require, while many devices also fire a keydown for the same character; xterm acts on both and the PTY receives it twice.
  Supporting it, there is no mobile, touch or composition handling anywhere in the terminal client or in `live/term.py`: the code was written for a desktop throughout, so the phone path was never in scope rather than having been handled and broken.
  Not confirmed on a device, and the distinguishing test is cheap: doubling from the very first keystroke with no `[connection lost…]` banner ever shown points at the composition path, while doubling that begins only after a reconnect banner points back at the listener cause.

- 260801 JL · 🎛 The session button already exists; it is hidden the moment the terminal opens
  JL: "我在最下面有 Quick Action Settings，能不能加一个 button? 就是说我可以选某一个具体的 session."
  Everything asked for is built. The picker lists this page's sessions, marks the ones with a live terminal `⌨` and labels them `terminal running` or `terminal parked`, attaches that session's terminal on click, and offers `＋ New session`, all in `10-drawer/20-chat/10-sessions.js`.
  It renders into `.sid`, which sits inside ⚙ Settings, the tab immediately beside ✨ Quick actions in the same utility strip JL is describing, so the request and the feature are one tab apart.
  The reason it reads as missing is a single line: `termView()` in `30-terminal.js` sets `display:none` on `.sfocus`, `.bd`, `.acts`, `.cfg`, `.sid`, `.ft` and `.tip` whenever the terminal is showing, so the session control vanishes precisely when the reader is in the terminal and most likely to want another session.
  Adding a button to Quick actions would answer the symptom and re-break the 260801 ruling that there be `one chooser, not two`, which is what removed the tab strip.

- 260801 CC · ❌ The paragraph above is wrong in its details, and the correction is the lesson
  CC read `30-terminal.js` early in the session, saw `.sid` in `termView()`'s hide list, and concluded that `.sid` was the picker and that the terminal hid it. Both halves were false.
  The picker is `.spick` / `.spl` and it lives in a 🗂 Sessions TAB that JL had already asked for and that already shipped; `.sid` is only a session-id readout in ⚙ Settings; and `termView()` hides neither `.sessions` nor `.spick`, so the picker was reachable from the terminal the whole time.
  The file had also changed under CC mid-session, since the `.tstrip` tab strip that the early read contained is gone from the current source, which is the second time this board has been bitten by another session editing the same files.
  Caught by driving JL's own Chrome over CDP instead of re-reading: the tab strip reads `✨ Quick actions · 🗂 Sessions · ⚙ Settings`, clicking 🗂 leaves `.utility` at `open show-sessions`, `.sessions` computes to `display:block`, and two session rows rendered.
  The lesson is the board's own standing one, arrived at from a new direction: a claim read out of source is a hypothesis, and this page had already recorded three of those in one day.

- 260801 JL · 🖼 Images cannot be uploaded from a phone, because both entry points are paste events
  JL: "然后我们手机上的话，如何 upload 这个 image 呢?"
  The answer is that there is no way, and the reason is a clean example of the shape this whole page is about: the capability exists, the server supports it, and only the GESTURE assumes a desktop.
  An image can enter the board through exactly two listeners, both `paste`: the terminal pane in `30-terminal.js` and the comment box in `10-comment/40-paste.js`. A survey of `assets/js/` finds no file input, no `capture` attribute, and no drop handler.
  Pasting an image into a pane is a desktop gesture; a phone offers a photo library and a camera, and both require a file input the board never gained.
  `/_board/image` itself is indifferent to where the bytes came from, since it takes a base64 data URL and writes into the board's `fig/`, so the whole gap is one missing button.
  Two constraints shape that button rather than the endpoint: `live/write.py` caps an image at 8MB and accepts only png/jpeg/gif/webp, while a phone routinely produces larger files and an iPhone shoots HEIC, so the browser must downscale and re-encode before posting instead of forwarding the file untouched.

- 260801 CC · 🔍 The narrow width is the same story as the shredded screen, one device further on
  `QD3` closed a shredded-screen round on 260801 by nudging the width on attach so the app repaints at the size this browser really has, which was the right fix for a desktop where the true width still fits the art.
  A phone does not clear that bar: roughly 390 CSS pixels at the current 13px metrics is about 46 columns, and claude's frames are drawn for far more, so a correct repaint at the true width is still an unreadable one.
  This is the point where polishing the grid stops paying and the form itself has to change.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🎨 Rule how far to close the gap with the SDK drawer, on the DESKTOP
      A · **Fix the layout defects only.** One surface, the rail reclaimed, notices positioned to the pane. Cheap, lands this week, and the pane still shows a screen rather than a document, so headings stay bold-ish text and URLs stay characters.
      B · **Fix the layout AND render the session as a document** (the archived `QD3m` route, owned as `QD3`'s 🪄 smooth pane): tail the session's jsonl and draw markdown bubbles, keeping the PTY as the engine and the raw TTY one toggle away. This is the only version that can actually match the drawer, and it is the larger build.
      C · **Drop the terminal pane on the desktop** and let the SDK drawer be the one chat surface, keeping the TUI for the phone or for a real CLI window.
      → CC's proposal: A now, B next, because A is cheap and true under every future, while B is the only thing that answers the comparison JL actually made.

- [ ] 📐 Rule the phone's form
      A · **Composer plus a read-only pane.** The TUI stays a screen but stops taking keystrokes on a phone; a plain native input sits under it and writes whole lines to the PTY. Smallest change, keeps one engine, and the pane is still 46 columns of art nobody can read.
      B · **The phone gets the smooth pane** (`QD3`'s route D, already the adopted plan of record there): the session renders as chat, which reflows to any width by construction, and the raw grid stays one toggle away for the moments only it can serve, such as permission dialogs and pickers. Largest change, and it is already on the roadmap for other reasons.
      C · **Keep the raw grid everywhere and fix only the input.** Cheapest, and it leaves the width problem standing, so the terminal stays readable-only on a tablet and up.
      → CC's proposal: **B**, with A shipped first as the stopgap, because A is a few hours and unblocks JL's phone this week while B is the form that actually fits the device and is already committed to on `QD3`.

- [ ] 🧭 Rule whether this page owns the desktop form too, or only the phone
      A · this page owns the terminal's form on every device, and `QD3` keeps strictly to the engine.
      B · this page is the phone question alone, and desktop polish stays in `QD3`'s 🚧 smoothness items.
      → CC's proposal: **A**, because `QD3`'s smoothness items are already half form and half engine, and splitting on that seam is what let the phone fall through both pages until JL hit it.

## Files
- `assets/js/10-drawer/30-terminal.js`
  The whole terminal front end: xterm construction, `fitTerm`, the WS protocol, input binding, paste, the ⌨ toggle, and the `pagehide` park beacon. Every option in the ruling lands here.
- `assets/js/10-drawer/20-chat/50-prefs-paste.js`
  The chat send loop: the streaming reader, `inflight`, `chatBusy`, and the `watchdog` whose `QUIET_GIVEUP` is the seven-minute stall.
- `assets/js/80-restore.js`
  Already records which half the drawer was showing and restores it on load; the natural home for a real entry handler.
- `live/term.py`
  `spawn_pty`, the `/_term/<key>/ws` terminus, and `park`. A composer that writes whole lines still arrives through this socket.

## Log
260802 0117 · Opening rebuilt to QB4 §1. The old version put the whole rationale BELOW the first blank line, so the stage showed one bare question and the four sentences that explained it were hidden in `More details` (QB4 §1.1.2 names this exact failure by example). The visible paragraph is now 4 sentences, about 455 characters, and follows the required shape: the question, what its own words mean with a real value for each, why that is hard, what this page decides. `More details` was one prose block and is now five bold-labelled parts per QB4 §1.3.1, including the bearing on `QD3` and `QD5` that QB4 §1.2.2 requires and the Opening did not have
260801 · JL compared the desktop terminal pane with the SDK drawer and called it ugly; five defects recorded (L-shaped session rail, three unjoined colour zones, CJK clipped at the right edge, a viewport-positioned notice landing outside the pane, a URL wrapping as bare characters), split into three cheap layout items plus the structural one: the drawer renders a document, the terminal renders a screen, so a 🎨 Decision Now row asks how far to close that gap
260801 · JL: "你这 opening 写得太操蛋了 … 我这个 opening 是要说我们怎么设计 TUI，然后它能够在这个配置上 work" Right, and the rewrite was measured against QB4 line 28 rather than taste. The old lead asked what the terminal should BECOME and then listed breakage, so it named the problem and never the design, which fails "name what this page GIVES the reader". It now leads on how one TUI is designed to survive a changing device, states the four-part contract as the ONE central idea, and ends on the crisp test. `method:` was carrying only three of the four constraints and now matches the Opening, Boundary and Content
260801 · JL: "为什么我们这个 page 里面没有 content?" Correct, and it was a real defect: the page had no `## Content` at all, so every piece of substance was sitting in dated `Where we are` bullets, which makes a LOG rather than a design page (QB4: "Substance found in Opening moves to Content"). Added five Content divisions, each opening with a face figure per QB4: the four-constraint device model, where typing happens, the width below which the grid itself is the defect, what a suspendable page owes on return, and the gesture audit
260801 · 🖼 BUILT and verified in Chrome on both branches: `35-imagepick.js` + a header button; terminal branch writes the path to the PTY, chat branch inserts markdown; canvas re-encode respects the 8MB cap and HEIC. Phone confirmation still owed
260801 · JL asked for a session button in the Quick actions strip; it already exists one tab over under ⚙ Settings and is hidden by `termView()` whenever the terminal is open. Recorded as a 🎛 item to UNHIDE rather than to add, since a second chooser is what JL's own "one chooser, not two" ruling removed
260801 · JL asked how to upload an image from a phone; the answer is that there is no way. Both entry points are `paste` listeners and `assets/js/` has no file input, `capture`, or drop handler, while `/_board/image` is already device-agnostic. Recorded as its own 🖼 item with the two `live/write.py` constraints the gesture must respect (8MB cap, no HEIC)
260801 · Opened from JL after the terminal proved hard to use on a phone: `QD3` owns the engine and has no design half, so the form question gets its own page. Carries the third-cause diagnosis for the doubled keystroke, the width argument that a correct repaint is still unreadable at ~46 columns, the exit-handler-without-entry-handler diagnosis for the freeze on returning, and the phone-form ruling for JL
