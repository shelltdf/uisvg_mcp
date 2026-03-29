# 开发维护说明书

## 仓库结构（与本项目相关）

| 路径 | 说明 |
|------|------|
| `ai-software-engineering/` | 四阶段工程文档 |
| `uisvg-editor/` | Vue 3 + Vite 实现（**uisvg-editor-web**） |

## 依赖

- **Node.js**：建议 LTS（v18+）。
- 包管理：使用 `npm`（随 `package-lock.json` 若存在；否则首次 `npm install` 生成）。

## 构建 / 测试 / 运行 / 发布

在 `uisvg-editor/` 下提供 Python 封装脚本（与多实现规则一致）：

- `build.py`：生产构建
- `test.py`：冒烟检查（依赖已安装时运行 `npm run build`）
- `run.py`：开发服务器
- `publish.py`：输出 `dist/` 目录说明

等价 npm 命令见 `uisvg-editor/package.json`。

## 配置

- 无强制环境变量；开发主机/端口以 Vite 默认为准（`5173`）。

## UISVG 实现要点（与文档同步）

- **概念**：UISVG 是对 UI 结构的抽象；文件侧为 **SVG 扩展**（`http://uisvg.org/ns/1` + 对象根 `<g>` 下类型化语义节点）。见 `00-concept/uisvg-format-spec.md`。
- **类型标识**：以 uisvg 语义子元素的 **localName** 为准（`Form`、`Frame`、`Rect`…）；内存对象 **`UisvgObjectBundleV1.uisvgLocalName`**、大纲 **`OutlineNode.uisvgLocalName`** 与之对齐。旧版 **`kind`** / **`win.*`** 字符串仅在读入迁移路径中出现（`legacyLogicalKindToUisvgLocalName`）。
- **源码**：文档模型与迁移主逻辑在 `uisvg-editor/src/lib/uisvgDocument.ts`；语义读写、`normalizeBundle`、QName 展示在 `uisvg-editor/src/lib/uisvgMetaNode.ts`；右栏 UI 语义行与 `UiPropertiesPanelModel` 在 `uisvg-editor/src/lib/uiObjectProperties.ts`。
- **物理规格**：`02-physical/uisvg-editor-web/spec.md`。

## 关键模块（对齐 / 大纲列宽 / 画布）

| 模块 | 路径 | 说明 |
|------|------|------|
| 选中缩放与 Chrome 重布局 | `uisvg-editor/src/lib/svgElementResize.ts`（常量 `libraryPlacement.ts`，占位结构 `windowsUiControls.ts`） | `getResizeTargetElement`、`applyResizeDelta`、`ensureResizeChromeLayoutSynced`；详见 `02-physical/uisvg-editor-web/spec.md` |
| 多选对齐（字符串 DOM 解析、写回） | `uisvg-editor/src/lib/canvasClipboardAlign.ts` | `alignUisvgObjectRoots`；`ownerDocument !== window.document` 时优先 `transform` 父链；`SVGMatrix`→`DOMMatrix` 用 `[a,b,c,d,e,f]`，禁止 `new DOMMatrix(svgMatrix)` |
| 大纲列宽 provide/inject 与存储键 | `uisvg-editor/src/lib/outlineColumnResize.ts` | `outlineColumnResizeKey`；`OUTLINE_NAME_COL_STORAGE_KEY`（`uisvg-outline-name-col-pct`）；默认约 52% / 48%，拖动限制约 25%～75% |
| 外壳（菜单、工具栏、对齐调试 ref） | `uisvg-editor/src/components/AppShell.vue` | 对齐命令 `try/catch/finally`：`finally` 中写入 `alignDebugInfo`、递增 `alignDebugNonce`；工具栏六对齐图标常显、`disabled` 当可选中对象不足 2 |
| 大纲表头拖动条 | `uisvg-editor/src/components/OutlinePanel.vue` | 表头 `outline-col-resizer` 拖动调整 `nameColumnPercent`，松手后 `localStorage` |
| 大纲行 | `uisvg-editor/src/components/OutlineTreeItem.vue` | 注入列宽比例，与表头同 `flex`；名称/类型过长省略号 |
| 画布视图 | `uisvg-editor/src/components/CanvasView.vue` | 选中框/框选/吸附等；左下角 **仅** 展示对齐调试摘要（`selectionDebugLines` 由 `alignDebugInfo` + 占位符组成）；`v-if="showSelectionDebug"` |
| 工具栏 16×16 图标（含对齐） | `uisvg-editor/src/components/ToolbarIcon.vue` | `alignLeft` … `alignBottom` |
| 界面语言与文案键 | `uisvg-editor/src/composables/useI18n.ts`、`uisvg-editor/src/i18n/messages.ts` | 设置中切换 `zh`/`en`；`MessageKey` 与 `zh`/`en` 表需同步 |
| 属性侧栏文案与 tooltip 拼接 | `uisvg-editor/src/lib/propertyLabels.ts` | 导出函数入参为 `t`，非硬编码双语字符串 |
