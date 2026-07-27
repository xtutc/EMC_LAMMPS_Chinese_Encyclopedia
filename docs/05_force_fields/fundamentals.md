# 力场基础

* **适用对象：** EMC + LAMMPS 用户
* **翻译状态：** 完整教程

---

## 1. 力场是什么

力场（Force Field）是分子模拟中势能函数及其参数的集合，定义了原子间相互作用的数学形式：

```
E_total = E_bond + E_angle + E_dihedral + E_improper + E_vdw + E_coulomb
```

| 项 | 物理含义 | 典型形式 |
|----|---------|---------|
| E_bond | 键伸缩能 | harmonic: k(r − r₀)² |
| E_angle | 键角弯曲能 | harmonic: k(θ − θ₀)² |
| E_dihedral | 二面角扭转能 | OPLS/CHARMM 多参数形式 |
| E_improper | 非正则二面角 | harmonic（保持平面性） |
| E_vdw | 范德华作用 | Lennard-Jones 12-6: 4ε[(σ/r)¹² − (σ/r)⁶] |
| E_coulomb | 静电作用 | qᵢqⱼ/(4πε₀r) |

---

## 2. 力场分类

### Class I（经典力场）
- OPLS、CHARMM、AMBER、TraPPE
- Harmonic bond/angle，无交叉耦合项
- **EMC 自动 typing 的主要力场类型**

### Class II（高级力场）
- PCFF、COMPASS、CFF
- 包含键-键、键-角交叉耦合项
- LAMMPS 中使用 `class2` style

### 粗粒化力场
- Martini、DPD、SDK
- 多原子合并为"珠子"
- **EMC 不自动 typing，需用户自行指定**

---

## 3. LAMMPS 中的力场实现

| EMC 力场 | LAMMPS pair_style | kspace_style | special_bonds |
|---------|-------------------|-------------|---------------|
| OPLS-AA/UA | `lj/cut/coul/long` | `pppm 1e-4` | `lj/coul 0.0 0.0 0.5` |
| CHARMM | `lj/charmm/coul/long` | `pppm 1e-4` | `lj/coul 0.0 0.0 0.5` |
| PCFF/COMPASS | `lj/class2/coul/long` | `pppm 1e-4` | `lj/coul 0.0 0.0 0.5` |
| TraPPE | `lj/cut/coul/long` | `pppm 1e-4` | `lj/coul 0.0 0.0 0.5` |
| DPD | `dpd` | — | — |
| SDK | `lj/sdk/coul/long` | `pppm` | 视情况 |

---

## 4. 力场选择指南

| 模拟体系 | 推荐力场 | 理由 |
|---------|---------|------|
| 有机小分子液体 | **OPLS-AA** | 最广泛验证 |
| 蛋白质/脂质 | **CHARMM c36a** | 生物大分子标准 |
| 聚合物（通用） | **OPLS-AA** | EMC 很好验证 |
| 聚合物（精确力学） | **PCFF** 或 **COMPASS** | 含交叉耦合项 |
| 相平衡 | **TraPPE** | 专门优化 |
| 药物分子 | **CGENFF** | CHARMM 兼容 |
| 金属氧化物 | **Born** | 专门设计 |
| 介观尺度 | **Martini** 或 **DPD** | 粗粒化标准 |

---

## 5. 力场文件结构 (EMC)

```
/opt/emc-9.4.4/field/
├── opls/2012/
│   ├── opls-aa/     ← .top (拓扑) + .prm (参数)
│   └── opls-ua/
├── charmm/c36a/     ← 含 cgenff 子目录
├── pcff/
├── compass/
├── trappe/
├── born/
├── dpd/
├── martini/
├── sdk/
└── uff/
```

---

## 6. 快速验证力场设置

```bash
# 1. 检查原子类型覆盖
grep "atom types" system.data
grep -c "pair_coeff" system.params

# 2. run 0 静态检查
lmp_serial -skiprun -in system.in

# 3. 检查电荷中性
grep "Atoms" -A 9999 system.data | awk '{sum+=$4} END {print sum}'
```

---

## 7. 验证状态

* ✅ 基于官方文档
* ✅ EMC 力场目录在服务器确认
* ⬜ 未端到端验证

## 8. 相关页面

- [EMC 力场清单](emc_force_field_inventory.md)
- [Units 映射](../09_emc_to_lammps/units_mapping.md)
- [EMC→LAMMPS 工作流](../09_emc_to_lammps/complete_workflow.md)

## 官方来源

- **官方标题：** EMC Features — Force Fields
- **官方章节：** EMC Supported Force Fields
- **官方 URL：** https://montecarlo.sourceforge.net/emc/Features.html
- **本地来源：** `sources/emc/emc_manual.pdf` 及相关力场目录
- **适用版本：** EMC 9.4.4 (Jul 21 2026)；LAMMPS 22 Jul 2025 - Update 4
- **核对日期：** 2026-07-27
- **内容说明：** 本章为编者根据多方资料整理的基础说明，部分内容属于编者注。
