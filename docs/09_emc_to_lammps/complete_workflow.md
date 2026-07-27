# EMC → LAMMPS 完整工作流

* **EMC 版本：** 9.4.4 (Jul 21 2026)
* **LAMMPS 版本（服务器）：** 7 Feb 2024 - Update 1
* **LAMMPS 版本（本地）：** 22 Jul 2025 - Update 4
* **官方来源：** EMC 官方手册, EMC Setup 文档, LAMMPS 官方文档
* **翻译状态：** 完整（含编者注释和实际运行建议）

---

## 1. 工作流总览

EMC → LAMMPS 的完整工作流包含以下步骤：

```
EMC Setup (emc.pl)
    │
    ▼
生成构建文件 (build.emc, 化学定义)
    │
    ▼
EMC 主程序 (emc)
    │
    ├── Monte Carlo 采样
    ├── 力场 typing
    │
    ▼
输出 LAMMPS 文件
    ├── system.data      ← 结构 + 拓扑
    ├── system.params    ← 力场参数
    ├── system.in        ← LAMMPS 输入脚本
    ├── system.pdb       ← PDB 结构（可视化）
    └── system.xyz       ← XYZ 坐标

    ▼
LAMMPS 模拟
    ├── 1. 最小化
    ├── 2. NVT 平衡
    ├── 3. NPT 平衡（可选）
    └── 4. 生产模拟
```

---

## 2. 第一步：EMC Setup 生成项目

### 2.1 最小示例：水+乙醇混合物

```bash
# 在服务器上运行
perl /opt/emc-9.4.4/scripts/emc.pl \
  -field=opls-aa \
  -density=0.9 \
  water-ethanol 1 500 water + 200 ethanol
```

**参数解释：**

| 参数 | 含义 |
|------|------|
| `-field=opls-aa` | 使用 OPLS-AA 力场 |
| `-density=0.9` | 目标密度 0.9 g/cm³ |
| `water-ethanol` | 项目名称 |
| `1` | 1 个相 |
| `500 water` | 500 个水分子 |
| `+ 200 ethanol` | 200 个乙醇分子 |

### 2.2 Setup 生成的文件

```
water-ethanol/
├── build/
│   ├── build.emc        ← EMC 构建脚本
│   ├── build.sh         ← 构建执行脚本
│   └── (构建后生成):
│       ├── system.data  ← LAMMPS data 文件
│       ├── system.in    ← LAMMPS 输入脚本
│       ├── system.params ← 力场参数
│       ├── system.pdb   ← PDB 结构
│       └── system.xyz   ← XYZ 坐标
├── run/
│   └── run.sh           ← 运行脚本
└── analyze/
    └── analysis.sh      ← 分析脚本
```

---

## 3. 第二步：EMC 构建体系

```bash
cd water-ethanol/build
emc -nthreads=4 build.emc
```

**预期输出：**

```
Info: Thank you for using EMC v9.4.4
Info: Reading build.emc
Info: Building system...
Info: Output: system.data, system.in, system.params, system.pdb, system.xyz
Info: Done.
```

**检查要点：**

```bash
# 检查文件是否生成
ls -la system.data system.in system.params

# 检查 data 文件是否合理
head -30 system.data

# 检查原子数
grep "atoms" system.data
```

---

## 4. 第三步：检查 EMC 生成的文件

### 4.1 检查 LAMMPS 输入脚本 (system.in)

```lammps
# EMC 生成的 system.in 通常包含：
units           real
atom_style      full
boundary        p p p
read_data       system.data
pair_style      lj/cut/coul/long 10.0 12.0
kspace_style    pppm 1e-4
include         system.params       # ← 力场参数
# ... 键/角/二面角设置
# ... fix, minimize, run 命令
```

**验证清单：**
- [ ] `units` 匹配力场要求
- [ ] `atom_style` 为 `full`（对于 OPLS/CHARMM）
- [ ] `pair_style` 和 `kspace_style` 合理
- [ ] `include system.params` 文件存在
- [ ] `timestep` 为合理值（通常 1.0 fs）

### 4.2 检查力场参数文件 (system.params)

```bash
head -50 system.params
```

应包含 `pair_coeff`、`bond_coeff`、`angle_coeff`、`dihedral_coeff` 等。

### 4.3 检查 data 文件 (system.data)

```bash
# 检查头部
head -20 system.data

# 检查原子段
grep -A 5 "^Atoms" system.data | head -10

# 检查键段（如果有）
grep -A 5 "^Bonds" system.data | head -10
```

---

## 5. 第四步：LAMMPS 最小化

### 5.1 创建最小化输入

EMC 生成的 `system.in` 通常已包含最小化部分。如需独立控制，可以创建 `minim.in`：

```lammps
# minim.in
units           real
atom_style      full
boundary        p p p

read_data       system.data

pair_style      lj/cut/coul/long 10.0 12.0
pair_modify     mix geometric
kspace_style    pppm 1.0e-4

include         system.params

bond_style      harmonic
angle_style     harmonic
dihedral_style  opls
improper_style  harmonic

special_bonds   lj/coul 0.0 0.0 0.5

neighbor        2.0 bin
neigh_modify    every 1 delay 0 check yes

thermo          100
thermo_style    custom step pe ke etotal temp press

min_style       cg
minimize        1.0e-4 1.0e-6 1000 10000

write_data      minimized.data
```

### 5.2 运行

```bash
lmp -in minim.in -log minim.log
```

### 5.3 检查结果

```bash
grep "Minimization" minim.log
grep "ERROR" minim.log
```

---

## 6. 第五步：NVT 平衡

```lammps
# nvt.in
read_data       minimized.data

pair_style      lj/cut/coul/long 10.0 12.0
pair_modify     mix geometric
kspace_style    pppm 1.0e-4
include         system.params
bond_style      harmonic
angle_style     harmonic
dihedral_style  opls
improper_style  harmonic
special_bonds   lj/coul 0.0 0.0 0.5

velocity        all create 300.0 12345 mom yes rot yes

fix             1 all nvt temp 300.0 300.0 100.0
timestep        1.0
thermo          100
thermo_style    custom step temp press etotal density
dump            1 all custom 1000 nvt.lammpstrj id type x y z

run             50000
write_restart   nvt.restart
```

---

## 7. 第六步：NPT 生产模拟

```lammps
# npt.in
read_restart    nvt.restart

pair_style      lj/cut/coul/long 10.0 12.0
pair_modify     mix geometric
kspace_style    pppm 1.0e-4
include         system.params
bond_style      harmonic
angle_style     harmonic
dihedral_style  opls
improper_style  harmonic
special_bonds   lj/coul 0.0 0.0 0.5

fix             1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
timestep        1.0
thermo          1000
thermo_style    custom step temp press density etotal
dump            1 all custom 5000 npt.lammpstrj id type x y z

run             1000000
write_restart   production.restart
write_data      production.data
```

---

## 8. EMC Setup 关键参数速查表

| Setup 命令 | 功能 | 默认值 | 常用值 |
|-----------|------|--------|--------|
| `-field=opls-aa` | 力场选择 | — | opls-aa, charmm/c36a, pcff |
| `-density=0.9` | 目标密度 (g/cc) | 1.0 | 0.6–1.5 取决于材料 |
| `-cut=10.0` | 对偶截断 (Å) | 9.5 | 10.0–15.0 |
| `-charge_cut=10.0` | 电荷截断 (Å) | 9.5 | 10.0–15.0 |
| `-dtdump=5000` | dump 频率 | 100000 | 1000–10000 |
| `-dtthermo=1000` | thermo 频率 | 1000 | 100–10000 |
| `-dtrestart=50000` | restart 频率 | 100000 | 10000–100000 |
| `-emc_execute` | 自动执行 EMC | false | true |

---

## 9. 力场与 LAMMPS 设置速查

| EMC 力场 | pair_style | bond_style | kspace | special_bonds |
|---------|-----------|------------|--------|---------------|
| OPLS-AA/UA | `lj/cut/coul/long` | `harmonic` | `pppm` | `lj/coul 0.0 0.0 0.5` |
| CHARMM | `lj/charmm/coul/long` | `harmonic` | `pppm` | `lj/coul 0.0 0.0 0.5` |
| PCFF/COMPASS | `lj/class2/coul/long` | `class2` | `pppm` | `lj/coul 0.0 0.0 0.5` |
| TraPPE | `lj/cut/coul/long` | `harmonic` | `pppm` | `lj/coul 0.0 0.0 0.5` |

---

## 10. 常见问题排查

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| EMC Setup 报错 "unknown molecule" | 化学名称拼写错误 | 检查分子名称（water, ethanol, polyethylene 等） |
| EMC 构建报 "density too high" | 目标密度不现实 | 降低 `-density` 或减少分子数 |
| LAMMPS 报 "Out of range atoms" | 最小化不够充分 | 增大 minim 的 `maxiter` |
| LAMMPS 报 "lost atoms" | 原子运动出盒子 | 使用 `fix nve/limit` 或增大盒子 |
| 密度不收敛 | Pdamp 设置不当 | 调整 Pdamp 或用 Berendsen 先 |

---

## 11. 验证状态

* ✅ EMC 和 LAMMPS 均在服务器上可用
* ✅ EMC 版本确认为 9.4.4 (Jul 21 2026)
* ✅ 服务器 LAMMPS 版本确认为 7 Feb 2024 - Update 1
* ✅ 服务器上有用户已验证的示例 (simple-water-ethanol)
* ⬜ 本机端到端运行验证

---

## 12. 相关页面

- [最小化流程](../10_simulation_workflows/minimization.md)
- [NVT 平衡](../10_simulation_workflows/nvt.md)
- [NPT 模拟](../10_simulation_workflows/npt.md)
- [单位映射](units_mapping.md)
- [力场清单](../05_force_fields/emc_force_field_inventory.md)
- [Style 映射](style_mapping.md)
- 文件映射（待创建）

## 官方来源

- **官方标题：** EMC Setup Manual v9.4.4 and LAMMPS Documentation — workflow references
- **官方章节：** EMC Setup / LAMMPS export workflow；LAMMPS documentation
- **官方 URL：** https://montecarlo.sourceforge.net/emc/Welcome.html
- **本地来源：** `sources/emc/emc_manual.pdf`；`/opt/emc-9.4.4/scripts/emc2lammps.emc`（服务器安装路径）
- **适用版本：** EMC 9.4.4 (Jul 21 2026)；LAMMPS 22 Jul 2025 - Update 4（本地）/ 7 Feb 2024 - Update 1（服务器）
- **核对日期：** 2026-07-27
- **内容说明：** 本章为编者整理的工作流指南，结合官方文档与实践建议编写。
