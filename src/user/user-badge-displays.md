# 批量查询展示徽章

> 批量查询展示徽章 `/api/v1/user-badge-displays` GET

用于帖子/列表一次性拿到多位用户的展示徽章。

## Query

| KEY     | 说明                                             |
| ------- | ------------------------------------------------ |
| userIds | 用户UUID列表，以逗号分隔（URL 中被编码为 `%2C`） |

## 响应体

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

| KEY                        | VALUE                 | TYPE          |
| -------------------------- | --------------------- | ------------- |
| items[].userId             | 用户UUID              | String        |
| items[].displayedBadge     | 展示徽章，可为 null   | Object/Option |

## 值得注意的

- 按传入顺序返回，`displayedBadge` 为 `null` 表示该用户没有可展示的徽章。
- 帖子/列表项中的 `author.displayedBadge` 与本接口返回的是同一结构。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const IDS: &str = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195,03829981-0c9c-458d-a2df-1f30b78bc35a";

#[tokio::main]
async fn main() -> Result<()> {
    let bulk: Value = Client::new()
        .get(format!("{BASE_URL}/user-badge-displays?userIds={IDS}"))
        .send().await?.error_for_status()?.json().await?;
    for item in bulk["items"].as_array().unwrap_or(&vec![]) {
        println!("{} -> {}", item["userId"], item["displayedBadge"]);
    }
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
IDS = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195,03829981-0c9c-458d-a2df-1f30b78bc35a"

bulk = requests.get(f"{BASE_URL}/user-badge-displays",
                    params={"userIds": IDS}).raise_for_status().json()
for item in bulk["items"]:
    print(item["userId"], "->", item["displayedBadge"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const IDS = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195,03829981-0c9c-458d-a2df-1f30b78bc35a";

async function main() {
  const res = await fetch(`${BASE_URL}/user-badge-displays?userIds=${IDS}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const bulk = await res.json();
  for (const item of bulk.items) console.log(item.userId, "->", item.displayedBadge);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
