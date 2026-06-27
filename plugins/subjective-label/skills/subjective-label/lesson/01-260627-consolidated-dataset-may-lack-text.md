---
status: active
created: 2026-06-27
context: data-prep
---

Consolidated review datasets may strip review text to save space. The 10.2M `physician_reviews_complete` HF Dataset only kept `review_text_length`, not the text itself. The text-bearing version was a separate parquet in `0-RawOutputStore`. Always verify the text column exists before building a labeling corpus -- don't assume a "reviews" dataset has review text.
