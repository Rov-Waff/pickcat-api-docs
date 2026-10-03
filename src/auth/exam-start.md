# 开始一次考试

> 开始一次考试 `/api/v1/entrance-exam/attempts` POST **需要Cookie**

## 请求体

无请求体。

## 响应体

```json
{
    "state": "IN_PROGRESS",
    "attempt": {
        "attemptId": "01a0fcb5-97ab-70a8-a38f-e184ca006064",
        "totalQuestions": 10,
        "completedQuestions": 0,
        "currentOrdinal": 0,
        "deadlineAt": "2026-10-02T13:12:34.401Z",
        "startedAt": "2026-10-02T13:02:34.401Z"
    }
}
```

| KEY                        | VALUE                  | TYPE     |
| -------------------------- | ---------------------- | -------- |
| state                      | 固定 `IN_PROGRESS`     | String   |
| attempt.attemptId          | 本次考试UUID           | String   |
| attempt.totalQuestions     | 总题数，固定 `10`      | Integer  |
| attempt.completedQuestions | 已完成题数             | Integer  |
| attempt.currentOrdinal     | 当前题序号（从 0 开始）| Integer  |
| attempt.deadlineAt         | 本题截止时间           | DateTime |
| attempt.startedAt          | 开始时间               | DateTime |

## 值得注意的

- 10 题，初始 `deadlineAt` = 开始 + 10 分钟。
- 每次提交答案后会**顺延 deadline**（观测值逐题滚动，属「每题限时」而非整场限时）。
- 若上一场未通过且处于冷却期，返回 `409 ENTRANCE_EXAM_COOLDOWN`，`details.nextAttemptAt` 为下次可用时间。

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

    // 开始一次考试
    let start: Value = client.post(format!("{BASE_URL}/entrance-exam/attempts"))
        .send().await?.error_for_status()?.json().await?;

    println!("state: {}", start["state"]);
    println!("attemptId: {}", start["attempt"]["attemptId"]);
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

    # 开始一次考试
    start = s.post(f"{BASE_URL}/entrance-exam/attempts").raise_for_status().json()
    print("state:", start["state"])
    print("attemptId:", start["attempt"]["attemptId"])
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

  // 开始一次考试
  const start = await (await request("/entrance-exam/attempts", { method: "POST" })).json();
  console.log("state:", start.state);
  console.log("attemptId:", start.attempt.attemptId);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
