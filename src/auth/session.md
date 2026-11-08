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
      "tokenBalance": 7,
      "level": { "current": 1 },
      "effectivePermissions": [
        { "key": "content.publish", "scopes": [{ "type": "SITE" }] },
        { "key": "content.own.edit", "scopes": [{ "type": "SITE" }] },
        { "key": "content.like", "scopes": [{ "type": "SITE" }] }
      ]
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
- `user.tokenBalance` 为代币余额；`user.effectivePermissions` 是对象数组，元素包含 `key` 与 `scopes`。
- 通过入站考试后再次调用本接口，`user.level.current` 会由 `0` 变为 `1`，同时 `expiresAt` 顺延。
- 会话 Cookie 名为 `pickcat_session`（HttpOnly / Secure / SameSite=Lax，有效期 7 天）。
- 登出请使用[登出](./logout.md)（`DELETE /api/v1/session`）。

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
import os
import requests

BASE_URL = "https://pickcat.dao3.fun/api/v1"

with requests.Session() as s:
    # 复用浏览器中已登录的 Cookie（见《登录》的 CAPTCHA 说明）
    s.headers["Cookie"] = f"pickcat_session={os.environ['PICKCAT_SESSION']}"

    # 获取当前会话
    session = s.get(f"{BASE_URL}/session").raise_for_status().json()

    print("当前用户:", session["user"]["username"])
    print("等级    : Lv.", session["user"]["level"]["current"])
    print("过期于  :", session["expiresAt"])
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

  // 获取当前会话
  const session = await (await request("/session")).json();
  console.log("当前用户:", session.user.username);
  console.log("等级    : Lv." + session.user.level.current);
  console.log("过期于  :", session.expiresAt);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
