# OBSOverlay — release 说明

本目录用于**项目内**的发布相关说明。**实际的 release 产物（zip / exe）不在这里、也不进 Git。**

本地 release 产物统一归档在仓库之外：

```
E:\Backup\Releases\OBSOverlay\<version>\
```

例如 `E:\Backup\Releases\OBSOverlay\v0.1.0\`。

打包与发布流程见 [`../docs/RELEASE_GUIDE.md`](../docs/RELEASE_GUIDE.md)。

要点回顾：

- 用 `git archive` 从已提交的仓库打包，自动排除 `.git`、`config.json`、`__pycache__` 等。
- release 产物不要提交进 Git（`.gitignore` 已忽略 `*.zip` / `*.exe`）。
- 发布前再次扫描敏感关键词。
