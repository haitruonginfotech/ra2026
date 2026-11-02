# PROJECT_RULES — E:\games\Ra2

1. **Không sửa thư mục gốc** `ra2-yuris-revenge[taira2.org]`, `SETUP_RA2`, `Yuris-Revenge`, `2.Red_alert_2_setup.rar`: đây là nguồn đối chiếu.
2. **Ra2026 là bản chơi portable.** Giữ nguyên các file tích hợp: `BINKW32.DLL` (guard), `binkw32_o.dll` (Bink gốc), `Play_RA2.exe`, `Play_YR.exe`. Không đưa lại `Ra2.exe`/`RA2MD.exe`/`YURI.exe`, keygen, RegSetup/SetupReg/uninstal, DRVMGT.DLL, PATCH*, file `.reg`.
3. Chạy game **chỉ qua Play_*.exe** (game.exe/gamemd.exe tự thoát nếu thiếu mutex).
4. Luật chơi: file rời `rules.ini` (RA2) / `rulesmd.ini` (YR) trong Ra2026 được ưu tiên hơn .mix. YR hiện dùng mod trong `expandmd03.mix` khi không có `rulesmd.ini` rời. Bản chính thức tham chiếu: `AI\mod\`.
5. Sửa luật bằng `AI\tools\RA2_Mod_Editor.html` (tự sao lưu vào `Ra2026\mod_backups\`). Chơi LAN: các máy phải dùng cùng file luật.
6. Tài liệu, công cụ, mã nguồn, báo cáo mới: để trong `AI\` theo `D:\AI\.claude\CLAUDE.md` (v5.7). Cập nhật `AI\AI_HANDOFF.md` sau mỗi lần ghi.
