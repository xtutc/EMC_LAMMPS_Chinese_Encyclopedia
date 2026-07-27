# 第 6 章：脚本命令参考 (Scripting Commands)

* **官方章节号：** 6 | **官方页码：** 103–174 | **EMC 9.4.4**

---

## 命令列表（42 个命令）

| # | 命令 | 章节 | 功能 |
|---|------|------|------|
| 1 | `build` | 6.1 | 构建分子体系 |
| 2 | `cancel` | 6.2 | 取消操作 |
| 3 | `carve` | 6.3 | 雕刻/裁剪结构 |
| 4 | `clusters` | 6.4 | 簇管理 |
| 5 | `crystal` | 6.5 | 晶体构建（支持 bcc, fcc, diamond 等） |
| 6 | `cut` | 6.6 | 截断函数定义 |
| 7 | `deform` | 6.7 | 体系变形（拉伸/压缩） |
| 8 | `delete` | 6.8 | 删除原子/簇 |
| 9 | `duplicate` | 6.9 | 复制结构 |
| 10 | `export` | 6.10 | 导出数据（含 CESA 分析） |
| 11 | `field` | 6.11 | 力场设置（选择 .top/.prm） |
| 12 | `flag` | 6.12 | 全局标志开关 |
| 13 | `focus` | 6.13 | 聚焦区域选择 |
| 14 | `force` | 6.14 | 力计算控制 |
| 15 | `former` | 6.15 | 前体/历史定义 |
| 16 | `get` | 6.16 | 获取计算值 |
| 17 | `groups` | 6.17 | 组管理 |
| 18 | `insight` | 6.18 | Insight II 格式导入/导出 |
| 19 | `lammps` | 6.19 | LAMMPS 输入脚本自动生成 |
| 20 | `memory` | 6.20 | 内存管理 |
| 21 | `message` | 6.21 | 输出消息 |
| 22 | `moves` | 6.22 | MC 移动定义 |
| 23 | `pdb` | 6.23 | PDB 格式输出 |
| 24 | `put` | 6.24 | 放置原子/分子 |
| 25 | `rename` | 6.25 | 重命名类型 |
| 26 | `remove` | 6.26 | 移除原子/类型 |
| 27 | `reset` | 6.27 | 重置数据 |
| 28 | `restart` | 6.28 | 重启文件读写 |
| 29 | `retype` | 6.29 | 重新分配类型 |
| 30 | `run` | 6.30 | 运行 MC 模拟（默认 1000 步） |
| 31 | `sample` | 6.31 | 采样分析 |
| 32 | `shell` | 6.32 | 执行 Shell 命令 |
| 33 | `sites` | 6.33 | 位点操作 |
| 34 | `simulation` | 6.34 | 模拟全局控制 |
| 35 | `split` | 6.35 | 分割结构 |
| 36 | `terminate` | 6.36 | 终止条件 |
| 37 | `timing` | 6.37 | 计时信息 |
| 38 | `traject` | 6.38 | 轨迹输出 |
| 39 | `translate` | 6.39 | 平移原子 |
| 40 | `types` | 6.40 | 类型定义和操作 |
| 41 | `variables` | 6.41 | 变量系统 |
| 42 | `xyz` | 6.42 | XYZ 格式输出 |

## 核心命令详解

### build (6.1)
```emc
build N
```
构建 N 个分子。最重要的命令之一。

### field (6.11)
```emc
field opls-aa
field charmm/c36a
```
选择力场。支持 11 种力场目录。

### lammps (6.19)
```emc
lammps system
```
**自动生成 LAMMPS 输入脚本**。EMC 最有价值的命令。自动输出 system.data, system.in, system.params 等。

### pdb / xyz (6.23, 6.42)
```emc
pdb system.pdb
xyz system.xyz
```
输出可视化格式。

### run (6.30)
```emc
run 5000
```
运行 MC 采样。默认 1000 步。

---

## 编者注

> **编者注：** EMC 的 `.emc` 脚本是图灵完备的——命令按顺序执行，支持变量、条件、循环（通过 workflow agent）。`build`, `field`, `lammps` 是最核心的三个命令。参见完整的 6.1–6.42 各节获取语法、用法和示例。

---

## 验证： ✅ 官方翻译 | ⬜ 未验证
## 相关： [第4章](emc_ch4_simulation_setup.md) | [第5章](emc_ch5_workflow_agent.md) | [EMC CLI](../03_emc_command_reference/emc_cli.md)

## 官方来源

- **官方标题：** EMC Setup Manual v9.4.4 — Chapter 6: Scripting Commands
- **官方章节：** 6 Scripting Commands
- **官方 URL：** https://montecarlo.sourceforge.net/emc/Welcome.html
- **本地来源：** `sources/emc/emc_manual.pdf`（服务器路径：`/opt/emc-9.4.4/docs/emc.pdf`）
- **适用版本：** EMC 9.4.4 (Jul 21 2026)
- **核对日期：** 2026-07-27
- **翻译状态：** 概览翻译（本章为概览翻译，未逐段完整翻译）
