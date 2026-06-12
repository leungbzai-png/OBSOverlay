# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.2.1] - 2026-06-13 — Hotfix

在 v0.2.0 portable 基础上的小修补丁，仅修两个问题，不改项目定位、不引入新框架、不做新功能。

### Fixed
- **设置窗口最小化按钮无响应**：设置窗口此前用 `grab_set()`（模态）+ `-topmost` 创建，
  且作为隐藏 override-redirect 根窗口的 Toplevel，没有独立任务栏按钮 —— 模态 + 无任务栏目标
  导致点击标题栏「最小化」无任何反应。现已移除 `grab_set()` 与 `-topmost`，并通过 Win32
  `WS_EX_APPWINDOW` 给设置窗口一个独立任务栏按钮，最小化按钮恢复正常。

### Changed
- **增强 OBS 程序路径自动识别**：自动检测优先级改为
  ① `config.json` 中已有且存在的 `obs_path` / `obs_exe_path`；
  ② 现有 Startup `OBS Studio.lnk` 指向的 `obs64.exe`；
  ③ 常见安装路径（新增 `E:\OBS`、`D:\OBS`、`E:\OBS Studio`、`D:\OBS Studio` 等）；
  ④ 对少数常见目录做浅层固定子路径探测（**不**做全盘递归扫描）。
- **从托盘「打开设置」可恢复已最小化窗口**：窗口存在且最小化时 `deiconify` 恢复，否则 `lift` 置前，
  已关闭则重新打开。
- **保存时按需识别 OBS 路径**：勾选「OBS 开机自启」但路径为空时，保存前自动识别一次，
  成功则继续，失败才提示浏览选择 `obs64.exe`；**未勾选时路径为空不阻止保存**，也不会创建无效 `.lnk`。

### Unchanged
- 保持 v0.2.0 的 portable-first 行为：配置 / 日志 / 缓存 / 数据继续跟随 `OBSOverlay.exe` 所在目录。
- 密码仍**绝不**写入日志 / 异常 / 弹窗；只管理本项目自己的 `OBSOverlay.lnk` / `OBS Studio.lnk`。

## [0.2.0] - 2026-06-13 — Final Portable Edition

最终实用 portable 版本。普通用户解压即用，不再需要手动编辑 `config.json`，也不需要手动运行 `.bat`。

### Added
- **Portable `OBSOverlay.exe`**：用 PyInstaller 打包的免装 Python 单文件（windowed，无控制台）。
- **首次启动设置窗口**：没有 `config.json`（或密码仍是 `CHANGE_ME`）时自动弹出 tkinter 设置窗口。
- **中文 / English 语言选择**：设置窗口、弹窗、托盘菜单支持中英文，语言保存到 `config.json`；
  首启可按系统语言自动判断。
- **GUI 填写 WebSocket 配置**：在设置窗口填写 host / port / password（密码隐藏输入）。
- **GUI 管理 OBSOverlay 开机自启**：勾选/取消即创建/删除 Startup 里的 `OBSOverlay.lnk`。
- **GUI 管理 OBS 开机自启**：勾选/取消即创建/删除 Startup 里的 `OBS Studio.lnk`；
  支持自动检测 `obs64.exe`、浏览选择路径。
- **托盘菜单管理入口**：打开设置 / 测试连接 / 重新连接 OBS / 打开程序目录 / 打开配置文件 / 退出。
- **测试连接**：设置窗口与托盘均可测试 OBS WebSocket，失败时友好提示且**不显示密码**。
- **打包脚本** `scripts/build_portable.bat`：构建 exe、组装 portable 目录、生成 portable zip 与 source zip。

### Changed
- **配置 / 日志 / 缓存 / 数据全部跟随 exe 目录**：portable 模式下 `base_dir = exe 所在目录`，
  源码模式下 `base_dir = 项目根`；新增 `logs/` `cache/` `data/` 目录。
- `config.json` 新增 `language` 与 `obs_path` 字段；`load_config` 容错旧版 v0.1.0 配置。
- `.bat` 脚本定位为**高级用户 / 故障恢复工具**，普通用户不再需要。
- ROADMAP 改为维护计划，不再堆叠大型新功能。

### Security
- OBS WebSocket 密码**绝不**写入日志、异常文本或错误弹窗。
- portable zip / source zip 均不含 `config.json` / `.env` / `secrets` / `credentials` / `.git` / `__pycache__`。
- `config.example.json` 的 `password` 仍为占位符 `CHANGE_ME`。

## [0.1.0] - 2026-06-12

首个开源整理版本——一个完整、可用的初始版本。

### Added
- 初始化开源项目结构（`src/` `scripts/` `docs/` `release/`）。
- 实现 OBS 状态悬浮提示：右上角浮窗显示开始 / 停止 / 暂停 / 继续录制状态，
  使用 `WDA_EXCLUDEFROMCAPTURE` 保证浮窗**不被录进画面**。
- 支持 OBS WebSocket 联动：监听录制事件，断线自动重连。
- 支持 OBS WebSocket 配置化：从项目根 `config.json` 读取 host / port / password；
  配置外置为 `config.example.json` 模板 + 本地 `config.json`（不入库）；
  缺失 / 占位符 / 格式错误时弹窗提示，不静默失败。
- 支持系统托盘常驻：带托盘图标，提供「测试提示」「退出」菜单。
- 支持开机自启管理：`install_startup` / `uninstall_startup` 安装与取消提示工具自启。
- 支持 OBS 开机自启管理：`install_obs_startup` / `uninstall_obs_startup`，
  自动检测安装路径，找不到时让用户输入并校验。
- 支持安全清理回归：`reset_clean.bat` 仅清理本项目自身内容，逐步确认。
- 依赖安装脚本 `install_deps.bat`，普通用户双击 `.bat` 即可使用。
- 完整文档：README、USER_GUIDE、DEV_GUIDE、RELEASE_GUIDE、ROADMAP、AI_HANDOFF、PROJECT_CONTEXT。
- `.gitignore`、MIT `LICENSE`、`requirements.txt`。
- 完成本地 source release（`git archive` 生成的源码包，归档于仓库外）。

### Security
- 移除源码中硬编码的真实 OBS WebSocket 密码，改为本地配置。
- 移除脚本中的硬编码个人安装路径。
- `.gitignore` 忽略 `config.json` / `.env` / `secrets.*` / `credentials.*` 等。

### Changed
- 旧中文文件名整理为英文文件名，便于开源。
