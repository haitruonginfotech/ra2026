# PROJECT_RULES — Ra2026 (gốc repo = E:\games\Ra2\Ra2026)

1. **Gốc repo là thư mục game `Ra2026`.** Chỉ các file của dự án được đưa lên git (xem `.gitignore`): `BINKW32.DLL`, `Play_RA2.exe`, `Play_YR.exe`, `AI/`, `README.md`, `README.en.md`, `.gitignore`. **Không bao giờ** commit file game của EA (exe, mix, csf, ini game, save...). GitHub cũng từ chối file > 100 MB (`ra2.mix`, `ra2md.mix`).
2. **Không sửa file game gốc** ngoài các thay đổi tích hợp đã ghi trong `AI/AI_HANDOFF.md`. Đặc biệt: không ghi đè `Readme.txt` của game (Windows không phân biệt hoa/thường → README dự án dùng `.md`).
3. Giữ nguyên file tích hợp: `BINKW32.DLL` (guard), `binkw32_o.dll` (Bink gốc, không lên git), `Play_*.exe`. Không đưa lại `Ra2.exe`/`RA2MD.exe`/`YURI.exe`, keygen, RegSetup/SetupReg/uninstal, `DRVMGT.DLL`, `PATCH*`, file `.reg`.
4. Chạy game **chỉ qua `Play_*.exe`**.
5. Luật chơi: `rules.ini` (RA2) / `rulesmd.ini` (YR) rời trong thư mục được ưu tiên hơn `.mix`. Nếu không có `rulesmd.ini` rời, YR dùng luật mod trong `expandmd03.mix`. Bản tham chiếu: `AI/mod/`.
6. Sửa luật bằng `AI/tools/RA2_Mod_Editor.html` (tự sao lưu vào `mod_backups/`, thư mục này không lên git). Chơi LAN: các máy phải dùng cùng file luật.
7. Thư mục nguồn đối chiếu ngoài repo (không sửa): `E:\games\Ra2\ra2-yuris-revenge[taira2.org]`, `SETUP_RA2`, `Yuris-Revenge`, `2.Red_alert_2_setup.rar`.
8. Tài liệu, công cụ, mã nguồn, báo cáo mới để trong `AI/` theo `D:\AI\.claude\CLAUDE.md` (v5.7). Cập nhật `AI/AI_HANDOFF.md` sau mỗi lần ghi.
