# SMS Style Profile

Drafting guide for SMS artifacts: voice, tone, and template rules for the SMS venue.


## Voice examples

**General reader, warm:**
```
Hi [Name], your <item> is ready in 2 days. <One plain
reason it matters>. Reply YES to start or tap
[ShortURL]. Reply STOP to opt out.
```

**General reader, motivational:**
```
[Name], <one plain reason this step helps>. Your
<window> opens tomorrow: tap here: [ShortURL].
STOP to opt out.
```

**Professional, concise:**
```
[SenderName]: 12 <items> in your list are due within
72h. 4 may need follow-up. Review list:
[ListURL].
```


## Drafting rules

1. One message = one SMS segment (≤ 160 chars) when possible.
   If 2 segments needed, keep under 320 chars total.

2. Follow the venue template slots:
   - Greeting: the reader's name + context (~30 chars)
   - Benefit: why this matters to them (~60 chars)
   - CTA: specific action + deadline (~50 chars)
   - Close: reassurance or opt-out (~20 chars)

3. Personalization variables:
   `[Name]`, `[Item]`, `[Phone]`, `[ShortURL]`,
   `[ProviderName]`, `[DashboardURL]`

4. Every factual statement maps through the Job's inputs/ fence (its manifest) to the signed Wisdom
   handoff or another fence file. Recipient copy contains
   no internal D/I/K/W ids; the Job's records carry the evidence map.

5. Always include opt-out mechanism (STOP keyword or equivalent).

6. No jargon for a general reader. Technical terms OK for a professional.

7. No URLs longer than 30 chars (use short links).


## Audience pairing

```
audience=general      → warm, plain, 6th grade, no internal ids in body
audience=professional → precise, technical, no internal ids in body
```

The tone-by-audience rows above are the full tone rules for this venue.


## Self-review checklist

```
[ ] Within 160-char segment limit (or ≤ 320 for 2-segment)
[ ] CTA is specific and actionable (not "<a vague ask>")
[ ] Opt-out present
[ ] No jargon (if a general reader)
[ ] Personalization variables are available in the data pipeline
[ ] Job and Task ids, the pinned goal · method · inputs, and the Run's result/ paths resolve
[ ] Any render manifest binds the exact source and picture inside its Run's result/
[ ] Tone matches audience profile
```


## Recorded identity

A design is the Task `tNN_d<NN>_<name>/` of its Job; its words come from
`run-generate-d<NN>/result/design.md` (or the newest revise pass), and the Job's
pinned goal, method version and inputs version own the design's aim, method and
checks. These identifiers belong in records, not recipient copy. A passed verify ④,
then t99's rank ⑤ and a person's release, put the exact message in delivery/.
Distribution belongs to downstream work.
