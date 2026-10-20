# Secondary system-integration research: AI computing loads

**Separate workstream; not part of SCREEN-001 turbine validation.** Tidal generation is predictable but intermittent at slack flow; a tidal-only always-on data centre is not demonstrated. Cooling and generation have different environmental constraints.

Required model (future): hourly measured/validated tidal export + hourly computing workload and flexible deferral, complementary wind/solar/grid, grid carbon intensity and outages, battery efficiency and degradation. Enforce `SOC_(t+1) = SOC_t + eta_charge*charge_kWh - discharge_kWh/eta_discharge`, `0<=SOC<=E_max`, independent charge/discharge power constraints, and initial/final SOC parity. Include unsupplied energy rather than silently filling demand.

Seawater cooling requires heat-exchanger separation from IT loops, pump power, material/corrosion qualification, intake/entrainment/impingement, discharge thermal plume and permits. Add coastal flooding, storms, biofouling, thermal recovery feasibility and lifetime embedded emissions.

Do not claim zero emissions, continuous green power, zero intake impact, or financial advantage without site, grid and environmental evidence. Begin **after** RM1 physical benchmark reproduction; register any measured demand/source datasets with license and quality metadata.
