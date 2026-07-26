# EMC Setup 总览与基础

* **EMC 版本：** 9.4.4
* **EMC Setup 版本：** 5.3 (July 16, 2026)
* **官方来源：** [EMC Welcome](https://montecarlo.sourceforge.net/emc/Welcome.html), `emc.pl -help` 输出
* **服务器路径：** `/opt/emc-9.4.4/scripts/emc.pl`
* **翻译状态：** 完整翻译 + 注释

---

## 1. EMC Setup 简介

EMC Setup (emc.pl) 是 EMC 的工作流引擎和项目生成器。它是一个 Perl 脚本，位于 EMC 安装目录的 `./scripts/emc.pl`。

### 1.1 核心功能

- 生成 EMC 构建脚本和 LAMMPS 输入脚本
- 支持 GROMACS 和 NAMD 输出
- 组织模拟项目为 build / run / analyze 三层结构
- 支持多相体系、表面和聚合物的定义
- 支持 PBS、LSF、Slurm 队列系统
- 集成化学类型定义和力场选择

### 1.2 命令行语法

```bash
emc.pl [-command[=#[,..]]] project [phase 1 clusters + ...]
```

**参数：**
| 参数 | 含义 |
|------|------|
| `-command` | 命令/选项（大量可用） |
| `project` | 项目名称 |
| `phase` | 模拟阶段 |
| `clusters` | 簇数 + 化学定义 |

---

## 2. 项目结构

EMC Setup 生成的典型项目结构：

```
project/
├── build/          ← 构建脚本、EMC 输入和 LAMMPS 输入
│   ├── build.emc   ← EMC 构建脚本
│   ├── system.in   ← LAMMPS 输入脚本
│   ├── system.data ← LAMMPS data 文件
│   └── system.params ← 力场参数文件
├── run/            ← LAMMPS 运行目录
│   ├── run.sh      ← 队列系统提交脚本
│   └── log.lammps  ← 运行日志
└── analyze/        ← 分析脚本
    └── analysis.sh ← 自动分析脚本
```

---

## 3. EMC Setup 核心命令参考

以下是从 `emc.pl -help` 输出中提取的关键命令（完整版见 [setup_cli.md](setup_cli.md)）：

### 3.1 构建控制

| 命令 | 默认值 | 功能 |
|------|--------|------|
| `-build` | `build` | 设置构建脚本名称 |
| `-build_dir` | `../build` | 构建输出目录 |
| `-build_replace` | `false` | 是否覆盖已有构建结果 |
| `-build_order` | `random` | 簇构建顺序 |
| `-build_center` | `false` | 首个位点插入盒子中心 |
| `-build_origin` | `x=0, y=0, z=0` | 中心插入坐标 |
| `-build_compress` | `false` | 错误输出压缩 |
| `-build_type` | `xyz` | 错误输出类型 |
| `-direction` | `x` | 相的构建方向 |

### 3.2 模拟参数

| 命令 | 默认值 | 功能 |
|------|--------|------|
| `-density` | `1` | 模拟密度（g/cc），每相一个值 |
| `-cut` | `9.5` | 对偶相互作用截断距离 |
| `-charge_cut` | `9.5` | 电荷相互作用截断距离 |
| `-core` | `-1` | 核心直径 |
| `-dielectric` | `1` | 介质介电常数 |
| `-binsize` | `0.01` | LAMMPS profile 的 bin 大小 |

### 3.3 LAMMPS 输出控制

| 命令 | 默认值 | 功能 |
|------|--------|------|
| `-dtdump` / `-lammps_dtdump` | `100000` | LAMMPS 轨迹文件写入频率 |
| `-dtrestart` / `-lammps_dtrestart` | `100000` | LAMMPS restart 文件频率 |
| `-dtthermo` / `-lammps_dtthermo` | `1000` | LAMMPS 热力学输出频率 |
| `-dlimit` / `-lammps_dlimit` | `0.2` | LAMMPS nve/limit 最大位移 |
| `-dump_box` | `false` | LAMMPS 轨迹中包含盒子倍数 |

> **版本说明：** 带 `lammps_` 前缀的命令是新版推荐写法；不带前缀的旧版写法已标记 `deprecated`。

### 3.4 EMC 构建控制

| 命令 | 默认值 | 功能 |
|------|--------|------|
| `-emc` | `true` | 创建 EMC 构建脚本 |
| `-emc_execute` | `false` | 执行 EMC 构建脚本 |
| `-emc_depth` | `8` | 组段落中的环识别深度 |
| `-emc_exclude` | `build=false` | 要排除的 EMC 段 |
| `-emc_export` | `smiles=` | 要导出的 EMC 段 |
| `-emc_output` | `debug=false, exit=true, info=true, warning=true` | EMC 输出模式 |

### 3.5 分析控制

| 命令 | 默认值 | 功能 |
|------|--------|------|
| `-analyze_archive` | `true` | 归档分析数据 |
| `-analyze_data` | `true` | 从交换文件列表创建 tar 存档 |
| `-analyze_replace` | `false` | 覆盖已有分析结果 |
| `-analyze_skip` | `0` | 跳过的初始帧数 |
| `-analyze_window` | `1` | 窗口平均的帧数 |
| `-analyze_source` | — | 分析脚本的数据源目录 |
| `-analyze_user` | — | 用户分析脚本目录 |

### 3.6 力场和拓扑

| 命令 | 默认值 | 功能 |
|------|--------|------|
| `-angle` | `5, 180` | DPD 角常数 `k` 和 `theta`；或设置角力场选项 |
| `-bond` | — | 设置键常数 `k, l` |
| `-charge` | `true` | 化学含电荷 |
| `-cross` | `false` | LAMMPS params 中包含非键交叉项 |
| `-auto` | `false` | DPD .prm 中加入通配符条目 |

### 3.7 特殊功能

| 命令 | 默认值 | 功能 |
|------|--------|------|
| `-crystal` | `auto` | 将导入结构视为晶体 |
| `-deform` | — | 从指定密度变形体系 |
| `-delete` | — | 删除指定簇 |
| `-backwards` | `true` | 向后兼容性 |
| `-debug` | `false` | 输出调试信息 |

---

## 4. EMC Setup 工作流示例

### 4.1 最简单的调用

```bash
perl /opt/emc-9.4.4/scripts/emc.pl \
  water-ethanol 1 1000 water + 200 ethanol
```

- 项目名：`water-ethanol`
- 1 个相
- 1000 个水分子 + 200 个乙醇分子

### 4.2 带力场和密度

```bash
perl /opt/emc-9.4.4/scripts/emc.pl \
  -field=opls-aa \
  -density=0.9 \
  polymer_melt 1 50 polyethylene
```

### 4.3 使用环境模式

```bash
perl /opt/emc-9.4.4/scripts/emc.pl \
  -field=opls-aa \
  -setup=shear \
  -density=0.85 \
  polymer_shear 1 100 polypropylene
```

---

## 5. EMC Setup 示例目录

官方示例位于 `/opt/emc-9.4.4/examples/setup/`：

```
examples/setup/
├── chemistry/          ← 化学模式示例
│   ├── bulk/          ← 体相体系
│   ├── polymer/       ← 聚合物
│   ├── surface/       ← 表面/界面
│   └── multiphase/    ← 多相体系
└── environment/        ← 环境模式示例
    └── shear/          ← 剪切模拟
        └── t_glass/    ← 玻璃化转变温度
```

---

## 6. EMC Setup 与 EMC 主程序的关系

```
EMC Setup (emc.pl Perl)
    │
    ├── 读取化学定义、力场参数
    ├── 调用 emc_setup.pl v4.1.5 (legacy) 或内置模块
    ├── 生成 build.emc (EMC 主程序输入)
    │
    └── EMC 主程序 (emc_linux_x86_64)
        │
        ├── 读取 build.emc
        ├── MC 采样构建体系
        ├── 输出 data, params, pdb, xyz
        └── 输出 system.in (LAMMPS 输入脚本)
```

**编者注：** EMC Setup 是一个**生成器**，EMC 主程序是**执行器**。Setup 生成 EMC 的输入文件，EMC 主程序执行实际的 Monte Carlo 构建。用户通常直接与 Setup 交互。

---

## 7. 验证状态

* ✅ 官方信息（来自 `emc.pl -help` 和官方网站）
* ✅ 服务器实际安装确认
* ⬜ 本机实际运行 EMC Setup
* ⬜ 尚未验证

---

## 8. 相关页面

- [EMC Setup 命令行完整参考](setup_cli.md)
- [EMC Setup 文件规则](setup_file_rules.md)
- [EMC 主程序命令行](emc_cli.md)
- [EMC→LAMMPS 完整工作流](../09_emc_to_lammps/complete_workflow.md)
- [力场清单](../05_force_fields/emc_force_field_inventory.md)
