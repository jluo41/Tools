---
name: logseq-markdown
description: Create and edit LogSeq block-based markdown with properties, wikilinks, block references, embeds, tasks, and namespaces. Use when working with .md files in a LogSeq graph, or when the user mentions LogSeq blocks, properties, namespaces, or journal pages.
---

# LogSeq Block-Based Markdown

LogSeq uses a block-based outliner approach to markdown. Every piece of content is a **block** (a bullet point), and indentation creates parent-child relationships. This is fundamentally different from document-based editors like Obsidian.

## Block Structure

Every line in a LogSeq markdown file is a block, prefixed with `- `:

```markdown
- This is a top-level block
	- This is a child block (indented with tab)
		- This is a grandchild block
	- Another child block
```

**Critical rules:**
- Use **tabs** (not spaces) for indentation in LogSeq markdown files
- Every block gets a unique UUID automatically assigned by LogSeq
- Pages are root-level containers; every block belongs to a page
- Journal pages use date-based filenames (e.g., `2026_02_12.md`)
- Date links use ISO format: `[[2026-02-12]]` (configured via `:journal/page-title-format "yyyy-MM-dd"`)
- Page files go in `pages/` directory, journal files in `journals/` directory

## Text Formatting

| Format | Syntax | Result |
|--------|--------|--------|
| Bold | `**text**` | **bold** |
| Italic | `*text*` | *italic* |
| Strikethrough | `~~text~~` | ~~struck~~ |
| Highlight | `^^text^^` | highlighted |
| Underline | `<ins>text</ins>` | underlined |
| Inline code | `` `code` `` | `code` |
| Superscript | `X^{2}` | X² |
| Subscript | `H_{2}O` | H₂O |

## Headings

Standard markdown headings work within blocks:

```markdown
- # Heading 1
- ## Heading 2
- ### Heading 3
- #### Heading 4
- ##### Heading 5
- ###### Heading 6
```

Note: Headings are less commonly used in LogSeq since the outliner structure provides hierarchy naturally.

## Page References

```markdown
[[page name]]                    Basic page reference (creates page if missing)
#tag                             Single-word tag (equivalent to [[tag]])
#[[multi word tag]]              Multi-word tag
[display text]([[page name]])    Labeled page reference
```

Tags and page references are **functionally identical** in LogSeq — `#project` and `[[project]]` both create/link to the same page.

## Block References

```markdown
((block-uuid))                           Reference a block by its UUID
[display text](((block-uuid)))           Labeled block reference
```

Block references render the referenced block's content inline. Type `((` to trigger autocomplete search.

## Embeds

```markdown
{{embed [[page name]]}}                  Embed entire page content
{{embed ((block-uuid))}}                 Embed a single block and its children
```

Embeds render the full content inline (editable in place), unlike references which are read-only links.

## Links and Images

```markdown
[link text](https://example.com)         External link
![alt text](../assets/image.png)         Local image
![alt text](https://example.com/img.png) Remote image
```

Bare URLs are automatically converted to clickable links.

## Properties

Properties use `key:: value` syntax (note the double colon).

### Page Properties

Must be in the **first block** of the page. They annotate the entire page:

```markdown
- title:: My Project
  tags:: [[project]], [[active]]
  alias:: My Proj, MP
  type:: documentation
  status:: in-progress
```

### Block Properties

Can be on any block. They annotate only that block:

```markdown
- Buy groceries
  priority:: A
  due-date:: [[2025-01-15]]
  estimated-time:: 30min
```

### Built-in Properties (Editable)

| Property | Scope | Description |
|----------|-------|-------------|
| `title` | Page | Override page title (different from filename) |
| `icon` | Page | Icon identifier for the page |
| `tags` | Both | Tags listed in "Pages tagged with X" |
| `alias` | Both | Synonyms for a page (comma-separated) |
| `template` | Both | Designates block as a template |
| `template-including-parent` | Both | Include parent block when inserting template |
| `filters` | Page | Store selected filters for linked references |
| `public` | Page | Include page in export (true/false) |
| `exclude-from-graph-view` | Page | Exclude from global graph |

### System Properties (Auto-managed)

| Property | Scope | Description |
|----------|-------|-------------|
| `id` | Block | Block's UUID |
| `collapsed` | Block | Whether block is collapsed |
| `created-at` | Block | Creation timestamp (Unix ms) |
| `updated-at` | Block | Modification timestamp (Unix ms) |
| `query-table` | Block | Show query results as table |
| `query-properties` | Block | Properties shown in query table |
| `query-sort-by` | Block | Sort property for query table |
| `query-sort-desc` | Block | Sort direction (true = descending) |

### Property Value Types

- **Plain text**: `status:: active`
- **Page references**: `tags:: [[project]], [[important]]`
- **Numbers**: `rating:: 8`
- **Dates**: `due:: [[Jan 15th, 2025]]`
- **Multiple values**: Comma-separated — `tags:: value1, value2, value3`

**Important**: Commas separate multiple values. A value containing a literal comma will be split.

## Task Management

### Task Keywords

LogSeq supports two configurable workflows (Settings > Editor > Preferred workflow):

**Workflow 1 (default)**: `TODO` → `DOING` → `DONE`
**Workflow 2**: `LATER` → `NOW` → `DONE`

Additional markers: `WAITING`, `CANCELED`

```markdown
- TODO Buy groceries
- DOING Write report
- DONE Send email
- LATER Read paper
- NOW Fix critical bug
- WAITING Response from client
- CANCELED Deprecated feature
```

`DONE` items display with strikethrough. Use `/TODO` or click the checkbox to cycle states.

### Priority

```markdown
- TODO [#A] Urgent task
- TODO [#B] Normal priority
- TODO [#C] Low priority
```

### Deadlines and Scheduled Dates

```markdown
- TODO Submit report
  DEADLINE: <2025-01-15 Wed>
  SCHEDULED: <2025-01-10 Mon>
```

Use `/Deadline` or `/Scheduled` slash commands to insert these with a date picker.

## Namespaces

Namespaces create hierarchical page organization using `/`:

```markdown
[[Projects/WebApp]]
[[Projects/WebApp/Frontend]]
[[Projects/WebApp/Backend]]
```

This creates a navigable hierarchy:
- `Projects` (parent page)
  - `Projects/WebApp` (child page)
    - `Projects/WebApp/Frontend` (grandchild)
    - `Projects/WebApp/Backend` (grandchild)

Each namespace level is a separate page with breadcrumb navigation.

## Aliases

Allow a page to be referenced by multiple names:

```markdown
- title:: Artificial Intelligence
  alias:: AI, Machine Intelligence
```

Referencing `[[AI]]` links to the `Artificial Intelligence` page.

## Code Blocks

Inline code: `` `code` ``

Fenced code blocks with syntax highlighting:

````markdown
- ```javascript
  console.log("hello");
  ```
````

Org-mode style:

```markdown
- #+BEGIN_SRC javascript
  console.log("hello");
  #+END_SRC
```

## Math (KaTeX)

```markdown
$E = mc^2$                               Inline math
$$\int_0^\infty e^{-x} dx = 1$$          Block/display math
```

LogSeq uses KaTeX for rendering LaTeX expressions.

## Tables

Standard markdown pipe-delimited tables:

```markdown
- | Header 1 | Header 2 | Header 3 |
  |----------|:--------:|---------:|
  | Left     | Center   | Right    |
  | Cell     | Cell     | Cell     |
```

## Blockquotes

Markdown style:

```markdown
- > This is a blockquote
  > Second line
```

Org-mode style:

```markdown
- #+BEGIN_QUOTE
  This is a blockquote
  #+END_QUOTE
```

## Advanced Commands (Admonition Blocks)

Type `<` in a block to access these org-mode style commands:

```markdown
- #+BEGIN_NOTE
  This is a note
  #+END_NOTE

- #+BEGIN_TIP
  This is a tip
  #+END_TIP

- #+BEGIN_IMPORTANT
  This is important
  #+END_IMPORTANT

- #+BEGIN_CAUTION
  Exercise caution
  #+END_CAUTION

- #+BEGIN_WARNING
  This is a warning
  #+END_WARNING

- #+BEGIN_PINNED
  Pinned content
  #+END_PINNED
```

## Macros

Define custom macros in `logseq/config.edn` under `:macros`:

```clojure
:macros {
  "docs-url" "https://docs.logseq.com/#/page/$1"
  "highlight" "[:mark \"$1\"]"
  "iframe" "<iframe src=\"$1\" style=\"width:100%; height:600px;\"></iframe>"
}
```

Usage: `{{docs-url getting-started}}` — `$1`, `$2`, `$3` are positional arguments.

## Comments

```markdown
- #+BEGIN_COMMENT
  This is only visible in edit mode
  #+END_COMMENT
```

## Horizontal Rules

```markdown
---
```

## Complete Example

A realistic LogSeq page combining multiple features:

```markdown
- title:: Project Alpha
  tags:: [[project]], [[active]]
  alias:: Alpha, PA
  status:: in-progress
  start-date:: [[Jan 10th, 2025]]
- ## Overview
	- This project aims to build a new [[API Gateway]] for the [[Projects/WebApp/Backend]].
	- Key requirements documented in ((block-uuid-here))
- ## Tasks
	- TODO [#A] Design API schema
	  DEADLINE: <2025-01-20 Mon>
		- Reference the [[OpenAPI]] specification
		- Include authentication endpoints
	- DOING [#B] Set up CI/CD pipeline
	  SCHEDULED: <2025-01-15 Wed>
		- Using [[GitHub Actions]]
	- DONE [#C] Initial project setup
- ## Notes
	- #+BEGIN_TIP
	  Use `^^highlight^^` for important terms in documentation
	  #+END_TIP
	- Meeting notes from <% today %>:
		- Discussed timeline with [[John]]
		- Action items tagged with #action
- ## References
	- {{embed [[API Design Principles]]}}
```

## Key Differences from Obsidian

| Feature | LogSeq | Obsidian |
|---------|--------|----------|
| Structure | Block-based outliner (every line is a bullet) | Document-based (free-form markdown) |
| Properties | `key:: value` (inline) | YAML frontmatter (`---` block) |
| Highlight | `^^text^^` | `==text==` |
| Daily notes | Built-in journal system | Optional via plugin |
| Queries | Native Datalog queries | Search + Datalog via plugin |
| Indentation | Tabs in .md files | Spaces or tabs |
| File format | Markdown or Org-mode | Markdown only |
| Callouts | Org-mode `#+BEGIN_NOTE` etc. | `> [!note]` callout syntax |

## References

- [LogSeq Documentation](https://docs.logseq.com/)
- [Markdown Guide - LogSeq](https://www.markdownguide.org/tools/logseq/)
- [LogSeq GitHub](https://github.com/logseq/logseq)
