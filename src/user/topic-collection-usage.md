# 合集配额用量

> 获取合集配额用量 `/api/v1/topic-collection-usage` GET **需要Cookie**

## 响应体

```json
{ "currentLevel": 1, "limitCount": 5, "usedCount": 0, "remainingCount": 5 }
```

| KEY            | VALUE        | TYPE    |
| -------------- | ------------ | ------- |
| currentLevel   | 当前等级     | Integer |
| limitCount     | 合集数量上限 | Integer |
| usedCount      | 已用数量     | Integer |
| remainingCount | 剩余数量     | Integer |

## 示例

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

    let usage: Value = client.get(format!("{BASE_URL}/topic-collection-usage"))
        .send().await?.error_for_status()?.json().await?;
    println!("合集 {}/{}", usage["usedCount"], usage["limitCount"]);
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

    usage = s.get(f"{BASE_URL}/topic-collection-usage").raise_for_status().json()
    print("合集", usage["usedCount"], "/", usage["limitCount"])
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

  const usage = await (await request("/topic-collection-usage")).json();
  console.log("合集", usage.usedCount, "/", usage.limitCount);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
