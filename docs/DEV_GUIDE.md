# OBSOverlay 开发指南 (DEV_GUIDE)

面向开发 / 维护者。

## 项目结构

```
OBSOverlay/
├─ src/obs_overlay.pyw       # 主程序：托盘 + tkinter 浮窗 + OBS WebSocket 事件
├─ scripts/*.bat             # 安装/卸载/清理脚本（英文 echo，自定位）
├─ docs/*.md                 # 文档
├─ release/README.md         # 发布说明（产物不入库）
├─ config.example.json       # 配置模板（占位符）
├─ requirements.txt
├─ .gitignore
├─ LICENSE
├─ README.md
└─ PROJECT_CONTEXT.md
```

## Python 依赖

运行时（`requirements.txt`）：

- `obsws-python` — OBS WebSocket v5 客户端。
- `pystray` — 系统托盘图标。
- `pillow` — 生成托盘图标位图。

标准库：`tkinter`、`ctypes`、`threading`、`json`、`pathlib`。

安装：

```
python -m pip install -r requirements.txt
```

## 本地运行

```
pythonw src\obs_overlay.pyw      # 无控制台（正式运行方式）
python  src\obs_overlay.pyw      # 有控制台，便于调试看 traceback
```

> 注意：`.pyw` 由 `pythonw.exe` 运行时**没有控制台**，因此所有面向用户的报错都用
> `tkinter.messagebox` 弹窗，不要用 `print` / `stderr`（用户看不到）。

## bat 脚本说明

| 脚本 | 作用 |
|------|------|
| `install_deps.bat` | `python -m pip install -r requirements.txt`，先确认 |
| `install_startup.bat` | 创建 `OBS Overlay.lnk` 自启项，写入前确认 |
| `uninstall_startup.bat` | 删除 `OBS Overlay.lnk` |
| `install_obs_startup.bat` | 检测/询问 `obs64.exe`，创建 `OBS Studio.lnk`，确认后写入 |
| `uninstall_obs_startup.bat` | 删除 `OBS Studio.lnk` |
| `reset_clean.bat` | 仅清理本项目自启项/缓存/可选 config.json，逐步确认 |

脚本约定：

- 用 `cd /d "%~dp0.."` 自定位到项目根，不依赖当前目录。
- 所有 `echo` 用**英文 ASCII**，避免控制台 OEM 代码页下中文乱码；中文说明放在 `.md`。
- 自启脚本指向 `%CD%\src\obs_overlay.pyw`。
- 危险动作前显示路径并要求输入 `YES`/`DELETE`；出错 `pause`。

## 配置文件规则

- 程序从**项目根**的 `config.json` 读取（`Path(__file__).resolve().parent.parent / "config.json"`），
  因此从 Startup 快捷方式启动（CWD 不确定）也能正确定位。
- 缺少 `config.json`、JSON 格式错误、密码仍为 `CHANGE_ME` → 弹窗提示并退出。
- 仓库只含模板 `config.example.json`。

## 敏感信息规则

- **任何**真实密码 / token / 个人路径 / 用户名都不得进入源码、文档、提交历史。
- 真实配置仅存于本地 `config.json`（已 `.gitignore`）。
- 错误处理里不要把密码写进日志或异常文本。
- 提交 / 发布前按 `RELEASE_GUIDE.md` 跑敏感关键词扫描。

## 测试方式

目前为手动测试：

1. 准备本地 `config.json`（真实密码）。
2. `python src\obs_overlay.pyw`，托盘右键「测试提示」应弹蓝框。
3. 故意删除 `config.json` / 把密码改回 `CHANGE_ME`，应弹出对应提示窗。
4. OBS 开始/停止/暂停/继续录制，验证四种状态浮窗。

## 打包思路（可选）

- 用 `pyinstaller` 打成单文件 exe（`*.spec`、`build/`、`dist/` 已忽略）。
- 注意：exe 仍需读取外部 `config.json`，打包时不要把真实配置打进去。

## 后续开发注意事项

- 改主程序前先读 `PROJECT_CONTEXT.md` 与 `docs/AI_HANDOFF.md`。
- 新增配置项时同步更新 `config.example.json`、README、USER_GUIDE。
- 保持轻量，不要引入重型框架。
