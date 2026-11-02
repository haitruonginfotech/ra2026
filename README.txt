RA2026 — RED ALERT 2 & YURI'S REVENGE PORTABLE + CÔNG CỤ MOD
==============================================================
Bản tiếng Việt (mặc định). English version: README.en.txt
Repo: https://github.com/haitruonginfotech/ra2026
Cập nhật: 02/11/2026


1. GIỚI THIỆU
-------------
Dự án biến bản Red Alert 2 + Yuri's Revenge (repack taira2.org) thành một
bản chơi "portable" sạch tên Ra2026: game không ghi registry hay file ra ngoài
thư mục của nó. Kèm theo:
  - Sổ tay người chơi (PDF, tiếng Việt, 24 trang).
  - RA2 Mod Editor: trang web offline để chỉnh luật chơi trực quan.
  - Ghi chép quét virus của bản repack gốc.

LƯU Ý BẢN QUYỀN: repo KHÔNG chứa file game (game.exe, *.mix...). Một số file
trong AI\ có dữ liệu trích từ game (file luật .ini, icon trong Mod Editor và
sổ tay). Nên để repo ở chế độ PRIVATE.


2. CẤU TRÚC
-----------
E:\games\Ra2\                       (gốc repo)
  README.txt / README.en.txt        Hướng dẫn + lịch sử thay đổi
  .gitignore                        Chỉ đưa lên git phần của dự án
  Ra2026\                           Thư mục game portable (chỉ 3 file lên git)
    Play_YR.exe                     Mở Yuri's Revenge
    Play_RA2.exe                    Mở Red Alert 2
    BINKW32.DLL                     Lớp chặn ghi (registry ảo + chặn ghi file)
  AI\
    AI_HANDOFF.md                   Trạng thái chi tiết cho người/agent làm tiếp
    PROJECT_RULES.md                Quy tắc của dự án
    guide\guide-20261102-vi.pdf     Sổ tay người chơi (bản hiện hành)
    tools\RA2_Mod_Editor.html       Công cụ chỉnh luật chơi
    tools\src\                      Mã nguồn: portable-guard, mod-editor, guide
    mod\                            Luật tham chiếu: chính thức & mod của 2 game
    security\20261030\findings.md   Kết quả quét virus


3. HƯỚNG DẪN SỬ DỤNG
--------------------
3.1 Cài từ repo (máy mới)
  a) Có sẵn thư mục game Red Alert 2 + Yuri's Revenge (bản repack).
  b) Chép toàn bộ file game vào Ra2026\, TRỪ: keygen\, LAN-play-serials\,
     RegSetup.exe, SetupReg.exe, uninstal.exe/.ini, DRVMGT.DLL, PATCHGET.DAT,
     patchgetmd.dat, PATCHW32.DLL, src.7z, aqrit.cfg, Ra2.exe, RA2MD.exe, YURI.exe.
  c) Đổi tên BINKW32.DLL của game thành binkw32_o.dll, rồi chép BINKW32.DLL,
     Play_RA2.exe, Play_YR.exe từ repo vào Ra2026\.
  d) Đổi tên "cnc-ddraw config.exe" thành "cnc-ddraw config.exe.disabled".

3.2 Chơi game
  - Bấm đúp Ra2026\Play_YR.exe (Yuri's Revenge) hoặc Play_RA2.exe (RA2 gốc).
  - KHÔNG mở trực tiếp game.exe / gamemd.exe (game sẽ tự thoát).
  - Những gì game "ghi" vào registry nằm ở Ra2026\portable\registry.txt.
  - Mọi lần bị chặn ghi ra ngoài được ghi vào Ra2026\portable\blocked.log.
  - Xóa game = xóa thư mục Ra2026.

3.3 Chỉnh luật chơi (mod)
  1. Mở AI\tools\RA2_Mod_Editor.html bằng Chrome hoặc Edge.
  2. "Mở thư mục game" -> chọn E:\games\Ra2\Ra2026 (KHÔNG chọn thư mục AI).
  3. Chọn bộ luật: bản mod có sẵn / bản chính thức.
  4. Sửa (giá, máu, tốc độ, vũ khí, siêu vũ khí, luật chung...) hoặc "Mod nhanh".
  5. "Lưu vào game" -> mở Play_YR / Play_RA2 để chơi thử.
  - Ctrl+Z hoàn tác. File cũ được sao lưu trong Ra2026\mod_backups\.
  - Nút "Khôi phục..." đưa game về bản chính thức hoặc bản mod có sẵn.
  - Chơi LAN: các máy phải dùng cùng file luật.

3.4 Lưu ý về bản game
  Cả hai game trong bản repack đều ĐÃ BỊ MOD:
  - Red Alert 2: file rules.ini rời (thêm >30 bộ binh, ~40 xe).
  - Yuri's Revenge: expandmd03.mix (xây nhanh ~3 lần, bán hoàn 100%,
    thêm 51 quân mới, bỏ Harrier).
  Sổ tay PDF mô tả luật CHÍNH THỨC.

3.5 Build lại từ mã nguồn
  Xem AI\tools\src\README.md (mingw-w64 cho DLL/EXE; Python + Playwright cho
  sổ tay; template.html + dữ liệu cho Mod Editor).


4. LỊCH SỬ THAY ĐỔI (CHANGELOG)
-------------------------------
[2026-11-02]
  + Thêm .gitignore, README.txt (VI) và README.en.txt (EN) để đưa lên git.
  + Gom mọi tài liệu, công cụ, mã nguồn vào AI\ theo chính sách CLAUDE.md v5.7;
    thêm AI_HANDOFF.md, PROJECT_RULES.md, security\20261030\findings.md.
  + RA2 Mod Editor (AI\tools\RA2_Mod_Editor.html): chỉnh toàn bộ luật YR & RA2,
    icon thật, mod nhanh, hoàn tác, nhân bản quân, sao lưu & khôi phục.
  * Phát hiện Yuri's Revenge đã bị mod qua expandmd03.mix (trước đó ghi nhầm là
    bản chuẩn). Sửa sổ tay -> guide-20261102-vi.pdf (bản hiện hành).
  + Thêm luật tham chiếu: AI\mod\ (chính thức YR/RA2, mod YR).

[2026-10-31]
  + Sổ tay người chơi PDF (26 trang): 3 phe, 10 quốc gia, quân & công trình
    có ảnh, siêu vũ khí, phím tắt, mẹo.
  * Bản in tiết kiệm mực (24 trang): bỏ bìa, nền trắng viền mảnh; thêm icon
    vào bảng tra cứu và ảnh công trình trung lập; thêm chương "Thủ thuật".
  + Trích file luật chính thức rulesmd.ini để tự mod.

[2026-10-30]
  + Quét virus/malware bản repack (phân tích tĩnh): không phát hiện mã độc;
    keygen bị AV báo HackTool là cảnh báo công cụ crack.
  + Tạo bản portable Ra2026: lớp chặn BINKW32.DLL (registry ảo, chặn ghi file
    ngoài thư mục), trình mở Play_RA2.exe / Play_YR.exe; loại bỏ keygen, công cụ
    cài đặt, driver SafeDisc, trình mở gốc; tắt cnc-ddraw config.
  * Kiểm thử trên Wine: game khởi động, không ghi registry hay file ra ngoài.


5. CHƯA KIỂM CHỨNG
------------------
  - Chạy game trên Windows thật sau khi cài lớp chặn.
  - Nút Mở thư mục / Lưu / Khôi phục của Mod Editor trên Chrome/Edge thật.
  Chi tiết: AI\AI_HANDOFF.md.
