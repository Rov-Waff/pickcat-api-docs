# 表情图片

> 获取表情图片 `/api/v1/emojis/{emojiName}/image` GET

`emoji-read` 为一次性的读取 ID，用于去重与埋点：

```
/api/v1/emojis/{emojiName}/image?emoji-read={uuid}
```

## 响应体

二进制图片数据（`content-type` 为 `image/*`，通常为 GIF）。

## 值得注意的

- 表情名可从帖子正文的 `cookedHtml` 中提取（形如 `gif_expression_...`）。
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
        .get(format!("{BASE_URL}/emojis/gif_expression_bianchenmao_funny/image"))
        .send().await?.error_for_status()?.bytes().await?;
    println!("表情字节数: {}", bytes.len());
    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

data = requests.get(f"{BASE_URL}/emojis/gif_expression_bianchenmao_funny/image").raise_for_status().content
print("表情字节数:", len(data))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";

async function main() {
  const res = await fetch(`${BASE_URL}/emojis/gif_expression_bianchenmao_funny/image`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  console.log("表情字节数:", (await res.arrayBuffer()).byteLength);
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
