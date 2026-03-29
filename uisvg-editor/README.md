# UISVG Editor（Vue）

基于 Vue 3 + Vite 的 **UISVG** 可视化编辑器，界面布局贴近 Windows 窗口习惯。设计稿扩展名为 **`*.ui.svg`**（SVG + uisvg 语义），可用常规 SVG 软件打开。

## UISVG 是什么

**UISVG** 是对 **UI 结构**的抽象描述（有哪些对象、类型与关系），不是某一种 UI 框架的专有格式。  
在工程上，它是 **SVG 的扩展方案**：在标准 SVG 可绘制图形的前提下，用命名空间与约定节点/属性承载界面语义，使同一份文件既可预览又可被工具解析。

规范说明见：`ai-software-engineering/00-concept/uisvg-format-spec.md`。

## 依赖

- Node.js 18+（建议 LTS）

## 命令

| 操作 | npm | Python 封装 |
|------|-----|-------------|
| 安装依赖 | `npm install` | （先执行 npm install） |
| 开发 | `npm run dev` | `python run.py` |
| 构建 | `npm run build` | `python build.py` |
| 冒烟 | — | `python test.py` |
| 发布目录 | `npm run build` → `dist/` | `python publish.py` |

## 画布与编辑

- **滚轮**：缩放（以指针为锚点）；在 **左下角对齐调试** 面板内滚动时不缩放画布。
- **中键拖拽**：平移视图。
- **左键**：点选 UISVG 对象根；**Shift+左键**、**框选** 多选；拖拽已选对象移动。
- **对齐**：**工具栏** 始终显示六个对齐图标（16×16）；未选满 2 个可移动对象时为 **禁用**。**编辑** 菜单与 **画布右键** 亦可执行对齐。实现见 `src/lib/canvasClipboardAlign.ts`；详细说明见 `ai-software-engineering/01-logic/detailed-design-canvas.md`。
- **对齐调试**：**视图** 或工具栏 **调试图标** 控制左下角面板开关；面板内 **仅** 对齐摘要（无选中框/框选长日志）。
- **UI 大纲**：**标识 (ID)** 与 **UISVG 类型** 两列；表头 **竖向分隔条** 可拖动列宽（约 25%～75%），键名 `uisvg-outline-name-col-pct` 存于 `localStorage`（历史键名未改，避免丢失列宽）。

## 规范

见 `ai-software-engineering/00-concept/uisvg-format-spec.md`（与上一节「UISVG 是什么」一致）。

更完整的交互说明见 `ai-software-engineering/03-ops/user-manual.md`；实现映射见 `ai-software-engineering/02-physical/uisvg-editor-web/mapping.md`。

## 实现备忘（类型字段）

- 对象类型以 **DOM 中 uisvg 子元素名（localName）** 为权威；代码侧 bundle / 大纲使用 **`uisvgLocalName`**，与 `uisvg:Form` 中的 `Form` 一致。
- 主要入口：`src/lib/uisvgMetaNode.ts`（读写 bundle）、`src/lib/uisvgDocument.ts`（大纲）、`src/lib/uiObjectProperties.ts`（右栏语义表）。
