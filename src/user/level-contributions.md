# 用户贡献日历

> 获取用户贡献日历 `/api/v1/users/{userId}/level-contributions/{year}` GET

## 响应体

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

| KEY                                   | VALUE                     | TYPE      |
| ------------------------------------- | ------------------------- | --------- |
| year                                  | 年份                      | Integer   |
| timeZone                              | 统计时区（如 `Asia/Shanghai`） | String |
| days                                  | 每日贡献，只返回有记录的日子 | ArrayList |
| days[].date                           | 日期 `YYYY-MM-DD`         | String    |
| days[].ability / responsibility / care | 能力/责任/关怀三种贡献分 | Integer   |
| updating                              | 是否正在重新计算          | Boolean   |
| calculatedAt                          | 计算时间                  | DateTime  |

## 值得注意的

- `days` 为空数组是正常情况（如该年无贡献记录）。
- 当前用户的贡献日历（省略 `{userId}`）见[当前用户贡献日历](./my-level-contributions.md)。

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
    let contrib: Value = Client::new()
        .get(format!("{BASE_URL}/users/{USER_ID}/level-contributions/2026"))
        .send().await?.error_for_status()?.json().await?;
    println!("有贡献的天数: {}", contrib["days"].as_array().map_or(0, Vec::len));
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"

contrib = requests.get(f"{BASE_URL}/users/{USER_ID}/level-contributions/2026").raise_for_status().json()
print("有贡献的天数:", len(contrib["days"]))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195";

async function main() {
  const res = await fetch(`${BASE_URL}/users/${USER_ID}/level-contributions/2026`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const contrib = await res.json();
  console.log("有贡献的天数:", contrib.days.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
