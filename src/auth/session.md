# 当前会话

> 获取当前会话 `/api/v1/session` GET **需要Cookie**

用于在页面刷新/重新进入时判断本地 Session 是否仍然有效，并拉取当前登录用户。

## 响应体

返回结构与[登录](./login.md)响应一致（已实测确认）：

```json
{
    "user": {
      "id": "01a0fbca-eee1-70ad-a00d-a1ed4c89b195",
      "username": "CarbonPremium",
      "createdAt": "2026-10-02T08:46:15.771Z",
      "avatar": { "type": "PRESET", "id": 1, "url": "/api/v1/avatars/1?v=..." },
      "level": { "current": 1 },
      "effectivePermissions": []
    },
    "createdAt": "2026-10-02T10:19:14.833Z",
    "expiresAt": "2026-10-09T10:19:14.833Z",
    "silence": null
}
```

| KEY       | VALUE           | TYPE       |
| --------- | --------------- | ---------- |
| user      | 当前用户基础信息 | Object     |
| createdAt | Session建立时间 | DateTime   |
| expiresAt | Session过期时间 | DateTime   |
| silence   | 含义未验证（可能与禁言有关） | Any/Option |

## 值得注意的

- 与会话相关的响应体均**不含 token**，凭据仅通过 Cookie 传递。
- 通过入站考试后再次调用本接口，`user.level.current` 会由 `0` 变为 `1`，同时 `expiresAt` 顺延。
- 会话 Cookie 名为 `pickcat_session`（HttpOnly / Secure / SameSite=Lax，有效期 7 天）。
- 登出请使用[登出](./logout.md)（`DELETE /api/v1/session`）。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USERNAME: &str = "xxxx@gmail.com";
const PASSWORD: &str = "P@ssW0rd123";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 先登录, 会话 Cookie 会保存在 jar 中 (见《登录》)
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": USERNAME, "password": PASSWORD }))
        .send().await?.error_for_status()?;

    // 获取当前会话
    let session: Value = client.get(format!("{BASE_URL}/session"))
        .send().await?.error_for_status()?.json().await?;

    println!("当前用户: {}", session["user"]["username"]);
    println!("等级    : Lv.{}", session["user"]["level"]["current"]);
    println!("过期于  : {}", session["expiresAt"]);

    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USERNAME = "xxxx@gmail.com"
PASSWORD = "P@ssW0rd123"

with requests.Session() as s:
    # 先登录, Session Cookie 会自动保存 (见《登录》)
    s.post(f"{BASE_URL}/session", json={"username": USERNAME, "password": PASSWORD}).raise_for_status()

    # 获取当前会话
    session = s.get(f"{BASE_URL}/session").raise_for_status().json()

    print("当前用户:", session["user"]["username"])
    print("等级    : Lv.", session["user"]["level"]["current"])
    print("过期于  :", session["expiresAt"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USERNAME = "xxxx@gmail.com";
const PASSWORD = "P@ssW0rd123";
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
  // 先登录 (见《登录》), 响应的 Set-Cookie 会存入 jar
  await request("/session", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username: USERNAME, password: PASSWORD }),
  });

  // 获取当前会话
  const session = await (await request("/session")).json();
  console.log("当前用户:", session.user.username);
  console.log("等级    : Lv." + session.user.level.current);
  console.log("过期于  :", session.expiresAt);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
