# OBSOverlay — release 说明

本目录用于**项目内**的发布相关说明。**实际的 release 产物（exe / zip）不在这里、也不进 Git。**

本地 release 产物统一归档在仓库之外：

```
E:\Backup\Releases\OBSOverlay\<version>\
```

例如 `E:\Backup\Releases\OBSOverlay\v0.2.0\`，其中包含：

- `OBSOverlay-v0.2.0-portable.zip` — portable 版（含 `OBSOverlay.exe`），普通用户下载这个。
- `OBSOverlay-v0.2.0-source.zip` — 源码包（`git archive HEAD`）。
- `RELEASE_NOTES.md` — 发布要点。

打包与发布流程见 [`../docs/RELEASE_GUIDE.md`](../docs/RELEASE_GUIDE.md)。

要点回顾：

- 用 `scripts\build_portable.bat` 构建 exe 与两个 zip；source zip 需在**提交后**再生成。
- portable zip 是手动组装的，组装后要**显式核对**不含 `config.json` / `.env` / `.git` /
  `__pycache__` / secrets。
- release 产物不要提交进 Git（`.gitignore` 已忽略 `*.zip` / `*.exe`）。
- 发布前再次扫描敏感关键词（旧真实密码在文档中用占位 `OLD_PASSWORD_EXAMPLE` 代指，绝不写真值）。
