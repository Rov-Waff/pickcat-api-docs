# 登录

> 登录 `/api/v1/session` POST

> ⚠️ **登录已接入 CAPTCHA**
>
> 登录请求现在需要携带阿里云验证码结果 `captchaVerifyParam`。该参数必须由前端验证码组件在真实浏览器中生成，脚本无法凭空构造，因此**通过接口自动登录获取 Session 并不现实**。脚本场景建议先在浏览器手动登录，再导出并复用 `pickcat_session` Cookie。

## 请求体

```json
{
    "account": "xxxx@gmail.com",
    "password": "P@ssW0rd123",
    "captchaVerifyParam": "<base64(阿里云验证码回调 JSON)>"
}
```

| KEY                 | VALUE                                              | TYPE   |
| ------------------- | -------------------------------------------------- | ------ |
| account             | 账号，可填邮箱或用户名                             | String |
| password            | 密码                                               | String |
| captchaVerifyParam  | 阿里云验证码结果，Base64 编码后的回调 JSON         | String |

`captchaVerifyParam` 解码后形如：

```json
{
    "certifyId": "...",
    "sceneId": "1icer78a",
    "isSign": true,
    "securityToken": "..."
}
```

## 响应体

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
| user      | 用户基础信息    | Object     |
| createdAt | Session建立时间 | DateTime   |
| expiresAt | Session过期时间 | DateTime   |
| silence   | 含义未验证（可能与禁言有关） | Any/Option |

### user字段



| KEY                  | VALUE                          | TYPE          |
| -------------------- | ------------------------------ | ------------- |
| id                   | 用户UUID                       | String        |
| username             | 用户昵称                       | String        |
| createdAt            | 账户创建时间                   | DateTime      |
| avatar               | 头像                           | Object        |
| tokenBalance         | 代币余额（字段含义推测）       | Integer       |
| level                | 用户等级                       | Object        |
| effectivePermissions | 特殊权限列表，元素含 key/scopes | ArrayList/Vec |

### effectivePermissions 元素

| KEY    | VALUE                          | TYPE          |
| ------ | ------------------------------ | ------------- |
| key    | 权限标识，如 `content.publish` | String        |
| scopes | 生效范围，如 `[{"type":"SITE"}]` | ArrayList/Vec |

## 值得注意的

- **登录新增了 CAPTCHA**：`captchaVerifyParam` 来自前端阿里云验证码组件，无法仅靠脚本生成；没有有效验证码时登录会失败。
- 因此**用接口登录获取 Session 并不现实**。推荐在浏览器手动登录后，从开发者工具复制 `pickcat_session` Cookie 供脚本复用；已有 Cookie 也可通过 [`GET /api/v1/session`](./session.md) 验证是否仍有效。
- 账号字段已由 `username` 改为 `account`，邮箱或用户名均可。
- 与主站不同，Pickcat使用Session鉴权，而不是JWT，因此，返回体**不含 token**，会话凭据通过 HTTP头部`Set-Cookie` 下发
- Session有效期 **7 天**
- 成功返回 `201 Created`，响应头包含 `location: /api/v1/session`。

## 示例
<!-- langtabs-start -->

```rust
use anyhow::{Context, Result};
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

// 注意: 已包含 /api/v1
const BASE_URL: &str = "https://pickcat.dao3.fun/api/v1";
const ACCOUNT: &str = "xxxx@gmail.com";
const PASSWORD: &str = "P@ssW0rd123";
// 必须由浏览器中的阿里云验证码组件生成，脚本无法凭空构造
const CAPTCHA_VERIFY_PARAM: &str = "<base64(阿里云验证码回调 JSON)>";

async fn login(client: &Client) -> Result<Value> {
    // 没有有效的 CAPTCHA_VERIFY_PARAM 时，该请求会失败
    let resp = client
        .post(format!("{BASE_URL}/session")) // -> /api/v1/session
        .json(&json!({
            "account": ACCOUNT,
            "password": PASSWORD,
            "captchaVerifyParam": CAPTCHA_VERIFY_PARAM,
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

BASE_URL = "https://pickcat.dao3.fun/api/v1"
ACCOUNT = "xxxx@gmail.com"
PASSWORD = "P@ssW0rd123"
# 必须由浏览器中的阿里云验证码组件生成，脚本无法凭空构造
CAPTCHA_VERIFY_PARAM = "<base64(阿里云验证码回调 JSON)>"


def login(session: requests.Session) -> dict:
    # 没有有效的 CAPTCHA_VERIFY_PARAM 时，该请求会失败
    resp = session.post(
        f"{BASE_URL}/session",
        json={
            "account": ACCOUNT,
            "password": PASSWORD,
            "captchaVerifyParam": CAPTCHA_VERIFY_PARAM,
        },
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
const BASE_URL = "https://pickcat.dao3.fun/api/v1";
const ACCOUNT = "xxxx@gmail.com";
const PASSWORD = "P@ssW0rd123";
// 必须由浏览器中的阿里云验证码组件生成，脚本无法凭空构造
const CAPTCHA_VERIFY_PARAM = "<base64(阿里云验证码回调 JSON)>";

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
  // 没有有效的 CAPTCHA_VERIFY_PARAM 时，该请求会失败
  const res = await request("/session", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      account: ACCOUNT,
      password: PASSWORD,
      captchaVerifyParam: CAPTCHA_VERIFY_PARAM,
    }),
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
