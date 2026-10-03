# 预设头像列表

> 获取预设头像列表 `/api/v1/avatar-presets` GET

返回可供选择的预设头像。

## 响应体

```json
{
  "items": [
    { "type": "PRESET", "id": 1, "url": "/api/v1/avatars/1?v=f558..." },
    { "type": "PRESET", "id": 2, "url": "/api/v1/avatars/2?v=fed2..." }
  ]
}
```

| KEY  | VALUE                   | TYPE    |
| ---- | ----------------------- | ------- |
| type | 头像类型，固定 `PRESET` | String  |
| id   | 预设编号（1~8）         | Integer |
| url  | 头像地址，带内容哈希    | String  |

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let presets: Value = Client::new().get(format!("{BASE_URL}/avatar-presets"))
        .send().await?.error_for_status()?.json().await?;
    println!("预设头像数: {}", presets["items"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

presets = requests.get(f"{BASE_URL}/avatar-presets").raise_for_status().json()
print("预设头像数:", len(presets["items"]))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";

async function main() {
  const res = await fetch(`${BASE_URL}/avatar-presets`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const presets = await res.json();
  console.log("预设头像数:", presets.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
