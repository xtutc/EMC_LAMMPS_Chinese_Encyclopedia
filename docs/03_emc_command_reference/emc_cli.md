# EMC 主程序命令行参考

* **EMC 版本：** 9.4.4 (Jul 21 2026)
* **可执行文件：** `emc_linux_x86_64`（服务器路径：`/opt/emc-9.4.4/bin/emc_linux_x86_64`）
* **官方来源：** `emc -help` 输出, EMC 官方手册
* **翻译状态：** 完整翻译 + 注释

---

## 1. EMC 简介

> **编者注：** EMC (Enhanced Monte Carlo) 是一个多用途、模块化、可扩展的分子和介观模拟工具。它使用 Monte Carlo 方法构建分子体系，并输出为 LAMMPS、GROMACS、NAMD、PDB、XYZ 等格式。

**必须引用的参考文献：**
> P.J. in 't Veld and G.C. Rutledge, *Macromolecules* 2003, **36**, 7358.

---

## 2. EMC 命令行语法

```bash
emc [-option[=value]] input[.emc] [argument ...]
```

### 2.1 基本用法

```bash
# 执行 EMC 输入文件
emc build.emc

# 带选项
emc -nthreads=8 build.emc

# 传递变量
emc -seed=12345 -temp=300 build.emc arg1 arg2
```

---

## 3. 完整命令行选项

### -debug

激活或关闭调试输出。

```bash
emc -debug build.emc         # 激活调试
emc -debug=off build.emc     # 关闭调试
```

### -error

重定向错误输出和/或设置输出基名。

### -ext_error

重新定义错误文件扩展名。默认：`.err`

```bash
emc -ext_error=.error build.emc
```

### -ext_file

重新定义常规输入/输出文件扩展名。默认：`.emc`

### -ext_history

重新定义历史文件扩展名。默认：`.hst`

### -help

显示帮助信息（即本页内容）。

```bash
emc -help
```

### -history

请求二进制历史文件和/或设置输出基名。历史文件记录 Monte Carlo 移动历史。

### -info

激活或关闭信息输出。

```bash
emc -info=off build.emc
```

### -nthreads

设置线程数（用于并行 MC 采样）。

```bash
emc -nthreads=8 build.emc     # 使用 8 个线程
emc -nthreads=1 build.emc     # 单线程运行
```

> **编者注：** EMC 的 Monte Carlo 构建过程支持多线程加速。在多核 CPU 上使用 `-nthreads` 可以显著减少体系构建时间。

### -quiet

同时关闭信息（info）和警告（warning）输出。

```bash
emc -quiet build.emc          # 安静模式
```

### -var, -variables

定义变量。

```bash
emc -var=seed=12345 build.emc
emc -variables=temp=300,press=1 build.emc
```

> **编者注：** EMC 输入文件支持变量替换。通过 `-var` 传递的变量可在 `.emc` 文件中通过 `$variable` 引用。

### -version

输出版本信息。

```bash
emc -version
# 输出：EMC, version 9.4.4 (Jul 21 2026 07:58:38)
```

### -warning

激活或关闭警告输出。

---

## 4. 变量系统

EMC 内置变量系统：

| 特性 | 说明 |
|------|------|
| 非存在选项自动为变量 | `-seed=123` 自动创建变量 `seed`，值 `123` |
| 位置参数 | `$arg0`, `$arg1`, `$arg2` ... 引用命令行位置参数 |
| 类型转换 | 以非数字字符开头的变量值自动转换为字符串 |

### 示例

```bash
emc -seed=12345 -temperature=300 -molecules=1000 build.emc extra_arg
```

在 `build.emc` 中：
```
# $seed = 12345
# $temperature = 300
# $molecules = 1000
# $arg0 = extra_arg
# $arg1 = （空）
```

---

## 5. EMC 输入文件格式 (.emc)

EMC 输入文件（`.emc`）是需要完整翻译的另一重要主题。

### 5.1 基本结构

```
# 注释
ITEM ...           ← 定义 ITEM 区块
ITEM OPTIONS       ← 设置全局选项
ITEM MOLECULE      ← 定义分子
ITEM GROUP         ← 定义组
ITEM CLUSTER       ← 定义簇
ITEM END           ← 结束定义
```

### 5.2 典型 EMC 输入示例

见 EMC Setup 文件规则（待创建）获取完整的 `.emc` 文件格式说明和 ITEM 关键字详解。

---

## 6. EMC 输出文件

| 输出文件 | 内容 |
|---------|------|
| `system.data` | LAMMPS data 文件 |
| `system.in` | LAMMPS 输入脚本 |
| `system.params` | 力场参数 |
| `system.pdb` | PDB 格式结构 |
| `system.xyz` | XYZ 格式坐标 |
| `*.err` | 错误文件 |
| `*.hst` | 历史文件 |

---

## 7. EMC 脚本工具

EMC 提供多个 Perl 脚本用于格式转换：

| 脚本 | 功能 |
|------|------|
| `emc.pl` | EMC Setup 主脚本 |
| `emc_setup.pl` | EMC Setup 旧版 |
| `emc_opls.pl` | OPLS 力场 typing 脚本 |
| `emc_trappe.pl` | TraPPE 力场 typing 脚本 |
| `emc_sdk.pl` | SDK 粗粒化力场脚本 |
| `emc_martini.pl` | MARTINI 粗粒化力场脚本 |
| `emc_generate.pl` | 生成工具 |
| `emc_align.pl` | 对齐工具 |
| `emc2lammps.emc` | EMC→LAMMPS 转换 |
| `emc2gromacs.emc` | EMC→GROMACS 转换 |
| `emc2namd.emc` | EMC→NAMD 转换 |
| `emc2pdb.emc` | EMC→PDB 转换 |
| `emc2xyz.emc` | EMC→XYZ 转换 |
| `emc2vtk.emc` | EMC→VTK 转换 |
| `lammps2emc.emc` | LAMMPS→EMC 转换 |
| `charmm2lammps.pl` | CHARMM→LAMMPS 参数转换 |

---

## 8. 典型用法

### 8.1 执行 EMC Setup 生成的构建脚本

```bash
emc -nthreads=4 build.emc
```

### 8.2 带参数运行

```bash
emc -seed=99999 -temperature=400 build.emc
```

### 8.3 安静模式批量运行

```bash
emc -quiet -nthreads=16 build.emc
```

---

## 9. 本机验证

| 项目 | 状态 |
|------|------|
| EMC 二进制存在 | ✅ `/opt/emc-9.4.4/bin/emc_linux_x86_64` |
| 版本确认 | ✅ v9.4.4 (Jul 21 2026) |
| help 输出获取 | ✅ 完整 |
| 实际运行 EMC | ⬜ 待验证 |

---

## 10. 相关页面

- [EMC Setup 总览](../02_emc_setup_reference/setup_overview.md)
- [EMC Setup 命令行](../02_emc_setup_reference/setup_cli.md)
- EMC Setup 文件规则（待创建）
- EMC 文件工作流（待创建）
- [EMC→LAMMPS 工作流](../09_emc_to_lammps/complete_workflow.md)
