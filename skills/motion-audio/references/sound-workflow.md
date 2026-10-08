# Sound workflow

## Cue semantics
start_frame: cue placement on global picture timeline.
duration_frames: intended cue region, including tail.
source_offset_seconds: trim into source, not timeline time.
visual_event_frame: frame where action/hit occurs.
intentional_offset_frames: explicit perceptual lead/lag when needed.
Store relative media paths in project and verify existence. Audio sample placement can use fractional samples computed from frame time, but do not mutate picture timing to match a rounding error.

## Measurement
Use `ffmpeg -i mix.wav -af loudnorm=I=-16:TP=-1:LRA=11:print_format=json -f null -` for analysis when these targets fit. The filter's measured input values describe the source; do not report its target as an observed result. A two-pass loudnorm workflow needs values from the first pass applied to the second, then output remeasurement. Use sample rate 48kHz for a normal video master unless destination requires another. Keep a lossless mix as well as delivery audio.

## Beat decision
A click confirms an interaction; place it at contact/activation, not after a button has settled. A reveal hit can emphasize the information change. A riser needs an earned resolution. Silence can make an important hold stronger. Avoid five different sounds for one operation. If there is no music, synthesize an original limited cue palette and still review the shape with eyes closed.

## Missing input
If licensed music is required but absent, continue visual production and output a clearly labeled silent draft while reporting the missing track. If silent delivery is allowed by the brief, finalize silent and score sync as not applicable with a reason.

## Executable mixer
Use `python3 <motion-studio-dir>/scripts/audio.py <project> --output <new-output-directory>`. Canonical inputs are `spec.json.audio_cues` and asset provenance; no separate audio-cues.json is accepted. Cue role is music, voice or sfx. Optional fade_in_seconds/fade_out_seconds apply before cue placement. Music ducks against the summed voice bus using sidechain compression when both exist. Export a 48kHz stereo PCM mix, measure it, normalize in two passes, remeasure and retain audio-qc.json. Targets default to -16 LUFS and -1 dBTP; override through audio_target in spec. Measured results describe the file, not proof of intelligibility or artistic sync. Mark audio listening pending until actually heard.

## v1.3 procedural event cues

Use motion-studio's `scripts/sfx.py PROJECT --event saveNote --kind click --id save-click --frames 6`. Optional `--offset` is an intentional integer pre/post-lap and `--gain-db` sets cue gain. Define `spec.events.saveNote` first. Kinds: click, tick, blip, whoosh, riser, impact, pad. The generator writes original 48kHz mono PCM, records usable original provenance and a linked canonical audio cue. It switches explicit audio mode to designed; existing other cues remain intact.

Sound seed derives from project seed, cue ID, event ID and kind; adding/reordering another cue does not alter existing noise. Exact sample count derives from frames/fps. Inputs must fit the timeline, and existing IDs/files are refused. These are small procedural textures, not guaranteed polished music. Use the existing mixer for stereo buses, voice ducking, two-pass LUFS normalization and encoded true-peak measurement. Do not replace these checks with raw RMS/peak or assume synthesized audio sounds good without listening.
