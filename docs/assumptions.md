# Assumptions

The digital twin is based on the following engineering assumptions:

## Process Assumptions

- The plant operates under steady-state conditions during each simulation tick.
- Feed water properties remain constant within a scenario.
- Reverse Osmosis recovery is calculated using simplified engineering equations.
- Pressure losses in connecting pipelines are neglected.
- Temperature effects are not considered.

---

## Equipment Assumptions

### High Pressure Pump

- Pump efficiency decreases with wear.
- Pump degradation occurs gradually over time.
- Pump operates within its rated pressure range.

### Reverse Osmosis Membrane

- Fouling increases slowly with operating time.
- Membrane rejection remains constant.
- Cleaning cycles are not simulated.

### Pressure Exchanger (PX)

- PX efficiency remains constant within a scenario.
- Mechanical losses are represented by an efficiency coefficient.

---

## Economic Assumptions

- Electricity price is constant.
- Maintenance cost is not included.
- Energy savings are calculated using PX efficiency.

---

## Simulation Assumptions

- Fixed simulation time step.
- Deterministic simulation.
- No random disturbances.
- No sensor noise.
