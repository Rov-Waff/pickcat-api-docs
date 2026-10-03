# 我的文件列表

> 我的文件列表 `/api/v1/files` GET **需要Cookie**

## Query

| KEY   | 观测值  | 说明                         |
| ----- | ------- | ---------------------------- |
| scope | `OWN`   | 只看自己的文件               |
| state | `READY` | 只看已就绪（上传完成）的文件 |

## 响应体

```json
{ "pageInfo": { "hasNextPage": false, "nextCursor": null }, "items": [] }
```

| KEY      | VALUE    | TYPE      |
| -------- | -------- | --------- |
| items    | 文件列表 | ArrayList |
| pageInfo | 分页信息 | Object    |

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

    let files: Value = client.get(format!("{BASE_URL}/files?scope=OWN&state=READY"))
        .send().await?.error_for_status()?.json().await?;
    println!("文件数: {}", files["items"].as_array().map_or(0, Vec::len));
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

    files = s.get(f"{BASE_URL}/files",
                  params={"scope": "OWN", "state": "READY"}).raise_for_status().json()
    print("文件数:", len(files["items"]))
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

  const files = await (await request("/files?scope=OWN&state=READY")).json();
  console.log("文件数:", files.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
