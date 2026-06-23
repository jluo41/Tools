# SMS Style Profile

Drafting guide for SMS artifacts. Absorbed from the former
haipipe-application-message specialist.


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
due within 72h. 4 are high-risk for lapse (K03). Review
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

4. Every factual claim maps to a K/W entry in the claims stage.
   Patient body: no K-id visible. Clinician body: inline K-id.

5. Always include opt-out mechanism (STOP keyword or equivalent).

6. No jargon for patient audience. Clinical terms OK for clinician.

7. No URLs longer than 30 chars (use short links).


## Audience pairing

```
audience=patient     → warm, plain, 6th grade, no K-id in body
audience=clinician   → precise, clinical, inline K-id
```

Read `_audience/profile-<audience>/README.md` for full tone rules.


## Self-review checklist

```
[ ] Within 160-char segment limit (or ≤ 320 for 2-segment)
[ ] CTA is specific and actionable (not "talk to your doctor")
[ ] Opt-out present
[ ] No jargon (if patient)
[ ] Personalization variables are available in the data pipeline
[ ] cited_K / cited_W in artifact frontmatter
[ ] Tone matches audience profile
```


## Artifact frontmatter

```yaml
---
kind: intervention
venue: sms
audience: patient | clinician
intent: "<one-line>"
created: YYYY-MM-DD
cited_K: [K03]
cited_W: [W02]
status: draft | reviewed | deployed
---
```
