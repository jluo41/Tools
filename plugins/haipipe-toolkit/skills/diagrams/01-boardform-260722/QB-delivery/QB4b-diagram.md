# Page Diagram: the figure, and the board canvas

state: 🟡 PARTIAL
owner: JL
method: settle what can be generated before deciding what to pay for; the hosted half turned out to be a container we run ourselves
session: d446a3be-4cd7-40c2-a680-0c76a82e394b

## Question
Can a board own ONE excalidraw, carrying a frame per page, with each page's Diagram opening at its own frame?
Yes, and it is running: one scene in the repo, one frame per page, an open-source editor in a container reached through the one port that is forwarded, and what you draw is written back to the file.
What is still a question is the edges of that: regenerating overwrites the seeded figure, and a deleted image leaves its file behind.

Before this, an excalidraw was pasted per page, one at a time, by a human who drew it somewhere else.
That works and it loses the thing a board most wants from a drawing, which is the relationships BETWEEN pages: the Pipeline ASCII in `board.md` is exactly that attempt, made in a medium that cannot show a link.
One excalidraw with a frame per page puts every page on one surface, so moving a box is a statement about the board rather than about one question.
The thing that would have made this fragile is identity, since a hosted deep link is `…/s/<scene>/<key>?element=<id>` and a re-share kills all 28 at once; owning the file removes that failure entirely, which is most of why the local route won.


## Boundary
- ✅ Covered here
  The `## Diagram` section itself (the ▧ ASCII over ✏️ Excalidraw ranking, the ascii-survives-copy rule, the one-URL-alone-on-a-line embed), and the board canvas: whether one excalidraw per board is generated or hand-made, how a page names its frame, where the scene identity lives, and what a re-share costs.
- ↪ Covered elsewhere
  Attaching a single excalidraw to one page by hand, from the page, is `QD5`.
  Where a secret would live if one were needed is `QE6`.
  The fixed on-stage order the Diagram section sits in: `QAa0`.

## Diagram

```
 WHAT IS BUILT · one file, two URLs off it, nothing bought
 ═══════════════════════════════════════════════════════════════════════

   board.md            ## Pages -> the groups, the order
   QA4a-*.md  ×28      ## Diagram's first ``` block -> this frame's seed
        │
        │  xcal.py                 (re-runnable: stable ids, keeps a human's
        ▼                           drawing and position, drops dead frames)
   board.excalidraw            ONE scene · 40 frames · 127 elements
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
   truth       board.excalidraw, committed, diffed, reviewed
   page shows  inline SVG, exported at build time
   deep link   none. there is no URL, so nothing to anchor into
   needs       an SVG exporter we do not have yet
   costs       nothing. no account, no key, no network, ever
   survives    copy · offline · git history · anyone with the folder
   breaks      a human draws freehand and our renderer cannot draw it back

 ② PLUS API · they host it, we drive it
   edit in     excalidraw.com, in a Plus workspace
   truth       their scene; our file becomes a copy
   page shows  iframe + fallback link, which is what QD5 already renders
   deep link   ?element=<frameId>, and the ids are OURS because we PUT
               the content, so a frame can simply be called QA4
   needs       Plus subscription · API key in env.sh (QE6) · network
   costs       paid tier, public beta, breaking changes expected
   survives    nothing offline. no network is an empty box
   breaks      the beta moves, or the subscription lapses, and every
               page's Diagram goes blank at once

 ③ FILE IS TRUTH, SCENE IS A PROJECTION
   edit in     either; the file is what gets committed
   truth       board.excalidraw, exactly as in ①
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
   truth       board.excalidraw, exactly as in ①
   page shows  an iframe of our own editor, opened at this page's frame
   deep link   yes, and computed by serve.py rather than bought
   needs       docker, and serve.py already running
   costs       nothing. ① 's price with ② 's deep link
   survives    git history, offline, anyone with the folder AND docker
   breaks      a copied board.html has no server, so the iframe is empty;
               the ASCII figure is why the page still reads (§0)

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

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QAa2

## Content
### §0 The Diagram section itself
Diagram gives one visual account of the flow, comparison, before/after, or option set.
Its heading remains visible, but the figure starts hidden so a large drawing does not dominate the page before it is wanted.
Keep it only when opening it replaces or clarifies prose; decoration does not earn a section.
Under the base/variant model on `QAa0`, this section is frame: it renders identically for every page kind, and no variant may restructure it.

#### The section holds two subsections, and they are not equals
(JL 260726: ▧ ASCII opens with the section, ✏️ Excalidraw takes one more click)
Opening 🖼 Diagram shows the ASCII figure immediately, because that is the thing a reader came for and the thing that survives leaving the page.
The Excalidraw canvas sits behind its own shut row, because it is heavy, it is a place to draw together rather than a thing to read, and it is not what most readers want.
A shut `<details>` never displays its contents, so the canvas's `loading="lazy"` iframe does not load until somebody asks for it, and a board carrying twenty-eight canvases stopped booting twenty-eight of them on open.
The ranking is the whole point: the two are not peers, so giving them equal weight would have been the wrong drawing of the same content.
The SOURCE keeps one plain `## Diagram`, and the split is a render decision.
Not one of the thirty pages had to be rewritten, and a page that later gains a canvas splits itself, which is the same bargain the board already makes with `![[...]]` and the bare URL line: the markdown stays something a person types and the renderer does the arranging.
The canvas row is emitted even when no canvas exists, reading "No canvas attached yet", because it is where the 🖌 attach button lives and an affordance with no home cannot be found.

#### The ASCII figure is what the section owes
(the part that must be there, because it is the part that survives leaving the page)
An ASCII figure has to survive being copied, because copying a page into chat or an email is a thing the board exists for.
Two trees drawn side by side do not: the column boundary is whitespace, it vanishes on paste, and the right column's rows land inside the left column's branches, so the figure asserts a structure that does not exist.
Stack them instead, one complete tree at a time; columns are safe only for short parallel lists where a wrong reading is obvious at a glance.

#### An excalidraw is optional, and empty is the default
(nothing to write until a figure is worth drawing on together; then it is one line)
A Diagram section with only an ASCII figure is complete, and most pages should stay that way.
When a figure is worth drawing on together, put an Excalidraw share URL on a line of its own inside `## Diagram`, below the ASCII, with nothing else on that line.
A line matching `excalidraw.com/…` and nothing else becomes a `div.xcal`: a lazily loaded iframe at 440px, growing to 520px when the page is opened alone, with an `↗ Open in Excalidraw` link directly underneath.
Anything else on the line, a caption or a bullet marker, leaves it as ordinary prose with a plain link, so the rule is one URL, one line, no decoration.
The hosted embed works only because excalidraw.com sends no `X-Frame-Options` or `frame-ancestors`, which was measured rather than assumed; offline or after they change headers, the link underneath is the only thing that still reaches the drawing.
The ASCII figure stays for the same reason and is never replaced by the excalidraw: it is the version that survives a paste into chat, a printed page, and a reader with no network.

#### The source stays ONE `## Diagram`
Write one useful ASCII figure and, optionally, one Excalidraw share link under `## Diagram`.
QA4 renders the section between Opening and Content with the body hidden until clicked.
Delete the whole source section when the visual adds no understanding.

Write ONE `## Diagram` section, not two.
The renderer splits it into `▧ ASCII`, which opens with the section, and `✏️ Excalidraw`, which takes one more click (QA4 §2, JL 260726).
The rule that decides the halves is the one already governing the body: a bare Excalidraw URL alone on its own line is the canvas, and every other line is the figure.
So do not add `### ASCII` or `### Excalidraw` headings here; a `###` inside `## Diagram` is not a recognized construct and would render as ordinary prose inside the figure half.
Put the URL below the figure with nothing else on the line, exactly as before, and a URL written inside a fence stays in the figure where it was drawn.

### §1 The route: our own Excalidraw, on localhost
Proved 260726. It removes the API key, the subscription, the vendored bundle and the SVG exporter at once.

#### P0. One excalidraw for the board, one FRAME per page
(JL 260726, and the single scene is the point rather than a packaging detail)
`board.excalidraw` is one file holding one frame per page, named for the page: `QAa2`, `QD5`, `QAb1`.
It is never split into a file per page, because a single surface is the only thing that can say how the pages RELATE, which is the job `## Pipeline` does badly in ASCII and the only argument for drawing at all.
Editing happens on the whole board; a page's Diagram opens at its own frame.

#### P0b. The scene lives at the board ROOT, as a first-class citizen
(JL 260729: "we will put the excalidraw at the root, as the 1st level citizen")
`board.excalidraw` sits beside `board.md` and `board.html`, and `fig/` goes back to holding images only.
The reason it is a decision rather than a preference is what the three root files are: the source you write, the page you read, and the surface you draw on, which are the board's three projections of one topic. A figure folder is where a page's assets go, and the scene is not one page's asset.
It was found as a defect the same day, which is how the question surfaced at all: the scene had been sitting at the root since 260729 1211 while `xcal.py` still wrote to `fig/`, so 35 faces carried a `## Diagram` URL that returned 404 and no page's canvas opened.
`xcal.py` now writes the root path and falls back to an existing `fig/` scene where a board already keeps one, because migrating another board's scene is that board owner's call under `QB1` §4.

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
   127.0.0.1:5599/_excalidraw/#url=http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw

 one page's frame, for its Diagram
   127.0.0.1:5599/_excalidraw/#url=http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw?frame=QA4a

 same file · the second returns that frame and its children only
 an unknown name answers with the list of real ones, never silently empty
```

#### P3. Every frame is SEEDED with the ASCII figure its page already has
(a blank frame reads as a broken feature, which is how JL found it)
JL opened `?frame=QC4` on 260726, worked through the load dialog, and landed on an empty rectangle.
The scene at that point was 28 named frames and nothing inside them, so the feature looked broken while working exactly as built.
`xcal.py` now writes each page's first `## Diagram` fenced block into its frame as one monospace text element, so opening any frame shows the figure that page already argues with, and the frame is sized to it rather than to a fixed grid.
It is a ONE-WAY seed and the markdown stays the truth: the ASCII figure is the half that survives being copied, which is §0's rule and is not weakened by also being drawable.
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

#### P7. An image is a file on disk, not base64 in the scene
(`fig/assets/<fileId>.png`, with a pointer in the scene; JL 260726)
Excalidraw stores a pasted image as a base64 dataURL inside the document, which is the one thing a version-controlled scene cannot afford: a single screenshot is megabytes that git re-diffs every time anyone moves a box.
So the save endpoint decodes the bytes into `fig/assets/` and leaves `{"id", "mimeType", "path"}` behind, and the read endpoint turns the pointer back into a dataURL for whichever elements it is returning.
Fetched through `serve.py` the scene is therefore self-contained, exactly as the editor expects; read straight off disk by the VS Code or Obsidian plugin it is not, and images will show as missing there.
That is the cost of the split and it is worth naming, because "open the file in any Excalidraw" was one of the arguments for owning the file in the first place.

#### P8. A frame saves its own slice, which is what makes one file safe to share
(`/_board/excalidraw-save` merges; it does not overwrite)
Editing QC4 replaces the elements whose `frameId` is QC4's and leaves the other 27 frames byte-identical, verified by comparing every other slice before and after.
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
Rendering it ourselves means exporting to SVG at build time and inlining the result, which is the same shape as every other rule on this board: an inlined SVG survives being copied, works offline, and needs nothing from anyone, exactly as §0 requires of the ASCII figure.
The catch is the exporter, since Excalidraw's own is JavaScript and a hand-rolled one would render only the subset we generate, not what a human later draws by hand.

### §4 Where identity has to live
#### P5. One scene id in board.md, one anchor per page
(so a re-share costs one line instead of twenty-seven)
The scene half of the URL is minted by the share and is the same for every frame; the element half belongs to the page.
Declaring the scene once in `## Links` and composing the anchor at build time means a re-share edits one line, and a page that has no frame yet simply has no link rather than a broken one.
Storing the whole URL per page is the version that breaks all at once, and this board has now watched that exact failure three times in one afternoon.

## Items to Finish
### The route ruling, and the road not taken
- [x] 🔎 Find out whether a public Excalidraw API exists at all
      It does. Excalidraw+ documents a bearer-key API with scene create and full content replace, checked 260726.
      This page said the opposite for its first hour, on the strength of a Playwright script in this repo.
- [x] 🧠 JL ruled the route: our own Excalidraw, run locally
      JL asked to try the localhost version first on 260726, then used it and asked for it on every page, which is the ruling in practice.
      It takes the fourth route rather than any of the three this page opened with: the file is the truth, the editor is the open-source app in a container, and the per-frame anchor is computed by `serve.py` instead of bought.
      No key, no subscription, no vendored bundle, and no SVG exporter.
- [ ] 💳 Whether the Plus route stays open at all
      It is documented on this page and costs a subscription plus a public-beta dependency, and nothing on the local route needs it.
      This closes when JL either parks it explicitly or names what would make it worth buying.

### The generated scene, and what a regen must keep
- [x] 📍 The scene's home is decided: the board root, not `fig/`
      JL 260729: "we will put the excalidraw at the root, as the 1st level citizen."
      `xcal.py` writes `<board>/board.excalidraw` and falls back to an existing `fig/board.excalidraw` where a board already keeps one, so the two other boards holding a scene keep working and neither forks in two.
      All 35 stale `## Diagram` URLs on this board were repointed the same round, and both the scene and a `?frame=` projection were verified to return 200.
- [ ] 🧭 The regenerated scene is laid out again without losing what a human drew
      The 260729 regen produced 40 frames and reported 21 overlapping pairs: kept human positions collided with widths recomputed for the restructured pages.
      `--fresh` fixes the layout and drops the 2 elements a human owns, so it was not run.
      This closes when those 2 elements are identified and preserved, or JL says they are expendable.
- [x] 🖼 A board-shaped scene is generated, one frame per page
      `xcal.py` builds `board.excalidraw` from `board.md`: frames named for the pages, one row per `## Pages` group with the group's name above it, each frame sized to the figure it holds.
      It is its own script rather than part of `build.py` because `build.py` runs on every file save and a scene regen must not.
      Stable prefixed ids were the acceptance bar and they hold: two consecutive runs produce the same file.
- [x] 🧹 A retired or renamed page does not leave a dead frame
      A prefixed id that matches no page is a ghost, so it is dropped; an unprefixed id is a human's drawing, so it is kept.
      Verified 260726 by injecting a `frame-QF2` and a hand-shaped rectangle into the scene and regenerating: the ghost went, the rectangle stayed.
- [x] 🌱 A frame opens onto something rather than onto a blank box
      Each frame carries its page's `## Diagram` ASCII figure as a monospace text element, seeded one way from the markdown.
      25 of 28 pages have a figure to seed; the other three get a grey placeholder saying so.
- [ ] 🌱 A regen does not quietly revert what someone drew over a seed
      The seeded ASCII text is a generated element, so `xcal.py` rewrites it; editing that text in Excalidraw and then regenerating loses the edit.
      Drawings around it are safe (unprefixed ids are kept) and this only touches the seed itself.
      This closes when the seed is either locked in the editor or the rule is written where someone about to edit it will read it.

### Drawing in the browser, and the write-back
- [x] 🔁 A drawing made in the browser returns to `board.excalidraw`
      `serve.py` injects `assets/xcal-boot.js` into the app it proxies; the script seeds the editor from the file and POSTs changes to `/_board/excalidraw-save`, which merges that frame's slice.
      Verified server-side on 260726 by drawing into QC4 over HTTP: the element landed, it was adopted by the frame, all 27 other frames stayed byte-identical, and both an unknown frame name and a path outside `--root` were refused.
      Verified client-side against a stubbed browser (38 assertions): an embed leaves real storage untouched, the editing tab seeds and saves, a deleted element is stripped, an idle tick posts nothing, and a second editing tab is refused the pen.
      Then verified in a REAL browser, which is the only test that counted: headless Chrome driven over the DevTools protocol opened the frame, pressed `r`, dragged a rectangle, and the rectangle arrived in `board.excalidraw` inside `frame-QB3` with the other 88 elements untouched.
- [x] 🚪 Opening another page stops destroying what you drew
      The "Replace my content" dialog came from `#url=`, which is now gone: the URL is `?board=&frame=` and the boot script seeds storage directly, so there is no external scene to confirm against.
      An embed persists nothing at all, so 28 iframes on one origin can no longer overwrite each other.
- [x] 🖼 An image pasted into the scene survives
      The bytes go to `fig/assets/<fileId>.<ext>` and the scene keeps a pointer, on JL's suggestion of a folder for them (260726).
      Inline was the alternative and it is what Excalidraw itself does: one screenshot is megabytes of base64 that git then re-diffs on every stroke, so the sidecar is the version a repo can live with.
      The server rehydrates on the way out, so the editor still receives the dataURL it expects and the split is invisible to it.
      Images are also read from and written to IndexedDB rather than localStorage, which is where Excalidraw actually keeps them, and that being async is why the app's own script is now held until the seed lands.
      Verified over HTTP: a PNG saved, landed on disk byte-identical, left no base64 in the scene, and came back byte-identical through both the frame and the whole-scene URL.
- [ ] 🧹 A deleted image does not leave its bytes behind
      `fig/assets/` is only ever written to: removing the image element drops it from the scene and leaves the file on disk.
      Deleting it automatically is the wrong default, because an undo would then have nothing to come back to.
      This closes when there is a way to sweep the unreferenced ones deliberately, or the rule is written where it will be read.
- [x] 🔇 Opening a page to look at it does not dirty the repo
      Excalidraw rewrites `version`, `versionNonce`, `updated` and `boundElements` on everything it loads, so the first build saved the file one second after the editor opened, with nothing drawn.
      The tab now compares CONTENT rather than raw JSON, and `xcal.py` keeps an element the browser has enriched rather than writing its plainer version back.
      Without the second half the two would have dirtied the file in turn forever, each undoing the other.
      Measured, not assumed: opening the editor twice in a row leaves the file byte-identical the second time, and two `xcal.py` runs in a row do too.

### Identity, links, and copies that leave the repo
- [ ] 🗂 The two boards still keeping a scene under `fig/` are told, not moved
      `01-haipipe-paper-260725` and the MISQ paper's `0-lifecycle/` each hold a `fig/board.excalidraw`.
      Under `QB1` §4 moving another board's file is that owner's decision, so this closes with a report to each, not a `git mv`.
- [ ] 🔗 The URL is composed rather than stored, or the storing is made cheap
      Today the whole URL sits on each page and `xcal.py --wire` rewrites all 28 in one command, which answers the RISK (a change is one command) without answering the QUESTION (the page still stores something it did not decide).
      `board.md` declares the host once, on its `excalidraw:` line, so only the path and the frame name are duplicated.
      This closes when either the anchor is composed at build time from the host plus the page id, or JL rules that a rewritable duplicate is the right trade.
- [ ] 📄 A copied `board.html` still shows something where the excalidraw is
      The iframe needs `serve.py` and the container, so a page mailed to someone renders an empty box in place of the drawing.
      The ASCII figure in `## Diagram` is the standing answer (§0), and the seed means the same figure is now in both places, so this may close by rule rather than by code.

### The proof of use
- [ ] 🧪 One real board is drawn this way and read by someone else
      An excalidraw nobody opens is a prettier version of the problem.
      Nothing has been drawn yet: all 89 elements in the scene are generated.

## Where we are
The arrow now points both ways: one scene, 40 frames, every page reading its own frame and any page able to edit it, with what you draw landing in `board.excalidraw`.
The route is settled and it is the cheapest of the four: no key, no subscription, no exporter.
Images round-trip too, as files in `fig/assets/` with a pointer in the scene, and the whole thing has now been driven by a real browser rather than argued about: headless Chrome drew a rectangle and it landed in the file.
What is left is smaller: a regen still overwrites the seeded ASCII text, and an image whose element is deleted leaves its file behind.

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
      JL opened `?frame=QC4`, got past the load dialog, and found a blank rectangle.
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

### Decision Now
- [ ] 🧭 Say whether the 2 human-drawn elements are expendable
      The options the Items row records: identify and preserve the 2 elements a human owns before a relayout, or rule them expendable so `--fresh` can fix the 21 overlapping pairs.
- [ ] 🔗 Rule the URL trade: composed at build, or stored and rewritable
      The options the Items row records: compose the anchor at build time from the host plus the page id, or accept the stored duplicate because `xcal.py --wire` rewrites all 28 in one command.
- [ ] 💳 Park the Plus route or name what would make it worth buying
      The options the Items row records: park it explicitly, or name what would make it worth buying; nothing on the local route needs it.

## Files
### Engines
- `../../board/haipipe-board/assets/xcal-boot.js`
  Injected into the proxied editor. Owns the storage: seeds it from the file, writes it back, and keeps an embed from persisting anything.
- `../../board/haipipe-board/xcal.py`
  Builds the scene and wires the pages. Everything this page settled is implemented here; start here.
- `../../board/haipipe-board/serve.py`
  Holds `serve_frame()` (the `?frame=` projection), `save_excalidraw()` (the merge back), and `proxy_excalidraw()` (the container behind the one forwarded port, and the script injection).

### The scene and its declaration
- `board.excalidraw`
  The scene itself, one file, at the board root since 260729. 40 frames, of which 2 elements are a human's and the rest are generated.
- `board.md`
  Declares the editor host once, on its `excalidraw:` line.

### Prior art to read first
- `../../0_utils/diagram-ascii-canvas/bin/txt_to_canvas_lib.py`
  Already wrote `.excalidraw` JSON with frames before any of this. Read it before writing a second emitter.
- `../../0_utils/diagram-ascii-canvas/bin/share-via-excalidraw.py`
  The existing attempt at the hosted half, by Playwright. Read it before proposing an API.

## Glossary
frame: an Excalidraw container with a name; on the hosted app it is addressable by `?element=<its id>`, and here by `serve.py`'s `?frame=<name>`.
scene: one Excalidraw document. On Excalidraw+ it is `…/s/<scene>/<key>` and a re-share mints a new one; here it is `board.excalidraw`, one file, and a regen mints nothing.
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
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260729 · Marked frame under the base/variant model on QAa0; §0's heading simplified and the provenance parentheticals dropped from headings on JL's ask (the Log already records the merges)
260729 · Renamed QA4a -> QAa2 when the QAa page group was carved (JL), and the `## Diagram` section's own render rules moved in from the page-layout face as §0, so the section and its canvas are one subject. Older lines cite QA4/QA4a; they are history
260726 · DRIVEN BY A REAL BROWSER (JL: "will it work?"): headless Chrome over the DevTools protocol, which found two things no amount of reading would have. First, the boot script was injected BEFORE the variable it reads, so the app never started at all behind a correct-looking badge. Second, merely opening the editor rewrote the file, because Excalidraw renormalises everything it loads
260726 · IMAGES SAVED (JL: "could we make it saved? we can have assets/excalidraw folder for it"): bytes to `fig/assets/<fileId>.<ext>`, a pointer in the scene, rehydrated on read; images live in IndexedDB not localStorage, so the app's own module script is now held until that seed lands
260726 · CLOSED THE LOOP (JL: "when I edit the excalidraw, the changes won't save ... what I added will be gone"): `assets/xcal-boot.js` injected into the proxied app takes over the browser's storage, `#url=` replaced by `?board=&frame=`, `/_board/excalidraw-save` merges one frame's slice, an embed persists nothing and the ✏️ tab holds a lock; images and the seed-overwrite are the two edges left
260726 · SEEDED and made re-runnable: `xcal.py` added (scene from `board.md`, `--wire` for the URLs, `--fresh` for a relayout), each frame now carries its page's ASCII figure, retired frames are dropped and human drawings kept, 28 pages wired; one bad regex damaged 4 pages on the way and the repair is in the script
260726 · BUILT the local route end to end: excalidraw in a container, proxied at `/_excalidraw/` so it rides the one forwarded port, `serve_frame()` projecting `?frame=<page>` out of one scene, and `board.md` declaring the host once
260726 · checked Excalidraw+'s API docs and corrected this page: the API exists (bearer key, scene create, content replace, public beta), the Playwright script was evidence about us rather than about them, and the self-hosted route via the VS Code/Obsidian plugins was added as the third option
260726 · opened from JL's idea; scoped to one excalidraw per board with a frame per page, with the identity rule (`scene once, anchor per page`) written down before anything is built
