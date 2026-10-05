# Review rubric

## Blockers
Invented product fact/screen; wrong logo; absent required asset; unreadable essential copy; clipped important content; corrupt export; unresolved required audio; missing requested aspect ratio; unreviewed mandatory temporal/audio quality. These prevent verified final regardless of score.

## Observed score (0–5 each)
Hook: clear first impression linked to the film's purpose.
Readability: essential copy can be understood at destination size during actual holds.
Hierarchy: focal priority remains clear, including transitions.
Continuity: spatial/object/story relationships are understandable.
Motion: acceleration, weight, settle and holds support meaning.
Sound: mix and cues support the film; mark N/A only for intentional silence.
Format adaptation: each composition works in its own aspect ratio.
Truth/brand: observed assets and claims match provenance and brief.
Use 0 broken, 1 severe, 2 weak, 3 usable with visible issues, 4 strong with minor issues, 5 excellent observed execution. Default pass policy: each applicable dimension >=4 and no blockers; do not average away a weak category. Mark unobserved categories pending, not 4.

## Evidence requirements
Visual: image paths plus frame numbers/timestamps; phone-scale snapshot.
Temporal: viewed clip/segment and inspection notes.
Audio: listened file/segment plus measured loudness/peaks if target requested.
Technical: ffprobe metadata compared with spec, full decode check, presence of requested streams, exact frame count and duration tolerance <= one frame.
Determinism: decoded pixel hashes for repeated/shuffled seeks within a controlled runtime.
Delivery: files exist, source rerender command works, dependency versions and asset list supplied.

## Local repair example
Observed: frame 210 of vertical.mp4, supporting text lies under CTA at phone width. Impact: proof cannot be read. Fix: reduce concurrent UI card count and move CTA to the close; preserve typography token. Retest: 190, 210, 230 and the preceding/following transition segment. Avoid "make it more polished".
