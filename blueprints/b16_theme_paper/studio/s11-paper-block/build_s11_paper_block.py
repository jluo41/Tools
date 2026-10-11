"""s11 · Block level: s11-paper-block.excalidraw, the paper Board's tab on the shared frame, its Spaces as
full screens with "on disk" under each, then Guide › Method opened from the Block tab (JL 261007: "add
the s11 s12 s13 like b11").

It draws Q01's proposal for the Board (s05-board-job-task-boundary): the Board keeps the paper's scope, venues,
related work and questions; the Ideation and the Story show in its Audience Report (on disk not Pages but
studio topics, s01-ideation/ and sNN-story-<telling>/, and Board Questions with reports: Q04, JL 261007); its Work Details are its versions, grants and slides. Placeholders only; written
through canvas.write, so every mark a person adds survives a rebuild.

    python build_s11_paper_block.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
import paper_ui as U  # noqa: E402

GRAY, RED, INK, MONO = U.GRAY, U.RED, U.INK, U.MONO
text, base, path = U.text, U.base, U.path

MOVES = [("Guide › 4 Views", "Guide tab, three sections Block · Job · Task in each View"),
         ("Ideation › (no Views)", "Audience Report › Ideation: questions (why this paper), studio/s01-ideation/ their work"),
         ("Story › Spine · RoadMap Draw · Sections › Narrative", "Audience Report › Narrative: says · drawn · told · attracts"),
         ("Story › High-level logic + Low-level work", "Audience Report › High-level logic + Low-level work: RQ │ work │ report (name kept)"),
         ("Story › RoadMap Draw", "Idea Studio: one topic per drawing (no Design view)"),
         ("Story › Related Papers", "Description › Related: paper cards, each opening on its drawing"),
         ("(none)", "Description › Venue (venues/<venue>/: call.md · kit/)"),
         ("Sections › Main · Appendix", "Work Details: the versions, each open to its Sections (s12)"),
         ("Sections › Narrative", "a version's Audience Report › Draft-Main (s12), no Board view"),
         ("(none)", "Runs: the Board's own soft Runs, by run type"),
         ("Delivery › LaTeX · Word · Cover letter · Rounds", "Delivery: each version's build, from below ? (Q02)")]

# what changed on this drawing, in green (JL 261007: "add the short green comments to where we made the changes")
CHANGES = ["each Space a row, its explanation on the right",
           "Description › Related: paper cards, one open on its drawing (was a table)",
           "Audience Report is only questions: Ideation · Narrative · High-level logic + Low-level work · Related Questions",
           "Narrative: Spine, Design and the §8 Narrative merged into N1–N4 (says · drawn · told · attracts)",
           "a Story is not a Job (was a j00_story/ Job)",
           "the Story and Ideation stop being Pages: studio/s01-ideation/ · sNN-story-<telling>/; research questions "
           "are Board Questions with reports/qNN_; §8 goes to the version face (Q04)",
           "names: versions j0N_v<MMDD>_<desk>/, Sections t0N_<title>/ (was j02_v2_<venue>, S-<desk>-Main-N-…)"]


def scope(cx, cy, cw):
    y = U.lines(cx, cy, [
        ("bNN_<topic>.md  (was board.md)", INK, MONO),
        ("paper: <one-line contribution>", INK),
        ("tells now: studio/sNN-story-<telling>/  (the G0 pick)", INK),
        ("? which Story, when the Board has several", RED),
        ("target now: <venue> · version j02_v<MMDD>_<desk> · deadline <date>", INK),
        ("state: drafting · 6 of 9 Sections written · 2 questions open", INK),
        ("", GRAY),
        ("its resources: the next tab, Resources", GRAY)])
    return U.changed(cx, y + 6, ["tells: no j00_story/ · version j02_v<MMDD>_<desk> (was j02_v2_)",
                                 "tells: a studio topic, sNN-story-<telling>/ (was a Story Page, Q04)"])


def resources(cx, cy, cw):
    y = U.table(cx, cy, cw, ["resource", "kind", "for", "link"], [0, 380, 560, 760],
                [("work/bNN_<topic>/", "work Block", "RQ1 · RQ2", "Results ↗"),
                 ("discovery/bNN_<topic>/", "discovery Block", "related work", "reads ↗"),
                 ("<data extract> (ExternalStore)", "data", "j02", "pointer ↗"),
                 ("? <code repo>", "repo", "Resources", "—")], mono=(0,))
    return U.lines(cx, y + 20, [("what the paper uses and does not own: linked, never copied", GRAY),
                                ("a number in the paper always comes from one of their hard Runs", GRAY)])


def venue(cx, cy, cw):
    return U.table(cx, cy, cw, ["venue", "call read", "deadline", "limits", "kit", "used by"],
                   [0, 170, 330, 480, 680, 820],
                   [("<venue A>", "<date> ↗", "<date>", "<n> words · 6 displays", "kit/ ✓", "j01"),
                    ("<venue B>", "<date> ↗", "<date>", "<n> pages", "kit/ ✓", "j02"),
                    ("? <venue C>", "? not read", "—", "—", "—", "—")], mono=(0,))


def paper_drawing(cx, cy, cw):
    """A paper's drawing, one template for every paper (JL 261007: drawn in its deep read, view only):
    question -> data and method -> finding -> limits. Returns the bottom."""
    base("rectangle", cx, cy, cw, 180, INK, 1, rough=0)
    text(cx + 14, cy + 10, "rNN_<author><year>_<subject>.excalidraw  ·  drawn by the read, view only  ↗ full size",
         13, GRAY)
    bw, gap, by = (cw - 28 - 3 * 34) / 4, 34, cy + 40
    for k, (head, body) in enumerate([("question", "<what it asks>"), ("data · method", "<sample>\n<design>"),
                                      ("finding", "<the result>\n<effect · CI>"), ("limits", "<where it\nstops>")]):
        x = cx + 14 + k * (bw + gap)
        base("rectangle", x, by, bw, 92, INK, 1, rough=1)
        text(x + 12, by + 10, head, 15, INK)
        text(x + 12, by + 34, body, 13, GRAY)
        if k:
            path([(x - gap + 4, by + 46), (x - 4, by + 46)], color=INK)
    text(cx + 14, by + 106, "from facts.md · abstract.md of the same Result; regenerated with it, never edited", 13, GRAY)
    return cy + 180 + 10


def related(cx, cy, cw):
    """Description › Related as paper cards (JL 261007), the Guide's paper card (b03 s31-D06), grouped by
    what each serves; one card open on its drawing, one with no deep read yet."""
    y = cy
    for group, cards in [("RQ1", [("▾", "★ <author> <year> · <title>      <venue>",
                                    "paper · why here: <why> · bears on RQ1 · read r03 ↗", "open"),
                                   ("▸", "<author> <year> · <title>      <venue>",
                                    "paper · why here: <why> · read r05 ↗", "")]),
                         ("RQ2", [("▸", "<author> <year> · <title>      <venue>",
                                   "? paper · why here: <why> · no deep read yet", "unread")]),
                         ("Resources", [("▸", "<dataset> ↗", "dataset · why here: <why> · j02", ""),
                                        ("▸", "<repo> ↗", "repo · why here: <why>", "")])]:
        text(cx, y, group, 16, INK)
        y += 30
        for mark, title, second, state in cards:
            y = U.card(cx, y, cw, title, second.lstrip("? "), red=second.startswith("?"), mark=mark)
            if state == "open":
                y = paper_drawing(cx + 34, y - 4, cw - 34)
            elif state == "unread":
                y = U.drawing_box(cx + 34, y - 4, cw - 34, 56, "no drawing yet: Read a paper opens its deep read")
        y += 8
    return U.changed(cx, y, ["paper cards grouped by RQ, one open on its drawing (was the Related Papers table)"])


def studio(cx, cy, cw):
    y = U.card(cx, cy, cw, "s01-roadmap   the Story's RoadMap Draw", "drawing · the person's · was Story › RoadMap Draw",
               mark="▾")
    y = U.drawing_box(cx + 20, y, cw - 40, 300, "[ the RoadMap drawing, live, editable ]")
    y = U.card(cx, y, cw, "s02-paper-map   the Sections of the version in view", "generated by excalidraw-section · view only")
    return U.card(cx, y, cw, "s03-<topic>", "a drawing · 1 chat")


def design(cx, cy, cw):
    y = U.card(cx, cy, cw, "<Story>.excalidraw   the Story's design", "presented, view only · its working copy is edited in Idea Studio",
               mark="▾")
    y = U.drawing_box(cx + 20, y, cw - 40, 300, "[ the Story's design: questions → claims → evidence → Sections ]")
    return U.card(cx, y, cw, "<Story>-sections.excalidraw   the paper map", "generated by excalidraw-section · view only")


def narrative(cx, cy, cw):
    y = U.table(cx, cy, cw, ["#", "Section", "claim it carries", "state"], [0, 50, 420, 760],
                [("1", "t01_introduction", "C0 the gap", "written"),
                 ("2", "t02_methods", "— (how)", "written"),
                 ("3", "t03_results", "C1 · C2", "drafting"),
                 ("4", "t04_discussion", "C2 · C3", "planned")], mono=(1,))
    return U.lines(cx, y + 20, [("the reading order = the compile order: the paper's telling, top to bottom", GRAY),
                                ("? the Board's default telling; a version may tell it in its own order (s12)", RED)])


def related_q(cx, cy, cw):
    y = U.table(cx, cy, cw, ["Logic · the question", "Work · what answers it", "Report"], [0, 470, 800],
                ["Reviewer questions",
                 ("RV1  Is the effect causal, or selection?", "work/…/t05 r02 robustness", "q04 · answered"),
                 ("RV2  Does it hold beyond this platform?", "discovery/…/t02 · 4 read", "q05 · partial"),
                 ("RV3  What is new over <prior paper>?", "Related › RQ1 cards", "q06 · open"),
                 "Coauthor questions",
                 ("CO1  What does each author contribute?", "—", "q07 · open"),
                 ("CO2  May the data be shared, and how?", "Resources › <data extract>", "q08 · answered"),
                 "Editor questions",
                 ("ED1  Is the contribution big enough?", "Spine › C1 · Related › RQ1", "q09 · partial"),
                 ("ED2  Is it in scope for the venue?", "Description › Venue", "q10 · answered"),
                 "Reader questions",
                 ("RE1  What is the one thing to take away?", "Spine › Seed", "q11 · answered"),
                 ("RE2  Can I use the method on my data?", "work/…/t03 code · Resources", "q12 · open")], h=30)
    y = U.lines(cx, y + 16, [("one Board question each, group: reviewer · coauthor · editor · reader;", GRAY),
                             ("its report in reports/qNN_<topic>/", GRAY)])
    return U.changed(cx, y + 6, ["new view: the audience's questions, four groups"])


def narrative(cx, cy, cw):
    """Narrative, the story's design (JL 261007: "for the spine and design, they should be merged with one thing,
    Narrative. Like how do we want to tell the story here? Will this story attract the editor or reviewer or
    public."): four questions top to bottom: what it says, how it is drawn, how it is told, will it attract."""
    def head(y, s):
        U.text(cx, y, s, 16, INK)
        return y + 28
    y = U.changed(cx, cy, ["Spine, Design and the §8 Narrative merged: four questions, N1–N4"]) + 8
    y = head(y, "N1 · What does the story say?   ← studio/sNN-story-<telling>/ face (§1 · §2 · §4)")
    y = U.lines(cx + 10, y, [("Seed: <one sentence: what the paper shows and why it matters>", INK)], size=14, gap=24)
    y = U.table(cx + 10, y + 4, cw - 10, ["RQ", "hypothesis", "claim"], [0, 80, 470],
                [("RQ1", "<hypothesis>", "C1 <claim>  ✓ answered"), ("RQ2", "<hypothesis>", "C2 <claim>  stated")],
                mono=(0,), h=26)
    y = head(y + 14, "N2 · How is it drawn?   ← the telling's drawings, beside its face, view only")
    y = U.drawing_box(cx + 10, y, cw - 10, 110, "[ questions → claims → evidence → Sections; edited in Idea Studio ]")
    y = head(y + 4, "N3 · How is it told?   ← the version face's ## Narrative, in reading order (s12)")
    y = U.table(cx + 10, y, cw - 10, ["#", "Section", "claim it carries"], [0, 50, 470],
                [("1", "t01_introduction", "C0 the gap"), ("2", "t02_methods", "— (how)"),
                 ("3", "t03_results", "C1 · C2"), ("4", "t04_discussion", "C2 · C3")],
                mono=(1,), h=26)
    y = U.changed(cx + 10, y + 4, ["Sections named t0N_<title> (was S-<desk>-Main-N-<Title>)"])
    y = head(y + 14, "N4 · Will it attract?   ← a review Run reads the story as each audience")
    return U.table(cx + 10, y, cw - 10, ["audience", "looks for", "where the Story answers", "verdict"],
                   [0, 120, 470, 760],
                   [("editor", "fit · the one-sentence contribution", "Seed · Description › Venue", "✓ yes"),
                    ("reviewer", "claims backed by evidence · rigour", "RQ reports · Related", "partial"),
                    ("public", "the stakes · a plain takeaway", "Stakes · N1", "? not reviewed")], h=26)


def questions(cx, cy, cw):
    """High-level logic + Low-level work: the research questions, each answered by work outside the Board."""
    y = U.table(cx, cy, cw, ["Logic · the question", "Work · what answers it", "Report"], [0, 470, 800],
                [("RQ1  <question> ↗", "work/…/t03 r02 ● ok", "q01_<topic> · answered"),
                 ("RQ2  <question> ↗", "discovery/…/t01 · 6 read", "q02_<topic> · partial"),
                 ("RQ3  <question> ↗", "? not released (G1)", "— · open")], h=30)
    return U.lines(cx, y + 16, [("the paper's own questions: the Story's RQs, answered by work and discovery Tasks", GRAY)])


def ideation(cx, cy, cw):
    """Ideation as questions: why this paper, answered from studio/s01-ideation/ and its tests."""
    y = U.table(cx, cy, cw, ["Logic · the question", "Work · what answers it", "Report"], [0, 470, 800],
                [("ID1  Which question is this paper, and why this one?", "Ideation › the admitted idea (G0)", "q18 · answered"),
                 ("ID2  Is it new?", "the novelty test · Related › RQ1 cards", "q19 · answered"),
                 ("ID3  Can we do it with what we have?", "the feasibility test · Resources", "q20 · partial"),
                 ("ID4  Which ideas were left, and why?", "Ideation › parked ideas", "q21 · open")], h=30)
    y = U.lines(cx, y + 16, [("studio/s01-ideation/ is the work these answers read; the ideation skill runs there", GRAY)])
    return U.changed(cx, y + 6, ["Ideation as questions, ID1–ID4 (was the Ideation Page as a view)",
                                 "the idea pool is a studio topic, s01-ideation/ (was the Ideation Page, Q04)"])


def work(cx, cy, cw):
    y = U.table(cx, cy, cw, ["Job", "kind", "state", "Sections"], [0, 380, 560, 760],
                [("j01_v<MMDD>_<desk A>/ ↗", "version", "submitted <date>", "9 · all ✓"),
                 ("j02_v<MMDD>_<desk B>/ ↗", "version", "drafting", "6 of 9 ▢▢▢"),
                 ("j03_grant_<funder>/ ↗", "grant", "planned", "—")], mono=(0,))
    y = U.lines(cx, y + 20, [("▢ = a Section's map, embedded, view only; pick a row → the Job tab (s12)", GRAY)])
    return U.changed(cx, y + 6, ["no j00_story row: a Story is not a Job · versions dated j0N_v<MMDD>_<desk>"])


def runs(cx, cy, cw):
    return U.table(cx, cy, cw, ["Run", "type", "target", "state"], [0, 380, 560, 760],
                   [("run-venue-<venue B>/", "venue", "venues/<venue B>", "closed · p01"),
                    ("run-question-q02/", "question", "reports/q02", "open · p02"),
                    ("run-draw-roadmap/", "draw", "studio/s01", "closed · p03"),
                    ("run-version-j02/", "version", "j02_v<MMDD>_<desk B>", "closed · p01"),
                    ("j02 › t02_methods runs", "from below", "Section", "open")], mono=(0,))


def delivery(cx, cy, cw):
    y = U.lines(cx, cy, [("from below, by version", GRAY)])
    y = U.card(cx, y + 6, cw, "j01_v<MMDD>_<desk A>   paper.pdf · paper.docx · cover letter", "submitted <date> · frozen in its sent/")
    y = U.card(cx, y, cw, "j02_v<MMDD>_<desk B>   paper.pdf (DRAFT)", "built <date> · 6 of 9 Sections · G4 not yet")
    y = U.card(cx, y, cw, "? its own: reference.bib, or nothing", "? Q02: is the built paper the Board's or the version's", red=True)
    return y


AR = ["Ideation", "Narrative", "High-level logic + Low-level work", "Related Questions"]   # every view: questions

SCREENS = [
    ("Description", U.third(["Scope", "Venue", "Resources", "Related"], "Scope"), ["Update the Board", "Add a venue"],
     "run-version-j02  closed", scope,
     [("Paper-<Name>/bNN_<topic>.md", "the face: Scope (was board.md)"),
      ("Paper-<Name>/studio/sNN-story-<telling>/", "the telling it tells now (face: tells)")]),
    ("Description", U.third(["Scope", "Venue", "Resources", "Related"], "Venue"), ["Add a venue", "Check the rules"], "",
     venue, [("Paper-<Name>/venues/<venue>/call.md", "dates · limits · format · review rules"),
             ("Paper-<Name>/venues/<venue>/kit/", "the author template, as shipped")]),
    ("Description", U.third(["Scope", "Venue", "Resources", "Related"], "Resources"), ["Add a resource"], "",
     resources, [("Paper-<Name>/bNN_<topic>.md ## Related resources", "one row each: title · url · the questions it serves"),
                 ("<project>/work/ · discovery/ · $EXTERNAL_STORE/", "what the rows point to; never copied here")]),
    ("Description", U.third(["Scope", "Venue", "Resources", "Related"], "Related"), ["Add a related item", "Read a paper"],
     "", related, [("Paper-<Name>/related/related.md", "one row per card; reference.bib is built from its papers"),
                   ("Paper-<Name>/related/README.md", "the open-licensed full texts kept"),
                   ("<project>/discovery/…/rNN_<author><year>_<subject>/", "the deep read, a discovery Run: facts · abstract · .bib"),
                   ("  result/rNN_<…>.excalidraw ?", "? the paper's drawing, drawn by the read ticket")]),
    ("Idea Studio", None, ["Draw", "+ Add topic"], "", studio,
     [("Paper-<Name>/studio/s01-roadmap/", "drawing · builder · chat/"),
      ("Paper-<Name>/studio/s02-paper-map/", "generated by excalidraw-section")]),
    ("Audience Report", U.third(AR, "Ideation"), ["Ask a Question", "Generate ideas", "Test idea"], "", ideation,
     [("Paper-<Name>/bNN_<topic>.md ## Questions", "ID1 … one row each, group: ideation"),
      ("Paper-<Name>/studio/s01-ideation/", "the idea pool, the work they read")]),
    ("Audience Report", U.third(AR, "Narrative"), ["Story revise", "Narrative review", "Review for an audience"], "",
     narrative, [("Paper-<Name>/studio/sNN-story-<telling>/", "its face: §1 · §2 · §4 (N1), its drawings (N2)"),
                 ("Paper-<Name>/studio/<Story>.excalidraw", "the Story's design, shown view only (N2)"),
                 ("jNN_v<MMDD>_<desk>/…md  ## Narrative", "the reading order and claims (N3)"),
                 ("Paper-<Name>/runs/run-review-<audience>/ ?", "? the review Run behind each verdict (N4)")]),
    ("Audience Report", U.third(AR, "High-level logic + Low-level work"),
     ["Task review", "Write the report", "Review the report"], "", questions,
     [("Paper-<Name>/reports/qNN_<topic>/", "one Report Page per RQ (answers: RQ<n>)"),
      ("<project>/work/ · discovery/", "the work that answers it, outside the Board")]),
    ("Audience Report", U.third(AR, "Related Questions"), ["Ask a Question", "Write the report", "Review the report"], "",
     related_q, [("Paper-<Name>/bNN_<topic>.md ## Questions", "one row each, group: reviewer · coauthor · editor · reader"),
                 ("Paper-<Name>/reports/qNN_<topic>/", "its report: Answer · Evidence · Limits · Next")]),
    ("Work Details", U.third(["All", "versions", "grants", "slides"], "All"),
     ["Open a version", "? Open a grant"], "", work,
     [("Paper-<Name>/jNN_v<MMDD>_<desk>/", "a version (s12)"),
      ("Paper-<Name>/jNN_grant_<funder>/ · jNN_slides_<talk>/", "the same Story, other forms")]),
    ("Runs", U.third(["All", "venue", "question", "draw", "version", "from below"], "All"), ["Update the Board status"], "",
     runs, [("Paper-<Name>/runs/README.md", "the run types it has (written from run.yaml)"),
            ("Paper-<Name>/runs/run-<type>-<target>/", "run.yaml · ticket .md · passes/")]),
    ("Delivery", U.third(["All", "j01", "j02"], "All"), ["? Build reference.bib"], "", delivery,
     [("Paper-<Name>/delivery/ ?", "? Q02: the Board's, or none"),
      ("jNN_v<MMDD>_<desk>/delivery/", "each version's build (s12)")]),
    U.guide_method("Block"),
]

# the text beside each screen, one list per entry of SCREENS, in order (JL 261007: "make each space a row",
# as s12 and s13 do); a "?" in a paragraph draws it red from there on
NOTES = [
    [("What it is", "The Board's face, bNN_<topic>.md (today board.md): one paper. It says what the paper "
      "argues in one line, which Story the Board tells now, the target venue and version, and where it stands. "
      "The band above it is the old page's line: desk · Story version · questions · Sections · built or not."),
     ("Open", "? With several Stories in one Board (one per idea), the face names the one it tells now "
      "(story-current); the others stay as records.")],
    [("What it is", "Every venue the paper writes for, one folder each, venues/<venue>/: call.md (dates, limits, "
      "format, review rules, the link and the date it was read) and kit/ (the author template as shipped)."),
     ("Why on the Board", "A paper may go to one venue, be declined, and go to another: the Board keeps every "
      "venue, each version names the one it targets and builds with that venue's kit."),
     ("Runs", "Add a venue reads a call into venues/<venue>/; Check the rules re-reads it and marks what changed."),
     ("Open", "? No paper has venues/ yet; today the target venue is read from the Story (Q02).")],
    [("What it is", "What the paper uses and does not own: the work Blocks whose Results it cites, the discovery "
      "Blocks it reads from, its data extracts and code. One row each, with the questions it serves and a link."),
     ("Not Related", "Related is what the paper sits beside (other people's work, cited); Resources is what it is "
      "built from (our own work and data, used). A resource is linked, never copied, so a number in the paper "
      "always traces to one hard Run."),
     ("On disk", "The face's ## Related resources register (title · url · questions), as the live screen reads it "
      "today; the rows point to work/, discovery/ and the ExternalStore."),
     ("Open", "? Today's old page has no Resources view: the Story's Task Roadmap names the work instead.")],
    [("What it is", "What the paper sits beside: related papers, repos and datasets, one card each, grouped by "
      "the question they serve (RQ1, RQ2 …), then Resources. A card's two lines: who · year · title · venue, then "
      "kind · why here · the deep read it links (read rNN ↗)."),
     ("The drawing", "Opened, a card shows the paper's drawing, view only: question → data · method → finding → "
      "limits, drawn by the discovery read from its facts and abstract. A paper not read yet is a red dashed "
      "card; Read a paper fills it."),
     ("On disk", "related/related.md, one table (b03: kind · group · key · paper · venue · doi · why here · read); "
      "a deep read stays a discovery Task's Run. Today it reads the Story's related-papers table."),
     ("Open", "? The discovery read's draw step is not built yet: no card shows a drawing today."),
     ("✎ 261007", "Paper cards in place of the Related Papers table, one open on its drawing.")],
    [("What it is", "The paper's own drawings, one row each, by name; a click opens the drawing in place. The "
      "Story's RoadMap Draw is the first: the person's canvas for the paper's logic, editable."),
     ("Generated ones", "A drawing a script writes (the paper map, by excalidraw-section) opens view only and is "
      "redrawn from its files, never edited."),
     ("Runs", "Draw opens a new drawing; + Add topic adds a studio/sNN-<topic>/ folder with its notes and chat.")],
    [("What it is", "The Audience Report is only questions now (JL 261007), every view in Question │ Work │ Report. "
      "Ideation asks why this paper: which question it is and why this one, whether it is new, whether it can be "
      "done with what we have, which ideas were left and why."),
     ("The work they read", "The idea pool, studio/s01-ideation/ (its tested ideas and the one a person admitted, G0) is the work these "
      "answers cite; it is no longer a view of its own. Generate ideas and Test idea run there, as run types."),
     ("On disk", "Each question is a Board question, a row in the face's ## Questions with group ideation, and its "
      "report in reports/qNN_<topic>/."),
     ("✎ 261007", "Ideation became questions (ID1–ID4); studio/s01-ideation/ is their work (Q04: the "
      "Ideation Page becomes a studio topic; j00_story/ is dropped).")],
    [("What it is", "Narrative is the story's design (JL 261007: Spine, Design and the old Narrative merged into one): "
      "how we want to tell the story here, and whether it will attract its audience. Four questions, top to bottom."),
     ("The four parts", "N1 what the story says: the Seed, then each RQ with its hypothesis and claim. N2 how it is "
      "drawn: the telling's drawings, view only (edited in Idea Studio). N3 how it is told: the Sections in "
      "reading order, each with its claim. N4 will it attract: one row per audience, editor, reviewer and public, "
      "what each looks for, where the Story answers it, and a verdict."),
     ("Where the verdicts come from", "? A review Run reads the story as one audience: an editor checks fit and the "
      "one-sentence contribution, a reviewer checks claims against evidence, the public looks for the stakes and a "
      "plain takeaway. A person signs the verdict; the Run never changes the Story."),
     ("Board and version", "N3 is the Board's default telling. A version may tell the same Story in its own order "
      "(s12 Draft-Main), and its own N4 against its venue's editor."),
     ("✎ 261007", "Spine, Design and the §8 Narrative merged into one view, N1–N4. Sections are named t0N_<title>. "
      "The Story Page is gone (Q04): N1 and N2 read the telling's studio topic, N3 the version face's ## Narrative, "
      "and each research question is a Board Question with its report.")],
    [("What it is", "The paper's research questions, RQ1 … RQn, each with the work that answers it (work and "
      "discovery Tasks, their Runs) and the report that states the answer, reports/qNN_<topic>/."),
     ("Why on the Board", "The questions are the paper's, not a version's: every version tells the same answers. "
      "Fix the evidence first (G1 releases the work), then the report answers it (G2)."),
     ("Runs", "Task review, Write the report, Review the report; the work itself runs in its own Blocks.")],
    [("What it is", "The questions the paper's audience will ask of it, each a Board question with its report: "
      "reviewer questions (is it causal, does it generalize, what is new), coauthor questions (who contributed "
      "what, may the data be shared), editor questions (is it big enough, is it in scope) and reader questions "
      "(what to take away, can I use it)."),
     ("How", "One row each in Question │ Work │ Report: the question, the work that answers it (a robustness "
      "Run, a discovery read, a related card, a Resource), and its report in reports/qNN_<topic>/. They are "
      "answered before a reviewer asks, and a real reviewer's point that recurs across rounds lands here too."),
     ("On disk", "board.md ## Questions, one row each with group: reviewer · coauthor · editor · reader; the "
      "research questions stay in High-level logic + Low-level work."),
     ("Four groups (JL 261007)", "Reviewer, coauthor, editor and reader questions each have a group of their own: "
      "an editor asks whether the contribution is big enough and in scope; a reader asks what to take away and "
      "whether the method carries to their data."),
     ("✎ 261007", "A new view: the audience's questions in four groups.")],
    [("What it is", "The paper's Jobs: its versions (one per send, j0N_v<MMDD>_<desk>), plus grants and talks "
      "told from the same Story. Each row says its kind, its state and its Sections, "
      "each Section's map embedded; a row opens the Job tab (s12)."),
     ("Today", "No paper has version folders yet: the live screen lists the Sections of the one current version "
      "(Main · Appendix · Narrative · Evidence), each opening its Page."),
     ("Open", "? Groups: versions · grants · slides (b03 lists main · appendix, which are a version's)."),
     ("✎ 261007", "No story row: a Story is not a j00_story/ Job. Versions are "
      "dated by their send.")],
    [("What it is", "The Board's own Runs, one folder each in runs/, grouped by run type: adding a venue, "
      "answering a question, drawing, opening a version. Every one is soft: it writes into one item of the Board."),
     ("From below", "The Runs of the Board's versions and Sections show here too, under from below, so a person "
      "sees all the paper's work in one list."),
     ("On disk", "runs/README.md lists the run types (written from each run.yaml, never by hand).")],
    [("What it is", "What leaves the paper, from below: each version's built paper (PDF, Word), its cover letter "
      "and its state, sent or draft."),
     ("Today", "The live screen shows the one build there is (delivery/): the PDF and Word files, their checks "
      "(words, citations, pages ready, submission readiness) and each review round."),
     ("Open", "? Is the built paper the Board's delivery/ or each version's (Q02)? The Board's own would be "
      "reference.bib at most.")],
    [("What it is", "The Guide opened from the Board's tab: its Block section open, the Job and Task sections "
      "folded. Its steps, cards and papers are read from the paper Guide's files (method.md, guide.yaml, "
      "papers.md)."),
     ("The Block's steps", "1 Frame the question · 2 Write the Story · 3 Fix the evidence, then the work; their "
      "method cards are Framing (2) and Story (3)."),
     ("Open", "? A step 0, Set up the paper (scope, venues, related work), signed by naming the target venue "
      "(s31).")],
]

# today: the old paper page (/_board/paper-board) doing each screen's job, drawn under it, dashed and gray
# (JL 261007: "add what is the current workbench UI"); keyed by (Space, the open third-row choice)
STORY_VIEWS = ["Spine", "RoadMap Draw", "High-level logic + Low-level work", "Related Papers"]
TODAY = {
    ("Description", "Scope"): ("Story › Spine › Identity, and the band", "Story", STORY_VIEWS, "Spine", [
        "the band: <desk> · Story v<n> · <N> questions · <N> Sections · built or not",
        "Identity   Open ↗", "- Working title: <title>", "- One-sentence identity: <one sentence>",
        "- Study object and unit: <unit> · Scope: <what is in, what is out>",
        "? no Scope, Venue or Resources view: the venue is one line in the Story"], ("Story revise",)),
    ("Description", "Resources"): ("the Story's Task Roadmap (§7) names the work", "Story", STORY_VIEWS, "Spine", [
        "? no Resources view: the work a paper uses is named in its Story's Task Roadmap,",
        "  shown inside High-level logic + Low-level work as B › J › T › R under each question"], ()),
    ("Description", "Related"): ("Story › Related Papers", "Story", STORY_VIEWS, "Related Papers", [
        "<N> papers · <N> with a PDF", "At <venue>   classic <N> · method <N> · evidence <N>",
        "▸ <title>", "   <author> · <year> · <venue>   RQ1  📄", "▸ <title>", "   <author> · <year> · <venue>   All",
        "Other venues  …", "opened: why we keep it · logic and work · PDF inline"], ("Discovery runs",)),
    ("Idea Studio", ""): ("Story › RoadMap Draw", "Story", STORY_VIEWS, "RoadMap Draw", [
        "chips: one per drawing in studio/ (the Story's first)   Open full screen ↗",
        "[ <Story stem>.excalidraw, editable; a generated one opens view only ]"], ("Redraw",)),
    ("Audience Report", "Narrative"): ("Story › Spine", "Story", STORY_VIEWS, "Spine", [
        "Identity   Open ↗", "   <working title · one-sentence identity · unit · scope>",
        "Pitch   Open ↗", "   <paragraphs>", "Stakes   Open ↗", "   <practical stakes · gap · contribution>",
        "Questions · Claims · …   one card per Story division"], ("Story revise",)),
    ("Audience Report", "High-level logic + Low-level work"): ("Story › High-level logic + Low-level work", "Story", STORY_VIEWS, "High-level logic + Low-level work", [
        "High-level logic   Low-level work · B → J → T → R   Report",
        "▸ Question 1   <question>", "   <what we expect · what would answer it>",
        "   B › J › T › R   <the work that answers it>     q01_<topic> · answered",
        "▸ Question 2   <question>", "▸ Not under a question"], ("Claim review", "Task review", "Write the report")),
    ("Audience Report", "Ideation"): ("Ideation", "Ideation", [], "", [
        "› I1   <the question the idea asks>          ✅ admitted (G0)",
        "› I2   <question>                            parked",
        "› I3   <question>                            open",
        "opened: its substance, writing plan, evidence items, verdict, where it went"],
        ("Generate ideas", "Test idea", "Select idea")),
    ("Audience Report", "Related Questions"): ("Delivery › Rounds (no view of its own)", "Delivery",
        ["LaTeX", "Word", "Cover letter", "Rounds"], "Rounds", [
        "? no reviewer or coauthor questions before a round:",
        "  a reviewer's points arrive only in a Round (Bc-<desk>-Round/RD<NN>-…) as its concern table",
        "▸ RD01-<venue>-editor-decision-<date>    received · response due <date>"], ("Response",)),
    ("Work Details", "All"): ("Sections › Main › Table", "Sections", ["Main", "Appendix", "Table", "Narrative", "Evidence"],
        "Table", ["#   Section            plan    state        ",
                  "1   Introduction       v0.1    🟡 Open   Open ↗", "2   Methods            v0.1    🟡 Open   Open ↗",
                  "3   Results            v0.2    🟢 Written Open ↗", "a row opens the Section's Page workbench"],
        ("Draft runs", "Evidence runs", "Page check")),
    ("Runs", "All"): ("each Space's Runs strip, folded", "Story", STORY_VIEWS, "Spine", [
        "? no list of the Board's Runs: each Space has its own panel of run types",
        "and the matching runs of its Pages"], ()),
    ("Delivery", "All"): ("Delivery › LaTeX › Preview", "Delivery", ["LaTeX", "Word", "Cover letter", "Rounds",
        "Preview", "Artifacts", "Checks"], "Preview", [
        "[ the built PDF, embedded ]", "Artifacts: .tex · .pdf · figures · sizes · when written",
        "Checks: words · citations · displays · pages ready · submission (G4)"], ("Build", "Check", "Cover letter")),
    ("Method", ""): ("Guide › Method, one list", "Guide", ["Description", "Method", "RoadMap Draw", "Related Paper"],
        "Method", ["1 · Frame the question · 2 · Write the Story · 3 · Fix the evidence",
                   "4 · Write the Sections · 5 · Deliver · 6 · Answer the rounds",
                   "the method cards: Framing · Story · Writing and response", "? one list, not split by level"], ()),
}

POPOUTS = [("<author> <year>  ·  a paper's drawing, full size", [
    ("discovery/…/rNN_<author><year>_<subject>/result/rNN_<…>.excalidraw", GRAY),
    ("[ question → data · method → finding → limits, full size, view only ]", GRAY),
    ("facts.md ↗ · abstract.md ↗ · rNN_<…>.bib ↗", INK),
    ("cited by this Board for RQ1: <why here>", INK),
    ("regenerated when the read reruns; never edited by hand", GRAY)]),
    ("<venue B>  ·  a venue's call", [
    ("venues/<venue B>/call.md", GRAY),
    ("read <date> from <link> ↗", INK),
    ("deadline <date> · <n> words · 6 displays · double blind", INK),
    ("kit/: <template>.cls · <template>.bst", INK),
    ("j02 builds with this kit (paper-build.toml names it)", GRAY)]),
    ("C2  ·  a claim, from the Spine", [
        ("RQ2 <question>", INK),
        ("claim: <claim> · warrant: <why the evidence supports it>", INK),
        ("evidence: E01 value · E04 display (q02's report)", INK),
        ("told in: j02 › t04_discussion ↗", GRAY),
        ("state 📝 until q02 says answered (G2)", RED)])]

QUESTIONS = ["? The read ticket's draw step (discovery theme): one template from facts.md",
             "? Several Stories in one Board: the Board shows the one the face's tells: names",
             "? Work Details groups: versions · grants · slides",
             "? Board Delivery: from below only, or its own reference.bib (Q02)",
             "? Guide › Method: step 'Fix the evidence, then the work' at Block, its work in other Blocks"]

if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s11-paper-block.excalidraw"
    U.level_drawing(out, "build_s11_paper_block.py", "Block",
                    "Block level: the paper Board, one paper and its versions",
                    "Q01's proposal (s01): the Board holds the paper's scope, venues, related work, questions and Story; "
                    "its Work Details are the versions.", MOVES, SCREENS, POPOUTS, QUESTIONS, notes=NOTES, today=TODAY, changes=CHANGES)
