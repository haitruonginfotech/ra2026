# AI_HANDOFF — E:\games\Ra2

_Cập nhật: 2026-11-02 (Asia/Ho_Chi_Minh) · Agent: Claude (Cowork, cloud session + device bridge tới máy haitruong-it)_

## Dự án
- **PROJECT_ROOT:** `E:\games\Ra2` (thư mục người dùng chọn). Dự kiến làm gốc git của `https://github.com/haitruonginfotech/ra2026` (repo đang được clone tạm ở `aaa\ra2026`, nhánh main, commit cuối "clean src" 1811d66). Chưa có `.git` ở gốc.
- **Nội dung:** Red Alert 2 + Yuri's Revenge (bản repack taira2.org) → bản chơi portable `Ra2026`, sổ tay, công cụ mod.
- **Chế độ:** DESKTOP_DIRECT. Ghi trực tiếp vào thư mục đã kết nối, đã được người dùng cho phép. Chính sách `D:\AI\.claude\CLAUDE.md` v5.7 đã đọc ngày 02/11 (trước đó chưa truy cập được: `GLOBAL_INSTRUCTIONS_UNAVAILABLE`, `LOCAL_SKILLS_UNAVAILABLE`).

## Trạng thái
| Hạng mục | Trạng thái | Đường dẫn |
|---|---|---|
| Quét malware thư mục gốc (30/10) | Xong, không phát hiện mã độc (phân tích tĩnh) | `AI/security/20261030/findings.md`, `evidence/sha256-executables.txt` |
| Bản portable Ra2026 (30/10) | Tích hợp, đang dùng | `Ra2026/` (xem dưới) |
| Sổ tay PDF | **Hiện hành:** `AI/guide/guide-20261102-vi.pdf` (24 trang). Bản cũ `guide-20261031-vi.pdf` đã bị thay thế vì ghi sai “YR là bản chuẩn” | `AI/guide/` |
| RA2 Mod Editor (02/11) | Xong, đã test bằng Playwright | `AI/tools/RA2_Mod_Editor.html` |
| Luật tham chiếu | `rulesmd-official-yr.ini` (expandmd01), `rulesmd-mod-expandmd03-yr.ini`, `rules-official-ra2.ini` (local.mix) | `AI/mod/` |
| Mã nguồn | portable-guard, mod-editor, guide | `AI/tools/src/` (README.md) |
| Git (02/11) | `.gitignore` + `README.txt` (VI, mặc định) + `README.en.txt` (EN) ở gốc; chưa commit/push | `E:\games\Ra2\` |

## Thay đổi trong Ra2026 (tích hợp trực tiếp, cố ý giữ ngoài AI/)
- Chép từ `ra2-yuris-revenge[taira2.org]`, **loại**: keygen\, LAN-play-serials\, RegSetup/SetupReg/uninstal(.exe/.ini), DRVMGT.DLL, PATCHGET.DAT, patchgetmd.dat, PATCHW32.DLL, src.7z, aqrit.cfg, Ra2.exe, RA2MD.exe, YURI.exe.
- `BINKW32.DLL` = guard (src: portable.c, SHA-256 b09599b1…); `binkw32_o.dll` = Bink gốc (SHA-256 1fd7ef78…).
- `Play_RA2.exe` (d4104e90…), `Play_YR.exe` (51edab53…) = launcher không ghi gì.
- `cnc-ddraw config.exe` → `cnc-ddraw config.exe.disabled`.
- Runtime tạo: `Ra2026\portable\registry.txt`, `portable\blocked.log`; editor tạo `Ra2026\mod_backups\`.
- 02/11: đã **chuyển** khỏi Ra2026 sang AI/: RA2_Mod_Editor.html, Huong_dan_choi_RA2_YR.pdf, DOC_TRUOC.txt (→ `AI/guide/ra2026-readme-20261030-vi.txt`, đường dẫn `_portable_src` trong đó nay là `AI/tools/src/portable-guard`), `_portable_src/`, `rulesmd (ban goc).ini`.

## Phát hiện quan trọng
- **Cả hai game đã bị mod:** RA2 qua `Ra2026\rules.ini` rời (~4.100 khác biệt, thêm >30 bộ binh, ~40 xe). YR qua `expandmd03.mix` (không phải gói chính thức): BuildSpeed .7→.25, RefundPercent 50%→100%, 51 quân/công trình mới, Harrier TechLevel -1, 12 chỉ số quân cũ đổi.
- game.exe/gamemd.exe bản crack (bỏ SafeDisc); `wsock32.dll` wrapper LAN; `ddraw.dll` = cnc-ddraw.

## Đã kiểm chứng
- Guard: Wine — test.exe (registry ảo, chặn ghi ngoài thư mục); game.exe & gamemd.exe khởi động qua Play_*.exe, không thêm khóa registry thật, không file mới ngoài thư mục; hành vi mở file giống hệt khi dùng binkw32 gốc.
- Editor: Chromium/Playwright — mở, sửa field, vũ khí/verses, Luật chung, Mod nhanh, hoàn tác/làm lại, nhân bản, tải file (diff đúng các dòng sửa, giữ comment, CRLF), chuyển RA2. Không lỗi console.
- PDF: kiểm tra trang bằng render + trích chữ.

## CHƯA kiểm chứng
- Chưa chạy game trên **Windows thật** sau khi cài guard (Wine headless chỉ đến màn đen do cnc-ddraw).
- Editor: chưa test thao tác **Mở thư mục / Lưu vào game / Khôi phục** bằng File System Access API thật (headless không chọn thư mục được); chưa test trên Edge/Chrome Windows, chưa test mobile/200% zoom.
- Mẹo trong sổ tay chưa kiểm chứng trong game: sửa Credits trong RA2MD.INI, bán công trình ra lính, lính bị điều khiển vào Bio Reactor.
- Không có báo cáo PDF EN/VI cho lần quét (người dùng chưa yêu cầu).

## Thiết kế
- Editor: `DESIGN_REFERENCE_UNAVAILABLE` lúc làm (chưa có quyền `D:\images\`); hướng “hồ sơ quân sự sáng”: nền thép nhạt #E6EAEE, mực #17212B, hổ phách #B97A06 cho giá trị đã sửa, màu phe; Bahnschrift + Segoe UI. Skill đọc: frontend-design (bản có sẵn trong phiên), không dùng skill local.
- Style log: `STYLE_LOG_NOT_UPDATED`. Ghi vào `D:\AI\.claude\style-log.md` bị chặn (“Writing to .claude is not permitted via remote tools”). Mục cần thêm (người dùng tự dán nếu muốn): `2026-11-02 | E:\games\Ra2 — RA2 Mod Editor | Bahnschrift + Segoe UI + Cascadia Mono | #E6EAEE #17212B #2B3743 #B97A06 + màu phe | 3-pane tool, unit dossier | no motion | frontend-design (built-in), DESIGN_REFERENCE_UNAVAILABLE`.

## Việc tiếp theo
1. Người dùng chạy thử Play_YR/Play_RA2 trên Windows; xem `Ra2026\portable\blocked.log`.
2. Thử editor: Mở thư mục `E:\games\Ra2\Ra2026` → sửa → Lưu → chơi.
3. (Chờ người dùng) cập nhật sổ tay theo bản mod (51 quân mới, hoàn tiền 100%, bỏ Harrier).
4. Tùy chọn: báo cáo bảo mật PDF EN/VI; quét Defender/VirusTotal.

## 2026-11-02 — Chuẩn bị đưa lên git
- Thêm ở gốc repo (người dùng yêu cầu, ngoại lệ hợp lý ngoài `AI/`): `.gitignore`, `README.txt` (VI: hướng dẫn + changelog), `README.en.txt` (EN).
- `.gitignore` kiểu whitelist: chỉ theo dõi `AI/`, 3 file tích hợp của `Ra2026` (BINKW32.DLL, Play_RA2.exe, Play_YR.exe), README, .gitignore. Bỏ qua file game gốc, `.rar`, `aaa/`, `Ra2026/portable/`, `Ra2026/mod_backups/`, `AI/security/*/evidence/`, rác OS/build.
- Kiểm thử: dựng lại 851 đường dẫn thật bằng file rỗng ở thư mục tạm trên máy, `git add -A --dry-run` → 28 file, không lọt file game (~13 MB). Thư mục tạm đã xóa.
- Chưa làm: `git init`/chuyển `.git`, commit, push (shell từ xa không xóa được lock file của git → để người dùng chạy).
- Lưu ý: repo chứa dữ liệu trích từ game (AI/mod/*.ini, icon trong Mod Editor/PDF) → nên để private.

## 2026-11-02 — SEO repo GitHub
- Cập nhật qua Chrome của người dùng (API của phiên bị chặn ghi cài đặt): About của `haitruonginfotech/ra2026` → mô tả EN+VI, giữ website haitruongit.com, 20 topics (red-alert-2, yuris-revenge, command-and-conquer, ra2, ra2yr, westwood, rts, retro-gaming, game-modding, mod-editor, rules-ini, portable-apps, windows, dll-proxy, iat-hooking, virtual-registry, offline-web-app, vietnamese, bao-dong-do-2, game-guide); bỏ tick Packages. Đã xác minh bằng `gh api`.
- Repo **public**. Người dùng đã được cảnh báo về dữ liệu trích từ game (bản quyền EA) và **chọn: public, đẩy hết**.
- Phiên cloud không push được (chưa cài Claude GitHub App) → người dùng tự commit/push theo README/hướng dẫn.
- Gợi ý chưa làm: README.md (GitHub hiển thị đẹp, tốt cho SEO), ảnh social preview 1280×640, release/tag v2026.11.02 sau khi push.
