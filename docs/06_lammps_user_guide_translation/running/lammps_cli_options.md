# LAMMPS 命令行参数完整参考

* **适用版本：** LAMMPS 22 Jul 2025 - Update 4
* **官方来源：** [LAMMPS Run Options](https://docs.lammps.org/Run_options.html)
* **本机验证：** ✅ 通过 `lmp_serial -h` 验证
* **翻译状态：** 完整翻译

---

## 基本用法

```bash
lmp_serial -var t 300 -echo screen -in in.alloy
```

## 完整命令行参数列表

### -echo none/screen/log/both （简写：-e）

控制输入脚本的回显方式。

| 值 | 含义 |
|----|------|
| `none` | 不回显任何输入命令 |
| `screen` | 将输入命令输出到屏幕 |
| `log` | 将输入命令输出到日志文件 |
| `both` | 同时输出到屏幕和日志文件 |

**编者注：** 调试时建议使用 `-echo screen`，这样可以在终端直接看到每条输入命令的执行。生产运行时建议使用 `-echo log` 或 `-echo none` 以减少屏幕输出。

---

### -help （简写：-h）

打印帮助信息，列出所有可用的命令行选项。

```bash
lmp_serial -h
```

输出包含当前版本号、编译配置、已安装的 packages 以及所有可用的 style 列表。

---

### -in none/filename （简写：-i）

指定输入脚本文件。如果设为 `none`，LAMMPS 从标准输入读取。

```bash
lmp_serial -in my_script.in       # 从文件读取
lmp_serial -in none               # 从标准输入读取
```

**编者注：** 这是最常用的命令行参数。输入脚本文件通常以 `.in`、`.input` 或 `.lmp` 为后缀，但没有强制要求。

---

### -kokkos on/off ... （简写：-k）

开启或关闭 KOKKOS 加速模式及设置选项。

**编者注：** KOKKOS 是一个性能可移植框架，支持 GPU 加速（CUDA、HIP、SYCL）和多线程（OpenMP、Pthreads）。Homebrew 安装的 LAMMPS 版本未启用 KOKKOS。

---

### -log none/filename （简写：-l）

指定日志输出文件。默认日志文件名为 `log.lammps`。设为 `none` 则不写日志文件。

```bash
lmp_serial -log my_sim.log        # 写入 my_sim.log
lmp_serial -log none              # 不写日志文件
```

**警告：** 如果已有同名日志文件，LAMMPS 会追加而不是覆盖。

---

### -mdi '<mdi flags>'

传递 MolSSI Driver Interface (MDI) 标志。MDI 允许 LAMMPS 与其他模拟代码耦合运行。

**编者注：** MDI 是一个标准化的代码耦合接口，由 MolSSI（Molecular Sciences Software Institute）开发。用于 QM/MM 等多尺度模拟场景。

---

### -mpicolor color （简写：-m）

在多可执行文件 MPI 运行中，为每个 LAMMPS 实例分配颜色值。用于 `mpirun` 启动多个 LAMMPS 实例进行耦合计算。

---

### -cite （简写：-c）

选择引用提醒样式。LAMMPS 在运行结束时输出相关论文引用提醒。

---

### -nocite （简写：-nc）

禁用引用提醒。

---

### -nonbuf （简写：-nb）

禁用屏幕和日志文件输出缓冲。用于实时查看输出。

**编者注：** 在某些系统上，标准输出可能被缓冲，导致不能实时看到模拟进展。使用此选项可强制立即输出每一行。

---

### -package style ... （简写：-pk）

调用 package 命令。用于在启动时设置特定 package 的选项。

```bash
lmp_serial -package gpu 1         # 使用 GPU package
```

---

### -partition size1 size2 ... （简写：-p）

分配分区大小。多个数字表示将处理器分成多个分区，每个分区独立运行相同的输入脚本。

```bash
mpirun -np 16 lmp_mpi -partition 8 4 4 -in in.file
# 创建3个分区：8核、4核、4核，各运行独立的 in.file
```

**版本说明：** 分区功能主要用于 replica exchange 等多副本模拟方法。

---

### -plog basename （简写：-pl）

为每个分区指定日志文件基名。第 N 个分区的日志文件名为 `basename.N`。

---

### -pscreen basename （简写：-ps）

为每个分区指定屏幕输出基名。第 N 个分区的屏幕输出文件名为 `basename.N`。

---

### -restart2data rfile dfile ... （简写：-r2data）

将 restart 文件转换为 data 文件。

```bash
lmp_serial -restart2data restart.save my_data.data
```

| 参数 | 含义 |
|------|------|
| `rfile` | 输入的 restart 文件 |
| `dfile` | 输出的 data 文件 |

---

### -restart2dump rfile dgroup dstyle dfile ... （简写：-r2dump）

将 restart 文件转换为 dump 文件。

| 参数 | 含义 |
|------|------|
| `rfile` | 输入的 restart 文件 |
| `dgroup` | dump 的原子组 |
| `dstyle` | dump 样式（如 atom, custom） |
| `dfile` | 输出的 dump 文件 |

---

### -restart2info rfile （简写：-r2info）

打印 restart 文件的信息（时间步、原子数、box 大小等）。

```bash
lmp_serial -restart2info restart.save
```

---

### -reorder topology-specs （简写：-r）

处理器重排序，用于优化并行通信效率。拓扑规范定义如何将 MPI 进程映射到物理处理器核心。

---

### -screen none/filename （简写：-sc）

指定屏幕输出文件。默认输出到终端屏幕。设为 `none` 则不输出到屏幕。

```bash
lmp_serial -screen sim_output.txt  # 屏幕输出写入文件
```

**编者注：** 与 `-log` 的区别：`-screen` 控制的是「屏幕输出通道」（包括 thermo 输出、print 命令等），`-log` 控制的是「日志文件通道」。两者可以独立设置。

---

### -skiprun （简写：-sr）

跳过 `run` 和 `minimize` 命令中的实际循环。用于快速测试输入脚本的语法和结构。

**编者注：** 这是调试新输入脚本的宝贵选项。开启后 LAMMPS 会解析整个输入脚本、设置模拟体系，但不实际进行耗时的力计算和时间积分。也称为 "run 0" 测试。

```bash
lmp_serial -skiprun -in test.in   # 只检查脚本，不真正运行
```

---

### -suffix gpu/intel/kk/opt/omp （简写：-sf）

为所有适用的命令自动添加样式后缀。例如 `-suffix opt` 会让 LAMMPS 自动选择优化版本的 pair style。

| 后缀 | 含义 |
|------|------|
| `gpu` | GPU 加速 |
| `intel` | Intel 优化包 |
| `kk` | KOKKOS 包 |
| `opt` | 通用优化版本 |
| `omp` | OpenMP 多线程版本 |

```bash
lmp_serial -suffix opt -in in.file
```

**编者注：** Homebrew 安装的 LAMMPS 包含 `OPENMP` 和 `OPT` 包，可以使用 `-suffix omp` 和 `-suffix opt`。

---

### -var varname value （简写：-v）

设置输入脚本中的 index 类型变量。

```bash
lmp_serial -var t 300 -var p 1.0 -in npt.in
```

在输入脚本中使用：

```
variable t index 300     # 默认值
# 如果命令行指定了 -var t 500，则使用 500

fix 1 all nvt temp ${t} ${t} 100.0
```

**编者注：** 这是参数化模拟的关键功能。可以用一个输入脚本配合不同的 `-var` 参数运行多个模拟，无需修改输入文件。

---

## 本机编译配置

本机 LAMMPS 版本编译信息：

| 项目 | 值 |
|------|-----|
| 操作系统 | Darwin 24.6.0 arm64 |
| 编译器 | Clang C++ Apple LLVM 17.0.0 |
| C++ 标准 | C++17 |
| OpenMP | 未启用（API: Serial） |
| FFT 精度 | double |
| FFT 引擎 | mpiFFT (FFTW3 with threads) |
| MPI | LAMMPS MPI STUBS |

### 编译时标志

| 标志 | 含义 |
|------|------|
| `LAMMPS_GZIP` | 支持 gzip 压缩文件读写 |
| `LAMMPS_PNG` | 支持 PNG 图像输出 |
| `LAMMPS_JPEG` | 支持 JPEG 图像输出 |
| `LAMMPS_CURL` | 支持从 URL 读取文件 |
| `LAMMPS_SMALLBIG` | 32-bit smallint, 32-bit imageint, 32-bit tagint, 64-bit bigint |

### 支持的压缩格式

| 扩展名 | 命令 |
|--------|------|
| `.gz` | gzip |
| `.bz2` | bzip2 |
| `.zst` | zstd |
| `.xz` | xz |
| `.lzma` | xz |
| `.lz4` | lz4 |

**编者注：** 这意味着 LAMMPS 可以直接读写压缩的 data 文件、dump 文件和 restart 文件。例如 `read_data system.data.gz` 是合法命令。

---

## 已安装的 Packages

本机 LAMMPS 版本共安装了以下 **75 个 packages**（完整列表来自 `lmp_serial -h`）：

**核心物理包：** AMOEBA, ASPHERE, BOCS, BODY, BPM, BROWNIAN, CG-DNA, CG-SPICA, CLASS2, COLLOID, COLVARS, CORESHELL, DIELECTRIC, DIFFRACTION, DIPOLE, DPD-BASIC, DPD-MESO, DPD-REACT, DPD-SMOOTH, DRUDE, EFF, EXTRA-COMMAND, EXTRA-COMPUTE, EXTRA-DUMP, EXTRA-FIX, EXTRA-MOLECULE, EXTRA-PAIR, FEP, GRANULAR, INTERLAYER, KIM, KSPACE, MANIFOLD, MANYBODY, MC, MEAM, MESONT, MGPT, MISC, ML-IAP, ML-POD, ML-RANN, ML-SNAP, ML-UF3, MOFFF, MOLECULE, OPENMP, OPT, ORIENT, PERI, PHONON, PLUGIN, POEMS, PTM, QEQ, QTB, REACTION, REAXFF, REPLICA, RHEO, RIGID, SHOCK, SMTBQ, SPH, SPIN, SRD, TALLY, UEF, VORONOI, YAFF

---

## 典型用法示例

### 1. 基本串行运行

```bash
lmp_serial -in input.in -log run.log
```

### 2. 参数化运行

```bash
lmp_serial -var temp 300 -var press 1.0 -in npt.in
```

### 3. 调试模式

```bash
lmp_serial -skiprun -echo screen -in new_input.in
```

### 4. Restart 转换

```bash
lmp_serial -restart2data restart.100000 system.data
lmp_serial -restart2info restart.100000
```

### 5. MPI 并行运行

```bash
mpirun -np 8 lmp_mpi -in input.in -log run.log
```

### 6. 带优化后缀

```bash
lmp_serial -suffix opt -in input.in
```

---

## 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `ERROR: Cannot open input script` | 输入文件不存在或路径错误 | 检查文件路径 |
| `ERROR: Variable does not exist` | 引用了未定义的变量 | 用 `-var` 定义或检查变量名 |
| `ERROR: Unknown command` | 输入脚本中有拼写错误或缺少 package | 检查命令拼写，确认 package 已安装 |

---

## 验证状态

* ✅ 官方翻译（基于 `lmp_serial -h` 和官方文档）
* ✅ 本机静态检查
* ⬜ 本机实际运行
* ⬜ 尚未验证
