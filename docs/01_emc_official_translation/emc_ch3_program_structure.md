# 第 3 章：程序结构 (Program Structure)

* **官方章节号：** 3 | **官方页码：** 6–7 | **EMC 9.4.4**
* **官方来源：** EMC Manual PDF

---

## 3.1 分子表示 (Molecular Representation)

### 位点 (Sites)
EMC 基本构建单元，对应原子或粗粒化珠子。每个位点含坐标、类型、电荷、质量。

### 组 (Groups)
位点集合，代表分子子结构（官能团、单体）。用于定义重复单元和 SMILES 解析。

### 簇 (Clusters)
组的集合，代表完整分子（聚合物链/小分子）。

## 3.2 分子相互作用
类型系统分类（原子类型、键类型、角类型），计算所有经典力场项（bond, angle, dihedral, vdW, Coulomb）。

## 3.3 体系
三维周期、二维周期表面、多相界面。

## 3.4 构型移动 (MC Moves)
Displace, Cluster, Reptation, Rebridge/Endbridge, Deform, Rotate, Surface。

## 3.5 测量
g(r)、回转半径、密度/能量/压力分布、CESA。

---

**验证：** 官方翻译 | 未运行验证

**相关：** [第2章](emc_ch2_methodology.md) | [EMC建模](../04_emc_modeling/molecules.md)

## 官方来源

- **官方标题：** EMC Setup Manual v9.4.4 — Chapter 3: Program Structure
- **官方章节：** 3 Program Structure（PDF 第 6–7 页）
- **官方 URL：** https://montecarlo.sourceforge.net/emc/Welcome.html
- **本地来源：** `sources/emc/emc_manual.pdf`（服务器路径：`/opt/emc-9.4.4/docs/emc.pdf`）
- **适用版本：** EMC 9.4.4 (Jul 21 2026)
- **核对日期：** 2026-07-27
