"""Judgment schema — pydantic model for what the judge LLM emits.

Judge consumes a Report (from inference-report) and scores it along
rubric dimensions defined by the JUDGE persona (not the report persona).

Each rubric persona MAY define its own dimension list — but the schema
here is permissive: dimensions are name→{score, reasoning} pairs, the
persona prompt enumerates which names are expected.
"""

from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

VERDICT_VALUES = {"pass", "warn", "fail"}


class DimensionScore(BaseModel):
    """One rubric dimension. score is 1-5; reasoning is free-form."""
    score: int = Field(ge=1, le=5)
    reasoning: str


class IssueFlag(BaseModel):
    """A specific concrete problem the judge spotted in the Report."""
    severity: Literal["info", "warning", "critical"]
    location: str        # e.g. "interpretation.actions[1]" or "nl"
    issue: str
    suggestion: Optional[str] = None


class Judgment(BaseModel):
    """The judge's structured output for one Report."""
    judge_persona: str               # which judge produced this
    rubric_dimensions: Dict[str, DimensionScore]
    issues: List[IssueFlag] = Field(default_factory=list)
    overall_verdict: Literal["pass", "warn", "fail"]
    overall_score: float = Field(ge=0.0, le=5.0)
    summary: str                     # one-paragraph synthesis
