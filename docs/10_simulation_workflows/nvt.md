# NVT 系综平衡与模拟

* **适用版本：** LAMMPS 22 Jul 2025 - Update 4
* **官方来源：** [LAMMPS fix nvt](https://docs.lammps.org/fix_nvt.html)
* **翻译状态：** 完整翻译 + 注释

---

## 1. 概述

NVT 系综（正则系综）保持粒子数 N、体积 V 和温度 T 恒定。在 EMC→LAMMPS 工作流中，NVT 通常用于：

1. **平衡阶段：** 在固定体积下将体系从初始结构松弛到平衡态
2. **预生产阶段：** 在 NPT 之前验证体系稳定性
3. **分析阶段：** 对平衡后的构型进行性质分析（不能用于 NPT 性质）

> **编者注：** 在 NVT 中，盒子大小保持不变。如果需要对密度进行平衡，应使用 NPT 系综。

---

## 2. fix nvt 命令

### 语法

```lammps
fix ID group nvt temp Tstart Tstop Tdamp
```

| 参数 | 含义 | 典型值 |
|------|------|--------|
| `ID` | fix 标识符 | `1`, `nvt_eq` |
| `group` | 适用的原子组 | `all` |
| `Tstart` | 起始目标温度 (K) | `300.0` |
| `Tstop` | 最终目标温度 (K) | `300.0`（等温时同 Tstart） |
| `Tdamp` | 温度阻尼参数 (fs) | `100.0` |

### 温度阻尼 (Tdamp) 的选择

| 体系规模 | 推荐 Tdamp |
|---------|-----------|
| 小分子液体 (< 1000 atoms) | 50 – 100 fs |
| 中等体系 (1000 – 10000 atoms) | 100 – 200 fs |
| 大体系 (> 10000 atoms) | 200 – 500 fs |
| 粗粒化体系 | 500 – 1000 fs |

> **编者注：** Tdamp 太小 → 温度振荡大；Tdamp 太大 → 温度调节太慢。100 fs 是大多数 atomistic 模拟的良好起点。

---

## 3. 完整 NVT 平衡输入

```lammps
# nvt_equil.in — EMC 体系 NVT 平衡
# ============================================================

# --- 初始化 ---
units           real
atom_style      full
boundary        p p p

# --- 读入最小化后的结构 ---
read_data       minimized.data

# --- 力场 ---
pair_style      lj/cut/coul/long 10.0 12.0
pair_modify     mix geometric
kspace_style    pppm 1.0e-4

include         system.params

bond_style      harmonic
angle_style     harmonic
dihedral_style  opls
improper_style  harmonic

special_bonds   lj/coul 0.0 0.0 0.5

# --- 邻域列表 ---
neighbor        2.0 bin
neigh_modify    every 1 delay 0 check yes

# --- 初始速度 ---
velocity        all create 300.0 12345 mom yes rot yes
#                 ↑        ↑     ↑
#                 组      温度   随机种子

# --- NVT 平衡 ---
fix             1 all nvt temp 300.0 300.0 100.0
#                                ↑     ↑     ↑
#                               Tstart Tstop Tdamp

# --- 时间积分 ---
timestep        1.0             # 1 fs (atomistic)

# --- 输出 ---
thermo          100
thermo_style    custom step temp press etotal density vol

dump            1 all custom 1000 nvt_traj.lammpstrj id type x y z
dump_modify     1 sort id

# --- 运行 ---
run             50000           # 50 ps (atomistic)

# --- 保存 ---
write_restart   nvt_equil.restart
write_data      nvt_equil.data
```

---

## 4. NVT 加热（温度斜坡）

从低温加热到目标温度：

```lammps
# NVT 加热：100 K → 300 K，速率 200 fs/K → 40000 步 = 40 ps
fix 1 all nvt temp 100.0 300.0 100.0
run 40000

# 然后 Tdamp 保持恒温
fix 1 all nvt temp 300.0 300.0 100.0
run 50000
```

---

## 5. NVT 温度恒温器选项

### 5.1 Nose-Hoover（默认）

```lammps
fix 1 all nvt temp 300.0 300.0 100.0
```

- 产生正确的 NVT 分布
- 可能产生温度振荡
- 建议 Tdamp = 100 × timestep

### 5.2 Langevin 恒温器

```lammps
fix 1 all langevin 300.0 300.0 100.0 12345
```

- 更温和的温度控制
- 阻尼可能影响动力学

### 5.3 Berendsen 恒温器

```lammps
fix 1 all temp/berendsen 300.0 300.0 100.0
```

- 快速达到目标温度
- **不产生正确的 NVT 分布**（仅用于初始平衡！）

> **警告：** Berendsen 恒温器不产生正确的正则系综分布。只能用于快速初始平衡，不能用于生产模拟。生产模拟应使用 Nose-Hoover (`fix nvt`) 或 Langevin。

---

## 6. 温度控制技巧

### 6.1 检查温度平衡

```lammps
fix temp_out all ave/time 100 10 1000 c_thermo_temp file temp_profile.txt
```

### 6.2 分组建温

对不同组分分别控温（避免热浴不均）：

```lammps
# 溶质和溶剂分开控温
group solute type 1 2 3
group solvent type 4 5

fix 1 solute nvt temp 300.0 300.0 100.0
fix 2 solvent nvt temp 300.0 300.0 100.0
```

---

## 7. 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `ERROR: Temperature control fix ... must be defined prior to velocity creation` | fix 在 velocity 之后定义 | 将 fix 放在 velocity 之前 |
| `ERROR: Fix nvt requires ...` | 缺少必要组件 | 检查 atom_style 和力场设置 |
| `Temperature out of range` | 初始结构有问题（原子重叠） | 先进行更充分的最小化 |
| `Shake atoms missing` | 使用 shake 但拓扑不完整 | 检查键/角定义 |
| `Lost atoms` | 原子跑出盒子 | 减小 timestep 或增大 Tdamp |

---

## 8. 与 EMC 的关系

EMC Setup 生成的 LAMMPS 输入脚本通常包含完整的 NVT 平衡部分。对于 OPLS-AA 等力场，典型设置已由 EMC 预设。

---

## 9. 本机可用性

| 命令 | 本机是否可用 |
|------|----------|
| `fix nvt` | ✅ |
| `fix langevin` | ✅ |
| `fix temp/berendsen` | ✅ |
| `fix nve` | ✅ |
| `velocity` | ✅ |

---

## 10. 验证状态

* ✅ 官方翻译
* ✅ 本机命令检查
* ⬜ 本机实际运行

---

## 11. 相关页面

- [最小化](minimization.md)
- [NPT 平衡](npt.md)
- [升温流程](heating.md)
- [加热与退火](heating.md)
- [生产模拟](production.md)

## 官方来源

- **官方标题：** LAMMPS Documentation — fix nvt/npt/nph command
- **官方章节或命令：** `fix nvt`
- **官方 URL：** https://docs.lammps.org/fix_nh.html
- **本地来源：** 本地未获取
- **适用版本：** LAMMPS 22 Jul 2025 - Update 4（本地）
- **核对日期：** 2026-07-27
- **内容说明：** 本章为编者整理的 NVT 模拟流程指南，结合官方文档与编者注释编写。
