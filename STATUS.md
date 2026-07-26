# 百科完成状态

> 最后更新：2026-07-27

> 阶段 1 Harness：TASK-001 ~ TASK-004 ✅；TASK-005 等待验收，下一项为 TASK-006。

## 总体完成率

| 模块 | 总章节/命令数 | 已完成 | 完成率 | 下一任务 |
|------|------------:|------:|------:|---------|
| 01 EMC 官方手册翻译 | ~80 节 | 7（3 章完整翻译、3 章概览翻译、1 个 index） | 9% | 细化第 4–6 章并继续逐章翻译 |
| 02 EMC Setup 参考 | ~12 节 | 2 (总览, CLI) | 16% | 翻译 setup_file_rules |
| 03 EMC 命令参考 | ~8 节 | 1 (emc_cli) | 12% | 翻译 emc_file_workflow |
| 04 EMC 建模 | ~10 节 | 2 (molecules, homopolymers) | 20% | 扩展其他建模主题 |
| 05 力场 | ~12 节 | 2 (inventory, fundamentals) | 16% | 补充力场样式与映射 |
| 06 LAMMPS 用户指南 | ~8 节 | 2 (CLI, Input) | 25% | 翻译 errors |
| 07 LAMMPS 命令参考 | ~75+ 命令 | 5（4 个命令、1 个 index） | 6% | 核对现有命令完整性并扩展命令覆盖 |
| 08 LAMMPS 文件格式 | ~6 节 | 1 (data_file) | 16% | 翻译 input_script |
| 09 EMC→LAMMPS | ~7 节 | 3 (workflow, units, style) | 42% | 补充其余工作流主题 |
| 10 模拟流程 | ~9 节 | 5 (min, heating, nvt, npt, production) | 56% | 补充其余模拟流程 |
| 11-17 其余 | ~30 节 | 0 | 0% | 建立索引 |

### 总体进度

- **已创建 Markdown 页面：** 38 个（`docs/` 下实际 `.md` 文件数）
- **内容字数（估计）：** 约 65,000+ 中文字（依据 112,988 个非空字符估算）
- **EMC 手册 PDF：** ✅ 已获取 (906KB)
- **EMC 手册 TOC：** ✅ 已映射
- **服务器验证环境：** LAMMPS 7 Feb 2024；EMC 9.4.4 的安装状态以本机环境表记录的“待安装”为准。

### 已登记模块页面（30 个文件）

以下计数对应模块目录 `01`–`10` 的实际 Markdown 文件数；“已登记”不等同于“完整翻译”或“本机验证”。

| # | 文件 | 内容 |
|---|------|------|
| 1 | [docs/01_emc_official_translation/index.md](docs/01_emc_official_translation/index.md) | EMC 手册翻译首页（新增于 TASK-004） |
| 2 | [docs/01_emc_official_translation/emc_ch1_introduction.md](docs/01_emc_official_translation/emc_ch1_introduction.md) | EMC 手册第 1 章完整翻译 |
| 3 | [docs/01_emc_official_translation/emc_ch2_methodology.md](docs/01_emc_official_translation/emc_ch2_methodology.md) | EMC 手册第 2 章完整翻译 |
| 4 | [docs/01_emc_official_translation/emc_ch3_program_structure.md](docs/01_emc_official_translation/emc_ch3_program_structure.md) | EMC 手册第 3 章完整翻译 |
| 5 | [docs/01_emc_official_translation/emc_ch4_simulation_setup.md](docs/01_emc_official_translation/emc_ch4_simulation_setup.md) | EMC 手册第 4 章（概览翻译，部分完成） |
| 6 | [docs/01_emc_official_translation/emc_ch5_workflow_agent.md](docs/01_emc_official_translation/emc_ch5_workflow_agent.md) | EMC 手册第 5 章（概览翻译，部分完成） |
| 7 | [docs/01_emc_official_translation/emc_ch6_scripting_commands.md](docs/01_emc_official_translation/emc_ch6_scripting_commands.md) | EMC 手册第 6 章（概览翻译，部分完成） |
| 8 | [docs/02_emc_setup_reference/setup_overview.md](docs/02_emc_setup_reference/setup_overview.md) | EMC Setup 总览 |
| 9 | [docs/02_emc_setup_reference/setup_cli.md](docs/02_emc_setup_reference/setup_cli.md) | EMC Setup CLI 完整参考 |
| 10 | [docs/03_emc_command_reference/emc_cli.md](docs/03_emc_command_reference/emc_cli.md) | EMC 主程序命令行 |
| 11 | [docs/04_emc_modeling/molecules.md](docs/04_emc_modeling/molecules.md) | EMC 小分子建模 |
| 12 | [docs/04_emc_modeling/homopolymers.md](docs/04_emc_modeling/homopolymers.md) | EMC 均聚物建模 |
| 13 | [docs/05_force_fields/emc_force_field_inventory.md](docs/05_force_fields/emc_force_field_inventory.md) | EMC 力场清单 |
| 14 | [docs/05_force_fields/fundamentals.md](docs/05_force_fields/fundamentals.md) | 力场基础 |
| 15 | [docs/06_lammps_user_guide_translation/running/lammps_cli_options.md](docs/06_lammps_user_guide_translation/running/lammps_cli_options.md) | LAMMPS CLI 完整参考 |
| 16 | [docs/06_lammps_user_guide_translation/input_scripts/input_script_syntax.md](docs/06_lammps_user_guide_translation/input_scripts/input_script_syntax.md) | LAMMPS 输入脚本语法 |
| 17 | [docs/07_lammps_command_reference/index.md](docs/07_lammps_command_reference/index.md) | LAMMPS 命令参考首页（新增于 TASK-004） |
| 18 | [docs/07_lammps_command_reference/dumps/dump.md](docs/07_lammps_command_reference/dumps/dump.md) | LAMMPS `dump` 命令 |
| 19 | [docs/07_lammps_command_reference/computes/thermo.md](docs/07_lammps_command_reference/computes/thermo.md) | LAMMPS `thermo` 命令 |
| 20 | [docs/07_lammps_command_reference/fixes/fix_shake.md](docs/07_lammps_command_reference/fixes/fix_shake.md) | LAMMPS `fix shake` 命令 |
| 21 | [docs/07_lammps_command_reference/initialization/velocity.md](docs/07_lammps_command_reference/initialization/velocity.md) | LAMMPS `velocity` 命令 |
| 22 | [docs/08_lammps_file_formats/data_file.md](docs/08_lammps_file_formats/data_file.md) | LAMMPS data 文件格式 |
| 23 | [docs/09_emc_to_lammps/complete_workflow.md](docs/09_emc_to_lammps/complete_workflow.md) | EMC→LAMMPS 完整工作流 |
| 24 | [docs/09_emc_to_lammps/units_mapping.md](docs/09_emc_to_lammps/units_mapping.md) | Units 系统与映射 |
| 25 | [docs/09_emc_to_lammps/style_mapping.md](docs/09_emc_to_lammps/style_mapping.md) | Style 映射表 |
| 26 | [docs/10_simulation_workflows/minimization.md](docs/10_simulation_workflows/minimization.md) | 能量最小化流程 |
| 27 | [docs/10_simulation_workflows/heating.md](docs/10_simulation_workflows/heating.md) | 升温流程 |
| 28 | [docs/10_simulation_workflows/nvt.md](docs/10_simulation_workflows/nvt.md) | NVT 平衡流程 |
| 29 | [docs/10_simulation_workflows/npt.md](docs/10_simulation_workflows/npt.md) | NPT 流程 |
| 30 | [docs/10_simulation_workflows/production.md](docs/10_simulation_workflows/production.md) | 生产模拟流程 |

### 站点入口与导航页面（8 个文件）

| 文件 | 内容 |
|------|------|
| [docs/index.md](docs/index.md) | 百科主页索引 |
| [docs/00_navigation/error_index.md](docs/00_navigation/error_index.md) | 错误信息索引 |
| [docs/00_navigation/file_index.md](docs/00_navigation/file_index.md) | 文件格式索引（新增于 TASK-004） |
| [docs/00_navigation/force_field_index.md](docs/00_navigation/force_field_index.md) | 力场索引（新增于 TASK-004） |
| [docs/00_navigation/command_index.md](docs/00_navigation/command_index.md) | 命令索引 |
| [docs/00_navigation/keyword_index.md](docs/00_navigation/keyword_index.md) | 关键字索引 |
| [docs/00_navigation/task_index.md](docs/00_navigation/task_index.md) | 任务索引 |
| [docs/00_navigation/how_to_use.md](docs/00_navigation/how_to_use.md) | 使用说明 |

**辅助文件：**
| - | [sources/source_manifest.csv](sources/source_manifest.csv) | 来源清单 |
| - | [sources/emc/emc_manual.pdf](sources/emc/emc_manual.pdf) | EMC 官方手册 (906KB) |
| - | [reports/emc_manual_toc.md](reports/emc_manual_toc.md) | EMC 手册目录映射 |
| - | [reports/emc_keyword_inventory.csv](reports/emc_keyword_inventory.csv) | EMC 关键字清单 |

### 详细完成率

#### LAMMPS 用户指南

| 章节 | 状态 |
|------|------|
| installation (CMake) | ⬜ 待翻译 |
| running (命令行) | ✅ 完成 |
| input_scripts (输入脚本) | ⬜ 待翻译 |
| input_parsing (解析规则) | ⬜ 待翻译 |
| data_file (数据文件) | ⬜ 待翻译 |
| errors (错误) | ⬜ 待翻译 |
| accelerators (加速器) | ⬜ 待翻译 |

---

## 本机环境

| 项目 | 值 |
|------|-----|
| 操作系统 | macOS 15 (Darwin 24.6.0, arm64) |
| LAMMPS 版本 | 22 Jul 2025 - Update 4 |
| LAMMPS 路径 | `/opt/homebrew/bin/lmp_serial`, `/opt/homebrew/bin/lmp_mpi` |
| EMC 版本 | 9.4.4（待安装，来源：SourceForge） |
| EMC Setup 版本 | 5.3 (emc.pl) |
| Python | 3.9.6 |
| pandoc | 可用 |
| pdflatex | 可用 |

---

## 官方来源清单

| 来源 | URL | 状态 |
|------|-----|------|
| EMC 官方网站 | https://montecarlo.sourceforge.net/emc/Welcome.html | ✅ 已获取 |
| EMC 功能说明 | https://montecarlo.sourceforge.net/emc/Features.html | ✅ 已获取 |
| EMC 手册 PDF | montecarlo.sourceforge.net/emc/Welcome_files/droppedImage.pdf | ⬜ 待下载 |
| LAMMPS 官方首页 | https://docs.lammps.org/ | ⬜ 待系统获取 |
| LAMMPS 运行选项 | https://docs.lammps.org/Run_options.html | ✅ 已参考 |
| LAMMPS 输入脚本 | https://docs.lammps.org/Commands_input.html | ⬜ 待翻译 |
| LAMMPS 解析规则 | https://docs.lammps.org/Commands_parse.html | ⬜ 待翻译 |
| LAMMPS 脚本结构 | https://docs.lammps.org/Commands_structure.html | ⬜ 待翻译 |

---

## 下一步执行计划

1. ✅ TASK-001：Markdown 内部链接检查脚本
2. ✅ TASK-002：导航检查与状态统计脚本
3. ✅ TASK-003：修复所有内部失效链接
4. ✅ TASK-004：创建缺失 index 页面与 `.gitignore`
5. ⏳ TASK-005：修正 STATUS.md（等待验收）
6. ⬜ TASK-006：修正“本机验证”标记
7. ⬜ TASK-007：统一所有页面版本信息
8. ⬜ 阶段 1 Harness 建设其余 P1/P2 任务
