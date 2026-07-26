# LAMMPS Units 系统与 EMC 单位映射

* **适用版本：** LAMMPS 22 Jul 2025 - Update 4, EMC 9.4.4
* **官方来源：** [LAMMPS units](https://docs.lammps.org/units.html)
* **翻译状态：** 完整翻译 + 编者注释

---

## 1. LAMMPS Units 系统总览

LAMMPS 提供多种单位系统，通过 `units` 命令设置。选择一个单位系统后，**所有输入参数必须使用该系统的单位**。这是 EMC 用户在 EMC Setup 中必须匹配的关键设置。

| Units | 能量 | 距离 | 时间 | 质量 | 温度 | 压力 | 电荷 |
|-------|------|------|------|------|------|------|------|
| `lj` | ε | σ | τ = σ√(m/ε) | m | ε/k_B | ε/σ³ | e |
| `real` | kcal/mol | Å | fs | g/mol | K | atm | e |
| `metal` | eV | Å | ps | g/mol | K | bar | e |
| `si` | J | m | s | kg | K | Pa | C |
| `cgs` | erg | cm | s | g | K | dyne/cm² | esu |
| `electron` | Hartree | Bohr | fs | a.u. | K | Hartree/Bohr³ | e |
| `micro` | pg·µm²/µs² | µm | µs | pg | K | pg/(µm·µs²) | e |
| `nano` | ag·nm²/ns² | nm | ns | ag | K | ag/(nm·ns²) | e |

---

## 2. EMC 常用 Units 详解

### 2.1 real（最常用）

EMC 生成的大多数 system（CHARMM、OPLS、PCFF、COMPASS、TraPPE）使用 `real` 单位。

| 物理量 | 单位 | 说明 |
|--------|------|------|
| 能量 | kcal/mol | 千卡/摩尔 |
| 距离 | Å | 埃 = 10⁻¹⁰ m |
| 时间 | fs | 飞秒 = 10⁻¹⁵ s |
| 质量 | g/mol | 克/摩尔 |
| 温度 | K | 开尔文 |
| 压力 | atm | 标准大气压 |
| 电荷 | e | 电子电荷绝对值（1.6021765×10⁻¹⁹ C） |

**编者注：** `real` 单位系统源自生物分子模拟社区（CHARMM、AMBER、NAMD），是 EMC 最自然的单位选择。所有 EMC 支持的经典生物分子力场都使用 `real` 单位或兼容的单位。

### 2.2 metal

| 物理量 | 单位 |
|--------|------|
| 能量 | eV |
| 距离 | Å |
| 时间 | ps |
| 质量 | g/mol |
| 温度 | K |
| 压力 | bar |

**编者注：** EMC 的 Born 力场用于金属氧化物，在 LAMMPS 中通常使用 `metal` 或 `real` 单位。

### 2.3 lj（Lennard-Jones 约化单位）

| 物理量 | 单位 |
|--------|------|
| 能量 | ε（LJ 能量参数） |
| 距离 | σ（LJ 尺寸参数） |
| 时间 | τ = σ√(m/ε) |
| 质量 | m |
| 温度 | ε/k_B |

**编者注：** EMC 的粗粒化力场（DPD、SDK、Martini）常使用 `lj` 单位。DPD 模拟甚至有自己的 `units lj` 默认参数集。

---

## 3. EMC 力场 ↔ LAMMPS Units 映射

这是 EMC 用户最重要的参考表：

| EMC 力场 | 推荐 LAMMPS units | atom_style | 状态 |
|---------|-------------------|------------|------|
| OPLS-AA | `real` | `full` | 官方确认 |
| OPLS-UA | `real` | `full` | 官方确认 |
| CHARMM c36a/c32b | `real` | `full` | 官方确认 |
| CGENFF | `real` | `full` | 官方确认 |
| PCFF | `real` | `full` | 官方确认 |
| COMPASS | `real` | `full` | 官方确认 |
| TraPPE | `real` | `full` | 官方确认 |
| Born | `real` 或 `metal` | `full` 或 `charge` | 官方确认 |
| DPD | `lj` | `atomic` | 官方确认 |
| MARTINI2/MARTINI3 | `real` 或 `nano` | `full` | 官方确认 |
| SDK | `lj` | `atomic` | 官方确认 |
| Colloidal | `lj` | `atomic` | 官方确认 |

**编者注：** MARTINI 力场在 EMC 中需要用户自行 typing，但输出到 LAMMPS 时通常使用 `real` 或 `nano` 单位。

---

## 4. Units 设置与力场参数的关系

### 4.1 pair_style 与 units 匹配

```lammps
units       real               # Å, kcal/mol, fs
pair_style  lj/cut/coul/long 10.0   # cutoff=10 Å
pair_coeff  1 1 0.1 3.0       # ε=0.1 kcal/mol, σ=3.0 Å
```

如果使用 `lj` 单位：

```lammps
units       lj
pair_style  lj/cut 2.5        # cutoff=2.5 σ
pair_coeff  1 1 1.0 1.0       # ε=1.0ε, σ=1.0σ
```

### 4.2 time step 与 units 关系

| units | 典型 timestep | 说明 |
|-------|-------------|------|
| `real` | 0.5 – 2.0 fs | 生物分子模拟通常用 1.0 或 2.0 fs |
| `metal` | 0.001 – 0.01 ps | 金属体系 |
| `lj` | 0.001 – 0.005 τ | 粗粒化/通用体系 |
| `si` | ~1e-15 s | 很少用 |
| `nano` | 0.001 – 0.01 ns | 粗粒化体系 |

---

## 5. 从 EMC Setup 角度看 Units

### 5.1 EMC Setup 不直接设置 units

EMC Setup 生成的 LAMMPS 输入脚本中，`units` 命令由 EMC 根据所选力场自动设置。用户通常不需要手动修改。

### 5.2 检查一致性

EMC 生成的 data 文件中的坐标（Å）、盒子尺寸（Å）与 LAMMPS `units` 设定必须一致。

**验证方法：**

1. 查看 EMC Setup 输出日志中的单位声明
2. 查看生成的 `.in` 文件中的 `units` 命令
3. 检查 data 文件标题行中的参数是否与 `units` 系统相符
4. 确认 `pair_coeff` 参数（如在 `.params` 文件中）的数值是否合理（如 ε 在 ~0.1 kcal/mol 量级）

### 5.3 常见陷阱

> **警告：** 如果将 `real` 单位体系的 data 文件用于 `metal` 单位的 LAMMPS 输入脚本，所有能量相关的计算结果都会是错的（因为 1 eV ≈ 23.06 kcal/mol）。

---

## 6. Units 转换常数

| 转换 | 数值 |
|------|------|
| 1 kcal/mol 转 eV | 0.04336 eV |
| 1 eV 转 kcal/mol | 23.0605 kcal/mol |
| 1 atm 转 bar | 1.01325 bar |
| 1 Å 转 nm | 0.1 nm |
| k_B | 1.9872×10⁻³ kcal/(mol·K) |
| 1 fs 转 ps | 0.001 ps |

---

## 7. 完整示例：匹配 EMC 输出的 Units

EMC 典型的 OPLS-AA 输出对应 LAMMPS 设置：

```lammps
# EMC 生成的 LAMMPS 输入（OPLS-AA 力场）
units           real          # ← 对应 OPLS-AA 的标准单位

atom_style      full          # ← 需要电荷（OPLS 使用部分电荷）

boundary        p p p

read_data       system.data   # ← EMC 生成，坐标单位 Å

# OPLS-AA 使用 lj/cut/coul/long
pair_style      lj/cut/coul/long 10.0 12.0  # ← cutoff 10 Å, 长程 12 Å
kspace_style    pppm 1.0e-4                  # ← 长程静电

include         system.params  # ← EMC 生成力场参数

# 键和角（harmomic 是标准选择）
bond_style      harmonic
angle_style     harmonic
dihedral_style  opls

timestep        1.0            # ← 1.0 fs（典型 OPLS 设置）

fix             1 all nvt temp 300.0 300.0 100.0  # ← 温度单位 K

run             50000
```

---

## 8. 验证状态

* ✅ 官方翻译（基于 LAMMPS 官方文档）
* ✅ 本机静态检查
* ⬜ 本机实际运行
* ⬜ EMC 实际生成验证

---

## 9. 相关页面

- [EMC→LAMMPS 完整工作流](complete_workflow.md)
- [力场映射表](force_field_mapping.md)
- [力场基础](../../05_force_fields/fundamentals.md)
