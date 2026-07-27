# thermo / thermo_style 命令 — 热力学输出控制

* **命令类别：** 输出 (Output)
* **所属 package：** 内置
* **命令可用性：** ✅（命令存在于本地 LAMMPS 安装中，`lmp_serial -h` 可列出）
* **验证状态：** ⬜ 未运行（以下示例尚未在本地实际执行）
* **官方链接：** [LAMMPS thermo](https://docs.lammps.org/thermo.html)

---

## thermo 命令

### 语法

```lammps
thermo N
```

每 N 步输出一行热力学信息到屏幕和日志文件。

| N | 含义 |
|---|------|
| `100` | 每 100 步输出（适合小体系） |
| `1000` | 每 1000 步输出（适合生产模拟） |
| `0` | 关闭输出 |

---

## thermo_style 命令

### 语法

```lammps
thermo_style style args
```

### 预定义 style

| style | 输出内容 |
|-------|--------|
| `one` | 一行输出，包含最基本的量 |
| `multi` | 多行输出，详细列出每个量 |
| `custom` | **自定义输出（推荐）** |

### custom 格式

```lammps
thermo_style custom step temp press etotal density vol pe ke
```

---

## 可用的 thermo 关键字

### 模拟状态

| 关键字 | 含义 | 单位 (real) |
|--------|------|-----------|
| `step` | 时间步数 | — |
| `time` | 模拟时间 | fs |
| `dt` | 时间步长 | fs |
| `cpu` | 累计 CPU 时间 | s |
| `spcpu` | 每步 CPU 时间 | s |
| `remain` | 估计剩余时间 | s |

### 热力学量

| 关键字 | 含义 | 单位 (real) |
|--------|------|-----------|
| `temp` | 温度 | K |
| `press` | 总压力 | atm |
| `pxx`, `pyy`, `pzz` | 压力张量对角分量 | atm |
| `pxy`, `pxz`, `pyz` | 压力张量非对角分量 | atm |
| `etotal` | 总能量 | kcal/mol |
| `pe` | 势能 | kcal/mol |
| `ke` | 动能 | kcal/mol |
| `evdwl` | 范德华能 | kcal/mol |
| `ecoul` | 库仑能 | kcal/mol |
| `ebond` | 键能 | kcal/mol |
| `eangle` | 角能 | kcal/mol |
| `edihed` | 二面角能 | kcal/mol |
| `eimp` | 非正则二面角能 | kcal/mol |
| `elong` | 长程能量 | kcal/mol |
| `enthalpy` | 焓 | kcal/mol |

### 体系属性

| 关键字 | 含义 | 单位 (real) |
|--------|------|-----------|
| `vol` | 体积 | Å³ |
| `density` | 密度 | g/cm³ |
| `lx`, `ly`, `lz` | 盒子尺寸 | Å |
| `natoms` | 原子数 | — |
| `atoms` | 原子数 | — |

### Compute 和 Fix 输出

| 关键字 | 含义 |
|--------|------|
| `c_ID` | compute ID 的标量值 |
| `c_ID[N]` | compute ID 的第 N 个向量元素 |
| `f_ID` | fix ID 的标量值 |
| `v_name` | equal 类型变量的值 |

---

## 完整示例

```lammps
# 调试阶段 — 详细输出
thermo 100
thermo_style custom step temp press etotal density vol pe ke ebond eangle edihed

# 生产阶段 — 简洁输出
thermo 1000
thermo_style custom step temp press density etotal cpu

# 带 compute 的输出
compute rdf all rdf 50 1 1
thermo_style custom step temp press c_rdf[1] c_rdf[2] c_rdf[3]

# 带变量的输出
variable mytemp equal c_thermo_temp
thermo_style custom step temp press v_mytemp
```

---

## thermo_modify

```lammps
thermo_modify keyword value ...
```

| 选项 | 功能 |
|------|------|
| `lost ignore` | 忽略丢失原子（危险！） |
| `lost warn` | 丢失原子时警告（默认） |
| `lost error` | 丢失原子时报错 |
| `flush yes` | 每步刷新输出缓冲 |
| `line one` | 单行输出 |
| `line multi` | 多行输出 |
| `norm yes` | 归一化某些量 |
| `format "..."` | 自定义数字格式 |

```lammps
thermo_modify flush yes
thermo_modify line one
```

---

## 典型用途

### 1. 模拟过程监控

```lammps
thermo 1000
thermo_style custom step temp press density etotal
```

### 2. 调试能量问题

```lammps
thermo 10
thermo_style custom step pe evdwl ecoul ebond eangle edihed elong
```

### 3. 检查压力分量（界面体系）

```lammps
thermo 1000
thermo_style custom step temp pxx pyy pzz pxy pxz pyz
```

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `ERROR: Thermo keyword 'xxx' not found` | 关键字不存在 | 检查拼写 |
| `ERROR: Compute ID xxx does not exist` | compute 未定义 | 先定义 compute |
| `WARNING: Temperature is not being computed` | 无温度计算 | 确保 group 包含平移自由度的原子 |

---

## 与 EMC 的关系

EMC Setup 的 `-dtthermo` 参数控制 thermo 输出频率。生成的脚本通常使用 `thermo_style custom`。

---

## 验证状态

* ✅ 官方翻译

---

## 相关页面

- [dump 命令](../dumps/dump.md)
- compute 命令（相关类别目录，待创建）
- [最小化流程](../../10_simulation_workflows/minimization.md)

## 官方来源

- **官方标题：** LAMMPS Documentation — thermo command
- **官方命令：** thermo
- **官方 URL：** https://docs.lammps.org/thermo.html
- **本地来源：** 通过 `lmp_serial -h thermo` 可验证参数存在性
- **适用版本：** LAMMPS 22 Jul 2025 - Update 4（本地）
- **核对日期：** 2026-07-27
