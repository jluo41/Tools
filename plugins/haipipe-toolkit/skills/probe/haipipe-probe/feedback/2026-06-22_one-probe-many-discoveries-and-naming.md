---
status: open
created: 2026-06-22
context: P.0622 trait-behavior-matrix, Gather stage; discovery discoveries/L01_personality-prescribing-landscape/01_field-scan
fixed_in: ""
---

Reporter (JL): 这个其实是不是可以开几个discovery呢？现在这个field-scan这个名字起的很不好，根本不知道干啥. 所以我在想是不是你一个probe可以有n个discovery或者n个tasks folder 你可以再想想

Two issues, both about how Gather fans out evidence:

1. NAMING. The agent named the discovery folder `01_field-scan`. That is a
   STAGE/ACTION name (scanning), not a TOPIC name, so it does not say what the
   discovery is about. Discovery folders must be named by their research
   question/topic (e.g. `risk-attitude-practice-intensity`), never by the verb.

2. GRANULARITY. The agent crammed a 6-sub-literature broad scan into ONE
   discovery folder. Those 6 clusters are 6 distinct topics with different
   verdicts (cluster 2 strong, cluster 5 near-empty, cluster 6 = feasibility).
   One folder -> one muddy verdict + not reusable by other parents. The
   discovery skill's own unit is "one topic = one folder", so a multi-cluster
   scan should fan out into N sibling topic-folders under the probe's discovery
   GROUP. JL's underlying question: is 1 probe : N discoveries : N tasks the
   intended model? (It is — but the skill did not STEER the agent to use it.)

Fix:
- In fn/gather.md: when a Gather call spans multiple distinct sub-questions /
  sub-literatures, split into N discovery topic-folders (one question per
  folder, each its own verdict), not one umbrella folder. State explicitly that
  one probe legitimately references N discoveries AND N tasks (cells already do
  this for tasks; say it for discoveries too).
- Add a naming rule (probe gather.md + cross-ref discovery skill): name
  discovery/task folders by TOPIC, never by stage/action ("field-scan",
  "search", "review" are stage names). This also belongs in the discovery
  skill's docs — flag there too.
- Decide in a revision pass. Also retro-fix the existing L01 folder per whatever
  rule lands (rename + possibly split).
