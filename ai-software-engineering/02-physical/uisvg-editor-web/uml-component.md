# 组件图（uisvg-editor-web）

```mermaid
flowchart TB
  subgraph shell [AppShell]
    MB[MenuBar]
    TB[ToolBar]
    SB[StatusBar]
    OL[OutlinePanel]
    CP[ComponentPalette]
    CV[CanvasView]
    DP[DataPanel]
  end
  DOC[uisvgDocument / File IO]
  MB --> DOC
  TB --> DOC
  OL --> DOC
  CP --> CV
  CV --> DOC
  DP --> DOC
```
