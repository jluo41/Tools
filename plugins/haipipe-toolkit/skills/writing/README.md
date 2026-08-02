# writing

The prose layer: rewriting what someone already wrote so a reader whose English
is weak can follow it, and leaving a word-level record of every edit under the
sentence it changed.

```
writing/
└── haipipe-writing/     the verb: score → rewrite → record → check
```

**Why a bucket of its own.** Every other family owns a KIND of artifact: `paper`
owns manuscripts, `board` owns pages, `application` owns reports. This one owns
none. Its consumer is any authored prose in the repo, and its test does not care
what file the prose is in.

**The seam with `paper/`.** `haipipe-paper-revise-humanizer` rewrites academic
prose for a venue and writes `%%` comments into LaTeX. Different reader,
different host, same machinery. It should become a consumer of
`haipipe-writing/cli/wdiff.py` rather than grow a second copy of it; until then
the two dialects are written down together in `ref/change-record.md` §3.
