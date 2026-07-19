# Engineering Assumptions

This document defines the assumptions used in the Sorek-inspired
Reverse Osmosis (RO), Pressure Exchanger (PX), and simplified
Zero Liquid Discharge (ZLD) Digital Twin.

The project is a system-level engineering simulation.

It is inspired by large-scale seawater desalination concepts associated
with plants such as Sorek 1 and Sorek 2, particularly high-pressure
reverse osmosis and pressure-energy recovery.

The model does not claim to reproduce the exact proprietary design,
operating data, or control systems of Sorek 1 or Sorek 2.

---

# 1. General Modeling Scope

The digital twin represents the following process chain:

Seawater Feed

→ High-Pressure Pump

→ Reverse Osmosis

→ Permeate + High-Pressure Brine

→ Pressure Exchanger

→ Simplified ZLD Treatment

→ Recovered Water + Concentrated Residue / Salt Load

The objective is to study interactions between:

- Feed-water conditions
- Pump operation
- RO performance
- Pressure-energy recovery
- Equipment degradation
- Brine treatment
- Water recovery
- Energy consumption
- Electricity cost

The model prioritizes system behavior and interaction between components
rather than detailed thermodynamic or chemical-process simulation.

---

# 2. Simulation Assumptions

The simulation uses a fixed discrete time step.

Default time step:

10 seconds

Each simulation tick assumes that component outputs can be calculated
from the current plant state.

The simulation is deterministic.

No random sensor noise, stochastic failures, or probabilistic disturbances
are currently included.

Equipment degradation evolves deterministically with operating time.

---

# 3. Feed-Water Assumptions

Feed-water flow is assumed constant within the current scenarios unless
explicitly changed by configuration.

Feed salinity is not constant.

The simulation applies a simplified sinusoidal 24-hour variation around
the scenario-specific base TDS.

Baseline reference:

38,000 mg/L

High-TDS scenario reference:

45,000 mg/L

The variation is a simulation assumption intended to create dynamic
operating conditions.

It is not claimed to represent measured Sorek seawater data.

---

# 4. Temperature Assumptions

Feed-water temperature is not constant.

The simulation applies a simplified sinusoidal daily temperature cycle
around the scenario-specific reference temperature.

Temperature affects calculated RO recovery through a simplified
temperature correction factor.

Detailed temperature-dependent membrane transport equations are outside
the scope of the current model.

---

# 5. Hydraulic Assumptions

The high-pressure pump provides the operating pressure required by the
simplified RO model.

Operating pressure is constrained between:

55 bar and 70 bar.

Pressure losses through:

- Pipelines
- Valves
- Pretreatment equipment
- Fittings
- RO pressure vessels

are not modeled separately.

The model therefore treats operating pressure as a simplified
system-level variable.

---

# 6. Pump Assumptions

The high-pressure pump has a nominal design efficiency.

Pump efficiency decreases as pump wear increases.

Pump wear increases gradually with operating time.

A minimum effective pump efficiency is imposed to prevent physically
invalid simulation values.

Pump power is calculated using a simplified proportional engineering
relationship involving:

- Feed flow
- Operating pressure
- Effective efficiency

The pump equation is not a fully unit-converted hydraulic pump model.

Therefore absolute power values should be interpreted as model outputs
for comparative scenario analysis unless full engineering unit
calibration is later introduced.

---

# 7. Reverse Osmosis Assumptions

The RO unit is modeled using simplified relationships rather than
detailed membrane transport equations.

RO recovery depends on:

- Operating pressure
- Feed TDS
- Feed temperature
- Membrane fouling

Reference design recovery:

50%

The simulation constrains calculated RO recovery between:

10% and 60%.

The controller attempts to maintain a target recovery.

Default target:

45%.

---

# 8. Salt Rejection Assumption

RO membrane salt rejection is assumed constant.

Current assumed salt rejection:

99.5%.

Permeate TDS is estimated from:

Feed TDS × (1 − Salt Rejection)

The model does not currently simulate changes in salt rejection caused by:

- Membrane age
- Membrane damage
- Specific ion chemistry
- Pressure-dependent rejection
- Temperature-dependent rejection

---

# 9. RO Water and Salt Balance

RO feed is separated into:

- Permeate
- Brine

Water balance:

Feed Flow = Permeate Flow + Brine Flow

Salt entering with feed is divided between:

- Small salt passage into permeate
- Remaining salt concentrated in brine

Brine TDS is estimated using this simplified salt mass balance.

Individual ions such as:

- Sodium
- Chloride
- Calcium
- Magnesium
- Sulfate

are not modeled separately.

TDS is treated as an aggregate dissolved-solids concentration.

---

# 10. Membrane Fouling Assumptions

RO membrane fouling increases gradually with operating time.

Fouling reduces effective membrane performance.

The fouling model is simplified and deterministic.

It does not separately model:

- Scaling
- Biofouling
- Organic fouling
- Colloidal fouling

These mechanisms are represented collectively through a single
fouling variable.

---

# 11. CIP Cleaning Assumption

Clean-In-Place (CIP) cleaning is represented using a simplified
threshold-based event.

When membrane fouling exceeds the configured model threshold,
a cleaning event is triggered.

The membrane is not restored to perfectly new condition.

Residual fouling remains after cleaning.

The model does not simulate:

- Cleaning chemicals
- Cleaning duration
- Cleaning water consumption
- Chemical cost
- Plant downtime during CIP

The CIP event represents simplified restoration of membrane performance.

---

# 12. Pressure Exchanger Assumptions

The Pressure Exchanger recovers hydraulic energy from high-pressure
RO brine.

PX efficiency is not constant over long operation.

The simulation models gradual PX efficiency degradation.

A minimum efficiency limit is imposed.

When the PX is disabled:

Recovered Power = 0

The brine itself is not removed.

It continues downstream toward the ZLD section.

The PX model is simplified and does not simulate detailed:

- Rotor dynamics
- Leakage
- Mixing
- Pressure losses
- Mechanical geometry

---

# 13. Sorek Inspiration

Sorek 1 and Sorek 2 form a central engineering inspiration for the project.

The project draws particularly from the broader concepts of:

- Large-scale seawater reverse osmosis
- High-pressure desalination
- Energy-efficiency requirements
- Pressure-energy recovery
- Modular plant operation

The project does not claim that Sorek 1 or Sorek 2 uses the exact equations,
parameters, scenarios, ZLD configuration, or software architecture
implemented in this digital twin.

The downstream ZLD extension is a project-specific modeling layer added
to study concentrated-brine management and higher overall water recovery.

---

# 14. ZLD Modeling Scope

The ZLD section is intentionally represented using a simplified
lumped system-level model.

The current simulation does not explicitly model individual industrial
ZLD equipment such as:

- Brine concentrators
- Multiple-effect evaporators
- Mechanical vapor recompression systems
- Crystallizer geometry
- Dryers
- Centrifuges

Instead, these downstream processes are represented collectively as a
simplified ZLD unit.

---

# 15. ZLD Water-Recovery Assumption

The baseline simplified ZLD water-recovery fraction is:

90% of the brine entering the ZLD section.

This value is configurable through scenario YAML files.

It is a modeling assumption.

It must not be presented as the exact recovery of Sorek 1, Sorek 2,
or every industrial ZLD facility.

---

# 16. ZLD Residual Liquid

The simplified ZLD model currently calculates:

ZLD Feed

=

Recovered ZLD Water

+

Residual Concentrated Liquid

Therefore the model approaches high overall water recovery but does not
mathematically force the residual liquid stream to exactly zero.

The term "Zero Liquid Discharge" describes the intended downstream
treatment concept.

A real complete ZLD system would further process concentrated residual
liquid through evaporation, crystallization, solids separation, and
associated handling systems.

The current model represents this final stage at a simplified system level.

---

# 17. Salt / Solid Residue Assumption

The model estimates the dissolved salt load entering the ZLD section
using:

- Brine flow
- Brine TDS

The variable named `zld_solid_residue` represents the estimated salt mass
available for eventual concentration and crystallization.

It does not mean that every kilogram of dissolved salt instantaneously
becomes dry crystalline solid during each simulation tick.

Detailed crystallization chemistry is outside the current model scope.

---

# 18. ZLD Energy Assumption

ZLD treatment is energy intensive.

The simulation therefore includes an explicit ZLD energy requirement.

Baseline assumed specific energy consumption:

20 kWh per m3 of brine treated.

This value is configurable.

It is used as a simplified engineering assumption for comparative
simulation.

It is not claimed to represent the exact specific energy consumption of:

- Sorek 1
- Sorek 2
- Every thermal ZLD system
- Every commercial crystallizer

Actual industrial ZLD energy demand depends strongly on process design,
feed concentration, thermal integration, evaporation technology, and
energy-recovery systems.

---

# 19. Total Plant Energy Assumption

The simulation distinguishes between:

1. Gross pump power
2. PX recovered power
3. RO/PX net power
4. ZLD power
5. Total plant power

RO/PX Net Power:

Pump Power − PX Recovered Power

Total Plant Power:

RO/PX Net Power + ZLD Power

This allows the simulation to demonstrate both:

- Energy savings produced by pressure recovery
- Additional energy required for downstream ZLD treatment

---

# 20. Electricity Price Assumptions

Electricity price is not constant.

The simulation uses a simplified time-of-use tariff.

Normal tariff:

8 currency units/kWh

Peak tariff:

12 currency units/kWh

Peak period:

18:00 to 22:00

The currency is intentionally treated as a configurable model unit unless
a specific tariff dataset and currency source are formally defined.

---

# 21. Economic Scope

The current economic model includes:

- RO/PX energy cost
- ZLD energy cost
- Total energy cost
- Economic value of PX energy recovery

The current model does not include:

- Capital expenditure
- Membrane replacement cost
- Pump replacement cost
- CIP chemical cost
- Labor
- Pretreatment chemicals
- Salt-product revenue
- Maintenance contracts
- Disposal cost
- Carbon pricing

Therefore `net_operating_cost` currently represents modeled energy-related
operating cost rather than the complete financial operating expenditure
of a real desalination facility.

---

# 22. PX Savings Accounting

PX recovered energy reduces RO net power.

Therefore the actual calculated electricity cost already includes the
benefit of the PX.

PX savings are also calculated separately as an informational metric to
show how much energy cost was avoided.

PX savings are not subtracted a second time from actual energy cost,
because doing so would double-count the same energy benefit.

---

# 23. Control-System Assumption

The project uses a simplified feedback controller.

The controller compares:

Actual RO Recovery

with:

Target RO Recovery.

If recovery is too low:

Operating pressure increases.

If recovery is too high:

Operating pressure decreases.

The controller uses fixed pressure increments.

It is not a full industrial:

- PID controller
- Model Predictive Controller
- SCADA control strategy

It represents the basic concept of closed-loop process control.

---

# 24. Equipment Degradation

The model includes simplified degradation for:

- Pump wear
- RO fouling
- PX efficiency

Degradation is deterministic and based primarily on operating time.

The current model does not include probabilistic failure distributions
or condition-based machine-learning prediction.

---

# 25. Scenario Assumptions

The project currently supports scenarios including:

- Baseline operation
- High feed TDS
- Aged assets
- PX failure

Scenarios modify initial conditions and operating configuration while
using the same simulation architecture.

This allows controlled comparison between different plant conditions.

---

# 26. Telemetry Assumptions

Simulation telemetry is written to InfluxDB.

Grafana is used to visualize time-series plant behavior.

The timestamps displayed in Grafana are virtual simulation timestamps
generated for visualization.

They should not be interpreted as live sensor timestamps from a physical
industrial plant.

---

# 27. Digital Twin Scope

The project is described as a Digital Twin simulation architecture because
it creates a structured virtual representation of plant:

- Process state
- Asset state
- Health state
- Economic state
- Simulation state

However, the current implementation primarily operates using simulated
data rather than continuous live sensor synchronization with a physical
plant.

Therefore, when presenting the project, it is most precise to describe it
as:

"A simulation-driven digital twin prototype of a Sorek-inspired RO,
pressure-energy recovery, and simplified ZLD desalination process."

---

# 28. Model Limitations

The following are intentionally outside the current project scope:

- Detailed pretreatment simulation
- Intake-system hydraulics
- Full membrane transport physics
- Individual ionic chemistry
- Detailed osmotic-pressure equations
- Pipeline hydraulic losses
- Full PID/MPC control
- Detailed evaporator thermodynamics
- Crystallizer thermodynamics
- Mineral-specific crystallization
- Real-time physical plant sensor integration
- Predictive-maintenance machine learning
- Full lifecycle economic analysis

These limitations are intentional.

The project focuses on demonstrating how multiple engineering subsystems
can interact within a modular digital twin architecture.

---

# 29. Core Engineering Interpretation

The project should be interpreted as:

Dynamic Seawater Conditions

→ High-Pressure Pump

→ Reverse Osmosis

→ Product Water + Concentrated Brine

→ Pressure-Energy Recovery

→ Simplified ZLD Treatment

→ Additional Water Recovery + Concentrated Salt/Residue

while simultaneously modeling:

- Equipment degradation
- Closed-loop pressure adjustment
- Energy consumption
- Electricity cost
- Scenario disturbances
- Telemetry
- Visualization

This provides a coherent system-level representation of an advanced
desalination and brine-management process.