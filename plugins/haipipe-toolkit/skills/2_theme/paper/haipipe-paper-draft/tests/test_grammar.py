"""CONSTITUTION A04: grammar a machine can see keeps the W4 fix loop open (JL 261118)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "1_base/draft/haipipe-draft-review/cli"))
from grammar import findings  # noqa: E402

# the sentences JL saw underlined in Word (ScalingGlucose Methods v1.17), each must be named
BAD = {
    "We trained every MLP with AdamW at a learning rate of 1e-3 and batches of 512 rows.": "e-notation",
    "For all three traits we report 1 minus AUROC, so lower is better.": "opening-comma",
    "For stride we used 4 hours.": "opening-comma",
    "Each share MLP outputs two numbers.": "label-noun",
    "Training stopped after 10 passes without a gain on the selection patients.": "label-noun",
    "We standardized states by the mean and spread of the fitting rows.": "label-noun",
}
GOOD = [
    "For all three traits, we report 1 minus AUROC, so lower is better and chance is 0.5.",
    "We trained every MLP with AdamW at a learning rate of 0.001 and with batches of 512 rows.",
    "The MLP for each share outputs two numbers.",
    "For a miss $r$, the loss is $2(\\sqrt{1+(r/s)^2}-1)$.",
    "In both encodings, glucose readings below 11 mg/dL are masked.",
    "We fit $L = E + A N^{-\\alpha}$ with $\\alpha < 1e-3$ inside math.",
]


def test_bad_sentences_are_named():
    for sentence, kind in BAD.items():
        assert kind in {k for k, _ in findings(sentence)}, sentence


def test_good_sentences_pass():
    for sentence in GOOD:
        assert findings(sentence) == [], (sentence, findings(sentence))
