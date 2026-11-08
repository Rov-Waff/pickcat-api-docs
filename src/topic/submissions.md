# 投稿审核列表

> 获取投稿审核列表 `/api/v1/post-submissions` GET **需要Cookie**

既用于版务的审核队列，也用于个人主页查看自己的待审投稿。

## Query

| KEY         | 观测值                                                       | 说明                                        |
| ----------- | ------------------------------------------------------------ | ------------------------------------------- |
| contentRole | `TOPIC_FIRST_POST` / `TOPIC_REPLY` / `WORK_COMMENT`          | **必填**，内容角色（主题首楼 / 回帖 / 作品评论） |
| status      | `PENDING` / `REJECTED`                                       | **必填**，审核状态筛选                      |
| topicId     | 目标主题UUID                                                 | 可选，按主题过滤                            |
| limit       | `100` / `20`                                                 | 每页数量                                    |

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

- `contentRole` 与 `status` 均为**必填**，缺失时返回 `400 VALIDATION_FAILED`。
- `contentRole` 实测枚举还包含 `WORK_COMMENT`（作品评论）。
- `request` 随 `contentRole` 变化：主题首楼含 `title`/`kind`/`tagIds`/`markdown`，回帖含 `topicId`/`markdown`/`replyToPostNumber`。
- `status` 观测到 `PENDING`、`PENDING_PROVIDER`（送第三方审核中）、`REJECTED`；推测还有 `APPROVED` 等终态。
- 审核期间主题尚未对他人可见。单条详情见[投稿详情](./submission-detail.md)。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::Value;
use std::sync::Arc;

const BASE_URL: &str = "https://pickcat.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 复用浏览器中已登录的 Cookie（见《登录》的 CAPTCHA 说明）
    let session_cookie = std::env::var("PICKCAT_SESSION").expect("请先设置 PICKCAT_SESSION");
    jar.add_cookie_str(&format!("pickcat_session={session_cookie}"), &BASE_URL.parse()?);

    let subs: Value = client
        .get(format!("{BASE_URL}/post-submissions?contentRole=TOPIC_REPLY&status=PENDING&limit=100"))
        .send().await?.error_for_status()?.json().await?;

    println!("待审核: {}", subs["items"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import os
import requests

BASE_URL = "https://pickcat.dao3.fun/api/v1"

with requests.Session() as s:
    # 复用浏览器中已登录的 Cookie（见《登录》的 CAPTCHA 说明）
    s.headers["Cookie"] = f"pickcat_session={os.environ['PICKCAT_SESSION']}"

    subs = s.get(f"{BASE_URL}/post-submissions",
                 params={"contentRole": "TOPIC_REPLY", "status": "PENDING", "limit": 100}
                 ).raise_for_status().json()
    print("待审核:", len(subs["items"]))
```
```typescript
const BASE_URL = "https://pickcat.dao3.fun/api/v1";
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
  // 复用浏览器中已登录的 Cookie（见《登录》的 CAPTCHA 说明）
  const pickcatSession = process.env.PICKCAT_SESSION;
  if (!pickcatSession) throw new Error("请先设置 PICKCAT_SESSION");
  jar.set("pickcat_session", pickcatSession);

  const subs = await (await request(
    "/post-submissions?contentRole=TOPIC_REPLY&status=PENDING&limit=100"
  )).json();
  console.log("待审核:", subs.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
