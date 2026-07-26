# 文件格式索引

> **适用对象：** EMC 与 LAMMPS 用户
> **索引状态：** 当前仅列出项目已经覆盖或已建立入口的格式。

本页用于按文件类型定位相关说明。文件格式页面描述语法、字段或使用场景；
命令页面则说明生成、读取或修改这些文件的命令行为。

## 已覆盖的文件格式

| 文件格式 | 相关页面 | 简要说明 |
|---|---|---|
| LAMMPS data 文件 | [data 文件](../08_lammps_file_formats/data_file.md) | 保存原子、拓扑、盒子与力场系数等体系初始数据。 |
| LAMMPS 输入脚本 | [输入脚本语法](../06_lammps_user_guide_translation/input_scripts/input_script_syntax.md) | 定义 LAMMPS 读取数据、设置相互作用和执行计算的命令序列。 |
| EMC Setup 文件 | [EMC Setup 总览](../02_emc_setup_reference/setup_overview.md) | 用于通过 `emc.pl` 定义建模任务与生成工作流。 |

## 与 `08_lammps_file_formats` 分类的关系

- `08_lammps_file_formats` 是 LAMMPS 专用文件格式说明的主分类。
- 本页是跨分类入口：除 LAMMPS data 文件外，也索引 LAMMPS 输入脚本和 EMC Setup 文件。
- 新增 restart、dump、PDB、XYZ 等格式页面后，应同时在本页增加入口。

## 使用提示

- 需要建立初始结构时，先查看 EMC Setup 文件与 LAMMPS data 文件。
- 需要编写运行步骤时，查看 LAMMPS 输入脚本语法。
- 文件内容与具体命令的兼容性仍需以对应软件版本的官方文档为准。

## 相关页面

- [命令索引](command_index.md)
- [EMC→LAMMPS 完整工作流](../09_emc_to_lammps/complete_workflow.md)
- [LAMMPS 命令参考](../07_lammps_command_reference/index.md)

## 官方来源

- **官方标题：** LAMMPS Documentation；EMC Setup documentation
- **官方章节或页面：** LAMMPS data 文件与输入脚本；EMC Setup 文件说明
- **官方 URL：** [LAMMPS 文档](https://docs.lammps.org/)；[EMC 官方网站](https://montecarlo.sourceforge.net/emc/Welcome.html)
- **本地来源：** `docs/08_lammps_file_formats/data_file.md`、`docs/06_lammps_user_guide_translation/input_scripts/input_script_syntax.md`、`docs/02_emc_setup_reference/setup_overview.md`
- **适用版本：** EMC 9.4.4；LAMMPS 22 Jul 2025 - Update 4
- **核对日期：** 2026-07-27
