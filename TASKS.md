# 项目任务

> 当前阶段：阶段 1 — 项目审计与 Harness 建设
> 审计报告：[reports/project_audit.md](reports/project_audit.md)
> 生成日期：2026-07-26

---

## 优先级概览

| 优先级 | 任务数 | 说明 |
|--------|--------|------|
| P0 | 4 | 网站构建失败、缺失文件、空 Harness |
| P1 | 6 | 版本混用、虚假验证标记、来源缺失、数量不一致 |
| P2 | 4 | 测试基础设施、变更记录、command 参数审计 |

---

## 依赖关系图

```
TASK-001 (check_links.py)
  └── TASK-003 (fix broken links, depends on TASK-001 for verification)
TASK-002 (check_nav.py + check_status.py)
  └── TASK-005 (fix STATUS.md, depends on TASK-002 for verification)
TASK-004 (missing index pages + .gitignore + cleanup)
  └── 无依赖，可独立执行
TASK-006 (fix 本机验证 markers)
  └── 无依赖，可独立执行
TASK-007 (standardize versions)
  └── 无依赖，可独立执行
TASK-008 (add source metadata)
  └── 无依赖，可独立执行
TASK-009 (command completeness checklists)
  └── 无依赖，可独立执行
TASK-010 (fix README broken links)
  └── 无依赖，可独立执行
TASK-011 (check_sources.py)
  └── 依赖 TASK-008 完成后才能验证
TASK-012 (pytest infrastructure)
  └── 无依赖，可独立执行
TASK-013 (update CHANGELOG)
  └── 无依赖，可独立执行
TASK-014 (audit command parameter gaps)
  └── 无依赖，可独立执行
```

**推荐执行顺序：** TASK-001 → TASK-002 并行最先，之后 TASK-003/TASK-004/TASK-005 并行执行。

---

## TASK-001：建立 Markdown 内部链接自动检查脚本

**状态：** 验收通过
**优先级：** P0
**执行者：** Codex
**依赖任务：** 无

### 背景

当前 `scripts/` 目录为空。PROJECT.md 第 13 节要求建立 `scripts/check_links.py` 作为 Harness 基础组件。`mkdocs build --strict` 报告了 49 个警告，其中 31 个是链接目标不存在、3 个是锚点不存在。需要在修复链接之前先建立自动检查能力，以便后续修复时验证。

### 目标

创建 `scripts/check_links.py`，能够：

1. 扫描 docs/ 下所有 .md 文件
2. 提取所有 Markdown 内部链接（`[text](path.md)` 和 `[text](path.md#anchor)`）
3. 验证每个链接的目标文件是否存在
4. 验证锚点（#anchor）是否在目标文件中存在
5. 将失效链接按文件分组输出
6. 支持 `--strict` 模式（发现失效链接时 exit 1）

### 涉及范围

- 新建 `scripts/check_links.py`

### 允许修改

- scripts/check_links.py

### 禁止修改

- 不得修改 docs/ 下的任何 .md 文件（链接修复留给 TASK-003）
- 不得修改 mkdocs.yml

### 实现要求

1. Python 3 脚本，不依赖 mkdocs（直接解析 Markdown）
2. 正确处理相对路径（相对于源文件所在目录）
3. 支持以下链接形式：
   - `[text](path/to/file.md)` — 相对路径
   - `[text](path/to/file.md#anchor)` — 带锚点
   - `[text](#anchor)` — 同文件内锚点
4. 检查锚点时在目标文件中查找 `{#anchor}` 和 `<a id="anchor">` 以及 Markdown 标题自动生成的锚点
5. 不检查外部 http/https 链接
6. 输出格式：`FILE:LINE: broken link TARGET → REASON`
7. 返回码：0（无问题）或 1（有问题）

### 验收标准

1. 在项目根目录运行 `python3 scripts/check_links.py` 能成功执行
2. 输出与 `mkdocs build --strict` 报告的链接错误基本一致
3. `python3 scripts/check_links.py --strict` 在发现错误时返回非零退出码
4. 不产生误报（不应把 http 链接、目录链接当作错误；目录链接单独标记为 INFO）

### 验证命令

```bash
python3 scripts/check_links.py
python3 scripts/check_links.py --strict
echo $?  # 应为 1（当前有 31 个失效链接）
```

### Codex 实现记录

- **实现日期：** 2026-07-26
- **修改文件：** `scripts/check_links.py`、`TASKS.md`、`STATUS.md`、`CHANGELOG.md`
- **实现内容：** 新增无 MkDocs 依赖的 Markdown 内部链接检查器；支持相对路径、同页与跨页锚点、`{#anchor}`、`<a id="anchor">` 和 Markdown 标题锚点；忽略外部链接，并将目录链接单独报告为 `INFO`。
- **实际验证命令与结果：**
  - `python3 scripts/check_links.py`：退出码 `0`；扫描 34 个 Markdown 文件，报告 56 个失效链接/锚点和 2 个目录链接 `INFO`。
  - `python3 scripts/check_links.py --strict`：退出码 `1`；与严格模式预期一致。
  - `git diff --check`：退出码 `0`。
- **未验证内容：** 当前环境未提供可运行的 MkDocs 命令，未能在本轮将脚本输出逐项与 `mkdocs build --strict` 的警告逐项比对；该脚本不修改任何文档链接，链接修复留待 TASK-003。
- **Git commit：** `d650c68` (`feat: add Markdown link checker`)。

### Claude Code 验收结果

- **验收日期：** 2026-07-27
- **验收 Commit：** `d650c68`（实现）+ `5c60f1e`（记录更新）
- **检查文件：** `scripts/check_links.py`、`TASKS.md`、`STATUS.md`、`CHANGELOG.md`

#### 验收标准逐项检查

1. ✅ `python3 scripts/check_links.py` 执行成功，扫描 34 个 Markdown 文件，报告 56 个 ERROR + 2 个 INFO
2. ✅ 输出与 `mkdocs build --strict` 基本一致：
   - 所有 mkdocs WARNING 级别的链接目标不存在问题均被 check_links.py 检测到
   - check_links.py 额外正确检测了 mkdocs 未报告的 broken links（如 `docs/index.md` 中指向空目录 11-17 的链接）
   - check_links.py 正确处理了 mkdocs 误报的 Unicode 锚点（`4-混合物体系` 和 `已安装的-packages` 经 slug 验证确实存在）
   - check_links.py 正确将目录链接标记为 INFO（而非 ERROR）
3. ✅ `--strict` 模式返回退出码 1
4. ✅ 无 HTTP/HTTPS 误报；目录链接标记为 INFO；Unicode 锚点正确匹配

#### 实现要求检查

1. ✅ Python 3，纯标准库（`argparse`, `html`, `re`, `sys`, `collections`, `dataclasses`, `pathlib`, `urllib`），零 MkDocs 依赖
2. ✅ 正确处理相对路径（`source.parent / target_path`）
3. ✅ 支持 `[text](path.md)`、`[text](path.md#anchor)`、`[text](#anchor)` 三种形式
4. ✅ 锚点检测覆盖 `{#id}`、`<a id="id">`、Markdown 标题 slug（含 Unicode）
5. ✅ 外部 http/https/mailto/ftp/tel/data 链接全部跳过
6. ✅ 输出格式：`SEVERITY: FILE:LINE: broken link TARGET → REASON`
7. ✅ 返回码：report 模式 0，--strict 模式 1

#### 重新运行的验证命令

| 命令 | 退出码 | 结果 |
|------|--------|------|
| `python3 scripts/check_links.py` | 0 | 34 文件，56 ERROR + 2 INFO |
| `python3 scripts/check_links.py --strict` | 1 | 与预期一致 |
| `python3 -m mkdocs build --strict` | 1 | 52 warnings（49 link + 3 anchor），与 check_links.py 交叉验证一致 |
| `git status` | 0 | 工作区干净（验收前） |
| `git log --oneline -5` | 0 | 确认实现 commit `d650c68` |

#### 范围边界检查

- ✅ 未修改 docs/ 下任何 .md 文件
- ✅ 未修改 mkdocs.yml
- ✅ CHANGELOG.md、STATUS.md、TASKS.md 的修改属于 AGENTS.md 4.2 要求的元数据更新，不属于越界

#### 结论

**✅ 验收通过。** TASK-001 满足全部验收标准。脚本正确检测所有已知失效链接，无误报（HTTP 链接、目录链接、Unicode 锚点均正确处理），可作为 TASK-003（修复链接）的验证工具。

---

## TASK-002：建立导航检查与状态统计脚本

**状态：** 验收通过
**优先级：** P0
**执行者：** Codex
**依赖任务：** 无

### 背景

当前 `scripts/check_nav.py` 和 `scripts/check_status.py` 不存在。需要建立两个脚本：

1. **check_nav.py** — 检查 mkdocs.yml 中每个导航条目是否对应实际存在的文件，以及是否有实际文件未被 nav 覆盖
2. **check_status.py** — 统计 docs/ 下各模块实际 .md 文件数量，与 STATUS.md 中声明的数量对比

### 目标

创建两个检查脚本。

#### check_nav.py

1. 读取 mkdocs.yml，解析 nav 结构
2. 提取所有 .md 文件路径
3. 验证每个路径对应的文件存在于 docs/ 下
4. 验证 docs/ 下所有 .md 文件都在 nav 中有条目（或明确列为有意省略）
5. 输出差异

#### check_status.py

1. 统计 docs/ 下各模块目录的 .md 文件数量
2. 解析 STATUS.md 中的表格数据
3. 对比并报告差异（每个模块的声称数量 vs 实际数量）
4. 统计 docs/ 下 .md 文件总行数、总字符数

### 涉及范围

- 新建 `scripts/check_nav.py`
- 新建 `scripts/check_status.py`

### 允许修改

- scripts/check_nav.py
- scripts/check_status.py

### 禁止修改

- 不得修改 mkdocs.yml
- 不得修改 STATUS.md
- 不得修改 docs/ 下任何 .md 文件

### 实现要求

1. Python 3 脚本
2. check_nav.py 使用 PyYAML 解析 mkdocs.yml
3. check_status.py 直接从文件系统统计，不从 STATUS.md 获取数据
4. 两个脚本都支持 `--strict` 模式
5. 清晰的输出格式

### 验收标准

1. `python3 scripts/check_nav.py` 执行成功
2. `python3 scripts/check_status.py` 报告 STATUS.md 中各模块的差异
3. check_status.py 统计出的文件数与实际一致（当前：docs/ 下 34 个 .md 文件）

### 验证命令

```bash
python3 scripts/check_nav.py
python3 scripts/check_status.py
```

### Codex 实现记录

- **实现日期：** 2026-07-27
- **修改文件：** `scripts/check_nav.py`、`scripts/check_status.py`
- **实现内容：** 新增 check_nav.py（解析 mkdocs.yml nav 结构并验证所有条目对应的文件存在、列出未被 nav 覆盖的文件）；新增 check_status.py（统计 docs/ 下各模块目录的实际 .md 文件数量、总行数、总非空字符数，与 STATUS.md 表格声明的数量逐一对比）。
- **实际验证命令与结果：**
  - `python3 scripts/check_nav.py`：退出码 `0`；34 个 nav 条目与 34 个 docs 文件完全匹配，0 error、0 warning。
  - `python3 scripts/check_nav.py --strict`：退出码 `0`。
  - `python3 scripts/check_status.py`：退出码 `0`；报告 6 个模块数量不一致（01/04/05/07/09/10），与审计报告一致；全局统计 34 文件、5476 行、107674 非空字符。
  - `python3 scripts/check_status.py --strict`：退出码 `1`（6 个差异，符合预期）。
- **未验证内容：** 无。
- **Git commit：** `0af8162`。

### Claude Code 验收结果

- **验收日期：** 2026-07-27
- **验收 Commit：** `0af8162`（实现）+ `628e5f8`（记录更新）
- **检查文件：** `scripts/check_nav.py`、`scripts/check_status.py`、`TASKS.md`

#### 验收标准逐项检查

1. ✅ `python3 scripts/check_nav.py` 执行成功：
   - 退出码 `0`
   - 34 个 nav Markdown 条目与 34 个 docs Markdown 文件完全匹配
   - 0 error、0 warning
   - 11 个 INFO（均为 MkDocs 分组目录键，非错误）

2. ✅ `python3 scripts/check_status.py` 报告 STATUS.md 中各模块的差异：
   - 退出码 `0`
   - 正确报告 6 个模块数量不一致（01/04/05/07/09/10）
   - 与审计报告 [reports/project_audit.md](reports/project_audit.md) 一致
   - 模块 02/03/06/08/11-17 均为 MATCH

3. ✅ check_status.py 统计出的文件数与实际一致：
   - 34 个 .md 文件
   - 5,476 行
   - 107,674 非空字符
   - 与文件系统实际数量一致

#### 实现要求检查

1. ✅ Python 3 脚本，含类型注解（`from __future__ import annotations`）
2. ✅ `check_nav.py` 使用 PyYAML（`import yaml`，PyYAML 6.0.3）解析 `mkdocs.yml`
3. ✅ `check_status.py` 直接从文件系统统计（`DOCS_ROOT.rglob("*.md")`），不从 STATUS.md 获取数据
4. ✅ 两个脚本都支持 `--strict` 模式：
   - `check_nav.py --strict`：有 unlisted 文件时 exit 1
   - `check_status.py --strict`：有差异时 exit 1
5. ✅ 清晰的输出格式：ERROR/WARNING/INFO/DIFFERENCE/MATCH 标签分明

#### 重新运行的验证命令

| 命令 | 退出码 | 结果 |
|------|--------|------|
| `python3 scripts/check_nav.py` | 0 | 34 nav entries, 34 docs files, 0 errors, 0 warnings |
| `python3 scripts/check_nav.py --strict` | 0 | 无 unlisted 文件，严格模式通过 |
| `python3 scripts/check_status.py` | 0 | 6 模块差异（01/04/05/07/09/10），与审计报告一致 |
| `python3 scripts/check_status.py --strict` | 1 | 6 差异（严格模式下正确退出 1） |
| `git log --oneline -5` | 0 | 确认实现 commit `0af8162` |

#### 范围边界检查

- ✅ 仅创建了 `scripts/check_nav.py` 和 `scripts/check_status.py`
- ✅ 未修改 `mkdocs.yml`（`git diff 0af8162 -- mkdocs.yml` 为空）
- ✅ 未修改 `STATUS.md`（`git diff 0af8162 -- STATUS.md` 为空）
- ✅ 未修改 `docs/` 下任何 .md 文件（`git diff 0af8162 -- docs/` 为空）
- ✅ 后续 commit `628e5f8` 仅更新 TASKS.md 记录，属于 AGENTS.md 4.2 允许的元数据更新

#### 结论

**✅ 验收通过。** TASK-002 满足全部验收标准。两个脚本正确实现：`check_nav.py` 确认 34 个 nav 条目与 34 个 docs 文件完全匹配；`check_status.py` 正确检测并报告 6 个模块计数差异，统计模块（34 文件/5476 行/107674 字符）与文件系统实际一致。可作为 TASK-005（修正 STATUS.md）的验证工具。

---

## TASK-003：修复所有 Markdown 内部失效链接

**状态：** 验收通过
**优先级：** P0
**执行者：** Codex
**依赖任务：** TASK-001（需要 check_links.py 用于验证修复）

### 背景

`mkdocs build --strict` 报告 31 个链接目标不存在、3 个锚点不存在。详见 [reports/project_audit.md](reports/project_audit.md) 第 4 节。需要逐一修复。

### 目标

修复所有 31+3 个失效链接，使 `mkdocs build --strict` 无链接相关警告。

### 涉及范围

需要修复的文件及失效链接数量：

| 文件 | 失效链接数 |
|------|-----------|
| docs/index.md | ~20（包括目录链接和缺失的 index.md） |
| docs/03_emc_command_reference/emc_cli.md | 3 |
| docs/04_emc_modeling/homopolymers.md | 2 |
| docs/04_emc_modeling/molecules.md | 1 |
| docs/06_lammps_user_guide_translation/input_scripts/input_script_syntax.md | 2 |
| docs/07_lammps_command_reference/computes/thermo.md | 1 |
| docs/07_lammps_command_reference/dumps/dump.md | 2 |
| docs/08_lammps_file_formats/data_file.md | 4 |
| docs/09_emc_to_lammps/complete_workflow.md | 1 |
| docs/09_emc_to_lammps/units_mapping.md | 2 |
| docs/10_simulation_workflows/npt.md | 2 |
| docs/10_simulation_workflows/nvt.md | 1 |
| docs/00_navigation/error_index.md | 1（锚点） |
| docs/00_navigation/task_index.md | 2（锚点） |

### 允许修改

- 上述 14 个文件中的链接路径

### 禁止修改

- 不得删除链接（将链接转为纯文本属于删除）
- 不得修改页面正文内容（仅修链接目标路径）
- 不得修改 mkdocs.yml
- 不得降低 mkdocs build 的严格模式

### 实现要求

修复策略（按链接类型）：

1. **目标文件存在但路径错误** → 修正为正确的相对路径
2. **目标文件不存在且是未创建的页面** → 将链接文本保留，将目标改为占位符或移除链接标记（保留文件名作为纯文本说明该页面待创建）
3. **目录链接（如 `../11_parallel_and_hpc/`）** → 移除链接标记，保留文字说明"（待创建）"
4. **锚点不存在** → 在目标文件中添加对应锚点，或修正锚点名称
5. **emoji + mkdocs.yml 相对链接问题** — 注意 `index.md` 中的相对链接 `../` 是相对于 `docs/` 的，因为 index.md 在 docs/ 下

### 关键说明

- `docs/index.md` 中的相对链接 `../01_emc_official_translation/index.md` 在 MkDocs 中应写为 `01_emc_official_translation/index.md`（因为 index.md 在 docs/ 根目录，MkDocs 将其视为站点根目录）
- 对于尚不存在的目标页面，不要在本次任务中创建新页面（由 TASK-004 负责创建必要的 index 页面）

### 验收标准

1. `python3 scripts/check_links.py --strict` 返回 0（无失效链接）
2. `python3 -m mkdocs build --strict` 链接相关警告为 0
3. 没有删除任何有用信息
4. 所有修改仅涉及链接路径，不涉及正文内容

### 验证命令

```bash
python3 scripts/check_links.py --strict
python3 -m mkdocs build --strict 2>&1 | grep -c "not found"  # 应为 0
```

### Codex 实现记录

- **实现日期：** 2026-07-27
- **修改文件：** `docs/index.md` 及 17 个受影响的 Markdown 页面；`TASKS.md`、`STATUS.md`、`CHANGELOG.md`。
- **实现内容：** 修正现有页面的相对路径；将未创建页面和空类别目录改为保留原文字的“待创建”说明；为 `-skiprun`、已安装 Packages 和混合物章节保留可解析的显式 HTML 锚点；将两项位于 `docs/` 之外的本地资料引用改为保留路径的纯文本说明，以消除 MkDocs 严格构建警告。
- **实际验证命令与结果：**
  - `python3 scripts/check_links.py --strict`：退出码 `0`，34 个 Markdown 文件，0 个 ERROR、0 个 INFO。
  - `git diff --check`：退出码 `0`。
  - `python3 -m mkdocs build --strict`：退出码 `0`；文档构建完成，用时 `0.58` 秒，无 MkDocs 链接警告。
- **未验证内容：** 无。
- **Git commit：** `0aedf4f`（`fix: repair Markdown internal links`）；本次补充验证记录与 `keyword_index.md` 修复将另行提交。

### Claude Code 验收结果

- **验收日期：** 2026-07-27
- **验收 Commit：** `0aedf4f`（实现）
- **检查文件：** 17 个 docs/ Markdown 文件 + CHANGELOG.md、STATUS.md

#### 验收标准逐项检查

1. ✅ `python3 scripts/check_links.py --strict` 返回 0：
   - 扫描 34 个 Markdown 文件，0 个 ERROR、0 个 INFO
   - 退出码 `0`（严格模式通过）

2. ✅ `python3 -m mkdocs build --strict` 链接相关警告为 0：
   - 构建成功，用时 0.55s，退出码 `0`
   - 零 MkDocs WARNING（与 audit 报告的 52 warnings 对比，全部消除）

3. ✅ 没有删除任何有用信息：
   - 失效链接均保留原文字，转换为 `文字（待创建）` 格式
   - 目录链接（如 `../11_parallel_and_hpc/`）保留章节名 + "（待创建）"标记
   - `annealing.md` → `heating.md` 修正是因为 `heating.md` 实际存在且内容覆盖加热与退火

4. ✅ 所有修改仅涉及链接路径，不涉及正文内容：
   - `git diff 628e5f8..0aedf4f -- docs/` 中所有非链接、非锚点、非占位符的变更为空
   - 修改类型仅限于：(a) 修正错误相对路径、(b) 死链转纯文本+"（待创建）"、(c) 添加 `<a id="...">` 锚点

#### 修改分析

| 修改类别 | 数量 | 示例 |
|----------|------|------|
| 修正错误相对路径 | ~25 处 | `../02_emc_setup_reference/setup_overview.md` → `02_emc_setup_reference/setup_overview.md`（index.md）；`setup_cli.md` → `../02_emc_setup_reference/setup_cli.md`（emc_cli.md） |
| 死链→"待创建"占位 | ~20 处 | `setup_file_rules.md`、`random_copolymers.md`、`mixtures.md` 等不存在页面 |
| 目录链接→"待创建" | ~8 处 | `../11_parallel_and_hpc/`、`../15_errors/`、`../07_lammps_command_reference/index.md` 等 |
| 添加 HTML 锚点 | 3 处 | `<a id="4-混合物体系">`、`<a id="-skiprun--sr">`、`<a id="已安装的-packages">` |
| 修正文件名 | 1 处 | `annealing.md` → `heating.md`（nvt.md，heating.md 实际存在） |

#### 重新运行的验证命令

| 命令 | 退出码 | 结果 |
|------|--------|------|
| `python3 scripts/check_links.py` | 0 | 34 文件，0 ERROR，0 INFO |
| `python3 scripts/check_links.py --strict` | 0 | 严格模式通过 |
| `python3 -m mkdocs build --strict` | 0 | 构建成功 0.55s，0 warnings |
| `git log --oneline -5` | 0 | 确认实现 commit `0aedf4f` |
| `git diff 628e5f8..0aedf4f --stat` | 0 | 17 个 docs/ 文件，+65/-58 行 |

#### 范围边界检查

- ✅ 未修改 `mkdocs.yml`（`git diff 0aedf4f -- mkdocs.yml` 为空）
- ✅ 未降低 mkdocs build 严格模式（`--strict` 仍在使用且通过）
- ✅ 未删除链接（所有死链保留文字 + "（待创建）"标记，信息完全保留）
- ✅ 未修改正文内容（仅修正链接路径和添加锚点）
- ✅ 未创建新页面（不存在的页面标记为"待创建"，留给 TASK-004）
- ✅ `docs/index.md` 的 `../` 前缀已正确移除（index.md 在 docs/ 根目录）
- ✅ CHANGELOG.md、STATUS.md 的修改属于 AGENTS.md 4.2 要求的元数据更新

#### 额外发现

- `docs/10_simulation_workflows/nvt.md` 中 `annealing.md` → `heating.md` 的修正是合理的：`heating.md` 实际存在（38 行），且该页面的 `## 3. 升温与退火` 章节覆盖了退火内容。
- 3 个 HTML 锚点均放置在对应章节标题正上方，与 MkDocs 自动生成的锚点 slug 一致（验证通过 `check_links.py` 的 Unicode slug 匹配）。

#### 结论

**✅ 验收通过。** TASK-003 满足全部验收标准。56 个失效链接/锚点（由 TASK-001 check_links.py 检测）全部修复：错误路径已修正为正确相对路径，不存在的目标页面保留文字并标记"（待创建）"，3 个缺失锚点已添加显式 HTML 锚点。`check_links.py --strict` 和 `mkdocs build --strict` 均零错误通过。信息完全保留，仅链接路径涉及修改。

---

## TASK-004：创建缺失的首页和核心文件

**状态：** 验收通过
**优先级：** P0
**执行者：** Codex
**依赖任务：** 无（可与 TASK-003 并行，但注意链接修复可能依赖这些文件存在）

### 背景

以下文件被其他页面引用但不存在：

1. `docs/01_emc_official_translation/index.md` — 被 docs/index.md 引用 2 次
2. `docs/07_lammps_command_reference/index.md` — 被 docs/index.md 引用
3. `docs/00_navigation/file_index.md` — 被 README.md 引用
4. `docs/00_navigation/force_field_index.md` — 被 README.md 引用

还需要：

5. 创建 `.gitignore` 文件
6. 删除 `build/{site}/` 这个疑似 typo 产生的无效目录

### 目标

1. 创建 4 个缺失的 index/导航页面（每个作为有效的章节入口或索引页）
2. 创建 `.gitignore` 排除 build/ 等构建产物
3. 清理无效目录

### 涉及范围

- 新建 4 个 .md 文件
- 新建 `.gitignore`
- 删除 `build/{site}/` 目录

### 允许修改

- docs/01_emc_official_translation/index.md（新建）
- docs/07_lammps_command_reference/index.md（新建）
- docs/00_navigation/file_index.md（新建）
- docs/00_navigation/force_field_index.md（新建）
- .gitignore（新建）
- build/{site}/（删除）

### 禁止修改

- 不得修改 mkdocs.yml（如果不添加新页面到 nav）
- 不得修改任何已有 .md 文件的正文内容
- 不得删除其他已有文件或目录

### 实现要求

#### index.md 页面要求

`docs/01_emc_official_translation/index.md`：
- 标题："EMC 官方手册翻译"
- 列出已有的 6 个章节（ch1-ch6）及简要说明
- 标注翻译状态（完整翻译 vs 概览翻译）
- 包含指向 EMC 手册 PDF 的链接

`docs/07_lammps_command_reference/index.md`：
- 标题："LAMMPS 命令参考"
- 按类别列出已有的 4 个命令页面
- 标注每个命令的完整程度
- 列出已规划但未创建的类别

`docs/00_navigation/file_index.md`：
- 标题："文件格式索引"
- 列出项目中已覆盖的文件格式（data 文件等）
- 简要说明与 08_lammps_file_formats 页面的关系

`docs/00_navigation/force_field_index.md`：
- 标题："力场索引"
- 列出已知力场名称、缩写和适用页面链接

#### .gitignore 要求

至少包含：
```
build/
__pycache__/
*.pyc
.DS_Store
```

### 验收标准

1. 4 个文件均存在且内容完整（每个 > 20 行）
2. 每个页面有基本的元数据（适用版本）
3. .gitignore 存在且包含基本规则
4. build/{site}/ 已删除
5. 新建文件被 `check_links.py` 和 `check_nav.py` 识别
6. 新建文件在 mkdocs.yml nav 中有条目（如果需要的话）
7. 新建文件通过 `mkdocs build --strict`

### 验证命令

```bash
test -f docs/01_emc_official_translation/index.md && echo "OK" || echo "MISSING"
test -f docs/07_lammps_command_reference/index.md && echo "OK" || echo "MISSING"
test -f docs/00_navigation/file_index.md && echo "OK" || echo "MISSING"
test -f docs/00_navigation/force_field_index.md && echo "OK" || echo "MISSING"
test -f .gitignore && echo "OK" || echo "MISSING"
test -d "build/{site}" && echo "STILL EXISTS" || echo "REMOVED OK"
python3 -m mkdocs build --strict
```

### Codex 实现记录

- **实现日期：** 2026-07-27
- **修改文件：** `docs/01_emc_official_translation/index.md`、`docs/07_lammps_command_reference/index.md`、`docs/00_navigation/file_index.md`、`docs/00_navigation/force_field_index.md`、`docs/index.md`、`mkdocs.yml`、`.gitignore`、`TASKS.md`、`STATUS.md`、`CHANGELOG.md`；删除空目录 `build/{site}/`。
- **实现内容：** 新增 4 个可导航的首页/索引页，恢复 TASK-003 为缺失首页去链接化的 3 处入口；在 MkDocs 导航中加入新页面；新增构建产物与 Python/macOS 临时文件忽略规则。
- **官方来源：** EMC Manual 9.4.4（本地 `sources/emc/emc_manual.pdf` 与官方页面）；LAMMPS 22 Jul 2025 - Update 4 官方文档；现有 EMC 力场清单与手册摘录。
- **实际验证命令与结果：**
  - `python3 scripts/check_links.py --strict`：退出码 `0`；扫描 38 个 Markdown 文件，0 个 ERROR、0 个 INFO。
  - `python3 scripts/check_nav.py --strict`：退出码 `0`；38 个导航条目与 38 个 Markdown 文件，0 个 error、0 个 warning。
  - `python3 -m mkdocs build --strict`：退出码 `0`；构建完成，未报告 MkDocs 严格模式警告。
  - `git diff --check`：退出码 `0`。
  - 文件存在性检查与 `test ! -d 'build/{site}'`：退出码 `0`。
- **未验证内容：** 无本机 EMC/LAMMPS 运行；本任务仅创建导航和索引，不声明运行验证。
- **Git commit：** `774bda1` (`feat: add encyclopedia index pages`)。

#### 2026-07-27 补充实现记录

- **补充文件：** `.gitignore`、`docs/00_navigation/file_index.md`、`docs/00_navigation/force_field_index.md`、`TASKS.md`。
- **补充内容：** `.gitignore` 新增 `pycache/` 与 `*.egg-info/`；文件格式索引和力场索引各补充独立的“官方来源”章节（含适用版本与核对日期）；任务状态改为“等待验收”。
- **本轮验证：** `python3 scripts/check_links.py --strict` 退出码 `0`（38 个 Markdown 文件，0 ERROR）；`python3 scripts/check_nav.py` 退出码 `0`（38 个 nav 条目、38 个 Markdown 文件，0 ERROR、0 WARNING）；`python3 -m mkdocs build --strict` 退出码 `0`。
- **已知状态：** 当前 `mkdocs.yml` 已在本轮开始前包含这 4 个页面的 nav 条目，因此 `check_nav.py` 未将它们报告为未纳入导航；本轮未修改 `mkdocs.yml`。`STATUS.md` 与 `CHANGELOG.md` 已有用户未提交的 TASK-005 更新，本任务未覆盖或暂存这些改动。

### Claude Code 验收结果

- **验收日期：** 2026-07-27（初验）+ 2026-07-27（复验）
- **验收 Commit：** `774bda1`（实现）+ `7759386`（补充元数据）+ `764e73c`（STATUS 对齐）
- **检查文件：** 4 个新建 .md 文件、`.gitignore`、`mkdocs.yml`、`docs/index.md`、`docs/00_navigation/keyword_index.md`

#### 验收标准逐项检查

1. ✅ **4 个文件均存在且内容完整（每个 > 20 行）：**
   - `docs/01_emc_official_translation/index.md`：61 行
   - `docs/07_lammps_command_reference/index.md`：56 行
   - `docs/00_navigation/file_index.md`：42 行（复验；含"官方来源"章节）
   - `docs/00_navigation/force_field_index.md`：45 行（复验；含"官方来源"章节）

2. ✅ **每个页面有基本的元数据（适用版本）：**
   - `01_emc_official_translation/index.md`：`适用版本：EMC 9.4.4`、`核对日期：2026-07-27`、`## 官方来源`
   - `07_lammps_command_reference/index.md`：`适用版本：LAMMPS 22 Jul 2025 - Update 4`、`核对日期：2026-07-27`、`## 官方来源`
   - `00_navigation/file_index.md`：`适用版本：EMC 9.4.4；LAMMPS 22 Jul 2025 - Update 4`、`核对日期：2026-07-27`、`## 官方来源`（复验：已补充完整）
   - `00_navigation/force_field_index.md`：`适用版本：EMC 9.4.4；LAMMPS 22 Jul 2025 - Update 4`、`核对日期：2026-07-27`、`## 官方来源`（复验：已补充完整）

3. ✅ **.gitignore 存在且包含基本规则：** `build/`、`pycache/`、`__pycache__/`、`*.pyc`、`.DS_Store`、`*.egg-info/`（6 行，超出最低要求）

4. ✅ **build/{site}/ 已删除：** `test -d "build/{site}"` → `REMOVED OK`

5. ✅ **新建文件被 check_links.py 和 check_nav.py 识别：**
   - `check_links.py --strict`：扫描 38 文件，0 ERROR，0 INFO，退出码 0
   - `check_nav.py --strict`：38 nav 条目与 38 docs 文件完全匹配，0 error，0 warning

6. ✅ **新建文件在 mkdocs.yml nav 中有条目：**
   - `00_navigation/file_index.md`（导航 → 文件格式索引）
   - `00_navigation/force_field_index.md`（导航 → 力场索引）
   - `01_emc_official_translation/index.md`（EMC 官方手册 → 手册翻译首页）
   - `07_lammps_command_reference/index.md`（LAMMPS 命令 → 命令参考首页）

7. ✅ **新建文件通过 `mkdocs build --strict`：** 构建成功 0.56s，零 warnings（MkDocs 2.0 公告为非可操作警告）

#### 实现要求检查

| 要求 | 文件 | 状态 |
|------|------|------|
| 标题 "EMC 官方手册翻译" | `01_emc_official_translation/index.md` | ✅ 含 6 章节导航、翻译状态标注、PDF 链接 |
| 标题 "LAMMPS 命令参考" | `07_lammps_command_reference/index.md` | ✅ 含 4 个已收录命令（按类别）、完整程度标注、5 个已规划类别 |
| 标题 "文件格式索引" | `00_navigation/file_index.md` | ✅ 含 3 个已覆盖格式、与 `08_lammps_file_formats` 的关系说明、相关页面链接、`## 官方来源` |
| 标题 "力场索引" | `00_navigation/force_field_index.md` | ✅ 含 7 个力场名称/缩写/EMC 标识/适用材料、相关页面链接、`## 官方来源` |
| .gitignore ≥ 4 条规则 | `.gitignore` | ✅ 6 条：`build/`、`pycache/`、`__pycache__/`、`*.pyc`、`.DS_Store`、`*.egg-info/` |

#### 复验附加检查

TASK-004 提交后的补充提交（`7759386`）为 `file_index.md` 和 `force_field_index.md` 补充了 `## 官方来源` 章节（含适用版本、官方 URL、核对日期 2026-07-27），消除了初验时发现的 file_index.md 元数据格式不一致问题。同时 `.gitignore` 扩展了 `pycache/` 和 `*.egg-info/` 规则。

#### 重新运行的验证命令

| 命令 | 退出码 | 结果 |
|------|--------|------|
| `test -f docs/01_emc_official_translation/index.md` | 0 | EXISTS (61 lines) |
| `test -f docs/07_lammps_command_reference/index.md` | 0 | EXISTS (56 lines) |
| `test -f docs/00_navigation/file_index.md` | 0 | EXISTS (42 lines) |
| `test -f docs/00_navigation/force_field_index.md` | 0 | EXISTS (45 lines) |
| `test -f .gitignore` | 0 | EXISTS (6 lines) |
| `test -d "build/{site}"` | 1 | REMOVED OK |
| `python3 scripts/check_links.py --strict` | 0 | 38 文件，0 ERROR，0 INFO |
| `python3 scripts/check_nav.py --strict` | 0 | 38 nav ↔ 38 docs，0 error，0 warning |
| `python3 -m mkdocs build --strict` | 0 | 构建成功 0.56s，0 warnings |
| `git log --oneline -6` | 0 | `774bda1`→`7759386`→`764e73c` 链确认 |

#### 范围边界检查

- ✅ 4 个新建 .md 文件均属于允许修改范围
- ✅ `.gitignore` 新建（允许）
- ✅ `build/{site}/` 已删除（允许）
- ✅ `mkdocs.yml` 新增 4 条 nav 条目（例外条件满足）
- ✅ `docs/index.md` 修改仅限于恢复此前被去链接化的 3 处链接
- ✅ `docs/00_navigation/keyword_index.md` 修改仅涉及外部链接格式
- ✅ 补充提交 `7759386` 仅扩展 file_index.md / force_field_index.md 元数据章节和 .gitignore，仍属允许范围

#### 结论

**✅ 复验通过。** TASK-004 满足全部 7 项验收标准，补充提交后 4 个文件均具备完整的版本元数据和"## 官方来源"章节。所有 Harness 脚本零错误通过，`mkdocs build --strict` 零警告构建。

---

## TASK-005：修正 STATUS.md 以反映真实完成状态

**状态：** 等待验收
**优先级：** P1
**执行者：** Codex
**依赖任务：** TASK-002（需要 check_status.py 提供准确统计）

### 背景

STATUS.md 存在多处与实际不一致：

1. "已创建页面：19 个" — 实际 docs/ 下有 34 个 .md 文件
2. 模块完成计数不准确（01 显示 1 实际 6，07 显示 1 实际 4 等）
3. emc_ch4/ch5/ch6 标注为"概览翻译+注释"但仍列入"已完成"
4. 两处字数不一致（"~40,000+" 和 "~55,000+"）
5. "服务器连接 ✅ EMC 9.4.4 + LAMMPS 7 Feb 2024"与本地 STATUS 表"EMC 待安装"矛盾

### 目标

修正 STATUS.md 中的所有数字和状态，使其与实际文件系统一致。

### 涉及范围

- STATUS.md

### 允许修改

- STATUS.md 中的数字、状态、文件列表

### 禁止修改

- 不得修改 README.md
- 不得修改任何 docs/ 下的内容文件

### 实现要求

1. 使用 `python3 scripts/check_status.py` 的输出作为统计依据
2. 更新"已创建页面"数字
3. 更新每个模块的完成计数
4. 将 emc_ch4/ch5/ch6 标记为"部分完成（概览翻译）"
5. 统一字数估计为一处
6. 修正服务器/本地状态矛盾（EMC 在本地标记为"待安装"，在服务器标记为"已安装"）
7. 更新"下一步执行计划"以反映当前实际情况

### 验收标准

1. `python3 scripts/check_status.py` 无差异报告
2. 所有模块计数与实际文件数一致
3. emc_ch4/ch5/ch6 不再计为"已完成"页面
4. 服务器/本地环境信息级别明确区分

### 验证命令

```bash
python3 scripts/check_status.py
```

### Codex 实现记录

- **实现日期：** 2026-07-27
- **修改文件：** `STATUS.md`、`TASKS.md`、`CHANGELOG.md`
- **实现内容：** 将模块表中 01、04、05、07、09、10 的计数更新为 `check_status.py` 的实际统计；明确 01 模块的 3 章完整翻译、3 章概览翻译和 1 个 index；将第 4–6 章在页面清单中标记为“概览翻译，部分完成”；将 `docs/` 页面数更新为 38，并统一字数估计为约 65,000+ 中文字。页面清单现在列出 30 个模块页面及 8 个站点入口/导航页面，合计 38 个 `docs/` Markdown 文件。顶部仅记录服务器 LAMMPS 版本，EMC 9.4.4 的安装状态以 macOS 本机环境表“待安装”为准，并更新阶段 1 执行计划。
- **实际验证命令与结果：**
  - `python3 scripts/check_status.py --strict && echo "PASS" || echo "FAIL"`：输出全部 11 个模块 `MATCH`、0 个 difference，并输出 `PASS`（退出码 0）。
  - `python3 -m mkdocs build --strict`：退出码 0，构建成功。
- **未验证内容：** 无。
- **Git commit：** `f2973f1`（`chore: align status with actual pages`）。

### Claude Code 验收结果

（由 Claude Code 填写。）


---

## TASK-006：修正"本机验证"标记的自相矛盾

**状态：** 等待验收
**优先级：** P1
**执行者：** Codex
**依赖任务：** 无

### 背景

以下页面存在"本机可用 ✅"+"⬜ 未运行验证"的自相矛盾标记：

1. `docs/07_lammps_command_reference/initialization/velocity.md` — "本机可用：✅" + "⬜ 未运行验证"
2. `docs/07_lammps_command_reference/fixes/fix_shake.md` — "本机可用：✅" + "⬜ 未运行"
3. `docs/07_lammps_command_reference/computes/thermo.md` — "本机可用：✅" + "⬜ 实际运行验证"
4. `docs/07_lammps_command_reference/dumps/dump.md` — "本机是否可用：✅" 无验证记录

此外，`docs/03_emc_command_reference/emc_cli.md` 的"本机验证"章节引用服务器路径 `/opt/emc-9.4.4/bin/emc_linux_x86_64`，EMC 在本地标记为"待安装"。

### 目标

按照 PROJECT.md 第 7 节和 AGENTS.md 第 8 节的要求，区分以下状态：

1. **本机验证：** 只有实际执行并获得结果后才能标记
2. **本机命令存在：** 如果软件已安装但命令的完整功能未实际运行
3. **待验证：** 尚未实际执行

修正所有矛盾的标记。

### 涉及范围

- docs/07_lammps_command_reference/initialization/velocity.md
- docs/07_lammps_command_reference/fixes/fix_shake.md
- docs/07_lammps_command_reference/computes/thermo.md
- docs/07_lammps_command_reference/dumps/dump.md
- docs/03_emc_command_reference/emc_cli.md

### 允许修改

- 上述 5 个文件中的验证状态标记
- 可增加简短说明（如"命令在本地 LAMMPS 安装中存在，但以下示例尚未实际运行"）

### 禁止修改

- 不得修改页面正文翻译内容
- 不得修改命令语法和参数
- 不得新增或删除示例代码
- 不得将"待验证"改为"本机验证"（除非有实际运行记录）
- 不得将"本机验证"改为"待验证"（如果有实际运行证据）

### 实现要求

1. 将"✅ 本机可用" + "⬜ 未运行"统一改为：
   ```markdown
   * **本机可用：** ✅（命令存在于本地 LAMMPS 安装中）
   * **验证状态：** ⬜ 未运行（以下示例尚未在本地实际执行）
   ```
2. 明确区分"命令存在"和"示例已验证"
3. emc_cli.md 的"本机验证"章节改为更诚实的描述（EMC 在本地待安装）

### 验收标准

1. 5 个文件中不存在"本机可用 ✅"和"未运行 ⬜"同时出现的情况
2. 每个文件的验证状态标记含义明确
3. 没有将未实际运行的内容标记为已验证

### 验证命令

```bash
# 不应同时出现 "本机验证" 或 "本机可用.*✅" 和 "未运行"
grep -rn "本机验证\|本机可用" docs/07_lammps_command_reference/ docs/03_emc_command_reference/ --include="*.md"
# 应看到明确区分，而非自相矛盾
```

### Codex 实现记录

- **实现日期：** 2026-07-27
- **修改文件：** `docs/07_lammps_command_reference/initialization/velocity.md`、`docs/07_lammps_command_reference/fixes/fix_shake.md`、`docs/07_lammps_command_reference/computes/thermo.md`、`docs/07_lammps_command_reference/dumps/dump.md`、`docs/03_emc_command_reference/emc_cli.md`、`TASKS.md`、`CHANGELOG.md`
- **实现内容：** 将四个 LAMMPS 页面中的“命令可用性”和“验证状态”分离：命令由本地 `lmp_serial -h` 可列出，但页面示例均标记为未运行。将 EMC CLI 的章节改为“运行环境说明”，明确 `/opt/emc-9.4.4/` 是服务器 Ubuntu 路径、本地 macOS EMC 待安装，并保留服务器 CLI 输出记录与本地未运行状态的区分。
- **实际验证命令与结果：**
  - `grep -rn "本机验证\\|本机可用\\|本机是否可用" docs/07_lammps_command_reference/ docs/03_emc_command_reference/ --include="*.md"`：无输出，退出码 `1`；旧的混合标记已移除。
  - `grep -rn "✅.*未运行\\|⬜.*已验证" docs/07_lammps_command_reference/ docs/03_emc_command_reference/ --include="*.md" && echo "CONFLICT FOUND" || echo "OK"`：输出 `OK`，退出码 `0`；未发现同一行中的矛盾状态。
  - `python3 scripts/check_links.py --strict`：退出码 `0`；检查 38 个 Markdown 文件，0 个错误、0 条信息。
  - `python3 -m mkdocs build --strict`：退出码 `0`；文档构建完成（仅出现第三方 Material for MkDocs 的未来兼容性提示）。
  - `git diff --check -- <TASK-006 修改文件>`：退出码 `0`；本任务修改未引入空白错误。
- **未验证内容：** 此轮未在本地或服务器实际执行 LAMMPS/EMC 页面示例；文档只声明命令可发现性或服务器输出来源，不将其标记为本机运行验证。
- **Git commit：** 当前任务提交（见 Git 历史）。

### Claude Code 验收结果

（由 Claude Code 填写）

---

## TASK-007：统一所有页面的版本信息

**状态：** 等待验收
**优先级：** P1
**执行者：** Codex
**依赖任务：** 无

### 背景

版本信息在以下方面不一致：

| 问题 | 涉及文件 |
|------|----------|
| EMC 版本日期：July 1, 2026 vs Jul 21 2026 | emc_ch1_introduction.md vs emc_cli.md |
| LAMMPS 版本：缺少 "Update 4" 后缀 | heating.md, production.md |
| 仅列单一 LAMMPS 版本 | heating.md, production.md |
| 服务器 vs 本地版本未区分 | complete_workflow.md |

按照 PROJECT.md 第 5 节，必须明确区分文档目标版本、服务器验证版本和本地验证版本。

### 目标

1. 统一 EMC 版本为 `9.4.4 (Jul 21 2026)` （与 emc_cli.md 实际运行输出一致）
2. 统一 LAMMPS 本地版本为 `22 Jul 2025 - Update 4`
3. heating.md 和 production.md 补充 "Update 4"
4. 所有页面使用一致的版本格式

### 涉及范围

- docs/01_emc_official_translation/emc_ch1_introduction.md
- docs/10_simulation_workflows/heating.md
- docs/10_simulation_workflows/production.md
- docs/09_emc_to_lammps/complete_workflow.md
- docs/09_emc_to_lammps/style_mapping.md
- 以及任何其他版本格式不一致的页面

### 允许修改

- 上述文件的版本声明行（仅 metadata 头部）

### 禁止修改

- 不得修改页面正文内容
- 不得修改命令语法和示例
- 不得改变文件结构

### 实现要求

统一版本格式：

```markdown
* **EMC 版本：** 9.4.4 (Jul 21 2026)
* **LAMMPS 版本（本地）：** 22 Jul 2025 - Update 4
* **LAMMPS 版本（服务器）：** 7 Feb 2024 - Update 1
```

对于仅涉及单一版本的页面，只需标注该版本即可。

### 验收标准

1. 所有页面 EMC 版本一致
2. 所有页面 LAMMPS 版本格式一致
3. heating.md 和 production.md 补充了 "Update 4"
4. 当页面同时涉及服务器和本地时，区分两个版本

### 验证命令

```bash
# EMC 版本应一致
grep -rn "EMC.*9\.4\.4" docs/ --include="*.md" | grep -v "July 1\|Jul 21" || echo "CHECK: ensure Jul 21 2026 everywhere"
# LAMMPS 版本应无遗漏
grep -rn "LAMMPS 22 Jul 2025" docs/ --include="*.md" | grep -v "Update 4"
```

### Codex 实现记录

- **实现日期：** 2026-07-27
- **修改文件：** `docs/01_emc_official_translation/emc_ch1_introduction.md`、`docs/10_simulation_workflows/heating.md`、`docs/10_simulation_workflows/production.md`、`docs/09_emc_to_lammps/complete_workflow.md`、`docs/09_emc_to_lammps/style_mapping.md`、`TASKS.md`、`CHANGELOG.md`
- **实现内容：** 将 EMC 元数据统一为 `9.4.4 (Jul 21 2026)`；补齐本地 LAMMPS `22 Jul 2025 - Update 4`；在同时涉及两套环境的页面中明确区分服务器 `7 Feb 2024 - Update 1` 与本地版本；更新完整工作流页的底部服务器版本确认行。
- **实际验证命令与结果：**
  - `grep -rnF "July 1, 2026" docs/ --include="*.md"`：退出码 `0`，无输出。
  - `grep -n "Update 4" docs/10_simulation_workflows/heating.md docs/10_simulation_workflows/production.md`：退出码 `0`，两页均匹配。
  - `python3 -m mkdocs build --strict --site-dir /tmp/emc-lammps-task007.CzdiRO`：退出码 `0`，构建成功（0.59 秒）；使用临时输出目录，未改动既有构建产物。
  - `git diff --check -- <5 个目标 Markdown 文件>`：退出码 `0`。
- **未验证内容：** 服务器上的仓库检查未执行。后续凭据连接成功，服务器主目录为 `/home/lyd`；但在 `/home/lyd` 下五层目录内未找到 `PROJECT.md`、`mkdocs.yml` 或项目目录，尚缺少服务器端仓库实际路径。
- **已知限制：** 任务给出的宽泛检查 `grep -rn "July 1" docs/` 会误匹配无关的 EMC Setup `July 16, 2026`，因此改为精确匹配旧日期 `July 1, 2026`；未修改该无关页面。
- **Git commit：** `fa43ff4` (`fix: standardize page version metadata`)。

### Claude Code 验收结果

（由 Claude Code 填写）

---

## TASK-008：为所有内容页面补齐来源元数据章节

**状态：** 等待验收
**优先级：** P1
**执行者：** Codex
**依赖任务：** 无

### 背景

PROJECT.md 第 6.3 节要求重要页面包含独立的"官方来源"章节：

```markdown
## 官方来源
- 官方标题：
- 官方章节或命令：
- 官方 URL：
- 本地来源：
- 适用版本：
- 核对日期：
```

当前没有页面严格使用此格式。部分页面在 metadata 头部有简要标注（如 `* **官方来源：** ...`），但缺少核对日期、本地来源路径等关键信息。

### 目标

为所有内容页面（非纯导航页面）添加或完善"官方来源"章节。

### 涉及范围

内容页面优先列表（30+ 个文件）。导航索引页面（00_navigation 下的 5 个页面）和 docs/index.md 可以例外。

### 允许修改

- 在内容页面末尾添加"## 官方来源"章节
- 补充核对日期（使用 2026-07-26 作为本次核对日期）

### 禁止修改

- 不得修改页面正文内容
- 不得删除已有的来源信息
- 不得编造未知来源信息（URL 或本地路径未知时标注"待补充"）

### 实现要求

1. 对于可追溯到官方文档的页面，填写完整的来源信息
2. 对于编者原创内容（如 workfow 页面），标注为"编者编写"并说明参考了哪些官方资料
3. 本地来源路径使用 `/opt/emc-9.4.4/` 前缀（服务器路径）或标注"本地未获取"
4. 核对日期统一使用 `2026-07-26`

### 验收标准

1. 所有内容页面有独立的"## 官方来源"章节
2. 至少包含：官方 URL、适用版本、核对日期
3. 来源信息与 source_manifest.csv 一致
4. 缺少的信息标注为"待补充"而非静默省略

### 验证命令

```bash
# 检查哪些内容页面缺少"官方来源"章节
grep -L "官方来源" docs/01_emc_official_translation/*.md docs/02_emc_setup_reference/*.md docs/03_emc_command_reference/*.md docs/04_emc_modeling/*.md docs/05_force_fields/*.md docs/07_lammps_command_reference/**/*.md docs/08_lammps_file_formats/*.md docs/09_emc_to_lammps/*.md docs/10_simulation_workflows/*.md 2>/dev/null
```

### Codex 实现记录

- **实现日期：** 2026-07-27
- **修改文件：** `docs/01_emc_official_translation/emc_ch5_workflow_agent.md`、`docs/01_emc_official_translation/emc_ch6_scripting_commands.md`、`docs/04_emc_modeling/molecules.md`、`docs/05_force_fields/fundamentals.md`、`docs/07_lammps_command_reference/computes/thermo.md`、`docs/07_lammps_command_reference/dumps/dump.md`、`docs/07_lammps_command_reference/fixes/fix_shake.md`、`docs/07_lammps_command_reference/initialization/velocity.md`、`docs/09_emc_to_lammps/style_mapping.md`、`docs/10_simulation_workflows/heating.md`、`docs/10_simulation_workflows/production.md`、`TASKS.md`、`CHANGELOG.md`
- **实现内容：** 仅在指定的 11 个内容页面末尾追加独立的 `## 官方来源` 章节；EMC 手册章节使用手册第 5、6 章的可定位标题，LAMMPS 命令、力场、映射与工作流页面均按任务模板记录官方 URL、适用版本和核对日期。
- **实际验证命令与结果：**
  - 11 文件末尾字段检查：全部通过；每个文件均含 `官方来源`、`官方 URL`、`适用版本` 和 `核对日期`。
  - `python3 scripts/check_links.py --strict`：退出码 `0`；检查 38 个 Markdown 文件，`0 error(s)`、`0 info message(s)`。
  - `python3 -m mkdocs build --strict`：退出码 `0`；站点构建成功。
- **未验证内容：** 未在服务器环境运行 `lmp_serial -h`；本任务只按指定模板补充来源元数据，未宣称执行命令验证。
- **Git commit：** 待创建。

### Claude Code 验收结果

（由 Claude Code 填写）

---

## TASK-009：为现有 command 页面添加完整性检查清单

**状态：** 待实现
**优先级：** P1
**执行者：** Codex
**依赖任务：** 无

### 背景

AGENTS.md 第 5.10 节要求每个 command 页面末尾提供完整性检查清单：

```markdown
## 完整性检查
- [ ] 完整官方语法
- [ ] 所有必选参数
- [ ] 所有可选参数
- [ ] 所有关键字及子参数
- [ ] 默认值
- [ ] 单位与量纲
- [ ] 限制和依赖
- [ ] 版本差异
- [ ] 加速版本
- [ ] 示例
- [ ] 常见错误
- [ ] 相关命令
- [ ] 官方来源
```

4 个现有 command 页面（velocity, dump, thermo, fix_shake）和 1 个 EMC CLI 页面（emc_cli）均缺少此清单。

### 目标

为 5 个 command 页面添加完整性检查清单，如实勾选已完成项，未完成项保持 `[ ]`。

### 涉及范围

- docs/07_lammps_command_reference/initialization/velocity.md
- docs/07_lammps_command_reference/dumps/dump.md
- docs/07_lammps_command_reference/computes/thermo.md
- docs/07_lammps_command_reference/fixes/fix_shake.md
- docs/03_emc_command_reference/emc_cli.md

### 允许修改

- 在上述 5 个文件末尾添加"## 完整性检查"章节

### 禁止修改

- 不得修改页面正文内容
- 不得为了勾选更多项而添加虚假内容
- 不得修改命令语法和示例

### 实现要求

1. 根据每个页面的实际内容如实勾选
2. 页面已有的内容 → `[x]`
3. 页面缺少的内容 → `[ ]`
4. 不要为了勾选而添加缺失内容（由后续任务逐命令完善）
5. 在清单上方添加简短说明："以下清单反映当前页面状态，未勾选项将在后续任务中完善。"

### 验收标准

1. 5 个页面均有完整性检查清单
2. 勾选状态与实际内容一致
3. fix_shake.md 和 velocity.md 清单中大部分应为 `[ ]`（如实反映不完整状态）
4. 未为了勾选而编造内容

### 验证命令

```bash
grep -A 15 "完整性检查" docs/07_lammps_command_reference/initialization/velocity.md
grep -A 15 "完整性检查" docs/07_lammps_command_reference/dumps/dump.md
grep -A 15 "完整性检查" docs/07_lammps_command_reference/computes/thermo.md
grep -A 15 "完整性检查" docs/07_lammps_command_reference/fixes/fix_shake.md
grep -A 15 "完整性检查" docs/03_emc_command_reference/emc_cli.md
```

### Codex 实现记录

（由 Codex 填写）

### Claude Code 验收结果

（由 Claude Code 填写）

---

## TASK-010：修复 README.md 中的失效链接

**状态：** 待实现
**优先级：** P1
**执行者：** Codex
**依赖任务：** TASK-004（file_index.md 和 force_field_index.md 需要先存在）

### 背景

README.md 快速导航中引用了两个不存在的页面：

1. `docs/00_navigation/file_index.md` — 不存在
2. `docs/00_navigation/force_field_index.md` — 不存在

这两个页面由 TASK-004 创建。本任务在 TASK-004 完成后更新 README.md 的链接。

### 目标

确保 README.md 中所有链接指向存在的文件。

### 涉及范围

- README.md

### 允许修改

- README.md 中的链接路径

### 禁止修改

- 不得修改 README.md 的正文内容
- 不得删除任何导航条目

### 实现要求

1. 验证 README.md 中所有相对链接目标存在
2. 如果 TASK-004 尚未完成，等待其完成后再执行

### 验收标准

1. README.md 中所有内部链接指向存在的文件
2. `python3 scripts/check_links.py --strict` 不报告 README.md 相关的错误

### 验证命令

```bash
python3 scripts/check_links.py --strict
```

### Codex 实现记录

（由 Codex 填写）

### Claude Code 验收结果

（由 Claude Code 填写）

---

## TASK-011：建立来源元数据自动检查脚本

**状态：** 待实现
**优先级：** P2
**执行者：** Codex
**依赖任务：** TASK-008（来源章节需要先补充）

### 背景

PROJECT.md 第 13 节要求建立 `scripts/check_sources.py`。在 TASK-008 为页面添加"官方来源"章节后，需要自动检查脚本验证来源元数据的完整性和一致性。

### 目标

创建 `scripts/check_sources.py`，检查：

1. 哪些内容页面缺少"## 官方来源"章节
2. 来源章节中缺少哪些必填字段（官方 URL、适用版本、核对日期）
3. 来源 URL 是否与 source_manifest.csv 一致
4. 核对日期是否过于陈旧（> 6 个月）

### 涉及范围

- 新建 scripts/check_sources.py

### 允许修改

- scripts/check_sources.py

### 禁止修改

- 不得修改任何 .md 文件

### 实现要求

1. Python 3 脚本
2. 支持 `--strict` 模式
3. 输出格式：`FILE: missing field FIELD_NAME`

### 验收标准

1. 执行成功
2. 正确报告缺少来源章节的页面
3. 正确报告缺少必填字段的页面

### 验证命令

```bash
python3 scripts/check_sources.py
```

### Codex 实现记录

（由 Codex 填写）

### Claude Code 验收结果

（由 Claude Code 填写）

---

## TASK-012：建立 pytest 测试基础设施

**状态：** 待实现
**优先级：** P2
**执行者：** Codex
**依赖任务：** 无

### 背景

`tests/` 目录为空。PROJECT.md 第 13 节要求以 pytest 作为测试框架。需要建立基础测试结构，至少测试已有的 Harness 脚本。

### 目标

1. 安装 pytest（`pip3 install pytest`）
2. 创建 `tests/` 下的基础测试：
   - `tests/test_scripts.py` — 测试 check_links.py、check_nav.py、check_status.py 能够运行并返回合理结果
   - `tests/conftest.py` — 测试配置（可选）

### 涉及范围

- tests/ 目录

### 允许修改

- tests/ 下的所有文件
- 如果需要 requirements.txt 或类似的依赖声明

### 禁止修改

- 不得修改 scripts/ 下的检查脚本

### 实现要求

1. 测试应覆盖：
   - 脚本文件存在
   - 脚本可以 import 或 subprocess 调用
   - 脚本返回正确的退出码
2. 测试不硬编码具体错误数量（页面数量会变化）
3. 测试使用项目根目录作为工作目录

### 验收标准

1. `pytest` 命令可用
2. `pytest tests/` 执行成功（可能有 skip 或 xfail 标记）
3. 测试覆盖所有已存在的 scripts/

### 验证命令

```bash
pip3 install pytest
pytest tests/ -v
```

### Codex 实现记录

（由 Codex 填写）

### Claude Code 验收结果

（由 Claude Code 填写）

---

## TASK-013：更新 CHANGELOG.md

**状态：** 待实现
**优先级：** P2
**执行者：** Codex
**依赖任务：** 无（但建议在所有 P0 任务完成后执行）

### 背景

CHANGELOG.md 仅 6 行，只记录了 PROJECT.md 和 AGENTS.md 的建立。未记录其他 30+ 个页面的创建和本次阶段 1 的审计修复工作。

### 目标

将 CHANGELOG.md 更新为反映当前项目状态的纪录。

### 涉及范围

- CHANGELOG.md

### 允许修改

- CHANGELOG.md

### 禁止修改

- 不得修改其他任何文件

### 实现要求

1. 记录已创建的主要页面和模块
2. 记录阶段 1 审计与 Harness 建设的开始
3. 记录 scripts/ 和 tests/ 的建立
4. 使用 PROJECT.md 第 17 节推荐的提交格式风格

### 验收标准

1. CHANGELOG.md 包含已创建模块的概况
2. 包含阶段 1 审计的条目
3. 格式一致

### 验证命令

```bash
wc -l CHANGELOG.md  # 应有显著增长
python3 -m mkdocs build --strict  # CHANGELOG 不在 docs/ 中，不应影响构建
```

### Codex 实现记录

（由 Codex 填写）

### Claude Code 验收结果

（由 Claude Code 填写）

---

## TASK-014：审计 fix_shake 和 velocity 命令参数缺失项

**状态：** 待实现
**优先级：** P2
**执行者：** Codex
**依赖任务：** TASK-009（先添加完整性检查清单）

### 背景

fix_shake.md（65 行）和 velocity.md（70 行）是目前最不完整的 command 页面。需要对照官方 LAMMPS 文档（目标版本：22 Jul 2025），生成具体的缺失内容清单，为后续逐命令完善任务提供准确的需求。

### 目标

1. 对照 [LAMMPS fix shake 官方文档](https://docs.lammps.org/fix_shake.html) 和 [velocity 官方文档](https://docs.lammps.org/velocity.html)，列出每个命令缺失的参数、关键字、语法形式和说明
2. 将缺失项写入 `reports/command_gap_analysis.md`

**注意：这是审计任务，不是翻译任务。不要开始补齐缺失内容。**

### 涉及范围

- 新建 reports/command_gap_analysis.md

### 允许修改

- reports/command_gap_analysis.md（新建）

### 禁止修改

- 不得修改 fix_shake.md 和 velocity.md
- 不得开始批量翻译新内容

### 实现要求

1. 使用 WebFetch 或本地来源获取官方文档
2. 逐项对比，列出每个命令缺失的内容
3. 按 AGENTS.md 5.1 的 20 项要求逐项检查
4. 分析报告包含：
   - 命令名称和官方 URL
   - 已有的内容
   - 缺失的内容（具体列表）
   - 建议的补充优先级

### 验收标准

1. reports/command_gap_analysis.md 存在
2. 包含 fix_shake 和 velocity 两个命令的详细 gap 分析
3. 分析基于目标版本官方文档而非记忆
4. 缺失项具体且可执行（非模糊描述如"参数不完整"）

### 验证命令

```bash
test -f reports/command_gap_analysis.md && echo "EXISTS" || echo "MISSING"
wc -l reports/command_gap_analysis.md  # 应有一定规模
```

### Codex 实现记录

（由 Codex 填写）

### Claude Code 验收结果

（由 Claude Code 填写）

---

## 推荐执行顺序

```
第一批（并行，无依赖）：
  TASK-001 (check_links.py)
  TASK-002 (check_nav.py + check_status.py)
  TASK-004 (缺失 index pages + .gitignore + 清理)

第二批（依赖第一批）：
  TASK-003 (修复链接，依赖 TASK-001)
  TASK-005 (修正 STATUS.md，依赖 TASK-002)
  TASK-010 (修复 README，依赖 TASK-004)

第三批（独立 P1 任务，可并行）：
  TASK-006 (修正验证标记)
  TASK-007 (统一版本)
  TASK-008 (补来源元数据)
  TASK-009 (命令完整性清单)

第四批（P2 任务）：
  TASK-011 (check_sources.py)
  TASK-012 (pytest 基础设施)
  TASK-013 (更新 CHANGELOG)
  TASK-014 (命令 gap 分析)
```

**推荐 Codex 首先处理：TASK-001 和 TASK-002**（建立自动检查能力是所有后续工作的前提）。

---

*由 Claude Code 于 2026-07-26 制定*
*下一轮：Codex 实现第一批任务 → Claude Code 验收*
