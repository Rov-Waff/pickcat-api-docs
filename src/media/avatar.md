# 预设头像

> 获取头像 `/api/v1/avatars/{id}` GET

`{id}` 为预设编号（1~8）或自定义头像的 `fileId`，`?v=` 为内容哈希（支持长缓存 / 304）。

## 响应体

二进制图片数据（`content-type` 为 `image/*`）。

## 值得注意的

- 会带 `ETag`，配合 `If-None-Match` 协商缓存，常见 304 响应。
- 通常直接由 `<img>` 标签加载，不需要 Cookie。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let bytes = Client::new()
        .get(format!("{BASE_URL}/avatars/1"))
        .send().await?.error_for_status()?.bytes().await?;
    println!("头像字节数: {}", bytes.len());
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

data = requests.get(f"{BASE_URL}/avatars/1").raise_for_status().content
print("头像字节数:", len(data))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";

async function main() {
  const res = await fetch(`${BASE_URL}/avatars/1`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  console.log("头像字节数:", (await res.arrayBuffer()).byteLength);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
