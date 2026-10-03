# 用户获得的徽章

> 获取用户获得的徽章 `/api/v1/users/{userId}/badges` GET

返回该用户获得的所有徽章。

## 响应体

```json
{
  "items": [
    {
      "userId": "01a0c957-53a6-798f-bf2a-2a83c94280d0",
      "badgeId": "badge_pioneer",
      "grantedAt": "2026-09-23T13:48:39.720Z",
      "revision": "013d6b44-6077-4834-aab2-0bbc80a96195",
      "badge": {
        "id": "badge_pioneer",
        "slug": "badge_pioneer",
        "name": "开拓者",
        "description": "参与Pickcat社区第一次内测",
        "icon": "trophy",
        "version": 4,
        "image": {
          "fileId": "01a0b34f-c685-7777-b60d-fe2a6adb6f52",
          "url": "/api/v1/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52",
          "width": 512, "height": 512
        }
      }
    }
  ]
}
```

| KEY       | VALUE            | TYPE     |
| --------- | ---------------- | -------- |
| userId    | 用户UUID         | String   |
| badgeId   | 徽章ID           | String   |
| grantedAt | 获得时间         | DateTime |
| revision  | 授予记录版本UUID | String   |
| badge     | 徽章详情         | Object   |

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USER_ID: &str = "01a0c957-53a6-798f-bf2a-2a83c94280d0";

#[tokio::main]
async fn main() -> Result<()> {
    let badges: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/badges"))
        .send().await?.error_for_status()?.json().await?;
    for b in badges["items"].as_array().unwrap_or(&vec![]) {
        println!("{} ({})", b["badge"]["name"], b["grantedAt"]);
    }
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0c957-53a6-798f-bf2a-2a83c94280d0"

badges = requests.get(f"{BASE_URL}/users/{USER_ID}/badges").raise_for_status().json()
for b in badges["items"]:
    print(b["badge"]["name"], "(" + b["grantedAt"] + ")")
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0c957-53a6-798f-bf2a-2a83c94280d0";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/badges`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const badges = await res.json();
  for (const b of badges.items) console.log(b.badge.name, `(${b.grantedAt})`);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
