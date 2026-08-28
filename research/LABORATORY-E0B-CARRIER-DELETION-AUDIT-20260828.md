# Laboratory E0-B Carrier Deletion Audit — 2026-08-28

## Result

**SDS824X HD is not deletion-essential for the first E0-B physical contact.**

The original preregistration allocated `AD3 AWG -> RC -> SDS824X HD`. That is strong, but it binds the first physical bridge to two major instruments. A pre-data subtraction found a smaller responsibility split:

```text
Pico 2 GPIO      = independent deterministic stimulus carrier
Analog Discovery 3 = independent two-channel analog observer
UT61E+           = post-classification static reference/reveal
```

The AD3 documentation exposes two simultaneous analog inputs and acquisition capacity far above the experiment's 1 MS/s requirement; Pico 2 GPIO is fixed at the 3.3 V rail and has a simple BOOTSEL USB mass-storage/UF2 programming path. Because AD3 captures the actual physical `Vin` together with `Vout`, neither the Pico command nor nominal 3.3 V is treated as physical-input truth.

Therefore the discriminating relation survives deletion of the bench scope from the **first-contact dependency**. At the 2026-08-27 pre-payment planning prices, AD3 + one Pico 2 + UT61E+ is approximately ¥3,787.85 before cheap stock, versus ¥8,279.23 for AD3 + SDS824X HD + UT61E+; about ¥4,491 of capital can be deferred before the first physical bridge. These are planning coordinates, not current quotations.

This does **not** reject SDS824X HD from the long-horizon first-order portfolio. It remains a stronger independent benchtop observer for later cross-instrument measurement-adequacy work, higher-bandwidth consumers, and cases where AD3's own measurement boundary becomes the object under test.

The practical distinction is:

```text
PortfolioApproved
!= DeletionEssentialForFirstPhysicalContact
```

This audit also sharpens acquisition staging: the first payment need not materialize every already-approved first-order carrier before Reality contact begins.
