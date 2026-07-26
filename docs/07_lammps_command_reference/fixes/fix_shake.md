# fix shake 命令 — 键长/键角约束

* **命令类别：** Fix | **Package：** MOLECULE | **本机可用：** ✅
* **官方链接：** [LAMMPS fix shake](https://docs.lammps.org/fix_shake.html)

---

## 语法

```lammps
fix ID group shake tol max_iter N constraint values ...
```

## 常用用法

### SHAKE 约束所有含 H 键

```lammps
fix 1 all shake 0.0001 20 0 b 1 2 3
#                              ↑ 约束 ID=1,2,3 的 bond type
```

| 参数 | 含义 |
|------|------|
| `0.0001` | 容差（相对误差） |
| `20` | 最大迭代次数 |
| `0` | 每个时间步重新约束 = 0 |
| `b` | 约束键 (bond) |
| `1 2 3` | 要约束的 bond type 列表 |

### 约束键角

```lammps
fix 1 all shake 0.0001 20 0 b 1 a 1
#                              bond type 1 的键
#                              angle type 1 的角
```

---

## OPLS/CHARMM 典型设置

```lammps
# 约束所有 X-H 键（允许 timestep 2.0 fs）
fix shake all shake 0.0001 20 0 b 1 2 3 4 5
# bond type 1-5 是各 C-H, O-H, N-H 键

timestep 2.0    # ← 可提升到 2 fs
```

> **编者注：** SHAKE 约束含 H 键是 atomistic 模拟的标准做法。它允许将 timestep 从 0.5 fs 提升到 1.0–2.0 fs，显著加快模拟。但 SHAKE 有计算开销，通常净加速 1.5–2×。

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `ERROR: Shake atoms missing` | 约束的原子组不完整 | 检查拓扑 |
| `WARNING: Shake determinant = 0` | 约束过度 | 减少约束数量 |
| `Shake did not converge` | 迭代不够 | 增大 `max_iter` 或减小 `tol` |

---

## 验证： ✅ 官方 | ✅ 本机 | ⬜ 未运行
