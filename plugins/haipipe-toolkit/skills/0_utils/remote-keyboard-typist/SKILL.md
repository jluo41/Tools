---
name: remote-keyboard-typist
description: >-
  Type an exact text into an editor on a remote machine that allows no paste, by
  pressing the Chrome Remote Desktop on-screen keyboard one key at a time (a page
  script presses its buttons, 70 ms per key; click batches as fallback). The AI
  is only a typist: it cleans the text, guides the person to get the remote
  editor and keyboard ready, confirms that state itself with a probe, types the
  whole file in one pass, then reviews every line and fixes wrong ones. It never clicks the remote screen (one
  focus click inside the editor excepted), never saves, never runs. Use when the person says "type this into <file> on the
  server", "you cannot paste, type it", "operate the keyboard", or shares a
  Chrome Remote Desktop tab with an open editor. Trigger: type on the server,
  remote typing, on-screen keyboard, no paste, keyboard only, /remote-keyboard-typist.
argument-hint: "<file path or pasted text>  [--target <file name open in the remote editor>]"
allowed-tools: Bash, Read, Write, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__javascript_tool, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__browser_batch
metadata:
  version: "0.2.0"
  last_updated: "2026-10-25"
---

Skill: remote-keyboard-typist
=============================

Some machines take no paste: a secure server behind Chrome Remote Desktop (CRD),
often with a second Remote Desktop window inside it. The only way in is keys.
This skill makes the AI a typist and nothing else.

```
  THE AI DOES                          THE PERSON DOES
  clean the text, build the key plan   open the editor, the file, the keyboard
  check the prepared screen (probe)    unlock, reconnect, type any PIN
  press keyboard keys, whole file      save, run, close dialogs
  check every line against the text    decide what to do with a mismatch it cannot fix
```

**The one sentence that governs this skill:** the AI clicks only the on-screen
keyboard's own buttons, and only after the probe in step 3 passed.


The five steps
--------------

```
1 CLEAN   (AI, offline)    text ─▶ key_plan.py ─▶ <stem>.typed.txt + <stem>.plan.json
2 PREPARE (person)         checklist below, then the person says "ready"
3 CONFIRM (AI, read+probe) four checks + probe; fail ─▶ say which, wait; pass ─▶ go
4 TYPE    (AI)             page script presses the whole file (70 ms/key), then review
5 REPORT  (AI)             lines typed, lines fixed, "not saved, not run"
```

Step 1 and step 2 happen together: the AI sends the checklist and the cleaned
text in ONE message, so the person's "ready" also approves the text. Step 3
starts on "ready" and step 4 follows the passed probe without asking again.


1 · CLEAN (offline, before anything on the remote)
---------------------------------------------------

```bash
python <skill>/scripts/key_plan.py SOURCE [--from-markdown] [--compare FILE] --out-dir <scratchpad>
```

- **Look for the file first.** Search the working repository for the target's
  file name (`find . -name <target> -not -path '*/_WorkSpace/*'`). Chat copies
  lose things no cleaner can recover (see CHECK INDENT).
- **Pasted text** (signs: `&#x20;`, a line starting `*Set-Location*`, `\*`,
  `\_`): save it to the scratchpad as `.md` and pass `--from-markdown`. It renders
  Markdown escapes (`\X` becomes `X`), entities (`&#x20;` becomes a space),
  `*emphasis*` around a word, and smart quotes, and prints each changed line.
  It refuses a code file, where `\*` is real code.
- **Paste and file both exist:** clean the paste with `--compare <file>`.
  Differences only in indentation: type the file. Any other difference: type
  the paste (it is the request) and list the differing lines in the PREPARE
  message, so "ready" approves them.
- **CHECK INDENT with no file:** give each flagged line the indent of the line
  above it inside the same block, edit `<stem>.typed.txt`, rerun key_plan.py on
  it (no flag), and list those lines in the PREPARE message.
- **STOP** means a character has no key (tab, non-ASCII). Report line and column.
- `keys_needed` already includes the probe's keys, so one key map serves both.
- The plan names BASE keys only: `$` is `Shift, 4`; `{` is `Shift, [`; `\` is
  `Backslash`; space is `Space`. Read the plan from disk inside the driver.
  **Never retype the text into a code string**: `String.raw` with `\\` gives
  two backslashes, which is where every doubled backslash came from (261024).


1b · WRITE FOR THE KEYBOARD (when the AI writes the text itself)
-----------------------------------------------------------------

Every character is a click, and a shifted character (`$ ( ) { } " _ | :`,
capitals) is two. `run_fix_data_table.ps1` (261025) cost 1,159 clicks: 372 for
shifted characters, 162 for indent spaces. When the AI writes a script that
will be typed this way:

1. Lowercase cmdlets and parameters (`get-childitem -recurse`); PowerShell ignores case.
2. Single quotes unless the string needs a `$` expanded.
3. Two-space indent, short variable names, no comments.
4. A plain variable instead of `$( )` where it works; fewer lines over clever lines.
5. Print the click count from key_plan.py next to the script. With the page
   script about 1,200 keys is two minutes; much longer text belongs in an upload
   package, not in typing.


2 · PREPARE (the person, guided by one message)
------------------------------------------------

Send this checklist, fill in the target name, and put the cleaned text under it
(numbered lines, as key_plan.py printed them), with any source choice from step
1 named. The person's own reply-format rules still apply around it: the
checklist and the text are the body. Then wait for "ready".

```
Before I type <N> lines into <target>, please get these ready:
1. CRD (Chrome Remote Desktop) tab open and connected; the remote is unlocked (you type any PIN).
2. CRD on-screen keyboard shown, letter layout (extended keys hidden).
3. In the remote VS Code, once per machine, these in settings.json:
     "editor.autoClosingBrackets": "never",
     "editor.autoClosingQuotes": "never",
     "editor.autoSurround": "never",
     "editor.autoIndent": "none",
     "editor.formatOnType": false,
     "editor.acceptSuggestionOnEnter": "off",
     "editor.quickSuggestions": { "other": false, "comments": false, "strings": false },
     "editor.suggestOnTriggerCharacters": false,
     "editor.stickyScroll.enabled": false
4. <target> is open, the cursor is where the text goes (an empty file is best),
   and you clicked inside the editor once.
5. No dialog, notification or save conflict covers the editor.
Reply "ready" and I start. I will not click anything but keyboard keys,
and I will not save or run.
```

Item 3 is why the 261023 to 261025 session was slow: VS Code closed brackets,
indented, accepted a suggestion on Enter, and closed the `'@` here-string on its
own, and every one of those had to be found and undone. Another editor
(PowerShell ISE, Notepad++): item 3 becomes "turn off its auto-pairing and
auto-indent"; the probe below works the same in any editor.


3 · CONFIRM (four checks, then a probe)
----------------------------------------

On "ready", run C1 to C4. Any failure: one sentence naming it, then wait for
"ready" again. Never repair it by clicking.

```
C1 tab        the tab URL is remotedesktop.google.com/access/session/...
C2 keyboard   buttons named q, Shift, Enter, Space, Backspace exist
C3 key map    page script: crd_type.js loads and returns no MISSING;
              click batches: a ref for every key in plan.keys_needed
C4 target     a screenshot shows <target> as the active editor tab
P1 probe      press (through the page script: crd_batches.py PLAN --tab 0 --js --probe):
              Shift a, a, Shift 4, Backslash, Shift 9, Shift [, Shift ', ;, Space, z, /
              the zoomed line must read exactly  Aa$\({"; z/   (11 characters)
P2 clean up   Backspace until the zoom shows the line's start state
```

The probe proves four things at once: Shift lasts one key (`Aa`), shifted
digits work (`$`), the unnamed Backslash button is right, and the editor added
no closer after `(`, `{` or `"`. In VS Code an added closer sits to the RIGHT of
the cursor (`Aa$\({";"})`). Then: clean up and stop, item 3 is not in effect.

Clean-up counts from the screen, never from the plan: click Backspace once per
character seen left of the cursor, zoom, repeat until the start state. VS Code
may delete a pair with one Backspace, so check before each extra round. Text
left to the right of the cursor: open the extended keys (a keyboard button),
click Delete as needed, hide them again, and read the key map again (C3).

A doubled letter means the keyboard repeats keys: wait 0.3 s between clicks
from then on and probe again. The default pace has no wait.

After P2, say one line ("Probe passed, typing <N> lines") and go straight on.


4 · TYPE (whole file in one pass, then review)
-----------------------------------------------

**Main path: the page script** (tested 261025, about 2 minutes for 35 lines).

```
1 load    javascript_tool: paste scripts/crd_type.js        ─▶ 'crd_type ready'
2 keys    crd_batches.py PLAN --tab 0 --js                   ─▶ one JSON key list
3 start   javascript_tool: window.__keys = <that list>;
          window.__crdResult = 'running';
          window.__crdType(window.__keys, 70).then(r => { window.__crdResult = r; })
4 wait    about 75 ms per key (35 lines: ~90 s), then read window.__crdResult
5 review  4b FINAL CHECK, then fix wrong lines (Replace line N below)
```

- The script presses the CRD on-screen keyboard's own buttons from inside the
  page, one per key: the same keyboard, no paste, no clipboard.
- **70 ms per key, never less.** At 25 ms the remote fell behind and lines 9
  to 14 came out scrambled (`Where-Ob4seen.`); at 70 ms all 1,162 keys landed.
- Start it without `await` and poll `window.__crdResult`; a long await can time
  out the tool call. `MISSING <keys>` means the keyboard is not on the letter
  layout or Shift is latched: fix that, reload the script, start again.
- Run the probe (P1) through the script once first. If the probe does not read
  exactly, use the fallback.
- Waiting: several `computer wait` calls of up to 10 s (shell sleep is blocked).
- If a doubled letter shows, raise the delay to 300 ms and probe again.
- The page script presses only the letter layout. Home, End, Page Down and
  Delete live on the extended layout: for the final check and line fixes,
  click them by ref (`read_page` after showing the extended keys), then hide
  them again.
- To clear the file first, put `"Control","a","Backspace"` at the front of the
  key list (Control latches for one key, tested 261025).

**Fallback: click batches** (8 minutes for the same file). `crd_batches.py PLAN
--tab <id> [--iso] --max 600` prints `browser_batch` lists of `computer
left_click` items; send them back to back with no zoom in between. One list of
all 1,159 clicks also worked. It is slow only because the AI writes one click
object (about 100 characters) per key: 6.5 of the 8 minutes.

- The screen trails the clicks by 1 to 2 seconds: wait 2 s before any zoom, or
  a correct line looks short.
- Read the line from a zoom of the editor, never from memory. Count spaces in
  the indent, and every `\`, quote and bracket.
- Fixes use only keyboard keys, never the mouse. The person does not need to
  approve each fix (JL 261025): a wrong line is replaced whole.
- **Replace line N** (any line, also after the whole file is typed):

  ```
  Control + g, digits of N, Enter     go to line N, cursor at column 1
  Shift + End  (End: extended keys)   select the whole line, indent included
  click the keys of the correct line  typing replaces the selection
  Control + End                       back to the end of the file
  ```

  Then zoom on line N and its neighbours. First use on a machine: check that
  Control and Shift latch for one key on the CRD keyboard, like Shift does in
  the probe, and that the extended layout's End works; read the key map again
  after every Fn toggle.
- If a click errors or the keyboard looks different (Shift stuck, extended keys
  shown), read the key map again before the next line (C3).
- The final line gets no Enter after it. The editor decides line endings
  (CRLF on Windows) and the final newline when the person saves; the promise is
  the same characters, line for line.


Stop rules (one sentence, then wait)
-------------------------------------

```
CRD shows "reconnect", "unable to reach" or a PIN screen     ─▶ stop
the editor tab is gone, focus is on the desktop or a dialog  ─▶ stop
a notification or "not responding" box appears               ─▶ stop
the same line fails twice                                    ─▶ stop
```

Say the last line that passed its check ("line 13 of 35 checked; line 14 may be
partly typed"), so the person can restore the state and say "continue". If the
person put a PIN or password in the chat, say once that they should change it.

On "continue":

1. Run C1 to C4 again and build the key map fresh (refs may be new).
2. Zoom on the last lines. Check line N, the last one that passed, against the text.
3. A partly typed line N+1: Backspace it to its start state, counting from the screen.
4. After a reconnect or page reload, run the probe again on that empty line.
5. Resume at line N+1.


Never
-----

1. Never click anything on the remote picture (menus, taskbar, dialogs), with
   one exception (JL 261025): one click inside the editor's text area to give it
   focus, when the probe shows the keys are not arriving.
2. Never send keys any other way than clicking the on-screen keyboard (JL
   261025): no `typeText`, no `type` action, no `key` action into the remote.
   The `key` action sends Shift only as a flag, not as its own key event
   (tested 261025 on a local page: `shift+4` typed `4`), so the remote loses it.
3. Never paste, never use "Compose text locally", never touch the clipboard.
4. Never save, run, rename, or change the file's language mode.
5. Never type a PIN, password or token, even when asked; the person types it.
6. Never call the text "complete" before every line passed its check.
7. Never change the text: no reformatting, no fixes, no newer version. If the
   text looks wrong, say so in the REPORT, and still type it as given.


4b · FINAL CHECK (the whole file, keys only)
---------------------------------------------

Per-line checks miss lines that change later (an auto-closer, a joined line).
After the last line, read the whole file once:

1. Click Control + Home, then take a screenshot; Page Down until the end.
2. Compare every visible line with typed.txt: line numbers, indent, every character.
3. Count `{` and `}` (and `(` `)`) on screen; they must equal the counts in typed.txt.
4. Sticky scroll pins outer lines at the top and hides the lines under them;
   if it is on, say which lines could not be seen.

For a PowerShell file, also give the person this one-line syntax check to type
after saving (empty output means no syntax error; it does not prove the text):

```
$e=$null; [void][Management.Automation.Language.Parser]::ParseFile("$PWD\<target>",[ref]$null,[ref]$e); $e
```

Never compare by content hash.


5 · REPORT
----------

```
Typed <target>: <N>/<N> lines, <k> fixed on the way, not saved, not run.
```

Then list any line that needed a fix (line number, what went wrong), any
CHECK INDENT decision, and anything in the text that looked wrong to you. If
typing stopped, report where (see Stop rules) instead of a count.


Drivers
-------

The steps are the same for every harness; only the click call differs. In both,
map key names to refs ONCE while the keyboard is unshifted (C3); since the plan
uses base keys, the map stays right when Shift changes the labels.

**Fast path (claude-in-chrome, tested 261025).** Paste `scripts/crd_type.js`
with `javascript_tool`, then send the key list from `crd_batches.py PLAN --tab 0
--js` (6.6 KB for 35 lines) as `window.__keys` and start
`window.__crdType(window.__keys, 70)` without await; read `window.__crdResult`
after about 75 ms per key. It presses the same on-screen keyboard buttons from
inside the page, so nothing is pasted. Measured: 35 lines, 1,162 keys, 84 s of
pressing, about 2 minutes in all, against 8 minutes for click batches, where
6.5 of the 8 minutes were the AI writing one click object per key. Never go
below 70 ms: at 25 ms the remote fell behind and scrambled lines 9 to 14.
Probe with it first (P1). If the probe fails, use click batches below.

**Claude Code (claude-in-chrome), click batches.** The CRD tab must be in this session's tab
group: create the group (`tabs_context_mcp` with `createIfEmpty`), then the
person drags the CRD tab into it; never open a second session. `read_page`
(interactive filter) lists the keyboard buttons, but the character keys have NO
names, only refs, in screen order (verified 261025, letter layout):

```
ref_5..17   ` 1 2 3 4 5 6 7 8 9 0 - =      ref_18 Backspace  ref_19 Tab
ref_20..32  q w e r t y u i o p [ ] \      (ref_32 = Backslash)
ref_33..43  a s d f g h j k l ; '          ref_44 Enter      ref_45 Shift
ref_46..55  z x c v b n m , . /            ref_61 Space
```

Ref numbers can shift if the page changes, and the layout itself can change
after a reconnect: on 261025 a second layout had one more key (also `\`)
between the left Shift and `z`, so z..m , . / move to ref_47..56, the right
Shift to ref_57 and Space to ref_62. Count the unnamed buttons between the two
"Shift" buttons in read_page: 10 = the map above, 11 = pass `--iso` to
crd_batches.py. The probe's ` z/` proves the bottom row and Space. Shift: one
click on the LEFT Shift (ref_45) shifts only the next key (probe `Aa`). Two
clicks on either Shift lock the shifted layer, shown in blue, and one more
click on the same Shift unlocks it (both tested 261025: `$$A`, then `aa`). A
lock costs 3 extra clicks, so it pays only for 4 or more shifted characters in
a row (8 clicks saved in run_fix_data_table.ps1). Control also latches for one
key: Control, then a, selects all (tested 261025). Build the
batches with a script from plan.json (base key to ref), then send them as
`browser_batch` lists of `computer left_click {ref}` items. Never use the
`type` or `key` actions. If the probe shows nothing, the page focus may be off
the remote (`document.activeElement` is BODY, not the DIV labelled "Desktop"):
ask the person to click inside the editor once, then probe again.

**Codex (browser tab in node_repl).** `tab.playwright.getByRole('button', {name, exact: true}).click()`;
for Shift use `.first()`; for Backslash use its index from `tab.getAXState()`
(the unnamed button after `]`). Load the plan with `JSON.parse(fs.readFileSync(plan))`
and loop over `keys`; never put the text itself in a string literal.

**The CRD keyboard's icons** (names as the accessibility tree reports them).
`Fn` is the button "Show/hide extended keys". The pencil at the bottom right is
"Compose text locally": never click it. In the extended layout, the block on
the right is laid out as on a PC keyboard:

```
⎀ Insert     ↖ Home   ⇞ Page Up     ⌫ Backspace
⌦ Delete     ↘ End    ⇟ Page Down
             ↑ Up
← Left       ↓ Down   → Right       ⇧ Shift
```

Top left: the circular arrow is Escape, the arrows over a bar are Tab. The
middle block is the number pad (`/ * - +`, digits, `.`, Enter). Backslash is not
in the extended layout: it is in the letter layout, right of `]`.

Where this came from: a Codex session of 261023 to 261025 typed six PowerShell
files into VS Code on a secure server this way, in 745 tool calls. Each rule
above answers one thing that went wrong there.
