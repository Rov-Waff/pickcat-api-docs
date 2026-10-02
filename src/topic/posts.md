# 楼层列表

> 获取楼层列表 `/api/v1/topics/{topicId}/posts` GET

### Query

| KEY   | 观测值 | 说明            |
| ----- | ------ | --------------- |
| limit | `50`   | 每页数量        |
| sort  | `hot`  | 排序方式（热度）|

### 响应体

```json
{
  "items": [
    {
      "id": "...", "topicId": "...", "postNumber": 8, "replyToPostNumber": 1,
      "deleted": false, "children": [], "currentRevision": 1, "likeCount": 2,
      "pinned": false, "cookedHtml": "<p>获奖了哈哈哈</p>",
      "author": { "id": "...", "username": "...", "avatar": { "...": "..." }, "displayedBadge": null },
      "createdAt": "...", "editedAt": null,
      "viewerCapabilities": { "...": "..." }, "viewerState": { "...": "..." }
    }
  ],
  "pageInfo": { "hasNextPage": false, "nextCursor": null }
}
```

| KEY                        | VALUE                        | TYPE           |
| -------------------------- | ---------------------------- | -------------- |
| id / topicId               | 楼层UUID / 所属主题UUID      | String         |
| postNumber                 | 楼层号（从 1 开始）          | Integer        |
| replyToPostNumber          | 回复的目标楼层号，可为 null  | Integer/Option |
| deleted                    | 是否已删除                   | Boolean        |
| children                   | 子楼层（树形结构）           | ArrayList      |
| currentRevision            | 当前编辑版本号               | Integer        |
| likeCount                  | 点赞数                       | Integer        |
| pinned                     | 是否置顶                     | Boolean        |
| cookedHtml                 | 渲染好的正文 HTML            | String         |
| author                     | 作者（含头像、展示徽章）     | Object         |
| createdAt / editedAt       | 创建/编辑时间                | DateTime/Option|
| viewerCapabilities / viewerState | 当前用户权限/状态      | Object         |

## 值得注意的

- 楼层为**树形结构**：顶层回复通过 `replyToPostNumber` 指向父楼层，子回复放在 `children` 中。
- 与主题详情一致，`viewerCapabilities` / `viewerState` 随内容下发。
- 分页游标同样使用 `pageInfo.nextCursor`。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const TOPIC_ID: &str = "01a0eb91-5d11-7fb0-b998-179add93620f";

#[tokio::main]
async fn main() -> Result<()> {
    let client = Client::new();
    let posts: Value = client
        .get(format!("{BASE_URL}/topics/{TOPIC_ID}/posts?limit=50&sort=hot"))
        .send().await?.error_for_status()?.json().await?;

    for p in posts["items"].as_array().unwrap_or(&vec![]) {
        println!("#{} {} - {}", p["postNumber"], p["author"]["username"], p["cookedHtml"]);
    }
    println!("还有下一页: {}", posts["pageInfo"]["hasNextPage"]);
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
TOPIC_ID = "01a0eb91-5d11-7fb0-b998-179add93620f"

with requests.Session() as s:
    posts = s.get(
        f"{BASE_URL}/topics/{TOPIC_ID}/posts",
        params={"limit": 50, "sort": "hot"},
    ).raise_for_status().json()

    for p in posts["items"]:
        print(f'#{p["postNumber"]}', p["author"]["username"], "-", p["cookedHtml"])
    print("还有下一页:", posts["pageInfo"]["hasNextPage"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const TOPIC_ID = "01a0eb91-5d11-7fb0-b998-179add93620f";

async function main() {
  const res = await fetch(`${BASE_URL}/topics/${TOPIC_ID}/posts?limit=50&sort=hot`);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  const posts = await res.json();

  for (const p of posts.items) {
    console.log(`#${p.postNumber}`, p.author.username, "-", p.cookedHtml);
  }
  console.log("还有下一页:", posts.pageInfo.hasNextPage);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
