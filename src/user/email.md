# 查询用户邮箱

> 查询用户邮箱 `/api/v1/users/{userId}/email` GET **需要Cookie**

## 响应体

```json
{ "email": "user@example.com", "verifiedAt": "2026-10-02T08:46:15.771Z" }
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

    // 该接口只对本人开放，先取当前登录用户 ID
    let me: Value = client.get(format!("{BASE_URL}/session"))
        .send().await?.error_for_status()?.json().await?;
    let user_id = me["user"]["id"].as_str().unwrap_or_default();

    let email: Value = client.get(format!("{BASE_URL}/users/{user_id}/email"))
        .send().await?.error_for_status()?.json().await?;
    println!("邮箱: {} ({})", email["email"], email["verifiedAt"]);
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

    me = s.get(f"{BASE_URL}/session").raise_for_status().json()
    user_id = me["user"]["id"]
    email = s.get(f"{BASE_URL}/users/{user_id}/email").raise_for_status().json()
    print("邮箱:", email["email"], email["verifiedAt"])
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

  const me = await (await request("/session")).json();
  const userId: string = me.user.id;
  const email = await (await request(`/users/${userId}/email`)).json();
  console.log("邮箱:", email.email, email.verifiedAt);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
