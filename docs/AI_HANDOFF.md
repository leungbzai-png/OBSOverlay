# AI 交接说明 (AI_HANDOFF)

> 写给后续接手本项目的 AI（Claude / GPT / Codex 等）。先读本文件，再动手。

## 这个项目是什么

**OBSOverlay** — 轻量级 Windows OBS 录屏提示 / 状态悬浮小工具。
通过 OBS WebSocket 监听录制状态，在屏幕右上角显示一个**录制不进画面**的浮窗，常驻托盘。

## 关键目录

- **旧目录（只读素材，禁止破坏 / 删除 / 在其中开发）：**
  `E:\OBSOverlay`
- **新项目源码目录（正式开发，Git 仓库在此）：**
  `E:\Projects\Active\OBSOverlay`
- **本地发布目录（产物归档，不入库）：**
  `E:\Backup\Releases\OBSOverlay`

## 当前版本

`v0.2.1 — Final Portable Edition (Hotfix)` —— 已开源发布到 GitHub（<https://github.com/leungbzai-png/OBSOverlay>）。
v0.2.1 在 v0.2.0 之上只修两点：设置窗口最小化按钮无响应、OBS 路径自动识别（含读取已有
Startup `OBS Studio.lnk` 目标、支持 D/E 盘常见路径）。详见 `docs/CHANGELOG.md`。

## v0.2.0 已实现功能（不要再当成待办）

Portable `OBSOverlay.exe`（PyInstaller，数据跟随 exe 目录）、首次启动设置窗口、
中文 / English 选择、GUI 填写 OBS WebSocket、GUI 管理 OBSOverlay / OBS 开机自启、
托盘菜单（设置 / 测试连接 / 重连 / 打开目录 / 打开配置 / 退出）、`build_portable.bat` 打包脚本。
加上 v0.1.0 的状态悬浮提示（不进画面）、WebSocket 联动与自动重连、托盘常驻、`.bat` 工具。
详见 README / `docs/CHANGELOG.md`。

## 维护态项目（重要）

v0.2.0 是**最终实用版本**，后续只做维护：修 bug、适配未来 OBS WebSocket 变化、
必要时更新依赖 / 优化打包。**不要**引入 PyQt / Electron / Wails、自动更新、多主题、多场景、
复杂日志页面，也**不要**大规模重构。见 `docs/ROADMAP.md`。

## 关键实现要点

- 主程序单文件 `src/obs_overlay.pyw`，**单一 tkinter 根**（overlay.root）贯穿整个生命周期；
  设置窗口永远是它的 `Toplevel`；托盘线程通过 `overlay.root.after(0, ...)` 回到 GUI 线程。
- portable 路径：`IS_FROZEN` 时 `BASE_DIR = exe 目录`，否则 `= 项目根`。所有数据从 `BASE_DIR` 推导。
- 自启用 Startup 文件夹 `.lnk`（PowerShell + `CREATE_NO_WINDOW`，绝不闪控制台）。
- 密码绝不进日志 / 异常 / 弹窗；`obsws-python` 内部 INFO 日志默认无 handler，不要给它加 INFO 文件日志。

## 核心文件

- `src/obs_overlay.pyw` — 主程序（托盘 + tkinter 浮窗 + OBS WebSocket 事件，配置来自 `config.json`）。
- `config.example.json` — 配置模板（占位符 `CHANGE_ME`）。
- `scripts/*.bat` — 安装 / 卸载 / 清理脚本。
- `.gitignore` — 已忽略 `config.json` 等敏感文件。

## 修改前必须先读

1. `PROJECT_CONTEXT.md`
2. 本文件 `docs/AI_HANDOFF.md`
3. `docs/DEV_GUIDE.md`
4. 涉及发布时：`docs/RELEASE_GUIDE.md`

## 敏感信息规则（最高优先级）

- 真实 OBS WebSocket 密码 / token / 个人路径 / 用户名**绝不**进入源码、文档、提交历史、release。
- 真实配置只放本地 `config.json`（已 `.gitignore`）。
- `.pyw` 无控制台，报错用 `tkinter.messagebox` 弹窗，且**不要**把密码写进日志 / 异常文本。
- 不确定是否敏感 → 当作敏感处理，不提交。
- 历史上旧源码里出现过一个真实密码，已**不得**再次引入新仓库。

## 禁止事项

- 不删除 / 不破坏旧目录 `E:\OBSOverlay`。
- 不在旧目录或 release 目录里初始化 Git。
- 不把 release 产物或 `config.json` 提交进 Git。
- 不改动其它项目（`E:\Projects\Active` 下的其它文件夹）。
- 未经用户明确确认，不 `git push`、不 `gh repo create`。
- 不在脚本里写死个人安装路径。

## 后续优先级

见 `docs/ROADMAP.md`。近期重点：UI 美化、配置项扩展（位置/颜色/时长）、全局快捷键、打包 exe。
