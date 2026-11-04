/*
 * Ra2026 portable guard (binkw32.dll proxy)
 *
 * Loaded by game.exe / gamemd.exe because they import binkw32.dll.
 * All Bink exports are forwarded to binkw32_o.dll (the original).
 *
 * On load it patches the import tables of the game exe and of every DLL
 * that lives inside the game folder so that:
 *   - the game only ever receives VIRTUAL registry handles; writes go to
 *     <game>\portable\registry.txt, reads fall back to the real registry
 *     opened READ-ONLY (so nothing can be written there)
 *   - file writes / directory creation / delete / move outside the game
 *     folder are refused and logged to <game>\portable\blocked.log
 *   - CoCreateInstance: when Windows says a class is not registered (because
 *     the game registered it only in the virtual registry, e.g. Blowfish.dll),
 *     the in-proc server DLL listed there is loaded straight from the game
 *     folder (registration-free COM).  Without this the game stops with
 *     "String Manager failed to initialize properly" on real Windows.
 */
#define WIN32_LEAN_AND_MEAN
#define _WIN32_WINNT 0x0601
#include <windows.h>
#include <objbase.h>
#include <tlhelp32.h>
#include <wchar.h>
#include <stdlib.h>


static WCHAR g_dir[MAX_PATH];      /* game folder, long form, no trailing slash */
static WCHAR g_dirShort[MAX_PATH]; /* 8.3 form */
static WCHAR g_portable[MAX_PATH];
static HMODULE g_self;
static CRITICAL_SECTION g_cs;

/* ------------------------------------------------------------------ util */

static void logtag(const char *tag, const WCHAR *what, const WCHAR *arg)
{
    WCHAR path[MAX_PATH];
    char buf[1400];
    SYSTEMTIME st;
    HANDLE h;
    DWORD n;
    int len;
    CreateDirectoryW(g_portable, NULL);
    wsprintfW(path, L"%s\\blocked.log", g_portable);
    h = CreateFileW(path, FILE_APPEND_DATA, FILE_SHARE_READ | FILE_SHARE_WRITE, NULL,
                    OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (h == INVALID_HANDLE_VALUE) return;
    GetLocalTime(&st);
    len = wsprintfA(buf, "%04d-%02d-%02d %02d:%02d:%02d  %s %ls  %ls\r\n",
                    st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond,
                    tag, what, arg ? arg : L"");
    WriteFile(h, buf, len, &n, NULL);
    CloseHandle(h);
}
static void logline(const WCHAR *what, const WCHAR *arg) { logtag("BLOCKED", what, arg); }

static int has_prefix_ci(const WCHAR *s, const WCHAR *pre)
{
    size_t n = wcslen(pre);
    if (!n || _wcsnicmp(s, pre, n) != 0) return 0;
    return s[n] == 0 || s[n] == L'\\' || s[n] == L'/';
}

/* returns 1 if the path is inside the game folder */
static int inside_w(const WCHAR *p)
{
    WCHAR full[MAX_PATH * 2];
    DWORD n;
    if (!p || !*p) return 1;
    if (_wcsicmp(p, L"NUL") == 0 || _wcsicmp(p, L"\\\\.\\NUL") == 0) return 1;
    n = GetFullPathNameW(p, MAX_PATH * 2, full, NULL);
    if (!n || n >= MAX_PATH * 2) return 0;
    return has_prefix_ci(full, g_dir) || (g_dirShort[0] && has_prefix_ci(full, g_dirShort));
}

static WCHAR *a2w(const char *s, WCHAR *out, int cap)
{
    if (!s) return NULL;
    if (!MultiByteToWideChar(CP_ACP, 0, s, -1, out, cap)) out[0] = 0;
    return out;
}

/* WritePrivateProfileString with a bare file name writes to C:\Windows */
static int profile_inside(const WCHAR *f)
{
    if (!f) return 0;
    if (!wcschr(f, L'\\') && !wcschr(f, L'/')) return 0;
    return inside_w(f);
}

/* -------------------------------------------------------------- registry
 * Virtual registry.  Every key handle given to the game is a virtual handle
 * (root + path).  Writes go to an in-memory tree that is saved to
 * <game>\portable\registry.txt.  Reads look at the tree first, then at the
 * real registry opened KEY_READ only.  No real key handle ever reaches the
 * game, so nothing can be written to the Windows registry.
 */

typedef struct VAL { struct VAL *next; char name[260]; DWORD type, cb; BYTE *data; } VAL;
typedef struct NODE { struct NODE *child, *next; char name[260]; VAL *vals; } NODE;
typedef struct VH { DWORD magic; HKEY root; char path[1024]; } VH;
#define VH_MAGIC 0x52413236u /* 'RA26' */

static NODE g_roots[6];       /* index = predefined key & 0xF */
static volatile LONG g_vregInit;
static HANDLE g_heap;

static int is_predef(HKEY h)
{
    ULONG_PTR v = (ULONG_PTR)h;
    return (v & 0xFFFFFFF0u) == 0x80000000u && (v & 0xF) < 6;
}

static VH *as_vh(HKEY h)
{
    ULONG_PTR v = (ULONG_PTR)h;
    VH *p;
    if ((v & 3) != 1) return NULL;          /* real handles are multiples of 4 */
    p = (VH *)(v & ~(ULONG_PTR)3);
    return p->magic == VH_MAGIC ? p : NULL;
}

static HKEY new_vh(HKEY root, const char *path)
{
    VH *p = (VH *)HeapAlloc(g_heap, HEAP_ZERO_MEMORY, sizeof(VH));
    if (!p) return NULL;
    p->magic = VH_MAGIC;
    p->root = root;
    lstrcpynA(p->path, path, sizeof p->path);
    return (HKEY)((ULONG_PTR)p | 1);
}

/* join base path and sub path, normalising slashes */
static void join(char *out, const char *base, const char *sub)
{
    int n = 0;
    const char *s;
    out[0] = 0;
    for (s = base; s && *s && n < 1000; s++) out[n++] = *s;
    if (sub && *sub) {
        if (n && out[n - 1] != '\\') out[n++] = '\\';
        for (s = sub; *s && n < 1000; s++) out[n++] = (*s == '/') ? '\\' : *s;
    }
    while (n && out[n - 1] == '\\') n--;
    out[n] = 0;
    while (out[0] == '\\') memmove(out, out + 1, lstrlenA(out));
}

static NODE *find_child(NODE *n, const char *name, int len)
{
    NODE *c;
    for (c = n->child; c; c = c->next)
        if (lstrlenA(c->name) == len && CompareStringA(LOCALE_INVARIANT, NORM_IGNORECASE, c->name, len, name, len) == CSTR_EQUAL)
            return c;
    return NULL;
}

/* walk path; create missing nodes if mk */
static NODE *walk(HKEY root, const char *path, int mk)
{
    NODE *n = &g_roots[(ULONG_PTR)root & 0xF];
    const char *p = path;
    while (p && *p) {
        const char *e = p;
        int len;
        NODE *c;
        while (*e && *e != '\\') e++;
        len = (int)(e - p);
        if (len) {
            c = find_child(n, p, len);
            if (!c) {
                if (!mk) return NULL;
                c = (NODE *)HeapAlloc(g_heap, HEAP_ZERO_MEMORY, sizeof(NODE));
                if (!c) return NULL;
                lstrcpynA(c->name, p, len + 1 > 260 ? 260 : len + 1);
                c->next = n->child;
                n->child = c;
            }
            n = c;
        }
        p = *e ? e + 1 : e;
    }
    return n;
}

static VAL *find_val(NODE *n, const char *name)
{
    VAL *v;
    if (!name) name = "";
    for (v = n ? n->vals : NULL; v; v = v->next)
        if (lstrcmpiA(v->name, name) == 0) return v;
    return NULL;
}

static int real_exists(HKEY root, const char *path)
{
    HKEY k;
    if (RegOpenKeyExA(root, path[0] ? path : NULL, 0, KEY_READ, &k) != ERROR_SUCCESS) return 0;
    if (!is_predef(k)) RegCloseKey(k);
    return 1;
}

/* ---- persistence: portable\registry.txt ---- */

static void hexout(char **o, const BYTE *d, DWORD n)
{
    static const char hx[] = "0123456789abcdef";
    DWORD i;
    for (i = 0; i < n; i++) { *(*o)++ = hx[d[i] >> 4]; *(*o)++ = hx[d[i] & 15]; }
}

static int hexval(char c) { return c >= '0' && c <= '9' ? c - '0' : c >= 'a' && c <= 'f' ? c - 'a' + 10 : c >= 'A' && c <= 'F' ? c - 'A' + 10 : -1; }

static DWORD hexin(const char *s, BYTE *out, DWORD cap)
{
    DWORD n = 0;
    while (s[0] && s[1] && hexval(s[0]) >= 0 && hexval(s[1]) >= 0 && n < cap) { out[n++] = (BYTE)(hexval(s[0]) * 16 + hexval(s[1])); s += 2; }
    return n;
}

typedef struct { HANDLE f; } SAVECTX;

static void save_node(SAVECTX *sc, int root, NODE *n, char *path, int plen)
{
    NODE *c;
    VAL *v;
    char *buf, *o;
    DWORD wr, need = 64 + (DWORD)plen * 2;
    for (v = n->vals; v; v = v->next) need += 64 + lstrlenA(v->name) * 2 + v->cb * 2;
    buf = (char *)HeapAlloc(g_heap, 0, need);
    if (buf) {
        o = buf + wsprintfA(buf, "K %d ", root);
        hexout(&o, (const BYTE *)path, plen);
        *o++ = '\r'; *o++ = '\n';
        for (v = n->vals; v; v = v->next) {
            *o++ = 'V'; *o++ = ' ';
            if (v->name[0]) hexout(&o, (const BYTE *)v->name, lstrlenA(v->name)); else *o++ = '-';
            o += wsprintfA(o, " %lu ", v->type);
            if (v->cb) hexout(&o, v->data, v->cb); else *o++ = '-';
            *o++ = '\r'; *o++ = '\n';
        }
        WriteFile(sc->f, buf, (DWORD)(o - buf), &wr, NULL);
        HeapFree(g_heap, 0, buf);
    }
    for (c = n->child; c; c = c->next) {
        int l = plen;
        if (l) path[l++] = '\\';
        lstrcpynA(path + l, c->name, 1100 - l);
        save_node(sc, root, c, path, lstrlenA(path));
        path[plen] = 0;
    }
}

static void vreg_save(void)
{
    WCHAR fn[MAX_PATH], tmp[MAX_PATH];
    SAVECTX sc;
    char path[1200];
    int r;
    CreateDirectoryW(g_portable, NULL);
    wsprintfW(fn, L"%s\\registry.txt", g_portable);
    wsprintfW(tmp, L"%s\\registry.tmp", g_portable);
    sc.f = CreateFileW(tmp, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
    if (sc.f == INVALID_HANDLE_VALUE) return;
    for (r = 0; r < 6; r++) { path[0] = 0; if (g_roots[r].child || g_roots[r].vals) save_node(&sc, r, &g_roots[r], path, 0); }
    CloseHandle(sc.f);
    MoveFileExW(tmp, fn, MOVEFILE_REPLACE_EXISTING);
}

static void set_val(NODE *n, const char *name, DWORD type, const BYTE *d, DWORD cb)
{
    VAL *v = find_val(n, name);
    if (!v) {
        v = (VAL *)HeapAlloc(g_heap, HEAP_ZERO_MEMORY, sizeof(VAL));
        if (!v) return;
        lstrcpynA(v->name, name ? name : "", 260);
        v->next = n->vals;
        n->vals = v;
    }
    if (v->data) HeapFree(g_heap, 0, v->data);
    v->data = cb ? (BYTE *)HeapAlloc(g_heap, 0, cb) : NULL;
    v->cb = v->data ? cb : 0;
    if (v->data && d) CopyMemory(v->data, d, cb);
    v->type = type;
}

static void vreg_load(void)
{
    WCHAR fn[MAX_PATH];
    HANDLE f;
    DWORD sz, rd;
    char *buf, *line, *nl;
    NODE *cur = NULL;
    wsprintfW(fn, L"%s\\registry.txt", g_portable);
    f = CreateFileW(fn, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (f == INVALID_HANDLE_VALUE) return;
    sz = GetFileSize(f, NULL);
    buf = (sz != INVALID_FILE_SIZE && sz < 64 * 1024 * 1024) ? (char *)HeapAlloc(g_heap, 0, sz + 1) : NULL;
    if (!buf || !ReadFile(f, buf, sz, &rd, NULL)) { CloseHandle(f); return; }
    CloseHandle(f);
    buf[rd] = 0;
    for (line = buf; line && *line; line = nl) {
        nl = line;
        while (*nl && *nl != '\n') nl++;
        if (*nl) *nl++ = 0;
        if (line[0] == 'K' && line[1] == ' ') {
            int root = line[2] - '0';
            char path[1100];
            DWORD n = hexin(line + 4, (BYTE *)path, sizeof path - 1);
            path[n] = 0;
            cur = (root >= 0 && root < 6) ? walk((HKEY)(ULONG_PTR)(0x80000000u | root), path, 1) : NULL;
        } else if (line[0] == 'V' && line[1] == ' ' && cur) {
            char name[260], *p = line + 2, *q;
            BYTE *data;
            DWORD type, n = 0;
            if (*p == '-') { name[0] = 0; p++; }
            else { n = hexin(p, (BYTE *)name, 259); name[n] = 0; p += n * 2; }
            while (*p == ' ') p++;
            type = strtoul(p, &q, 10);
            p = q;
            while (*p == ' ') p++;
            n = (DWORD)lstrlenA(p) / 2 + 1;
            data = (BYTE *)HeapAlloc(g_heap, 0, n);
            if (data) {
                n = (*p == '-') ? 0 : hexin(p, data, n);
                set_val(cur, name, type, data, n);
                HeapFree(g_heap, 0, data);
            }
        }
    }
    HeapFree(g_heap, 0, buf);
}

static void vreg_init(void)
{
    if (g_vregInit == 2) return;
    EnterCriticalSection(&g_cs);
    if (g_vregInit != 2) { vreg_load(); g_vregInit = 2; }
    LeaveCriticalSection(&g_cs);
}

/* resolve (handle, sub) -> root + full path.  returns 0 if handle is foreign */
static int resolve(HKEY h, const char *sub, HKEY *root, char *full)
{
    VH *v;
    if (is_predef(h)) { *root = h; join(full, "", sub); return 1; }
    if ((v = as_vh(h))) { *root = v->root; join(full, v->path, sub); return 1; }
    return 0;
}

static LONG v_open(HKEY h, const char *sub, PHKEY out)
{
    HKEY root;
    char full[1100];
    LONG r;
    if (!out) return ERROR_INVALID_PARAMETER;
    vreg_init();
    EnterCriticalSection(&g_cs);
    if (!resolve(h, sub, &root, full)) r = ERROR_INVALID_HANDLE;
    else if (walk(root, full, 0) || real_exists(root, full)) r = (*out = new_vh(root, full)) ? ERROR_SUCCESS : ERROR_OUTOFMEMORY;
    else r = ERROR_FILE_NOT_FOUND;
    LeaveCriticalSection(&g_cs);
    return r;
}

static LONG v_create(HKEY h, const char *sub, PHKEY out, LPDWORD disp)
{
    HKEY root;
    char full[1100];
    LONG r;
    int existed;
    if (!out) return ERROR_INVALID_PARAMETER;
    vreg_init();
    EnterCriticalSection(&g_cs);
    if (!resolve(h, sub, &root, full)) r = ERROR_INVALID_HANDLE;
    else {
        existed = walk(root, full, 0) || real_exists(root, full);
        if (!walk(root, full, 1)) r = ERROR_OUTOFMEMORY;
        else {
            if (!existed) vreg_save();
            if (disp) *disp = existed ? REG_OPENED_EXISTING_KEY : REG_CREATED_NEW_KEY;
            r = (*out = new_vh(root, full)) ? ERROR_SUCCESS : ERROR_OUTOFMEMORY;
        }
    }
    LeaveCriticalSection(&g_cs);
    return r;
}

static LONG v_set(HKEY h, const char *sub, const char *name, DWORD type, const BYTE *d, DWORD cb)
{
    HKEY root;
    char full[1100];
    NODE *n;
    LONG r = ERROR_SUCCESS;
    vreg_init();
    EnterCriticalSection(&g_cs);
    if (!resolve(h, sub, &root, full)) r = ERROR_INVALID_HANDLE;
    else if (!(n = walk(root, full, 1))) r = ERROR_OUTOFMEMORY;
    else { set_val(n, name, type, d, cb); vreg_save(); }
    LeaveCriticalSection(&g_cs);
    return r;
}

static LONG v_query(HKEY h, const char *name, LPDWORD type, LPBYTE data, LPDWORD cb)
{
    HKEY root, k;
    char full[1100];
    VAL *v;
    LONG r;
    vreg_init();
    EnterCriticalSection(&g_cs);
    if (!resolve(h, NULL, &root, full)) { LeaveCriticalSection(&g_cs); return ERROR_INVALID_HANDLE; }
    v = find_val(walk(root, full, 0), name);
    if (v) {
        if (type) *type = v->type;
        r = ERROR_SUCCESS;
        if (data) {
            if (!cb) r = ERROR_INVALID_PARAMETER;
            else if (*cb < v->cb) r = ERROR_MORE_DATA;
            else if (v->cb) CopyMemory(data, v->data, v->cb);
        }
        if (cb) *cb = v->cb;
        LeaveCriticalSection(&g_cs);
        return r;
    }
    LeaveCriticalSection(&g_cs);
    r = RegOpenKeyExA(root, full[0] ? full : NULL, 0, KEY_READ, &k);
    if (r != ERROR_SUCCESS) return ERROR_FILE_NOT_FOUND;
    r = RegQueryValueExA(k, name, NULL, type, data, cb);
    if (!is_predef(k)) RegCloseKey(k);
    return r;
}

/* list union of virtual + real sub key names (index -> name) */
static LONG v_enumkey(HKEY h, DWORD idx, char *name, LPDWORD cch, DWORD *count, DWORD *maxlen)
{
    HKEY root, k;
    char full[1100], nm[260];
    NODE *n, *c;
    DWORD i = 0, ml = 0, j, l;
    LONG found = ERROR_NO_MORE_ITEMS;
    vreg_init();
    EnterCriticalSection(&g_cs);
    if (!resolve(h, NULL, &root, full)) { LeaveCriticalSection(&g_cs); return ERROR_INVALID_HANDLE; }
    n = walk(root, full, 0);
    for (c = n ? n->child : NULL; c; c = c->next, i++) {
        l = lstrlenA(c->name);
        if (l > ml) ml = l;
        if (i == idx && name) {
            if (*cch <= l) found = ERROR_MORE_DATA;
            else { lstrcpyA(name, c->name); *cch = l; found = ERROR_SUCCESS; }
        }
    }
    if (RegOpenKeyExA(root, full[0] ? full : NULL, 0, KEY_READ, &k) == ERROR_SUCCESS) {
        for (j = 0;; j++) {
            DWORD c2 = sizeof nm;
            if (RegEnumKeyExA(k, j, nm, &c2, NULL, NULL, NULL, NULL) != ERROR_SUCCESS) break;
            if (n && find_child(n, nm, (int)c2)) continue;
            if (c2 > ml) ml = c2;
            if (i == idx && name) {
                if (*cch <= c2) found = ERROR_MORE_DATA;
                else { lstrcpyA(name, nm); *cch = c2; found = ERROR_SUCCESS; }
            }
            i++;
        }
        if (!is_predef(k)) RegCloseKey(k);
    }
    LeaveCriticalSection(&g_cs);
    if (count) *count = i;
    if (maxlen) *maxlen = ml;
    return found;
}

static LONG v_delkey(HKEY h, const char *sub)
{
    HKEY root;
    char full[1100], parent[1100], *last;
    NODE *p, **pp;
    LONG r = ERROR_FILE_NOT_FOUND;
    vreg_init();
    EnterCriticalSection(&g_cs);
    if (!resolve(h, sub, &root, full)) { LeaveCriticalSection(&g_cs); return ERROR_INVALID_HANDLE; }
    lstrcpyA(parent, full);
    last = strrchr(parent, '\\');
    if (last) *last++ = 0; else { last = full; parent[0] = 0; }
    p = walk(root, parent, 0);
    if (p) {
        for (pp = &p->child; *pp; pp = &(*pp)->next)
            if (lstrcmpiA((*pp)->name, last) == 0) { *pp = (*pp)->next; r = ERROR_SUCCESS; vreg_save(); break; }
    }
    if (r != ERROR_SUCCESS && real_exists(root, full)) r = ERROR_SUCCESS; /* pretend; real key untouched */
    LeaveCriticalSection(&g_cs);
    return r;
}

static LONG v_delval(HKEY h, const char *name)
{
    HKEY root;
    char full[1100];
    NODE *n;
    VAL **pv;
    LONG r = ERROR_FILE_NOT_FOUND;
    vreg_init();
    EnterCriticalSection(&g_cs);
    if (!resolve(h, NULL, &root, full)) { LeaveCriticalSection(&g_cs); return ERROR_INVALID_HANDLE; }
    if (!name) name = "";
    if ((n = walk(root, full, 0)))
        for (pv = &n->vals; *pv; pv = &(*pv)->next)
            if (lstrcmpiA((*pv)->name, name) == 0) { *pv = (*pv)->next; r = ERROR_SUCCESS; vreg_save(); break; }
    if (r != ERROR_SUCCESS) {
        HKEY k;
        if (RegOpenKeyExA(root, full[0] ? full : NULL, 0, KEY_READ, &k) == ERROR_SUCCESS) {
            if (RegQueryValueExA(k, name, NULL, NULL, NULL, NULL) == ERROR_SUCCESS) r = ERROR_SUCCESS;
            if (!is_predef(k)) RegCloseKey(k);
        }
    }
    LeaveCriticalSection(&g_cs);
    return r;
}

static char *w2a(LPCWSTR s, char *out, int cap)
{
    if (!s) return NULL;
    if (!WideCharToMultiByte(CP_ACP, 0, s, -1, out, cap, NULL, NULL)) out[0] = 0;
    return out;
}

#define FOREIGN(h) (!is_predef(h) && !as_vh(h))

static LONG WINAPI H_RegOpenKeyExA(HKEY h, LPCSTR sub, DWORD opt, REGSAM sam, PHKEY out)
{ if (FOREIGN(h)) return RegOpenKeyExA(h, sub, opt, sam, out); return v_open(h, sub, out); }
static LONG WINAPI H_RegOpenKeyExW(HKEY h, LPCWSTR sub, DWORD opt, REGSAM sam, PHKEY out)
{ char a[1024]; if (FOREIGN(h)) return RegOpenKeyExW(h, sub, opt, sam, out); return v_open(h, w2a(sub, a, 1024), out); }
static LONG WINAPI H_RegOpenKeyA(HKEY h, LPCSTR sub, PHKEY out)
{ if (FOREIGN(h)) return RegOpenKeyA(h, sub, out); return v_open(h, sub, out); }
static LONG WINAPI H_RegOpenKeyW(HKEY h, LPCWSTR sub, PHKEY out)
{ char a[1024]; if (FOREIGN(h)) return RegOpenKeyW(h, sub, out); return v_open(h, w2a(sub, a, 1024), out); }

static LONG WINAPI H_RegCreateKeyExA(HKEY h, LPCSTR sub, DWORD res, LPSTR cls, DWORD opt, REGSAM sam,
                                     const LPSECURITY_ATTRIBUTES sa, PHKEY out, LPDWORD disp)
{ if (FOREIGN(h)) return RegCreateKeyExA(h, sub, res, cls, opt, sam, sa, out, disp); return v_create(h, sub, out, disp); }
static LONG WINAPI H_RegCreateKeyExW(HKEY h, LPCWSTR sub, DWORD res, LPWSTR cls, DWORD opt, REGSAM sam,
                                     const LPSECURITY_ATTRIBUTES sa, PHKEY out, LPDWORD disp)
{ char a[1024]; if (FOREIGN(h)) return RegCreateKeyExW(h, sub, res, cls, opt, sam, sa, out, disp); return v_create(h, w2a(sub, a, 1024), out, disp); }
static LONG WINAPI H_RegCreateKeyA(HKEY h, LPCSTR sub, PHKEY out)
{ if (FOREIGN(h)) return RegCreateKeyA(h, sub, out); return v_create(h, sub, out, NULL); }
static LONG WINAPI H_RegCreateKeyW(HKEY h, LPCWSTR sub, PHKEY out)
{ char a[1024]; if (FOREIGN(h)) return RegCreateKeyW(h, sub, out); return v_create(h, w2a(sub, a, 1024), out, NULL); }

static LONG WINAPI H_RegSetValueExA(HKEY h, LPCSTR name, DWORD res, DWORD type, const BYTE *d, DWORD cb)
{ if (FOREIGN(h)) return RegSetValueExA(h, name, res, type, d, cb); return v_set(h, NULL, name, type, d, cb); }
static LONG WINAPI H_RegSetValueExW(HKEY h, LPCWSTR name, DWORD res, DWORD type, const BYTE *d, DWORD cb)
{ char a[260]; if (FOREIGN(h)) return RegSetValueExW(h, name, res, type, d, cb); return v_set(h, NULL, name ? w2a(name, a, 260) : NULL, type, d, cb); }
static LONG WINAPI H_RegSetValueA(HKEY h, LPCSTR sub, DWORD type, LPCSTR d, DWORD cb)
{ if (FOREIGN(h)) return RegSetValueA(h, sub, type, d, cb); return v_set(h, sub, "", REG_SZ, (const BYTE *)d, d ? lstrlenA(d) + 1 : 0); }
static LONG WINAPI H_RegSetValueW(HKEY h, LPCWSTR sub, DWORD type, LPCWSTR d, DWORD cb)
{ char a[1024]; if (FOREIGN(h)) return RegSetValueW(h, sub, type, d, cb); return v_set(h, w2a(sub, a, 1024), "", REG_SZ, (const BYTE *)d, d ? (lstrlenW(d) + 1) * 2 : 0); }

static LONG WINAPI H_RegQueryValueExA(HKEY h, LPCSTR name, LPDWORD res, LPDWORD type, LPBYTE data, LPDWORD cb)
{ if (FOREIGN(h)) return RegQueryValueExA(h, name, res, type, data, cb); return v_query(h, name, type, data, cb); }
static LONG WINAPI H_RegQueryValueExW(HKEY h, LPCWSTR name, LPDWORD res, LPDWORD type, LPBYTE data, LPDWORD cb)
{ char a[260]; if (FOREIGN(h)) return RegQueryValueExW(h, name, res, type, data, cb); return v_query(h, name ? w2a(name, a, 260) : NULL, type, data, cb); }

static LONG WINAPI H_RegEnumKeyExA(HKEY h, DWORD i, LPSTR name, LPDWORD cch, LPDWORD res, LPSTR cls, LPDWORD ccls, PFILETIME ft)
{
    if (FOREIGN(h)) return RegEnumKeyExA(h, i, name, cch, res, cls, ccls, ft);
    if (ccls) *ccls = 0;
    if (ft) { ft->dwLowDateTime = ft->dwHighDateTime = 0; }
    return v_enumkey(h, i, name, cch, NULL, NULL);
}
static LONG WINAPI H_RegEnumKeyA(HKEY h, DWORD i, LPSTR name, DWORD cch)
{ if (FOREIGN(h)) return RegEnumKeyA(h, i, name, cch); return v_enumkey(h, i, name, &cch, NULL, NULL); }

static LONG WINAPI H_RegQueryInfoKeyA(HKEY h, LPSTR cls, LPDWORD ccls, LPDWORD res, LPDWORD nsub, LPDWORD maxsub,
                                      LPDWORD maxcls, LPDWORD nval, LPDWORD maxvname, LPDWORD maxvlen, LPDWORD sd, PFILETIME ft)
{
    HKEY root, k;
    char full[1100];
    NODE *n;
    VAL *v;
    DWORD cnt = 0, ml = 0, nv = 0, mvn = 0, mvl = 0, rnv = 0, rmvn = 0, rmvl = 0;
    if (FOREIGN(h)) return RegQueryInfoKeyA(h, cls, ccls, res, nsub, maxsub, maxcls, nval, maxvname, maxvlen, sd, ft);
    v_enumkey(h, 0xFFFFFFFF, NULL, NULL, &cnt, &ml);
    EnterCriticalSection(&g_cs);
    resolve(h, NULL, &root, full);
    n = walk(root, full, 0);
    for (v = n ? n->vals : NULL; v; v = v->next) { nv++; if ((DWORD)lstrlenA(v->name) > mvn) mvn = lstrlenA(v->name); if (v->cb > mvl) mvl = v->cb; }
    LeaveCriticalSection(&g_cs);
    if (RegOpenKeyExA(root, full[0] ? full : NULL, 0, KEY_READ, &k) == ERROR_SUCCESS) {
        RegQueryInfoKeyA(k, NULL, NULL, NULL, NULL, NULL, NULL, &rnv, &rmvn, &rmvl, NULL, NULL);
        if (!is_predef(k)) RegCloseKey(k);
    }
    if (cls && ccls && *ccls) cls[0] = 0;
    if (ccls) *ccls = 0;
    if (nsub) *nsub = cnt;
    if (maxsub) *maxsub = ml;
    if (maxcls) *maxcls = 0;
    if (nval) *nval = nv + rnv;
    if (maxvname) *maxvname = mvn > rmvn ? mvn : rmvn;
    if (maxvlen) *maxvlen = mvl > rmvl ? mvl : rmvl;
    if (sd) *sd = 0;
    if (ft) { ft->dwLowDateTime = ft->dwHighDateTime = 0; }
    return ERROR_SUCCESS;
}

static LONG WINAPI H_RegDeleteKeyA(HKEY h, LPCSTR sub)
{ if (FOREIGN(h)) return RegDeleteKeyA(h, sub); return v_delkey(h, sub); }
static LONG WINAPI H_RegDeleteKeyW(HKEY h, LPCWSTR sub)
{ char a[1024]; if (FOREIGN(h)) return RegDeleteKeyW(h, sub); return v_delkey(h, w2a(sub, a, 1024)); }
static LONG WINAPI H_RegDeleteValueA(HKEY h, LPCSTR name)
{ if (FOREIGN(h)) return RegDeleteValueA(h, name); return v_delval(h, name); }
static LONG WINAPI H_RegDeleteValueW(HKEY h, LPCWSTR name)
{ char a[260]; if (FOREIGN(h)) return RegDeleteValueW(h, name); return v_delval(h, name ? w2a(name, a, 260) : NULL); }

static LONG WINAPI H_RegCloseKey(HKEY h)
{
    VH *v;
    if (is_predef(h)) return ERROR_SUCCESS;
    if ((v = as_vh(h))) { v->magic = 0; HeapFree(g_heap, 0, v); return ERROR_SUCCESS; }
    return RegCloseKey(h);
}


/* ----------------------------------------------------------------- files */

#define FWRITE_BITS (GENERIC_WRITE | GENERIC_ALL | FILE_WRITE_DATA | FILE_APPEND_DATA | \
                     FILE_WRITE_ATTRIBUTES | FILE_WRITE_EA | DELETE | WRITE_DAC | WRITE_OWNER)

static int create_is_write(DWORD acc, DWORD disp)
{
    if (acc & FWRITE_BITS) return 1;
    return disp == CREATE_NEW || disp == CREATE_ALWAYS || disp == OPEN_ALWAYS || disp == TRUNCATE_EXISTING;
}

static HANDLE WINAPI H_CreateFileW(LPCWSTR p, DWORD acc, DWORD share, LPSECURITY_ATTRIBUTES sa,
                                   DWORD disp, DWORD fl, HANDLE tpl)
{
    if (create_is_write(acc, disp) && !inside_w(p)) {
        logline(L"CreateFile(write)", p);
        SetLastError(ERROR_ACCESS_DENIED);
        return INVALID_HANDLE_VALUE;
    }
    return CreateFileW(p, acc, share, sa, disp, fl, tpl);
}

static HANDLE WINAPI H_CreateFileA(LPCSTR p, DWORD acc, DWORD share, LPSECURITY_ATTRIBUTES sa,
                                   DWORD disp, DWORD fl, HANDLE tpl)
{
    WCHAR w[MAX_PATH * 2];
    if (create_is_write(acc, disp) && !inside_w(a2w(p, w, MAX_PATH * 2))) {
        logline(L"CreateFile(write)", w);
        SetLastError(ERROR_ACCESS_DENIED);
        return INVALID_HANDLE_VALUE;
    }
    return CreateFileA(p, acc, share, sa, disp, fl, tpl);
}

#define GUARD1W(fn, p) if (!inside_w(p)) { logline(L##fn, p); SetLastError(ERROR_ACCESS_DENIED); return FALSE; }
#define GUARD1A(fn, p) { WCHAR _w[MAX_PATH * 2]; if (!inside_w(a2w(p, _w, MAX_PATH * 2))) { logline(L##fn, _w); SetLastError(ERROR_ACCESS_DENIED); return FALSE; } }

static BOOL WINAPI H_CreateDirectoryA(LPCSTR p, LPSECURITY_ATTRIBUTES sa) { GUARD1A("CreateDirectory", p) return CreateDirectoryA(p, sa); }
static BOOL WINAPI H_CreateDirectoryW(LPCWSTR p, LPSECURITY_ATTRIBUTES sa) { GUARD1W("CreateDirectory", p) return CreateDirectoryW(p, sa); }
static BOOL WINAPI H_RemoveDirectoryA(LPCSTR p) { GUARD1A("RemoveDirectory", p) return RemoveDirectoryA(p); }
static BOOL WINAPI H_RemoveDirectoryW(LPCWSTR p) { GUARD1W("RemoveDirectory", p) return RemoveDirectoryW(p); }
static BOOL WINAPI H_DeleteFileA(LPCSTR p) { GUARD1A("DeleteFile", p) return DeleteFileA(p); }
static BOOL WINAPI H_DeleteFileW(LPCWSTR p) { GUARD1W("DeleteFile", p) return DeleteFileW(p); }
static BOOL WINAPI H_SetFileAttributesA(LPCSTR p, DWORD a) { GUARD1A("SetFileAttributes", p) return SetFileAttributesA(p, a); }
static BOOL WINAPI H_SetFileAttributesW(LPCWSTR p, DWORD a) { GUARD1W("SetFileAttributes", p) return SetFileAttributesW(p, a); }
static BOOL WINAPI H_CopyFileA(LPCSTR s, LPCSTR d, BOOL f) { GUARD1A("CopyFile", d) return CopyFileA(s, d, f); }
static BOOL WINAPI H_CopyFileW(LPCWSTR s, LPCWSTR d, BOOL f) { GUARD1W("CopyFile", d) return CopyFileW(s, d, f); }
static BOOL WINAPI H_MoveFileA(LPCSTR s, LPCSTR d) { GUARD1A("MoveFile", s) GUARD1A("MoveFile", d) return MoveFileA(s, d); }
static BOOL WINAPI H_MoveFileW(LPCWSTR s, LPCWSTR d) { GUARD1W("MoveFile", s) GUARD1W("MoveFile", d) return MoveFileW(s, d); }
static BOOL WINAPI H_MoveFileExA(LPCSTR s, LPCSTR d, DWORD f)
{
    GUARD1A("MoveFileEx", s)
    if (d) GUARD1A("MoveFileEx", d)
    if (f & MOVEFILE_DELAY_UNTIL_REBOOT) { logline(L"MoveFileEx(reboot)", NULL); SetLastError(ERROR_ACCESS_DENIED); return FALSE; }
    return MoveFileExA(s, d, f);
}
static BOOL WINAPI H_MoveFileExW(LPCWSTR s, LPCWSTR d, DWORD f)
{
    GUARD1W("MoveFileEx", s)
    if (d) GUARD1W("MoveFileEx", d)
    if (f & MOVEFILE_DELAY_UNTIL_REBOOT) { logline(L"MoveFileEx(reboot)", s); SetLastError(ERROR_ACCESS_DENIED); return FALSE; }
    return MoveFileExW(s, d, f);
}

static BOOL WINAPI H_WritePrivateProfileStringA(LPCSTR a, LPCSTR k, LPCSTR v, LPCSTR f)
{
    WCHAR w[MAX_PATH * 2];
    if (!profile_inside(a2w(f, w, MAX_PATH * 2))) { logline(L"WritePrivateProfileString", f ? w : L"win.ini"); SetLastError(ERROR_ACCESS_DENIED); return FALSE; }
    return WritePrivateProfileStringA(a, k, v, f);
}
static BOOL WINAPI H_WritePrivateProfileStringW(LPCWSTR a, LPCWSTR k, LPCWSTR v, LPCWSTR f)
{
    if (!profile_inside(f)) { logline(L"WritePrivateProfileString", f ? f : L"win.ini"); SetLastError(ERROR_ACCESS_DENIED); return FALSE; }
    return WritePrivateProfileStringW(a, k, v, f);
}
static BOOL WINAPI H_WritePrivateProfileSectionA(LPCSTR a, LPCSTR s, LPCSTR f)
{
    WCHAR w[MAX_PATH * 2];
    if (!profile_inside(a2w(f, w, MAX_PATH * 2))) { logline(L"WritePrivateProfileSection", f ? w : L"win.ini"); SetLastError(ERROR_ACCESS_DENIED); return FALSE; }
    return WritePrivateProfileSectionA(a, s, f);
}
static BOOL WINAPI H_WriteProfileStringA(LPCSTR a, LPCSTR k, LPCSTR v) { logline(L"WriteProfileString", L"win.ini"); SetLastError(ERROR_ACCESS_DENIED); return FALSE; }
static BOOL WINAPI H_WriteProfileStringW(LPCWSTR a, LPCWSTR k, LPCWSTR v) { logline(L"WriteProfileString", L"win.ini"); SetLastError(ERROR_ACCESS_DENIED); return FALSE; }

static void patch_module(HMODULE m);

/* ------------------------------------------------- COM (registration-free) */

typedef HRESULT (WINAPI *PFN_DGCO)(REFCLSID, REFIID, LPVOID *);

/* InprocServer32 of a class registered in the VIRTUAL registry (HKCR) */
static int vreg_inproc(REFCLSID clsid, WCHAR *dll, int cap)
{
    WCHAR g[64];
    char ga[64], path[160];
    VAL *v;
    dll[0] = 0;
    if (!StringFromGUID2(clsid, g, 64)) return 0;
    WideCharToMultiByte(CP_ACP, 0, g, -1, ga, sizeof ga, NULL, NULL);
    wsprintfA(path, "CLSID\\%s\\InprocServer32", ga);
    vreg_init();
    EnterCriticalSection(&g_cs);
    v = find_val(walk(HKEY_CLASSES_ROOT, path, 0), "");
    if (v && v->data && v->cb >= 2) {
        if (v->cb >= 4 && v->data[1] == 0)            /* stored by a ...W call */
            lstrcpynW(dll, (const WCHAR *)v->data, cap < (int)(v->cb / 2) ? cap : (int)(v->cb / 2) + 1);
        else
            MultiByteToWideChar(CP_ACP, 0, (const char *)v->data, -1, dll, cap);
    }
    LeaveCriticalSection(&g_cs);
    return dll[0] != 0;
}

static HRESULT WINAPI H_CoCreateInstance(REFCLSID clsid, LPUNKNOWN outer, DWORD ctx, REFIID riid, LPVOID *ppv)
{
    HRESULT hr = CoCreateInstance(clsid, outer, ctx, riid, ppv), hr2;
    WCHAR dll[MAX_PATH * 2], *ext;
    HMODULE m;
    PFN_DGCO dgco;
    IClassFactory *cf = NULL;
    if (hr != REGDB_E_CLASSNOTREG && hr != REGDB_E_READREGDB && hr != CO_E_DLLNOTFOUND && hr != CO_E_ERRORINDLL)
        return hr;
    if (!(ctx & CLSCTX_INPROC_SERVER) || !vreg_inproc(clsid, dll, MAX_PATH * 2)) return hr;
    ext = wcsrchr(dll, L'.');
    if (!inside_w(dll) || !ext || _wcsicmp(ext, L".dll") != 0) return hr;  /* only DLLs from the game folder */
    m = LoadLibraryW(dll);
    if (!m) return hr;
    patch_module(m);                                       /* keep its writes inside the folder too */
    dgco = (PFN_DGCO)GetProcAddress(m, "DllGetClassObject");
    if (!dgco) return hr;
    hr2 = dgco(clsid, &IID_IClassFactory, (LPVOID *)&cf);
    if (FAILED(hr2) || !cf) return hr;
    hr2 = cf->lpVtbl->CreateInstance(cf, outer, riid, ppv);
    cf->lpVtbl->Release(cf);
    if (SUCCEEDED(hr2)) logtag("COM-PORTABLE", L"CoCreateInstance", dll);
    return SUCCEEDED(hr2) ? hr2 : hr;
}

/* ------------------------------------------------------------ IAT patch */


static HMODULE after_load(HMODULE m)
{
    WCHAR p[MAX_PATH];
    if (m && m != g_self && GetModuleFileNameW(m, p, MAX_PATH) && inside_w(p)) patch_module(m);
    return m;
}

static HMODULE WINAPI H_LoadLibraryA(LPCSTR n) { return after_load(LoadLibraryA(n)); }
static HMODULE WINAPI H_LoadLibraryW(LPCWSTR n) { return after_load(LoadLibraryW(n)); }
static HMODULE WINAPI H_LoadLibraryExA(LPCSTR n, HANDLE f, DWORD fl) { return after_load(LoadLibraryExA(n, f, fl)); }
static HMODULE WINAPI H_LoadLibraryExW(LPCWSTR n, HANDLE f, DWORD fl) { return after_load(LoadLibraryExW(n, f, fl)); }

typedef struct { const char *dll; const char *name; void *hook; void *real; } HOOK;

#define HK(d, n) { d, #n, (void *)H_##n, NULL }
static HOOK g_hooks[] = {
    HK("advapi32.dll", RegOpenKeyExA), HK("advapi32.dll", RegOpenKeyExW),
    HK("advapi32.dll", RegOpenKeyA), HK("advapi32.dll", RegOpenKeyW),
    HK("advapi32.dll", RegCreateKeyExA), HK("advapi32.dll", RegCreateKeyExW),
    HK("advapi32.dll", RegCreateKeyA), HK("advapi32.dll", RegCreateKeyW),
    HK("advapi32.dll", RegSetValueExA), HK("advapi32.dll", RegSetValueExW),
    HK("advapi32.dll", RegSetValueA), HK("advapi32.dll", RegSetValueW),
    HK("advapi32.dll", RegDeleteKeyA), HK("advapi32.dll", RegDeleteKeyW),
    HK("advapi32.dll", RegDeleteValueA), HK("advapi32.dll", RegDeleteValueW),
    HK("advapi32.dll", RegCloseKey),
    HK("advapi32.dll", RegQueryValueExA), HK("advapi32.dll", RegQueryValueExW),
    HK("advapi32.dll", RegEnumKeyExA), HK("advapi32.dll", RegEnumKeyA),
    HK("advapi32.dll", RegQueryInfoKeyA),
    HK("ole32.dll", CoCreateInstance),
    HK("kernel32.dll", CreateFileA), HK("kernel32.dll", CreateFileW),
    HK("kernel32.dll", CreateDirectoryA), HK("kernel32.dll", CreateDirectoryW),
    HK("kernel32.dll", RemoveDirectoryA), HK("kernel32.dll", RemoveDirectoryW),
    HK("kernel32.dll", DeleteFileA), HK("kernel32.dll", DeleteFileW),
    HK("kernel32.dll", SetFileAttributesA), HK("kernel32.dll", SetFileAttributesW),
    HK("kernel32.dll", CopyFileA), HK("kernel32.dll", CopyFileW),
    HK("kernel32.dll", MoveFileA), HK("kernel32.dll", MoveFileW),
    HK("kernel32.dll", MoveFileExA), HK("kernel32.dll", MoveFileExW),
    HK("kernel32.dll", WritePrivateProfileStringA), HK("kernel32.dll", WritePrivateProfileStringW),
    HK("kernel32.dll", WritePrivateProfileSectionA),
    HK("kernel32.dll", WriteProfileStringA), HK("kernel32.dll", WriteProfileStringW),
    HK("kernel32.dll", LoadLibraryA), HK("kernel32.dll", LoadLibraryW),
    HK("kernel32.dll", LoadLibraryExA), HK("kernel32.dll", LoadLibraryExW),
};
#define NHOOKS (sizeof(g_hooks) / sizeof(g_hooks[0]))

static void resolve_hooks(void)
{
    size_t i;
    for (i = 0; i < NHOOKS; i++) {
        HMODULE d = GetModuleHandleA(g_hooks[i].dll);
        if (!d) d = LoadLibraryA(g_hooks[i].dll); /* both are already loaded by the game */
        g_hooks[i].real = d ? (void *)GetProcAddress(d, g_hooks[i].name) : NULL;
    }
}

static void patch_module(HMODULE m)
{
    BYTE *base = (BYTE *)m;
    IMAGE_DOS_HEADER *dos = (IMAGE_DOS_HEADER *)base;
    IMAGE_NT_HEADERS *nt;
    IMAGE_DATA_DIRECTORY *dd;
    IMAGE_IMPORT_DESCRIPTOR *imp;

    if (!m || dos->e_magic != IMAGE_DOS_SIGNATURE) return;
    nt = (IMAGE_NT_HEADERS *)(base + dos->e_lfanew);
    if (nt->Signature != IMAGE_NT_SIGNATURE) return;
    dd = &nt->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT];
    if (!dd->VirtualAddress || !dd->Size) return;

    for (imp = (IMAGE_IMPORT_DESCRIPTOR *)(base + dd->VirtualAddress); imp->Name; imp++) {
        IMAGE_THUNK_DATA *iat = (IMAGE_THUNK_DATA *)(base + imp->FirstThunk);
        IMAGE_THUNK_DATA *oft = imp->OriginalFirstThunk ? (IMAGE_THUNK_DATA *)(base + imp->OriginalFirstThunk) : NULL;
        for (; iat->u1.Function; iat++, oft = oft ? oft + 1 : NULL) {
            size_t i;
            void *cur = (void *)iat->u1.Function;
            const char *nm = NULL;
            if (oft && !IMAGE_SNAP_BY_ORDINAL(oft->u1.Ordinal))
                nm = (const char *)((IMAGE_IMPORT_BY_NAME *)(base + oft->u1.AddressOfData))->Name;
            for (i = 0; i < NHOOKS; i++) {
                if ((g_hooks[i].real && cur == g_hooks[i].real) || (nm && lstrcmpA(nm, g_hooks[i].name) == 0)) {
                    DWORD old;
                    if (cur == g_hooks[i].hook) break;
                    if (VirtualProtect(&iat->u1.Function, sizeof(void *), PAGE_READWRITE, &old)) {
                        iat->u1.Function = (ULONG_PTR)g_hooks[i].hook;
                        VirtualProtect(&iat->u1.Function, sizeof(void *), old, &old);
                    }
                    break;
                }
            }
        }
    }
}

static void patch_all(void)
{
    MODULEENTRY32W me;
    HANDLE s = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE, GetCurrentProcessId());
    patch_module(GetModuleHandleW(NULL));
    if (s == INVALID_HANDLE_VALUE) return;
    me.dwSize = sizeof(me);
    if (Module32FirstW(s, &me)) {
        do {
            if (me.hModule != g_self && me.hModule != GetModuleHandleW(NULL) && inside_w(me.szExePath))
                patch_module(me.hModule);
        } while (Module32NextW(s, &me));
    }
    CloseHandle(s);
}

BOOL WINAPI DllMain(HINSTANCE h, DWORD reason, LPVOID r)
{
    if (reason == DLL_PROCESS_ATTACH) {
        WCHAR *slash;
        WCHAR tmp[MAX_PATH];
        g_self = h;
        DisableThreadLibraryCalls(h);
        InitializeCriticalSection(&g_cs);
        g_heap = GetProcessHeap();
        GetModuleFileNameW(NULL, tmp, MAX_PATH);
        if (!GetLongPathNameW(tmp, g_dir, MAX_PATH)) lstrcpyW(g_dir, tmp);
        slash = wcsrchr(g_dir, L'\\');
        if (slash) *slash = 0;
        if (!GetShortPathNameW(g_dir, g_dirShort, MAX_PATH)) g_dirShort[0] = 0;
        wsprintfW(g_portable, L"%s\\portable", g_dir);
        resolve_hooks();
        patch_all();
    }
    return TRUE;
}
