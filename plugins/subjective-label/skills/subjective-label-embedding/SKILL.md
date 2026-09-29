---
name: subjective-label-embedding
description: >-
  The Data › Embedding view skill of the subjective-label family: it
  builds and reads the embedding map of the development items: one build per model and settings, started only by a person. Every Run in this view names this skill, and no other view uses it.
  Use for building an embedding, choosing an embedding model, the map, groups, typical items, embedding_build.py, or /subjective-label-embedding.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-embedding · Data Space › Embedding

This skill owns the Runs of the labeling workbench's Data › Embedding
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-building` (who decides what) first. Which Run
comes before and after these is in `label-building-workflow`.

## Runs in this view

```text
step  run                          state
 3    run-embedding-build      built · engine/embedding_build.py build
```

A Run is named `rlNN_<operation>_<target>` on disk and shown as
`run-<operation>-<target>` on the page. Its Ticket is `<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

`create` intentionally leaves `cache/embeddings/` empty. `embedding-build` is
an explicit non-gating operation because choosing or invoking an embedding
model is a separate execution decision; the scaffold API never makes a
network/model call implicitly.

`embedding-build` runs only when a person asks for it: the identified human presses
`Run embedding` in `Data → Embedding`, or names themselves with `--started-by`
on the command line. No agent starts a build on its own, not even when the job
has no embedding yet; the CLI refuses a build without `--started-by`, and the
Ticket and manifest record who asked and how (`started_by`).

The `embedding-build` action is `engine/embedding_build.py build`. It embeds every
`population_status: eligible` item once and never reads a sealed row into the
model. Each input is the response, a blank line, then the context, so a
word-piece cut only ever drops the end of the context. It writes
`cache/embeddings/<version>/` (`manifest.json`, `vectors.npy`, `rows.jsonl`,
`map.jsonl`, `groups.json`) and one `rlNN_embedding-build_<version>` Run,
where `<version>` is the model name in lower case. The embedder choice lives on
the Ticket, so `config.yaml` is never edited. Because a vector sets no label,
the build is not gated on G0; it refuses only a HOLD job or P0 files that do
not verify. Rerunning with the same model and corpus is a no-op. The retrieval
subcommands in `engine/embed.py` (`nearest`, `stratify`, `project`) keep their
G0 guard. The Board shows the result in `Data → Embedding`, where the person
also chooses the model: `CATALOG` in `embedding_build.py` lists the open-weight
models allowed, `--device auto` picks cuda, then mps, then cpu, and the 4B and
8B Qwen3 models load in bfloat16. Each model is its own `<version>` folder and
its own Run, so a second model never changes the first. A person may also set
`--input` (`reply_context`, `reply`, `context`), `--instruction` (Qwen3 and
e5-instruct only), `--groups` (2-20), `--map` (`tsne`, `pca`), and `--seed`.
Each non-default setting adds a tag to `<version>`, for example
`qwen3-embedding-0-6b-reply-only-instr-d30f16-k5-pca-seed3`, so every setting
combination is its own folder and Run. Every build also writes `map3d.jsonl`
for the rotating view; `embedding_build.py map3d` adds it to an older build
without touching its vectors.

```bash
python3 plugins/subjective-label/engine/embedding_build.py build \
  --job-root <page-folder>/labeling --started-by <the person who asked> \
  --model Qwen/Qwen3-Embedding-0.6B
```

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
