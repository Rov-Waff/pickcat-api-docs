# 修改个人资料

> 修改个人资料 `/api/v1/users/{userId}` PATCH **需要Cookie**

只能修改自己的资料，`{userId}` 必须与当前会话用户一致。

## 请求体

```json
{ "bio": "Acrb" }
```

| KEY | VALUE    | TYPE   |
| --- | -------- | ------ |
| bio | 个人简介 | String |

## 响应体

返回更新后的完整用户对象，字段见[用户资料](./profile.md#响应体)。

## 值得注意的

- 只提交需要变更的字段即可，未提交的字段保持不变。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://pickcat.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 复用浏览器中已登录的 Cookie（见《登录》的 CAPTCHA 说明）
    let session_cookie = std::env::var("PICKCAT_SESSION").expect("请先设置 PICKCAT_SESSION");
    jar.add_cookie_str(&format!("pickcat_session={session_cookie}"), &BASE_URL.parse()?);

    // 取当前登录用户 ID，PATCH 只能改自己
    let me: Value = client.get(format!("{BASE_URL}/session"))
        .send().await?.error_for_status()?.json().await?;
    let user_id = me["user"]["id"].as_str().unwrap_or_default();

    let updated: Value = client.patch(format!("{BASE_URL}/users/{user_id}"))
        .json(&json!({ "bio": "Acrb" }))
        .send().await?.error_for_status()?.json().await?;
    println!("新简介: {}", updated["bio"]);
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
    updated = s.patch(f"{BASE_URL}/users/{user_id}", json={"bio": "Acrb"}
                      ).raise_for_status().json()
    print("新简介:", updated["bio"])
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
  const updated = await (await request(`/users/${userId}`, {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ bio: "Acrb" }),
  })).json();
  console.log("新简介:", updated.bio);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
