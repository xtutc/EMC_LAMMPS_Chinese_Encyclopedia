# velocity 命令 — 初始速度设定

* **命令类别：** 初始化 | **所属 package：** 内置
* **命令可用性：** ✅（命令存在于本地 LAMMPS 安装中，`lmp_serial -h` 可列出）
* **验证状态：** ⬜ 未运行（以下示例尚未在本地实际执行）
* **官方链接：** [LAMMPS velocity](https://docs.lammps.org/velocity.html)

---

## 语法

```lammps
velocity group style args
```

## 常用 style

### create — 从 Maxwell-Boltzmann 分布生成

```lammps
velocity all create 300.0 12345 mom yes rot yes
```

| 参数 | 含义 |
|------|------|
| `300.0` | 目标温度 (K) |
| `12345` | 随机种子 |
| `mom yes` | 移除质心平动 |
| `rot yes` | 移除质心转动 |

### set — 设定指定值

```lammps
velocity all set 0.0 0.0 0.0     # 归零
velocity upper set 0.0 5.0 0.0   # group 指定
```

### scale — 缩放现有速度到目标温度

```lammps
velocity all scale 300.0
```

---

## 典型用法

```lammps
# 最小化后初始化
minimize 1e-4 1e-6 1000 10000
velocity all create 300.0 12345 mom yes rot yes
fix 1 all nvt temp 300.0 300.0 100.0

# 从 restart 继续 → 不需要 velocity（速度已在 restart 中）
read_restart nvt.restart
fix 1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0
```

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `ERROR: Velocity after fix` | velocity 在 fix 之后 | velocity 放 fix 前面 |
| `Temperature out of range` | 原子重叠 | 充分最小化后再 velocity |

---

## 验证状态

* ✅ 官方翻译

## 官方来源

- **官方标题：** LAMMPS Documentation — velocity command
- **官方命令：** velocity
- **官方 URL：** https://docs.lammps.org/velocity.html
- **本地来源：** 通过 `lmp_serial -h velocity` 可验证参数存在性
- **适用版本：** LAMMPS 22 Jul 2025 - Update 4（本地）
- **核对日期：** 2026-07-27
