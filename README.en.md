# RA Reborn — Red Alert 2 + Yuri's Revenge on the OpenRA engine

[Tiếng Việt](README.md) · **English**

The project's **own** real-time strategy game, built on [OpenRA](https://github.com/OpenRA/OpenRA) (open-source engine, GPLv3) and developed from the [OpenRA Red Alert 2 mod](https://github.com/OpenRA/ra2). Goal: play like Red Alert 2 + Yuri's Revenge, but with everything moddable — e.g. **4 veterancy ranks**.

> **No EA game files included.** Art and audio are, for now, read from your own Red Alert 2 + Yuri's Revenge copy. EA has not endorsed and does not support this project.
>
> The old Ra2026 project (portable build + Mod Editor + handbook) lives on branch [`ra2026-legacy`](https://github.com/haitruonginfotech/ra2026/tree/ra2026-legacy).

## 1. Status

| Item | Status |
|---|---|
| OpenRA `release-20231010` + RA2 mod, renamed **RA Reborn** (`rareborn`) | ✅ builds, rules & sprite checks clean |
| Reads game files straight from the sibling `Ra2026` folder, adds Yuri's Revenge files | ✅ |
| **4 veterancy ranks**: Rookie · Bronze · Gold · Diamond (new insignia) | ✅ (not yet play-tested on Windows) |
| Allied & Soviet factions (10 countries) | ✅ from the RA2 mod |
| **Yuri faction** | 🚧 in progress (milestone 1a: all buildings & units, special mechanics simplified) |
| Yuri special mechanics (Grinder, Slave Miner, Gatling, Magnetron, Chaos, Genetic Mutator) | ⏳ milestone 1b |

## 2. Install (Windows 10/11)

### Option 1 — click and play (recommended)

1. Extract the portable build `RAReborn-<version>-win-x64-portable.zip` next to the game folder:
   ```
   E:\games\Ra2\Ra2026     ← RA2 + YR game files (ra2.mix, ra2md.mix, langmd.mix, expandmd01.mix…)
   E:\games\Ra2\RAReborn   ← portable build, contains RAReborn.exe
   ```
2. Double-click **`RAReborn.exe`**. No .NET install needed (bundled), nothing written to the registry.
3. Controls default to RA2 style (**Classic**: left-click selects and commands). Change in *Settings → Input → Control Scheme*. Deploy the MCV: select it, then click it again.

**Portable** mode: settings, saves and logs live in `RAReborn\Support`, nothing goes to AppData.

### Option 2 — run from source (developers)

1. `git clone https://github.com/haitruonginfotech/ra2026.git E:\games\Ra2\RAReborn-src` (next to `Ra2026`).
2. Install the [.NET 6 SDK](https://dotnet.microsoft.com/download/dotnet/6.0) (x64), run `make.cmd` → `all`, then `launch-game.cmd`.
3. Build the portable package (on Linux): `packaging/windows/build-portable.sh <version> <outdir>`.

> ⚠️ Do not `git pull` branch `main` inside the old `Ra2026` game folder: main is now RA Reborn and git would delete `BINKW32.DLL` and `Play_*.exe`. In `Ra2026` switch to the old branch: `git fetch origin`, then `git checkout -B ra2026-legacy origin/ra2026-legacy`.

## 3. Four veterancy ranks

| Rank | Insignia | Kills needed (cumulative, × own cost) | Bonus |
|---|---|---|---|
| 1 Rookie | — | 0 | — |
| 2 Bronze | 1 bronze chevron | 4× | firepower +10%, damage taken −10%, speed +10%, reload −10% |
| 3 Gold | 2 gold chevrons | 9× | +20%, −18%, +20%, −18%, better accuracy |
| 4 Diamond | diamond | 15× | +30%, −25%, +30%, −25%, self-heal, elite weapons |

Config: `mods/rareborn/rules/defaults.yaml` (`^GainsExperience`). Insignia: `artsrc/ranks/make_ranks.py` → `mods/rareborn/bits/ranks/`.

## 4. Layout

| Path | Contents |
|---|---|
| `mods/rareborn/` | Rules (`rules/`), weapons, art (`sequences/`), UI, maps |
| `OpenRA.Mods.RA2/` | Mod-specific C# (mind control, carriers, mirage…) |
| `artsrc/` | Art sources (rank insignia…) |
| `AI/` | Project status (`AI_HANDOFF.md`), rules (`PROJECT_RULES.md`) |
| `README.openra-ra2.md` | Original OpenRA RA2 mod README |

## 5. License

GPLv3 (same as OpenRA and the OpenRA RA2 mod), see `LICENSE`. Red Alert 2 / Yuri's Revenge game assets are © Electronic Arts.

## 6. Changelog

### 2026-11-04
- 🖱️ Portable build defaults to **Classic** controls (left-click commands, like RA2); Modern (right-click commands) made units look unresponsive.
- 🖱️ **Click-and-play Windows portable build** (`RAReborn.exe`, .NET bundled, 64-bit): script `packaging/windows/build-portable.sh`. Tested under Wine in Windows 11 mode: reaches the first-run setup screen, logs go to `RAReborn\Support` (portable).
- 💬 Startup notice renamed to “RA Reborn - early preview”.
- 🚀 Started **RA Reborn** on `main` from the OpenRA RA2 mod (upstream commit in `UPSTREAM_RA2_COMMIT`), engine `release-20231010`.
- 📦 Mod id `ra2` → `rareborn`; reads game files from `../Ra2026`; also mounts ra2md/langmd/expandmd01 and the nested YR mixes (mounted later so they override RA2).
- 🎖️ 4 veterancy ranks Rookie / Bronze / Gold / Diamond with new 16×16 insignia.
- 🗂️ The old Ra2026 project moved to branch `ra2026-legacy`.
