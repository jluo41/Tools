---
name: logseq-queries
description: Write LogSeq simple queries and advanced Datalog queries to filter, search, and aggregate blocks and pages. Use when the user wants to query their LogSeq graph, create dynamic views, filter tasks, or build advanced database queries with Datalog.
---

# LogSeq Queries

LogSeq provides two query systems: **simple queries** for common filtering, and **advanced queries** using Datalog for full database access. Both render live, updating results inline.

## Simple Queries

### Basic Syntax

Type `/query` to insert a query block:

```markdown
{{query search term}}
{{query [[page reference]]}}
```

### Boolean Operators

```markdown
{{query (and [[tag1]] [[tag2]])}}                Blocks with BOTH tags
{{query (or [[tag1]] [[tag2]])}}                 Blocks with EITHER tag
{{query (and [[tag2]] (not [[tag1]]))}}          tag2 but NOT tag1
```

Operators nest freely:

```markdown
{{query (and (or [[project]] [[task]]) (not [[archived]]))}}
```

### Filters

**between** — Date range (journal pages):

```markdown
{{query (between -7d today)}}
{{query (between [[Dec 5th, 2020]] [[Dec 7th, 2020]])}}
{{query (between -2w today)}}
```

Time units: `min` (minutes), `h` (hours), `d` (days), `w` (weeks), `m` (months), `y` (years).
Signs: `+` (future), `-` (past).
Built-in symbols: `today`, `yesterday`, `tomorrow`, `now`.

**task** — Filter by task marker:

```markdown
{{query (task TODO)}}
{{query (task NOW LATER)}}
{{query (task TODO DOING DONE)}}
```

**priority** — Filter by priority level:

```markdown
{{query (priority A)}}
{{query (priority A B)}}
```

**property** — Match blocks by property value:

```markdown
{{query (property type book)}}
{{query (property status active)}}
```

**page-property** — Filter by page-level property:

```markdown
{{query (page-property type project)}}
{{query (page-property status "in-progress")}}
```

**page-tags** — Filter pages by their tags:

```markdown
{{query (page-tags project)}}
{{query (page-tags book)}}
```

**all-page-tags** — Return all tags used across pages:

```markdown
{{query (all-page-tags)}}
```

**page** — Filter by specific page name:

```markdown
{{query (page "my page name")}}
```

**namespace** — Filter by namespace hierarchy:

```markdown
{{query (namespace projects)}}
```

**sort-by** — Sort results by property:

```markdown
{{query (and (task NOW LATER) (sort-by created-at desc))}}
{{query (and (property type book) (sort-by rating asc))}}
```

Accepts any user property or built-in `created-at` / `updated-at`. Order: `desc` (default) or `asc`.

### Combining Filters

```markdown
{{query (and (task TODO) [[project]] (between -7d today))}}
{{query (and (task NOW LATER) (priority A) (sort-by created-at desc))}}
{{query (and (page-tags book) (page-property status "reading"))}}
```

---

## Advanced Queries (Datalog)

Advanced queries use Datalog (via Datascript) to query LogSeq's internal database directly. They provide full power over block, page, and file data.

### Query Structure

Wrap in a query block:

```clojure
#+BEGIN_QUERY
{:title  [:h2 "Query Title"]
 :query  [:find (pull ?b [*])
          :in $ ?input1
          :where
          [?b :block/marker "TODO"]]
 :inputs [:today]
 :result-transform (fn [result] ...)
 :view (fn [result] [:div ...])
 :collapsed? false
 :group-by-page? false
 :remove-block-children? false
 :breadcrumb-show? true}
#+END_QUERY
```

| Key | Required | Description |
|-----|----------|-------------|
| `:title` | No | Title as string or Hiccup (e.g., `[:h2 "Title"]`) |
| `:query` | **Yes** | Datalog query with `:find`, `:in`, `:where` |
| `:inputs` | No | Values bound to `:in` variables |
| `:rules` | No | Custom Datalog rules (bound to `%` in `:in`) |
| `:result-transform` | No | Function to transform results before rendering |
| `:view` | No | Custom Hiccup rendering function |
| `:collapsed?` | No | Collapse results by default (true/false) |
| `:group-by-page?` | No | Group results by page |
| `:remove-block-children?` | No | Exclude child blocks from results |
| `:breadcrumb-show?` | No | Show/hide breadcrumbs (default true) |

### :find Clause

Specifies what to return:

```clojure
[:find (pull ?b [*])]              Full block entity (most common)
[:find ?name]                      Single variable
[:find (count ?b)]                 Aggregation
[:find ?name ?content]             Multiple variables
```

`(pull ?b [*])` returns all attributes of the block entity. This is the standard pattern for block-level results.

### :in Clause

Declares input parameters:

```clojure
[:in $]                            Database only (default, can omit)
[:in $ ?variable]                  Database + one input
[:in $ ?var1 ?var2]                Database + multiple inputs
[:in $ %]                          Database + rules
[:in $ ?var1 ?var2 %]              Database + inputs + rules
```

`$` = the database (always first). `%` = rules (from `:rules` key).

### :where Clause

Contains filtering patterns. Each clause is `[entity attribute value]`:

```clojure
:where
[?b :block/marker "TODO"]          Block has marker "TODO"
[?b :block/content ?content]       Bind content to ?content
[?b :block/page ?p]                Block belongs to page ?p
[?p :block/name "my-page"]         Page name equals "my-page"
[?b :block/refs ?ref]              Block references ?ref
[?b :block/properties ?props]      Block has properties
[?b :block/scheduled ?d]           Block has scheduled date
[?b :block/deadline ?d]            Block has deadline
[?b :block/priority "A"]           Block has priority A
[?b :block/marker _]               Block has any marker (_ = wildcard)
```

**IMPORTANT**: Page names are stored as **lowercase** in the database. Always use lowercase in name comparisons.

---

## Database Schema

### Block Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `:block/uuid` | UUID | Unique block identifier |
| `:block/content` | String | Raw text content |
| `:block/marker` | String | Task marker: TODO, DOING, DONE, LATER, NOW, WAITING, CANCELED |
| `:block/priority` | String | Priority: A, B, C |
| `:block/page` | Ref | Parent page entity |
| `:block/parent` | Ref | Parent block entity |
| `:block/refs` | Ref (many) | Page/block references in content |
| `:block/path-refs` | Ref (many) | All ancestor references |
| `:block/tags` | Ref (many) | Block tags |
| `:block/properties` | Map | User-defined properties (key-value) |
| `:block/scheduled` | Integer | Scheduled date as YYYYMMDD integer |
| `:block/deadline` | Integer | Deadline date as YYYYMMDD integer |
| `:block/collapsed?` | Boolean | Block collapsed state |
| `:block/created-at` | Integer | Creation timestamp (Unix ms) |
| `:block/updated-at` | Integer | Modification timestamp (Unix ms) |
| `:block/format` | Keyword | `:markdown` or `:org` |
| `:block/level` | Integer | Indentation level |
| `:block/name` | String | Page name (lowercase, page entities only) |
| `:block/original-name` | String | Original page name (preserves case) |
| `:block/namespace` | Ref | Namespace parent page |
| `:block/alias` | Ref (many) | Alias pages |
| `:block/journal?` | Boolean | Whether this is a journal page |
| `:block/journal-day` | Integer | Journal date as YYYYMMDD integer |
| `:block/children` | Ref (many) | Child block entities |
| `:block/pre-block?` | Boolean | Pre-block (page properties block) |
| `:block/file` | Ref | Source file entity |

### Page-Specific Attributes

Pages are blocks with `:block/name` set. These additional attributes apply:

| Attribute | Type | Description |
|-----------|------|-------------|
| `:page/name` | String | Page name (lowercase) |
| `:page/original-name` | String | Original case page name |
| `:page/file` | Ref | Source file |
| `:page/tags` | Ref (many) | Page tags |
| `:page/alias` | Ref (many) | Page aliases |
| `:page/properties` | Map | Page-level properties |
| `:page/journal?` | Boolean | Is journal page |
| `:page/journal-day` | Integer | Journal date (YYYYMMDD) |

### File Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `:file/path` | String | File path (unique) |
| `:file/created-at` | Integer | Creation timestamp |
| `:file/last-modified-at` | Integer | Last modified timestamp |

---

## Special Input Variables

### Page and Block Inputs

| Input | Description |
|-------|-------------|
| `:current-page` | Lowercase name of the current page |
| `:query-page` | Lowercase name of the page containing the query |
| `:current-block` | Database ID of the current block |
| `:parent-block` | Database ID of the parent block |

### Date Inputs

| Input | Description |
|-------|-------------|
| `:today` | Today's date (YYYYMMDD integer) |
| `:yesterday` | Yesterday's date |
| `:tomorrow` | Tomorrow's date |
| `:right-now-ms` | Current timestamp in milliseconds |

### Relative Date Inputs

Format: `:<sign><amount><unit>`

| Input | Description |
|-------|-------------|
| `:-7d` | 7 days ago |
| `:+10d` | 10 days from now |
| `:-2w` | 2 weeks ago |
| `:-1m` | 1 month ago |
| `:+1y` | 1 year from now |

Units: `d` (days), `w` (weeks), `m` (months), `y` (years).

### Timestamp Suffixes

For precise time-of-day matching:

| Suffix | Description |
|--------|-------------|
| `:-1d-start` | Yesterday 00:00:00.000 |
| `:-1d-end` | Yesterday 23:59:59.999 |
| `:today-start` | Today midnight |
| `:today-end` | Today end of day |
| `:+1d-14` | Tomorrow 2:00 PM |
| `:+1d-1430` | Tomorrow 2:30 PM |

---

## Built-in Rules

Predefined rules usable directly in `:where` clauses:

```clojure
(task ?b #{"TODO" "NOW" "DOING"})          Match task markers (set)
(priority ?b #{"A" "B"})                   Match priorities (set)
(property ?b :key "value")                 Block property equals value
(has-property ?b :key)                     Block has property (any value)
(page-property ?page :key "value")         Page property equals value
(has-page-property ?page :key)             Page has property
(page-ref ?b ?page-name)                   Block references a page
(between ?b ?start ?end)                   Block in date range
(block-content ?b "search string")         Block content contains string
(namespace ?p "parent-namespace")          Page in namespace
```

---

## Logic Operators

### OR — Match any condition

```clojure
(or
  [?b :block/marker "TODO"]
  [?b :block/marker "DOING"])
```

### OR-JOIN — OR with explicit variable binding

```clojure
(or-join [?b]
  [?b :block/scheduled ?d]
  [?b :block/deadline ?d])
```

### NOT — Exclude matches

```clojure
(not [?b :block/marker "DONE"])
```

### NOT-JOIN — NOT with explicit variable binding

```clojure
(not-join [?b]
  [?b :block/page ?excluded-page]
  [?excluded-page :block/name "archive"])
```

---

## Predicate Functions

Clojure functions usable in `:where` clauses within square brackets:

### Comparison

```clojure
[(> ?d ?start)]
[(< ?d ?end)]
[(>= ?d ?start)]
[(<= ?d ?end)]
[(= ?val "string")]
[(not= ?val "excluded")]
```

### String Functions

```clojure
[(clojure.string/includes? ?content "search term")]
[(clojure.string/starts-with? ?content "prefix")]
[(clojure.string/ends-with? ?content "suffix")]
[(clojure.string/lower-case ?str) ?lower]
[(clojure.string/upper-case ?str) ?upper]
```

### Regular Expressions

```clojure
[(re-pattern "regex-pattern") ?regex]
[(re-find ?regex ?content)]
```

### Collection and Map Access

```clojure
[(get ?props :key) ?val]                   Get property value from map
[(get ?props :key "default") ?val]         With default value
[(contains? #{"TODO" "DOING"} ?marker)]    Set membership check
[(count ?collection) ?n]                   Count items
```

### Missing Attribute Check

```clojure
[(missing? $ ?b :block/scheduled)]         Block has no scheduled date
[(missing? $ ?b :block/deadline)]          Block has no deadline
```

### Math

```clojure
[(- ?timestamp 259200000) ?three-days-ago]  Subtract milliseconds
[(+ ?val 1) ?incremented]                   Addition
[(* 1.0 ?num) ?float]                       Convert to float
```

---

## Custom Rules

Define reusable patterns in `:rules` or inline in `:inputs`.

### Via :rules parameter

```clojure
{:query [:find (pull ?b [*])
         :in $ %
         :where (url-block ?b)]
 :rules [[(url-block ?b)
           [?b :block/content ?content]
           [(clojure.string/starts-with? ?content "https://")]]]}
```

### Via :inputs parameter (inline)

```clojure
{:query [:find (pull ?b [*])
         :in $ ?search %
         :where
         (content-match ?b ?search)]
 :inputs ["TODO"
          [[(content-match ?b ?term)
            [?b :block/content ?content]
            [(clojure.string/includes? ?content ?term)]]]]}
```

The `%` in `:in` binds to rules. When using inline rules in `:inputs`, the rules definition is the last element of the inputs array.

---

## Result Transform

Transform results with a Clojure function before rendering:

### Sort by priority

```clojure
:result-transform
  (fn [result]
    (sort-by (fn [h] (get h :block/priority "Z")) result))
```

### Sort by creation date

```clojure
:result-transform
  (fn [result]
    (sort-by (fn [h] (get h :block/created-at)) result))
```

### Reverse order

```clojure
:result-transform
  (fn [result] (reverse result))
```

---

## Custom Rendering (:view)

Render results with Hiccup (Clojure HTML DSL):

```clojure
:view (fn [result]
        [:div.flex.flex-col
         (for [page result]
           [:a {:href (str "#/page/" page)}
            (clojure.string/capitalize page)])])
```

Hiccup syntax: `[:tag.css-class {:html-attrs} children]`

### Tag list example

```clojure
:view (fn [tags]
        [:div
         (for [tag (flatten tags)]
           [:a.tag.mr-1 {:href (str "#/page/" tag)}
            (str "#" tag)])])
```

---

## Query Display as Table

Control table display via block properties on the query block:

```markdown
- #+BEGIN_QUERY
  ...
  #+END_QUERY
  query-table:: true
  query-properties:: [:block/content :priority :status]
  query-sort-by:: priority
  query-sort-desc:: false
```

---

## Complete Examples

### All open tasks

```clojure
#+BEGIN_QUERY
{:title "All Open Tasks"
 :query [:find (pull ?b [*])
         :where
         [?b :block/marker ?m]
         [(contains? #{"TODO" "DOING" "NOW" "LATER"} ?m)]]}
#+END_QUERY
```

### Tasks on current page

```clojure
#+BEGIN_QUERY
{:title "Tasks on this page"
 :query [:find (pull ?b [*])
         :in $ ?current-page
         :where
         [?p :block/name ?current-page]
         [?b :block/page ?p]
         [?b :block/marker ?m]
         [(contains? #{"TODO" "DOING"} ?m)]]
 :inputs [:current-page]}
#+END_QUERY
```

### Blocks referencing a specific page

```clojure
#+BEGIN_QUERY
{:title "Blocks about [[project]]"
 :query [:find (pull ?b [*])
         :where
         [?p :block/name "project"]
         [?b :block/refs ?p]]}
#+END_QUERY
```

### Property matching

```clojure
#+BEGIN_QUERY
{:title "Books I'm reading"
 :query [:find (pull ?b [*])
         :where
         (property ?b :type "book")
         (property ?b :status "reading")]}
#+END_QUERY
```

### Journal blocks in the last 7 days

```clojure
#+BEGIN_QUERY
{:title "Last 7 days"
 :query [:find (pull ?b [*])
         :in $ ?start ?today
         :where
         [?b :block/page ?p]
         [?p :block/journal-day ?d]
         [(>= ?d ?start)]
         [(<= ?d ?today)]]
 :inputs [:-7d :today]}
#+END_QUERY
```

### Upcoming deadlines (next 7 days)

```clojure
#+BEGIN_QUERY
{:title "Upcoming Deadlines"
 :query [:find (pull ?b [*])
         :in $ ?start ?next
         :where
         (or
           [?b :block/scheduled ?d]
           [?b :block/deadline ?d])
         [(> ?d ?start)]
         [(< ?d ?next)]]
 :inputs [:today :+7d]
 :collapsed? false}
#+END_QUERY
```

### Active tasks sorted by priority

```clojure
#+BEGIN_QUERY
{:title "Active Tasks by Priority"
 :query [:find (pull ?b [*])
         :where
         [?b :block/marker ?m]
         [(contains? #{"TODO" "DOING" "NOW"} ?m)]]
 :result-transform
   (fn [result]
     (sort-by (fn [h] (get h :block/priority "Z")) result))
 :collapsed? false}
#+END_QUERY
```

### Pages with a specific tag

```clojure
#+BEGIN_QUERY
{:title "Project Pages"
 :query [:find ?name
         :where
         [?t :block/name "project"]
         [?p :block/tags ?t]
         [?p :block/original-name ?name]]
 :view (fn [result]
         [:div
          (for [name (flatten result)]
            [:a.mr-2 {:href (str "#/page/" name)} name])])}
#+END_QUERY
```

### Blocks containing a regex pattern

```clojure
#+BEGIN_QUERY
{:title "Blocks with URLs"
 :query [:find (pull ?b [*])
         :where
         [?b :block/content ?c]
         [(re-pattern "https?://\\S+") ?regex]
         [(re-find ?regex ?c)]]}
#+END_QUERY
```

### Count blocks per page

```clojure
#+BEGIN_QUERY
{:title "Block count on this page"
 :query [:find (count ?b)
         :in $ ?current-page
         :where
         [?p :block/name ?current-page]
         [?b :block/page ?p]]
 :inputs [:current-page]}
#+END_QUERY
```

---

## Common Patterns and Tips

1. **Always use lowercase** for page names in `:where` clauses — LogSeq stores names lowercase
2. **Use `(pull ?b [*])`** for block results — this is the standard pattern that renders properly
3. **Use sets for multiple values** — `#{"TODO" "DOING"}` instead of separate OR clauses
4. **Date integers are YYYYMMDD** — e.g., January 15, 2025 = `20250115`
5. **Wildcard `_`** matches any value — `[?b :block/marker _]` finds blocks with any marker
6. **Debug with simple queries first** — verify your logic with `{{query}}` before converting to Datalog
7. **`:inputs` order must match `:in` order** — first input binds to first variable after `$`

## References

- [LogSeq Advanced Queries Documentation](https://docs.logseq.com/#/page/advanced%20queries)
- [LogSeq Simple Queries](https://docs.logseq.com/#/page/queries)
- [Datascript Query Syntax](https://github.com/tonsky/datascript)
- [LogSeq Community Hub - Advanced Queries](https://hub.logseq.com/features/av5LyiLi5xS7EFQXy4h4K8/getting-started-with-advanced-queries/8xwSRJNVKFJhGSvJUxs5B2)
