# 鉴权相关

收录了一些与账号鉴权有关的API接口

## 一览

| METHOD | URL                                                    | COOKIE | 说明                                                       |
| ------ | ------------------------------------------------------ | ------ | ---------------------------------------------------------- |
| POST   | `/api/v1/session`                                      | 否     | [登录](./auth/login.md)，成功后通过 Set-Cookie 下发 Session |
| GET    | `/api/v1/session`                                      | 是     | [获取当前会话](./auth/session.md)                           |
| DELETE | `/api/v1/session`                                      | 是     | [登出](./auth/logout.md)，使当前 Session 失效              |
| POST   | `/api/v1/registrations`                                | 否     | [发起注册](./auth/register.md)，仅创建待验证的注册会话      |
| PATCH  | `/api/v1/registrations/{id}`                           | 否     | [验证邮箱](./auth/verify.md)，提交验证码与密码并自动登录    |
| GET    | `/api/v1/entrance-exam`                                | 是     | [获取入站考试状态](./auth/entrance-exam.md)                 |
| POST   | `/api/v1/entrance-exam/attempts`                       | 是     | [开始一次考试](./auth/exam-start.md)                        |
| GET    | `/api/v1/entrance-exam/attempts/{id}/current-question` | 是     | [取当前题](./auth/exam-question.md)                         |
| PATCH  | `/api/v1/entrance-exam/attempts/{id}/current-question` | 是     | [提交答案](./auth/exam-submit.md)                           |

> `COOKIE` 列为「是否需要携带 Session Cookie」；`{id}` 为路径变量，注册场景下是 `registrationId`，考试场景下是 `attemptId`。
>
> 会话 Cookie 名为 `pickcat_session`（HttpOnly / Secure / SameSite=Lax，有效期 7 天）。
>
> 入站考试题库（非 API）见[考题与正确答案](./auth/exam-questions.md)。
