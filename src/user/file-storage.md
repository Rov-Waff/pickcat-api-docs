# 文件存储配额

> 获取文件存储配额 `/api/v1/file-storage` GET **需要Cookie**

用于设置页展示当前用户已用的文件存储空间。

## 响应体

```json
{ "usedBytes": 0, "limitBytes": 20971520, "remainingBytes": 20971520 }
```

| KEY            | VALUE          | TYPE    |
| -------------- | -------------- | ------- |
| usedBytes      | 已用字节数     | Integer |
| limitBytes     | 总配额字节数   | Integer |
| remainingBytes | 剩余可用字节数 | Integer |

> 观测到的默认配额为 `20971520` 字节（20 MiB）。

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

    let storage: Value = client.get(format!("{BASE_URL}/file-storage"))
        .send().await?.error_for_status()?.json().await?;
    println!("已用 {}/{} 字节", storage["usedBytes"], storage["limitBytes"]);
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

    storage = s.get(f"{BASE_URL}/file-storage").raise_for_status().json()
    print("已用", storage["usedBytes"], "/", storage["limitBytes"], "字节")
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

  const storage = await (await request("/file-storage")).json();
  console.log("已用", storage.usedBytes, "/", storage.limitBytes, "字节");
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
