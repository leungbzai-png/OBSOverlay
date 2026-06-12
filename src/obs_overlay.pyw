"""OBSOverlay - lightweight OBS recording status overlay for Windows.

Shows a small, capture-excluded floating banner in the top-right corner that
reacts to OBS recording state changes (start / stop / pause / resume) via the
OBS WebSocket API. Lives in the system tray.

v0.2.0 "Final Portable Edition": runs as a portable ``OBSOverlay.exe``. All
data (``config.json``, ``logs/``, ``cache/``, ``data/``) lives next to the
executable. On first launch (no ``config.json`` or password still ``CHANGE_ME``)
a small tkinter settings window opens so ordinary users never edit JSON or run
.bat files by hand. The tray menu can re-open settings, test / reconnect, and
manage Windows auto-start for both OBSOverlay and OBS via Startup shortcuts.

No real credentials are ever stored in this source file, and the OBS WebSocket
password is never written to logs or shown in error dialogs.
"""

import os
import sys
import json
import shutil
import threading
import subprocess
from pathlib import Path

import ctypes
from ctypes import wintypes

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Third-party deps (see requirements.txt)
import pystray
from PIL import Image, ImageDraw
import obsws_python as obs


# --------------------------------------------------------------------------
# Portable paths: everything lives next to the exe (or project root in source)
# --------------------------------------------------------------------------
IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    # PyInstaller exe -> data sits beside OBSOverlay.exe
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    # Source run -> project root = parent of this file's "src" folder
    BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = BASE_DIR / "config.json"
EXAMPLE_PATH = BASE_DIR / "config.example.json"
LOG_DIR = BASE_DIR / "logs"
CACHE_DIR = BASE_DIR / "cache"
DATA_DIR = BASE_DIR / "data"

PLACEHOLDER_PASSWORD = "CHANGE_ME"

# Windows CreateProcess flag so helper shells never flash a console window.
CREATE_NO_WINDOW = 0x08000000

STARTUP_DIR = Path(os.environ.get("APPDATA", "")) / \
    "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
OVERLAY_LNK = STARTUP_DIR / "OBSOverlay.lnk"
OBS_LNK = STARTUP_DIR / "OBS Studio.lnk"

OBS_CANDIDATES = [
    r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
    r"C:\Program Files (x86)\obs-studio\bin\64bit\obs64.exe",
]


def ensure_dirs():
    for d in (LOG_DIR, CACHE_DIR, DATA_DIR):
        try:
            d.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass


# --------------------------------------------------------------------------
# Minimal i18n (simple dict, no framework)
# --------------------------------------------------------------------------
T = {
    "zh": {
        "settings_title": "OBSOverlay 设置",
        "language": "语言 / Language",
        "host": "OBS WebSocket 主机 (Host)",
        "port": "端口 (Port)",
        "password": "WebSocket 密码 (Password)",
        "autostart_overlay": "开机自动启动 OBSOverlay",
        "autostart_obs": "开机自动启动 OBS",
        "obs_path": "OBS 程序路径 (obs64.exe)",
        "detect": "自动检测",
        "browse": "浏览…",
        "test": "测试连接",
        "save": "保存并启动",
        "cancel": "取消",
        "test_ok": "连接成功！已连上 OBS WebSocket。",
        "test_fail": "连接失败。请检查 OBS 是否已开启、WebSocket 是否启用，"
                     "以及主机 / 端口 / 密码是否正确。",
        "testing": "正在测试连接…",
        "saved": "配置已保存。",
        "bad_port": "端口必须是数字 (例如 4455)。",
        "warn_password": "密码为空或仍是 CHANGE_ME，可能无法连接 OBS。仍要保存吗？",
        "warn_obs_path": "已勾选 OBS 开机自启，但没有有效的 obs64.exe 路径，"
                         "将跳过 OBS 自启。",
        "obs_not_found": "未自动检测到 OBS，请用“浏览…”选择 obs64.exe。",
        "tray_settings": "打开设置",
        "tray_test": "测试连接",
        "tray_reconnect": "重新连接 OBS",
        "tray_folder": "打开程序目录",
        "tray_config": "打开配置文件",
        "tray_exit": "退出",
        "tray_tooltip": "OBSOverlay 录制提示",
        "rec_start": "●  REC  开始录制",
        "rec_stop": "■  停止录制",
        "rec_pause": "∥  已暂停",
        "rec_resume": "●  继续录制",
        "test_flash": "●  测试提示",
        "no_config_title": "OBSOverlay",
    },
    "en": {
        "settings_title": "OBSOverlay Settings",
        "language": "Language / 语言",
        "host": "OBS WebSocket Host",
        "port": "Port",
        "password": "WebSocket Password",
        "autostart_overlay": "Start OBSOverlay with Windows",
        "autostart_obs": "Start OBS with Windows",
        "obs_path": "OBS executable (obs64.exe)",
        "detect": "Auto-detect",
        "browse": "Browse…",
        "test": "Test connection",
        "save": "Save and start",
        "cancel": "Cancel",
        "test_ok": "Connected! OBS WebSocket is reachable.",
        "test_fail": "Connection failed. Check that OBS is running, that its "
                     "WebSocket server is enabled, and that host / port / "
                     "password are correct.",
        "testing": "Testing connection…",
        "saved": "Configuration saved.",
        "bad_port": "Port must be a number (e.g. 4455).",
        "warn_password": "Password is empty or still CHANGE_ME; OBS may not "
                         "connect. Save anyway?",
        "warn_obs_path": "OBS auto-start is checked but there is no valid "
                         "obs64.exe path; OBS auto-start will be skipped.",
        "obs_not_found": "OBS was not auto-detected. Use \"Browse…\" to pick "
                         "obs64.exe.",
        "tray_settings": "Open settings",
        "tray_test": "Test connection",
        "tray_reconnect": "Reconnect OBS",
        "tray_folder": "Open folder",
        "tray_config": "Open config",
        "tray_exit": "Exit",
        "tray_tooltip": "OBSOverlay recording status",
        "rec_start": "●  REC  recording",
        "rec_stop": "■  recording stopped",
        "rec_pause": "∥  paused",
        "rec_resume": "●  resumed",
        "test_flash": "●  test",
        "no_config_title": "OBSOverlay",
    },
}

# Current UI language (zh / en). Updated when settings are saved.
current_lang = "zh"


def tr(key):
    return T.get(current_lang, T["zh"]).get(key, key)


def detect_system_language():
    """Best-effort system UI language -> 'zh' or 'en' (defaults to zh)."""
    try:
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        if (lang_id & 0x3FF) == 0x04:  # LANG_CHINESE
            return "zh"
        return "en"
    except Exception:
        return "zh"


# --------------------------------------------------------------------------
# Config load / save (tolerant of missing fields so old v0.1.0 configs load)
# --------------------------------------------------------------------------
def load_config():
    """Return config dict, or None if config.json is missing / unreadable."""
    if not CONFIG_PATH.exists():
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    ws = data.get("obs_websocket") or {}
    return {
        "language": data.get("language") or detect_system_language(),
        "host": str(ws.get("host", "127.0.0.1")),
        "port": int(ws.get("port", 4455)) if str(ws.get("port", 4455)).isdigit() else 4455,
        "password": str(ws.get("password", "")),
        "obs_path": str(data.get("obs_path", "")),
    }


def save_config(cfg):
    data = {
        "language": cfg["language"],
        "obs_websocket": {
            "host": cfg["host"],
            "port": int(cfg["port"]),
            "password": cfg["password"],
        },
        "obs_path": cfg.get("obs_path", ""),
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def needs_setup(cfg):
    """First-run condition: no config, or password unset / placeholder."""
    if cfg is None:
        return True
    pw = cfg.get("password", "")
    return (not pw) or pw == PLACEHOLDER_PASSWORD


def detect_obs_path():
    for p in OBS_CANDIDATES:
        if os.path.isfile(p):
            return p
    return ""


# --------------------------------------------------------------------------
# Windows Startup-folder shortcut management (PowerShell, no console flash)
# --------------------------------------------------------------------------
def _run_powershell(script):
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            creationflags=CREATE_NO_WINDOW,
            check=False,
            timeout=20,
        )
        return True
    except Exception:
        return False


def _ps_quote(value):
    # Single-quote for PowerShell; escape embedded single quotes.
    return "'" + str(value).replace("'", "''") + "'"


def _create_shortcut(lnk_path, target, arguments, workdir, window_style=None):
    try:
        STARTUP_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    parts = [
        "$s=(New-Object -ComObject WScript.Shell).CreateShortcut(%s);"
        % _ps_quote(lnk_path),
        "$s.TargetPath=%s;" % _ps_quote(target),
        "$s.Arguments=%s;" % _ps_quote(arguments),
        "$s.WorkingDirectory=%s;" % _ps_quote(workdir),
    ]
    if window_style is not None:
        parts.append("$s.WindowStyle=%d;" % window_style)
    parts.append("$s.Save()")
    return _run_powershell("".join(parts))


def _remove_shortcut(lnk_path):
    try:
        if Path(lnk_path).exists():
            Path(lnk_path).unlink()
        return True
    except Exception:
        return False


def overlay_autostart_target():
    """(target, arguments, workdir) for an OBSOverlay startup shortcut."""
    if IS_FROZEN:
        return str(sys.executable), "", str(BASE_DIR)
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    script = Path(__file__).resolve()
    return str(pythonw), '"%s"' % script, str(BASE_DIR)


def set_overlay_autostart(enabled):
    if enabled:
        target, args, workdir = overlay_autostart_target()
        return _create_shortcut(OVERLAY_LNK, target, args, workdir, window_style=7)
    return _remove_shortcut(OVERLAY_LNK)


def set_obs_autostart(enabled, obs_path):
    if enabled:
        if not obs_path or not os.path.isfile(obs_path):
            return False
        workdir = str(Path(obs_path).parent)
        return _create_shortcut(
            OBS_LNK, obs_path,
            "--minimize-to-tray --disable-shutdown-check", workdir)
    return _remove_shortcut(OBS_LNK)


# --------------------------------------------------------------------------
# OBS WebSocket connection (test + live event loop with reconnect)
# --------------------------------------------------------------------------
def test_connection(host, port, password):
    """Return (ok, error_type_name). Never returns / logs the password."""
    client = None
    try:
        client = obs.ReqClient(host=host, port=int(port),
                               password=password, timeout=3)
        client.get_version()
        return True, ""
    except Exception as exc:  # noqa: BLE001 - surfaced as a friendly dialog
        return False, type(exc).__name__
    finally:
        try:
            if client is not None:
                client.disconnect()
        except Exception:
            pass


class ConnManager:
    """Owns the live OBS event connection; supports credential hot-reload."""

    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 4455
        self.password = ""
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.reconnect = threading.Event()
        self._thread = None

    def update(self, host, port, password):
        with self.lock:
            self.host, self.port, self.password = host, int(port), password
        self.reconnect.set()

    def ensure_started(self):
        if self._thread is None or not self._thread.is_alive():
            self.stop.clear()
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def request_reconnect(self):
        self.reconnect.set()

    def shutdown(self):
        self.stop.set()
        self.reconnect.set()

    def _loop(self):
        while not self.stop.is_set():
            self.reconnect.clear()
            with self.lock:
                host, port, password = self.host, self.port, self.password
            client = None
            try:
                client = obs.EventClient(host=host, port=port, password=password)
                client.callback.register(on_record_state_changed)
                while not self.stop.is_set() and not self.reconnect.is_set():
                    self.reconnect.wait(2)
                    if self.reconnect.is_set() or self.stop.is_set():
                        break
                    try:
                        client.base_client.ws.ping()
                    except Exception:
                        break
            except Exception:
                # Swallow connection errors (never log credentials); retry.
                pass
            finally:
                try:
                    if client is not None:
                        client.disconnect()
                except Exception:
                    pass
            if self.stop.is_set():
                break
            # Wait before retrying, but wake immediately on reconnect request.
            self.reconnect.wait(5)


# --------------------------------------------------------------------------
# Win32 capture-excluded overlay banner
# --------------------------------------------------------------------------
user32 = ctypes.windll.user32
SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
SetWindowDisplayAffinity.argtypes = [wintypes.HWND, wintypes.DWORD]
SetWindowDisplayAffinity.restype = wintypes.BOOL
GetAncestor = user32.GetAncestor
GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
GetAncestor.restype = wintypes.HWND
WDA_EXCLUDEFROMCAPTURE = 0x11
GA_ROOT = 2


class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.92)
        w, h = 240, 56
        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"{w}x{h}+{sw - w - 24}+24")
        self.label = tk.Label(self.root, text="", font=("Segoe UI", 14, "bold"),
                              fg="white", bg="#1e1e1e")
        self.label.pack(fill="both", expand=True)
        self.root.update_idletasks()
        hwnd = GetAncestor(self.root.winfo_id(), GA_ROOT)
        SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)

    def flash(self, text, color, duration=2500):
        def _show():
            self.label.config(text=text, bg=color)
            self.root.configure(bg=color)
            self.root.deiconify()
            self.root.after(duration, self.root.withdraw)
        self.root.after(0, _show)

    def run(self):
        self.root.mainloop()

    def quit(self):
        self.root.after(0, self.root.destroy)


def on_record_state_changed(data):
    s = data.output_state
    if s == "OBS_WEBSOCKET_OUTPUT_STARTED":
        overlay.flash(tr("rec_start"), "#d13438")
    elif s == "OBS_WEBSOCKET_OUTPUT_STOPPED":
        overlay.flash(tr("rec_stop"), "#107c10")
    elif s == "OBS_WEBSOCKET_OUTPUT_PAUSED":
        overlay.flash(tr("rec_pause"), "#b7950b")
    elif s == "OBS_WEBSOCKET_OUTPUT_RESUMED":
        overlay.flash(tr("rec_resume"), "#d13438")


# --------------------------------------------------------------------------
# Settings window (single persistent root: always a Toplevel of overlay.root)
# --------------------------------------------------------------------------
settings_win = None


def open_settings(first_run=False):
    """Open (or focus) the settings window. Must run on the GUI thread."""
    global settings_win
    if settings_win is not None and tk.Toplevel.winfo_exists(settings_win):
        settings_win.lift()
        settings_win.focus_force()
        return
    SettingsWindow(first_run=first_run)


class SettingsWindow:
    def __init__(self, first_run=False):
        global settings_win
        self.first_run = first_run
        cfg = load_config() or {}
        self.lang_var = tk.StringVar(
            value=cfg.get("language") or current_lang)
        self.host_var = tk.StringVar(value=cfg.get("host", "127.0.0.1"))
        self.port_var = tk.StringVar(value=str(cfg.get("port", 4455)))
        self.pw_var = tk.StringVar(value=cfg.get("password", ""))
        obs_path = cfg.get("obs_path") or detect_obs_path()
        self.obs_path_var = tk.StringVar(value=obs_path)
        self.auto_overlay_var = tk.BooleanVar(value=OVERLAY_LNK.exists())
        self.auto_obs_var = tk.BooleanVar(value=OBS_LNK.exists())

        win = tk.Toplevel(overlay.root)
        settings_win = win
        win.resizable(False, False)
        win.attributes("-topmost", True)
        win.protocol("WM_DELETE_WINDOW", self._on_close)
        win.grab_set()
        self.win = win

        self._labels = {}
        self._build()
        self._apply_language()
        win.update_idletasks()
        # Center on screen.
        w, h = win.winfo_width(), win.winfo_height()
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        win.geometry(f"+{(sw - w) // 2}+{(sh - h) // 3}")
        win.focus_force()

    # -- layout -----------------------------------------------------------
    def _build(self):
        f = ttk.Frame(self.win, padding=16)
        f.grid(sticky="nsew")
        row = 0

        def label(key):
            lbl = ttk.Label(f)
            lbl.grid(row=label.row, column=0, sticky="w", pady=(6, 0))
            self._labels[key] = lbl
            label.row += 1
            return label.row - 1
        label.row = 0

        # Language
        r = label("language")
        lang_combo = ttk.Combobox(
            f, state="readonly", width=28,
            values=["中文 (Chinese)", "English"])
        lang_combo.grid(row=r, column=1, sticky="we", pady=(6, 0))
        lang_combo.current(0 if self.lang_var.get() == "zh" else 1)
        lang_combo.bind("<<ComboboxSelected>>", self._on_lang_change)
        self.lang_combo = lang_combo

        # Host
        r = label("host")
        ttk.Entry(f, textvariable=self.host_var, width=30).grid(
            row=r, column=1, sticky="we", pady=(6, 0))

        # Port
        r = label("port")
        ttk.Entry(f, textvariable=self.port_var, width=30).grid(
            row=r, column=1, sticky="we", pady=(6, 0))

        # Password (hidden)
        r = label("password")
        ttk.Entry(f, textvariable=self.pw_var, show="*", width=30).grid(
            row=r, column=1, sticky="we", pady=(6, 0))

        # OBS path + buttons
        r = label("obs_path")
        path_frame = ttk.Frame(f)
        path_frame.grid(row=r, column=1, sticky="we", pady=(6, 0))
        ttk.Entry(path_frame, textvariable=self.obs_path_var, width=22).pack(
            side="left", fill="x", expand=True)
        self.detect_btn = ttk.Button(path_frame, command=self._on_detect, width=4)
        self.detect_btn.pack(side="left", padx=(4, 0))
        self.browse_btn = ttk.Button(path_frame, command=self._on_browse, width=4)
        self.browse_btn.pack(side="left", padx=(4, 0))

        # Checkboxes
        self.cb_overlay = ttk.Checkbutton(f, variable=self.auto_overlay_var)
        self.cb_overlay.grid(row=label.row, column=0, columnspan=2,
                             sticky="w", pady=(10, 0))
        self._labels["autostart_overlay"] = self.cb_overlay
        label.row += 1
        self.cb_obs = ttk.Checkbutton(f, variable=self.auto_obs_var)
        self.cb_obs.grid(row=label.row, column=0, columnspan=2, sticky="w")
        self._labels["autostart_obs"] = self.cb_obs
        label.row += 1

        # Buttons row
        btns = ttk.Frame(f)
        btns.grid(row=label.row, column=0, columnspan=2, sticky="we", pady=(16, 0))
        self.test_btn = ttk.Button(btns, command=self._on_test)
        self.test_btn.pack(side="left")
        self.cancel_btn = ttk.Button(btns, command=self._on_close)
        self.cancel_btn.pack(side="right")
        self.save_btn = ttk.Button(btns, command=self._on_save)
        self.save_btn.pack(side="right", padx=(0, 8))

        f.columnconfigure(1, weight=1)

    def _apply_language(self):
        # Set UI language from the dropdown so labels follow the choice live.
        lang = "zh" if self.lang_combo.current() == 0 else "en"
        self.lang_var.set(lang)
        tbl = T[lang]
        self.win.title(tbl["settings_title"])
        for key, widget in self._labels.items():
            widget.config(text=tbl[key])
        self.detect_btn.config(text=tbl["detect"])
        self.browse_btn.config(text=tbl["browse"])
        self.test_btn.config(text=tbl["test"])
        self.save_btn.config(text=tbl["save"])
        self.cancel_btn.config(text=tbl["cancel"])

    # -- handlers ---------------------------------------------------------
    def _on_lang_change(self, _evt=None):
        self._apply_language()

    def _on_detect(self):
        path = detect_obs_path()
        if path:
            self.obs_path_var.set(path)
        else:
            messagebox.showinfo(T[self.lang_var.get()]["settings_title"],
                                T[self.lang_var.get()]["obs_not_found"],
                                parent=self.win)

    def _on_browse(self):
        path = filedialog.askopenfilename(
            parent=self.win, title="obs64.exe",
            filetypes=[("obs64.exe", "obs64.exe"), ("exe", "*.exe")])
        if path:
            self.obs_path_var.set(path)

    def _on_test(self):
        lang = self.lang_var.get()
        port = self.port_var.get().strip()
        if not port.isdigit():
            messagebox.showerror(T[lang]["settings_title"], T[lang]["bad_port"],
                                 parent=self.win)
            return
        ok, _err = test_connection(self.host_var.get().strip(), port,
                                   self.pw_var.get())
        if ok:
            messagebox.showinfo(T[lang]["settings_title"], T[lang]["test_ok"],
                                parent=self.win)
        else:
            messagebox.showwarning(T[lang]["settings_title"], T[lang]["test_fail"],
                                   parent=self.win)

    def _on_save(self):
        lang = self.lang_var.get()
        port = self.port_var.get().strip()
        if not port.isdigit():
            messagebox.showerror(T[lang]["settings_title"], T[lang]["bad_port"],
                                 parent=self.win)
            return
        pw = self.pw_var.get()
        if not pw or pw == PLACEHOLDER_PASSWORD:
            if not messagebox.askyesno(T[lang]["settings_title"],
                                       T[lang]["warn_password"], parent=self.win):
                return

        obs_path = self.obs_path_var.get().strip()
        cfg = {
            "language": lang,
            "host": self.host_var.get().strip() or "127.0.0.1",
            "port": int(port),
            "password": pw,
            "obs_path": obs_path,
        }
        try:
            save_config(cfg)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror(T[lang]["settings_title"],
                                 "%s (%s)" % (type(exc).__name__, "save"),
                                 parent=self.win)
            return

        # Apply auto-start choices (only this project's shortcuts).
        set_overlay_autostart(self.auto_overlay_var.get())
        if self.auto_obs_var.get() and not (obs_path and os.path.isfile(obs_path)):
            messagebox.showwarning(T[lang]["settings_title"],
                                   T[lang]["warn_obs_path"], parent=self.win)
            set_obs_autostart(False, obs_path)
        else:
            set_obs_autostart(self.auto_obs_var.get(), obs_path)

        # Apply language + (re)connect live.
        global current_lang
        current_lang = lang
        cm.update(cfg["host"], cfg["port"], cfg["password"])
        cm.ensure_started()

        self._destroy()

    def _on_close(self):
        # First run with no usable config -> nothing to do, exit the app.
        if self.first_run and needs_setup(load_config()):
            self._destroy()
            shutdown_app()
            return
        self._destroy()

    def _destroy(self):
        global settings_win
        try:
            self.win.grab_release()
        except Exception:
            pass
        try:
            self.win.destroy()
        except Exception:
            pass
        settings_win = None


# --------------------------------------------------------------------------
# System tray
# --------------------------------------------------------------------------
def make_icon_image():
    img = Image.new("RGB", (64, 64), "#1e1e1e")
    d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 48, 48), fill="#d13438")
    return img


def _gui(func):
    """Schedule a callable on the tkinter GUI thread."""
    overlay.root.after(0, func)


def tray_open_settings(icon, item):
    _gui(lambda: open_settings(first_run=False))


def tray_test(icon, item):
    cfg = load_config()
    if not cfg:
        _gui(lambda: open_settings(first_run=True))
        return

    def _do():
        ok, _err = test_connection(cfg["host"], cfg["port"], cfg["password"])
        lang = current_lang
        if ok:
            overlay.flash(tr("test_flash"), "#0078d4", duration=1500)
            _gui(lambda: messagebox.showinfo(T[lang]["settings_title"],
                                             T[lang]["test_ok"]))
        else:
            _gui(lambda: messagebox.showwarning(T[lang]["settings_title"],
                                                T[lang]["test_fail"]))
    threading.Thread(target=_do, daemon=True).start()


def tray_reconnect(icon, item):
    cfg = load_config()
    if cfg:
        cm.update(cfg["host"], cfg["port"], cfg["password"])
        cm.ensure_started()


def tray_open_folder(icon, item):
    try:
        os.startfile(str(BASE_DIR))
    except Exception:
        pass


def tray_open_config(icon, item):
    if CONFIG_PATH.exists():
        try:
            os.startfile(str(CONFIG_PATH))
        except Exception:
            pass
    else:
        _gui(lambda: open_settings(first_run=False))


def tray_exit(icon, item):
    icon.stop()
    shutdown_app()


def tray_loop():
    icon = pystray.Icon(
        "obs_overlay",
        make_icon_image(),
        tr("tray_tooltip"),
        menu=pystray.Menu(
            pystray.MenuItem(lambda i: tr("tray_settings"), tray_open_settings,
                             default=True),
            pystray.MenuItem(lambda i: tr("tray_test"), tray_test),
            pystray.MenuItem(lambda i: tr("tray_reconnect"), tray_reconnect),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(lambda i: tr("tray_folder"), tray_open_folder),
            pystray.MenuItem(lambda i: tr("tray_config"), tray_open_config),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(lambda i: tr("tray_exit"), tray_exit),
        ),
    )
    global tray_icon
    tray_icon = icon
    icon.run()


tray_icon = None


def shutdown_app():
    cm.shutdown()
    try:
        if tray_icon is not None:
            tray_icon.stop()
    except Exception:
        pass
    overlay.quit()


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
overlay = None
cm = None


def main():
    global overlay, cm, current_lang
    ensure_dirs()
    cfg = load_config()
    current_lang = (cfg or {}).get("language") or detect_system_language()

    overlay = Overlay()
    cm = ConnManager()

    threading.Thread(target=tray_loop, daemon=True).start()

    if needs_setup(cfg):
        overlay.root.after(0, lambda: open_settings(first_run=True))
    else:
        cm.update(cfg["host"], cfg["port"], cfg["password"])
        cm.ensure_started()

    overlay.run()


if __name__ == "__main__":
    main()
