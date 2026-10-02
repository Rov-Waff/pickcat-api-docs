# 验证邮箱

> 验证邮箱 `/api/v1/registrations/{id}` PATCH

## 请求体
  ```json
  { 
    "code": "<邮箱验证码>",
    "password": "<密码>" 
  }
  ```
## 响应体
  ```json
  {
    "id": "01a0fcb0-5f5b-772d-a8ba-4b39d1ee4445",
    "username": "SilverPremium",
    "avatar": { "type": "PRESET", "id": 1, "url": "/api/v1/avatars/1?v=..." },
    "bio": null, "region": null,
    "showFollowingList": true, "showFollowersList": true,
    "createdAt": "2026-10-02T12:56:52.310Z",
    "level": { "current": 0 },          // 注册后为 Lv.0
    "stats": { "followers": 0, "following": 0, "topics": 0, "replies": 0 },
    "viewerState": { "following": false, "canFollow": false }
  }
  ```

## 值得注意的

- 验证后将会用Set-Cookie设置Session,自动登录