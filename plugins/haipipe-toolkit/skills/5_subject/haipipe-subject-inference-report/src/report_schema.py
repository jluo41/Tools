"""Report schema — pydantic models for the dual-layer Message.

The report has two layers — a structured JSON payload (for downstream
consumption: judge, doctor UI, eval harness) and a free-text NL rendering
(for the patient or clinician reading it).

Both come from the same LLM call. The XML response shape is:

    <report>
      <basics>...</basics>
      <current>...</current>
      <forecast_summary>...</forecast_summary>
      <interpretation>
        <verdict>rising | stable | falling</verdict>
        <why>...</why>
        <actions>...</actions>
        <confidence>high | medium | low</confidence>
        <safety_flag>none | hypo_risk | hyper_risk</safety_flag>
      </interpretation>
      <nl>... free text patient/clinician message ...</nl>
    </report>
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field

VERDICT_VALUES = {"rising", "stable", "falling", "mixed"}
CONFIDENCE_VALUES = {"high", "medium", "low"}
SAFETY_VALUES = {"none", "hypo_risk", "hyper_risk", "hypo_and_hyper_risk"}


class Basics(BaseModel):
    """Patient demographics from Ptt + manifest. Codes are decoded to
    human-readable labels (e.g. Gender 1 → 'Male') before the LLM sees
    them — so this layer carries strings, not codes."""
    subject_id: str
    dataset: Optional[str] = None
    gender: Optional[str] = None             # 'Male' / 'Female' / 'Unknown'
    year_of_birth: Optional[int] = None
    age_years: Optional[int] = None
    disease_type: Optional[str] = None       # 'Type 1 diabetes' / 'Type 2 diabetes'


class CurrentStatus(BaseModel):
    """The 'right now' snapshot."""
    last_obs_dt: str
    last_bg_mg_dl: float
    last_meal: Optional[dict] = None  # {food, carbs_g, time}  if available
    recent_window_n: int  # how many CGM points were considered
    recent_min: Optional[float] = None
    recent_max: Optional[float] = None
    recent_mean: Optional[float] = None


class ForecastSummary(BaseModel):
    """Compact summary of the model's forecast (raw forecast lives in meta)."""
    horizon_minutes: int            # e.g. 120
    n_windows: int                  # e.g. 45
    pred_min: float
    pred_max: float
    pred_mean: float


class Interpretation(BaseModel):
    verdict: Literal["rising", "stable", "falling", "mixed"]
    why: str
    actions: List[str] = Field(default_factory=list, max_length=4)
    confidence: Literal["high", "medium", "low"]
    safety_flag: Literal["none", "hypo_risk", "hyper_risk", "hypo_and_hyper_risk"]


class Report(BaseModel):
    """Dual-layer Message. `nl` is the patient/clinician-facing text;
    everything else is structured for downstream automation."""
    basics: Basics
    current: CurrentStatus
    forecast_summary: ForecastSummary
    interpretation: Interpretation
    nl: str
