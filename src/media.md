# 媒体资源

包括文件上传与读取，以及预设头像、表情等资源。这些资源在浏览器里多被归类为 `image`，但路径位于 `/api/v1` 下。

## 图片上传

> 上传图片 `/api/v1/files` POST **需要Cookie**

请求头需带 `Idempotency-Key`，`content-type` 为 `multipart/form-data`。

### 表单字段

| 字段      | 值         | 说明                             |
| --------- | ---------- | -------------------------------- |
| ownership | `PERSONAL` | 归属，推测还有帖子/主题归属等    |
| file      | 二进制     | 图片本体                         |

### 响应体

成功返回 `201 Created`，响应头 `location: /api/v1/files/{id}`：

```json
{
  "id": "01a0ff24-bc3f-7140-a78c-73f6b40137b0",
  "ownership": "PERSONAL",
  "uploadedByUserId": "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445"
}
```

| KEY              | VALUE      | TYPE   |
| ---------------- | ---------- | ------ |
| id               | 文件UUID   | String |
| ownership        | 归属       | String |
| uploadedByUserId | 上传者UUID | String |

## 我的文件列表

> 我的文件列表 `/api/v1/files` GET **需要Cookie**

### Query

| KEY   | 观测值   | 说明                             |
| ----- | -------- | -------------------------------- |
| scope | `OWN`    | 只看自己的文件                   |
| state | `READY`  | 只看已就绪（上传完成）的文件     |

### 响应体

```json
{ "pageInfo": { "hasNextPage": false, "nextCursor": null }, "items": [] }
```

## 获取文件

> 获取文件 `/api/v1/files/{fileId}` GET

帖子图片、徽章图片等都通过该接口读取。

## 预设头像

> 获取头像 `/api/v1/avatars/{id}` GET

`{id}` 为预设编号（1~8）或自定义头像的 `fileId`，`?v=` 为内容哈希（支持长缓存 / 304）。

## 表情图片

> 获取表情图片 `/api/v1/emojis/{emojiName}/image` GET

`emoji-read` 为一次性的读取 ID，用于去重与埋点：

```
/api/v1/emojis/{emojiName}/image?emoji-read={uuid}
```

## 值得注意的

- 上传后文件存储配额会相应增加；同一张图会生成多尺寸，计费通常大于原图。
- 发帖正文中通过 `![fileId]` 引用图片（不是 URL）。
- 头像/表情会带 `ETag`，配合 `If-None-Match` 协商缓存，常见 304 响应。
- 读取类接口通常直接由 `<img>` 标签加载，不需要 Cookie。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::header::HeaderName;
use reqwest::multipart;
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

    // 上传图片 (需要 reqwest 的 multipart feature)
    let bytes = std::fs::read("cover.png")?;
    let form = multipart::Form::new()
        .text("ownership", "PERSONAL")
        .part("file", multipart::Part::bytes(bytes).file_name("cover.png"));
    let up: Value = client.post(format!("{BASE_URL}/files"))
        .header(HeaderName::from_static("idempotency-key"),
                "d384a653-0000-4000-8000-000000000000")
        .multipart(form)
        .send().await?.error_for_status()?.json().await?;
    println!("上传成功: {}", up["id"]);

    // 我的文件列表
    let list: Value = client.get(format!("{BASE_URL}/files?scope=OWN&state=READY"))
        .send().await?.error_for_status()?.json().await?;
    println!("文件数: {}", list["items"].as_array().map_or(0, Vec::len));

    // 读取文件
    let img = client.get(format!("{BASE_URL}/files/{}", up["id"].as_str().unwrap_or("")))
        .send().await?.error_for_status()?.bytes().await?;
    println!("图片字节数: {}", img.len());

    Ok(())
}
```
```python
import uuid
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

with requests.Session() as s:
    # 先登录 (见《登录》)
    s.post(f"{BASE_URL}/session",
           json={"username": "xxxx@gmail.com", "password": "P@ssW0rd123"}).raise_for_status()

    # 上传图片
    with open("cover.png", "rb") as f:
        up = s.post(
            f"{BASE_URL}/files",
            headers={"Idempotency-Key": str(uuid.uuid4())},
            data={"ownership": "PERSONAL"},
            files={"file": f},
        ).raise_for_status().json()
    print("上传成功:", up["id"])

    # 我的文件列表
    files = s.get(f"{BASE_URL}/files",
                  params={"scope": "OWN", "state": "READY"}).raise_for_status().json()
    print("文件数:", len(files["items"]))

    # 读取文件
    img = s.get(f"{BASE_URL}/files/{up['id']}").raise_for_status().content
    print("图片字节数:", len(img))
```
```typescript
import { readFile } from "node:fs/promises";

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

  // 上传图片 (FormData 会自动设置 content-type)
  const form = new FormData();
  form.set("ownership", "PERSONAL");
  form.set("file", new Blob([await readFile("cover.png")]), "cover.png");
  const up = await (await request("/files", {
    method: "POST",
    headers: { "Idempotency-Key": crypto.randomUUID() },
    body: form,
  })).json();
  console.log("上传成功:", up.id);

  // 我的文件列表
  const files = await (await request("/files?scope=OWN&state=READY")).json();
  console.log("文件数:", files.items.length);

  // 读取文件
  const img = await (await request(`/files/${up.id}`)).arrayBuffer();
  console.log("图片字节数:", img.byteLength);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
