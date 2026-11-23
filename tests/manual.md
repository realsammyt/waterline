# Local smoke checks

1. Disconnect internet, or use browser offline emulation. Open index.html locally, then each study link. Both load without a web server. Confirm DevTools shows no HTTP(S) requests, permissions, or runtime errors.
2. v0.3: select Edge, then Weave, and move the angle slider by keyboard. Verify the angle and six ribs update. Change weather to Passing wake; it must change the reflection, not the six physical ribs. Verify sound is initially off, switch to Night, start a handoff, and return to Day before it finishes. Make sure an old cue does not keep playing after the mode change. Repeat with reduced motion and sound muted.
3. v0.2: confirm three ribs, change viewpoint, and use Day/Night, Shore tap and Event release. Confirm status explains local simulation and that no connected device is implied by any cue.
4. At 360 px viewport width, verify that controls wrap, text is readable and there is no horizontal scrolling. Tab through all controls at desktop and narrow widths; verify focus and that every control has a readable name.
5. Read the original SVGs and their paired PNGs. Follow all local doc, asset and demo links. Confirm imagery is synthetic or original, no personal or private references are bundled, and earlier studies are identified as such.

Run the automated static checks: `python3 tests/check_public.py`. Browser testing is also needed for interactive changes.
