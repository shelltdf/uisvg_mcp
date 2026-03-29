# 模型元素 → 源码映射（uisvg-editor-web）

| 元素/能力 | 源码路径 |
|-----------|----------|
| 应用入口 | `uisvg-editor/src/main.ts` |
| 根布局 | `uisvg-editor/src/App.vue` |
| 外壳（菜单/工具/状态/三栏） | `uisvg-editor/src/components/AppShell.vue` |
| 画布（网格/白底与左上角说明叠层/变换/左键拾取/选中框/拖拽吸附/框选/右键菜单） | `uisvg-editor/src/components/CanvasView.vue`；左上角尺寸/DPI/原点、缩放手柄 `title`、选中框 `title`、对齐调试占位与复制按钮等文案键为 `canvas.*`（见 `i18n/messages.ts`）；左下角对齐调试正文来自 `alignDebugInfo`（由 `AppShell` 传入），`alignDebugNonce` 用于强制刷新 |
| 图元平移（rect/text/circle/g 等） | `uisvg-editor/src/lib/svgElementMove.ts` |
| 选中缩放与控件 Chrome 重布局（`getResizeTargetElement`、`applyResizeDelta`、`ensureResizeChromeLayoutSynced`；按 `data-uisvg-part` 与控件类型重排子几何） | `uisvg-editor/src/lib/svgElementResize.ts`；默认尺寸与网格/滚动条等常量 `libraryPlacement.ts`；占位图元结构 `windowsUiControls.ts` |
| 对齐线与吸附目标 | `uisvg-editor/src/lib/canvasSnap.ts` |
| 剥离编辑器辅助节点 | `stripEditorCanvasChromeFromMarkup`、`removeEditorCanvasChrome`（`uisvg-editor/src/lib/uisvgDocument.ts`）；打开/保存及任意文档变更路径 |
| 画布设置对话框 | `uisvg-editor/src/components/CanvasSettingsDialog.vue` |
| 属性面板（上方全局 SVG DOM 树 / 属性表 / 显示名称 / 只读 SVG 片段） | `uisvg-editor/src/components/DataPanel.vue` |
| 界面语言（`zh` / `en`）、文案表 `t(key)` | `uisvg-editor/src/composables/useI18n.ts`、`uisvg-editor/src/i18n/messages.ts` |
| 大纲/对象 tooltip 纯函数（入参 `TranslateFn`） | `uisvg-editor/src/lib/propertyLabels.ts` |
| UI 语义行标签（按语言选 `name` / `nameEn`） | `uisvg-editor/src/lib/uiObjectProperties.ts`（`formatSemanticRowLabel`） |
| SVG DOM 树视图 | `uisvg-editor/src/components/SvgDomTree.vue`、`SvgDomTreeItem.vue` |
| 选中元素解析与写回 | `uisvg-editor/src/lib/uisvgDocument.ts`（`resolveDomElementId`、`resolveCanvasPickToUisvgObjectDomId`、`getSelectedElementSnapshot`、`applyElementEdits`、`parseUisvgOutline` 等） |
| UISVG 语义读写（`uisvgLocalName`、`UisvgObjectBundleV1`、legacy `kind` 迁移） | `uisvg-editor/src/lib/uisvgMetaNode.ts` |
| 文档与 uisvg 常量、`OutlineNode`、`parseUisvgOutline` | `uisvg-editor/src/lib/uisvgDocument.ts` |
| 右栏 UI 属性模型（`UiPropertiesPanelModel`、`semanticRowsForUisvgLocalName`） | `uisvg-editor/src/lib/uiObjectProperties.ts` |
| UI 大纲树（名称 / UISVG 类型两列；列宽与 `OutlinePanel` 表头拖动条同步） | `uisvg-editor/src/components/OutlineTreeItem.vue`、`OutlinePanel.vue` |
| 大纲列宽上下文（inject） | `uisvg-editor/src/lib/outlineColumnResize.ts` |
| 多选对齐、剪贴板删除/序列化 | `uisvg-editor/src/lib/canvasClipboardAlign.ts` |
| 画布命中 → uisvg 对象根 | `CanvasView.vue` + `resolveCanvasPickToUisvgObjectDomId` |
| 位图导入写文档 | `uisvg-editor/src/lib/rasterUiAppend.ts` |
| 组件占位与库 | `uisvg-editor/src/lib/windowsUiControls.ts`、`libraryPlacement.ts` |
| Windows 主题样式 | `uisvg-editor/src/styles/win-theme.css` |
| WinForms 组件库数据与占位图元 | `uisvg-editor/src/lib/windowsUiControls.ts` |
| 组件库象形小图标（16×16） | `uisvg-editor/src/lib/windowsPaletteIcons.ts` |
| 组件库图标组件 | `uisvg-editor/src/components/PaletteItemIcon.vue` |
| 工具栏矢量图标 | `uisvg-editor/src/components/ToolbarIcon.vue` |
