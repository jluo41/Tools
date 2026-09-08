# value-rules · machine checks for a value Result

Current value Evidence Items are served by a consumer-owned Local Run and an
accepted Result.  These rules check the machine-verifiable part of that
contract; a person's interpretation or decision remains outside this file.

## Rules

```text
R1  THE PROSE NUMBER EQUALS THE RESULT NUMBER. Every value the page states
    from this item appears, character for character, in the accepted Result.
    A rounded number names its rounding.
R2  THE RESULT RESOLVES. The Local Run and its Result path exist, the Result
    names the Supporting Run(s), and the item points to that exact receipt.
R3  PROVENANCE IS COMPLETE. Each pulled value names source, run, unit/window,
    and sha256 (when the source is a file); hashes match the bytes on disk.
R4  THE RESULT ANSWERS THE ITEM. The Result's scope and fields address the
    Evidence Item specification, not a topic-similar neighbour.
R5  SERVES NAMES REAL ADDRESSES. Every page/division address in `serves:`
    exists in the approved outline for the round that owns the item.
R6  STATE IS CURRENT. An item is one of `planned · commissioned · landed ·
    embedded · deferred · failed · concern`; an obsolete or unknown state is
    a finding, not an implicit pass.
R7  THE STAKE WALL HOLDS. Supporting Run artifacts contain no consumer prose
    or page-only claim; the Local Run is the only place that adapts them for
    this Evidence Item.
R8  ONE ITEM, ONE SPECIFICATION. Duplicate Evidence Items with the same
    type/name and scope are a defect; reuse the immutable Result instead.
R9  THE AGENT WRITES `checked:`, NEVER A HUMAN DECISION. A passing check may
    record `checked: ✅ auto <YYMMDD> · value-rules R1-R8 pass`; it may not
    write `approved:`, `verified:`, `accepted:`, or a person's ruling.
```

## Out of scope

```text
"is this number important enough to report?"
"was this the right item to specify?"
"does this number change the page's argument?"
```

Those are page decisions.  If a Supporting Run is stale or a Local Run is
missing, reopen the item and start the shallowest bounded Run required; do not
create a parallel answer bank or question channel.
