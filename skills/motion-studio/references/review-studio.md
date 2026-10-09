# Review studio — v1.4

## Prepare and inspect a run

Render a fresh run with pipeline.py. It records an input snapshot (spec, inventory, registered asset bytes, source, capture plan and dependency files) and creates review-v1.4.json with pending per-format observations. Existing v1.3 runs must be rendered again; do not manufacture a snapshot for an old film.

Run `python <motion-studio-dir>/scripts/preview.py PROJECT --run-id RUN`. Open the printed localhost URL. The server is read-only, binds 127.0.0.1 and serves allowed project media/source plus bundled review UI. It does not publish a website or attach to an existing browser account. Stop with Ctrl+C.

Live composition uses the project's frame function and the run's lossless audio mix. Frame stepping, timeline seek, format switching and the safe-area overlay are review tools. Live view is supported for bundled DOM/Canvas entrypoints. Pillow supports encoded-film review. Live preview can drop frames on a slow device; inspect the encoded film for temporal delivery quality. DOM uses src/promo.html and Canvas uses src/canvas-starter.html; adapt those entrypoints for custom films.

Use Encoded film to watch the delivered MP4 and listen to its encoded audio. A technical browser test of the controls does not establish that a person watched or listened. Record actual observations separately for every requested format. Add timestamped open defects and describe what was inspected. Checkbox changes are explicit assertions, never inferred from play events.

Export review notes, then run `python <motion-studio-dir>/scripts/review.py import PROJECT --run-id RUN --notes /path/motion-review-notes.json`. The tool rejects mismatched inputs/export hashes, missing formats, nonboolean observations and malformed defect frames. Existing review files are backed up. Run `review.py assess PROJECT --run-id RUN` to list pending observations/open defects. Intentional silence needs no listening assertion. Review completion is a recorded observation state, not an automatic aesthetic certificate or publication action; the pipeline manifest remains a draft.

## Repair without losing evidence

Fix the highest-impact defects and render a new run. Old review stays attached to the old export and becomes stale against current source. New observations start pending. Run `review.py compare PROJECT --run-id AFTER --before BEFORE` to produce a hash-bound changed-input report. This permits the historical input snapshot to differ while verifying old/new export bytes. It does not inherit approvals or automatically prove the repair. Inspect both versions and record the resolution in new notes. Resolved defects require an observed resolution description.

Editing source, spec, inventory, an asset, capture plan or dependency lock invalidates the run for current review/preview notes export. Editing exported film bytes also invalidates it. Do not bypass staleness by copying old flags or altering stored fingerprints.

## Focus UI with a deterministic camera

Copy camera-ui.mjs beside motion-dom.mjs. Use `cameraAt(frame, keys, capture.viewport, box)` with ordered integer frame/region keys. Regions are `[x,y,width,height]` in capture CSS coordinates, independent of DPR. `box` is `{x,y,width,height}` in stage coordinates. The helper fits the region uniformly into the box and computes the image position/size; clip the full screenshot in that box. `applyCamera(image, pose, box)` resets image geometry. `targetPoint(captureTarget.css, pose)` maps a cursor/click center through exactly the same transform.

Shot `camera` fields in the demo hold frame/region keys within `[shot.start,shot.end)`. Validate capture bounds before render. Use separate camera layouts when aspect ratios demand different proof. The sample focuses save/theme controls and includes a click ripple; copied captures remain the real UI, never re-created fake controls. Review context and label readability after zooming.

## Readability diagnostics

Tag essential DOM text with `data-read="id"` and significant UI regions with `data-region="id"`. Declare projected control height with `data-ui-control="name" data-ui-control-px="52"` after camera scale. The DOM runner samples text ranges, effective parent visibility, declared control size, text/region overlap and estimated copy reading holds into frames/readability-check.json.

Optional spec.readability contains positive finite phone_width (default360), min_text_px (12), min_ui_control_px (18) and words_per_second (3). These are adjustable heuristics, not universal standards. The report warns rather than silently approving or failing a creative choice. Required safe-area overflow still fails through the existing layout check. Sample selection includes cuts, stable shot frames, camera-settle frames and named events; untagged text/controls and between-sample overlap are not covered.

The tool does not OCR screenshots, measure contrast, check shaping/ink or establish semantic readability. Full captured UI labels still require actual phone-size review. Estimated holds use shot copy after declared transitions; secondary animated copy requires manual review. Read warnings before G4/G6, fix high-impact problems or document the observed justification. Keep warnings separate from technical encode success.
