# EMC → LAMMPS Style 映射表

* **EMC 9.4.4** | **LAMMPS 22 Jul 2025 / 7 Feb 2024**

---

## Pair Style

| EMC 力场 | LAMMPS pair_style | cutoff |
|---------|-------------------|--------|
| OPLS-AA/UA | `lj/cut/coul/long` | 10.0 12.0 |
| CHARMM c36a/c32b | `lj/charmm/coul/long` | 10.0 12.0 |
| CGENFF | `lj/charmm/coul/long` | 10.0 12.0 |
| PCFF | `lj/class2/coul/long` | 10.0 |
| COMPASS | `lj/class2/coul/long` | 10.0 |
| TraPPE | `lj/cut/coul/long` | 10.0 12.0 |
| Born | `born/coul/long` | 视情况 |
| DPD | `dpd` | ~1.0 (lj) |
| SDK | `lj/sdk/coul/long` | 视情况 |
| MARTINI | `lj/cut/coul/long` | 11.0 |

## Bond/Angle/Dihedral/Improper Style

| EMC 力场 | bond_style | angle_style | dihedral_style | improper_style |
|---------|-----------|-------------|----------------|----------------|
| OPLS-AA/UA | `harmonic` | `harmonic` | `opls` | `harmonic` |
| CHARMM | `harmonic` | `charmm` | `charmm` | `harmonic` |
| PCFF/COMPASS | `class2` | `class2` | `class2` | `class2` |
| TraPPE | `harmonic` | `harmonic` | `opls` | `harmonic` |

## 其他核心设置

| 设置 | OPLS/CHARMM/TraPPE | PCFF/COMPASS | DPD |
|------|-------------------|-------------|-----|
| kspace_style | `pppm 1e-4` | `pppm 1e-4` | — |
| special_bonds | `lj/coul 0.0 0.0 0.5` | `lj/coul 0.0 0.0 0.5` | — |
| units | `real` | `real` | `lj` |
| atom_style | `full` | `full` | `atomic` |

---

## 验证状态

* ✅ 基于 EMC 官方信息，✅ LAMMPS style 可用性确认，⬜ 未全部运行验证

## 相关页面

- [力场清单](../05_force_fields/emc_force_field_inventory.md)
- [Units 映射](units_mapping.md)
- [完整工作流](complete_workflow.md)
