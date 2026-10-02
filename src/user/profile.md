# 用户资料

## 获取用户资料

> 获取用户资料 `/api/v1/users/{userId}` GET

用于个人主页，返回用户基础信息、统计以及当前访问者与 TA 的关系。

### 响应体

```json
{
  "id": "01a0fbca-eee1-70ad-a00d-a1ed4c89b195",
  "username": "CarbonPremium",
  "avatar": { "type": "PRESET", "id": 1, "url": "/api/v1/avatars/1?v=f558..." },
  "bio": null,
  "region": null,
  "showFollowingList": true,
  "showFollowersList": true,
  "createdAt": "2026-10-02T08:46:15.771Z",
  "level": { "current": 1 },
  "stats": { "followers": 0, "following": 0, "topics": 0, "replies": 0 },
  "viewerState": { "following": false, "canFollow": false }
}
```

| KEY               | VALUE                        | TYPE          |
| ----------------- | ---------------------------- | ------------- |
| id                | 用户UUID                     | String        |
| username          | 用户昵称                     | String        |
| avatar            | 头像                         | Object        |
| bio               | 个人简介，可为 null          | String/Option |
| region            | 地区，可为 null              | String/Option |
| showFollowingList | 是否公开「关注」列表         | Boolean       |
| showFollowersList | 是否公开「粉丝」列表         | Boolean       |
| createdAt         | 账户创建时间                 | DateTime      |
| level.current     | 当前等级                     | Integer       |
| stats             | 关注/粉丝/主题/回帖计数      | Object        |
| viewerState       | 当前访问者与用户的关系       | Object        |

> `avatar.type` 为 `PRESET` 时，`id` 是预设头像编号，`url` 带 `?v=<内容哈希>`；为 `CUSTOM` 时，`id` 是自定义头像的 `fileId`，`url` 形如 `/api/v1/avatars/{fileId}`。
>
> `viewerState.following` 表示当前访问者是否已关注该用户；`canFollow` 表示是否允许关注（自己不能关注自己）。

## 修改个人资料

> 修改个人资料 `/api/v1/users/{userId}` PATCH **需要Cookie**

只能修改自己的资料，`{userId}` 必须与当前会话用户一致。

### 请求体

```json
{ "bio": "Acrb" }
```

| KEY | VALUE    | TYPE   |
| --- | -------- | ------ |
| bio | 个人简介 | String |

### 响应体

返回更新后的完整用户对象，结构同「获取用户资料」，其中 `bio` 已变更。

## 查询用户邮箱(仅自己)

> 查询用户邮箱 `/api/v1/users/{userId}/email` GET **需要Cookie**

### 响应体

```json
{ "email": "2710182206@qq.com", "verifiedAt": "2026-10-02T08:46:15.771Z" }
```

| KEY        | VALUE        | TYPE     |
| ---------- | ------------ | -------- |
| email      | 邮箱地址     | String   |
| verifiedAt | 邮箱验证时间 | DateTime |

## 值得注意的

- 邮箱接口只对用户本人开放，访问他人邮箱的具体错误响应尚未验证。
- `PATCH` 只提交需要变更的字段即可，未提交的字段保持不变。

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

    // 获取用户资料
    let user: Value = client.get(format!("{BASE_URL}/users/{USER_ID}"))
        .send().await?.error_for_status()?.json().await?;
    println!("{} Lv.{} 主题{} 回帖{}",
        user["username"], user["level"]["current"],
        user["stats"]["topics"], user["stats"]["replies"]);

    // 修改个人资料 (仅自己)
    let updated: Value = client.patch(format!("{BASE_URL}/users/{USER_ID}"))
        .json(&json!({ "bio": "Acrb" }))
        .send().await?.error_for_status()?.json().await?;
    println!("新简介: {}", updated["bio"]);

    // 查询邮箱 (仅自己)
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

    # 获取用户资料
    user = s.get(f"{BASE_URL}/users/{USER_ID}").raise_for_status().json()
    print(user["username"], "Lv." + str(user["level"]["current"]),
          "主题", user["stats"]["topics"], "回帖", user["stats"]["replies"])

    # 修改个人资料 (仅自己)
    updated = s.patch(f"{BASE_URL}/users/{USER_ID}", json={"bio": "Acrb"}).raise_for_status().json()
    print("新简介:", updated["bio"])

    # 查询邮箱 (仅自己)
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

  // 获取用户资料
  const user = await (await request(`/users/${USER_ID}`)).json();
  console.log(user.username, `Lv.${user.level.current}`,
    "主题", user.stats.topics, "回帖", user.stats.replies);

  // 修改个人资料 (仅自己)
  const updated = await (await request(`/users/${USER_ID}`, {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ bio: "Acrb" }),
  })).json();
  console.log("新简介:", updated.bio);

  // 查询邮箱 (仅自己)
  const email = await (await request(`/users/${USER_ID}/email`)).json();
  console.log("邮箱:", email.email, email.verifiedAt);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
