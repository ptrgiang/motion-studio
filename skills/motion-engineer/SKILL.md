---
name: motion-engineer
description: "Implement or repair seekable code-rendered video using Canvas, SVG, Remotion or a verified HTML renderer. Use for deterministic frame rendering, source templates, asset loading, render commands and video encoding."
---

# Motion Engineer

Read [deterministic-rendering.md](references/deterministic-rendering.md). Make the composition a pure query of frame, spec, resolved assets and seed. Choose an engine based on the film, not the model name.

1. Inspect tool availability, existing project and dependency lockfile. Read primary docs for installed APIs. Preserve an existing working stack. Choose Pillow for original procedural 2D graphics, Canvas/SVG for browser graphic films, Remotion for React/UI/media structure, or a verified seekable HTML engine. Do not install a large framework for a simple film without reason.
2. Define renderFrame(frame) or the engine equivalent. Derive time from frame/fps only. Eliminate wall clocks, requestAnimationFrame accumulation, hidden CSS animation state, unseeded random and previous-frame dependencies. For simulation, bake deterministic state or derive it analytically.
3. Preload fonts/images/media and await readiness before capture. Save assets locally and validate their ids/paths/provenance. Fix viewport, pixel ratio, color assumptions and dependency versions. Use seeded variation keyed by object id/frame as appropriate; avoid frame-random values causing unintended flicker.
4. Keep style/layout, motion parameters, copy, asset ids and cues in editable files. Implement explicit wide/vertical/square layouts. Use the canonical spec frame ranges and composition ids.
5. Render selected frames in shuffled order, including first/last and transition boundaries. Compare decoded pixel results for repeated identical frame inputs in the same controlled runtime. Compare a direct seek with sequential state at the same frame. Visual consistency across different OS/GPU/font environments needs separate checks.
6. Create reproducible still, rough and final render commands. Encode exact frame count at canonical fps; avoid filename ordering bugs. Mux actual audio only when supplied/generated under the audio plan. Verify dimensions, codec, pixel format, fps, duration and frame count with ffprobe.
7. Provide full editable source, manifest/lockfile, captured versions and instructions. Distinguish a technical render pass from visual/audio approval; hand evidence to `motion-review`.

Use motion-studio’s doctor.py and pipeline.py for executable Pillow/Canvas production, frame-based audio and technical QC. Keep perceptual review pending until observed.

For the bundled Canvas starter, locate `motion-studio` by frontmatter name and read its renderer recipe. Copy starter and renderer to the project, resolve Playwright in the project, and render the generic test. Do not silently use its sample artwork as the client's film.

For executable whole-page HTML motion, read motion-studio’s `references/dom-production.md`. Use its DOM adapter, local capture tool and font packer; keep Canvas and DOM renderer contracts explicit. Tag essential layout bounds, verify out-of-order seeks and inspect normal-speed output.

## v1.4 review workflow

Read motion-studio’s references/review-studio.md for the local preview, camera geometry, readability diagnostics and review.py commands. Resolve motion-studio by frontmatter name. Inspect actual exported motion/audio; source or asset changes require a new run and fresh review. Treat machine readability findings as heuristics.

## Showreel revisions

For a studio intro, brand reel or slideshow critique, resolve motion-studio by frontmatter name and read references/showreel-craft.md. Follow the motif/action/camera/reading plan and use executable craft tools when appropriate. Review encoded results; ambient wobble is not narrative motion and a machine pass is not creative approval.
