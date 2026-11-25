# Six Rings on Mother · v0.5

**Six half rings, one woven eye.** Six slender arches spring from one floating ring and cross over the round of lake it holds. The lake supplies their lower halves. From the shore the six rings and their six reflections weave into a single eye that you look through. From above they cross like the strands of a basket. A wake takes the lower half away and lets it come back. Nothing moves mechanically, and nothing below the waterline is built.

A bubble sitting in the foam on a kitchen jar is half in the liquid. Seen from the side it is a half ring, finished by its reflection. Each arch is that outline, more than a thousand times life size. The mother is the disc that grows on top of a jar of fermenting tea and is passed from kitchen to kitchen. Here it is a floating ring and the round of lake inside it. The jar is the basin itself, walled on three sides and open to the harbour on the fourth, 112 m by 51 m in the call's description.

[Diagram source](../assets/diagrams/rings-on-mother-v05.svg) · [PNG](../assets/diagrams/rings-on-mother-v05.png) · [Offline simulator](../simulators/weave.html)

This form returns to the six ribs of [v0.3](six-ring-weave.md) and keeps the mother, the four words and the safety answers of [v0.4](honey-foam.md), whose nine domes are archived. The domes were something to look at. The rings are something to look through. In November 2026 the form was reworked in a solid model: the ribs now foot on the ring and weave, and the mesh is gone. The statement text at the end is a working draft, not a record of anything submitted.

[Model generator and first-pass checks](../models/gen_rim.py) · views from the model: [above](../models/waterline-rim-weave-r3-top.png), [shore](../models/waterline-rim-weave-r3-front.png), [angle](../models/waterline-rim-weave-r3-iso.png) · renders: [day](../models/renders/day.png), [night from the shore](../models/renders/night-strips-shore.png), [night from above](../models/renders/night-strips-above.png). The night renders light every strip along its whole length to show where the strips sit; the work itself lights one to three short bands.

The v0.5 diagram, the simulator, the solid model, the first-pass checks and the drafts in this note were prepared with AI assistance (Claude, by Anthropic) at the artist's direction. The idea, the four words and the choice of form are the artist's.

## The form

All dimensions are illustrative values for optical study. None is surveyed, engineered or costed.

- **Mother.** One floating ring about 7 m across, its top roughly 0.2 m above the water, with open lake inside it. There is no mesh and no deck, and nowhere flat and dry to stand. A slim aluminium ring sits on the float and carries the ribs.
- **Rings.** Six fixed half rings, each one smooth round tube about 15 cm thick, each a single circular arc. Every foot lands on the ring, so each rib spans about 6.5 to 6.7 m. Three tall ribs rise about 1.85, 1.7 and 1.55 m and turn about 25 degrees one way. Three low ribs rise about 1.3, 1.15 and 1.0 m and turn about 25 degrees the other way. Each set tips a little, by 10 and 25 degrees. Seen from above they cross at nine points. The low ribs pass under the tall ones, and the tubes stay about 0.2 m apart where they come closest. They do not touch.
- **Out of scale.** A bubble in kitchen foam is a few millimetres across, so the widest ring is more than a thousand times life size. A mother in a jar is about 15 cm across, so the ring is under fifty times. The bubbles have outgrown what they rest on.
- **Finish.** Starting point: honey-toned anodised aluminium, satin, so the ribs carry the colour of the mother without paint. Bare silver aluminium stays as the fallback until coupons are compared. Anodising follows rolling, half a rib at a time. The float has a water-grey outer skin so that it recedes into the lake, and the aluminium ring on top of it is the same grey, so the ribs are the only warm thing. A black float and a honey ring were both tried in renders and set aside.

## The eye

Each rib is a shallow arc, so rib plus reflection is not a circle. It is an eye with pointed corners. Head-on, the six cross one another and read as one woven eye. Through it, from the shore, is open water. From the water, through the same eye, is the city.

The eye is complete only when the water is calm. That is the point of it: the lake decides whether it is there. The upper ribs must still read as a finished work on a day when no reflection forms.

With no mesh, the water inside the ring is open, so the reflections of the ribs fall on lake water all the way to their feet. Only the ring itself breaks the mirror, as one thin line. This is read from the solid model, not measured, and is the first thing a small physical model has to show.

## Proposal-stage build basis

First estimates for a proposal, not engineering. The call requires a marine engineer licensed in Ontario to set the real values and stamp drawings before fabrication.

- **Overall size.** About 7 m across and about 2.2 m above the water at the highest point. Low on purpose: the call asks for simple, light and not too tall.
- **Anticipated weight.** Roughly 0.8 to 0.9 tonnes afloat by a first count of parts: float about 330 kg, aluminium ring about 115 kg, six ribs about 180 kg, the rest fixings, light and power. Built in sections that travel by road and lift separately: four float quarters and twelve half ribs.
- **Materials.** Polyethylene pipe float in four sealed, foam-filled quarters. One aluminium tube ring on top of it. Six rolled aluminium tube ribs in two halves each, socketed and bolted at the feet and joined at the crown by a sleeve inside the tube, so the seam is flush. Stainless fixings, kept from touching the aluminium directly. No paint, no antifouling coating and no treated wood in the water. Mechanical fixings throughout, so it comes apart.
- **Mooring.** Three lakebed anchors spread around the ring, none to the dock wall or pier, with slack for changing water levels. Three points hold the heading, so the eye keeps facing the same stretch of shore. A first estimate of the sideways push in a summer storm is about 8 kN, far more than a 50 lb block holds, so anchor type and size are the first question for the engineer and Waterfront Toronto.
- **Light and power.** Two slim light strips run the full length of each rib, from socket to socket and unbroken over the crown: one along the top and one along the underside, each in a shallow channel under a flush diffuser so the tube stays smooth. The underside strip faces the water, so it is the one the lake reflects. Only a short band of each is lit at a time, in that ring's own tone. Through the night one, two or three rings carry a band at a low level, rarely all six, and strips on unlit ribs are switched off. Narrow solar panels on the ring, on the side away from the shore, and a small battery carry it: a first estimate is about 145 Wh a day, 90 to 120 W of panel and a 450 Wh battery, none of it measured. A small cellular modem fetches the hour's choice, and nothing can reach in. Required navigation lights sit on their own power and control, and no public choice touches them.
- **First-pass checks.** The float could carry about 2.5 times the weight before going under, and about 1.9 times with one quarter flooded. A 100 kg load on one edge tilts it about half a degree, and a storm gust about 2 degrees. Waves, not wind, size the aluminium ring. The ribs are lightly loaded, but a steady breeze could set a bare tube humming, so a damper hangs inside each rib. These figures come from the model generator, which stops if a margin is lost. They are a planner's arithmetic, not engineering.
- **Warnings.** Do-not-climb notices on the outer face of the float, readable from a boat approaching from any side.
- **Maintenance.** A boat inspection every two weeks and after any storm: fixings, rib feet, mooring lines, lights. Floating litter caught inside the ring is lifted out on the same visit. There is no skin to tear and nothing to patch.
- **Installation and removal.** Sections arrive by road, are joined at the water's edge, lowered or assembled afloat, towed into place and moored. Removal runs the same steps in reverse in early October.
- **Afterwards.** The ribs are sized to stand again on land as garden arches or the frame of a growing tunnel. No recipient is confirmed.

## Four words

The form is built from four working words in the artist's own Honey Foam vocabulary. Each fit is a judgement.

| Word | In a jar | On the basin |
| --- | --- | --- |
| Mould | The vessel and the conditions we shape | The basin walls, the ring, the six ribs |
| Mold | What grows by itself, spoiling or nourishing | Wake, chop, weather and daylight. Also the literal kind: twenty weeks of fouling on anything that floats. |
| Bubbles | Expression rising, the inside getting out | Each rib with its reflected half, and the light that threads through them after dark |
| Goo | The shared living culture, passed hand to hand | The mother. Under it, the lake, which a city drinks and nobody can rebuild from parts. After October, the work's next keeper. |

## Walking it

From the shore the six cross into one woven eye. Walking along, the crossings slide, and ribs that seemed joined come apart. From the side the work closes to a low stack of arcs. From the buildings above there is no reflection at all, and the work reads as a woven round: six strands crossing over open water inside a ring. From a ferry or a kayak the rings sit at eye level with their reflections under them.

Looking out through the eye from the shore is the inside seen out. Looking in through it from the water is the outside seen in.

## Six values, one hour at a time

A mother stays alive on six things: leaf, sweetness, water, air, warmth and time. Each ring carries one, read as something a city needs to keep its people. The names are the artist's, and each fit is a judgement.

| Ring | Rise | Value | Light this one if | Pitch | Tone |
| --- | --- | --- | --- | --- | --- |
| 1 | 1.15 m | Warmth | someone arrived today and should feel welcome | A | magenta |
| 2 | 1.55 m | Leaf | you are thinking of where you came from | E | pale gold |
| 3 | 1.85 m | Water | the lake, and what we all share, needs looking after | C | terracotta |
| 4 | 1.7 m | Time | the city needs to slow down, or someone should be remembered | D | orange |
| 5 | 1.3 m | Air | someone needs room to breathe or to speak | G | rose |
| 6 | 1.0 m | Sweetness | something today is worth celebrating | C above | violet |

Water sits on the tallest ring because it is the one value nobody opts out of.

- **Choosing.** A sign on shore carries a code to a web page. The same page opens anywhere in the world, for people who call Toronto home. One person, one choice an hour: which value should hold the next hour. No account, no text and no names, so there is nothing to moderate and nothing personal to keep.
- **The hour.** At the top of each hour one thread of light passes through all six rings in the order 1 → 3 → 5 → 6 → 4 → 2. Then the most chosen value shows as one short band of its tone, which travels along its ring from one foot to the other through the hour. Where the band sits tells how much of the hour is left. It moves about 2 mm a second, too slowly to see as motion. With no choices, the thread passes and nothing stays lit.
- **Tones.** The six tones sit in a dusk range, from pale gold through orange, terracotta and rose to magenta and violet, warmest on the tallest ring. None is red, green, white, yellow or blue, the colours that carry meaning on the water.
- **Chords.** Any value with at least half the leader's count joins it, dimmer, and its band travels alongside. Two or three rings lit together are a chord. All six within reach of one another is full harmony. It will be rare, and it rewards balance, not one side winning.
- **They light each other.** Where two rings cross they pass about 0.2 m apart in a satin finish, so a lit ring puts a faint glow on the ones it crosses.
- **Sound.** Each ring has a pitch, tallest lowest. Any chord of the six agrees. The sound plays on the visitor's phone; nothing sounds over the water.
- **Calendar.** A few nights come from the lake and the sky: the first and last night of the season, the solstice, the full moons. On those nights the work plays an authored score stored on the float. No nation's dates, and no colours beyond the six tones.
- **Limits.** Slow fades, no flashes, no spill toward the residences, and a level low enough to run all night. That level is for the mockup and Waterfront Toronto to settle. The link is one way: once an hour the float fetches a count, and nothing can reach in. If the link fails, the work plays its authored order. Required navigation lighting is separate, independently powered and outside the score. The ring numbers are for the diagram; nothing is painted on the work.

The simulator's choices and water presets are simulated. It has no network connection and controls nothing. The web page and the link to the float are proposed, not built.

## Advance only if

1. All six ribs read as a finished work with the reflection masked, from frontal, oblique, side, overhead and water-level views.
2. A small model shows where the reflection lands at shore distances and eye heights, and how much of it the ring blocks.
3. A two-rib mockup shows the light changing ribs from at least two viewpoints at low brightness.
4. The work is legible without sound, without mist and without a device in the visitor's hands.
5. The six ribs on a 7 m ring earn an engineer's review for wind load on the anchors, wave bending of the ring, rib feet, hum in steady wind, handling and climbability: no walkable deck, no foothold on a smooth tube, and open water inside the ring. Nothing transfers from the earlier studies.
6. A written inspection routine says what fouling is cleaned, what is left, and who decides.
7. The six tones and the all-night light level are agreed with Waterfront Toronto and the harbour authority as low enough for the residences and clear of navigation colours, the work plays its authored order with the link cut, and nothing a visitor chooses can reach the navigation lights.

## What it must not become

- A literal jar, lid or bottle. The call recommends work that is simple, light and not too tall. The basin is the jar.
- A health or origin story. Kombucha's ancient-origin tales are unattested, and no drink, benefit, recipe, tasting or live culture is part of the work. Nothing is placed in the lake.
- A scoreboard or a flag. No counts, names or messages appear on the work. Its six tones stay in one dusk range, and it is rare for all six to show at once. The six values name what a living culture needs; they are not a recipe.
- A claim on anyone else's water teachings. The call notes that the lakes are sacred to Indigenous Peoples. The kitchen image and the eye are the artist's own and speak for no one else.
- A gate to pass through. It is seen from shore; nobody boards it, touches it or goes through it.

## Draft opening for the artist statement

> Look closely at the foam on any jar where something is fermenting. Each bubble sits half in the liquid, and from the side it is a half ring, finished by its own reflection. Under the foam floats the mother, the disc that grows on a jar of fermenting tea and is passed from kitchen to kitchen. WATERLINE sets both on Harbour Square Park Basin: six slender half rings, the widest more than a thousand times the size of a bubble, springing from one low floating ring and crossing over the water it holds. Only the upper halves are physical. The lake supplies the rest and takes it away again whenever a wake comes through. From the shore the six rings and their reflections weave into a single eye, and through it you see open water. From the towers above they cross like the strands of a basket. After dark each ring carries one value and one tone, and people on the shore, or anywhere they call Toronto home, choose which one sends a low band of colour slowly along its ring through the next hour. The basin is the jar. The water in it belongs to the Great Lakes, a fifth of the surface fresh water on Earth, and like a mother it can be kept and handed on but not rebuilt from parts.

The call caps the statement at two pages and also asks it for dimensions, anticipated weight, materials, maintenance and installation method. The build basis above gives first values for each; none is engineered or quoted.
