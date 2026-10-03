# 查询用户邮箱

> 查询用户邮箱 `/api/v1/users/{userId}/email` GET **需要Cookie**

## 响应体

```json
{ "email": "2710182206@qq.com", "verifiedAt": "2026-10-02T08:46:15.771Z" }
```

| KEY        | VALUE        | TYPE     |
| ---------- | ------------ | -------- |
| email      | 邮箱地址     | String   |
| verifiedAt | 邮箱验证时间 | DateTime |

## 值得注意的

- 该接口只对用户本人开放，访问他人邮箱的具体错误响应尚未验证。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USER_ID: &str = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 先登录 (见《登录》)
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": "xxxx@gmail.com", "password": "P@ssW0rd123" }))
        .send().await?.error_for_status()?;

    let email: Value = client.get(format!("{BASE_URL}/users/{USER_ID}/email"))
        .send().await?.error_for_status()?.json().await?;
    println!("邮箱: {} ({})", email["email"], email["verifiedAt"]);
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

with requests.Session() as s:
    # 先登录 (见《登录》)
    s.post(f"{BASE_URL}/session",
           json={"username": "xxxx@gmail.com", "password": "P@ssW0rd123"}).raise_for_status()

    email = s.get(f"{BASE_URL}/users/{USER_ID}/email").raise_for_status().json()
    print("邮箱:", email["email"], email["verifiedAt"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";
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

  const email = await (await request(`/users/${USER_ID}/email`)).json();
  console.log("邮箱:", email.email, email.verifiedAt);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
