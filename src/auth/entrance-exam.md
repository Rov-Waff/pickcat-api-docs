# 获取入站考试是否可用

> GET `/api/v1/entrance-exam` 需要Cookie

## 响应体

如果入站考试可用，即你未参加入站考试
```json
{ 
    "state": "AVAILABLE",
    "nextAttemptAt": "2026-10-02T12:56:52.310Z" 
}
```
如果你已经通过入站考试
```json
{
  "state": "PASSED",
  "result": {
    "attemptId": "01a0fcb5-97ab-70a8-a38f-e184ca006064",
    "status": "PASSED",
    "totalQuestions": 10,
    "correctCount": 10,
    "requiredCorrectCount": 9,
    "startedAt": "2026-10-02T13:02:34.401Z",
    "finishedAt": "2026-10-02T13:07:24.494Z"
  }
}
```
如果你入站考试处于冷却状态
```json
{
  "state": "COOLDOWN",
  "nextAttemptAt": "2026-10-03T08:37:35.348Z" # 下次可用时间
}
```