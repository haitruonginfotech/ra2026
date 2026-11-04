# RA Reborn — Red Alert 2 + Yuri's Revenge trên engine OpenRA

**Tiếng Việt** (mặc định) · [English](README.en.md)

Game chiến thuật thời gian thực **của riêng dự án**, dựng trên [OpenRA](https://github.com/OpenRA/OpenRA) (engine mã nguồn mở, GPLv3) và phát triển tiếp từ [OpenRA Red Alert 2 mod](https://github.com/OpenRA/ra2). Mục tiêu: chơi như Red Alert 2 + Yuri's Revenge nhưng sửa được mọi thứ, ví dụ **4 bậc lên cấp**.

> **Không chứa file game của EA.** Hình, âm thanh tạm thời được đọc từ bộ game Red Alert 2 + Yuri's Revenge của bạn. EA không liên quan và không hỗ trợ dự án này.
>
> Dự án Ra2026 cũ (bản portable + Mod Editor + sổ tay) nằm ở nhánh [`ra2026-legacy`](https://github.com/haitruonginfotech/ra2026/tree/ra2026-legacy).

## 1. Tình trạng

| Hạng mục | Trạng thái |
|---|---|
| Engine OpenRA `release-20231010` + mod RA2, đổi tên **RA Reborn** (`rareborn`) | ✅ build, kiểm tra luật & hình sạch |
| Đọc thẳng file game từ thư mục `Ra2026` nằm cạnh, nạp thêm file Yuri's Revenge | ✅ |
| **4 bậc lên cấp**: Tân binh · Đồng · Vàng · Kim cương (huy hiệu vẽ mới) | ✅ (chưa chơi thử trên Windows) |
| Phe Đồng Minh, Liên Xô (10 quốc gia) | ✅ có sẵn từ mod RA2 |
| **Phe Yuri** | 🚧 đang làm (mốc 1a: đủ nhà & quân, cơ chế đặc biệt làm đơn giản) |
| Cơ chế Yuri đặc biệt (Grinder, Slave Miner, Gatling, Magnetron, Chaos, Genetic Mutator) | ⏳ mốc 1b |

## 2. Cài đặt (Windows 10/11)

### Cách 1 — bấm là chạy (khuyên dùng)

1. Giải nén bản portable `RAReborn-<phiên bản>-win-x64-portable.zip` vào cạnh thư mục game:
   ```
   E:\games\Ra2\Ra2026     ← bộ game RA2 + YR (ra2.mix, ra2md.mix, langmd.mix, expandmd01.mix…)
   E:\games\Ra2\RAReborn   ← bản portable, có RAReborn.exe
   ```
2. Bấm đúp **`RAReborn.exe`**. Không cần cài .NET (đã kèm sẵn), không ghi registry.

Chế độ **portable**: cài đặt, save, log nằm trong `RAReborn\Support`, không ghi vào AppData.

### Cách 2 — chạy từ mã nguồn (cho người phát triển)

1. `git clone https://github.com/haitruonginfotech/ra2026.git E:\games\Ra2\RAReborn-src` (cạnh `Ra2026`).
2. Cài [.NET 6 SDK](https://dotnet.microsoft.com/download/dotnet/6.0) (x64), chạy `make.cmd` → `all`, rồi `launch-game.cmd`.
3. Đóng gói bản portable (trên Linux): `packaging/windows/build-portable.sh <phiên bản> <thư mục ra>`.

> ⚠️ Đừng chạy `git pull` nhánh `main` bên trong thư mục `Ra2026` (thư mục game cũ): nhánh này giờ là RA Reborn, git sẽ xóa `BINKW32.DLL`, `Play_*.exe`. Trong `Ra2026` hãy chuyển sang nhánh cũ: `git fetch origin` rồi `git checkout -B ra2026-legacy origin/ra2026-legacy`.

## 3. 4 bậc lên cấp

| Bậc | Huy hiệu | Cần tiêu diệt (cộng dồn, × giá của chính quân) | Thưởng |
|---|---|---|---|
| 1 Tân binh | — | 0 | — |
| 2 Đồng | 1 chữ V đồng | 4× | hỏa lực +10%, chịu đòn −10%, tốc độ +10%, nạp đạn −10% |
| 3 Vàng | 2 chữ V vàng | 9× | +20%, −18%, +20%, −18%, chính xác hơn |
| 4 Kim cương | viên kim cương | 15× | +30%, −25%, +30%, −25%, tự hồi máu, mở vũ khí tinh nhuệ |

Cấu hình: `mods/rareborn/rules/defaults.yaml` (`^GainsExperience`). Huy hiệu: `artsrc/ranks/make_ranks.py` → `mods/rareborn/bits/ranks/`.

## 4. Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `mods/rareborn/` | Luật (`rules/`), vũ khí, hình (`sequences/`), giao diện, bản đồ |
| `OpenRA.Mods.RA2/` | Mã C# riêng của mod (điều khiển tâm trí, carrier, mirage…) |
| `artsrc/` | Nguồn đồ họa (huy hiệu 4 bậc…) |
| `AI/` | Trạng thái dự án (`AI_HANDOFF.md`), quy tắc (`PROJECT_RULES.md`) |
| `README.openra-ra2.md` | README gốc của OpenRA RA2 mod |

## 5. Giấy phép

GPLv3 (giống OpenRA và OpenRA RA2 mod), xem `LICENSE`. Bản quyền tài sản game Red Alert 2 / Yuri's Revenge thuộc Electronic Arts.

## 6. Lịch sử thay đổi

### 2026-11-04
- 🖱️ **Bản Windows portable bấm là chạy** (`RAReborn.exe`, .NET kèm sẵn, 64-bit): script `packaging/windows/build-portable.sh`. Thử trên Wine giả lập Windows 11: vào tới màn hình thiết lập đầu tiên, nhật ký nằm trong `RAReborn\Support` (portable).
- 💬 Thông báo đầu game đổi thành “RA Reborn - early preview”.
- 🚀 Khởi tạo **RA Reborn** trên nhánh `main` từ OpenRA RA2 mod (commit upstream trong `UPSTREAM_RA2_COMMIT`), engine `release-20231010`.
- 📦 Đổi mã mod `ra2` → `rareborn`; đọc file game từ `../Ra2026`; nạp thêm ra2md/langmd/expandmd01 và các mix YR lồng bên trong (nạp sau để đè RA2).
- 🎖️ 4 bậc lên cấp Tân binh / Đồng / Vàng / Kim cương, huy hiệu vẽ mới (16×16).
- 🗂️ Dự án Ra2026 cũ chuyển sang nhánh `ra2026-legacy`.
