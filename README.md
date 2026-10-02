# Pickcat 社区 API 文档

使用 [mdBook](https://rust-lang.github.io/mdBook/) 构建的 Pickcat（`cdsq.dao3.fun`）社区 API 文档，旨在辅助脚本与第三方应用的开发。

> ⚠️ **请注意**
>
> - **文档并不完善**：目前只收录了部分模块与接口，大量接口（发帖、回复、点赞、关注、举报、私信、搜索等）尚未整理。
> - **部分内容未经验证**：不少字段、状态码与行为来自抓包分析或合理推断，并未逐一实测；文中标注「存疑」「推测」的地方尤其如此。
> - **由 AI 辅助编写**：本文档由 AI 参与撰写与整理，可能存在错误、遗漏或过时之处。请以实际接口返回为准，发现问题欢迎指出。

## 内容

| 模块 | 说明 |
| --- | --- |
| 鉴权 | 登录、当前会话、登出、注册、邮箱验证、入站考试 |
| 用户 | 资料、内容、徽章、动态与贡献、等级与配额、账户设置 |
| 主题与内容 | 主题列表与推荐、主题详情、楼层、投稿审核 |
| 分区标签 | 全部分区与侧边子标签 |
| 通知 | 未读通知汇总 |
| 阅读会话 | 阅读行为埋点上报 |
| 媒体资源 | 头像、表情、文件 |

完整目录见 [`src/SUMMARY.md`](src/SUMMARY.md)。

## 本地构建

### 依赖

- [Rust / Cargo](https://rustup.rs/)
- [mdBook](https://rust-lang.github.io/mdBook/) `v0.5+`
- `mdbook-langtabs`（代码多语言标签预处理器）

```bash
cargo install mdbook
cargo install mdbook-langtabs
```

### 预览与构建

```bash
mdbook serve --open   # 本地预览（默认 http://localhost:3000）
mdbook build          # 静态输出到 book/
```

> 若未安装 `mdbook-langtabs`，可临时注释掉 `book.toml` 中的 `[preprocessor.langtabs]` 再构建，此时多语言示例会并排显示为普通代码块。

## 目录结构

```
.
├── book.toml            # mdBook 配置
├── langtabs.css / .js   # 多语言代码标签的样式与脚本
├── src/
│   ├── SUMMARY.md       # 目录
│   ├── chapter_1.md     # 概述与约定
│   ├── auth.md          # 鉴权（子页见 auth/）
│   ├── user.md          # 用户（子页见 user/）
│   ├── topic.md         # 主题与内容（子页见 topic/）
│   ├── tag.md
│   ├── notification.md
│   ├── reading-session.md
│   └── media.md
└── LICENSE              # CC0 1.0
```

## 接口约定

- **基础地址**：`https://cdsq.dao3.fun/api/v1`
- **鉴权**：服务端会话 Cookie `pickcat_session`（非 JWT），有效期 7 天；登出用 `DELETE /api/v1/session`
- **分页**：游标分页，统一为 `pageInfo.hasNextPage` / `pageInfo.nextCursor`
- **错误**：统一返回 `{ statusCode, code, message, details? }`，常见错误见「概述」

## 贡献

欢迎通过 Issue / PR 补充或修正接口。为保持风格一致，请尽量遵循：

- 每个接口页包含：头部行 `> {中文描述} \`{路径}\` {METHOD}`、`请求体` / `响应体`、`值得注意的`、`示例`
- `示例` 提供 **Rust / Python / TypeScript** 三种语言（使用 `<!-- langtabs-start -->` / `<!-- langtabs-end -->` 包裹）
- 字段表统一为 `| KEY | VALUE | TYPE |`
- 未经验证的信息请明确标注

## 许可证

本项目基于 [CC0 1.0](LICENSE) 协议共享。
