# AI_HANDOFF — RA Reborn (repo haitruonginfotech/ra2026, nhánh main)

_Cập nhật: 2026-11-04 (Asia/Ho_Chi_Minh) · Agent: Claude (cloud session + device bridge tới máy người dùng)_

## Dự án
- **RA Reborn**: game RTS riêng dựng trên OpenRA (`release-20231010`) + OpenRA RA2 mod (upstream `OpenRA/ra2`, commit trong `UPSTREAM_RA2_COMMIT`), mã mod `rareborn`. Người dùng chọn “hướng 3” (game riêng), tạm dùng hình/âm thanh RA2+YR từ thư mục game của họ; tên “RA Reborn”; đè lên repo ra2026; mốc 1 phải **đủ 3 phe**.
- Dự án cũ: nhánh `ra2026-legacy` @ `7a067ff` (đủ handoff lịch sử trong `AI/AI_HANDOFF.md` của nhánh đó). Thư mục game trên máy: `E:\games\Ra2\Ra2026` (vẫn là repo git theo dõi `main` cũ → người dùng cần chuyển sang `ra2026-legacy`, KHÔNG pull main ở đó).
- Bố cục dự kiến trên máy: `E:\games\Ra2\RAReborn` (repo này) cạnh `E:\games\Ra2\Ra2026` (file game).

## Trạng thái (2026-11-04)
| Hạng mục | Trạng thái |
|---|---|
| Build engine + mod (Linux, .NET 6.0.428) | ✅ `make` 0 cảnh báo |
| Đọc file game từ `../Ra2026` (+ `../../Ra2026`, `Support/Content/rareborn`) | ✅ kiểm chứng: có file 0 hình thiếu, bỏ file 2.349 hình thiếu |
| Nạp mix YR (ra2md, langmd, expandmd01, multimd, cachemd, cameomd, conqmd, genermd, iso*md, loadmd, localmd, ntrlmd, sidec02md, snowmd, audiomd) sau RA2 | ✅ |
| 4 bậc: rank-veteran (Đồng, 400%), rank-gold (Vàng, 900%), rank-elite (Kim cương, 1500%) | ✅ `--check-yaml` sạch; `--resolved-rules e1` có đủ 3 WithDecoration |
| Huy hiệu mới 16×16 (`artsrc/ranks/make_ranks.py`, palette `rank` từ rank-bronze.png) | ✅ (sửa luôn lỗi: pips.shp YR đè RA2 làm sequence cũ Start 13/14 trỏ sai hình) |
| Portable: `launch-game.cmd` tạo `Support\` cạnh game | ✅ |
| Phe Yuri | 🚧 chưa làm |
| Chạy thử trên Windows | ⏳ chưa |

## Kỹ thuật cần nhớ
- OpenRA FileSystem: gói nạp SAU được ưu tiên (`LastOrDefault`).
- `utility.sh` có EngineDir = thư mục `engine/` (nên ../Ra2026 = repo/Ra2026 — trong container là symlink tới file game đã stage); `launch-game.cmd` đặt `Engine.EngineDir=".."` = thư mục repo (../Ra2026 = E:\games\Ra2\Ra2026).
- Engine tải bằng `git clone --branch release-20231010` khi zip GitHub bị chặn; ghi `engine/VERSION`.
- Mod chỉ có 2 phe; Yuri là lính Liên Xô. Trait sẵn có: MindController/MindControllable, Carrier/BaseSpawner, Mirage, TintedCells, PeriodicExplosion, WeatherControl, ChronoResourceDelivery. Thiếu: Grinder, Slave Miner, Gatling tăng tốc, Magnetron, Chaos gas, Genetic Mutator, Psychic Dominator, Cloning Vats.
- Người dùng đã đồng ý (04/11 11:14) cho chạy mã OpenRA build từ GitHub.

## Việc tiếp theo
1. Phe Yuri mốc 1a: faction + nhà + quân từ rulesmd (art YR), cơ chế đặc biệt làm đơn giản.
2. Bản build Windows chạy thử (hoặc hướng dẫn make.cmd) → người dùng test 4 bậc + 3 phe.
3. Mốc 1b: viết trait C# cho cơ chế Yuri.
