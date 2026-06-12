# PROJECT_CONTEXT — OBSOverlay

> 项目上下文速览，方便新的 AI 对话快速接手。配合 `docs/AI_HANDOFF.md` 阅读。

## 项目名称

OBSOverlay

## 项目定位

轻量级 Windows OBS 录屏提示 / 状态悬浮小工具。录屏 / 直播时在右上角显示录制状态，
浮窗**不会被录进画面**，常驻系统托盘，通过 OBS WebSocket 联动。

## 技术栈

- 语言：Python 3（`.pyw`，由 `pythonw.exe` 无控制台运行）。
- GUI：`tkinter`（浮窗）+ `pystray`（托盘）+ `pillow`（图标）。
- 系统：`ctypes` 调用 Win32 `SetWindowDisplayAffinity`（capture-excluded）。
- 通信：`obsws-python`（OBS WebSocket v5）。
- 脚本：Windows `.bat`。

## 目录规范

| 用途 | 路径 | 规则 |
|------|------|------|
| 旧目录（素材） | `E:\OBSOverlay` | 只读，禁止破坏 / 删除 / 在其中开发 |
| 源码（开发 + Git） | `E:\Projects\Active\OBSOverlay` | 正式开发目录 |
| 本地发布 | `E:\Backup\Releases\OBSOverlay` | 产物归档，不入库、不反向复制进仓库 |

## 当前版本

v0.2.1 — Final Portable Edition (Hotfix)

## 当前状态

v0.2.1 是 v0.2.0 之上的小修补丁：修复设置窗口最小化按钮无响应（移除 `grab_set`/`-topmost`，
通过 `WS_EX_APPWINDOW` 给设置窗口独立任务栏按钮），并增强 OBS 路径自动识别（读取已有
Startup `OBS Studio.lnk` 目标、支持 D/E 盘常见安装路径）。其余沿用 v0.2.0：免装 Python 的 `OBSOverlay.exe`，
首次启动设置窗口、中英文选择、GUI 填写 WebSocket、GUI 管理 OBSOverlay / OBS 开机自启、
托盘菜单管理，配置 / 日志 / 缓存 / 数据全部跟随 exe 目录。已开源发布到 GitHub
（<https://github.com/leungbzai-png/OBSOverlay>）。

## v0.2.0 已实现功能

- Portable `OBSOverlay.exe`（PyInstaller，windowed 无控制台），数据跟随 exe 目录。
- 首次启动设置窗口（无 `config.json` 或密码仍为 `CHANGE_ME` 时弹出）。
- 中文 / English 语言选择，保存到 `config.json`，可按系统语言自动判断。
- GUI 填写 OBS WebSocket host / port / password（密码隐藏，不进日志）。
- GUI 管理 OBSOverlay 开机自启（Startup `OBSOverlay.lnk`）。
- GUI 管理 OBS 开机自启（Startup `OBS Studio.lnk`，支持自动检测 / 浏览 `obs64.exe`）。
- 托盘菜单：打开设置 / 测试连接 / 重新连接 / 打开程序目录 / 打开配置文件 / 退出。
- `scripts/build_portable.bat` 打包脚本，生成 portable zip + source zip。

## v0.1.0 已实现功能（沿用至今）

- OBS 录屏状态悬浮提示（开始 / 停止 / 暂停 / 继续，`WDA_EXCLUDEFROMCAPTURE` 不进画面）。
- OBS WebSocket 联动，断线自动重连。
- 从 `config.json` 读取配置；`config.example.json` / `config.json` 分离，真实密码不提交。
- 系统托盘常驻 + 托盘图标。
- 自启 / 清理 / 依赖 `.bat` 脚本（v0.2.0 起定位为高级用户 / 故障恢复工具）。

## 已完成的整理过程

- 从旧目录复制并改造源码与脚本，整理为英文文件名。
- 主程序改为从 `config.json` 读取配置；移除硬编码真实密码。
- OBS 自启脚本去除硬编码路径；清理脚本重写为安全版。
- 生成全套文档、`.gitignore`、MIT LICENSE、`requirements.txt`、`config.example.json`。

## 后续迭代计划

见 `docs/ROADMAP.md`：v0.2.0 已是最终实用版本，后续只做维护（修 bug、适配 OBS WebSocket 变化、
必要时更新依赖 / 优化打包），不计划引入大型功能或框架。

## 开发前必须阅读的文档

1. 本文件 `PROJECT_CONTEXT.md`
2. `docs/AI_HANDOFF.md`
3. `docs/DEV_GUIDE.md`
4. 发布相关：`docs/RELEASE_GUIDE.md`

## 禁止事项

- 不删除 / 破坏旧目录与 release 目录。
- 不提交 `config.json` / `.env` / 真实密码 / token / 个人路径 / 用户名。
- 不在旧目录或 release 目录初始化 Git。
- 未经用户确认不 push、不创建远程仓库。
- 不改动其它项目。

## 敏感信息处理规则

- 真实凭据只存本地 `config.json`（已忽略）；仓库只含 `config.example.json` 占位符。
- `.pyw` 无控制台，用弹窗报错，且不在日志 / 异常中输出密码。
- 提交 / 发布前跑敏感关键词扫描（见 `docs/RELEASE_GUIDE.md`）。
- 不确定是否敏感 → 当作敏感，不提交。
