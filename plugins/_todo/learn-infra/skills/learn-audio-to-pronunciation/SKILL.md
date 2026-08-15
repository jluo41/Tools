---
name: learn-audio-to-pronunciation
description: "Given an audio file, split into sentence chunks, run Azure pronunciation assessment, clip ALL words with timestamps, generate TTS for weak words, call Claude for confusion/Chinese analysis, and output an Obsidian-friendly markdown report with clickable audio. Stores results in _WorkSpace/LearnStore/pronunciation/."
trigger: pronunciation report, audio pronunciation, assess audio, pronunciation analysis, 发音分析, 发音报告, /learn-audio-to-pronunciation
---

# learn-audio-to-pronunciation

Generate a full pronunciation analysis report from an audio file.

## Input

An audio file (WAV, OGG, MP3, M4A, FLAC) and optionally a reference text.

```
/learn-audio-to-pronunciation <audio-path> [--ref "what you intended to say"] [--output <dir>]
```

## Pipeline

```
Audio file (any length)
  │
  ├─ 1. CONVERT + SPLIT
  │     Convert to 16kHz mono WAV.
  │     If > 10s, split on silence (~8-9s chunks).
  │     Output: chunks/*.wav
  │
  ├─ 2. ASSESS (Azure Speech SDK)
  │     Run pronunciation assessment per chunk.
  │     Output: assess/*.json (full Azure response with phonemes, syllables, timestamps)
  │
  ├─ 3. CLIP ALL WORDS + TTS
  │     Clip ALL words from audio using Azure offset/duration timestamps.
  │     Generate TTS correct pronunciation for weak words only.
  │     Build words.json manifest with editable start_ms/end_ms per word.
  │     Output: audio/words/*.wav, audio/tts/*.wav, words.json
  │
  ├─ 4. ANALYZE (Claude via OAuth SDK)
  │     Send weak words + Azure phoneme/syllable data to Claude.
  │     For each word:
  │       - 🔀 What it might sound like (confusion words)
  │       - 🇨🇳 Why Chinese/Mandarin speakers make this error
  │       - 💡 How to fix it
  │     Output: analysis/*.md
  │
  └─ 5. REPORT (Obsidian-friendly)
        Combine everything into a structured markdown report.
        Uses ![[file.wav]] embeds for clickable audio in Obsidian.
        Output: report.md
```

## Output structure

Default output: `_WorkSpace/LearnStore/pronunciation/<audio-stem>/`

```
_WorkSpace/LearnStore/pronunciation/<audio-stem>/
├── report.md                    # Obsidian-friendly report with ![[]] audio embeds
├── words.json                   # Manifest: all words with start_ms, end_ms, scores
├── chunks/
│   ├── chunk_001.wav
│   └── chunk_002.wav
├── assess/
│   ├── chunk_001.json           # Azure assessment JSON (full timing data)
│   └── chunk_002.json
├── audio/
│   ├── words/                   # ALL words clipped from audio
│   │   ├── delegate.wav
│   │   ├── knowledge.wav
│   │   └── ...                  # every word, not just weak ones
│   └── tts/                     # Correct pronunciation (weak words only)
│       ├── delegate.wav
│       └── knowledge.wav
└── analysis/
    ├── chunk_001.md             # Claude analysis per chunk
    └── chunk_002.md
```

## words.json manifest

Each word entry contains:

```json
{
  "word": "person",
  "word_index": 5,
  "chunk": "chunk_001",
  "start_ms": 2960,
  "end_ms": 3590,
  "score": 11.0,
  "error_type": "Mispronunciation",
  "ipa": "/ˈpərsən/",
  "weak": true,
  "clip_file": "words/person.wav",
  "tts_file": "tts/person.wav",
  "syllables": [...],
  "phonemes": [...]
}
```

To adjust word boundaries: edit start_ms/end_ms in words.json, then:
```bash
python pipeline.py <audio> --reclip --output <dir>
```

## Re-assess with reference text

Run with `--ref` to improve Azure word segmentation:
```bash
python pipeline.py recording.ogg --ref "I'm totally know nothing about Python and learn model"
```
This overwrites the existing results with better word boundaries and scores.

## Dependencies

All in the shared venv at `jluo41-repo/.venv`:
- `pydub` — audio splitting and clipping
- `azure-cognitiveservices-speech` — assessment + TTS
- `eng-to-ipa` — IPA with stress marks
- `claude-code-sdk` — Claude OAuth for analysis
- `pyyaml`, `static-ffmpeg`

## Environment

- `AZURE_SPEECH_KEY` — Azure Speech Services key
- Claude Code OAuth — via `~/.claude` (free under subscription)

## On trigger

Parse args for: `<audio-path>` (required), optional `--ref "text"`, optional `--threshold N`.

```bash
# 1. Source Azure key
source MacStudio-Service/VoiceEcho/env.sh

# 2. Run the pipeline
.venv/bin/python Tools/plugins/learn-infra/skills/learn-audio-to-pronunciation/ref/pipeline.py \
  <audio-path> [--ref "text"] [--threshold N] [--skip-analysis]

# 3. Read and show the report inline
cat _WorkSpace/LearnStore/pronunciation/<audio-stem>/report.md
```

After the pipeline finishes:
- Show the report.md content to the user
- Highlight weak words and their scores
- Mention that results are in `_WorkSpace/LearnStore/pronunciation/<stem>/`
- If the user wants to adjust boundaries, show the `--reclip` command

## Integration with VoiceEcho

Both this skill and VoiceEcho (`MacStudio-Service/VoiceEcho/`) can read from
`_WorkSpace/LearnStore/pronunciation/`. The assess JSON and words.json are compatible.
VoiceEcho can be updated to read from LearnStore as its data source.
