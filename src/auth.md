# 鉴权相关

收录了一些与账号鉴权有关的API接口

## 一览

| METHOD | URL                                                    | COOKIE | 说明                                                       |
| ------ | ------------------------------------------------------ | ------ | ---------------------------------------------------------- |
| POST   | `/api/v1/session`                                      | 否     | [登录](./auth/login.md)，成功后通过 Set-Cookie 下发 Session |
| GET    | `/api/v1/session`                                      | 是     | [获取当前会话](./auth/session.md)，判断登录态是否有效       |
| DELETE | `/api/v1/session`                                      | 是     | [登出](./auth/session.md#登出)，使当前 Session 失效          |
| POST   | `/api/v1/registrations`                                | 否     | [发起注册](./auth/register.md)，仅创建待验证的注册会话      |
| PATCH  | `/api/v1/registrations/{id}`                           | 否     | [验证邮箱](./auth/verify.md)，提交验证码与密码并自动登录    |
| GET    | `/api/v1/entrance-exam`                                | 是     | [获取入站考试状态](./auth/entrance-exam.md)                 |
| POST   | `/api/v1/entrance-exam/attempts`                       | 是     | [开始一次考试](./auth/exam-content.md#开始一次考试)         |
| GET    | `/api/v1/entrance-exam/attempts/{id}/current-question` | 是     | [取当前题](./auth/exam-content.md#取当前题)                 |
| PATCH  | `/api/v1/entrance-exam/attempts/{id}/current-question` | 是     | [提交答案](./auth/exam-content.md#提交答案)                 |

> `COOKIE` 列为「是否需要携带 Session Cookie」；`{id}` 为路径变量，注册场景下是 `registrationId`，考试场景下是 `attemptId`。
>
> 会话 Cookie 名为 `pickcat_session`（HttpOnly / Secure / SameSite=Lax，有效期 7 天）。
