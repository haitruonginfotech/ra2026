/* Ra2026 portable launcher: creates the mutex the game expects from the
 * original Westwood launcher, then starts the game from its own folder.
 * Writes nothing: no registry, no files. */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#ifndef GAME_EXE
#define GAME_EXE "gamemd.exe"
#endif

int WINAPI WinMain(HINSTANCE hi, HINSTANCE hp, LPSTR args, int show)
{
    char dir[MAX_PATH], exe[MAX_PATH], cmd[MAX_PATH * 2 + 512], *p;
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    HANDLE mtx;

    GetModuleFileNameA(NULL, dir, MAX_PATH);
    p = strrchr(dir, '\\');
    if (p) *p = 0;
    wsprintfA(exe, "%s\\%s", dir, GAME_EXE);
    if (GetFileAttributesA(exe) == INVALID_FILE_ATTRIBUTES) {
        MessageBoxA(NULL, "Khong tim thay " GAME_EXE " trong thu muc game.", "Ra2026", MB_ICONERROR);
        return 1;
    }
    wsprintfA(cmd, "\"%s\" %s", exe, args ? args : "");

    mtx = CreateMutexA(NULL, FALSE, "48BC11BD-C4D7-466b-8A31-C6ABBAD47B3E");

    ZeroMemory(&si, sizeof si);
    si.cb = sizeof si;
    if (!CreateProcessA(exe, cmd, NULL, NULL, FALSE, 0, NULL, dir, &si, &pi)) {
        MessageBoxA(NULL, "Khong chay duoc " GAME_EXE ".", "Ra2026", MB_ICONERROR);
        if (mtx) CloseHandle(mtx);
        return 1;
    }
    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    if (mtx) CloseHandle(mtx);
    return 0;
}
