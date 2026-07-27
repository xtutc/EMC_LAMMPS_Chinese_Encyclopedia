# LAMMPS 输入脚本完整语法与结构

* **适用版本：** LAMMPS 22 Jul 2025 - Update 4
* **官方来源：** [Commands_input](https://docs.lammps.org/Commands_input.html), [Commands_parse](https://docs.lammps.org/Commands_parse.html), [Commands_structure](https://docs.lammps.org/Commands_structure.html)
* **翻译状态：** 完整翻译 + 注释

---

## 1. 输入脚本概述

LAMMPS 输入脚本是一个文本文件（通常以 `.in` 或 `.input` 为后缀），其中每一行是一个 LAMMPS 命令。LAMMPS 按行读取并逐条执行。

**编者注：** LAMMPS 输入脚本不是声明式配置，而是命令式脚本——写在前面的命令先执行，顺序很重要。

---

## 2. 输入脚本的四段式结构

典型的 LAMMPS 输入脚本包含四个阶段：

```
# ============================================================
# 第一阶段：初始化 (Initialization)
# ============================================================
units           real
dimension       3
boundary        p p p
atom_style      full

# ============================================================
# 第二阶段：体系定义 (System Definition)
# ============================================================
read_data       system.data
# 或：
# lattice       fcc 4.05
# region        box block 0 10 0 10 0 10
# create_box    1 box
# create_atoms  1 box

# ============================================================
# 第三阶段：模拟设置 (Simulation Settings)
# ============================================================
pair_style      lj/cut/coul/long 10.0
pair_coeff      * * 0.1 3.0
kspace_style    pppm 1e-4
bond_style      harmonic
angle_style     harmonic
dihedral_style  opls

fix             1 all nvt temp 300.0 300.0 100.0
timestep        1.0
thermo          100

# ============================================================
# 第四阶段：运行 (Run)
# ============================================================
run             10000
```

### 第一阶段：初始化

设置基本参数，定义模拟盒子和原子类型。

**必须在其他命令之前执行的命令：**

| 命令 | 用途 | 是否必须 |
|------|------|---------|
| `units` | 设置单位系统 | 是 |
| `dimension` | 设置维数 (2D/3D) | 否（默认3） |
| `boundary` | 设置边界条件 (p/f/s/m) | 否（默认 p p p） |
| `atom_style` | 设置原子样式 | 是 |
| `newton` | 设置牛顿第三定律处理方式 | 否 |
| `processors` | 设置处理器网格 | 否 |

### 第二阶段：体系定义

定义模拟盒子、原子、分子拓扑、力场参数。

**编者注：** 在输入脚本中定义体系有两种方式：
1. **从 data 文件读取：** 使用 `read_data` 命令（大多数情况下推荐，尤其是 EMC 生成的体系）
2. **在输入脚本中构建：** 使用 `lattice`、`region`、`create_box`、`create_atoms` 等命令

### 第三阶段：模拟设置

定义力场、系综、热浴、时间步和输出。

**关键命令：**

| 类别 | 命令示例 |
|------|---------|
| 力场 | `pair_style`, `pair_coeff`, `bond_style`, `kspace_style` |
| 系综 | `fix nvt`, `fix npt`, `fix nve` |
| 约束 | `fix shake`, `fix rigid` |
| 输出 | `thermo`, `dump`, `fix ave/time` |
| 最小化 | `minimize` |

### 第四阶段：运行

执行实际的分子动力学模拟。

```lammps
run     50000          # 运行 50000 步
write_restart restart.final
```

---

## 3. 输入脚本语法规则

### 3.1 基本规则

1. **每行一条命令。**
2. **命令名 + 参数，以空格分隔。**
3. **不区分大小写**（命令名自动转换为小写，文件名区分）。
4. **行首 `#` 表示注释**（如果行首没有 `#`，一行末尾的 `#` 不被视为注释）。

```
# 这是注释
pair_coeff  * * 0.1 3.0       # 这不是注释！（会被解析）
```

> **警告：** 在 LAMMPS 中输入脚本行末尾的 `#` **不是**注释符号！如果在命令参数后面追加 `#` 和说明文字，LAMMPS 会尝试将 `#` 和后续文字作为参数解析并报错。

### 3.2 续行

使用 `&` 将一行命令延续到下一行。

```lammps
pair_coeff 1 1 0.10 3.0 &
            1 2 0.15 3.2 &
            2 2 0.12 3.1
```

### 3.3 变量替换

使用 `$` 或 `${}` 引用变量：

```lammps
variable t index 300
fix 1 all nvt temp $t $t 100.0          # $t = 300
fix 1 all nvt temp ${t} ${t} 100.0      # 推荐写法，更安全
```

**编者注：** 建议始终使用 `${variable}` 形式，因为在紧跟字母或数字时 `$variable` 会产生歧义。例如 `$t100` 被解析为变量 `t100`，而 `${t}100` 被正确解析为变量 `t` 后接 `100`。

### 3.4 引号

当参数包含空格时，使用单引号 `'` 或双引号 `"`：

```lammps
print "Starting simulation at temperature $t"
variable s string "my file with spaces.txt"
```

### 3.5 立即求值

使用 `$(...)` 或 `$(...)` 进行立即求值表达式和公式计算：

```lammps
variable N equal 100
variable V equal $(2.0*3.0*4.0)          # V = 24.0
create_atoms 1 box $(100*2)              # 创建 200 个原子
```

**编者注：** 立即求值表达式在命令执行前计算，支持 `+`, `-`, `*`, `/`, `^` 运算符和许多数学函数（`sqrt()`, `exp()`, `log()`, `sin()`, `cos()`, `abs()`, `int()`, `floor()`, `ceil()`, `atan()`, `atan2()` 等）。

### 3.6 Include 文件

使用 `include` 命令将另一个文件的内容插入当前位置：

```lammps
include system.init              # 引用同目录下的 system.init 文件
include ../common/forcefield.in  # 相对路径引用
```

**编者注：** `include` 是一个很好的实践，可以将力场参数、系综设置等可复用部分单独存放。EMC 经常使用 `include` 将力场参数文件嵌入主输入脚本。

### 3.7 跳转

使用 `jump` 和 `next` 命令控制脚本执行流程：

```lammps
jump newfile              # 跳转到 newfile 并继续执行
jump SELF breakloop       # 跳转到当前文件的 breakloop 标签
```

使用 `label` 定义跳转目标：

```lammps
label   loopstart
# ... 一些命令 ...
jump    input.in loopstart
```

---

## 4. 输入脚本解析规则

### 4.1 命令解析顺序

LAMMPS 按照以下步骤解析每一行输入：

1. **去掉注释：** 如果行首是 `#`，整行跳过
2. **续行拼接：** 如果行尾是 `&`，与下一行拼接
3. **变量替换：** 替换 `${variable}` 和 `$(...)` 
4. **分词：** 以空白字符分割
5. **命令查找：** 查找并执行命令

### 4.2 关于 # 的重要警告

> **警告：** 命令行中间或末尾出现的 `#` 字符**不会被当作注释**。LAMMPS 只将**行首的第一个非空白字符为 `#`** 的行视为注释行。

```lammps
# 这是注释行
pair_coeff * * 1.0 1.0  # 这不是注释！会导致错误！
```

### 4.3 变量命名规则

- 必须以字母开头
- 可包含字母、数字、下划线
- 不能以数字开头
- 区分大小写：`$T` 和 `$t` 是不同的变量

### 4.4 特殊字符

| 字符 | 含义 |
|------|------|
| `#` | 行首表示注释 |
| `$` | 变量引用 |
| `&` | 行尾续行符 |
| `*` | 通配符（在 `pair_coeff` 等命令中表示所有类型） |
| `()` | 立即求值表达式 |

---

## 5. 完整输入脚本示例

### 5.1 最小化脚本

```lammps
# minim.in - 最小化示例
units           real
atom_style      full
boundary        p p p

read_data       system.data

pair_style      lj/cut/coul/long 10.0
pair_coeff      * * 0.1 3.0
kspace_style    pppm 1.0e-4

bond_style      harmonic
angle_style     harmonic
dihedral_style  harmonic

thermo          100
thermo_style    custom step pe ke etotal temp press

minimize        1.0e-4 1.0e-6 1000 10000

write_data      minimized.data
```

### 5.2 NVT 平衡脚本

```lammps
# nvt.in - NVT 系综平衡
units           real
atom_style      full

read_data       minimized.data

pair_style      lj/cut/coul/long 10.0
pair_coeff      * * 0.1 3.0
kspace_style    pppm 1.0e-4

velocity        all create 300.0 12345

fix             1 all nvt temp 300.0 300.0 100.0

timestep        1.0
thermo          100
thermo_style    custom step temp press etotal density

dump            1 all custom 1000 traj.lammpstrj id type x y z

run             50000
write_restart   nvt.restart
```

### 5.3 NPT 生产脚本

```lammps
# npt.in - NPT 系综生产模拟
units           real
atom_style      full

read_restart    nvt.restart

pair_style      lj/cut/coul/long 10.0
pair_coeff      * * 0.1 3.0
kspace_style    pppm 1.0e-4

fix             1 all npt temp 300.0 300.0 100.0 iso 1.0 1.0 1000.0

timestep        1.0
thermo          1000
thermo_style    custom step temp press density etotal

dump            1 all custom 5000 npt_traj.lammpstrj id type x y z
dump            2 all xyz 5000 npt_traj.xyz

run             1000000
write_restart   npt_final.restart
write_data      npt_final.data
```

---

## 6. 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `ERROR: Illegal ... command` | 命令拼写错误或缺少参数 | 检查命令名和参数个数 |
| `ERROR: Unknown command: ...` | 命令不存在或 package 未安装 | 检查命令拼写和可用的 packages |
| `ERROR: Cannot open ...` | 文件不存在或路径错误 | 检查文件路径 |
| `ERROR: All pair coeffs are not set` | 缺少某些原子类型对的 `pair_coeff` | 检查 `pair_coeff` 是否覆盖所有类型对 |
| `ERROR: # of atoms in file does not match` | data 文件中的原子数与创建的不一致 | 检查 data 文件头部 |
| `ERROR: Unknown atom style` | `atom_style` 不支持 | 检查是否安装了对应的 package |

---

## 7. 验证状态

* ✅ 官方翻译（基于 LAMMPS 官方文档）
* ✅ 本机静态检查（`lmp_serial -h` 验证了 packages 可用性）
* ⬜ 本机实际运行
* ⬜ 尚未验证

---

## 8. 相关页面

- [LAMMPS 命令行参数](../running/lammps_cli_options.md)
- [LAMMPS data 文件格式](../../08_lammps_file_formats/data_file.md)
- [最小化流程](../../10_simulation_workflows/minimization.md)
- [NVT 流程](../../10_simulation_workflows/nvt.md)
- [NPT 流程](../../10_simulation_workflows/npt.md)

## 官方来源

- **官方标题：** LAMMPS Documentation — Commands input, parse, and structure
- **官方章节或命令：** Commands_input、Commands_parse、Commands_structure
- **官方 URL：** https://docs.lammps.org/Commands_input.html
- **本地来源：** 本地未获取
- **适用版本：** LAMMPS 22 Jul 2025 - Update 4（本地）
- **核对日期：** 2026-07-27
