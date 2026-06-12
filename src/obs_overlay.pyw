"""OBSOverlay - lightweight OBS recording status overlay for Windows.

Shows a small, capture-excluded floating banner in the top-right corner that
reacts to OBS recording state changes (start / stop / pause / resume) via the
OBS WebSocket API. Lives in the system tray.

Configuration is read from ``config.json`` in the project root (the parent of
this ``src`` folder). Copy ``config.example.json`` to ``config.json`` and fill
in your own OBS WebSocket host / port / password. No credentials are stored in
this source file.
"""

import json
import sys
import threading
from pathlib import Path

import ctypes
from ctypes import wintypes

import tkinter as tk
from tkinter import messagebox

# Third-party deps (see requirements.txt)
import pystray
from PIL import Image, ImageDraw
import obsws_python as obs


# --------------------------------------------------------------------------
# Configuration loading
# --------------------------------------------------------------------------
# config.json lives in the project root = parent of this file's "src" folder.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.json"
EXAMPLE_PATH = PROJECT_ROOT / "config.example.json"
PLACEHOLDER_PASSWORD = "CHANGE_ME"


def _fatal(title, message):
    """Show a GUI error (this is a .pyw with no console) and exit.

    Never echo secrets here -- only configuration guidance.
    """
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:
        # Last resort if even Tk fails; harmless if no console is attached.
        pass
    sys.exit(1)


def load_config():
    """Load OBS WebSocket settings from config.json with friendly GUI errors."""
    if not CONFIG_PATH.exists():
        _fatal(
            "OBSOverlay - 缺少配置文件 / Missing config",
            "未找到 config.json。\n\n"
            "请复制 config.example.json 为 config.json，\n"
            "然后填写你自己的 OBS WebSocket 密码。\n\n"
            "Copy config.example.json to config.json and fill in your own "
            "OBS WebSocket password.\n\n"
            f"位置 / Location:\n{CONFIG_PATH}",
        )

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        ws = data["obs_websocket"]
        host = ws.get("host", "127.0.0.1")
        port = int(ws.get("port", 4455))
        password = ws.get("password", "")
    except Exception as exc:  # noqa: BLE001 - report parse/format issues to user
        # Note: exception text here is about JSON structure, not secrets.
        _fatal(
            "OBSOverlay - 配置文件错误 / Bad config",
            "config.json 格式有误，请参考 config.example.json 修正。\n\n"
            "config.json is malformed. Please compare it with "
            "config.example.json.\n\n"
            f"({type(exc).__name__})",
        )

    if not password or password == PLACEHOLDER_PASSWORD:
        _fatal(
            "OBSOverlay - 请填写密码 / Set your password",
            "config.json 中的 password 还是占位符 CHANGE_ME。\n\n"
            "请把它改成你 OBS 里设置的 WebSocket 密码：\n"
            "OBS -> 工具 -> WebSocket 服务器设置 -> 显示连接信息。\n\n"
            "The password in config.json is still the placeholder CHANGE_ME. "
            "Set it to your real OBS WebSocket password.",
        )

    return host, port, password


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
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.92)
        w, h = 240, 56
        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"{w}x{h}+{sw - w - 24}+24")
        self.label = tk.Label(self.root, text="", font=("Segoe UI", 14, "bold"),
                              fg="white", bg="#1e1e1e")
        self.label.pack(fill="both", expand=True)
        self.root.update_idletasks()
        hwnd = GetAncestor(self.root.winfo_id(), GA_ROOT)
        SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
        self.root.withdraw()

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


reconnect_stop = threading.Event()


def on_record_state_changed(data):
    s = data.output_state
    if s == "OBS_WEBSOCKET_OUTPUT_STARTED":
        overlay.flash("●  REC  开始录制", "#d13438")
    elif s == "OBS_WEBSOCKET_OUTPUT_STOPPED":
        overlay.flash("■  停止录制", "#107c10")
    elif s == "OBS_WEBSOCKET_OUTPUT_PAUSED":
        overlay.flash("∥  已暂停", "#b7950b")
    elif s == "OBS_WEBSOCKET_OUTPUT_RESUMED":
        overlay.flash("●  继续录制", "#d13438")


def ws_loop(host, port, password):
    while not reconnect_stop.is_set():
        try:
            client = obs.EventClient(host=host, port=port, password=password)
            client.callback.register(on_record_state_changed)
            while not reconnect_stop.is_set():
                reconnect_stop.wait(2)
                try:
                    client.base_client.ws.ping()
                except Exception:
                    break
        except Exception:
            # Swallow connection errors (and never log credentials); retry below.
            pass
        reconnect_stop.wait(5)


def make_icon_image():
    img = Image.new("RGB", (64, 64), "#1e1e1e")
    d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 48, 48), fill="#d13438")
    return img


def on_quit(icon, item):
    reconnect_stop.set()
    icon.stop()
    overlay.quit()


def on_test(icon, item):
    overlay.flash("●  测试提示", "#0078d4", duration=1500)


def tray_loop():
    icon = pystray.Icon(
        "obs_overlay",
        make_icon_image(),
        "OBS 录制提示",
        menu=pystray.Menu(
            pystray.MenuItem("测试提示", on_test),
            pystray.MenuItem("退出", on_quit),
        ),
    )
    icon.run()


if __name__ == "__main__":
    OBS_HOST, OBS_PORT, OBS_PASSWORD = load_config()
    overlay = Overlay()
    threading.Thread(target=ws_loop,
                     args=(OBS_HOST, OBS_PORT, OBS_PASSWORD),
                     daemon=True).start()
    threading.Thread(target=tray_loop, daemon=True).start()
    overlay.run()
