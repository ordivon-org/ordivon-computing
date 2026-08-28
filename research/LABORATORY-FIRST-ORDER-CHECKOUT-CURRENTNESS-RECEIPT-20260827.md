# Ordivon Laboratory — First-Order Checkout Currentness Receipt

Date: 2026-08-27  
Status: **PRE-PAYMENT CURRENTNESS REVALIDATION COMPLETED / PURCHASE NOT YET EXECUTED**  
Parent: `research/LABORATORY-FIRST-ORDER-ACQUISITION-SHEET-20260827.md`

## 0. Purpose

Revalidate the first-order acquisition boundary against current mainland-China public product/stock/price evidence immediately before any actual payment.

This receipt does not claim that an order has been placed. It classifies every first-order class as:

```text
READY          — current SKU/price/stock evidence remains consistent with standing
PRICE-GATED    — capability standing holds but exact current transaction price is not robustly visible
SITE-GATED     — physical site condition is still required
SPEC-GATED     — low-cost generic category; exact seller may vary inside written specification
```

## 1. READY — major electrical capital

### SDS824X HD

Current SIGLENT Store CN evidence:

```text
SKU: SDS824X HD
price: ¥4,541
stock: 有货
warranty: 3 years
shipping statement: 48 h / SF Express
included: 200 MHz passive probe(s), certificate/calibration report, power cable
```

Standing: **READY**.

No current price/availability reversal was found that invalidates the long-horizon 200 MHz choice.

### Analog Discovery 3 Pro Bundle

Current DigiKey CN evidence:

```text
manufacturer SKU: 471-060
price: ¥3,382.23 incl. VAT
stock: >500 units in current crawl
status: active / in sale
bundle includes: cable, probes, software, test leads; product-highlight confirms BNC adapter + pair of BNC probes + 6 mini-grabbers
```

Standing: **READY**.

The Pro Bundle still dominates bare 410-415 at the current ~¥248 delta.

### SDM3055X-E

Current SIGLENT Store CN evidence:

```text
SKU: SDM3055X-E
price: ¥3,686
stock: 有货
warranty: 3 years
interfaces: USB Device / USB Host / LAN; GPIB optional
machine data paths: VXI-11 / USBTMC / USB storage
included: USB cable + power cable
```

Standing: **READY**.

### SPD4323X

Current SIGLENT Store CN evidence:

```text
SKU: SPD4323X
price: ¥4,636
stock: 有货
4 independent outputs
240 W
1 mV / 1 mA resolution
List timing <50 ms; 1 ms setting resolution
Sense
included: USB cable + test leads + power cable
```

Standing: **READY**.

Its ~¥950 premium over SPD3303X remains small relative to the fourth rail and stronger sequencing/Sense platform.

### Raspberry Pi Pico 2 with headers / SC1632

Current Raspberry Pi + DigiKey CN evidence:

```text
official current product name: Raspberry Pi Pico 2 with headers
manufacturer SKU: SC1632
price: ¥49.62 ea incl. VAT
stock: >2,000 units in current crawls
status: active
```

Raspberry Pi's current documentation explicitly states that, unlike first-generation Pico H/WH, the Pico 2 header variant is not shortened to `H`. DigiKey may still surface a commerce description containing `Pico 2 H`; canonical Laboratory naming follows the manufacturer.

Quantity standing: **4 units, all same SKU**.

Total: `¥198.48`.

Standing: **READY**.

### UT61E+

The prior official UNI-T product/mall standing remains unchanged in this checkout pass; no contrary product-line evidence was found.

Standing: **READY WITH FINAL CART PRICE CHECK**.

Keep the acquisition-sheet planning value `~¥356` until actual cart/checkout confirms it.

## 2. READY — buy-once adaptation capital

### QUICK TS1200A

Current SZYJC evidence:

```text
SKU: C005909777 / TS1200A
price: ¥1,024.15
MOQ: 1
reference lead time: 2–5 working days
120 W
200–420 °C
integrated heater
TSS02 tips
```

Standing: **READY**.

The computer-management path remains a post-arrival interface question; do not delay purchase on that basis because soldering capability is valuable independently.

### KNIPEX 78 03 125 ESD

Current element14 CN evidence:

```text
SKU: 78 03 125 ESD
order code: 4135581
price: ¥355.0799 incl. tax at qty 1
```

Standing: **READY**.

### ENGINEER PA-14

Current LCSC MRO evidence:

```text
SKU: PA-14 / C5252594
price: ¥272.01 incl. tax
MOQ: 1
strip range: 0.25–0.95 mm
```

Standing: **READY**.

### Mitutoyo 500-171-30

Corrected current element14 CN + official Series 500 evidence:

```text
SKU: 500-171-30
price: ¥2,382.38 incl. tax
stock shown: 43
range: 0–150 mm / 0–6 in
resolution: 0.01 mm
accuracy: ±0.02 mm
repeatability: 0.01 mm
SPC measurement data output: YES
IP67: NO (not the coolant-proof 500-7xx series)
```

Standing: **READY — corrected from 500-196-30 after official model-table audit**.

## 3. PRICE-GATED — exact model standing holds, transaction price must be checked in cart

### Godox P260C Pro

Current official product evidence confirms:

```text
45 W
2800–6500 K
CRI/TLCI average >=98
USB-C / DC / NP-F power
Bluetooth + Godox Light APP
NFC pairing
```

The product is current. However a robust current checkout price was not exposed by the current public search result.

Standing:

```text
PRICE-GATED
buy if current authorized/self-operated price <= ¥650
if materially > ¥650 → pause and rerun lighting knee comparison
```

### NANCH precision driver

Current JD evidence confirms multiple self-operated S2 22-in-1 / 23-in-1 NANCH variants remain current.

Standing:

```text
PRICE-GATED / VARIANT-GATED
prefer current 22-in-1 S2 self-operated variant
avoid CRV variant when similarly priced S2 is available
avoid 55+/100-piece expansion for piece-count prestige
```

### SATA current 9pc 1.5–10 mm metric ball-end family

Current JD evidence shows both the long 09105/09105A and extra-long 09101/09101A families remain current/self-operated options. The Laboratory need is the 9-piece metric ball-end geometry; this low-cost hand tool does not justify treating one transient model number as semantic identity.

Standing:

```text
PRICE/SPEC-GATED
choose 09105/09105A when ordinary long reach is fit and cheaper
choose 09101/09101A only when extra-long reach is useful at a reasonable current delta
prefer current self-operated/authorized supply
```

## 4. SOLDER-FUME SITE GATE — RESOLVED 2026-08-27

The operator has now confirmed that the Laboratory bench can support safe direct external exhaust.

Current standing:

```text
source capture
→ short maintainable duct
→ safe outdoor discharge
```

Therefore:

```text
QUICK 6601 = NOT IN FIRST ORDER
QUICK 6611 = NOT IN FIRST ORDER
```

This is not a rejection of their filtration capability. The physical site itself supplies a lower-capital carrier for the same support need, without recirculating captured solder fume through the room.

The direct-exhaust implementation still requires ordinary F01/F02 fitness checks: capture point near source, maintainable duct path, adequate airflow, no discharge into occupied/intake-sensitive areas, and no unsafe interference with electrical/bench operation.

If the site changes or direct exhaust later proves inadequate, 6611/6601 can be reopened from the preserved prior comparison.

## 5. SPEC-GATED — low-cost support and working stock

The following should not wait for exact permanent SKUs:

```text
general cutter
VETUS ESD tweezers
ESD mat/ground/wrist
banana/grabber/BNC/USB data cables
TS1200A tip geometries
solder/flux/wick/cleaning
breadboards/protoboards
resistors/capacitors/LEDs/diodes/minimal discretes
22 AWG solid + 24 AWG flexible wire
2.54 mm jumpers/headers
heat-shrink/cable management
M3-centric fasteners/standoffs
labels/storage
clear side-protection eye protection if no suitable current pair already exists
```

Use the exact quantities/specifications frozen in `LABORATORY-FIRST-ORDER-ACQUISITION-SHEET-20260827.md`.

Seller substitution is allowed only inside those specifications.

## 6. Recomputed current known subtotal

Mechanically rechecked from current verified/planning values:

```text
SDS824X HD                       4,541.00
AD3 Pro Bundle                   3,382.23
SDM3055X-E                       3,686.00
UT61E+ planning                    356.00
SPD4323X                         4,636.00
4 × Pico 2 with headers / SC1632    198.48
-----------------------------------------
major electrical               ¥16,799.71

TS1200A                          1,024.15
KNIPEX 78 03 125 ESD              355.08
ENGINEER PA-14                     272.01
Mitutoyo 500-171-30              2,382.38
-----------------------------------------
verified adaptation             ¥4,033.62

known major + verified adapt   ¥20,833.33
```

With P260C Pro at the acquisition-sheet planning threshold/reference around `¥598`, known/planned becomes approximately `¥21,431.33` before NANCH/SATA/support/stock.

No arithmetic drift was found relative to the acquisition sheet.

## 7. Purchase readiness

Current decision surface:

```text
READY NOW:
SDS824X HD
AD3 Pro 471-060
SDM3055X-E
SPD4323X
Raspberry Pi Pico 2 with headers / SC1632 ×4
UT61E+ subject only to final cart price
TS1200A
KNIPEX 78 03 125 ESD
ENGINEER PA-14
Mitutoyo 500-171-30
spec-bounded cheap support/stock

PRICE-GATED IN CART:
P260C Pro
NANCH S2 22/23-in-1
SATA 9pc metric ball-end family — 09105/09105A or 09101/09101A by current reach/price

SITE-GATED:
fume path

NOT PART OF ORDER:
E1 target-specific hardware and previously deferred specialized capital
```

## 8. Final boundary

The research phase is no longer the blocker.

The remaining pre-payment work is transactional currentness and one physical-site fact:

```text
current cart prices
+ exact seller/stock/accessories/warranty
+ measured direct-exhaust hood/duct route and capture commissioning
```

After those are checked, there is no current research reason to delay the READY items.

This receipt intentionally does not claim purchase/payment/shipping because those external effects have not been executed through the current Ordivon control surface.

## 9. Public evidence snapshot

```text
SDS824X HD:
https://store.siglent.com/product/sds824x-hd-%E9%AB%98%E6%B8%85%E7%A4%BA%E6%B3%A2%E5%99%A8/

SDM3055X-E:
https://store.siglent.com/product/sdm3055x-e-5-5%E4%BD%8D%E5%8F%8C%E6%98%BE%E5%8F%B0%E5%BC%8F%E6%95%B0%E5%AD%97%E4%B8%87%E7%94%A8%E8%A1%A8/

SPD4323X:
https://store.siglent.com/product/spd4323x-%E5%8F%AF%E7%BC%96%E7%A8%8B%E7%BA%BF%E6%80%A7%E7%9B%B4%E6%B5%81%E7%94%B5%E6%BA%90/

AD3 Pro 471-060:
https://www.digikey.cn/zh/products/detail/digilent-inc/471-060/19235252

Raspberry Pi Pico 2 with headers / SC1632:
https://pip.raspberrypi.com/categories/1264-raspberry-pi-pico-2-h
https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html
https://www.digikey.cn/zh/products/detail/raspberry-pi/SC1632/26241102

TS1200A:
https://www.szyjc.com/product/C005909777

KNIPEX 78 03 125 ESD:
https://www.element14.cn/c/tools-production-supplies/tools-hand-workholding/cutters/electronic?product-range=knipex-super-knips

ENGINEER PA-14:
https://item.szlcsc.com/mro/5970189.html

Mitutoyo 500-171-30:
https://www.element14.cn/en-CN/mitutoyo/500-171-30/digital-caliper-6-150mm/dp/559507

Historical fallback only — QUICK 6611 / 6601, not first-order purchases:
https://en.quick-global.com/proinfo/109.html
https://www.quick-global.com/proinfo/111.html

Godox P260C Pro:
https://cn.godox.com/product-a/P260CPro.html
```
