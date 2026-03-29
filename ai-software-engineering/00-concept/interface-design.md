# 接口设计（程序间）

## 说明

本客户端以**本地文件**与 **SVG/uisvg 文档**为主要对外数据形态，**不包含**独立 HTTP/gRPC 服务接口。

## 文件接口

| 接口形态 | 说明 |
|----------|------|
| `*.ui.svg` | 符合 [uisvg-format-spec.md](./uisvg-format-spec.md) 的 UTF-8 文本文件；可被标准 SVG 渲染器消费可见子集 |

## GUI

窗口、菜单、画布操作等人机交互**不属于**本文件范畴，见 `product-design.md` 与 `01-logic/`。
