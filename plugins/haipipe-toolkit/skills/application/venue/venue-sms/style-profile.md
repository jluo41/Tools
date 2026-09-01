# SMS Style Profile

Drafting guide for SMS artifacts: voice, tone, and template rules for the SMS venue.


## Voice examples

**Patient, warm:**
```
Hi [Name], your [Medication] refill is due in 2 days.
Refilling on time helps keep your levels steady. Reply
REFILL to start or call [PharmacyPhone]. Reply STOP to
opt out.
```

**Patient, motivational:**
```
[Name], staying on track with [Medication] can make a
real difference. Your refill window opens tomorrow —
tap here to refill: [ShortURL]. STOP to opt out.
```

**Clinician, concise:**
```
[ProviderName]: 12 patients in your panel have refills
due within 72h. 4 may need follow-up. Review
list: [DashboardURL].
```


## Drafting rules

1. One message = one SMS segment (≤ 160 chars) when possible.
   If 2 segments needed, keep under 320 chars total.

2. Follow the venue template slots:
   - Greeting: patient name + context (~30 chars)
   - Benefit: why this matters to them (~60 chars)
   - CTA: specific action + deadline (~50 chars)
   - Close: reassurance or opt-out (~20 chars)

3. Personalization variables:
   `[Name]`, `[Medication]`, `[PharmacyPhone]`, `[ShortURL]`,
   `[ProviderName]`, `[DashboardURL]`

4. Every factual statement maps through the card grant to the signed Wisdom
   handoff or another source allowed by board `reads:`. Recipient copy contains
   no internal D/I/K/W ids; the Design Folder carries the evidence map.

5. Always include opt-out mechanism (STOP keyword or equivalent).

6. No jargon for patient audience. Clinical terms OK for clinician.

7. No URLs longer than 30 chars (use short links).


## Audience pairing

```
audience=patient     → warm, plain, 6th grade, no internal ids in body
audience=clinician   → precise, clinical, no internal ids in body
```

The tone-by-audience rows above are the full tone rules for this venue.


## Self-review checklist

```
[ ] Within 160-char segment limit (or ≤ 320 for 2-segment)
[ ] CTA is specific and actionable (not "talk to your doctor")
[ ] Opt-out present
[ ] No jargon (if patient)
[ ] Personalization variables are available in the data pipeline
[ ] Card id, grant, and exact render version resolve in the Design Folder
[ ] Tone matches audience profile
```


## Unit identity

```yaml
unit: DU<NN>-<slug>
kind: sms
venue: sms
audience: patient | clinician
serves: <division-id>
state: draft | judged
```

The colocated `card.md` owns stance, grant, expected effect, and release state.
The division owns `accepted:`. No SMS artifact on a DesignBoard may carry a
`deployed` terminal; distribution belongs to a downstream Task Folder.
