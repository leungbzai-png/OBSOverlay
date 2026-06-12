# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

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
