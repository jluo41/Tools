---
status: fixed
created: 2026-06-22
context: where "venue" lives in the lifecycle; affects haipipe-paper-structure-pitch rubric + lifecycle-map.md / paper-dashboard.md (venue placement) + haipipe-paper-enter (STATUS frontmatter)
fixed_in: "haipipe-paper-structure-pitch v1.1.0"
---
status 算是lifecycle的那一阶段呀，我觉得还是应该放到pitch里，为什么这个对这个venue的audience 有用，你觉得呢。 这个加到feedback里去

Distilled ask / design decision:
- STATUS.md is NOT a lifecycle stage. It is console/meta state (in lifecycle-map.md it is the `enter` machine output, not a node on seed -> pitch -> claims -> narrative -> figures -> minimap). So venue should not be conceptually OWNED by STATUS.
- venue = audience. The reason "why this finding is useful to THIS venue's audience" is a positioning/story concern, which the PITCH owns (its Hook / So-What are audience-facing). The pitch skill already lists "venue strategy" as a legitimate pitch provenance source.
- Therefore venue's RATIONALE belongs in the pitch, not in STATUS.

Agreed resolution (split):
- pitch: add an explicit "Audience / Venue Fit" beat to the pitch rubric -- who reads this venue and why the finding matters to them. This is the home of venue meaning.
- STATUS.md: keep only a thin machine-readable routing label (venue: journal|conference|is) as a pointer so the orchestrator can dispatch without parsing prose. The rationale lives in the pitch.

Suggested fix direction (later revision pass):
- haipipe-paper-structure-pitch: add "Audience / Venue Fit" to the seven-part template (between So-What and Why-Believe, or folded into So-What) and to its done-rubric.
- lifecycle-map.md / paper-dashboard.md: document that venue rationale is a pitch artifact; STATUS holds only the routing label.
- haipipe-paper-enter: when deriving the dashboard, read venue rationale from the pitch, not just the STATUS label.

Note: on 2026-06-22 venue was first written into STATUS.md frontmatter (venue/venue_frame/venue_target). Per this decision, the substantive audience-fit should move into 1-pitch.tex and STATUS should keep only the thin `venue:` routing key.

Fix (2026-06-22): Added "Audience and Venue Fit" to haipipe-paper-structure-pitch (v1.1.0) -- question list, backbone statement, and the section template (new P5 [pitch.audience]; renumbered Why-Believe/Fragile/Next to P6/P7/P8). Documented the split in the skill: the venue routing label (journal/conference/is) stays in STATUS.md, the audience rationale lives in the pitch. Applied to Paper-Personality-Opioid-MedJournal: inserted the pitch.audience beat into 1-pitch.tex (P5) and trimmed STATUS frontmatter to a thin `venue: journal`. Residual (folded into the console redesign, see 2026-06-22_console-too-dense): haipipe-paper-enter could surface venue rationale from the pitch rather than the STATUS label.
