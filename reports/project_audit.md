# 项目审计报告：阶段 1 — 项目审计与 Harness 建设

> **审计日期：** 2026-07-26
> **审计者：** Claude Code（项目规划者与验收者）
> **审计范围：** 整个项目，只读为主
> **下一阶段：** Codex 根据 TASKS.md 实现修复

---

## 1. Markdown 页面统计

### 1.1 根目录文件

| 文件 | 行数 | 状态 |
|------|------|------|
| README.md | 107 | 存在 |
| STATUS.md | 122 | 存在，统计数据不一致 |
| CHANGELOG.md | 7 | 存在，内容极少 |
| PROJECT.md | 743 | 存在 |
| AGENTS.md | 775 | 存在 |
| TASKS.md | 5 | 存在，仅有占位符 |
| REVIEW.md | 3 | 存在，仅有占位符 |

### 1.2 各模块 Markdown 页面统计

| 模块 | 目录 | 文档数 | 文件列表 |
|------|------|--------|----------|
| — | docs/ | 1 | index.md |
| 00 导航 | docs/00_navigation/ | 5 | how_to_use, task_index, command_index, keyword_index, error_index |
| 01 EMC 手册翻译 | docs/01_emc_official_translation/ | 6 | emc_ch1 到 emc_ch6 |
| 02 EMC Setup 参考 | docs/02_emc_setup_reference/ | 2 | setup_overview, setup_cli |
| 03 EMC 命令参考 | docs/03_emc_command_reference/ | 1 | emc_cli |
| 04 EMC 建模 | docs/04_emc_modeling/ | 2 | molecules, homopolymers |
| 05 力场参考 | docs/05_force_fields/ | 2 | fundamentals, emc_force_field_inventory |
| 06 LAMMPS 用户指南 | docs/06_lammps_user_guide_translation/ | 2 | lammps_cli_options, input_script_syntax |
| 07 LAMMPS 命令参考 | docs/07_lammps_command_reference/ | 4 | velocity, dump, thermo, fix_shake |
| 08 LAMMPS 文件格式 | docs/08_lammps_file_formats/ | 1 | data_file |
| 09 EMC→LAMMPS | docs/09_emc_to_lammps/ | 3 | complete_workflow, units_mapping, style_mapping |
| 10 模拟流程 | docs/10_simulation_workflows/ | 5 | minimization, nvt, npt, heating, production |
| 11 并行与 HPC | docs/11_parallel_and_hpc/ | 0 | **空目录** |
| 12 可视化 | docs/12_visualization/ | 0 | **空目录** |
| 13 分析 | docs/13_analysis/ | 0 | **空目录** |
| 14 示例 | docs/14_examples/ | 0 | **空目录** |
| 15 错误排查 | docs/15_errors/ | 0 | **空目录** |
| 16 术语表 | docs/16_glossary/ | 0 | **空目录** |
| 17 参考文献 | docs/17_references/ | 0 | **空目录** |

**总计：** 34 个 .md 文件位于 docs/（含 index.md），7 个根目录 .md 文件。

### 1.3 辅助文件

| 文件 | 状态 |
|------|------|
| sources/source_manifest.csv | 存在，33 条记录 |
| sources/emc/emc_manual.pdf | 存在，927KB |
| sources/emc/emc_manual.txt | 存在，747KB |
| reports/emc_manual_toc.md | 存在 |
| reports/emc_keyword_inventory.csv | 存在 |

---

## 2. STATUS.md 与实际文件不一致

### 已确认问题

| STATUS.md 声称 | 实际情况 | 严重程度 |
|----------------|----------|----------|
| "已创建页面：19 个" | docs/ 下有 34 个 .md 文件 | P2 |
| "已完成页面 (26 个文件)" | 列表包含 26 个条目，但其中 emc_ch4/ch5/ch6 标注为"概览翻译"而非完整翻译 | P1 |
| "内容字数（估计）：~40,000+" → 后改 "~55,000+" | 两处字数不一致 | P2 |
| 01 模块 "1 (TOC)" 已完成 | 实际有 6 个 .md 文件 | P1 |
| 02 模块 "2 (总览, CLI)" 已完成 | 与文件数匹配 | — |
| 03 模块 "1 (emc_cli)" 已完成 | 与文件数匹配 | — |
| 04 模块 "1 (molecules)" 已完成 | 实际有 2 个 .md 文件 | P1 |
| 05 模块 "1 (inventory)" 已完成 | 实际有 2 个 .md 文件 | P1 |
| 06 模块 "2 (CLI, Input)" | 与文件数匹配 | — |
| 07 模块 "1 (dump)" | 实际有 4 个 .md 文件 | P1 |
| 08 模块 "1 (data_file)" | 与文件数匹配 | — |
| 09 模块 "2 (workflow, units)" | 实际有 3 个 .md 文件 | P2 |
| 10 模块 "3 (min, nvt, npt)" | 实际有 5 个 .md 文件 | P2 |
| 11-17 模块 "0" | 与实际情况一致 | — |
| 已列出 emc_ch4/ch5/ch6 为已完成页面 | 这三个文件标注翻译状态为"概览翻译+注释"，不应计为已完成 | P1 |

---

## 3. mkdocs.yml 引用不存在页面

### 已确认问题

mkdocs.yml 中所有导航条目对应的文件**均实际存在**（34 个页面与 nav 中的条目一一对应）。没有引用不存在的页面。

但 mkdocs.yml 的 nav 结构并未覆盖所有实际存在的文件：

| 实际存在的文件 | mkdocs.yml 中是否存在 |
|----------------|---------------------|
| docs/00_navigation/error_index.md | ✅ |
| docs/01_emc_official_translation/emc_ch4_simulation_setup.md | ✅ |
| docs/01_emc_official_translation/emc_ch5_workflow_agent.md | ✅ |
| docs/01_emc_official_translation/emc_ch6_scripting_commands.md | ✅ |
| docs/10_simulation_workflows/heating.md | ✅ |
| docs/10_simulation_workflows/production.md | ✅ |
| docs/07_lammps_command_reference/fixes/fix_shake.md | ✅ |

所有实际存在的文件均在 mkdocs.yml 中有对应条目。

---

## 4. Markdown 内部相对链接

### 4.1 mkdocs build --strict 结果

**构建失败：** `mkdocs build --strict` 产生 **49 个警告**（严格模式下视为错误），构建中止。

### 4.2 目标文件不存在的链接（已确认问题，P0）

| 源文件 | 失效链接 | 预期目标 |
|--------|----------|----------|
| [docs/index.md](docs/index.md) | `../01_emc_official_translation/index.md` | 01_emc_official_translation/index.md **不存在** |
| [docs/index.md](docs/index.md) | `../07_lammps_command_reference/index.md` | 07_lammps_command_reference/index.md **不存在** |
| [docs/index.md](docs/index.md) | `../06_lammps_user_guide_translation/installation/` | 目录存在但无 index.md |
| [docs/index.md](docs/index.md) | `../11_parallel_and_hpc/` | 空目录 |
| [docs/index.md](docs/index.md) | `../12_visualization/` | 空目录 |
| [docs/index.md](docs/index.md) | `../13_analysis/` | 空目录 |
| [docs/index.md](docs/index.md) | `../14_examples/` | 空目录 |
| [docs/03_emc_command_reference/emc_cli.md](docs/03_emc_command_reference/emc_cli.md) | `setup_cli.md` | 应指向 `../02_emc_setup_reference/setup_cli.md` |
| [docs/03_emc_command_reference/emc_cli.md](docs/03_emc_command_reference/emc_cli.md) | `setup_file_rules.md` | 文件不存在 |
| [docs/03_emc_command_reference/emc_cli.md](docs/03_emc_command_reference/emc_cli.md) | `emc_file_workflow.md` | 文件不存在 |
| [docs/04_emc_modeling/homopolymers.md](docs/04_emc_modeling/homopolymers.md) | `random_copolymers.md` | 文件不存在 |
| [docs/04_emc_modeling/homopolymers.md](docs/04_emc_modeling/homopolymers.md) | `mixtures.md` | 文件不存在 |
| [docs/04_emc_modeling/molecules.md](docs/04_emc_modeling/molecules.md) | `mixtures.md` | 文件不存在 |
| [docs/06_lammps_user_guide_translation/input_scripts/input_script_syntax.md](docs/06_lammps_user_guide_translation/input_scripts/input_script_syntax.md) | `running/lammps_cli_options.md` | 应使用 `../running/lammps_cli_options.md` |
| [docs/06_lammps_user_guide_translation/input_scripts/input_script_syntax.md](docs/06_lammps_user_guide_translation/input_scripts/input_script_syntax.md) | `../08_lammps_file_formats/data_file.md` | 应使用 `../../08_lammps_file_formats/data_file.md` |
| [docs/07_lammps_command_reference/computes/thermo.md](docs/07_lammps_command_reference/computes/thermo.md) | `../computes/` | 链接到目录而非文件 |
| [docs/07_lammps_command_reference/dumps/dump.md](docs/07_lammps_command_reference/dumps/dump.md) | `write_dump.md` | 文件不存在 |
| [docs/07_lammps_command_reference/dumps/dump.md](docs/07_lammps_command_reference/dumps/dump.md) | `read_dump.md` | 文件不存在 |
| [docs/08_lammps_file_formats/data_file.md](docs/08_lammps_file_formats/data_file.md) | `input_scripts/input_script_syntax.md` | 路径错误 |
| [docs/08_lammps_file_formats/data_file.md](docs/08_lammps_file_formats/data_file.md) | `../../09_emc_to_lammps/file_mapping.md` | 文件不存在 |
| [docs/08_lammps_file_formats/data_file.md](docs/08_lammps_file_formats/data_file.md) | `../../09_emc_to_lammps/units_mapping.md` | 路径层级错误 |
| [docs/08_lammps_file_formats/data_file.md](docs/08_lammps_file_formats/data_file.md) | `../07_lammps_command_reference/force_fields/` | 空目录 |
| [docs/09_emc_to_lammps/complete_workflow.md](docs/09_emc_to_lammps/complete_workflow.md) | `file_mapping.md` | 文件不存在 |
| [docs/09_emc_to_lammps/units_mapping.md](docs/09_emc_to_lammps/units_mapping.md) | `force_field_mapping.md` | 文件不存在 |
| [docs/09_emc_to_lammps/units_mapping.md](docs/09_emc_to_lammps/units_mapping.md) | `../../05_force_fields/fundamentals.md` | 路径层级错误 |
| [docs/10_simulation_workflows/npt.md](docs/10_simulation_workflows/npt.md) | `nve.md` | 文件不存在 |
| [docs/10_simulation_workflows/npt.md](docs/10_simulation_workflows/npt.md) | `equilibrium_check.md` | 文件不存在 |
| [docs/10_simulation_workflows/nvt.md](docs/10_simulation_workflows/nvt.md) | `annealing.md` | 文件不存在（但 heating.md 存在） |

### 4.3 锚点不存在的链接（P1）

| 源文件 | 链接 | 问题 |
|--------|------|------|
| [docs/00_navigation/error_index.md](docs/00_navigation/error_index.md) | `lammps_cli_options.md#已安装的-packages` | 目标页面无此锚点 |
| [docs/00_navigation/task_index.md](docs/00_navigation/task_index.md) | `molecules.md#4-混合物体系` | 目标页面无此锚点 |
| [docs/00_navigation/task_index.md](docs/00_navigation/task_index.md) | `lammps_cli_options.md#-skiprun--sr` | 目标页面无此锚点 |

### 4.4 README.md 中引用的不存在的导航页面

| README 快速导航链接 | 目标文件 | 状态 |
|---------------------|----------|------|
| `docs/00_navigation/how_to_use.md` | ✅ 存在 |
| `docs/00_navigation/task_index.md` | ✅ 存在 |
| `docs/00_navigation/command_index.md` | ✅ 存在 |
| `docs/00_navigation/keyword_index.md` | ✅ 存在 |
| `docs/00_navigation/error_index.md` | ✅ 存在 |
| `docs/00_navigation/file_index.md` | ❌ **不存在** |
| `docs/00_navigation/force_field_index.md` | ❌ **不存在** |

---

## 5. 空目录与缺失首页

### 5.1 完全为空的 docs 子目录（P0/P2）

| 目录 | PROJECT.md 规划内容 | 问题 |
|------|---------------------|------|
| docs/11_parallel_and_hpc/ | 并行计算、MPI、SLURM 作业 | 空，但 index.md 和 mkdocs.yml 中未引用 |
| docs/12_visualization/ | OVITO、VMD 可视化 | 空 |
| docs/13_analysis/ | RDF、MSD、密度分布 | 空 |
| docs/14_examples/ | 验证示例 | 空 |
| docs/15_errors/ | 错误排查 | 空（error_index.md 在 00_navigation 中） |
| docs/16_glossary/ | 中英术语对照 | 空 |
| docs/17_references/ | 参考文献 | 空 |

### 5.2 部分为空的子目录（P0）

| 目录 | 状态 |
|------|------|
| docs/06_lammps_user_guide_translation/installation/ | 空 |
| docs/06_lammps_user_guide_translation/errors/ | 空 |
| docs/06_lammps_user_guide_translation/accelerators/ | 空 |
| docs/07_lammps_command_reference/force_fields/ | 空 |
| docs/07_lammps_command_reference/minimization/ | 空 |
| docs/07_lammps_command_reference/running/ | 空 |
| docs/07_lammps_command_reference/system_definition/ | 空 |
| docs/07_lammps_command_reference/variables_and_control/ | 空 |

### 5.3 缺失的模块首页（P0）

| 缺失文件 | 被引用位置 |
|----------|-----------|
| `docs/01_emc_official_translation/index.md` | docs/index.md（2 处） |
| `docs/07_lammps_command_reference/index.md` | docs/index.md |
| `docs/00_navigation/file_index.md` | README.md |
| `docs/00_navigation/force_field_index.md` | README.md |

### 5.4 其他空目录

| 目录 | 问题 |
|------|------|
| examples/ | 空目录 |
| scripts/ | 空目录 |
| tests/ | 空目录 |
| sources/lammps/ | 空目录 |
| build/{site}/ | 疑似 typo 创建的无效目录 |

---

## 6. EMC / EMC Setup / LAMMPS 版本混用

### 6.1 EMC 版本不一致（P1）

| 文件 | 版本声明 | 问题 |
|------|----------|------|
| PROJECT.md | EMC 9.4.4 | 主目标版本 |
| STATUS.md | EMC 9.4.4（待安装） | 本地未安装 |
| docs/index.md | EMC 9.4.4 (Jul 21 2026) | 日期精确 |
| docs/01_emc_official_translation/emc_ch1_introduction.md | 9.4.4 (July 1, 2026) | **日期不同：July 1 vs Jul 21** |
| docs/03_emc_command_reference/emc_cli.md | 9.4.4 (Jul 21 2026) | — |
| source_manifest.csv | EMC binary valid until Jul 1 2027 | — |

### 6.2 LAMMPS 版本不一致（P1）

| 文件 | 版本声明 |
|------|----------|
| PROJECT.md | 服务器: 7 Feb 2024 Update 1; 本地: 22 Jul 2025 Update 4 |
| STATUS.md | 本地 22 Jul 2025 - Update 4 |
| README.md | 22 Jul 2025 - Update 4 |
| docs/index.md | 7 Feb 2024 / 22 Jul 2025 |
| docs/09_emc_to_lammps/complete_workflow.md | 7 Feb 2024 / 22 Jul 2025 |
| docs/09_emc_to_lammps/style_mapping.md | 22 Jul 2025 / 7 Feb 2024 |
| docs/09_emc_to_lammps/units_mapping.md | 22 Jul 2025 - Update 4 |
| docs/10_simulation_workflows/heating.md | 22 Jul 2025（**缺少 Update 4**） |
| docs/10_simulation_workflows/production.md | 22 Jul 2025（**缺少 Update 4**） |
| docs/06_lammps_user_guide_translation/running/lammps_cli_options.md | 22 Jul 2025 - Update 4 |
| docs/08_lammps_file_formats/data_file.md | 22 Jul 2025 - Update 4 |

**主要问题：**
- heating.md 和 production.md 缺少 "Update 4" 后缀
- 服务器版本 vs 本地版本未在所有页面明确区分
- 部分页面仅列出单一版本，未区分服务器/本地

---

## 7. 页面来源、适用版本和验证状态

### 7.1 来源元数据覆盖

| 状态 | 页面数 | 说明 |
|------|--------|------|
| 有明确官方来源 | ~25 | 大部分内容页面声明了官方来源 |
| 缺少官方来源 | ~5 | navigation 页面和部分内容页面 |
| 缺少核对日期 | ~30 | **几乎所有页面都缺少核对日期** |
| 缺少本地来源路径 | ~20 | 仅 EMC 翻译章节有本地 PDF 路径 |

### 7.2 PROJECT.md 要求的来源格式

PROJECT.md 第 6.3 节要求重要页面包含：
```markdown
## 官方来源
- 官方标题：
- 官方章节或命令：
- 官方 URL：
- 本地来源：
- 适用版本：
- 核对日期：
```

**实际情况：** 没有页面严格使用此格式。大多数页面仅在前言 metadata 中简要标注，缺少独立的"官方来源"章节。

---

## 8. "本机验证" 实际运行依据

### 8.1 声称"本机验证"或"本机可用"的页面

| 页面 | 声明 | 验证记录 | 评定 |
|------|------|----------|------|
| [emc_cli.md](docs/03_emc_command_reference/emc_cli.md) | "本机验证" 章节 | 引用服务器路径 `/opt/emc-9.4.4/bin/emc_linux_x86_64` | **高风险**：服务器≠本机 |
| [data_file.md](docs/08_lammps_file_formats/data_file.md) | "本机验证：✅ read_data 命令在本地可用" | 无操作系统、退出码、执行日期 | **高风险**：证据不足 |
| [lammps_cli_options.md](docs/06_lammps_user_guide_translation/running/lammps_cli_options.md) | "✅ 通过 lmp_serial -h 验证" | 仅提及命令，无完整记录 | **高风险**：证据不足 |
| [velocity.md](docs/07_lammps_command_reference/initialization/velocity.md) | "本机可用：✅" + "⬜ 未运行验证" | **自相矛盾** | **P1**：标记冲突 |
| [fix_shake.md](docs/07_lammps_command_reference/fixes/fix_shake.md) | "本机可用：✅" + "⬜ 未运行" | **自相矛盾** | **P1**：标记冲突 |
| [dump.md](docs/07_lammps_command_reference/dumps/dump.md) | "本机是否可用：✅" | 列出了本地支持的 dump styles | **待核查** |
| [thermo.md](docs/07_lammps_command_reference/computes/thermo.md) | "本机可用：✅" + "⬜ 实际运行验证" | **自相矛盾** | **P1**：标记冲突 |
| heating.md | "✅ 官方资料翻译 \| ⬜ 未运行" | 诚实标记 | ✅ |
| production.md | 无验证状态，仅"翻译状态：完整" | 缺少验证标记 | P2 |

### 8.2 核心问题

按照 PROJECT.md 第 7.3 节，本机验证必须包含：操作系统、软件版本、执行命令、输入文件、退出状态、关键输出、验证日期。

**所有声称"本机验证"的页面均缺少完整验证记录。**

多个页面存在"本机可用 ✅" + "⬜ 未运行验证"的自相矛盾标记。按照 AGENTS.md 第 8.1 节，"只有实际执行软件并获得结果时才能写'本机验证'"。在当前本地环境 EMC 为"待安装"状态（STATUS.md）的情况下，EMC 相关页面的"本机验证"声明尤为可疑。

---

## 9. Command 页面参数覆盖率

### 9.1 LAMMPS velocity 命令（70 行）

按照 AGENTS.md 第 5 节（Command 完整性强制要求），需要覆盖全部官方参数。

| 检查项 | 状态 |
|--------|------|
| 完整官方语法 | ❌ 仅列 3 种 style（create, set, scale），缺少 zero, ramp |
| 所有必选参数 | ❌ 不完整 |
| 所有关键字及子参数 | ❌ 缺少 loop, rigid, dist, sum, mom, rot, bias, temp |
| 默认值与单位 | ❌ 未说明 |
| 限制和依赖 | ❌ 未说明 |
| 版本差异 | ❌ 无 |
| 加速版本 | ❌ 无 |
| 完整性检查清单 | ❌ 无 |
| 官方来源章节 | ❌ 仅有链接 |

### 9.2 LAMMPS dump 命令（155 行）

| 检查项 | 状态 |
|--------|------|
| 完整官方语法 | ⚠️ 部分覆盖 |
| 所有 style 变体 | ⚠️ 覆盖了 atom, custom, xyz, dcd, xtc, movie，缺少 netcdf, vt, local, grid 等 |
| dump_modify 全部选项 | ❌ 仅覆盖 7 个选项，官方有 20+ |
| 所有关键字 | ❌ 缺少 thresh, delay, format, sort, first, every, flush, maxfiles 等 |
| 版本差异 | ❌ 无 |
| 完整性检查清单 | ❌ 无 |

### 9.3 LAMMPS thermo 命令（205 行）

| 检查项 | 状态 |
|--------|------|
| 完整官方语法 | ⚠️ 基本覆盖 |
| 输出关键字列表 | ⚠️ 列了 ~30 个，官方有 100+ |
| thermo_modify 选项 | ⚠️ 列了 8 个，覆盖主要选项 |
| 版本差异 | ❌ 无 |
| 完整性检查清单 | ❌ 无 |

### 9.4 LAMMPS fix shake 命令（65 行）

| 检查项 | 状态 |
|--------|------|
| 完整语法 | ❌ 严重不完整 |
| 所有参数和子参数 | ❌ 缺少角度约束 (a), tip 约束 (t), mol 参数 |
| 默认值与容差单位 | ❌ 未说明容差的物理含义 |
| 版本差异 | ❌ 无 |
| 官方来源 | ❌ 仅有链接 |
| 完整性检查清单 | ❌ 无 |

### 9.5 EMC emc_cli 命令（263 行）

| 检查项 | 状态 |
|--------|------|
| 完整语法 | ⚠️ 覆盖了大部分选项 |
| 参数默认值 | ⚠️ 部分覆盖 |
| 版本差异 | ❌ 无 |
| EMC vs EMC Setup 混淆 | ❌ 内容混杂 |

**总结：** 所有现有 command 页面都不满足 AGENTS.md 第 5 节的完整性要求。缺少完整性检查清单（5.10 要求的 checklist）。每个 command 页面缺少覆盖全部官方参数的结构化表格。

---

## 10. scripts/ 和 tests/ 缺少的 Harness 自动检查

### 10.1 当前状态

- `scripts/` — **空目录**，零个检查脚本
- `tests/` — **空目录**，零个测试
- 没有 `.gitignore` 文件

### 10.2 需要的 Harness 检查（按 PROJECT.md 第 13 节）

| 检查 | 实现状态 | 优先级 |
|------|----------|--------|
| MkDocs 导航文件存在性检查 | ❌ scripts/check_nav.py 不存在 | P0 |
| Markdown 内部链接检查 | ❌ scripts/check_links.py 不存在 | P0 |
| 页面来源元数据检查 | ❌ scripts/check_sources.py 不存在 | P1 |
| 页面标题重复检查 | ❌ 未实现 | P2 |
| 术语一致性检查 | ❌ 未实现 | P2 |
| 示例验证状态检查 | ❌ 未实现 | P1 |
| STATUS.md 页面数量检查 | ❌ scripts/check_status.py 不存在 | P1 |
| Markdown 代码块闭合检查 | ❌ 未实现 | P2 |
| MkDocs 严格构建 | ⚠️ mkdocs build --strict 失败（49 warnings） | P0 |
| pytest 测试 | ❌ tests/ 为空 | P1 |

### 10.3 PROJECT.md 推荐的验证命令

```bash
pytest                                    # ❌ 不可用
python scripts/check_links.py             # ❌ 脚本不存在
python scripts/check_nav.py               # ❌ 脚本不存在
python scripts/check_sources.py          # ❌ 脚本不存在
python scripts/check_status.py           # ❌ 脚本不存在
mkdocs build --strict                     # ❌ 失败（49 warnings）
```

**6 条推荐命令中，5 条不可能执行，1 条执行失败。**

---

## 11. 真实运行结果

### 11.1 mkdocs build --strict

**结果：失败**
- 49 个警告（严格模式下作为错误处理）
- 47 个链接目标不存在
- 2 个锚点不存在
- 构建在生成 HTML 之前中止

### 11.2 pytest

**结果：不可用**
- tests/ 目录为空

### 11.3 检查脚本

**结果：不可用**
- scripts/ 目录为空

### 11.4 已安装的 Python 包

```
mkdocs 1.6.1
mkdocs-material 9.7.7
mkdocs-material-extensions 1.3.1
```

pytest 未安装。

---

## 12. 问题分类汇总

### 12.1 已确认问题（Confirmed）

| # | 问题 | 严重程度 |
|---|------|----------|
| C1 | mkdocs build --strict 因 49 个警告而失败 | P0 |
| C2 | 31 个 Markdown 内部链接指向不存在的目标文件 | P0 |
| C3 | 4 个页面/索引文件被引用但不存在（index.md ×2, file_index.md, force_field_index.md） | P0 |
| C4 | 8 个空子目录有结构规划但无内容（06 子目录和 07 子类别） | P0 |
| C5 | scripts/ 和 tests/ 完全为空 | P0 |
| C6 | STATUS.md 完成数量与实际文件数不匹配 | P1 |
| C7 | 3 个锚点链接指向不存在的页面内锚点 | P1 |
| C8 | EMC 版本日期在两个页面间不一致（July 1 vs Jul 21 2026） | P1 |
| C9 | heating.md 和 production.md LAMMPS 版本缺少 "Update 4" 后缀 | P1 |
| C10 | velocity.md、fix_shake.md、thermo.md "本机可用 ✅"与"⬜ 未运行验证"自相矛盾 | P1 |
| C11 | 所有"本机验证"声明均缺少 PROJECT.md 要求的完整验证记录 | P1 |
| C12 | emc_cli.md 的"本机验证"指向服务器路径而非本机 | P1 |
| C13 | fix_shake.md 极不完整（65 行），缺少 90% 以上的参数 | P1 |
| C14 | velocity.md 不完整（70 行），缺少 zero/ramp style 等 | P1 |
| C15 | 所有 command 页面缺少 AGENTS.md 5.10 要求的完整性检查清单 | P1 |
| C16 | 没有页面使用 PROJECT.md 6.3 要求的独立"官方来源"格式 | P2 |
| C17 | 没有 .gitignore 文件 | P2 |
| C18 | build/{site}/ 疑似 typo 产生的无效目录 | P2 |
| C19 | CHANGELOG.md 极其简短（仅 6 行），未记录所有已创建页面 | P2 |
| C20 | README.md 引用 file_index.md 和 force_field_index.md 但这两文件不存在 | P1 |
| C21 | sources/lammps/ 目录为空 | P2 |

### 12.2 高风险问题（High Risk）

| # | 问题 | 风险 |
|---|------|------|
| H1 | "本机验证"标记混乱 — 用户可能相信示例已在本地运行成功，实际并未运行 | 用户被误导运行可能失败的脚本 |
| H2 | version 混用 — 服务器/本地 LAMMPS 版本混用，可能导致用户使用错误语法 | 命令语法和参数在不同版本间有差异 |
| H3 | emc_cli.md 引用的 EMC 路径 `/opt/emc-9.4.4/` 为服务器路径，本地用户无法使用 | 示例不可复现 |
| H4 | 4 个 command 页面严重不完整但都未标记为"部分完成" | 用户以为已获得完整参考 |
| H5 | EMC 第 4-6 章（共 89+5+71 页原文）仅数百字概览，STATUS.md 却将其列入"已完成" | 用户误判项目进度 |

### 12.3 尚需进一步核查的问题（Needs Investigation）

| # | 问题 | 需要什么 |
|---|------|----------|
| N1 | 所有 LAMMPS 和 EMC 命令页面的参数完整性与官方文档逐项对比 | 需要获取目标版本官方文档，逐参数核对 |
| N2 | 中英文术语一致性（术语表尚不存在） | 需要建立术语表后才能检查 |
| N3 | 示例代码是否可在目标环境实际编译运行 | 需要安装 EMC 和 LAMMPS 后实际执行 |
| N4 | 代码块是否正确闭合（300+ 行的页面中可能存在问题） | 需要自动化脚本检查 |
| N5 | 页面标题是否存在重复 | 需要自动化脚本检查 |
| N6 | 力场参数和映射是否正确 | 需要对照官方力场文件核对 |
| N7 | EMC Keywords 清单（emc_keyword_inventory.csv）是否覆盖全部 EMC 命令 | 需要逐项对比 EMC 手册第 6 章 |

---

## 13. 审计结论

### 13.1 总体评定

项目处于**早期建设阶段**。基础架构（MkDocs + Material）已就位，34 个内容页面已创建，关键官方来源已收集（EMC 手册 PDF + TXT）。但工程质量基础设施（自动检查、测试、来源元数据、版本一致性）基本为零。

**最严重的问题按影响排序：**

1. **mkdocs build --strict 失败（49 warnings）** — 网站无法在严格模式下构建
2. **scripts/ 和 tests/ 完全为空** — 零自动检查能力，无法约束后续内容质量
3. **"本机验证"标记系统性问题** — 多个页面自相矛盾或缺少证据，可能误导用户

### 13.2 是否可以进入 Codex 实现阶段

**可以。** 本轮审计已识别出足够明确的修复任务。所有 P0 任务涉及明确的文件路径、固定数量的链接修复、脚本编写，不需要模糊判断。P1 任务同样有明确范围。

### 13.3 不应在本阶段进行的工作

- 大规模翻译新章节
- 重写或重新设计任何页面内容
- 重新设计 mkdocs.yml 结构
- 更换主题或技术栈

---

*审计完成时间：2026-07-26*
*由 Claude Code 执行*
