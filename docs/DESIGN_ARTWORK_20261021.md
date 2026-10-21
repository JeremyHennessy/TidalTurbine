# TidalLab fourteen-mechanism illustration refresh — 2026-10-21

**Evidence classification: CONCEPT VISUALIZATION / DESIGN HYPOTHESIS.** These images represent component layouts in readable, visually consistent scalable vectors. They are **not** measured dimensions, fabrication drawings, site-specific designs, CFD results, validated loads or vendor/manufacturer specifications.

## One visual language; fourteen distinct mechanism studies

A new, dependency-free `site/artwork.js` renders each of the 14 source-indexed converter mechanisms in the same 700 × 410 illustrated underwater engineering setting (ocean depth gradient, unobtrusive grid, flow direction, distinct metallic components, support/seafloor or mooring context). Artwork is hand-authored source SVG geometry rather than binary hosted stock imagery. The identical vector system is used by large selected concept drawings, side-by-side architecture comparison, overview previews and newly added selection-thumbnail images. Images can be saved via **Download drawing** in the studio as actual standalone, XML-valid SVG files.

| Canonical ID | Mechanical image identity and drawing emphasis |
| --- | --- |
| `seabed` | fixed monopile, three-bladed axial propeller, nacelle and illustrative cable |
| `floating` | surface-service hull, two removable submerged turbine pods and seabed moorings |
| `counter` | two axial propeller disks, opposite rotations, common support |
| `rim` | rim-driven annular turbine, blades round an open centre and outer drive ring |
| `crossflow` | vertical H-rotor with straight lift blades, central shaft and struts |
| `helical` | three curved/twisted cross-flow lifting ribbons round a vertical axis |
| `savonius` | overlapping drag-scoop cross-flow rotor, top/bottom supports |
| `foil` | reciprocating heave/pitch foil, guide and PTO linkage |
| `screw` | axial continuous spiral helix around horizontal shaft and bearings |
| `kite` | tethered flying hydrofoil with two carried rotors and anchored flight envelope |
| `duct` | axial rotor enclosed inside a tapered inlet/diffuser, with support |
| `pressure` | immersed pressure coupling and symbolic secondary PTO path (concept only) |
| `eel` | compliant fluttering flag with putative piezoelectric strips and rectifier |
| `viv` | oscillating cylinder with illustrated vortices, springs and linear PTO |

These **mechanical arrangement sketches** are informed by the taxonomy in `research/mechanisms.json`. They do not imply that a particular prototype operates, converts net electrical energy, outperforms another architecture or has acceptable ecological/fatigue behaviour. The speculative pressure, flutter and VIV options remain hypotheses with low-confidence measured power and lifetime boundaries.

## Rendering, UI and accessibility changes

- `site/artwork.js` defines 14 explicit keyed SVG scenes, reusable component drawing primitives and per-mechanism component annotation points. SVG has unique keyed gradient IDs for variant-specific illustrations, text alternatives in the full-size drawing, and decorative thumbnails marked `aria-hidden`.
- `site/index.html` loads `artwork.js` **before** the existing `app.js`. The existing `designSvg()` uses the new renderer when present and preserves the legacy drawing fallback if it fails to load. Original experimental tables/reports are unchanged.
- `setupDesign()` now renders all 14 as illustrated card choices with actual pressed-state accessibility; search and mechanism filters retain the existing source catalogue. The existing **Labels on/off** control toggles SVG component callouts, not geometry. An actual **Download drawing** control saves source-generated **self-contained SVG** with no remote texture or font; the exported XML is valid in the browser QA. The source SVG carries no numerical size specification.
- Styles remain consistent with the existing dark TidalLab desktop layout, with grid gallery and simplified side-by-side art on phones. No image downloads from remote servers or fonts required.
- Static `scripts/build_site.py` bundles `site/artwork.js` as its 18th source-controlled Pages file. All raw third-party current data, lab NI data and binary illustrations remain out of Git.

## Verification (branch stage; no premature live-site claim)

Branch: `ui/design-artwork-atlas-20261021`, based on verified main `a33a885194b9f6003e145e7e77b7fa7dca49e707`. Temporary one-day CI artifact created solely to render the **exact build** from the reviewed Git blobs. Final source-check browser asset identities after XML export fix: site HTML Git blob `4a430de4b68877cbefa72c20a8a8ea2ae4df512c`, CSS `1048cee3bd629dd923806bebc5b57bd7cc41f882`, vector artwork JS `c9375765df75a18d85efa822f8724935d14f570b`, app JS `61d6e8915d2e7aca3bfca7c0d00c5b88ed2685ee`. The native-source research and experiment reports were not modified by this visual pass.

Offline source-exact Chromium QA (network-navigation sandboxed; original HTML/CSS/JS source inlined unchanged, all reports furnished unchanged via fixture-backed `fetch`): at **1600×900, 1280×800, 800×1000 and 390×844**, all **14** thumbnails and **14 selectable large design scenes** rendered and validly XML-serialized, for 56 viewed scene selections. No JS console exceptions, unintended document-wide horizontal overflow or broken selection state across Overview/Designs/Experiments/Ocean/Research. Checked labels toggle off/on, comparison rendering and a clicked SVG image download: `tidallab-crossflow-concept.svg` parsed as a stand-alone valid XML image with no remote image tags. Screenshots for all 14 concept panels inspected as a contact sheet and mobile examples. This is offline real Chromium QA, **not** live public Pages interaction testing.

Automated Node `tests/ui_smoke.cjs` verifies 14 distinct keys, all thumbnail markup, illustration role/text alternative, isolated vector scenes, annotation removal/restoration, and XML-safe standalone text, in addition to prior SCREEN/RM1/RM2/FORCE status assertions. Python `tests/test_site.py` asserts correct script order, source packaging and self-contained artwork. **Final-head CI still required after removing temporary artifact upload**, then isolated PR review/merge, postmerge main CI and Pages deploy validation. Independent live HTTP byte parity may be checked via `python scripts/verify_pages_live.py --check`; HTTP parity is not proof of JS interaction.

**Release boundaries:** no performance figures, simulator current, field current, cost, blade-root fatigue, marine permit, manufacture or prototype selection changed. The images remain meaningful *illustrations*, not dimensioned engineering designs.
