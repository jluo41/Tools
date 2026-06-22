---
status: open
created: 2026-06-22
context: haipipe-paper-pitch (the pitch sub-skill) + example output examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality-Opioid-MedJournal/0-lifecycle/1-pitch/1-pitch.tex
fixed_in: ""
---
The pitch this skill produces is weak. The MedJournal 1-pitch.tex is just a flat
"One-Minute Story" paragraph + "Current Fragility" -- a generic study summary. It
has no hook, no surprise/tension, no explicit implication (so-what), and no
why-believe evidence pointers.

The frustrating part: the pitch skill's OWN template already prescribes the right
shape (Hook / Surprise / So What / Why Believe / Still Fragile / Next Evidence
Move). The output ignored it. So the gap is enforcement, not design.

What a good pitch needs (per the skill's own template): a HOOK (why a random
reader cares), a SURPRISE (the non-obvious turn), an IMPLICATION / so-what (what
changes if true, who uses it), then WHY-BELIEVE (what evidence supports it), then
the fragile point.

Fix directions:
- Make the skill ENFORCE / lint its template: a pitch that is one flat paragraph
  with no Hook/Surprise/So What/Why Believe sections should be flagged, not accepted.
- Rewrite the MedJournal pitch into the Hook -> Surprise -> So What -> Why Believe
  structure as the worked example.

Fix:
