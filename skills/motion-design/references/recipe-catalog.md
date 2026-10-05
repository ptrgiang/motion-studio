# Runnable motion recipes — v1.2

Use `python motion-design/scripts/recipes.py RECIPE PROJECT`, then `python motion-studio/scripts/pipeline.py run PROJECT --engine pillow --run-id first`. Run from your installed pack; personal folder names may differ. The script resolves siblings by frontmatter. Use `--source-root PATH` for another complete pack. All six are four-second, 30fps, silent procedural studies with wide and vertical layouts. Copy and edit the project source; it no longer depends on installed skill files. Canvas remains a separate renderer example, not a recipe engine.

| Recipe | Design reason | Main phase at 30fps | Tune in src/motion_library.py | Avoid |
| --- | --- | --- | --- | --- |
| kinetic-typography | Stagger reading order, hold the full idea | Words start 0/9/18; settle 24/33/42; hold to119 | Entry displacement, stagger, optical size | An unreadable cascade or safe-area clipping |
| mask-reveal | One edge guides discovery | Reveal8–48; hold49–119 | Edge speed, headline width, mask | A wipe with no focal relationship |
| match-cut | Retain identity while changing context | Hard cut at60; circle position and radius retained | Context change, matched anchor | Teleporting the anchor across the cut |
| camera-move | Reframe attention toward the right node | Travel12–66; rest67–119 | Zoom, world offset, easing | Overshoot that loses the subject |
| ui-interaction | Connect action to feedback | Pointer8–28; press28–34; response34–52 | Press amplitude, response duration | Delayed feedback or treating schematic UI as product proof |
| state-transition | Preserve identity through a property change | Morph18–66; rest67–119 | Position, radius, easing | Changing identity at the settle boundary |

Read the movement at normal speed and phone size. These are small controlled examples, not a complete client-film style system. Replace procedural copy and objects with brief-grounded designs. Measure text, use approved fonts, check glyph coverage and add audio only when the brief calls for it.

The library exposes clamped `progress`, cubic `ease`, analytical `spring` and pure `render(frame, spec, format_id, recipe, variant)`. Durations scale to the canonical frame count; no accumulated simulation state is permitted. `spring` has intentional overshoot and explicit endpoints; it is not a physical solver. `MOTION_FONT_PATH` selects a locally installed font. Pin it for repeatable output; cross-platform pixel equivalence is not promised.

`--variant flawed` creates a deliberately defective control for review calibration. Keep variants and diagnosis private during a blind review. A clean control is intended to satisfy its stated micro-brief; do not infer a professional aesthetic score from that label. The benchmark is a separate review workflow in motion-review.
