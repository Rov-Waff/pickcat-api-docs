# 图片上传

> 上传图片 `/api/v1/files` POST **需要Cookie**

请求头需带 `Idempotency-Key`，`content-type` 为 `multipart/form-data`。

## 请求体

### 表单字段

| 字段      | 值         | 说明                          |
| --------- | ---------- | ----------------------------- |
| ownership | `PERSONAL` | 归属，推测还有帖子/主题归属等 |
| file      | 二进制     | 图片本体                      |

## 响应体

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

## 值得注意的

- 所有写接口都需要 `Idempotency-Key` 请求头。
- 上传后文件存储配额会相应增加；同一张图会生成多尺寸，计费通常大于原图。
- 发帖正文中通过 `![fileId]` 引用图片（不是 URL）。

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

    // 需要 reqwest 的 multipart feature
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

    with open("cover.png", "rb") as f:
        up = s.post(
            f"{BASE_URL}/files",
            headers={"Idempotency-Key": str(uuid.uuid4())},
            data={"ownership": "PERSONAL"},
            files={"file": f},
        ).raise_for_status().json()
    print("上传成功:", up["id"])
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

  // FormData 会自动设置 content-type
  const form = new FormData();
  form.set("ownership", "PERSONAL");
  form.set("file", new Blob([await readFile("cover.png")]), "cover.png");
  const up = await (await request("/files", {
    method: "POST",
    headers: { "Idempotency-Key": crypto.randomUUID() },
    body: form,
  })).json();
  console.log("上传成功:", up.id);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
