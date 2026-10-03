# 媒体资源

包括文件上传与读取，以及预设头像、表情等资源。这些资源在浏览器里多被归类为 `image`，但路径位于 `/api/v1` 下。

## 一览

| METHOD | URL                              | COOKIE | 说明                             |
| ------ | -------------------------------- | ------ | -------------------------------- |
| POST   | `/api/v1/files`                  | 是     | [图片上传](./media/upload.md)    |
| GET    | `/api/v1/files`                  | 是     | [我的文件列表](./media/files.md) |
| GET    | `/api/v1/files/{fileId}`         | 否     | [获取文件](./media/file.md)      |
| GET    | `/api/v1/avatars/{id}`           | 否     | [预设头像](./media/avatar.md)    |
| GET    | `/api/v1/emojis/{emojiName}/image` | 否   | [表情图片](./media/emoji.md)     |

> 读取类接口通常直接由 `<img>` 标签加载，不需要 Cookie；上传与文件列表需要登录。
