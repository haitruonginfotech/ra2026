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

## 2. Khác biệt so với bản gốc

So từng byte với bản repack gốc: **296 file game giữ nguyên**. Repo chỉ chứa phần đã chỉnh sửa hoặc thêm mới:

| Loại | File | Lên git |
|---|---|---|
| Chỉnh sửa | `BINKW32.DLL` (thay bằng lớp chặn ghi) | ✅ |
| Thêm mới | `Play_RA2.exe`, `Play_YR.exe`, `README.md`, `README.en.md`, `.gitignore`, `AI/` (23 file) | ✅ |
| Đổi tên (nội dung gốc) | `BINKW32.DLL` gốc → `binkw32_o.dll`; `cnc-ddraw config.exe` → `cnc-ddraw config.exe.disabled` | ❌ (file của bên thứ ba) |
| Đã loại bỏ | `keygen\` (Keygen.exe, RegSetup.exe, fdxra2k.nfo), `LAN-play-serials\` (4× ra2.reg + Woldata.key), `Ra2.exe`, `RA2MD.exe`, `YURI.exe`, `RegSetup.exe`, `SetupReg.exe`, `uninstal.exe`, `uninstal.ini`, `DRVMGT.DLL`, `PATCHGET.DAT`, `patchgetmd.dat`, `PATCHW32.DLL`, `src.7z`, `aqrit.cfg` | ❌ |

## 3. Cài đặt

1. Clone repo vào thư mục sẽ chứa game:
   ```
   git clone https://github.com/haitruonginfotech/ra2026.git Ra2026
   ```
2. Chép toàn bộ file game Red Alert 2 + Yuri's Revenge vào `Ra2026\`, **trừ**: `keygen\`, `LAN-play-serials\`, `RegSetup.exe`, `SetupReg.exe`, `uninstal.exe/.ini`, `DRVMGT.DLL`, `PATCHGET.DAT`, `patchgetmd.dat`, `PATCHW32.DLL`, `src.7z`, `aqrit.cfg`, `Ra2.exe`, `RA2MD.exe`, `YURI.exe`.
3. **Không** ghi đè `BINKW32.DLL` của repo: lưu file `BINKW32.DLL` của game với tên `binkw32_o.dll`.
4. Đổi tên `cnc-ddraw config.exe` thành `cnc-ddraw config.exe.disabled`.

## 4. Chơi game

- Bấm đúp `Play_YR.exe` (Yuri's Revenge) hoặc `Play_RA2.exe` (Red Alert 2).
- **Không** mở trực tiếp `game.exe` / `gamemd.exe`: game sẽ tự thoát.
- Những gì game "ghi" vào registry nằm ở `portable\registry.txt`. Mọi lần bị chặn ghi ra ngoài được ghi vào `portable\blocked.log` (dòng `COM-PORTABLE` là lớp chặn tự nạp `Blowfish.dll`, bình thường).
- Gỡ game = xóa thư mục.

### Windows 11

Dự án dùng được trên Windows 10 và 11 (64-bit, cả máy ARM). `BINKW32.DLL` và `Play_*.exe` chỉ gọi các thư viện có sẵn trong mọi bản Windows (kernel32, advapi32, user32, msvcrt). Lưu ý:

- **Không cần** chế độ tương thích (Compatibility mode) hay *Run as administrator*. Nếu đã bật thì nên tắt: chạy bằng quyền admin không cần thiết cho bản portable.
- Để thư mục game ở ổ riêng (vd `E:\games\Ra2\Ra2026`). **Không** đặt trong `C:\Program Files` (Windows chặn ghi) hay thư mục OneDrive (Desktop/Documents thường được OneDrive đồng bộ).
- **SmartScreen:** nếu tải repo bằng file ZIP, Windows có thể hiện “Windows protected your PC” khi mở `Play_*.exe`. Bấm *More info → Run anyway*, hoặc chuột phải file ZIP → *Properties → Unblock* trước khi giải nén. Clone bằng `git` thì không bị.
- **Smart App Control** (chỉ bật sẵn trên máy cài mới Windows 11 22H2 trở lên) có thể chặn hẳn các file exe không có chữ ký số: `Play_*.exe` tự build, và cả `game.exe`/`gamemd.exe` của bản repack. Xem ở *Windows Security → App & browser control → Smart App Control*. Muốn chơi thì phải để Off.
- **Microsoft Defender** có thể nghi ngờ `BINKW32.DLL` vì nó sửa bảng import của game (để chặn ghi). Nếu bị cách ly, khôi phục và thêm thư mục `Ra2026` vào *Exclusions*. Mã nguồn ở `AI/tools/src/portable-guard/`.
- **Màn hình đen / văng khi đổi độ phân giải:** mở Mod Editor → **Hiệu năng** → đổi *Bộ vẽ hình* (Direct3D 9 ↔ OpenGL ↔ GDI).
- Mod Editor: dùng Edge (có sẵn) hoặc Chrome. Font Bahnschrift/Segoe UI có sẵn trong Windows 11.

## 5. Chỉnh luật chơi (mod)

1. Mở `AI\tools\RA2_Mod_Editor.html` bằng **Chrome** hoặc **Edge**.
2. Bấm **Mở thư mục game** rồi chọn thư mục `Ra2026` (thư mục có `gamemd.exe`).
3. Chọn bộ luật: bản mod có sẵn hoặc bản chính thức.
4. Sửa giá, máu, tốc độ, vũ khí, siêu vũ khí, luật chung… hoặc dùng **Mod nhanh**.
5. Bấm **Lưu vào game** rồi mở `Play_YR` / `Play_RA2` để chơi thử.

`Ctrl+Z` để hoàn tác. File cũ được sao lưu vào `mod_backups\`. Nút **Khôi phục…** đưa game về bản chính thức hoặc bản mod có sẵn. Chơi LAN: mọi máy phải dùng cùng file luật.

### Giảm giật khi đông quân

Engine RA2/YR chạy logic game trên **một luồng**, nên trận càng đông quân thì càng dễ giật, máy nhiều nhân cũng không đỡ. Trong Mod Editor, bấm **Hiệu năng**:

- **Hiển thị** (`ddraw.ini`, dùng chung 2 game): bộ vẽ Direct3D 9, giới hạn 60 FPS, V-Sync, cho phần vẽ hình chạy trên nhân CPU khác (`singlecpu=false`), chế độ màn hình.
- **Độ nét hình** (`ddraw.ini`): kiểu phóng hình (bilinear mờ → nearest sắc nét, hoặc xBRZ/Lanczos qua OpenGL), giữ đúng tỉ lệ khung hình, phóng to theo số nguyên.
- **Thiết lập trong game** (`RA2MD.INI` / `RA2.INI`): độ phân giải (editor tự nhận độ phân giải màn hình), mức chi tiết. Thoát game trước khi áp dụng.
- **Luật chơi**: giảm hoặc tắt mảnh vỡ khi nổ, cho game tự tắt hiệu ứng sớm hơn khi tụt FPS, bỏ khói lửa trên công trình hư hại.

Nút **Đề xuất cho trận đông quân** điền sẵn cấu hình khuyên dùng. Nút **Hình nét nhất** đặt độ phân giải game bằng màn hình (không phải phóng to) + nearest + giữ tỉ lệ; nét nhất nhưng thấy rộng hơn, quân nhỏ hơn và nặng hơn. Muốn vừa nét vừa nhẹ: giữ độ phân giải thấp, chọn kiểu **xBRZ**. Bấm **Áp dụng**: file cấu hình được ghi thẳng vào thư mục game (bản cũ sao lưu vào `mod_backups\`), phần luật chơi chuyển sang bước **Lưu vào game** và hoàn tác được bằng `Ctrl+Z`. Nếu game bị treo hay văng sau khi bật “Dùng nhiều nhân CPU”, chọn lại “Không”.

> **Lưu ý:** bản repack đã có sẵn mod. RA2 dùng `rules.ini` rời; Yuri's Revenge dùng `expandmd03.mix` (xây nhanh ~3 lần, bán hoàn 100%, thêm 51 quân, bỏ Harrier). Sổ tay PDF mô tả **luật chính thức**.

## 6. Build lại từ mã nguồn

Xem [`AI/tools/src/README.md`](AI/tools/src/README.md): mingw-w64 cho DLL/EXE, Python + Playwright cho sổ tay, `template.html` + dữ liệu cho Mod Editor.

---

## 7. Lịch sử thay đổi

### 2026-11-04
- 🐞 **Sửa lỗi “\*\*\*FATAL\*\*\* String Manager failed to initialize properly” khi mở game trên Windows**: game đăng ký `Blowfish.dll` (COM) vào registry ảo, nhưng `CoCreateInstance` của Windows chỉ đọc registry thật. `BINKW32.DLL` giờ nạp thẳng `Blowfish.dll` từ thư mục game khi Windows báo chưa đăng ký. Vẫn không ghi gì vào registry thật. `portable\blocked.log` có thêm dòng `COM-PORTABLE` (bình thường, không phải lỗi).

### 2026-11-02
- 🤖 **Ảnh quân & công trình phóng to bằng AI (Real-ESRGAN x4plus)**: 434 cameo 60×48 → 240×192 (WebP), nét và mịn ở khung chi tiết; danh sách dùng cùng ảnh thu nhỏ. AI tự vẽ thêm chi tiết nên có thể hơi khác ảnh gốc. File editor ~4,3 MB.
- 📋 **Bảng Thay đổi có ảnh và giải thích**: gộp theo từng quân/mục, có ảnh cameo (hoặc nhãn Luật / Vũ khí / Nhà…), tên tiếng Việt, loại (vd “Vũ khí của Sniper”, “Công trình · nhà dân, không xây được”), tên và giải thích từng thuộc tính; dòng tóm tắt số thay đổi theo loại.
- 🖼️ **Ảnh quân & công trình trong Mod Editor nét hơn**: trích lại 434 ảnh cameo gốc (60×48) từ file game thành PNG 8-bit không mất dữ liệu (trước là JPEG nén), hiển thị đúng cỡ trong danh sách và phóng đúng ×3 (×2 trên điện thoại) với `image-rendering: pixelated`, nền trong suốt.
- 🔎 **Làm nét hình trong game**: hình mờ do cnc-ddraw phóng to bằng bilinear (`d3d9linear=true`, `shader=bilinear.glsl`) và kéo méo (`maintas=false`). Hộp Hiệu năng thêm phần **Độ nét hình** (nearest / xBRZ / Lanczos, giữ tỉ lệ, phóng số nguyên) và nút **Hình nét nhất** (độ phân giải bằng màn hình).
- 🪟 Hướng dẫn **Windows 11** (SmartScreen, Smart App Control, Defender, bộ vẽ hình); thử lại trên Wine giả lập Windows 11.
- 🖥️ Mod Editor hợp màn hình hơn: màn 1024–1439 px thanh nút xuống 2 dòng (trước đó nút **Lưu vào game** bị đẩy ra ngoài ở 1024 px); màn 1920+ hiện 6–7 ô mỗi hàng.
- ⚡ **Mod Editor → Hiệu năng**: chỉnh `ddraw.ini` (bộ vẽ, FPS, V-Sync, nhiều nhân CPU, chế độ màn hình), độ phân giải và mức chi tiết trong `RA2MD.INI`/`RA2.INI`, giảm mảnh vỡ/hiệu ứng trong luật chơi; ghi thẳng vào file, có sao lưu. Kèm nút cấu hình đề xuất cho trận đông quân.
- 🏷️ Mốc phiên bản `v2026.11.02` (baseline) để quay lại khi cần.
- 📋 Repo chỉ giữ file **đã chỉnh sửa hoặc thêm mới** so với bản gốc (đã đối chiếu từng byte: 296 file game giữ nguyên); thêm bảng khác biệt ở mục 2.
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

## 8. Chưa kiểm chứng

- Chạy game trên Windows 11 thật sau khi cài lớp chặn. Đã thử trên Wine giả lập Windows 11 (build 22000): YR và RA2 khởi động qua `Play_*.exe`, registry ghi vào `portable\registry.txt`, không ghi gì ra ngoài thư mục. Wine không thay được Windows thật (đồ họa, Defender, Smart App Control).
- Các nút Mở thư mục / Lưu / Khôi phục / Hiệu năng của Mod Editor trên Chrome/Edge thật (đã thử bằng thư mục giả lập trong Chromium).
- Mức giảm giật thực tế của từng tùy chọn Hiệu năng; “Bỏ khói lửa trên công trình” chưa thử trong game.

Chi tiết: [`AI/AI_HANDOFF.md`](AI/AI_HANDOFF.md).
