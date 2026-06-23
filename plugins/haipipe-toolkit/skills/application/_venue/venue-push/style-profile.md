# Push Notification Style Profile

Drafting guide for push notification artifacts.


## Voice examples

**Patient, urgent:**
```
Title: Refill Due Tomorrow
Body:  [Name], your [Medication] is due for refill. Tap to start.
```

**Patient, motivational:**
```
Title: Keep the streak going 💪
Body:  3 refills on time! Your next one is due Friday.
```

**Clinician, alert:**
```
Title: 4 patients at risk
Body:  Refill lapse risk detected. Tap to review panel.
```


## Drafting rules

1. Title ≤ 50 chars — hook + urgency.
2. Body ≤ 100 chars — benefit + action hint.
3. One tap action → deep link to specific app screen.
4. No opt-out in body (OS handles notification settings).


## Self-review checklist

```
[ ] Title ≤ 50 chars
[ ] Body ≤ 100 chars
[ ] Deep link target specified
[ ] Tone matches audience
[ ] cited_K / cited_W in frontmatter
```
