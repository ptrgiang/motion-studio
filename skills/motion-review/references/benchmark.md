# Blind motion calibration — v1.2

Run `python motion-review/scripts/benchmark.py prepare WORKSPACE` for 12 anonymized cases, each with 18 stills across wide and vertical. Add `--render` for 24 four-second silent videos through the real Pillow pipeline. Render requires FFmpeg/ffprobe and Pillow; still preparation requires Pillow. The script resolves motion-design and motion-studio siblings; `--source-root PATH` selects a complete pack. A used destination is refused to preserve evidence.

Send only `WORKSPACE/public` to the reviewer. Keep private projects, variant names, source code, recipe catalog diagnoses and `private/answer-key.json` unavailable during review. Read each brief and manifest. Inspect both aspect ratios, phone-scale type and the cut frames; watch both full videos before judging timing or continuity. Stills-only review leaves those dimensions null. Audio is intentionally absent and unscored.

Fill each case's review.json with reviewer attribution, actual observed flags, scores and observations. Each observation requires:

```
{"dimension":"readability","media":"case-01/wide-119.png","sha256":"COPY_FROM_MANIFEST","frame":119,"finding":"Concrete visible evidence and its consequence"}
```

For timing/continuity, cite video evidence for both formats with the frame of the issue or demonstrated rest. Use `frame / fps` for timestamp interpretation. Do not merely repeat a brief or infer behavior from a still. Scores are reviewer judgments:

| Dimension | 0–1 | 2–3 | 4–5 |
| --- | --- | --- | --- |
| hierarchy | Primary element unclear | Competing attention | Primary and secondary sequence clear |
| readability | Key copy unusable | Strained at delivery size | Copy and hold comfortably readable |
| continuity | Identity/anchor breaks | Some unintended jumps | Intentional cuts and stable identity |
| timing | Action/feedback or hold fails | Uneven pace | Purposeful entry, travel, settle, hold |
| purpose | Motion obscures stated intent | Partial relationship | Movement makes the brief clear |

Run `benchmark.py assess WORKSPACE/public`. It checks case IDs, media SHA256, exact still frames, score range, attribution and observed evidence. It cannot prove a reviewer actually watched or that an opinion is correct. Null scores remain pending. Invalid or incomplete cases prevent aggregate scores. Do not call a technical render pass an aesthetic pass.

After locking the blind reviews, separately compare findings to the private injected-defect key. Report detected, missed and false-positive defects in prose with evidence; do not conflate detection accuracy with aesthetic quality. These controls are synthetic instructional samples, not independently judged professional gold standards. Preserve review versions, reviewer/model identity and playback limitations before comparing future agents.
