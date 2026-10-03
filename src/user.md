# 用户相关

收录与用户资料、内容、徽章、动态、等级以及账户设置有关的API接口

## 一览

| METHOD | URL                                                    | COOKIE | 说明                                                       |
| ------ | ------------------------------------------------------ | ------ | ---------------------------------------------------------- |
| GET    | `/api/v1/users/{userId}`                               | 否     | [获取用户资料](./user/profile.md#获取用户资料)              |
| PATCH  | `/api/v1/users/{userId}`                               | 是     | [修改个人资料](./user/profile.md#修改个人资料)              |
| GET    | `/api/v1/users/{userId}/email`                         | 是     | [查询用户邮箱（仅自己）](./user/profile.md#查询用户邮箱仅自己) |
| GET    | `/api/v1/users/{userId}/following`                     | 否     | [关注列表](./user/follow.md#获取关注列表)                   |
| GET    | `/api/v1/users/{userId}/followers`                     | 否     | [粉丝列表](./user/follow.md#获取粉丝列表)                   |
| GET    | `/api/v1/users/{userId}/topics`                        | 否     | [用户发布的主题](./user/content.md#发布的主题)              |
| GET    | `/api/v1/users/{userId}/posts`                         | 否     | [用户的回帖](./user/content.md#回帖)                        |
| GET    | `/api/v1/users/{userId}/featured-topics`               | 否     | [精选主题](./user/content.md#精选主题)                      |
| GET    | `/api/v1/users/{userId}/topic-collections`             | 否     | [用户的合集](./user/content.md#合集)                        |
| GET    | `/api/v1/users/{userId}/badges`                        | 否     | [用户获得的徽章](./user/badge.md#用户获得的徽章)            |
| GET    | `/api/v1/users/{userId}/badge-display`                 | 否     | [徽章展示设置](./user/badge.md#徽章展示设置)                |
| GET    | `/api/v1/user-badge-displays`                          | 否     | [批量查询展示徽章](./user/badge.md#批量查询展示徽章)        |
| GET    | `/api/v1/users/{userId}/profile-activities`            | 否     | [用户动态（公开）](./user/activity.md#用户动态公开)         |
| GET    | `/api/v1/users/{userId}/level-contributions/{year}`    | 否     | [用户贡献日历](./user/activity.md#用户贡献日历)             |
| GET    | `/api/v1/profile-activities`                           | 是     | [当前用户动态](./user/activity.md#当前用户动态)             |
| GET    | `/api/v1/level-contributions/{year}`                   | 是     | [当前用户贡献日历](./user/activity.md#当前用户贡献日历)     |
| GET    | `/api/v1/level-progress`                               | 是     | [等级进度](./user/level.md#等级进度)                        |
| GET    | `/api/v1/content-length-limit`                         | 是     | [内容长度上限](./user/level.md#内容长度上限)                |
| GET    | `/api/v1/topic-collection-usage`                       | 是     | [合集配额用量](./user/level.md#合集配额用量)                |
| GET    | `/api/v1/file-storage`                                 | 是     | [文件存储配额](./user/settings.md#文件存储配额)             |
| GET    | `/api/v1/avatar-presets`                               | 否     | [预设头像列表](./user/settings.md#预设头像列表)             |
| GET    | `/api/v1/bookmarks`                                    | 是     | [我的书签](./user/settings.md#我的书签)                     |

> `{userId}` 为用户 UUID；省略 `{userId}` 前缀的接口（`/level-progress`、`/profile-activities` 等）只作用于当前登录用户，因此**需要Cookie**。
>
> 公开接口（如 `/users/{userId}`）即使不携带 Cookie 也能访问，携带时会在 `viewerState` 中返回与访问者的关注关系。
