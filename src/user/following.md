# 关注列表

> 获取关注列表 `/api/v1/users/{userId}/following` GET

## Query

| KEY    | 观测值 | 说明                 |
| ------ | ------ | -------------------- |
| limit  | `50`   | 每页数量             |
| cursor | —      | 游标，取下一页时回传 |

## 响应体

```json
{
  "items": [
    {
      "user": {
        "id": "01a0fba5-06a4-7518-b863-cebb1ed0de30",
        "username": "example-user",
        "avatar": { "type": "PRESET", "id": 7, "url": "/api/v1/avatars/7?v=..." }
      },
      "followedAt": "2026-11-05T13:09:04.442Z"
    }
  ],
  "pageInfo": { "hasNextPage": false, "nextCursor": null }
}
```

| KEY              | VALUE              | TYPE     |
| ---------------- | ------------------ | -------- |
| items            | 用户列表           | ArrayList |
| items[].user     | 精简用户对象（id/username/avatar） | Object |
| items[].followedAt | 关注发生时间      | DateTime |
| pageInfo         | 分页信息           | Object   |

## 值得注意的

- 是否可见受用户资料中的 `showFollowingList` 控制。
- `items` 可能为空数组；`cursor` 用于取下一页。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://pickcat.dao3.fun/api/v1";
const USER_ID: &str = "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445";

#[tokio::main]
async fn main() -> Result<()> {
    let following: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/following?limit=50"))
        .send().await?.error_for_status()?.json().await?;
    println!("关注: {}", following["items"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import requests

BASE_URL = "https://pickcat.dao3.fun/api/v1"
USER_ID = "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445"

following = requests.get(f"{BASE_URL}/users/{USER_ID}/following",
                         params={"limit": 50}).raise_for_status().json()
print("关注:", len(following["items"]))
```
```typescript
const BASE_URL = "https://pickcat.dao3.fun/api/v1";
const USER_ID = "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/following?limit=50`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const following = await res.json();
  console.log("关注:", following.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
