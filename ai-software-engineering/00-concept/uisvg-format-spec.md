# uisvg 文件格式规范（1.0 草案）

## 定位

**UISVG** 是对 **UI 结构**的抽象描述：用一套与具体控件库解耦的语义（对象类型、层级、属性等）表达界面由哪些部分组成、各自扮演什么角色。

在实现上，UISVG 是 **SVG 的扩展方案**：在标准 **SVG**（推荐 SVG 1.1 子集）之上增加命名空间、约定元素与属性，使单个文件同时承载：

1. **可被任意 SVG 实现渲染的矢量内容**（根元素仍为 `<svg>`）。
2. **上述 UI 抽象的结构化实例化数据**（层级、组件类型、画布视口偏好、与几何对齐的语义等）。

文件扩展名：**`*.ui.svg`**（先 `.ui` 再 `.svg`，便于识别且 MIME 仍可按 `image/svg+xml` 处理）。

## 兼容性原则

- **必须**：根元素为 `http://www.w3.org/2000/svg` 命名空间下的 `<svg>`，且整体为良构 XML。
- **应当**：可见图形使用标准 SVG 元素（`rect`、`g`、`text` 等），以便 Inkscape、浏览器、预览器直接打开。
- **可以**：将 uisvg 专有信息放在 `<metadata>` 内，避免干扰多数仅渲染图形的查看器。

## 命名空间

建议使用以下 URI 作为 uisvg 元素命名空间（可在实现中固定）：

```text
http://uisvg.org/ns/1
```

前缀约定：`uisvg`（仅为文档说明；实际 XML 中以前缀绑定为准）。

## 根元素与画布（当前编辑器实现）

根 `<svg>` 上除标准 `width` / `height` / `viewBox` / `overflow` 外，可使用：

| 属性 | 含义 |
|------|------|
| `xmlns:uisvg` | 绑定 `http://uisvg.org/ns/1`（推荐） |
| `data-uisvg-version` | uisvg 规范主版本，例如 `1.0` |
| `data-uisvg-editor` | 最后写入的编辑器标识（短字符串） |
| `data-uisvg-grid` | 逻辑网格步长（用户单位，与画布一致） |
| `data-uisvg-dpi` | 文档/导出参考 DPI（用户单位仍为 px） |

逻辑画布尺寸、网格、DPI 以根 `svg` 属性为准；**白底、网格与左上角说明**仅由 **UISVG 编辑器视口**绘制，**不**写入交付物（参见 `02-physical/uisvg-editor-web/spec.md`）。

## 内容层：对象根与 uisvg 语义（当前实现）

- **内容根组**：`#layer-root`（及可选 `#layer-sibling`）为顶层 `<g>`，承载画布内图元。
- **可编辑对象**：每个对象对应一个带 **`id`** 的对象根 `<g id="…">`。
- **UISVG 语义**：在该 `<g>` 下，**第一个**子节点推荐使用 **uisvg 命名空间**（`http://uisvg.org/ns/1`）中的**具体类型元素**；**元素名（localName）即为类型标识**，与 WinForms 类名或 `Frame`/`Rect`/`Text` 等一致，例如：
  - 通用容器 / 画布根语义：`Frame`
  - WinForms 映射：`Form`、`Button`、`TextBox` 等
- 语义元素上承载：`label`、`data-uisvg-ui-props`（JSON）、`data-winforms` / `data-win32` / `data-qt`、可选 `from` 等（见实现）。
- **内存与旧版 JSON**：编辑器内对象 bundle（`v: 1`）使用字段 **`uisvgLocalName`**，与上述 **localName** 对齐。历史文件若在 JSON 中仍写 **`kind`**（如 `frame`、`win.Form`）或对象根上仍有 **`data-uisvg-kind`**，打开时会迁移为类型化子元素并规范为同一 localName；保存后以子元素为准，不再依赖单独 `kind` 字段。
- **几何**：语义节点之后的兄弟节点为标准 SVG（`rect`、`text`、`path` 等）。**寻址与编辑以对象根 `<g id>` 为主**；纯几何子节点可不设 `id`。**uisvg 语义子节点**仍建议稳定 `id`（如 `{gId}-ui`），便于与实现一致。
- **编辑器子节点标记**：部分占位控件在几何子节点上使用 **`data-uisvg-part`**（如 `listview-face`、`datagridview-hline-0`），供编辑器在 **缩放后** 重算标题栏、网格线、固定厚度槽道等；该属性随 `.ui.svg` 持久化，非编辑器实现可忽略。

**说明**：嵌入 HTML（如 Vue `v-html`）时，勿在 SVG 内使用 HTML 敏感的标签名作 uisvg 子节点；实现选用具体类型名（如 `Frame`）与 `bundle` 容器，避免使用会与 HTML 解析冲突的 `meta`。

## 兼容：旧版 metadata / 分散属性

历史文档可能在 `<metadata>` 内含 `uisvg:root`、`uisvg:canvas`、`uisvg:tree` 等；编辑器在打开时**迁移**到当前 DOM 模型（画布属性提升到根 `svg`，大纲由 DOM 推导）。  
仍可能存在的 **`bundle` / `meta`（CDATA JSON）** 或对象根上的 **`data-uisvg-*` / `data-winforms`** 可被读入并在保存时合并为上述语义模型（JSON 内 **`kind` → `uisvgLocalName`** 在读入时归一）；具体行为以 `uisvg-editor` 与 `02-physical` 为准。

## 可见层（标准 SVG）

标准 SVG 内容（`<defs>`、`clipPath`、`g`、`rect`、`text` …）与 uisvg 语义通过**对象根 `g` 的 `id`** 及**其下语义子节点**关联；旧版「仅 `data-*` 写在 `g` 上」的写法在迁移后写入语义子节点。

## 字符编码

**UTF-8**（无 BOM 或与工具链一致即可）。

## 版本演进

- 主版本变更时升级 `data-uisvg-version` 与本文档；解析器应忽略未知元素/属性（向前兼容）。
