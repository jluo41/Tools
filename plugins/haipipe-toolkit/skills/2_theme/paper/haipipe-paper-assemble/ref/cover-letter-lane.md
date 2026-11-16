The cover letter lane (run-delivery-coverletter): its words, facts, output, checks and send (haipipe-paper-assemble).

## ✉️ The cover letter lane · run-delivery-coverletter (0.9.0)

A submission sends a cover letter with the manuscript, so the build makes it the same way (JL 260929):

```text
WORDS   on the ladder (b16 Q05): the version's letter Task t31_cover-letter/, else t01_cover-letter/ of the submission
        Job whose face says `for: <version>` (or the Task [coverletter] task names), its "Cover letter" division,
        else its whole Content; on an older Board the "Cover letter" division of the submission Round page
        (B<x>-<desk>-Round/RD<NN>-…/<stem>.md, named by [coverletter] round) · approved like any page;
        until the Content has the words, the latest draft is used and the letter is not ready
FACTS   filled by code: {title} {journal} {article_type} {pages} {tables} {figures} in the words,
        plus date, addressee and author block from paper-build.toml [coverletter]
OUTPUT  delivery/cover-letter/ PDF (generated LaTeX) and DOCX · [outputs] cover_letter_pdf / _docx
CHECKS  every number printed in the manuscript · required mentions (profile cover_letter_must_mention
        + [coverletter] must_mention) · no causal verb · no process text · manuscript within the
        profile's page_cap · author block complete · one or two pages
TASK    with [coverletter] task, the same PDF and Word file (and Word's own PDF print) are also the letter Task's
        Delivery: delivery/<its Job>/<task>/latex/<stem>.pdf and word/<stem>.docx (0.13.1; manifest
        cover_letter.task_delivery); the Task's face says delivery-builder: so page.py export runs this build
SEND    build.py send qNN (a comments report of the version) or send RD<NN> (an older Round) freezes the
        letter with the manuscript into its sent/
```

The words are authored and approved; everything factual is code-filled, so a number or a title can
never drift from the manuscript. `scripts/cover_letter.py` holds the lane; `build-manifest.json`
records it under `cover_letter` (source, ready, checks). The rules for the words are `haipipe-paper-draft`
§ A cover letter's words. `send` skips an output switched off with an
empty value and, when the profile's `appendices = "main"`, the supplement a manuscript-with-appendices
never produces.
