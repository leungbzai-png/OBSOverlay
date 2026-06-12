# OBSOverlay 发布指南 (RELEASE_GUIDE)

## 本地发布目录

所有本地 release 产物归档在：

```
E:\Backup\Releases\OBSOverlay
```

每次发布建立一个版本子目录，例如：

```
E:\Backup\Releases\OBSOverlay\v0.1.0\
```

> 该目录**不在** Git 仓库内，也**不要**反向复制进源码仓库。

## 一次发布包含什么

`v0.1.0\` 至少包含：

- `OBSOverlay-v0.1.0-source.zip` — 源码包（仅 Git 跟踪的文件）。
- `README.md` — 该版本说明（可复制项目 README）。
- `CHANGELOG.md` — 变更记录。
- `RELEASE_NOTES.md` — 本次发布要点。

## release zip 必须排除

zip 中**不得**包含：

- `.git/`
- `.venv/`、`venv/`
- `__pycache__/`、`*.pyc`
- `build/`、`dist/`、`*.spec`
- `config.json`、`.env`、`secrets.*`、`credentials.*`
- 任何 release zip / exe 本身

## 推荐打包方式（最安全）

在**已提交**的仓库中用 `git archive`，它只会打包 Git 跟踪的文件，
自动排除 `.gitignore` 忽略项与 `.git` 本身：

```powershell
cd E:\Projects\Active\OBSOverlay
git archive --format=zip -o "E:\Backup\Releases\OBSOverlay\v0.1.0\OBSOverlay-v0.1.0-source.zip" HEAD
```

> 因为输出路径在 `E:\Backup\Releases\...`，产物不会进入仓库。

## 发布前检查清单

1. 跑一遍敏感关键词扫描（PowerShell）：

```powershell
cd E:\Projects\Active\OBSOverlay
Get-ChildItem -Recurse -File | Select-String -Pattern "password|passwd|token|secret|websocket|auth|credential|OLD_PASSWORD_EXAMPLE|Leung" | Where-Object { $_.Path -notlike "*\.git\*" }
```

可接受：`config.example.json` 里的 `CHANGE_ME`、文档中的占位符与配置说明。
不可接受：真实密码、真实 token、真实个人路径、用户名。

2. 确认 `config.json` 不在 zip 里：

```powershell
# 列出 zip 内容，确认无 config.json / .git / __pycache__
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::OpenRead("E:\Backup\Releases\OBSOverlay\v0.1.0\OBSOverlay-v0.1.0-source.zip").Entries | Select-Object FullName
```

3. GitHub 发布前**再次**人工检查 README、docs、scripts 是否有隐私信息或硬编码个人路径。

## GitHub Release（可选）

确认无敏感信息后，可在 GitHub 上以 tag `v0.1.0` 创建 Release，并上传
`OBSOverlay-v0.1.0-source.zip` 作为附件。**发布是不可逆的对外动作，发布前务必再核对一次。**
