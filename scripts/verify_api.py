#!/usr/bin/env python3
"""验证 Pickcat 文档中记录的全部 API。

用法:
    PICKCAT_SESSION='<pickcat_session>' python3 scripts/verify_api.py
    python3 scripts/verify_api.py --session '<pickcat_session>'

说明:
- 所有 GET 接口都会真实请求；需要 Cookie 的接口使用传入的 Session。
- 写接口不会真正写入数据：脚本只发送不合法的最小请求，确认路由存在且返回业务错误。
- 登录接口需要阿里云 CAPTCHA，脚本不会尝试真实登录。
- 脚本不会输出 Session 值，也不会调用会注销当前会话的 DELETE /session。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from typing import Any

try:
    import requests
except ImportError:  # pragma: no cover - 仅用于给出友好提示
    sys.exit("缺少依赖 requests，请先执行: pip install requests")

DEFAULT_BASE_URL = "https://pickcat.dao3.fun/api/v1"
TIMEOUT = 25
USER_AGENT = "pickcat-api-docs-verifier/1.0"
CURRENT_YEAR = time.localtime().tm_year

# 文档中的回退示例值，只有在无法动态发现真实 ID 时才会使用
FALLBACK_USER_ID = "01a0fbca-eee1-70ad-a00d-a1ed4c89b195"
FALLBACK_TOPIC_ID = "01a0eb91-5d11-7fb0-b998-179add93620f"
FALLBACK_TAG_SLUG = "interest-plaza"
FALLBACK_FILE_ID = "01a0b34f-c685-7777-b60d-fe2a6adb6f52"
EMOJI_NAME = "gif_expression_bianchenmao_funny"

_UNSET = object()


@dataclass
class Result:
    group: str
    name: str
    method: str
    path: str
    status: int | None
    verdict: str
    elapsed_ms: int
    note: str = ""


class Verifier:
    def __init__(self, base_url: str, session_cookie: str | None) -> None:
        self.base_url = base_url.rstrip("/")
        self.session_cookie = session_cookie
        self.http = requests.Session()
        self.http.headers.update(
            {
                "Accept": "application/json, image/*;q=0.9, */*;q=0.8",
                "User-Agent": USER_AGENT,
            }
        )
        self.results: list[Result] = []
        self.discovered: dict[str, str | None] = {}
        self.current_group = ""

    # ---------- 基础请求 ----------

    def _request(
        self,
        method: str,
        path: str,
        *,
        auth: bool = False,
        params: dict[str, Any] | None = None,
        json_body: Any = _UNSET,
    ) -> tuple[requests.Response, int, str]:
        url = f"{self.base_url}{path}"
        headers: dict[str, str] = {}
        if auth and self.session_cookie:
            headers["Cookie"] = f"pickcat_session={self.session_cookie}"

        kwargs: dict[str, Any] = {
            "headers": headers,
            "params": params,
            "timeout": TIMEOUT,
            "allow_redirects": True,
        }
        if json_body is not _UNSET:
            kwargs["json"] = json_body

        start = time.perf_counter()
        resp = self.http.request(method, url, **kwargs)
        elapsed = int((time.perf_counter() - start) * 1000)
        # 不让服务端 Set-Cookie 影响后续请求，Cookie 仅由显式传入的 Session 控制
        self.http.cookies.clear()
        time.sleep(0.05)
        return resp, elapsed, url

    def _record(
        self,
        name: str,
        method: str,
        path: str,
        status: int | None,
        verdict: str,
        elapsed_ms: int = 0,
        note: str = "",
    ) -> Result:
        result = Result(
            group=self.current_group,
            name=name,
            method=method,
            path=path,
            status=status,
            verdict=verdict,
            elapsed_ms=elapsed_ms,
            note=note,
        )
        self.results.append(result)
        status_text = "-" if status is None else str(status)
        print(f"[{verdict:<5}] {name:<32} {method:<6} {path:<58} {status_text:>3} {elapsed_ms:>5}ms  {note}")
        return result

    def group(self, name: str) -> None:
        self.current_group = name
        print(f"\n== {name} ==")

    # ---------- 断言 ----------

    def test_json(
        self,
        name: str,
        method: str,
        path: str,
        *,
        auth: bool = False,
        params: dict[str, Any] | None = None,
        keys: tuple[str, ...] = (),
    ) -> dict[str, Any] | None:
        if auth and not self.session_cookie:
            self._record(name, method, path, None, "SKIP", note="未提供 Session")
            return None
        try:
            resp, elapsed, _ = self._request(method, path, auth=auth, params=params)
        except requests.RequestException as exc:
            self._record(name, method, path, None, "FAIL", note=f"请求异常: {exc}")
            return None

        if resp.status_code != 200:
            self._record(name, method, path, resp.status_code, "FAIL", elapsed, self._error_note(resp))
            return None

        content_type = resp.headers.get("content-type", "")
        if "json" not in content_type:
            self._record(
                name,
                method,
                path,
                resp.status_code,
                "FAIL",
                elapsed,
                f"Content-Type 不是 JSON: {content_type or '<none>'}",
            )
            return None

        try:
            data = resp.json()
        except ValueError as exc:
            self._record(name, method, path, resp.status_code, "FAIL", elapsed, f"JSON 解析失败: {exc}")
            return None

        if not isinstance(data, dict):
            self._record(name, method, path, resp.status_code, "FAIL", elapsed, "顶层不是对象")
            return None

        missing = [key for key in keys if key not in data]
        if missing:
            self._record(
                name,
                method,
                path,
                resp.status_code,
                "FAIL",
                elapsed,
                f"缺少字段: {', '.join(missing)}",
            )
            return None

        self._record(name, method, path, resp.status_code, "PASS", elapsed, self._shape_note(data))
        return data

    def test_image(self, name: str, path: str, *, auth: bool = False) -> None:
        if auth and not self.session_cookie:
            self._record(name, "GET", path, None, "SKIP", note="未提供 Session")
            return
        try:
            resp, elapsed, _ = self._request("GET", path, auth=auth)
        except requests.RequestException as exc:
            self._record(name, "GET", path, None, "FAIL", note=f"请求异常: {exc}")
            return

        if resp.status_code != 200:
            self._record(name, "GET", path, resp.status_code, "FAIL", elapsed, self._error_note(resp))
            return

        content_type = resp.headers.get("content-type", "")
        size = len(resp.content)
        if not content_type.startswith("image/"):
            self._record(name, "GET", path, resp.status_code, "FAIL", elapsed, f"Content-Type: {content_type or '<none>'}")
            return
        if size == 0:
            self._record(name, "GET", path, resp.status_code, "FAIL", elapsed, "响应体为空")
            return

        self._record(name, "GET", path, resp.status_code, "PASS", elapsed, f"{content_type}, {size} bytes")

    def probe_write(self, name: str, method: str, path: str, *, with_body: bool = True) -> None:
        """只验证写接口路由存在，不发送 Session，也不会真正写入数据。"""
        body: Any = {} if with_body else _UNSET
        try:
            resp, elapsed, _ = self._request(method, path, auth=False, json_body=body)
        except requests.RequestException as exc:
            self._record(name, method, path, None, "FAIL", note=f"请求异常: {exc}")
            return

        status = resp.status_code
        if status in (200, 201, 202, 204, 400, 401, 403, 409, 422):
            code = None
            try:
                payload = resp.json()
                if isinstance(payload, dict):
                    code = payload.get("code")
            except ValueError:
                payload = None

            if code == "ROUTE_NOT_FOUND":
                self._record(name, method, path, status, "FAIL", elapsed, "路由不存在")
                return
            if status == 400 and code is None:
                self._record(
                    name,
                    method,
                    path,
                    status,
                    "FAIL",
                    elapsed,
                    "400 但响应不是业务 JSON，无法确认路由",
                )
                return

            detail = f"路由存在，返回 {code}" if code else "路由存在"
            self._record(name, method, path, status, "PROBE", elapsed, f"{detail}（未写入数据）")
            return

        self._record(name, method, path, status, "FAIL", elapsed, self._error_note(resp))

    def skip(self, name: str, method: str, path: str, reason: str) -> None:
        self._record(name, method, path, None, "SKIP", note=reason)

    # ---------- 工具 ----------

    @staticmethod
    def _error_note(resp: requests.Response) -> str:
        try:
            payload = resp.json()
        except ValueError:
            text = resp.text.strip().replace("\n", " ")
            return text[:120] if text else "<empty body>"
        if isinstance(payload, dict):
            code = payload.get("code", "")
            message = payload.get("message", "")
            return f"{code} {message}".strip() or json.dumps(payload, ensure_ascii=False)[:120]
        return json.dumps(payload, ensure_ascii=False)[:120]

    @staticmethod
    def _shape_note(data: dict[str, Any]) -> str:
        if isinstance(data.get("items"), list):
            return f"items={len(data['items'])}"
        if isinstance(data.get("days"), list):
            return f"days={len(data['days'])}"
        if "user" in data and isinstance(data["user"], dict):
            return f"user={data['user'].get('username', '')}"
        if "state" in data:
            return f"state={data['state']}"
        return ""

    @staticmethod
    def _first_item_id(payload: dict[str, Any] | None) -> str | None:
        if not payload:
            return None
        items = payload.get("items")
        if isinstance(items, list) and items and isinstance(items[0], dict):
            value = items[0].get("id")
            if isinstance(value, str):
                return value
        return None

    def _discover_json(
        self,
        path: str,
        *,
        auth: bool = False,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        try:
            resp, _, _ = self._request("GET", path, auth=auth, params=params)
        except requests.RequestException:
            return None
        if resp.status_code != 200:
            return None
        try:
            payload = resp.json()
        except ValueError:
            return None
        return payload if isinstance(payload, dict) else None

    def discover(self) -> None:
        print("正在发现可用的真实 ID ...")

        topics = self._discover_json("/topics", params={"limit": 20})
        self.discovered["topic_id"] = self._first_item_id(topics) or FALLBACK_TOPIC_ID

        tags = self._discover_json("/tags")
        tag_slug = None
        if tags:
            items = tags.get("items")
            if isinstance(items, list) and items and isinstance(items[0], dict):
                slug = items[0].get("slug")
                if isinstance(slug, str):
                    tag_slug = slug
        self.discovered["tag_slug"] = tag_slug or FALLBACK_TAG_SLUG

        self.discovered["user_id"] = FALLBACK_USER_ID
        self.discovered["file_id"] = FALLBACK_FILE_ID
        self.discovered["submission_id"] = None
        self.discovered["session_user"] = None

        if not self.session_cookie:
            print("未提供 Session，需要 Cookie 的接口将跳过。")
            return

        session_info = self._discover_json("/session", auth=True)
        if session_info:
            user = session_info.get("user")
            if isinstance(user, dict):
                user_id = user.get("id")
                username = user.get("username")
                if isinstance(user_id, str):
                    self.discovered["user_id"] = user_id
                    self.discovered["session_user"] = f"{username or '?'} ({user_id})"
                avatar = user.get("avatar")
                if isinstance(avatar, dict) and avatar.get("type") == "CUSTOM" and isinstance(avatar.get("id"), str):
                    self.discovered["avatar_file_id"] = avatar["id"]

        files = self._discover_json("/files", auth=True, params={"scope": "OWN", "state": "READY"})
        file_id = self._first_item_id(files)
        if file_id:
            self.discovered["file_id"] = file_id
        elif self.discovered.get("avatar_file_id"):
            self.discovered["file_id"] = self.discovered["avatar_file_id"]

        # contentRole 与 status 均为必填；遍历组合尽量找到一个真实 submissionId
        for content_role in ("TOPIC_REPLY", "TOPIC_FIRST_POST", "WORK_COMMENT"):
            for status in ("PENDING", "REJECTED"):
                submissions = self._discover_json(
                    "/post-submissions",
                    auth=True,
                    params={
                        "contentRole": content_role,
                        "status": status,
                        "limit": 100,
                    },
                )
                submission_id = self._first_item_id(submissions)
                if submission_id:
                    self.discovered["submission_id"] = submission_id
                    break
            if self.discovered["submission_id"]:
                break

        summary = ", ".join(
            f"{key}={value}" for key, value in self.discovered.items() if value and key != "session_user"
        )
        print(f"发现结果: {summary}")
        if self.discovered.get("session_user"):
            print(f"当前 Session 用户: {self.discovered['session_user']}")

    # ---------- 测试集 ----------

    def run(self) -> None:
        self.discover()

        user_id = self.discovered["user_id"]
        topic_id = self.discovered["topic_id"]
        tag_slug = self.discovered["tag_slug"]
        file_id = self.discovered["file_id"]
        submission_id = self.discovered["submission_id"]

        self.group("会话与鉴权")
        self.test_json("获取当前会话", "GET", "/session", auth=True, keys=("user", "createdAt", "expiresAt", "silence"))
        self.test_json("获取入站考试状态", "GET", "/entrance-exam", auth=True, keys=("state",))

        self.group("主题与投稿")
        self.test_json("主题列表", "GET", "/topics", params={"limit": 20}, keys=("items", "pageInfo"))
        self.test_json(
            "首页推荐",
            "GET",
            "/topic-recommendations",
            params={"sort": "recommended", "limit": 20},
            keys=("items", "pageInfo"),
        )
        self.test_json("主题详情", "GET", f"/topics/{topic_id}", keys=("id", "title"))
        self.test_json(
            "楼层列表",
            "GET",
            f"/topics/{topic_id}/posts",
            params={"limit": 50, "sort": "hot"},
            keys=("items", "pageInfo"),
        )
        self.test_json(
            "投稿审核列表（回帖 / PENDING）",
            "GET",
            "/post-submissions",
            auth=True,
            params={"contentRole": "TOPIC_REPLY", "status": "PENDING", "limit": 100},
            keys=("items", "pageInfo"),
        )
        self.test_json(
            "投稿审核列表（主题 / REJECTED）",
            "GET",
            "/post-submissions",
            auth=True,
            params={"contentRole": "TOPIC_FIRST_POST", "status": "REJECTED", "limit": 100},
            keys=("items", "pageInfo"),
        )
        self.test_json(
            "投稿审核列表（按 topicId 过滤）",
            "GET",
            "/post-submissions",
            auth=True,
            params={
                "contentRole": "TOPIC_REPLY",
                "status": "PENDING",
                "topicId": topic_id,
                "limit": 20,
            },
            keys=("items", "pageInfo"),
        )
        if submission_id:
            self.test_json(
                "投稿详情",
                "GET",
                f"/post-submissions/{submission_id}",
                auth=True,
                keys=("id", "status"),
            )
        else:
            self.skip("投稿详情", "GET", "/post-submissions/{submissionId}", "没有可用的 submissionId")

        self.group("用户")
        self.test_json("用户资料", "GET", f"/users/{user_id}", keys=("id", "username"))
        self.test_json("查询用户邮箱", "GET", f"/users/{user_id}/email", auth=True, keys=("email", "verifiedAt"))
        self.test_json(
            "关注列表",
            "GET",
            f"/users/{user_id}/following",
            params={"limit": 20},
            keys=("items", "pageInfo"),
        )
        self.test_json(
            "粉丝列表",
            "GET",
            f"/users/{user_id}/followers",
            params={"limit": 20},
            keys=("items", "pageInfo"),
        )
        self.test_json(
            "用户发布的主题",
            "GET",
            f"/users/{user_id}/topics",
            params={"limit": 20},
            keys=("items", "pageInfo"),
        )
        self.test_json(
            "用户的回帖",
            "GET",
            f"/users/{user_id}/posts",
            params={"role": "reply", "limit": 20},
            keys=("items", "pageInfo"),
        )
        self.test_json("精选主题", "GET", f"/users/{user_id}/featured-topics", keys=("items",))
        self.test_json(
            "用户的合集",
            "GET",
            f"/users/{user_id}/topic-collections",
            params={"limit": 20},
            keys=("items", "pageInfo"),
        )
        self.test_json("用户获得的徽章", "GET", f"/users/{user_id}/badges", keys=("items",))
        self.test_json("徽章展示设置", "GET", f"/users/{user_id}/badge-display", keys=("mode",))
        self.test_json(
            "批量查询展示徽章",
            "GET",
            "/user-badge-displays",
            params={"userIds": user_id},
            keys=("items",),
        )
        self.test_json(
            "用户动态",
            "GET",
            f"/users/{user_id}/profile-activities",
            params={"year": CURRENT_YEAR, "limit": 50},
            keys=("items", "pageInfo"),
        )
        self.test_json(
            "用户贡献日历",
            "GET",
            f"/users/{user_id}/level-contributions/{CURRENT_YEAR}",
            keys=("year", "days"),
        )
        self.test_json(
            "当前用户动态",
            "GET",
            "/profile-activities",
            auth=True,
            params={"year": CURRENT_YEAR, "limit": 50},
            keys=("items", "pageInfo"),
        )
        self.test_json(
            "当前用户贡献日历",
            "GET",
            f"/level-contributions/{CURRENT_YEAR}",
            auth=True,
            keys=("year", "days"),
        )
        self.test_json("等级进度", "GET", "/level-progress", auth=True, keys=("currentLevel",))
        self.test_json(
            "内容长度上限",
            "GET",
            "/content-length-limit",
            auth=True,
            keys=("level", "topicMaxLength", "replyMaxLength"),
        )
        self.test_json(
            "合集配额用量",
            "GET",
            "/topic-collection-usage",
            auth=True,
            keys=("currentLevel", "limitCount", "usedCount", "remainingCount"),
        )
        self.test_json(
            "文件存储配额",
            "GET",
            "/file-storage",
            auth=True,
            keys=("usedBytes", "limitBytes", "remainingBytes"),
        )
        self.test_json(
            "我的书签",
            "GET",
            "/bookmarks",
            auth=True,
            params={"limit": 20},
            keys=("items", "pageInfo"),
        )
        self.test_json("预设头像列表", "GET", "/avatar-presets", keys=("items",))

        self.group("标签")
        self.test_json("全部分区标签", "GET", "/tags", keys=("items",))
        self.test_json(
            "分区侧边子标签",
            "GET",
            f"/tags/{tag_slug}/sidebar-links",
            keys=("source", "items"),
        )

        self.group("媒体")
        self.test_json(
            "我的文件列表",
            "GET",
            "/files",
            auth=True,
            params={"scope": "OWN", "state": "READY"},
            keys=("items", "pageInfo"),
        )
        self.test_image("获取文件", f"/files/{file_id}")
        self.test_image("预设头像", "/avatars/1")
        emoji_read = uuid.uuid4()
        self.test_image("表情图片", f"/emojis/{EMOJI_NAME}/image?emoji-read={emoji_read}")

        self.group("通知")
        self.test_json(
            "通知汇总",
            "GET",
            "/notification-summary",
            auth=True,
            keys=("unreadCount", "unreadCountByType"),
        )

        self.group("写接口路由探测（不发送 Session，不写入数据）")
        self.probe_write("登录（空请求体）", "POST", "/session", with_body=True)
        self.probe_write("登出（不带 Cookie）", "DELETE", "/session", with_body=False)
        self.probe_write("发起注册（空请求体）", "POST", "/registrations", with_body=True)
        self.probe_write(
            "验证邮箱（空请求体）",
            "PATCH",
            "/registrations/00000000-0000-0000-0000-000000000000",
            with_body=False,
        )
        self.probe_write("发布内容（空请求体）", "POST", "/posts", with_body=True)
        self.probe_write("修改个人资料（空请求体）", "PATCH", f"/users/{user_id}", with_body=True)
        self.probe_write("上传图片（空请求体）", "POST", "/files", with_body=True)
        self.probe_write("开始一次考试（空请求体）", "POST", "/entrance-exam/attempts", with_body=True)
        self.probe_write(
            "提交答案（空请求体）",
            "PATCH",
            "/entrance-exam/attempts/00000000-0000-0000-0000-000000000000/current-question",
            with_body=True,
        )
        self.probe_write(
            "上报阅读批次（空请求体）",
            "PUT",
            f"/reading-sessions/{uuid.uuid4()}/batches/1",
            with_body=True,
        )

        self.group("未实际执行")
        self.skip("登录并获取新 Session", "POST", "/session", "需要阿里云 CAPTCHA，脚本无法生成")
        self.skip("登出", "DELETE", "/session", "会注销当前 Session，避免影响调用方")
        self.skip(
            "取当前题",
            "GET",
            "/entrance-exam/attempts/{id}/current-question",
            "需要先创建考试 attempt，脚本不发起写操作",
        )
        self.skip("真实发帖 / 回帖", "POST", "/posts", "会产生真实内容")
        self.skip("真实发起注册 / 验证邮箱", "POST", "/registrations", "会产生注册会话并修改账号")
        self.skip("真实开始考试 / 提交答案", "POST", "/entrance-exam/attempts", "会消耗考试次数并写入答案")
        self.skip("真实上传文件", "POST", "/files", "会产生真实文件并占用配额")
        self.skip("真实修改资料", "PATCH", f"/users/{user_id}", "会修改账号资料")
        self.skip("真实上报阅读批次", "PUT", "/reading-sessions/{id}/batches/{no}", "会写入阅读埋点")

    def report(self, json_out: str | None) -> int:
        passed = sum(1 for r in self.results if r.verdict == "PASS")
        failed = sum(1 for r in self.results if r.verdict == "FAIL")
        skipped = sum(1 for r in self.results if r.verdict == "SKIP")
        probed = sum(1 for r in self.results if r.verdict == "PROBE")

        print("\n" + "=" * 90)
        print(f"总计: {len(self.results)} 项 | PASS {passed} | FAIL {failed} | SKIP {skipped} | PROBE {probed}")

        if failed:
            print("\n失败项:")
            for result in self.results:
                if result.verdict == "FAIL":
                    print(f"  - {result.name}: {result.method} {result.path} -> {result.status} {result.note}")

        if json_out:
            with open(json_out, "w", encoding="utf-8") as handle:
                json.dump(
                    {
                        "base_url": self.base_url,
                        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                        "summary": {
                            "total": len(self.results),
                            "passed": passed,
                            "failed": failed,
                            "skipped": skipped,
                            "probed": probed,
                        },
                        "results": [asdict(result) for result in self.results],
                    },
                    handle,
                    ensure_ascii=False,
                    indent=2,
                )
            print(f"\nJSON 报告已写入: {json_out}")

        return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="验证 Pickcat 文档中记录的全部 API")
    parser.add_argument(
        "--session",
        default=os.environ.get("PICKCAT_SESSION"),
        help="pickcat_session 的值；也可通过环境变量 PICKCAT_SESSION 传入",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("PICKCAT_BASE_URL", DEFAULT_BASE_URL),
        help=f"API 基础地址，默认 {DEFAULT_BASE_URL}",
    )
    parser.add_argument("--json-out", help="把结果另存为 JSON 报告")
    args = parser.parse_args()

    cookie = args.session.strip() if args.session else None
    if not cookie:
        print("提示: 未提供 Session，需要 Cookie 的接口会被跳过。\n")

    verifier = Verifier(args.base_url, cookie)
    try:
        verifier.run()
        return verifier.report(args.json_out)
    except KeyboardInterrupt:
        print("\n已中断")
        return 130


if __name__ == "__main__":
    sys.exit(main())
