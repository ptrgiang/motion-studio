# Motion language

## Craft
Anticipation prepares the next action; use it briefly when surprise would otherwise confuse. Overshoot suggests elasticity; use it for playful or soft objects, not every financial UI control. A large panel should usually take longer to settle than a tiny indicator. A camera should preserve orientation unless disorientation serves the story. A headline may enter rapidly but then needs a stable reading hold. Use delay based on hierarchy, not a random stagger.

## Adjustable starting points at 30fps
Micro feedback: 4–8 frames; compact entrances: 8–14; panel move/settle: 12–24; orientation-preserving camera move: 20–45. These are starting estimates for testing, not industry limits. Calculate holds separately from movement. Convert seconds with round(seconds*fps); do not reuse raw frame values at a different fps without reviewing perceived timing.

## Curves
For cubic easing, clamp normalized progress and specify endpoint velocity where a move joins another move. For spring motion, pick damping/mass/stiffness, inspect peak overshoot and settled frame, then ensure the layout can tolerate excursions. Clamp only when the design calls for it, not to hide poorly tuned motion. Use linear movement for deliberate constant speed; use steps for mechanical or editorial effects. Motion blur cannot fix a bad curve.

## Typography
Use hierarchy with size, weight, width, placement and space. Animate words as meaningful units. Avoid arbitrary letter fragmentation that slows reading. Do not distort logos or variable-font axes beyond their design. Review phone-scale copy, longest localized line and smallest supporting text. Raster screenshots require enough pixel resolution at the largest crop. Keep thin lines on stable pixel boundaries if subpixel shimmer becomes visible.

## Continuity test
At a transition's before/mid/after frames, identify the same focal object and explain its transformation. If the viewer must find a new object and read new copy while the camera moves, reduce one competing action. Cut on a purposeful change of information; do not insist all shots morph.
