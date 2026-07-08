  # Plaxis 2D 01

Project Properties : Set Contour x -20 to 10 , y: -30 to 10

Fill:
Soil model: Hardening soil
Unit weight unsaturated: 18 , Sat: 19
E ref 50 : 10000 
E ref ur : 3 x E ref 50
C' = 1
phi = 27
interface : R inter : 0.33 [Roughness interaction]


Dense Sand:
Soil model: Hardening soil
Unit weight unsaturated: 19 , Sat: 21
E ref 50 : 60000 
E ref ur : 3 x E ref 50
C' = 0
phi = 37
psi = phi - 30  = 07
interface : R inter : 0.33 [Roughness interaction]

Medium Dense Sand :
Soil model: Hardening soil
Unit weight unsaturated: 17 , Sat: 20
E ref 50 : 30000 
E ref ur : 3 x E ref 50
C' = 0
phi = 35
psi = phi - 30  = 05
interface : R inter : 0.33 [Roughness interaction]

Loose Sand:
Soil model: Hardening soil
Unit weight unsaturated: 15 , Sat: 18
E ref 50 : 15000 
E ref ur : 3 x E ref 50
C' = 0
phi = 30
psi = phi - 30  = 0
interface : R inter : 0.33 [Roughness interaction]

Firm Clay:
Soil model: Hardening soil
Unit weight unsaturated: 18 , Sat: 18
E ref 50 : 7000 
E ref ur : 3 x E ref 50
C' = 3
phi = 27
psi = phi - 30  = 0
interface : R inter : 0.33 [Roughness interaction]


Stiff to Hard Clay:
Soil model: Hardening soil
Unit weight unsaturated: 20 , Sat: 20
Young’s Modulus(MPa) E ref 50 : 40000 
E ref ur : 3 x E ref 50
Cohesion (kPa)-C' = 5
Friction Angle (degrees) phi = 28
psi = phi - 30  = 0
interface : R inter : 0.33 [Roughness interaction]



  