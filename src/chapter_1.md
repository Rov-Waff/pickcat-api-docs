# 概述

这个文档收集了PICKCat部分已知的API接口，旨在辅助一些脚本的开发。

> ⚠️ **请注意**
>
> - **文档并不完善**：目前只收录了部分模块与接口，大量接口（点赞、关注操作、举报、私信、搜索等）尚未整理，内容也会持续变动。
> - **部分内容未经验证**：不少字段、状态码与行为来自抓包分析或合理推断，并未逐一实测；文中标注「存疑」「推测」的地方尤其如此，接口也可能随服务端更新而失效。
> - **由 AI 辅助编写**：本文档由 AI 参与撰写与整理，可能存在错误、遗漏或过时之处。请以实际接口返回为准，发现问题欢迎指出。
>
> 最近一次公开接口抽查：**2026-11-08**（仅覆盖无需登录的接口）。

## 特征

- 尽量解释清晰，帮助脚本开发快速上手
- 会随接口变化持续更新（速度视情况而定）
- 响应示例大多来自真实请求或抓包，但**不保证完整与长期有效**

## 规约

1. 在每篇文档前都会有类似这样的说明

> 修改个人资料
> `/users/{userId}` PATCH **需要Cookie**

- 没有特殊标注的 API 都基于这个 URL：`https://pickcat.dao3.fun/api/v1`
- URL 中类似 `/abc/{userId}` 的表达里，`{xxx}` 是一个变量；一般可从变量名看出含义，例如 `{userId}` 是用户 ID
- 如果请求不需要用到 cookie，不会专门标注
- 部分写接口需要 `Idempotency-Key`：注册接口**强制**，发帖/上传等当前建议携带（详见各接口页）

2. 响应示例大多为真实返回，但可能经过精简、脱敏，或仅有结构而无真实数据。

## 错误响应

失败时统一返回 JSON：

```json
{ "statusCode": 401, "code": "UNAUTHENTICATED", "message": "Authentication is required" }
```

参数校验失败时会附带 `details`。`details` 的结构并不完全统一，常见两种：

```json
{
  "statusCode": 400,
  "code": "VALIDATION_FAILED",
  "message": "请求参数不合法",
  "details": { "password": ["Too small: expected string to have >=10 characters"] }
}
```

```json
{
  "statusCode": 400,
  "code": "VALIDATION_FAILED",
  "message": "请求参数不合法",
  "details": {
    "fieldErrors": [
      { "field": "title", "rule": "REQUIRED" },
      { "field": "markdown", "rule": "REQUIRED" }
    ]
  }
}
```

实测常见错误：

| HTTP | code | 说明 |
| --- | --- | --- |
| 400 | `IDEMPOTENCY_KEY_REQUIRED` | 发起注册缺少 `Idempotency-Key` 头 |
| 400 | `VALIDATION_FAILED` | 参数校验失败，附 `details` |
| 401 | `UNAUTHENTICATED` / `AUTHENTICATION_REQUIRED` | 未登录或会话已失效；不同接口可能使用不同 code |
| 404 | `NOT_FOUND` / `USER_NOT_FOUND` / `TOPIC_NOT_FOUND` / `EMOJI_NOT_FOUND` | 资源不存在 |
| 409 | `ENTRANCE_EXAM_COOLDOWN` | 入站考试冷却中 |
| 422 | `EXTERNAL_LINK_NOT_ALLOWED` | 发帖正文含社区外链接 |

## 开源

根据CC0协议共享知识
