# 用户的回帖

> 获取用户的回帖 `/api/v1/users/{userId}/posts` GET

## Query

| KEY   | 观测值  | 说明     |
| ----- | ------- | -------- |
| role  | `reply` | 内容角色 |
| limit | `20`    | 每页数量 |

## 响应体

注意：该接口返回的是「回帖摘要 + 所属主题」，**不是**楼层列表的完整楼层对象，不含 `author`、`children`、`viewerCapabilities` 等字段。

```json
{
  "items": [
    {
      "id": "01a1b427-9044-75a1-a5e8-9e1c739779fb",
      "postNumber": 4,
      "cookedHtml": "<p>...</p>",
      "replyCount": 0,
      "viewCount": 18,
      "likeCount": 0,
      "bookmarkCount": 0,
      "topic": { "id": "01a1b3d9-9625-732c-839d-68195f11644a", "title": "主题标题" },
      "createdAt": "2026-11-07T03:57:34.124Z"
    }
  ],
  "pageInfo": { "hasNextPage": false, "nextCursor": null }
}
```

| KEY             | VALUE                       | TYPE     |
| --------------- | --------------------------- | -------- |
| id              | 楼层UUID                    | String   |
| postNumber      | 楼层号（从 1 开始）         | Integer  |
| cookedHtml      | 渲染好的正文 HTML           | String   |
| replyCount      | 该楼层的回复数              | Integer  |
| viewCount       | 该楼层的浏览数              | Integer  |
| likeCount       | 点赞数                      | Integer  |
| bookmarkCount   | 收藏数                      | Integer  |
| topic           | 所属主题的精简信息          | Object   |
| topic.id        | 主题UUID                    | String   |
| topic.title     | 主题标题                    | String   |
| createdAt       | 创建时间                    | DateTime |

## 值得注意的

- 与楼层列表 [`/topics/{id}/posts`](../topic/posts.md) 不同：本接口不返回 `author`、`children`、`viewerCapabilities` / `viewerState`，需要作者信息时请再请求楼层列表或主题详情。
- 使用统一游标分页 `pageInfo.hasNextPage` / `pageInfo.nextCursor`。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://pickcat.dao3.fun/api/v1";
const USER_ID: &str = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

#[tokio::main]
async fn main() -> Result<()> {
    let posts: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/posts?role=reply&limit=20"))
        .send().await?.error_for_status()?.json().await?;
    for p in posts["items"].as_array().unwrap_or(&vec![]) {
        println!("#{} {} - {}", p["postNumber"], p["topic"]["title"], p["cookedHtml"]);
    }
    Ok(())
}
```
```python
import requests

BASE_URL = "https://pickcat.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

posts = requests.get(f"{BASE_URL}/users/{USER_ID}/posts",
                     params={"role": "reply", "limit": 20}).raise_for_status().json()
for p in posts["items"]:
    print(f'#{p["postNumber"]}', p["topic"]["title"], "-", p["cookedHtml"])
```
```typescript
const BASE_URL = "https://pickcat.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/posts?role=reply&limit=20`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const posts = await res.json();
  for (const p of posts.items) console.log(`#${p.postNumber}`, p.topic.title, "-", p.cookedHtml);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
