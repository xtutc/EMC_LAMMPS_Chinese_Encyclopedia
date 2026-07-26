# NPT 系综平衡与生产模拟

* **适用版本：** LAMMPS 22 Jul 2025 - Update 4
* **官方来源：** [LAMMPS fix npt](https://docs.lammps.org/fix_npt.html)
* **翻译状态：** 完整翻译 + 注释

---

## 1. 概述

NPT 系综（等温等压系综）保持粒子数 N、压力 P 和温度 T 恒定。在 EMC→LAMMPS 工作流中，NPT 用于：

1. **密度平衡：** 让盒子尺寸自动调整到正确的平衡密度
2. **生产模拟：** 在目标压力和温度下采集数据（大多数实验条件对应 NPT）
3. **相变和力学性质研究**

---

## 2. fix npt 命令

### 语法

```lammps
fix ID group npt temp Tstart Tstop Tdamp pstyle Pstart Pstop Pdamp
```

| 参数 | 含义 | 典型值 |
|------|------|--------|
| `ID` | fix 标识符 | `1`, `npt_prod` |
| `group` | 适用的原子组 | `all` |
| `Tstart` | 起始目标温度 (K) | `300.0` |
| `Tstop` | 最终目标温度 (K) | `300.0` |
| `Tdamp` | 温度阻尼参数 (fs) | `100.0` |
| `pstyle` | 压力控制方式：`iso`, `aniso`, `x`, `y`, `z`, `tri` | `iso` |
| `Pstart` | 起始目标压力 | `1.0` (atm) |
| `Pstop` | 最终目标压力 | `1.0` |
| `Pdamp` | 压力阻尼参数 (fs) | `1000.0` |

### 压力控制方式

| pstyle | 含义 | 适用场景 |
|--------|------|---------|
| `iso` | 各项同性：xyz 同步缩放 | 液体、气体、无定形聚合物 |
| `aniso` | 各向异性：xyz 独立缩放 | 晶体、液晶 |
| `x`, `y`, `z` | 单方向缩放 | 薄膜、拉伸 |
| `tri` | 三斜盒子完全自由 | 剪切、相变 |

### 压力阻尼 (Pdamp)

| 体系类型 | 推荐 Pdamp |
|---------|-----------|
| 小分子液体 | 500 – 1000 fs |
| 聚合物 | 1000 – 2000 fs |
| 粗粒化 | 2000 – 5000 fs |

> **编者注：** Pdamp 太小 → 盒子振荡太大；Pdamp 太大 → 密度平衡太慢。`Pdamp = 1000 × timestep` 是良好的经验规则。

---

## 3. 完整 NPT 生产输入

```lammps
# npt_production.in — NPT 生产模拟
# ============================================================

# --- 初始化 ---
units           real
atom_style      full
boundary        p p p

# --- 从 NVT 平衡结果继续 ---
read_restart    nvt_equil.restart
# 或
# read_data    nvt_equil.data

# --- 力场（必须重新声明，restart 文件不包含力场设置）---
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

# --- NPT 生产模拟 ---
fix             1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
#                                Tstart Tstop Tdamp pstyle Pstart Pstop Pdamp

# --- 时间积分 ---
timestep        1.0             # 1 fs

# --- 热力学输出 ---
thermo          1000
thermo_style    custom step temp press density vol etotal ke pe

# --- 轨迹输出 ---
dump            1 all custom 5000 npt_traj.lammpstrj id type x y z ix iy iz
dump_modify     1 sort id

# --- 附加输出 ---
dump            2 all xyz 5000 npt_traj.xyz      # XYZ 格式（用于可视化）

# --- 运行 ---
run             1000000         # 1 ns

# --- 保存 ---
write_restart   npt_prod.restart
write_data      npt_prod.data
```

---

## 4. 压力平衡监控

### 4.1 密度平衡

```bash
grep "^ *[0-9]" log.lammps | awk '{print $1, $9}' > density_vs_step.txt
```

密度应该围绕平衡值波动，不应有持续上升或下降趋势。

### 4.2 压力平衡

```bash
grep "^ *[0-9]" log.lammps | awk '{print $1, $3}' > pressure_vs_step.txt
```

瞬时压力波动很大（~数百 atm）是正常的。关注的是时间平均值是否接近目标压力。

### 4.3 盒子尺寸平衡

```lammps
thermo_style custom step lx ly lz density
```

盒子尺寸应该稳定在平衡值附近。

---

## 5. 从 NVT 转换到 NPT 的建议

### 5.1 渐进式压力加载

```lammps
# 阶段 1：NVT 平衡（固定体积）
fix 1 all nvt temp 300.0 300.0 100.0
run 50000

# 阶段 2：NPT 密度调整（允许盒子松弛）
unfix 1
fix 2 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
run 100000

# 阶段 3：NPT 生产（数据采集）
unfix 2
fix 3 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
run 1000000
```

### 5.2 检查密度合理性

EMC 构建时设置的目标密度（`-density` 选项）应该接近平衡密度。如果 NPT 平衡后密度显著偏离，可能是：
- 力场参数不匹配
- EMC 密度设置不合理
- 温度/压力设置错误

---

## 6. NPT 压力恒压器选项

### 6.1 Nose-Hoover（默认，推荐）

```lammps
fix 1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
```

- 产生正确的 NPT 分布
- 压力和温度的 Nose-Hoover 链耦合

### 6.2 Berendsen 恒压器

```lammps
fix 1 all press/berendsen iso 1.0 1.0 1000.0
```

- 快速调整密度
- **不产生正确的 NPT 分布**（仅用于初始密度调整！）

---

## 7. 与 EMC Setup 的关系

EMC Setup 生成的脚本通常包含 NVT 和 NPT。关键参数由 Setup 命令控制：

| EMC Setup 命令 | 对应 LAMMPS 设置 |
|---------------|-----------------|
| `-density=0.9` | NPT 目标密度间接设定 |
| `-dtdump=5000` | `dump ... 5000` |
| `-dtthermo=1000` | `thermo 1000` |
| `-dtrestart=50000` | `restart 50000` |

---

## 8. 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `ERROR: Fix npt must be defined prior to velocity creation` | fix 命令顺序错误 | 调整顺序（但 restart 不需要 velocity） |
| `Volume fluctuating too much` | Pdamp 太小 | 增大 Pdamp |
| `Density not converging` | 压力平衡太慢 | 先用 Berendsen 快速调整，再换 Nose-Hoover |
| `ERROR on proc 0: Out of range atoms` | 盒子收缩太快导致原子重叠 | 增大 Pdamp，使用更小的 timestep |

---

## 9. 本机可用性

| 命令 | 本机是否可用 |
|------|----------|
| `fix npt` | ✅ |
| `fix npt/omp` | ✅ (OPENMP package) |
| `fix press/berendsen` | ✅ |
| `fix nph` | ✅ |

---

## 10. 验证状态

* ✅ 官方翻译
* ✅ 本机命令可用性检查
* ⬜ 本机实际运行

---

## 11. 相关页面

- [最小化](minimization.md)
- [NVT 平衡](nvt.md)
- [生产模拟](production.md)
- NVE 流程（待创建）
- 平衡检查（待创建）
