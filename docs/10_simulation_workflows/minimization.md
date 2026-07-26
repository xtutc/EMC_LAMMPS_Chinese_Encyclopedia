# 能量最小化完整流程

* **适用版本：** LAMMPS 22 Jul 2025 - Update 4
* **官方来源：** [LAMMPS minimize](https://docs.lammps.org/minimize.html)
* **翻译状态：** 完整翻译 + 注释

---

## 1. 概述

能量最小化（Energy Minimization）是分子动力学模拟的第一步。它的目的是：

- 消除 EMC 构建后的不合理的原子重叠
- 将体系松弛到最近的势能面局部极小值
- 为后续的升温、平衡和生产模拟提供合理的初始结构

> **编者注：** EMC 使用 Monte Carlo 方法构建体系，可能产生一些不合理的原子构型（原子太近、键过度拉伸等）。最小化是必不可少的预处理步骤。

---

## 2. minimize 命令

### 语法

```lammps
minimize etol ftol maxiter maxeval
```

| 参数 | 含义 | 典型值 |
|------|------|--------|
| `etol` | 能量容差（停止条件） | `1.0e-4` |
| `ftol` | 力容差（停止条件） | `1.0e-6` |
| `maxiter` | 最大迭代次数 | `1000` |
| `maxeval` | 最大力计算次数 | `10000` |

### 停止条件

最小化在满足以下**任一**条件时停止：

1. 相邻迭代的能量差 < `etol`
2. 任意原子的最大力分量 < `ftol`（力单位取决于 `units`）
3. 迭代次数 > `maxiter`
4. 力计算次数 > `maxeval`

### 示例

```lammps
# 较宽松的最小化（初始构建后）
minimize 1.0e-4 1.0e-6 1000 10000

# 更严格的最小化（生产前精细调整）
minimize 1.0e-6 1.0e-8 5000 50000

# 快速最小化（仅消除重叠）
minimize 1.0e-3 1.0e-4 100 1000
```

---

## 3. 最小化算法

LAMMPS 提供多种最小化算法，通过 `min_style` 选择：

### 3.1 cg（共轭梯度，默认）

```lammps
min_style cg
minimize 1.0e-4 1.0e-6 1000 10000
```

- Polak-Ribiere 共轭梯度法
- 对大多数体系效果最好
- 收敛速度快

### 3.2 sd（最速下降）

```lammps
min_style sd
minimize 1.0e-4 1.0e-6 1000 10000
```

- 对初始结构很差时效果好
- 收敛速度较慢

### 3.3 quickmin

```lammps
min_style quickmin
minimize 1.0e-4 1.0e-6 1000 10000
```

- 类似于阻尼动力学
- 对某些体系可能更快

### 3.4 fire

```lammps
min_style fire
minimize 1.0e-4 1.0e-6 1000 10000
```

- FIRE (Fast Inertial Relaxation Engine)
- 对大体系或长程相互作用更好的表现

### 3.5 hftn

```lammps
min_style hftn
minimize 1.0e-4 1.0e-6 1000 10000
```

- Hessian-Free Truncated Newton
- 对精密最小化有效

---

## 4. 完整最小化输入脚本

```lammps
# minim.in — EMC 体系能量最小化
# ============================================================

# --- 初始化 ---
units           real
atom_style      full
boundary        p p p

# --- 读入 EMC 生成的体系 ---
read_data       system.data

# --- 力场设置（OPLS-AA 示例）---
pair_style      lj/cut/coul/long 10.0 12.0
pair_modify     mix geometric
kspace_style    pppm 1.0e-4

include         system.params    # EMC 生成的力场参数

bond_style      harmonic
angle_style     harmonic
dihedral_style  opls
improper_style  harmonic

special_bonds   lj/coul 0.0 0.0 0.5

# --- 全局设置 ---
neighbor        2.0 bin
neigh_modify    every 1 delay 0 check yes

# --- 热力学输出 ---
thermo          100
thermo_style    custom step pe ke etotal temp press vol

# --- 最小化 ---
min_style        cg
minimize         1.0e-4 1.0e-6 1000 10000

# --- 保存最小化结果 ---
write_data       minimized.data
```

---

## 5. 最小化策略

### 5.1 两阶段最小化

对于初始结构很差的体系，建议使用两阶段策略：

```lammps
# 阶段 1：使用固定原子位置限制过度运动
fix 1 all nve/limit 0.1              # 限制最大位移 0.1 Å/步
min_style sd                          # 最速下降
minimize 1.0e-3 1.0e-4 500 5000

unfix 1

# 阶段 2：自由最小化
fix 2 all box/relax iso 0.0           # 允许盒子松弛（可选）
min_style cg                          # 共轭梯度
minimize 1.0e-4 1.0e-6 1000 10000
```

### 5.2 带盒子松弛的最小化

```lammps
fix 1 all box/relax iso 0.0 vmax 0.001
minimize 1.0e-4 1.0e-6 1000 10000
```

---

## 6. 最小化后检查

### 6.1 判断最小化是否成功

```bash
grep "Minimization" log.lammps
# 输出示例：
# Minimization stats:
#   Stopping criterion = energy tolerance
#   Energy initial, next-to-last, final = ...
#   Force two-norm initial, final = ...
```

成功的标志：
- 能量变化趋于平稳
- 最大力分量 < `ftol`
- 没有 `ERROR: Lost atoms` 或 `ERROR: Out of range atoms`

### 6.2 检查残留力

```lammps
compute maxforce all reduce max fmax
thermo_style custom step pe c_maxforce
```

---

## 7. 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `ERROR: Lost atoms: original N ... current M` | 原子运动出盒子（非周期边界） | 增大盒子或用 `fix nve/limit` |
| `ERROR: Out of range atoms - cannot compute PPPM` | 原子超出 PPPM 计算范围 | 增大 box 或减小截断 |
| `ERROR: Non-numeric atom coords` | 原子坐标变成 NaN | 初始结构有问题，检查 data 文件 |
| `WARNING: Energy is not going down. Stopping.` | 能量不下降 | 尝试 `min_style sd` 先 |
| `WARNING: Using a manybody potential with bonds/angles/dihedrals and special_bonds` | special_bonds 设置可能导致错力 | 检查力场一致性 |

---

## 8. 与 EMC 的关系

EMC 生成体系后，**必须**进行最小化。EMC Setup 生成的 `.in` 文件通常已包含最小化部分。

典型的 EMC→LAMMPS 最小化流程：

```bash
# 1. EMC 构建体系
emc build.emc                    # 生成 system.data, system.params, system.in

# 2. 检查生成的文件
ls system.data system.params system.in

# 3. 最小化
lmp -in system.in -log minim.log

# 4. 检查结果
grep "Minimization" minim.log
```

---

## 9. 本机可用性

| 算法 | 本机是否可用 |
|------|----------|
| `cg` | ✅ |
| `sd` | ✅ |
| `fire` (旧版) | ✅ |
| `fire` (新版) | ✅ |
| `quickmin` | ✅ |
| `hftn` | ✅ |
| `spin` | ✅ |

---

## 10. 验证状态

* ✅ 官方翻译
* ✅ 本机命令可用性检查
* ⬜ 本机实际运行
* ⬜ EMC 体系最小化验证

---

## 11. 相关页面

- [升温流程](heating.md)
- [NVT 平衡](nvt.md)
- [NPT 平衡](npt.md)
- [LAMMPS 输入脚本语法](../06_lammps_user_guide_translation/input_scripts/input_script_syntax.md)
- [EMC→LAMMPS 完整工作流](../09_emc_to_lammps/complete_workflow.md)
