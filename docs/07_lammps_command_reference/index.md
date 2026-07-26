# LAMMPS 命令参考

> **适用版本：** LAMMPS 22 Jul 2025 - Update 4
> **内容状态：** 当前页面仅索引已收录命令；各页面的完整程度见下表。

本节提供 LAMMPS 22 Jul 2025 命令的中文参考入口。命令参数、默认值、
限制和版本差异必须以目标版本的官方文档为准；当前收录页面尚未全部达到
“完整命令参考”的标准。

## 已收录命令

### 初始化命令

| 命令 | 页面 | 当前完整程度 | 说明 |
|---|---|---|---|
| `velocity` | [初始化 / velocity](initialization/velocity.md) | 严重不完整 | 现有内容未覆盖全部官方语法、关键字和限制。 |

### 计算命令

| 命令 | 页面 | 当前完整程度 | 说明 |
|---|---|---|---|
| `thermo` | [计算 / thermo](computes/thermo.md) | 部分覆盖 | 已提供基础用法，尚未完成全部参数审计。 |

### 输出命令

| 命令 | 页面 | 当前完整程度 | 说明 |
|---|---|---|---|
| `dump` | [输出 / dump](dumps/dump.md) | 部分覆盖 | 已覆盖部分格式与选项，尚未完成完整性核对。 |

### 约束命令

| 命令 | 页面 | 当前完整程度 | 说明 |
|---|---|---|---|
| `fix shake` | [约束 / fix shake](fixes/fix_shake.md) | 严重不完整 | 现有内容未覆盖全部语法形式、关键字和限制。 |

## 已规划类别

- `force_fields`：待创建
- `minimization`：待创建
- `running`：待创建
- `system_definition`：待创建
- `variables_and_control`：待创建

## 阅读与引用说明

- “部分覆盖”表示页面可用于定位基础概念，但不能替代官方完整语法。
- “严重不完整”表示当前内容尚不足以支撑独立的命令配置。
- 计划补齐的命令页面将按官方类别组织，并逐项记录参数、默认值、单位和限制。

## 官方来源

- **官方标题：** LAMMPS Documentation
- **官方命令分类：** Commands
- **官方 URL：** [LAMMPS Commands documentation](https://docs.lammps.org/Commands.html)
- **适用版本：** LAMMPS 22 Jul 2025 - Update 4
- **核对日期：** 2026-07-27
