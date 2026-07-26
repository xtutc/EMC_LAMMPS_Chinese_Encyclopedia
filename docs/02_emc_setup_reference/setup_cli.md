# EMC Setup 命令行完整参考

* **EMC Setup 版本：** 5.3 (July 16, 2026)
* **官方来源：** `emc.pl -help` 输出
* **本机路径：** `/opt/emc-9.4.4/scripts/emc.pl`

---

## 语法

```bash
emc.pl [-command[=#[,..]]] project [phase 1 clusters + ...]
```

---

## 完整命令列表

### 分析类（Analyze）

| 命令 | 类型 | 默认值 | 功能 |
|------|------|--------|------|
| `-analyze_archive` | bool | `true` | 归档分析相关文件名 |
| `-analyze_data` | bool | `true` | 从交换文件列表创建 tar 存档 |
| `-analyze_last` | bool (deprecated) | `false` | 包含最后一帧轨迹 |
| `-analyze_replace` | bool | `false` | 覆盖已有分析结果 |
| `-analyze_skip` | int | `0` | 跳过的初始帧数 |
| `-analyze_source` | dir | — | 分析脚本数据源目录 |
| `-analyze_user` | dir | — | 用户分析脚本目录 |
| `-analyze_window` | int | `1` | 窗口平均的帧数 |

### DPD 相关

| 命令 | 类型 | 默认值 | 功能 |
|------|------|--------|------|
| `-angle` | float,float | `5, 180` | DPD 角常数 k 和 theta |
| `-auto` | bool | `false` | DPD .prm 中加入通配符条目 |
| `-bond` | float,float | — | 键常数 k, l |

### 构建类（Build）

| 命令 | 类型 | 默认值 | 功能 |
|------|------|--------|------|
| `-backwards` | bool | `true` | 向后兼容性 |
| `-binsize` | float | `0.01` | LAMMPS profile 的 bin 大小 |
| `-build` | string | `build` | 构建脚本名称 |
| `-build_center` | bool | `false` | 首个位点插入盒子中心 |
| `-build_compress` | bool | `false` | 错误输出压缩 |
| `-build_dir` | dir | `../build` | 构建输出目录 |
| `-build_order` | enum | `random` | 簇构建顺序 |
| `-build_origin` | float×3 | `0, 0, 0` | 中心插入坐标 |
| `-build_replace` | bool | `false` | 覆盖已有构建结果 |
| `-build_theta` | bool | `false` | 最小插入角 |
| `-build_type` | enum | `xyz` | 错误输出类型 |

### 电荷与截断

| 命令 | 类型 | 默认值 | 功能 |
|------|------|--------|------|
| `-charge` | bool | `true` | 化学含电荷 |
| `-charge_cut` | float | `9.5` | 电荷相互作用截断距离 (Å) |
| `-core` | float | `-1` | 核心直径 |
| `-cross` | bool | `false` | params 中包含非键交叉项 |
| `-crystal` | enum | `auto` | 将结构视为晶体 |
| `-cut` | float | `9.5` | 对偶相互作用截断距离 (Å) |

### 变形与删除

| 命令 | 类型 | 默认值 | 功能 |
|------|------|--------|------|
| `-deform` | complex | — | 从指定密度变形体系 |
| `-delete` | complex | — | 删除指定簇 |

### 密度与介电常数

| 命令 | 类型 | 默认值 | 功能 |
|------|------|--------|------|
| `-density` | float[] | `1` | 模拟密度 (g/cc)，每相一个值 |
| `-dielectric` | float | `1` | 介质介电常数 |
| `-direction` | enum | `x` | 相的构建方向 |
| `-debug` | bool | `false` | 输出调试信息 |

### EMC 构建

| 命令 | 类型 | 默认值 | 功能 |
|------|------|--------|------|
| `-emc` | bool | `true` | 创建 EMC 构建脚本 |
| `-emc_depth` | int | `8` | 组段落中的环识别深度 |
| `-emc_exclude` | complex | `build=false` | 排除的 EMC 段 |
| `-emc_execute` | bool | `false` | 自动执行 EMC 构建脚本 |
| `-emc_export` | complex | `smiles=` | 导出的 EMC 段 |
| `-emc_moves` | complex | — | 构建后的 Monte Carlo 移动 |
| `-emc_output` | complex | — | EMC 输出模式 |

### LAMMPS 输出（推荐使用 lammps_ 前缀）

| 命令（新） | 旧命令 | 默认值 | 功能 |
|-----------|--------|--------|------|
| `-lammps_dlimit` | `-dlimit` | `0.2` | nve/limit 最大位移 (Å) |
| `-lammps_dtdump` | `-dtdump` | `100000` | 轨迹写入频率 |
| `-lammps_dtrestart` | `-dtrestart` | `100000` | restart 频率 |
| `-lammps_dtthermo` | `-dtthermo` | `1000` | thermo 输出频率 |
| `-lammps_dump_box` | `-dump_box` | `false` | 轨迹包含盒子倍数 |
| `-lammps_communicate` | `-communicate` | `false` | 使用 communicate 关键字 |
| `-lammps_chunk` | `-chunk` | `true` | 使用 chunk 方法做 profile |
| `-lammps_cutoff` | `-cutoff` | `false` | params 输出对偶截断 |

### 其他

| 命令 | 类型 | 默认值 | 功能 |
|------|------|--------|------|
| `-field` | string | — | 力场选择（如 `opls-aa`） |
| `-setup` | string | — | 环境模式名称 |

> **版本说明：** 标记 `(deprecated)` 的命令已计划在未来版本中移除，建议迁移到新版本（`-lammps_` 前缀版本）。

---

## 典型调用模式

### 模式 1：快速小分子体系

```bash
perl emc.pl -field=opls-aa -density=0.997 water 1 1000 water
```

### 模式 2：混合物

```bash
perl emc.pl -field=opls-aa -density=0.9 mix 1 500 water + 200 ethanol
```

### 模式 3：聚合物

```bash
perl emc.pl -field=opls-aa -density=0.85 poly 1 50 polyethylene
```

### 模式 4：多相界面

```bash
perl emc.pl -field=opls-aa -density="0.9,0.9" -direction=z interface 2 500 water 500 hexane
```

---

## 相关页面

- [EMC Setup 总览](setup_overview.md)
- EMC Setup 文件规则（待创建）
- [EMC 主程序命令行](../03_emc_command_reference/emc_cli.md)
- [EMC→LAMMPS 工作流](../09_emc_to_lammps/complete_workflow.md)
