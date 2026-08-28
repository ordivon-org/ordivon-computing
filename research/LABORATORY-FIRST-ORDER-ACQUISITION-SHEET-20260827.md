# Ordivon Laboratory — First-Order Acquisition Sheet v0.1

Date: 2026-08-27  
Status: **EXECUTABLE FIRST-ORDER BOUNDARY / CHECKOUT-CURRENTNESS REVALIDATED 2026-08-27**
Current locality: mainland China / Anhui region

Latest pre-payment receipt: `research/LABORATORY-FIRST-ORDER-CHECKOUT-CURRENTNESS-RECEIPT-20260827.md`. Compact transaction projection: `research/LABORATORY-FIRST-ORDER-ORDER-PACKET-20260827.md`. High-value READY items remain unchanged; P260C Pro / NANCH / SATA are cart-price gated. The solder-fume site gate is now resolved in favor of source capture + safe direct external exhaust, so QUICK 6601/6611 are removed from the first-order equipment purchase.

## 0. Purpose

Compile the completed Laboratory capital audits into one purchase-executable boundary.

This sheet separates:

```text
ORDER NOW — exact load-bearing capital
ORDER NOW — spec/quantity bounded low-cost stock
CONDITIONAL — site/interface dependent
JIT LATER — E1 target-specific
DO NOT ORDER — no current consumer
```

High-value/high-risk items use exact SKUs. Low-value interchangeable consumables use exact functional specifications, quantities and substitution rules rather than fragile permanent links.

No price below is a quotation. Revalidate immediately before checkout.

## 1. ORDER NOW — exact major electrical capital

| Priority | Item | Exact SKU | Qty | Current observed price | Source/currentness | Ordivon role | Arrival receipt |
|---|---|---|---:|---:|---|---|---|
| A1 | 4ch 12-bit 200 MHz bench oscilloscope | **SIGLENT SDS824X HD** | 1 | **¥4,541** | SIGLENT Store CN, observed 2026-08-27, in stock | independent high-bandwidth physical observer | identity/serial → SCPI configure/query → raw waveform → reconnect/rebind |
| A2 | Agent-native mixed-signal experiment carrier | **Digilent Analog Discovery 3 Pro Bundle, 471-060** | 1 | **¥3,382.23** | DigiKey CN, observed 2026-08-27, hundreds in stock | AWG + logic + pattern + mixed-signal I/O + WaveForms SDK | enumerate → configure AWG/scope/digital → raw buffers → USB/process-loss recovery |
| A3 | programmable bench DMM | **SIGLENT SDM3055X-E** | 1 | **¥3,686** | SIGLENT Store CN, observed 2026-08-27, in stock | programmable metrology channel | ID → configure/query range/function → log → transport-loss recovery → handheld cross-check |
| A4 | independent handheld DMM | **UNI-T UT61E+** | 1 | **¥356** | UNI-T official mall, observed 2026-08-27 | independent/manual electrical observer; USB protocol is a bonus | basic function/continuity/DCV check → compare to bench DMM/reference |
| A5 | programmable multi-rail PSU | **SIGLENT SPD4323X** | 1 | **¥4,636** | SIGLENT Store CN, observed 2026-08-27 | Agent-programmable physical energy actuator | bounded low-voltage setup → query → output ON → independent DMM/scope observe → safe response-loss UNKNOWN/reconcile |
| A6 | deterministic MCU controller | **Raspberry Pi Pico 2 with headers / SC1632** | 4 | **¥49.62 ea / ¥198.48 total** | DigiKey CN, observed 2026-08-27, >2k stock | local timing/control + A/B generation + parallel controller + immediate spare | flash same firmware → identity A/B/C/D → replacement/rebind test |

### Major electrical exact subtotal

```text
¥16,799.71
```

This is the same long-horizon portfolio established by the product audit.

## 2. ORDER NOW — exact buy-once adaptation tools

| Priority | Item | Exact SKU | Qty | Current price/target | Source | Role / note |
|---|---|---|---:|---:|---|---|
| B1 | soldering station | **QUICK TS1200A / C005909777** | 1 | **¥1,024.15** | SZYJC current listing; 2–5 working-day reference | 120 W local adaptation; ESD monitoring; computer-management path must be interface-tested |
| B2 | precision ESD flush cutter | **KNIPEX 78 03 125 ESD / 4135581** | 1 | **¥355.08 incl. tax** | element14 CN | precision component/lead cutting; keep separate abuse cutter |
| B3 | fine-wire stripper | **ENGINEER PA-14 / C5252594** | 1 | **¥272.01 incl. tax** | LCSC MRO | 0.25–0.95 mm fine electronics wire |
| B4 | long-horizon digital caliper | **Mitutoyo 500-171-30** | 1 | **¥2,382.38 incl. tax** | element14 CN; current listing showed stock | durable mechanical reference + SPC measurement data output; machine ingestion still requires cable/interface receipt |
| B5 | first observation/task light | **Godox P260C Pro** | 1 | **target ≤¥650; launch MSRP ¥598; exact checkout price revalidate** | Godox official current product + mainland retail availability | 45 W, 2800–6500 K, CRI/TLCI≥98; Bluetooth/App is Human-remote until protocol openness is proven |
| B6 | precision screwdriver set | **NANCH 22/23-in-1 S2 current model** | 1 | checkout-current | JD official/self-operated listing preferred | compact electronics screw coverage; do not buy giant piece-count kit |
| B7 | metric hex set | **SATA current 9pc 1.5–10 mm metric ball-end set; 09101/09101A extra-long or 09105/09105A long** | 1 | checkout-current | SATA/JD self-operated current family | fixture/mechanics baseline; choose long vs extra-long from real reach/price at checkout rather than treating one low-cost model number as load-bearing identity |

### Buy-once exact/near-exact subtotal

Known exact lines excluding B5/B6/B7:

```text
¥4,033.62
```

With P260C Pro around the established ~¥598 class:

```text
~¥4,631.62 before screwdriver/hex
```

## 3. ORDER NOW — bounded support tools, choose current equivalent at checkout

These items are low enough in price and sufficiently commoditized that functional specification is the authoritative purchase identity.

### C1 — robust general cutter

```text
Qty: 1
Target: 150–180 mm general diagonal cutter
Use: thicker copper wire, cable ties, unknown/general material
Constraint: never use precision KNIPEX Super Knips as abuse cutter
Preferred brands: SATA / Pro'sKit / KNIPEX general side-cutter if local price is favorable
```

### C2 — ESD tweezers

```text
Qty: 4
Brand class: VETUS ESD
Preferred functional set:
1 × ESD-10 — fine straight
1 × ESD-11 — longer/stronger fine straight
1 × ESD-15 — fine curved
1 × ESD-13 — blunt/rounded straight
```

Current VETUS documentation continues to offer the ESD series as static-dissipative stainless precision tweezers. The four-model set is intentionally function-diverse: precision placement, longer reach/stronger straight handling, curved access and blunt handling of larger/delicate parts. Do not buy six nearly identical pointed tweezers merely to complete the numbered series. Preserve tip covers/case so precision tips do not become the consumable failure point.

### C3 — ESD handling

```text
1 × ~600 × 1200 mm ESD mat
1 × known ground cord
1 × wrist strap + lead
1 × bench ground/common-point hardware
```

Do not buy ionizer/ESD furniture now.

### C4 — test connection quality set

```text
2 pairs quality 4 mm banana leads
2 pairs banana-to-alligator
2 pairs mini-hook/fine grabbers
2–4 short BNC patch cables
1 BNC-to-grabber/alligator path
spare scope probe ground springs / hook accessories
2 known-good USB-C data cables
2 known-good USB-A/C data cables as needed by actual instrument ports
```

AD3 Pro Bundle already supplies BNC adapter, probes and mini-grabbers; avoid redundant accessory bundles.

### C5 — soldering tip set for TS1200A

Buy compatible TSS02-family tips in approximately:

```text
1 × small chisel
1 × medium chisel/hoof
1 × fine bent/precision
1 × larger thermal-mass tip
```

Do not buy a large tip collection before actual geometry pressure.

### C6 — solder process consumables

Keep one known process:

```text
1 × known solder wire alloy, ~0.5–0.8 mm
1 × compatible no-clean flux
2 × solder wick widths
1 × brass wool/tip cleaner
1 × electronics-cleaning IPA/appropriate cleaner
lint-free wipes
small heat-resistant silicone/work mat if current bench surface requires it
```

Do not mix many solder/flux chemistries initially. Treat alloy/diameter, flux chemistry, tip geometry and working temperature as one process identity; if one changes, record it rather than assuming the prior joint process is unchanged.

### C7 — ordinary drivers

```text
PH1 / PH2
small/medium flat-blade
```

The precision NANCH set should not replace ordinary full-size drivers for higher torque.

### C8 — reversible holding / workholding

Keep the first holding vocabulary small and role-diverse:

```text
1 × low-profile PCB holder/vise with non-marring electrically benign jaws
1 × small ~50–75 mm general bench vise with removable soft jaws and a stable mounting method
2 × small F/bar clamps
2 × small spring clamps or equivalent quick temporary clamps
binder clips / simple temporary fixtures as commodity aids
```

The PCB holder is for flat board soldering/probing; the small general vise is for wire, connector, small bracket and light mechanical work. Do not clamp a PCB in a metal vise merely because it fits. Clamps establish reversible geometry but are not precision-positioning or force-measurement fixtures. Helping-hand/articulated-holder systems and large T-slot/extrusion ecosystems remain pressure-driven.

### C9 — heat-shrink heat source — site-inventory gate

```text
IF an appropriate controlled hot-air/heat-gun source already exists
→ use and receipt-test it.

ELSE
→ add one documented 220–240 V adjustable heat gun with a stable rest/stand and a low-temperature/low-power operating regime.
```

Current reference carrier: Pro'sKit SS-615 family; the current SS-615H documentation provides a LOW regime around 210–300 W / 200 L·min⁻¹ with temperature adjustable from 100–400°C, plus over-temperature protection and stand-up use. Choose the site-compatible 220–240 V plug variant at checkout. Use the lowest effective temperature/airflow and appropriate distance for the tubing; do not touch heat-shrink with a soldering-iron tip.

This heat source is admitted for heat-shrink/process heating, **not** as promotion of a precision SMD rework station. If controlled component reflow/rework later becomes a recurring consumer, select that capability separately.

### C10 — operator eye protection — site-inventory/spec gate

The horizontal whole-order audit found one genuine first-order omission: hand soldering and lead/wire cutting can create hot-solder or flying-particle eye exposure. This is a direct consumer pressure, not starter-lab checklist completion.

```text
IF a suitable clear impact-protection eye protector with side protection already exists and is current/fit
→ receipt-test/use it.

ELSE
→ add at least 1 × clear safety spectacles / equivalent eye protector with side protection,
   compliant with current GB 14866-2023 or another recognized equivalent standard.
```

Use a model that fits the actual operator; ordinary prescription or fashion glasses are not automatically protective eyewear. A second pair is guest/spare stock only if that use is expected. Do not promote welding shades, face shields or chemical-splash goggles without the corresponding hazard.

This PPE does not replace source capture, low-energy design, tool fitness or safe work practice; it closes a residual eye-exposure path after those upstream controls.

## 4. SITE-RESOLVED FACILITY — source capture + direct external exhaust

The site has already been confirmed capable of safe direct external exhaust. Therefore QUICK 6601/6611 are **not first-order purchases**. Preserve the old comparison only as historical fallback if the physical site changes.

First-order facility path:

```text
solder source
→ movable close-capture hood or small partial enclosure
→ short smooth/maintainable duct
→ pressure-capable inline fan
→ safe outdoor discharge
```

Design/receipt boundaries:

```text
capture geometry:
  keep the solder-fume source inside the actual capture zone;
  HSE manual-solder guidance gives roughly 1–2 hood diameters / ~50–100 mm for a typical movable hood.

capture performance:
  select fan/duct/hood as a system, not from free-air fan m³/h alone;
  HSE LEV guidance gives 0.5–1.0 m/s as a reference capture-velocity range for soldering/capturing hoods.

outlet:
  discharge to a safe external location that does not expose people or readily re-enter openings/air intakes;
  comply with building/site/environmental rules.

make-up air:
  provide a path for replacement air so room negative pressure does not collapse extraction performance.

maintenance:
  use accessible, cleanable duct/fan/hood geometry; rosin fume creates sticky residue and extraction performance must not be assumed permanent.
```

A small recirculating desktop 'smoke absorber' is not an equivalent substitute. HSE guidance warns that simple bench disperser/filter boxes may provide inadequate control; recirculated air requires suitable high-efficiency filtration and maintenance.

Agent control is not a first-order requirement for this safety control. The important initial invariant is procedural: **no routine soldering unless extraction is operating and visibly capturing the plume away from the breathing zone**. If soldering becomes automated or high-frequency, promote airflow/pressure sensing so extraction readiness becomes machine-observable/interlockable.

## 5. ORDER NOW — curated cheap-abundance electrical working stock

The rule here is:

```text
common + tiny carrying cost + frequent experiment use
→ stock locally
```

not JIT per part.

### E1 — breadboards / prototype substrate

```text
2 × known-good 830-point breadboards — active
2 × additional spare/value 830-point breadboards
10 × small perfboard/protoboard pieces
```

Use inexpensive commodity sources, but assign board identity on arrival. Keep two boards as known-good active exploration substrates and two as replacement/parallel spares. Any board that develops unexplained intermittency, weak retention, contact damage or repeated suspect behavior is demoted from authoritative experiment use and marked retired/sacrificial rather than silently returned to stock. Perfboard is the stabilization bridge for circuits worth preserving before a custom PCB is justified.

### E2 — 1% through-hole metal-film resistor stock

Use 1/4 W, ±1%, ordinary metal-film with known manufacturer/part identity or at minimum known value/tolerance/power class. The current quantity plan is 27 values and approximately 1,700 physical resistors total: 50 pcs/value baseline plus an extra 50 pcs for seven high-use values.

This is intentional cheap abundance, not anonymous assortment buying. At current distributor pricing, the carrying cost of these parts is materially below repeated experiment interruption/search/procurement cost.

Initial values:

```text
10 Ω
47 Ω
100 Ω
150 Ω
220 Ω
330 Ω
470 Ω
680 Ω
1 kΩ
1.5 kΩ
2.2 kΩ
3.3 kΩ
4.7 kΩ
6.8 kΩ
10 kΩ
15 kΩ
22 kΩ
33 kΩ
47 kΩ
68 kΩ
100 kΩ
150 kΩ
220 kΩ
330 kΩ
470 kΩ
680 kΩ
1 MΩ
```

Quantity:

```text
50 pcs/value default
100 pcs/value for 100 Ω / 220 Ω / 330 Ω / 1 kΩ / 4.7 kΩ / 10 kΩ / 100 kΩ
```

Current LCSC evidence shows common 1/4 W 1% metal-film parts are sufficiently cheap that this stock costs far less than repeated procurement interruption. Adapt quantity upward to supplier MOQ where needed rather than fragmenting procurement merely to preserve an arbitrary count.

The 1/4 W stock is for signal/bias/RC/LED/general low-power experiments, **not as generic power-load stock**. Before using a resistor as a dissipative load, check `P = V²/R = I²R` with engineering margin; the presence of a resistance value in inventory does not make it admissible across the bench-voltage range.

Do not stock broad 0.1% precision values yet. If a claim depends on tighter resistance knowledge, measure/select the actual part or procure a suitable precision/reference component under capability pressure.

### E3 — capacitors

The initial quantity plan is 190 physical capacitors total, but dielectric/technology is part of inventory identity rather than a cosmetic attribute.

Ceramic, 20 pcs/value:

```text
100 pF
1 nF
10 nF
100 nF
1 µF
```

Policy:

```text
100 pF / 1 nF: prefer C0G/NP0 where practical for stable small-value work
10 nF / 100 nF / 1 µF: prefer documented X7R-class or otherwise known-stable general-purpose ceramic for decoupling / ordinary experiments
Y5V / Z5U-class parts: do not use as default timing/measurement reference stock
```

Film, 10 pcs/value:

```text
10 nF
100 nF
1 µF
```

Film parts are the first-order stable-RC candidate where dielectric stability matters, but `film capacitor` still does not mean metrology reference; actual capacitance/tolerance/voltage identity and, where load-bearing, measurement remain required.

Electrolytic, 10 pcs/value:

```text
1 µF
10 µF
47 µF
100 µF
470 µF
1000 µF
```

Electrolytics are primarily bulk-energy / filtering carriers. Polarity, voltage rating, ESR/frequency behavior and age matter; do not silently treat them as stable timing references.

Use known voltage ratings comfortably above initial low-voltage work. Reject anonymous capacitor assortments that omit dielectric, tolerance or voltage identity even when the nominal capacitance labels look complete.

### E4 — LEDs / diodes / minimal discretes

```text
20 × red LED
20 × green LED
20 × blue LED
20 × white LED
50 × 1N4148-class
20 × 1N4007-class
20 × common Schottky (e.g. SS14-class)
20 × common NPN (2N3904-class)
20 × common PNP (2N3906-class)
20 × small N-MOSFET (2N7000-class)
```

These remain low-cost generic experiment carriers, not metrology references.

### E5 — wire

Wire stock is split by **mechanical role**, not gauge number alone.

Breadboard / shape-retaining prototype wire:

```text
22 AWG solid-core
red / black / white / yellow / blue / orange
~5 m each color
```

Use for breadboards, perfboards and short fixed low-voltage prototype wiring where shape retention is useful. 22 AWG solid-core is not the default fixture-harness wire: repeated flexing near stripped/soldered ends can create fatigue failures even when electrical current is modest.

Flexible fixture / harness wire:

```text
24 AWG stranded silicone or documented flexible hook-up wire
red + black ~10 m each
4 signal colors ~5 m each
```

Use for routed fixture wiring, sensor leads and connections expected to move during apparatus revision. Prefer known conductor construction/insulation/temperature/voltage data rather than anonymous 'silicone wire' listings.

Color is a representation aid, not electrical authority. Default convention:

```text
red   = positive supply / energized rail
black = return / circuit reference where appropriate
white / yellow / blue / orange = signals / channels / control
green-yellow combination = reserved for protective-earth semantics; not ordinary signal wiring
```

Do not infer polarity or net identity from color alone; apparatus records/labels remain authoritative. Preserve at least four non-red/black signal colors so photographs and successor reconstruction can discriminate parallel nets.

Wire gauge does **not** imply a universal safe current. Current admissibility depends on conductor construction, insulation temperature, bundle/ambient conditions, length, connector/termination and allowable voltage drop. The 22/24 AWG first-order stock is for low-voltage electronics/fixture interconnect, not high-power actuator or mains wiring.

Optional 26 AWG only if actual connector/fixture density benefits. Promote thicker wire, paired/twisted/shielded cable, mains-rated cable or dedicated motor/power harnesses only under real interface/current/noise pressure.

### E6 — jumpers / headers / basic connectors

The first-order goal is a **minimal interface vocabulary**, not a connector-family collection.

```text
3 × 40-wire M-M 2.54 mm jumper ribbons
3 × 40-wire F-F
3 × 40-wire M-F
10 × breakaway straight 2.54 mm header strips
5 × right-angle 2.54 mm header strips
10 × small 2-pin screw-terminal blocks/adapters
10 × 3-pin screw-terminal blocks/adapters
small set of pre-crimped pigtails only when device-specific wiring appears
```

Role boundary:

```text
2.54 mm jumpers / headers
→ reversible low-voltage prototype and inspection interface

screw terminals
→ coarse, field-reworkable low-voltage wire-to-apparatus boundary

locking/crimp connector family
→ promoted only when recurrent fixture/device pressure establishes a stable interface contract
```

Do not treat Dupont-style jumpers or generic 2.54 mm friction connections as persistent vibration-resistant fixture wiring, current-authoritative power connectors or safety interlocks. Their value is low-friction exploration and inspection.

Do not stock multiple JST/Molex families now. Connector family selection is a system decision that includes pitch, wire range, current/voltage regime, locking/keying, board footprint, housing/contact inventory, mating geometry, crimp process/tooling and replacement continuity. Buying housings without the correct contacts/tool/process is nominal inventory rather than realized connector capability.

Current JST families illustrate why premature unification is wrong: XH is a 2.5 mm wire-to-board family rated up to 3 A with AWG22 in its stated condition; PH is 2.0 mm and 2 A with AWG24; GH is 1.25 mm, 1 A with AWG26 and a secure-lock/keyed high-density role. These are different physical regimes, not merely small/medium/large versions of one universal connector.

Promotion triggers for a persistent connector family include repeated mating, vibration/motion, required keying/polarization, recurring detachable modules, known current/voltage pressure, density/space pressure, or repeated Human wiring errors. When one family begins recurring across several apparatuses, standardize deliberately and then acquire the matching housings, contacts, pre-crimped leads or validated crimp tooling/process.

Until then prefer commercially pre-crimped pigtails/adapters for device-specific interfaces rather than creating a crimp-tool ecosystem before a recurring consumer exists.

### E7 — insulation / cable management

The first-order set is divided by physical responsibility rather than treated as interchangeable wrapping material.

```text
2:1 thin-wall polyolefin heat-shrink:
1.5 / 2 / 3 / 4 / 6 mm — ~2 m each

100 small nylon cable ties
1 roll documented polyimide electrical/masking tape (Kapton-class)
1 roll quality PVC electrical insulation tape
```

Role boundary:

```text
heat-shrink
→ preferred persistent insulation / identification / light mechanical support around small soldered joints and terminations

polyimide tape
→ heat-resistant local masking / temporary retention / high-temperature electrical isolation during solder/rework

PVC electrical tape
→ conformable insulation, repair and irregular-geometry overwrap where tape is actually fit; not the default way to hide every small solder joint

cable ties
→ cable routing / bundle restraint; not conductor insulation and not termination strain relief
```

Prefer documented thin-wall flexible polyolefin around 2:1 shrink ratio for the baseline stock. Current industrial examples such as 3M FP-301 use this regime for cable-splice/termination insulation and lightweight harness covering. Do not add adhesive-lined/3:1/environmental-seal tubing until moisture, abrasion or stronger strain-relief pressure appears.

For polyimide tape, do not equate any anonymous amber tape with DuPont Kapton film performance. Film and adhesive together define the tape. Buy a documented polyimide electrical/masking product whose adhesive temperature and residue behavior are suitable for electronics work.

A quality PVC electrical tape can be a legitimate insulation product; for example current 3M Super 33+ documentation covers primary cable insulation and harnessing. In the Ordivon first-order bench, however, heat-shrink remains the preferred small-joint persistent carrier because its state is visually/mechanically clearer and not primarily adhesive-held. Product voltage ratings do not expand Laboratory authority beyond the current low-voltage regime.

Cable ties should be snug enough to route the bundle but not crushed tight. Over-tension can damage cable bundles. They do not replace a clamp, grommet, connector backshell or other true strain-relief feature where motion/load reaches a termination.

### E8 — fasteners / standoffs

The first-order mechanical vocabulary is deliberately asymmetric: **M3 is the fixture default**, while M2/M2.5 exist only as small-board mounting regimes.

M3 coarse-thread fixture stock:

```text
M3×0.5 socket-head / hex-drive stainless fasteners
50 each: M3×6 / 8 / 10 / 12 / 16 / 20 / 25 mm
200 × matching M3 nuts
200 × M3 flat washers
50 × mixed-length M3 standoffs (document length/material)
```

M3 is preferred for early brackets, perfboard/adapter mounting, light mechatronic fixture construction and reversible apparatus because it is compact but materially easier to handle and torque than very small PCB hardware. The socket-head/metric-hex choice aligns with the existing metric hex-key set; ordinary reference geometry uses M3×0.5 coarse thread and a 2.5 mm hex key.

Small-board mounting stock:

```text
30 × M2 mounting/standoff sets for Pico-class boards
20 × M2.5 PCB mounting/standoff sets for secondary/common board regimes
```

A `set` means a realized mating path — appropriate screw + standoff + nut/retention where required — rather than a loose pillar with no matching hardware. Raspberry Pi Pico 2 has 4×2.1 mm mounting holes, so M2 is the immediate first-order board-mount consumer; M2.5 remains useful for other common PCB/module geometries but is not allowed to masquerade as Pico-compatible stock.

For board mounting, prefer electrically benign/isolating hardware where appropriate and verify head/washer clearance from pads, traces and components. Metal washers/standoffs near a PCB are not automatically safe simply because the screw diameter fits. Do not over-tighten thin PCBs.

Flat washers distribute clamp load and provide a replaceable bearing surface; they are not mandatory at every joint. On PCB/insulating surfaces, use material/geometry appropriate to the electrical and mechanical boundary rather than reflexively adding a stainless washer.

The first-order stock does not yet include nyloc nuts, spring washers, threadlocker, torque tools or large bracket inventories. Repeated vibration/loosening promotes a retention strategy; load-bearing or repeatability-sensitive joints promote torque-controlled assembly. Until then ordinary hand-tightened reversible fixture assembly is sufficient.

Add small brackets/clamps only when E1 geometry freezes; do not pre-buy arbitrary bracket ecosystems before the actual hole pattern, load direction and fixture geometry exist.

### E9 — storage / identity

Storage is an **identity/discoverability substrate**, not a housekeeping goal.

```text
small labeled bins or drawer units
zip bags in several sizes
ESD shielding/dissipative bags where the device actually requires them
printed/hand labels
per-category reorder card / QR / part note
```

Use three identity levels rather than serializing everything:

```text
L1 — unique object identity
high-value instruments; Pico/controller generations; calibrated/reference carriers;
known-good/suspect/retired breadboards or cables; safety-relevant apparatus; items whose
history/currentness changes whether they may be used.

L2 — lot/bin/specification identity
resistors, capacitors, semiconductors, wire, screws, standoffs, connectors and other
cheap abundance where pieces are interchangeable enough for ordinary use but the
value/tolerance/dielectric/rating/material/source class must remain known.

L3 — role-only commodity identity
non-load-bearing generic wipes, ordinary cable ties, bags and similar items for which
individual or lot provenance does not materially affect the experiment claim.
```

Do not turn L2 stock into thousands of serialized assets. Preserve the supplier/manufacturer label or transcribe the fields that determine experimental fitness. Electronics distributors themselves retain fields such as manufacturer part number, quantity, lot/date code, ESD/MSL status and compliance on component labels; this is the useful model, not per-piece serialization.

Minimum useful bin/lot label where applicable:

```text
human-readable role/name
manufacturer part number or specification class
critical value/rating/material/dielectric/tolerance
quantity band or reorder threshold
source/reorder reference
ESD/MSL/polarity warning where relevant
status: active / suspect / retired / reserved when currentness matters
```

Location is part of discoverability. Use a stable shallow location vocabulary such as `ELECTRICAL/PASSIVE/R-10K-1PCT` or equivalent drawer/bin IDs, but do not encode mutable facts such as exact quantity into the physical location name.

Reorder metadata is not a promise to buy the same SKU forever. For generic stock record the admitted specification + preferred source class + substitute constraints. For load-bearing/characterized parts record the exact manufacturer/part number and do not silently substitute.

Preserve original ESD/MSL packaging for sensitive components when useful. Anti-static/dissipative packaging and ESD warnings are functional protection/handling metadata, not decorative packaging. Do not empty every component into ordinary clear plastic merely for visual neatness.

## 6. First-order budget interpretation

### Known exact/near-exact high-value capital

```text
major electrical exact subtotal            ¥16,799.71
TS1200A + KNIPEX + PA-14 + Mitutoyo        ¥4,033.62
P260C Pro planning price                    ~¥598
-----------------------------------------------------
known/planned subtotal                      ~¥21,431.33
```

### Remaining support + cheap stock

Plan approximately:

```text
precision driver / hex / general cutter
site-gated clear side-protection eye protection
ESD mat / wrist / tweezers
quality leads / grabbers / cables
solder tips + solder/flux/wick/cleaning
breadboards / passive/discrete stock
wire / jumpers / heat-shrink / M2/M2.5/M3 / storage
PCB holder / small vise / clamps
optional heat-shrink heat gun if the site lacks one
-----------------------------------------------------
~¥2,800–5,000 planning envelope before site-specific exhaust hardware
```

Therefore the purchased electrical/adaptation/tool stock remains approximately:

```text
~¥24.2k–26.4k
```

The direct-exhaust hood/duct/fan is site infrastructure rather than a filtered-fume-extractor SKU. Keep its cost as a separate measured-route checkout line until hood geometry, duct length/diameter and fan pressure requirement are known; do not reinsert QUICK 6601/6611 into the first-order budget merely to fill that line.

A realistic all-in first-order bench remains in the mid-¥20k range, with the final facility increment determined by the actual short direct-exhaust route and any heat source/workholding already present.

## 7. JIT LATER — not part of first order

E1-only target hardware remains downstream of E0:

```text
1 small stepper
1 current-limited driver
independent actuator-energy cut
~500 g load cell + bridge ADC
known small masses
exact fixture/base/brackets/hard stops
compliant specimens
SHT45-class ambient witness
```

Do not include these merely to save shipping time.

## 8. DO NOT ORDER NOW

```text
hot-air station
reflow oven
second soldering station
production/JBC soldering automation
scope-vendor AWG option
scope-vendor logic module/probe
standalone AWG
6.5-digit DMM
SMU
electronic load
RF spectrum/VNA
ToF / encoder
IMU
thermal camera
machine-vision camera
second observation light
local 3D printer/CNC/laser
large connector/crimper ecosystems
large anonymous component assortments
ESD furniture/ionizer
FPGA/PLC/realtime host
```

Every item can be reopened by actual capability pressure.

## 9. Checkout currentness checklist

Before payment, revalidate for every exact SKU:

```text
exact model / revision
seller/channel authority
stock
checkout price
included probes/cables/adapters
warranty / invoice
mains voltage and plug compatibility
firmware/manual availability
LAN/USB/SDK/SCPI claims where load-bearing
```

For AD3 confirm SKU `471-060` Pro Bundle, not bare `410-415`.

For Pico controllers buy all four as the same physical SKU: Raspberry Pi Pico 2 with headers / SC1632. Raspberry Pi documentation explicitly does not shorten the Pico 2 header variant to `H`.

For scope confirm the `SDS824X HD` 4-channel model, not SDS822X HD.

For DMM confirm `SDM3055X-E`.

For PSU confirm `SPD4323X`.

## 10. Receipt order after delivery

Do not immediately treat arrival as capability.

```text
1. photograph / inventory / serial / SKU / source receipt
2. inspect physical damage/accessories
3. power-on within bounded conditions
4. record firmware / device identity
5. install vendor/native software only where needed
6. bind device to its Ordivon logical role
7. run Agent Realizability Receipt for programmable carriers
8. run manual fitness receipt for manual tools
9. establish working-stock locations/labels
10. execute frozen E0-A → E0-E
```

## 11. Current first-order standing

### Ready to order now

```text
SDS824X HD ×1
Analog Discovery 3 Pro Bundle 471-060 ×1
SDM3055X-E ×1
UT61E+ ×1
SPD4323X ×1
Raspberry Pi Pico 2 with headers SC1632 ×4
TS1200A ×1
KNIPEX 78 03 125 ESD ×1
ENGINEER PA-14 ×1
Mitutoyo 500-171-30 ×1
Godox P260C Pro ×1
NANCH S2 precision driver set ×1
SATA current 9pc 1.5–10 mm ball-end metric hex set ×1
support-tool bounded set including PCB holder / small vise / clamps
clear side-protection eye protection if no suitable current pair already exists
curated cheap-abundance stock
site-resolved source-capture + direct-exhaust facility
heat-shrink heat gun only if no suitable site heat source exists
```

### Remaining site checkout gates

```text
direct exhaust:
measure actual hood/duct route
→ select fan from real pressure/capture requirement
→ verify safe outlet / make-up air / capture before routine soldering

heat shrink:
existing suitable hot-air source?
→ YES: receipt-test and use
→ NO: add documented adjustable heat gun
```

### Not in first order

```text
E1 target hardware
specialized/production/RF/HV/fabrication categories
```

This is now the first purchase-executable Ordivon Laboratory boundary.

## 12. Current web source snapshot

Major current sources revalidated on 2026-08-27:

```text
SIGLENT SDS824X HD:
https://store.siglent.com/product/sds824x-hd-%E9%AB%98%E6%B8%85%E7%A4%BA%E6%B3%A2%E5%99%A8/

SIGLENT SDM3055X-E:
https://store.siglent.com/product/sdm3055x-e-5-5%E4%BD%8D%E5%8F%8C%E6%98%BE%E5%8F%B0%E5%BC%8F%E6%95%B0%E5%AD%97%E4%B8%87%E7%94%A8%E8%A1%A8/

SIGLENT SPD4323X category/current price:
https://store.siglent.com/product-category/%E7%9B%B4%E6%B5%81%E7%94%B5%E6%BA%90/

Analog Discovery 3 Pro Bundle 471-060:
https://www.digikey.cn/zh/products/detail/digilent-inc/471-060/19235252

Raspberry Pi Pico 2 with headers / SC1632:
https://pip.raspberrypi.com/categories/1264-raspberry-pi-pico-2-h
https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html
https://www.digikey.cn/en/products/detail/raspberry-pi/SC1632/26241102

UNI-T UT61E+ official:
https://meters.uni-trend.com.cn/content/1301.html
https://mall.uni-trend.com.cn/products/?op_238492=UT61E%2B&size=15

QUICK TS1200A current supply:
https://www.szyjc.com/product/C005909777

Historical fallback only — QUICK 6611 / 6601, **not first-order purchases**:
https://www.quick-global.com/index.php/proinfo/109.html
https://www.quick-global.com/proinfo/111.html

KNIPEX 78 03 125 ESD:
https://www.element14.cn/c/tools-production-supplies/tools-hand-workholding/cutters/electronic?product-range=knipex-super-knips

ENGINEER PA-14:
https://item.szlcsc.com/mro/5970189.html

Mitutoyo 500-171-30:
https://www.element14.cn/en-CN/mitutoyo/500-171-30/digital-caliper-6-150mm/dp/559507

Godox P260C Pro official:
https://cn.godox.com/product-a/P260CPro.html

LCSC through-hole resistor current evidence:
https://www.lcsc.com/category/1203.html
```
