# Engineering Specification

## 1. Project Title

Sorek-Inspired Reverse Osmosis and Zero Liquid Discharge Digital Twin

---

## 2. Objective

The objective of this project is to develop a modular, simulation-driven
Digital Twin prototype for an advanced seawater desalination process.

The system combines:

- High-pressure pumping
- Reverse Osmosis (RO)
- Pressure Exchanger (PX) energy recovery
- Simplified Zero Liquid Discharge (ZLD) treatment
- Equipment degradation
- Closed-loop operating-pressure control
- Energy and economic analysis
- Scenario-based simulation
- Time-series telemetry
- Real-time dashboard visualization

The project is inspired by large-scale seawater desalination concepts
associated with Sorek 1 and Sorek 2, particularly the use of efficient
seawater reverse osmosis and pressure-energy recovery.

The ZLD section is a simplified project-specific downstream extension
used to study brine management, additional water recovery, salt loading,
and the energy trade-off associated with high water recovery.

---

# 3. Complete Process Architecture

The simulated process is:

Seawater Feed

↓

High-Pressure Pump

↓

Reverse Osmosis

↙                         ↘

Permeate Water       High-Pressure Brine

                           ↓

                  Pressure Exchanger

                           ↓

                 Pressure Energy Recovery

                           ↓

                Depressurized RO Brine

                           ↓

                 Simplified ZLD Unit

                    ↙             ↘

             Recovered Water    Concentrated
                                Residue /
                                Salt Load

The digital simulation architecture surrounding this process is:

Scenario YAML

↓

Scenario Runner

↓

Plant State

↓

Simulation Kernel

↓

Pump → RO → PX → ZLD

↓

Engineering and Economic Calculations

↓

InfluxDB

↓

Grafana

---

# 4. Central Engineering Theme

The central engineering theme combines two ideas.

## 4.1 Sorek-Inspired Desalination

Sorek 1 and Sorek 2 provide the conceptual inspiration for:

- Large-scale seawater desalination
- High-pressure reverse osmosis
- Energy-efficient plant operation
- Pressure-energy recovery
- Modular process thinking

The project does not reproduce proprietary Sorek plant designs or
operating parameters.

---

## 4.2 Zero Liquid Discharge

Traditional RO produces:

- Product water
- Concentrated reject brine

The project extends the RO/PX process by routing the concentrated brine
to a simplified ZLD stage.

The ZLD model estimates:

- Brine requiring treatment
- Additional recovered water
- Remaining concentrated liquid
- Salt load available for eventual crystallization
- Additional ZLD energy demand

This allows the project to study the trade-off between:

Higher water recovery

and

Higher energy consumption.

---

# 5. State Architecture

The complete plant condition is represented by `PlantState`.

`PlantState` acts as the central state container and contains:

- ProcessState
- AssetState
- HealthState
- EconomicState
- SimulationState

This separation prevents process variables, equipment outputs,
degradation variables, economics, and simulation timing from being
mixed together.

---

# 6. ProcessState

## Responsibility

Represents the physical process conditions and water-flow state.

## Inputs / Variables

- Feed flow
- Feed TDS
- Feed temperature
- Operating pressure
- Target RO recovery

## RO Outputs

- Permeate flow
- Brine flow

## ZLD Process Outputs

- ZLD feed flow
- ZLD recovered water
- ZLD residual liquid

## Complete Plant Outputs

- Total recovered water
- Overall water recovery

---

# 7. AssetState

## Responsibility

Stores calculated outputs and operating conditions associated with
individual plant assets.

## Pump Variables

- Pump pressure
- Pump power
- Pump efficiency

## RO Variables

- RO recovery
- RO permeate flow
- RO brine flow
- Required pressure indicator
- Permeate TDS
- Brine TDS

## PX Variables

- PX recovered power
- PX efficiency
- PX enabled/disabled state

## ZLD Variables

- Brine sent to ZLD
- ZLD recovered water
- ZLD residual liquid
- ZLD recovery
- Salt/solid residue equivalent
- ZLD power
- ZLD energy consumption

## Plant Energy Variables

- RO/PX net power
- Total plant power

---

# 8. HealthState

## Responsibility

Represents equipment degradation.

## Variables

- Pump wear
- RO membrane fouling
- PX efficiency

These values evolve during simulation and influence plant performance.

---

# 9. EconomicState

## Responsibility

Tracks energy-related operating economics.

## Variables

- Current energy cost
- RO energy cost
- ZLD energy cost
- Cumulative energy cost
- Cumulative RO energy cost
- Cumulative ZLD energy cost
- PX savings
- Cumulative PX savings
- Net operating cost
- Current electricity price

The current economic model represents energy-related operating cost,
not complete industrial OPEX.

---

# 10. SimulationState

## Responsibility

Tracks simulation progression.

## Variables

- Simulation tick
- Runtime hours

The default simulation time step is:

10 seconds.

---

# 11. High-Pressure Pump Model

## Responsibility

The pump raises seawater pressure to the operating pressure required
for reverse osmosis.

## Inputs

- Feed flow
- Operating pressure
- Pump wear

## Calculations

The model calculates:

- Effective pump efficiency
- Pump power
- Pump pressure

## Degradation

Pump wear increases gradually with operating time.

Increasing wear reduces effective efficiency.

## Outputs

- Pump pressure
- Pump power
- Pump efficiency
- Pump wear

---

# 12. Reverse Osmosis Model

## Responsibility

The RO unit separates seawater into:

- Low-TDS permeate
- Concentrated brine

## Inputs

- Feed flow
- Feed TDS
- Feed temperature
- Pump pressure
- Membrane fouling

## Performance Factors

RO recovery responds to:

- Pressure
- Salinity
- Temperature
- Fouling

## Calculations

The RO model calculates:

- Recovery
- Permeate flow
- Brine flow
- Permeate TDS
- Brine TDS
- Required pressure indicator

## Outputs

- RO recovery
- Product-water flow
- Concentrated brine flow
- Permeate quality estimate
- Brine concentration estimate

---

# 13. RO Water Balance

The RO model maintains:

Feed Flow

=

Permeate Flow

+

Brine Flow

A validation function calculates the numerical balance error.

---

# 14. RO Salt Balance

The model estimates salt distribution between permeate and brine.

Feed Salt Load

=

Permeate Salt Load

+

Brine Salt Load

Most dissolved salt remains in the brine because the membrane uses a
high assumed salt-rejection value.

The calculated brine salt load is used to estimate brine TDS.

---

# 15. Membrane Fouling

RO membrane fouling increases with operating time.

Fouling reduces membrane performance and therefore affects recovery.

When fouling exceeds the defined threshold, a simplified
Clean-In-Place event is triggered.

The cleaning event reduces fouling but does not restore the membrane
to a perfectly new state.

---

# 16. Closed-Loop Pressure Controller

The simulation includes simplified feedback control.

The controller compares:

Actual RO Recovery

with

Target RO Recovery.

If recovery is below target:

Operating pressure increases.

If recovery is above target:

Operating pressure decreases.

Operating pressure is constrained between:

55 bar and 70 bar.

This represents simplified feedback control rather than a full
industrial PID or Model Predictive Controller.

---

# 17. Pressure Exchanger Model

## Responsibility

The Pressure Exchanger recovers hydraulic energy from high-pressure
RO brine.

## Inputs

- RO brine flow
- Brine pressure
- PX efficiency
- PX enabled/disabled status

## Calculations

The model estimates:

- Recovered hydraulic power
- PX efficiency degradation

## Outputs

- PX recovered power
- PX efficiency
- PX energy savings

If the PX is disabled:

Recovered Power = 0.

The brine continues downstream to ZLD.

---

# 18. RO/PX Net Power

The energy-recovery relationship is:

RO/PX Net Power

=

Pump Power

−

PX Recovered Power

This metric represents the actual modeled power requirement of the
RO pressurization section after pressure-energy recovery.

---

# 19. Simplified ZLD Model

## Responsibility

The ZLD unit receives concentrated RO brine after the PX stage.

The model represents downstream brine concentration and water recovery
using a simplified lumped process.

## Inputs

- RO brine flow
- Brine TDS
- ZLD enabled/disabled status
- ZLD water-recovery assumption
- ZLD specific-energy assumption

## Calculations

The model calculates:

- Brine sent to ZLD
- Recovered ZLD water
- Residual concentrated liquid
- Salt load / solid residue equivalent
- ZLD recovery percentage
- ZLD power
- ZLD energy consumption

## Outputs

- Additional recovered water
- Residual concentrate
- Estimated salt load
- ZLD energy demand

---

# 20. ZLD Scope Limitation

The ZLD model does not explicitly simulate:

- Individual evaporators
- Mechanical vapor recompression
- Multiple-effect evaporation
- Crystallizer thermodynamics
- Crystal nucleation
- Mineral-specific chemistry
- Drying
- Centrifugation

These operations are represented collectively by a simplified
system-level ZLD model.

The model should therefore not be described as a detailed thermal
crystallizer simulator.

---

# 21. ZLD Water Balance

The simplified ZLD balance is:

Brine Entering ZLD

=

Recovered ZLD Water

+

Residual Concentrated Liquid

This balance is validated separately from the RO water balance.

---

# 22. Overall Plant Water Balance

The complete simplified plant balance is:

Feed Water

=

RO Permeate

+

ZLD Recovered Water

+

Residual Concentrated Liquid

Solid salt mass is handled separately because mass and volumetric flow
must not be directly mixed.

---

# 23. Overall Water Recovery

Total recovered water is:

RO Permeate

+

ZLD Recovered Water

Overall Water Recovery (%) is:

Total Recovered Water
/
Original Feed Flow
×
100

This demonstrates the increase in modeled water utilization produced
by downstream brine treatment.

---

# 24. Salt / Residue Estimation

The ZLD model estimates dissolved salt load from:

- Brine flow
- Brine TDS

The resulting `zld_solid_residue` metric represents salt mass available
for eventual concentration and crystallization.

It does not represent detailed instantaneous crystal production.

---

# 25. ZLD Energy Model

The simplified ZLD power demand is based on:

Brine Flow

×

Specific ZLD Energy Consumption

The baseline scenario uses a configurable assumption of:

20 kWh/m³ of brine treated.

This is a project modeling assumption and not an exact value attributed
to Sorek 1 or Sorek 2.

---

# 26. Total Plant Power

The complete modeled plant power is:

Total Plant Power

=

RO/PX Net Power

+

ZLD Power

This makes the engineering trade-off visible:

PX reduces desalination energy demand.

ZLD increases energy demand while recovering additional water.

---

# 27. Dynamic Feed Conditions

The simulation includes dynamic seawater conditions.

## Feed TDS

TDS varies over a simplified 24-hour sinusoidal cycle around the
scenario-specific base salinity.

Examples:

Baseline:

38,000 mg/L reference.

High-TDS:

45,000 mg/L reference.

## Feed Temperature

Temperature also varies over a simplified daily cycle.

These dynamic conditions influence RO performance.

---

# 28. Electricity Tariff

The model uses simplified time-of-use electricity pricing.

Normal tariff:

8 currency units/kWh.

Peak tariff:

12 currency units/kWh.

Peak period:

18:00 to 22:00.

This allows plant operating cost to vary with simulation time.

---

# 29. Economic Model

The model separately calculates:

- RO/PX energy use
- ZLD energy use
- RO energy cost
- ZLD energy cost
- Total actual energy cost
- PX energy savings

PX savings are shown separately as the economic value of recovered
hydraulic energy.

They are not subtracted twice from actual electricity cost.

---

# 30. Scenario System

Plant operating conditions are configured using YAML scenario files.

Current main scenarios are:

## Baseline

Represents normal reference operation with:

- Healthy equipment
- Normal seawater TDS
- Active PX
- Active ZLD

## High TDS

Represents elevated feed salinity.

Used to study:

- RO performance
- Pressure response
- Brine concentration
- ZLD salt loading
- Energy effects

## Aged Assets

Starts the simulation with:

- Pump wear
- Membrane fouling
- Reduced PX efficiency

Used to study degradation effects.

## PX Failure

Disables pressure-energy recovery.

Used to demonstrate:

- Increased RO net power
- Loss of PX savings
- Continued downstream brine treatment

---

# 31. Scenario Loader

The Scenario Loader reads YAML configuration files.

Scenario configuration defines values including:

- Feed conditions
- Operating targets
- Initial asset conditions
- Equipment health
- PX status
- ZLD configuration

This separates operating configuration from simulation code.

---

# 32. Scenario Runner

The Scenario Runner:

1. Loads the selected YAML scenario.
2. Creates the initial PlantState.
3. Creates the SimulationKernel.
4. Creates the SimulationClock.
5. Executes simulation ticks.
6. Writes telemetry to InfluxDB.
7. Prints periodic engineering summaries.
8. Returns the final plant state.

---

# 33. Simulation Kernel

The Simulation Kernel is the central execution engine.

Each simulation step follows approximately:

1. Determine simulation time.
2. Update dynamic feed TDS.
3. Update feed temperature.
4. Compare RO recovery with target.
5. Adjust operating pressure.
6. Update high-pressure pump.
7. Update RO.
8. Update PX.
9. Calculate RO/PX net power.
10. Update ZLD.
11. Calculate total plant power.
12. Calculate energy consumption.
13. Apply electricity tariff.
14. Calculate RO and ZLD energy costs.
15. Calculate PX savings.
16. Update cumulative economics.
17. Advance simulation time.
18. Produce periodic engineering output.

---

# 34. Simulation Clock

The simulation uses a fixed time step.

Default:

10 seconds per tick.

The clock converts seconds into hours because degradation, energy,
and economic equations use time expressed in hours.

---

# 35. Validation

The project validates water conservation at multiple levels.

## RO Balance

Feed

=

Permeate + Brine

## ZLD Balance

ZLD Feed

=

Recovered ZLD Water + Residual Liquid

## Overall Balance

Feed

=

RO Permeate
+
ZLD Recovered Water
+
Residual Liquid

Validation outputs numerical balance errors.

Values close to zero indicate correct flow conservation.

---

# 36. Telemetry Storage

Simulation telemetry is written to InfluxDB.

Stored metrics include:

## Feed / Process

- Feed flow
- Feed TDS
- Feed temperature
- Operating pressure

## Pump

- Pump pressure
- Pump power
- Pump efficiency
- Pump wear

## RO

- RO recovery
- Permeate flow
- Brine flow
- Permeate TDS
- Brine TDS
- RO required pressure
- RO fouling

## PX

- PX recovered power
- PX efficiency
- PX status

## ZLD

- Brine sent to ZLD
- ZLD recovered water
- ZLD residual liquid
- ZLD recovery
- Salt/residue estimate
- ZLD power
- ZLD energy

## Complete Plant

- Total recovered water
- Overall water recovery
- RO/PX net power
- Total plant power

## Economics

- RO energy cost
- ZLD energy cost
- Total energy cost
- PX savings
- Net operating cost

## Simulation

- Tick
- Runtime hours

---

# 37. Visualization

Grafana is used as the visualization layer.

Existing and planned dashboard panels represent:

- Pump Power
- Pump Wear
- RO Recovery
- RO Fouling
- PX Efficiency
- PX Savings
- RO/PX Net Power
- Feed TDS
- Feed Temperature
- Operating Pressure
- Brine TDS
- Brine to ZLD
- ZLD Water Recovery
- Salt/Residue Production
- ZLD Power
- Total Plant Power
- Overall Water Recovery
- Energy Cost

Grafana therefore provides a time-series view of the simulated
digital plant.

---

# 38. Software Architecture

The project follows a modular architecture.

Typical structure:

twin/

    assets/
        base_asset.py
        pump.py
        ro.py
        px.py
        zld.py

    state/
        plant_state.py
        process_state.py
        asset_state.py
        health_state.py
        economic_state.py
        simulation_state.py

    kernel/
        simulation_kernel.py
        clock.py

    scenarios/
        scenario_loader.py
        scenario_runner.py

    configs/
        baseline.yaml
        high_tds.yaml
        aged_assets.yaml
        px_failure.yaml

    validation/
        water_balance.py

    storage/
        influx_writer.py

docs/

    engineering_specification.md
    equations.md
    assumptions.md

---

# 39. Design Principles

The software architecture follows several principles.

## Modularity

Each physical asset has its own model.

## Separation of State

Process, asset, health, economics, and simulation information are
stored separately.

## Scenario Configurability

Operating conditions are defined outside the simulation code using YAML.

## Deterministic Simulation

The same scenario and initial conditions produce repeatable results.

## Observability

Important variables are written to time-series storage and visualized.

## Extensibility

Future assets or models can be added without redesigning the complete
simulation architecture.

---

# 40. Technology Stack

## Python

Used for:

- Simulation logic
- Asset models
- State management
- Engineering calculations
- Scenario execution

## Python Dataclasses

Used to structure simulation state.

## YAML

Used for human-readable scenario configuration.

## InfluxDB

Used for time-series telemetry storage.

## Grafana

Used for dashboard visualization and engineering monitoring.

---

# 41. Digital Twin Interpretation

The project creates a structured virtual representation of:

- Physical process behavior
- Equipment behavior
- Equipment health
- Energy behavior
- Economic behavior
- Time evolution

The current system is simulation-driven.

It does not currently receive continuous sensor data from a physical
desalination facility.

The technically precise description is:

A simulation-driven Digital Twin prototype for a Sorek-inspired
seawater RO, pressure-energy recovery, and simplified ZLD process.

---

# 42. Complete Engineering Story

The final project can be summarized as:

Seawater enters the simulated plant.

↓

Dynamic salinity and temperature affect operating conditions.

↓

The high-pressure pump supplies the pressure required for RO.

↓

RO produces low-salinity permeate and concentrated high-pressure brine.

↓

Membrane fouling gradually affects RO performance.

↓

A feedback controller adjusts pressure to maintain target recovery.

↓

The high-pressure brine passes through a Pressure Exchanger.

↓

The PX recovers hydraulic energy, reducing RO net power demand.

↓

The concentrated brine then enters a simplified ZLD stage.

↓

Additional water is recovered.

↓

The remaining stream becomes highly concentrated, and its salt load is
estimated for eventual crystallization/solid handling.

↓

ZLD requires additional energy.

↓

The model calculates the trade-off between water recovery and energy use.

↓

Pump wear, RO fouling, and PX degradation evolve over time.

↓

Different scenarios test salinity disturbances, aging, and PX failure.

↓

All important telemetry is stored in InfluxDB.

↓

Grafana visualizes the behavior of the virtual plant.

This creates one connected engineering system:

Sorek-inspired efficient seawater desalination

+

Pressure-energy recovery

+

Simplified Zero Liquid Discharge

+

Digital Twin simulation and monitoring.