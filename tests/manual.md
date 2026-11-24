# Local smoke checks

1. Disconnect internet, or use browser offline emulation. Open index.html locally, then each study link. All three load without a web server. Confirm DevTools shows no HTTP(S) requests, permissions, or runtime errors.
2. v0.4: select Pier, then Boardwalk, and move the viewpoint slider by keyboard. Verify the angle and nine domes update. Change water to Passing wake; it must change the reflections, not the nine physical domes. Select From above: no reflection is drawn and the status line says so. Verify sound is initially off, start a rise, and switch to Day or change the water before it finishes; no dome may stay lit and no old cue may keep playing. Let a rise finish: nothing stays lit. Repeat with reduced motion (the order appears as text, with no timed animation) and with sound muted.
3. v0.3 archive: confirm six ribs and the Archived label, change viewpoint and weather, start a handoff and return to Day before it finishes.
4. v0.2 archive: confirm three ribs, change viewpoint, and use Day/Night, Shore tap and Event release. Confirm status explains local simulation and that no connected device is implied by any cue.
5. At 360 px viewport width, verify that controls wrap, text is readable and there is no horizontal scrolling. Tab through all controls at desktop and narrow widths; verify focus and that every control has a readable name.
6. Read the original SVGs and their paired PNGs. Follow all local doc, asset and demo links. Confirm imagery is synthetic or original, no personal or private references are bundled, and earlier studies are identified as such.

Run the automated static checks: `python3 tests/check_public.py`. Browser testing is also needed for interactive changes.
