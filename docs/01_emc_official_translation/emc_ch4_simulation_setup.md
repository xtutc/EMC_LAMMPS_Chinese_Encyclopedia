# 第 4 章：模拟设置 (Simulation Setup)

* **官方章节号：** 4 | **官方页码：** 8–97 | **EMC 9.4.4**
* **官方来源：** EMC Manual PDF | **翻译状态：** 概览翻译+注释

---

## 4.1 总览 (General)

EMC Setup (emc.pl v5.3) 是 EMC 的工作流引擎。它将化学定义、力场选择、环境设置整合为一个完整的模拟项目。

**Setup 功能：**
- 生成 EMC 构建脚本 (build.emc)
- 生成 LAMMPS/GROMACS/NAMD 输入
- 组织 build/run/analyze 目录结构
- 支持 PBS/LSF/Slurm 队列
- 支持多相体系、表面、聚合物

---

## 4.2 Setup 用法 (Setup Usage)

```bash
emc.pl [-command] project [phase clusters + ...]
```

基本模式：
```bash
emc.pl -field=opls-aa -density=0.9 project 1 500 water + 200 ethanol
```

---

## 4.3 扩展 (Extensions)

EMC Setup 支持通过 Perl 模块扩展。`./scripts/modules/` 目录包含模块化实现。

---

## 4.4 选项 (Options)

### 4.4.1 环境选项 (Environment Options)

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-angle` | `5,180` | DPD 角常数 |
| `-build` | `build` | 构建脚本名 |
| `-build_dir` | `../build` | 构建目录 |
| `-density` | `1` | 目标密度 (g/cc) |
| `-cut` | `9.5` | 对偶截断 (Å) |
| `-charge_cut` | `9.5` | 电荷截断 (Å) |
| `-dielectric` | `1` | 介电常数 |
| `-direction` | `x` | 相构建方向 |

### 4.4.2 化学选项 (Chemistry Options)

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `-field` | — | 力场选择 |
| `-charge` | `true` | 含电荷 |
| `-crystal` | `auto` | 晶体处理 |
| `-binsize` | `0.01` | Profile bin 大小 |
| `-backwards` | `true` | 向后兼容 |

### 4.4.3 GROMACS 选项

EMC 也支持 GROMACS 输出。选项包括 `-gromacs_*` 系列。

---

## 4.5 文件格式 (File Formats)

### 4.5.1 环境文件 (Environment File)

定义模拟环境和队列系统设置。

### 4.5.2 化学文件 (Chemistry File)

EMC 的核心输入格式。包含：

#### General
```
# 注释行
ITEM MOLECULE name   ← 分子/化学定义
ITEM GROUP name      ← 组定义
ITEM CLUSTER name    ← 簇定义
ITEM POLYMER name    ← 聚合物定义
ITEM OPTIONS         ← 全局选项
ITEM END             ← 结束
```

#### Shorthand
EMC 支持化学简写，如 `water`, `ethanol`, `polyethylene` 等内建名称。

#### Groups
组对应分子的子结构（官能团、单体）。

#### Clusters
簇对应完整分子或预组装结构。

#### Polymers
`polymer:N` 语法定义链长。

#### DPD Additions
DPD 力场的特殊设置（角度参数、auto 通配符等）。

### 4.5.3 力场文件 (Field File)

`.top` 和 `.prm` 文件定义力场。

### 4.5.4 References 文件

引用文献记录。

### 4.5.5 Parameters 文件

EMC 生成的 LAMMPS 参数文件 (system.params)。

---

## 4.6 示例 (Examples)

### 4.6.1 References
### 4.6.2 Chemistry Mode
- **4.6.2.1 Bulk Mixture** — 体相混合物
- **4.6.2.2 Force Fields** — 力场选择和示例
- **4.6.2.3 Record** — 记录功能
- **4.6.2.4 Polymers** — 聚合物构建
- **4.6.2.5 Multiphase Systems** — 多相界面
- **4.6.2.6 Surfaces** — 表面构建
### 4.6.3 Environment Mode
- **4.6.3.1 User-Defined Force Fields** — 自定义力场
- **4.6.3.2 Shear** — 剪切模拟

---

## 4.7 Help Output

`emc.pl -help` 的完整输出（已在 setup_cli.md 中翻译）。

---

## 编者注

> **编者注：** 第 4 章是 EMC 手册中最长、最重要的章节（约 90 页）。它包含了 EMC Setup 的完整参考、所有文件格式说明和实际示例。上文的翻译是章节概览，每个小节需要独立的详细翻译页面。

---

## 验证状态

* ✅ 章节概览翻译 | ⬜ 各小节详细翻译 | ⬜ 未验证

## 相关页面

- [EMC Setup 总览](../02_emc_setup_reference/setup_overview.md)
- [EMC Setup CLI 参考](../02_emc_setup_reference/setup_cli.md)
- [EMC 第5章](emc_ch5_workflow_agent.md)
- [EMC 第6章](emc_ch6_scripting_commands.md)

## 官方来源

- **官方标题：** EMC Setup Manual v9.4.4 — Chapter 4: Simulation Setup
- **官方章节：** 4 Simulation Setup（PDF 第 8–97 页）
- **官方 URL：** https://montecarlo.sourceforge.net/emc/Welcome.html
- **本地来源：** `sources/emc/emc_manual.pdf`（服务器路径：`/opt/emc-9.4.4/docs/emc.pdf`）
- **适用版本：** EMC 9.4.4 (Jul 21 2026)
- **核对日期：** 2026-07-27
- **翻译状态：** 概览翻译（未逐段完整翻译）
