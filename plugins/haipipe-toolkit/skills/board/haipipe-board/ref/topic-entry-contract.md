# Evidence page and nested QA-probe contract

Use this optional overlay when a Board has one reader-facing evidence page and several neutral requests to run beneath it.
The contract is generic. It names neither a Paper stage nor an evidence bank.
"Evidence page" is the collective name for the two page types this overlay serves: the for-literature page (outward) and the for-value page (inward).

```text
S evidence page                       the ONE board page this overlay adds
  ├── head `route:` line            the type key: outward | inward
  ├── ### E0 · incoming             the queue of collected, untranslated Q-consumers
  ├── ### E<n> · <question>         one Content division per Q-executor conversation
  │     ├── 🔗 QA-probe pointer     the record this division owns, with its status
  │     ├── #### consumers          the Q-consumers served, each with its A-consumer
  │     └── #### answer digest      2-3 lines from the A-executor
  └── probes/<topic>/
       └── one QA-probe = one Q-executor            <n>-<slug>.md · not a page
            ├── consumer trace     audit copy of each Q-consumer
            ├── bank binding       route, bank, target, and state
            └── A-executor         the returned answer
```

An originating delivery page may raise a Q first. The evidence page owns the canonical evidence-routing record, while the QA-probe owns the Q-executor because it is the neutral question another system can answer. The consumer trace is never a second register.

## The head route line

The type key is ONE machine-readable line in the page's metadata head, right after `owner:`/`method:` (JL 260806; it replaces the retired `### Q-consumer register` marker):

```text
route: outward    the questions face published knowledge
route: inward     the questions face results this project must produce
```

An evidence page wears a stage-shaped filename, so only this line separates it from a plain stage page: a page with E divisions and no `route:` head line, or one with any other value, leaves the page's type unresolvable and the page defective. `route: outward` resolves the page to `page-types/haipipe-board-page-for-literature`; `route: inward` resolves it to `page-types/haipipe-board-page-for-value`.

## The E divisions: one per Q-executor conversation

The evidence page organizes its Content BY EXECUTOR (JL 260806). Each division is `### E<n> · <the executor question>`, and one E<n> division binds to exactly one QA-probe (1:1). Many QA-probes across papers may point at one QA-bank; that sharing lives at the bank, never on the page. Inside each E<n> division, in order:

1. a pointer line, `🔗 QA-probe: probes/<topic>/<n>-<slug>.md · state: <its bank-binding state>`
2. a `#### consumers` block: one row per Q-consumer collected from other pages. Each row carries the source page id, the stake in one line, then its A-consumer interpretation, and wears exactly one row state: `⬜` open · SUPPORTED (outward) or BOUND (inward) · DEFERRED, with the reason on the row · WITHDRAWN, because the claim the row served changed
3. a `#### answer digest` block: 2-3 lines from the A-executor. The full text stays in the QA-probe record, one click away; the digest is what a reader scans.

`### E0 · incoming` is the one standing division: the queue where a newly collected Q-consumer waits until PROBE translates it into a new E<n> and opens its QA-probe. A Q-consumer born on ANY page is COLLECTED into the owning topic's E0 first, then promoted.

The page closes only when every E<n> division's consumers are terminal AND E0 is empty. The human gate reads the E divisions, not the QA-probes: an answer sitting in a QA-probe's `#### A-executor` that never became an A-consumer row closes nothing.

## The QA-probe: a record, not a Page

The nested file is a QA-probe ("entry" survives only as an informal alias). It is a RECORD, not a board Page (JL ruling B, 260806): "an entry is a source file the topic page points at, like a PDF; the board renders the topic page, never the entry."

The twin naming law (JL, 260806): one conversation, two QAs. The QA-bank is the original: it lives in the executor's own tree at `tasks|discoveries/…/QA/<n>-<slug>.md`, its `# Q` is the Q-executor and its `## Answer` the A-executor. The QA-probe is the consumer's stub that points at the QA-bank by the `**target**:` path. Word order matters: QA-bank and QA-probe, never bank-QA or probe-QA in a file name. The file-level names "QA-executor" and "QA-consumer" are WRONG and retired: consumer and executor name SLOTS only, and the four slot words are CAPITALS everywhere, including heading slots: Q-consumer, A-consumer, Q-executor, A-executor. `consumer trace` and `bank binding` are not among the four words and stay lowercase.

The naming law on disk: a QA-probe is named `<n>-<slug>.md`, digit first, inside its topic's `probes/<topic>/` folder, and `<n>` restarts at 1 per folder. The digit-first name IS the hiding mechanism, not a style choice: the Board engine's page sweep (`page_files` in `src/common.py`) discovers pages only by the filename prefixes `Q`, `S`, `Agent`, and `Meeting`, so a digit-first file is never swept onto the board, never listed in `## Pages`, and never rendered. Do not "fix" a missing QA-probe by giving it a page-shaped name.

A QA-probe carries no page frame: no `state:` header, no Opening, no Aims, no States, no Log, and no gate; the evidence page carries all of those on its behalf. The record is a `# title` line, a `requires: <evidence-page-id>` line naming the one evidence page whose E division owns it, and exactly one each of the four slots:

```markdown
#### Q-executor
#### consumer trace
#### bank binding
**route**: task | discovery
**bank**: reuse | run | code | new
**target**: <path to the answering QA-bank file>
**state**: planned | commissioned | deferred | read | answered-local
#### A-executor
```

Queue membership is derived, not maintained in another file. `planned`, `commissioned`, and `deferred` are queued. `read` and `answered-local` are resolved.

`cli/check.py` detects this overlay only when an S page carries the head `route:` line. It then checks each QA-probe's direct-topic dependency, slot anatomy (capital slot headings canonical; a lowercase executor slot heading is a `topic-entry-heading-case` WARN, not a second grammar), bank state, the one-E-division-per-record link, and whether each trace id occurs on its parent evidence page.
