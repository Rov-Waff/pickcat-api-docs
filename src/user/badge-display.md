# 徽章展示设置

> 获取徽章展示设置 `/api/v1/users/{userId}/badge-display` GET

返回用户选择展示哪个徽章的策略。

## 响应体

```json
{ "mode": "AUTO_LATEST", "badgeId": null, "displayedBadge": null }
```

| KEY            | VALUE                         | TYPE          |
| -------------- | ----------------------------- | ------------- |
| mode           | 展示模式，如 `AUTO_LATEST`    | String        |
| badgeId        | 指定展示的徽章ID，可为 null   | String/Option |
| displayedBadge | 当前实际展示的徽章，可为 null | Object/Option |

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
    let display: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/badge-display"))
        .send().await?.error_for_status()?.json().await?;
    println!("展示模式: {}", display["mode"]);
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

display = requests.get(f"{BASE_URL}/users/{USER_ID}/badge-display").raise_for_status().json()
print("展示模式:", display["mode"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/badge-display`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const display = await res.json();
  console.log("展示模式:", display.mode);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
