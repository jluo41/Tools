# Transcript originals inside a Task Studio

Part of hai-studio's topic contract (`ref/topic-contract.md`).


A video Task topic can keep `transcripts/index.json` with schema `studio-transcripts/v1`.
The shared Studio displays its source PDFs in folding cards below the drawing. Each
card loads its PDF only when opened; `#topic-<topic>--transcript-rNN` opens one directly.
The drawing explains the source; the transcript holds the full original text.

```json
{
  "schema": "studio-transcripts/v1",
  "documents": [{
    "rid": "r01",
    "title": "Source video title",
    "file": "original.pdf",
    "page": 1,
    "end_page": 8,
    "raw_file": "original.md",
    "source_url": "https://example.test/video",
    "transcription": "automatic_unchecked",
    "warnings": []
  }],
  "missing": []
}
```

`file` is relative to the index and must be a kept PDF inside the owning Block's
`studio/`. Several videos may point to their page ranges in one shared PDF book
under `studio/_transcripts/`. `raw_file` is a Markdown text file beside the index.
Preserve every source segment and timestamp; retain the cached record or its
checksum and provenance. Distinguish creator captions, automatic recognition,
and corrected text. Automatic recognition is unverified until checked against the
video; export never changes a source Run's verification state. A missing transcript
is listed as missing, never replaced by a summary. Flag truncation and timestamp
inconsistencies. The PDF remains searchable text, rather than screenshots of text.

For an article edition, add `presentation: "article"` and an optional PDF named
`destination`. The reader opens `#nameddest=<destination>` at the source's exact
heading, so compact articles may share pages. Keep the earlier PDF in
`original_pdf`, with `original_page` and `original_end_page`; the card offers a
separate verbatim-original link. Editorial rewriting and paragraph arrangement
remain distinct from a checked transcript. Preserve source verification state
and note what was edited; typesetting alone is not source verification.
