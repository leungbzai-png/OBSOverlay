# OBSOverlay

> 轻量级 Windows OBS 录屏提示 / 状态悬浮小工具（v0.2.1 Final Portable Edition）
> A lightweight Windows overlay that shows OBS recording status while you record or stream.

OBSOverlay 在屏幕右上角显示一个**录制不进画面**（capture-excluded）的小浮窗，当 OBS
开始 / 停止 / 暂停 / 继续录制时闪一下状态提示，并常驻系统托盘。它通过 **OBS WebSocket**
与 OBS Studio 通信。

**v0.2.1** 是最终实用 **portable 版本**（v0.2.0 的小修补丁：修复设置窗口最小化按钮、
增强 OBS 路径自动识别）：解压即用，普通用户不再需要手动编辑 `config.json`，
也不需要手动运行 `.bat`。首次启动会弹出设置窗口，让你选择语言、填写 OBS WebSocket、
并按需开启开机自启。

---

## 适用场景

- 录屏时想确认「现在到底有没有在录」，但又不想让提示出现在录制画面里。
- 直播 / 教学录制时，给自己一个明显的开始 / 暂停 / 停止状态反馈。
- 希望开机自动启动 OBS 和提示工具，少点几步操作。

## 快速开始（推荐：portable 版）

1. 下载 `OBSOverlay-v0.2.1-portable.zip` 并**解压到任意目录**（建议放在你有写权限的文件夹）。
2. 双击 **`OBSOverlay.exe`**。
3. 首次启动会弹出**设置窗口**：
   - **选择语言**：中文 / English。
   - **填写 OBS WebSocket**：Host（默认 `127.0.0.1`）、Port（默认 `4455`）、Password。
   - 可选 **勾选开机自启**（OBSOverlay 和 / 或 OBS）。
   - 点 **测试连接** 验证，再点 **保存并启动**。
4. 托盘出现深色小圆点图标，开始录制时右上角会闪红色「● REC 开始录制」。

> 配置、日志、缓存、数据都保存在 **`OBSOverlay.exe` 所在目录**（`config.json` / `logs/` /
> `cache/` / `data/`）。把整个文件夹搬到别处仍可用。`config.json` 只留在本机，**不会上传、不进 Git**。

## 在 OBS 里启用 WebSocket

在 OBS Studio 中：**工具(Tools) → WebSocket 服务器设置(WebSocket Server Settings)**

- 勾选 *Enable WebSocket server*。
- 默认端口 `4455`。
- 点击 *Show Connect Info* 查看 / 设置密码，填进 OBSOverlay 设置窗口。

## 托盘菜单

右键托盘图标：

- **打开设置 / Open settings** — 重新打开设置窗口。
- **测试连接 / Test connection** — 测试当前配置能否连上 OBS。
- **重新连接 OBS / Reconnect OBS** — 用最新配置重连。
- **打开程序目录 / Open folder** — 打开 exe 所在目录。
- **打开配置文件 / Open config** — 打开 `config.json`。
- **退出 / Exit**。

## 设置窗口字段

- 语言 / Language：中文 / English
- OBS WebSocket Host / Port / Password（密码隐藏输入）
- 开机自动启动 OBSOverlay / Start OBSOverlay with Windows
- 开机自动启动 OBS / Start OBS with Windows
- OBS 程序路径（`obs64.exe`）+ **自动检测** / **浏览…** 按钮
- 按钮：**测试连接** / **保存并启动** / **取消**

自启通过 Windows **Startup 文件夹快捷方式**实现：勾选创建 `OBSOverlay.lnk` /
`OBS Studio.lnk`，取消时只删除本项目创建的对应快捷方式，不动你的其它启动项。

## 高级用户 / 故障恢复

`scripts/` 下的 `.bat` 脚本是给高级用户和故障恢复用的，普通用户**不需要**：

| 脚本 | 作用 |
|------|------|
| `build_portable.bat` | 构建 `OBSOverlay.exe` 与 portable / source zip |
| `install_deps.bat` | 安装 Python 运行依赖（源码运行时用） |
| `install_startup.bat` / `uninstall_startup.bat` | 命令行方式管理 OBSOverlay 自启 |
| `install_obs_startup.bat` / `uninstall_obs_startup.bat` | 命令行方式管理 OBS 自启 |
| `reset_clean.bat` | 安全清理本项目自身内容（自启项 / 缓存 / 可选 config.json） |

从源码运行（开发者）：见 [`docs/DEV_GUIDE.md`](docs/DEV_GUIDE.md)。

## config.example.json

仓库只包含**模板** `config.example.json`（普通用户无需手动复制，设置窗口会自动生成 `config.json`）：

```json
{
  "language": "zh",
  "obs_websocket": {
    "host": "127.0.0.1",
    "port": 4455,
    "password": "CHANGE_ME"
  },
  "obs_path": ""
}
```

`config.json` 已在 `.gitignore` 中，**不会被提交**，也不放进任何发布 zip。

## 目录结构

```
OBSOverlay/
├─ src/obs_overlay.pyw       # 主程序（portable 路径 + 设置窗口 + 托盘 + OBS WebSocket）
├─ scripts/
│  ├─ build_portable.bat     # 打包 exe + portable / source zip
│  ├─ install_deps.bat
│  ├─ install_startup.bat / uninstall_startup.bat
│  ├─ install_obs_startup.bat / uninstall_obs_startup.bat
│  └─ reset_clean.bat        # 安全清理回归
├─ docs/                     # 用户 / 开发 / 发布 / 路线图等文档
├─ logs/ cache/ data/        # 运行时数据（跟随 exe；内容不入库）
├─ release/README.md
├─ config.example.json
├─ requirements.txt
├─ .gitignore / LICENSE / README.md / PROJECT_CONTEXT.md
```

## 安全注意事项

- **绝不**把真实 OBS WebSocket 密码 / token 写进源码、文档或提交历史。
- 真实配置只放在本地 `config.json`（已被 `.gitignore` 忽略，且不进任何 zip）。
- 程序在日志 / 异常 / 错误弹窗中**不会**输出密码。
- 发布 / 提交前请按 [`docs/RELEASE_GUIDE.md`](docs/RELEASE_GUIDE.md) 再次检查敏感关键词。

## License

[MIT](LICENSE) © OBSOverlay contributors
