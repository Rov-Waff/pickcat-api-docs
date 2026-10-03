# 提交答案

> 提交答案 `/api/v1/entrance-exam/attempts/{id}/current-question` PATCH **需要Cookie**

## 请求体

```json
{
    "questionId": "...",
    "deliveryToken": "...",
    "selectedOptionIds": ["...", "..."]
}
```

| KEY               | VALUE                   | TYPE      |
| ----------------- | ----------------------- | --------- |
| questionId        | 题目UUID                | String    |
| deliveryToken     | 取题时返回的作答 token  | String    |
| selectedOptionIds | 所选选项ID列表          | ArrayList |

## 响应体

中间态（未到最后一题）：

```json
{
    "state": "IN_PROGRESS",
    "attempt": { "...": "completedQuestions 递增" }
}
```

最后一题：

```json
{
    "state": "FINISHED",
    "result": {
        "attemptId": "...",
        "status": "PASSED",
        "totalQuestions": 10,
        "correctCount": 10,
        "requiredCorrectCount": 9,
        "startedAt": "...",
        "finishedAt": "2026-10-02T13:07:24.494Z"
    }
}
```

## 值得注意的

- 合格线 `requiredCorrectCount = 9`（10 题对 9 题）。
- **通过后** `GET /session` 中 `level.current` 由 `0` → `1`，会话 `expiresAt` 顺延。

## 示例

示例先开始考试并取当前题以获得 `questionId` 与 `deliveryToken`。

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

    // 开始考试并取当前题
    let start: Value = client.post(format!("{BASE_URL}/entrance-exam/attempts"))
        .send().await?.error_for_status()?.json().await?;
    let attempt_id = start["attempt"]["attemptId"].as_str().unwrap();
    let q: Value = client
        .get(format!("{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question"))
        .send().await?.error_for_status()?.json().await?;

    // 提交答案 (演示: 选第一个选项)
    let resp: Value = client
        .patch(format!("{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question"))
        .json(&json!({
            "questionId": q["questionId"],
            "deliveryToken": q["deliveryToken"],
            "selectedOptionIds": [q["options"][0]["id"]],
        }))
        .send().await?.error_for_status()?.json().await?;

    println!("state: {}", resp["state"]);
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

    # 开始考试并取当前题
    start = s.post(f"{BASE_URL}/entrance-exam/attempts").raise_for_status().json()
    attempt_id = start["attempt"]["attemptId"]
    q = s.get(f"{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question"
              ).raise_for_status().json()

    # 提交答案 (演示: 选第一个选项)
    resp = s.patch(
        f"{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question",
        json={
            "questionId": q["questionId"],
            "deliveryToken": q["deliveryToken"],
            "selectedOptionIds": [q["options"][0]["id"]],
        },
    ).raise_for_status().json()

    print("state:", resp["state"])
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

  // 开始考试并取当前题
  const start = await (await request("/entrance-exam/attempts", { method: "POST" })).json();
  const attemptId: string = start.attempt.attemptId;
  const q = await (await request(
    `/entrance-exam/attempts/${attemptId}/current-question`
  )).json();

  // 提交答案 (演示: 选第一个选项)
  const resp = await (await request(
    `/entrance-exam/attempts/${attemptId}/current-question`, {
      method: "PATCH",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        questionId: q.questionId,
        deliveryToken: q.deliveryToken,
        selectedOptionIds: [q.options[0].id],
      }),
    }
  )).json();
  console.log("state:", resp.state);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
