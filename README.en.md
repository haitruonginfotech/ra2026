# Ra2026 — Red Alert 2 & Yuri's Revenge portable + mod tools

[Tiếng Việt](README.md) · **English**

A **portable** setup for Red Alert 2 + Yuri's Revenge: the game **writes nothing to the Windows registry or outside its own folder**. Also included:

- 📘 **Player handbook** (Vietnamese PDF, 24 pages): 3 factions, 10 countries, illustrated units & buildings, superweapons, hotkeys, tricks.
- 🛠️ **RA2 Mod Editor**: an offline web page for editing the game rules (`rulesmd.ini` / `rules.ini`) visually.
- 🔍 **Malware scan notes** for the original repack.

> **This repo contains no game files.** You need your own copy of Red Alert 2 + Yuri's Revenge. Some files in `AI/` contain data extracted from the game (rules `.ini` files, icons in the Mod Editor, images in the handbook), which is copyrighted by EA.

---

## 1. Layout

The repository root **is the game folder** (on the author's machine: `E:\games\Ra2\Ra2026`).

| Path | Contents |
|---|---|
| `Play_YR.exe` | Launches Yuri's Revenge |
| `Play_RA2.exe` | Launches Red Alert 2 |
| `BINKW32.DLL` | Write guard: virtual registry + blocks file writes outside the folder |
| `AI/guide/guide-20261102-vi.pdf` | Player handbook (current) |
| `AI/tools/RA2_Mod_Editor.html` | Rules editor |
| `AI/tools/src/` | Source: `portable-guard`, `mod-editor`, `guide` |
| `AI/mod/` | Reference rules: official & modded, both games |
| `AI/security/20261030/findings.md` | Malware scan results |
| `AI/AI_HANDOFF.md`, `AI/PROJECT_RULES.md` | Detailed status & project rules |

Every other game file in the folder is ignored by `.gitignore`.

## 2. Differences from the original

Byte-for-byte comparison with the original repack: **296 game files unchanged**. The repo contains only what was modified or added:

| Type | Files | In git |
|---|---|---|
| Modified | `BINKW32.DLL` (replaced by the write guard) | ✅ |
| Added | `Play_RA2.exe`, `Play_YR.exe`, `README.md`, `README.en.md`, `.gitignore`, `AI/` (23 files) | ✅ |
| Renamed (original content) | original `BINKW32.DLL` → `binkw32_o.dll`; `cnc-ddraw config.exe` → `cnc-ddraw config.exe.disabled` | ❌ (third-party files) |
| Removed | `keygen\` (Keygen.exe, RegSetup.exe, fdxra2k.nfo), `LAN-play-serials\` (4× ra2.reg + Woldata.key), `Ra2.exe`, `RA2MD.exe`, `YURI.exe`, `RegSetup.exe`, `SetupReg.exe`, `uninstal.exe`, `uninstal.ini`, `DRVMGT.DLL`, `PATCHGET.DAT`, `patchgetmd.dat`, `PATCHW32.DLL`, `src.7z`, `aqrit.cfg` | ❌ |

## 3. Install

1. Clone the repo into the folder that will hold the game:
   ```
   git clone https://github.com/haitruonginfotech/ra2026.git Ra2026
   ```
2. Copy all Red Alert 2 + Yuri's Revenge files into `Ra2026\` **except**: `keygen\`, `LAN-play-serials\`, `RegSetup.exe`, `SetupReg.exe`, `uninstal.exe/.ini`, `DRVMGT.DLL`, `PATCHGET.DAT`, `patchgetmd.dat`, `PATCHW32.DLL`, `src.7z`, `aqrit.cfg`, `Ra2.exe`, `RA2MD.exe`, `YURI.exe`.
3. **Do not** overwrite the repo's `BINKW32.DLL`: save the game's own `BINKW32.DLL` as `binkw32_o.dll`.
4. Rename `cnc-ddraw config.exe` to `cnc-ddraw config.exe.disabled`.

## 4. Playing

- Double-click `Play_YR.exe` (Yuri's Revenge) or `Play_RA2.exe` (Red Alert 2).
- **Do not** start `game.exe` / `gamemd.exe` directly: the game exits immediately.
- Registry data the game "writes" is kept in `portable\registry.txt`. Every blocked write outside the folder is logged in `portable\blocked.log`.
- To uninstall, delete the folder.

### Windows 11

The project works on Windows 10 and 11 (64-bit, ARM PCs included). `BINKW32.DLL` and `Play_*.exe` only call libraries present in every Windows version (kernel32, advapi32, user32, msvcrt). Notes:

- **No** compatibility mode or *Run as administrator* is needed. Turn them off if set: the portable build does not need admin rights.
- Keep the game folder on its own drive (e.g. `E:\games\Ra2\Ra2026`). **Do not** put it in `C:\Program Files` (writes are blocked) or a OneDrive folder (Desktop/Documents are often synced by OneDrive).
- **SmartScreen:** if you download the repo as a ZIP, Windows may show “Windows protected your PC” when opening `Play_*.exe`. Click *More info → Run anyway*, or right-click the ZIP → *Properties → Unblock* before extracting. Cloning with `git` avoids this.
- **Smart App Control** (on by default only on clean installs of Windows 11 22H2+) can block unsigned executables outright: the self-built `Play_*.exe`, and the repack's `game.exe`/`gamemd.exe`. Check *Windows Security → App & browser control → Smart App Control*; it must be Off to play.
- **Microsoft Defender** may flag `BINKW32.DLL` because it patches the game's import table (to block writes). If it is quarantined, restore it and add the `Ra2026` folder to *Exclusions*. Source code is in `AI/tools/src/portable-guard/`.
- **Black screen / crash after changing resolution:** open the Mod Editor → **Hiệu năng** (Performance) → change the renderer (Direct3D 9 ↔ OpenGL ↔ GDI).
- Mod Editor: use Edge (built in) or Chrome. Bahnschrift/Segoe UI fonts ship with Windows 11.

## 5. Editing the rules (modding)

1. Open `AI\tools\RA2_Mod_Editor.html` in **Chrome** or **Edge**.
2. Click **Mở thư mục game** (Open game folder) and choose the `Ra2026` folder (the one containing `gamemd.exe`).
3. Pick a rule set: the bundled mod or the official rules.
4. Edit cost, strength, speed, weapons, superweapons, general rules… or use **Mod nhanh** (quick mod).
5. Click **Lưu vào game** (Save to game), then start `Play_YR` / `Play_RA2` to test.

`Ctrl+Z` undoes. Previous files are backed up in `mod_backups\`. **Khôi phục…** (Restore) returns the game to the official or the bundled mod rules. LAN play: every PC must use the same rules file.

### Reducing lag in big battles

The RA2/YR engine runs the game logic on **a single thread**, so large battles stutter no matter how many CPU cores you have. In the Mod Editor, click **Hiệu năng** (Performance):

- **Display** (`ddraw.ini`, shared by both games): Direct3D 9 renderer, 60 FPS cap, V-Sync, let the renderer run on another CPU core (`singlecpu=false`), screen mode.
- **In-game settings** (`RA2MD.INI` / `RA2.INI`): resolution, detail level. Quit the game before applying.
- **Rules**: reduce or remove explosion debris, let the game drop effects sooner when FPS falls, remove smoke/fire on damaged buildings.

**Đề xuất cho trận đông quân** (Recommended for big battles) fills in suggested values. **Áp dụng** (Apply) writes the config files straight into the game folder (old copies go to `mod_backups\`); rule changes go through **Lưu vào game** (Save to game) and can be undone with `Ctrl+Z`. If the game hangs or crashes with multiple CPU cores enabled, switch it back to “Không” (No).

> **Note:** the repack ships with mods. RA2 uses a loose `rules.ini`; Yuri's Revenge uses `expandmd03.mix` (about 3× faster building, 100% sell refund, 51 new units, Harrier removed). The PDF handbook describes the **official** rules.

## 6. Rebuilding from source

See [`AI/tools/src/README.md`](AI/tools/src/README.md): mingw-w64 for the DLL/EXEs, Python + Playwright for the handbook, `template.html` + data for the Mod Editor.

---

## 7. Changelog

### 2026-11-02
- 🪟 **Windows 11** notes (SmartScreen, Smart App Control, Defender, renderer); re-tested under Wine reporting Windows 11.
- 🖥️ Mod Editor fits more screens: at 1024–1439 px the button bar wraps to 2 rows (before, **Lưu vào game** was pushed off-screen at 1024 px); 1920+ px shows 6–7 fields per row.
- ⚡ **Mod Editor → Performance**: edit `ddraw.ini` (renderer, FPS cap, V-Sync, multi-core, screen mode), resolution and detail level in `RA2MD.INI`/`RA2.INI`, and cut debris/effects in the rules; written straight to the files with backups. Includes a recommended preset for big battles.
- 🏷️ Version milestone `v2026.11.02` (baseline) to roll back to.
- 📋 The repo keeps only files **modified or added** compared with the original (byte-checked: 296 game files unchanged); added a differences table in section 2.
- 🔁 **Repository root changed to the `Ra2026` game folder**: `BINKW32.DLL` and `Play_*.exe` sit at the root, `AI/` next to the game files; `.gitignore` allows only project files.
- 📝 README renamed to `README.md` (VI) and `README.en.md` (EN) so it no longer clashes with the game's own `Readme.txt` (Windows file names are case-insensitive).
- 🌐 GitHub: EN+VI description and 20 topics for SEO; source, tools and documents published to the repo.
- ➕ `.gitignore` and bilingual README with guide and changelog.
- 📁 Moved documents, tools and source into `AI/` (per the `CLAUDE.md` v5.7 policy); added `AI_HANDOFF.md`, `PROJECT_RULES.md`, `security/20261030/findings.md`.
- 🛠️ **RA2 Mod Editor**: edits all YR & RA2 rules, real unit icons, quick mods, undo, unit cloning, backup & restore.
- ⚠️ Found that Yuri's Revenge is modded via `expandmd03.mix` (earlier reported as stock by mistake); handbook corrected to `guide-20261102-vi.pdf`.
- ➕ Reference rules under `AI/mod/`.

### 2026-10-31
- 📘 Player handbook PDF (26 pages).
- 🖨️ Ink-saving print edition (24 pages): no cover, white background; icons in the quick-reference table, tech-building images, new **Tricks** chapter.
- ➕ Extracted the official `rulesmd.ini` for manual modding.

### 2026-10-30
- 🔍 Static malware scan of the repack: no malware found; the keygen's HackTool detection by antivirus software is a crack-tool warning.
- 🎮 Built the portable setup: `BINKW32.DLL` guard (virtual registry, blocks writes outside the folder), `Play_RA2.exe` / `Play_YR.exe` launchers; removed keygen, setup tools, SafeDisc driver, original launchers; disabled cnc-ddraw config.
- ✅ Tested under Wine: the games start without writing to the registry or outside the folder.

## 8. Not yet verified

- Running the game on real Windows 11 with the guard installed. Tested under Wine reporting Windows 11 (build 22000): YR and RA2 start via `Play_*.exe`, registry goes to `portable\registry.txt`, nothing is written outside the folder. Wine is no substitute for real Windows (graphics, Defender, Smart App Control).
- The Mod Editor's Open folder / Save / Restore / Performance buttons in real Chrome/Edge (tested with a simulated folder in Chromium).
- The real-world lag reduction of each Performance option; removing building smoke/fire has not been tried in-game.

Details: [`AI/AI_HANDOFF.md`](AI/AI_HANDOFF.md).
