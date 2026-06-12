# OBSOverlay 路线图 (ROADMAP)

当前版本：**v0.2.0 — Final Portable Edition**。

v0.2.0 是面向普通用户的最终实用 portable 版本：免装 Python 的 `OBSOverlay.exe`、
首次启动设置窗口、中文 / English 选择、GUI 填写 OBS WebSocket、GUI 管理 OBSOverlay 与 OBS
开机自启、托盘菜单管理，配置 / 日志 / 缓存 / 数据全部跟随 exe 目录（详见 README / CHANGELOG）。

## 维护计划（不再做大型新功能）

本项目已达到设计目标，后续只做**维护性**工作，保持轻量、稳定、简单：

- **修 bug**：修复使用中发现的问题。
- **适配未来 OBS WebSocket 变化**：OBS / `obsws-python` 协议或接口变动时跟进。
- **必要时更新依赖**：安全或兼容性需要时升级 `obsws-python` / `pystray` / `pillow` / PyInstaller。
- **必要时优化打包**：打包体积、启动速度、兼容性等小幅优化。

## 明确不计划做的事

- 不引入 PyQt / Electron / Wails 等大型 GUI 框架。
- 不做自动更新。
- 不做多主题系统。
- 不做多场景模板。
- 不做复杂日志页面。
- 不做大规模重构。
- 不跨平台（依赖 Windows 的 `WDA_EXCLUDEFROMCAPTURE`）。
