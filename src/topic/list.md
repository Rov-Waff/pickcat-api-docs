# 主题列表

> 获取主题列表 `/api/v1/topics` GET

## Query

| KEY     | 观测值              | 说明                                          |
| ------- | ------------------- | --------------------------------------------- |
| limit   | `20`                | 每页数量                                      |
| tag     | `interest-plaza` 等 | 标签 slug，**可重复传入**实现多标签过滤       |
| tagMode | `all`               | 多标签匹配模式，`all` 表示同时包含这些标签    |

## 响应体

```json
{
  "items": [ { "...": "主题列表项，见下表" } ],
  "pageInfo": { "hasNextPage": false, "nextCursor": null }
}
```

## 主题列表项字段

| KEY                                              | VALUE                                | TYPE             |
| ------------------------------------------------ | ------------------------------------ | ---------------- |
| id                                               | 主题UUID                             | String           |
| title                                            | 标题                                 | String           |
| kind                                             | `DISCUSSION`/`QUESTION`/`ANNOUNCEMENT` | String         |
| excerpt                                          | 摘要                                 | String           |
| author                                           | 作者（id/username/avatar/displayedBadge） | Object       |
| tags                                             | 所属标签                             | ArrayList        |
| replyCount / viewCount / likeCount / bookmarkCount | 回复/浏览/点赞/收藏数              | Integer          |
| questionState                                    | 问答状态，仅 `QUESTION` 时存在       | Object/Option    |
| closedAt                                         | 关闭时间，可为 null                  | DateTime/Option  |
| pinned / pinnedGlobally                          | 是否分区内/全局置顶                  | Boolean          |
| pinnedTagId / pinnedAt / pinnedUntil             | 置顶相关信息                         | String/DateTime/Option |
| createdAt / editedAt / lastActivityAt            | 创建/编辑/最后活跃时间               | DateTime         |

## 值得注意的

- 分页统一为 `pageInfo.hasNextPage` / `pageInfo.nextCursor`，取下一页时把 `nextCursor` 作为 `cursor` 参数回传。
- 多标签过滤时同一个 `tag` 参数会重复出现，例如 `?tag=interest-plaza&tag=creative-works&tagMode=all`。
- 首页推荐请使用[首页推荐](./recommendations.md)，单次返回 20 条并用 `reason` 解释推荐原因。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const TAG: &str = "interest-plaza";

async fn get(client: &Client, path: &str) -> Result<Value> {
    Ok(client.get(format!("{BASE_URL}{path}"))
        .send().await?.error_for_status()?.json().await?)
}

#[tokio::main]
async fn main() -> Result<()> {
    let client = Client::new();

    // 主题列表（多标签过滤: 同一个 tag 重复出现）
    let list = get(&client, &format!("/topics?limit=20&tag={TAG}&tagMode=all")).await?;
    for t in list["items"].as_array().unwrap_or(&vec![]) {
        println!("[{}] {}", t["kind"], t["title"]);
    }

    println!("还有下一页: {}", list["pageInfo"]["hasNextPage"]);
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
TAG = "interest-plaza"

with requests.Session() as s:
    # 主题列表（多标签过滤: 同一个 tag 重复出现）
    list_resp = s.get(f"{BASE_URL}/topics",
                      params=[("limit", 20), ("tag", TAG), ("tagMode", "all")]).raise_for_status().json()
    for t in list_resp["items"]:
        print(f'[{t["kind"]}]', t["title"])
    print("还有下一页:", list_resp["pageInfo"]["hasNextPage"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const TAG = "interest-plaza";

async function get(path: string): Promise<any> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

async function main() {
  // 主题列表（多标签过滤: 同一个 tag 重复出现）
  const list = await get(`/topics?limit=20&tag=${TAG}&tagMode=all`);
  for (const t of list.items) console.log(`[${t.kind}]`, t.title);
  console.log("还有下一页:", list.pageInfo.hasNextPage);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
