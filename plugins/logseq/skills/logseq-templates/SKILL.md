---
name: logseq-templates
description: Create and use LogSeq templates with dynamic variables for reusable block structures. Use when the user wants to create templates, use dynamic date or time variables, or set up recurring journal structures in LogSeq.
---

# LogSeq Templates

Templates in LogSeq are reusable block structures that can include dynamic variables. They are defined as blocks with the `template` property and inserted via the `/Template` slash command.

## Defining Templates

### Method 1: Right-Click Menu

1. Create a block with desired content (including child blocks)
2. Right-click the block's bullet point
3. Select "Make Template"
4. Enter a template name and click Submit

### Method 2: Manual Property

Add the `template` property directly:

```markdown
- My Template Name
  template:: my-template
  template-including-parent:: false
  - First child block
  - Second child block
    - Nested content
```

## Template Properties

| Property | Values | Description |
|----------|--------|-------------|
| `template` | String | Name of the template (used for lookup) |
| `template-including-parent` | `true` / `false` | Whether to include the parent block when inserting |

When `template-including-parent:: false` (recommended for most cases), only the child blocks are inserted. When `true` or omitted, the parent block and all children are inserted.

## Inserting Templates

1. Type `/` in any block
2. Select **Template** from the slash command menu
3. Choose the desired template from the list
4. Press Enter

The template content is copied into the current location with dynamic variables resolved.

## Dynamic Variables

Dynamic variables use `<% variable %>` syntax. They resolve to actual values at the moment of insertion.

| Variable | Syntax | Resolves To |
|----------|--------|-------------|
| Today | `<% today %>` | `[[2025-01-15]]` (today's journal link, format depends on config) |
| Yesterday | `<% yesterday %>` | `[[2025-01-14]]` |
| Tomorrow | `<% tomorrow %>` | `[[2025-01-16]]` |
| Current time | `<% time %>` | `22:44` (HH:MM format) |
| Current page | `<% current page %>` | `[[Current Page Name]]` |

### Natural Language Dates

LogSeq supports NLP date parsing in template variables:

```markdown
<% last friday %>         Resolves to last Friday's journal link
<% next monday %>         Resolves to next Monday's journal link
<% last week %>           Resolves to last week's date
<% in two days %>         Resolves to the date 2 days from now
```

## Examples

### Weekly Planning

```markdown
- Weekly Planning
  template:: weekplan
  template-including-parent:: false
  - ## Week of <% today %>
    - **Goals**
      - TODO Goal 1
      - TODO Goal 2
      - TODO Goal 3
    - **Schedule**
      - Monday
      - Tuesday
      - Wednesday
      - Thursday
      - Friday
    - **Review** (due <% next friday %>)
      - What went well?
      - What to improve?
      - Key learnings
```

### Meeting Notes

```markdown
- Meeting Notes Template
  template:: meeting
  template-including-parent:: false
  - ## Meeting: <% current page %> — <% today %> <% time %>
    - **Attendees**
      -
    - **Agenda**
      -
    - **Discussion**
      -
    - **Action Items**
      - TODO
    - **Next Meeting**
      -
```

### Daily Journal

```markdown
- Daily Journal
  template:: daily
  template-including-parent:: false
  - ## <% today %>
    - **Morning Review**
      - How am I feeling?
      - Top 3 priorities:
        - TODO Priority 1
        - TODO Priority 2
        - TODO Priority 3
    - **Work Log**
      -
    - **Evening Reflection**
      - What did I accomplish?
      - What did I learn?
      - Grateful for:
```

### Project Kickoff

```markdown
- Project Template
  template:: project-kickoff
  template-including-parent:: false
  - tags:: [[project]], [[active]]
    status:: planning
    start-date:: <% today %>
  - ## Objectives
    -
  - ## Key Results
    - TODO KR1
    - TODO KR2
    - TODO KR3
  - ## Timeline
    - Start: <% today %>
    - Milestone 1:
    - Milestone 2:
    - Target completion:
  - ## Resources
    -
  - ## Notes
    -
```

### Quick Capture

```markdown
- Quick Capture
  template:: capture
  template-including-parent:: false
  - **Captured** <% today %> <% time %>
    source::
    tags::
    -
```

## Finding All Templates

Use a simple query to list all templates in your graph:

```markdown
{{query (property template)}}
```

## Tips and Limitations

1. **Changes don't propagate** — Editing a template source does NOT update previously inserted instances
2. **Use `template-including-parent:: false`** for most templates — avoids inserting the template definition block itself
3. **Page properties caveat** — Templates with `template-including-parent:: false` may not properly set page-level properties when inserted as the first block
4. **Dynamic variables only resolve on insert** — They become static text after insertion
5. **Organize templates on a dedicated page** — Create a `[[Templates]]` page to keep all templates discoverable
6. **Nest templates** — Templates can contain page references and block embeds for modular composition

## References

- [LogSeq Templates Documentation](https://docs.logseq.com/#/page/templates)
- [LogSeq Dynamic Variables](https://docs.logseq.com/#/page/dynamic%20variables)
