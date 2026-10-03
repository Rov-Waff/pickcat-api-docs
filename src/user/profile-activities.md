# 用户动态

> 获取用户动态 `/api/v1/users/{userId}/profile-activities` GET

## Query

| KEY   | 观测值 | 说明     |
| ----- | ------ | -------- |
| year  | `2026` | 年份     |
| limit | `50`   | 每页数量 |

## 响应体

```json
{
  "items": [
    { "id": "...", "kind": "POSTED", "occurredAt": "2026-09-27T05:09:55.600Z", "title": "做了一个联机小测试，欢迎大家体验", "level": null },
    { "id": "...", "kind": "LIKED",  "occurredAt": "2026-09-26T05:24:34.925Z", "title": "Q&A | 关于pickCat……", "level": null },
    { "id": "...", "kind": "LEVEL_UP", "occurredAt": "2026-09-22T13:39:43.876Z", "title": null, "level": 1 }
  ],
  "pageInfo": { "hasNextPage": false, "nextCursor": null }
}
```

| KEY        | VALUE                                 | TYPE           |
| ---------- | ------------------------------------- | -------------- |
| id         | 动态UUID                              | String         |
| kind       | `POSTED`/`LIKED`/`LEVEL_UP`           | String         |
| occurredAt | 发生时间                              | DateTime       |
| title      | 关联帖子标题，升级类动态为 null       | String/Option  |
| level      | 升级后的等级，仅 `LEVEL_UP` 时非 null | Integer/Option |

## 值得注意的

- 当前用户的动态（省略 `{userId}`）见[当前用户动态](./my-profile-activities.md)。

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
    let acts: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/profile-activities?year=2026&limit=50"))
        .send().await?.error_for_status()?.json().await?;
    for a in acts["items"].as_array().unwrap_or(&vec![]) {
        println!("{} {}", a["kind"], a["occurredAt"]);
    }
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

acts = requests.get(f"{BASE_URL}/users/{USER_ID}/profile-activities",
                    params={"year": 2026, "limit": 50}).raise_for_status().json()
for a in acts["items"]:
    print(a["kind"], a["occurredAt"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/profile-activities?year=2026&limit=50`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const acts = await res.json();
  for (const a of acts.items) console.log(a.kind, a.occurredAt);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
