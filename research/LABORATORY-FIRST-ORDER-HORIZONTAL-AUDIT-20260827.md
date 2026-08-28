# Ordivon Laboratory — First-Order Whole-Order Horizontal Audit v0.1

Date: 2026-08-27
Status: **HORIZONTAL AUDIT COMPLETE / FIRST-ORDER BOUNDARY CONTRACTED**
Input head: `6494399c6d207049cf796eaf923505345338294a` (`research: close first-order facility layer`)

## 0. Why this pass exists

The vertical item-by-item pass is complete. The remaining question is not `what else belongs in a laboratory?` but whether the order works as one capability portfolio.

Audit dimensions:

```text
overlap / redundancy
missing persistent capability
currentness / representation drift
first-order vs JIT placement
budget arithmetic
checkout / receipt gates
```

No category is admitted merely because a conventional bench would contain it.

## 1. High-value overlap audit

### SDS824X HD + AD3 Pro Bundle

**KEEP BOTH.** The overlap is useful rather than wasteful. AD3 supplies Agent-native stimulus/orchestration and compact mixed-signal I/O; SDS824X HD supplies an independent common-timebase waveform observer. Deleting the scope collapses stimulus and observation toward one software/device path; deleting AD3 recreates separate AWG/logic/pattern purchases or Human orchestration.

### SDM3055X-E + UT61E+

**KEEP BOTH.** The bench DMM is programmable repeated metrology; the handheld is a cheap battery/manual failure path for continuity/static checks and cross-checking shared software/configuration failures.

### SPD4323X self-readback + independent observers

**KEEP THE INDEPENDENT OBSERVERS.** PSU telemetry is actuator state/readback, not independent physical evidence.

### Four same-SKU controllers

**KEEP ×4.** At current carrying cost the pool creates explicit generation replacement, parallel fixture capacity and an immediate spare/destructive carrier. This redundancy is itself consumed by E0-D/currentness experiments.

Result:

```text
major electrical deletion count = 0
reason = complementary responsibility + independent evidence + replacement semantics
```

## 2. Lower-cost overlap contraction

Several support purchases remain conditional on what exact instruments already include.

```text
AD3 Pro bundle included probes/grabbers
→ do not buy duplicate accessory bundles; only close missing binding geometries.

SDS scope probes included
→ buy only short BNC patch / grabber paths that the frozen E0 topology consumes.

NANCH precision driver
!= full-size PH1/PH2 / flat drivers
→ precision and higher-torque roles remain separate.

PCB holder
!= small soft-jaw vise
→ board-safe flat work vs wire/connector/light mechanics.

heat gun
!= SMD hot-air rework station
→ conditional process heat stays narrow.
```

No large accessory ecosystem survives merely for completeness.

## 3. Missing-capability audit

One first-order residual survives.

### Operator eye protection — ADMIT, site-inventory/spec gated

Current work includes hand soldering and lead/wire cutting. NIOSH solder-station guidance requires eye protection, and CCOHS wire-cutter guidance calls for safety glasses/goggles/face protection when flying wire/particles are possible. Current China national standard `GB 14866-2023 眼面防护具通用技术规范` is in force from 2025-01-01.

First-order boundary:

```text
IF a current/fit clear impact eye protector with side protection already exists
→ reuse after receipt.
ELSE
→ acquire at least one operator-fit clear side-protection eye protector
   meeting GB 14866-2023 or a recognized equivalent current standard.
```

This is not a generic PPE collection. No welding shade, face shield, chemical splash goggle, laser eyewear or respirator is promoted without the corresponding hazard. Source capture and hazard reduction remain upstream controls.

No other persistent missing first-order capability survived. E0 manual all-energy removal can be realized by the reachable bounded source output-off / low-voltage disconnect already required by F02; a dedicated E-stop remains unearned at E0 risk.

Public evidence:

- Raspberry Pi Pico naming: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html
- Raspberry Pi SC1632 product portal: https://pip.raspberrypi.com/categories/1264-raspberry-pi-pico-2-h
- China GB 14866-2023 current standard: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=AA239F6971526695D122CEFF9F3FA301
- NIOSH soldering-station guide: https://www.cdc.gov/niosh/docs/2004-101/pdfs/Safe.pdf
- CCOHS pliers/wire-cutter guidance: https://www.ccohs.ca/oshanswers/safety_haz/hand_tools/pliers.html

## 4. Currentness / representation audit

### Pico

Canonical name is now:

```text
Raspberry Pi Pico 2 with headers
SKU SC1632
```

Raspberry Pi explicitly states that Pico 2 header variants do **not** shorten `with headers` to `H`. Distributor commerce text may still say `Pico 2 H`; it is not canonical owner naming. Historical product-audit prose may retain what the distributor page displayed, but active purchase surfaces use manufacturer naming.

### SATA metric hex set

The earlier surfaces disagreed between 09105/09105A and a later 09101 preference. Current JD results show both long and extra-long 9-piece families remain available. Because this is a low-cost hand tool and the load-bearing requirement is:

```text
metric 1.5–10 mm
9-piece
ball-end
current authorized/self-operated supply
geometry fit for bench/fixture reach
```

the exact 0910x suffix is checkout state, not a semantic commitment. Use 09105/09105A for ordinary long reach; pay for 09101/09101A extra-long only when geometry/current price makes that useful.

### QUICK 6601 / 6611

All active first-order surfaces now classify them as:

```text
HISTORICAL_FALLBACK
NOT_FIRST_ORDER
```

Their old comparison remains legitimate historical evidence if site topology changes. It is not an active branch and not budgeted.

## 5. First-order vs JIT audit

### Remain first-order

```text
slow-depreciating general observation / stimulus / metrology / power
local soldering + hand adaptation
small universal mechanical/ESD/binding support
curated cheap-abundance electrical stock
small workholding
site-resolved fume source capture + direct exhaust
conditional heat-shrink heat source
operator eye protection if site inventory lacks a suitable pair
```

### Remain JIT / pressure-driven

```text
stepper + driver + independent actuator-energy cut
load cell + bridge ADC
known masses / compliant specimens / exact E1 brackets
SHT45-class ambient witness
dedicated camera mount/fixture geometry after G1/E1 geometry consumes it
locking/crimp connector ecosystem
SMD hot-air/reflow
electronic load / SMU / RF / thermal / machine-vision / fabrication machinery
```

The fact that the existing integrated camera may serve E1 does not justify buying camera fixturing before the physical geometry is frozen. Conversely, the caliper and P260C Pro remain rational early buy-once carriers because dimensional inspection and controlled bench observation have independent immediate consumers and low obsolescence risk.

## 6. Budget audit

Mechanically stable known/planned subtotal remains:

```text
major electrical                         ¥16,799.71
TS1200A + KNIPEX + PA-14 + Mitutoyo      ¥4,033.62
P260C Pro planning class                    ~¥598
--------------------------------------------------
known/planned                            ~¥21,431.33
```

Support/workholding/working-stock envelope remains `~¥2.8k–5.0k`. The added eye-protection line is deliberately small and fits inside this envelope; it does not justify widening the planning range.

Therefore purchased bench/tool stock remains approximately:

```text
~¥24.2k–26.4k
```

before the measured-route direct-exhaust hood/duct/fan line. Do not invent a facility SKU or placeholder price to make the budget look complete.

## 7. Checkout gates after horizontal audit

### Exact/load-bearing

```text
SDS824X HD ×1
Analog Discovery 3 Pro Bundle 471-060 ×1
SDM3055X-E ×1
UT61E+ ×1
SPD4323X ×1
Raspberry Pi Pico 2 with headers / SC1632 ×4
QUICK TS1200A / C005909777 ×1
KNIPEX 78 03 125 ESD ×1
ENGINEER PA-14 ×1
Mitutoyo 500-171-30 ×1
Godox P260C Pro ×1, hold if authorized/self-operated checkout materially >¥650
```

### Spec/checkout-bounded

```text
NANCH current S2 precision set
SATA current 9pc 1.5–10 mm metric ball-end set
general cutter / tweezers / ESD path
leads / BNC / USB / solder process stock
PCB holder / small vise / clamps
curated components / wire / fasteners / storage
clear side-protection eye protector if absent
heat gun only if suitable site heat source is absent
```

### Site-measurement bound

```text
hood geometry
duct diameter / route / length
fan pressure capability under actual resistance
safe outlet / make-up air
commissioned capture at actual soldering posture
```

## 8. Horizontal closeout

The first-order Laboratory boundary is now sufficiently contracted for checkout.

```text
vertical expansion       CLOSED
high-value redundancy    JUSTIFIED
missing persistent gap   1 small safety carrier admitted
currentness conflicts    RECONCILED
E1 hardware              JIT
budget                    RECONCILED
facility                  ROUTE-MEASURED, not fictitious SKU
```

The compact checkout projection is now `research/LABORATORY-FIRST-ORDER-ORDER-PACKET-20260827.md`. The next correct phase is not another product-family survey. It is:

```text
checkout-current transaction evidence
→ order freeze
→ arrival / identity / fitness / Agent-Realizability receipts
→ E0-A → E0-E
→ only then new capability pressure
```
