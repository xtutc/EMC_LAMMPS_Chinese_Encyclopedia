# EMC 力场清单与 LAMMPS 映射表

* **EMC 版本：** 9.4.4
* **LAMMPS 版本：** 22 Jul 2025 - Update 4
* **官方来源：** [EMC Welcome](https://montecarlo.sourceforge.net/emc/Welcome.html), [EMC Features](https://montecarlo.sourceforge.net/emc/Features.html)
* **翻译状态：** 完整

---

## 1. EMC 支持的 Atomistic 力场

| 力场名称 | 完整名称 | 适用体系 | Typing 方式 | LAMMPS units | LAMMPS pair_style | 状态 |
|---------|---------|---------|------------|-------------|-----------------|------|
| **OPLS-AA** | Optimized Potentials for Liquid Simulations - All Atom | 有机分子、聚合物、液体 | EMC 自动 typing | `real` | `lj/cut/coul/long` | 官方确认 |
| **OPLS-UA** | OPLS - United Atom | 有机分子、聚合物（联合原子） | EMC 自动 typing | `real` | `lj/cut/coul/long` | 官方确认 |
| **CHARMM c36a** | Chemistry at HARvard Macromolecular Mechanics | 蛋白质、脂质、水+离子 | EMC 自动 typing | `real` | `lj/charmm/coul/long` | 官方确认 |
| **CHARMM c32b** | CHARMM 旧版本 | 蛋白质、脂质 | EMC 自动 typing | `real` | `lj/charmm/coul/long` | 官方确认 |
| **CGENFF** | CHARMM General Force Field | 药物类小分子 | EMC 自动 typing | `real` | `lj/charmm/coul/long` | CHARMM c36a 子集 |
| **PCFF** | Polymer Consistent Force Field | 聚合物 | EMC 自动 typing | `real` | `lj/class2/coul/long` | 官方确认 |
| **COMPASS** | Condensed-phase Optimized Molecular Potentials for Atomistic Simulation Studies | 凝聚态材料 | EMC 自动 typing | `real` | `lj/class2/coul/long` | 官方确认 |
| **TraPPE** | Transferable Potentials for Phase Equilibria | 有机分子相平衡 | EMC 自动 typing | `real` | `lj/cut/coul/long` | 官方确认 |
| **Born** | Born 模型势 | 金属氧化物 | EMC 自动 typing | `real` 或 `metal` | 视具体实现 | 官方确认 |

### 1.1 OPLS-AA/UA 力场细节

- **来源：** 2012 年版本，另有 2024 年更新版本
- **文件位置（EMC）：** `./field/opls/2012/opls-aa/` 和 `./field/opls/2012/opls-ua/`
- **水模型：** 适配 TIPnP 系列水模型
- **修改记录：**
  - 2016.08.19：修正酯和酰亚胺规则
  - 2016.12.20：修正 OPLS 扭转参数转换问题
  - OPLS-UA 适配 PET 正确表示

### 1.2 CHARMM 力场细节

- **文件位置：** `./field/charmm/c36a/` 和 `./field/charmm/c32b/`
- **CGENFF：** 位于 `./field/charmm/c36a/cgenff/`
- **修改记录：**
  - 添加（聚）环氧丙烷的键合贡献

---

## 2. EMC 支持的 Coarse-Grained 力场

| 力场名称 | 完整名称 | Typing 方式 | LAMMPS units | LAMMPS pair_style | 状态 |
|---------|---------|-----------|-------------|-----------------|------|
| **DPD** | Dissipative Particle Dynamics | 用户自行 typing | `lj` | `dpd` | 官方确认 |
| **MARTINI2** | Martini 粗粒化力场 v2 | **用户自行 typing** | `real` 或 `nano` | 用户自定义 | 官方确认 |
| **MARTINI3** | Martini 粗粒化力场 v3 | **用户自行 typing** | `real` 或 `nano` | 用户自定义 | 基本功能已添加 |
| **SDK** | Shinoda-Devane-Klein | **用户自行 typing** | `lj` | `lj/sdk` | 官方确认 |
| **Colloidal** | 胶体力场 | **用户自行 typing** | `lj` | `colloid` | 官方确认 |

> **警告：** MARTINI、SDK 和 DPD 的 typing 不能由 EMC 自动完成，需要用户自行指定。EMC 只提供结构构建，力场参数映射需要外部提供。

---

## 3. 每种力场的完整 LAMMPS 对应关系

### 3.1 OPLS-AA

```
EMC 力场：OPLS-AA
├── LAMMPS units:        real
├── atom_style:          full
├── pair_style:          lj/cut/coul/long 10.0 12.0
├── bond_style:          harmonic
├── angle_style:         harmonic
├── dihedral_style:      opls
├── improper_style:      harmonic (或 cvff)
├── kspace_style:        pppm 1e-4
├── special_bonds:       lj/coul 0.0 0.0 0.5
└── package:             MOLECULE, KSPACE
```

### 3.2 CHARMM c36a

```
EMC 力场：CHARMM c36a
├── LAMMPS units:        real
├── atom_style:          full
├── pair_style:          lj/charmm/coul/long 10.0 12.0
├── bond_style:          harmonic
├── angle_style:         charmm
├── dihedral_style:      charmm
├── improper_style:      harmonic
├── kspace_style:        pppm 1e-4
├── special_bonds:       lj/coul 0.0 0.0 0.5
└── package:             MOLECULE, KSPACE
```

### 3.3 PCFF / COMPASS

```
EMC 力场：PCFF 或 COMPASS
├── LAMMPS units:        real
├── atom_style:          full
├── pair_style:          lj/class2/coul/long 10.0
├── bond_style:          class2
├── angle_style:         class2
├── dihedral_style:      class2
├── improper_style:      class2
├── kspace_style:        pppm 1e-4
├── special_bonds:       lj/coul 0.0 0.0 0.5
└── package:             CLASS2, MOLECULE, KSPACE
```

**编者注：** CLASS2 力场（PCFF、COMPASS）使用更复杂的势能函数，包括键-键耦合和键-角耦合项。LAMMPS 的 `class2` style 支持这些耦合项。

---

## 4. 力场文件位置（EMC 安装目录结构）

```
./field/
├── born/           Born 力场参数
├── charmm/          CHARMM 力场（c32b, c36a, cgenff）
├── compass/         COMPASS 力场
├── dpd/             DPD 力场参数
├── martini/         MARTINI2, MARTINI3
├── opls/            OPLS（AA, UA, 2012, 2024）
├── pcff/            PCFF 力场
├── sdk/             SDK 力场
└── trappe/          TraPPE 力场
```

每种力场目录下包含：
- `.top` 文件：拓扑（原子类型定义、连接规则）
- `.prm` 文件：参数（力常数、平衡值）

---

## 5. 力场选择建议

| 体系 | 推荐力场 | 原因 |
|------|---------|------|
| 有机小分子液体 | OPLS-AA 或 TraPPE | 最好的验证和测试 |
| 生物分子（蛋白质/脂质） | CHARMM c36a | 生物分子标准 |
| 聚合物（通用） | OPLS-AA 或 PCFF | EMC 很好的验证 |
| 聚合物（精确） | PCFF 或 COMPASS | 包含耦合项 |
| 药物分子 | CGENFF | CHARMM 兼容 |
| 金属氧化物 | Born | 专为此设计 |
| 介观尺度（粗粒化） | DPD 或 MARTINI | 粗粒化标准 |
| 粗粒化脂质双层 | MARTINI2/3 | 粗粒化生物膜 |

---

## 6. 本机可用性

| LAMMPS style | 本机是否可用 |
|-------------|----------|
| `lj/cut/coul/long` | ✅ (KSPACE package) |
| `lj/charmm/coul/long` | ✅ |
| `lj/class2/coul/long` | ✅ (CLASS2 package) |
| `class2` (bond/angle/dihedral) | ✅ |
| `harmonic` (bond/angle/dihedral) | ✅ |
| `opls` (dihedral) | ✅ |
| `charmm` (dihedral) | ✅ |
| `pppm` (kspace) | ✅ |
| `dpd` (pair) | ✅ (DPD-BASIC package) |
| `colloid` (pair) | ✅ (COLLOID package) |

---

## 7. 验证状态

* ✅ 资料收集（来自 EMC 官方网站）
* ✅ LAMMPS style 可用性检查
* ⬜ EMC 实际 force field typing 验证
* ⬜ 短模拟验证

---

## 8. 相关页面

- [力场基础](fundamentals.md)
- [EMC→LAMMPS 单位映射](../09_emc_to_lammps/units_mapping.md)
- [EMC→LAMMPS Style 映射](../09_emc_to_lammps/style_mapping.md)
- [EMC Setup 总览](../02_emc_setup_reference/setup_overview.md)
