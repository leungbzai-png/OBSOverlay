# OBSOverlay 使用指南 (USER_GUIDE)

面向普通用户。跟着做即可，不需要懂编程。

## 0. 前置条件

- Windows 10 / 11。
- 已安装 [Python 3](https://www.python.org/)，安装时务必勾选 **Add Python to PATH**。
- 已安装 [OBS Studio](https://obsproject.com/)。

## 1. 安装依赖

双击：

```
scripts\install_deps.bat
```

它会显示要安装的包并让你输入 `YES` 确认，然后执行：

```
python -m pip install -r requirements.txt
```

如果提示找不到 Python，说明 Python 没装好或没加入 PATH，重新安装 Python 并勾选 *Add Python to PATH*。

## 2. 复制配置文件

在项目根目录，把：

```
config.example.json
```

复制一份，改名为：

```
config.json
```

（右键复制 → 粘贴 → 重命名即可。）

## 3. 填写你自己的 OBS WebSocket 配置

1. 打开 OBS → **工具(Tools) → WebSocket 服务器设置**。
2. 勾选 *Enable WebSocket server*，记下端口（默认 `4455`）。
3. 点 *Show Connect Info* 查看 / 设置密码。
4. 用记事本打开 `config.json`，把 `password` 改成你的真实密码：

```json
{
  "obs_websocket": {
    "host": "127.0.0.1",
    "port": 4455,
    "password": "这里填你自己的密码"
  }
}
```

> 注意：`config.json` 只保存在你本机，不会上传，也不会进入 Git。

## 4. 启动

双击：

```
src\obs_overlay.pyw
```

- 右下角托盘（点「^」展开）会出现一个深色小圆点图标。
- 右键图标 → **测试提示**，右上角出现蓝色弹窗即表示正常。
- 打开 OBS 开始录制，右上角会闪红色「● REC 开始录制」。

如果没创建 `config.json`，或密码还是 `CHANGE_ME`，程序会弹窗提示你先去配置，不会闪退而无声。

## 5. 设置开机自启（提示工具）

双击：

```
scripts\install_startup.bat
```

它会显示将要创建的自启项名称和路径，输入 `YES` 确认后才会写入，并立即启动一次。

## 6. 取消开机自启（提示工具）

双击：

```
scripts\uninstall_startup.bat
```

只会删除本工具创建的 `OBS Overlay.lnk`，不会动其他启动项。

## 7. 设置 OBS 开机自启

双击：

```
scripts\install_obs_startup.bat
```

- 会自动找常见 OBS 安装路径。
- 找不到时让你粘贴 `obs64.exe` 的完整路径，并检查文件是否存在。
- 写入前显示自启项名称和目标路径，输入 `YES` 确认。

## 8. 取消 OBS 开机自启

双击：

```
scripts\uninstall_obs_startup.bat
```

只会删除本工具创建的 `OBS Studio.lnk`。

## 9. 安全清理回归

双击：

```
scripts\reset_clean.bat
```

它**只**清理本项目自身的内容，并且每一步都显示目标路径、要求确认：

- 删除本工具的开机自启项（OBS Overlay / OBS Studio）。
- 删除本项目的 `__pycache__` / `logs` / `temp` / `cache`。
- 可选删除本地 `config.json`（需要单独输入 `DELETE` 确认）。

它**不会**删除任何项目源码目录、上级目录、旧目录或发布目录，也不会卸载其它软件。

## 常见问题 (FAQ)

**Q: 双击 .pyw 没反应？**
A: 多半是没装依赖或没建 `config.json`。先做第 1、2、3 步。如果配置缺失，程序会弹窗说明。

**Q: 浮窗被录进视频了？**
A: OBS 的「显示器采集」采集方法请选 **Windows 10 (1903 and up)**（新版默认即是）。

**Q: 托盘没图标？**
A: 点托盘区「^」展开隐藏图标；或确认程序确实在运行（任务管理器里有 `pythonw.exe`）。

**Q: 连不上 OBS？**
A: 确认 OBS 已开、WebSocket 已启用、`config.json` 里的端口和密码与 OBS 一致。程序会自动重连。

**Q: 自动找不到 pythonw.exe？**
A: 编辑 `scripts\install_startup.bat`，去掉 `REM set PYTHONW=...` 前的 `REM`，填上你的 `pythonw.exe` 路径后重新运行。
