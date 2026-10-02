# 获取入站考试状态

> 获取入站考试状态 `/api/v1/entrance-exam` GET **需要Cookie**

用于查询当前用户能否参加入站考试，`state` 有 `AVAILABLE` / `PASSED` / `COOLDOWN` 三种取值。

## 响应体

如果入站考试可用，即你未参加入站考试：

```json
{
    "state": "AVAILABLE",
    "nextAttemptAt": "2026-10-02T12:56:52.310Z"
}
```

如果你已经通过入站考试：

```json
{
    "state": "PASSED",
    "result": {
        "attemptId": "01a0fcb5-97ab-70a8-a38f-e184ca006064",
        "status": "PASSED",
        "totalQuestions": 10,
        "correctCount": 10,
        "requiredCorrectCount": 9,
        "startedAt": "2026-10-02T13:02:34.401Z",
        "finishedAt": "2026-10-02T13:07:24.494Z"
    }
}
```

如果你入站考试处于冷却状态：

```json
{
    "state": "COOLDOWN",
    "nextAttemptAt": "2026-10-03T08:37:35.348Z"
}
```

| KEY           | VALUE                          | TYPE           |
| ------------- | ------------------------------ | -------------- |
| state         | `AVAILABLE`/`PASSED`/`COOLDOWN` | String        |
| nextAttemptAt | 下一次可用时间，`AVAILABLE`/`COOLDOWN` 时返回 | DateTime |
| result        | 考试结果，仅 `PASSED` 时返回   | Object/Option  |

## 值得注意的

- `AVAILABLE` 表示尚未参加考试；`PASSED` 表示已通过并附带成绩；`COOLDOWN` 表示未通过后的冷却期。
- `result.status` 为 `PASSED`，合格线为 `requiredCorrectCount`（10 题对 9 题）。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USERNAME: &str = "xxxx@gmail.com";
const PASSWORD: &str = "P@ssW0rd123";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": USERNAME, "password": PASSWORD }))
        .send().await?.error_for_status()?;

    let exam: Value = client.get(format!("{BASE_URL}/entrance-exam"))
        .send().await?.error_for_status()?.json().await?;

    match exam["state"].as_str().unwrap_or("") {
        "AVAILABLE" => println!("可以开始考试"),
        "PASSED" => println!("已通过考试, 成绩: {}", exam["result"]["correctCount"]),
        "COOLDOWN" => println!("冷却中, 下次可用: {}", exam["nextAttemptAt"]),
        other => println!("未知状态: {other}"),
    }

    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USERNAME = "xxxx@gmail.com"
PASSWORD = "P@ssW0rd123"

with requests.Session() as s:
    s.post(f"{BASE_URL}/session", json={"username": USERNAME, "password": PASSWORD}).raise_for_status()

    exam = s.get(f"{BASE_URL}/entrance-exam").raise_for_status().json()

    state = exam["state"]
    if state == "AVAILABLE":
        print("可以开始考试")
    elif state == "PASSED":
        print("已通过考试, 成绩:", exam["result"]["correctCount"])
    elif state == "COOLDOWN":
        print("冷却中, 下次可用:", exam["nextAttemptAt"])
    else:
        print("未知状态:", state)
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USERNAME = "xxxx@gmail.com";
const PASSWORD = "P@ssW0rd123";
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
  await request("/session", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username: USERNAME, password: PASSWORD }),
  });

  const exam = await (await request("/entrance-exam")).json();
  switch (exam.state) {
    case "AVAILABLE": console.log("可以开始考试"); break;
    case "PASSED": console.log("已通过考试, 成绩:", exam.result.correctCount); break;
    case "COOLDOWN": console.log("冷却中, 下次可用:", exam.nextAttemptAt); break;
    default: console.log("未知状态:", exam.state);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
