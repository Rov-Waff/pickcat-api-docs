# 取当前题

> 取当前题 `/api/v1/entrance-exam/attempts/{id}/current-question` GET **需要Cookie**

## 响应体

```json
{
    "state": "QUESTION",
    "attemptId": "...",
    "questionId": "...",
    "ordinal": 0,
    "totalQuestions": 10,
    "questionType": "MULTIPLE_CHOICE",
    "stemHtml": "<p>题干</p>",
    "options": [
        { "id": "...", "position": 0, "contentHtml": "<p>选项</p>" }
    ],
    "deliveryToken": "<本题一次性作答 token>",
    "deadlineAt": "..."
}
```

| KEY            | VALUE                             | TYPE      |
| -------------- | --------------------------------- | --------- |
| state          | 固定 `QUESTION`                   | String    |
| attemptId      | 本次考试UUID                      | String    |
| questionId     | 题目UUID                          | String    |
| ordinal        | 题号（从 0 开始）                 | Integer   |
| totalQuestions | 总题数                            | Integer   |
| questionType   | `MULTIPLE_CHOICE`/`SINGLE_CHOICE` | String    |
| stemHtml       | 题干 HTML                         | String    |
| options        | 选项列表（`id`/`position`/`contentHtml`） | ArrayList |
| deliveryToken  | 本题一次性作答 token              | String    |
| deadlineAt     | 本题截止时间                      | DateTime  |

## 值得注意的

- `deliveryToken` 与题目绑定，提交答案时必须回传，防止重放/跳题。
- 题目为单选或多选（`MULTIPLE_CHOICE` / `SINGLE_CHOICE`）。

## 示例

示例先开始一场考试以取得 `attemptId`（开始考试见[开始一次考试](./exam-start.md)），再获取当前题。

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::Value;
use std::sync::Arc;

const BASE_URL: &str = "https://pickcat.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 复用浏览器中已登录的 Cookie（见《登录》的 CAPTCHA 说明）
    let session_cookie = std::env::var("PICKCAT_SESSION").expect("请先设置 PICKCAT_SESSION");
    jar.add_cookie_str(&format!("pickcat_session={session_cookie}"), &BASE_URL.parse()?);

    // 取得 attemptId
    let start: Value = client.post(format!("{BASE_URL}/entrance-exam/attempts"))
        .send().await?.error_for_status()?.json().await?;
    let attempt_id = start["attempt"]["attemptId"].as_str().unwrap();

    // 取当前题
    let q: Value = client
        .get(format!("{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question"))
        .send().await?.error_for_status()?.json().await?;

    println!("题干: {}", q["stemHtml"]);
    println!("选项数: {}", q["options"].as_array().map_or(0, Vec::len));
    println!("token : {}", q["deliveryToken"]);
    Ok(())
}
```
```python
import os
import requests

BASE_URL = "https://pickcat.dao3.fun/api/v1"

with requests.Session() as s:
    # 复用浏览器中已登录的 Cookie（见《登录》的 CAPTCHA 说明）
    s.headers["Cookie"] = f"pickcat_session={os.environ['PICKCAT_SESSION']}"

    # 取得 attemptId
    start = s.post(f"{BASE_URL}/entrance-exam/attempts").raise_for_status().json()
    attempt_id = start["attempt"]["attemptId"]

    # 取当前题
    q = s.get(f"{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question"
              ).raise_for_status().json()
    print("题干:", q["stemHtml"])
    print("选项数:", len(q["options"]))
    print("token :", q["deliveryToken"])
```
```typescript
const BASE_URL = "https://pickcat.dao3.fun/api/v1";
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
  // 复用浏览器中已登录的 Cookie（见《登录》的 CAPTCHA 说明）
  const pickcatSession = process.env.PICKCAT_SESSION;
  if (!pickcatSession) throw new Error("请先设置 PICKCAT_SESSION");
  jar.set("pickcat_session", pickcatSession);

  // 取得 attemptId
  const start = await (await request("/entrance-exam/attempts", { method: "POST" })).json();
  const attemptId: string = start.attempt.attemptId;

  // 取当前题
  const q = await (await request(
    `/entrance-exam/attempts/${attemptId}/current-question`
  )).json();
  console.log("题干:", q.stemHtml);
  console.log("选项数:", q.options.length);
  console.log("token :", q.deliveryToken);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
