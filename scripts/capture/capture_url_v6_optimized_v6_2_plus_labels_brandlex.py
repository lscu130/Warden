#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""EVT Dataset Crawler v6 (new-structure only)

目标
- 不生成 CSV，不生成 log 文件
- 失败/不可访问：不创建样本目录（只 stdout 打印原因）
- 成功样本才创建目录并落盘，输出“完整新结构”（A~G），不再兼容旧结构文件名

A) 元信息
  - meta.json / url.json / env.json
B) 跳转链
  - redirect_chain.json
C) 页面内容
  - html_raw.html / html_rendered.html / visible_text.txt
D) 表单结构
  - forms.json
E) 视觉
  - screenshot_viewport.png / screenshot_full.png
F) 轻量交互（可选）
  - actions.jsonl / after_action/step1_*（一次保守点击）
G) 网络证据（可选）
  - network.har / net_summary.json
H) 自动弱标签（新增）
  - auto_labels.json

实现要点
- 每个 URL 单独 new_context(record_har_path=...)：HAR 会在 context.close() 时落盘
- 截图质量闸门：纯色/低信息量/过小截图 => 同一次尝试内“再等+再截”，仍不行则失败
- 错误/拦截页识别：title/innerText/html 命中 502、Access Denied、captcha 等 => 直接失败

依赖
- playwright
- pillow（可选，用于截图“纯色/低信息量”检测）
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import ipaddress
import json
import math
import os
import re
import sys
import tempfile
import time
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
LABELING_DIR = REPO_ROOT / "scripts" / "labeling"
if str(LABELING_DIR) not in sys.path:
    sys.path.insert(0, str(LABELING_DIR))

try:
    from Warden_auto_label_utils_brandlex import derive_auto_labels, derive_rule_labels
except ModuleNotFoundError:
    from evt_auto_label_utils_brandlex import derive_auto_labels, derive_rule_labels

# Pillow 可选：用于像素级“纯色/低信息量”检测
try:
    from PIL import Image, ImageStat
except Exception:
    Image = None
    ImageStat = None

try:
    from playwright_stealth import Stealth
except Exception:
    Stealth = None


# =========================
# 可配置路径（你按需改）
# =========================
EVT_DATASET_PHISH_ROOT = Path(r"C:\Users\lscu1\Desktop\EVT Dataset\phish1")
EVT_DATASET_BENIGN_ROOT = Path(r"C:\Users\lscu1\Desktop\EVT Dataset\benign")

# 输入文件（也可用命令行传参覆盖）
DEFAULT_INPUT_PATH = Path(r"C:\Users\lscu1\Desktop\EVT Dataset\phish44.txt")
DEFAULT_INPUT_FORMAT = "csv"  # csv / txt
DEFAULT_CSV_URL_COLUMN = "url"

# 浏览器设置
BROWSER_CHANNEL = "chrome"  # 机器没装对应通道会报错；删掉 channel 就用 Playwright 自带 Chromium
HEADLESS = True
VIEWPORT = {"width": 1365, "height": 768}
NAV_TIMEOUT_MS = 60_000
POST_NAV_NETIDLE_MS = 2_500
RETRY_VISIT = 2
DEFAULT_GOTO_WAIT_UNTIL = "commit"
BROWSER_LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-setuid-sandbox",
]
POST_GOTO_DOMCONTENTLOADED_TIMEOUT_MS = 30_000
POST_GOTO_HYDRATION_WAIT_MS = 2_000
GOOGLE_CONSENT_WAIT_MS = 1_500
GOOGLE_CONSENT_SELECTORS = [
    'button:has-text("I agree")',
    'button:has-text("Accept all")',
    'button:has-text("同意")',
    'button:has-text("全部接受")',
]

# 显式代理（可选）
PROXY_SERVER: Optional[str] = None
PROXY_USERNAME: Optional[str] = None
PROXY_PASSWORD: Optional[str] = None

# 安全/副作用控制
ACCEPT_DOWNLOADS = False
SERVICE_WORKERS = "block"
JAVA_SCRIPT_ENABLED = True
IGNORE_HTTPS_ERRORS = False
BYPASS_CSP = False

# 允许继续的状态码
OK_STATUSES = {100, 101, 200, 201, 202, 203, 204, 205, 206}

# =========================
# 截图质量闸门参数（可调）
# =========================
MIN_PNG_BYTES = 12_000          # 太小通常是空白/错误页
DOM_TEXT_MIN_LEN = 40          # innerText 太短通常是错误/拦截页
DOMINANT_COLOR_MAX = 0.985     # 主色占比太高 => 近似纯色
GRAY_STDDEV_MIN = 3.0          # 灰度标准差过低 => 低信息量
SECOND_PASS_WAIT_MS = 1800

PRINT_REQUEST_FAILED = True

# =========================
# A~G 输出开关
# =========================
RECORD_NET_EVIDENCE_LITE = True
RECORD_HAR = False  # Ignored when RECORD_NET_EVIDENCE_LITE is True.
SAVE_FULLPAGE_SHOT = True
SAVE_RENDERED_HTML = True
SAVE_RAW_HTML = True
SAVE_VISIBLE_TEXT = True
SAVE_FORMS_JSON = True
ENABLE_STEP1_ACTION = False
STEP1_WAIT_MS = 1500
MAX_VISIBLE_TEXT_CHARS = 120_000
DRY_RUN = False
SAVE_AUTO_LABELS = True
SAVE_RULE_LABELS = False
BRAND_LEXICON_PATH = ""

# =========================
# Variants (cloaking) capture
# =========================
ENABLE_VARIANTS = False
MAX_VARIANT_COUNT = 4
VARIANT_TOTAL_TIMEOUT_MS = 60_000
VARIANTS = [
    {
        "name": "desktop_zh",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36",
        "locale": "zh-CN",
        "timezone_id": "Asia/Shanghai",
        "viewport": {"width": 1365, "height": 768},
        "headless": True,
    },
    {
        "name": "desktop_en",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36",
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "viewport": {"width": 1365, "height": 768},
        "headless": True,
    },
]

# 轻度网络收敛：阻断 websocket / eventsource / media（减少无关请求）
BLOCK_RESOURCE_TYPES = {"websocket", "eventsource", "media", "font", "manifest"}
ROUTE_INTERCEPT_ENABLED = True

ERROR_HINT_PATTERNS = [
    r"\b502\b", r"bad gateway",
    r"\b403\b", r"forbidden", r"access denied",
    r"attention required", r"verify you are human",
    r"captcha", r"cloudflare",
    r"service unavailable", r"\b503\b",
    r"temporarily unavailable",
]

# Precompiled regexes (tiny speed-up + avoids recompiling inside hot loops)
ERROR_HINT_REGEXES = [re.compile(p, re.I) for p in ERROR_HINT_PATTERNS]
BENIGN_RELAXED_ERROR_HINT_PATTERNS = [p for p in ERROR_HINT_PATTERNS if p != r"cloudflare"]
BENIGN_RELAXED_ERROR_HINT_REGEXES = [re.compile(p, re.I) for p in BENIGN_RELAXED_ERROR_HINT_PATTERNS]
RE_WS = re.compile(r"\s+")
RE_MANY_NL = re.compile(r"\n{3,}")
RE_URL_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
RE_SAFE_FOLDER = re.compile(r"[^A-Za-z0-9._-]+")

STEP1_CTA_KEYWORDS = [
    "login", "log in", "sign in", "continue", "next", "verify", "submit",
    "\u767b\u5f55", "\u4e0b\u4e00\u6b65", "\u7ee7\u7eed", "\u9a8c\u8bc1", "\u786e\u8ba4",
]
STEP1_NEGATIVE_KEYWORDS = [
    "privacy", "terms", "policy", "cookie", "gdpr",
    "logout", "log out", "sign out", "delete", "unsubscribe",
    "\u9690\u79c1", "\u6761\u6b3e", "\u653f\u7b56", "\u9000\u51fa", "\u5220\u9664",
]
STEP1_AD_CLASS_HINTS = ["ad", "ads", "sponsor", "promo", "banner"]
STEP1_SOCIAL_HINTS = ["share", "facebook", "twitter", "wechat", "weibo", "linkedin"]
STEP1_MIN_SCORE = 10

MAX_TEXT_HEAD_CHARS = 1024
MAX_HTML_CHARS = 2_000_000
MAX_NET_TIMING_SAMPLES = 2_000
MAX_FULLPAGE_HEIGHT = 12_000


def now_utc_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def normalize_url(u: str) -> str:
    u = u.strip()
    if not u:
        return ""
    if not RE_URL_SCHEME.match(u):
        u = "https://" + u
    return u


def truncate_large_text(text: Optional[str], max_chars: int, marker: str = "\n\n[TRUNCATED]") -> str:
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    keep = max(0, max_chars - len(marker))
    return text[:keep] + marker


def _is_ip_address(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _host_from_url(url: str) -> str:
    try:
        p = urlparse(url)
    except Exception:
        return ""
    return (p.hostname or "").lower()


def sanitize_url_for_summary(url: str) -> str:
    if not url:
        return ""
    try:
        p = urlparse(url)
    except Exception:
        return ""
    host = (p.hostname or "").lower()
    if not p.scheme or not host:
        return url.split("?", 1)[0].split("#", 1)[0]
    port = f":{p.port}" if p.port else ""
    path = p.path or "/"
    return f"{p.scheme}://{host}{port}{path}"


def origin_from_url(url: str) -> str:
    if not url:
        return ""
    try:
        p = urlparse(url)
    except Exception:
        return ""
    host = (p.hostname or "").lower()
    if not p.scheme or not host:
        return ""
    port = f":{p.port}" if p.port else ""
    return f"{p.scheme}://{host}{port}"


def _fallback_etld1(host: str) -> str:
    host = host.lower()
    if _is_ip_address(host):
        return host
    parts = [p for p in host.split(".") if p]
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return host


ETLD1_MODE = "fallback"
try:
    from publicsuffix2 import get_sld as _get_sld

    def etld1_from_host(host: str) -> str:
        host = host.lower()
        if not host:
            return ""
        if _is_ip_address(host):
            return host
        sld = _get_sld(host)
        return sld or host

    ETLD1_MODE = "publicsuffix2"
except Exception:
    try:
        import tldextract

        _tld_extract = tldextract.TLDExtract(suffix_list_urls=None)

        def etld1_from_host(host: str) -> str:
            host = host.lower()
            if not host:
                return ""
            if _is_ip_address(host):
                return host
            ext = _tld_extract(host)
            if ext.domain and ext.suffix:
                return f"{ext.domain}.{ext.suffix}".lower()
            return host

        ETLD1_MODE = "tldextract"
    except Exception:
        def etld1_from_host(host: str) -> str:
            if not host:
                return ""
            return _fallback_etld1(host)

        ETLD1_MODE = "fallback"


def get_etld1_from_url(url: str) -> str:
    return etld1_from_host(_host_from_url(url))


def percentile(values: List[float], p: float) -> Optional[float]:
    if not values:
        return None
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    k = (len(xs) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return xs[int(k)]
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def _sorted_counter(counter: Counter) -> List[Tuple[str, int]]:
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))


def _group_status_counts(status_counter: Counter) -> Dict[str, int]:
    out = {"2xx": 0, "3xx": 0, "4xx": 0, "5xx": 0, "other": 0}
    for status, count in status_counter.items():
        try:
            s = int(status)
        except Exception:
            out["other"] += count
            continue
        if 200 <= s < 300:
            out["2xx"] += count
        elif 300 <= s < 400:
            out["3xx"] += count
        elif 400 <= s < 500:
            out["4xx"] += count
        elif 500 <= s < 600:
            out["5xx"] += count
        else:
            out["other"] += count
    return out


def sanitize_variant_name(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", (name or "").strip()).strip("_")
    return safe or "variant"


def make_proxy_config(server: Optional[str], username: Optional[str], password: Optional[str]) -> Optional[dict]:
    if not server:
        return None
    proxy = {"server": server}
    if username:
        proxy["username"] = username
    if password:
        proxy["password"] = password
    return proxy


def normalize_proxy_config(proxy_cfg: Optional[dict]) -> Optional[dict]:
    if not proxy_cfg:
        return None
    if isinstance(proxy_cfg, str):
        return {"server": proxy_cfg}
    if not isinstance(proxy_cfg, dict):
        return None
    server = proxy_cfg.get("server") or ""
    if not server:
        return None
    proxy = {"server": server}
    username = proxy_cfg.get("username")
    password = proxy_cfg.get("password")
    if username:
        proxy["username"] = username
    if password:
        proxy["password"] = password
    return proxy


def proxy_key(proxy_cfg: Optional[dict]) -> Tuple[str, str, str]:
    if not proxy_cfg:
        return ("", "", "")
    return (
        str(proxy_cfg.get("server") or ""),
        str(proxy_cfg.get("username") or ""),
        str(proxy_cfg.get("password") or ""),
    )


# =========================
# Playwright browser pool (resilient)
# =========================
def is_driver_connection_closed_error(exc: Exception) -> bool:
    """Heuristic: Playwright driver/browser died, so pipe got closed.

    Typical message:
      - Browser.new_context: Connection closed while reading from the driver
    """
    hay = f"{type(exc).__name__}: {exc} {repr(exc)}".lower()
    if "connection closed while reading from the driver" in hay:
        return True
    if "browser.new_context" in hay and "connection closed" in hay:
        return True
    if "targetclosederror" in hay:
        return True
    return False


def is_navigation_timeout_error(exc: Exception) -> bool:
    hay = f"{type(exc).__name__}: {exc} {repr(exc)}".lower()
    return "timeout" in hay and "exceeded" in hay


def require_stealth_runtime() -> "Stealth":
    if Stealth is None:
        raise RuntimeError(
            "playwright-stealth is required for the current capture hardening patch. "
            "Install it with: python -m pip install playwright-stealth"
        )
    return Stealth()


def apply_stealth_sync(page) -> bool:
    helper = require_stealth_runtime()
    helper.apply_stealth_sync(page)
    return True


def is_google_like_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    return "google" in host.split(".")


def handle_google_consent(page) -> Tuple[bool, bool]:
    current_url = ""
    try:
        current_url = page.url or ""
    except Exception:
        current_url = ""
    if not is_google_like_url(current_url):
        return False, False

    attempted = True
    for selector in GOOGLE_CONSENT_SELECTORS:
        try:
            page.locator(selector).first.click(timeout=2_500)
            try:
                page.wait_for_timeout(GOOGLE_CONSENT_WAIT_MS)
            except Exception:
                pass
            return attempted, True
        except Exception:
            continue
    return attempted, False


def goto_with_fallback(page, url: str, nav_timeout_ms: int, goto_wait_until: str):
    wait_until = (goto_wait_until or DEFAULT_GOTO_WAIT_UNTIL).strip().lower() or DEFAULT_GOTO_WAIT_UNTIL
    fallback_used = False
    try:
        resp = page.goto(url, wait_until=wait_until, timeout=nav_timeout_ms)
        return resp, wait_until, fallback_used
    except Exception as exc:
        if wait_until == "load" and is_navigation_timeout_error(exc):
            fallback_wait_until = "domcontentloaded"
            print(f"  [INFO] goto wait_until=load timed out; retrying with wait_until={fallback_wait_until}")
            resp = page.goto(url, wait_until=fallback_wait_until, timeout=nav_timeout_ms)
            fallback_used = True
            return resp, fallback_wait_until, fallback_used
        raise


class BrowserPoolManager:
    """Cache browsers by (headless, proxy) and relaunch on driver disconnect."""

    def __init__(self, chromium, browser_channel: str = ""):
        self.chromium = chromium
        self.browser_channel = (browser_channel or "").strip()
        self.pool: Dict[Tuple, object] = {}
        self.effective_channels: Dict[Tuple, str] = {}

    def _launch(self, key: Tuple, headless: bool, proxy_cfg: Optional[dict]):
        launch_kwargs = {"headless": headless, "args": list(BROWSER_LAUNCH_ARGS)}
        if proxy_cfg:
            launch_kwargs["proxy"] = proxy_cfg
        if self.browser_channel:
            try:
                launch_kwargs["channel"] = self.browser_channel
                browser = self.chromium.launch(**launch_kwargs)
                self.effective_channels[key] = self.browser_channel
                return browser
            except Exception as exc:
                print(
                    f"  [WARN] launch with channel={self.browser_channel} failed; "
                    f"retrying with bundled Chromium. error={repr(exc)}"
                )
                launch_kwargs.pop("channel", None)

        browser = self.chromium.launch(**launch_kwargs)
        self.effective_channels[key] = "chromium"
        return browser

    def get_browser(self, headless: bool, proxy_cfg: Optional[dict]):
        key = (headless,) + proxy_key(proxy_cfg)
        if key not in self.pool:
            self.pool[key] = self._launch(key, headless, proxy_cfg)
        return self.pool[key]

    def relaunch(self, headless: bool, proxy_cfg: Optional[dict]):
        key = (headless,) + proxy_key(proxy_cfg)
        old = self.pool.get(key)
        if old is not None:
            try:
                old.close()
            except Exception:
                pass
        self.pool[key] = self._launch(key, headless, proxy_cfg)
        return self.pool[key]

    def get_effective_channel(self, headless: bool, proxy_cfg: Optional[dict]) -> str:
        key = (headless,) + proxy_key(proxy_cfg)
        return self.effective_channels.get(key, self.browser_channel or "chromium")

    def new_context_resilient(
        self,
        headless: bool,
        proxy_cfg: Optional[dict],
        context_kwargs: dict,
        max_relaunch: int = 1,
        warn_prefix: str = "  [WARN]",
    ):
        """Create a new context; if driver connection closes, relaunch browser and retry."""
        last_exc: Optional[Exception] = None
        for attempt in range(max_relaunch + 1):
            browser = self.get_browser(headless, proxy_cfg)
            try:
                return browser.new_context(**context_kwargs)
            except Exception as e:
                last_exc = e
                if attempt >= max_relaunch or not is_driver_connection_closed_error(e):
                    raise
                try:
                    print(f"{warn_prefix} driver disconnected during new_context; relaunching browser and retrying...")
                except Exception:
                    pass
                try:
                    self.relaunch(headless, proxy_cfg)
                except Exception:
                    # if relaunch fails, fall through and raise original
                    break
        if last_exc is not None:
            raise last_exc
        raise RuntimeError("new_context_resilient: unexpected empty error")

    def close_all(self):
        for b in list(self.pool.values()):
            try:
                b.close()
            except Exception:
                pass
        self.pool.clear()


def tokenize_for_diff(text: str, max_tokens: int = 5000) -> List[str]:
    if not text:
        return []
    text = text.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    if not tokens:
        tokens = list(text.strip())
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return tokens


def simhash_tokens(tokens: List[str]) -> Optional[int]:
    if not tokens:
        return None
    counts = Counter(tokens)
    weights = [0] * 64
    for token, weight in counts.items():
        h = hashlib.md5(token.encode("utf-8", errors="ignore")).hexdigest()
        hv = int(h, 16)
        for i in range(64):
            if (hv >> i) & 1:
                weights[i] += weight
            else:
                weights[i] -= weight
    out = 0
    for i, val in enumerate(weights):
        if val >= 0:
            out |= (1 << i)
    return out


def hamming_distance(a: Optional[int], b: Optional[int]) -> Optional[int]:
    if a is None or b is None:
        return None
    return bin(a ^ b).count("1")


def jaccard_similarity(a: set, b: set) -> Optional[float]:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def build_text_features(text: str) -> dict:
    tokens = tokenize_for_diff(text)
    return {
        "len": len(text),
        "simhash": simhash_tokens(tokens),
        "token_set": set(tokens),
    }


def summarize_forms_for_diff(forms_json: dict) -> dict:
    forms = []
    if isinstance(forms_json, dict):
        forms = forms_json.get("forms") or []
    if not isinstance(forms, list):
        forms = []
    has_password = False
    has_otp = False
    input_count = 0
    input_types: Counter = Counter()
    action_domains = set()
    for f in forms:
        if not isinstance(f, dict):
            continue
        if f.get("has_password"):
            has_password = True
        if f.get("has_otp"):
            has_otp = True
        inputs = f.get("inputs") or []
        if isinstance(inputs, list):
            input_count += len(inputs)
            for inp in inputs:
                if isinstance(inp, dict):
                    t = (inp.get("type") or "").lower()
                    if t:
                        input_types[t] += 1
        action = f.get("action_abs") or f.get("action") or ""
        domain = get_etld1_from_url(action)
        if domain:
            action_domains.add(domain)
    return {
        "has_password": has_password,
        "has_otp": has_otp,
        "input_count": input_count,
        "input_types": dict(input_types),
        "action_domains": sorted(action_domains),
    }


def summarize_network_for_diff(net_summary: Optional[dict]) -> dict:
    third_party = set()
    post_targets = set()
    if isinstance(net_summary, dict):
        for d in net_summary.get("third_party_domains") or []:
            if isinstance(d, str):
                third_party.add(d)
        for item in net_summary.get("post_targets") or []:
            if isinstance(item, dict):
                d = item.get("domain_etld1")
                if d:
                    post_targets.add(d)
            elif isinstance(item, str):
                post_targets.add(item)
    return {
        "third_party_domains": sorted(third_party),
        "post_targets": sorted(post_targets),
    }


def diff_visible_text(base_feat: dict, var_feat: dict) -> dict:
    base_set = base_feat.get("token_set") or set()
    var_set = var_feat.get("token_set") or set()
    simhash_distance = hamming_distance(base_feat.get("simhash"), var_feat.get("simhash"))
    return {
        "simhash_distance": simhash_distance,
        "jaccard": jaccard_similarity(base_set, var_set),
        "len_delta": (var_feat.get("len") or 0) - (base_feat.get("len") or 0),
    }


def diff_forms(base_summary: dict, var_summary: dict) -> dict:
    base_domains = set(base_summary.get("action_domains") or [])
    var_domains = set(var_summary.get("action_domains") or [])
    return {
        "has_password_changed": bool(base_summary.get("has_password")) != bool(var_summary.get("has_password")),
        "input_count_delta": (var_summary.get("input_count") or 0) - (base_summary.get("input_count") or 0),
        "action_domain_changed": base_domains != var_domains,
    }


def diff_network(base_summary: dict, var_summary: dict) -> dict:
    base_tp = set(base_summary.get("third_party_domains") or [])
    var_tp = set(var_summary.get("third_party_domains") or [])
    base_post = set(base_summary.get("post_targets") or [])
    var_post = set(var_summary.get("post_targets") or [])
    return {
        "third_party_domains_delta": len(base_tp ^ var_tp),
        "post_targets_changed": base_post != var_post,
    }


def is_large_text_diff(base_len: int, diff: dict) -> bool:
    jaccard = diff.get("jaccard")
    if isinstance(jaccard, (int, float)) and jaccard < 0.6:
        return True
    sim_dist = diff.get("simhash_distance")
    if isinstance(sim_dist, int) and sim_dist >= 20:
        return True
    len_delta = diff.get("len_delta")
    if isinstance(len_delta, int):
        if base_len == 0:
            return len_delta != 0
        if abs(len_delta) / max(base_len, 1) >= 0.5:
            return True
    return False


def sanitize_folder_name(url: str, ts: str, max_len: int = 96) -> str:
    p = urlparse(url)
    base = (p.netloc + p.path).strip("/")
    base = base or (p.netloc or "unknown")
    base = RE_SAFE_FOLDER.sub("_", base).strip("_")
    name = f"{base}_{ts}"
    return name[:max_len]


def iter_urls(input_path: Path, fmt: str, url_col: str) -> Iterator[str]:
    if fmt.lower() == "txt":
        with input_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                yield line
        return

    if fmt.lower() == "csv":
        with input_path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
            reader = csv.DictReader(f)
            if url_col not in (reader.fieldnames or []):
                raise ValueError(f"CSV missing column: {url_col}; fields={reader.fieldnames}")
            for row in reader:
                v = (row.get(url_col) or "").strip()
                if v:
                    yield v
        return

    raise ValueError("input_format must be csv or txt")


def iter_normalized_urls(input_path: Path, fmt: str, url_col: str) -> Iterator[str]:
    for url in iter_urls(input_path, fmt, url_col):
        normalized = normalize_url(url)
        if normalized:
            yield normalized


def count_urls(input_path: Path, fmt: str, url_col: str) -> int:
    return sum(1 for _ in iter_normalized_urls(input_path, fmt, url_col))


def parse_ingest_metadata(raw: str) -> Dict[str, object]:
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid --ingest_metadata_json: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("--ingest_metadata_json must decode to a JSON object")
    return parsed


def ensure_dirs() -> None:
    EVT_DATASET_PHISH_ROOT.mkdir(parents=True, exist_ok=True)
    EVT_DATASET_BENIGN_ROOT.mkdir(parents=True, exist_ok=True)


def unique_out_dir(root: Path, folder: str) -> Path:
    p = root / folder
    if not p.exists():
        return p
    k = 2
    while True:
        p2 = root / f"{folder}_{k}"
        if not p2.exists():
            return p2
        k += 1


def build_redirect_chain_from_response(resp) -> List[str]:
    chain_rev: List[str] = []
    req = resp.request if resp else None
    while req:
        chain_rev.append(req.url)
        req = req.redirected_from
    return list(reversed(chain_rev))


def build_navigation_chain_with_status(resp) -> List[dict]:
    chain_rev: List[dict] = []
    req = resp.request if resp else None
    while req:
        status = None
        try:
            r = req.response()
            status = r.status if r else None
        except Exception:
            status = None
        chain_rev.append({"url": sanitize_url_for_summary(req.url), "status": status})
        req = req.redirected_from
    return list(reversed(chain_rev))


def collect_step1_candidates(page) -> List[dict]:
    return page.evaluate(
        """
        () => {
            const candidates = [];
            const seen = new WeakSet();
            const maxTextLen = 160;
            const isVisible = (el) => {
                if (!el) return false;
                const style = window.getComputedStyle(el);
                if (!style || style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
                    return false;
                }
                const rect = el.getBoundingClientRect();
                if (!rect || rect.width < 2 || rect.height < 2) return false;
                return true;
            };
            const inViewport = (rect) => {
                if (!rect) return false;
                return rect.bottom > 0 && rect.right > 0 && rect.top < window.innerHeight && rect.left < window.innerWidth;
            };
            const cssPath = (el) => {
                if (!el || el.nodeType !== 1) return '';
                if (el.id) return `#${CSS.escape(el.id)}`;
                const parts = [];
                let cur = el;
                while (cur && cur.nodeType === 1 && cur.tagName.toLowerCase() !== 'html') {
                    let tag = cur.tagName.toLowerCase();
                    const parent = cur.parentElement;
                    if (!parent) break;
                    const siblings = Array.from(parent.children).filter(e => e.tagName === cur.tagName);
                    if (siblings.length > 1) {
                        const idx = siblings.indexOf(cur) + 1;
                        tag += `:nth-of-type(${idx})`;
                    }
                    parts.unshift(tag);
                    cur = parent;
                }
                return parts.join(' > ');
            };
            const xpath = (el) => {
                if (!el || el.nodeType !== 1) return '';
                if (el.id) return `//*[@id="${el.id.replace(/"/g, '\\"')}"]`;
                const parts = [];
                let cur = el;
                while (cur && cur.nodeType === 1) {
                    let idx = 1;
                    let sib = cur.previousSibling;
                    while (sib) {
                        if (sib.nodeType === 1 && sib.tagName === cur.tagName) idx += 1;
                        sib = sib.previousSibling;
                    }
                    parts.unshift(`${cur.tagName.toLowerCase()}[${idx}]`);
                    cur = cur.parentElement;
                }
                return '/' + parts.join('/');
            };
            const safeText = (el) => {
                let t = (el.innerText || el.value || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim();
                t = t.replace(/\\s+/g, ' ');
                if (t.length > maxTextLen) t = t.slice(0, maxTextLen);
                return t;
            };
            const hasOtpField = (root) => {
                if (!root) return false;
                return !!root.querySelector('input[name*="otp" i],input[id*="otp" i],input[autocomplete*="one-time" i]');
            };
            const hasPasswordField = (root) => {
                if (!root) return false;
                return !!root.querySelector('input[type="password"]');
            };
            const isNearSensitive = (el, root) => {
                if (!root) return false;
                return root.contains(el) && (hasPasswordField(root) || hasOtpField(root));
            };
            const addCandidate = (el, meta) => {
                if (!el || seen.has(el)) return;
                seen.add(el);
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                const form = el.closest('form');
                const attrs = {
                    id: el.getAttribute('id') || '',
                    name: el.getAttribute('name') || '',
                    type: (el.getAttribute('type') || '').toLowerCase(),
                    role: el.getAttribute('role') || '',
                    'aria-label': el.getAttribute('aria-label') || '',
                    class: el.getAttribute('class') || '',
                    href: el.getAttribute('href') || '',
                };
                const formAction = form ? (form.getAttribute('action') || '') : '';
                const formMethod = form ? (form.getAttribute('method') || '').toUpperCase() : '';
                candidates.push({
                    selector: cssPath(el),
                    xpath: xpath(el),
                    text: safeText(el),
                    tag: el.tagName.toLowerCase(),
                    attributes: attrs,
                    visible: isVisible(el),
                    in_viewport: inViewport(rect),
                    area: rect.width * rect.height,
                    font_size: parseFloat(style.fontSize) || 0,
                    disabled: el.disabled || el.getAttribute('disabled') !== null,
                    in_form: !!form,
                    form_selector: form ? cssPath(form) : '',
                    form_action: formAction,
                    form_method: formMethod,
                    form_has_password: form ? hasPasswordField(form) : false,
                    form_has_otp: form ? hasOtpField(form) : false,
                    near_password: isNearSensitive(el, form || el.parentElement || null),
                });
            };

            document.querySelectorAll('form').forEach(form => {
                const buttons = form.querySelectorAll('button,input[type="submit"],input[type="button"]');
                buttons.forEach(el => {
                    addCandidate(el, {source: 'form'});
                });
            });

            const sensitiveInputs = Array.from(document.querySelectorAll('input[type="password"],input[name*="otp" i],input[id*="otp" i]'));
            for (const input of sensitiveInputs) {
                const container = input.closest('form') || input.parentElement;
                if (!container) continue;
                const buttons = container.querySelectorAll('button,input[type="submit"],input[type="button"],[role="button"]');
                buttons.forEach(el => addCandidate(el, {source: 'near_sensitive'}));
            }

            const ctaNodes = document.querySelectorAll('button,[role="button"],input[type="submit"],input[type="button"],a[role="button"],a.btn,.btn');
            ctaNodes.forEach(el => addCandidate(el, {source: 'cta'}));

            return candidates;
        }
        """
    ) or []


def score_step1_candidates(candidates: List[dict], base_url: str) -> Tuple[List[dict], Optional[dict]]:
    scored: List[dict] = []
    base_etld1 = get_etld1_from_url(base_url)
    for cand in candidates:
        if not isinstance(cand, dict):
            continue
        breakdown: Dict[str, int] = {}
        score = 0
        text = (cand.get("text") or "").strip()
        text_lower = text.lower()
        attrs = cand.get("attributes") or {}
        tag = (cand.get("tag") or "").lower()
        role = (attrs.get("role") or "").lower()
        ctype = (attrs.get("type") or "").lower()
        href = (attrs.get("href") or "").strip()
        form_action = (cand.get("form_action") or "").strip()

        if not cand.get("visible"):
            breakdown["not_visible_penalty"] = -100
            score -= 100
        if not cand.get("in_viewport"):
            breakdown["offscreen_penalty"] = -40
            score -= 40
        if cand.get("disabled"):
            breakdown["disabled_penalty"] = -40
            score -= 40

        is_submit = False
        if tag == "input" and ctype in {"submit", "button"}:
            is_submit = True
        if tag == "button":
            is_submit = ctype in {"", "submit"}

        if cand.get("in_form") and is_submit:
            breakdown["form_submit_bonus"] = 40
            score += 40
        if cand.get("form_has_password") or cand.get("near_password"):
            breakdown["near_password_bonus"] = 30
            score += 30
        if cand.get("form_has_otp"):
            breakdown["near_otp_bonus"] = 20
            score += 20
        if any(k in text_lower for k in STEP1_CTA_KEYWORDS):
            breakdown["cta_text_bonus"] = 20
            score += 20
        if role == "button":
            breakdown["role_button_bonus"] = 5
            score += 5
        if (cand.get("area") or 0) >= 10_000:
            breakdown["size_bonus"] = 6
            score += 6
        elif (cand.get("area") or 0) >= 4_000:
            breakdown["size_bonus"] = 3
            score += 3
        if (cand.get("font_size") or 0) >= 16:
            breakdown["font_bonus"] = 3
            score += 3

        if any(k in text_lower for k in STEP1_NEGATIVE_KEYWORDS):
            breakdown["negative_text_penalty"] = -80
            score -= 80

        id_val = (attrs.get("id") or "").lower()
        class_hint = (attrs.get("class") or "").lower()
        combined_hint = id_val + " " + class_hint
        if any(h in combined_hint for h in STEP1_AD_CLASS_HINTS):
            breakdown["ad_penalty"] = -60
            score -= 60
        if any(h in combined_hint for h in STEP1_SOCIAL_HINTS):
            breakdown["social_penalty"] = -40
            score -= 40

        if href:
            href_lower = href.lower()
            if href_lower.startswith("mailto:") or href_lower.startswith("tel:"):
                breakdown["external_link_penalty"] = -120
                score -= 120
            else:
                href_s = sanitize_url_for_summary(href)
                href_etld1 = get_etld1_from_url(href_s)
                if href_etld1 and base_etld1 and href_etld1 != base_etld1:
                    breakdown["external_link_penalty"] = -120
                    score -= 120

        if form_action:
            form_action_s = sanitize_url_for_summary(form_action)
            action_etld1 = get_etld1_from_url(form_action_s)
            if action_etld1 and base_etld1 and action_etld1 != base_etld1:
                breakdown["cross_domain_action_penalty"] = -80
                score -= 80

        cand = dict(cand)
        safe_attrs = {
            "id": attrs.get("id") or "",
            "name": attrs.get("name") or "",
            "type": attrs.get("type") or "",
            "role": attrs.get("role") or "",
            "aria-label": attrs.get("aria-label") or "",
            "href": sanitize_url_for_summary(href) if href else "",
        }
        if attrs.get("class"):
            safe_attrs["class"] = attrs.get("class")
        cand["attributes"] = safe_attrs
        cand["score_total"] = score
        cand["score_breakdown"] = breakdown
        cand["is_submit"] = is_submit
        cand["form_action"] = sanitize_url_for_summary(form_action) if form_action else ""
        scored.append(cand)

    scored.sort(key=lambda x: (x.get("score_total", 0), x.get("area", 0)), reverse=True)
    chosen = scored[0] if scored and scored[0].get("score_total", 0) >= STEP1_MIN_SCORE else None
    return scored, chosen


def chosen_reason_from_breakdown(breakdown: Dict[str, int]) -> str:
    positives = [(k, v) for k, v in breakdown.items() if v > 0]
    positives.sort(key=lambda kv: kv[1], reverse=True)
    parts = [f"{k}:{v}" for k, v in positives[:3]]
    return "; ".join(parts)


def fill_dummy_passwords(page, form_selector: str) -> None:
    if not form_selector:
        return
    page.evaluate(
        """
        (sel) => {
            const form = document.querySelector(sel);
            if (!form) return;
            const pwds = form.querySelectorAll('input[type="password"]');
            pwds.forEach(el => {
                el.value = 'dummy123!';
                el.dispatchEvent(new Event('input', {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
            });
        }
        """,
        form_selector,
    )


def is_safe_to_click_candidate(cand: dict, base_url: str) -> Tuple[bool, str]:
    href = (cand.get("attributes") or {}).get("href") or ""
    form_action = cand.get("form_action") or ""
    base_etld1 = get_etld1_from_url(base_url)
    if href:
        href_lower = href.lower()
        if href_lower.startswith("mailto:") or href_lower.startswith("tel:"):
            return False, "href_scheme_blocked"
        href_etld1 = get_etld1_from_url(href)
        if href_etld1 and base_etld1 and href_etld1 != base_etld1:
            return False, "external_href_blocked"
    if cand.get("is_submit") and form_action:
        action_etld1 = get_etld1_from_url(form_action)
        if action_etld1 and base_etld1 and action_etld1 != base_etld1:
            return False, "external_form_action_blocked"
    return True, ""


def collect_page_signals(page) -> dict:
    title = ""
    try:
        title = page.title() or ""
    except Exception:
        pass

    text_len = 0
    text_head = ""
    try:
        body_meta = page.evaluate(
            f"""
            () => {{
                const raw = document.body ? (document.body.innerText || document.body.textContent || '') : '';
                return {{
                    text_len: raw.length,
                    text_head: raw.slice(0, {MAX_TEXT_HEAD_CHARS}),
                }};
            }}
            """
        ) or {}
        text_len = int(body_meta.get("text_len") or 0)
        text_head = body_meta.get("text_head") or ""
    except Exception:
        pass

    text_head = RE_WS.sub(" ", text_head).strip()
    return {
        "title": title,
        "text_len": text_len,
        "text_head": text_head,
    }


def looks_blocked_or_error(signals: dict, html_text: Optional[str], sample_label: str = "") -> bool:
    hay = (signals.get("title", "") + " " + signals.get("text_head", "")).lower()
    if html_text:
        h = re.sub(r"\s+", " ", html_text[:4000]).lower()
        hay += " " + h

    regexes = BENIGN_RELAXED_ERROR_HINT_REGEXES if (sample_label or "").strip().lower() == "benign" else ERROR_HINT_REGEXES
    for rx in regexes:
        if rx.search(hay):
            return True
    return False


def is_suspicious_screenshot(png_bytes: bytes) -> Tuple[bool, str]:
    if len(png_bytes) < MIN_PNG_BYTES:
        return True, f"png_too_small:{len(png_bytes)}"

    if Image is None or ImageStat is None:
        return False, "no_pillow_skip_pixel_checks"

    try:
        im = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        im_small = im.resize((128, 128))

        pal = im_small.convert("P", palette=Image.ADAPTIVE, colors=16)
        hist = pal.histogram()
        total = sum(hist) or 1
        dominant = max(hist) / total
        if dominant >= DOMINANT_COLOR_MAX:
            return True, f"dominant_color:{dominant:.4f}"

        gray = im_small.convert("L")
        stddev = ImageStat.Stat(gray).stddev[0]
        if stddev <= GRAY_STDDEV_MIN:
            return True, f"low_stddev:{stddev:.2f}"

        return False, "ok"
    except Exception as e:
        return False, f"pixel_check_error:{repr(e)}"


def capture_fullpage_screenshot(page) -> Optional[bytes]:
    try:
        page_height = page.evaluate(
            """
            () => Math.max(
                window.innerHeight || 0,
                document.documentElement ? (document.documentElement.scrollHeight || 0) : 0,
                document.body ? (document.body.scrollHeight || 0) : 0
            )
            """
        )
        if isinstance(page_height, (int, float)) and page_height > MAX_FULLPAGE_HEIGHT:
            return None
    except Exception:
        pass

    try:
        return page.screenshot(full_page=True)
    except Exception:
        return None


def extract_visible_text(page) -> str:
    try:
        txt = page.evaluate(
            r"""
            () => {
                const clean = (s) => String(s || '').replace(/\s+/g, ' ').trim();
                const title = clean(document.title || '');
                const body = document.body ? (document.body.innerText || document.body.textContent || '') : '';
                const normalizedBody = body.replace(/\r/g, '').trim();
                if (normalizedBody) {
                    return title ? `${title}\n\n${normalizedBody}` : normalizedBody;
                }

                const fallback = [];
                const nodes = document.querySelectorAll('h1,h2,h3,button,a,label,p,span');
                for (let i = 0; i < Math.min(nodes.length, 120); i++) {
                    const t = clean(nodes[i].innerText || nodes[i].textContent || '');
                    if (t) fallback.push(t);
                }
                if (title) fallback.unshift(title);
                return fallback.join('\n');
            }
            """
        ) or ""
    except Exception:
        txt = ""
    txt = RE_MANY_NL.sub("\n\n", txt).strip()
    return truncate_large_text(txt, MAX_VISIBLE_TEXT_CHARS)


def extract_forms_json(page, base_url: str) -> dict:
    try:
        data = page.evaluate(
            """
            (baseUrl) => {
                const absUrl = (u) => {
                    try { return new URL(u, baseUrl).toString(); } catch(e) { return u || ''; }
                };
                const forms = [];
                const fs = Array.from(document.querySelectorAll('form'));
                for (const f of fs) {
                    const action = f.getAttribute('action') || '';
                    const method = (f.getAttribute('method') || 'GET').toUpperCase();
                    const inputs = [];
                    const ins = Array.from(f.querySelectorAll('input, textarea, select'));
                    for (const el of ins) {
                        const tag = el.tagName.toLowerCase();
                        const type = (el.getAttribute('type') || '').toLowerCase();
                        inputs.push({
                            tag,
                            type,
                            name: el.getAttribute('name') || '',
                            id: el.getAttribute('id') || '',
                            autocomplete: el.getAttribute('autocomplete') || '',
                            placeholder: el.getAttribute('placeholder') || '',
                            aria_label: el.getAttribute('aria-label') || '',
                        });
                    }
                    const allText = (f.innerText || '').toLowerCase();
                    const has_password = inputs.some(x => x.type === 'password') || allText.includes('password') || allText.includes('密码');
                    const has_otp = allText.includes('otp') || allText.includes('one-time') || allText.includes('验证码') || allText.includes('动态码');
                    const has_card = allText.includes('cvv') || allText.includes('card') || allText.includes('银行卡') || allText.includes('信用卡');
                    forms.push({
                        action,
                        action_abs: absUrl(action),
                        method,
                        inputs,
                        has_password,
                        has_otp,
                        has_card,
                    });
                }
                return { forms };
            }
            """,
            base_url,
        )
        if not isinstance(data, dict):
            return {"forms": []}
        return data
    except Exception:
        return {"forms": []}


def _load_har_entries(har_path: Path) -> list:
    raw = har_path.read_bytes()
    if har_path.suffix.lower() == ".zip" or raw[:2] == b"PK":
        with zipfile.ZipFile(har_path, "r") as zf:
            har_files = [n for n in zf.namelist() if n.lower().endswith(".har")]
            if not har_files:
                return []
            har_json = zf.read(har_files[0]).decode("utf-8", errors="ignore")
    else:
        har_json = raw.decode("utf-8", errors="ignore")

    try:
        obj = json.loads(har_json)
    except Exception:
        return []
    log = obj.get("log") if isinstance(obj, dict) else None
    entries = log.get("entries") if isinstance(log, dict) else None
    return entries if isinstance(entries, list) else []


def summarize_har(har_path: Path) -> dict:
    entries = _load_har_entries(har_path)

    domains: List[str] = []
    post_domains: List[str] = []
    methods: List[str] = []
    status: List[int] = []
    mime: List[str] = []

    for e in entries:
        try:
            req = e.get("request", {})
            resp = e.get("response", {})
            u = (req.get("url") or "")
            p = urlparse(u)
            if p.netloc:
                d = p.netloc.lower()
                domains.append(d)
            m = (req.get("method") or "").upper()
            methods.append(m)
            if m == "POST" and p.netloc:
                post_domains.append(p.netloc.lower())
            status.append(int(resp.get("status") or 0))
            ct = ""
            content = resp.get("content", {})
            if isinstance(content, dict):
                ct = content.get("mimeType") or ""
            mime.append(ct)
        except Exception:
            continue

    dom_cnt = Counter(domains)
    post_cnt = Counter(post_domains)

    return {
        "har_path": str(har_path.name),
        "entry_count": len(entries),
        "unique_domains": len(dom_cnt),
        "top_domains": dom_cnt.most_common(30),
        "post_domains": post_cnt.most_common(30),
        "methods": Counter(methods).most_common(),
        "status": Counter(status).most_common(20),
        "mime": Counter(mime).most_common(20),
    }


class NetEvidenceLiteCollector:
    def __init__(self) -> None:
        self.request_total = 0
        self.by_resource_type: Counter = Counter()
        self.by_method: Counter = Counter()
        self.domain_counts: Counter = Counter()
        self.domain_methods: Dict[str, Counter] = {}
        self.post_counts: Counter = Counter()
        self.status_counts: Counter = Counter()
        self.ttfb_ms: List[float] = []
        self.response_end_ms: List[float] = []
        self.errors: List[str] = []
        self._pending_keys: set = set()

    def attach(self, page) -> None:
        page.on("request", self._on_request)
        page.on("response", self._on_response)
        page.on("requestfinished", self._on_requestfinished)

    def _request_key(self, req) -> str:
        guid = getattr(req, "_guid", None)
        if guid:
            return str(guid)
        return str(id(req))

    def _append_timing_sample(self, bucket: List[float], value) -> None:
        if len(bucket) < MAX_NET_TIMING_SAMPLES:
            bucket.append(float(value))

    def _on_request(self, req) -> None:
        try:
            self.request_total += 1
            method = (req.method or "").upper()
            if method:
                self.by_method[method] += 1
            rt = req.resource_type or ""
            if rt:
                self.by_resource_type[rt] += 1

            self._pending_keys.add(self._request_key(req))

            domain_etld1 = get_etld1_from_url(req.url or "")
            if domain_etld1:
                self.domain_counts[domain_etld1] += 1
                methods = self.domain_methods.setdefault(domain_etld1, Counter())
                if method:
                    methods[method] += 1
                if method == "POST":
                    self.post_counts[domain_etld1] += 1
        except Exception as e:
            self.errors.append(f"request:{type(e).__name__}")

    def _on_response(self, resp) -> None:
        try:
            status = int(resp.status)
            if status:
                self.status_counts[status] += 1
        except Exception as e:
            self.errors.append(f"response:{type(e).__name__}")

    def _on_requestfinished(self, req) -> None:
        try:
            key = self._request_key(req)
            if self._pending_keys:
                if key not in self._pending_keys:
                    return
                self._pending_keys.discard(key)

            try:
                timing = req.timing
            except Exception:
                timing = None
            if isinstance(timing, dict):
                resp_start = timing.get("responseStart")
                resp_end = timing.get("responseEnd")
                if isinstance(resp_start, (int, float)) and resp_start >= 0:
                    self._append_timing_sample(self.ttfb_ms, resp_start)
                if isinstance(resp_end, (int, float)) and resp_end >= 0:
                    self._append_timing_sample(self.response_end_ms, resp_end)
        except Exception as e:
            self.errors.append(f"requestfinished:{type(e).__name__}")

    def build_summary(self, final_url: str, navigation_chain: Optional[List[dict]]) -> dict:
        final_url_s = sanitize_url_for_summary(final_url or "")
        top_origin = origin_from_url(final_url or "")
        top_etld1 = etld1_from_host(_host_from_url(final_url or ""))

        domain_list = _sorted_counter(self.domain_counts)
        domain_counts = []
        for domain, count in domain_list:
            methods = dict(self.domain_methods.get(domain, {}))
            domain_counts.append({"domain_etld1": domain, "count": count, "methods": methods})

        third_party_domains = [d for d, _ in domain_list if d and d != top_etld1]
        post_targets = [{"domain_etld1": d, "count": c} for d, c in _sorted_counter(self.post_counts)]

        nav_chain = []
        for item in navigation_chain or []:
            if isinstance(item, dict):
                nav_chain.append(
                    {"url": sanitize_url_for_summary(item.get("url") or ""), "status": item.get("status")}
                )
            elif isinstance(item, str):
                nav_chain.append({"url": sanitize_url_for_summary(item), "status": None})

        anomalies: List[str] = []
        if len(third_party_domains) >= 10:
            anomalies.append("many_third_party")
        if top_etld1 and any(pt.get("domain_etld1") != top_etld1 for pt in post_targets):
            anomalies.append("post_to_third_party")
        if len(nav_chain) >= 6:
            anomalies.append("too_many_redirects")

        timing = {
            "ttfb_p50": percentile(self.ttfb_ms, 50),
            "ttfb_p95": percentile(self.ttfb_ms, 95),
            "response_end_p50": percentile(self.response_end_ms, 50),
            "response_end_p95": percentile(self.response_end_ms, 95),
        }

        summary = {
            "final_url": final_url_s,
            "top_frame_final_origin": top_origin,
            "request_counts": {
                "total": self.request_total,
                "by_resource_type": dict(self.by_resource_type),
                "by_method": dict(self.by_method),
            },
            "domain_counts": domain_counts,
            "third_party_domains": third_party_domains,
            "post_targets": post_targets,
            "status_counts": _group_status_counts(self.status_counts),
            "timing_ms": timing,
            "navigation_chain": nav_chain,
            "anomalies": anomalies,
        }
        if self.errors:
            summary["errors"] = self.errors[:20]
        return summary


def validate_net_summary(summary: dict) -> List[str]:
    required_keys = [
        "final_url",
        "top_frame_final_origin",
        "request_counts",
        "domain_counts",
        "third_party_domains",
        "post_targets",
        "status_counts",
        "timing_ms",
        "navigation_chain",
        "anomalies",
    ]
    issues: List[str] = []
    missing = [k for k in required_keys if k not in summary]
    if missing:
        issues.append("missing_keys:" + ",".join(missing))

    urls: List[str] = []
    final_url = summary.get("final_url")
    if isinstance(final_url, str):
        urls.append(final_url)
    for item in summary.get("navigation_chain", []) or []:
        if isinstance(item, dict):
            u = item.get("url")
            if isinstance(u, str):
                urls.append(u)
    for u in urls:
        if "?" in u or "#" in u:
            issues.append("url_has_query_or_fragment")
            break

    for key in ("headers", "cookies", "authorization", "body", "post_data"):
        if key in summary:
            issues.append(f"unexpected_field:{key}")
    return issues


def build_variant_summary(payload: dict, net_summary: Optional[dict]) -> Tuple[dict, dict]:
    visible_text = payload.get("visible_text") or ""
    text_feat = build_text_features(visible_text)
    forms_summary = summarize_forms_for_diff(payload.get("forms_json") or {})
    network_summary = summarize_network_for_diff(net_summary)
    summary = {
        "final_url": sanitize_url_for_summary(payload.get("final_url") or ""),
        "status": payload.get("status"),
        "title": (payload.get("page_signals") or {}).get("title"),
        "visible_text_len": text_feat.get("len"),
        "visible_text_simhash": text_feat.get("simhash"),
        "forms_summary": forms_summary,
        "network_summary": network_summary,
    }
    return summary, text_feat


def capture_variant(
    url: str,
    variant_cfg: dict,
    browser_mgr: "BrowserPoolManager",
    headless: bool,
    route_handler,
    proxy_cfg: Optional[dict],
    nav_timeout_ms: int,
    goto_wait_until: str,
    enable_route_intercept: bool,
    sample_label: str,
) -> dict:
    context = None
    page = None
    net_collector: Optional[NetEvidenceLiteCollector] = None
    start_ts = time.time()
    try:
        context_kwargs = dict(
            viewport=variant_cfg.get("viewport") or VIEWPORT,
            accept_downloads=ACCEPT_DOWNLOADS,
            service_workers=SERVICE_WORKERS,
            java_script_enabled=JAVA_SCRIPT_ENABLED,
            ignore_https_errors=IGNORE_HTTPS_ERRORS,
            bypass_csp=BYPASS_CSP,
        )
        if variant_cfg.get("locale"):
            context_kwargs["locale"] = variant_cfg.get("locale")
        if variant_cfg.get("timezone_id"):
            context_kwargs["timezone_id"] = variant_cfg.get("timezone_id")
        if variant_cfg.get("user_agent"):
            context_kwargs["user_agent"] = variant_cfg.get("user_agent")
        if proxy_cfg:
            context_kwargs["proxy"] = proxy_cfg

        context = browser_mgr.new_context_resilient(headless, proxy_cfg, context_kwargs)
        context.set_default_timeout(nav_timeout_ms)
        if enable_route_intercept:
            context.route("**/*", route_handler)
        page = context.new_page()
        apply_stealth_sync(page)
        if RECORD_NET_EVIDENCE_LITE:
            net_collector = NetEvidenceLiteCollector()
            net_collector.attach(page)

        success, payload, err = crawl_one_url_to_memory(
            page,
            url,
            enable_step1_action=False,
            capture_raw_html=False,
            nav_timeout_ms=nav_timeout_ms,
            goto_wait_until=goto_wait_until,
            sample_label=sample_label,
        )

        try:
            context.close()
        except Exception:
            pass

        net_summary = None
        if RECORD_NET_EVIDENCE_LITE and net_collector is not None and payload:
            try:
                net_summary = net_collector.build_summary(
                    payload.get("final_url") or "",
                    payload.get("navigation_chain") or payload.get("redirects") or [],
                )
            except Exception as e:
                                net_summary = {"error": repr(e)}

        return {
            "success": bool(success and payload),
            "payload": payload,
            "error": err,
            "net_summary": net_summary,
            "elapsed_ms": int((time.time() - start_ts) * 1000),
        }
    except Exception as e:
        if is_driver_connection_closed_error(e):
            try:
                browser_mgr.relaunch(headless, proxy_cfg)
            except Exception:
                pass
        try:
            if context is not None:
                context.close()
        except Exception:
            pass
        return {
            "success": False,
            "payload": None,
            "error": repr(e),
            "net_summary": None,
            "elapsed_ms": int((time.time() - start_ts) * 1000),
        }


def do_step1_action(page) -> Tuple[List[dict], Optional[dict]]:
    """一次可信、可解释的轻量交互。失败不影响主样本。"""
    actions: List[dict] = []
    try:
        try:
            page.wait_for_load_state("networkidle", timeout=STEP1_WAIT_MS + 2_000)
        except Exception:
            pass
        try:
            page.wait_for_timeout(300)
        except Exception:
            pass

        before_url = page.url
        candidates = collect_step1_candidates(page)
        scored, chosen = score_step1_candidates(candidates, before_url)

        for cand in scored:
            actions.append(
                {
                    "type": "candidate",
                    "selector": cand.get("selector") or "",
                    "xpath": cand.get("xpath") or "",
                    "text": cand.get("text") or "",
                    "tag": cand.get("tag") or "",
                    "attributes": cand.get("attributes") or {},
                    "in_form": bool(cand.get("in_form")),
                    "form_action": cand.get("form_action") or "",
                    "form_method": cand.get("form_method") or "",
                    "score_total": cand.get("score_total"),
                    "score_breakdown": cand.get("score_breakdown") or {},
                    "chosen": False,
                }
            )

        if not scored:
            actions.append({"type": "decision", "error": "no_candidates"})
            return actions, None

        if not chosen or not chosen.get("selector"):
            actions.append({"type": "decision", "error": "no_candidate_above_threshold"})
            return actions, None

        chosen_reason = chosen_reason_from_breakdown(chosen.get("score_breakdown") or {})
        for item in actions:
            if item.get("type") == "candidate" and item.get("selector") == chosen.get("selector"):
                item["chosen"] = True
                item["chosen_reason"] = chosen_reason
                break

        safe, safe_reason = is_safe_to_click_candidate(chosen, before_url)
        if not safe:
            actions.append(
                {
                    "type": "decision",
                    "chosen_selector": chosen.get("selector"),
                    "chosen_reason": chosen_reason,
                    "error": safe_reason,
                }
            )
            return actions, None

        popup_count = 0
        download_count = 0

        def _on_popup(p):
            nonlocal popup_count
            popup_count += 1
            try:
                p.close()
            except Exception:
                pass

        def _on_download(d):
            nonlocal download_count
            download_count += 1
            try:
                d.cancel()
            except Exception:
                pass

        page.on("popup", _on_popup)
        page.on("download", _on_download)

        if chosen.get("is_submit") and chosen.get("form_selector"):
            try:
                fill_dummy_passwords(page, chosen.get("form_selector") or "")
            except Exception:
                pass

        step1_net = None
        step1_net_collector: Optional[NetEvidenceLiteCollector] = None
        if RECORD_NET_EVIDENCE_LITE:
            step1_net_collector = NetEvidenceLiteCollector()
            step1_net_collector.attach(page)

        try:
            page.locator(chosen.get("selector")).first.click(timeout=4_000)
        except Exception as e:
            actions.append(
                {
                    "type": "decision",
                    "chosen_selector": chosen.get("selector"),
                    "chosen_reason": chosen_reason,
                    "error": f"click_failed:{type(e).__name__}",
                }
            )
            return actions, None

        try:
            page.wait_for_load_state("networkidle", timeout=STEP1_WAIT_MS + 2_000)
        except Exception:
            pass
        try:
            page.wait_for_timeout(STEP1_WAIT_MS)
        except Exception:
            pass

        after_url = page.url
        base_etld1 = get_etld1_from_url(before_url)
        after_etld1 = get_etld1_from_url(after_url)
        cross_domain = bool(base_etld1 and after_etld1 and base_etld1 != after_etld1)

        if step1_net_collector is not None:
            try:
                step1_net = step1_net_collector.build_summary(after_url, [])
            except Exception as e:
                step1_net = {"error": repr(e)}

        step_shot = page.screenshot(full_page=False)
        step_html = None
        try:
            step_html = page.content()
        except Exception:
            step_html = None

        step_visible = extract_visible_text(page) if SAVE_VISIBLE_TEXT else ""
        step_forms = extract_forms_json(page, after_url) if SAVE_FORMS_JSON else {"forms": []}

        decision = {
            "type": "decision",
            "chosen_selector": chosen.get("selector"),
            "chosen_reason": chosen_reason,
            "before_url": sanitize_url_for_summary(before_url),
            "after_url": sanitize_url_for_summary(after_url),
            "popup_count": popup_count,
            "download_count": download_count,
        }
        if cross_domain:
            decision["error"] = "cross_domain_navigation"
        actions.append(decision)

        result = {
            "url": after_url,
            "screenshot_viewport_bytes": step_shot,
            "html_rendered": step_html,
            "visible_text": step_visible,
            "forms": step_forms,
        }
        if step1_net is not None:
            result["net_summary"] = step1_net
        if cross_domain:
            result["error"] = "cross_domain_navigation"
        return actions, result
    except Exception as e:
        actions.append({"type": "decision", "error": repr(e)})
        return actions, None


def crawl_one_url_to_memory(
    page,
    url: str,
    enable_step1_action: Optional[bool] = None,
    capture_raw_html: Optional[bool] = None,
    nav_timeout_ms: Optional[int] = None,
    goto_wait_until: Optional[str] = None,
    sample_label: str = "",
) -> Tuple[bool, Optional[Dict], Optional[str]]:
    """不落盘、不建目录。成功时返回 payload（写盘用）。"""
    ts = now_utc_compact()
    if enable_step1_action is None:
        enable_step1_action = ENABLE_STEP1_ACTION
    if capture_raw_html is None:
        capture_raw_html = SAVE_RAW_HTML
    if nav_timeout_ms is None or nav_timeout_ms <= 0:
        nav_timeout_ms = NAV_TIMEOUT_MS
    if not goto_wait_until:
        goto_wait_until = DEFAULT_GOTO_WAIT_UNTIL

    scheme = urlparse(url).scheme.lower()
    if scheme not in {"http", "https"}:
        return False, None, "unsupported_scheme"

    last_err: Optional[Exception] = None

    for attempt in range(1, RETRY_VISIT + 1):
        resp = None
        try:
            # 1) 导航
            resp, used_wait_until, goto_fallback_used = goto_with_fallback(
                page,
                url,
                nav_timeout_ms,
                goto_wait_until,
            )
            if resp is None:
                raise RuntimeError("page.goto returned None")
            if goto_fallback_used:
                print(f"  [INFO] navigation succeeded after fallback wait_until={used_wait_until}")

            status = resp.status
            if status not in OK_STATUSES:
                return False, None, f"status_not_allowed:{status}"

            response_header_flags = {}
            try:
                hdrs = getattr(resp, "headers", None) or {}
                response_header_flags = {
                    "content_security_policy": bool(hdrs.get("content-security-policy")),
                    "strict_transport_security": bool(hdrs.get("strict-transport-security")),
                    "x_frame_options": bool(hdrs.get("x-frame-options")),
                    "x_content_type_options": bool(hdrs.get("x-content-type-options")),
                    "referrer_policy": bool(hdrs.get("referrer-policy")),
                }
            except Exception:
                response_header_flags = {}

            # 2) 先等 DOM 可用，再给 hydration 一点时间
            try:
                page.wait_for_load_state("domcontentloaded", timeout=POST_GOTO_DOMCONTENTLOADED_TIMEOUT_MS)
            except Exception:
                pass
            try:
                page.wait_for_timeout(POST_GOTO_HYDRATION_WAIT_MS)
            except Exception:
                pass

            google_consent_attempted = False
            google_consent_clicked = False
            try:
                google_consent_attempted, google_consent_clicked = handle_google_consent(page)
            except Exception:
                google_consent_attempted, google_consent_clicked = False, False

            # 3) 稍等网络空闲；best-effort，不作为唯一成功标准
            try:
                page.wait_for_load_state("networkidle", timeout=POST_NAV_NETIDLE_MS)
            except Exception:
                pass
            try:
                page.wait_for_timeout(600)
            except Exception:
                pass

            final_url = resp.url
            redirects = build_redirect_chain_from_response(resp)
            navigation_chain = build_navigation_chain_with_status(resp)

            # 4) 抓 raw（主文档响应体）
            html_raw_text = None
            if capture_raw_html:
                try:
                    html_raw_text = truncate_large_text(resp.text(), MAX_HTML_CHARS, "\n<!-- TRUNCATED -->\n")
                except Exception:
                    html_raw_text = None

            # 5) 抓 rendered DOM
            html_rendered = None
            try:
                html_rendered = truncate_large_text(page.content(), MAX_HTML_CHARS, "\n<!-- TRUNCATED -->\n")
            except Exception:
                html_rendered = None

            signals = collect_page_signals(page)
            if looks_blocked_or_error(signals, html_rendered, sample_label=sample_label):
                return False, None, f"blocked_or_error:title={signals.get('title','')[:80]}"

            # 6) 抓截图（viewport + full）
            shot_view = page.screenshot(full_page=False)
            shot_full = capture_fullpage_screenshot(page) if SAVE_FULLPAGE_SHOT else None

            bad1, why1 = is_suspicious_screenshot(shot_view)

            # 同一次 attempt 内补救：再等 + 再截一次
            if bad1:
                try:
                    page.wait_for_timeout(SECOND_PASS_WAIT_MS)
                except Exception:
                    pass

                # 补救后再看一次是否错误页
                signals2 = collect_page_signals(page)
                if looks_blocked_or_error(signals2, html_rendered, sample_label=sample_label):
                    return False, None, f"blocked_or_error_after_wait:title={signals2.get('title','')[:80]}"

                shot_view2 = page.screenshot(full_page=False)
                bad2, why2 = is_suspicious_screenshot(shot_view2)
                if not bad2:
                    shot_view = shot_view2
                    bad1, why1 = bad2, why2

            if bad1 and signals.get("text_len", 0) < DOM_TEXT_MIN_LEN:
                raise RuntimeError(f"bad_capture:{why1};text_len={signals.get('text_len')}")

            # 7) 可见文本 / 表单
            visible_text = extract_visible_text(page) if SAVE_VISIBLE_TEXT else ""
            forms_json = extract_forms_json(page, final_url) if SAVE_FORMS_JSON else {"forms": []}

            # 8) userAgent
            user_agent = None
            try:
                user_agent = page.evaluate("() => navigator.userAgent")
            except Exception:
                user_agent = None

            # 9) step1 轻量交互（可选；失败不影响主样本）
            actions: List[dict] = []
            step1: Optional[dict] = None
            if enable_step1_action:
                actions, step1 = do_step1_action(page)

            payload = {
                "ts": ts,
                "input_url": url,
                "final_url": final_url,
                "status": status,
                "redirects": redirects,
                "navigation_chain": navigation_chain,
                "page_signals": signals,
                "response_header_flags": response_header_flags,
                "user_agent": user_agent,
                "screenshot_viewport_bytes": shot_view,
                "screenshot_full_bytes": shot_full,
                "html_raw_text": html_raw_text,
                "html_rendered": html_rendered,
                "visible_text": visible_text,
                "forms_json": forms_json,
                "actions": actions,
                "step1": step1,
            }
            return True, payload, None

        except Exception as e:
            last_err = e
            if attempt < RETRY_VISIT:
                try:
                    page.wait_for_timeout(400)
                except Exception:
                    pass
                continue

    return False, None, f"goto_failed_or_bad_capture:{repr(last_err)}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default=str(DEFAULT_INPUT_PATH))
    parser.add_argument("--input_format", type=str, default=DEFAULT_INPUT_FORMAT, choices=["csv", "txt"])
    parser.add_argument("--csv_url_column", type=str, default=DEFAULT_CSV_URL_COLUMN)
    parser.add_argument("--brand_lexicon", type=str, default=BRAND_LEXICON_PATH)
    parser.add_argument("--label", type=str, choices=["phish", "benign"], default="")
    parser.add_argument("--output_root", type=str, default="")
    parser.add_argument("--ingest_metadata_json", type=str, default="")
    parser.add_argument("--dry_run", action="store_true")
    parser.add_argument("--proxy_server", type=str, default="")
    parser.add_argument("--proxy_username", type=str, default="")
    parser.add_argument("--proxy_password", type=str, default="")
    parser.add_argument("--nav_timeout_ms", type=int, default=0)
    parser.add_argument("--disable_route_intercept", action="store_true")
    parser.add_argument(
        "--goto_wait_until",
        type=str,
        default=DEFAULT_GOTO_WAIT_UNTIL,
        choices=["load", "domcontentloaded", "commit", "networkidle"],
    )
    args = parser.parse_args()

    nav_timeout_ms = args.nav_timeout_ms if args.nav_timeout_ms and args.nav_timeout_ms > 0 else NAV_TIMEOUT_MS
    proxy_server = args.proxy_server.strip() or PROXY_SERVER
    proxy_username = args.proxy_username if args.proxy_server.strip() else PROXY_USERNAME
    proxy_password = args.proxy_password if args.proxy_server.strip() else PROXY_PASSWORD
    enable_route_intercept = ROUTE_INTERCEPT_ENABLED and not args.disable_route_intercept
    goto_wait_until = (args.goto_wait_until or DEFAULT_GOTO_WAIT_UNTIL).strip().lower() or DEFAULT_GOTO_WAIT_UNTIL

    if not args.output_root.strip():
        ensure_dirs()

    try:
        ingest_metadata = parse_ingest_metadata(args.ingest_metadata_json)
    except ValueError as exc:
        print(f"[FATAL] {exc}", file=sys.stderr)
        sys.exit(2)

    if DRY_RUN or args.dry_run:
        dry_run_urls = [
            "https://example.com/",
            "https://httpbin.org/redirect/1",
            "https://www.wikipedia.org/",
        ]
        urls_iter = iter(normalize_url(u) for u in dry_run_urls if u)
        total_urls = len(dry_run_urls)
        label = args.label or "benign"
        print("[INFO] DRY_RUN enabled; using 3 fixed URLs.")
    else:
        input_path = Path(args.input_path)
        if not input_path.exists():
            print(f"[FATAL] input file not found: {input_path}", file=sys.stderr)
            sys.exit(2)

        total_urls = count_urls(input_path, args.input_format, args.csv_url_column)
        if total_urls <= 0:
            print("[FATAL] no valid URL found", file=sys.stderr)
            sys.exit(2)

        urls_iter = iter_normalized_urls(input_path, args.input_format, args.csv_url_column)

        label = args.label.strip().lower()
        while label not in {"phish", "benign"}:
            label = input("Select label (phish/benign): ").strip().lower()

    if args.output_root.strip():
        root = Path(args.output_root)
    else:
        root = EVT_DATASET_PHISH_ROOT if label == "phish" else EVT_DATASET_BENIGN_ROOT
    root.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] label={label} total_urls={total_urls} output_root={root}")
    if Image is None:
        print("[WARN] 未安装 pillow：截图质量检测将退化为‘文件大小阈值’。可选：pip install pillow")

    ok_cnt = 0
    fail_cnt = 0

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        print(f"[FATAL] playwright import failed: {exc}", file=sys.stderr)
        sys.exit(2)

    try:
        require_stealth_runtime()
    except Exception as exc:
        print(f"[FATAL] playwright-stealth import failed: {exc}", file=sys.stderr)
        sys.exit(2)

    with sync_playwright() as p:
        chromium = p.chromium

        base_proxy = make_proxy_config(proxy_server, proxy_username, proxy_password)

        browser_mgr = BrowserPoolManager(chromium, browser_channel=BROWSER_CHANNEL)

        def route_handler(route, request):
            try:
                rt = request.resource_type
                if rt in BLOCK_RESOURCE_TYPES:
                    return route.abort()
            except Exception:
                pass
            return route.continue_()

        for i, url in enumerate(urls_iter, 1):
            print(f"[{i}/{total_urls}] {url}")

            # 临时 HAR：成功才移动到样本目录
            tmp_har_path: Optional[Path] = None
            record_har = RECORD_HAR and not RECORD_NET_EVIDENCE_LITE
            if record_har:
                tmp = tempfile.NamedTemporaryFile(prefix="evt_", suffix=".har", delete=False)
                tmp.close()
                tmp_har_path = Path(tmp.name)

            context = None
            page = None
            net_collector: Optional[NetEvidenceLiteCollector] = None
            try:
                context_kwargs = dict(
                    viewport=VIEWPORT,
                    accept_downloads=ACCEPT_DOWNLOADS,
                    service_workers=SERVICE_WORKERS,
                    java_script_enabled=JAVA_SCRIPT_ENABLED,
                    ignore_https_errors=IGNORE_HTTPS_ERRORS,
                    bypass_csp=BYPASS_CSP,
                )
                if tmp_har_path is not None:
                    # HAR 会在 context.close() 时写入文件
                    context_kwargs["record_har_path"] = str(tmp_har_path)

                context = browser_mgr.new_context_resilient(HEADLESS, base_proxy, context_kwargs)
                context.set_default_timeout(nav_timeout_ms)
                if enable_route_intercept:
                    context.route("**/*", route_handler)
                page = context.new_page()
                apply_stealth_sync(page)
                if RECORD_NET_EVIDENCE_LITE:
                    net_collector = NetEvidenceLiteCollector()
                    net_collector.attach(page)

                if PRINT_REQUEST_FAILED:
                    def _on_req_failed(req):
                        try:
                            failure = req.failure
                            err_text = ""
                            if failure and isinstance(failure, dict):
                                err_text = failure.get("errorText", "")
                            elif failure:
                                err_text = str(failure)
                            print("  [requestfailed]", req.url, err_text)
                        except Exception:
                            pass

                    page.on("requestfailed", _on_req_failed)

                success, payload, err = crawl_one_url_to_memory(
                    page,
                    url,
                    nav_timeout_ms=nav_timeout_ms,
                    goto_wait_until=goto_wait_until,
                    sample_label=label,
                )

                # close() 触发 HAR 落盘
                try:
                    context.close()
                except Exception:
                    pass

                if not success or payload is None:
                    fail_cnt += 1
                    print(f"  -> FAIL/SKIP: {err}")
                    if tmp_har_path is not None:
                        try:
                            os.remove(tmp_har_path)
                        except Exception:
                            pass
                    continue

                # ✅ 成功样本才建目录
                ts = payload["ts"]
                folder = sanitize_folder_name(url, ts)
                out_dir = unique_out_dir(root, folder)
                out_dir.mkdir(parents=True, exist_ok=False)

                # A) meta/url/env
                meta = {
                    "sample_id": out_dir.name,
                    "label": label,
                    "crawl_time_utc": payload.get("ts"),
                    "http_status": payload.get("status"),
                    "page_title": (payload.get("page_signals") or {}).get("title"),
                    "etld1_mode": ETLD1_MODE,
                }
                if ingest_metadata:
                    meta["ingest_metadata"] = ingest_metadata
                (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

                urlj = {
                    "input_url": payload.get("input_url"),
                    "final_url": payload.get("final_url"),
                    "redirect_chain": payload.get("redirects", []),
                }
                (out_dir / "url.json").write_text(json.dumps(urlj, ensure_ascii=False, indent=2), encoding="utf-8")

                env = {
                    "browser_channel": browser_mgr.get_effective_channel(HEADLESS, base_proxy),
                    "headless": HEADLESS,
                    "viewport": VIEWPORT,
                    "java_script_enabled": JAVA_SCRIPT_ENABLED,
                    "service_workers": SERVICE_WORKERS,
                    "ignore_https_errors": IGNORE_HTTPS_ERRORS,
                    "bypass_csp": BYPASS_CSP,
                    "proxy_server": proxy_server,
                    "user_agent": payload.get("user_agent"),
                }
                (out_dir / "env.json").write_text(json.dumps(env, ensure_ascii=False, indent=2), encoding="utf-8")

                # B) redirect_chain
                (out_dir / "redirect_chain.json").write_text(
                    json.dumps(payload.get("redirects", []), ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )

                payload_input_url = payload.get("input_url") or ""
                payload_final_url = payload.get("final_url") or ""
                payload_page_title = (payload.get("page_signals") or {}).get("title") or ""
                payload_visible_text = payload.get("visible_text") or ""
                payload_forms_json = payload.get("forms_json") or {"forms": []}
                payload_html_raw = payload.get("html_raw_text") or ""
                payload_html_rendered = payload.get("html_rendered") or ""
                payload_response_header_flags = payload.get("response_header_flags") or {}

                # E) screenshots
                (out_dir / "screenshot_viewport.png").write_bytes(payload["screenshot_viewport_bytes"])
                if SAVE_FULLPAGE_SHOT and payload.get("screenshot_full_bytes"):
                    (out_dir / "screenshot_full.png").write_bytes(payload["screenshot_full_bytes"])
                payload.pop("screenshot_viewport_bytes", None)
                payload.pop("screenshot_full_bytes", None)

                # C) html + visible text
                if SAVE_RAW_HTML and payload.get("html_raw_text"):
                    (out_dir / "html_raw.html").write_text(payload["html_raw_text"], encoding="utf-8", errors="ignore")
                if SAVE_RENDERED_HTML and payload.get("html_rendered"):
                    (out_dir / "html_rendered.html").write_text(payload["html_rendered"], encoding="utf-8", errors="ignore")
                payload.pop("html_raw_text", None)
                payload.pop("html_rendered", None)
                if SAVE_VISIBLE_TEXT and payload.get("visible_text"):
                    (out_dir / "visible_text.txt").write_text(payload["visible_text"], encoding="utf-8", errors="ignore")

                # D) forms
                if SAVE_FORMS_JSON:
                    (out_dir / "forms.json").write_text(
                        json.dumps(payload.get("forms_json", {"forms": []}), ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                # F) step1
                actions = payload.get("actions") or []
                if ENABLE_STEP1_ACTION:
                    actions_text = "\n".join(json.dumps(a, ensure_ascii=False) for a in actions)
                    if actions_text:
                        actions_text += "\n"
                    (out_dir / "actions.jsonl").write_text(actions_text, encoding="utf-8")

                step1 = payload.get("step1")
                if step1:
                    step_dir = out_dir / "after_action"
                    step_dir.mkdir(parents=True, exist_ok=True)
                    (step_dir / "step1_screenshot_viewport.png").write_bytes(step1["screenshot_viewport_bytes"])
                    if step1.get("html_rendered"):
                        (step_dir / "step1_html_rendered.html").write_text(step1["html_rendered"], encoding="utf-8", errors="ignore")
                    if step1.get("visible_text"):
                        (step_dir / "step1_visible_text.txt").write_text(step1["visible_text"], encoding="utf-8", errors="ignore")
                    if step1.get("forms"):
                        (step_dir / "step1_forms.json").write_text(json.dumps(step1["forms"], ensure_ascii=False, indent=2), encoding="utf-8")
                    if step1.get("net_summary"):
                        (step_dir / "step1_net_summary.json").write_text(
                            json.dumps(step1["net_summary"], ensure_ascii=False, indent=2),
                            encoding="utf-8",
                        )
                    step1.clear()

                # G) net_summary (lite) and optional HAR
                base_net_summary = None
                if RECORD_NET_EVIDENCE_LITE and net_collector is not None:
                    try:
                        base_net_summary = net_collector.build_summary(
                            payload.get("final_url") or "",
                            payload.get("navigation_chain") or payload.get("redirects") or [],
                        )
                    except Exception as e:
                        base_net_summary = {"error": repr(e)}
                    (out_dir / "net_summary.json").write_text(
                        json.dumps(base_net_summary, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                elif tmp_har_path is not None and tmp_har_path.exists():
                    har_out = out_dir / "network.har"
                    try:
                        os.replace(tmp_har_path, har_out)
                    except Exception:
                        har_out.write_bytes(tmp_har_path.read_bytes())
                        try:
                            os.remove(tmp_har_path)
                        except Exception:
                            pass

                    try:
                        base_net_summary = summarize_har(har_out)
                    except Exception as e:
                        base_net_summary = {"error": repr(e)}

                    (out_dir / "net_summary.json").write_text(
                        json.dumps(base_net_summary, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                else:
                    base_net_summary = {"note": "net_summary_disabled"}
                    (out_dir / "net_summary.json").write_text(
                        json.dumps(base_net_summary, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                if DRY_RUN and isinstance(base_net_summary, dict):
                    issues = validate_net_summary(base_net_summary)
                    if issues:
                        print("  [DRY_RUN] net_summary issues:", "; ".join(issues))

                diff_summary_data = None
                if ENABLE_VARIANTS:
                    variants_root = out_dir / "variants"
                    variants_root.mkdir(parents=True, exist_ok=True)

                    net_for_diff = base_net_summary if RECORD_NET_EVIDENCE_LITE else None
                    base_summary, base_text_feat = build_variant_summary(payload, net_for_diff)

                    variant_summaries: Dict[str, dict] = {}
                    diff_by_variant: Dict[str, dict] = {}
                    errors: Dict[str, str] = {}
                    flags: List[str] = []
                    used_names = set()

                    variants_list = VARIANTS[:MAX_VARIANT_COUNT]
                    if len(VARIANTS) > MAX_VARIANT_COUNT:
                        errors["_variant_limit"] = f"variant_limit:{MAX_VARIANT_COUNT}"

                    variant_start = time.time()
                    idx = 0
                    while idx < len(variants_list):
                        if (time.time() - variant_start) * 1000 > VARIANT_TOTAL_TIMEOUT_MS:
                            for j in range(idx, len(variants_list)):
                                cfg = variants_list[j]
                                raw_name = cfg.get("name") or f"variant_{j + 1}"
                                name = sanitize_variant_name(raw_name)
                                if name in used_names:
                                    name = f"{name}_{j + 1}"
                                used_names.add(name)
                                vdir = variants_root / name
                                vdir.mkdir(parents=True, exist_ok=True)
                                timeout_headless = cfg.get("headless")
                                if timeout_headless is None:
                                    timeout_headless = HEADLESS
                                meta_variant = {
                                    "name": name,
                                    "config": {
                                        "user_agent": cfg.get("user_agent"),
                                        "locale": cfg.get("locale"),
                                        "timezone_id": cfg.get("timezone_id"),
                                        "viewport": cfg.get("viewport") or VIEWPORT,
                                        "headless": timeout_headless,
                                        "proxy_server": (normalize_proxy_config(cfg.get("proxy")) or base_proxy or {}).get("server"),
                                    },
                                    "status": None,
                                    "final_url": None,
                                    "title": None,
                                    "error": "variant_total_timeout",
                                }
                                (vdir / "meta_variant.json").write_text(
                                    json.dumps(meta_variant, ensure_ascii=False, indent=2),
                                    encoding="utf-8",
                                )
                                errors[name] = "variant_total_timeout"
                            break

                        cfg = variants_list[idx]
                        idx += 1
                        raw_name = cfg.get("name") or f"variant_{idx}"
                        name = sanitize_variant_name(raw_name)
                        if name in used_names:
                            name = f"{name}_{idx}"
                        used_names.add(name)

                        vdir = variants_root / name
                        vdir.mkdir(parents=True, exist_ok=True)

                        variant_proxy = normalize_proxy_config(cfg.get("proxy")) or base_proxy
                        variant_headless = cfg.get("headless")
                        if variant_headless is None:
                            variant_headless = HEADLESS
                        result = capture_variant(
                            url,
                            cfg,
                            browser_mgr,
                            variant_headless,
                            route_handler,
                            variant_proxy,
                            nav_timeout_ms,
                            goto_wait_until,
                            enable_route_intercept,
                            label,
                        )
                        meta_variant = {
                            "name": name,
                            "config": {
                                "user_agent": cfg.get("user_agent"),
                                "locale": cfg.get("locale"),
                                "timezone_id": cfg.get("timezone_id"),
                                "viewport": cfg.get("viewport") or VIEWPORT,
                                "headless": variant_headless,
                                "proxy_server": (variant_proxy or {}).get("server"),
                            },
                            "status": None,
                            "final_url": None,
                            "title": None,
                            "error": result.get("error"),
                            "elapsed_ms": result.get("elapsed_ms"),
                        }

                        if result.get("success") and result.get("payload"):
                            vpayload = result["payload"]
                            meta_variant["status"] = vpayload.get("status")
                            meta_variant["final_url"] = sanitize_url_for_summary(vpayload.get("final_url") or "")
                            meta_variant["title"] = (vpayload.get("page_signals") or {}).get("title")

                            (vdir / "screenshot_viewport.png").write_bytes(vpayload["screenshot_viewport_bytes"])
                            if vpayload.get("html_rendered"):
                                (vdir / "html_rendered.html").write_text(
                                    vpayload["html_rendered"], encoding="utf-8", errors="ignore"
                                )
                            if vpayload.get("visible_text"):
                                (vdir / "visible_text.txt").write_text(
                                    vpayload["visible_text"], encoding="utf-8", errors="ignore"
                                )
                            if vpayload.get("forms_json"):
                                (vdir / "forms.json").write_text(
                                    json.dumps(vpayload.get("forms_json", {"forms": []}), ensure_ascii=False, indent=2),
                                    encoding="utf-8",
                                )

                            if RECORD_NET_EVIDENCE_LITE and result.get("net_summary") is not None:
                                (vdir / "net_summary.json").write_text(
                                    json.dumps(result["net_summary"], ensure_ascii=False, indent=2),
                                    encoding="utf-8",
                                )

                            variant_summary, variant_text_feat = build_variant_summary(
                                vpayload, result.get("net_summary")
                            )
                            variant_summaries[name] = variant_summary
                            diff_by_variant[name] = {
                                "visible_text": diff_visible_text(base_text_feat, variant_text_feat),
                                "forms": diff_forms(
                                    base_summary.get("forms_summary") or {},
                                    variant_summary.get("forms_summary") or {},
                                ),
                                "network": diff_network(
                                    base_summary.get("network_summary") or {},
                                    variant_summary.get("network_summary") or {},
                                ),
                                "final_url_changed": base_summary.get("final_url")
                                != variant_summary.get("final_url"),
                            }
                            vpayload.pop("screenshot_viewport_bytes", None)
                            vpayload.pop("html_rendered", None)
                            vpayload.pop("visible_text", None)
                            vpayload.pop("forms_json", None)
                            result["payload"] = None
                        else:
                            errors[name] = result.get("error") or "variant_failed"

                        (vdir / "meta_variant.json").write_text(
                            json.dumps(meta_variant, ensure_ascii=False, indent=2),
                            encoding="utf-8",
                        )

                    base_len = base_text_feat.get("len") or 0
                    for diff in diff_by_variant.values():
                        text_diff = diff.get("visible_text") or {}
                        forms_diff = diff.get("forms") or {}
                        net_diff = diff.get("network") or {}
                        if diff.get("final_url_changed"):
                            flags.append("dynamic_redirect")
                        if is_large_text_diff(base_len, text_diff):
                            flags.append("possible_cloaking")
                        if forms_diff.get("has_password_changed") or forms_diff.get("action_domain_changed"):
                            flags.append("possible_cloaking")
                        if net_diff.get("post_targets_changed") or (net_diff.get("third_party_domains_delta") or 0) >= 5:
                            flags.append("possible_cloaking")

                    if errors:
                        flags.append("variant_failed")

                    diff_summary = {
                        "base": base_summary,
                        "variants": variant_summaries,
                        "diff": diff_by_variant,
                        "flags": sorted(set(flags)),
                    }
                    diff_summary_data = diff_summary
                    if errors:
                        diff_summary["errors"] = errors

                    (out_dir / "diff_summary.json").write_text(
                        json.dumps(diff_summary, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )

                if SAVE_AUTO_LABELS:
                    try:
                        auto_labels = derive_auto_labels(
                            input_url=payload_input_url,
                            final_url=payload_final_url,
                            visible_text=payload_visible_text,
                            forms_json=payload_forms_json,
                            net_summary=base_net_summary,
                            html_rendered=payload_html_rendered,
                            html_raw=payload_html_raw,
                            diff_summary=diff_summary_data,
                            page_title=payload_page_title,
                            label=label,
                            response_header_flags=payload_response_header_flags,
                            source="crawler_v6_inline",
                            lexicon_path=args.brand_lexicon or None,
                        )
                        (out_dir / "auto_labels.json").write_text(
                            json.dumps(auto_labels, ensure_ascii=False, indent=2),
                            encoding="utf-8",
                        )
                        if SAVE_RULE_LABELS:
                            rule_labels = derive_rule_labels(auto_labels)
                            (out_dir / "rule_labels.json").write_text(
                                json.dumps(rule_labels, ensure_ascii=False, indent=2),
                                encoding="utf-8",
                            )
                    except Exception as e:
                        print(f"  [WARN] auto_labels failed: {repr(e)}")

                payload.pop("visible_text", None)
                payload.pop("forms_json", None)
                payload.pop("actions", None)
                payload.pop("step1", None)

                ok_cnt += 1
                print(f"  -> OK final={payload.get('final_url')} saved={out_dir.name}")

            except Exception as e:
                fail_cnt += 1
                print(f"  -> FAIL/SKIP: {repr(e)}")
                if is_driver_connection_closed_error(e):
                    try:
                        browser_mgr.relaunch(HEADLESS, base_proxy)
                    except Exception:
                        pass
                if tmp_har_path is not None:
                    try:
                        os.remove(tmp_har_path)
                    except Exception:
                        pass
                try:
                    if context is not None:
                        context.close()
                except Exception:
                    pass

        browser_mgr.close_all()

    print(f"[DONE] success={ok_cnt}/{total_urls} failed_or_skipped={fail_cnt}")


if __name__ == "__main__":
    main()
