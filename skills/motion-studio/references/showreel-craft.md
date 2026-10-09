# Showreel craft (v1.5)

Read [repo-research-v15.md](repo-research-v15.md) for evidence and boundaries. Use this route for a studio introduction, brand reel or a revision criticized as a slideshow.

## Direction before animation

Write three different concepts. Pick one whose motion expresses the subject. Describe its signature transformation in one sentence, not a list of effects. A recurring motif changes role and resolves in the lockup. Contrast one/many, flat/deep, quiet/impact, light/dark; reserve a material or color for the payoff. Default 15–20 seconds at 60 fps for this route; user instructions override.

Create motion-plan.json with motif, signature, chapters, seams, rests and cuts_seconds. Each chapter records frame range, primary action, secondary reaction, camera intent, legible copy window and audio event. Each seam records carrier, exit/entry geometry and velocity direction, and why it is a morph or deliberate cut. Rest ranges use start_seconds/end_seconds and a narrative reason. Keep canonical event frames in spec.json; derive human seconds. Choose two or three transition families; vary execution.

A shot performs after its entrance: assemble, fold, compress, propagate, route, transform, reveal a state, or travel to new information. Ambient noise and wobble do not satisfy this. Permit deliberate reading and pre-payoff pauses. Camera movement cannot rescue meaningless staging. Settle essential copy and budget legible holds; a fast texture word is not essential copy.

## Executable browser toolkit

`python <studio>/scripts/craft.py <fresh-project>` prepares an original six-second engine study. Install pinned Playwright and Chromium; run pipeline.py run with --engine canvas. Study art is not the finished film. Replace src/canvas-starter.html for the brief.

Copy assets/motion-craft.mjs, render-craft.mjs and browser-runtime.mjs into src. Set spec.render = {adapter:"craft", samples:3, shutter:0.5, cuts:[integer cut frames]}. Fractional renderFrame inputs are actual shutter times: never round them or blend neighboring exported PNGs. Use 1 for unblurred styleframes, 3–8 for fast moves after inspection. Averaging is sRGB, not physically exact linear light. Exposure never crosses a declared hard cut. The adapter captures one opaque Canvas, not DOM overlays. Other engines keep their adapters.

motion-craft.mjs exports:
- springTrack(t, initial, [[seconds,target],...], frequency, damping): analytic sum of spring steps; continuous through retargeting. Ordered keys, scalar targets.
- pose(t, keys): smooth finite segments; logarithmic positive zoom. Velocity rests at each key by design. For continuous fly-throughs use longer segments or a Hermite path; this is not a continuous-velocity spline.
- rotate/project: right/down/away coordinates; near-plane reject. Sort opaque geometry back-to-front and handle null projections.
- contour/morph: matched angular topology for circle/superellipse; arbitrary SVG morphing is outside the contract.
- textureQuad: two affine triangles approximate a projected plane. Subdivide large planes to reduce perspective distortion. Supply unscaled canvas coordinates.
- random(id,seed), phase, smooth, mix, path, shutterFrames.

Reset all Canvas state on every frame, including textBaseline, textAlign, clip, transform, shadows and compositing. ctx.clearRect alone does not reset state; use ctx.reset() on a verified browser, a canvas dimension reset, or assign every state explicitly. Keep failures in seek-diagnostic.json and fix the composition rather than relaxing hash checks.

Check capabilities before choosing direction. If unavailable, solve the runtime or state a viable direction before producing art; do not silently replace a dimensional film with flat title cards.

## Review encoded bytes

Run scripts/motion_audit.py <encoded.mp4> --plan <motion-plan.json> --out <audit.json>. Inspect static windows and luminance spikes, especially after entrances. Pauses can be intentional; noise can fool the detector. This is not a creative certificate.

Extract opening, chapter peaks, consecutive handoff strips, payoff and 360px versions. Record defects with frame/time, repair the worst three, rerender and compare. Watch normal-speed output and listen when supported; otherwise leave those checks pending. Never declare "wow" from a hash.
