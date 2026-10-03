# 用户资料

> 获取用户资料 `/api/v1/users/{userId}` GET

用于个人主页，返回用户基础信息、统计以及当前访问者与 TA 的关系。

## 响应体

```json
{
  "id": "01a0fbca-eee1-70ad-a00d-a1ed4c89b195",
  "username": "CarbonPremium",
  "avatar": { "type": "PRESET", "id": 1, "url": "/api/v1/avatars/1?v=f558..." },
  "bio": null,
  "region": null,
  "showFollowingList": true,
  "showFollowersList": true,
  "createdAt": "2026-10-02T08:46:15.771Z",
  "level": { "current": 1 },
  "stats": { "followers": 0, "following": 0, "topics": 0, "replies": 0 },
  "viewerState": { "following": false, "canFollow": false }
}
```

| KEY               | VALUE                  | TYPE          |
| ----------------- | ---------------------- | ------------- |
| id                | 用户UUID               | String        |
| username          | 用户昵称               | String        |
| avatar            | 头像                   | Object        |
| bio               | 个人简介，可为 null    | String/Option |
| region            | 地区，可为 null        | String/Option |
| showFollowingList | 是否公开「关注」列表   | Boolean       |
| showFollowersList | 是否公开「粉丝」列表   | Boolean       |
| createdAt         | 账户创建时间           | DateTime      |
| level.current     | 当前等级               | Integer       |
| stats             | 关注/粉丝/主题/回帖计数 | Object       |
| viewerState       | 当前访问者与用户的关系 | Object        |

> `avatar.type` 为 `PRESET` 时，`id` 是预设头像编号，`url` 带 `?v=<内容哈希>`；为 `CUSTOM` 时，`id` 是自定义头像的 `fileId`，`url` 形如 `/api/v1/avatars/{fileId}`。
>
> `viewerState.following` 表示当前访问者是否已关注该用户；`canFollow` 表示是否允许关注（自己不能关注自己）。

## 值得注意的

- 不携带 Cookie 也可访问；携带时会返回与访问者的关注关系。
- 修改资料见[修改个人资料](./profile-edit.md)；关注/粉丝列表见[关注列表](./following.md)、[粉丝列表](./followers.md)。

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
    let user: Value = Client::new().get(format!("{BASE_URL}/users/{USER_ID}"))
        .send().await?.error_for_status()?.json().await?;

    println!("{} Lv.{}", user["username"], user["level"]["current"]);
    println!("主题 {} / 回帖 {}", user["stats"]["topics"], user["stats"]["replies"]);
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

user = requests.get(f"{BASE_URL}/users/{USER_ID}").raise_for_status().json()
print(user["username"], "Lv." + str(user["level"]["current"]))
print("主题", user["stats"]["topics"], "/ 回帖", user["stats"]["replies"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const user = await res.json();
  console.log(user.username, "Lv." + user.level.current);
  console.log("主题", user.stats.topics, "/ 回帖", user.stats.replies);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
