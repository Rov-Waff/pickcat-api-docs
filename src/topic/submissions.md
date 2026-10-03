# 投稿审核列表

> 获取投稿审核列表 `/api/v1/post-submissions` GET **需要Cookie**

既用于版务的审核队列，也用于个人主页查看自己的待审投稿。

## Query

| KEY         | 观测值                             | 说明                       |
| ----------- | ---------------------------------- | -------------------------- |
| contentRole | `TOPIC_REPLY` / `TOPIC_FIRST_POST` | 内容角色（回帖 / 主题首楼）|
| status      | `PENDING` / `REJECTED`             | 审核状态筛选               |
| topicId     | 目标主题UUID                       | 可选，按主题过滤           |
| limit       | `100` / `20`                       | 每页数量                   |

## 响应体

```json
{
  "items": [
    {
      "id": "01a0ff25-1f05-7f09-8d1b-a32e2b0bab00",
      "status": "PENDING_PROVIDER",
      "contentRole": "TOPIC_FIRST_POST",
      "request": { "kind": "DISCUSSION", "title": "...", "tagIds": ["..."], "markdown": "..." },
      "riskLevel": null,
      "topicId": "01a0ff25-1f07-77f3-beb8-0dabe6dba5f3",
      "postId": "01a0ff25-1f0a-7ec1-890d-86612754c302",
      "postNumber": 1,
      "baseRevision": null,
      "createdAt": "...", "updatedAt": "..."
    }
  ],
  "pageInfo": { "hasNextPage": false, "nextCursor": null }
}
```

| KEY                          | VALUE                             | TYPE          |
| ---------------------------- | --------------------------------- | ------------- |
| id                           | 审核记录UUID                      | String        |
| status                       | 审核状态，如 `PENDING_PROVIDER`   | String        |
| contentRole                  | 内容角色                          | String        |
| request                      | 提交内容原样回显（含 `markdown`） | Object        |
| riskLevel                    | 风险等级，可为 null               | String/Option |
| topicId / postId / postNumber| 预生成的定位信息                  | String/Integer|
| baseRevision                 | 基线版本，可为 null               | String/Option |
| createdAt / updatedAt        | 创建/更新时间                     | DateTime      |

## 值得注意的

- `request` 随 `contentRole` 变化：主题首楼含 `title`/`kind`/`tagIds`/`markdown`，回帖含 `topicId`/`markdown`/`replyToPostNumber`。
- `status` 观测到 `PENDING`、`PENDING_PROVIDER`（送第三方审核中）、`REJECTED`；推测还有 `APPROVED` 等终态。
- 审核期间主题尚未对他人可见。单条详情见[投稿详情](./submission-detail.md)。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 先登录 (见《登录》)
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": "xxxx@gmail.com", "password": "P@ssW0rd123" }))
        .send().await?.error_for_status()?;

    let subs: Value = client
        .get(format!("{BASE_URL}/post-submissions?contentRole=TOPIC_REPLY&status=PENDING&limit=100"))
        .send().await?.error_for_status()?.json().await?;

    println!("待审核: {}", subs["items"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

with requests.Session() as s:
    # 先登录 (见《登录》)
    s.post(f"{BASE_URL}/session",
           json={"username": "xxxx@gmail.com", "password": "P@ssW0rd123"}).raise_for_status()

    subs = s.get(f"{BASE_URL}/post-submissions",
                 params={"contentRole": "TOPIC_REPLY", "status": "PENDING", "limit": 100}
                 ).raise_for_status().json()
    print("待审核:", len(subs["items"]))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
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

  const subs = await (await request(
    "/post-submissions?contentRole=TOPIC_REPLY&status=PENDING&limit=100"
  )).json();
  console.log("待审核:", subs.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
