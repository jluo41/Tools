# Template · the GENERATED mirror Page, and the eight slots a person writes

<!-- The heading above is not part of the page. It is the first line of this file, so
     `skillpage.py` prints it as this file's purpose row in every mirror page's
     generated tree. The page's own title is the `# <unit name> · v<version>` further
     down. -->

<!-- ═══ READ THIS BEFORE ANYTHING ELSE ═══════════════════════════════════════
     THIS FILE IS NOT COPIED. Every other Page Type's template is a file you copy
     and fill. A mirror Page is GENERATED, so this one is a MAP of the generated
     result plus the slots a person fills in AFTER generation.

     HOW A PAGE OF THIS TYPE IS CREATED:

       python3 <board-skill>/cli/skillpage.py new <board> <skill-or-agent-path> \
               --group <GROUP-KEY> --stamp "YYMMDD HHMM"

     `new` writes the Page from its own stub AND registers it in `board.md`
     `## Pages`. Copying a template and registering by hand produces a Page with
     no managed spans, which `skillpage.py check` then reports as `no managed
     block` forever. The base's `create a new page` steps do NOT apply here.

     Then work down the RULE comments below against the generated Page. A RULE is
     satisfied ON THE PAGE, not in this file. If you keep a scratch copy beside the
     page, delete each RULE as you satisfy it; nothing from this file ever ships.

     WHAT THIS TYPE ADDS, and nothing else is restated here:
       the base frame        haipipe-page/SKILL.md (sections, order, title,
                             Opening physical shape, evaluation contract)
       this type's contract  ./SKILL.md (the reasoning behind every RULE below)
       the writing standard  haipipe-board/ref/writing-rules.md
       the generator         haipipe-board/cli/skillpage.py

     English only. No em-dashes. One sentence per source line. -->

<!-- RULE · WHO WRITES WHAT. This is the whole point of this type. Eight slots are
     a person's and the rest is the generator's. A person writing inside a managed
     span is erased by the next `sync`, silently.

       🧑 a person writes    state: · owner: · method: · ## Opening ·
                             the WORKFLOW caption and fence in ## Diagram ·
                             ## Aims · ## States · the ## Log lines ABOVE the span
       🤖 skillpage.py owns  the `· v<version>` in the title · the tree span ·
                             the body span · the log span
       ⚙️ the live layer owns session:

     A script that rewrites one of the 🧑 slots is a defect. A person editing one of
     the 🤖 spans is wasted work.
     DELETE this RULE when you can say which half every line of your page is in. -->

<!-- RULE · DELETE THE STUB'S OWN INSTRUCTIONS. `new` seeds five blocks of text that
     tell you what to write. All five must be gone before the page is finished:
       ① the `REPLACE THIS PARAGRAPH.` paragraph in Opening
       ② the two paragraphs under it about never opening with a question
       ③ the placeholder body inside the WORKFLOW fence (`Draw how this skill is
         actually used ...`) and its `REPLACE THIS CAPTION` line
       ④ the single `P1 · Rule this skill's health.` Aim
       ⑤ `Page generated <stamp>; nothing ruled yet.` in States
     ⑤ is a claim that nobody has looked, and it stops being true the moment
     somebody has. DELETE this RULE when all five are gone. -->

<!-- RULE · THE NUMBER IS THE PAGE NUMBER, NOT THE UNIT. `new` takes
     `max(existing) + 1` for that kind: Skill numbering starts at 0, Agent at 1. A
     page archived into `_archive/` does not count, so a retired `Skill-1` leaves
     its number spent rather than free. `--group` takes the KEY only (`QC`), never
     the full heading (`QC · Engine`). DELETE when the file is named. -->

<!-- RULE · SHIPPING THE UNIT IS NOT THE SAME AS LINKING IT. A new skill folder is
     invisible to every agent until `./install.sh --global` links it
     into the roster. A session already running keeps its old roster. This bit
     `haipipe-page-for-skill` itself, which sat unlinked for a day after it
     shipped. DELETE when the unit resolves by name in a NEW session. -->

# <unit name, exactly as its frontmatter `name:` states> · v<version>

<!-- RULE · THE TITLE IS DERIVED, ALL OF IT. `new` writes it and `sync` rewrites the
     `· v<version>` suffix from the unit's frontmatter on every run, so the index row
     shows an unmaintained unit at a glance. Do not maintain the version by hand, do
     not put it in `state:`, and never in the filename: a name that changed every
     release would break every link to the page. This overrides the base's
     sentence-case purpose-stating title rule, because the title here is the unit's
     own name. DELETE this RULE once you have stopped touching the title. -->

state: <one of 🔴 OPEN · 🟡 · ✅ · ⏸️> · <the evidence for that judgment>
owner: <who rules on this unit, usually JL>
method: three managed spans sync from the skill folder; everything else is written by hand
session: <machine-written; do not type this line>

<!-- RULE · `state:` IS A HEALTH JUDGMENT AND ONLY A PERSON WRITES IT. It keeps the
     base's four values and answers one question: is this unit stable, in flux, in
     question, or parked? A version cannot answer it, so `new` seeds 🔴 OPEN and a
     person changes it. The readable note after the emoji carries EVIDENCE, not a
     mood:
       ✅  🟡 in flux · 168 releases in 15 days, 3 open defects
       ✅  🟡 in question · existence unruled since 260729
       🚫  🟡 in flux                 says nothing a reader can check
       🚫  🟡 in flux · v0.9.0        that is the title's job
     🔴 OPEN on a unit that ships is almost always a page nobody finished.
     DELETE when your note names something a reader can verify. -->

<!-- RULE · `session:` IS THE LIVE LAYER'S. `live/chat.py` inserts it directly after
     `method:` the first time a page chat runs, and rewrites it on every later
     session. A generated page has no such line and that is correct. Never hand-write
     one. DELETE this RULE when you have left the line alone. -->

## Opening

<!-- RULE · A MIRROR PAGE INTRODUCES; IT NEVER ASKS. Its subject exists on disk
     before the board mentions it, ships to other people, carries its own version and
     changelog, and DECIDES NOTHING. The base's Opening shape ends in `what this page
     decides`, so it leaves this kind with only a rhetorical question, and on 260802
     five pages filled that empty slot with the same one. The visible paragraph
     answers three questions in plain words for a reader who has never heard of the
     unit:
       ❶ WHAT IS IT, and what is it FOR. One line. A reader who stops here can say
         what it does.
       ❷ WHEN DO I REACH FOR IT, rather than the ONE SIBLING you would otherwise
         pick, named. A boundary stated against a real neighbour is checkable;
         "it owns X" is not.
       ❸ WHERE DOES IT STAND. The one thing to know before trusting it: what is
         unproven, unbuilt, unruled, or moving fast, with the fact that shows it.
     ❶❷❸ IS CONTENT, NOT A TEMPLATE. The slots say what the paragraph must ANSWER.
     They do not fix your sentence order and they do not hand you an opening move.
     The first batch written to this contract already showed the pull: 7 of 8 put a
     second-person "Reach for it when ..." line second. It survived review only
     because each slot carried a DIFFERENT checkable fact.
     DELETE when all three are answered without a reusable scaffold. -->

<one visible paragraph: ❶ what the unit is and is for, ❷ when you reach for it rather than the named sibling, ❸ where it stands with the fact that shows it>

<!-- RULE · FOUR THINGS THIS OPENING MAY NEVER DO.
       🚫 the LEAD SENTENCE never ends in `?`. Mechanical, so nobody has to judge
          "rhetorical". `check.py` enforces it as `skillpage-opening-is-a-question`,
          and it exempts `Skill-`/`Agent-` pages from the base's opposite rule,
          `opening-lead-not-a-question`.
       🚫 never paraphrase the unit's own description. Content already carries those
          bytes; a paraphrase is a lossy second copy.
       🚫 never use the own · hard-part · depend · healthy scaffold. Four slots
          produce four filler sentences and one form letter.
       🚫 never claim health the page cannot show. ❸ names its evidence or says the
          evidence is missing.
     DELETE when the lead does not end in `?` and none of the other three applies. -->

<!-- RULE · THE BASE'S PHYSICAL SHAPE IS UNCHANGED, so this file does not restate it,
     only names the three parts a mirror page keeps getting wrong: the FIRST BLANK
     LINE above is the split, everything below it is the `More details` drawer, and
     the drawer is a list of `**Label**:` parts and never one block of prose. The
     visible paragraph is capped at 520 characters, measured on the render by
     `check.py`. DELETE when the split and the labels are in place. -->

**<Label saying what this part answers>**: <its sentences, one per source line>

**Covered elsewhere**: <the neighbouring unit or page that owns what this one does not>

<!-- RULE · THE DECISIVE TEST IS NOT THE AUTHOR'S TO PASS. Read the changed Openings
     CONSECUTIVELY in board order, not one at a time: a page that is clear alone still
     fails if its Opening would introduce its sibling after a noun swap. The writer
     cannot see this, because the writer knows which unit they meant. Dispatch
     `haipipe-board-reviewer-agent`, which loads this contract for exactly this kind
     of page. DELETE when a fresh reviewer has read the batch. -->

## Writing Style

<!-- RULE · OPTIONAL, AND THE ROSTER IS SPLIT. `new` seeds this section, so a page
     generated today carries it; pages generated before the stub had it do not, and
     that is not a defect to repair. It renders inside Opening's drawer, not as its
     own section. Delete the heading if you have nothing page-specific to say.
     DELETE this RULE either way. -->

English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram

<!-- GENERATED SPAN · tree · DO NOT EDIT · DO NOT HAND-TYPE.
     On the page the two markers sit at column 0. They are indented by two spaces in
     the fence below so this file can never be read as a page carrying a real span,
     which is the failure mode that cost one page its Aims, States and Log on 260803. -->

```text
  <!-- haipipe:skill:tree:start <16-hex digest> <path/to/unit> -->

  **What `<unit>` ships**: every file in the folder, with the one-line purpose each one states for itself.

  ```
  <unit>/
    CHANGELOG.md          90 ln  <the purpose line the file states about itself>
    SKILL.md             292 ln  <the purpose line the file states about itself>
  ```

  <!-- haipipe:skill:tree:end -->
```

<!-- RULE · AN AGENT'S TREE SPAN IS EMPTY, AND IT IS KEPT. An agent is ONE file, so
     there is no folder to draw and the span renders with nothing between the markers.
     `sync` replaces spans it can find, so a span DELETED to tidy the page reports
     forever as an older page needing repair. Leave the empty pair alone.
     DELETE when you have not removed it. -->

<!-- RULE · THE TREE'S CAPTION IS GENERATED TOO, and it lives INSIDE the span on
     purpose: a caption written inside is erased by the next `sync`, one written just
     outside survives but is generated by nothing, so every new page would start
     non-compliant with the base's caption rule. Folder units only: an Agent page's
     empty span carries no caption, because it has no figure to caption. Do not add a
     caption above either span. DELETE when you have not added one. -->

<!-- RULE · ONE AUTHORED FIGURE FOLLOWS THE SPAN, and it is the only figure a person
     writes on this page. A folder can be read off disk; an INTENT cannot. Draw how
     the unit is actually used: the entry point, what it reads, what it writes, and
     where it hands off. On an AGENT page this fence carries the whole picture,
     because there is no tree to carry it. Base rules still bind: the caption line
     goes ABOVE the fence, and a row is a label and its value, never a clause that
     could end in a period. Delete the caption and the fence together if the tree is
     genuinely the whole story. DELETE this RULE when the figure is real. -->

**How `<unit>` is used**: <what the figure below actually shows>

```text
WORKFLOW  <the one line that says what this figure is>

  <the entry point>
        │
        ├─▶ <what it reads>
        └─▶ <what it writes, and where it hands off>
```

## Content

<!-- GENERATED SPAN · body · DO NOT EDIT · DO NOT HAND-TYPE.
     Markers indented by two spaces here for the same reason as the tree span. -->

```text
  <!-- haipipe:skill:body:start <16-hex digest> <path/to/unit> -->

  **<name>** · `<version>` · last shipped <last_updated>

  - folder   `<path/to/unit>/`
  - tools    <allowed-tools, or "not declared">
  - summary  <the frontmatter summary>

  ### SKILL.md            (or `<agent-name>.md` for an Agent page)
  ... the unit's own bytes: every `## ` becomes `- N ·`, every `### ` becomes `- N.M ·` ...

  ### The other files     (folder units only, and only when there are other files)
  ... one fenced row per file: path, line count, and the purpose the file states ...

  <!-- haipipe:skill:body:end -->
```

<!-- RULE · CONTENT IS NOT OURS. It is the unit's own bytes, and it is the reason this
     Page Type has no Content divisions of its own to number, caption, or key an Aim
     id to. A sentence written in here is deleted by the next `sync` without warning.
     If the words are wrong, fix the UNIT's `SKILL.md` and re-sync.
     DELETE when you have written nothing between those markers. -->

<!-- RULE · `- tools` READS `allowed-tools:` AND MOST UNITS DO NOT DECLARE IT.
     `skillpage.py` looks for a scalar `allowed-tools:` in the unit's frontmatter.
     Agent charters declare `tools:` as a YAML list instead, which this parser reads
     as an empty value, and no board-family `SKILL.md` declares `allowed-tools` at
     all. So the row prints `not declared` on every mirror page of the boardform
     board, agents and skills alike. That is a generated row: do not hand-correct it,
     and do not claim in your Opening that a unit's tools are declared on its page.
     Repairing it means changing the parser or the charters, which is the unit's
     work, not the page's. DELETE when you have left the row alone. -->

<!-- RULE · A GREEN `check` MEANS LESS THAN IT LOOKS. `digest()` hashes the
     frontmatter's derived facts only (`name`, `version`, `last_updated`, `summary`,
     `allowed-tools`), by its own docstring, "so prose edits never look like drift".
     ✅ means the metadata is current, NOT that this page's copy of the `SKILL.md`
     still matches the file it mirrors. Byte equality needs a regenerate-and-diff by
     hand. `sync` rewrites the spans; `check` REPORTS a stale hash and never rewrites,
     so drift is visible rather than possible. DELETE when you have stopped reading ✅
     as "the copy is current". -->

## Aims

<!-- RULE · AIMS ARE THE UNIT'S OPEN WORK, NOT THE PAGE'S. The page is finished the
     moment it describes the unit truthfully; the unit is not. Three sources fill
     them, and the third is the one people miss:
       ① what the unit itself still owes    unbuilt verbs, unwritten contracts
       ② what is unproven about it          shipped but never run, never measured
       ③ a defect another page ROUTED here  because this unit ships the file
     ③ is correct routing, not passing the buck: the page that finds a defect is
     rarely the page that ships the file, and a finding parked on the finder's page is
     a finding nobody owns. Name the page it came from.
     DELETE when every Aim is about the UNIT. -->

<!-- RULE · THE FORM OVERRIDES THE BASE, AND THE OVERRIDE IS CLAIMED ON PURPOSE. The
     base wants `- A<n>.<m> ·` ids with a testable `Done when`, one State row per Aim
     id, and no checkbox on a canonical Aim. A mirror page does none of that:
       ✅ HERE   - [ ] / - [x] <emoji> <the unit's open work>
                       <why, indented, one sentence per line>
       🚫 HERE   A<n> ids · `Done when:` · one State row per Aim
     WHY: the base's Aim ids key to CONTENT DIVISIONS, and this page's Content is the
     unit's own bytes in a managed span. There are no divisions of OURS to key to, so
     an A<n> id would point at somebody else's headings.
     The renderer already knows: `aim_progress` reads the checkboxes in legacy mode
     and the section header prints `<n> met · <m> open`. An independent reviewer
     refused to judge the Aim-to-State map on eight pages because three contracts
     disagreed and none claimed the override; this RULE is that claim.
     DELETE when the Aims are checkboxes with no ids. -->

- [ ] <emoji> <what the unit still owes, as a statement of the outcome>
      <why it is open, and what goes stale if it stays open, one sentence per line>
- [x] <emoji> <something the unit now does, written as done>
      <the evidence: a version, a date, a measured fact>

## States

<!-- RULE · STATES IS DATED RECORDS, NOT ONE ROW PER AIM. Open with one plain
     paragraph saying where the unit stands and why its `state:` reads the way it
     does, then dated records newest first:
       - YYMMDD WHO · <emoji> <title>
         <what happened, indented, one sentence per line>
     The base's one-to-one Aim-to-State map does not apply here, for the same reason
     the Aim ids do not. Give numbers: "168 releases in 15 days", "8 of 8 survived the
     noun swap", not "moving fast". DELETE when the records carry dates and numbers. -->

<one plain paragraph: where the unit stands, and the reason behind its `state:`>

- <YYMMDD> <WHO> · <emoji> <title of what happened>
  <the record, one sentence per line>

<!-- RULE · `## Files` IS OMITTED, AND THAT IS CORRECT. The base marks it "allowed,
     advised against"; here it is simply absent, because the derived Diagram tree
     already lists every file the unit ships and a Files section would be a second,
     staler copy of it. No mirror page on the boardform board carries one.
     DELETE when you have not added the section. -->

## Log

<!-- RULE · YOUR LINES GO ON TOP, ABOVE THE SPAN. The generated log span holds the
     unit's `CHANGELOG.md` converted into dated Log lines, so every release the unit
     ever shipped counts on the ACTIVITY strip. Your own hand-written lines go between
     the `## Log` heading and the start marker; anything written inside the span is
     replaced on the next `sync`. Newest first, `YYMMDD HHMM · what changed`, time
     optional, and take the time from the clock rather than inventing it. A leading
     `- ` makes the line a foldable item whose indented lines are its explanation.
     Live pages also prefix a phase and actor tag, `[REVISE-CC]`; that is an observed
     board convention, not a rule this contract sets. DELETE when your lines are above
     the marker. -->

<YYMMDD HHMM> · <what changed by hand, and why>
<YYMMDD HHMM> · page generated from `<path/to/unit>/` by `skillpage.py new`

<!-- GENERATED SPAN · log · DO NOT EDIT · DO NOT HAND-TYPE. -->

```text
  <!-- haipipe:skill:log:start <16-hex digest> <path/to/unit> -->

  Converted from the skill's own `CHANGELOG.md`: <n> releases.

  <YYMMDD> · `<version>` · <the release title>
        <the changelog entry's own lines, indented>

  <!-- haipipe:skill:log:end -->
```

<!-- RULE · NEVER DELETE A `> USER:` OR `> Comment` LANE. Resolve it, then move it
     into a dated Log record verbatim. DELETE when nothing has been dropped. -->

<!-- RULE · WHEN THE UNIT RETIRES, the page does not just stop. `git mv` it into
     `_archive/`, remove its line from `board.md` `## Pages`, and add BOTH its id and
     its old `Q-Skill-<name>` alias to `## Links` pointing at the archived path, so
     every existing citation still resolves. Then grep the board for prose that still
     names the unit as live: a Log line recording what was true when written STAYS, a
     live-prose sentence claiming the unit still ships is now false. Proven on
     `haipipe-board-index`, retired 260802: the sweep found eight live-prose sentences
     on four other pages plus one dead citation on a sibling board.
     DELETE this RULE when the unit is live, or when the archive sweep is done. -->
