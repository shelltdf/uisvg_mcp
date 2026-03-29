# 系统设计：UISVG 编辑器

## 子系统

1. **Shell**：布局骨架、主题（Windows 风格浅色）、菜单/工具栏/可拖分割侧栏与状态栏；工具栏含 **六个对齐** 快捷（未满 2 个可移动选中对象时禁用）与 **调试** 开关（控制画布左下角 **仅对齐** 调试摘要）。行为细节见 `01-logic/detailed-design-editor-shell.md`。
2. **DocumentService**：加载/保存 `*.ui.svg`；**UISVG** 为 UI 结构的抽象，在实现上为 **SVG 扩展**（命名空间 `http://uisvg.org/ns/1`、对象根 `<g>` 下类型化语义子节点）；解析/迁移与 `02-physical` 一致。
3. **Outline**：仅展示 uisvg 对象根 `<g>` 树；虚拟根「uisvg::root」对应 `#layer-root`；与画布选中同步；节点携带 **`uisvgLocalName`**（与首个 uisvg 子元素 localName 一致）；表头 **标识（id）/UISVG 类型** 两列，行内显示 `id` 与类型字符串；列宽可拖动（比例持久化至浏览器存储）；文案随语言切换。
4. **Palette**：组件条目列表；插入操作产生对象根 `<g>` + uisvg 类型子节点 + 占位几何。
5. **Canvas**：视口变换、网格绘制、SVG 宿主；点选 / Shift 多选 / 框选解析为 uisvg 对象根；拖拽移动、吸附与 **多选对齐**（菜单/工具栏/右键触发，字符串 DOM 层实现见 `02-physical/uisvg-editor-web/spec.md` 与 `canvasClipboardAlign`）；**选中框缩放**后按控件类型 **Chrome 重布局**（`svgElementResize.ts`，见同规格与 `detailed-design-canvas.md`）。行为细节见 `01-logic/detailed-design-canvas.md`。
6. **Inspector（属性面板）**：选中项属性与文档片段展示；UI 语义写在 uisvg 类型子节点上。

## 依赖关系

```
Shell
 ├── DocumentService
 ├── Outline ←→ DocumentService
 ├── Palette → DocumentService / Canvas
 ├── Canvas ↔ DocumentService
 └── Inspector ← selection
```

## 与物理阶段对应

构建目标 **`uisvg-editor-web`** 对应 Vue SPA；行为与字段级细节以 `02-physical/uisvg-editor-web/spec.md` 为准。
