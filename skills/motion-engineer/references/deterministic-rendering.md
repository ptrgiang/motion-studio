# Deterministic rendering

## Engine decisions
Pillow: explicit render_frame(frame,spec,format_id,project) returning an RGB image; suitable for procedural 2D typography/shapes, not a substitute for real UI capture or arbitrary organic footage. Inspect resolved fonts and record their hashes.
Canvas: direct 2D graphics, lightweight explicit frame function; build asset preloading, capture and audio yourself.
SVG: precise scalable shapes/text, but test filters, fonts and capture cost.
Remotion: React compositions at frame numbers; use useCurrentFrame/useVideoConfig and consistent installed package versions. Sequence-local frame is relative to its start, so use global time intentionally. Check licensing for intended production use without assuming every deployment is free.
Other HTML engines: inspect official seek/capture API first; avoid inventing HyperFrames CLI syntax from its name in the article.
Photoreal footage/characters: use authorized real footage or a separately specified video-generation/3D workflow. This skill does not make arbitrary organic performance realistic just because it can animate vectors.

## Remotion verified baseline
Read https://www.remotion.dev/docs/the-fundamentals and docs for the installed version.
`npx remotion still src/index.ts CompositionId out/frame-0240.png --frame=240`
`npx remotion render src/index.ts CompositionId out/film.mp4`
Confirm command flags and composition registration in the project's version. Use explicit separate composition ids or props for each aspect ratio. Save the exact successful command. Pin all Remotion package versions consistently and preserve the lockfile.

## Capture readiness
Browser: await document.fonts.ready, decode images and await any renderer media-ready contract. Avoid live URLs at final render when local assets are possible. Seek video to the requested timestamp and await the decoded frame. A loaded DOM is not proof that fonts/video textures are ready. Canvas getImageData hash can compare decoded pixels; identical PNG container bytes are not required.

## Timeline rules
Scenes are half-open frame ranges. Define frame-zero artwork explicitly; never rely on a prior setup animation. Audio starts at integer cue frames. Trim/extend visuals and audio intentionally rather than allowing an encoder's -shortest to hide a duration mismatch. Record output color profile assumptions and inspect actual color after encoding.
