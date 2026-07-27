# 变更记录

## 未发布

- docs: TASK-009 为 5 个现有 command 页面追加如实勾选的完整性检查清单。
- docs: TASK-008 返工补齐其余 17 个内容页面的官方来源元数据，覆盖全部 30 个内容页面。
- docs: TASK-008 为 11 个指定内容页面补齐独立的官方来源元数据章节。
- fix: TASK-007 统一指定页面的 EMC 与 LAMMPS 版本元数据，区分本地和服务器验证版本。
- fix: TASK-006 分离 LAMMPS 命令可用性与示例运行验证状态，并标明 EMC CLI 输出来自服务器、本地 macOS EMC 待安装。
- chore: TASK-005 修正 STATUS.md 的页面统计、模块计数、翻译完成度、环境说明、约 65,000+ 中文字估算和阶段 1 执行计划。
- feat: 新增 EMC 手册、LAMMPS 命令、文件格式与力场索引入口，并恢复相应首页链接。
- chore: 新增 `.gitignore`，清理空的 `build/{site}/` 无效目录。
- fix: 修复所有 Markdown 内部失效链接；对尚未创建的页面和类别目录保留文字并标记“待创建”。
- feat: 新增 `scripts/check_links.py`，用于检查 `docs/` 中的相对 Markdown 链接与锚点，并提供严格模式。
- 建立 `PROJECT.md`。
- 建立 `AGENTS.md`。
- 建立 Claude Code 与 Codex 双 Agent 协作规范。
