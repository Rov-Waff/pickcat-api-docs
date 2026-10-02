# 入站考试

入站考试全过程的API接口


## 开始一次考试

> `POST /api/v1/entrance-exam/attempts` 需要Cookie

无请求体
### 响应体
```json
{ "state": "IN_PROGRESS",
  "attempt": { "attemptId": "01a0fcb5-97ab-70a8-a38f-e184ca006064",
               "totalQuestions": 10, "completedQuestions": 0, "currentOrdinal": 0,
               "deadlineAt": "2026-10-02T13:12:34.401Z",
               "startedAt": "2026-10-02T13:02:34.401Z" } }
```
- 10 题，初始 `deadlineAt` = 开始 + 10 分钟。
- 每次提交答案后会**顺延 deadline**（观测值逐题滚动，属「每题限时」而非整场限时）。

## 取当前题

> `GET /api/v1/entrance-exam/attempts/{id}/current-question` 需要Cookie

### 响应体
```json
{ "state": "QUESTION", "attemptId": "...", "questionId": "...",
  "ordinal": 0, "totalQuestions": 10,
  "questionType": "MULTIPLE_CHOICE | SINGLE_CHOICE",
  "stemHtml": "<p>题干</p>",
  "options": [ { "id": "...", "position": 0, "contentHtml": "<p>选项</p>" } ],
  "deliveryToken": "<本题一次性作答 token>",
  "deadlineAt": "..." }
```
- `deliveryToken` 与题目绑定，提交答案时必须回传，防止重放/跳题。
- 题目为单选或多选（`MULTIPLE_CHOICE` / `SINGLE_CHOICE`）。

## 提交答案

> `PATCH /api/v1/entrance-exam/attempts/{id}/current-question`

### 请求体
```json
{ "questionId": "...",
  "deliveryToken": "...",
  "selectedOptionIds": ["...", "..."] }
```

### 响应体
```json
  { "state": "FINISHED",
    "result": { "attemptId": "...", "status": "PASSED",
                "totalQuestions": 10, "correctCount": 10, "requiredCorrectCount": 9,
                "startedAt": "...", "finishedAt": "2026-10-02T13:07:24.494Z" } }
```
- 中间态响应 `{ "state": "IN_PROGRESS", "attempt": { ...completedQuestions 递增... } }`
- 最后一题响应 `{ "state": "FINISHED", "result": {...} }`：
  
- 合格线 `requiredCorrectCount = 9`（10 题对 9 题）。
- **通过后** `GET /session` 中 `level.current` 由 `0` → `1`，会话 `expiresAt` 顺延。

## 考题与正确答案

> 下列加粗项即正确选项

| #   | 题型 | 题干                                         | 选项（**粗体=正确**）                                                                                                              |
| --- | ---- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1   | 多选 | 在发布作品后希望自己的作品可以上首页，你应该 | **努力学习知识，提升作品质量**；**根据相关要求与方式进行自荐**；在其他作品评论区刷屏打广告；在论坛发布帖子辱骂创委                 |
| 2   | 多选 | 在游玩作品时发现违规内容，可以如何举报       | **通过作品举报功能举报**；**将作品反馈给社区风纪委员**；**将作品链接及违规描述通过 QQ 反馈给官方**；在作品评论区辱骂作品作者       |
| 3   | 单选 | 循环无法做到以下哪个功能？                   | 让编程猫一直运动；让飞机一直发射子弹；让激光能造成持续伤害；**让游戏开始运行**                                                     |
| 4   | 单选 | 和他人意见不同时，合适做法是                 | 直接骂对方不懂编程；恶意举报其所有作品；**理性表达观点，尊重对方，不进行人身攻击**；故意发布错误信息误导对方                       |
| 5   | 单选 | 哪种做法是负责任的创作者态度                 | 随便水几个作品就发布；完全抄袭热门作品；**发布前充分测试，确保无明显 Bug**；给自己的作品刷数据                                     |
| 6   | 单选 | 在作品评论区留言，下列合适的评论是           | **“这个作品很有趣，如果音效再丰富些会更棒！”**；太烂了，别发了；你肯定是抄的；“……”（纯省略号）                                     |
| 7   | 单选 | 关于训练师编号（用户 ID），正确的是          | 可随意修改；就是电话号码；**可用于识别用户身份**；就是用户昵称                                                                     |
| 8   | 单选 | 哪种行为体现编程者的社会责任感               | 编写病毒/恶意程序/钓鱼链接；利用技术盗取他人账号；在社区散布不实信息；**为他人尽可能提供帮助**                                     |
| 9   | 多选 | 在社区中交流，你应该                         | **以尊重他人为前提、以客观事实为基础**；散播隐私/虚假/黄赌毒信息；发布引战脏话阴阳怪气内容；**以解决问题为导向、以友善沟通为原则** |
| 10  | 多选 | 发现编辑器 bug，可以如何反馈                 | 在论坛疯狂刷屏吐槽；**清晰完整地梳理自己遇到的问题**；**使用反馈问卷进行反馈**；**通过 QQ 反馈给官方**                             |
