# 首页推荐

> 获取首页推荐 `/api/v1/topic-recommendations` GET

## Query

| KEY   | 观测值        | 说明     |
| ----- | ------------- | -------- |
| sort  | `recommended` | 推荐排序 |
| limit | `20`          | 每页数量 |

## 响应体

```json
{
  "strategy": "PERSONALIZED",
  "items": [ { "...": "主题列表项，每个 item 额外带 reason 字段" } ],
  "pageInfo": {
    "hasNextPage": true,
    "nextCursor": "01a0fc20-11e8-7793-aeb0-5c029c04e0bb.19.AJy7Pzi0eUeQQuLx44dMv2YXqVSk1ro_bcY1vg1H5Go"
  }
}
```

| KEY                | VALUE                          | TYPE          |
| ------------------ | ------------------------------ | ------------- |
| strategy           | 推荐策略，如 `PERSONALIZED`    | String        |
| items              | 主题列表项，额外含 `reason`    | ArrayList     |
| items[].reason     | 推荐原因，`PINNED`/`TRENDING`  | String        |
| pageInfo.nextCursor| 游标，格式 `<最后一条ID>.<序号>.<签名>` | String/Option |

## 值得注意的

- 首页使用 `topic-recommendations` 替代普通 `/topics`，单次返回 20 条并用 `reason` 解释推荐原因。
- 分页统一为 `pageInfo.hasNextPage` / `pageInfo.nextCursor`，取下一页时把 `nextCursor` 作为 `cursor` 参数回传。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let client = Client::new();

    // 首页推荐
    let rec: Value = client
        .get(format!("{BASE_URL}/topic-recommendations?sort=recommended&limit=20"))
        .send().await?.error_for_status()?.json().await?;

    println!("策略: {}", rec["strategy"]);
    for t in rec["items"].as_array().unwrap_or(&vec![]) {
        println!("({}) {}", t["reason"], t["title"]);
    }

    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

with requests.Session() as s:
    # 首页推荐
    rec = s.get(f"{BASE_URL}/topic-recommendations",
                params={"sort": "recommended", "limit": 20}).raise_for_status().json()
    print("策略:", rec["strategy"])
    for t in rec["items"]:
        print(f'({t["reason"]})', t["title"])
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";

async function get(path: string): Promise<any> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

async function main() {
  // 首页推荐
  const rec = await get("/topic-recommendations?sort=recommended&limit=20");
  console.log("策略:", rec.strategy);
  for (const t of rec.items) console.log(`(${t.reason})`, t.title);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
