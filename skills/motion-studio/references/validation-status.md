# Authoring validation (2026-10-05)

Passed: frontmatter/basic validation for seven skills; production initialization; a valid two-format spec; seven rejected malformed cases (fps boolean, timeline gap, short coverage, unknown asset, missing format layout, empty safe area, invalid transition); frame sampling; seven-skill Claude export and overwrite refusal; contact sheets from stills and exact decoded video frames, inspected wide/vertical sheets; an FFmpeg fixture encoded as 60 frames, 30fps, 960x540, 2 seconds.

Passed with limited scope: Canvas frame function executes under a mocked drawing context and repeats identical draw operations after shuffled seeks in both formats; frame bounds and unknown formats reject correctly. render.mjs passes Node syntax check.

Not verified: real Chromium capture, actual Canvas pixel determinism and the complete Playwright-to-video pipeline. Chromium was absent and its download failed in the authoring environment. The FFmpeg fixture was generated separately for tool testing, not by the Canvas starter. Do not report this as an end-to-end browser rendering pass.

No actual Opus session or production client film was run. No artistic quality, audio mix/listening, platform performance or professional equivalence is certified by these tests. Re-run actual render and perceptual checks on a capable production machine before final delivery.

## Independent pre-production exercise
A fresh task used this pack for a 16-second accounting-app launch requesting real UI but supplying none. It produced provisional brief/story/layout records and explicitly labelled schematic animatics, without inventing UI, metrics, logo or product facts. Required identity/capture assets remained missing; validation reported ten asset-related errors with no timing/layout/schema errors. G1/G2 remained blocked and later gates pending. Optional missing music/reference did not prevent concept work; silence was documented. This confirms missing-input behavior for that scenario, not final-film artistic quality.
