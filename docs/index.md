# EMC 与 LAMMPS 中文百科全书

> **非官方中文翻译与注释版**
>
> EMC 版本：9.4.4 | LAMMPS 版本：22 Jul 2025 / 7 Feb 2024
>
> 生成日期：2026-07-26

---

## 欢迎使用

本百科全书是 Enhanced Monte Carlo (EMC) 和 LAMMPS 分子动力学模拟器的系统性中文参考。所有内容基于官方文档翻译，并增加了中文注释、实践指导和错误排查。

---

## 快速导航

### 🔍 按需求查找

| 我想... | 去哪里 |
|---------|--------|
| 了解 EMC 是什么 | EMC 官方手册翻译（待创建） |
| 写一个 EMC Setup 文件 | [EMC Setup 参考](02_emc_setup_reference/setup_overview.md) |
| 查找 EMC 关键字含义 | [关键字索引](00_navigation/keyword_index.md) |
| 查找 LAMMPS 命令 | [命令索引](00_navigation/command_index.md) |
| 从 EMC 输出运行 LAMMPS | [EMC→LAMMPS 完整工作流](09_emc_to_lammps/complete_workflow.md) |
| 写一个最小化脚本 | [最小化流程](10_simulation_workflows/minimization.md) |
| 写一个 NVT 脚本 | [NVT 流程](10_simulation_workflows/nvt.md) |
| 写一个 NPT 脚本 | [NPT 流程](10_simulation_workflows/npt.md) |
| 选择合适的力场 | [力场清单](05_force_fields/emc_force_field_inventory.md) |
| 理解 LAMMPS 输入脚本 | [输入脚本语法](06_lammps_user_guide_translation/input_scripts/input_script_syntax.md) |
| 理解 LAMMPS 命令行 | [命令行参数](06_lammps_user_guide_translation/running/lammps_cli_options.md) |
| 理解 LAMMPS data 文件 | [data 文件格式](08_lammps_file_formats/data_file.md) |
| 排查错误 | [错误索引](00_navigation/error_index.md) |
| 了解单位和单位映射 | [单位映射](09_emc_to_lammps/units_mapping.md) |

---

## 百科结构

### 第一部分：EMC（Enhanced Monte Carlo）

| 章节 | 内容 |
|------|------|
| 01 EMC 官方手册翻译（待创建） | EMC 官方 PDF 手册的逐章中文翻译 |
| [02 EMC Setup 参考](02_emc_setup_reference/setup_overview.md) | EMC Setup (emc.pl) 的完整命令和文件格式参考 |
| [03 EMC 命令参考](03_emc_command_reference/emc_cli.md) | EMC 主程序命令行、工作流和输出文件 |
| [04 EMC 建模](04_emc_modeling/molecules.md) | 各类体系的 EMC 建模教程 |
| [05 力场参考](05_force_fields/emc_force_field_inventory.md) | EMC 支持的力场清单和 LAMMPS 映射 |

### 第二部分：LAMMPS

| 章节 | 内容 |
|------|------|
| 06 LAMMPS 用户指南翻译（待创建） | LAMMPS 官方 User Guide 的中文翻译 |
| 07 LAMMPS 命令参考（待创建） | 每个 LAMMPS 命令的完整中文参考 |
| [08 LAMMPS 文件格式](08_lammps_file_formats/data_file.md) | 输入脚本、data 文件、restart、dump 等格式说明 |

### 第三部分：实践

| 章节 | 内容 |
|------|------|
| [09 EMC→LAMMPS](09_emc_to_lammps/complete_workflow.md) | 从 EMC 构建到 LAMMPS 模拟的完整工作流 |
| [10 模拟流程](10_simulation_workflows/minimization.md) | 最小化、升温、NVT、NPT、生产模拟等标准流程 |
| 11 并行与 HPC（待创建） | MPI、OpenMP、SLURM 作业脚本 |
| 12 可视化（待创建） | OVITO、VMD 可视化指南 |
| 13 分析（待创建） | 径向分布函数、均方位移、密度分布等 |
| 14 示例（待创建） | 所有验证过的示例 |

### 第四部分：索引与工具

| 章节 | 内容 |
|------|------|
| [00 导航](00_navigation/how_to_use.md) | 任务索引、命令索引、关键字索引、错误索引 |
| 15 错误排查（待创建） | 常见错误和解决方法 |
| 16 术语表（待创建） | 中英文术语对照 |
| 17 参考文献（待创建） | 引用来源 |

---

## 快速开始

### EMC 用户的最短路径

```bash
# 1. 在服务器上，使用 EMC Setup 构建体系
perl /opt/emc-9.4.4/scripts/emc.pl \
  -field=opls-aa -density=0.997 \
  water 1 1000 water

# 2. 这将生成：
#    build/build.emc     — EMC 输入
#    build/system.data   — LAMMPS data
#    build/system.in     — LAMMPS 输入
#    build/system.params — 力场参数

# 3. 执行构建
cd build && emc -nthreads=4 build.emc

# 4. 运行 LAMMPS
lmp -in system.in -log run.log
```

### LAMMPS 用户的最短路径

```lammps
# 最小 LAMMPS 输入脚本
units           real
atom_style      full
read_data       system.data
pair_style      lj/cut/coul/long 10.0
pair_coeff      * * 0.1 3.0
kspace_style    pppm 1e-4
minimize        1e-4 1e-6 1000 10000
velocity        all create 300.0 12345
fix             1 all nvt temp 300.0 300.0 100.0
timestep        1.0
thermo          100
run             10000
```

---

## 翻译约定

| 标记 | 含义 |
|------|------|
| > **编者注：** | 编者补充的中文解释 |
| > **本机验证：** | 经过实际运行验证 |
| > **警告：** | 需要特别注意的风险 |
| > **版本说明：** | 版本间差异说明 |

- 英文命令、关键字、变量名和文件名不翻译
- 首次出现的专业术语保留英文原名
- 所有官方章节号和来源链接保留

---

## 版本信息

| 组件 | 服务器 (Ubuntu) | 本地 (macOS) |
|------|----------------|-------------|
| EMC | 9.4.4 (Jul 21 2026) | — |
| LAMMPS | 7 Feb 2024 - Update 1 | 22 Jul 2025 - Update 4 |
| EMC Setup | 5.3 | — |
