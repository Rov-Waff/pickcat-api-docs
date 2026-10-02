# 用户徽章

## 用户获得的徽章

> 获取用户获得的徽章 `/api/v1/users/{userId}/badges` GET

返回该用户获得的所有徽章。

### 响应体

```json
{
  "items": [
    {
      "userId": "01a0c957-53a6-798f-bf2a-2a83c94280d0",
      "badgeId": "badge_pioneer",
      "grantedAt": "2026-09-23T13:48:39.720Z",
      "revision": "013d6b44-6077-4834-aab2-0bbc80a96195",
      "badge": {
        "id": "badge_pioneer",
        "slug": "badge_pioneer",
        "name": "开拓者",
        "description": "参与Pickcat社区第一次内测",
        "icon": "trophy",
        "version": 4,
        "image": {
          "fileId": "01a0b34f-c685-7777-b60d-fe2a6adb6f52",
          "url": "/api/v1/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52",
          "width": 512, "height": 512
        }
      }
    }
  ]
}
```

| KEY       | VALUE            | TYPE     |
| --------- | ---------------- | -------- |
| userId    | 用户UUID         | String   |
| badgeId   | 徽章ID           | String   |
| grantedAt | 获得时间         | DateTime |
| revision  | 授予记录版本UUID | String   |
| badge     | 徽章详情         | Object   |

## 徽章展示设置

> 获取徽章展示设置 `/api/v1/users/{userId}/badge-display` GET

返回用户选择展示哪个徽章的策略。

### 响应体

```json
{ "mode": "AUTO_LATEST", "badgeId": null, "displayedBadge": null }
```

| KEY            | VALUE                       | TYPE          |
| -------------- | --------------------------- | ------------- |
| mode           | 展示模式，如 `AUTO_LATEST`  | String        |
| badgeId        | 指定展示的徽章ID，可为 null | String/Option |
| displayedBadge | 当前实际展示的徽章，可为 null | Object/Option |

## 批量查询展示徽章

> 批量查询展示徽章 `/api/v1/user-badge-displays?userIds={id1},{id2},...` GET

用于帖子/列表一次性拿到多位用户的展示徽章。

### Query

| KEY     | 说明                                   |
| ------- | -------------------------------------- |
| userIds | 用户UUID列表，以逗号分隔（URL 中被编码为 `%2C`） |

### 响应体

```json
{
  "items": [
    { "userId": "01a0fbca-...", "displayedBadge": null },
    { "userId": "03829981-...",
      "displayedBadge": {
        "id": "badge_pioneer", "name": "开拓者",
        "description": "参与Pickcat社区第一次内测",
        "image": { "fileId": "...", "url": "/api/v1/files/...", "width": 512, "height": 512 }
      }
    }
  ]
}
```

## 值得注意的

- 批量接口按传入顺序返回，`displayedBadge` 为 `null` 表示该用户没有可展示的徽章。
- 帖子/列表项中的 `author.displayedBadge` 与批量接口返回的是同一结构。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USER_ID: &str = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";
const USER_ID_2: &str = "03829981-0c9c-458d-a2df-1f30b78bc35a";

async fn get(client: &Client, path: &str) -> Result<Value> {
    Ok(client.get(format!("{BASE_URL}{path}"))
        .send().await?.error_for_status()?.json().await?)
}

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 先登录 (见《登录》)
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": "xxxx@gmail.com", "password": "P@ssW0rd123" }))
        .send().await?.error_for_status()?;

    // 用户获得的徽章
    let badges = get(&client, &format!("/users/{USER_ID}/badges")).await?;
    println!("徽章数: {}", badges["items"].as_array().map_or(0, Vec::len));

    // 徽章展示设置
    let display = get(&client, &format!("/users/{USER_ID}/badge-display")).await?;
    println!("展示模式: {}", display["mode"]);

    // 批量查询展示徽章
    let bulk = get(&client, &format!("/user-badge-displays?userIds={USER_ID},{USER_ID_2}")).await?;
    for item in bulk["items"].as_array().unwrap_or(&vec![]) {
        println!("{} -> {}", item["userId"], item["displayedBadge"]);
    }

    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"
USER_ID_2 = "03829981-0c9c-458d-a2df-1f30b78bc35a"

with requests.Session() as s:
    # 先登录 (见《登录》)
    s.post(f"{BASE_URL}/session",
           json={"username": "xxxx@gmail.com", "password": "P@ssW0rd123"}).raise_for_status()

    # 用户获得的徽章
    badges = s.get(f"{BASE_URL}/users/{USER_ID}/badges").raise_for_status().json()
    print("徽章数:", len(badges["items"]))

    # 徽章展示设置
    display = s.get(f"{BASE_URL}/users/{USER_ID}/badge-display").raise_for_status().json()
    print("展示模式:", display["mode"])

    # 批量查询展示徽章 (逗号会被编码为 %2C)
    bulk = s.get(f"{BASE_URL}/user-badge-displays",
                 params={"userIds": f"{USER_ID},{USER_ID_2}"}).raise_for_status().json()
    for item in bulk["items"]:
        print(item["userId"], "->", item["displayedBadge"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";
const USER_ID_2 = "03829981-0c9c-458d-a2df-1f30b78bc35a";
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

  const badges = await (await request(`/users/${USER_ID}/badges`)).json();
  console.log("徽章数:", badges.items.length);

  const display = await (await request(`/users/${USER_ID}/badge-display`)).json();
  console.log("展示模式:", display.mode);

  const bulk = await (await request(`/user-badge-displays?userIds=${USER_ID},${USER_ID_2}`)).json();
  for (const item of bulk.items) console.log(item.userId, "->", item.displayedBadge);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
