# EMC 建模：均聚物体系

* **EMC 版本：** 9.4.4
* **EMC Setup 版本：** 5.3
* **官方来源：** EMC 手册第 4.6.2.4 节 (Polymers)

---

## 1. 概述

EMC 支持多种聚合物建模方式：均聚物 (homopolymer)、随机共聚物 (random copolymer)、交替共聚物 (alternating copolymer)、嵌段共聚物 (block copolymer)。通过 EMC Setup，可以在命令行直接指定链长和链数。

---

## 2. 从空文件写聚乙烯体系

### 2.1 完整的 EMC Setup 命令

```bash
perl /opt/emc-9.4.4/scripts/emc.pl \
  -field=opls-aa \
  -density=0.85 \
  polyethylene_melt 1 50 polyethylene:100
```

**逐行讲解：**

| 参数 | 含义 | 可修改？ | 修改依据 |
|------|------|:------:|---------|
| `-field=opls-aa` | OPLS-AA 力场 | 是 | 可选 `pcff`, `trappe`, `charmm/c36a` 等 |
| `-density=0.85` | 目标密度 0.85 g/cm³ | 是 | 聚乙烯熔体 ~0.78–0.87 g/cm³（取决于温度） |
| `polyethylene_melt` | 项目名 | 是 | 任意字符串 |
| `1` | 单相体系 | **否** | 多相体系才需要改 |
| `50` | 链数 | 是 | 根据目标体系大小和计算资源 |
| `polyethylene:100` | 聚合物名:聚合度 | 是 | `polyethylene` 是 EMC 内建名；`100` 是每条链的重复单元数 |

### 2.2 EMC 内建聚合物名称

| 聚合物名 | 单体 | 力场 |
|---------|------|------|
| `polyethylene` | -(CH₂-CH₂)- | OPLS, PCFF, TraPPE |
| `polypropylene` | -(CH₂-CH(CH₃))- | OPLS, PCFF |
| `polystyrene` | -(CH₂-CH(Ph))- | OPLS |
| `polybutadiene` | -(CH₂-CH=CH-CH₂)- | OPLS |
| `polyisoprene` | -(CH₂-C(CH₃)=CH-CH₂)- | OPLS |
| `poly(methyl-methacrylate)` / `pmma` | -(CH₂-C(CH₃)(COOCH₃))- | OPLS |
| `polyethylene-oxide` / `peo` | -(CH₂-CH₂-O)- | OPLS |
| `nylon-6` | -(NH-(CH₂)₅-CO)- | OPLS |
| `polyethylene-terephthalate` / `pet` | PET 重复单元 | OPLS-AA/UA |
| `polycarbonate` | PC 重复单元 | OPLS |
| `polydimethylsiloxane` / `pdms` | -(Si(CH₃)₂-O)- | OPLS |

> **编者注：** 完整的内建聚合物列表取决于力场。EMC 的力场目录（`/opt/emc-9.4.4/field/`）中可能包含更多聚合物定义。使用 `-field=opls-aa` 时，EMC 会从 `./field/opls/2012/opls-aa/` 中查找聚合物拓扑。

---

## 3. 链长（聚合度）设置

### 语法

```bash
polymer:N          # N = 重复单元数
polymer:N:M        # N-M = 重复单元数范围（随机）
```

### 示例

```bash
# 固定链长：50 条链，每条 200 个重复单元
50 polyethylene:200

# 分散链长：50 条链，链长在 80-120 之间均匀分布
50 polyethylene:80:120

# 质量分布：50 条链，使用质量分布（PDI 控制）
-mass 50 polyethylene:80:120
```

---

## 4. 完整工作流

### 4.1 Setup

```bash
perl /opt/emc-9.4.4/scripts/emc.pl \
  -field=opls-aa \
  -density=0.85 \
  -cut=12.0 \
  -lammps_dtdump=5000 \
  -lammps_dtthermo=1000 \
  pe_melt 1 50 polyethylene:200
```

### 4.2 构建

```bash
cd pe_melt/build
emc -nthreads=8 build.emc
```

### 4.3 检查输出

```bash
# 检查链数
grep "atoms" system.data
# 50 chains × 200 monomers × 6 atoms = 60000 atoms (PE: -CH₂-CH₂-, 每个单体 6 atoms)

# 检查键数
grep "bonds" system.data
```

### 4.4 最小化

```lammps
# minim.in
units           real
atom_style      full
read_data       system.data

pair_style      lj/cut/coul/long 12.0 14.0
kspace_style    pppm 1e-4
include         system.params

bond_style      harmonic
angle_style     harmonic
dihedral_style  opls

special_bonds   lj/coul 0.0 0.0 0.5

min_style       cg
minimize        1e-4 1e-6 2000 20000
write_data      minimized.data
```

> **编者注：** 聚合物体系比小分子体系更难最小化，因为长链容易缠绕。建议使用更多的迭代次数（2000+）和更保守的限制。

### 4.5 NVT 平衡

```lammps
read_data       minimized.data
# 力场设置同上 ...
velocity        all create 500.0 12345 mom yes rot yes
fix             1 all nvt temp 500.0 300.0 100.0   # 从 500K 冷却到 300K
timestep        1.0
thermo          1000
run             100000
write_restart   nvt.restart
```

### 4.6 NPT 密度平衡

```lammps
read_restart    nvt.restart
# 力场设置同上 ...
fix             1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
run             200000
# 观察密度是否稳定
```

### 4.7 生产模拟

```lammps
fix             1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
dump            1 all custom 5000 pe_prod.lammpstrj id type x y z
run             1000000
write_restart   production.restart
```

---

## 5. 聚合物模拟的特殊考虑

### 5.1 密度设置

EMC 构建时设置的密度 (`-density`) 只是**初始密度**。NPT 平衡后密度会自动调整到力场对应的平衡密度。

- 设定值偏离平衡值太多 → 盒子可能需要很长时间才能平衡
- 设定值太离谱 → 原子重叠，最小化失败

**建议：** 对于聚乙烯 OPLS-AA：
- T=300K → `-density=0.85`
- T=400K → `-density=0.80`
- T=500K → `-density=0.75`

### 5.2 timestep

聚合物模拟中 C-H 键振动是最高频运动。OPLS-AA 使用约束氢原子（bond type 固定）：

- 无 SHAKE 约束：`timestep 0.5` fs
- 使用 SHAKE 约束 H 键：`timestep 1.0` fs
- 使用 SHAKE 约束所有键（粗粒化模拟）：`timestep 2.0` fs

### 5.3 平衡时间

聚合物的弛豫时间远长于小分子。一般规则：

- 链长 < 50：50–100 ns 足够
- 链长 50–200：200–500 ns
- 链长 > 200：可能需要 μs 级别

**编者注：** 对于均聚物熔体，Rouse 时间 τ_R ∝ N²。通过检查链的均方末端距和回转半径是否稳定来判断是否平衡。

---

## 6. 常见错误

| 错误 | 原因 | 解决方法 |
|------|------|---------|
| EMC Setup: "unknown polymer: xxx" | 聚合物名不在库中 | 检查可用聚合物列表 |
| 最小化: "Lost atoms" | 聚合物缠绕太紧密 | 减小密度或增大盒子 |
| NPT: 密度不收敛 | Pdamp 不合适 | 增大 Pdamp 或先用 Berendsen |
| 温度失控 | 重叠原子释放势能 | 更充分的最小化 |

---

## 7. 与 LAMMPS 的关系

EMC 生成的聚合物体系输出包含：

- `system.data`: 每个链是一个 molecule（`molecule-ID` 区分链）
- `system.params`: harmonic bond/angle + opls dihedral
- 对于 PCFF 力场使用 `class2` bond/angle/dihedral style

---

## 8. 验证状态

* ✅ 官方文档翻译
* ✅ 服务器 EMC 可用
* ⬜ 未端到端验证

---

## 9. 相关页面

- [小分子建模](molecules.md)
- 共聚物建模（待创建）
- 混合物建模（待创建）
- [EMC→LAMMPS 工作流](../09_emc_to_lammps/complete_workflow.md)

## 官方来源

- **官方标题：** EMC Setup Manual v9.4.4 — Simulation Setup: Polymers
- **官方章节：** 4.6.2.4 Polymers
- **官方 URL：** https://montecarlo.sourceforge.net/emc/Welcome.html
- **本地来源：** `sources/emc/emc_manual.pdf`（服务器路径：`/opt/emc-9.4.4/docs/emc.pdf`）
- **适用版本：** EMC 9.4.4 (Jul 21 2026)；EMC Setup 5.3
- **核对日期：** 2026-07-27
