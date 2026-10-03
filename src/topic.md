# 主题与内容

收录主题（帖子）列表、详情、楼层、发布以及投稿审核相关的API接口

## 一览

| METHOD | URL                                          | COOKIE | 说明                                   |
| ------ | -------------------------------------------- | ------ | -------------------------------------- |
| GET    | `/api/v1/topics`                             | 否     | [主题列表](./topic/list.md)            |
| GET    | `/api/v1/topic-recommendations`              | 否     | [首页推荐](./topic/recommendations.md) |
| GET    | `/api/v1/topics/{topicId}`                   | 否     | [主题详情](./topic/detail.md)          |
| GET    | `/api/v1/topics/{topicId}/posts`             | 否     | [楼层列表](./topic/posts.md)           |
| POST   | `/api/v1/posts`                              | 是     | [发布主题/回帖](./topic/create.md)     |
| GET    | `/api/v1/post-submissions`                   | 是     | [投稿审核列表](./topic/submissions.md) |
| GET    | `/api/v1/post-submissions/{submissionId}`    | 是     | [投稿详情](./topic/submission-detail.md) |

> `{topicId}` 为主题 UUID。主题相关接口不带 Cookie 也可访问，携带时 `viewerCapabilities` / `viewerState` 会反映当前用户的权限与状态。
