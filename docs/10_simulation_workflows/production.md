# 生产模拟与续算流程

* **LAMMPS 22 Jul 2025 - Update 4** | **翻译状态：** 完整

---

## 生产模拟 (Production Run)

### 完整 NPT 生产脚本

```lammps
units real; atom_style full
read_restart npt_equil.restart
# 力场必须重新声明
pair_style lj/cut/coul/long 10.0 12.0
kspace_style pppm 1e-4; include system.params
bond_style harmonic; angle_style harmonic
dihedral_style opls; special_bonds lj/coul 0.0 0.0 0.5

timestep 1.0
fix 1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0

thermo 5000
thermo_style custom step temp press density etotal vol

dump traj all custom 10000 prod.lammpstrj id type x y z
dump xyz all xyz 10000 prod.xyz
restart 50000 prod.restart

run 5000000    # 5 ns
write_restart final.restart
write_data final.data
```

---

## 续算 (Restart)

### 从 restart 文件续算

```lammps
read_restart prod.restart
# 重新声明力场 ← 必须！
pair_style lj/cut/coul/long 10.0 12.0
kspace_style pppm 1e-4; include system.params
# 重新声明 fix
fix 1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
# 重新声明 dump, thermo
dump 1 all custom 10000 prod2.lammpstrj id type x y z
run 5000000
```

> **警告：** read_restart 后**必须**重新声明 `pair_style`、`kspace_style`、`fix`、`dump`、`thermo`。restart 文件只保存原子数据，不保存命令设置。

### write_restart 频率建议

| 模拟长度 | restart 频率 |
|---------|------------|
| < 1 ns | 每 100,000 步 |
| 1–10 ns | 每 500,000 步 |
| > 10 ns | 每 1,000,000 步 |

---

## 平衡判断标准

| 物理量 | 平衡标志 |
|--------|---------|
| 温度 | 围绕目标值波动 ±2%，无趋势 |
| 压力 | 围绕目标值波动 ±50 atm，无趋势 |
| 密度 | 稳定 ±0.5% |
| 总能量 | 稳定 ±1% |
| 势能 | 稳定 ±2% |

---

## 验证： [NVT](nvt.md) | [NPT](npt.md) | [加热](heating.md)

## 官方来源

- **官方标题：** LAMMPS Documentation — Howto discussions
- **官方章节：** LAMMPS 官方文档 Howto 部分中关于 NVT、NPT 模拟的说明
- **官方 URL：** https://docs.lammps.org/Howto.html
- **本地来源：** LAMMPS 本地安装内置示例（`/opt/homebrew/share/lammps/examples/`）
- **适用版本：** LAMMPS 22 Jul 2025 - Update 4
- **核对日期：** 2026-07-27
- **内容说明：** 本章为编者整理的模拟流程实践指南，结合官方文档与编者经验编写。
