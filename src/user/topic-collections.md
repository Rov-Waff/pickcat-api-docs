# 用户的合集

> 获取用户的合集 `/api/v1/users/{userId}/topic-collections` GET

## Query

| KEY   | 观测值 | 说明     |
| ----- | ------ | -------- |
| limit | `20`   | 每页数量 |

## 响应体

```json
{ "items": [], "pageInfo": { "hasNextPage": false, "nextCursor": null } }
```

| KEY      | VALUE    | TYPE      |
| -------- | -------- | --------- |
| items    | 合集列表 | ArrayList |
| pageInfo | 分页信息 | Object    |

## 值得注意的

- 合集配额（上限/已用）见[合集配额用量](./topic-collection-usage.md)。

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
    let collections: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/topic-collections?limit=20"))
        .send().await?.error_for_status()?.json().await?;
    println!("合集: {}", collections["items"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

collections = requests.get(f"{BASE_URL}/users/{USER_ID}/topic-collections",
                           params={"limit": 20}).raise_for_status().json()
print("合集:", len(collections["items"]))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/topic-collections?limit=20`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const collections = await res.json();
  console.log("合集:", collections.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
