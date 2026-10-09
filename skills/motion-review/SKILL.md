---
name: motion-review
description: "Review motion-video stills, transition strips, rough cuts and final exports with timestamped evidence. Use for contact sheets, phone-size readability, audio sync, technical QC, bounded repairs and final delivery verification."
---

# Motion Review

Read [review-rubric.md](references/review-rubric.md). Judge the observed output against the brief. Do not describe intention as evidence.

1. Verify source spec/version and the evidence matches the latest render. Select first frame, opening at <=2s, each beat midpoint/boundary, proof, end, and consecutive frames across fastest transitions. Generate a labeled contact sheet for every requested format.
2. Inspect actual images at full size and phone width. Review alignment, type consistency, readability, safe area, real product assets, collisions, continuity, last poster state and visual hierarchy. Look at enough representative images to assess the whole film; do not infer scenes you have not seen.
3. Watch the rough/final clip to judge timing, weight and temporal artifacts; listen with and without picture for shape and sync. If tools cannot play/hear it, identify exactly which checks remain pending; do not fabricate a score for them.
4. Write `reviews/review-N.md`: evidence file/frame/timestamp, observed defect, severity, viewer impact, smallest fix, owner role and retest frames. Choose the three highest-impact defects, fix locally and compare the affected evidence plus adjacent continuity. Repair blocker defects before scoring style.
5. Rate observed dimensions using the rubric. Aesthetic thresholds are studio policy, not objective proof of professional quality. Run technical validation/probe, but keep it distinct from visual and perceptual review.
6. Repeat at most three ordinary aesthetic cycles unless the user requests more. If critical defects remain or inspection is missing, deliver a draft with clear limitations; do not mark G6 passed. Never hide a broken claim by scoring it against easier categories.
7. Read pipeline outputs: per-format `qc.json`, transition clips, phone poster and contact sheet, plus run `manifest.json` and `review.json`. Record which encoded film hash was actually reviewed; invalidate notes when it changes. `technical_pass_review_pending` is never creative approval. Produce `qc.json` and `delivery.md` with completed/pending checks, exact exports, source commands, versions, asset provenance and unresolved human judgments. Final implies all required checks passed, not merely an MP4 path.

Use bundled `motion-studio` tools if available; otherwise use an equivalent verified local extraction workflow. Do not replace the client's artwork with a generated approximation to make the review easier.

For evidence-bound review calibration, read [benchmark.md](references/benchmark.md) and use `scripts/benchmark.py`. Keep private controls hidden during review; leave unobserved dimensions pending.

## v1.4 review workflow

Read motion-studio’s references/review-studio.md for the local preview, camera geometry, readability diagnostics and review.py commands. Resolve motion-studio by frontmatter name. Inspect actual exported motion/audio; source or asset changes require a new run and fresh review. Treat machine readability findings as heuristics.

## Showreel revisions

For a studio intro, brand reel or slideshow critique, resolve motion-studio by frontmatter name and read references/showreel-craft.md. Follow the motif/action/camera/reading plan and use executable craft tools when appropriate. Review encoded results; ambient wobble is not narrative motion and a machine pass is not creative approval.
