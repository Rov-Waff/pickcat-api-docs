# 用户发布的主题

> 获取用户发布的主题 `/api/v1/users/{userId}/topics` GET

## Query

| KEY   | 观测值 | 说明     |
| ----- | ------ | -------- |
| limit | `20`   | 每页数量 |

## 响应体

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

| KEY                                               | VALUE                                 | TYPE            |
| ------------------------------------------------- | ------------------------------------- | --------------- |
| id                                                | 主题UUID                              | String          |
| title                                             | 标题                                  | String          |
| kind                                              | `DISCUSSION`/`QUESTION`/`ANNOUNCEMENT` | String         |
| excerpt                                           | 摘要                                  | String          |
| author                                            | 作者（含头像、展示徽章）              | Object          |
| tags                                              | 所属标签                              | ArrayList       |
| replyCount / viewCount / likeCount / bookmarkCount | 回复/浏览/点赞/收藏数                | Integer         |
| questionState                                     | 问答状态，仅 `QUESTION` 时存在        | Object/Option   |
| closedAt                                          | 关闭时间，可为 null                   | DateTime/Option |
| pinned / pinnedGlobally                           | 是否分区内/全局置顶                   | Boolean         |
| createdAt / editedAt / lastActivityAt             | 创建/编辑/最后活跃时间                | DateTime        |

## 值得注意的

- 与主题列表 [`/topics`](../topic/list.md) 的列表项结构一致。
- 使用统一游标分页 `pageInfo.hasNextPage` / `pageInfo.nextCursor`。

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
    let topics: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/topics?limit=20"))
        .send().await?.error_for_status()?.json().await?;
    for t in topics["items"].as_array().unwrap_or(&vec![]) {
        println!("[{}] {}", t["kind"], t["title"]);
    }
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

topics = requests.get(f"{BASE_URL}/users/{USER_ID}/topics",
                      params={"limit": 20}).raise_for_status().json()
for t in topics["items"]:
    print(f'[{t["kind"]}]', t["title"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/topics?limit=20`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const topics = await res.json();
  for (const t of topics.items) console.log(`[${t.kind}]`, t.title);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
