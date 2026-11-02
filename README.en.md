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

## 2. Install

1. Clone the repo into the folder that will hold the game:
   ```
   git clone https://github.com/haitruonginfotech/ra2026.git Ra2026
   ```
2. Copy all Red Alert 2 + Yuri's Revenge files into `Ra2026\` **except**: `keygen\`, `LAN-play-serials\`, `RegSetup.exe`, `SetupReg.exe`, `uninstal.exe/.ini`, `DRVMGT.DLL`, `PATCHGET.DAT`, `patchgetmd.dat`, `PATCHW32.DLL`, `src.7z`, `aqrit.cfg`, `Ra2.exe`, `RA2MD.exe`, `YURI.exe`.
3. **Do not** overwrite the repo's `BINKW32.DLL`: save the game's own `BINKW32.DLL` as `binkw32_o.dll`.
4. Rename `cnc-ddraw config.exe` to `cnc-ddraw config.exe.disabled`.

## 3. Playing

- Double-click `Play_YR.exe` (Yuri's Revenge) or `Play_RA2.exe` (Red Alert 2).
- **Do not** start `game.exe` / `gamemd.exe` directly: the game exits immediately.
- Registry data the game "writes" is kept in `portable\registry.txt`. Every blocked write outside the folder is logged in `portable\blocked.log`.
- To uninstall, delete the folder.

## 4. Editing the rules (modding)

1. Open `AI\tools\RA2_Mod_Editor.html` in **Chrome** or **Edge**.
2. Click **Mở thư mục game** (Open game folder) and choose the `Ra2026` folder (the one containing `gamemd.exe`).
3. Pick a rule set: the bundled mod or the official rules.
4. Edit cost, strength, speed, weapons, superweapons, general rules… or use **Mod nhanh** (quick mod).
5. Click **Lưu vào game** (Save to game), then start `Play_YR` / `Play_RA2` to test.

`Ctrl+Z` undoes. Previous files are backed up in `mod_backups\`. **Khôi phục…** (Restore) returns the game to the official or the bundled mod rules. LAN play: every PC must use the same rules file.

> **Note:** the repack ships with mods. RA2 uses a loose `rules.ini`; Yuri's Revenge uses `expandmd03.mix` (about 3× faster building, 100% sell refund, 51 new units, Harrier removed). The PDF handbook describes the **official** rules.

## 5. Rebuilding from source

See [`AI/tools/src/README.md`](AI/tools/src/README.md): mingw-w64 for the DLL/EXEs, Python + Playwright for the handbook, `template.html` + data for the Mod Editor.

---

## 6. Changelog

### 2026-11-02
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

## 7. Not yet verified

- Running the game on real Windows with the guard installed.
- The Mod Editor's Open folder / Save / Restore buttons in real Chrome/Edge.

Details: [`AI/AI_HANDOFF.md`](AI/AI_HANDOFF.md).
