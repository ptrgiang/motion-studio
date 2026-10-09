# Validation scope — v1.4.0 (2026-10-09)

## Current v1.4 release evidence

Tested code commit: `5c4989d3e2a85dca88fd29ea0a8a04bc56de245d`.
[GitHub Actions run 37872009746](https://github.com/ptrgiang/motion-studio/actions/runs/37872009746) passed all five jobs: Windows/Ubuntu regression, full Pillow integration, existing Canvas/audio, 24-film calibration, and real local capture/DOM render/preview integration. The regression suite contains 49 tests; full integration also runs separately on Ubuntu. Locally the prior 48-test suite passed with integration enabled, and the updated nine-test v1.4 subset (including the additional camera check) passed.

Downloaded DOM evidence confirms both 15-second exports have 450 frames at 30fps, 18 passing reverse-seek checks, a passing direct/sequential check, passing layout samples and encode/decode QC. The renderer rebuilds stage paint state and disables LCD text rasterization to remove retained subpixel glyph-edge artifacts; exact PNG-hash checks remain enabled. Browser/runtime and rasterization choices are recorded. Padded text paint bounds keep ink inside text containers.

Actual browser integration passed frame stepping, format switch, safe-area display, camera cursor/ripple alignment, deliberately small/overlapping text diagnostics, short-hold diagnostics, encoded H.264/AAC metadata and play/pause, preserved frame on view switch, notes export and pending bound-review import. Automated playback checks do not establish human full-film inspection. Preview UI screenshot and representative evidence were inspected.

Readability diagnostics retain meaningful warnings: 19 sampled small-text/control warnings in wide, zero such sampled warnings in vertical, and a short estimated copy hold for the local shot. These are heuristic findings, not failures hidden as creative approval. Screenshot label text is not OCR-checked; full phone-size review remains required.

A fresh agent created and technically verified an original six-second silent Pillow film in both formats, inspected still evidence and imported per-format visual observations. The review correctly retained temporal inspection pending and treated intentional silence as not requiring listening. A standalone Claude-directory v1.4 export initialized a DOM study. Installed dependencies and capture are still required in the target environment.

Full DOM-film playback/listening and creative approval remain pending. The manifest keeps final=false. No actual Opus production session or professional aesthetic score is claimed. CI artifacts are retained for seven days.

## Historical v1.3 release evidence

Tested code commit: `c18519a3756ffa08c44fdec744de6a402f441290`.
[GitHub Actions run 37775799052](https://github.com/ptrgiang/motion-studio/actions/runs/37775799052) passed the real local UI capture/DOM promo, existing Chromium/audio, Windows regression and 24-film calibration jobs. The Ubuntu regression job timed out during package installation; its tests did not run in this attempt. The four other jobs passed. v1.4 bounds package-manager waits and checks installed tools first.

Forty local regression/integration tests passed. A fresh agent prepared the demo from the skill instructions and correctly reported missing local Chromium and required uncaptured UI assets. A standalone Claude-directory export validated the materialized study; install version is 1.3.0.

The DOM artifact was downloaded and checked: both formats have 450 frames at 30fps and exactly 15 seconds, H.264/yuv420p, stereo 48kHz AAC, passing full decode, 13 passing reverse-seek checks, a passing sequential/direct check and 13 passing tagged-layout samples. Original app save/reload persistence and theme toggle, three 2000x1400 captures with DPR2 geometry, shuffled rendering and missing external-asset failure passed in real Chromium. A vertical end-card pulse initially exceeded safe bounds by 3.68 pixels; the title width now reserves its maximum scale and browser regression covers the peak frame in both formats.

Measured lossless mix: -16.03 LUFS / -5.55 dBTP. Encoded exports: -16.05 LUFS / -5.56 dBTP. These are observed sample results. Representative capture, contact-sheet and poster stills were inspected; full-film playback/listening and creative review remain pending. The manifest intentionally retains `final=false`. No actual Opus production session or professional aesthetic score is claimed. Retained CI artifacts expire after seven days.

## Historical v1.2 release evidence

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


## v1.3 authoring scope (2026-10-08)

Forty local tests passed with Pillow integration enabled. New checks cover event-linked cue drift, each procedural SFX kind, stable per-cue seeds/sample counts, font cmap/rights assertion/hash checks, capture metadata tampering, timing/keyframe/shot behavior and complete transform resets. The DOM demo and local functional app are independently authored; browser execution is assigned to a dedicated Chromium CI job because local Chromium is unavailable.

The new CI job runs actual local-app save/persistence/theme tests, three-state 2x captures, CSS/pixel coordinate checks, shuffled DOM rendering, blocked external-asset failure and full two-format 15-second DOM/audio encoding with tagged layout/seek evidence. The successful run and downloaded evidence are recorded above. Perceptual playback/listening remains pending. No professional aesthetic score is claimed.
