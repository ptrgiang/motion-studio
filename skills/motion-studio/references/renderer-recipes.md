# Minimal Canvas recipe

## Prepare
Create a project with studio.py init; replace the draft spec with real shot/layout decisions. For the generic smoke test use the sample spec below. Copy canvas-starter.html and render.mjs from this skill's assets into src/. Install Playwright in the project using the package manager and pin the resolved version; install its Chromium browser. Python contact sheets require Pillow. FFmpeg and ffprobe must be on PATH. Capture dependencies/versions; do not present installation or browser download as already done.

## Commands from project root
`node src/render.mjs --spec spec.json --html src/canvas-starter.html --format wide --out reviews/wide-stills-v1 --frames 0,15,30,59`
`node src/render.mjs --spec spec.json --html src/canvas-starter.html --format wide --out out/wide-frames-v1`
`ffmpeg -framerate 30 -start_number 0 -i out/wide-frames-v1/frame-%06d.png -frames:v 60 -c:v libx264 -pix_fmt yuv420p -movflags +faststart out/wide-test.mp4`
`python3 <skill-dir>/scripts/studio.py samples . > reviews/samples.json`
`python3 <skill-dir>/scripts/contact_sheet.py --video out/wide-test.mp4 --samples reviews/samples.json --output reviews/wide-contact.png`
`ffprobe -v error -count_frames -show_streams -show_format -of json out/wide-test.mp4`
`ffmpeg -v error -i out/wide-test.mp4 -f null -`
The example is exactly 60 frames at 30fps. Replace both values for a real spec; do not copy a wrong count into production. No audio is included in this test. Encode vertical from its own rendered frames, not from a crop.

## Sample spec
Use version 1, fps=30, duration_frames=60, seed=42; formats wide 960x540 safe {top:36,right:48,bottom:36,left:48} and vertical 540x960 safe {top:64,right:40,bottom:80,left:40}; one shot TEST from 0 to 60, purpose "verify renderer", entry_state "graphic starts", exit_state "graphic settled", copy "FRAME, NOT CLOCK", asset_ids [], layouts {wide:"shape left, text right",vertical:"shape above, text below"}, transitions [{start:0,end:24}], audio_cues []. Set assets.json to {assets:[]}. This procedural artwork is original generic test material.

## Adaptation contract
Replace sample renderFrame artwork with approved scene layouts and local assets; await their preload promises. Implement frameHash or an equivalent decoded-pixel checksum for automated seeks. Keep preview wall-clock controls outside the frame query. Use a fresh output directory for every render version. The starter has no UI asset pipeline, voice/music mixer or advanced motion engine; these must be implemented as the actual film requires.
