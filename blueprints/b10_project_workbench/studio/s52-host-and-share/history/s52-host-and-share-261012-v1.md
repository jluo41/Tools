s52 · Host and share with the team
==================================

**Tags:** `Server`

**Stage:** closed

**Topic:** how a Block is shared with colleagues: who may open it, how they prove who they are (their JHU JHED
sign-in), what they see and never see, and where it is hosted. s51 is how the server runs; s52 is who can reach
it. New on 261012 (JL: "how could I host it and share it with others? ... share the block with others, could we
use the JHU jhed accouunt to verify it? ... How hard it will be?"; then "maybe we can have the s52 about host and
share with the team?").

**Feeds:** `reports/` q12_space_hosting


Files
-----

```text
s52-host-and-share/
├── s52-host-and-share.md            this face; its frames: yaml holds every word of the drawing
├── build_s52_host_and_share.py      the builder: draws the frames below as four maps in one row
├── s52-host-and-share.excalidraw    the drawing: the current setup in three acts, Later at the right
└── s52-host-and-share.png           its preview
```


The drawing
-----------

Six maps of the current setup in three acts, a row each, read left to right and then down, and one frame at the right for what comes later (JL 261012: "do not use the later, just use the current settings ... put all the later in that new frame") (JL 261012: "we should not put all the frames just always from left to right"; the s51 shape, JL 261012: "one frame should be as large as possible, within the
frame, we want the workflow map or the mindmap, the frames should be well arrange to form the narrative"). Edit the
words here; `python build_s52_host_and_share.py` redraws.

```yaml
frames:
- title: "① What a colleague sees"
  act: "Act 1 · Who sees what"
  intro: "One shared Block, read-only; everything else is hidden, as if it were not there."
  bridge: who may see it
  notes: [{date: "261012", text: "the current setup only; what comes later is the frame on the right (JL)"}]
  boxes:
  - {id: who, at: [0, 0], title: 👥 a colleague, why: a JHU email you named, cols: 1,
     tree: ["jhu.edu · jh.edu · jhmi.edu", one person or a group, "a Block of any SPACE"]}
  - {id: see, at: [1, 0], title: 👀 what they see, why: "view: read-only", cols: 1,
     tree: [the Block's Studio drawings, its Reports, its s00 background and index]}
  - {id: never, at: [2, 0], title: 🚫 never shown, why: "404, as if it were not there", cols: 1,
     tree: [other Blocks and SPACEs, "changes, chat, the terminal", "private files: .env, the keys"]}
  - {id: home, at: [0, 1], title: 🏠 their Home, why: "block.jjluo.com/", cols: 1,
     tree: [only the Blocks shared with them, a sign-out link]}
  - {id: block, at: [1, 1], title: 📦 one shared Block, why: "or a Job, a Task, a Project", cols: 1,
     tree: ["e.g. Tools-SPACE/…/b10", "e.g. WellDoc-SPACE/…/b00"]}
  - {id: log, at: [2, 1], title: 🧾 who opened what, why: a line per page, cols: 1,
     tree: ["share-log.tsv: time · email · page", readable by JL only]}
  arrows:
  - {from: who, to: block, label: opens}
  - {from: block, to: see, label: shows}
  - {from: block, to: never, label: never shows}
  - {from: block, to: home, label: is listed on}
  - {from: block, to: log, label: is noted in}

- title: "② Who may see what: one access table"
  intro: "~/Desktop/.server_config/access.yaml: one table for every SPACE; no line, no access."
  bridge: how they sign in
  boxes:
  - {id: share, at: [0, 0], title: 🧰 wb.py share, why: you run it, or ask me, cols: 1,
     tree: ["<folder> --people <name>: a list", "<folder> <email>: one person", prints the link to send, "--list: who has what"]}
  - {id: table, at: [1, 0], title: 📋 access.yaml, why: "~/Desktop/.server_config", cols: 1,
     tree: ["owners: jluo41@jhu.edu", "grants: who · what · level", "groups: people/<name>.txt", "anyone@jhu: every JHU email (unused)"]}
  - {id: level, at: [2, 0], title: 🎚 the level, why: two today, cols: 1,
     tree: ["👀 view: read-only", "👑 owner: everything (you)"]}
  - {id: stop, at: [0, 1], title: ✂️ stop sharing, why: delete their line, cols: 1,
     tree: [their cookie stops working, nothing else to undo]}
  - {id: fresh, at: [1, 1], title: 🔄 no restart, why: the host re-reads the table, cols: 1,
     tree: ["a new line: works at once", "a removed line: ends at the next click"]}
  - {id: check, at: [2, 1], title: 🛡 every request, why: checked before anything runs, cols: 1,
     tree: ["not signed in: to sign-in", "every path it names in a grant?", "no: 404 · a change: 403"]}
  arrows:
  - {from: share, to: table, label: writes a line in}
  - {from: table, to: level, label: gives}
  - {from: level, to: check, label: enforced on}
  - {from: table, to: fresh, label: changes take effect}
  - {from: stop, to: table, label: removes a line}

- title: "③ Sign in with an emailed code"
  act: "Act 2 · How a person gets in"
  intro: "As Debate-AI does: a JHU email, a six-digit code by email, then a signed cookie."
  bridge: the whole path of a page
  boxes:
  - {id: open, at: [0, 0], title: ① 👤 opens the link, why: you sent it, cols: 1,
     tree: [any browser, nothing to install]}
  - {id: ask, at: [1, 0], title: ② 🖥 asks for an email, why: no cookie yet, cols: 1,
     tree: ["/_share/signin: your JHU email", "a form, not a password"]}
  - {id: check, at: [2, 0], title: ③ ✉️ checks the email, why: before any code goes out, cols: 1,
     tree: ["jhu.edu · jh.edu · jhmi.edu", "jh.edu becomes jhu.edu", "on the access table?"]}
  - {id: send, at: [3, 0], title: ④ 📧 sends a code, why: from noreply@cdhai.com, cols: 1,
     tree: ["6 digits, 10 minutes, one use", "any recent code works", "Azure: anivum-acs", kept hashed, never logged]}
  - {id: enter, at: [3, 1], title: ⑤ 🔑 enters the code, why: proves the inbox is theirs, cols: 1,
     tree: ["5 wrong tries: a new code", "10 codes an hour, at most"]}
  - {id: cookie, at: [2, 1], title: ⑥ 🍪 a signed cookie, why: the host's own secret, cols: 1,
     tree: ["holds the email, 7 days", "HTTP-only, HTTPS only"]}
  - {id: table, at: [1, 1], title: ⑦ 📋 the access table, why: "this email, this Block", cols: 1,
     tree: ["view, or owner", "no line: 404"]}
  - {id: page, at: [0, 1], title: ⑧ 📄 the page, why: read-only, cols: 1,
     tree: [the same workbench page you see]}
  - {id: quiet, at: [0, 2], title: 🤫 not on the table, why: "the same answer, no code", cols: 1,
     tree: ["\"if you have access, a code is on its way\"", nobody learns who has access]}
  - {id: code, at: [1, 2], title: 🧩 the code, why: "serve.py --share", cols: 1,
     tree: ["servers/_host/live/share.py", "7 tests; signed in live"]}
  - {id: mail, at: [2, 2], title: 📨 the mail key, why: set up 261012, cols: 1,
     tree: ["anivum-acs, Azure subscription 1", "cdhai.com linked: noreply@ works", "in ~/Desktop/.server_config/share.env"]}
  arrows:
  - {from: open, to: ask, label: asks}
  - {from: ask, to: check, label: an email}
  - {from: check, to: send, label: on the table}
  - {from: send, to: enter, label: to the inbox}
  - {from: enter, to: cookie, label: right}
  - {from: cookie, to: table, label: each request}
  - {from: table, to: page, label: serves}

- title: "④ The path of a page"
  intro: "From a colleague's browser to one Block on this Mac; no port is open on the Mac."
  bridge: what runs on this Mac
  boxes:
  - {id: person, at: [0, 0], title: 👤 a colleague, why: anywhere, cols: 1,
     tree: ["block.jjluo.com/_board/workbench", "with path=<the Block>"]}
  - {id: dns, at: [1, 0], title: 🌐 block.jjluo.com, why: "a Cloudflare name (261012)", cols: 1,
     tree: ["DNS → the tunnel macstudio", HTTPS from Cloudflare]}
  - {id: tunnel, at: [2, 0], title: 🚇 the tunnel, why: cloudflared on this Mac, cols: 1,
     tree: ["~/.cloudflared/config.yml", "block.jjluo.com → 127.0.0.1:5690"]}
  - {id: host, at: [3, 0], title: 🖥 the share host, why: "serve.py --share", cols: 1,
     tree: ["--root ~/Desktop: every SPACE", "127.0.0.1:5690: only the tunnel", "log /tmp/blocks-share-5690.log"]}
  - {id: gate, at: [3, 1], title: 🔐 sign-in and table, why: "③ and ②", cols: 1,
     tree: ["a cookie, else the emailed code", "a path in a grant, else 404"]}
  - {id: page, at: [2, 1], title: 📄 the Block's page, why: the same workbench, cols: 1,
     tree: ["Studio · Reports · s00", no Runs buttons, no edits]}
  - {id: again, at: [1, 1], title: 🔁 next visit, why: the cookie, cols: 1,
     tree: ["7 days: straight in", "then a new code"]}
  arrows:
  - {from: person, to: dns, label: opens}
  - {from: dns, to: tunnel, label: routes to}
  - {from: tunnel, to: host, label: forwards to}
  - {from: host, to: gate, label: checks}
  - {from: gate, to: page, label: serves}
  - {from: page, to: again, label: next time}

- title: "⑤ What runs on this Mac"
  act: "Act 3 · What runs, and how you share"
  intro: "Two doors on one Mac: yours on the tailnet, and the share door for everyone else."
  bridge: how you share one
  boxes:
  - {id: you, at: [0, 0], title: 🔒 5602 · your door, why: "the tailnet, no sign-in", cols: 1,
     tree: ["WellDoc-SPACE, all of it", "every tool's link checks"]}
  - {id: mac, at: [1, 0], title: 🖥 this Mac, why: Mac Studio, cols: 1,
     tree: [one serve.py per door, the same code]}
  - {id: door, at: [2, 0], title: 🌐 5690 · the share door, why: "block.jjluo.com, sign-in", cols: 1,
     tree: ["--root ~/Desktop", read-only for all but you]}
  - {id: cf, at: [3, 0], title: 🚇 cloudflared, why: a LaunchAgent at login, cols: 1,
     tree: ["tunnel macstudio, 15 names", "block.jjluo.com since 261012"]}
  - {id: restart, at: [0, 1], title: 🔁 after a Mac restart, why: the share door does not come back, cols: 1,
     tree: ["start it again: serve.py --share", "(see Later)"]}
  - {id: cmds, at: [1, 1], title: 🧰 your commands, why: "wb.py share", cols: 1,
     tree: ["share <folder> <email>", "share --list"]}
  - {id: files, at: [2, 1], title: 🗂 the share files, why: "~/Desktop/.server_config", cols: 1,
     tree: ["access.yaml: who sees what", "share.env: the mail key (600)", "share-secret · share-codes.json", "share-log.tsv"]}
  - {id: acs, at: [3, 1], title: 📧 anivum-acs, why: Azure subscription 1, cols: 1,
     tree: [Debate-AI's mail too, "noreply@cdhai.com"]}
  arrows:
  - {from: mac, to: you, label: you}
  - {from: mac, to: door, label: everyone else}
  - {from: cf, to: door, label: forwards to}
  - {from: door, to: files, label: reads}
  - {from: door, to: acs, label: codes go out through}
  - {from: cmds, to: files, label: edit}

- title: "⑥ How you share a Block"
  intro: "Six steps; steps 1 to 3 are yours (or mine, if you ask), 4 and 5 are theirs."
  boxes:
  - {id: s1, at: [0, 0], title: 1 · pick a Block, why: any SPACE on this Mac, cols: 1,
     tree: ["e.g. Tools-SPACE/blueprints/b10_…"]}
  - {id: s2, at: [1, 0], title: 2 · a people list, why: one JHU email a line, cols: 1,
     tree: ["wb.py share <folder> --people <name>", "then edit people/<name>.txt", "b10: people/b10.txt (261012)"]}
  - {id: s3, at: [2, 0], title: 3 · send the link, why: it prints it, cols: 1,
     tree: ["block.jjluo.com/…?path=…", by email or chat]}
  - {id: s4, at: [3, 0], title: 4 · they sign in, why: their JHU email, cols: 1,
     tree: ["the code from noreply@cdhai.com", "7 days, then again"]}
  - {id: s5, at: [3, 1], title: 5 · they read it, why: only that Block, cols: 1,
     tree: [read-only]}
  - {id: s6, at: [2, 1], title: 6 · take someone out, why: delete their line, cols: 1,
     tree: ["in people/<name>.txt", ends at their next click]}
  arrows:
  - {from: s1, to: s2, label: then}
  - {from: s2, to: s3, label: then}
  - {from: s3, to: s4, label: they open it}
  - {from: s4, to: s5, label: signed in}
  - {from: s5, to: s6, label: when done}

- title: "⑦ Later: not built yet"
  aside: "Later"
  intro: "Everything planned but not in the current setup; each needs a decision or a request first."
  boxes:
  - {id: jhed, at: [0, 0], title: 🪪 JHED sign-in, why: stronger than an emailed code, cols: 1,
     tree: ["🙋 JHU IT: an Entra app (client ID, secret)", "tenant ID public: 9fa4f438-…", "Cloudflare Access passes a signed email", same table, same cookie]}
  - {id: levels, at: [1, 0], title: 🎚 comment and edit, why: levels above view, cols: 1,
     tree: [red marks on drawings, "edit faces, tick proposals"]}
  - {id: button, at: [2, 0], title: 🔗 a Share button, why: on each Block, owner only, cols: 1,
     tree: [writes the same table, "instead of wb.py share"]}
  - {id: boot, at: [0, 1], title: 🔁 survive a restart, why: a LaunchAgent, cols: 1,
     tree: ["start the share door at login", "like the tunnel's"]}
  - {id: later, at: [1, 1], title: ⏳ later, why: not in the current setup, cols: 1,
     tree: [JL decides each]}
  - {id: groups, at: [2, 1], title: 👥 JHU groups, why: from Research IT, cols: 1,
     tree: [JHED groups, "instead of the table's"]}
  - {id: data, at: [0, 2], title: ⚖️ data rules, why: before study data, cols: 1,
     tree: ["study data or PHI: who approves", "maybe hosted inside JHU"]}
  - {id: guests, at: [1, 2], title: 🌍 outside JHU, why: guests, cols: 1,
     tree: ["today: JHU emails only"]}
  - {id: keep, at: [2, 2], title: 🧾 the log, why: how long to keep it, cols: 1,
     tree: ["share-log.tsv grows"]}
  arrows:
  - {from: later, to: jhed, label: ""}
  - {from: later, to: levels, label: ""}
  - {from: later, to: button, label: ""}
  - {from: later, to: boot, label: ""}
  - {from: later, to: groups, label: ""}
  - {from: later, to: data, label: ""}
  - {from: later, to: guests, label: ""}
  - {from: later, to: keep, label: ""}
```


Decided
-------

s52-D01 · Proposed (JL 261012): share one Block at a time, read-only, to people named on an allow list, who sign in
    with JHED; the gate (Cloudflare Access) sits in front of the server, so the server never sees a password, only
    the verified email. A one-time email code to JHU addresses stands in until the JHED app is registered.
s52-D03 · Proposed (JL 261012: "how could I give differnt people to difference access to different blocks?"): one
    access table per SPACE, `.server_config/access.yaml` (git-ignored: emails stay out of the Blocks' repos), lines
    of who (an email or a group) · what (a Block, or a Project meaning all its Blocks) · level (view < comment <
    edit < owner; the highest matching line wins; no line, no access). The server checks it on every request
    and answers 404 where there is no access; each person's Home lists only their Blocks. A Share button on a
    Block (owner only) edits the table later; until then JL edits the file.
s52-D04 · Proposed (JL 261012: "how could they use the jhed to login?"): sign-in is OpenID Connect between Cloudflare
    Access and JHU's Microsoft Entra (frame ③): Access sends the browser to JHU's own page (JHED ID, password,
    MFA), takes back a token Microsoft signed, and passes the request on with a pass Cloudflare signed. The share
    host checks that signature and reads the email from it; a bare email header is refused. JHU IT registers one
    Entra app (tenant ID, client ID, secret, Access's callback as its return address); nothing is set per person.
s52-D05 · Found (261012; JL: "so I need this information? I need to ask the RIT for it?"): of the three values the
    sign-in needs, JHU's tenant ID is public (`9fa4f438-b1e6-473b-803f-86f8aedf0dec`, the same for jhu.edu and
    jh.edu, read from login.microsoftonline.com/jhu.edu's sign-in metadata). The client ID and its secret come only
    from an app registered in JHU's Entra, which is JHU IT's to do (Enterprise Authentication, Sam Bennett; cc
    RITRequest@jh.edu). The request gives them the return address, Cloudflare Access's
    `https://<team>.cloudflareaccess.com/cdn-cgi/access/callback`, so the Cloudflare team name is chosen first.
    The secret expires (IT sets when); its renewal date goes in the table of who to ask.
s52-D06 · Found (261012; JL: "we have a repo in JHU-CHDAI/Debate-AI ... check how do they give use the email?"):
    Debate-AI (now `platforms/HAIChat-SPACE/haichat-ai/debate-ai`, WellDoc-SPACE) does not use JHED. A person types
    a JHU email and gets a six-digit code (10 minutes, single use, a few tries) sent from `noreply@cdhai.com`
    through Azure Communication Services (`ACS_CONNECTION_STRING`, `MAIL_FROM`); entering it proves they own the
    mailbox. Only jhu.edu, jh.edu and jhmi.edu (and their subdomains) may hold an account, plus
    `EXTRA_EMAIL_DOMAINS`; jh.edu and jhu.edu fold into one account, jhmi.edu stays separate. The session is a
    signed cookie (HS256 with `SESSION_SECRET`, 7 days); what a person may do comes from per-course roles (owner,
    assistant) checked on the server, never from the account kind. `ADMIN_EMAILS` get their codes in the server
    log when mail is not set up. So a sign-in with no IT ticket already exists at CDHAI: the same emailed code,
    from CDHAI's own sender, could gate the share host (with CDHAI's OK to use its ACS sender).
s52-D07 · Proposed (JL 261012: "How do you think we can use the Debate-AI method? Do you think we can do the same
    things here?"): yes; the first sign-in is Debate-AI's emailed code, built into the share host (frame ③): a JHU
    email (jhu.edu, jh.edu folded into it, jhmi.edu its own), a six-digit code for 10 minutes and one use, sent
    from noreply@cdhai.com through Azure Communication Services, then a signed HTTP-only cookie for 7 days. One
    change from Debate-AI: a code goes only to an email the access table names, and everyone gets the same
    answer, so nobody learns who has access. It needs CDHAI's OK and its ACS connection string, not JHU IT; no
    Cloudflare Access gate in front. JHED (④) stays the later upgrade: the same table and the same cookie, a
    stronger proof. This changes D01's gate: Access only arrives with JHED.
s52-D08 · Built (JL 261012: "CDHAI is me, it is okay. Go ahead and update it."): version 1 of the share mode.
    `serve.py --share` with `servers/_host/live/share.py`'s `ShareMixin` ahead of `AuthMixin`: sign-in at
    `/_share/signin` → a code (Debate-AI's rules; only to an owner or a named email; the same answer for
    everyone) → `/_share/verify` → a signed cookie for 7 days; then each request's paths (`path=`, `board=`, ...
    or the file asked for) must sit inside a grant of `.server_config/access.yaml`, else 404; a viewer's Home
    lists only their Blocks; POST, the terminal and chat are an owner's (levels above view come later);
    every granted request is a line in `share-log.tsv`. Mail is Azure Communication Services from
    noreply@cdhai.com once `ACS_CONNECTION_STRING` is in `.server_config/share.env`; until then an owner's
    code goes to the server log. Tests: `_host/tests/test_share.py`, 7, and all 215 server tests pass. Live on
    WellDoc-SPACE (127.0.0.1:5690, then stopped): sent to sign-in, code from the log, signed in, b00's page 200,
    a wrong code 401. WellDoc-SPACE's `.server_config/` now holds `access.yaml` (owner jluo41@jhu.edu, no
    grants yet) and `share.env`, git-ignored.
s52-D09 · Proposed: two doors on one SPACE, one code. The tailnet host (WellDoc 5602) stays JL's private door
    with no sign-in, and every tool's link checks keep working; the share door is the same serve.py on the
    same SPACE root with `--share`, bound to 127.0.0.1 so only the tunnel reaches it. This revises D02 (which
    put share mode in the main host): the 261008 lesson was a host rooted at a folder with a password; this
    one is rooted at the SPACE and signs people in.
s52-D10 · Built and open (261012; JL: "could you make it to be the block.jjluo.com? please do it"; "How could i
    share one block to others? For example, for the b10."): `block.jjluo.com` is live: a tunnel line in
    `~/.cloudflared/config.yml` and its DNS name to `serve.py --share` on 127.0.0.1:5690, rooted at WellDoc-SPACE
    (sign-in 200, everything else 303 to sign-in, from outside). `wb.py share <folder> <email>` writes a grant and
    prints the link (`cli/wb_share.py`); the host reads `access.yaml` again when it changes. b10 sits in the Tools
    SPACE, which WellDoc reaches only through its `Tools` link, and the workbench refuses a path that leads out of
    its root, so b10 does not open on this door. Two ways: (A) one door rooted at the Desktop (tested locally: b10
    and b00 both 200), one table for every SPACE, but the permission check refused to put the whole Desktop behind
    the public tunnel; (B) one door per SPACE, Tools behind its own name (`.server_config/` ignored in Tools first).
s52-D11 · Decided (JL 261012, ran it; "I want the block.jjluo.com to share whatever blocks"): option A. The share
    host behind block.jjluo.com is rooted at the Desktop (`serve.py --root ~/Desktop --share`, 127.0.0.1:5690), so
    one table, `~/Desktop/.server_config/access.yaml`, can grant any Block of any SPACE; WellDoc's own table was
    removed. `wb.py share <folder> <email>` finds that table by itself. Checked from outside: sign-in 200; b10 and
    every other path 303 to sign-in; signed in as the owner, b10 and Proj01's b00 both 200. The risk taken: a gate
    bug would reach the whole Desktop, so the gate stays default-deny and its tests run with every change.
s52-D12 · Decided (JL 261012: "could you give me a link and I can share?"; then "Only people I name"): b10's link
    is `https://block.jjluo.com/_board/workbench?path=Tools-SPACE/blueprints/b10_project_workbench&studio=1`, and
    it opens only for the emails added with `wb.py share`. A grant `who: anyone@jhu` (every jhu.edu, jh.edu and
    jhmi.edu email) now exists for a link meant for all of JHU (live/share.py `ANYONE_JHU`, tested), unused for b10;
    the running share host loads it at its next start.
s52-D13 · Built (JL 261012: "could I only prepare a list of jh emails, only these people can access it"): a group
    may read its members from a list file, `groups: {b10: "@people/b10.txt"}`, one JHU email a line, # for notes;
    the host watches the file, so a saved edit lets someone in or takes them out at their next click.
    `wb.py share <folder> --people <name>` makes `~/Desktop/.server_config/people/<name>.txt` (mode 600) and the
    grant. b10 is shared with group b10 this way; its list is empty until JL fills it. 9 share tests pass.
s52-D14 · Fixed (JL 261012, a screenshot: the code email arrived, then "No response."): five codes for one email in an
    hour had used up the limit, so later asks showed "Check your inbox" and sent nothing; and each new code had
    replaced the last, so a code from an earlier email failed. Now any code from the last 10 minutes works, one
    success ends them all, the limit is 10 an hour, and the page says so. An owner's Home is the share list, not a
    scan of every SPACE under the Desktop. Checked through block.jjluo.com: verify 303, Home 200, b10 200.
s52-D15 · Closed (JL 261012: "looks good, you can close the s51 and s52 now"): block.jjluo.com shares any Block of any SPACE on this Mac, read-only, to the JHU
    emails a people list names, signed in by a code from noreply@cdhai.com; b10 is shared with group b10
    (xzhi2@jh.edu). What is left is frame ⑦ (Later): JHED, comment and edit, a Share button, surviving a
    restart, JHU groups, data rules, guests, the log's keeping.
s52-D02 · Proposed: the share mode is the main host's own (`serve.py --share`), not a second host rooted at a
    folder: the 261008 Samsung password host was that and was rolled back.


Open
----

1. Which Block is shared first, and with whom?
2. Study data or PHI in a shared Block: who approves, and must it be hosted inside JHU (⑤ B)?
3. Colleagues outside JHU: a JHU guest account, or no?
4. How long to keep the log of who opened what?
5. The four levels: is comment needed at first, or view and edit only?
6. Groups: kept in the table, or JHU's own groups (a JHED group, as Research IT builds for JH-CDHAI)?
7. Sign-in: Debate-AI's emailed code (CDHAI's sender, no IT), Cloudflare's emailed code, or JHED? (D06)
8. Decided: one door for every SPACE (D11). The share host stops at a reboot: keep it up with a LaunchAgent?

(write here, or mark the drawing in red)
