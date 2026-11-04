# Đối chiếu chỉ số RA Reborn ↔ luật gốc

Nguồn: `rulesmd-official-yr.ini`. Chỉ xét mục xây được (TechLevel 1–10).

- Quân/công trình lệch chỉ số: **24** (34 giá trị)
- Vũ khí lệch: **17** (51 giá trị)
- Chưa có trong RA Reborn: **41**

## Quân / công trình

| Loại | Mã | Tên | Thuộc tính | Gốc | RA Reborn |
|---|---|---|---|---|---|
| Bộ binh | ENGINEER | Engineer | Armament.primary | DefuseKit | None |
| Bộ binh | ENGINEER | Engineer | Armament.secondary | VirtualScanner | None |
| Bộ binh | GHOST | SEAL | Armament.secondary | Sapper | MP5, MP5E |
| Bộ binh | YURI | Yuri Clone | Armament.secondary | PsiWave | MindControl |
| Bộ binh | DESO | Desolater | Armament.secondary | RadEruptionWeapon | RadBeamWeapon, RadBeamWeaponE |
| Bộ binh | DOG | Attack Dog | Armament.primary | BadTeeth | DogJaw |
| Bộ binh | DOG | Attack Dog | Armament.secondary | VirtualScanner | DogJaw |
| Bộ binh | CLEG | Chrono Legionnaire | Armament.eliteprimary | NeutronRifleE | NeutronRifle |
| Bộ binh | SPY | Spy | Armament.primary | MakeupKit | None |
| Bộ binh | CCOMAND | Chrono Commando | Armament.primary | ChronoMP5 | MP5, MP5E |
| Bộ binh | CCOMAND | Chrono Commando | Armament.secondary | FakeC4 | MP5, MP5E |
| Bộ binh | CCOMAND | Chrono Commando | Armament.eliteprimary | ChronoMP5E | MP5, MP5E |
| Bộ binh | PTROOP | Psi-Corp Trooper | Armament.eliteprimary | MindControlE | MindControl |
| Bộ binh | YURIPR | Yuri Prime | Armament.secondary | SuperPsiWave | SuperMindControl |
| Bộ binh | TANY | Tanya | Armament.secondary | Sapper | DoublePistols, DoublePistolsE |
| Bộ binh | TANY | Tanya | Armament.elitesecondary | Sapper | DoublePistols, DoublePistolsE |
| Bộ binh | TERROR | Terrorist | Armament.primary | TerrorBomb | DemoTruckTargeting |
| Xe & tàu | DRON | Terror Drone | Armament.secondary | VirtualScanner | DroneJump |
| Xe & tàu | HTK | Flak Track | Armament.eliteprimary | FlakTrackGunE | FlakTrackAAGun, FlakTrackGun |
| Xe & tàu | HTK | Flak Track | Armament.elitesecondary | FlakTrackAAGunE | FlakTrackAAGun, FlakTrackGun |
| Xe & tàu | AEGIS | Aegis Cruiser | Armament.eliteprimary | MedusaE | Medusa |
| Xe & tàu | SHAD | BlackHawk Transport | Armament.eliteprimary | BlackHawkCannonE | BlackHawkCannon |
| Xe & tàu | SQD | Giant Squid | Armament.primary | SquidGrab | SquidPunch |
| Xe & tàu | SQD | Giant Squid | Armament.eliteprimary | SquidGrabE | SquidPunch |
| Xe & tàu | SQD | Giant Squid | Armament.elitesecondary | SquidPunchE | SquidPunch |
| Xe & tàu | DLPH | Dolphin | Armament.eliteprimary | SonicZapE | SonicZap |
| Xe & tàu | CMIN | Chrono Miner | Armament.primary | none | None |
| Xe & tàu | HYD | Sea Scorpion | Armament.eliteprimary | FlakTrackGunE | FlakTrackGun, FlakWeapon |
| Xe & tàu | HYD | Sea Scorpion | Armament.elitesecondary | FlakWeaponE | FlakTrackGun, FlakWeapon |
| Xe & tàu | DTRUCK | Demolitions Truck | Armament.primary | Demobomb | DemoTruckTargeting |
| Xe & tàu | DTRUCK | Demolitions Truck | Armament.secondary | none | DemoTruckTargeting |
| Máy bay | ORCA | Intruder | Armament.eliteprimary | MaverickE | Maverick |
| Máy bay | BEAG | Black Eagle | Armament.eliteprimary | Maverick2E | Maverick2 |
| Công trình | ATESLA | Allied Prism Cannon | Armament.secondary | PrismSupport | PrismShot |

## Vũ khí

Vũ khí đánh dấu ⚙️ có cơ chế riêng trong OpenRA (sạc điện, điều khiển tâm trí, nhảy…): không tự sửa.

| Vũ khí | Quân dùng | Thuộc tính | Gốc | RA Reborn |
|---|---|---|---|---|
| ⚙️ AssaultBolt | SHK | Damage | 10 | None |
| ⚙️ AssaultBolt | SHK | ReloadDelay | 25 | 70 |
| ⚙️ AssaultBolt | SHK | Range | 1c850 | 2c0 |
| ⚙️ AssaultBolt | SHK | Versus.None | 0 | 100 |
| ⚙️ AssaultBolt | SHK | Versus.Flak | 0 | 100 |
| ⚙️ AssaultBolt | SHK | Versus.Plate | 0 | 100 |
| ⚙️ AssaultBolt | SHK | Versus.Light | 0 | 100 |
| ⚙️ AssaultBolt | SHK | Versus.Medium | 0 | 100 |
| ⚙️ AssaultBolt | SHK | Versus.Heavy | 0 | 100 |
| ⚙️ AssaultBolt | SHK | Versus.Drone | 50 | 100 |
| ⚙️ MindControl | YURI | Damage | 1 | 0 |
| ⚙️ MindControl | YURI | Versus.Wood | 0 | 100 |
| ⚙️ MindControl | YURI | Versus.Steel | 0 | 100 |
| ⚙️ MindControl | YURI | Versus.Concrete | 0 | 100 |
| ⚙️ IvanBomber | IVAN | Damage | 400 | None |
| ⚙️ IvanBomber | IVAN | Range | 1c512 | 1c849 |
| ⚙️ IvanBomberE | IVAN | Damage | 600 | None |
| ⚙️ IvanBomberE | IVAN | Range | 1c512 | 1c849 |
| ⚙️ NeutronRifle | CLEG | Versus.Rocket | 0 | 100 |
| ⚙️ SuperMindControl | YURIPR | Damage | 1 | 0 |
| ⚙️ SuperMindControl | YURIPR | Range | 7c0 | 30c0 |
| ⚙️ HornetLauncher | CARRIER | Damage | 1 | None |
| ⚙️ HornetLauncher | CARRIER | ReloadDelay | 150 | 30 |
| ⚙️ BlimpBomb | ZEP | Range | 1c512 | 0c256 |
| ⚙️ BlimpBombE | ZEP | Range | 1c512 | 0c256 |
| ⚙️ DroneJump | DRON | Damage | 50 | 200 |
| ⚙️ DroneJump | DRON | ReloadDelay | 60 | 10 |
| ⚙️ DroneJump | DRON | Range | 1c850 | 3c0 |
| ⚙️ DroneJump | DRON | Versus.Light | 100 | 0 |
| ⚙️ DroneJump | DRON | Versus.Medium | 100 | 0 |
| ⚙️ DroneJump | DRON | Versus.Heavy | 100 | 0 |
| ⚙️ ASWLauncher | DEST | Damage | 1 | None |
| ⚙️ ASWLauncher | DEST | Range | -2c0 | 8c0 |
| ⚙️ Medusa | AEGIS | ReloadDelay | 15 | 100 |
| ⚙️ SquidPunch | SQD | Damage | 100 | 50 |
| ⚙️ SquidPunch | SQD | Range | 1c850 | 1c856 |
| ⚙️ SquidPunch | SQD | Versus.Light | 70 | 100 |
| ⚙️ SquidPunch | SQD | Versus.Medium | 70 | 100 |
| ⚙️ SquidPunch | SQD | Versus.Heavy | 35 | 100 |
| ⚙️ SquidPunch | SQD | Versus.Wood | 75 | 100 |
| ⚙️ SquidPunch | SQD | Versus.Steel | 40 | 100 |
| ⚙️ SquidPunch | SQD | Versus.Concrete | 20 | 100 |
| ⚙️ SquidPunch | SQD | Versus.Drone | 80 | 100 |
| ⚙️ SonicZap | DLPH | ReloadDelay | 120 | 180 |
| ⚙️ SonicZap | DLPH | Versus.Medium | 80 | 100 |
| ⚙️ SonicZap | DLPH | Versus.Steel | 60 | 100 |
| ⚙️ CoilBolt | TESLA | ReloadDelay | 80 | 3 |
| ⚙️ CoilBolt | TESLA | Range | 7c0 | 8c0 |
| ⚙️ OPCoilBolt | TESLA | ReloadDelay | 80 | 3 |
| ⚙️ OPCoilBolt | TESLA | Range | 8c0 | 8c512 |
| ⚙️ PrismShot | ATESLA | ReloadDelay | 45 | 1 |

## Chưa có

| Loại | Mã | Tên |
|---|---|---|
| Bộ binh | SENGINEER | Soviet Engineer |
| Bộ binh | ADOG | Allied Attack Dog |
| Bộ binh | YENGINEER | Yuri Engineer |
| Bộ binh | GGI | Guardian GI |
| Bộ binh | INIT | Yuri Initiate |
| Bộ binh | BORIS | Boris |
| Bộ binh | BRUTE | Yuri Brute |
| Bộ binh | VIRUS | Yuri Virus |
| Bộ binh | YDOG | Attack Dog (Yuri version) |
| Bộ binh | YADOG | Allied Attack Dog (Yuri version) |
| Xe & tàu | V3 | V3 Launcher |
| Xe & tàu | DRED | Dreadnought |
| Xe & tàu | LTNK | Lasher Light Tank |
| Xe & tàu | YHVR | Hover Transport Yuri |
| Xe & tàu | PCV | Yuri Construction Vehicle |
| Xe & tàu | SMIN | Slave Miner |
| Xe & tàu | YTNK | Gattling Tank |
| Xe & tàu | BFRT | Battle Fortress |
| Xe & tàu | TELE | Magnetron |
| Xe & tàu | CAOS | Chaos Drone |
| Xe & tàu | BSUB | Yuri Boomer |
| Xe & tàu | SCHP | Soviet Siege Chopper |
| Xe & tàu | MIND | Master Mind |
| Xe & tàu | DISK | Floating Disk |
| Xe & tàu | ROBO | Robot Tank |
| Công trình | YAPOWR | Yuri Bio Reactor |
| Công trình | YABRCK | Yuri Barracks |
| Công trình | YAWEAP | Yuri War Factory |
| Công trình | YAYARD | Yuri Submarine Pen |
| Công trình | YATECH | Yuri Battle Lab |
| Công trình | GAFWLL | Yuri Citadel Wall |
| Công trình | YAGGUN | Yuri Gattling Cannon |
| Công trình | YAPSYT | Yuri Psychic Tower |
| Công trình | NAINDP | Soviet Industrial Plant |
| Công trình | YAGRND | Yuri Grinder |
| Công trình | YAGNTC | Yuri Genetic Mutator Device |
| Công trình | YAPPET | Yuri Puppet Master |
| Công trình | NATBNK | Yuri Tank Bunker |
| Công trình | GAROBO | Allied Robot Control Center |
| Công trình | YAREFN | Yuri Ore Refinery |
| Công trình | NABNKR | Soviet Battle Bunker |
