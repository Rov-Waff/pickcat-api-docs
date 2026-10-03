# 登出

> 登出 `/api/v1/session` DELETE **需要Cookie**

调用后当前 Session 立即失效，之后访问受保护接口会返回 `401 UNAUTHENTICATED`。

## 响应体

成功返回 `204 No Content`（无响应体）。

## 值得注意的

- 实测确认：`DELETE /api/v1/session` 返回 `204`，随后 `GET /api/v1/session` 返回 `401 UNAUTHENTICATED`。
- 登出会清除服务端会话，客户端保存的 Cookie 即使仍在也已失效。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::json;
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

    // 登出
    let resp = client.delete(format!("{BASE_URL}/session"))
        .send().await?.error_for_status()?;
    println!("HTTP {}", resp.status()); // 204

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

    # 登出
    resp = s.delete(f"{BASE_URL}/session")
    resp.raise_for_status()
    print("HTTP", resp.status_code)  # 204
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

  // 登出
  const resp = await request("/session", { method: "DELETE" });
  console.log("HTTP", resp.status); // 204
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
