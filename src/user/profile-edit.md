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

    let updated: Value = client.patch(format!("{BASE_URL}/users/{USER_ID}"))
        .json(&json!({ "bio": "Acrb" }))
        .send().await?.error_for_status()?.json().await?;
    println!("新简介: {}", updated["bio"]);
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

    updated = s.patch(f"{BASE_URL}/users/{USER_ID}", json={"bio": "Acrb"}
                      ).raise_for_status().json()
    print("新简介:", updated["bio"])
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

  const updated = await (await request(`/users/${USER_ID}`, {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ bio: "Acrb" }),
  })).json();
  console.log("新简介:", updated.bio);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
