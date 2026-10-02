# 用户动态与贡献

## 用户动态(公开)

> 获取用户动态 `/api/v1/users/{userId}/profile-activities` GET

### Query

| KEY   | 观测值 | 说明     |
| ----- | ------ | -------- |
| year  | `2026` | 年份     |
| limit | `50`   | 每页数量 |

### 响应体

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

| KEY        | VALUE                                   | TYPE          |
| ---------- | --------------------------------------- | ------------- |
| id         | 动态UUID                                | String        |
| kind       | `POSTED`/`LIKED`/`LEVEL_UP`             | String        |
| occurredAt | 发生时间                                | DateTime      |
| title      | 关联帖子标题，升级类动态为 null         | String/Option |
| level      | 升级后的等级，仅 `LEVEL_UP` 时非 null   | Integer/Option |

## 当前用户动态

> 获取当前用户动态 `/api/v1/profile-activities` GET **需要Cookie**

参数与响应结构同「用户动态(公开)」，只是省略了 `{userId}`，作用于当前登录用户。

## 用户贡献日历

> 获取用户贡献日历 `/api/v1/users/{userId}/level-contributions/{year}` GET

### 响应体

```json
{
  "year": 2026,
  "timeZone": "Asia/Shanghai",
  "days": [
    { "date": "2026-09-22", "ability": 1, "responsibility": 0, "care": 0 },
    { "date": "2026-09-23", "ability": 1, "responsibility": 0, "care": 0 }
  ],
  "updating": false,
  "calculatedAt": "2026-10-02T08:49:09.230Z"
}
```

| KEY          | VALUE                                 | TYPE     |
| ------------ | ------------------------------------- | -------- |
| year         | 年份                                  | Integer  |
| timeZone     | 统计时区（如 `Asia/Shanghai`）        | String   |
| days         | 每日贡献，只返回有记录的日子          | ArrayList |
| days[].date  | 日期 `YYYY-MM-DD`                     | String   |
| days[].ability / responsibility / care | 能力/责任/关怀三种贡献分 | Integer |
| updating     | 是否正在重新计算                      | Boolean  |
| calculatedAt | 计算时间                              | DateTime |

## 当前用户贡献日历

> 获取当前用户贡献日历 `/api/v1/level-contributions/{year}` GET **需要Cookie**

参数与响应结构同「用户贡献日历」，省略 `{userId}`，作用于当前登录用户。

## 值得注意的

- `year` 也可作为路径变量传给「贡献日历」，如 `/users/{id}/level-contributions/2025`、`2026`。
- `days` 为空数组是正常情况（如该年无贡献记录）。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USER_ID: &str = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async fn get(client: &Client, path: &str) -> Result<Value> {
    Ok(client.get(format!("{BASE_URL}{path}"))
        .send().await?.error_for_status()?.json().await?)
}

fn count_activities(v: &Value) -> usize {
    v["items"].as_array().map_or(0, Vec::len)
}

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 先登录 (见《登录》)
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": "xxxx@gmail.com", "password": "P@ssW0rd123" }))
        .send().await?.error_for_status()?;

    // 指定用户的动态 / 贡献日历
    let acts = get(&client, &format!("/users/{USER_ID}/profile-activities?year=2026&limit=50")).await?;
    let contrib = get(&client, &format!("/users/{USER_ID}/level-contributions/2026")).await?;
    println!("[TA] 动态 {} 条, 有贡献的天数 {}", count_activities(&acts),
             contrib["days"].as_array().map_or(0, Vec::len));

    // 当前用户的动态 / 贡献日历 (省略 userId)
    let my_acts = get(&client, "/profile-activities?year=2026&limit=50").await?;
    let my_contrib = get(&client, "/level-contributions/2026").await?;
    println!("[我] 动态 {} 条, 有贡献的天数 {}", count_activities(&my_acts),
             my_contrib["days"].as_array().map_or(0, Vec::len));

    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

with requests.Session() as s:
    # 先登录 (见《登录》)
    s.post(f"{BASE_URL}/session",
           json={"username": "xxxx@gmail.com", "password": "P@ssW0rd123"}).raise_for_status()

    # 指定用户的动态 / 贡献日历
    acts = s.get(f"{BASE_URL}/users/{USER_ID}/profile-activities",
                 params={"year": 2026, "limit": 50}).raise_for_status().json()
    contrib = s.get(f"{BASE_URL}/users/{USER_ID}/level-contributions/2026").raise_for_status().json()
    print("[TA] 动态", len(acts["items"]), "条, 有贡献的天数", len(contrib["days"]))

    # 当前用户的动态 / 贡献日历 (省略 userId)
    my_acts = s.get(f"{BASE_URL}/profile-activities",
                    params={"year": 2026, "limit": 50}).raise_for_status().json()
    my_contrib = s.get(f"{BASE_URL}/level-contributions/2026").raise_for_status().json()
    print("[我] 动态", len(my_acts["items"]), "条, 有贡献的天数", len(my_contrib["days"]))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";
const jar = new Map<string, string>();

function cookieHeader(): string {
  return [...jar].map(([k, v]) => `${k}=${v}`).join("; ");
}

async function request(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  const cookie = cookieHeader();
  if (cookie) headers.set("cookie", cookie);
  const res = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  for (const c of res.headers.getSetCookie?.() ?? []) {
    const [pair] = c.split(";");
    const i = pair.indexOf("=");
    if (i > 0) jar.set(pair.slice(0, i), pair.slice(i + 1));
  }
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res;
}

async function main() {
  // 先登录 (见《登录》)
  await request("/session", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username: "xxxx@gmail.com", password: "P@ssW0rd123" }),
  });

  // 指定用户的动态 / 贡献日历
  const acts = await (await request(`/users/${USER_ID}/profile-activities?year=2026&limit=50`)).json();
  const contrib = await (await request(`/users/${USER_ID}/level-contributions/2026`)).json();
  console.log("[TA] 动态", acts.items.length, "条, 有贡献的天数", contrib.days.length);

  // 当前用户的动态 / 贡献日历 (省略 userId)
  const myActs = await (await request("/profile-activities?year=2026&limit=50")).json();
  const myContrib = await (await request("/level-contributions/2026")).json();
  console.log("[我] 动态", myActs.items.length, "条, 有贡献的天数", myContrib.days.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
