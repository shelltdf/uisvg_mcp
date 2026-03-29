# 详细设计：编辑器外壳（菜单 / 工具栏 / 侧栏 / 状态栏）

## 布局

- 纵向：`MenuBar` → `ToolBar` → `MainRow`（左 dock `SideLeft` | 中 `Canvas` | 右 dock `PropsPanel`）→ `StatusBar`。
- `SideLeft` 为 **dock 侧栏**：`Outline` 与 `ComponentPalette` 之间为 **可拖拽水平分割条**（典型 IDE 工具窗）；**UI 大纲**、**组件库**整体及组件库内各分类均可 **独立折叠/展开** 标题区。
- 右侧 **`DataPanel`** 为 dock 侧栏：自上而下为 **SVG 结构**、**UI 属性**、**SVG 对象属性** 三个分区，**各自可折叠/展开**；其中 **UI 属性** 可编辑平台 `data-*` 与 `data-uisvg-ui-props`；**SVG 对象属性** 含显示名称与其余 XML 等；`Canvas` 与其之间为 **可拖拽垂直分割条** 以调整侧栏宽度。
- 左、右 dock **常显**（可调宽度/左侧上下分割高度）；各 **分区** 独立 **侧栏折叠**（收起到左/右边条），无「整栏隐藏」按钮。
- `ComponentPalette` 顶层分为两块可 **折叠/展开**：**基础形状**、**Windows 桌面控件**（默认展开）。条目 **主行** 为当前语言的显示名（`uiLib.*`），**副行** 为 UISVG 语义标签（如 `uisvg:Button`），随语言切换而非中英并列。**Windows** 以 WinForms 类型名为放置主键，并与 Win32 / Qt 对照（悬停 `paletteTooltip`）；画布占位 `<g>` 可带 `data-winforms` 等。各按钮左侧有象形 **SVG** 小图标。`uisvg` 大纲中类型为语义子元素 **localName**（如 `Button`、`Form`）。

## 交互

- 菜单：文件（新建、打开、保存、另存为）；**编辑**（撤销占位；**六种对齐**，至少 2 个可选中对象时可用）；工具（像素图识别 UI）；**视图**（重置视图、全部显示画布、预览、画布全屏、画布设置、**显示/隐藏左下角对齐调试**）；帮助。
- 工具栏：新建/打开/保存；重置视图、全部显示画布；**六个对齐图标**（`ToolbarIcon`，与编辑菜单同源；未满足条件时禁用）；弹性空白；预览、画布全屏、**对齐调试开关**（调试图标）。
- **UI 大纲**：表头为 **标识（`id`）**、**UISVG 类型** 两列；行内第一列为对象 DOM `id`、第二列为类型全称；两列之间可 **拖动竖向分隔条** 调整比例（约 25%～75%），比例持久化到 `localStorage`（`uisvg-outline-name-col-pct`）；行内省略号，完整内容见 `title`。表头文案键 `outline.columnId` / `outline.columnUisvgType`（`useI18n`）。
- **右侧属性（DataPanel）**：分区标题、表头、对象标识、XML 属性表等与语言相关的字符串来自 `i18n/messages.ts`（`panel.*` 等）；**UI 语义**表格「名称」列按当前语言只显示中文名或英文名（`uiObjectProperties.formatSemanticRowLabel`，数据行可带 `nameEn`）；tooltip 字符串由 `propertyLabels.ts` 内函数接收 `t` 拼接（`tooltip.*` / `outline.itemHint` 等）。
- 状态栏：显示就绪、缩放与操作提示等。

## Windows 风格

- 使用浅灰背景（约 `#f0f0f0`～`#ffffff`）、细边框（`#d0d0d0`）、Segoe UI 或系统 UI 字体栈。
