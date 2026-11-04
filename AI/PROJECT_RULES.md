# PROJECT_RULES — RA Reborn (nhánh `main` của haitruonginfotech/ra2026)

1. **Nhánh:** `main` = RA Reborn (OpenRA). `ra2026-legacy` = dự án Ra2026 cũ (portable guard, Mod Editor, sổ tay) — chỉ sửa khi người dùng yêu cầu việc của Ra2026, và push vào nhánh đó, không vào `main`.
2. **Không bao giờ** commit file game của EA (`*.mix`, `*.csf`, `*.bag`, exe, save, ini game…). Game đọc chúng lúc chạy từ `../Ra2026` hoặc `Support/Content/rareborn`. `.gitignore` đã bỏ qua `/Ra2026`, `/Support`, `engine`.
3. Mã mod là `rareborn` (`mods/rareborn`). Tham chiếu nội bộ dùng `rareborn|…`. Engine OpenRA cố định theo `ENGINE_VERSION` trong `mod.config` (hiện `release-20231010`).
4. **Kiểm tra trước khi push** (cần .NET 6 SDK): `make` → `./utility.sh --check-yaml` và `./utility.sh --check-missing-sprites` phải sạch (0 lỗi, 0 “does not exist”) khi có file game ở `../Ra2026`.
5. Đồ họa mới do dự án tự làm để trong `artsrc/` (kèm script tạo) và `mods/rareborn/bits/`. Đồ họa EA chỉ được đọc từ file game của người dùng, không chép vào repo.
6. Giấy phép GPLv3 (kế thừa OpenRA / OpenRA RA2 mod): giữ `LICENSE`, ghi công tác giả gốc, ghi commit upstream trong `UPSTREAM_RA2_COMMIT`.
7. Tài liệu, báo cáo để trong `AI/` theo `D:\AI\.claude\CLAUDE.md` (v5.7). Cập nhật `AI/AI_HANDOFF.md` sau mỗi lần ghi.
8. **Tự động push (người dùng yêu cầu 02/11/2026):** sau MỖI lần cập nhật file dự án, agent tự commit + push lên `origin/main`, không cần hỏi lại:
   - Commit message tiếng Anh, ngắn, nêu rõ thay đổi; cập nhật `AI/AI_HANDOFF.md` và changelog trong `README.md`/`README.en.md` cùng đợt.
   - Sau khi push: đọc lại remote để xác minh; báo commit SHA cho người dùng.
   - Cách push: `git push`; nếu không được thì trang “Upload files” của GitHub trong Chrome người dùng; nếu không cách nào khả dụng: báo “CHƯA PUSH”.
9. Ngôn ngữ: README mặc định tiếng Việt (`README.md`), bản tiếng Anh `README.en.md`.
