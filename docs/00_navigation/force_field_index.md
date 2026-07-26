# 力场索引

> **适用版本：** EMC 9.4.4；LAMMPS 22 Jul 2025 - Update 4
> **索引状态：** EMC 参数名称以项目现有官方手册摘录和力场清单为准。

本页按力场名称定位本项目已涉及的 EMC 力场资料。力场适用性取决于具体
参数集和化学类型；下表仅作为索引，不替代参数化或验证。

## 已涉及的力场

| 力场名称 | 缩写 | EMC 中的参数名称或标识 | 适用材料/原子类型 |
|---|---|---|---|
| Optimized Potentials for Liquid Simulations—All Atom | OPLS-AA | `opls-aa` | 有机小分子、液体、聚合物的全原子表示。 |
| Optimized Potentials for Liquid Simulations—United Atom | OPLS-UA | `opls-ua` | 有机分子与聚合物的联合原子表示。 |
| Chemistry at HARvard Macromolecular Mechanics | CHARMM | `charmm`；可使用如 `charmm/c36a` 的具体标识 | 蛋白质、脂质、水、离子与相关生物分子。 |
| Assisted Model Building with Energy Refinement / General AMBER Force Field | AMBER/GAFF | 当前 EMC 9.4.4 力场清单未列出独立参数名称 | 生物分子与一般有机小分子；本项目仅在力场基础分类中涉及。 |
| Polymer Consistent Force Field | PCFF | `pcff` | 聚合物及其全原子、Class II 表示。 |
| Condensed-phase Optimized Molecular Potentials for Atomistic Simulation Studies | COMPASS | `compass`（项目清单中的 EMC 目录名；`-field` 值待逐项核对） | 凝聚态材料与聚合物的 Class II 表示。 |
| Transferable Potentials for Phase Equilibria—United Atom | TraPPE-UA | `trappe` | 有机分子相平衡和联合原子模型。 |

## 相关页面

- [力场基础](../05_force_fields/fundamentals.md)：力场分类、势函数与选择原则。
- [EMC 力场清单与 LAMMPS 映射表](../05_force_fields/emc_force_field_inventory.md)：EMC 支持的力场、目录与 LAMMPS 样式映射。

## 说明

- `AMBER/GAFF` 的 EMC 参数名称在当前项目的 EMC 9.4.4 力场清单中未给出，不能据此推断为可由 EMC 自动 typing。
- CHARMM 的具体标识依赖所选参数集；应在对应官方资料中核对完整路径和版本。
- PCFF、COMPASS 等 Class II 力场的交叉耦合项需要与 LAMMPS 的 `class2` 样式兼容。
- 力场选择、原子类型分配和参数覆盖的限制，请以相关页面记录的官方来源为准。

## 维护说明

- 新建力场页面时，应在本索引增加名称、缩写、EMC 标识和适用范围。
- 若官方资料未给出参数名称，应标记“官方资料未给出”，不得用经验推定。
