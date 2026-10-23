# L01: Settlement of a Circular Footing on Sand (PLAXIS 2D)

An axisymmetric model of a rigid circular footing pushed into a sand layer, built by following Lesson 1 of the PLAXIS 2D tutorial manual. It was my first complete PLAXIS model: geometry, material, mesh, phases and calculation.

**Status:** ✅ Complete. The calculation finished successfully (180 load steps).

## Model

| Item | Value (from `L01.p2dx`) |
|---|---|
| Software | PLAXIS 2D 2025.1 |
| Model type | **Axisymmetric**, 15-noded elements |
| Soil domain | 5 m (radius) × 4 m (depth) |
| Groundwater | Head at 2 m above the base of the model |
| Footing | Rigid footing of 1 m radius, modelled as a prescribed vertical displacement u<sub>y</sub> = −0.05 m with horizontal movement fixed |
| Mesh | Medium mesh (relative element size 0.06) |

## Soil: Mohr-Coulomb sand

| γ<sub>unsat</sub> / γ<sub>sat</sub> (kN/m³) | E′ (kN/m²) | ν′ | c′ (kPa) | φ′ (°) |
|---|---|---|---|---|
| 17 / 20 | 13,000 | 0.3 | 1 | 30 |

## Calculation phases

1. **Initial phase:** K<sub>0</sub> procedure to generate the initial stresses.
2. **Phase 1:** plastic calculation with the prescribed footing displacement activated (180 steps, completed without errors).

## Key concepts

- **Axisymmetric model:** a 2D model of a 3D circular problem (piles, shafts, circular footings), using radial symmetry about the left boundary.
- **Plane strain:** assumes the structure is infinitely long (retaining walls, embankments, tunnels, strip footings).
- **15-noded element:** a high-order triangular element that gives accurate stresses and failure loads.

## Next steps

Export the load–displacement curve and compare the footing bearing capacity with a hand calculation (Terzaghi / Meyerhof).

## Files

Open `L01.p2dx` in PLAXIS 2D (2024 or later); keep the `L01.p2dxdat/` folder next to it. Results can be viewed in PLAXIS Output without recalculating.
