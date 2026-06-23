Output exactly one `<judgment>...</judgment>` block. Inside, follow this
structure verbatim. Do not add fields. Do not add prose outside.

```xml
<judgment>
  <rubric_dimensions>
    <dimension>
      <name>clarity</name>
      <score>1-5</score>
      <reasoning>One short sentence.</reasoning>
    </dimension>
    <dimension>
      <name>actionability</name>
      <score>1-5</score>
      <reasoning>One short sentence.</reasoning>
    </dimension>
    <dimension>
      <name>tone</name>
      <score>1-5</score>
      <reasoning>One short sentence.</reasoning>
    </dimension>
    <dimension>
      <name>jargon_avoidance</name>
      <score>1-5</score>
      <reasoning>One short sentence — name any jargon if found.</reasoning>
    </dimension>
    <dimension>
      <name>length</name>
      <score>1-5</score>
      <reasoning>One short sentence.</reasoning>
    </dimension>
  </rubric_dimensions>

  <issues>
    <issue>
      <severity>info | warning | critical</severity>
      <location>field path, e.g. "nl" or "interpretation.actions[2]"</location>
      <issue>brief description</issue>
      <suggestion>optional fix</suggestion>
    </issue>
    <!-- repeat <issue> as needed; zero issues is fine -->
  </issues>

  <overall_verdict>pass | warn | fail</overall_verdict>
  <overall_score>4.2</overall_score>
  <summary>One paragraph synthesizing the scores and any blockers.</summary>
</judgment>
```

CONSTRAINTS:
- All five dimensions MUST appear (even if score is 5 with empty issue list).
- `score` integer 1-5; `overall_score` float 0.0-5.0.
- `severity` ∈ {info, warning, critical}; `overall_verdict` ∈ {pass, warn, fail}.
- No XML tags or markdown formatting inside the field text — plain text.
