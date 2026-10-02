# 分区标签

## 获取全部分区标签

> 获取全部分区标签 `/api/v1/tags` GET

### 响应体

```json
{
  "items": [
    { "id": "01a0ab26-84a8-718b-996a-36be3dda4fa4", "slug": "creative-works", "name": "创作与作品", "description": "作品发布、试玩反馈、开发日志与作品复盘" },
    { "id": "01a0ab26-...-3960a4789d05", "slug": "learning-technology", "name": "学习与技术", "description": "教程、知识分享与技术讨论" },
    { "id": "01a0ab26-...-3cce5e3bb015", "slug": "q-and-a", "name": "你问我答", "description": "技术求助、作品调试与问题交流" },
    { "id": "01a0ab26-...-42a29388f3fa", "slug": "events-competitions", "name": "活动与赛事", "description": "官方活动、社区赛事与赛后复盘" },
    { "id": "01a0ab26-...-4536506db3ba", "slug": "interest-plaza", "name": "兴趣广场", "description": "绘画、音乐、动画、生活交流与普通闲聊" },
    { "id": "01a0e6c6-...-f57cda4c985e", "slug": "box", "name": "神奇代码岛", "description": "神奇代码岛岛民专属交流区……" },
    { "id": "01a0e835-...-6bebe7ba21c9", "slug": "neko", "name": "KittenN创作", "description": "KittenN 专属交流阵地……" },
    { "id": "01a0e838-...-ca17bf6e8d22", "slug": "coconut", "name": "CoCo应用创作", "description": "CoCo专属交流区……" },
    { "id": "01a0e83b-...-e3b033e02a5f", "slug": "python", "name": "Python乐园", "description": "Python内容聚集地……" }
  ]
}
```

| KEY         | VALUE                    | TYPE          |
| ----------- | ------------------------ | ------------- |
| id          | 标签UUID                 | String        |
| slug        | 标签标识，用于过滤与路由 | String        |
| name        | 标签名称                 | String        |
| description | 标签描述                 | String/Option |

## 获取分区侧边子标签

> 获取分区侧边子标签 `/api/v1/tags/{slug}/sidebar-links` GET

### 响应体

```json
{
  "source": { "id": "...", "slug": "interest-plaza", "name": "兴趣广场", "description": "..." },
  "items": [ { "...": "该分区下的子标签，结构同上" } ]
}
```

| KEY    | VALUE            | TYPE      |
| ------ | ---------------- | --------- |
| source | 当前分区标签     | Object    |
| items  | 侧边栏子标签列表 | ArrayList |

## 值得注意的

- 全站共 9 个分区，`slug` 即[主题列表](./topic/list.md#主题列表)过滤时 `tag` 参数的值。
- `interest-plaza` 等分区下的子标签会通过 `sidebar-links` 单独返回。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;
use serde_json::Value;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const SLUG: &str = "interest-plaza";

#[tokio::main]
async fn main() -> Result<()> {
    let client = Client::new();

    // 全部分区
    let tags: Value = client.get(format!("{BASE_URL}/tags"))
        .send().await?.error_for_status()?.json().await?;
    for t in tags["items"].as_array().unwrap_or(&vec![]) {
        println!("{} ({})", t["name"], t["slug"]);
    }

    // 某个分区的侧边子标签
    let side: Value = client.get(format!("{BASE_URL}/tags/{SLUG}/sidebar-links"))
        .send().await?.error_for_status()?.json().await?;
    println!("{} 的子标签:", side["source"]["name"]);
    for t in side["items"].as_array().unwrap_or(&vec![]) {
        println!("- {} ({})", t["name"], t["slug"]);
    }
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
SLUG = "interest-plaza"

with requests.Session() as s:
    # 全部分区
    tags = s.get(f"{BASE_URL}/tags").raise_for_status().json()
    for t in tags["items"]:
        print(t["name"], "(" + t["slug"] + ")")

    # 某个分区的侧边子标签
    side = s.get(f"{BASE_URL}/tags/{SLUG}/sidebar-links").raise_for_status().json()
    print(side["source"]["name"], "的子标签:")
    for t in side["items"]:
        print("-", t["name"], "(" + t["slug"] + ")")
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const SLUG = "interest-plaza";

async function get(path: string): Promise<any> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

async function main() {
  const tags = await get("/tags");
  for (const t of tags.items) console.log(t.name, `(${t.slug})`);

  const side = await get(`/tags/${SLUG}/sidebar-links`);
  console.log(side.source.name, "的子标签:");
  for (const t of side.items) console.log("-", t.name, `(${t.slug})`);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
