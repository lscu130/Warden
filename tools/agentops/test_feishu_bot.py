"""
测试飞书自定义机器人 Webhook 是否可用。

功能：
1. 从环境变量读取 FEISHU_WEBHOOK_URL 和 FEISHU_SECRET
2. 生成飞书签名
3. 向飞书群发送一条测试消息

注意：
- 不要把 webhook 和 secret 写死在代码里
- 不要把 .env 提交到 GitHub
"""

import base64
import hashlib
import hmac
import json
import os
import time
import urllib.request


def make_feishu_sign(timestamp: str, secret: str) -> str:
    """
    生成飞书自定义机器人签名。

    飞书签名算法：
    string_to_sign = timestamp + "\n" + secret
    sign = base64(hmac_sha256(string_to_sign, ""))
    """
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(hmac_code).decode("utf-8")


def send_feishu_text(webhook_url: str, secret: str, text: str) -> None:
    """
    发送文本消息到飞书群机器人。
    """
    timestamp = str(int(time.time()))
    sign = make_feishu_sign(timestamp, secret)

    payload = {
        "timestamp": timestamp,
        "sign": sign,
        "msg_type": "text",
        "content": {
            "text": text,
        },
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        body = response.read().decode("utf-8")
        print(body)


def main() -> None:
    """
    主入口：读取环境变量并发送测试消息。
    """
    webhook_url = os.environ.get("FEISHU_WEBHOOK_URL")
    secret = os.environ.get("FEISHU_SECRET")

    if not webhook_url:
        raise RuntimeError("缺少环境变量：FEISHU_WEBHOOK_URL")

    if not secret:
        raise RuntimeError("缺少环境变量：FEISHU_SECRET")

    send_feishu_text(
        webhook_url=webhook_url,
        secret=secret,
        text="[Warden-AgentOps] 飞书机器人测试成功。本地脚本已经可以推送消息。",
    )


if __name__ == "__main__":
    main()