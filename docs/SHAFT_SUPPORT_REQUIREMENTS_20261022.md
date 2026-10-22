# Shaft support and manufacturing requirements 006

22 October 2026. Source-backed requirements candidate, not hardware selection, a fabrication drawing or a disassembly procedure.

## Useful result

A replaceable component does not by itself make the shaft serviceable. We can now distinguish three manufacturing routes and the support functions that must remain accounted for during renewal. This closes specific process-definition gaps without inventing bearing ratings or loads.

The [SXL guide, February 2024](https://thordonbearings.com/docs/default-source/marine/documents/for-successful-installation-of-sxl-turbine-guide-bearings.pdf?sfvrsn=b6b5eb2a_6), p2, distinguishes interference fitting from bonding into a split housing. The bonded route has its bore finish-machined after bonding. Its shaft/liner guidance identifies an ideal initial finish of 0.4 micrometres Ra and says up to 1.6 can perform satisfactorily; p3 separately requires maintaining roughness below 1.6. These are manufacturer guide statements, not an adopted project tolerance or proof of tidal suitability.

The [SKF maintenance handbook](https://www.skf.com/binaries/pub12/Images/0901d1968013be94-SKF-bearing-maintenance-handbook---10001_1-EN%281%29_tcm_12-463040.pdf), printed p30, describes locating support for radial load and axial location in both directions, with non-locating support accommodating thermal movement. Separate radial/thrust bearings are another arrangement. This is September 2011 general guidance, explicitly not an application design catalogue; no bearing or current product rating is selected.

## Manufacturing and renewal comparison

| Route, not selected | Documented constraint | Engineering implication to investigate | Missing evidence |
|---|---|---|---|
| Interference-fit SXL guide | Supplier sizing determines wall thickness and fit | Machining/inspection must be tied to the qualified sizing record | Dimensions, fit, supported removal motion and replacement acceptance |
| Bonded SXL in split housing | Bore finish machining follows bonding | Compare workshop-prepared housing replacement with on-site component work; do not assume either is feasible | Bonding/process qualification, re-machining access, datum repeatability and complete cost |
| Tapered-key SXL arrangement | Separate leaflet claims shell renewal while retaining shaft/housing | Treat this as a distinct candidate renewal task | Selected arrangement, access, support during renewal and measured task time |

The [tapered-key leaflet](https://thordonbearings.com/docs/default-source/hydro-power/documents/thordon-sxl-water-lubricated-main-shaft-guide-bearings.pdf?sfvrsn=538c03b4_24) does not establish that its renewal claim transfers to the bonded or interference-fit routes. No route is shown cheaper or faster for this turbine.

## Three interfaces that must not be conflated

1. Wet shaft/liner running surface: finish, corrosion resistance, bearing clearance, water and abrasive conditions.
2. Dry coupling shaft-hub joint: bore/key/contact geometry and independently checked torque transmission. The [KTR SH manual](https://www.ktr.com/fileadmin/ktr/media/Manuals/40229en000000.pdf), edition12 p7 section2.5, distinguishes spider torque from shaft-hub capacity and requires application selection and torsional consideration. A catalogue bore range does not size the turbine shaft.
3. Structural support: radial and axial rotor reactions, bending/misalignment, thermal movement and frame/housing paths. Shell retention does not establish rotor-thrust capacity. Neither guide nor coupling documents qualify this complete support system.

These interfaces may have different diameters, sleeves and tolerances. That is a design possibility, not permission to choose an arbitrary stepped shaft. Keyways, shoulders, fits and transitions remain stress/fatigue and manufacturing-review inputs.

## Load and support evidence needed before choosing hardware

Use the machine-readable `research/shaft_support_006.json` as the open requirements register. It intentionally contains no numerical loads or selected bearing ratings.

For each normal, transitional, fault, parked, service and retrieval case, record a coordinate frame; force and moment components; signed speed; duration/cycles; gravity/buoyancy; support locations and stiffness assumptions; source and uncertainty; and how simultaneous loads are combined. Component renewal states need their own support analysis, not just the operating diagram. This is an evidence checklist, not instructions to perform those states.

The previously illustrated 88.4 Nm mean torque is not a peak, reversing, fatigue, braking or stall envelope. Its nominal operating assumptions cannot qualify a shaft/hub or bearing. Support spacing and load placement are also missing, so even a trustworthy rotor resultant alone would not determine every bearing reaction. No fatigue life, critical speed or static margin is calculated here.

Crossflow dry PTO and axial dry PTO have the same conditional access to dry-side support/coupling evidence. Axial submerged-pod seals, pressure boundary and bearing environment remain separately unqualified. Rotor orientation and selected support arrangement are not frozen; no architecture wins by assumption.

## Next decision and stopping condition

Can a supplier/application-qualified shaft/support layout retain the required datums throughout the same defined renewal task, without relying on the component being removed to carry rotor loads?

Advance to component selection only when geometry, load cases, support reactions, material/fit, environment, service-state support and applicable supplier limits are documented and reviewed. If a proposed route cannot preserve support or requires inaccessible machining, reject that route or revise its service boundary before claiming savings. Requesting information, commissioning engineering, procurement and physical work are not performed or authorized by this document.

FORCE remains at zero qualified cells pending original native burst/configuration/QC lineage. RM2 B10/B12 originals and physical encoder zero remain missing for the unexecuted frozen comparison. Environmental and physical qualification gates are unchanged.

## Inspection and verification limits

SKF edition/foreword and printed p30 text/figures were inspected, not the entire handbook. SXL guide pp2–3 and KTR p7 text were rechecked against the previously downloaded official documents; SXL p2 was visually reinspected. No claim that those two files were freshly refetched. All new findings were reviewed on 22 October 2026. Source PDFs are not redistributed. Software tests check traceability and preservation of unknowns, not engineering validity.
