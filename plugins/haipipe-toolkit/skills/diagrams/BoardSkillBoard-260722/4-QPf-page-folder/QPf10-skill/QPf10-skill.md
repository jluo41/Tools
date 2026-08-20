# Skill · the page's citations into the skill tree
state: 🟡 PARTIAL · list, index, agent rows, boundary lived in · open: first drag, QPf6 git ruling
owner: JL
method: give each page a ranked skill list, fill it by scanning the page for names, and let the person drag the cards, because the order is the judgment

## Opening
Which skills stand behind a page, and who says which matters most?
This works like its twin bibex, the page's own list of paper references.
bibex points at the literature, and this points at the skills.
The list is the PAGE's own `skill/<stem>.md`, one row per skill.
A scan fills it by reading the names the page actually writes.
The 🛠 tab shows that list as cards, and what matters is the ORDER.
A person drags a card up or down, and top means most related.

**What the person gets per card**: the name, plus the description and the small print the card reads from the skill's own SKILL.md, its version and `last_updated`.
An agent row shows the single word `agent` there instead.
Each card also has a ⠿ handle to drag it into place, and a door that opens the skill, or the agent on an agent row.
It shows the person's note when the row carries one, and a ✕, which removes the name and keeps it removed.
**What the name does**: the 🛠 tab opens on the card INDEX.
Click a card's name, or `open the skill`, and that skill fills the SAME frame.
The skill's bar carries ← and → to walk this page's skills in ranked order, and ☰ to go back to the index.
An agent's name opens its definition in the markdown view, which sits outside that walk.
An earlier separate 🔍 tab was retired, see Log.
**Covered elsewhere**: `QPf1` rules the folder; the plugin list row is `../../board/haipipe-plugin/ref/roster.md`; the twin whose shape this copies is `QPf8` (bibex); `QPf6`'s own list is the first real user.

## Diagram
**The list is the truth, and three doors work on it**: the scan suggests names, the person ranks them, and the view only draws them.
```text
  📄 <page>/<stem>.md          the page's prose · the scan reads skill NAMES from it
        │
        ▼
  🗃 skill/<stem>.md           YOURS · one row per skill · order = the rank
        ▲
        │  three doors, one truth
    ↻ /_board/skill            re-scan · suggest names · draw again
    ⠿ /_board/skill-order      the drag · saves the new order
    ✎ /_board/skill-entry      add at top · ✕ remove · ↩ restore · note
        │
        ▼
  🖼 skill/<stem>-skill.html    REBUILT · the card index behind the 🛠 tab
```

## Content
### 1 · One file you own, and one view the machine rebuilds
**A MIXED plugin, like bibex**: one file a person rules, and one view a rebuild may replace.
```text
  <page>/skill/
    <stem>.md           🧑 YOURS · the page's ranked skill list · committed
    <stem>-skill.html   ⚙️ REBUILT · the card index · built again freely
  flat page fallback: <board>/skill/ · the same fallback every plugin has
  the row grammar, whole:
    - <name>              a related skill · position = rank
    - <name> · note: …    the same · with the person's note
    - <name> · removed    the ✕ removed line · folded · ↩ restorable
```
📌 This part settles that the list is yours to write and the card view is rebuilt, and it shows what a row looks like.

#### 1.1 · The scan
The scan only pulls out what is already there, the same way bibex does.
It lists names the page literally writes, and matches each whole word against the real SKILL.md folders and agent files in the toolkit tree.
So a name is never invented.

#### 1.2 · Agents are rows too
A row may name an AGENT as well as a skill.
An agent is one `agents/<name>-agent.md` file, so its card wears 🤖 and the word `agent`.
Its door opens the live markdown view, because there is no SKILL.md folder behind it.
The rank does not care which kind a row is.
A page that leans hardest on an agent puts that agent on top.

#### 1.3 · What git keeps
The list is committed, like the page's bib file.
What git does with the rebuilt view follows the one Decision row on `QPf6`, the latex plugin page, which answers it for every rebuilt plugin folder at once.

### 2 · Where you put a name is the whole judgment
**The one judgment**: where a name sits, and who put it there.
```text
  ⠿ TOP        most related           🧑 the person drags
  ＋ TOP       added by hand          🧑 the edit buttons · adding says "this matters"
  ⠿ MIDDLE     the ranked middle      🧑 the person drags
  ⠿ BOTTOM     newly scanned names    🤖 the scan adds here
  ✕ OFF        into the removed fold  🧑 the person's ✕ · ↩ restores
```
📌 This part settles that the order of the list is the judgment, and that only a person sets it.

#### 2.1 · Order is the judgment
The order of the list is the one judgment the plugin records, and top means most related.
Dragging a card saves that order to the list, and a scanned name waits at the bottom until the person ranks it.

### 3 · One tab, and you can step into a skill without leaving it
**The 🛠 tab, two depths**: the index of cards, and the skill it opens onto, one frame for both.
```text
  83-plugin-skillmap.js ──POST──▶ /_board/skill ──▶ scan + INDEX view
  tab.url()  names skill/<stem>-skill.html · HEAD hit ▶ frame it
  depth 1 · THE INDEX     one card per row: ⠿ · name · meta · description ·
            the open door · ✕ · drag anywhere to rank
            🛠 a skill row   meta v<version> · updated <date> · open the skill
            🤖 an agent row  meta agent · open the agent · outside ← →
  depth 2 · THE SKILL     same frame, /_board/skillview?p&map:
            ← prev · ☰ back to the index · next → (arrow keys too)
            header card + related-skill chips, then ONE fold grammar:
            ▸ 📜 SKILL.md (open) · ▸ 📜 CHANGELOG · ▸ 📚 ref/*.md · ▸ 🗂 rest
```
📌 This part settles that one tab holds both the card index and the skill you open from it.

#### 3.1 · The round trip
The drag POSTs the new order through `/_board/skill-order` and reloads.
✕ and ↩ POST through `/_board/skill-entry`.
Clicking the lit tab only builds the view again.

## Aims
### A1 · 🗃 One file you own, and one view the machine rebuilds
- A1.1 · The list, the scan, and the safe refresh shipped.
  **Done when:** every page keeps its skills in its own `skill/<stem>.md`, and a refresh only appends new names at the bottom of it.
- A1.2 · One page's list carries a person's own order, not a machine's.
  **Done when:** a list on disk holds the order a person set by dragging its cards.
- A1.3 · What git keeps of the rebuilt card view is ruled.
  **Done when:** `QPf6`'s Decision row is answered, and this folder follows the answer.

### A2 · 🧑 Where you put a name is the whole judgment
- A2.1 · The cards, the edit buttons, and the typo guard shipped, and the rank became the one judgment.
  **Done when:** the index shows one card per row with ⠿, ✕, ＋ and a note, and the drag is the only judgment it saves.
- A2.2 · The first REAL judgment on a list is JL's.
  **Done when:** a person's drag, not a migration, sets the top of a live list.

### A3 · 🖼 One tab, and you can step into a skill without leaving it
- A3.1 · One action in the workbench makes the whole round trip in a real browser.
  **Done when:** one click in the 🛠 tab writes the list and draws the view again, seen in the browser JL uses.

### P · 🚧 Discovery stays out of this folder
- P1 · Discovery treats `skill/` as plugin material and warns on nothing inside it.
  **Done when:** no file under any page's `skill/` is listed as a page, and the board builds clean around live `skill/` folders.

## States
### A1 · 🗃 One file you own, and one view the machine rebuilds
- ✅ A1.1 · Tested through its lifecycle 260815 on QPf6, the 260816 move rewrote all 15 live lists to the ranked-list shape in place, and an old-shape list still parses and is rewritten flat on its next write.
- 🧠 A1.2 · Waiting on a person: no drag has landed on any list, and QPf3's five rows sit where the 260816 move put them, sorted designs-first by the machine.
- 🧠 A1.3 · Waiting on a person: `QPf6`'s Decision Now row, on what git keeps of a folder the machine rebuilds, is still unticked.

### A2 · 🧑 Where you put a name is the whole judgment
- ✅ A2.1 · The flattened index is live: ⠿ drag, ✕ with the removed rows folded away, ＋ add at top, and nothing else on the card.
- 🧠 A2.2 · Waiting on a person: JL's 260815 work on two QPf3 rows was made in the relation vocabulary the flattening removed, so the list keeps no trace of it and the first drag is still to come.

### A3 · 🖼 One tab, and you can step into a skill without leaving it
- ✅ A3.1 · JL's own clicks made the whole round trip through the view's buttons, the POST, and the reload.

### P · 🚧 Discovery stays out of this folder
- ✅ P1 · The `_in_plugin` rule in `src/common.py` hides every non-page subfolder of a folded page, so it covers `skill/` without a list of names, and the board builds clean around live skill/ folders.

## Files
### ⚙️ Engines
- `../../board/haipipe-board/live/skillmap.py`
  All three doors: the skill index, the scan, the list writer, the drag order, the edit buttons, and the card view.
- `../../board/haipipe-board/assets/js/10-drawer/83-plugin-skillmap.js`
  The registry entry whose `tab` spec the shell builds the 🛠 tab from.

### 🧪 Evidence
- `../QPf6-latex/skill/QPf6-latex.md`
  The first live list, moved over 260816: five names in ranked order, with `haipipe-plugin-latex` and `haipipe-plugin` at the top.

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QPf6 page](4-QPf-page-folder/QPf6-latex/QPf6-latex.md)
  QPf6 carries the one Decision Now row on what git keeps of a folder the machine rebuilds, and that row rules this page's card view with the rest.

## Law
- 🤖 The list holds AGENTS beside skills (JL 260816: "我们的 Plug、我们的 Skill 其实也是包括 Agent 相关的。所以如果 Agent 跟它们相关，你也可以加上去")
      A page's working relations include the agents it dispatches, not only the skills it loads, so an agent definition is a first-class row: same rank, same ✕, same note.
      The first consumer is `QPf9`, whose cards crossed to the bank through two agents the map now names.
      Rejected: keeping agents in a skill row's note, because a relation buried in another row's note cannot be ranked, removed, or opened on its own.
- ✂️ The scan seeds, the person RANKS (JL 260816: "we just need to show these skills and the user can drag and rank them themselves")
      A scanned name lands at the bottom of the list; the order is the person's judgment, and ✕ is the person's removal.
      A refresh never edits, reorders, or removes a row it finds, and a scan never re-seeds a name whose row ends ` · removed`.

## Log
- 260816 · [RULE-CC, under JL's delegation] the head dropped ✅ SETTLED → 🟡 PARTIAL. The pass above demoted A1.2 and A2.2 to 🧠 because their evidence is not on disk, which left a page claiming settled while carrying three open Aims; `check.py` reported the contradiction as `settled-with-open-aims`. A page that under-claims can be re-closed by one drag on a real store, and a page that over-claims teaches a reader something false, so the state moved rather than the rows. Reopening it is JL's the moment the first drag lands.
- 260816 · [REVISE-CC] the evidence was read off the lists on disk, and two ✅ rows did not survive the reading.
      A1.2 and A2.2 now stand at 🧠, because `QPf3`'s list is five plain rows with no note, no ` · removed`, and nothing marking anyone's work, and the order they sit in is the one the 260816 move wrote from the retired designs-first sort, so no list on disk yet shows a person's own rank.
      Both aims stay exactly as written; only what is true of them today changed.
      The git leftover left States' lead prose and became `A1.3` with its own 🧠 row, which supersedes the 0056 entry's reasoning: that entry ruled out a second `A1.1` row, not a new id, so the one thing waiting on a person is machine-visible now and ✅ SETTLED survives as explicitly held.
      Every Aim gained a `**Done when:**` line and handed its shipped-and-dated sentence to States: the plain-word pass reports rewriting each of those lines, but none of them survived it, so Aims and States were saying the same past tense twice and neither said what would count as done.
      The id-and-no-checkbox form of the Aims had never been logged either, and it is what takes this page out of the checkbox exemption in `check.py`'s `check_state_mirrors_aims`, so the Aims-to-States mirror is enforced here and every continuation line sits at the template's two-space indent.
      Files gained the fixed `### 🔗 Related Board Pages` group, so `QPf6`'s Decision row has an address and not only a name; §1.3 says which page carries it, the Opening glosses bibex where the name first appears, and the state line's `open:` names the first drag beside the git ruling.
- 📖 260816 · [REVISE-CC, JL ruled] the page was rewritten in plain words, for a reader with ADHD whose English is a second language (JL: "我真的读不下去"). The 🧭 Outline tab had been showing this page's own sentences back, and they were unreadable, so the tab was right and the prose was not. Every division title now names its consequence instead of a mechanism, each one gained a `📌` line saying in one sentence what the part settles, and every aim, `Done when:` and State row was replaced with a short plain-word version. House words went with them, `division` to part, `store` to list, `render` to read or draw, `seed` to suggest, `mint` to build. Measured with `haipipe-writing`'s `cli/score.py`: 4 sentences flagged before, 1 after, every one that remains inside this Log, which is history and was not touched. No fact, id, `§` mark or section changed; only the words.
- 260816 · [REVISE-CC] the second review round landed: Law's ✂️ row states the whole tombstone rule again, that a scan never re-seeds a name whose row ends ` · removed`, which the earlier de-duplication had reduced to the bare noun; the state line and States both carry the one leftover the 0056 entry claims, the DERIVED view's git fate waiting on `QPf6`; §2's figure gained the ＋ and ✕ rows its caption promises and lost the retired badge/tick/drift row together with §2.1's sentence naming them; the Opening and §3 now say a card reads its meta from the skill's own SKILL.md while an agent row shows `agent` with an open-the-agent door outside the ← → walk; and the QPf6 evidence row names the two skills at the top of that list instead of teaching the retired `designs` relation.
      The leftover sits as States' lead line rather than as a second `A1.1` row, because `check.py`'s `check_state_mirrors_aims` warns `aim-stated-twice` when one Aim id carries two rows, and no Aim on this page owns the git question.
- 260816 · [REVISE-CC] the page caught up with its own flattening: §2 now states the rank rule in the present tense and the migration story lives only in the [RULE-JL] row below, the refresh rule is stated once in Law with the Diagram and §1 fences cut to label · value rows, Content paragraphs took #### numbers, Files moved above Law into the template order, States gained the A1/A2/A3/P group headings and dropped its narrative line, the git-fate row moved into §1.3, and A2.1's evidence was trimmed to the shipped result.
- 260816 · [RULE-JL] agents joined the list (JL: "我们的 Skill 其实也是包括 Agent 相关的"): the index now offers every `agents/<name>-agent.md` beside the SKILL.md folders, an agent card wears 🤖 with the live markdown view as its door, the scan seeds agent names a page writes, and the ← → walk stays skills-only because mdview has no map bar; `QPf9` is the first consumer, ranking the collector and the bank door its probe cards crossed through. The earlier agent-in-a-note workaround on QPf9's map is superseded and the Law row records why.
- 260816 · [RULE-JL] the judgment vocabulary came out whole (JL: "what does the design mean? I didn't get it? … maybe we don't need to have these concept … we just need to show these skills and the user can drag and rank them themselves"): relations, the aligned ✓, and drift dates left the store and the cards, the order became the one judgment saved by dragging through the new /_board/skill-order, /_board/skill-verify was removed, all 15 live stores migrated in place with the designs-first display order preserved as the initial rank, and the extracted skill moved to 0.2.0 the same hour.
- 260816 · [REVISE-CC] the surface caught up with the night's last ruling (JL: one tab, with the index to go back to): §3 gained the two-depth figure, card INDEX then the skill in the same frame with ← ☰ →, and the Opening's name-click line follows, and the retired 🔍 staging tab left the state line; the tab machinery's removal lives in live/shell.py and the index/card view in live/skillmap.py.
- 260816 0056 · [CHECK-CC] closed on JL's word ("so are we good to close it now?") after verifying every aim on disk: A1.2/A2.2/A3.1 by QPf3's two rows worked from JL's browser, P1 by the generic `_in_plugin` boundary in `src/common.py` plus a clean build around live skill/ folders; the one leftover, QPf6's CC-declared row awaiting JL, is recorded in States rather than holding the page open.
- 260815 2258 · [REVISE-CC] the name-click grew up (JL: "open a new small tab, the whole split should be the skill, like the display split, with ← and →"): the inline lazy iframe of 2240 is retired, the 🛠 card's NAME now posts to the shell, which stages a 🔍 Skill tab framing `/_board/skillview`, and the view itself carries ← → over the page's skills in card order with arrow keys live; standalone workbenches fall back to a browser tab.
- 260815 2240 · [REVISE-CC] two workbench rulings landed (JL: "only keep the most relative ones" · "each skills we can click and show its content"): pruning became a tombstone, so a person's not-relevant survives every refresh with the removed names in a ↩-restorable fold, and the card's NAME began toggling the skill's live bundle view inline as a lazy iframe; my test tombstone was reverted, because pruning is a person's judgment.
- 260815 · [DRAFT-CC] page born with the build (JL ruled the plugin into being the same hour): A1/A2 record what shipped and was route-tested, and the store format and refresh rule are written as the contract; the relation vocabulary and drift rule this draft carried were flattened away 260816.
