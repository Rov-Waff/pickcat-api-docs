# 等级进度

> 获取等级进度 `/api/v1/level-progress` GET **需要Cookie**

等级页核心接口，含当前分数、熟悉度、下一级要求与各项操作配额。

## 响应体

```json
{
  "currentLevel": 1,
  "promotionCeiling": null,
  "scores": { "ability": 0, "responsibility": 0, "care": 0 },
  "familiarity": {
    "tracking": true, "familiarityStartedAt": "2026-10-02T08:47:49.552Z",
    "daysSinceEntranceExam": 0, "validVisitDays": 0,
    "topicsEntered": 1, "postsRead": 16, "effectiveReadingSeconds": 3
  },
  "nextLevel": {
    "level": 2, "admission": "LEVEL_REQUIREMENTS",
    "scores": {
      "ability": { "current": 0, "required": 100, "met": false },
      "responsibility": { "current": 0, "required": 60, "met": false },
      "care": { "current": 0, "required": 100, "met": false }
    },
    "familiarity": {
      "daysSinceEntranceExam": { "current": 0, "required": 30, "met": false },
      "validVisitDays": { "current": 0, "required": 20, "met": false },
      "topicsEntered": { "current": 1, "required": 100, "met": false },
      "postsRead": { "current": 16, "required": 800, "met": false },
      "effectiveReadingSeconds": { "current": 3, "required": 43200, "met": false }
    },
    "hardRequirements": [
      { "key": "NO_ACTIVE_PENALTY", "met": true },
      { "key": "NO_CONFIRMED_VIOLATION_90_DAYS", "met": true }
    ],
    "blockedByPromotionCeiling": false, "eligible": false
  },
  "lv4Candidate": false,
  "quotas": [
    { "action": "TOPIC_CREATE", "limit": 10, "used": 0, "remaining": 10 },
    { "action": "QUESTION_CREATE", "limit": 5, "used": 0, "remaining": 5 },
    { "action": "REPLY_CREATE", "limit": 50, "used": 0, "remaining": 50 },
    { "action": "LIKE_CREATE", "limit": 50, "used": 0, "remaining": 50 },
    { "action": "BOOKMARK_CREATE", "limit": 40, "used": 0, "remaining": 40 },
    { "action": "REPORT_CREATE", "limit": 20, "used": 0, "remaining": 20 },
    { "action": "DUPLICATE_REQUEST_CREATE", "limit": 10, "used": 0, "remaining": 10 },
    { "action": "BOT_REQUEST", "limit": 5, "used": 0, "remaining": 5 }
  ],
  "updating": false,
  "calculatedAt": "2026-10-02T08:49:43.287Z"
}
```

| KEY                        | VALUE                                          | TYPE          |
| -------------------------- | ---------------------------------------------- | ------------- |
| currentLevel               | 当前等级                                       | Integer       |
| scores                     | 能力 / 责任 / 关怀 得分                        | Object        |
| familiarity                | 社区熟悉度指标                                 | Object        |
| nextLevel                  | 升级要求；已满级时可能为 null                  | Object/Option |
| nextLevel.hardRequirements | 硬性门槛（如无处罚、90 天无违规）              | ArrayList     |
| nextLevel.eligible         | 是否满足全部升级条件                           | Boolean       |
| lv4Candidate               | 是否 Lv.4 候选                                 | Boolean       |
| quotas                     | 各类操作配额（创建主题/回帖/点赞/收藏/举报等） | ArrayList     |
| updating                   | 是否正在重新计算                               | Boolean       |

## 值得注意的

- 等级体系由 **能力 / 责任 / 关怀** 三维得分叠加 **社区熟悉度** 共同决定，并受硬性门槛限制。
- 阅读埋点（见[阅读会话](../reading-session.md)）会折算成 `effectiveReadingSeconds`、`postsRead` 等熟悉度指标。

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

    let progress: Value = client.get(format!("{BASE_URL}/level-progress"))
        .send().await?.error_for_status()?.json().await?;

    println!("当前等级: Lv.{}", progress["currentLevel"]);
    println!("下一级可升级: {}", progress["nextLevel"]["eligible"]);
    println!("配额项数: {}", progress["quotas"].as_array().map_or(0, Vec::len));
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

    progress = s.get(f"{BASE_URL}/level-progress").raise_for_status().json()
    print("当前等级: Lv.", progress["currentLevel"])
    print("下一级可升级:", progress["nextLevel"]["eligible"])
    print("配额项数:", len(progress["quotas"]))
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

  const progress = await (await request("/level-progress")).json();
  console.log("当前等级: Lv." + progress.currentLevel);
  console.log("下一级可升级:", progress.nextLevel.eligible);
  console.log("配额项数:", progress.quotas.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
