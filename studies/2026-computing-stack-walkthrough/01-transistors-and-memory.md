# 01 — Transistors and Memory

## From continuous voltage to a reliable bit

Real voltage is continuous. Digital systems interpret ranges as logical states and design circuits with enough noise margin to restore imperfect signals.

A MOS transistor acts as a controllable conduction path. CMOS combines complementary NMOS and PMOS devices so that stable logical states consume little static power and transitions produce restored outputs.

The CMOS inverter is the first complete example:

```text
input low  → output high
input high → output low
```

From inverters and NAND gates, circuits construct Boolean logic. NAND is functionally complete: combinations of NAND gates can express every Boolean function.

## Combinational and sequential circuits

Combinational logic maps current inputs to outputs:

```text
output = F(inputs)
```

Examples include adders, multiplexers, decoders, and comparators.

Sequential logic includes stored state:

```text
next state = F(current state, inputs)
```

Feedback between gates can preserve one bit. Latches and flip-flops control when that state may change, giving larger systems stable registers and clocked transitions.

## Memory cells

### SRAM

A typical SRAM cell uses a small feedback circuit to maintain a bit while power remains. It is fast and area-intensive, making it suitable for registers and caches.

### DRAM

A DRAM cell stores charge in a capacitor selected by a transistor. Charge leaks, reads disturb the cell, and rows require refresh. DRAM offers greater density and forms system memory and HBM.

### Flash

Flash stores charge in transistor structures that retain state without continuous power. Multiple charge levels can encode more than one bit, trading endurance and sensing margin for density.

## Memory hierarchy

The technologies form a hierarchy because each occupies a different point in the trade space:

```text
latency
capacity
bandwidth
energy
persistence
density
price
```

Registers are close and scarce. Caches are fast and managed automatically. DRAM and HBM provide large active state. SSD and remote storage provide durable backing state.

## Energy and precision

Dynamic switching power is commonly approximated by:

```text
activity × capacitance × voltage² × frequency
```

Lower precision reduces storage, movement, and often arithmetic cost. This is why AI systems use formats such as BF16, FP8, INT8, and lower-bit weight representations when the numerical error remains acceptable.

## Recovery already exists in hardware

Physical systems experience bit errors, leakage, timing faults, and component failure. ECC, refresh, retry, redundancy, and fault isolation turn those imperfections into manageable signals.

The later Agent principle—errors should become recovery information—has a deep precedent in physical computing.

## Anchors

- Logic and memory are both arrangements of stateful circuits.
- A bit is a robust interpretation of a physical state range.
- Persistence has a physical mechanism and cost.
- Memory systems are layered because no medium optimizes every property.
