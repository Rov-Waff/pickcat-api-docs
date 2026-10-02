# 发起注册

> 注册帐号 `/api/v1/registrations` POST
> 此步骤仅发起注册，并没有注册账号

## 请求体

```json
{
    "username": "SilverPremium",
    "email": "xiao***@***.***",
    "captchaVerifyParam": "<base64(阿里云验证码回调 JSON)>"
}
```

## 响应体

```json
{ 
    "id": "01a0fcab-dae0-736a-8d90-583dc20def93",
    "status": "PENDING",
    "expiresAt": "2026-10-02T12:56:56.460Z" 
}
```

## 值得注意的

- `captchaVerifyParam` 是前端把阿里云返回的验证结果 Base64 编码后的字符串。此步骤**不发送密码**。
- 请求头**必须**携带 `Idempotency-Key`（1~128 个可见 ASCII 字符），用于防止重复发起注册；缺失时返回 `400 IDEMPOTENCY_KEY_REQUIRED`。
- `registrationId` 用于后续 PATCH；`PENDING` 表示等待邮箱验证；`expiresAt` 为验证有效期。
- 成功返回 `201 Created`。
- 由于存在CAPTHA，脚本注册大量账号并不现实

## 示例

<!-- langtabs-start -->
```rust
use anyhow::{Context, Result};
use reqwest::{cookie::Jar, Client};
use serde_json::{json, Value};
use std::sync::Arc;

const BASE_URL: &str = "https://cdsq.dao3.fun/api/v1";

/// 发起注册。返回注册会话 (含 id / status / expiresAt)
async fn start_registration(
    client: &Client,
    username: &str,
    email: &str,
    captcha_verify_param: &str,
) -> Result<Value> {
    let resp = client
        .post(format!("{BASE_URL}/registrations"))
        .json(&json!({
            "username": username,
            "email": email,
            "captchaVerifyParam": captcha_verify_param,
        }))
        .send()
        .await?
        .error_for_status()?;

    let data: Value = resp.json().await?;
    Ok(data)
}

fn get<'a>(v: &'a Value, path: &[&str]) -> Result<&'a Value> {
    let mut cur = v;
    for key in path {
        cur = cur
            .get(*key)
            .with_context(|| format!("缺少字段: {}", path.join(".")))?;
    }
    Ok(cur)
}

#[tokio::main]
async fn main() -> Result<()> {
    let jar = Arc::new(Jar::default());
    let client = Client::builder()
        .cookie_provider(jar.clone())
        .build()?;

    // 前端从阿里云验证码回调拿到的 JSON, 做 base64
    // 这里仅示意, 真实值应由前端传入
    let captcha_json = r#"{"certifyId":"...","sceneId":"1icer78a","isSign":true,"securityToken":"..."}"#;
    let captcha_b64 = base64_encode(captcha_json);

    let data = start_registration(
        &client,
        "SilverPremium",
        "xiao***@***.***",
        &captcha_b64,
    )
    .await?;

    let reg_id = get(&data, &["id"])?.as_str().unwrap_or("");
    let status = get(&data, &["status"])?.as_str().unwrap_or("");
    let expires = get(&data, &["expiresAt"])?.as_str().unwrap_or("");

    println!("注册会话已发起:");
    println!("registrationId : {reg_id}");
    println!("status         : {status}"); // PENDING
    println!("expiresAt      : {expires}");

    // 后续步骤: PATCH /registrations/{reg_id} 提交验证码/密码等

    Ok(())
}

// 简易 base64 
fn base64_encode(s: &str) -> String {
    const TABLE: &[u8; 64] =
        b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let bytes = s.as_bytes();
    let mut out = String::new();
    for chunk in bytes.chunks(3) {
        let b = [
            chunk[0],
            *chunk.get(1).unwrap_or(&0),
            *chunk.get(2).unwrap_or(&0),
        ];
        let n = ((b[0] as u32) << 16) | ((b[1] as u32) << 8) | b[2] as u32;
        out.push(TABLE[((n >> 18) & 63) as usize] as char);
        out.push(TABLE[((n >> 12) & 63) as usize] as char);
        out.push(if chunk.len() > 1 {
            TABLE[((n >> 6) & 63) as usize] as char
        } else {
            '='
        });
        out.push(if chunk.len() > 2 {
            TABLE[(n & 63) as usize] as char
        } else {
            '='
        });
    }
    out
}
```
```python
import base64
import json

import requests

BASE_URL = "https://cdsq.dao3.fun/api/v1"


def start_registration(
    session: requests.Session,
    username: str,
    email: str,
    captcha_verify_param: str,
) -> dict:
    """发起注册, 返回 { id, status, expiresAt }"""
    resp = session.post(
        f"{BASE_URL}/registrations",
        json={
            "username": username,
            "email": email,
            "captchaVerifyParam": captcha_verify_param,
        },
    )
    resp.raise_for_status()
    return resp.json()


def main():
    # 前端从阿里云验证码回调拿到的 JSON, base64 编码后传后端
    captcha_json = '{"certifyId":"...","sceneId":"1icer78a","isSign":true,"securityToken":"..."}'
    captcha_b64 = base64.b64encode(captcha_json.encode()).decode()

    with requests.Session() as s:
        data = start_registration(
            s,
            username="SilverPremium",
            email="xiao***@***.***",
            captcha_verify_param=captcha_b64,
        )

        reg_id = data["id"]
        print("注册会话已发起:")
        print(f"registrationId : {reg_id}")
        print(f"status         : {data['status']}")   # PENDING
        print(f"expiresAt      : {data['expiresAt']}")

        # 后续: PATCH /registrations/{reg_id} 提交密码 / 邮箱验证码
        # resp = s.patch(f"{BASE_URL}/registrations/{reg_id}", json={...})


if __name__ == "__main__":
    main()
```
```typescript
const BASE_URL = "https://cdsq.dao3.fun/api/v1";
const jar = new Map<string, string>();

function storeCookies(res: Response) {
  const setCookies = res.headers.getSetCookie?.() ?? [];
  for (const c of setCookies) {
    const [pair] = c.split(";");
    const idx = pair.indexOf("=");
    if (idx > 0) jar.set(pair.slice(0, idx), pair.slice(idx + 1));
  }
}

function cookieHeader(): string {
  return [...jar.entries()].map(([k, v]) => `${k}=${v}`).join("; ");
}

async function request(path: string, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers);
  const cookie = cookieHeader();
  if (cookie) headers.set("cookie", cookie);

  const res = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  storeCookies(res);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res;
}

// ===== 发起注册 =====

async function startRegistration(
  username: string,
  email: string,
  captchaVerifyParam: string,
): Promise<{ id: string; status: string; expiresAt: string }> {
  const res = await request("/registrations", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ username, email, captchaVerifyParam }),
  });
  return res.json();
}

async function main() {
  // 前端从阿里云验证码回调拿到的 JSON, base64 编码
  const captchaJson = JSON.stringify({ certifyId: "...", sceneId: "1icer78a", isSign: true, securityToken: "..." });
  const captchaB64 = Buffer.from(captchaJson, "utf8").toString("base64");

  const data = await startRegistration(
    "SilverPremium",
    "xiao***@***.***",
    captchaB64,
  );

  console.log("注册会话已发起:");
  console.log(`registrationId : ${data.id}`);
  console.log(`status         : ${data.status}`); // PENDING
  console.log(`expiresAt      : ${data.expiresAt}`);

  // 后续: PATCH /registrations/{id} 提交密码 / 邮箱验证码
  // await request(`/registrations/${data.id}`, {
  //   method: "PATCH",
  //   headers: { "content-type": "application/json" },
  //   body: JSON.stringify({ ... }),
  // });
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
```
<!-- langtabs-end -->