# 登录

> 登录 `/api/v1/session` POST

## 请求体

```json
{ 
    "username": "xxxx@gmail.com", 
    "password": "P@ssW0rd123"
}
```

| KEY      | VALUE                      | TYPE   |
| -------- | -------------------------- | ------ |
| username | 用户名，也就是你账号的邮箱 | String |
| password | 密码                       | String |

## 响应体

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
| user      | 用户基础信息    | Object     |
| createdAt | Session建立时间 | DateTime   |
| expiresAt | Session过期时间 | DateTime   |
| silence   | 含义未验证（可能与禁言有关） | Any/Option |

### user字段



| KEY                  | VALUE              | TYPE          |
| -------------------- | ------------------ | ------------- |
| id                   | 用户UUID           | String        |
| username             | 用户昵称           | String        |
| createdAt            | 账户创建时间       | DateTime      |
| avatar               | 头像               | Object        |
| level                | 用户等级           | Object        |
| effectivePermissions | 特殊权限（含义未验证） | ArrayList/Vec |

## 值得注意的

- 与主站不同，Pickcat使用Session鉴权，而不是JWT，因此，返回体**不含 token**，会话凭据通过 HTTP头部`Set-Cookie` 下发
- Session有效期 **7 天**
- 成功返回 `201 Created`，响应头包含 `location: /api/v1/session`。
- `username` 字段填邮箱或用户名均可，统一命名为 `username`。

## 示例
<!-- langtabs-start -->

```rust
use anyhow::{Context, Result};
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

// 注意: 已包含 /api/v1
const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USERNAME: &str = "xxxx@gmail.com";
const PASSWORD: &str = "P@ssW0rd123";

async fn login(client: &Client) -> Result<Value> {
    let resp = client
        .post(format!("{BASE_URL}/session")) // -> /api/v1/session
        .json(&json!({
            "username": USERNAME,
            "password": PASSWORD,
        }))
        .send()
        .await?
        .error_for_status()?;

    let data: Value = resp.json().await?;
    Ok(data)
}

/// 从 Value 里按路径取字段，缺字段时给出清晰错误
fn get<'a>(v: &'a Value, path: &[&str]) -> Result<&'a Value> {
    let mut cur = v;
    for key in path {
        cur = cur
            .get(*key)
            .with_context(|| format!("缺少字段: {}", path.join(".")))?;
    }
    Ok(cur)
}

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder()
        .cookie_provider(jar.clone())
        .build()?;

    let data = login(&client).await?;

    let user = get(&data, &["user"])?;
    println!("登录成功!");
    println!("用户 ID      : {}", get(user, &["id"])?.as_str().unwrap_or(""));
    println!("用户昵称     : {}", get(user, &["username"])?.as_str().unwrap_or(""));
    println!("账户创建时间 : {}", get(user, &["createdAt"])?.as_str().unwrap_or(""));
    println!("用户等级     : Lv.{}", get(user, &["level", "current"])?.as_u64().unwrap_or(0));
    println!("头像 URL     : {}", get(user, &["avatar", "url"])?.as_str().unwrap_or(""));
    println!("Session 建立 : {}", get(&data, &["createdAt"])?.as_str().unwrap_or(""));
    println!("Session 过期 : {}", get(&data, &["expiresAt"])?.as_str().unwrap_or(""));
    println!("禁言状态     : {}", data.get("silence").unwrap_or(&Value::Null));

    // 后续请求自动带 Cookie:
    // let me: Value = client
    //     .get(format!("{BASE_URL}/me"))
    //     .send().await?.error_for_status()?.json().await?;

    for cookie in jar.cookies(&BASE_URL.parse()?) {
        println!("Cookie: {}", cookie.to_str()?);
    }

    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USERNAME = "xxxx@gmail.com"
PASSWORD = "P@ssW0rd123"


def login(session: requests.Session) -> dict:
    resp = session.post(
        f"{BASE_URL}/session",
        json={"username": USERNAME, "password": PASSWORD},
    )
    resp.raise_for_status()  # 非 2xx 抛异常
    return resp.json()


def main():
    # Session 鉴权靠 Cookie, requests.Session 会自动保存并携带 Set-Cookie
    with requests.Session() as s:
        data = login(s)

        user = data["user"]
        print("登录成功!")
        print(f"用户 ID      : {user['id']}")
        print(f"用户昵称     : {user['username']}")
        print(f"账户创建时间 : {user['createdAt']}")
        print(f"用户等级     : Lv.{user['level']['current']}")
        print(f"头像 URL     : {user['avatar']['url']}")
        print(f"Session 建立 : {data['createdAt']}")
        print(f"Session 过期 : {data['expiresAt']}")
        print(f"禁言状态     : {data['silence']}")

        # 查看当前保存的 Cookie
        for name, value in s.cookies.items():
            print(f"Cookie: {name}={value}")

        # 之后的请求会自动带上会话 Cookie, 例如:
        # me = s.get(f"{BASE_URL}/me")
        # print(me.json())


if __name__ == "__main__":
    main()
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USERNAME = "xxxx@gmail.com";
const PASSWORD = "P@ssW0rd123";

// 极简 Cookie jar: 服务端返回的每个 Set-Cookie 只取第一段 name=value
const jar = new Map<string, string>();

function storeCookies(res: Response) {
  // Node 18.14+ 支持 getSetCookie()
  const setCookies = res.headers.getSetCookie?.() ?? [];
  for (const c of setCookies) {
    const [pair] = c.split(";");
    const idx = pair.indexOf("=");
    if (idx > 0) jar.set(pair.slice(0, idx), pair.slice(idx + 1));
  }
}

function cookieHeader(): string {
  return [...jar.entries()].map(([k, v]) => `${k}=${v}`).join("; ");
}

async function request(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  const cookie = cookieHeader();
  if (cookie) headers.set("cookie", cookie);

  const res = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  storeCookies(res);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res;
}

async function login() {
  const res = await request("/session", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username: USERNAME, password: PASSWORD }),
  });
  return res.json();
}

async function main() {
  const data = await login();
  const user = data.user;

  console.log("登录成功!");
  console.log(`用户 ID      : ${user.id}`);
  console.log(`用户昵称     : ${user.username}`);
  console.log(`账户创建时间 : ${user.createdAt}`);
  console.log(`用户等级     : Lv.${user.level.current}`);
  console.log(`头像 URL     : ${user.avatar.url}`);
  console.log(`Session 建立 : ${data.createdAt}`);
  console.log(`Session 过期 : ${data.expiresAt}`);
  console.log(`禁言状态     : ${data.silence}`);

  for (const [k, v] of jar) console.log(`Cookie: ${k}=${v}`);

  // 后续请求自动带 Cookie:
  // const me = await (await request("/me")).json();
  // console.log(me);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
```
<!-- langtabs-end -->

