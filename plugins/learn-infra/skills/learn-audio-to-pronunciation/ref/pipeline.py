"""
learn-audio-to-pronunciation pipeline.

Outputs to _WorkSpace/LearnStore/pronunciation/<stem>/ by default.
Produces a words.json manifest so word boundaries can be manually adjusted.

Usage:
    python pipeline.py <audio-path> [--ref "reference text"] [--output <dir>] [--threshold 70]
    python pipeline.py <audio-path> --reclip                # re-clip from edited words.json
"""
import argparse
import asyncio
import io
import json
import shutil
import time
from datetime import datetime
from pathlib import Path

import yaml
from pydub import AudioSegment
from pydub.silence import split_on_silence

# ─── Config ──────────────────────────────────────────────────────────────
AZURE_REGION = "eastus"
AZURE_LANG = "en-US"
TTS_VOICE = "en-US-JennyNeural"
MAX_CHUNK_MS = 9000
MIN_SILENCE_MS = 400
SILENCE_THRESH_DB = -40
KEEP_SILENCE_MS = 200
PADDING_MS = 100

ARPA_TO_IPA = {
    "th": "θ", "dh": "ð", "r": "ɹ", "l": "l", "w": "w", "v": "v", "f": "f",
    "z": "z", "s": "s", "sh": "ʃ", "zh": "ʒ", "ch": "tʃ", "jh": "dʒ",
    "ng": "ŋ", "n": "n", "m": "m", "p": "p", "b": "b", "t": "t", "d": "d",
    "k": "k", "g": "ɡ", "h": "h", "y": "j", "iy": "iː", "ih": "ɪ",
    "ey": "eɪ", "eh": "ɛ", "ae": "æ", "aa": "ɑː", "ao": "ɔː", "ow": "oʊ",
    "uh": "ʊ", "uw": "uː", "ah": "ʌ", "ax": "ə", "er": "ɝ", "ay": "aɪ",
    "aw": "aʊ", "oy": "ɔɪ",
}

PHONEME_ZH = {
    "th": "中文没有咬舌音。舌尖放在上下牙之间，轻轻吹气。",
    "dh": "和 th 一样咬舌，但要振动声带。",
    "r": "英语的 r 舌头卷起但不碰任何地方，和中文「日」不同。",
    "l": "舌尖要牢牢抵住上齿龈。南方方言容易和 r 混淆。",
    "v": "中文没有/v/！上牙咬住下嘴唇发声吹气。",
    "ae": "中文没有这个音。下巴下沉，嘴唇横向展开。",
    "ah": "中文没有这个音。嘴微张，短促有力。",
    "ax": "最弱的元音。中文每个字都有重量，英语非重读要弱化。",
    "ih": "比「衣」短而松弛。sit vs seat 的区别。",
    "uh": "比「乌」短而松弛。book vs boot 的区别。",
}

try:
    import eng_to_ipa as _ipa_lib
except ImportError:
    _ipa_lib = None


def word_to_ipa(word_data):
    wt = word_data.get("Word", "").strip(".,!?;:'\"")
    if _ipa_lib and wt:
        ipa = _ipa_lib.convert(wt)
        if ipa and "*" not in ipa:
            return ipa
    phs = word_data.get("Phonemes", [])
    if not phs:
        return ""
    return "".join(ARPA_TO_IPA.get(p.get("Phoneme", "").lower(), p.get("Phoneme", "?"))
                   for p in phs)


def ticks_to_ms(t):
    return t / 10_000


def safe_filename(word):
    return word.lower().strip(".,!?;:'\"").replace(" ", "_").replace("/", "_")


# ─── Step 1: Convert + Split ─────────────────────────────────────────────
def convert_and_split(audio_path, output_dir):
    print(f"[1/5] Loading {audio_path.name}...")
    audio = AudioSegment.from_file(str(audio_path))
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)

    chunks_dir = output_dir / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    if len(audio) <= MAX_CHUNK_MS + 2000:
        out = chunks_dir / "chunk_001.wav"
        audio.export(str(out), format="wav")
        print(f"  Single chunk: {len(audio)/1000:.1f}s")
        return [out]

    raw_chunks = split_on_silence(
        audio,
        min_silence_len=MIN_SILENCE_MS,
        silence_thresh=SILENCE_THRESH_DB,
        keep_silence=KEEP_SILENCE_MS,
    )

    merged = []
    current = AudioSegment.empty()
    for c in raw_chunks:
        if len(current) + len(c) > MAX_CHUNK_MS and len(current) > 0:
            merged.append(current)
            current = c
        else:
            current += c
    if len(current) > 0:
        merged.append(current)

    paths = []
    for i, chunk in enumerate(merged):
        out = chunks_dir / f"chunk_{i+1:03d}.wav"
        chunk.export(str(out), format="wav")
        paths.append(out)
    print(f"  Split into {len(paths)} chunks ({', '.join(f'{len(AudioSegment.from_wav(str(p)))/1000:.1f}s' for p in paths)})")
    return paths


# ─── Step 2: Assess ──────────────────────────────────────────────────────
def get_azure_key():
    import os
    import subprocess
    key = os.environ.get("AZURE_SPEECH_KEY")
    if not key:
        try:
            key = subprocess.check_output(
                "az cognitiveservices account keys list --name cdhai-speech "
                "--resource-group CDHAI-Databricks-RG --query key1 -o tsv",
                shell=True, text=True
            ).strip()
        except Exception:
            pass
    if not key:
        raise EnvironmentError("Set AZURE_SPEECH_KEY or login with az cli")
    return key


def assess_chunk(wav_path, ref_text, key):
    import azure.cognitiveservices.speech as speechsdk

    sc = speechsdk.SpeechConfig(subscription=key, region=AZURE_REGION)
    sc.speech_recognition_language = AZURE_LANG
    ac = speechsdk.audio.AudioConfig(filename=str(wav_path))

    pron_kwargs = dict(
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
    )
    if ref_text:
        pron_kwargs["reference_text"] = ref_text
        pron_kwargs["enable_miscue"] = True

    pc = speechsdk.PronunciationAssessmentConfig(**pron_kwargs)
    rec = speechsdk.SpeechRecognizer(speech_config=sc, audio_config=ac)
    pc.apply_to(rec)
    res = rec.recognize_once()

    if res.reason == speechsdk.ResultReason.RecognizedSpeech:
        rj = json.loads(res.properties.get(
            speechsdk.PropertyId.SpeechServiceResponse_JsonResult, "{}"))
        if ref_text:
            rj["ReferenceText"] = ref_text
        return rj
    print(f"  WARNING: assessment failed for {wav_path.name}: {res.reason}")
    return None


def assess_all(chunk_paths, ref_text, key, output_dir):
    print(f"[2/5] Running Azure assessment on {len(chunk_paths)} chunks...")
    assess_dir = output_dir / "assess"
    assess_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, cp in enumerate(chunk_paths):
        print(f"  [{i+1}/{len(chunk_paths)}] {cp.name}...", end=" ", flush=True)
        rj = assess_chunk(cp, ref_text, key)
        if rj:
            out = assess_dir / f"{cp.stem}.json"
            out.write_text(json.dumps(rj, indent=2))
            nb = rj.get("NBest", [{}])[0] if "NBest" in rj else rj
            pa = nb.get("PronunciationAssessment", {})
            print(f"acc={pa.get('AccuracyScore', 0):.0f} flu={pa.get('FluencyScore', 0):.0f}")
            results.append({"path": cp, "json": rj, "nb": nb})
        else:
            print("FAILED")
        time.sleep(0.3)
    return results


# ─── Step 3: Clip ALL words + TTS for weak ──────────────────────────────
def build_words_manifest(results, threshold):
    """Build a words.json manifest from Azure assessment results."""
    manifest = []
    for r in results:
        chunk_stem = r["path"].stem
        words = r["nb"].get("Words", [])
        for wi, w in enumerate(words):
            wt = w.get("Word", "?")
            wt_clean = safe_filename(wt)
            pa = w.get("PronunciationAssessment", {})
            score = pa.get("AccuracyScore", 0)
            error_type = pa.get("ErrorType", "None")

            offset_ticks = w.get("Offset", 0)
            dur_ticks = w.get("Duration", 0)
            start_ms = round(ticks_to_ms(offset_ticks))
            end_ms = round(ticks_to_ms(offset_ticks + dur_ticks))

            ipa = word_to_ipa(w)

            syllables = []
            for s in w.get("Syllables", []):
                syllables.append({
                    "syllable": s.get("Syllable", "?"),
                    "grapheme": s.get("Grapheme", ""),
                    "score": s.get("PronunciationAssessment", {}).get("AccuracyScore", 0),
                    "start_ms": round(ticks_to_ms(s.get("Offset", 0))),
                    "end_ms": round(ticks_to_ms(s.get("Offset", 0) + s.get("Duration", 0))),
                })

            phonemes = []
            for p in w.get("Phonemes", []):
                phonemes.append({
                    "phoneme": p.get("Phoneme", "?"),
                    "ipa": ARPA_TO_IPA.get(p.get("Phoneme", "").lower(), p.get("Phoneme", "?")),
                    "score": p.get("PronunciationAssessment", {}).get("AccuracyScore", 0),
                    "start_ms": round(ticks_to_ms(p.get("Offset", 0))),
                    "end_ms": round(ticks_to_ms(p.get("Offset", 0) + p.get("Duration", 0))),
                })

            entry = {
                "word": wt,
                "word_index": wi,
                "chunk": chunk_stem,
                "start_ms": start_ms,
                "end_ms": end_ms,
                "score": score,
                "error_type": error_type,
                "ipa": ipa,
                "weak": score < threshold,
                "clip_file": f"words/{wt_clean}.wav",
                "tts_file": f"tts/{wt_clean}.wav" if score < threshold else None,
                "syllables": syllables,
                "phonemes": phonemes,
            }
            manifest.append(entry)
    return manifest


def clip_all_words(manifest, output_dir):
    """Clip ALL words from chunk audio using manifest boundaries."""
    print(f"[3/5] Clipping {len(manifest)} words + generating TTS for weak ones...")
    words_dir = output_dir / "audio" / "words"
    tts_dir = output_dir / "audio" / "tts"
    words_dir.mkdir(parents=True, exist_ok=True)
    tts_dir.mkdir(parents=True, exist_ok=True)

    import azure.cognitiveservices.speech as speechsdk

    chunk_cache = {}
    clip_count = 0
    tts_count = 0

    for entry in manifest:
        chunk_path = output_dir / "chunks" / f"{entry['chunk']}.wav"
        if entry["chunk"] not in chunk_cache:
            chunk_cache[entry["chunk"]] = AudioSegment.from_wav(str(chunk_path))
        chunk_audio = chunk_cache[entry["chunk"]]

        s = entry["start_ms"]
        e = entry["end_ms"]
        if e <= s:
            continue

        clip_path = output_dir / "audio" / entry["clip_file"]
        if not clip_path.exists():
            padded = chunk_audio[max(0, s - PADDING_MS):e + PADDING_MS]
            padded.export(str(clip_path), format="wav")
            clip_count += 1

        if entry["weak"] and entry["tts_file"]:
            tts_path = output_dir / "audio" / entry["tts_file"]
            if not tts_path.exists():
                wt_clean = entry["word"].lower().strip(".,!?;:'\"")
                try:
                    key = get_azure_key()
                    sc = speechsdk.SpeechConfig(subscription=key, region=AZURE_REGION)
                    sc.speech_synthesis_voice_name = TTS_VOICE
                    ac = speechsdk.audio.AudioOutputConfig(filename=str(tts_path))
                    synth = speechsdk.SpeechSynthesizer(speech_config=sc, audio_config=ac)
                    result = synth.speak_text_async(wt_clean).get()
                    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
                        tts_path.unlink(missing_ok=True)
                    else:
                        tts_count += 1
                except Exception:
                    tts_path.unlink(missing_ok=True)

    print(f"  Clipped {clip_count} words, generated {tts_count} TTS")


def reclip_from_manifest(output_dir):
    """Re-clip word audio from an edited words.json manifest."""
    manifest_path = output_dir / "words.json"
    if not manifest_path.exists():
        print(f"Error: {manifest_path} not found")
        return
    manifest = json.loads(manifest_path.read_text())
    print(f"Re-clipping {len(manifest)} words from edited manifest...")

    words_dir = output_dir / "audio" / "words"
    chunk_cache = {}

    for entry in manifest:
        chunk_path = output_dir / "chunks" / f"{entry['chunk']}.wav"
        if entry["chunk"] not in chunk_cache:
            chunk_cache[entry["chunk"]] = AudioSegment.from_wav(str(chunk_path))
        chunk_audio = chunk_cache[entry["chunk"]]

        s = entry["start_ms"]
        e = entry["end_ms"]
        if e <= s:
            continue

        clip_path = output_dir / "audio" / entry["clip_file"]
        padded = chunk_audio[max(0, s - PADDING_MS):e + PADDING_MS]
        padded.export(str(clip_path), format="wav")

    print(f"  Done. {len(manifest)} clips updated.")


# ─── Step 4: Claude analysis ─────────────────────────────────────────────
def analyze_chunk(words, threshold):
    weak = [w for w in words
            if w.get("PronunciationAssessment", {}).get("AccuracyScore", 100) < threshold]
    if not weak:
        return None

    words_info = []
    for w in weak:
        words_info.append({
            "word": w.get("Word", "?"),
            "correct_ipa": word_to_ipa(w),
            "accuracy_score": w.get("PronunciationAssessment", {}).get("AccuracyScore", 0),
            "syllables_heard": [
                {"heard_as": s.get("Syllable", "?"), "score": s.get("PronunciationAssessment", {}).get("AccuracyScore", 0)}
                for s in w.get("Syllables", [])
            ],
            "phonemes": [
                {"phoneme": p.get("Phoneme", "?"), "score": p.get("PronunciationAssessment", {}).get("AccuracyScore", 0)}
                for p in w.get("Phonemes", [])
            ],
        })

    system = (
        "You are a pronunciation coach for Chinese (Mandarin) speakers learning English.\n"
        "For EACH word, provide:\n"
        "1. 🔀 **容易被误听为**: what English word(s) this might sound like\n"
        "2. 🇨🇳 **中文母语者的原因**: why Mandarin speakers make this error\n"
        "3. 💡 **怎么纠正**: one concrete tip\n\n"
        "Format: ### word. Keep each to 3-5 lines. Do NOT use any tools."
    )
    prompt = f"Analyze:\n{json.dumps(words_info, indent=2, ensure_ascii=False)}"

    async def _call():
        from claude_code_sdk import (
            query, ClaudeCodeOptions,
            AssistantMessage, TextBlock, ResultMessage,
        )
        options = ClaudeCodeOptions(
            max_turns=1, system_prompt=system,
            allowed_tools=[], model="claude-haiku-4-5-20251001",
        )
        result_text = ""
        for attempt in range(3):
            try:
                async for msg in query(prompt=prompt, options=options):
                    if isinstance(msg, AssistantMessage):
                        for block in msg.content:
                            if isinstance(block, TextBlock):
                                result_text += block.text
                    elif isinstance(msg, ResultMessage):
                        if not result_text and msg.result:
                            result_text = msg.result
                return result_text
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < 2:
                    time.sleep(10 * (attempt + 1))
                else:
                    return f"Error: {e}"
        return result_text

    return asyncio.run(_call())


def analyze_all(results, threshold, output_dir):
    print(f"[4/5] Running Claude analysis...")
    analysis_dir = output_dir / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)

    for r in results:
        stem = r["path"].stem
        words = r["nb"].get("Words", [])
        weak_count = sum(1 for w in words
                         if w.get("PronunciationAssessment", {}).get("AccuracyScore", 100) < threshold)
        if weak_count == 0:
            print(f"  {stem}: no weak words, skipping")
            continue

        print(f"  {stem}: analyzing {weak_count} weak words...", end=" ", flush=True)
        analysis = analyze_chunk(words, threshold)
        if analysis and not analysis.startswith("Error:"):
            (analysis_dir / f"{stem}.md").write_text(analysis)
            print("done")
        else:
            print(f"failed: {(analysis or '')[:80]}")
        time.sleep(2)


# ─── Step 5: Generate report ─────────────────────────────────────────────
def generate_report(results, manifest, threshold, output_dir, audio_name):
    print(f"[5/5] Generating report...")
    analysis_dir = output_dir / "analysis"

    lines = []
    lines.append(f"# Pronunciation Report")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Audio: {audio_name}")
    lines.append("")

    total_words = len(manifest)
    total_weak = sum(1 for m in manifest if m["weak"])
    all_acc = []
    all_flu = []

    for r in results:
        pa = r["nb"].get("PronunciationAssessment", {})
        all_acc.append(pa.get("AccuracyScore", 0))
        all_flu.append(pa.get("FluencyScore", 0))

    avg_acc = sum(all_acc) / len(all_acc) if all_acc else 0
    avg_flu = sum(all_flu) / len(all_flu) if all_flu else 0

    lines.append("## Overall")
    lines.append(f"- Chunks: {len(results)} | Words: {total_words} | Weak words: {total_weak}")
    lines.append(f"- Avg accuracy: {avg_acc:.1f} | Avg fluency: {avg_flu:.1f}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for idx, r in enumerate(results):
        stem = r["path"].stem
        nb = r["nb"]
        pa = nb.get("PronunciationAssessment", {})
        text = nb.get("Display", "")

        acc = pa.get("AccuracyScore", 0)
        flu = pa.get("FluencyScore", 0)
        comp = pa.get("CompletenessScore", 0)
        pron = pa.get("PronScore", 0)

        lines.append(f'## Chunk {idx+1}: "{text}"')
        lines.append(f"🎧 Audio: `chunks/{stem}.wav`")
        lines.append(f"| Acc: {acc:.0f} | Flu: {flu:.0f} | Comp: {comp:.0f} | Pron: {pron:.0f} |")
        lines.append("")

        chunk_words = [m for m in manifest if m["chunk"] == stem]

        # All words table
        lines.append("### All words")
        lines.append("")
        lines.append("| Word | IPA | Score | Your audio | Start | End |")
        lines.append("|------|-----|-------|------------|-------|-----|")
        for m in chunk_words:
            clip_link = f"![[{m['clip_file']}]]"
            lines.append(
                f"| {m['word']} | /{m['ipa']}/ | {m['score']:.0f} "
                f"| {clip_link} "
                f"| {m['start_ms']} | {m['end_ms']} |"
            )
        lines.append("")

        # Weak words detail
        weak_words = [m for m in chunk_words if m["weak"]]
        if weak_words:
            lines.append("### Words to practice")
            lines.append("")
            lines.append("| Word | IPA | Score | Your audio | Correct audio | Weak phonemes |")
            lines.append("|------|-----|-------|------------|---------------|---------------|")

            for m in weak_words:
                yours_link = f"![[{m['clip_file']}]]"
                correct_link = f"![[{m['tts_file']}]]" if m["tts_file"] else "-"
                weak_phs = [
                    f"/{p['phoneme']}/ {p['score']:.0f}"
                    for p in m["phonemes"]
                    if p["score"] < threshold
                ]
                phs_str = ", ".join(weak_phs) if weak_phs else "-"
                lines.append(
                    f"| {m['word']} | /{m['ipa']}/ | {m['score']:.0f} "
                    f"| 🔴 {yours_link} "
                    f"| 🟢 {correct_link} "
                    f"| {phs_str} |"
                )
            lines.append("")

            lines.append("### Phoneme details")
            lines.append("")
            seen = set()
            for m in weak_words:
                for p in m["phonemes"]:
                    if p["score"] < threshold and p["phoneme"] not in seen:
                        seen.add(p["phoneme"])
                        pn = p["phoneme"].lower()
                        zh = PHONEME_ZH.get(pn, "")
                        zh_line = f"\n  💡 {zh}" if zh else ""
                        lines.append(f"- **/{p['phoneme']}/** → /{p['ipa']}/ — Score: {p['score']:.0f}{zh_line}")
            lines.append("")

        # Claude analysis
        af = analysis_dir / f"{stem}.md"
        if af.exists():
            lines.append("### AI Analysis")
            lines.append("")
            lines.append(af.read_text().strip())
            lines.append("")

        lines.append("---")
        lines.append("")

    report_path = output_dir / "report.md"
    report_path.write_text("\n".join(lines))
    print(f"  Report: {report_path}")
    return report_path


# ─── Resolve output dir ─────────────────────────────────────────────────
def resolve_output_dir(audio_path, explicit_output):
    if explicit_output:
        return Path(explicit_output).resolve()
    repo_root = Path(__file__).resolve()
    for parent in repo_root.parents:
        candidate = parent / "_WorkSpace" / "LearnStore"
        if candidate.exists():
            stem = audio_path.stem
            return candidate / "pronunciation" / stem
    ts = datetime.now().strftime("%y%m%d-%H%M%S")
    return audio_path.parent / f"pronunciation-report-{ts}"


# ─── Main ─────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Pronunciation analysis pipeline")
    parser.add_argument("audio", help="Path to audio file")
    parser.add_argument("--ref", default="", help="Reference text (what you intended to say)")
    parser.add_argument("--output", default="", help="Output directory (default: LearnStore)")
    parser.add_argument("--threshold", type=int, default=70, help="Weak word threshold (default: 70)")
    parser.add_argument("--skip-analysis", action="store_true", help="Skip Claude analysis step")
    parser.add_argument("--reclip", action="store_true", help="Re-clip from edited words.json (no Azure call)")
    args = parser.parse_args()

    audio_path = Path(args.audio).resolve()
    if not audio_path.exists():
        print(f"Error: {audio_path} not found")
        return

    output_dir = resolve_output_dir(audio_path, args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.reclip:
        reclip_from_manifest(output_dir)
        return

    print(f"Audio: {audio_path}")
    print(f"Output: {output_dir}")
    print(f"Threshold: {args.threshold}")
    print()

    key = get_azure_key()
    chunk_paths = convert_and_split(audio_path, output_dir)
    results = assess_all(chunk_paths, args.ref or None, key, output_dir)

    if not results:
        print("No chunks were successfully assessed.")
        return

    manifest = build_words_manifest(results, args.threshold)

    manifest_path = output_dir / "words.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"  Manifest: {manifest_path} ({len(manifest)} words)")

    clip_all_words(manifest, output_dir)

    if not args.skip_analysis:
        analyze_all(results, args.threshold, output_dir)

    report = generate_report(results, manifest, args.threshold, output_dir, audio_path.name)

    print()
    print(f"{'='*50}")
    print(f"Done! Report at: {report}")
    print(f"Manifest: {manifest_path}")
    print(f"To adjust word boundaries: edit words.json, then run:")
    print(f"  python pipeline.py {args.audio} --reclip --output {output_dir}")


if __name__ == "__main__":
    main()
