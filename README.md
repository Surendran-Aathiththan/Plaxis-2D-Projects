# PLAXIS 2D Projects

Geotechnical finite-element models built in **PLAXIS 2D 2025**: a circular footing settlement analysis and a sheet-pile shoring wall in layered soil.

| Project | Model type | Soil model | Status |
|---|---|---|---|
| [L01: Circular footing on sand](L01) | Axisymmetric, 15-noded | Mohr-Coulomb | ✅ Calculated (180 steps) |
| [2D 01: Sheet-pile shoring wall with ground anchor](2D%2001) | Plane strain, 15-noded | Hardening Soil | 🚧 Geometry and materials done; phases pending |

## L01: Circular footing on sand

A 1 m radius rigid footing on a 4 m sand layer (E′ = 13 MPa, φ′ = 30°, c′ = 1 kPa), loaded by a prescribed 50 mm settlement. It follows Lesson 1 of the PLAXIS 2D tutorial and includes mesh generation, a K<sub>0</sub> initial phase and a completed plastic calculation. [Read more →](L01)

## 2D 01: Sheet-pile shoring wall

A temporary 12 m sheet-pile wall with a ground anchor at 1.5 m depth, retaining six soil layers to 20 m depth with the groundwater head at −4 m.

| Layer | Depth (m) | E<sub>50</sub><sup>ref</sup> (kN/m²) | c′ (kPa) | φ′ (°) |
|---|---|---|---|---|
| Fill | 0 to −0.5 | 10,000 | 1 | 27 |
| Loose sand | −0.5 to −2 | 15,000 | 0 | 30 |
| Medium dense sand | −2 to −9 | 30,000 | 0 | 35 |
| Dense sand | −9 to −14 | 60,000 | 0 | 37 |
| Firm clay | −14 to −15 | 7,000 | 3 | 27 |
| Stiff to hard clay | −15 to −20 | 40,000 | 5 | 28 |

The wall is modelled as a plate with positive and negative interfaces (R<sub>inter</sub> = 0.33) to capture soil–structure interaction. Full parameters, completed steps and next steps are in the [project README](2D%2001/readme.md).

## Skills demonstrated

- Choosing between axisymmetric and plane-strain models
- Selecting constitutive models (Mohr-Coulomb, Hardening Soil) and deriving parameters (E<sub>ur</sub> = 3E<sub>50</sub>, ψ = φ′ − 30°)
- Modelling groundwater, structural plates and soil–structure interfaces
- Mesh generation, initial stresses (K<sub>0</sub> procedure) and staged plastic calculations

## Opening the files

Open the `.p2dx` files in **PLAXIS 2D (2024 or later)** and keep each `.p2dxdat` folder next to its `.p2dx` file. The `.p2dx` files are also plain-text command logs that show every modelling step.

## Reference

`PLAXIS_2D_1_Tutorial Manual.pdf` is Bentley/Seequent's tutorial manual, kept for reference. It is not my own work.
