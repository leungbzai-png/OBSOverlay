# OBSOverlay 使用指南 (USER_GUIDE)

面向普通用户。v0.2.0 是 portable 版本，**解压即用**，不需要懂编程，也不需要安装 Python。

## 0. 前置条件

- Windows 10 / 11。
- 已安装 [OBS Studio](https://obsproject.com/)（并在其中启用 WebSocket，见第 3 步）。

## 1. 下载并解压

1. 下载 `OBSOverlay-v0.2.0-portable.zip`。
2. 解压到任意目录（建议放在你有写权限的文件夹，例如 `D:\Tools\OBSOverlay`）。
3. 解压后里面有 `OBSOverlay.exe`、`config.example.json`、`docs\`、`scripts\` 等。

> 配置、日志、缓存、数据都会保存在 `OBSOverlay.exe` 所在目录。整个文件夹搬到别处仍可用。

## 2. 双击启动

双击 **`OBSOverlay.exe`**。

- **首次启动**会自动弹出**设置窗口**（因为还没有 `config.json`）。
- 以后启动如果配置正常，会直接进托盘，不再弹窗。

## 3. 在 OBS 里启用 WebSocket

1. 打开 OBS → **工具(Tools) → WebSocket 服务器设置**。
2. 勾选 *Enable WebSocket server*，记下端口（默认 `4455`）。
3. 点 *Show Connect Info* 查看 / 设置密码。

## 4. 在设置窗口里填写

1. **语言 / Language**：选择 中文 或 English。
2. **Host**：一般保持 `127.0.0.1`。
3. **Port**：与 OBS 一致（默认 `4455`）。
4. **Password**：填 OBS 里的 WebSocket 密码（输入时以 `*` 隐藏）。
5. （可选）**OBS 程序路径**：点 **自动检测**；找不到就点 **浏览…** 选择 `obs64.exe`。
6. （可选）勾选 **开机自动启动 OBSOverlay** / **开机自动启动 OBS**。
7. 点 **测试连接** 验证（失败会提示，但不显示密码）。
8. 点 **保存并启动**。

保存后会在 exe 目录生成 `config.json`（只留在你本机，不会上传、不进 Git）。

## 5. 日常使用

- 托盘（右下角，点「^」展开）会出现一个深色小圆点图标。
- 右键图标可以：**打开设置 / 测试连接 / 重新连接 OBS / 打开程序目录 / 打开配置文件 / 退出**。
- 打开 OBS 开始录制，右上角会闪红色「● REC 开始录制」；停止 / 暂停 / 继续也各有提示。
- 浮窗使用 `WDA_EXCLUDEFROMCAPTURE`，**不会被录进视频**。

## 6. 开机自启

在设置窗口勾选 / 取消即可：

- **OBSOverlay 自启**：勾选创建 Startup 里的 `OBSOverlay.lnk`，取消时只删除它。
- **OBS 自启**：勾选创建 Startup 里的 `OBS Studio.lnk`（需要有效的 `obs64.exe` 路径），取消时只删除它。

> 这两个开关只动本工具创建的快捷方式，不会影响你已有的其它启动项。

## 7. 高级用户 / 故障恢复（可选）

普通用户用不到。`scripts\` 下的 `.bat` 是命令行备用工具：

- `install_startup.bat` / `uninstall_startup.bat`：命令行管理 OBSOverlay 自启。
- `install_obs_startup.bat` / `uninstall_obs_startup.bat`：命令行管理 OBS 自启。
- `reset_clean.bat`：安全清理本项目自身内容（自启项 / 缓存 / 可选 `config.json`），逐步确认，
  不会动你的项目目录、旧目录或其它软件。

## 常见问题 (FAQ)

**Q: 双击 exe 没反应？**
A: 等几秒看托盘。如果是首次启动应弹出设置窗口；若被杀软拦截，请允许运行。

**Q: 浮窗被录进视频了？**
A: OBS 的「显示器采集」采集方法请选 **Windows 10 (1903 and up)**（新版默认即是）。

**Q: 连不上 OBS？**
A: 确认 OBS 已开、WebSocket 已启用，设置窗口里的端口和密码与 OBS 一致。可在托盘点
   **重新连接 OBS**。程序也会自动重连。

**Q: 怎么改配置？**
A: 右键托盘 → **打开设置**，改完点 **保存并启动** 即可；或 **打开配置文件** 手动编辑 `config.json`。

**Q: 想换个文件夹？**
A: 直接整个文件夹移动即可，配置和数据都在里面。若开了自启，移动后请在设置里重新勾一次自启
   （让快捷方式指向新位置）。
