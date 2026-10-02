# 验证邮箱

> 验证邮箱 `/api/v1/registrations/{id}` PATCH

完成注册的最后一步：提交邮箱验证码与密码，成功后自动登录。

## 请求体

```json
{
    "code": "<邮箱验证码>",
    "password": "<密码>"
}
```

| KEY      | VALUE      | TYPE   |
| -------- | ---------- | ------ |
| code     | 邮箱验证码 | String |
| password | 设置的密码 | String |

## 响应体

```json
{
    "id": "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445",
    "username": "SilverPremium",
    "avatar": { "type": "PRESET", "id": 1, "url": "/api/v1/avatars/1?v=..." },
    "bio": null,
    "region": null,
    "showFollowingList": true,
    "showFollowersList": true,
    "createdAt": "2026-10-02T12:56:52.310Z",
    "level": { "current": 0 },
    "stats": { "followers": 0, "following": 0, "topics": 0, "replies": 0 },
    "viewerState": { "following": false, "canFollow": false }
}
```

| KEY               | VALUE                | TYPE          |
| ----------------- | -------------------- | ------------- |
| id                | 用户UUID             | String        |
| username          | 用户昵称             | String        |
| avatar            | 头像                 | Object        |
| bio               | 个人简介，可为 null  | String/Option |
| region            | 地区，可为 null      | String/Option |
| showFollowingList | 是否公开「关注」列表 | Boolean       |
| showFollowersList | 是否公开「粉丝」列表 | Boolean       |
| createdAt         | 账户创建时间         | DateTime      |
| level.current     | 当前等级（注册后为 0） | Integer     |
| stats             | 关注/粉丝/主题/回帖计数 | Object     |
| viewerState       | 当前访问者与用户的关系 | Object      |

## 值得注意的

- 验证后将会用 Set-Cookie 设置 Session，自动登录。
- 成功返回 `201 Created`。
- 密码长度至少 **10** 个字符，否则返回 `400 VALIDATION_FAILED`。
- 注册后 `level.current` 为 `0`，通过入站考试后才会升到 `1`。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
// 来自 POST /registrations 的响应
const REGISTRATION_ID: &str = "01a0fcab-dae0-736a-8d90-583dc20def93";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    let user: Value = client
        .patch(format!("{BASE_URL}/registrations/{REGISTRATION_ID}"))
        .json(&json!({ "code": "123456", "password": "P@ssW0rd123" }))
        .send().await?.error_for_status()?.json().await?;

    println!("注册成功: {} (Lv.{})", user["username"], user["level"]["current"]);
    // 响应的 Set-Cookie 已写入 jar, 之后自动携带
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
# 来自 POST /registrations 的响应
REGISTRATION_ID = "01a0fcab-dae0-736a-8d90-583dc20def93"

with requests.Session() as s:
    resp = s.patch(
        f"{BASE_URL}/registrations/{REGISTRATION_ID}",
        json={"code": "123456", "password": "P@ssW0rd123"},
    )
    resp.raise_for_status()
    user = resp.json()

    print("注册成功:", user["username"], "Lv.", user["level"]["current"])
    # 响应的 Set-Cookie 已保存在 s, 之后自动携带
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
// 来自 POST /registrations 的响应
const REGISTRATION_ID = "01a0fcab-dae0-736a-8d90-583dc20def93";
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
  const user = await (await request(`/registrations/${REGISTRATION_ID}`, {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ code: "123456", password: "P@ssW0rd123" }),
  })).json();

  console.log("注册成功:", user.username, "Lv." + user.level.current);
  // 响应的 Set-Cookie 已存入 jar
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
