# dump 命令 — 轨迹和原子数据输出

* **命令类别：** 输出 (Output)
* **所属 package：** 内置 (无)
* **命令可用性：** ✅（命令存在于本地 LAMMPS 安装中，`lmp_serial -h` 可列出）
* **验证状态：** ⬜ 未运行（以下示例尚未在本地实际执行）
* **官方链接：** [LAMMPS dump](https://docs.lammps.org/dump.html)

---

## 语法

```lammps
dump ID group style N file args
dump ID group style N file1 file2
```

| 参数 | 含义 |
|------|------|
| `ID` | dump 标识符 |
| `group` | 输出的原子组（`all` 表示全部） |
| `style` | 输出格式：`atom`, `custom`, `xyz`, `dcd`, `xtc`, `cfg`, `image` 等 |
| `N` | 每隔 N 步输出一次 |
| `file` | 输出文件名（% 通配符生成序列文件） |

---

## 常用 dump style

### atom（默认 LAMMPS 轨迹）

```lammps
dump 1 all atom 1000 traj.lammpstrj
```

输出 LAMMPS 原生轨迹格式。每个原子的信息取决于 `atom_style`：
- `full`: id type x y z ix iy iz（id, 类型, 坐标, 镜像标志）
- `atomic`: id type x y z

### custom（自定义输出）

```lammps
dump 1 all custom 1000 traj.custom id type x y z vx vy vz
```

可以输出任意 per-atom 属性：
`id`, `mol`, `type`, `q`（电荷）, `x`, `y`, `z`, `vx`, `vy`, `vz`, `fx`, `fy`, `fz`, `mass`, `element`, `radius`, `ix`, `iy`, `iz`, `c_*`（compute）, `f_*`（fix）

### xyz（通用格式）

```lammps
dump 1 all xyz 1000 traj.xyz
```

输出标准 XYZ 格式，适用于 VMD、Ovito 等可视化软件。

**编者注：** EMC 也输出 `.xyz` 文件。但这种 LAMMPS 的 `dump xyz` 可以输出模拟过程中的构型变化。

### dcd（CHARMM/NAMD 轨迹）

```lammps
dump 1 all dcd 1000 traj.dcd
```

二进制 DCD 格式，文件更小，适合长轨迹。

### xtc（GROMACS 压缩轨迹）

```lammps
dump 1 all xtc 1000 traj.xtc
```

高压缩比，文件极小，适合长模拟。

### movie（图像序列）

```lammps
dump 1 all movie 1000 movie.mpg type type size 512 512
```

直接生成电影文件（需要编译时支持图像库）。

---

## dump_modify 选项

```lammps
dump_modify ID keyword value ...
```

| 选项 | 功能 |
|------|------|
| `sort id` | 按原子 ID 排序输出 |
| `first yes` | 在第一步就输出 |
| `every N` | 覆盖输出频率 |
| `scale yes` | 输出缩放坐标（分数坐标）而非实际坐标 |
| `unwrap yes` | 输出 unwrapped 坐标（取消近邻镜像包装） |
| `format "..."` | 自定义输出格式字符串 |

```lammps
dump_modify 1 sort id
dump_modify 1 first yes
dump_modify 1 scale no
```

---

## 多 dump 示例

```lammps
# 全原子轨迹（每 5000 步）
dump traj all custom 5000 npt.lammpstrj id type x y z

# XYZ 格式（用于 Ovito/VMD，每 10000 步）
dump xyz all xyz 10000 npt.xyz

# 只输出聚合物链（每 1000 步）
dump poly polymer custom 1000 polymer.lammpstrj id type x y z
```

---

## 通配符文件名

使用 `*` 或 `%` 生成序列文件：

```lammps
dump 1 all custom 1000 traj.*.lammpstrj    # traj.0.lammpstrj, traj.1000.lammpstrj, ...
dump 1 all custom 1000 traj.%d.lammpstrj   # traj.0.lammpstrj, traj.1000.lammpstrj, ...
```

---

## 与 EMC 的关系

EMC 生成的 LAMMPS 输入脚本通常包含 dump 命令。Setup 的 `-dtdump` 参数控制输出频率。

| EMC Setup | LAMMPS |
|----------|--------|
| `-lammps_dtdump=5000` | `dump 1 all custom 5000 ...` |
| `-dump_box=true` | `dump_modify 1 ...` (unwrap) |

---

## 本地 LAMMPS 支持的 dump styles

本机 (Homebrew LAMMPS) 支持：
`atom`, `custom`, `cfg`, `dcd`, `image`, `local`, `movie`, `xtc`, `xyz`, `yaml`, `grid`, `grid/vtk`

---

## 相关页面

- [thermo 命令](../computes/thermo.md)
- write_dump 命令（待创建）
- read_dump 命令（待创建）
