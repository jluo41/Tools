# Board naming: the folder says its subject, and the count follows

state: ✅ SETTLED · naming and cardinality ruled 260820
owner: JL

## Opening

What is a board called, and how many of each may an Application hold?

A board's folder name carries its subject: the data for an InsightBoard, the topic for a DesignBoard. `InsightBoard/` alone tells a reader the kind and nothing else, and a reader opening an Application wants to know which data and which topic before opening anything. Naming the two subjects independently is also what makes the count free, so two boards became the common case rather than the limit.

### Writing Style

State the form, then one real example, then what the form makes possible. A naming page that gives only a template teaches nothing about why the template has that shape.

## Diagram

**The form**: subject, then the literal kind.

```text
<DataSubject>-InsightBoard      the subject is the DATA
<DesignTopic>-DesignBoard       the subject is the TOPIC

SmsClickR4-InsightBoard/        ls *-InsightBoard  finds every one
YoungMaleRefill-DesignBoard/    ls *-DesignBoard   finds every one
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

The subject is PascalCase and the suffix is the literal kind, so the suffix is greppable and the subject is readable. A board is renamed only with its PageX bindings, because those bind by path and a rename breaks every one that points into it.

#### 2 · Why the count is free

The two subjects are named independently, so nothing in the naming forces a pair. An Application may hold several InsightBoards when it reads distinct data, several DesignBoards when it designs for distinct topics, and any DesignBoard may PageX-bind any InsightBoard. Two is what most Applications need, not what the model allows.

#### 3 · No date suffix

The `<NN>-<topic>-<YYMMDD>` rule governs boards newly opened under `diagram/`, which are design records dated at birth. These are runtime boards that live as long as the Application does, so a birth date on the folder would age into noise.

#### 4 · Group folders carry their token

Inside a board, a group folder is `<NN>-<TOKEN>-<slug>`: `0-M-meta/`, `1-I-insights/`, `0-A-brief/`, `1-D-design/`. The token is what the engine resolves a group by, and a folder without one parses to no group, which was a real failure before the first runtime board was built. The number is its place in `## Pages`.

#### 5 · Page ids inside a board

`M00-meta`, `I<NN>-<slug>`, `A00-brief`, `D<NN>-<audience>-<job>`. The letter is the family and matches its group token; the digits order pages inside it. Four places in the engine resolve them: `PAGENAME`, `page_files`, the `## Pages` registry, and `parse.py`.

## Aims

### A1 · Contract
- A1.1 · A folder name says which data or which topic before anyone opens it.
  **Done when:** every runtime board is `<Subject>-<Kind>` and the kind is greppable.

#### P · Cardinality
- P1 · Nothing in the naming caps the number of boards.
  **Done when:** the subjects are independent and any DesignBoard may bind any InsightBoard.

#### P2 · Buildability
- P2.1 · The documented names are the ones that actually build.
  **Done when:** a worked specimen using these names passes build and check.

## States

### A1 · Contract
- ✅ A1.1 · Fixed in Application 0.10.0 and stated in the family README.

#### P · Cardinality
- ✅ P1 · Stated in the public door; the fixture uses one of each and neither name implies the other.

#### P2 · Buildability
- ✅ P2.1 · `_fixture/SmsClickR4-InsightBoard` and `_fixture/YoungMaleRefill-DesignBoard` each build 2 pages at 0 error, 0 warn.

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/SKILL.md`
  The runtime folder map and the naming rule.

### 🧪 Checks
- `../../_fixture/README.md`
  The worked specimen that proves the names build.

## Law

A runtime board's folder name states its subject, and its group folders state their token. A name that says only the kind makes a reader open the folder to learn what it is for.

## Log

260820 · Ruled after the two-board split (JL: "the InsightBoard and DesignBoard should have some name, like what is the data, and what is the topic of the design"). Group-token folders and the engine's page-id families were added when the first runtime board failed to build.
