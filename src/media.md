# 媒体资源

这些资源在浏览器里被归类为 `image`，但路径位于 `/api/v1` 下。

## 预设头像

> 获取头像 `/api/v1/avatars/{id}` GET

`{id}` 为预设编号（1~8）或自定义头像的 `fileId`，`?v=` 为内容哈希（支持长缓存 / 304）。

## 表情图片

> 获取表情图片 `/api/v1/emojis/{emojiName}/image` GET

`emoji-read` 为一次性的读取 ID，用于去重与埋点：

```
/api/v1/emojis/{emojiName}/image?emoji-read={uuid}
```

## 上传文件

> 获取文件 `/api/v1/files/{fileId}` GET

帖子图片、徽章图片等都通过该接口读取。

## 值得注意的

- 头像/表情会带 `ETag`，配合 `If-None-Match` 协商缓存，常见 304 响应。
- 这些接口通常直接由 `<img>` 标签加载，不需要 Cookie。

## 示例

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::Client;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";

#[tokio::main]
async fn main() -> Result<()> {
    let client = Client::new();

    // 预设头像
    let avatar = client.get(format!("{BASE_URL}/avatars/1"))
        .send().await?.error_for_status()?.bytes().await?;
    println!("头像字节数: {}", avatar.len());

    // 上传文件
    let file = client.get(format!("{BASE_URL}/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52"))
        .send().await?.error_for_status()?.bytes().await?;
    println!("文件字节数: {}", file.len());

    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"

with requests.Session() as s:
    avatar = s.get(f"{BASE_URL}/avatars/1").raise_for_status().content
    print("头像字节数:", len(avatar))

    file = s.get(f"{BASE_URL}/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52").raise_for_status().content
    print("文件字节数:", len(file))
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";

async function size(path: string): Promise<number> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return (await res.arrayBuffer()).byteLength;
}

async function main() {
  console.log("头像字节数:", await size("/avatars/1"));
  console.log("文件字节数:", await size("/files/01a0b34f-c685-7777-b60d-fe2a6adb6f52"));
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
