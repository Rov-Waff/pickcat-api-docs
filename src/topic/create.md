# 发布主题/回帖

> 发布内容 `/api/v1/posts` POST **需要Cookie**

发布主题首楼或回帖，内容走安全审核，属于**异步受理**（`202 Accepted`）。

## 请求头

| KEY             | VALUE                     | 说明                       |
| --------------- | ------------------------- | -------------------------- |
| content-type    | `application/json`        |                            |
| Idempotency-Key | `<uuid>`                  | **必填**，防止重复提交     |
| origin          | `https://cdsq.dao3.fun`   |                            |

## 请求体

发布主题首楼：

```json
{
  "title": "「不完整」Pickcat部分API文档",
  "markdown": "正文，图片写 ![01a0ff24-...]",
  "kind": "DISCUSSION",
  "tagIds": ["01a0ab26-84a8-718b-996a-3960a4789d05"]
}
```

| KEY      | VALUE                                  | TYPE      |
| -------- | -------------------------------------- | --------- |
| title    | 标题（发主题时必填）                   | String    |
| markdown | 正文，图片以 `![fileId]` 引用          | String    |
| kind     | `DISCUSSION`/`QUESTION`/`ANNOUNCEMENT` | String    |
| tagIds   | 分区标签UUID列表                       | ArrayList |

回帖（`replyToPostNumber` 可选，用于楼中楼）：

```json
{
  "topicId": "01a0c95a-10fa-79da-b024-f31384f0f805",
  "markdown": "合影",
  "replyToPostNumber": 1
}
```

| KEY               | VALUE                      | TYPE           |
| ----------------- | -------------------------- | -------------- |
| topicId           | 目标主题UUID               | String         |
| replyToPostNumber | 回复的目标楼层号，可为 null | Integer/Option |

## 响应体

### 成功：202 Accepted（异步审核）

```json
{
  "submissionId": "01a0ff25-1f05-7f09-8d1b-a32e2b0bab00",
  "topicId": "01a0ff25-1f07-77f3-beb8-0dabe6dba5f3",
  "postId": "01a0ff25-1f0a-7ec1-890d-86612754c302",
  "status": "PENDING_PROVIDER"
}
```

| KEY          | VALUE             | TYPE   |
| ------------ | ----------------- | ------ |
| submissionId | 审核记录UUID      | String |
| topicId      | 预先生成的主题UUID | String |
| postId       | 预先生成的楼层UUID | String |
| status       | 审核状态，如 `PENDING_PROVIDER` | String |

- `202` 表示已受理但**尚未发布**：先落库生成 `topicId` / `postId`，再送第三方内容安全审核。
- 响应头 `location: /api/v1/post-submissions/{submissionId}`。
- 审核期间 `GET /users/{id}/topics` 中看不到该主题。

### 失败：422 含站外链接

```json
{
  "statusCode": 422,
  "code": "EXTERNAL_LINK_NOT_ALLOWED",
  "message": "Links outside the community are not allowed",
  "details": { "field": "markdown", "host": "pickcat-docs.xiaole6324.fun" }
}
```

## 值得注意的

- 所有写接口都需要 `Idempotency-Key` 请求头。
- `markdown` 中**不允许社区外的链接**，否则返回 `422 EXTERNAL_LINK_NOT_ALLOWED`，`details` 会指出字段与命中的域名。
- 图片先通过 [`POST /files`](../media.md#图片上传) 上传，正文中以 `![fileId]`（不是 URL）引用。
- 提交后进入审核队列，可查询[投稿审核](./submission.md)。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::header::HeaderName;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 先登录 (见《登录》)
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": "xxxx@gmail.com", "password": "P@ssW0rd123" }))
        .send().await?.error_for_status()?;

    let resp = client.post(format!("{BASE_URL}/posts"))
        .header(HeaderName::from_static("idempotency-key"),
                "d384a653-0000-4000-8000-000000000000")
        .json(&json!({
            "title": "「不完整」Pickcat部分API文档",
            "markdown": "正文，图片写 ![01a0ff24-...]",
            "kind": "DISCUSSION",
            "tagIds": ["01a0ab26-84a8-718b-996a-3960a4789d05"],
        }))
        .send().await?;

    println!("HTTP {}", resp.status());
    let body: Value = resp.json().await?;
    println!("submissionId: {}", body["submissionId"]);
    println!("status      : {}", body["status"]); // PENDING_PROVIDER
    Ok(())
}
```
```python
import uuid
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

with requests.Session() as s:
    # 先登录 (见《登录》)
    s.post(f"{BASE_URL}/session",
           json={"username": "xxxx@gmail.com", "password": "P@ssW0rd123"}).raise_for_status()

    resp = s.post(
        f"{BASE_URL}/posts",
        headers={"Idempotency-Key": str(uuid.uuid4())},
        json={
            "title": "「不完整」Pickcat部分API文档",
            "markdown": "正文，图片写 ![01a0ff24-...]",
            "kind": "DISCUSSION",
            "tagIds": ["01a0ab26-84a8-718b-996a-3960a4789d05"],
        },
    )
    print("HTTP", resp.status_code)
    body = resp.json()
    if resp.status_code == 202:
        print("submissionId:", body["submissionId"], "status:", body["status"])
    else:
        print("失败:", body.get("code"), body.get("message"), body.get("details"))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const jar = new Map<string, string>();

function cookieHeader(): string {
  return [...jar].map(([k, v]) => `${k}=${v}`).join("; ");
}

async function request(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  const cookie = cookieHeader();
  if (cookie) headers.set("cookie", cookie);
  const res = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  for (const c of res.headers.getSetCookie?.() ?? []) {
    const [pair] = c.split(";");
    const i = pair.indexOf("=");
    if (i > 0) jar.set(pair.slice(0, i), pair.slice(i + 1));
  }
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res;
}

async function main() {
  // 先登录 (见《登录》)
  await request("/session", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username: "xxxx@gmail.com", password: "P@ssW0rd123" }),
  });

  const resp = await request("/posts", {
    method: "POST",
    headers: { "content-type": "application/json", "Idempotency-Key": crypto.randomUUID() },
    body: JSON.stringify({
      title: "「不完整」Pickcat部分API文档",
      markdown: "正文，图片写 ![01a0ff24-...]",
      kind: "DISCUSSION",
      tagIds: ["01a0ab26-84a8-718b-996a-3960a4789d05"],
    }),
  });

  console.log("HTTP", resp.status);
  const body = await resp.json();
  console.log("submissionId:", body.submissionId, "status:", body.status);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
