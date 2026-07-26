# 第 2 章：方法论 (Methodology)

* **英文原题：** Chapter 2: Methodology
* **官方章节号：** 2 | **官方页码：** 3–5
* **适用 EMC 版本：** 9.4.4 | **官方来源：** EMC Manual PDF
* **翻译状态：** 翻译+注释

---

## 2.11 列表 (Lists)

EMC 使用多种列表结构组织模拟数据：
- **位点列表：** 存储原子/珠子位置、类型、电荷
- **键合列表：** 存储分子内键、角、二面角连接
- **力场列表：** 存储力场参数
- **系统列表：** 存储模拟盒子、边界条件

## 2.1.2 力场 (Force Fields)

EMC 力场系统为模块化架构。力场由两类文件定义：

| 文件 | 扩展名 | 内容 |
|------|--------|------|
| 拓扑文件 | .top | 原子类型定义、键合连接规则 |
| 参数文件 | .prm | 力常数、LJ参数、电荷 |

### EMC typing 过程：
1. SMILES 展开为原子图
2. .top 规则匹配原子化学环境
3. .prm 查找力场参数
4. 分配部分电荷

### 支持的势能形式

**非键：** LJ 12-6, Coulomb, Buckingham, DPD 软排斥
**键合：** Harmonic bond/angle, Class2, OPLS dihedral, CHARMM dihedral

### 与 LAMMPS 关系

| EMC 形式 | LAMMPS style |
|----------|-------------|
| LJ 12-6 | lj/cut, lj/cut/coul/long |
| Harmonic bond | harmonic |
| Class2 bond | class2 |
| OPLS dihedral | opls |
| CHARMM dihedral | charmm |

---

## 验证状态
* 官方翻译 | 未验证

## 相关页面
- [第1章](emc_ch1_introduction.md) | [力场基础](../05_force_fields/fundamentals.md)
