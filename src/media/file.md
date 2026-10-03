# 获取文件

> 获取文件 `/api/v1/files/{fileId}` GET

帖子图片、徽章图片等都通过该接口读取。

## 响应体

二进制图片数据（`content-type` 为 `image/*`）。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let bytes = Client::new()
        .get(format!("{BASE_URL}/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52"))
        .send().await?.error_for_status()?.bytes().await?;
    println!("文件字节数: {}", bytes.len());
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

data = requests.get(f"{BASE_URL}/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52").raise_for_status().content
print("文件字节数:", len(data))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";

async function main() {
  const res = await fetch(`${BASE_URL}/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  console.log("文件字节数:", (await res.arrayBuffer()).byteLength);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
