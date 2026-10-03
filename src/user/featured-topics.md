# 精选主题

> 获取精选主题 `/api/v1/users/{userId}/featured-topics` GET

返回用户主页展示的精选主题，无分页。

## 响应体

```json
{ "items": [ { "...": "主题列表项，结构同用户发布的主题" } ] }
```

| KEY   | VALUE      | TYPE      |
| ----- | ---------- | --------- |
| items | 精选主题列表 | ArrayList |

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
    let featured: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/featured-topics"))
        .send().await?.error_for_status()?.json().await?;
    println!("精选主题: {}", featured["items"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

featured = requests.get(f"{BASE_URL}/users/{USER_ID}/featured-topics").raise_for_status().json()
print("精选主题:", len(featured["items"]))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/featured-topics`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const featured = await res.json();
  console.log("精选主题:", featured.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
