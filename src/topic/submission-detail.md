# 投稿详情

> 获取投稿详情 `/api/v1/post-submissions/{submissionId}` GET **需要Cookie**

## 响应体

```json
{
  "id": "01a0ff33-69c6-74a3-ba97-6370b8079f6c",
  "status": "PENDING_PROVIDER",
  "contentRole": "TOPIC_REPLY",
  "request": { "topicId": "01a0c95a-...", "markdown": "合影", "replyToPostNumber": 1 },
  "riskLevel": null,
  "topicId": "01a0c95a-...",
  "postId": "01a0ff33-...",
  "postNumber": 52,
  "baseRevision": null,
  "createdAt": "2026-10-03T00:39:14.613Z",
  "updatedAt": "2026-10-03T00:39:14.613Z"
}
```

字段说明见[投稿审核列表](./submissions.md#响应体)。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const SUBMISSION_ID: &str = "01a0ff33-69c6-74a3-ba97-6370b8079f6c";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 先登录 (见《登录》)
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": "xxxx@gmail.com", "password": "P@ssW0rd123" }))
        .send().await?.error_for_status()?;

    let sub: Value = client
        .get(format!("{BASE_URL}/post-submissions/{SUBMISSION_ID}"))
        .send().await?.error_for_status()?.json().await?;

    println!("状态: {} / 角色: {}", sub["status"], sub["contentRole"]);
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
SUBMISSION_ID = "01a0ff33-69c6-74a3-ba97-6370b8079f6c"

with requests.Session() as s:
    # 先登录 (见《登录》)
    s.post(f"{BASE_URL}/session",
           json={"username": "xxxx@gmail.com", "password": "P@ssW0rd123"}).raise_for_status()

    sub = s.get(f"{BASE_URL}/post-submissions/{SUBMISSION_ID}").raise_for_status().json()
    print("状态:", sub["status"], "/ 角色:", sub["contentRole"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const SUBMISSION_ID = "01a0ff33-69c6-74a3-ba97-6370b8079f6c";
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

  const sub = await (await request(`/post-submissions/${SUBMISSION_ID}`)).json();
  console.log("状态:", sub.status, "/ 角色:", sub.contentRole);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
