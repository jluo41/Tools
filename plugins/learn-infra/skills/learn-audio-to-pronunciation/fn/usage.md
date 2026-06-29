# Usage

## Quick start

```bash
# Source env for Azure key
source MacStudio-Service/VoiceEcho/env.sh

# Run on an audio file (auto-outputs to _WorkSpace/LearnStore/pronunciation/)
python Tools/plugins/learn-infra/skills/learn-audio-to-pronunciation/ref/pipeline.py \
  path/to/recording.ogg

# With reference text (better word segmentation)
python ... path/to/recording.ogg --ref "Can you delegate this to a sub agent"

# Custom output dir + threshold
python ... path/to/recording.ogg --output ./my-report --threshold 75

# Skip Claude analysis (faster, Azure-only)
python ... path/to/recording.ogg --skip-analysis

# Re-clip after editing word boundaries in words.json
python ... path/to/recording.ogg --reclip --output _WorkSpace/LearnStore/pronunciation/<stem>
```

## From Claude Code skill

```
/learn-audio-to-pronunciation path/to/recording.ogg
```

The skill will:
1. Run the pipeline
2. Show the report inline
3. Offer to open weak word audio comparisons

## Viewing results

The output directory (default `_WorkSpace/LearnStore/pronunciation/<stem>/`) contains:
- `report.md` — Obsidian-friendly with `![[file.wav]]` embeds for clickable audio
- `words.json` — manifest with all word boundaries (editable start_ms/end_ms)
- `audio/words/*.wav` — ALL words clipped from your audio
- `audio/tts/*.wav` — correct pronunciation for weak words
- `assess/*.json` — raw Azure data with full timing

## Adjusting word boundaries

1. Open `words.json`
2. Find the word entry and change `start_ms` / `end_ms`
3. Re-clip: `python pipeline.py <audio> --reclip --output <dir>`

## In Obsidian

Open `report.md` in Obsidian. The `![[words/person.wav]]` embeds become clickable
audio players. You can hear each word and compare with `![[tts/person.wav]]`.

## Importing into VoiceEcho

The LearnStore results are directly compatible with VoiceEcho.
VoiceEcho can be configured to read from `_WorkSpace/LearnStore/pronunciation/`.
