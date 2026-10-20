# TidalTurbine custodian instructions

Scope: **only** `JeremyHennessy/TidalTurbine`. Never touch other repos or buy infrastructure. No site visits, physical tests or external contacts without separate approval.

1. Before making a change: fetch default-branch tip, open PRs/issues, last commits, and AGENTS.md. Reconcile newer work. Preserve approvals as commit-specific checkpoints. Never force-push, overwrite another worker, or edit remote main during a PR review.
2. Evidence classes must remain distinct: `PUBLISHED_EVIDENCE`, `MANUFACTURER_OR_PROJECT_CLAIM`, `ENGINEERING_ASSUMPTION`, `DESIGN_HYPOTHESIS`, `SIMULATION_RESULT`, `EXPERIMENTALLY_VALIDATED_FINDING`, `UNKNOWN_OR_CONFLICT`.
3. An examined landing page does **not** equal a reviewed paper. In `research/catalogue.json` record reviewed page/section, access status, dated metadata, precise claim and limitation. Verify source locations and the current edition/access before referencing a standard. Do not guess missing measurements or reliability rates.
4. Every hypothesis must name comparator, mechanism, falsifier and necessary evidence. Negative and inconclusive results persist. Physical/design changes require staged validation, not merely a passing unit test or photorealistic rendering.
5. Minimize changes. For code changes add deterministic tests; verify both local run and exact pushed commit plus Actions status separately. If CI not yet run, say pending. Do not silently adjust approved displays or unrelated studies.
6. Screening data are synthetic and **not** the Bay of Fundy, FORCE or RM1 measurements. Restrict current model claims to export energy under an assumed fixed power curve. Electrical curtailment must never be treated as a blade load/thrust/fatigue model.
7. Maintain SI units and explicit timestamps and collection depth/coordinate metadata for measured data. Keep raw third-party datasets and large/binary material out of Git; use download instructions, license and checksum if obtained.
8. For Nova Scotia, preserve DFO adaptive environmental monitoring, marine-use, fisheries, Mi'kmaq knowledge/rights/engagement, federal and provincial permitting as decision gates. Avoid pretending this repository grants authorization.
9. `docs/CONTINUATION.md` is the authoritative next-work handoff: include checked remote SHA, actual test commands, the latest report, open PR, blocked resources, and top three actions. Don't claim to work outside the current session.
