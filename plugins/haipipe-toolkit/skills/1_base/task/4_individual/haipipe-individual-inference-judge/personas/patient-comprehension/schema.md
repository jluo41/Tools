Output exactly one `<judgment>...</judgment>` block.
Inside, follow this structure verbatim.
Do not add fields.
Do not add prose outside.

```xml
<judgment>
  <rubric_dimensions>
    <dimension>
      <name>clarity</name>
      <score>1-5 | unavailable</score>
      <reasoning>One short sentence.</reasoning>
    </dimension>
    <dimension>
      <name>actionability</name>
      <score>1-5 | unavailable</score>
      <reasoning>One short sentence.</reasoning>
    </dimension>
    <dimension>
      <name>tone</name>
      <score>1-5 | unavailable</score>
      <reasoning>One short sentence.</reasoning>
    </dimension>
    <dimension>
      <name>jargon_avoidance</name>
      <score>1-5 | unavailable</score>
      <reasoning>One short sentence — name any jargon if found.</reasoning>
    </dimension>
    <dimension>
      <name>length</name>
      <score>1-5 | unavailable</score>
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
  <overall_score>4.2 | unavailable</overall_score>
  <summary>One paragraph synthesizing the scores and any blockers.</summary>
</judgment>
```

CONSTRAINTS:
- All five declared dimensions MUST appear exactly once; use `unavailable` and
  explain the missing evidence when a dimension cannot be assessed.
- `score` is an integer 1-5 or `unavailable`; `overall_score` is the mean of
  numeric scores rounded to two decimals, or `unavailable` if none are numeric.
- `severity` ∈ {info, warning, critical}; `overall_verdict` ∈ {pass, warn, fail}.
- Overall verdict is `fail` for any score ≤2 or any critical issue; otherwise
  `warn` for any unavailable dimension or score 3; otherwise `pass`. These
  cases do not overlap and cover every complete judgment.
- No XML tags or markdown formatting inside the field text — plain text.
