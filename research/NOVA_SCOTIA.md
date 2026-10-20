# Nova Scotia / Bay of Fundy research notes (as of 2026-10-20)

**Site suitability is not established.** The provincial overview [NS-001] describes Minas Passage, Petit Passage and Grand Passage and cites exceptionally strong tidal currents; figures are regional promotional context, NOT verified turbine-hub current sequences. Strong flows can increase wake loading, turbulence, cavitation, installation and access risk.

## Status and governance

- The Province currently lists four licensees and says Orbital Marine Power and Nova Innovation are upcoming technology programs [NS-001]. A 2025 Government announcement describes additional Eauclaire/Orbital FORCE berths [NS-2025-001]. The FORCE 2025 update reports a DFO Fisheries Act authorization **for deployment of up to three devices**, not proof of deployment or grid generation [FORCE-2025-001]. Confirm any 2026 operational change before quoting installed generation.
- The 2026 demonstration-permit program [NS-2026-001] states an application window ending October 30, 2026, with a program total 7.70 MW and each project under 2 MW, subject to legal terms. Do not interpret research access as an authorization or apply without user direction.
- DFO's staged authorization under the Fisheries Act / Species at Risk Act requires adaptive risk assessment and environmental monitoring [DFO-001]. Monitor fish transit through swept area, both ebb/flood tides and day/night and seasonal variability; sensors need fail-detection and appropriate performance at high flow. Provincial Marine Renewable-energy Act and federal processes both matter.
- Fisheries including lobster, marine mammals and species at risk; navigation, fishing gear, cabling, seabed disturbance and marine noise require specific consultation and study. No low-risk claim is currently supported [DFO-001; OES-001].
- FORCE published a Mi'kmaq Ecological Knowledge Study prepared by the Confederacy of Mainland Mi'kmaq [MEK-2026-001]. Project decisions must respect Mi'kmaq rights, priorities, knowledge governance and engagement rather than treat the report as approval of any specific device or site. Do not publish sensitive traditional knowledge or presume consultation is complete.

## Data qualification needed before using a site

1. Identify independently accessible ADCP current vectors by georeferenced location, depth, timestamps, QA, sampling and tide phase; retrieve license and checksum. Validate vertical shear and turbulence as well as speed histogram.
2. Acquire depth/bathymetry, wave extremes, geotechnical/scour and ice/debris; verify navigation, fishing patterns, protected species, indigenous interests and grid/export distance.
3. Obtain DFO/FORCE monitoring plans/reports and detection probability/missing-data treatment; do not infer 'no collisions' from no detections.
4. Model access windows and mooring/foundation/cable loads using site-specific measured conditions before economic preference.

**New 2026-10-20 discovery:** [OCEAN-001 FORCE March–May 2018 ADCP current profiles](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Currents/index.html) provide a listed CC BY 4.0 NetCDF file, published instrument coordinates (45.3631, -64.4275) and east/north/up velocity variables in m/s, and [OCEAN-002 waves](https://cioosatlantic.ca/erddap/info/FORCE_Mar2018_ADCP_Waves/index.html) from the same campaign. Source metadata examined; raw observations **not downloaded**, bin depths/QA unverified. This changes the dataset-discovery status but **does not change** SCREEN-001, which remains synthetic. See [OCEAN_DATA.md](../docs/OCEAN_DATA.md) and `research/ocean_datasets.json`.

**Explicit open question:** After source acquisition and instrument calibration, can these public FORCE profiles support a defensible short-duration current characterization? They do **not** yet establish long-term resource adequacy, rotor load predictions or environmental safety.
