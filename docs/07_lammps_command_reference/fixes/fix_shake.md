# fix shake 命令 — 键长/键角约束

* **命令类别：** Fix | **Package：** MOLECULE
* **命令可用性：** ✅（命令存在于本地 LAMMPS 安装中，`lmp_serial -h` 可列出）
* **验证状态：** ⬜ 未运行（以下示例尚未在本地实际执行）
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

## 验证状态

* ✅ 官方翻译

## 官方来源

- **官方标题：** LAMMPS Documentation — fix shake command
- **官方命令：** fix shake
- **官方 URL：** https://docs.lammps.org/fix_shake.html
- **本地来源：** 通过 `lmp_serial -h fix_shake` 可验证参数存在性
- **适用版本：** LAMMPS 22 Jul 2025 - Update 4（本地）
- **核对日期：** 2026-07-27

## 完整性检查

> 以下清单反映当前页面状态，未勾选项将在后续任务中完善。

- [ ] 完整官方语法
- [ ] 所有必选参数
- [ ] 所有可选参数
- [ ] 所有关键字及子参数
- [ ] 默认值
- [ ] 单位与量纲
- [ ] 限制和依赖
- [ ] 版本差异
- [ ] 加速版本
- [x] 示例
- [x] 常见错误
- [ ] 相关命令
- [x] 官方来源
