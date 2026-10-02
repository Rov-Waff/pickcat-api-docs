# 主题详情

> 获取主题详情 `/api/v1/topics/{topicId}` GET

返回主题本体、1 楼（`firstPost`）以及当前用户的权限与状态。

## 响应体

```json
{
  "id": "01a0eb91-5d11-7fb0-b998-179add93620f",
  "title": "【共琢一轮月】……获奖名单公示",
  "kind": "ANNOUNCEMENT",
  "author": { "id": "...", "username": "hajimes", "avatar": { "...": "..." }, "displayedBadge": { "...": "..." } },
  "tags": [ { "id": "...", "slug": "events-competitions", "name": "活动与赛事" } ],
  "replyCount": 24, "viewCount": 96, "likeCount": 0, "bookmarkCount": 0,
  "collection": null,
  "closedAt": null, "closedBy": null,
  "pinned": true, "pinnedGlobally": true, "pinnedTagId": null,
  "pinnedAt": "2026-09-29T08:33:47.233Z", "pinnedUntil": null,
  "lastActivityAt": "2026-10-02T07:04:32.485Z",
  "createdAt": "2026-09-29T05:09:27.428Z",
  "editedAt": "2026-09-29T09:59:19.985Z",
  "updatedAt": "2026-10-02T07:04:32.485Z",
  "firstPost": {
    "id": "...", "topicId": "...", "postNumber": 1, "replyToPostNumber": null,
    "deleted": false, "children": [], "currentRevision": 2, "likeCount": 4,
    "pinned": false, "cookedHtml": "<p>...</p>", "author": { "...": "..." },
    "createdAt": "...", "editedAt": "...",
    "viewerCapabilities": { "canEdit": false, "canLike": true, "canBookmark": true, "canReport": true, "canSelectAnswer": false },
    "viewerState": { "liked": false, "bookmarkId": null, "selectedAnswer": false }
  },
  "repliesTruncated": true,
  "events": [],
  "eventsTruncated": false,
  "viewerCapabilities": {
    "canEdit": false, "canReply": true, "canDelete": false, "canBookmark": true,
    "canClose": false, "canReopen": false, "canPinGlobally": false, "pinnableTagIds": []
  },
  "viewerState": { "bookmarkId": null }
}
```

| KEY                  | VALUE                                       | TYPE            |
| -------------------- | ------------------------------------------- | --------------- |
| id / title / kind    | 主题UUID / 标题 / 类型                      | String          |
| author               | 作者（含头像、展示徽章）                    | Object          |
| tags                 | 所属标签                                    | ArrayList       |
| replyCount / viewCount / likeCount / bookmarkCount | 计数          | Integer         |
| collection           | 所属合集，可为 null                         | Object/Option   |
| closedAt / closedBy  | 关闭时间与操作人，可为 null                 | DateTime/String/Option |
| pinned / pinnedGlobally | 是否分区内/全局置顶                     | Boolean         |
| firstPost            | 1 楼内容（结构同楼层列表项）                | Object          |
| repliesTruncated     | 回复是否被截断（需要另外请求楼层列表）      | Boolean         |
| events / eventsTruncated | 主题事件流                              | ArrayList/Boolean |
| viewerCapabilities   | 当前用户可执行的操作                        | Object          |
| viewerState          | 当前用户与主题的关系（如是否收藏）          | Object          |

## 值得注意的

- `firstPost.currentRevision` 是编辑版本号；`cookedHtml` 是服务端渲染好的 HTML。
- `viewerCapabilities` / `viewerState` 预先随内容下发，前端据此显隐按钮，避免额外权限请求。
- `repliesTruncated` 为 `true` 时需要再调用[楼层列表](./posts.md)拉取回复。

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
    let topic: Value = client.get(format!("{BASE_URL}/topics/{TOPIC_ID}"))
        .send().await?.error_for_status()?.json().await?;

    println!("标题  : {}", topic["title"]);
    println!("回复/浏览: {}/{}", topic["replyCount"], topic["viewCount"]);
    println!("1楼   : {}", topic["firstPost"]["cookedHtml"]);
    println!("可回复: {}", topic["viewerCapabilities"]["canReply"]);
    println!("回复被截断: {}", topic["repliesTruncated"]);
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
TOPIC_ID = "01a0eb91-5d11-7fb0-b998-179add93620f"

with requests.Session() as s:
    topic = s.get(f"{BASE_URL}/topics/{TOPIC_ID}").raise_for_status().json()
    print("标题  :", topic["title"])
    print("回复/浏览:", topic["replyCount"], "/", topic["viewCount"])
    print("1楼   :", topic["firstPost"]["cookedHtml"])
    print("可回复:", topic["viewerCapabilities"]["canReply"])
    print("回复被截断:", topic["repliesTruncated"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const TOPIC_ID = "01a0eb91-5d11-7fb0-b998-179add93620f";

async function main() {
  const res = await fetch(`${BASE_URL}/topics/${TOPIC_ID}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  const topic = await res.json();

  console.log("标题  :", topic.title);
  console.log("回复/浏览:", topic.replyCount + "/" + topic.viewCount);
  console.log("1楼   :", topic.firstPost.cookedHtml);
  console.log("可回复:", topic.viewerCapabilities.canReply);
  console.log("回复被截断:", topic.repliesTruncated);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
