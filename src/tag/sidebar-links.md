# 分区侧边子标签

> 获取分区侧边子标签 `/api/v1/tags/{slug}/sidebar-links` GET

## 响应体

```json
{
  "source": { "id": "...", "slug": "interest-plaza", "name": "兴趣广场", "description": "..." },
  "items": [ { "...": "该分区下的子标签，结构同标签项" } ]
}
```

| KEY    | VALUE            | TYPE      |
| ------ | ---------------- | --------- |
| source | 当前分区标签     | Object    |
| items  | 侧边栏子标签列表 | ArrayList |

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const SLUG: &str = "interest-plaza";

#[tokio::main]
async fn main() -> Result<()> {
    let side: Value = Client::new().get(format!("{BASE_URL}/tags/{SLUG}/sidebar-links"))
        .send().await?.error_for_status()?.json().await?;
    println!("{} 的子标签:", side["source"]["name"]);
    for t in side["items"].as_array().unwrap_or(&vec![]) {
        println!("- {} ({})", t["name"], t["slug"]);
    }
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
SLUG = "interest-plaza"

side = requests.get(f"{BASE_URL}/tags/{SLUG}/sidebar-links").raise_for_status().json()
print(side["source"]["name"], "的子标签:")
for t in side["items"]:
    print("-", t["name"], "(" + t["slug"] + ")")
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const SLUG = "interest-plaza";

async function main() {
  const res = await fetch(`${BASE_URL}/tags/${SLUG}/sidebar-links`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const side = await res.json();
  console.log(side.source.name, "的子标签:");
  for (const t of side.items) console.log("-", t.name, `(${t.slug})`);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
