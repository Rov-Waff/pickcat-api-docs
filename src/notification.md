# 通知

> 获取通知汇总 `/api/v1/notification-summary` GET **需要Cookie**

首页轮询使用的未读通知汇总。

## 响应体

```json
{
  "unreadCount": 0,
  "unreadCountByType": {
    "REPLY_CREATED": 0,
    "MANAGEMENT_ACTION": 0,
    "POST_LIKED": 0,
    "TOPIC_EVENT": 0,
    "USER_FOLLOWED": 0,
    "LEVEL_CERTIFICATION": 0
  }
}
```

| KEY                                 | VALUE            | TYPE    |
| ----------------------------------- | ---------------- | ------- |
| unreadCount                         | 未读总数         | Integer |
| unreadCountByType                   | 按类型统计的未读数 | Object  |
| unreadCountByType.REPLY_CREATED     | 回复             | Integer |
| unreadCountByType.MANAGEMENT_ACTION | 管理操作         | Integer |
| unreadCountByType.POST_LIKED        | 帖子被赞         | Integer |
| unreadCountByType.TOPIC_EVENT       | 主题事件         | Integer |
| unreadCountByType.USER_FOLLOWED     | 新增关注         | Integer |
| unreadCountByType.LEVEL_CERTIFICATION | 等级认证       | Integer |

## 值得注意的

- 首页会**轮询**该接口刷新未读角标。
- 本次报告只捕获到汇总接口，通知列表 / 已读接口尚未记录。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{Map, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://pickcat.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 复用浏览器中已登录的 Cookie（见《登录》的 CAPTCHA 说明）
    let session_cookie = std::env::var("PICKCAT_SESSION").expect("请先设置 PICKCAT_SESSION");
    jar.add_cookie_str(&format!("pickcat_session={session_cookie}"), &BASE_URL.parse()?);

    let summary: Value = client.get(format!("{BASE_URL}/notification-summary"))
        .send().await?.error_for_status()?.json().await?;

    println!("未读总数: {}", summary["unreadCount"]);
    for (k, v) in summary["unreadCountByType"].as_object().unwrap_or(&Map::new()) {
        println!("  {k}: {v}");
    }
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

    summary = s.get(f"{BASE_URL}/notification-summary").raise_for_status().json()

    print("未读总数:", summary["unreadCount"])
    for kind, count in summary["unreadCountByType"].items():
        print(" ", kind + ":", count)
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

  const summary = await (await request("/notification-summary")).json();
  console.log("未读总数:", summary.unreadCount);
  for (const [kind, count] of Object.entries(summary.unreadCountByType)) {
    console.log(" ", kind + ":", count);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
