# Validation scope — v1.2.0 (2026-10-05)

## Current release evidence

Tested code commit: `d6f9f76202482d732298337d9aba625b03734f1d`.
[GitHub Actions run 37303373349](https://github.com/ptrgiang/motion-studio/actions/runs/37303373349) passed all four jobs: Windows regression, Ubuntu regression plus full Pillow integration, real Chromium/audio in both formats, and all 24 silent calibration films. Public calibration and Canvas evidence are retained as seven-day workflow artifacts.

Locally, all 32 tests passed with integration enabled. A fresh agent materialized and rendered a study using the instructions; observed mask compositing/travel issues were repaired and the updated study rendered again in both formats. A fresh Claude-directory export resolved sibling skills and validated a standalone study; install version is 1.2.0.

The Windows FFmpeg 9 run exposed unbounded output in the existing audio ducking path. The mixer now bounds padding and trim by exact sample count, resets output timestamps, adds an output duration limit and reports captured FFmpeg diagnostics. The regression asserts exactly 288,000 raw samples for the six-second fixture; Windows now passes.

Perceptual scope remains limited to inspected representative stills. No full-film playback/listening approval, automatic aesthetic score, professional gold-standard equivalence or actual Opus production session is claimed. The twelve blind benchmark reviews remain pending until reviewers inspect and record evidence.

## Historical v1.1 evidence

The following records describe the earlier sample and verification history.

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

Six new recipes and twelve blind controls were rendered through Pillow/FFmpeg in wide and vertical: 24 silent four-second films. Exact frame counts, durations, dimensions, H.264 decode and seek checks passed. Representative final layouts were inspected; forward usage identified mask/annotation compositing and extra edge travel; fixes retain the header/footer and align travel to headline bounds. The new benchmark report correctly leaves all twelve cases pending without recorded reviews. No aesthetic aggregate or full-playback approval is claimed.

New unit checks exercise every recipe and variant, both formats, seek order, blind manifests, stale media, exact still-frame evidence, score types and unobserved playback gating. CI adds a full 24-film calibration job alongside existing Windows/Linux regression and Chromium audio checks. See the repository workflow for current results; this document does not predeclare CI success for v1.2.
