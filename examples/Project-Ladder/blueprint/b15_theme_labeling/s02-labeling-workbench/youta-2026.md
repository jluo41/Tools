# YouTA · reference for Labeling

Checked 2026-11-12. Nicolás José Fernández-Martínez. *YouTA: A context-aware corpus
annotation tool for critical discourse analysis of YouTube comments*. Applied Corpus
Linguistics 6(3), 100226. [Paper](https://doi.org/10.1016/j.acorp.2026.100226).

YouTA links annotations to video and thread context, supports hierarchical labels,
and records human review of model suggestions. Its case study uses 99 comments from
one video and reports strict F1 0.578. The author reviews model predictions to build
the reference layer; this is not an independent blind gold set.
[Author-uploaded paper, §§3–5](https://www.researchgate.net/publication/407234082_YouTA_A_context-aware_corpus_annotation_tool_for_Critical_Discourse_Analysis_of_YouTube_comments).

Design implications for our Workbench (proposals, not implemented by this addition):

- **s02 · Workbench:** keep source and surrounding context accessible beside the item.
- **s13 · Task:** retain the original suggestion separately from the human decision,
  including edits, rejections and added missing labels.
- **s32 · UI:** put review actions with the annotation; reveal detail when needed.
- Preserve our blind-first judgment and sealed evaluation rules. Model-assisted review
  is useful workflow evidence, but cannot establish independent evaluation quality.

Reading scope: checked bibliographic identity, selected methods and limitations;
no replication or software installation. The [author's repository](https://github.com/njfm0001/YouTA)
provides implementation and experiment materials. Two DOI registry records returned
the matching title and 2026 publication year through `check_papers_table.py::lookup`.
The article states CC BY-NC-ND 4.0; PDF download links failed, so Related currently
links to the DOI and no local PDF is claimed. The software repository's license is
separate from the article's license.

Filed in [Block Related](../related/related.md) and Workbench Guide › Related Paper.
