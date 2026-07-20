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


<img width="50%" src="https://github.com/user-attachments/assets/88709813-cee3-48f1-a28f-f9d35050c6cc" />
<img width="50%" src="https://github.com/user-attachments/assets/d0ba0c32-92ef-4993-b0d2-f9650b690ce1" />



Shoring system (temporary structure used to support existing buildings):
Structure > Create line > Create plate - For model sheet pile wall   12m depth
Select Line > Create positive,negative interface  - To simulate soil interaction

Create start point of ground anchor on shoring wall - depth 1.5m


  
