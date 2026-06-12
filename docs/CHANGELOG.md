# Changelog

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [0.1.0] - 2026-06-12

首个项目化版本。

### Added
- 规范化项目结构（`src/` `scripts/` `docs/` `release/`）。
- 配置外置：`config.example.json` 模板 + 本地 `config.json`（不入库）。
- 主程序从项目根 `config.json` 读取 OBS WebSocket 配置；缺失 / 占位符 / 格式错误时弹窗提示。
- 安全脚本：`install_deps` / `install_startup` / `uninstall_startup` /
  `install_obs_startup` / `uninstall_obs_startup` / `reset_clean`，均带路径显示与确认。
- OBS 自启脚本去除硬编码路径，改为自动检测 + 手动输入并校验。
- `reset_clean.bat` 重写为安全版，仅清理本项目内容，逐步确认。
- 文档：README、USER_GUIDE、DEV_GUIDE、RELEASE_GUIDE、ROADMAP、AI_HANDOFF、PROJECT_CONTEXT。
- `.gitignore`、MIT `LICENSE`、`requirements.txt`。

### Security
- 移除源码中硬编码的真实 OBS WebSocket 密码，改为本地配置。
- 移除脚本中的硬编码个人安装路径。
- `.gitignore` 忽略 `config.json` / `.env` / `secrets.*` / `credentials.*` 等。

### Changed
- 旧中文文件名整理为英文文件名，便于开源。
