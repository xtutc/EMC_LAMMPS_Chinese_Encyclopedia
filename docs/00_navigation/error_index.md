# 错误信息索引

> 本索引按错误信息关键字组织，可快速定位问题和解决方案。

---

## EMC 错误

### EMC Setup 错误

| 错误信息 | 可能原因 | 解决方法 | 参考页面 |
|---------|---------|---------|---------|
| `unknown molecule: xxx` | 分子名不在 EMC 库中 | 检查内建分子列表，或用 SMILES 自定义 | [小分子建模](../04_emc_modeling/molecules.md) |
| `unknown polymer: xxx` | 聚合物名不在 EMC 库中 | 检查力场目录中可用聚合物 | [聚合物建模](../04_emc_modeling/homopolymers.md) |
| `density too high` | 初始密度不现实 | 降低 `-density` 或减少分子/链数 | [EMC Setup](../02_emc_setup_reference/setup_overview.md) |
| `cannot find field: xxx` | 力场目录不存在 | 检查力场名拼写和 `.top`/`.prm` 文件 | [力场清单](../05_force_fields/emc_force_field_inventory.md) |
| `unsupported SMILES: xxx` | SMILES 无法被力场 typing | 检查原子是否在力场参数范围内 | [小分子建模](../04_emc_modeling/molecules.md) |
| `cannot type atom: xxx` | 力场缺少对应原子类型 | 检查力场参数文件是否包含目标原子类型 | [力场清单](../05_force_fields/emc_force_field_inventory.md) |

### EMC 主程序错误

| 错误信息 | 可能原因 | 解决方法 |
|---------|---------|---------|
| `Error: system too dense` | MC 采样找不到可行插入位置 | 降低密度或使用更大的盒子 |
| `Error: out of memory` | 体系太大 | 减少原子数或使用更多内存的机器 |
| `Error: cannot open file xxx` | 文件不存在或权限问题 | 检查文件路径和权限 |
| `Warning: MC not converging` | MC 采样效率低 | 增加 `-nthreads` 或调整 MC 参数 |

---

## LAMMPS 初始化错误

| 错误信息 | 可能原因 | 解决方法 | 参考页面 |
|---------|---------|---------|---------|
| `ERROR: Cannot open input script xxx` | 文件不存在 | 检查路径和文件名 | [CLI 选项](../06_lammps_user_guide_translation/running/lammps_cli_options.md) |
| `ERROR: Unknown command: xxx` | 命令不存在/package 未安装 | 检查命令名拼写，确认 package 已安装 | [已安装 Packages](../06_lammps_user_guide_translation/running/lammps_cli_options.md#已安装的-packages) |
| `ERROR: Illegal units command` | `units` 命令语法错误 | 检查 units 拼写 | [单位映射](../09_emc_to_lammps/units_mapping.md) |
| `ERROR: Unknown atom style: xxx` | `atom_style` 不支持 | 检查可用的 atom_style | [输入脚本语法](../06_lammps_user_guide_translation/input_scripts/input_script_syntax.md) |
| `ERROR: All pair coeffs are not set` | 缺少某些原子类型的 pair_coeff | 检查 pair_coeff 覆盖所有对 | [Data 文件格式](../08_lammps_file_formats/data_file.md) |

---

## LAMMPS data 文件错误

| 错误信息 | 可能原因 | 解决方法 | 参考页面 |
|---------|---------|---------|---------|
| `ERROR: Unexpected end of data file` | 文件被截断 | 检查文件完整性 | [Data 文件格式](../08_lammps_file_formats/data_file.md) |
| `ERROR: Incorrect atom format in data file` | atom_style 与列数不匹配 | 检查 atom_style 和各段列数 | 同上 |
| `# of atoms in header not equal to # in body` | header 数与实际不一致 | 统计并修正 | 同上 |
| `ERROR: Did not find all elements in Masses table` | 缺少某些原子类型的质量 | 补充 Masses 段 | 同上 |
| `ERROR: Incorrect bond format` | Bonds 段格式错误 | 检查每行是否有 4 个整数 | 同上 |

---

## LAMMPS 运行时错误

### 几何/坐标错误

| 错误信息 | 可能原因 | 解决方法 |
|---------|---------|---------|
| `ERROR: Lost atoms: original N current M` | 原子运动出盒子（非周期边界） | 增大盒子、用 `fix nve/limit` 或 `fix enforce2d` |
| `ERROR: Out of range atoms - cannot compute PPPM` | 原子超出长程计算网格 | 增大盒子、减小 PPPM 精度要求 |
| `ERROR: Non-numeric atom coords` | 坐标变成 NaN/Inf | 初始结构有问题，检查是否存在过大势能/原子重叠 |
| `ERROR: Bond/angle/dihedral atoms missing` | 拓扑中引用不存在的原子 | 检查 data 文件的键/角/二面角段 |
| `ERROR: Bond extent > half of periodic box length` | 键跨越了半个盒子以上（PBC 问题） | 检查分子初始构型，可能需要 unwrap |

### 力场/参数错误

| 错误信息 | 可能原因 | 解决方法 |
|---------|---------|---------|
| `ERROR: Incorrect args for pair coefficients` | pair_coeff 参数个数不对 | 检查 pair_style 要求的参数个数 |
| `ERROR: KSpace style is incompatible with Pair style` | kspace_style 不兼容 pair_style | 参考力场对应的设置 |
| `ERROR: Pair style requires a KSpace style` | 缺少 kspace_style | 添加 `kspace_style pppm 1e-4` |
| `ERROR: All pair coeffs are not set` | 缺少某些原子类型对 | 检查所有类型是否都被覆盖 |

### 最小化错误

| 错误信息 | 可能原因 | 解决方法 |
|---------|---------|---------|
| `WARNING: Energy is not going down` | 无法找到能量下降方向 | 尝试 `min_style sd` 先粗优化 |
| `ERROR: Lost atoms during minimization` | 最小化导致原子飞出 | 使用 `fix nve/limit` 限制最大位移 |
| `Stopping: energy tolerance` | 正常停止（能量收敛） | ✅ 成功 |
| `Stopping: force tolerance` | 正常停止（力收敛） | ✅ 成功 |

### 分子动力学错误

| 错误信息 | 可能原因 | 解决方法 |
|---------|---------|---------|
| `ERROR: Shake atoms missing` | SHAKE 约束的原子不完整 | 检查 H 原子是否全部定义 |
| `ERROR: Temperature control must be defined before velocity` | fix 在 velocity 之后 | 调整命令顺序 |
| `ERROR on proc N: Out of range atoms` | 某些原子坐标无效 | 减小 timestep、增强最小化 |
| `WARNING: Temperature is not being computed` | group 没有平移自由度 | 检查 group 定义 |

---

## 性能/编译错误

| 错误信息 | 可能原因 | 解决方法 |
|---------|---------|---------|
| `ERROR: Cannot use pair style with KOKKOS` | KOKKOS 包未安装或未启用 | 使用非 KOKKOS 的 pair style |
| `ERROR: GPU package not installed` | 无 GPU 支持 | 使用 CPU 版本 |
| `ERROR: Must use 'kspace_modify pressure/scalar no'` | 要求标量压力计算 | 添加 `kspace_modify pressure/scalar no` |

---

## 常见警告

| 警告信息 | 严重性 | 处理建议 |
|---------|:------:|---------|
| `WARNING: Using a manybody potential with bonds/angles and special_bonds` | ⚠️ 中 | 检查 special_bonds 设置 |
| `WARNING: System is not charge neutral` | ⚠️ 中 | PPPM 需要净零电荷或特殊设置 |
| `WARNING: No fixes defined, atoms are not moving` | ⚠️ 低 | 添加系综 fix（NVE/NVT/NPT） |
| `WARNING: Communication cutoff is less than neighbor skin` | ⚠️ 低 | 增大 neighbor skin 或减小 communication cutoff |

---

## 调试建议

1. **先用 `-skiprun` 做静态检查**：`lmp_serial -skiprun -in test.in`
2. **使用 `-echo screen` 查看执行流程**：`lmp_serial -echo screen -in test.in`
3. **逐步添加命令**：从最小脚本开始，逐个添加命令
4. **检查 log 文件中的 CPU 时间和热力学量**：关注不正常的温度/压力/能量跳跃
5. **使用 OVITO 可视化初始构型**：确认结构合理

---

## 相关页面

- [LAMMPS 命令行参数](../06_lammps_user_guide_translation/running/lammps_cli_options.md)
- [Data 文件格式](../08_lammps_file_formats/data_file.md)
- [输入脚本语法](../06_lammps_user_guide_translation/input_scripts/input_script_syntax.md)
- [最小化流程](../10_simulation_workflows/minimization.md)
- [EMC→LAMMPS 工作流](../09_emc_to_lammps/complete_workflow.md)
