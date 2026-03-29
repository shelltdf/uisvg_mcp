# 物理规格：uisvg-editor-web

## 对外行为

### 文件

- 打开/保存扩展名：**`*.ui.svg`**
- 编码：**UTF-8**
- 新建文档最小结构：根 `<svg>`（含 `xmlns:uisvg`、`data-uisvg-*`、画布尺寸）、`#layer-root` 内 uisvg 类型子节点（如 `Frame`）及几何；详见 `00-concept/uisvg-format-spec.md`。

### 画布

| 项目 | 规格 |
|------|------|
| 默认画布逻辑尺寸 | 1200 × 800（用户单位） |
| 默认网格步长 | 16 |
| 默认 DPI | 96 |
| 缩放范围 | 约 0.1～8（实现可调） |
| 平移 | 二维 `tx, ty` 像素偏移叠加于变换 |
| 缩放输入 | 鼠标滚轮，锚点为指针 |
| 平移输入 | **仅**中键拖拽 |
| 画布右键菜单 | 自上而下：**复制** → **粘贴** → 分隔线 → **对齐**（子菜单：六种）→ 分隔线 → **删除**（末项） |
| 选择输入 | 左键命中后解析为 **UISVG 对象根**：`#layer-root` 或带 uisvg 语义的 `<g id>`；**Shift+左键** 多选；**框选** 与画布求交多选；非 uisvg 子树不建立选中；嵌套几何命中解析到所属对象根 `g` |
| 大纲逻辑 id | 画布选中 `#layer-root` 时，大纲侧逻辑 id 为 **`uisvg-root`**（虚拟根「uisvg::root」），与左侧大纲一致 |
| 选中反馈 | 逻辑画布坐标系内绘制虚线选中框（叠层）；多选时为各对象框 **并集** |
| 移动与吸附 | 左键拖拽已选中对象根（可多选一并移动）；与其它图元包络对齐，红虚线吸附（阈值约 7px 屏幕距离） |
| 剪贴板 | 内部 JSON 序列化对象根；粘贴生成新 id |
| 对齐 | 至少 2 个非 `uisvg-root` 的可移动对象根；六种对齐在 **内存 DOM 字符串** 上计算并写回；见 `canvasClipboardAlign.ts`；宿主在 `finally` 中写入对齐调试摘要，避免序列化异常导致左下角无反馈 |
| 视图与文档同步 | 编辑不自动重置平移/缩放；新建/打开/重置视图时恢复；「全部显示画布」按视口适配 |
| 预览 | 新窗口打开当前 SVG（剥离编辑器辅助节点） |
| 画布逻辑边界 | 根 `svg` 的 `width`/`height`/`viewBox` 与 `data-uisvg-grid`、`data-uisvg-dpi`；白底/网格/角标仅视口层；左上角只读标注（尺寸、DPI、原点）、选中框缩放手柄 `title`、选中框整体 `title`（几何行）、对齐调试区占位与复制反馈等使用 `canvas.*` 文案键（`i18n/messages.ts`），随界面语言切换 |
| 画布设置 | 对话框写回根 `svg` 属性 |
| 右侧栏 | **SVG 结构**（DOM 树）；**UI 属性**（读写在对象根下 uisvg 类型子节点的 `data-uisvg-ui-props` 与平台属性）；**SVG 对象属性**（对象根 `g` 的 XML 属性表与显示名等）；表头「名称/值」、对象标识行、dock 标题等文案键见 `uisvg-editor/src/i18n/messages.ts`（`panel.*`）；UI 语义表「名称」列按当前语言在 `formatSemanticRowLabel`（`uiObjectProperties.ts`）中取中文 `name` 或英文 `nameEn`，不中英并列 |
| 顶层分层 | 新图元插入 `#layer-root`；`#layer-sibling` 为可选顶层组 |
| 选中框缩放 | 对当前选中 uisvg 对象根内 **主几何**（`getResizeTargetElement`：优先带 `data-uisvg-part` 的 `face`/`frame`/`track` 等，否则首个 `rect`/`circle`/`ellipse`）拖动缩放手柄；增量写回 `x`/`y`/`width`/`height`（或圆/椭圆等价属性）。缩放结束后对同一对象根调用 **`ensureResizeChromeLayoutSynced`**（`svgElementResize.ts`），按控件类型重排子节点，**避免**整组比例缩放导致的标题栏/网格线/固定厚度控件变形 |
| 控件 Chrome 重布局（实现约定） | 逻辑与常量集中在 **`uisvg-editor/src/lib/svgElementResize.ts`**；各控件默认占位尺寸与数值常量在 **`libraryPlacement.ts`**；**`windowsUiControls.ts`** 生成占位 SVG 时为关键子节点设置 **`data-uisvg-part`**。含 **Form**、**ToolStrip**、**GroupBox**、**TabControl**、**ListBox** / **ListView** / **TreeView**、**TrackBar**（`trackbar-face` + 横向细槽 `trackbar-track` + `trackbar-thumb`；旧稿无 face 时首次同步可插入 face）、**ProgressBar**、**HScrollBar**（`hscrollbar-face` + 固定高度横向槽）、**VScrollBar**（`vscrollbar-face` + 固定宽度竖向槽）、**DataGridView**（`datagridview-face` + `datagridview-hline-0..3` + `datagridview-vline-0..2`；网格线坐标按默认 **160×88** 与 `libraryPlacement` 中 `DATAGRIDVIEW_*` 常量比例缩放后 **四舍五入为整数**）、**ComboBox** / **NumericUpDown** / **DateTimePicker** 等；完整分支以源码 `is*ResizeGroup` / `relayout*Chrome` 为准 |

### UI 大纲

- 根行：**uisvg::root**（逻辑 id `uisvg-root`），对应 DOM `#layer-root`。
- **仅列出 uisvg 对象根 `<g id>`**，不单独列出 uisvg 命名空间语义子节点（`Frame`/`Form` 等由父 `g` 代表）。
- 大纲节点模型（实现）：**`OutlineNode.uisvgLocalName`** 与对象根下首个 uisvg 子元素 **localName** 一致（虚拟根为 `uisvg.root` / 无层时为 `svg`）；界面 **UISVG 类型** 列由其推导 **QName**（如 `uisvg:Form`）。
- 表头两列：**标识（DOM `id`）**、**UISVG 类型**（由 uisvg 语义子元素 localName 得到 QName，如 `uisvg:Form`）；文案键 `outline.columnId` / `outline.columnUisvgType`，随界面语言切换；行内第一列显示 `id`、第二列显示类型字符串；列宽可拖动调整并持久化；行内过长省略，完整见悬停 `title`（`outlineItemTitle(..., t)` 与 `tooltip.*`，实现于 `propertyLabels.ts`，须传入 `useI18n().t`）。

### 语义 bundle（实现）

- 对象根关联的 **`UisvgObjectBundleV1`**（见 `uisvgMetaNode.ts`）使用 **`uisvgLocalName`**（如 `Form`、`Frame`），与 DOM 中 uisvg 类型子元素名一致；**不再**以独立字段 **`kind`**（`frame` / `win.Form`）作为持久化主字段。读入旧 JSON 或 `data-uisvg-kind` 时迁移归一。

### Shell

- 菜单栏、工具栏、左（UI 大纲 + 组件库）、中（画布）、右（属性）、状态栏。
- 界面文案：**中文 / English** 由设置中的语言切换；侧栏表头、属性列标题、tooltip 等使用 `uisvg-editor/src/i18n/messages.ts`，**不**采用「中文 (English)」并列一栏。
- 工具栏：16×16 矢量图标（含 **对齐** 六图标）；含全部显示画布、预览、画布全屏、**对齐调试开关** 等。
- 左侧 dock：大纲与组件库可分割；右侧属性可分割；各块可收起到侧条。
- 组件库「Windows」：以 WinForms 名为准，附 Win32/Qt 对照；**单击**插入时在内容根 `#layer-root` 下新建对象根；**拖入**画布时按指针落点判断父级：命中 **Form / Panel / GroupBox / TabControl / SplitContainer / FlowLayoutPanel / TableLayoutPanel** 等容器（含从子控件向上解析）则新对象根作为该容器的子节点，局部 `translate` 落在客户区内；否则插入在 `#layer-root` 下（与单击占位策略一致时可由实现回退）。

## 错误与退出

- Web 应用无进程退出码；文件 API 失败时在状态栏或 `alert` 提示。

## 重要过程

1. **保存**：序列化当前 SVG 字符串，下载为 `.ui.svg`；剥离编辑器专用叠层节点（若曾注入）。
2. **打开**：FileReader 读文本；执行元数据迁移与 legacy uisvg 属性迁移后再编辑。
