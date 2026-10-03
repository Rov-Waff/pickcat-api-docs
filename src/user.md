# 用户相关

收录与用户资料、内容、徽章、动态、等级以及账户设置有关的API接口

## 一览

| METHOD | URL                                                  | COOKIE | 说明                                       |
| ------ | ---------------------------------------------------- | ------ | ------------------------------------------ |
| GET    | `/api/v1/users/{userId}`                             | 否     | [用户资料](./user/profile.md)              |
| PATCH  | `/api/v1/users/{userId}`                             | 是     | [修改个人资料](./user/profile-edit.md)     |
| GET    | `/api/v1/users/{userId}/email`                       | 是     | [查询用户邮箱](./user/email.md)            |
| GET    | `/api/v1/users/{userId}/following`                   | 否     | [关注列表](./user/following.md)            |
| GET    | `/api/v1/users/{userId}/followers`                   | 否     | [粉丝列表](./user/followers.md)            |
| GET    | `/api/v1/users/{userId}/topics`                      | 否     | [用户发布的主题](./user/topics.md)         |
| GET    | `/api/v1/users/{userId}/posts`                       | 否     | [用户的回帖](./user/posts.md)              |
| GET    | `/api/v1/users/{userId}/featured-topics`             | 否     | [精选主题](./user/featured-topics.md)      |
| GET    | `/api/v1/users/{userId}/topic-collections`           | 否     | [用户的合集](./user/topic-collections.md)  |
| GET    | `/api/v1/users/{userId}/badges`                      | 否     | [用户获得的徽章](./user/badges.md)         |
| GET    | `/api/v1/users/{userId}/badge-display`               | 否     | [徽章展示设置](./user/badge-display.md)    |
| GET    | `/api/v1/user-badge-displays`                        | 否     | [批量查询展示徽章](./user/user-badge-displays.md) |
| GET    | `/api/v1/users/{userId}/profile-activities`          | 否     | [用户动态](./user/profile-activities.md)   |
| GET    | `/api/v1/users/{userId}/level-contributions/{year}`  | 否     | [用户贡献日历](./user/level-contributions.md) |
| GET    | `/api/v1/profile-activities`                         | 是     | [当前用户动态](./user/my-profile-activities.md) |
| GET    | `/api/v1/level-contributions/{year}`                 | 是     | [当前用户贡献日历](./user/my-level-contributions.md) |
| GET    | `/api/v1/level-progress`                             | 是     | [等级进度](./user/level-progress.md)       |
| GET    | `/api/v1/content-length-limit`                       | 是     | [内容长度上限](./user/content-length-limit.md) |
| GET    | `/api/v1/topic-collection-usage`                     | 是     | [合集配额用量](./user/topic-collection-usage.md) |
| GET    | `/api/v1/file-storage`                               | 是     | [文件存储配额](./user/file-storage.md)     |
| GET    | `/api/v1/bookmarks`                                  | 是     | [我的书签](./user/bookmarks.md)            |
| GET    | `/api/v1/avatar-presets`                             | 否     | [预设头像列表](./user/avatar-presets.md)   |

> `{userId}` 为用户 UUID；省略 `{userId}` 前缀的接口（`/level-progress`、`/profile-activities` 等）只作用于当前登录用户，因此**需要Cookie**。
>
> 公开接口（如 `/users/{userId}`）即使不携带 Cookie 也能访问，携带时会在 `viewerState` 中返回与访问者的关注关系。
