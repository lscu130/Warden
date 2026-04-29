"""
Feishu notification module.

功能：
1. 从环境变量读取飞书 Webhook 和 Secret
2. 生成飞书自定义机器人签名
3. 向飞书群发送文本消息

用途：
- 给 agent runner 发送任务开始、完成、失败消息
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
    """
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(hmac_code).decode("utf-8")


def send_feishu_text(text: str) -> None:
    """
    向飞书群发送文本消息。
    """
    webhook_url = os.environ.get("FEISHU_WEBHOOK_URL")
    secret = os.environ.get("FEISHU_SECRET")

    if not webhook_url:
        raise RuntimeError("缺少环境变量：FEISHU_WEBHOOK_URL")

    if not secret:
        raise RuntimeError("缺少环境变量：FEISHU_SECRET")

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

    with urllib.request.urlopen(request, timeout=15) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)