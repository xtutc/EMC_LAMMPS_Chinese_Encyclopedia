# EMC 与 LAMMPS 中文百科全书

## Ubuntu/macOS 安装、命令、语法、建模、模拟与排错

> **非官方中文翻译与注释版** — 仅供个人学习、实验室内部使用和科研查阅。
> 保留原作者、软件名称、官方章节号和官方链接。

---

## 关于本项目

本项目是 **Enhanced Monte Carlo (EMC)** 和 **Large-scale Atomic/Molecular Massively Parallel Simulator (LAMMPS)** 的系统性中文百科全书。包含：

1. EMC 官方手册的系统中文翻译与注释版
2. LAMMPS 用户指南和核心命令参考的系统中文翻译与注释版
3. EMC → LAMMPS 完整实践百科
4. 可按照命令、关键字、错误、任务和文件格式查询的知识库

### 软件定义

- **EMC** (Enhanced Monte Carlo)：由 Pieter J. in 't Veld 开发的分子与介观体系构建软件
- **LAMMPS** (Large-scale Atomic/Molecular Massively Parallel Simulator)：经典分子动力学模拟器

### 适用版本

| 软件 | 版本 |
|------|------|
| EMC | 9.4.4 |
| LAMMPS | 22 Jul 2025 - Update 4 (Homebrew) |
| 平台 | macOS (Apple Silicon) / Ubuntu |

---

## 快速导航

- [如何使用本百科](docs/00_navigation/how_to_use.md)
- [按任务查询](docs/00_navigation/task_index.md)
- [按命令查询](docs/00_navigation/command_index.md)
- [按关键字查询](docs/00_navigation/keyword_index.md)
- [按错误查询](docs/00_navigation/error_index.md)
- [按文件格式查询](docs/00_navigation/file_index.md)
- [按力场查询](docs/00_navigation/force_field_index.md)

---

## 目录结构

```
EMC_LAMMPS_Chinese_Encyclopedia/
├── README.md                   ← 本文件
├── STATUS.md                   ← 完成状态
├── CHANGELOG.md                ← 变更记录
├── docs/                       ← 文档主体
│   ├── 00_navigation/          ← 导航与索引
│   ├── 01_emc_official_translation/  ← EMC 官方手册翻译
│   ├── 02_emc_setup_reference/       ← EMC Setup 参考
│   ├── 03_emc_command_reference/     ← EMC 命令参考
│   ├── 04_emc_modeling/              ← EMC 建模教程
│   ├── 05_force_fields/              ← 力场参考
│   ├── 06_lammps_user_guide_translation/ ← LAMMPS 用户指南翻译
│   ├── 07_lammps_command_reference/  ← LAMMPS 命令参考
│   ├── 08_lammps_file_formats/       ← LAMMPS 文件格式
│   ├── 09_emc_to_lammps/             ← EMC→LAMMPS 工作流
│   ├── 10_simulation_workflows/      ← 模拟流程
│   ├── 11_parallel_and_hpc/          ← 并行与HPC
│   ├── 12_visualization/             ← 可视化
│   ├── 13_analysis/                  ← 数据分析
│   ├── 14_examples/                  ← 示例
│   ├── 15_errors/                    ← 错误排查
│   ├── 16_glossary/                  ← 术语表
│   └── 17_references/                ← 参考文献
├── examples/                   ← 所有示例文件
├── scripts/                    ← 脚本
├── tests/                      ← 测试
├── reports/                    ← 报告
├── sources/                    ← 官方来源文件
└── build/                      ← 构建输出 (HTML, PDF)
```

---

## 翻译规则

1. 使用正式、准确的中文技术表达
2. 英文命令、关键字、变量和文件名不翻译
3. 首次出现的专业术语保留英文
4. 不修改原公式和参数值
5. 明确区分官方原文和编者注释
   - **编者注：** 为注释标记
   - **本机验证：** 为验证标记
   - **警告：** 为风险提示
   - **版本说明：** 为版本差异

---

## 版权声明

- 原始文档版权归原作者所有
- 本翻译仅供个人学习、实验室内部和科研使用
- 保留所有原始版权和许可证说明
- 本翻译不是官方中文版本

---

*生成日期：2026-07-26*
*适用 EMC 版本：9.4.4 | LAMMPS 版本：22 Jul 2025 - Update 4*
