# Ra2026 — Red Alert 2 & Yuri's Revenge portable + công cụ mod

**Tiếng Việt** (mặc định) · [English](README.en.md)

Bản chơi **portable** của Red Alert 2 + Yuri's Revenge (Báo Động Đỏ 2): game **không ghi gì vào registry hay ra ngoài thư mục của nó**. Kèm theo:

- 📘 **Sổ tay người chơi** (PDF tiếng Việt, 24 trang): 3 phe, 10 quốc gia, quân & công trình có ảnh, siêu vũ khí, phím tắt, thủ thuật.
- 🛠️ **RA2 Mod Editor**: trang web offline, chỉnh luật chơi (`rulesmd.ini` / `rules.ini`) trực quan.
- 🔍 **Ghi chép quét virus** của bản repack gốc.

> **Repo không chứa file game.** Bạn cần có sẵn bộ game Red Alert 2 + Yuri's Revenge. Một số file trong `AI/` chứa dữ liệu trích từ game (file luật `.ini`, icon trong Mod Editor, ảnh trong sổ tay) thuộc bản quyền EA.

---

## 1. Cấu trúc

Gốc repo **chính là thư mục game** (trên máy tác giả: `E:\games\Ra2\Ra2026`).

| Đường dẫn | Nội dung |
|---|---|
| `Play_YR.exe` | Mở Yuri's Revenge |
| `Play_RA2.exe` | Mở Red Alert 2 |
| `BINKW32.DLL` | Lớp chặn ghi: registry ảo + chặn ghi file ra ngoài thư mục |
| `AI/guide/guide-20261102-vi.pdf` | Sổ tay người chơi (bản hiện hành) |
| `AI/tools/RA2_Mod_Editor.html` | Công cụ chỉnh luật chơi |
| `AI/tools/src/` | Mã nguồn: `portable-guard`, `mod-editor`, `guide` |
| `AI/mod/` | Luật tham chiếu: chính thức & mod của 2 game |
| `AI/security/20261030/findings.md` | Kết quả quét virus |
| `AI/AI_HANDOFF.md`, `AI/PROJECT_RULES.md` | Trạng thái chi tiết & quy tắc dự án |

Mọi file game khác trong thư mục đều bị `.gitignore` bỏ qua.

## 2. Cài đặt

1. Clone repo vào thư mục sẽ chứa game:
   ```
   git clone https://github.com/haitruonginfotech/ra2026.git Ra2026
   ```
2. Chép toàn bộ file game Red Alert 2 + Yuri's Revenge vào `Ra2026\`, **trừ**: `keygen\`, `LAN-play-serials\`, `RegSetup.exe`, `SetupReg.exe`, `uninstal.exe/.ini`, `DRVMGT.DLL`, `PATCHGET.DAT`, `patchgetmd.dat`, `PATCHW32.DLL`, `src.7z`, `aqrit.cfg`, `Ra2.exe`, `RA2MD.exe`, `YURI.exe`.
3. **Không** ghi đè `BINKW32.DLL` của repo: lưu file `BINKW32.DLL` của game với tên `binkw32_o.dll`.
4. Đổi tên `cnc-ddraw config.exe` thành `cnc-ddraw config.exe.disabled`.

## 3. Chơi game

- Bấm đúp `Play_YR.exe` (Yuri's Revenge) hoặc `Play_RA2.exe` (Red Alert 2).
- **Không** mở trực tiếp `game.exe` / `gamemd.exe`: game sẽ tự thoát.
- Những gì game "ghi" vào registry nằm ở `portable\registry.txt`. Mọi lần bị chặn ghi ra ngoài được ghi vào `portable\blocked.log`.
- Gỡ game = xóa thư mục.

## 4. Chỉnh luật chơi (mod)

1. Mở `AI\tools\RA2_Mod_Editor.html` bằng **Chrome** hoặc **Edge**.
2. Bấm **Mở thư mục game** rồi chọn thư mục `Ra2026` (thư mục có `gamemd.exe`).
3. Chọn bộ luật: bản mod có sẵn hoặc bản chính thức.
4. Sửa giá, máu, tốc độ, vũ khí, siêu vũ khí, luật chung… hoặc dùng **Mod nhanh**.
5. Bấm **Lưu vào game** rồi mở `Play_YR` / `Play_RA2` để chơi thử.

`Ctrl+Z` để hoàn tác. File cũ được sao lưu vào `mod_backups\`. Nút **Khôi phục…** đưa game về bản chính thức hoặc bản mod có sẵn. Chơi LAN: mọi máy phải dùng cùng file luật.

> **Lưu ý:** bản repack đã có sẵn mod. RA2 dùng `rules.ini` rời; Yuri's Revenge dùng `expandmd03.mix` (xây nhanh ~3 lần, bán hoàn 100%, thêm 51 quân, bỏ Harrier). Sổ tay PDF mô tả **luật chính thức**.

## 5. Build lại từ mã nguồn

Xem [`AI/tools/src/README.md`](AI/tools/src/README.md): mingw-w64 cho DLL/EXE, Python + Playwright cho sổ tay, `template.html` + dữ liệu cho Mod Editor.

---

## 6. Lịch sử thay đổi

### 2026-11-02
- 🔁 **Đổi gốc repo thành thư mục game `Ra2026`**: `BINKW32.DLL`, `Play_*.exe` nằm ở gốc, `AI/` nằm cạnh file game; `.gitignore` chỉ cho phép đúng các file của dự án.
- 📝 README đổi sang `README.md` (VI) và `README.en.md` (EN), để không trùng với `Readme.txt` gốc của game (Windows không phân biệt hoa/thường).
- 🌐 GitHub: mô tả EN+VI và 20 topics cho SEO; đưa mã nguồn, công cụ, tài liệu lên repo.
- ➕ `.gitignore`, README song ngữ có hướng dẫn và lịch sử thay đổi.
- 📁 Gom tài liệu, công cụ, mã nguồn vào `AI/` (theo chính sách `CLAUDE.md` v5.7); thêm `AI_HANDOFF.md`, `PROJECT_RULES.md`, `security/20261030/findings.md`.
- 🛠️ **RA2 Mod Editor**: chỉnh toàn bộ luật YR & RA2, icon thật, mod nhanh, hoàn tác, nhân bản quân, sao lưu & khôi phục.
- ⚠️ Phát hiện Yuri's Revenge đã bị mod qua `expandmd03.mix` (trước đó ghi nhầm là bản chuẩn); sửa sổ tay thành `guide-20261102-vi.pdf`.
- ➕ Luật tham chiếu trong `AI/mod/`.

### 2026-10-31
- 📘 Sổ tay người chơi PDF (26 trang).
- 🖨️ Bản in tiết kiệm mực (24 trang): bỏ bìa, nền trắng; thêm icon vào bảng tra cứu, ảnh công trình trung lập, chương **Thủ thuật**.
- ➕ Trích file luật chính thức `rulesmd.ini` để tự mod.

### 2026-10-30
- 🔍 Quét virus/malware bản repack (phân tích tĩnh): không phát hiện mã độc; keygen bị phần mềm diệt virus báo HackTool là cảnh báo công cụ crack.
- 🎮 Tạo bản portable: lớp chặn `BINKW32.DLL` (registry ảo, chặn ghi file ra ngoài), trình mở `Play_RA2.exe` / `Play_YR.exe`; loại keygen, công cụ cài đặt, driver SafeDisc, trình mở gốc; tắt cnc-ddraw config.
- ✅ Thử trên Wine: game khởi động, không ghi registry hay file ra ngoài.

## 7. Chưa kiểm chứng

- Chạy game trên Windows thật sau khi cài lớp chặn.
- Các nút Mở thư mục / Lưu / Khôi phục của Mod Editor trên Chrome/Edge thật.

Chi tiết: [`AI/AI_HANDOFF.md`](AI/AI_HANDOFF.md).
