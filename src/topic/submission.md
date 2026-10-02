# 投稿审核

> 获取投稿审核列表 `/api/v1/post-submissions` GET **需要Cookie**

版务使用的审核队列，需要相应权限。

### Query

| KEY         | 观测值         | 说明         |
| ----------- | -------------- | ------------ |
| contentRole | `TOPIC_REPLY`  | 内容角色     |
| status      | `PENDING`      | 审核状态     |
| topicId     | 目标主题UUID   | 指定主题     |
| limit       | `100`          | 每页数量     |

### 响应体

```json
{ "items": [], "pageInfo": { "hasNextPage": false, "nextCursor": null } }
```

| KEY      | VALUE        | TYPE      |
| -------- | ------------ | --------- |
| items    | 待审核投稿   | ArrayList |
| pageInfo | 分页信息     | Object    |

## 值得注意的

- 该接口面向版务，普通用户调用可能返回空列表或权限错误。
- 实测队列为空（`items: []`），具体投稿项结构尚未验证。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const TOPIC_ID: &str = "01a0eb91-5d11-7fb0-b998-179add93620f";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 先登录 (见《登录》)
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": "xxxx@gmail.com", "password": "P@ssW0rd123" }))
        .send().await?.error_for_status()?;

    let subs: Value = client
        .get(format!(
            "{BASE_URL}/post-submissions?contentRole=TOPIC_REPLY&status=PENDING&topicId={TOPIC_ID}&limit=100"
        ))
        .send().await?.error_for_status()?.json().await?;

    println!("待审核: {}", subs["items"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
TOPIC_ID = "01a0eb91-5d11-7fb0-b998-179add93620f"

with requests.Session() as s:
    # 先登录 (见《登录》)
    s.post(f"{BASE_URL}/session",
           json={"username": "xxxx@gmail.com", "password": "P@ssW0rd123"}).raise_for_status()

    subs = s.get(f"{BASE_URL}/post-submissions", params={
        "contentRole": "TOPIC_REPLY", "status": "PENDING",
        "topicId": TOPIC_ID, "limit": 100,
    }).raise_for_status().json()

    print("待审核:", len(subs["items"]))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const TOPIC_ID = "01a0eb91-5d11-7fb0-b998-179add93620f";
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
    `/post-submissions?contentRole=TOPIC_REPLY&status=PENDING&topicId=${TOPIC_ID}&limit=100`
  )).json();
  console.log("待审核:", subs.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
