# Reminder Style Profile

Drafting guide for recurring reminder artifacts.


## Voice examples

**Set of 3 rotating reminders:**
```
v1: Time to check in! Logging your meal helps us spot
    patterns. What did you have for lunch?

v2: Quick check-in: have you taken your [Medication]
    today? Staying consistent makes a difference.

v3: You're doing great with your routine. One more
    check-in today — how are you feeling?
```


## Drafting rules

1. For a rotating set, default to 3-5 variants; the released `unit.shape/count`
   fixes the scope. A commissioned single example is not a completed rotating set.
2. Each ≤ 200 chars.
3. Vary the motivation slot; keep prompt + encouragement stable.
4. Supportive tone — never nagging.
5. Include one question per reminder (engagement hook).


## Self-review checklist

```
[ ] Commissioned count met (rotating-set default: 3-5 variants)
[ ] Each ≤ 200 chars
[ ] Motivation varies across variants
[ ] Tone is supportive, not nagging
[ ] Item id, released Commission, allowed inputs and Result artifact hashes resolve
[ ] Any render manifest binds the exact source and picture inside its Result
```
