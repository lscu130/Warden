#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Warden TRAINSET_V1 manifest builder

目标：
1. 扫描样本目录，识别 screenshot / html / metadata / rule_labels 等文件
2. 可选合并外部标签表（CSV / JSON / JSONL）
3. 生成 manifest_trainset_v1.csv / parquet
4. 以 group_key（默认注册域）为单位进行 deterministic split，避免泄漏
5. 导出 splits 与基础 stats

设计原则：
- 对未知目录结构保持宽容，尽量通过常见文件名候选自动发现
- 对字段冻结保持克制：manifest 只导出训练真正要用的稳定字段
- rule_labels 仅作弱标签/辅助特征，不当作人工金标签
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

try:
    import pandas as pd
except Exception as exc:
    raise SystemExit("需要 pandas：pip install pandas pyarrow") from exc

# -----------------------------
# 头部配置区：优先在这里改你本地的输入/输出路径
# 命令行参数仍可覆盖这些默认值
# -----------------------------
CONFIG_DATA_ROOT = "./data"
CONFIG_INPUT_ROOTS = [
    "./data/raw/phish",
    "./data/raw/benign",
]
CONFIG_LABELS_PATH = "./data/labels/labels_v1.csv"  # 没有外部标签表就设为 None
CONFIG_OUTPUT_DIR = "./data/processed/trainset_v1"

# 导出文件名配置
CONFIG_MANIFEST_CSV_NAME = "manifest_trainset_v1.csv"
CONFIG_MANIFEST_PARQUET_NAME = "manifest_trainset_v1.parquet"
CONFIG_SPLITS_DIR_NAME = "splits"
CONFIG_STATS_DIR_NAME = "stats"
CONFIG_README_NAME = "README.md"

# -----------------------------
# 可按你本地实际结构微调的默认候选名
# -----------------------------
SCREENSHOT_CANDIDATES = [
    "screenshot.png", "screenshot.jpg", "screenshot.jpeg", "screenshot.webp",
    "page.png", "page.jpg", "page.jpeg", "page.webp",
    "shot.png", "screen.png", "capture.png",
]
HTML_CANDIDATES = [
    "page.html", "index.html", "final.html", "dom.html", "raw.html",
]
TEXT_CANDIDATES = [
    "visible_text.txt", "page_text.txt", "text.txt", "content.txt",
]
METADATA_CANDIDATES = [
    "metadata.json", "meta.json", "capture_meta.json", "manifest.json",
]
RULE_LABEL_CANDIDATES = [
    "rule_labels.json", "auto_labels.json", "weak_labels.json",
]

VALID_SCREEN_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
VALID_HTML_EXTS = {".html", ".htm"}
VALID_TEXT_EXTS = {".txt"}

LABEL_TRUE = {"1", "true", "yes", "y", "phish", "malicious", "positive", "pos"}
LABEL_FALSE = {"0", "false", "no", "n", "benign", "negative", "neg", "safe"}
REVIEW_TRUE = {"1", "true", "yes", "y", "reviewed", "done", "human_reviewed", "approved"}


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


# -----------------------------
# 基础工具函数
# -----------------------------
def load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {"_value": data}
    except Exception:
        return {}


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        rows.append(obj)
                except Exception:
                    continue
    except Exception:
        return []
    return rows



def normalize_bool_like(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        if value == 1:
            return True
        if value == 0:
            return False
        return None
    s = str(value).strip().lower()
    if s in LABEL_TRUE or s in REVIEW_TRUE:
        return True
    if s in LABEL_FALSE:
        return False
    return None



def normalize_label_binary(value: Any) -> Optional[int]:
    b = normalize_bool_like(value)
    if b is None:
        return None
    return 1 if b else 0



def normalize_review_status(value: Any) -> str:
    b = normalize_bool_like(value)
    if b is None:
        s = str(value).strip().lower() if value is not None else ""
        return s or "unreviewed"
    return "reviewed" if b else "unreviewed"



def first_non_empty(*values: Any) -> Any:
    for v in values:
        if v is None:
            continue
        if isinstance(v, str) and not v.strip():
            continue
        return v
    return None



def sha1_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()



def stable_hash_to_unit_interval(text: str, seed: int) -> float:
    h = hashlib.sha1(f"{seed}::{text}".encode("utf-8")).hexdigest()
    # 取前 15 位，足够 deterministic
    return int(h[:15], 16) / float(16 ** 15 - 1)



def safe_relpath(path: Optional[Path], start: Path) -> Optional[str]:
    if path is None:
        return None
    try:
        return str(path.resolve().relative_to(start.resolve()))
    except Exception:
        try:
            return str(path.relative_to(start))
        except Exception:
            return str(path)



def deep_get(data: Dict[str, Any], *keys: str) -> Any:
    cur: Any = data
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur



def flatten_scalar_dict(prefix: str, data: Dict[str, Any], out: Dict[str, Any]) -> None:
    for k, v in data.items():
        key = f"{prefix}{k}"
        if isinstance(v, (str, int, float, bool)) or v is None:
            out[key] = v


# -----------------------------
# 域名 / 注册域
# -----------------------------
def extract_hostname(url_or_host: Optional[str]) -> Optional[str]:
    if not url_or_host:
        return None
    s = str(url_or_host).strip()
    if not s:
        return None
    if "://" not in s:
        # 允许直接给 host
        if "/" not in s and " " not in s:
            return s.lower().strip(".")
        s = "http://" + s
    try:
        host = urlparse(s).hostname
        return host.lower() if host else None
    except Exception:
        return None


# 优先尝试更靠谱的库，没有就退化为简单启发式
try:
    import tldextract  # type: ignore

    def get_registered_domain(hostname: Optional[str]) -> Optional[str]:
        if not hostname:
            return None
        ext = tldextract.extract(hostname)
        if ext.domain and ext.suffix:
            return f"{ext.domain}.{ext.suffix}".lower()
        return hostname.lower()

except Exception:
    MULTI_PART_SUFFIXES = {
        "co.uk", "org.uk", "gov.uk", "ac.uk", "com.cn", "net.cn", "org.cn",
        "gov.cn", "com.au", "net.au", "org.au", "co.jp", "co.kr", "com.br",
    }

    def get_registered_domain(hostname: Optional[str]) -> Optional[str]:
        if not hostname:
            return None
        host = hostname.lower().strip(".")
        parts = host.split(".")
        if len(parts) <= 2:
            return host
        suffix2 = ".".join(parts[-2:])
        suffix3 = ".".join(parts[-3:])
        if suffix2 in MULTI_PART_SUFFIXES and len(parts) >= 3:
            return ".".join(parts[-3:])
        if suffix3 in MULTI_PART_SUFFIXES and len(parts) >= 4:
            return ".".join(parts[-4:])
        return ".".join(parts[-2:])


# -----------------------------
# 文件发现
# -----------------------------
def find_first_existing(base: Path, candidates: Sequence[str]) -> Optional[Path]:
    for name in candidates:
        p = base / name
        if p.exists() and p.is_file():
            return p
    return None



def heuristic_find_file(base: Path, exts: set[str], preferred_keywords: Sequence[str]) -> Optional[Path]:
    files = [p for p in base.iterdir() if p.is_file() and p.suffix.lower() in exts]
    if not files:
        return None

    # 先按关键词加权
    scored: List[Tuple[int, Path]] = []
    for p in files:
        name = p.name.lower()
        score = 0
        for i, kw in enumerate(preferred_keywords):
            if kw in name:
                score += 100 - i
        # 避免选择缩略图、临时文件
        if "thumb" in name or "temp" in name:
            score -= 20
        scored.append((score, p))
    scored.sort(key=lambda x: (-x[0], x[1].name))
    return scored[0][1]



def discover_sample_files(sample_dir: Path) -> Dict[str, Optional[Path]]:
    screenshot = find_first_existing(sample_dir, SCREENSHOT_CANDIDATES)
    if screenshot is None:
        screenshot = heuristic_find_file(sample_dir, VALID_SCREEN_EXTS, ["screenshot", "screen", "page", "capture", "shot"])

    html = find_first_existing(sample_dir, HTML_CANDIDATES)
    if html is None:
        html = heuristic_find_file(sample_dir, VALID_HTML_EXTS, ["page", "index", "final", "dom", "raw"])

    text = find_first_existing(sample_dir, TEXT_CANDIDATES)
    if text is None:
        text = heuristic_find_file(sample_dir, VALID_TEXT_EXTS, ["text", "visible", "content", "page"])

    metadata = find_first_existing(sample_dir, METADATA_CANDIDATES)
    if metadata is None:
        # 偏向 metadata / meta 命名的 json
        json_files = [p for p in sample_dir.iterdir() if p.is_file() and p.suffix.lower() == ".json"]
        if json_files:
            json_files.sort(key=lambda p: (0 if "meta" in p.name.lower() else 1, p.name))
            metadata = json_files[0]

    rule_labels = find_first_existing(sample_dir, RULE_LABEL_CANDIDATES)
    if rule_labels is None:
        json_files = [p for p in sample_dir.iterdir() if p.is_file() and p.suffix.lower() == ".json"]
        candidates = [p for p in json_files if "rule" in p.name.lower() or "label" in p.name.lower()]
        if candidates:
            candidates.sort(key=lambda p: p.name)
            rule_labels = candidates[0]

    return {
        "screenshot_path": screenshot,
        "html_path": html,
        "text_path": text,
        "metadata_path": metadata,
        "rule_labels_path": rule_labels,
    }



def looks_like_sample_dir(path: Path) -> bool:
    if not path.is_dir():
        return False
    names = {p.name.lower() for p in path.iterdir() if p.is_file()}
    if any(name in names for name in [n.lower() for n in SCREENSHOT_CANDIDATES + HTML_CANDIDATES + METADATA_CANDIDATES]):
        return True
    files = list(path.iterdir())
    has_img = any(p.is_file() and p.suffix.lower() in VALID_SCREEN_EXTS for p in files)
    has_html = any(p.is_file() and p.suffix.lower() in VALID_HTML_EXTS for p in files)
    has_json = any(p.is_file() and p.suffix.lower() == ".json" for p in files)
    return (has_img and has_html) or (has_img and has_json) or (has_html and has_json)



def iter_sample_dirs(input_roots: Sequence[Path], max_depth: int = 3) -> Iterable[Path]:
    seen: set[Path] = set()
    for root in input_roots:
        root = root.resolve()
        if not root.exists():
            continue
        if looks_like_sample_dir(root):
            if root not in seen:
                seen.add(root)
                yield root
            continue
        for dirpath, dirnames, _filenames in os.walk(root):
            cur = Path(dirpath)
            depth = len(cur.relative_to(root).parts)
            if depth > max_depth:
                dirnames[:] = []
                continue
            if looks_like_sample_dir(cur) and cur not in seen:
                seen.add(cur)
                yield cur
                dirnames[:] = []  # 样本目录内部不再继续深挖


# -----------------------------
# 标签表加载与合并
# -----------------------------
def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    if suffix == ".json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return pd.DataFrame(data)
        if isinstance(data, dict):
            # 尝试 records / data 包裹
            if isinstance(data.get("records"), list):
                return pd.DataFrame(data["records"])
            if isinstance(data.get("data"), list):
                return pd.DataFrame(data["data"])
            return pd.DataFrame([data])
    if suffix == ".jsonl":
        return pd.DataFrame(load_jsonl(path))
    raise ValueError(f"不支持的标签表格式: {path}")



def normalize_labels_df(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    for col in df.columns:
        lc = str(col).strip().lower()
        if lc in {"id", "sample", "sampleid"}:
            rename_map[col] = "sample_id"
        elif lc in {"final_url", "finalurl", "url_final", "landing_url"}:
            rename_map[col] = "final_url"
        elif lc in {"original_url", "orig_url", "source_url", "url"}:
            rename_map[col] = "original_url"
        elif lc in {"label", "binary_label", "is_malicious", "is_phish", "phish", "target"}:
            rename_map[col] = "label_binary"
        elif lc in {"reviewed", "human_reviewed", "is_reviewed", "review_status"}:
            rename_map[col] = "review_status"
        elif lc in {"labelsource", "label_src", "source"}:
            rename_map[col] = "label_source"
        elif lc in {"quality", "quality_grade", "q"}:
            rename_map[col] = "quality_grade"
        elif lc in {"brandconf", "brand_conf", "brand_score"}:
            rename_map[col] = "brand_confidence"
        elif lc in {"brandsrc", "brand_src"}:
            rename_map[col] = "brand_source"
        elif lc in {"risk_type", "threat_type", "intent_type"}:
            rename_map[col] = "risk_type"
    df = df.rename(columns=rename_map).copy()

    if "sample_id" in df.columns:
        df["sample_id"] = df["sample_id"].astype(str)

    if "label_binary" in df.columns:
        df["label_binary"] = df["label_binary"].apply(normalize_label_binary)

    if "review_status" in df.columns:
        df["review_status"] = df["review_status"].apply(normalize_review_status)

    if "label_source" in df.columns:
        df["label_source"] = df["label_source"].fillna("").astype(str)
        df.loc[df["label_source"].str.strip() == "", "label_source"] = "unknown"

    return df



def merge_label_row(sample: Dict[str, Any], labels_df: Optional[pd.DataFrame]) -> Dict[str, Any]:
    if labels_df is None or labels_df.empty:
        return sample

    row = None
    sid = sample.get("sample_id")
    final_url = sample.get("final_url")
    original_url = sample.get("original_url")

    if sid and "sample_id" in labels_df.columns:
        matched = labels_df.loc[labels_df["sample_id"].astype(str) == str(sid)]
        if len(matched) == 1:
            row = matched.iloc[0].to_dict()
        elif len(matched) > 1:
            # 重复 sample_id 很脏，但还是先拿第一条
            row = matched.iloc[0].to_dict()

    if row is None and final_url and "final_url" in labels_df.columns:
        matched = labels_df.loc[labels_df["final_url"].astype(str) == str(final_url)]
        if len(matched) >= 1:
            row = matched.iloc[0].to_dict()

    if row is None and original_url and "original_url" in labels_df.columns:
        matched = labels_df.loc[labels_df["original_url"].astype(str) == str(original_url)]
        if len(matched) >= 1:
            row = matched.iloc[0].to_dict()

    if row is None:
        return sample

    merged = dict(sample)
    for k, v in row.items():
        if k not in merged or merged[k] in (None, "", "unknown"):
            merged[k] = v
        elif k in {"label_binary", "review_status", "label_source", "quality_grade", "risk_type", "brand", "brand_source", "brand_confidence"}:
            # 标签表比抓取 metadata 更接近人工真值，允许覆盖这些关键列
            if v is not None and str(v) != "":
                merged[k] = v
    return merged


# -----------------------------
# 样本解析
# -----------------------------
def infer_label_source(metadata: Dict[str, Any], has_rule_labels: bool) -> str:
    candidates = [
        metadata.get("label_source"),
        deep_get(metadata, "labels", "label_source"),
        deep_get(metadata, "annotation", "label_source"),
    ]
    value = first_non_empty(*candidates)
    if value:
        return str(value)
    return "rule" if has_rule_labels else "unknown"



def infer_review_status(metadata: Dict[str, Any]) -> str:
    candidates = [
        metadata.get("review_status"),
        metadata.get("reviewed"),
        deep_get(metadata, "annotation", "review_status"),
        deep_get(metadata, "annotation", "reviewed"),
    ]
    return normalize_review_status(first_non_empty(*candidates))



def infer_brand(metadata: Dict[str, Any], rule_labels: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], Optional[float]]:
    brand = first_non_empty(
        metadata.get("brand"),
        deep_get(metadata, "labels", "brand"),
        deep_get(metadata, "annotation", "brand"),
        rule_labels.get("brand"),
        deep_get(rule_labels, "brand", "name"),
    )
    brand_source = first_non_empty(
        metadata.get("brand_source"),
        deep_get(metadata, "labels", "brand_source"),
        rule_labels.get("brand_source"),
        "rule" if brand else None,
    )
    brand_conf = first_non_empty(
        metadata.get("brand_confidence"),
        deep_get(metadata, "labels", "brand_confidence"),
        rule_labels.get("brand_confidence"),
        deep_get(rule_labels, "brand", "confidence"),
    )
    try:
        brand_conf = float(brand_conf) if brand_conf is not None and str(brand_conf) != "" else None
    except Exception:
        brand_conf = None
    if brand is not None:
        brand = str(brand)
    if brand_source is not None:
        brand_source = str(brand_source)
    return brand, brand_source, brand_conf



def infer_risk_type(metadata: Dict[str, Any], rule_labels: Dict[str, Any]) -> Optional[str]:
    return first_non_empty(
        metadata.get("risk_type"),
        deep_get(metadata, "labels", "risk_type"),
        deep_get(metadata, "annotation", "risk_type"),
        rule_labels.get("risk_type"),
        deep_get(rule_labels, "labels", "risk_type"),
    )



def infer_label_binary(metadata: Dict[str, Any], rule_labels: Dict[str, Any], dir_hint: Optional[str]) -> Optional[int]:
    # 先看 metadata / annotation / labels
    candidates = [
        metadata.get("label_binary"),
        metadata.get("label"),
        metadata.get("is_malicious"),
        metadata.get("is_phish"),
        deep_get(metadata, "labels", "label_binary"),
        deep_get(metadata, "annotation", "label_binary"),
    ]
    for c in candidates:
        value = normalize_label_binary(c)
        if value is not None:
            return value

    # 再看 rule_labels 中是否已有二分类提示（注意仍只是弱标签）
    rule_candidates = [
        rule_labels.get("label_binary"),
        rule_labels.get("is_malicious"),
        rule_labels.get("is_phish"),
        deep_get(rule_labels, "labels", "label_binary"),
    ]
    for c in rule_candidates:
        value = normalize_label_binary(c)
        if value is not None:
            return value

    # 最后仅作为弱兜底：如果目录名明确是 phish / benign，才用目录提示
    if dir_hint:
        hint = dir_hint.lower()
        if any(x in hint for x in ["phish", "malicious", "positive", "pos"]):
            return 1
        if any(x in hint for x in ["benign", "safe", "negative", "neg", "normal"]):
            return 0
    return None



def infer_urls(metadata: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    original_url = first_non_empty(
        metadata.get("original_url"), metadata.get("orig_url"), metadata.get("source_url"), metadata.get("url")
    )
    final_url = first_non_empty(
        metadata.get("final_url"), metadata.get("landing_url"), metadata.get("resolved_url"), deep_get(metadata, "navigation", "final_url")
    )
    return original_url, final_url



def infer_language(metadata: Dict[str, Any]) -> Optional[str]:
    return first_non_empty(
        metadata.get("language"), metadata.get("lang"), deep_get(metadata, "page", "language")
    )



def infer_title(metadata: Dict[str, Any]) -> Optional[str]:
    return first_non_empty(
        metadata.get("title"), metadata.get("page_title"), deep_get(metadata, "page", "title")
    )



def infer_site_category(metadata: Dict[str, Any]) -> Optional[str]:
    return first_non_empty(
        metadata.get("site_category"), metadata.get("category"), deep_get(metadata, "page", "site_category")
    )



def infer_capture_time(metadata: Dict[str, Any]) -> Optional[str]:
    return first_non_empty(
        metadata.get("capture_time"), metadata.get("captured_at"), metadata.get("timestamp"), metadata.get("created_at")
    )



def infer_quality_grade(has_screenshot: bool, has_html: bool, has_url: bool, review_status: str, label_source: str) -> str:
    if has_screenshot and has_html and has_url and review_status == "reviewed":
        return "Q1"
    if has_screenshot and has_html and has_url:
        return "Q2"
    if (has_screenshot or has_html) and has_url:
        return "Q3"
    if label_source == "rule":
        return "Q4"
    return "Q4"



def parse_sample(sample_dir: Path, data_root: Path) -> Dict[str, Any]:
    files = discover_sample_files(sample_dir)
    metadata = load_json(files["metadata_path"]) if files["metadata_path"] else {}
    rule_labels = load_json(files["rule_labels_path"]) if files["rule_labels_path"] else {}

    # sample_id: 元数据优先，其次目录名
    sample_id = first_non_empty(
        metadata.get("sample_id"), metadata.get("id"), deep_get(metadata, "sample", "id"), sample_dir.name
    )
    sample_id = str(sample_id)

    original_url, final_url = infer_urls(metadata)
    hostname = extract_hostname(first_non_empty(final_url, original_url))
    registered_domain = get_registered_domain(hostname)

    label_binary = infer_label_binary(metadata, rule_labels, sample_dir.parent.name if sample_dir.parent != sample_dir else None)
    review_status = infer_review_status(metadata)
    label_source = infer_label_source(metadata, has_rule_labels=files["rule_labels_path"] is not None)
    brand, brand_source, brand_confidence = infer_brand(metadata, rule_labels)
    risk_type = infer_risk_type(metadata, rule_labels)
    title = infer_title(metadata)
    language = infer_language(metadata)
    site_category = infer_site_category(metadata)
    capture_time = infer_capture_time(metadata)

    has_screenshot = files["screenshot_path"] is not None
    has_html = files["html_path"] is not None
    has_url = bool(first_non_empty(final_url, original_url))
    quality_grade = infer_quality_grade(has_screenshot, has_html, has_url, review_status, label_source)

    # 简单内容指纹：URL / 注册域 / 样本目录组合，防止 sample_id 复用时完全迷路
    content_fingerprint = sha1_text("||".join([
        sample_id,
        str(first_non_empty(final_url, original_url, "")),
        str(registered_domain or ""),
        str(sample_dir.resolve()),
    ]))

    row: Dict[str, Any] = {
        "dataset_version": "trainset_v1",
        "sample_id": sample_id,
        "source_dir": safe_relpath(sample_dir, data_root),
        "metadata_path": safe_relpath(files["metadata_path"], data_root),
        "rule_labels_path": safe_relpath(files["rule_labels_path"], data_root),
        "screenshot_path": safe_relpath(files["screenshot_path"], data_root),
        "html_path": safe_relpath(files["html_path"], data_root),
        "text_path": safe_relpath(files["text_path"], data_root),
        "original_url": original_url,
        "final_url": final_url,
        "hostname": hostname,
        "registered_domain": registered_domain,
        "page_title": title,
        "page_language": language,
        "site_category": site_category,
        "capture_time": capture_time,
        "label_binary": label_binary,
        "risk_type": risk_type,
        "brand": brand,
        "brand_source": brand_source,
        "brand_confidence": brand_confidence,
        "label_source": label_source,
        "review_status": review_status,
        "quality_grade": quality_grade,
        "has_screenshot": has_screenshot,
        "has_html": has_html,
        "has_text": files["text_path"] is not None,
        "has_rule_labels": files["rule_labels_path"] is not None,
        "completeness_ok": has_screenshot and has_html and has_url,
        "group_key": registered_domain or hostname or sample_id,
        "content_fingerprint": content_fingerprint,
    }

    # 轻量保留一些 metadata / rule_labels 的标量字段，方便调试分析，不把 manifest 搞成垃圾场
    flatten_scalar_dict("meta_", metadata, row)
    flatten_scalar_dict("rule_", rule_labels, row)

    return row


# -----------------------------
# 去重与切分
# -----------------------------
def mark_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # 粗粒度重复键：final_url > original_url > (group_key + title)
    dedup_key = []
    for _, r in out.iterrows():
        key = first_non_empty(
            r.get("final_url"),
            r.get("original_url"),
            f"{r.get('group_key')}||{r.get('page_title')}",
            r.get("content_fingerprint"),
        )
        dedup_key.append(str(key))
    out["dedup_key"] = dedup_key

    dup_counts = Counter(dedup_key)
    out["is_duplicate_candidate"] = out["dedup_key"].map(lambda x: dup_counts.get(x, 0) > 1)

    # 每个 dedup_key 保留质量更高者：Q1 > Q2 > Q3 > Q4，reviewed 优先，再按 sample_id
    q_rank = {"Q1": 4, "Q2": 3, "Q3": 2, "Q4": 1}
    out["_q_rank"] = out["quality_grade"].map(lambda x: q_rank.get(str(x), 0))
    out["_review_rank"] = out["review_status"].map(lambda x: 1 if str(x) == "reviewed" else 0)
    out = out.sort_values(by=["dedup_key", "_q_rank", "_review_rank", "sample_id"], ascending=[True, False, False, True]).copy()
    out["is_canonical"] = ~out.duplicated(subset=["dedup_key"], keep="first")
    out = out.drop(columns=["_q_rank", "_review_rank"])
    return out



def assign_splits(df: pd.DataFrame, train_ratio: float, val_ratio: float, test_ratio: float, seed: int) -> pd.DataFrame:
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-8
    out = df.copy()

    # group_key 粒度切分，避免域内泄漏
    group_to_split: Dict[str, str] = {}
    unique_groups = sorted(set(str(x) for x in out["group_key"].fillna("")))
    for g in unique_groups:
        u = stable_hash_to_unit_interval(g, seed)
        if u < train_ratio:
            split = "train"
        elif u < train_ratio + val_ratio:
            split = "val"
        else:
            split = "test"
        group_to_split[g] = split

    out["split"] = out["group_key"].astype(str).map(group_to_split)
    return out


# -----------------------------
# 质检与统计
# -----------------------------
def apply_trainset_v1_filters(df: pd.DataFrame, require_label: bool, canonical_only: bool) -> pd.DataFrame:
    out = df.copy()
    # 基础入选条件：截图 + HTML + URL
    out = out.loc[(out["has_screenshot"] == True) & (out["has_html"] == True)].copy()
    out = out.loc[out[["final_url", "original_url"]].notna().any(axis=1)].copy()

    if require_label:
        out = out.loc[out["label_binary"].isin([0, 1])].copy()

    if canonical_only and "is_canonical" in out.columns:
        out = out.loc[out["is_canonical"] == True].copy()

    return out



def build_stats(df: pd.DataFrame) -> Dict[str, Any]:
    def counter_dict(series: pd.Series) -> Dict[str, int]:
        c = Counter(str(x) for x in series.fillna("<NA>"))
        return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))

    stats = {
        "num_rows": int(len(df)),
        "class_distribution": counter_dict(df["label_binary"] if "label_binary" in df.columns else pd.Series(dtype=object)),
        "split_distribution": counter_dict(df["split"] if "split" in df.columns else pd.Series(dtype=object)),
        "brand_distribution": counter_dict(df["brand"] if "brand" in df.columns else pd.Series(dtype=object)),
        "source_distribution": counter_dict(df["label_source"] if "label_source" in df.columns else pd.Series(dtype=object)),
        "quality_distribution": counter_dict(df["quality_grade"] if "quality_grade" in df.columns else pd.Series(dtype=object)),
        "review_distribution": counter_dict(df["review_status"] if "review_status" in df.columns else pd.Series(dtype=object)),
    }
    return stats



def write_stats(stats_dir: Path, df: pd.DataFrame) -> None:
    stats_dir.mkdir(parents=True, exist_ok=True)
    stats = build_stats(df)
    for key, value in stats.items():
        path = stats_dir / f"{key}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(value, f, ensure_ascii=False, indent=2)



def write_splits(splits_dir: Path, df: pd.DataFrame) -> None:
    splits_dir.mkdir(parents=True, exist_ok=True)
    for split in ["train", "val", "test"]:
        ids = df.loc[df["split"] == split, "sample_id"].astype(str).tolist()
        with (splits_dir / f"{split}_ids.txt").open("w", encoding="utf-8") as f:
            for sid in ids:
                f.write(sid + "\n")



def write_readme(path: Path, args: argparse.Namespace, raw_count: int, final_count: int) -> None:
    text = f"""# trainset_v1 export\n\n- dataset_version: trainset_v1\n- raw_scanned_samples: {raw_count}\n- exported_samples: {final_count}\n- input_roots: {', '.join(str(p) for p in args.input_roots)}\n- labels_path: {args.labels if args.labels else '<none>'}\n- seed: {args.seed}\n- split_ratio: train={args.train_ratio}, val={args.val_ratio}, test={args.test_ratio}\n- require_label: {args.require_label}\n- canonical_only: {args.canonical_only}\n\n说明：\n- `rule_labels` 仅作为弱标签 / 辅助线索，不等同于人工金标签。\n- split 按 `group_key`（默认注册域）做 deterministic assignment，避免明显域级泄漏。\n- manifest 只导出 TRAINSET_V1 真正需要的稳定字段。\n"""
    path.write_text(text, encoding="utf-8")


# -----------------------------
# CLI
# -----------------------------
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build Warden TRAINSET_V1 manifest")
    p.add_argument("--data-root", default=CONFIG_DATA_ROOT, help=f"数据根目录，默认 {CONFIG_DATA_ROOT}")
    p.add_argument("--input-roots", nargs="+", default=CONFIG_INPUT_ROOTS, help=f"待扫描的样本目录，可多个；默认 {CONFIG_INPUT_ROOTS}")
    p.add_argument("--out-dir", default=CONFIG_OUTPUT_DIR, help=f"输出目录，默认 {CONFIG_OUTPUT_DIR}")
    p.add_argument("--labels", default=CONFIG_LABELS_PATH, help=f"外部标签表路径（csv/json/jsonl/parquet），可选；默认 {CONFIG_LABELS_PATH}")
    p.add_argument("--max-depth", type=int, default=3, help="样本目录最大扫描深度")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--train-ratio", type=float, default=0.70)
    p.add_argument("--val-ratio", type=float, default=0.15)
    p.add_argument("--test-ratio", type=float, default=0.15)
    p.add_argument("--require-label", action="store_true", help="仅导出已有 label_binary 的样本")
    p.add_argument("--canonical-only", action="store_true", help="仅保留去重后 canonical 样本")
    p.add_argument("--keep-all-columns", action="store_true", help="保留 meta_*/rule_* 调试列；默认会裁剪为训练主字段")
    return p.parse_args()



def main() -> None:
    args = parse_args()
    ratio_sum = args.train_ratio + args.val_ratio + args.test_ratio
    if abs(ratio_sum - 1.0) > 1e-8:
        raise SystemExit(f"切分比例之和必须为 1.0，当前为 {ratio_sum}")

    data_root = Path(args.data_root).resolve()
    input_roots = [Path(p).resolve() for p in args.input_roots]
    out_dir = Path(args.out_dir).resolve() if args.out_dir else Path(CONFIG_OUTPUT_DIR).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    labels_df: Optional[pd.DataFrame] = None
    if args.labels:
        labels_path = Path(args.labels)
        if labels_path.exists():
            labels_df = normalize_labels_df(read_table(labels_path))
            log(f"[info] 已加载标签表: {args.labels}, rows={len(labels_df)}")
        else:
            log(f"[warn] 标签表不存在，已跳过: {args.labels}")

    rows: List[Dict[str, Any]] = []
    sample_dirs = list(iter_sample_dirs(input_roots, max_depth=args.max_depth))
    log(f"[info] 发现候选样本目录: {len(sample_dirs)}")

    for sample_dir in sample_dirs:
        try:
            row = parse_sample(sample_dir, data_root)
            row = merge_label_row(row, labels_df)
            rows.append(row)
        except Exception as exc:
            log(f"[warn] 解析失败，跳过 {sample_dir}: {exc}")

    if not rows:
        raise SystemExit("没有解析出任何样本。先检查目录层级、文件名候选或 --input-roots 是否正确。")

    df = pd.DataFrame(rows)
    raw_count = len(df)

    # 规范化关键列
    if "label_binary" in df.columns:
        df["label_binary"] = df["label_binary"].apply(normalize_label_binary)
    if "review_status" in df.columns:
        df["review_status"] = df["review_status"].apply(normalize_review_status)
    if "label_source" in df.columns:
        df["label_source"] = df["label_source"].fillna("unknown").astype(str)
    if "quality_grade" in df.columns:
        df["quality_grade"] = df["quality_grade"].fillna("Q4")

    df = mark_duplicates(df)
    df = assign_splits(df, args.train_ratio, args.val_ratio, args.test_ratio, args.seed)
    df = apply_trainset_v1_filters(df, require_label=args.require_label, canonical_only=args.canonical_only)

    # 默认裁剪到训练稳定字段，避免 manifest 胀成一团宇宙微波背景辐射
    stable_cols = [
        "dataset_version",
        "sample_id",
        "source_dir",
        "metadata_path",
        "rule_labels_path",
        "screenshot_path",
        "html_path",
        "text_path",
        "original_url",
        "final_url",
        "hostname",
        "registered_domain",
        "page_title",
        "page_language",
        "site_category",
        "capture_time",
        "label_binary",
        "risk_type",
        "brand",
        "brand_source",
        "brand_confidence",
        "label_source",
        "review_status",
        "quality_grade",
        "has_screenshot",
        "has_html",
        "has_text",
        "has_rule_labels",
        "completeness_ok",
        "group_key",
        "dedup_key",
        "is_duplicate_candidate",
        "is_canonical",
        "content_fingerprint",
        "split",
    ]
    if args.keep_all_columns:
        export_df = df.copy()
    else:
        keep = [c for c in stable_cols if c in df.columns]
        export_df = df[keep].copy()

    export_df = export_df.sort_values(by=["split", "sample_id"], ascending=[True, True]).reset_index(drop=True)

    csv_path = out_dir / CONFIG_MANIFEST_CSV_NAME
    parquet_path = out_dir / CONFIG_MANIFEST_PARQUET_NAME
    export_df.to_csv(csv_path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)
    try:
        export_df.to_parquet(parquet_path, index=False)
    except Exception as exc:
        log(f"[warn] 写 parquet 失败：{exc}")

    write_splits(out_dir / CONFIG_SPLITS_DIR_NAME, export_df)
    write_stats(out_dir / CONFIG_STATS_DIR_NAME, export_df)
    write_readme(out_dir / CONFIG_README_NAME, args, raw_count=raw_count, final_count=len(export_df))

    log(f"[done] raw_scanned_samples={raw_count}")
    log(f"[done] exported_samples={len(export_df)}")
    log(f"[done] csv={csv_path}")
    log(f"[done] parquet={parquet_path}")


if __name__ == "__main__":
    main()