# 内容长度上限

> 获取内容长度上限 `/api/v1/content-length-limit` GET **需要Cookie**

## 响应体

```json
{ "level": 1, "topicMaxLength": 20000, "replyMaxLength": 2000 }
```

| KEY            | VALUE        | TYPE    |
| -------------- | ------------ | ------- |
| level          | 当前等级     | Integer |
| topicMaxLength | 主题字数上限 | Integer |
| replyMaxLength | 回帖字数上限 | Integer |

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

    let limit: Value = client.get(format!("{BASE_URL}/content-length-limit"))
        .send().await?.error_for_status()?.json().await?;
    println!("主题上限 {} / 回帖上限 {}", limit["topicMaxLength"], limit["replyMaxLength"]);
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

    limit = s.get(f"{BASE_URL}/content-length-limit").raise_for_status().json()
    print("主题上限", limit["topicMaxLength"], "/ 回帖上限", limit["replyMaxLength"])
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

  const limit = await (await request("/content-length-limit")).json();
  console.log("主题上限", limit.topicMaxLength, "/ 回帖上限", limit.replyMaxLength);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
