#!/bin/bash
# RA Reborn — đóng gói bản Windows portable (x64, .NET kèm sẵn, bấm RAReborn.exe là chạy).
# Không tạo bộ cài, không ghi registry. Cài đặt/save nằm trong thư mục Support cạnh exe.
#
# Dùng (Linux, cần .NET 6 SDK, python3, zip):  packaging/windows/build-portable.sh <version> [thư mục ra]
# Kết quả: <thư mục ra>/RAReborn/ và <thư mục ra>/RAReborn-<version>-win-x64-portable.zip
# Đặt thư mục RAReborn cạnh thư mục game:  E:\games\Ra2\RAReborn  +  E:\games\Ra2\Ra2026
set -e

if [ $# -eq 0 ]; then echo "Usage: $(basename "$0") version [outputdir]"; exit 1; fi
TAG="$1"
PACKAGING_DIR=$(python3 -c "import os; print(os.path.dirname(os.path.realpath('$0')))")
TEMPLATE_ROOT=$(python3 -c "import os; print(os.path.realpath('${PACKAGING_DIR}/../..'))")
OUTPUTDIR=$(python3 -c "import os; print(os.path.realpath('${2:-.}'))")
. "${TEMPLATE_ROOT}/mod.config"
[ -f "${TEMPLATE_ROOT}/user.config" ] && . "${TEMPLATE_ROOT}/user.config"

ENGINE="${TEMPLATE_ROOT}/${ENGINE_DIRECTORY}"
[ -f "${ENGINE}/Makefile" ] || { echo "Engine not found: run make first"; exit 1; }
. "${ENGINE}/packaging/functions.sh"
. "${TEMPLATE_ROOT}/packaging/functions.sh"

PLATFORM="win-x64"
BUILTDIR="${OUTPUTDIR}/${PACKAGING_WINDOWS_LAUNCHER_NAME}"
rm -rf "${BUILTDIR}"; mkdir -p "${BUILTDIR}"

echo "== Engine (${PLATFORM}, self-contained)"
install_assemblies "${ENGINE}" "${BUILTDIR}" "${PLATFORM}" "net6" "False" "${PACKAGING_COPY_CNC_DLL}" "${PACKAGING_COPY_D2K_DLL}"
install_data "${ENGINE}" "${BUILTDIR}"
for f in ${PACKAGING_COPY_ENGINE_FILES}; do
	mkdir -p "${BUILTDIR}/$(dirname "${f}")"
	cp -r "${ENGINE}/${f}" "${BUILTDIR}/${f}"
done

echo "== Mod ${MOD_ID}"
install_mod_assemblies "${TEMPLATE_ROOT}" "${BUILTDIR}" "${PLATFORM}" "net6" "${ENGINE}"
cp -Lr "${TEMPLATE_ROOT}/mods/"* "${BUILTDIR}/mods"
set_engine_version "${ENGINE_VERSION}" "${BUILTDIR}"
set_mod_version "${TAG}" "${BUILTDIR}/mods/${MOD_ID}/mod.yaml"

echo "== Launcher ${PACKAGING_WINDOWS_LAUNCHER_NAME}.exe"
install_windows_launcher "${ENGINE}" "${BUILTDIR}" "${PLATFORM}" "${MOD_ID}" "${PACKAGING_WINDOWS_LAUNCHER_NAME}" "${PACKAGING_DISPLAY_NAME}" "${PACKAGING_FAQ_URL}" "${TAG}"

# Chế độ portable: OpenRA dùng <thư mục exe>\Support thay cho %APPDATA%\OpenRA khi thư mục này tồn tại.
mkdir -p "${BUILTDIR}/Support"
printf 'RA Reborn portable: cai dat, save, log luu o day (khong ghi vao AppData).\r\n' > "${BUILTDIR}/Support/README.txt"
cp "${TEMPLATE_ROOT}/README.md" "${BUILTDIR}/README.md"
cp "${TEMPLATE_ROOT}/README.en.md" "${BUILTDIR}/README.en.md"
cp "${TEMPLATE_ROOT}/LICENSE" "${BUILTDIR}/LICENSE.txt"

echo "== Zip"
( cd "${OUTPUTDIR}" && rm -f "RAReborn-${TAG}-${PLATFORM}-portable.zip" && zip -r -9 -q "RAReborn-${TAG}-${PLATFORM}-portable.zip" "${PACKAGING_WINDOWS_LAUNCHER_NAME}" )
echo "Done: ${BUILTDIR}"
