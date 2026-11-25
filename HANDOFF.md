# HANDOFF: WATERLINE, Six Rings on Mother (v0.5, rim-footed weave)

> **Living document.** Single source of truth for where this work stands and
> what's next. Any agent starting fresh reads this first, then updates it before
> ending. If anything here disagrees with reality, reality wins: fix the doc.

**Last updated:** 2026-11-25 by Claude (model, renders, docs brought to the woven ring form)
**Active branch:** `main` (work arrives by pull request; do not push to `main` directly)
**Driving refs:** [AGENTS.md](AGENTS.md) (repo rules, binding), [docs/rings-on-mother.md](docs/rings-on-mother.md) (the design), [models/gen_rim.py](models/gen_rim.py) (geometry and first-pass checks)

---

## 1. Read-this-first orientation (for a fresh agent)

1. Read this whole file, then AGENTS.md. Its rules override defaults.
2. Read the design note. Detail lives there, not here.
3. Verify ground truth live before trusting any number below.
4. Check **Status** for what is done and what is next.
5. Check **Open questions**. They are the artist's to call. Do not guess.
6. When you finish a unit of work, update Sections 3, 5 and 7.

**Ground truth (re-verify; never trust a stale number):**

| Thing | Value | How to check |
| ----- | ----- | ------------ |
| Static check | passes | `python -I tests/check_public.py` |
| Float and structure check | about 851 kg, buoyancy 2.4 times weight, tubes 189 mm apart counting strips | `python -I models/gen_rim.py out.json` (asserts stop it if a margin is lost) |
| Model bodies | all closed solids | `solidcraft-cli eval --in models/waterline-rim-weave-r3.sc` |
| Simulator | no console errors, sound off at start | open `simulators/weave.html`, follow `tests/manual.md` step 2 |

---

## 2. What this effort is

WATERLINE is an unbuilt concept for a floating artwork on Harbour Square Park Basin, Toronto, for a 2027 public call. Six aluminium half rings foot on one floating ring and weave over open water; the lake reflects their lower halves. After dark each ring carries a value and a tone, and a short band of colour travels along it through the hour. This repo holds the public design note, an offline simulator, diagrams, and a solid model with first-pass checks. Nothing here is engineered, surveyed, priced or approved.

The current task is **previs**: better renders and views of the model.

---

## 3. Status

Statuses: `Not started` · `In progress` · `Blocked` · `Done`.

| # | Item | Status | Updated | Note |
| - | ---- | ------ | ------- | ---- |
| 1 | Form: six ribs footed on the ring, woven, no mesh | Done | 2026-11-25 | `models/gen_rim.py`, revision 3 |
| 2 | First-pass float, wind, wave, rib, power checks | Done | 2026-11-25 | Planning arithmetic only. No engineer has seen it. |
| 3 | Design note, diagram, simulator in the new form | Done | 2026-11-25 | Simulator has an Above view, six tones, travelling bands |
| 4 | Light: two strips per rib, top and underside | Done | 2026-11-25 | Modelled and written into the note. Not priced. |
| 5 | Previs: close-up renders | In progress | 2026-11-25 | `models/renders/` has day and three night views. Plain lighting, flat water. |
| 6 | Previs: animation of the hour (thread, then travelling bands) | Not started | 2026-11-25 | Simulator shows the logic in 2D; no 3D animation exists |
| 7 | Previs: in-situ views | In progress | 2026-11-25 | Composites exist locally only (see Key facts). They look pasted in. |

**Next action:** improve the renders in `models/render_closeup.py`: real water (ripples, depth colour), sky lighting that suits dusk, the normal operating state (one to three short bands, not every strip lit), and a short animation of one hour.

---

## 4. Decisions locked (don't relitigate without the artist)

1. Ribs weave seen from above and keep a clear gap; they do not touch. 2026-11-25.
2. Every rib foots on the ring. No mesh, no cross-frame, open water inside. 2026-11-25.
3. Six tones in a dusk range (pale gold, orange, terracotta, rose, magenta, violet). No red, green, white, yellow or blue. 2026-11-25.
4. A held value shows as a short band that travels foot to foot through the hour. 2026-11-25.
5. Light strips run the full length of each rib, one on top and one on the underside. No block at the crown. 2026-11-25.
6. Float and the ring on it are water grey. Ribs are the only honey-toned part. 2026-11-25.
7. One navigation light post, on the side away from the shore. The shore-side post was removed. 2026-11-25.
8. No camera, no powered shore unit. Public choice is one way, via a code on a sign, and stays a local simulation in this repo. 2026-11-24.

---

## 5. Open questions owned by the artist (get answers before acting)

1. Does one navigation light satisfy the harbour authority? The call requires navigation lights. Blocks the final model.
2. Can the float pipe be supplied with a grey outer skin, or does it need a sleeve? Blocks the finish description.
3. Anchor type. A storm gust pushes about 8.5 kN sideways and the lakebed type is unknown. Blocks the mooring design.
4. Which stretch of shore the eye faces. Blocks final in-situ views.
5. Does the second row of light strip fit the budget? It is unpriced.

---

## 6. Key facts a fresh agent will want

- **Geometry has one source.** `models/gen_rim.py` holds every size. It writes a SolidCraft script; the simulator (`simulators/weave.html`) repeats the same six ribs by hand, so change both together.
- **Rebuild the model:** `python -I models/gen_rim.py models/waterline-rim-weave-r3.script.json`, then `solidcraft-cli run <script> --save <name>.sc --out <name>.step --out <name>.glb`. Add the word `mooring` to the first command for the version with anchors.
- **Render:** `blender -b -P models/render_closeup.py -- models/waterline-rim-weave-r3.glb models/renders`. Blender 5.x, Cycles. Body names in the GLB drive materials: `Rib ...`, `Light strip top ...`, `Light strip under ...`, `Float ring`, `Aluminium ring`.
- **The GLB is in metres, Y up.** Water is at height zero. The shore view looks along +Y from the -Y side.
- **The night renders light every strip end to end** to show placement. The work itself lights one to three short bands. Say so on any image.
- **Tones wash toward white** when emission is strong. Keep emission low to hold the colour.
- **A local, untracked folder holds submission drafts and composites on third-party site photos.** It is excluded from git on purpose. Never commit it, and never add those photos to this repo.
- **Writing rules for all public text:** plain words, no em or en dashes, no partner, approval or commission claims, estimates labelled as estimates. See AGENTS.md.
- `models/waterline-v05.*` is the earlier parallel-rib form, kept for comparison only.

---

## 7. Activity log (newest first; append, don't overwrite)

- **2026-11-25** Reworked the form in a solid model: ribs footed on the ring, woven, mesh removed. Added first-pass checks, feet, strips, power and mooring to the model. Brought the note, diagram and simulator to the new form. Added six tones, travelling bands, a second row of strips, grey ring; removed the shore-side navigation post. First close-up renders.

---

## 8. Update protocol (keep this doc honest)

Update this file at the end of any session that touched the work, and before
handing off or clearing context. Minimum: Status table (status + date + note),
one Activity-log line, move answered items from Open questions to Decisions, and
the `Last updated` line. Keep it tight: state, not narrative.
