# 升温与退火流程

* **适用版本：** LAMMPS 22 Jul 2025 - Update 4 | **翻译状态：** 完整

---

## 升温 (Heating)

### 方案 1：NVT 温度斜坡（最常用）

```lammps
# 最小化后，从 100K 升温到 300K
velocity all create 100.0 12345 mom yes rot yes
fix 1 all nvt temp 100.0 300.0 100.0
timestep 1.0
run 200000    # 升温速率 = 200K / 200ps = 1 K/ps
```

升温速率选择：

| 体系 | 推荐速率 | timestep | 步数 |
|------|---------|----------|------|
| 小分子 | 1–5 K/ps | 1 fs | 200K/200ps |
| 聚合物 | 0.1–1 K/ps | 1 fs | 200K/1ns |
| 粗粒化 | 0.01–0.1 K/ps | 5 fs | 200K/5ns |

### 方案 2：分步升温

```lammps
# 阶段 1: 100K → 200K
fix 1 all nvt temp 100.0 200.0 100.0
run 100000

# 阶段 2: 200K → 300K
fix 1 all nvt temp 200.0 300.0 100.0
run 100000
```

---

## 退火 (Annealing)

### 循环退火

```lammps
variable t equal 300
variable a loop 5
label loop
fix 1 all nvt temp 300.0 500.0 100.0
run 50000
fix 1 all nvt temp 500.0 300.0 100.0
run 50000
next a
jump SELF loop
```

### 使用 fix nve + fix langevin

```lammps
fix 1 all nve
fix 2 all langevin 300.0 500.0 100.0 12345
run 100000
```

---

## NVE 验证（能量守恒检查）

```lammps
velocity all create 300.0 12345
fix 1 all nve
timestep 0.5        # 更小步长保证能量守恒
thermo 10
run 10000
# 观察总能量 etotal 是否漂移
```

---

## 验证状态

* ✅ 官方资料翻译 | ⬜ 未运行

## 相关： [NVT](nvt.md) | [NPT](npt.md) | [生产](production.md)

## 官方来源

- **官方标题：** LAMMPS Documentation — Howto discussions
- **官方章节：** LAMMPS 官方文档 Howto 部分中关于 NVT、NPT 模拟的说明
- **官方 URL：** https://docs.lammps.org/Howto.html
- **本地来源：** LAMMPS 本地安装内置示例（`/opt/homebrew/share/lammps/examples/`）
- **适用版本：** LAMMPS 22 Jul 2025 - Update 4
- **核对日期：** 2026-07-27
- **内容说明：** 本章为编者整理的模拟流程实践指南，结合官方文档与编者经验编写。
