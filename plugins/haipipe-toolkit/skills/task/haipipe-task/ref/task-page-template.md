<!-- TASK PAGE TEMPLATE · owned by haipipe-task/ref/task-page.md
     Copy into one canonical tNN_<task>/ Folder as tNN_<task>.md.
     Delete every guide comment after satisfying it. -->

# <the question this Task was run to answer, stated in three to five words>
state: 🔴 OPEN
owner: <who>
folder-kind: task
task-type: <data|raw|algo|fit|eval|display|individual|agent|endpoint|page|stata>
task: .

## Opening
<!-- One visible paragraph: what this Task is, why its question matters, and
     what this Page lets the reader decide. Opening orients; Introduction below
     begins the technical argument. -->

## Content
<!-- SHAPE chooses FLAT or NESTED using one test: does another topic need its
     own Data or Method? The closed role order is Introduction, Concept,
     Landscape, Data, Method, Result, Conclusion. At least one Result is
     required; Conclusion is page-level, exactly once, and always last.
     The rendered Outline is generated from outline/<stem>-outline-v<N>.md;
     do not author a second ## Outline section here. Each prose paragraph
     realizes exactly one plan Bullet and ends on its final source line with
     the HTML-comment backlink specified in ref/task-page.md. -->

### 1 · Introduction · <what this Folder was run to settle and what the report claims>
<!-- Every division begins with one captioned face diagram that previews this
     division's argument. Replace both placeholders; do not add a Page-level
     Diagram section. -->
**Division map — <what this introduction connects>**
```text
<question> ─▶ <scope> ─▶ <claim>
```

### 2 · Data · <what went in and the fact a reader needs to trust the Result>
**Division map — <what this data establishes>**
```text
<source> ─▶ <selection> ─▶ <analysis-ready input>
```

### 3 · Method · <what was run and what it was chosen instead of>
**Division map — <how the method turns input into an answer>**
```text
<input> ─▶ <method> ─▶ <estimand or output>
```

### 4 · Result · <what came out, expressed as a finding rather than a file>
<!-- Every shown number names its full Run id. A new Run adds a READING row;
     it earns a new Result division only when it carries a new message. -->
**Division map — <the evidence path to this finding>**
```text
<accepted Result + run id> ─▶ <finding> ─▶ <implication>
```

### 5 · Result · <what remains unresolved>
<!-- Keep the residual visible. Delete this division only when the accepted
     Runs actually settled the full question. -->
**Division map — <the boundary of the current evidence>**
```text
<known> ─▶ <residual> ─▶ <next discriminating Run>
```

### 6 · Conclusion · <what the accepted Results mean and what should run next>
**Division map — <the final reading and next decision>**
```text
<accepted findings> ─▶ <reading> ─▶ <close or next Run>
```

<a id="reading-current"></a>
#### READING · current
| ID | Topic | Verdict Run | Ruling | Meaning |
|---|---|---|---|---|
| R01 | <topic> | <bNNjNNtNNrNN> | ⬜ unread | <plain-language meaning after reading> |

answers        <Aim ids now answered>
not answered   <what these Runs did not settle>
next run       <full planned Run id, or "none: the question is closed">

## Aims
### A1 · ❓ <same name as Content division 1>
- ⬜ A1.1 · <durable target>
  **Done when:** <observable test>
  **Now:** <current fact, with the owning Run or Page address when relevant>

## Law
<!-- Dated phase, rerun, and gate history lives in outline/<stem>-log.md.
     Task machinery is indexed through outline/<stem>-files.md. -->
