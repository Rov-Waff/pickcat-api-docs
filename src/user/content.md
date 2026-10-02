# 用户内容

用户发布或收藏的内容列表，除「精选主题」外均为游标分页。

## 发布的主题

> 获取用户发布的主题 `/api/v1/users/{userId}/topics` GET

### Query

| KEY   | 观测值 | 说明     |
| ----- | ------ | -------- |
| limit | `20`   | 每页数量 |

### 响应体

```json
{
  "items": [
    {
      "id": "01a0e145-131b-708a-bfd2-051c68c7cf24",
      "title": "做了一个联机小测试，欢迎大家体验",
      "kind": "DISCUSSION",
      "excerpt": "https://player.codemao.cn/new/327450447",
      "author": { "id": "...", "username": "朗kea9", "avatar": { "type": "CUSTOM", "id": "...", "url": "/api/v1/avatars/..." } },
      "tags": [ { "id": "...", "slug": "creative-works", "name": "创作与作品" } ],
      "replyCount": 0, "viewCount": 5, "likeCount": 0, "bookmarkCount": 0,
      "closedAt": null,
      "pinned": false, "pinnedGlobally": false, "pinnedTagId": null,
      "pinnedAt": null, "pinnedUntil": null,
      "createdAt": "2026-09-27T05:09:55.600Z",
      "editedAt": null,
      "lastActivityAt": "2026-09-27T05:10:12.121Z"
    }
  ],
  "pageInfo": { "hasNextPage": false, "nextCursor": null }
}
```

| KEY              | VALUE                              | TYPE          |
| ---------------- | ---------------------------------- | ------------- |
| id               | 主题UUID                           | String        |
| title            | 标题                               | String        |
| kind             | `DISCUSSION`/`QUESTION`/`ANNOUNCEMENT` | String    |
| excerpt          | 摘要                               | String        |
| author           | 作者（含头像、展示徽章）           | Object        |
| tags             | 所属标签                           | ArrayList     |
| replyCount       | 回复数                             | Integer       |
| viewCount        | 浏览数                             | Integer       |
| likeCount        | 点赞数                             | Integer       |
| bookmarkCount    | 收藏数                             | Integer       |
| closedAt         | 关闭时间，可为 null                | DateTime/Option |
| pinned           | 是否置顶（分区内）                 | Boolean       |
| pinnedGlobally   | 是否全局置顶                       | Boolean       |
| createdAt        | 发布时间                           | DateTime      |
| editedAt         | 编辑时间，可为 null                | DateTime/Option |
| lastActivityAt   | 最后活跃时间                       | DateTime      |

> `kind` 为 `QUESTION` 时还会带 `questionState` 字段。

## 回帖

> 获取用户的回帖 `/api/v1/users/{userId}/posts` GET

### Query

| KEY   | 观测值   | 说明               |
| ----- | -------- | ------------------ |
| role  | `reply`  | 内容角色           |
| limit | `20`     | 每页数量           |

### 响应体

```json
{
  "items": [
    {
      "id": "...", "topicId": "...", "postNumber": 8, "replyToPostNumber": 1,
      "deleted": false, "children": [], "currentRevision": 1, "likeCount": 2,
      "pinned": false, "cookedHtml": "<p>...</p>",
      "author": { "id": "...", "username": "...", "avatar": { "...": "..." } },
      "createdAt": "...", "editedAt": null,
      "viewerCapabilities": { "...": "..." }, "viewerState": { "...": "..." }
    }
  ],
  "pageInfo": { "hasNextPage": false, "nextCursor": null }
}
```

## 精选主题

> 获取精选主题 `/api/v1/users/{userId}/featured-topics` GET

返回用户主页展示的精选主题，无分页。

### 响应体

```json
{ "items": [ { "...": "主题列表项，结构同上" } ] }
```

## 合集

> 获取用户的合集 `/api/v1/users/{userId}/topic-collections` GET

### Query

| KEY   | 观测值 | 说明     |
| ----- | ------ | -------- |
| limit | `20`   | 每页数量 |

### 响应体

```json
{ "items": [], "pageInfo": { "hasNextPage": false, "nextCursor": null } }
```

> 合集配额（上限/已用）见[合集配额用量](./level.md#合集配额用量)。

## 值得注意的

- 个人主页会并发调用上述多个接口按需加载，而非使用聚合接口。
- 所有列表接口共用同一套游标分页结构：`pageInfo.hasNextPage` / `pageInfo.nextCursor`。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USER_ID: &str = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

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

    let topics = get(&client, &format!("/users/{USER_ID}/topics?limit=20")).await?;
    let posts = get(&client, &format!("/users/{USER_ID}/posts?role=reply&limit=20")).await?;
    let featured = get(&client, &format!("/users/{USER_ID}/featured-topics")).await?;
    let collections = get(&client, &format!("/users/{USER_ID}/topic-collections?limit=20")).await?;

    println!("发布主题: {}", topics["items"].as_array().map_or(0, Vec::len));
    println!("回帖    : {}", posts["items"].as_array().map_or(0, Vec::len));
    println!("精选主题: {}", featured["items"].as_array().map_or(0, Vec::len));
    println!("合集    : {}", collections["items"].as_array().map_or(0, Vec::len));

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

    topics = s.get(f"{BASE_URL}/users/{USER_ID}/topics", params={"limit": 20}).raise_for_status().json()
    posts = s.get(f"{BASE_URL}/users/{USER_ID}/posts",
                  params={"role": "reply", "limit": 20}).raise_for_status().json()
    featured = s.get(f"{BASE_URL}/users/{USER_ID}/featured-topics").raise_for_status().json()
    collections = s.get(f"{BASE_URL}/users/{USER_ID}/topic-collections",
                        params={"limit": 20}).raise_for_status().json()

    print("发布主题:", len(topics["items"]))
    print("回帖    :", len(posts["items"]))
    print("精选主题:", len(featured["items"]))
    print("合集    :", len(collections["items"]))
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

  const topics = await (await request(`/users/${USER_ID}/topics?limit=20`)).json();
  const posts = await (await request(`/users/${USER_ID}/posts?role=reply&limit=20`)).json();
  const featured = await (await request(`/users/${USER_ID}/featured-topics`)).json();
  const collections = await (await request(`/users/${USER_ID}/topic-collections?limit=20`)).json();

  console.log("发布主题:", topics.items.length);
  console.log("回帖    :", posts.items.length);
  console.log("精选主题:", featured.items.length);
  console.log("合集    :", collections.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
