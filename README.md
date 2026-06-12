# OBSOverlay

> 轻量级 Windows OBS 录屏提示 / 状态悬浮小工具
> A lightweight Windows overlay that shows OBS recording status while you record or stream.

OBSOverlay 是一个轻量级 Windows OBS 录屏状态悬浮工具，支持 OBS WebSocket 联动、
系统托盘常驻、开机自启、OBS 自启管理与安全配置文件。它在屏幕右上角显示一个
**录制不进画面**（capture-excluded）的小浮窗，当 OBS 开始 / 停止 / 暂停 / 继续录制时
闪一下状态提示，并常驻系统托盘。它通过 **OBS WebSocket** 与 OBS Studio 通信。

---

## 适用场景

- 录屏时想确认「现在到底有没有在录」，但又不想让提示出现在录制画面里。
- 直播 / 教学录制时，给自己一个明显的开始 / 暂停 / 停止状态反馈。
- 希望开机自动启动 OBS 和提示工具，少点几步操作。

## 功能列表（v0.1.0 已支持）

- **状态悬浮提示**：右上角浮窗显示录制状态（开始 / 停止 / 暂停 / 继续）。
- **录制不进画面**：使用 `WDA_EXCLUDEFROMCAPTURE`，浮窗**不会被录进视频**。
- **OBS WebSocket 联动**：监听 OBS 录制事件，断线自动重连。
- **OBS WebSocket 配置化**：从本地 `config.json` 读取 host / port / password。
- **系统托盘常驻**：带托盘图标，可手动「测试提示」和「退出」。
- **开机自启管理**：一键安装 / 取消提示工具的开机自启。
- **OBS 自启管理**：一键安装 / 取消 OBS Studio 的开机自启。
- **安全清理回归**：一键脚本只清理本项目自身内容，逐步确认。
- **`config.example.json` 模板**：配置与代码分离，**真实 `config.json` 不提交**。
- **缺配置友好提示**：缺少 `config.json` 或密码仍为 `CHANGE_ME` 时弹窗提示，不静默失败。

## 快速开始

1. 安装 [Python 3](https://www.python.org/)（勾选 *Add Python to PATH*）。
2. 安装依赖：双击 `scripts\install_deps.bat`（或 `python -m pip install -r requirements.txt`）。
3. 复制 `config.example.json` 为 `config.json`，填写你自己的 OBS WebSocket 密码。
4. 在 OBS 里启用 WebSocket（见下）。
5. 运行 `src\obs_overlay.pyw`（双击即可），托盘会出现深色小图标。

## 配置 OBS WebSocket

在 OBS Studio 中：**工具(Tools) → WebSocket 服务器设置(WebSocket Server Settings)**

- 勾选 *Enable WebSocket server*。
- 默认端口 `4455`。
- 点击 *Show Connect Info* 查看 / 设置密码。

## config.example.json / config.json 说明

仓库只包含**模板** `config.example.json`：

```json
{
  "obs_websocket": {
    "host": "127.0.0.1",
    "port": 4455,
    "password": "CHANGE_ME"
  }
}
```

使用前：

1. 复制 `config.example.json` → `config.json`。
2. 把 `password` 从 `CHANGE_ME` 改成你 OBS 里的真实 WebSocket 密码。

`config.json` 已在 `.gitignore` 中，**不会被提交**，你的密码只留在本机。
若未创建 `config.json` 或密码仍是 `CHANGE_ME`，程序会弹窗提示，不会静默失败。

## 安装依赖

```bat
python -m pip install -r requirements.txt
```

依赖：`obsws-python`、`pystray`、`pillow`（`tkinter` / `ctypes` 为 Python 标准库）。

## 启动方式

- 双击 `src\obs_overlay.pyw`（由 `pythonw.exe` 运行，无控制台窗口）。
- 或命令行：`pythonw src\obs_overlay.pyw`。

## 开机自启

- 安装：`scripts\install_startup.bat`（创建 Startup 快捷方式 `OBS Overlay.lnk`，会先让你确认）。
- 取消：`scripts\uninstall_startup.bat`（只删除本项目创建的该快捷方式）。

## OBS 开机自启

- 安装：`scripts\install_obs_startup.bat`
  - 自动检测常见 OBS 安装路径，找不到时让你手动输入 `obs64.exe` 路径。
  - 写入前显示自启项名称和目标路径并要求确认。
- 取消：`scripts\uninstall_obs_startup.bat`（只删除本项目创建的 `OBS Studio.lnk`）。

## 目录结构

```
OBSOverlay/
├─ src/
│  └─ obs_overlay.pyw        # 主程序（从 config.json 读取配置）
├─ scripts/
│  ├─ install_deps.bat
│  ├─ install_startup.bat
│  ├─ uninstall_startup.bat
│  ├─ install_obs_startup.bat
│  ├─ uninstall_obs_startup.bat
│  └─ reset_clean.bat        # 安全清理回归
├─ docs/                     # 用户 / 开发 / 发布 / 路线图等文档
├─ release/README.md         # 发布说明（产物本身不入库）
├─ config.example.json       # 配置模板（占位符）
├─ requirements.txt
├─ .gitignore
├─ LICENSE
├─ README.md
└─ PROJECT_CONTEXT.md
```

## 安全注意事项

- **绝不**把真实 OBS WebSocket 密码 / token 写进源码、文档或提交历史。
- 真实配置只放在本地 `config.json`（已被 `.gitignore` 忽略）。
- 发布 / 提交前请按 `docs/RELEASE_GUIDE.md` 再次检查敏感关键词。
- 清理请使用 `scripts\reset_clean.bat`，它只处理本项目自身的内容。

## License

[MIT](LICENSE) © OBSOverlay contributors
