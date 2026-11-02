# Findings — quét virus/malware 30/10/2026

- **Mục tiêu:** `E:\games\Ra2\ra2-yuris-revenge[taira2.org]` (322 file, 745 MB). Không quét `SETUP_RA2`, `Yuris-Revenge`, file `.rar`.
- **Thời điểm:** 2026-10-30 ~15:45 (Asia/Ho_Chi_Minh). Ghi chép này được lập lại ngày 2026-11-02 từ kết quả phiên làm việc.
- **Phương pháp:** phân tích tĩnh, chỉ đọc: liệt kê định dạng (`file`), import table PE (`pefile`), chuỗi nghi vấn (URL, Run keys, API tiêm mã/tải file, đào coin, Telegram/Discord...), entropy section, giải nén UPX của keygen (`upx -d`) trong container cách ly, kiểm tra header MZ trong file không phải exe, rà script trong HTML.
- **Không làm được:** quét chữ ký ClamAV (máy chủ cập nhật CSDL bị chặn mạng); không tra VirusTotal (không có quyền gửi mẫu ra ngoài). Không chạy bất kỳ mẫu nào.
- **Ảnh chụp:** `SCREENSHOT_UNAVAILABLE` (phiên không có công cụ chụp màn hình bằng chứng). Bằng chứng dạng văn bản: `evidence/sha256-executables.txt` (SHA-256 của mọi .exe/.dll/.dat/.7z/.reg, tính lại 02/11/2026).

| ID | Đối tượng | Trạng thái | Mức | Nhận định |
|---|---|---|---|---|
| F001 | `keygen\Keygen.exe` (UPX) | false-positive (có thể bị AV báo HackTool) | Thấp | Sau giải nén chỉ import KERNEL32 cơ bản + hộp thoại USER32; không mạng, không ghi registry. Công cụ tạo serial. Không chép sang Ra2026. |
| F002 | `wsock32.dll` (2024) | false-positive | Thấp | Chỉ import WS2_32 + CRT; 48 export forward sang ws2_32 (wrapper IPX/LAN). Không truy cập file/registry/tiến trình. |
| F003 | `DRVMGT.DLL` | false-positive (rủi ro hệ thống) | Trung bình nếu chạy | Thành phần SafeDisc, có CreateServiceA cho `secdrv.sys`. Không file game nào nạp. Không chép sang Ra2026. |
| F004 | `Ra2.exe`, `RA2MD.exe`, `YURI.exe` | false-positive | Thấp | Chuỗi `RunOnce` thuộc bộ patcher gốc Westwood. Có ghi HKLM\Software\Westwood. Không chép sang Ra2026 (thay bằng Play_*.exe). |
| F005 | `ddraw.dll`, `cnc-ddraw config.exe` | false-positive | Thấp | cnc-ddraw (CnCNet). Config tool có API registry → đổi tên `.disabled` trong Ra2026. |
| F006 | Bản game có mod | observed (không phải malware) | Thông tin | `rules.ini` rời (RA2) và `expandmd03.mix` (YR) là mod luật chơi, không phải mã độc. Phát hiện ngày 01–02/11. |

**Kết luận:** không phát hiện mã độc trong phạm vi phân tích tĩnh. Đề xuất: quét bổ sung bằng Microsoft Defender trên máy; tra các hash trong `evidence/` trên VirusTotal nếu người dùng đồng ý.

**Trạng thái xử lý:** không xóa/cách ly gì trong thư mục gốc. Bản sạch hơn được tạo tại `E:\games\Ra2\Ra2026` (loại F001, F003, F004, công cụ cài đặt; F005 tắt).
