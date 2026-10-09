# Motion Studio

Version **1.4.0** — real UI capture, whole-DOM rendering, shared events, procedural SFX and a 15-second app promo.

Seven agent skills for directing, designing, engineering, and reviewing code-rendered motion films. Built for Claude Code with Opus 5.5, with portable `SKILL.md` instructions that other compatible coding agents can also use.

Start from a clear brief and real assets. Develop the story and motion language, render deterministic frames, inspect the actual output, and repair specific defects before delivery.

## Skills

| Skill | Responsibility |
| --- | --- |
| [motion-studio](skills/motion-studio/SKILL.md) | Coordinate production, checkpoints, review gates, and delivery |
| [motion-director](skills/motion-director/SKILL.md) | Brief, concepts, reference analysis, and asset provenance |
| [motion-storyboard](skills/motion-storyboard/SKILL.md) | Narrative beats, states, styleframes, and format-specific layouts |
| [motion-design](skills/motion-design/SKILL.md) | Typography, hierarchy, easing, weight, and continuity |
| [motion-engineer](skills/motion-engineer/SKILL.md) | Seekable frame rendering, source code, and reproducible exports |
| [motion-audio](skills/motion-audio/SKILL.md) | Music, voice, effects, mix, and picture synchronization |
| [motion-review](skills/motion-review/SKILL.md) | Timestamped critique, contact sheets, local repairs, and final QC |

These are workflow roles. Installing the skills does not automatically launch seven agents or change the selected model.

## Install in Claude Code

Clone this repository, then run from its root:

```sh
git clone https://github.com/ptrgiang/motion-studio.git
cd motion-studio
python3 skills/motion-studio/scripts/export_claude.py --destination /absolute/path/to/your-video-project/.claude/skills
```

On Windows, use `python` if that is your Python command and quote paths containing spaces. For a personal installation, pass the full path to your user `.claude/skills` directory instead. The exporter refuses blind overwrites. For installations created by v1.1 or later, inspect and apply a backed-up update:

```sh
python3 skills/motion-studio/scripts/export_claude.py --destination /path/to/project/.claude/skills --update --dry-run
python3 skills/motion-studio/scripts/export_claude.py --destination /path/to/project/.claude/skills --update
```

Updates stop when installed files differ from their recorded baseline. A v1.0 installation has no baseline: preserve it and migrate into a fresh destination instead of overwriting unknown local edits.

Alternatively, copy each complete folder under `skills/` into `.claude/skills/<skill-name>/`. Preserve its references, scripts, and assets. Do not add an extra container directory around the seven skills.

Select Opus 5.5 in your Claude Code session. Invoke:

```text
/motion-studio Create a 15-second English launch film for [product].
Audience: [audience]. Takeaway: [one sentence].
Formats: 16:9 and 9:16.
Use the real product assets in ./assets and inspect ./reference.mp4.
Work autonomously through documented review gates.
Deliver editable source, videos, poster frames, contact sheets,
asset provenance, and a note identifying any incomplete checks.
```

The main skill loads the specialist instructions as needed. Autonomous gates are internal checks; the agent asks for input when a material requirement is unresolved or when you requested a supervised approval.

## Production workflow

1. Establish the idea, product facts, reference, and approved assets.
2. Write the style guide and frame-based shot list; design each aspect ratio explicitly.
3. Build a deterministic composition and inspect representative stills.
4. Render a rough cut; inspect transition frames, watch the movement, and listen to audio.
5. Repair the three highest-impact observed defects and recheck affected sections.
6. Verify the requested formats and deliver the source alongside the exports.

Never invent product screens or metrics. Treat missing required assets as production blockers while continuing feasible planning. A contact sheet cannot establish temporal quality or audio quality, and a successful encode cannot establish artistic quality.

## Included tools

Under `skills/motion-studio/`:

- `scripts/pipeline.py`: one-command per-format rendering, audio, encoding, technical QC, posters, phone-size evidence, and transition clips.
- `scripts/audio.py`: frame-aligned mix, trims, fades, voice/music ducking, two-pass normalization, and output measurement.
- `scripts/doctor.py`: dependency/browser availability checks without installing anything.
- `scripts/studio.py`: initialize project records, validate the asset/timeline/layout structure, and select review frames.
- `scripts/contact_sheet.py`: generate labeled contact sheets from stills or exact decoded video frames.
- `scripts/export_claude.py`: export all seven skills into Claude Code's directory structure without overwriting existing skills.
- `assets/pillow_composition.py`: original procedural 2D frame-function example.
- `assets/canvas-starter.html`: generic deterministic Canvas frame-function example.
- `assets/render.mjs`: Playwright capture script with within-runtime seek checks.

Example project initialization:

```sh
python3 skills/motion-studio/scripts/studio.py init /absolute/path/to/new-film
```

Read [the production contract](skills/motion-studio/references/production-contract.md) before filling the draft spec, and [the renderer recipe](skills/motion-studio/references/renderer-recipes.md) before running the starter. The generic sample artwork is a renderer test, not a finished client film.

## Requirements

Reading and planning require a compatible agent. Rendering additionally requires local execution tools:

| Component | Requirement |
| --- | --- |
| Project scripts | Python 3.10+ |
| Contact sheets | Pillow |
| Video extraction and encoding | FFmpeg and ffprobe on PATH |
| Canvas capture | Recent Node.js, project-installed Playwright, and its Chromium browser |
| Optional React video stack | Remotion, with matching pinned package versions |

Dependencies and browser binaries are not bundled. Pin the actual installed versions and preserve the production project's lockfile. The skills do not include model API credentials or force a paid API workflow.

## Run the sample

Install Python dependencies and make FFmpeg/ffprobe available. From the repository root:

```sh
python3 -m pip install -r requirements.txt
python3 skills/motion-studio/scripts/doctor.py --engine pillow
python3 skills/motion-studio/scripts/pipeline.py demo ./my-demo
python3 skills/motion-studio/scripts/pipeline.py run ./my-demo --engine pillow --run-id v1
```

This produces separate 16:9 and 9:16 six-second original motion studies with audio, posters, contact sheets, transition clips and QC under `my-demo/out/v1/`. Source samples are editable. They are toolchain examples, not product films or a visual benchmark.

For Canvas, install the demo's pinned Node dependency and Chromium from inside `my-demo` (`npm install`, then `npx playwright install chromium`), and run the pipeline with `--engine canvas`. Use `MOTION_CHROMIUM_PATH` for an existing compatible browser. The runner never substitutes another engine after a Canvas failure.

Canonical audio lives in `spec.json.audio_cues`. Explicit `audio_mode` chooses `designed` or `silent`; a separate `audio-cues.json` is rejected. All used audio files need approved provenance records.

Read [the pipeline contract](skills/motion-studio/references/pipeline.md) for inputs, outputs, engine contracts and review boundaries.

## Checks and validation scope

Run regression checks:

```sh
python3 -m unittest discover -s tests -v
```

Set `MOTION_INTEGRATION=1` to include the full Pillow/FFmpeg pipeline tests. GitHub Actions checks Linux and Windows regressions and runs the real Chromium pipeline with audio for both formats. Generated Canvas evidence is retained as a workflow artifact; check the actual workflow result rather than assuming a configured job passed.

Local verification has exercised the complete Pillow pipeline with original audio in both formats, measured output loudness, checked exact duration/count/fps/dimensions and full decode, and inspected representative stills. Chromium remains unavailable in the local authoring environment, but its real two-format rendering/audio pipeline has now passed in [GitHub Actions](https://github.com/ptrgiang/motion-studio/actions/runs/37299324016). Windows and Ubuntu regression jobs also passed. The retained Canvas artifact was checked for frame counts, seek results, encoded QC and sampled poster layouts. See [exact validation status](skills/motion-studio/references/validation-status.md).

A successful run reports **technical_pass_review_pending**, not a finished film. Video playback, required audio listening, typography/readability and artistic judgment must be observed and recorded against the actual output hashes. Technical metadata, a waveform or a contact sheet cannot certify those checks.

## Source and adaptation

Inspired by the supplied article *Motion Engineering: Build a Video Studio Around Opus 5.5*, attributed to `@0xwhrrari`, and its studio diagram. This repository contains an authored workflow adaptation rather than a reproduction of the article. Added policies include explicit role responsibilities, a frame-based production contract, asset checks, bounded repairs, and evidence requirements.

See [source mapping and primary documentation](skills/motion-studio/references/sources.md).

## v1.2: runnable techniques and blind calibration

Six four-second silent Pillow studies: kinetic typography, mask reveal, match cut, camera move, schematic UI interaction, and state transition. Each has an editable frame function, wide/vertical layouts, an intentional variant and an injected-defect variant. Read [the design reasons and tuning guide](skills/motion-design/references/recipe-catalog.md).

```sh
python3 skills/motion-design/scripts/recipes.py match-cut ./match-study
python3 skills/motion-studio/scripts/pipeline.py run ./match-study --engine pillow --run-id first
python3 skills/motion-review/scripts/benchmark.py prepare ./calibration
# Add --render to prepare to encode all 24 films as well as stills.
python3 skills/motion-review/scripts/benchmark.py assess ./calibration/public
```

Give only `calibration/public` to a reviewer; retain the private answer key separately. The 12 cases have media hashes, integer-frame evidence and a five-dimension rubric. Scores remain null until observed. Timing and continuity require video evidence in both formats; still-only preparation leaves them pending. A validator checks attribution and evidence integrity, not the truth of a reviewer’s opinion. No aggregate is emitted until all cases have complete valid reviews. Read [the benchmark protocol](skills/motion-review/references/benchmark.md).

These procedural controls teach critique; they are not independently rated professional gold standards. The recipe library uses Pillow; Canvas remains the separately tested starter. New regression checks cover every recipe in both formats, reverse seeking, defective controls, blind manifests, stale evidence and review gating.


v1.2 release verification: all four [CI jobs passed](https://github.com/ptrgiang/motion-studio/actions/runs/37303373349), including the 24-film calibration render and Windows regression with exact audio sample-count protection. Locally, all 32 tests passed with integration enabled. Perceptual reviews remain pending; see the validation status for the tested commit and limitations.


## v1.3: product capture and DOM production

Capture authorized local product states with screenshots, CSS/pixel rectangles, viewport/DPR and source/plan/image hashes. Render the entire HTML stage with the explicit `dom` engine and reusable frame-based motion helpers. Package approved fonts and licenses, validate glyph coverage and link generated original SFX to named events in the sole `spec.json` timeline.

The new `Motion Notes` fixture is a functional original local note app: save/persist a note, toggle its view, and render a 15-second promo with a three-second end card in 16:9 and 9:16. It demonstrates an actual sample app, not fabricated client UI. [Runnable setup and contracts](skills/motion-studio/references/dom-production.md).

```sh
python3 skills/motion-studio/scripts/promo.py ./my-promo --font /path/DejaVuSans.ttf --license-file /path/font-license.txt
# In my-promo: npm install --ignore-scripts; npx playwright install chromium
python3 skills/motion-studio/scripts/capture.py ./my-promo --run-id ui --rights original --provenance "Original local Motion Notes app" --approved
python3 skills/motion-studio/scripts/pipeline.py run ./my-promo --engine dom --run-id first
```

Additional commands: `pack_font.py` packages caller-approved font/license assets; `sfx.py` generates click/tick/blip/whoosh/riser/impact/pad cues with independent stable seeds. The existing measured mixer, exact encode/decode checks and pending perceptual reviews remain in use. Capture uses fresh headless contexts and local project entrypoints; it does not access existing browser sessions or authenticated accounts. DOM render blocks external asset requests and checks tagged safe-area bounds. Bounds, cmap and hash checks cannot certify final readability or artistic quality.

The implementation was independently authored after reviewing [promo-video-generator](https://github.com/visser23/promo-video-generator) at `70031de47d0cb11dcd95fffa050672f953bcbb04`. No upstream code or Pitchcraft assets are included. Motion blur and parallel worker/resume optimization remain future work.

v1.3 verification: 40 local tests passed. The [verified CI run](https://github.com/ptrgiang/motion-studio/actions/runs/37775799052) passed real local capture and both 15-second DOM exports, browser integration, existing Canvas/audio, Windows regression and 24-film calibration. Check the run for the remaining Ubuntu job status. Downloaded DOM evidence confirms 450 frames per format, seek/layout/decode checks and encoded audio measurement. Full playback/listening remains pending; [exact validation scope](skills/motion-studio/references/validation-status.md).

## v1.4: preview, UI camera and version-bound review

A local review studio provides frame stepping, timeline seek, format switching, a safe-area overlay, synchronized lossless live audio and an encoded-film view. Export timestamped notes with explicit per-format inspection flags; import them with the review tool. Updated inputs or video bytes invalidate prior review. Each fresh render starts pending.

```sh
python skills/motion-studio/scripts/preview.py ./my-promo --run-id first
python skills/motion-studio/scripts/review.py import ./my-promo --run-id first --notes /path/motion-review-notes.json
python skills/motion-studio/scripts/review.py assess ./my-promo --run-id first
# After fixing and rendering another run:
python skills/motion-studio/scripts/review.py compare ./my-promo --run-id second --before first
```

The DOM demo now focuses real capture regions with camera keyframes and maps cursor/click ripple through the same CSS geometry. Tagged text/control sizes, overlaps and estimated reading holds appear in readability-check.json. These are warnings for inspection, not automatic creative approval. [Workflow, limits and camera contract](skills/motion-studio/references/review-studio.md).

v1.3 historical CI: the Ubuntu regression job eventually timed out during package installation; its four other jobs passed. v1.4 checks existing tools first and bounds package-manager waits, then reruns regression and browser checks.

v1.4 verification: all five [CI jobs passed](https://github.com/ptrgiang/motion-studio/actions/runs/37872009746), including real preview controls, encoded playback, camera/click mapping, readability fixtures and both 450-frame DOM exports. The regression suite has 49 tests, plus Ubuntu full integration. Downloaded evidence and [exact validation scope](skills/motion-studio/references/validation-status.md) distinguish technical success from remaining perceptual review.
