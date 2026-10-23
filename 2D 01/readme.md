# Sheet-Pile Shoring Wall with Ground Anchor (PLAXIS 2D)

A plane-strain finite-element model of a temporary shoring system, a sheet-pile wall with a ground anchor, used to support an excavation next to existing buildings in layered sand and clay.

**Status:** 🚧 In progress. Soil profile, material sets, groundwater and the wall are modelled. The anchor, excavation phases, mesh and calculation are still to be completed.

<img width="48%" alt="PLAXIS 2D model screenshot" src="https://github.com/user-attachments/assets/88709813-cee3-48f1-a28f-f9d35050c6cc" />
<img width="48%" alt="PLAXIS 2D model screenshot" src="https://github.com/user-attachments/assets/d0ba0c32-92ef-4993-b0d2-f9650b690ce1" />

## Model set-up

| Item | Value (from `Example 01.p2dx`) |
|---|---|
| Software | PLAXIS 2D 2025.1 |
| Model type | Plane strain, 15-noded triangular elements |
| Model boundaries | x = −20 m to +10 m, y = −30 m to +10 m |
| Groundwater | Borehole head at −4.0 m; firm clay and stiff clay layers set to dry |
| Wall | Plate from 0 to −11.8 m (≈ 12 m sheet pile) with positive and negative interfaces |
| Anchor | Anchor point created on the wall at −1.5 m |

## Soil profile and parameters

All layers use the **Hardening Soil (HS)** model with E<sub>ur</sub><sup>ref</sup> = 3 × E<sub>50</sub><sup>ref</sup> and interface strength R<sub>inter</sub> = 0.33.

| Layer | Depth (m) | γ<sub>unsat</sub> / γ<sub>sat</sub> (kN/m³) | E<sub>50</sub><sup>ref</sup> (kN/m²) | c′ (kPa) | φ′ (°) | ψ (°) |
|---|---|---|---|---|---|---|
| Fill | 0 to −0.5 | 18 / 19 | 10,000 | 1 | 27 | 0 |
| Loose sand | −0.5 to −2 | 15 / 18 | 15,000 | 0 | 30 | 0 |
| Medium dense sand | −2 to −9 | 17 / 20 | 30,000 | 0 | 35 | 5 (intended) |
| Dense sand | −9 to −14 | 19 / 21 | 60,000 | 0 | 37 | 7 |
| Firm clay | −14 to −15 | 18 / 18 | 7,000 | 3 | 27 | 0 |
| Stiff to hard clay | −15 to −20 | 20 / 20 | 40,000 | 5 | 28 | 0 |

Dilatancy follows ψ = φ′ − 30° for sands (ψ = 0 when φ′ ≤ 30°).

## Modelling steps completed

1. Set the project properties and model boundaries.
2. Created six soil material sets (Hardening Soil) and assigned them to the borehole layers.
3. Set the groundwater head and dry clay layers.
4. Modelled the sheet-pile wall as a plate with positive and negative interfaces to capture soil–structure interaction.
5. Created the start point of the ground anchor on the wall at 1.5 m depth.

## Next steps

- Add the anchor (node-to-node anchor + embedded grout body) and pre-stress
- Define staged-construction phases: wall installation → excavation stages → anchor activation
- Generate the mesh, calculate, and report wall deflection, bending moment, anchor force and a safety factor (φ–c reduction)

## Review note

In the saved model the medium dense sand has ψ = **30°**; the intended value from ψ = φ′ − 30° is **5°**. This should be corrected before the calculation.

## Files

| File | Description |
|---|---|
| `Example 01.p2dx` | PLAXIS 2D project file (also a readable command log) |
| `Example 01.p2dxdat/` | PLAXIS project data folder (keep it next to the `.p2dx` file) |

Open `Example 01.p2dx` in PLAXIS 2D (2024 or later).
