# 阅读会话

> 上报阅读批次 `/api/v1/reading-sessions/{sessionId}/batches/{batchNo}` PUT

用于埋点上报「主题阅读行为」，服务端据此折算社区熟悉度。

## 请求体

```json
{
  "topicId": "01a0eb91-5d11-7fb0-b998-179add93620f",
  "elapsedMs": 9589,
  "visiblePosts": [
    { "postId": "01a0eb91-5d14-...", "visibleMs": 2184 },
    { "postId": "01a0eca4-...", "visibleMs": 972 }
  ]
}
```

| KEY                     | VALUE              | TYPE      |
| ----------------------- | ------------------ | --------- |
| topicId                 | 主题UUID           | String    |
| elapsedMs               | 本批次总时长(ms)   | Integer   |
| visiblePosts            | 各楼层可见时长     | ArrayList |
| visiblePosts[].postId   | 楼层UUID           | String    |
| visiblePosts[].visibleMs| 该楼层可见时长(ms) | Integer   |

## 响应体

```json
{
  "acceptedElapsedMs": 3029,
  "familiarity": {
    "tracking": true,
    "familiarityStartedAt": "2026-10-02T08:47:49.552Z",
    "daysSinceEntranceExam": 0,
    "topicsEntered": 1,
    "postsRead": 16,
    "effectiveReadingSeconds": 3,
    "validVisitDays": 0
  }
}
```

| KEY                      | VALUE                | TYPE     |
| ------------------------ | -------------------- | -------- |
| acceptedElapsedMs        | 服务端接受的有效时长(ms) | Integer |
| familiarity              | 熟悉度进度           | Object   |
| familiarity.topicsEntered| 进入过的主题数       | Integer  |
| familiarity.postsRead    | 已读楼层数           | Integer  |
| familiarity.effectiveReadingSeconds | 有效阅读秒数 | Integer |
| familiarity.validVisitDays | 有效访问天数       | Integer  |

## 值得注意的

- 路径中 `{sessionId}` 由前端生成，`{batchNo}` 为批次序号；成功返回 `201 Created`。
- `visiblePosts` 至少包含 1 项，否则返回 `400 VALIDATION_FAILED`。
- 服务端会把 `elapsedMs` 折算为 `effectiveReadingSeconds`，`acceptedElapsedMs` 可能小于上报值。
- 熟悉度会计入[等级进度](./user/level-progress.md)。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
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

    let session_id = "9510a879-c404-409d-82c8-e0ee9abe0e68"; // 由前端生成
    let body = json!({
        "topicId": "01a0eb91-5d11-7fb0-b998-179add93620f",
        "elapsedMs": 9589,
        "visiblePosts": [
            { "postId": "01a0eb91-5d14-7d7d-9cea-f08cc47d900f", "visibleMs": 2184 },
            { "postId": "01a0eca4-4663-779b-b57f-cbb6b3a98cc1", "visibleMs": 972 }
        ]
    });

    let resp: Value = client
        .put(format!("{BASE_URL}/reading-sessions/{session_id}/batches/1"))
        .json(&body)
        .send().await?.error_for_status()?.json().await?;

    println!("接受时长: {}ms", resp["acceptedElapsedMs"]);
    println!("有效阅读: {}s", resp["familiarity"]["effectiveReadingSeconds"]);
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

with requests.Session() as s:
    # 先登录 (见《登录》)
    s.post(f"{BASE_URL}/session",
           json={"username": "xxxx@gmail.com", "password": "P@ssW0rd123"}).raise_for_status()

    session_id = "9510a879-c404-409d-82c8-e0ee9abe0e68"  # 由前端生成
    body = {
        "topicId": "01a0eb91-5d11-7fb0-b998-179add93620f",
        "elapsedMs": 9589,
        "visiblePosts": [
            {"postId": "01a0eb91-5d14-7d7d-9cea-f08cc47d900f", "visibleMs": 2184},
            {"postId": "01a0eca4-4663-779b-b57f-cbb6b3a98cc1", "visibleMs": 972},
        ],
    }

    resp = s.put(f"{BASE_URL}/reading-sessions/{session_id}/batches/1",
                 json=body).raise_for_status().json()

    print("接受时长:", resp["acceptedElapsedMs"], "ms")
    print("有效阅读:", resp["familiarity"]["effectiveReadingSeconds"], "s")
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

  const sessionId = "9510a879-c404-409d-82c8-e0ee9abe0e68"; // 由前端生成
  const body = {
    topicId: "01a0eb91-5d11-7fb0-b998-179add93620f",
    elapsedMs: 9589,
    visiblePosts: [
      { postId: "01a0eb91-5d14-7d7d-9cea-f08cc47d900f", visibleMs: 2184 },
      { postId: "01a0eca4-4663-779b-b57f-cbb6b3a98cc1", visibleMs: 972 },
    ],
  };

  const resp = await (await request(`/reading-sessions/${sessionId}/batches/1`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  })).json();

  console.log("接受时长:", resp.acceptedElapsedMs, "ms");
  console.log("有效阅读:", resp.familiarity.effectiveReadingSeconds, "s");
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
