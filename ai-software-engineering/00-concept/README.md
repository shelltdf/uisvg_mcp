# 概念阶段（00-concept）

本仓库主线产品：**UISVG 编辑器**——基于 Web（Vue）的 UI 设计工具。**UISVG** 是对 UI 结构的抽象描述；文件格式为 **SVG 的扩展方案** **uisvg**（`*.ui.svg`）。

## 索引

| 文档 | 职责 |
|------|------|
| [product-design.md](./product-design.md) | 产品设计（唯一主文档）：愿景与目标用户；**主窗口布局**（菜单/工具栏/左大纲+组件库/画布/右属性/底状态栏）；**编辑器外壳与画布**（工具栏六对齐常显与禁用条件、调试图与左下角仅对齐调试、画布多选与菜单/右键对齐、大纲名称/类型列拖动与本地持久化）；核心用例表；成功标准 |
| [software-design.md](./software-design.md) | 软件结构、模块划分 |
| [database-design.md](./database-design.md) | 存储与持久化（文件、本地状态） |
| [interface-design.md](./interface-design.md) | 程序间接口（本客户端以文件格式为主；非 GUI） |
| [uisvg-format-spec.md](./uisvg-format-spec.md) | **uisvg** 文件格式（SVG 扩展）规范 |

## UI 几何权威

编辑器画布上的控件几何与层级关系以设计文件及画布状态为准；概念资产可配合 `ui.svg` 类资源描述视觉规范（若存在）。
