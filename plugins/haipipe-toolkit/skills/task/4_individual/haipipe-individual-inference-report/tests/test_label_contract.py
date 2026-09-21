"""Focused tests for trend classification and confidence abstention."""

from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path

from pydantic import ValidationError

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

# Parsing helpers do not call the SDK. Stub its import-only names so this
# contract test stays offline and does not need the Claude runtime installed.
sdk = types.ModuleType("claude_agent_sdk")
sdk.ClaudeAgentOptions = type("ClaudeAgentOptions", (), {})
sdk.ClaudeSDKClient = type("ClaudeSDKClient", (), {})
sdk_types = types.ModuleType("claude_agent_sdk.types")
for _name in ("AssistantMessage", "ResultMessage", "TextBlock"):
    setattr(sdk_types, _name, type(_name, (), {}))
sys.modules.setdefault("claude_agent_sdk", sdk)
sys.modules.setdefault("claude_agent_sdk.types", sdk_types)

from compose_report import _classify_trend, parse_report_xml  # noqa: E402


def report_xml(*, verdict="rising", confidence="unavailable"):
    return f"""<report>
      <basics><individual_id>1</individual_id></basics>
      <current><last_obs_dt>2026-01-01 00:00:00</last_obs_dt></current>
      <forecast_summary><horizon_minutes>120</horizon_minutes></forecast_summary>
      <interpretation>
        <verdict>{verdict}</verdict><why>Forecast evidence; cause is unknown.</why>
        <actions></actions><confidence>{confidence}</confidence>
        <safety_flag>none</safety_flag>
      </interpretation>
      <nl>Timing is unverified.</nl>
    </report>"""


class TrendContractTests(unittest.TestCase):
    def test_four_labels_are_disjoint_and_use_adjacent_direction_only(self):
        self.assertEqual(_classify_trend([100] * 10)["verdict"], "stable")
        self.assertEqual(_classify_trend([100] * 8 + [115, 115])["verdict"], "rising")
        self.assertEqual(_classify_trend([115] * 2 + [100] * 8)["verdict"], "falling")
        self.assertEqual(
            _classify_trend([100, 100, 110, 130, 110, 100, 100, 100, 100, 100])["verdict"],
            "mixed",
        )
        self.assertEqual(_classify_trend([100.0, 100.01])["verdict"], "rising")

    def test_empty_or_nonfinite_trajectory_is_rejected(self):
        with self.assertRaises(ValueError):
            _classify_trend([])
        with self.assertRaises(ValueError):
            _classify_trend([100, float("nan")])


class ReportLabelParsingTests(unittest.TestCase):
    def test_parser_requires_model_to_use_deterministic_verdict(self):
        parsed = parse_report_xml(report_xml(), expected_verdict="rising")
        self.assertEqual(parsed.interpretation.verdict, "rising")
        with self.assertRaisesRegex(ValueError, "disagrees with deterministic"):
            parse_report_xml(report_xml(verdict="stable"), expected_verdict="rising")

    def test_confidence_must_abstain_without_calibration_evidence(self):
        parsed = parse_report_xml(report_xml())
        self.assertEqual(parsed.interpretation.confidence, "unavailable")
        with self.assertRaises(ValidationError):
            parse_report_xml(report_xml(confidence="high"))

    def test_missing_required_label_is_not_defaulted(self):
        xml = report_xml().replace("<verdict>rising</verdict>", "")
        with self.assertRaisesRegex(ValueError, "Missing required interpretation.verdict"):
            parse_report_xml(xml)

    def test_missing_explanation_is_rejected(self):
        xml = report_xml().replace("<why>Forecast evidence; cause is unknown.</why>", "")
        with self.assertRaisesRegex(ValueError, "Missing required interpretation.why"):
            parse_report_xml(xml)


if __name__ == "__main__":
    unittest.main()
