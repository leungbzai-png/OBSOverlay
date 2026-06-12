# OBSOverlay 开发指南 (DEV_GUIDE)

面向开发 / 维护者。当前版本 **v0.2.0 — Final Portable Edition**（维护态项目，见 ROADMAP）。

## 项目结构

```
OBSOverlay/
├─ src/obs_overlay.pyw       # 主程序：portable 路径 + 设置窗口 + 托盘 + OBS WebSocket
├─ scripts/
│  ├─ build_portable.bat     # 打包 exe + portable / source zip
│  ├─ install_deps.bat
│  ├─ install_startup.bat / uninstall_startup.bat
│  ├─ install_obs_startup.bat / uninstall_obs_startup.bat
│  └─ reset_clean.bat
├─ docs/*.md
├─ logs/ cache/ data/        # 运行时数据（跟随 exe；内容 .gitignore，仅留 .gitkeep）
├─ release/README.md
├─ config.example.json       # 配置模板（占位符 CHANGE_ME）
├─ requirements.txt / .gitignore / LICENSE / README.md / PROJECT_CONTEXT.md
```

## Python 依赖

运行时（`requirements.txt`）：`obsws-python`（OBS WebSocket v5）、`pystray`（托盘）、`pillow`（图标）。
打包时另需 `pyinstaller`。标准库：`tkinter`、`ctypes`、`threading`、`json`、`pathlib`、`subprocess`。

```
python -m pip install -r requirements.txt
python -m pip install pyinstaller
```

## 本地运行（源码）

```
pythonw src\obs_overlay.pyw      # 无控制台（正式运行方式）
python  src\obs_overlay.pyw      # 有控制台，便于调试看 traceback
```

> `.pyw` 由 `pythonw.exe` 运行时**没有控制台**，所有面向用户的报错都用 `tkinter.messagebox`
> 弹窗，不要用 `print` / `stderr`。

## Portable 路径规则（核心）

```python
IS_FROZEN = getattr(sys, "frozen", False)
if IS_FROZEN:
    BASE_DIR = Path(sys.executable).resolve().parent      # exe 所在目录
else:
    BASE_DIR = Path(__file__).resolve().parent.parent     # 项目根
```

所有数据从 `BASE_DIR` 推导：`config.json` / `config.example.json` / `logs/` / `cache/` / `data/`。
**不写 AppData、不写 C:\Users**。图标在运行时用 PIL 生成、`config.example.json` 在 exe 旁边读取，
因此**不需要** `sys._MEIPASS` / 打包数据文件。

## 架构要点

- **单一 tkinter 根**：`Overlay.root` 贯穿整个生命周期；设置窗口永远是它的 `Toplevel`（`grab_set`），
  首启与托盘「打开设置」走同一条代码路径。
- 托盘线程（pystray）通过 `overlay.root.after(0, ...)` 回到 GUI 线程（与 `flash` 同一机制）。
- OBS 事件连接由 `ConnManager` 管理，支持凭据热更新与重连（`update()` / `request_reconnect()`）。
- 托盘菜单文本用 `lambda: tr(key)`，语言切换后菜单文本随之更新。

## 配置文件规则

- 程序从 `BASE_DIR / "config.json"` 读取；`load_config()` 容错缺字段（兼容旧 v0.1.0 配置）。
- 结构：

```json
{
  "language": "zh",
  "obs_websocket": { "host": "127.0.0.1", "port": 4455, "password": "CHANGE_ME" },
  "obs_path": ""
}
```

- 无 `config.json` 或密码仍为 `CHANGE_ME` → 首启弹出设置窗口（`needs_setup`）。
- 仓库只含模板 `config.example.json`。

## 自启管理

- 用 Windows **Startup 文件夹快捷方式**，不用注册表。
- OBSOverlay → `OBSOverlay.lnk`（frozen 指向 exe；源码指向 `pythonw + 脚本`）。
- OBS → `OBS Studio.lnk`（指向自动检测 / 用户选择的 `obs64.exe`）。
- 用 PowerShell `WScript.Shell` 创建 `.lnk`，**所有** `subprocess` 调用都带
  `creationflags=CREATE_NO_WINDOW`（`0x08000000`），绝不闪控制台。取消时只删除本项目的 `.lnk`。

## 敏感信息规则

- 真实密码 / token / 个人路径 / 用户名**绝不**进入源码、文档、提交历史、release。
- 真实配置仅存于本地 `config.json`（已 `.gitignore`，且不进任何 zip）。
- 错误处理 / 日志 / 弹窗里**不要**出现密码。`obsws-python` 内部会在 INFO 级日志里带 host/password，
  默认无 handler 不会输出 —— **不要**给它加 INFO 级文件日志。
- 提交 / 发布前按 `RELEASE_GUIDE.md` 跑敏感关键词扫描。

## 打包

```
scripts\build_portable.bat
```

它会：安装/检查依赖与 PyInstaller → 清理 `build/` `dist/` →
`pyinstaller --onefile --windowed --name OBSOverlay --hidden-import pystray._win32 src\obs_overlay.pyw` →
组装 portable 目录到 `E:\Backup\Releases\OBSOverlay\v0.2.0\` → 生成 portable zip 与
（`git archive HEAD`）source zip。

> 注意：source zip 用 `git archive HEAD`，**必须在提交 v0.2.0 之后**再生成 / 重生成，才会包含新代码。
> 优先 onefile；若某环境下 onefile 启动有问题，可改 `--onedir`（体积更大但更稳）。

## 测试方式

1. `python -m py_compile src\obs_overlay.pyw`。
2. `python src\obs_overlay.pyw` 跑一遍（验证导入 + 线程）。
3. 构建后**启动 exe**，确认进程存活并弹出设置窗口（onefile 常在缺后端时构建成功却启动崩溃，
   只检查「exe 存在」不够）。
4. 删除 `config.json` → 应弹设置窗口；保存后应生成 `config.json` 并进托盘。
5. OBS 开始 / 停止 / 暂停 / 继续录制，验证四种状态浮窗。

## 后续开发注意事项

- 改主程序前先读 `PROJECT_CONTEXT.md` 与 `docs/AI_HANDOFF.md`。
- 新增配置项时同步更新 `config.example.json`、README、USER_GUIDE。
- 保持轻量：不引入大型框架、不做自动更新 / 多主题 / 多场景 / 复杂日志页面（见 ROADMAP）。
