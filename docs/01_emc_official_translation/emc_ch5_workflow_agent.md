# 第 5 章：工作流代理 (Workflow Agent)

* **官方章节号：** 5 | **官方页码：** 98–102 | **EMC 9.4.4**

---

## 5.1 示例：玻璃化转变 (Glass Transition)

EMC Workflow Agent 支持全自动模拟工作流。以玻璃化转变温度 Tg 的计算为例。

## 5.2 目录结构与设置

```
project/
├── build/           ← 构建文件
├── run/             ← 运行脚本
├── analyze/         ← 分析脚本
├── environment.emc  ← 环境配置
└── config.emc       ← 版本化配置
```

## 5.3 配置与版本索引

EMC Workflow 使用配置文件记录所有参数。支持版本化，确保可复现性。

## 5.4 工作流架构

- 执行模型：Bash 脚本包装 EMC Setup → EMC → LAMMPS → 分析
- 分析管道：自动后处理（密度、压力、能量分布）

## 5.5 名称与概要

`environment.emc` 定义环境名称、描述和参数。

## 5.6 配置块 (ITEM)

### ITEM ENVIRONMENT
定义模拟环境（队列系统、模块、并行设置）。

### ITEM ANALYZE
定义分析任务和脚本。

### ITEM VARIABLES
定义模拟变量和循环范围。

### ITEM LOOPS
定义变量空间的嵌套循环。

## 5.7 模板块 (ITEM TEMPLATE)

### 预处理器宏
支持条件编译和变量替换。

### ITEM OPTIONS
设置构建选项（力场、密度、截断等）。

### ITEM LAMMPS
定义 LAMMPS 特定的松弛方案和参数。

## 5.8 分子架构定义

### ITEM GROUPS
定义化学组（官能团、单体）。

### ITEM CLUSTERS / ITEM POLYMERS
定义分子簇和聚合物架构。

---

## 验证： ✅ 官方翻译 | ⬜ 未验证
## 相关： [第4章](emc_ch4_simulation_setup.md) | [第6章](emc_ch6_scripting_commands.md)
