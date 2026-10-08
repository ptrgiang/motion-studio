# DOM product films — v1.3

## Engine and assets

Use `--engine dom` for a whole HTML stage; `canvas` still captures its Canvas starter and `pillow` still uses a Python frame function. These engines have explicit separate contracts. DOM does not silently replace either engine. Copy `assets/render-dom.mjs`, `browser-runtime.mjs` and `motion-dom.mjs` into the project's `src/`. The pipeline uses `src/promo.html`: keep that entrypoint or link it to your own scene. Define `#stage` with exactly the current spec format dimensions, asynchronous `window.motionReady`, and `window.renderFrame(frame,spec,format_id)`. Set every property and inactive scene on every seek. Do not use timers, autoplay media, CSS transitions or `will-change:transform` to drive production state.

The DOM runner serves only project-local files, blocks external render requests, preloads declared fonts/images, captures lossless stage PNGs and records runtime. It compares representative reverse seeks and sequential/direct traversal using SHA256 screenshot bytes. This is a same-runtime diagnostic; font rasterization differences across OS/GPU/browser versions are not equal-pixel failures. Fix state dependencies before considering any documented pixel tolerance; do not turn off checks merely to pass a scene.

Tag essential elements with `data-qc="id"`. At selected frames the runner records their bounds and fails if they exceed format safe insets. This checks tagged geometry, not overlaps, contrast, visible glyph ink, reading speed, audio or artistic quality. It does not inspect untagged objects. Review actual films and phone-scale evidence separately.

## Capture real local product UI

Use `scripts/capture.py PROJECT --plan capture-plan.json --run-id ui --rights user-provided --provenance "Authorized local product demo" --approved`. Pass approval only for assets whose rights you have confirmed; the tool does not establish rights from a label. It opens fresh headless contexts and never uses an existing browser profile, credentials or user session. It captures a local app entrypoint under the project; remote/authenticated app capture requires a separately authorized asset workflow. Use a local production snapshot or the supplied screenshots when appropriate.

Capture plan:

```json
{"source":"src/product.html","viewport":{"width":1000,"height":700},"dpr":2,"ready":"#app","fonts":["400 32px MotionFont"],"states":[{"id":"saved","actions":[{"type":"fill","selector":"#note","value":"A demo thought"},{"type":"click","selector":"#save"}],"ready":"#notes li","targets":{"save":"#save"}}]}
```

Supported actions are fill/click/select; selectors must resolve to the intended element. Each state starts fresh. Prefer application readiness selectors over fixed sleeps. The output `assets/ui/capture.json` includes viewport/DPR, screenshot/source/plan hashes and targets in CSS pixels and screenshot pixels. Screen-space cursor placement is `card_origin + css_coordinate * displayed_width / viewport_width`. DPR improves capture resolution; do not multiply CSS coordinates twice. Wait for fonts before measuring. Missing/offscreen targets, network errors and nonempty output destinations fail.

The Python wrapper registers every screenshot and metadata asset with provenance. Add those asset IDs to shots that use them. Validation detects edited source, plan or screenshot bytes and requires recapture. The pipeline also preserves source/asset hashes; changes invalidate prior review evidence.

## Package fonts

Install the repository requirements (Pillow and fontTools), then run:

`python scripts/pack_font.py PROJECT /path/font.ttf --license-file /path/LICENSE.txt --family MotionFont --text "All required copy, including Tiếng Việt" --approved`

This copies the font and license into project assets, registers provenance, verifies cmap coverage and records font SHA256/preload CSS in `spec.fonts`. Rights are an explicit caller assertion; the tool does not interpret license permissions. For DOM add matching `@font-face` declarations and preload all faces, including ones only used in later shots. Validation checks packaged bytes and shot-copy glyphs. A font with a missing glyph is a blocker, not a reason to accept tofu/fallback. A license file must describe the supplied font.

## Events and motion primitives

Keep integer-frame `spec.events` as `{event_id: frame}`. A linked audio cue adds `event_id`; its `visual_event_frame` must equal the event and `start_frame` must equal event plus `intentional_offset_frames`. Legacy cues without event IDs remain supported. Changing an event requires updating linked cues; validation rejects stale links. Do not add another cue file.

`motion-dom.mjs` exports progress/easeOut/easeInOut, scalar/vector keyframes, half-open `shotAt`, `eventFrame`, `beatClock`, complete-state `put`, grapheme-aware kinetic/revealLetters. Compile paths outside renderFrame for complex films. Beat clock uses `spec.rhythm={bpm,offset_frame}` and returns fractional-frame beat positions; quantize deliberately for integer audio placement. It is constant-tempo arithmetic, not song analysis. Never infer a supplied song's BPM from this clock.

## Run the original 15-second demo

```sh
python skills/motion-studio/scripts/promo.py my-promo --font /path/DejaVuSans.ttf --license-file /path/font-license.txt
cd my-promo
npm install --ignore-scripts
npx playwright install chromium
cd ..
python skills/motion-studio/scripts/capture.py my-promo --run-id ui --rights original --provenance "Original working Motion Notes local app" --approved
python skills/motion-studio/scripts/pipeline.py run my-promo --engine dom --run-id first
```

The fixture requires a TTF with English/Vietnamese glyph coverage. It creates a functional original browser-local note app and captures draft/saved/dark states. The film shows those actual functions: hook, save, view change, local persistence, three-second end hold. It is a renderer demonstration, not a real client launch or a claim that Motion Studio ships a notes product. Generated captures/font/audio stay in the project; no upstream Pitchcraft artwork is reused. Both formats use explicit layouts. The sample's small full-app text requires perceptual review; bounds checks cannot approve readability.

SFX are original and event-seeded; see motion-audio's sound workflow. Capture and DOM render require the project's pinned Playwright/Chromium. No browser binaries are bundled; doctor checks availability without downloads. Windows uses the same Python/Node commands; no Bash dependency is added. Playback, listening and final aesthetic scores remain pending until observed.
