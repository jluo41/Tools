# How Content gets its structure
state: ✅ SETTLED
owner: JL
method: compose stage craft, venue form, and accepted upstream requirements at page creation

## Question
Where does the structure of a stage's Content come from?

A generic template is not enough for a real manuscript section, and a venue template alone does not know the paper's accepted claims and narrative. The page creator needs a deterministic composition order that produces explicit headings the page then owns.

## Boundary
- ✅ Covered here
  The sources and precedence used to create a stage or section Content blueprint.
- ↪ Covered elsewhere
  The single page creator is `QC4`; dependency declarations are `QC2`; the Content boundary is `QBa1`.

## Content
### Composition order
```
1. stage template       the disciplinary jobs and gate
2. venue blueprint      section order, reader expectation, length, and style
3. Stage Contracts      accepted upstream requirements and explicit dependencies
4. page authoring       materialize resolved direct headings in ## Content
```

### Ownership after creation
The creator does not keep recomputing the page on every render.
The composed headings become authored Content and change only through normal revision.
Managed Stage Contract text may refresh independently without overwriting Content.

### Template lookup
The stage registry identifies the stage template.
The pinned venue page is the first venue source.
The venue playbook is only a fallback or a deeper source behind the pinned contract.

## Items to Finish
- [x] 🧱 Choose the four-layer composition
      Stage, venue, upstream contracts, and page ownership have an explicit order.
- [ ] 📐 Define merge conflicts
      State what happens when stage craft, venue form, and upstream requirements disagree.
- [ ] 🛠 Put composition behind one creator
      Board shell creation and paper Content composition must happen through one entry.
- [ ] 🧪 Create a venue-aligned section page
      It must be Board-valid and carry the right section jobs without manual restructuring.

## Where we are
The sources and precedence are designed.
The current Board creator still writes a generic stub and the paper worker composes pages by hand.

## Files
- `stages/*/template.md`
  Stage craft.
- `0-lifecycle/2a-venue/S-Venue-0-venue.md`
  Pinned venue structure and style.
- `haipipe-board/stage.py`
  The current shell creator.
