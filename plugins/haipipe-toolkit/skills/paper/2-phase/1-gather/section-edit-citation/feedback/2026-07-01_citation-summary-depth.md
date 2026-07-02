---
date: 2026-07-01
status: open
source: MISQ-Literature-literature session
---

# Citation map summaries are too concise -- need richer detail

## Problem

JL flagged multiple entries in `_CITATION_2-literature.md`:

> JL (on `buchmueller2018pdmp`): "the summary here is too concise, you should make it more detailed."
> JL (on `john2008paradigm`): "all the summaries here are too concise."
> JL (on `barnett2017opioid`): "why this paper can be published in NEJM?"

One-line summaries like "Evaluates the effect of PDMPs on opioid prescribing and health outcomes" are too generic to be useful. The summary should help the author understand WHY the paper matters to this manuscript and WHAT specific finding is being cited.

## Rule

**Summary** in `_CITATION_` maps must include:

1. **What the paper did** (method, data, scale)
2. **Key finding** relevant to the assertion (specific number or conclusion, not "found effects")
3. **Why it matters for this manuscript** (one clause connecting to the assertion)

Bad: "Evaluates the effect of PDMPs on opioid prescribing and health outcomes."
Good: "Uses Medicare Part D data (2007-2013) to show that states adopting must-access PDMPs reduced opioid prescribing by 10% but physician-level variation persisted; supports P1.S5 claim that policy interventions haven't closed the gap."

## Additional: JL's question as annotation

JL asked "why this paper can be published in NEJM?" about Barnett et al. 2017. This kind of question should be preserved as a `> JL:` annotation and optionally answered with a `> CC:` response, NOT deleted or ignored. The answer (NEJM published it because the natural experiment design -- quasi-random ED physician assignment -- yielded causal evidence that a single prescribing decision has years-long consequences) is itself useful context for understanding why we cite it.

## How to apply

When generating or updating `_CITATION_` maps, write 2-3 sentence summaries with method, finding, and relevance. When JL leaves a `> JL:` comment, preserve it verbatim and add a brief `> CC:` response.
