# One excalidraw per board, one frame per page

state: 🟡 PARTIAL
owner: JL
method: settle what can be generated before deciding what to pay for; the hosted half turned out to be a container we run ourselves

## Question
Can a board own ONE excalidraw, carrying a frame per page, with each page's Diagram opening at its own frame?
Yes, and it is running: one scene in the repo, 28 frames, an open-source editor in a container reached through the one port that is forwarded, and what you draw is written back to the file.
What is still a question is the edges of that: an image pasted into a scene does not survive, regenerating overwrites the seeded figure, and none of it has been through a real browser yet.

Before this, an excalidraw was pasted per page, one at a time, by a human who drew it somewhere else.
That works and it loses the thing a board most wants from a drawing, which is the relationships BETWEEN pages: the Pipeline ASCII in `board.md` is exactly that attempt, made in a medium that cannot show a link.
One excalidraw with a frame per page puts every page on one surface, so moving a box is a statement about the board rather than about one question.
The thing that would have made this fragile is identity, since a hosted deep link is `…/s/<scene>/<key>?element=<id>` and a re-share kills all 28 at once; owning the file removes that failure entirely, which is most of why the local route won.

## Boundary
- ✅ Covered here
  Whether one excalidraw per board is generated or hand-made, how a page names its frame, where the scene identity lives, and what a re-share costs.
- ↪ Covered elsewhere
  How an excalidraw RENDERS inside a Diagram, and why the ASCII figure stays regardless, is `QA4 §2`.
  Attaching a single excalidraw to one page by hand, from the page, is `QD7`.
  Where a secret would live if one were needed is `QE6`.

## Diagram

```
 WHAT IS BUILT · one file, two URLs off it, nothing bought
 ═══════════════════════════════════════════════════════════════════════

   board.md            ## Pages -> the groups, the order
   QA4a-*.md  ×28      ## Diagram's first ``` block -> this frame's seed
        │
        │  xcal.py                 (re-runnable: stable ids, keeps a human's
        ▼                           drawing and position, drops dead frames)
   fig/board.excalidraw            ONE scene · 28 frames · 89 elements
        │                          committed, diffed, no account, no key
        │
        ├──► ?board=<scene>              the whole board, every page side by
        │                                side. the only place the relations
        │                                BETWEEN pages can be said at all
        └──► ?board=<scene>&frame=QA4a   one page's frame, computed per
                                         request by serve_frame(); an unknown
                                         name lists the real ones

   the editor        excalidraw/excalidraw in docker on :5610
        │            proxied by serve.py at /_excalidraw/ , so it rides the
        │            single forwarded port (QE6) and is same-origin
        ▼
   assets/xcal-boot.js   INJECTED into that app by the proxy, because the
                         app has no save-to-a-server: it loads from #url=
                         and saves to the browser. so the script takes the
                         browser's storage instead. no #url= -> no dialog.

 WHO MAY WRITE, AND WHY IT IS NOT EVERYONE
 ───────────────────────────────────────────────────────────────────────
   28 iframes on a board page share ONE origin and ONE storage key, so an
   editable embed would be 28 editors overwriting each other.

   embed   ?board=&frame=          in-memory storage · hand tool · zen mode
           reads, pans, zooms, PERSISTS NOTHING
   ✏️ tab   ?board=&frame=&edit=1   real storage · holds a lock · autosaves
           a second tab drops to read-only and says whose pen it is

 BOTH DIRECTIONS NOW
 ───────────────────────────────────────────────────────────────────────
   markdown ──► scene   xcal.py, any time, re-runnable
   scene ──► markdown   POST /_board/excalidraw-save every 1.5s + on unload
                        with frame=  MERGES that slice, other 27 untouched
                        without      replaces the scene, since that edit was
                                     made with the whole scene on screen
   still one-way        the SEED. edit the ASCII text in Excalidraw and the
                        next regen takes it back. drawings around it survive.
```

```
 THE THREE ROUTES THIS PAGE OPENED WITH, AND WHY NONE OF THEM WON
 ═════════════════════════════════════════════════════════════════════

 ① FILE ONLY · we host it, nobody else is involved
   edit in     VS Code Excalidraw ext · Obsidian Excalidraw plugin
   truth       fig/board.excalidraw, committed, diffed, reviewed
   page shows  inline SVG, exported at build time
   deep link   none. there is no URL, so nothing to anchor into
   needs       an SVG exporter we do not have yet
   costs       nothing. no account, no key, no network, ever
   survives    copy · offline · git history · anyone with the folder
   breaks      a human draws freehand and our renderer cannot draw it back

 ② PLUS API · they host it, we drive it
   edit in     excalidraw.com, in a Plus workspace
   truth       their scene; our file becomes a copy
   page shows  iframe + fallback link, which is what QD7 already renders
   deep link   ?element=<frameId>, and the ids are OURS because we PUT
               the content, so a frame can simply be called QA4
   needs       Plus subscription · API key in env.sh (QE6) · network
   costs       paid tier, public beta, breaking changes expected
   survives    nothing offline. no network is an empty box
   breaks      the beta moves, or the subscription lapses, and every
               page's Diagram goes blank at once

 ③ FILE IS TRUTH, SCENE IS A PROJECTION
   edit in     either; the file is what gets committed
   truth       fig/board.excalidraw, exactly as in ①
   page shows  inline SVG for reading, plus a link to the live scene
               for drawing on together
   deep link   yes, via ②
   needs       everything ① needs, plus everything ② needs
   costs       the union of both
   survives    the SVG does, so the page still reads with no network
   breaks      DRIFT: the file is edited and the scene is not re-PUT,
               so the page shows one drawing and the link opens another

 ④ WHAT WE BUILT · the file is truth AND the editor is ours
   edit in     the OSS app, in a container, on this machine
   truth       fig/board.excalidraw, exactly as in ①
   page shows  an iframe of our own editor, opened at this page's frame
   deep link   yes, and computed by serve.py rather than bought
   needs       docker, and serve.py already running
   costs       nothing. ① 's price with ② 's deep link
   survives    git history, offline, anyone with the folder AND docker
   breaks      a copied board.html has no server, so the iframe is empty;
               the ASCII figure is why the page still reads (QA4 §2)

 WHAT ACTUALLY DECIDED IT
 ─────────────────────────────────────────────────────────────────────
   the fork was "must a colleague DRAW on it, without the repo?", where
   yes cost a subscription. ④ dissolves the fork instead of answering
   it: the editor is a container, so drawing needs no account, and the
   deep link is a projection we compute, so it needs no share.

   what ④ does NOT give is a colleague with no machine of ours, and
   that is QE1's question, not this one.

 THE IDENTITY RULE, and what ④ did to it
 ─────────────────────────────────────────────────────────────────────
   hosted   …/s/<scene>/<key>?element=<id>
            re-share mints a NEW <scene>, so all 28 links die together
   ours     …/board.excalidraw?frame=<page id>
            there is no <scene> to mint, so there is nothing to die

   the risk moved rather than vanished: each page now stores a whole
   URL, and what keeps that cheap is that `xcal.py --wire` rewrites all
   28 in one command. one open item still asks whether cheap is enough.

   this was never hypothetical: four cross-board ids broke on 260726 alone
```

http://127.0.0.1:5599/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw&frame=QA4a

## Content
### §1 The route: our own Excalidraw, on localhost
Proved 260726. It removes the API key, the subscription, the vendored bundle and the SVG exporter at once.

#### P0. One excalidraw for the board, one FRAME per page
(JL 260726, and the single scene is the point rather than a packaging detail)
`fig/board.excalidraw` is one file holding one frame per page, named for the page: `QA4a`, `QD7`, `QA8`.
It is never split into a file per page, because a single surface is the only thing that can say how the pages RELATE, which is the job `## Pipeline` does badly in ASCII and the only argument for drawing at all.
Editing happens on the whole board; a page's Diagram opens at its own frame.

#### P1. The editor is ours, and it already knows how to load our file
(`docker run --rm -d -p 5610:80 excalidraw/excalidraw`, reached through `serve.py`)
The open-source app carries a scene loader nobody documents: `window.location.hash.match(/^#url=(.*)$/)`.
So it fetches a scene from any URL, which means it fetches ours, out of the repo, served by `serve.py`.
It runs in its own container on its own port, and only 5599 is forwarded to a laptop, so an iframe at `127.0.0.1:5610` answers "refused to connect" on any machine that is not the one running docker.
`serve.py` therefore proxies it at `/_excalidraw/`, the same trick ttyd already uses for the terminal, and the whole thing lives behind the one port that is forwarded.
That also makes the editor same-origin with the scene, so the `Access-Control-Allow-Origin` header on `.excalidraw` is now a belt rather than the braces it was.

#### P2. The per-frame anchor has to come from our side
(`?element=` is Excalidraw+; the open-source app does not read it)
Grepping the app's own bundle, the query string it reads is `id`, `resourcekey`, `start`, `t`, and nothing else.
So `serve.py` computes the projection instead: one file on disk, two kinds of URL off it.

```
 the whole board, for drawing
   127.0.0.1:5599/_excalidraw/#url=http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw

 one page's frame, for its Diagram
   127.0.0.1:5599/_excalidraw/#url=http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw?frame=QA4a

 same file · the second returns that frame and its children only
 an unknown name answers with the list of real ones, never silently empty
```

#### P3. Every frame is SEEDED with the ASCII figure its page already has
(a blank frame reads as a broken feature, which is how JL found it)
JL opened `?frame=QB3` on 260726, worked through the load dialog, and landed on an empty rectangle.
The scene at that point was 28 named frames and nothing inside them, so the feature looked broken while working exactly as built.
`xcal.py` now writes each page's first `## Diagram` fenced block into its frame as one monospace text element, so opening any frame shows the figure that page already argues with, and the frame is sized to it rather than to a fixed grid.
It is a ONE-WAY seed and the markdown stays the truth: the ASCII figure is the half that survives being copied, which is `QA4 §2`'s rule and is not weakened by also being drawable.
Three pages seed a grey placeholder instead, because they have no ASCII figure at all, and that placeholder is the most honest thing the frame can say.

#### P4. Regenerating is safe, which is what makes it usable
(stable ids, kept positions, kept drawings, dropped ghosts)
Every element `xcal.py` mints carries a prefixed id (`frame-QA4a`, `t-QA4a-fig`), so a regen renames nothing and no page's link dies.
An element with any other id is a human's drawing and is carried through untouched, and a frame that already exists keeps the x/y a human moved it to.
A frame whose page has been retired is dropped rather than kept, since a prefixed id that matches no page is a ghost and not a drawing; `--fresh` is the one destructive mode and is never the default.
This is the acceptance bar this page set before anything was built, and it is the only reason the generator can be re-run at all.

#### P5. The loop is closed by taking over the browser's own storage
(`#url=` is gone; the editor is seeded from the file and writes back to it)
The app has no save-to-a-server, and both of its failures came from one place: it loads from `#url=` and saves to `localStorage`.
So `serve.py` injects a script into the app it already proxies, and that script owns the storage instead.
On load it fetches the scene and seeds it, which means there is no external drawing to confirm and the "Replace my content" dialog never appears.
While editing it watches the same key and POSTs changes to `/_board/excalidraw-save`, which merges them into the file.
A page's URL is now `?board=<scene>&frame=<page>` rather than `#url=…`, and the boot script is the only thing that reads it.

#### P6. An embed reads, a tab writes, and that split is forced by the browser
(28 iframes on one page share one origin, so an editable embed would be 28 editors fighting over one key)
Every page's Diagram is an iframe of the same app on the same origin, so if each one persisted, each would overwrite the others and then read somebody else's drawing back as its own.
An embed therefore gets an IN-MEMORY storage: it renders the frame, pans and zooms, and persists nothing.
Editing happens in the tab that "✏️ Edit this frame" opens, and a lock in real storage keeps that to one tab at a time; a second tab silently drops to read-only and says so.
The app refuses to restore `viewModeEnabled` from storage, which is the obvious way to do this and does not work; it does restore `activeTool` and `zenModeEnabled`, so a locked hand tool and zen mode do the job better, because panning survives.

#### P7. A frame saves its own slice, which is what makes one file safe to share
(`/_board/excalidraw-save` merges; it does not overwrite)
Editing QB3 replaces the elements whose `frameId` is QB3's and leaves the other 27 frames byte-identical, verified by comparing every other slice before and after.
The frame's id and name are forced back on save, because the name IS the page's link and an editor rename would break that page.
Deleting the frame puts it back rather than losing the page's anchor, deleted elements are dropped rather than accumulating, and the write is atomic through a temp file.
Editing the whole board, with no `frame=`, replaces everything, because that edit was made with everything on screen.

### §2 What we own either way
#### P1. The scene is just JSON, and we own the ids
(so a frame can be named for the page it belongs to, and stay named)
`.excalidraw` is an open format, and `diagram-ascii-canvas/bin/txt_to_canvas_lib.py` already writes it with `frameId`, so a board-shaped excalidraw is a generator away rather than a product away.
Element ids are strings we choose, which is the part that makes any of this automatable: a frame can carry the page id itself, so `?element=QA4` is predictable instead of discovered.
The board already holds everything the layout needs, because `## Pages` gives the groups and the order and `## Pipeline` gives the arrows.

#### P2. What a generated excalidraw would be FOR
(not prettier figures; the relationships a single page cannot hold)
A per-page excalidraw can only ever say something about that page.
One surface can say QA6 feeds QA8, that QD is the live layer, that QE6 is the local half of QE1, and it can say it by position and arrow rather than by prose.
That is the job `## Pipeline` does badly today, in ASCII, and it is the only argument for this feature that a per-page excalidraw does not already satisfy.

### §3 The routes not taken
#### P3. Excalidraw+ publishes an API, and this repo did not know
(checked against their docs on 260726, after this page first said the opposite)
`plus.excalidraw.com/docs/api` documents a key created in workspace settings and sent as a bearer token, with endpoints for Scenes, Scene Content, Collections, Logs, Users and Workspace.
Scenes can be created, their metadata patched, and their content replaced outright, and the list endpoint returns scenes "with their metadata and associated links".
Frames are not mentioned, which does not block anything: a frame is an element, so it arrives with the content we replace, and the id is ours to choose.
It is a paid tier and marked public beta with breaking changes expected, and both of those are the real cost rather than the engineering.

#### P4. This repo's own attempt predates or ignores it
(the Playwright script is evidence about us, not about Excalidraw)
`share-via-excalidraw.py` drives a browser: drag-drop, button hunting, screenshots to a debug folder.
I read that first and told JL an API probably did not exist, which was wrong, and the lesson is the one this board keeps relearning: a local artifact is evidence of what someone tried, never of what is available.

#### P5. We can also host it ourselves, and JL is right that the plugins already do
(the file is the thing; both editors open it with no server at all)
The VS Code Excalidraw extension and the Obsidian Excalidraw plugin both open and edit `.excalidraw` in place, so a drawing committed beside the board is fully editable with no account, no key and no network.
What that route does not give is a URL, and therefore no `?element=` deep link, so a page would have to render the drawing rather than link to it.
Rendering it ourselves means exporting to SVG at build time and inlining the result, which is the same shape as every other rule on this board: an inlined SVG survives being copied, works offline, and needs nothing from anyone, exactly as `QA4 §2` requires of the ASCII figure.
The catch is the exporter, since Excalidraw's own is JavaScript and a hand-rolled one would render only the subset we generate, not what a human later draws by hand.

### §4 Where identity has to live
#### P5. One scene id in board.md, one anchor per page
(so a re-share costs one line instead of twenty-seven)
The scene half of the URL is minted by the share and is the same for every frame; the element half belongs to the page.
Declaring the scene once in `## Links` and composing the anchor at build time means a re-share edits one line, and a page that has no frame yet simply has no link rather than a broken one.
Storing the whole URL per page is the version that breaks all at once, and this board has now watched that exact failure three times in one afternoon.

## Items to Finish
- [x] 🔎 Find out whether a public Excalidraw API exists at all
      It does. Excalidraw+ documents a bearer-key API with scene create and full content replace, checked 260726.
      This page said the opposite for its first hour, on the strength of a Playwright script in this repo.
- [x] 🧠 JL ruled the route: our own Excalidraw, run locally
      JL asked to try the localhost version first on 260726, then used it and asked for it on every page, which is the ruling in practice.
      It takes the fourth route rather than any of the three this page opened with: the file is the truth, the editor is the open-source app in a container, and the per-frame anchor is computed by `serve.py` instead of bought.
      No key, no subscription, no vendored bundle, and no SVG exporter.
- [x] 🖼 A board-shaped scene is generated, one frame per page
      `xcal.py` builds `fig/board.excalidraw` from `board.md`: frames named for the pages, one row per `## Pages` group with the group's name above it, each frame sized to the figure it holds.
      It is its own script rather than part of `build.py` because `build.py` runs on every file save and a scene regen must not.
      Stable prefixed ids were the acceptance bar and they hold: two consecutive runs produce the same file.
- [x] 🧹 A retired or renamed page does not leave a dead frame
      A prefixed id that matches no page is a ghost, so it is dropped; an unprefixed id is a human's drawing, so it is kept.
      Verified 260726 by injecting a `frame-QF2` and a hand-shaped rectangle into the scene and regenerating: the ghost went, the rectangle stayed.
- [x] 🌱 A frame opens onto something rather than onto a blank box
      Each frame carries its page's `## Diagram` ASCII figure as a monospace text element, seeded one way from the markdown.
      25 of 28 pages have a figure to seed; the other three get a grey placeholder saying so.
- [ ] 🔗 The URL is composed rather than stored, or the storing is made cheap
      Today the whole URL sits on each page and `xcal.py --wire` rewrites all 28 in one command, which answers the RISK (a change is one command) without answering the QUESTION (the page still stores something it did not decide).
      `board.md` declares the host once, on its `excalidraw:` line, so only the path and the frame name are duplicated.
      This closes when either the anchor is composed at build time from the host plus the page id, or JL rules that a rewritable duplicate is the right trade.
- [x] 🔁 A drawing made in the browser returns to `fig/board.excalidraw`
      `serve.py` injects `assets/xcal-boot.js` into the app it proxies; the script seeds the editor from the file and POSTs changes to `/_board/excalidraw-save`, which merges that frame's slice.
      Verified server-side on 260726 by drawing into QB3 over HTTP: the element landed, it was adopted by the frame, all 27 other frames stayed byte-identical, and both an unknown frame name and a path outside `--root` were refused.
      Verified client-side against a stubbed browser (22 assertions): an embed leaves real storage untouched, the editing tab seeds and saves, a deleted element is stripped, an idle tick posts nothing, and a second editing tab is refused the pen.
      NOT yet verified in a real browser, because no browser was reachable from this session.
- [x] 🚪 Opening another page stops destroying what you drew
      The "Replace my content" dialog came from `#url=`, which is now gone: the URL is `?board=&frame=` and the boot script seeds storage directly, so there is no external scene to confirm against.
      An embed persists nothing at all, so 28 iframes on one origin can no longer overwrite each other.
- [ ] 🖼 An image pasted into the scene survives
      Excalidraw keeps images in a `files` map beside the elements, and the save endpoint writes `elements` only.
      So a pasted image renders while the tab is open and is gone on reload, which is worse than refusing it.
      This closes when `files` round-trips too, or when the endpoint says plainly that it does not.
- [ ] 🌱 A regen does not quietly revert what someone drew over a seed
      The seeded ASCII text is a generated element, so `xcal.py` rewrites it; editing that text in Excalidraw and then regenerating loses the edit.
      Drawings around it are safe (unprefixed ids are kept) and this only touches the seed itself.
      This closes when the seed is either locked in the editor or the rule is written where someone about to edit it will read it.
- [ ] 📄 A copied `board.html` still shows something where the excalidraw is
      The iframe needs `serve.py` and the container, so a page mailed to someone renders an empty box in place of the drawing.
      The ASCII figure in `## Diagram` is the standing answer (`QA4 §2`), and the seed means the same figure is now in both places, so this may close by rule rather than by code.
- [ ] 💳 Whether the Plus route stays open at all
      It is documented on this page and costs a subscription plus a public-beta dependency, and nothing on the local route needs it.
      This closes when JL either parks it explicitly or names what would make it worth buying.
- [ ] 🧪 One real board is drawn this way and read by someone else
      An excalidraw nobody opens is a prettier version of the problem.
      Nothing has been drawn yet: all 89 elements in the scene are generated.

## Where we are
The arrow now points both ways: one scene, 28 frames, every page reading its own frame and any page able to edit it, with what you draw landing in `fig/board.excalidraw`.
The route is settled and it is the cheapest of the four: no key, no subscription, no exporter.
What is left is not the loop but its edges: images do not round-trip, a regen still overwrites the seeded text, and none of it has been exercised in a real browser yet, only against a stub.

- 260726 JL · 🔁 Editing saved nothing, and switching pages destroyed it
      JL drew on a frame, found the change did not persist, and then found that opening another page offered to overwrite the drawing.
      Both came from one place: the app loads from `#url=` and saves to the browser, so the file was never in the loop at either end.
      Closed by injecting a boot script into the proxied app: it seeds the editor from the file, so no dialog, and posts changes back, so the file is the truth.
      JL also named the property this has to have, which is that the excalidraw is shared by every page of the board; the merge is what delivers it, because a page saves only its own slice.
- 260726 CC · 🚧 The browser forced the read/write split
      The first design had every embed editable, which cannot work: a board carries one iframe per page, they share an origin, and they would have overwritten each other's storage and then read it back as their own.
      So an embed persists nothing (in-memory storage), the ✏️ tab is the only writer, and a lock keeps it to one tab.
      The intended way to say "read-only" is `viewModeEnabled` and the app refuses to restore it, which was found by reading its own per-key table; `activeTool` and `zenModeEnabled` do restore, and a locked hand tool is better anyway because it still pans.
- 260726 CC · 🌱 Frames were empty, so the feature looked broken while working
      JL opened `?frame=QB3`, got past the load dialog, and found a blank rectangle.
      The scene was 28 named frames with nothing inside, which is what had been built and not what anyone would call done.
      `xcal.py` now seeds each frame with its page's ASCII figure, and the lesson is below.
- 260726 CC · 🧰 The generator became a script rather than a one-off
      The first scene was built by an ad-hoc script in a scratch folder, which was gone by the next session, so the second one had to be written from scratch.
      `xcal.py` is that script kept: it reads `board.md` and the pages, writes the scene, and with `--wire` puts every frame's URL in its page.
      Re-running it is now a normal thing to do, which is what the stable ids and the keep rules were for.
- 260726 CC · 🩹 One bad regex damaged 28 pages, and the fix is in the script
      `^\s*<url>\s*$` looks line-anchored and is not: `\s` spans newlines, so the match ate the blank lines around the URL and, with an off-by-one, the `#` of the heading below it.
      Three pages came out with `## Diagramhttp://…` welded together and one grew a second `## Diagram`.
      All four were repaired by hand; the script now rebuilds the section instead of splicing into it, and warns rather than writes when a page has two `## Diagram` headings.
- 260726 JL · 💡 Opened from the idea of an Excalidraw key in env.sh, and JL was right
  JL asked whether an API key in `env.sh` would let one excalidraw be created per board, with a frame per page and the frame link dropped into each Diagram.
  I answered that an API probably did not exist, reasoning from `share-via-excalidraw.py`, and then checked: Excalidraw+ publishes exactly that API.
  JL then asked whether the VS Code and Obsidian plugins mean we could host it ourselves, which is the second real route and needs no key at all.
  So the page changed from "is this possible" to "which of three routes", and `QE6` still owns where the credential would live if the paid one is chosen.

## Files
- `../../0_utils/haipipe-board/assets/xcal-boot.js`
  Injected into the proxied editor. Owns the storage: seeds it from the file, writes it back, and keeps an embed from persisting anything.
- `../../0_utils/haipipe-board/xcal.py`
  Builds the scene and wires the pages. Everything this page settled is implemented here; start here.
- `../../0_utils/haipipe-board/serve.py`
  Holds `serve_frame()` (the `?frame=` projection), `save_excalidraw()` (the merge back), and `proxy_excalidraw()` (the container behind the one forwarded port, and the script injection).
- `fig/board.excalidraw`
  The scene itself, one file, committed. 28 frames, all of them generated so far.
- `board.md`
  Declares the editor host once, on its `excalidraw:` line.
- `../../0_utils/diagram-ascii-canvas/bin/txt_to_canvas_lib.py`
  Already wrote `.excalidraw` JSON with frames before any of this. Read it before writing a second emitter.
- `../../0_utils/diagram-ascii-canvas/bin/share-via-excalidraw.py`
  The existing attempt at the hosted half, by Playwright. Read it before proposing an API.

## Glossary
frame: an Excalidraw container with a name; on the hosted app it is addressable by `?element=<its id>`, and here by `serve.py`'s `?frame=<name>`.
scene: one Excalidraw document. On Excalidraw+ it is `…/s/<scene>/<key>` and a re-share mints a new one; here it is `fig/board.excalidraw`, one file, and a regen mints nothing.
seed: the one-way copy of a page's ASCII figure into its frame. The markdown stays the truth, so a seed is never read back.

## Lesson
A frame with a name and nothing in it is indistinguishable, to the person opening it, from a feature that does not work.
The scaffold and the content are two different deliverables and only the second one is visible, so shipping the first and reporting it as done puts the reader in front of a blank box with no way to tell which of the two they are looking at.
Excalidraw's `#url=` loader always asks before overwriting, and its confirm button is called "Replace my content" rather than anything with "load" in it, so a reader who is looking for "Load" reads the three backup offers as the whole dialog and stops.
`^\s*…\s*$` is not a line anchor: `\s` matches newlines, so a pattern that looks like it selects one line selects the blank lines around it too, and a splice built on `hit.end()` then eats the first character of whatever came next.
When a script edits a section, rebuilding the section from its parts is safe in a way that splicing into it is not, because rebuilding is idempotent by construction and a splice is only ever as correct as its offsets.

## Discussion
> JL: I want to add env.sh with an excalidraw api, if we have the excalidraw API, could we create an excalidraw board for this board only, and for each Q, we can create the frame and give the frame link to in the diagram section, how do you think?
>> CC0726: the drawing half is generable today and the id design is the interesting part; the hosted half is the unknown, and this repo's own `share-via-excalidraw.py` uses a browser rather than an API, which is what I would check before adding a key to `env.sh`.
> JL: It is not QA4.excalidraw, it will only be a board.excalidraw, and QA4a will only be one frame element within it, do you get what I mean here?
>> CC0726: took two corrections to land. The scene is one file and a page's Diagram is a projection of it, which is now `serve_frame()` and is the reason `xcal.py` refuses to emit a file per page.
> JL: why I didn't see the content here?
>> CC0726: two causes, and only the second was ours. The dialog's confirm is called "Replace my content", and the frame behind it held nothing, because 28 named empty frames was the whole scene. Frames are seeded from the pages' ASCII figures as of this entry.

## Log
260726 · CLOSED THE LOOP (JL: "when I edit the excalidraw, the changes won't save ... what I added will be gone"): `assets/xcal-boot.js` injected into the proxied app takes over the browser's storage, `#url=` replaced by `?board=&frame=`, `/_board/excalidraw-save` merges one frame's slice, an embed persists nothing and the ✏️ tab holds a lock; images and the seed-overwrite are the two edges left
260726 · SEEDED and made re-runnable: `xcal.py` added (scene from `board.md`, `--wire` for the URLs, `--fresh` for a relayout), each frame now carries its page's ASCII figure, retired frames are dropped and human drawings kept, 28 pages wired; one bad regex damaged 4 pages on the way and the repair is in the script
260726 · BUILT the local route end to end: excalidraw in a container, proxied at `/_excalidraw/` so it rides the one forwarded port, `serve_frame()` projecting `?frame=<page>` out of one scene, and `board.md` declaring the host once
260726 · checked Excalidraw+'s API docs and corrected this page: the API exists (bearer key, scene create, content replace, public beta), the Playwright script was evidence about us rather than about them, and the self-hosted route via the VS Code/Obsidian plugins was added as the third option
260726 · opened from JL's idea; scoped to one excalidraw per board with a frame per page, with the identity rule (`scene once, anchor per page`) written down before anything is built
