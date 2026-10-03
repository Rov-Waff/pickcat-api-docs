# 用户的回帖

> 获取用户的回帖 `/api/v1/users/{userId}/posts` GET

## Query

| KEY   | 观测值  | 说明     |
| ----- | ------- | -------- |
| role  | `reply` | 内容角色 |
| limit | `20`    | 每页数量 |

## 响应体

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

| KEY               | VALUE                   | TYPE            |
| ----------------- | ----------------------- | --------------- |
| id / topicId      | 楼层UUID / 所属主题UUID | String          |
| postNumber        | 楼层号（从 1 开始）     | Integer         |
| replyToPostNumber | 回复的目标楼层号，可为 null | Integer/Option |
| deleted           | 是否已删除              | Boolean         |
| children          | 子楼层（树形结构）      | ArrayList       |
| currentRevision   | 当前编辑版本号          | Integer         |
| likeCount         | 点赞数                  | Integer         |
| cookedHtml        | 渲染好的正文 HTML       | String          |
| author            | 作者（含头像、展示徽章）| Object          |
| createdAt / editedAt | 创建/编辑时间        | DateTime/Option |

## 值得注意的

- 与楼层列表 [`/topics/{id}/posts`](../topic/posts.md) 的楼层项结构一致。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USER_ID: &str = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

#[tokio::main]
async fn main() -> Result<()> {
    let posts: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/posts?role=reply&limit=20"))
        .send().await?.error_for_status()?.json().await?;
    for p in posts["items"].as_array().unwrap_or(&vec![]) {
        println!("#{} {}", p["postNumber"], p["cookedHtml"]);
    }
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

posts = requests.get(f"{BASE_URL}/users/{USER_ID}/posts",
                     params={"role": "reply", "limit": 20}).raise_for_status().json()
for p in posts["items"]:
    print(f'#{p["postNumber"]}', p["cookedHtml"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/posts?role=reply&limit=20`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const posts = await res.json();
  for (const p of posts.items) console.log(`#${p.postNumber}`, p.cookedHtml);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
