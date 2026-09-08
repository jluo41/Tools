#!/usr/bin/env python3
"""Count the tells a REVIEWER reacts to in a manuscript. Read-only, never rewrites.

    python3 slop.py FILE [FILE ...] [--control FILE] [--gate]

Why this exists. `haipipe-writing/cli/score.py` counts BOARD tells: house words,
long words, the four house skeletons. A paper can pass it and still read as
generated, because the loudest academic tell is not a word, it is the RHYTHM.

Measured 2026-09-08 on Paper-AgreeablePrescriptionDiscretion §1 (50 sentences,
every one realizing one plan bullet) against the peer-reviewed npj introduction
by the same authors:

                        sentences   SD   <=12w   >=40w
    MISQ §1 Introduction       50   4.2      0%      0%
    MISQ §3 Theory            114   2.5      5%      0%
    npj  §1 Introduction       27  12.8     18%     25%

114 sentences with a standard deviation of 2.5 words is not a style, it is a
metronome, and it is what "one bullet = one sentence" produces. Twenty word-level
humanizer swaps had already been applied to §1 and changed none of these numbers,
because the defect lives at the sentence BOUNDARY, above the word.

The thresholds below are the human control's, not invented.
"""
import argparse
import re
import statistics
from pathlib import Path

# ── the tells, each one counted, each one near-zero in the human control ─────
TELLS = [
    ("contrast-template", r"\b(?:rather than|not merely|not simply|instead of|as opposed to)\b",
     "'X rather than Y' as the default sentence shape"),
    ("trailing-disclaimer",
     # a disclaimer about what the STUDY did not do, tacked onto the end of a claim.
     # It must name research apparatus: an ordinary apposition ("the context, not the
     # people in it") is prose, and gating on that shape rewrote correct sentences.
     r"(?:,|;)\s*(?:although|though|but|and|while)?\s*(?:it|this|which|we)?\s*(?:is|are|does|do|was)?\s*not\s+"
     r"(?:a|an|the|directly|itself|necessarily)?\s*"
     r"(?:causal|directly measured|measured|assessed|observed|tested|claimed|a measure of|a test of|"
     r"a moderator|identification|a causal|part of the|a direct measure)\b",
     "a reviewer-defence clause welded onto the end of a claim"),
    ("hedge-stack",
     r"\b(?:may|might|could|can)\s+(?:be\s+)?(?:reveal|inform|indicate|suggest|carry|motivate|widen|alter|informative)\b",
     "possibility verb where a finding belongs"),
    ("citation-stack", r"\\cite[a-z]*\{[^}]*,[^}]*,[^}]*\}",
     "3+ keys behind one synthesized sentence"),
    ("rule-of-three", r"\b\w+, \w+,? and \w+\b",
     "three-item list as filler rhythm"),
    ("glossary-voice", r"\b\w+ is the [a-z][^.;]{10,80}[;:] it is\b|\bis defined as\b",
     "textbook definition instead of argument"),
    ("self-reference",
     r"\b(?:this (?:paper|study|section|article)|the (?:study|paper) (?:shows|links|develops|treats|asks|seeks))\b",
     "the paper narrating itself"),
    ("process-word",
     r"\b(?:prespecified|predeclared|theory-guided|under a shared|as reported in the|in the empirical section|the focal (?:exposure|construct))\b",
     "pipeline vocabulary leaking into prose"),
    ("roadmap-subject",
     r"^The (?:Literature Review|Theory|Empirical Strategy|Results|Discussion|Conclusion|next section)\b",
     "a section title used as a sentence subject"),
    ("em-dash", r"—", "banned in this repo (JL 260724)"),
]

# Only SOME tells discriminate. Measured across five sections of the peer-reviewed
# npj paper, these six are ZERO everywhere, so a single hit is a real signal:
GATED_TELLS = ("trailing-disclaimer", "glossary-voice", "self-reference",
               "process-word", "roadmap-subject", "em-dash")
# These are REPORTED but never gated. The human limitations section uses five
# "rather than" in 370 words, because stating a scope boundary IS that sentence
# shape; gating on it would have failed real human prose (checked, 260908).
REPORTED_TELLS = ("contrast-template", "rule-of-three", "hedge-stack", "citation-stack")

# Floors read off the peer-reviewed npj paper by the same authors, rounded DOWN.
# Each one separates the two corpora COMPLETELY, with no overlap:
#   sd            npj 12.8 13.2 17.0 21.9 13.9  |  MISQ 2.5 4.2 5.3 5.4 5.8 7.8
#   short+long    npj   45   43   45   70   34  |  MISQ   0   0   5   9  18  19  20
#   numbers/1k    npj 36.6 45.9 74.6 93.3 101.7 |  MISQ 3.5 (Discussion) .. 78.9
GATE = {
    "sd": 8.0,
    "variety_pct": 25.0,     # (<=12w share) + (>=40w share): how much length VARIES
    "gated_per_1k": 3.0,
    "numbers_per_1k": 25.0,
}


def strip_markup(text):
    text = re.sub(r"^---.*?^---\s*", "", text, flags=re.S | re.M)   # front matter
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)              # realizes:/log comments
    text = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)      # fenced blocks
    return text


def content_division(text):
    """The `## Content` division only: the prose a reader sees. Line-based on purpose;
    a DOTALL heading match swallows the whole file and silently reports zero words."""
    out, inside = [], False
    for ln in text.splitlines():
        if re.match(r"^##\s", ln):
            inside = "content" in ln.lower()
            continue
        if inside:
            out.append(ln)
    return "\n".join(out) if out else text


def prose_lines(block):
    return "\n".join(ln for ln in block.splitlines()
                     if ln.strip() and not ln.lstrip().startswith(("#", "|", "-", ">", "`", "*")))


def sentence_words(text):
    """word count per sentence, with LaTeX reduced to placeholders so \\citep does not
    inflate or split a sentence."""
    text = re.sub(r"\\cite[a-z]*\{[^}]*\}", "", text)
    text = re.sub(r"\\ref\{[^}]*\}", "X", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(\{[^}]*\})?", " ", text)
    text = re.sub(r"[%#*|>`\[\]]", " ", text)
    return [n for n in (len(re.findall(r"[A-Za-z][A-Za-z'-]*", s))
                        for s in re.split(r"(?<=[.!?])\s+", text)) if n >= 4]


def measure(path):
    body = prose_lines(content_division(strip_markup(Path(path).read_text(encoding="utf-8", errors="replace"))))
    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", body))
    if not words:
        return None
    hits = {name: len(re.findall(pat, body, re.I | (re.M if name == "roadmap-subject" else 0)))
            for name, pat, _ in TELLS}
    nums = len(re.findall(r"(?<![A-Za-z])\d[\d,.]*(?:\s?%)?(?![A-Za-z])", body))
    lens = sentence_words(body)
    return {
        "path": path, "words": words, "hits": hits, "sentences": len(lens),
        "mean": statistics.mean(lens) if lens else 0,
        "sd": statistics.pstdev(lens) if len(lens) > 1 else 0,
        "short_pct": 100.0 * sum(1 for x in lens if x <= 12) / len(lens) if lens else 0,
        "long_pct": 100.0 * sum(1 for x in lens if x >= 40) / len(lens) if lens else 0,
        "tells_per_1k": 1000.0 * sum(hits.values()) / words,
        "numbers_per_1k": 1000.0 * nums / words,
    }


def failures(m):
    """which floors this text is under. A gate, not an opinion: every threshold is the
    human control's own number, and every one separates the two corpora with no overlap."""
    out = []
    if m["sentences"] >= 12:                       # rhythm needs a sample to mean anything
        if m["sd"] < GATE["sd"]:
            out.append(f"sentence-length SD {m['sd']:.1f} < {GATE['sd']} "
                       f"(a metronome, which is what one-bullet-one-sentence produces)")
        variety = m["short_pct"] + m["long_pct"]
        if variety < GATE["variety_pct"]:
            out.append(f"length variety {variety:.0f}% < {GATE['variety_pct']:.0f}% "
                       f"({m['short_pct']:.0f}% under 12 words + {m['long_pct']:.0f}% over 40)")
    if m["words"] < 250:      # an abstract or a 5-sentence closing cannot carry a rate
        return out
    gated = 1000.0 * sum(m["hits"][t] for t in GATED_TELLS) / m["words"]
    if gated > GATE["gated_per_1k"]:
        named = ", ".join(f"{t} {m['hits'][t]}" for t in GATED_TELLS if m["hits"][t])
        out.append(f"{gated:.1f} gated tells/1k > {GATE['gated_per_1k']} ({named})")
    if m["numbers_per_1k"] < GATE["numbers_per_1k"]:
        out.append(f"{m['numbers_per_1k']:.1f} numbers/1k words < {GATE['numbers_per_1k']} "
                   f"(claims carrying no magnitude)")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--gate", action="store_true", help="exit 1 if any file is under a floor")
    ap.add_argument("--detail", action="store_true", help="per-tell totals")
    a = ap.parse_args(argv)

    ms = [m for m in (measure(f) for f in a.files) if m]
    print(f"{'TEXT':<44}{'WORDS':>6}{'SENTS':>6}{'MEAN':>6}{'SD':>6}{'<=12w':>7}{'>=40w':>7}{'TELL/1k':>8}{'NUM/1k':>7}")
    for m in ms:
        print(f"{Path(m['path']).stem[:44]:<44}{m['words']:>6}{m['sentences']:>6}{m['mean']:>6.1f}"
              f"{m['sd']:>6.1f}{m['short_pct']:>6.0f}%{m['long_pct']:>6.0f}%"
              f"{m['tells_per_1k']:>8.1f}{m['numbers_per_1k']:>7.1f}")
    if a.detail:
        print()
        for label, group in (("GATED (zero in every human section)", GATED_TELLS),
                             ("reported only (context-dependent)", REPORTED_TELLS)):
            print(f"  {label}")
            for name, _pat, why in TELLS:
                if name in group:
                    print(f"    {name:<20}{sum(m['hits'][name] for m in ms):>5}  {why}")
    bad = 0
    for m in ms:
        fs = failures(m)
        if fs:
            bad += 1
            print(f"\n⛔ {Path(m['path']).stem}")
            for f in fs:
                print(f"   · {f}")
    if not bad:
        print("\n✅ every text is above the human-control floors")
    return 1 if (a.gate and bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
