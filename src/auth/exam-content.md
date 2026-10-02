# 入站考试

入站考试全过程的API接口

## 开始一次考试

> 开始一次考试 `/api/v1/entrance-exam/attempts` POST **需要Cookie**

### 请求体

无请求体。

### 响应体

```json
{
    "state": "IN_PROGRESS",
    "attempt": {
        "attemptId": "01a0fcb5-97ab-70a8-a38f-e184ca006064",
        "totalQuestions": 10,
        "completedQuestions": 0,
        "currentOrdinal": 0,
        "deadlineAt": "2026-10-02T13:12:34.401Z",
        "startedAt": "2026-10-02T13:02:34.401Z"
    }
}
```

| KEY                       | VALUE              | TYPE     |
| ------------------------- | ------------------ | -------- |
| state                     | 固定 `IN_PROGRESS` | String   |
| attempt.attemptId         | 本次考试UUID       | String   |
| attempt.totalQuestions    | 总题数，固定 `10`  | Integer  |
| attempt.completedQuestions| 已完成题数         | Integer  |
| attempt.currentOrdinal    | 当前题序号（从 0 开始） | Integer |
| attempt.deadlineAt        | 本题截止时间       | DateTime |
| attempt.startedAt         | 开始时间           | DateTime |

### 值得注意的

- 10 题，初始 `deadlineAt` = 开始 + 10 分钟。
- 每次提交答案后会**顺延 deadline**（观测值逐题滚动，属「每题限时」而非整场限时）。
- 若上一场未通过且处于冷却期，返回 `409 ENTRANCE_EXAM_COOLDOWN`，`details.nextAttemptAt` 为下次可用时间。

## 取当前题

> 取当前题 `/api/v1/entrance-exam/attempts/{id}/current-question` GET **需要Cookie**

### 响应体

```json
{
    "state": "QUESTION",
    "attemptId": "...",
    "questionId": "...",
    "ordinal": 0,
    "totalQuestions": 10,
    "questionType": "MULTIPLE_CHOICE | SINGLE_CHOICE",
    "stemHtml": "<p>题干</p>",
    "options": [
        { "id": "...", "position": 0, "contentHtml": "<p>选项</p>" }
    ],
    "deliveryToken": "<本题一次性作答 token>",
    "deadlineAt": "..."
}
```

| KEY            | VALUE                        | TYPE     |
| -------------- | ---------------------------- | -------- |
| state          | 固定 `QUESTION`              | String   |
| attemptId      | 本次考试UUID                 | String   |
| questionId     | 题目UUID                     | String   |
| ordinal        | 题号（从 0 开始）            | Integer  |
| totalQuestions | 总题数                       | Integer  |
| questionType   | `MULTIPLE_CHOICE`/`SINGLE_CHOICE` | String |
| stemHtml       | 题干 HTML                    | String   |
| options        | 选项列表（`id`/`position`/`contentHtml`） | ArrayList |
| deliveryToken  | 本题一次性作答 token         | String   |
| deadlineAt     | 本题截止时间                 | DateTime |

### 值得注意的

- `deliveryToken` 与题目绑定，提交答案时必须回传，防止重放/跳题。
- 题目为单选或多选（`MULTIPLE_CHOICE` / `SINGLE_CHOICE`）。

## 提交答案

> 提交答案 `/api/v1/entrance-exam/attempts/{id}/current-question` PATCH **需要Cookie**

### 请求体

```json
{
    "questionId": "...",
    "deliveryToken": "...",
    "selectedOptionIds": ["...", "..."]
}
```

| KEY               | VALUE                   | TYPE      |
| ----------------- | ----------------------- | --------- |
| questionId        | 题目UUID                | String    |
| deliveryToken     | 取题时返回的作答 token  | String    |
| selectedOptionIds | 所选选项ID列表          | ArrayList |

### 响应体

中间态（未到最后一题）：

```json
{
    "state": "IN_PROGRESS",
    "attempt": { "...": "completedQuestions 递增" }
}
```

最后一题：

```json
{
    "state": "FINISHED",
    "result": {
        "attemptId": "...",
        "status": "PASSED",
        "totalQuestions": 10,
        "correctCount": 10,
        "requiredCorrectCount": 9,
        "startedAt": "...",
        "finishedAt": "2026-10-02T13:07:24.494Z"
    }
}
```

### 值得注意的

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

## 示例

自动完成整场考试（演示：每题都选第一个选项，实际使用请填入正确答案）。

<!-- langtabs-start -->
```rust
use anyhow::Result;
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";
const USERNAME: &str = "xxxx@gmail.com";
const PASSWORD: &str = "P@ssW0rd123";

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder().cookie_provider(jar.clone()).build()?;

    // 登录
    client.post(format!("{BASE_URL}/session"))
        .json(&json!({ "username": USERNAME, "password": PASSWORD }))
        .send().await?.error_for_status()?;

    // 开始一次考试
    let start: Value = client.post(format!("{BASE_URL}/entrance-exam/attempts"))
        .send().await?.error_for_status()?.json().await?;
    let attempt_id = start["attempt"]["attemptId"].as_str().unwrap().to_string();
    println!("开始考试: {attempt_id}");

    loop {
        // 取当前题
        let q: Value = client
            .get(format!("{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question"))
            .send().await?.error_for_status()?.json().await?;

        let qid = q["questionId"].as_str().unwrap().to_string();
        let token = q["deliveryToken"].as_str().unwrap().to_string();
        // 演示: 选择第一个选项
        let pick = json!([q["options"][0]["id"].as_str().unwrap()]);

        // 提交答案
        let resp: Value = client
            .patch(format!("{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question"))
            .json(&json!({
                "questionId": qid,
                "deliveryToken": token,
                "selectedOptionIds": pick,
            }))
            .send().await?.error_for_status()?.json().await?;

        if resp["state"] == "FINISHED" {
            let r = &resp["result"];
            println!("考试结束: {} {}/{}", r["status"], r["correctCount"], r["totalQuestions"]);
            break;
        }
        println!("已提交, 已完成 {} 题", resp["attempt"]["completedQuestions"]);
    }

    Ok(())
}
```
```python
import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"
USERNAME = "xxxx@gmail.com"
PASSWORD = "P@ssW0rd123"

with requests.Session() as s:
    s.post(f"{BASE_URL}/session", json={"username": USERNAME, "password": PASSWORD}).raise_for_status()

    # 开始一次考试
    start = s.post(f"{BASE_URL}/entrance-exam/attempts").raise_for_status().json()
    attempt_id = start["attempt"]["attemptId"]
    print("开始考试:", attempt_id)

    while True:
        # 取当前题
        q = s.get(
            f"{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question"
        ).raise_for_status().json()

        # 演示: 选择第一个选项
        pick = [q["options"][0]["id"]]

        # 提交答案
        resp = s.patch(
            f"{BASE_URL}/entrance-exam/attempts/{attempt_id}/current-question",
            json={
                "questionId": q["questionId"],
                "deliveryToken": q["deliveryToken"],
                "selectedOptionIds": pick,
            },
        ).raise_for_status().json()

        if resp["state"] == "FINISHED":
            r = resp["result"]
            print("考试结束:", r["status"], f'{r["correctCount"]}/{r["totalQuestions"]}')
            break
        print("已提交, 已完成", resp["attempt"]["completedQuestions"], "题")
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const USERNAME = "xxxx@gmail.com";
const PASSWORD = "P@ssW0rd123";
const jar = new Map<string, string>();

function cookieHeader(): string {
  return [...jar].map(([k, v]) => `${k}=${v}`).join("; ");
}

async function request(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  const cookie = cookieHeader();
  if (cookie) headers.set("cookie", cookie);
  const res = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  for (const c of res.headers.getSetCookie?.() ?? []) {
    const [pair] = c.split(";");
    const i = pair.indexOf("=");
    if (i > 0) jar.set(pair.slice(0, i), pair.slice(i + 1));
  }
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res;
}

async function main() {
  await request("/session", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username: USERNAME, password: PASSWORD }),
  });

  // 开始一次考试
  const start = await (await request("/entrance-exam/attempts", { method: "POST" })).json();
  const attemptId: string = start.attempt.attemptId;
  console.log("开始考试:", attemptId);

  while (true) {
    // 取当前题
    const q = await (await request(`/entrance-exam/attempts/${attemptId}/current-question`)).json();
    const pick = [q.options[0].id]; // 演示: 选择第一个选项

    // 提交答案
    const resp = await (await request(`/entrance-exam/attempts/${attemptId}/current-question`, {
      method: "PATCH",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        questionId: q.questionId,
        deliveryToken: q.deliveryToken,
        selectedOptionIds: pick,
      }),
    })).json();

    if (resp.state === "FINISHED") {
      const r = resp.result;
      console.log("考试结束:", r.status, `${r.correctCount}/${r.totalQuestions}`);
      break;
    }
    console.log("已提交, 已完成", resp.attempt.completedQuestions, "题");
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
```
<!-- langtabs-end -->
