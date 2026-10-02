# 账户设置

## 文件存储配额

> 获取文件存储配额 `/api/v1/file-storage` GET **需要Cookie**

用于设置页展示当前用户已用的文件存储空间。

### 响应体

```json
{ "usedBytes": 0, "limitBytes": 20971520, "remainingBytes": 20971520 }
```

| KEY            | VALUE          | TYPE    |
| -------------- | -------------- | ------- |
| usedBytes      | 已用字节数     | Integer |
| limitBytes     | 总配额字节数   | Integer |
| remainingBytes | 剩余可用字节数 | Integer |

> 观测到的默认配额为 `20971520` 字节（20 MiB）。

## 预设头像列表

> 获取预设头像列表 `/api/v1/avatar-presets` GET

返回可供选择的预设头像。

### 响应体

```json
{
  "items": [
    { "type": "PRESET", "id": 1, "url": "/api/v1/avatars/1?v=f558..." },
    { "type": "PRESET", "id": 2, "url": "/api/v1/avatars/2?v=fed2..." }
  ]
}
```

| KEY  | VALUE                  | TYPE    |
| ---- | ---------------------- | ------- |
| type | 头像类型，固定 `PRESET` | String  |
| id   | 预设编号（1~8）        | Integer |
| url  | 头像地址，带内容哈希   | String  |

## 我的书签

> 获取我的书签 `/api/v1/bookmarks` GET **需要Cookie**

### Query

| KEY   | 观测值 | 说明     |
| ----- | ------ | -------- |
| limit | `20`   | 每页数量 |

### 响应体

```json
{ "items": [], "pageInfo": { "hasNextPage": false, "nextCursor": null } }
```

## 值得注意的

- 预设头像列表与具体用户无关，可不带 Cookie 访问。
- 文件存储、书签等接口作用于当前登录用户，均需要 Cookie。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";

async fn get(client: &Client, path: &str) -> Result<Value> {
    Ok(client.get(format!("{BASE_URL}{path}"))
        .send().await?.error_for_status()?.json().await?)
}

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 先登录 (见《登录》)
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": "xxxx@gmail.com", "password": "P@ssW0rd123" }))
        .send().await?.error_for_status()?;

    // 文件存储配额
    let storage = get(&client, "/file-storage").await?;
    println!("已用 {}/{} 字节", storage["usedBytes"], storage["limitBytes"]);

    // 预设头像列表
    let presets = get(&client, "/avatar-presets").await?;
    println!("预设头像数: {}", presets["items"].as_array().map_or(0, Vec::len));

    // 我的书签
    let bookmarks = get(&client, "/bookmarks?limit=20").await?;
    println!("书签数: {}", bookmarks["items"].as_array().map_or(0, Vec::len));

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

    # 文件存储配额
    storage = s.get(f"{BASE_URL}/file-storage").raise_for_status().json()
    print("已用", storage["usedBytes"], "/", storage["limitBytes"], "字节")

    # 预设头像列表
    presets = s.get(f"{BASE_URL}/avatar-presets").raise_for_status().json()
    print("预设头像数:", len(presets["items"]))

    # 我的书签
    bookmarks = s.get(f"{BASE_URL}/bookmarks", params={"limit": 20}).raise_for_status().json()
    print("书签数:", len(bookmarks["items"]))
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

  const storage = await (await request("/file-storage")).json();
  console.log("已用", storage.usedBytes, "/", storage.limitBytes, "字节");

  const presets = await (await request("/avatar-presets")).json();
  console.log("预设头像数:", presets.items.length);

  const bookmarks = await (await request("/bookmarks?limit=20")).json();
  console.log("书签数:", bookmarks.items.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
