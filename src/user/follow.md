# 关注与粉丝

## 获取关注列表

> 获取关注列表 `/api/v1/users/{userId}/following` GET

## 获取粉丝列表

> 获取粉丝列表 `/api/v1/users/{userId}/followers` GET

两个接口结构一致，仅路径不同。

### Query

| KEY    | 观测值 | 说明                       |
| ------ | ------ | -------------------------- |
| limit  | `50`   | 每页数量                   |
| cursor | —      | 游标，取下一页时回传       |

### 响应体

```json
{ "items": [], "pageInfo": { "hasNextPage": false, "nextCursor": null } }
```

| KEY      | VALUE      | TYPE      |
| -------- | ---------- | --------- |
| items    | 用户列表项 | ArrayList |
| pageInfo | 分页信息   | Object    |

## 值得注意的

- 是否可见受用户资料中的 `showFollowingList` / `showFollowersList` 控制。
- 本次抓包两个列表均为空，`items` 的具体字段尚未验证（推测为精简用户对象）。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USER_ID: &str = "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445";

async fn get(client: &Client, path: &str) -> Result<Value> {
    Ok(client.get(format!("{BASE_URL}{path}"))
        .send().await?.error_for_status()?.json().await?)
}

#[tokio::main]
async fn main() -> Result<()> {
    let client = Client::new();
    let following = get(&client, &format!("/users/{USER_ID}/following?limit=50")).await?;
    let followers = get(&client, &format!("/users/{USER_ID}/followers?limit=50")).await?;

    println!("关注 {}", following["items"].as_array().map_or(0, Vec::len));
    println!("粉丝 {}", followers["items"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445"

with requests.Session() as s:
    following = s.get(f"{BASE_URL}/users/{USER_ID}/following",
                      params={"limit": 50}).raise_for_status().json()
    followers = s.get(f"{BASE_URL}/users/{USER_ID}/followers",
                      params={"limit": 50}).raise_for_status().json()

    print("关注", len(following["items"]))
    print("粉丝", len(followers["items"]))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445";

async function get(path: string): Promise<any> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

async function main() {
  const following = await get(`/users/${USER_ID}/following?limit=50`);
  const followers = await get(`/users/${USER_ID}/followers?limit=50`);
  console.log("关注", following.items.length);
  console.log("粉丝", followers.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
