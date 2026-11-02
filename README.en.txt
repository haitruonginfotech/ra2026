RA2026 — RED ALERT 2 & YURI'S REVENGE PORTABLE + MOD TOOLS
============================================================
English version. Bản tiếng Việt (mặc định): README.txt
Repo: https://github.com/haitruonginfotech/ra2026
Updated: 2026-11-02


1. OVERVIEW
-----------
This project turns a Red Alert 2 + Yuri's Revenge repack (taira2.org) into a
clean "portable" install called Ra2026: the game writes nothing to the Windows
registry or outside its own folder. Also included:
  - Player handbook (PDF, Vietnamese, 24 pages).
  - RA2 Mod Editor: an offline web page for editing game rules visually.
  - Malware scan notes for the original repack.

COPYRIGHT NOTE: the repo does NOT contain game files (game.exe, *.mix...).
Some files under AI\ contain data extracted from the game (rules .ini files,
icons in the Mod Editor and handbook). Keep the repository PRIVATE.


2. LAYOUT
---------
E:\games\Ra2\                       (repository root)
  README.txt / README.en.txt        Guide + changelog
  .gitignore                        Only project files are tracked
  Ra2026\                           Portable game folder (3 files tracked)
    Play_YR.exe                     Launches Yuri's Revenge
    Play_RA2.exe                    Launches Red Alert 2
    BINKW32.DLL                     Write guard (virtual registry + file-write blocking)
  AI\
    AI_HANDOFF.md                   Detailed status for the next person/agent
    PROJECT_RULES.md                Project rules
    guide\guide-20261102-vi.pdf     Player handbook (current, Vietnamese)
    tools\RA2_Mod_Editor.html       Rules editor
    tools\src\                      Source: portable-guard, mod-editor, guide
    mod\                            Reference rules: official & modded, both games
    security\20261030\findings.md   Malware scan results


3. HOW TO USE
-------------
3.1 Install from the repo (new machine)
  a) Have the Red Alert 2 + Yuri's Revenge game files (the repack).
  b) Copy all game files into Ra2026\ EXCEPT: keygen\, LAN-play-serials\,
     RegSetup.exe, SetupReg.exe, uninstal.exe/.ini, DRVMGT.DLL, PATCHGET.DAT,
     patchgetmd.dat, PATCHW32.DLL, src.7z, aqrit.cfg, Ra2.exe, RA2MD.exe, YURI.exe.
  c) Rename the game's BINKW32.DLL to binkw32_o.dll, then copy BINKW32.DLL,
     Play_RA2.exe and Play_YR.exe from the repo into Ra2026\.
  d) Rename "cnc-ddraw config.exe" to "cnc-ddraw config.exe.disabled".

3.2 Playing
  - Double-click Ra2026\Play_YR.exe (Yuri's Revenge) or Play_RA2.exe (original RA2).
  - Do NOT start game.exe / gamemd.exe directly (the game exits immediately).
  - Registry data the game "writes" is kept in Ra2026\portable\registry.txt.
  - Every blocked write outside the folder is logged in Ra2026\portable\blocked.log.
  - To uninstall, delete the Ra2026 folder.

3.3 Editing the rules (modding)
  1. Open AI\tools\RA2_Mod_Editor.html in Chrome or Edge.
  2. "Mở thư mục game" (Open game folder) -> pick E:\games\Ra2\Ra2026 (NOT the AI folder).
  3. Choose a rule set: the bundled mod or the official rules.
  4. Edit cost, strength, speed, weapons, superweapons, general rules... or use "Mod nhanh" (quick mod).
  5. "Lưu vào game" (Save to game) -> start Play_YR / Play_RA2 to test.
  - Ctrl+Z undoes. Previous files are backed up in Ra2026\mod_backups\.
  - "Khôi phục..." (Restore) returns the game to the official or the bundled mod rules.
  - LAN play: every PC must use the same rules file.

3.4 About this game copy
  Both games in the repack are ALREADY MODDED:
  - Red Alert 2: a loose rules.ini (adds 30+ infantry, ~40 vehicles).
  - Yuri's Revenge: expandmd03.mix (about 3x faster building, 100% sell refund,
    51 new units, Harrier removed).
  The PDF handbook describes the OFFICIAL rules.

3.5 Rebuilding from source
  See AI\tools\src\README.md (mingw-w64 for the DLL/EXEs; Python + Playwright
  for the handbook; template.html + data for the Mod Editor).


4. CHANGELOG
------------
[2026-11-02]
  + Added .gitignore, README.txt (VI) and README.en.txt (EN) for git.
  + Moved all documents, tools and source into AI\ per the CLAUDE.md v5.7 policy;
    added AI_HANDOFF.md, PROJECT_RULES.md, security\20261030\findings.md.
  + RA2 Mod Editor (AI\tools\RA2_Mod_Editor.html): edits all YR & RA2 rules,
    real unit icons, quick mods, undo, unit cloning, backup & restore.
  * Found that Yuri's Revenge is modded via expandmd03.mix (earlier reported as
    stock by mistake). Handbook corrected -> guide-20261102-vi.pdf (current).
  + Added reference rules under AI\mod\ (official YR/RA2, modded YR).

[2026-10-31]
  + Player handbook PDF (26 pages): 3 factions, 10 countries, illustrated units
    and buildings, superweapons, hotkeys, tips.
  * Ink-saving print edition (24 pages): no cover, white background with thin
    rules; icons in the quick-reference table, tech-building images; new
    "Tricks" chapter.
  + Extracted the official rulesmd.ini for manual modding.

[2026-10-30]
  + Static malware scan of the repack: no malware found; the keygen's
    HackTool detection is a crack-tool warning.
  + Built the Ra2026 portable copy: BINKW32.DLL guard (virtual registry,
    blocks file writes outside the folder), Play_RA2.exe / Play_YR.exe launchers;
    removed keygen, setup tools, SafeDisc driver, original launchers; disabled
    cnc-ddraw config.
  * Tested under Wine: the games start without writing to the registry or
    outside the folder.


5. NOT YET VERIFIED
-------------------
  - Running the game on real Windows with the guard installed.
  - The Mod Editor's Open folder / Save / Restore buttons in real Chrome/Edge.
  Details: AI\AI_HANDOFF.md.
