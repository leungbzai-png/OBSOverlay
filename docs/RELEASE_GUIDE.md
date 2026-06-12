# OBSOverlay 发布指南 (RELEASE_GUIDE)

## 本地发布目录

所有本地 release 产物归档在仓库**之外**：

```
E:\Backup\Releases\OBSOverlay\<version>\
```

例如 `E:\Backup\Releases\OBSOverlay\v0.2.1\`。该目录**不在** Git 仓库内，也**不要**反向复制进源码仓库。

## 一次发布包含什么（v0.2.1）

`v0.2.1\` 目录：

- `OBSOverlay-v0.2.1-portable\` — 组装好的 portable 目录。
- `OBSOverlay-v0.2.1-portable.zip` — portable 版（含 `OBSOverlay.exe`）。**普通用户下载这个。**
- `OBSOverlay-v0.2.1-source.zip` — 源码包（`git archive HEAD`，仅 Git 跟踪文件）。
- `RELEASE_NOTES.md` — 本次发布要点（`gh release create --notes-file` 读取）。

## 打包

```
scripts\build_portable.bat
```

构建 `OBSOverlay.exe`（`--onefile --windowed`，无控制台）、组装 portable 目录、生成两个 zip。
**source zip 用 `git archive HEAD`，必须在提交 v0.2.1 之后再生成 / 重生成**，否则只含旧代码。

## portable / source zip 必须排除

zip 中**不得**包含：

- `config.json`、`.env`、`secrets.*`、`credentials.*`
- `.git/`、`__pycache__/`、`*.pyc`
- `build/`、`dist/`、`*.spec`、`.venv/`、`venv/`
- 任何真实密码

> source zip 由 `git archive` 保证（只打包 Git 跟踪文件）。portable zip 由 `build_portable.bat`
> 手动组装 —— 因此组装后要**显式核对**上面这些都不在 zip 里。

## 发布前检查清单

1. 敏感关键词扫描（PowerShell，跳过 `.git`）：

```powershell
cd E:\Projects\Active\OBSOverlay
Get-ChildItem -Recurse -File |
  Where-Object { $_.FullName -notlike "*\.git\*" } |
  Select-String -Pattern "password|passwd|token|secret|websocket|auth|credential|OLD_PASSWORD_EXAMPLE|C:\\Users|E:\\OBSOverlay" |
  Select-Object Path, LineNumber, Line
```

可接受：`config.example.json` 的 `CHANGE_ME`、文档中的占位符与配置字段说明、`.gitignore` 规则、
标准 OBS 安装路径、把旧目录 `E:\OBSOverlay` 作为「不要改动」的说明。
不可接受：真实密码（旧真实密码在文档中一律用占位 `OLD_PASSWORD_EXAMPLE` 代指，绝不写真值）、
真实 token / secret、真实 `config.json` 内容、个人凭据。

2. 核对两个 zip 的内容（确认无 `config.json` / `.git` / `__pycache__` / secrets）：

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
foreach ($z in 'OBSOverlay-v0.2.1-portable.zip','OBSOverlay-v0.2.1-source.zip') {
  [IO.Compression.ZipFile]::OpenRead("E:\Backup\Releases\OBSOverlay\v0.2.1\$z").Entries.FullName
}
```

3. 启动 `OBSOverlay.exe` 确认能正常起来（弹设置窗口 / 进托盘），不要只检查 exe 是否存在。

4. GitHub 发布前**再次**人工检查 README / docs / scripts 是否有隐私信息或硬编码个人路径。

## GitHub Release

确认无敏感信息后：

```powershell
gh release create v0.2.1 ^
  "E:\Backup\Releases\OBSOverlay\v0.2.1\OBSOverlay-v0.2.1-portable.zip" ^
  "E:\Backup\Releases\OBSOverlay\v0.2.1\OBSOverlay-v0.2.1-source.zip" ^
  --title "OBSOverlay v0.2.1 Hotfix" ^
  --notes-file "E:\Backup\Releases\OBSOverlay\v0.2.1\RELEASE_NOTES.md"
```

> **发布是不可逆的对外动作**，发布前务必再核对一次。若该 tag 的 Release 已存在，不要重复创建。
