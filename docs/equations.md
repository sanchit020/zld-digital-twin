# Engineering Equations

## 1. High-Pressure Pump

### Effective Pump Efficiency

\[
\eta_{effective}=\eta_{design}\times(1-\text{Pump Wear})
\]

\[
\eta_{effective}\ge0.50
\]

### Pump Power

\[
P_{pump}=\frac{Q_{feed}\times P_{operating}}{\eta_{effective}}
\]

---

# 2. Reverse Osmosis

### Pressure Factor

\[
Pressure\ Factor=\frac{Pump\ Pressure}{60}
\]

### TDS Factor

\[
TDS\ Factor=\frac{Feed\ TDS}{38000}
\]

### Temperature Factor

\[
Temperature\ Factor=1+\left((Feed\ Temperature-25)\times0.01\right)
\]

### Fouling Factor

\[
Fouling\ Factor=1-RO\ Fouling
\]

### RO Recovery

\[
Recovery=
Design\ Recovery
\times Pressure\ Factor
\times Temperature\ Factor
\times Fouling\ Factor
\div TDS\ Factor
\]

\[
0.10\le Recovery\le0.60
\]

\[
RO\ Recovery(\%)=Recovery\times100
\]

### Permeate Flow

\[
Q_{permeate}=Q_{feed}\times Recovery
\]

### Brine Flow

\[
Q_{brine}=Q_{feed}-Q_{permeate}
\]

### RO Water Balance

\[
Q_{feed}=Q_{permeate}+Q_{brine}
\]

---

# 3. Salt Balance

### Permeate TDS

\[
Permeate\ TDS=Feed\ TDS\times(1-Salt\ Rejection)
\]

### Feed Salt Load

\[
Feed\ Salt=Q_{feed}\times Feed\ TDS
\]

### Permeate Salt Load

\[
Permeate\ Salt=Q_{permeate}\times Permeate\ TDS
\]

### Brine Salt Load

\[
Brine\ Salt=Feed\ Salt-Permeate\ Salt
\]

### Brine TDS

\[
Brine\ TDS=\frac{Brine\ Salt}{Q_{brine}}
\]

---

# 4. RO Membrane Fouling

\[
RO\ Fouling_{new}
=
RO\ Fouling_{old}
+
(Fouling\ Rate\times\Delta t)
\]

\[
RO\ Fouling>0.35
\]

\[
RO\ Fouling=0.05
\]

---

# 5. Pump Wear

\[
Pump\ Wear_{new}
=
Pump\ Wear_{old}
+
(Wear\ Rate\times\Delta t)
\]

\[
Pump\ Wear\le0.30
\]

---

# 6. Pressure Exchanger

### Pressure Factor

\[
PX\ Pressure\ Factor=\frac{Brine\ Pressure}{60}
\]

### PX Recovered Power

\[
P_{PX}
=
Q_{brine}
\times
P_{brine}
\times
PX\ Pressure\ Factor
\times
\eta_{PX}
\]

### PX Efficiency

\[
PX\ Efficiency_{new}
=
PX\ Efficiency_{old}
-
(Degradation\ Rate\times\Delta t)
\]

\[
PX\ Efficiency\ge0.80
\]

### RO Net Power

\[
P_{RO,net}=P_{pump}-P_{PX}
\]

\[
P_{RO,net}\ge0
\]

If PX is disabled:

\[
P_{PX}=0
\]

\[
P_{RO,net}=P_{pump}
\]

---

# 7. Zero Liquid Discharge

### Brine to ZLD

\[
Q_{ZLD,feed}=Q_{brine}
\]

### Water Recovery

\[
Q_{ZLD,recovered}
=
Q_{ZLD,feed}
\times
R_{ZLD}
\]

### Residual Liquid

\[
Q_{ZLD,residual}
=
Q_{ZLD,feed}
-
Q_{ZLD,recovered}
\]

### ZLD Water Balance

\[
Q_{ZLD,feed}
=
Q_{ZLD,recovered}
+
Q_{ZLD,residual}
\]

---

# 8. Salt Load

\[
Salt\ Load
=
\frac{Q_{brine}\times Brine\ TDS}{1000}
\]

---

# 9. ZLD Power

\[
P_{ZLD}
=
Q_{ZLD,feed}
\times
SEC_{ZLD}
\]

---

# 10. ZLD Energy

\[
E_{ZLD}
=
P_{ZLD}
\times
\Delta t
\]

---

# 11. Total Water Recovery

\[
Q_{total}
=
Q_{permeate}
+
Q_{ZLD,recovered}
\]

### Overall Recovery

\[
Overall\ Recovery(\%)
=
\frac{Q_{total}}{Q_{feed}}
\times100
\]

---

# 12. Overall Water Balance

\[
Q_{feed}
=
Q_{permeate}
+
Q_{ZLD,recovered}
+
Q_{ZLD,residual}
\]

---

# 13. Total Plant Power

\[
P_{RO,net}
=
P_{pump}
-
P_{PX}
\]

\[
P_{total}
=
P_{RO,net}
+
P_{ZLD}
\]

---

# 14. Plant Energy

### RO Energy

\[
E_{RO}
=
P_{RO,net}
\times
\Delta t
\]

### ZLD Energy

\[
E_{ZLD}
=
P_{ZLD}
\times
\Delta t
\]

### Total Energy

\[
E_{total}
=
E_{RO}
+
E_{ZLD}
\]

---

# 15. Electricity Tariff

Normal:

\[
Price=8
\]

Peak:

\[
18:00\le Time<22:00
\]

\[
Price=12
\]

---

# 16. RO Energy Cost

\[
RO\ Cost
=
E_{RO}
\times
Price
\]

---

# 17. ZLD Energy Cost

\[
ZLD\ Cost
=
E_{ZLD}
\times
Price
\]

---

# 18. Total Energy Cost

\[
Total\ Cost
=
E_{total}
\times
Price
\]

---

# 19. PX Savings

### Energy Saved

\[
Energy_{saved}
=
P_{PX}
\times
\Delta t
\]

### Economic Savings

\[
PX\ Savings
=
Energy_{saved}
\times
Price
\]

---

# 20. Net Operating Cost

\[
Net\ Operating\ Cost
=
Cumulative\ Energy\ Cost
\]

---

# 21. Simulation Time

\[
\Delta t=\frac{10}{3600}
\]

\[
Runtime_{new}
=
Runtime_{old}
+
\Delta t
\]

---

# 22. Dynamic Feed Conditions

### Feed TDS

\[
Feed\ TDS
=
Base\ TDS
+
3000
\times
\sin\left(\frac{2\pi\times Hour}{24}\right)
\]

### Feed Temperature

\[
Feed\ Temperature
=
Base\ Temperature
+
3
\times
\sin\left(\frac{2\pi(Hour-6)}{24}\right)
\]

---

# 23. Pressure Control

If

\[
Recovery_{actual}<Recovery_{target}
\]

\[
Pressure=Pressure+0.5
\]

If

\[
Recovery_{actual}>Recovery_{target}
\]

\[
Pressure=Pressure-0.5
\]

\[
55\le Pressure\le70
\]

---

# 24. Simulation Sequence

```
Dynamic Feed Conditions
        ↓
Pressure Controller
        ↓
Pump
        ↓
Reverse Osmosis
        ↓
Pressure Exchanger
        ↓
RO Net Power
        ↓
Zero Liquid Discharge
        ↓
Total Water Recovery
        ↓
Total Plant Power
        ↓
Energy Cost & PX Savings
        ↓
Telemetry Storage
```