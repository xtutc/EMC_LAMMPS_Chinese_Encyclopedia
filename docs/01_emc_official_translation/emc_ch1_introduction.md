# 第 1 章：引言 (Introduction)

* **英文原题：** Chapter 1: Introduction
* **官方章节号：** 1
* **官方页码：** 1–2
* **适用 EMC 版本：** 9.4.4 (Jul 21 2026)
* **官方来源：** EMC Manual PDF (`/opt/emc-9.4.4/docs/emc.pdf`)

---

## 1.1 总体介绍 (General Introduction)

### 中文翻译

EMC（Enhanced Monte Carlo）是一个通用模拟软件包，可使用 Monte Carlo 技术构建和模拟原子级及粗粒化体系。

EMC 提供了一个灵活的环境，用于创建和操作粒子模拟的输入结构。它支持多种力场：

- **原子级力场：** Born、COMPASS、PCFF、CHARMM（c32b 和 c36a，包括 CGENFF）、OPLS（AA 和 UA，2012 和 2024 版本）以及 TraPPE。这些力场由 EMC 通过 typing 规则进行 typing。
- **粗粒化力场：** DPD、Martini（v2 和 v3）、SDK 以及胶体力场。这些力场不由 EMC typing，但 EMC 支持其参数化。

**核心功能：**

1. **结构操作：** 通过 SMILES 字符串操作分子或粗粒化结构
2. **力场 typing：** 为选定的力场自动分配原子类型
3. **构象构建：** 使用 Monte Carlo 原理构建构象
4. **输出端口：** LAMMPS、PDB、XYZ、GROMACS、NAMD
5. **分析功能：** CESA（Cavity Energetic Sizing Algorithm，空腔能量尺度算法）、密度分布、压力分布、能量分布

---

### 术语说明

| 英文术语 | 中文翻译 | 说明 |
|---------|---------|------|
| Enhanced Monte Carlo | 增强 Monte Carlo | EMC 的全称 |
| Force field typing | 力场类型分配 | 自动为每个原子分配力场参数类型 |
| Coarse-grained | 粗粒化 | 将多个原子合并为一个"珠子"的简化模型 |
| SMILES | SMILES 字符串 | Simplified Molecular Input Line Entry System，分子结构的线性表示 |
| CESA | 空腔能量尺度算法 | Cavity Energetic Sizing Algorithm |

---

### 中文注释

> **编者注：** EMC 的核心价值在于它是一个**构建工具**而非模拟器。它的 Monte Carlo 方法用于生成合理的分子构型，然后输出给 LAMMPS、GROMACS 等 MD 引擎进行动力学模拟。EMC 本身的 MC 模拟能力相对有限。
>
> EMC 的力场 typing 能力是其最重要的特色之一。通过 `emc.pl` (EMC Setup) 和力场目录中的 `.top`/`.prm` 文件，EMC 可以自动将标准化学结构（SMILES 或 IUPAC 名）映射到力场参数。

---

### 与 LAMMPS 的关系

EMC 作为 LAMMPS 的**前置工具**：
- 生成 LAMMPS 可读取的 `data` 文件（原子坐标、拓扑）
- 生成 LAMMPS 的力场参数文件（`pair_coeff`、`bond_coeff` 等）
- 生成完整的 LAMMPS 输入脚本（`.in` 文件）
- 支持自动化的 EMC→LAMMPS 工作流

---

## 1.2 发布内容 (Distribution Content)

### 中文翻译

EMC 软件包包含以下内容：

1. **`bin/`** — 预编译的 EMC 二进制可执行文件
2. **`scripts/`** — EMC Setup 脚本（`emc.pl`、`emc_setup.pl`）和格式转换脚本
3. **`field/`** — 力场文件（`.top` 拓扑文件和 `.prm` 参数文件）
4. **`lib/`** — 晶体结构和预构建模板库
5. **`docs/`** — 文档（本 PDF 手册）
6. **`examples/`** — 示例（`build/`、`setup/`、`tutorial/`）

---

### 发布目录对照

| 目录 | 路径（服务器） | 内容 |
|------|-------------|------|
| 二进制 | `/opt/emc-9.4.4/bin/emc_linux_x86_64` | EMC 主程序 |
| 脚本 | `/opt/emc-9.4.4/scripts/` | `emc.pl`, `emc_setup.pl`, 格式转换脚本 |
| 力场 | `/opt/emc-9.4.4/field/` | born, cff, charmm, dpd, gauss, martini, opls, polystyrene, sdk, trappe, uff |
| 库 | `/opt/emc-9.4.4/lib/` | bcc.emc, fcc.emc, diamond.emc, polyethylene.emc 等 |
| 文档 | `/opt/emc-9.4.4/docs/emc.pdf` | 官方手册（本 PDF，906KB） |
| 示例 | `/opt/emc-9.4.4/examples/` | build/, setup/, tutorial/ |

---

### 常见错误

无（本章为概述，不涉及具体操作）。

---

## 验证状态

* ✅ 官方文档翻译
* ✅ 服务器文件确认
* ✅ 目录结构实地验证
* ⬜ 尚未运行 EMC

---

## 相关页面

- [EMC Setup 总览](../02_emc_setup_reference/setup_overview.md)
- [EMC 主程序命令行](../03_emc_command_reference/emc_cli.md)
- [力场清单](../05_force_fields/emc_force_field_inventory.md)
- [EMC→LAMMPS 完整工作流](../09_emc_to_lammps/complete_workflow.md)
- [第 2 章：方法论](emc_ch2_methodology.md)
