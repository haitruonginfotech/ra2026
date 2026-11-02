# Mã nguồn công cụ — dự án Ra2 (E:\games\Ra2)

## portable-guard/ (đang chạy trong Ra2026)
- `portable.c` → biên dịch thành `Ra2026\BINKW32.DLL` (proxy của binkw32; bản gốc đổi tên `binkw32_o.dll`).
  Vá IAT của game.exe/gamemd.exe: registry ảo (lưu `Ra2026\portable\registry.txt`), chặn ghi file ngoài thư mục game (log `Ra2026\portable\blocked.log`).
- `launcher.c` → `Play_RA2.exe` (GAME_EXE="game.exe") và `Play_YR.exe` (GAME_EXE="gamemd.exe"); tạo mutex 48BC11BD-… mà game đòi rồi chạy game.
- `binkw32.def` → bảng forward 83 export sang `binkw32_o.dll`.
- Build (Linux, mingw-w64 i686):
  ```
  i686-w64-mingw32-gcc -O2 -s -shared -o binkw32.dll portable.c binkw32.def -Wl,--enable-stdcall-fixup -static-libgcc -ladvapi32
  i686-w64-mingw32-gcc -O2 -s -mwindows -DGAME_EXE='"gamemd.exe"' -o Play_YR.exe launcher.c yr.res
  ```

## mod-editor/
- `template.html` — mã của `AI\tools\RA2_Mod_Editor.html`; dòng `/*DATA*/` được thay bằng `window.RA2DATA=…` (luật gốc/mod gzip+base64, bảng art→cameo, tên CSF, icon cameo JPEG).
- Dữ liệu trích từ: expandmd01.mix (rulesmd chính thức YR), expandmd03.mix (rulesmd/artmd mod YR), local.mix/localmd.mix, cameo.mix, cameomd.mix, ecache03/04/5.mix, ra2.csf, ra2md.csf, art.ini, rules.ini (rời).
- `test1.js`, `test2.js` — kiểm thử Playwright (mở, sửa, mod nhanh, hoàn tác, nhân bản, tải file, chuyển RA2).

## guide/
- `build2.py` + `content.py` → HTML sổ tay; `pdf.js` (Playwright) → PDF A4.
- `data.py` (đọc INI/CSF), `shp.py` (giải mã SHP TS/RA2).
- Cần thư viện Python `ra2mix`, `Pillow`; dữ liệu MIX trích ra file pickle tạm (không lưu kèm).
