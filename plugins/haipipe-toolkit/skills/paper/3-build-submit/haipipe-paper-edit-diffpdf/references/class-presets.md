# Class Presets

Per-class recommended `latexdiff` flags + silencer protect-blocks. The
auto-detector (`detect-paper-class.sh`) ships these as defaults; users can
override via `config.sh` in the diff subdir.

The principle behind every preset:

- `--exclude-textcmd` lists short top-of-page commands (title, running heads,
  affiliations) that **must NOT** be word-level diffed. These commands have
  fixed-height layout boxes; injecting struck-through old + new text overruns
  the box and breaks page 1.
- `--append-textcmd` lists body-like commands (abstracts, keywords) where
  word-level diff is **wanted**.
- `protect-block:` lists block names whose contents the silencer must NEVER
  touch — usually the same set as `--append-textcmd` (the abstract/title)
  because that's where every change should remain visible regardless of
  audit-fix silencing rules elsewhere.

---

## INFORMS journals (informs0 / informs3 / informs4)

Used for: Management Science, ISR, Marketing Science, Operations Research,
Manufacturing & Service Operations Management, Mathematics of Operations
Research, Organization Science. Class options pick the journal:
`mnsc`, `isre`, `mksc`, `opre`, `msom`, `moor`, `orsc`.

```
--exclude-textcmd     section,subsection,subsubsection,TITLE,RUNTITLE,RUNAUTHOR
--append-textcmd      ABSTRACT,KEYWORDS
--append-context2cmd  abstract,caption
protect-block:        ABSTRACT
protect-block:        TITLE
```

Why: INFORMS uses uppercase macros (`\TITLE{}`, `\RUNTITLE{}`, `\AUTHOR{}`,
`\ABSTRACT{}`). The title block is fixed-height — word-level diff inside
`\TITLE{}` overruns and pushes the title page to page 2.

---

## ACM venues (acmart)

Used for: CHI, KDD, SIGGRAPH, SIGIR, SIGCOMM, NeurIPS-via-acmart, ICSE,
ASE, FSE, etc.

```
--exclude-textcmd     section,subsection,subsubsection,affiliation,thanks
--append-textcmd      title,subtitle,abstract,keywords
--append-context2cmd  abstract,caption
protect-block:        abstract
protect-block:        title
```

Why: acmart uses lowercase standard commands. Affiliation blocks are
multi-line and noisy in diffs. Keywords are short body commands.

---

## IEEE journals & conferences (IEEEtran)

Used for: T-PAMI, JSAC, TWC, TCOM, TSP, TIP, ICC, GLOBECOM, INFOCOM,
ICASSP, etc.

```
--exclude-textcmd     section,subsection,subsubsection,markboth,thanks,IEEEauthorrefmark
--append-textcmd      title,IEEEkeywords,IEEEpubid
--append-context2cmd  abstract,caption
protect-block:        abstract
protect-block:        title
```

Why: `\markboth{}{}` controls the running header — diff inside it produces
header overflow. `IEEEauthorrefmark{N}` is a short ref symbol that can
appear inside diffs as garbage if expanded.

---

## Springer Lecture Notes (llncs / sn-jnl)

Used for: LNCS, LNAI, LNBI; some Nature Springer journals.

```
--exclude-textcmd     section,subsection,subsubsection,institute,thanks
--append-textcmd      title,subtitle,author,abstract,keywords
--append-context2cmd  abstract,caption
protect-block:        abstract
protect-block:        title
```

Why: `\institute{}` blocks are multi-line addresses with email/footnote
hooks; diff inside them is unreadable.

---

## ML conferences (NeurIPS / ICML / TMLR / COLM)

Used for: NeurIPS, ICML, ICLR, COLM, TMLR.

```
--exclude-textcmd     section,subsection,subsubsection,thanks,affiliation
--append-textcmd      title,abstract
--append-context2cmd  abstract,caption
protect-block:        abstract
protect-block:        title
```

Why: NeurIPS-style classes use a custom `\author{}` block with affiliations
and emails packed into one macro — diff inside it would be visual noise.

---

## Elsevier (elsarticle / cas-sc / cas-dc)

Used for: most Elsevier journals.

```
--exclude-textcmd     section,subsection,subsubsection,thanks,address
--append-textcmd      title,author,abstract
--append-context2cmd  abstract,caption
protect-block:        abstract
protect-block:        title
```

---

## Generic LaTeX (article / amsart / book / report / memoir / unknown)

Fallback for anything not listed above. Uses standard LaTeX command names.

```
--exclude-textcmd     section,subsection,subsubsection,thanks,maketitle
--append-textcmd      title,subtitle,author,abstract
--append-context2cmd  abstract,caption
protect-block:        abstract
protect-block:        title
```

This is also what `detect-paper-class.sh` falls back to when the class
isn't recognized.

---

## Adding a new class

1. Identify the class name with `grep '\\documentclass' master.tex`.
2. Read the class .cls/.sty for the top-level commands (`\title{}`,
   `\TITLE{}`, custom journal macros).
3. Decide: which commands have fixed-layout pages (exclude), which are
   body-like (append), which contain only meta/cross-ref content (context2).
4. Add a `case` arm to `detect-paper-class.sh` and a section here.
5. Test on a real paper, look for the empty-page-1 / overrun symptoms, and
   tighten the lists.
