---
name: motion-audio
description: "Plan and implement sound design, voiceover, music edits and audio mixing on the same frame timeline as a motion film. Use for cue sheets, beat alignment, loudness measurement and audio-visual sync review."
---

# Motion Audio

Read [sound-workflow.md](references/sound-workflow.md). Shape the film's sound with the same timeline that controls picture.

1. Inspect available source audio, rights/provenance and desired voice/music style. Record whether the film is intentionally silent. Do not substitute a commercial song from a visual reference without usable rights. Use a licensed supplied track or original synthesized cues; use TTS only when tools and permission exist.
2. Build `audio-plan.md` and update the sole cue timeline, `spec.json.audio_cues`: id, path, start_frame, duration_frames, trim offset, gain/fades, purpose and linked visual event. Set `audio_mode` to `designed` or explicitly `silent`; never create a second cue file. Keep exact sync cues and flexible musical accents distinct.
3. For recorded voice, finalize approved script and actual recording timing first, then adjust holds. Do not animate to an imagined speaking duration. Include pronunciation/localization review and readable caption timing when requested.
4. Measure or manually inspect actual beat/onset positions. Align major cuts and reveals where this helps the narrative; do not snap every interaction to a beat at the expense of believable UI behavior. Use pre-lap/tails intentionally.
5. Mix voice for intelligibility, control competing music, avoid harsh repetitive whooshes, clipping and abrupt tails. Choose output targets based on destination. As a starting web draft policy use approximately -16 LUFS integrated and <= -1 dBTP; measure before claiming either target. Do not apply normalization twice.
6. Render picture and audio, inspect waveform/peaks and listen separately, then watch together on headphones and modest speakers when possible. Check cue onset against the linked event (default sync tolerance one frame, adjustable for deliberate offset).
7. Report what was heard and measured. If listening was unavailable, mark perceptual audio review pending even if a loudness script passed. Hand the mixed asset, cue sheet and evidence to `motion-review`.

Locate `motion-studio` and use its `scripts/audio.py` for frame-based placement, fades, voice/music ducking, two-pass normalization and output measurement. Read [sound-workflow.md](references/sound-workflow.md) for CLI and limits.

Do not call sound finished from a contact sheet. An intentionally silent film is valid only if it fits the brief and is explicitly recorded.

For original event-seeded procedural cues, use motion-studio’s `scripts/sfx.py` and the v1.3 section of [sound-workflow.md](references/sound-workflow.md). Link generated cues to named events in the sole spec and retain the existing measured mixer/listening gates.

## Showreel revisions

For a studio intro, brand reel or slideshow critique, resolve motion-studio by frontmatter name and read references/showreel-craft.md. Follow the motif/action/camera/reading plan and use executable craft tools when appropriate. Review encoded results; ambient wobble is not narrative motion and a machine pass is not creative approval.
