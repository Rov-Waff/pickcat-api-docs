# 粉丝列表

> 获取粉丝列表 `/api/v1/users/{userId}/followers` GET

## Query

| KEY    | 观测值 | 说明                 |
| ------ | ------ | -------------------- |
| limit  | `50`   | 每页数量             |
| cursor | —      | 游标，取下一页时回传 |

## 响应体

```json
{ "items": [], "pageInfo": { "hasNextPage": false, "nextCursor": null } }
```

| KEY      | VALUE      | TYPE      |
| -------- | ---------- | --------- |
| items    | 用户列表项 | ArrayList |
| pageInfo | 分页信息   | Object    |

## 值得注意的

- 是否可见受用户资料中的 `showFollowersList` 控制。
- 本次抓包列表为空，`items` 的具体字段尚未验证（推测为精简用户对象）。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USER_ID: &str = "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445";

#[tokio::main]
async fn main() -> Result<()> {
    let followers: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/followers?limit=50"))
        .send().await?.error_for_status()?.json().await?;
    println!("粉丝: {}", followers["items"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445"

followers = requests.get(f"{BASE_URL}/users/{USER_ID}/followers",
                         params={"limit": 50}).raise_for_status().json()
print("粉丝:", len(followers["items"]))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/followers?limit=50`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const followers = await res.json();
  console.log("粉丝:", followers.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
