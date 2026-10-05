# Executable production pipeline

## Prepare and run
From the skill directory, or replace these paths with absolute ones:
`python3 scripts/doctor.py --engine pillow`
`python3 scripts/pipeline.py demo /path/to/new-demo`
`python3 scripts/pipeline.py run /path/to/new-demo --engine pillow --run-id v1`

The original six-second demo has 180 frames at 30fps, explicit 960x540 and 540x960 layouts, and synthesized original audio. It proves a renderer/toolchain; it is not a client product film. Set final required resolution in spec and inspect readability again. For a new film, use studio.py init, write truthful brief/assets/spec, and create src/pillow_composition.py or the browser composition to match the brief.

## Engine contracts
Pillow: src/pillow_composition.py exposes render_frame(frame,spec,format_id,project), returns RGB image with exact format dimensions. Direct/shuffled/sequential seeks compare SHA-256 decoded RGB bytes at representative frames. Use MOTION_FONT_PATH for an explicit licensed font. Capture the resolved font hash.
Canvas: src/canvas-starter.html exposes async renderFrame and async frameDigest (SHA-256 of decoded RGBA); optional motionReady is awaited. src/render.mjs uses project-installed Playwright. From project root install exact pinned dependencies and its Chromium: npm install; npx playwright install chromium. Then run doctor.py --project <project> --engine canvas and pipeline.py run --engine canvas. MOTION_CHROMIUM_PATH can select an already installed compatible browser. No silent fallback to Pillow occurs on Canvas failure.

## Audio
Only spec.json.audio_cues drives the mixer. Designed audio requires approved provenance assets for cue paths. Optional cue role music/voice/sfx groups buses; voice ducks music, and fades precede frame-aligned placement at 48kHz. Trim ranges longer than source fail. Normalize in two passes, measure the exported WAV and encoded film; reject silent/unmeasurable audio or missed targets. Default -16 LUFS with +/-1 tolerance, true peak <= -1 dBTP with small measurement/encoding tolerances. A true peak far below the ceiling is valid. Targets are adjustable draft policy, not universal platform specifications.

## Evidence and checkpoints
Each fresh run is isolated under project/out/<run-id>. A run-id cannot overwrite earlier output. pipeline-state.json records stages and failure reason. The runner aborts on failure rather than filling missing media or claiming completion. A new run-id rerenders; incremental scene resume is not implemented.

Each ratio receives film.mp4, poster.png, phone-poster.png, contact-sheet.png, transition preview clips, frame digest evidence and qc.json. The run includes lossless audio/mix measurement, samples.json, manifest.json with source/spec/asset hashes and actual runtime versions, review.json with matching film hashes, and delivery.md.

Technical checks: exact count/fps/dimensions, H.264/yuv420p, expected audio stream/duration, full decode, output measurements. Odd dimensions are rejected for yuv420p. Store Unicode JSON as UTF-8.

## Review boundary
Success status is technical_pass_review_pending. Open the generated image evidence, review full/transition playback and listen to audio. Record observations against the encoded film/spec hashes, fix local defects, and produce new evidence when changed. No machine-generated artistic pass, waveform-derived listening claim or automatic final approval is emitted.
