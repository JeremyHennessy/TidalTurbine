# TidalLab GitHub Pages research app — UX specification and boundaries

## Objective
A responsive, accessible *research workbench* for comparing established tidal-stream architectures and examining the verified SCREEN-001 numerical result. **A visualization of a device concept is not design engineering.** A synthetic power curve must remain visually differentiated from real measured ocean data.

## Routes (static, client-side hash)

- `#overview`: hero, research state, illustrative turbine SVG, archived experiment values, source discovery and six-stage validation progression.
- `#designs`: four SVG architecture **mockups** (seabed HAT, recoverable floating, cross-flow, tethered kite), choice selector, annotations, pros/cons and specific falsification evidence. No scored ranking/winner.
- `#experiments`: read `reports/SCREEN-001.json`. Replot two synthetic harmonics, baseline vs 80%-rated export cap, and archived 81-case sweep. Slider 50–100% runs **browser-only electrical** calculation; does not mutate report or infer blade load, Cp change, structural life, or ecological safety.
- `#ocean`: approximate labelled Fundy schematic with one precisely documented FORCE instrument coordinate marker (45.3631, -64.4275), curated metadata table, search/type filters, data access status and expanded provenance/source links. No invented current values, no false cartographic precision.
- `#research`: stages, actual evidence qualification status, source read path and three next gates.

**No subscription or build service:** static HTML, SVG, JS, CSS; Python stdlib for test/site copying; no third-party JavaScript or embedded external maps. Text is encoded before injection. Mobile single-column layout; nav expands on small viewports; accessible link/focus/section labels; prefers-reduced-motion respected.

## Hosting

Repository-root `index.html` redirects to `site/`. All static files and canonical experiment/metadata JSON are committed to the repo; Pages can publish directly from main/root. The `.nojekyll` sentinel avoids Jekyll transformations. The site fetches relative canonical paths `../reports/SCREEN-001.json` and `../research/ocean_datasets.json`; paths work both locally and with repository-subpath GitHub Pages. **Check live Pages settings and complete post-merge deployment before claiming a public URL**; GitHub Actions tests are not a substitute for browser inspection.

Local preview:

```sh
python scripts/build_site.py --out dist
python -m http.server 8000 --directory .
# Open http://localhost:8000/ (or /site/)
```

The `dist/` folder also contains the static artifact (root redirect + `site/`, archived JSON and registry), reproducibly copied by the builder. Build artifacts and raw datasets are not checked into Git.

## Visual regression / approval

This iteration introduces the first TidalLab visual language; no previously approved UI existed. After a screenshot is approved, lock that commit + screenshot and do not restyle the approved state for unrelated data/logic fixes. A design-review screenshot is not a scientifically calibrated illustration.

## Boundaries and next functionality

Not yet implemented: validated measured ADCP series visualization, RM1 benchmark overlays, physical blade/control model, solver visualization, authenticated collaborative edits, downloadable signed design files, grid-scale scheduling/battery dispatch and environmental risk prediction. Add each **only** when source and validation gates are met. GitHub Pages serves public files; sensitive Traditional Knowledge or restricted survey products must not be uploaded.
