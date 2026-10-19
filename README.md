# PLAXIS 2D Projects

Geotechnical finite-element models built in **PLAXIS 2D**.

## Projects

### [2D 01 – Sheet-pile shoring wall with ground anchor](2D%2001)

A temporary shoring system to support an excavation next to existing buildings.

- **Model domain:** x = −20 to 10 m, y = −30 to 10 m
- **Soil model:** Hardening Soil (HS) for every layer, with E<sub>ur</sub><sup>ref</sup> = 3 × E<sub>50</sub><sup>ref</sup> and R<sub>inter</sub> = 0.33
- **Structure:** 12 m deep sheet-pile wall modelled as a plate, with positive and negative interfaces to capture soil–structure interaction
- **Support:** ground anchor starting 1.5 m below the top of the wall

| Layer | γ<sub>unsat</sub> / γ<sub>sat</sub> (kN/m³) | E<sub>50</sub><sup>ref</sup> (kN/m²) | c′ (kPa) | φ′ (°) | ψ (°) |
|---|---|---|---|---|---|
| Fill | 18 / 19 | 10,000 | 1 | 27 | – |
| Dense sand | 19 / 21 | 60,000 | 0 | 37 | 7 |
| Medium dense sand | 17 / 20 | 30,000 | 0 | 35 | 5 |
| Loose sand | 15 / 18 | 15,000 | 0 | 30 | 0 |
| Firm clay | 18 / 18 | 7,000 | 3 | 27 | 0 |
| Stiff to hard clay | 20 / 20 | 40,000 | 5 | 28 | 0 |

Full modelling notes and screenshots are in the [project readme](2D%2001/readme.md).

### [L01](L01)

A PLAXIS 2D model with a complete mesh and calculation run.

## Opening the files

Open the `.p2dx` files in **PLAXIS 2D** (CONNECT Edition or later). The reference tutorial manual is included as `PLAXIS_2D_1_Tutorial Manual.pdf`.
