# Validation scope — v1.1.0 (2026-10-05)

## Passed locally
26 regression/integration tests: canonical audio mode/timeline, cue/asset provenance, malformed fps/version, gaps/coverage, layouts, safe area, Unicode, path traversal, short source trim, mixer placement and voice ducking, measured loudness, repeated/shuffled/sequential Pillow pixels, odd yuv420p dimensions, installer diff/backup/legacy refusal/local-edit protection, full two-format Pillow render and silent render.

The original six-second sample rendered as 180 frames at 30fps, 960x540 and 540x960, with H.264/yuv420p video and 48kHz stereo AAC audio. Both exports passed ffprobe comparisons and full decode. Lossless mix measured -16.07 LUFS / -9.43 dBTP; encoded audio measured -16.06 LUFS / -9.43 dBTP. These are actual observations for the sample, not requirements for every future film. SHA-256 seek checks operate within one runtime; they do not assert pixel equivalence across OS/fonts.

A fresh agent used the documented workflow to generate both formats, inspected contact sheets and phone posters, and correctly left full playback/listening pending. A node-size reset identified in sample stills was removed; the updated frame function passed the targeted deterministic seek test. The sample is original procedural artwork, not a client film or evidence of professional equivalence.

## Separate Canvas status
Canvas now awaits motionReady and uses SHA-256 decoded RGBA digests. Node syntax checks passed. Chromium remains absent in the local authoring environment; its earlier download failed. GitHub Actions defines a real Chromium two-format pipeline job with original audio and retained evidence. Read the current workflow result before claiming this engine's end-to-end check passed. Pillow success does not imply Canvas success.

## Pending perceptual checks
No full-video playback or audio listening was observed in authoring. The runner deliberately emits technical_pass_review_pending and final=false. Future productions must review actual motion, sound, readability and truthful claims against the exported film/spec hashes. No actual Opus model production session was run here.

## Confirmed GitHub Actions evidence
Run https://github.com/ptrgiang/motion-studio/actions/runs/37299324016 completed successfully for code commit 3eac78435485c7f9fa2caaae06cd6f702540910f. Windows regression, Ubuntu regression/full Pillow integration, and Chromium two-format rendering jobs all passed. The Canvas artifact was downloaded and checked: wide and vertical each have 180 captured frames, 180 passing reverse-seek SHA-256 checks, a passing direct/sequential check, technical encode/decode QC, and encoded audio measured -16.06 LUFS / -9.43 dBTP. Both Canvas poster frames were inspected for layout/readability. Full video playback/listening remain pending; CI success is technical evidence, not creative approval.


## v1.2 local verification (2026-10-05)

Six new recipes and twelve blind controls were rendered through Pillow/FFmpeg in wide and vertical: 24 silent four-second films. Exact frame counts, durations, dimensions, H.264 decode and seek checks passed. Representative final layouts were inspected; a mask compositing fix retains the header/footer. The new benchmark report correctly leaves all twelve cases pending without recorded reviews. No aesthetic aggregate or full-playback approval is claimed.

New unit checks exercise every recipe and variant, both formats, seek order, blind manifests, stale media, exact still-frame evidence, score types and unobserved playback gating. CI adds a full 24-film calibration job alongside existing Windows/Linux regression and Chromium audio checks. See the repository workflow for current results; this document does not predeclare CI success for v1.2.
