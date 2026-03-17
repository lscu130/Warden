#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Warden TRAINSET_V1 dataset consistency checker

目标：
1. 检查 manifest 是否满足 TRAINSET_V1 的完整性要求
2. 检查关键字段逻辑一致性（label / brand / review / path / split）
3. 检查明显的数据泄漏（registered_domain / group_key / dedup_key / content_fingerprint 跨 split）
4. 产出可读报告与 machine-readable JSON 报告，供训练前把关

注意：
- 本脚本默认只做检查，不自动修复数据
- 发现问题时会输出 warning / error；若开启 --strict，则存在 error 时返回非 0
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import pandas as pd
except Exception as exc:
    raise SystemExit("需要 pandas：pip install pandas pyarrow") from exc


# -----------------------------
# 头部配置区：优先在这里改默认输入/输出位置
# 命令行参数仍可覆盖这些默认值
# -----------------------------
CONFIG_DATA_ROOT = "./data"
CONFIG_MANIFEST_PATH = "./data/processed/trainset_v1/manifest_trainset_v1.csv"
CONFIG_OUTPUT_DIR = "./data/processed/trainset_v1/consistency_check"


POSITIVE_RISK_HINTS = {
    "login_phish", "wallet_phish", "fake_support", "fake_giveaway", "fake_download",
    "payment_fraud", "credential_theft", "otp_phish", "seed_phrase_phish",
    "connect_wallet", "verify_account", "fake_security_check", "impersonation"
}

ALLOWED_SPLITS = {"train", "val", "test"}
ALLOWED_REVIEW_STATUS = {"reviewed", "unreviewed"}
ALLOWED_QUALITY = {"Q1", "Q2", "Q3", "Q4"}


def log(msg: str) -> None:
    print(msg, file=sys.stderr)


def read_table(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(path)
    if suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return pd.DataFrame(data)
        if isinstance(data, dict):
            if isinstance(data.get("records"), list):
                return pd.DataFrame(data["records"])
            if isinstance(data.get("data"), list):
                return pd.DataFrame(data["data"])
            return pd.DataFrame([data])
    if suffix == ".jsonl":
        rows = []
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
        return pd.DataFrame(rows)
    raise ValueError(f"不支持的 manifest 格式: {path}")


def safe_str(x: Any) -> str:
    if x is None:
        return ""
    if pd.isna(x):
        return ""
    return str(x)


def is_empty(x: Any) -> bool:
    if x is None:
        return True
    try:
        if pd.isna(x):
            return True
    except Exception:
        pass
    return str(x).strip() == ""


def norm_label_binary(x: Any) -> Optional[int]:
    if x is None:
        return None
    try:
        if pd.isna(x):
            return None
    except Exception:
        pass
    s = str(x).strip().lower()
    if s in {"1", "true", "yes", "y", "phish", "malicious", "positive", "pos"}:
        return 1
    if s in {"0", "false", "no", "n", "benign", "safe", "negative", "neg"}:
        return 0
    try:
        v = int(float(s))
        if v in (0, 1):
            return v
    except Exception:
        pass
    return None


def norm_review_status(x: Any) -> str:
    if x is None:
        return "unreviewed"
    try:
        if pd.isna(x):
            return "unreviewed"
    except Exception:
        pass
    s = str(x).strip().lower()
    if s in {"1", "true", "yes", "y", "reviewed", "done", "approved", "human_reviewed"}:
        return "reviewed"
    if s in {"0", "false", "no", "n", "unreviewed", "pending", "todo", "unknown", ""}:
        return "unreviewed"
    return s


def resolve_relpath(data_root: Path, value: Any) -> Optional[Path]:
    if is_empty(value):
        return None
    p = Path(str(value))
    if p.is_absolute():
        return p
    return (data_root / p).resolve()


def counter_dict(series: pd.Series) -> Dict[str, int]:
    c = Counter(safe_str(x) if not is_empty(x) else "<NA>" for x in series)
    return dict(sorted(c.items(), key=lambda kv: (-kv[1], kv[0])))


class Report:
    def __init__(self) -> None:
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.infos: List[Dict[str, Any]] = []

    def error(self, code: str, message: str, count: int = 1, examples: Optional[List[Dict[str, Any]]] = None) -> None:
        self.errors.append({"level": "error", "code": code, "message": message, "count": int(count), "examples": examples or []})

    def warn(self, code: str, message: str, count: int = 1, examples: Optional[List[Dict[str, Any]]] = None) -> None:
        self.warnings.append({"level": "warning", "code": code, "message": message, "count": int(count), "examples": examples or []})

    def info(self, code: str, message: str, count: int = 0, payload: Optional[Dict[str, Any]] = None) -> None:
        item = {"level": "info", "code": code, "message": message}
        if count:
            item["count"] = int(count)
        if payload is not None:
            item["payload"] = payload
        self.infos.append(item)

    def has_errors(self) -> bool:
        return len(self.errors) > 0


REQUIRED_COLUMNS = [
    "dataset_version", "sample_id", "screenshot_path", "html_path",
    "original_url", "final_url", "label_binary", "label_source",
    "review_status", "group_key", "split"
]

RECOMMENDED_COLUMNS = [
    "metadata_path", "rule_labels_path", "text_path", "hostname", "registered_domain",
    "page_title", "page_language", "site_category", "capture_time", "risk_type",
    "brand", "brand_source", "brand_confidence", "quality_grade", "dedup_key",
    "is_duplicate_candidate", "is_canonical", "content_fingerprint", "has_screenshot",
    "has_html", "has_text", "has_rule_labels", "completeness_ok", "source_dir"
]


def check_schema(df: pd.DataFrame, report: Report) -> None:
    missing_required = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    missing_recommended = [c for c in RECOMMENDED_COLUMNS if c not in df.columns]

    if missing_required:
        report.error(
            "missing_required_columns",
            f"manifest 缺少必备字段: {', '.join(missing_required)}",
            count=len(missing_required),
            examples=[{"missing": missing_required}],
        )
    if missing_recommended:
        report.warn(
            "missing_recommended_columns",
            f"manifest 缺少推荐字段: {', '.join(missing_recommended)}",
            count=len(missing_recommended),
            examples=[{"missing": missing_recommended}],
        )


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "label_binary" in out.columns:
        out["label_binary"] = out["label_binary"].apply(norm_label_binary)
    if "review_status" in out.columns:
        out["review_status"] = out["review_status"].apply(norm_review_status)
    if "split" in out.columns:
        out["split"] = out["split"].apply(lambda x: safe_str(x).strip().lower())
    if "quality_grade" in out.columns:
        out["quality_grade"] = out["quality_grade"].apply(lambda x: safe_str(x).strip().upper() if not is_empty(x) else "")
    if "brand_confidence" in out.columns:
        out["brand_confidence"] = pd.to_numeric(out["brand_confidence"], errors="coerce")
    return out


def check_ids(df: pd.DataFrame, report: Report, example_limit: int) -> None:
    if "sample_id" not in df.columns:
        return

    empty_mask = df["sample_id"].apply(is_empty)
    if empty_mask.any():
        examples = df.loc[empty_mask, [c for c in ["sample_id", "source_dir", "metadata_path"] if c in df.columns]].head(example_limit).to_dict("records")
        report.error("empty_sample_id", "存在空 sample_id。", count=int(empty_mask.sum()), examples=examples)

    dup = df["sample_id"].astype(str).value_counts()
    dup = dup[dup > 1]
    if len(dup) > 0:
        examples = []
        for sid, cnt in dup.head(example_limit).items():
            examples.append({"sample_id": sid, "count": int(cnt)})
        report.error("duplicate_sample_id", "存在重复 sample_id。", count=int(dup.sum()), examples=examples)


def check_core_fields(df: pd.DataFrame, report: Report, example_limit: int, require_label: bool) -> None:
    if "label_binary" in df.columns and require_label:
        bad = ~df["label_binary"].isin([0, 1])
        if bad.any():
            examples = df.loc[bad, [c for c in ["sample_id", "label_binary", "source_dir"] if c in df.columns]].head(example_limit).to_dict("records")
            report.error("invalid_label_binary", "存在缺失或非法的 label_binary。", count=int(bad.sum()), examples=examples)

    url_cols = [c for c in ["final_url", "original_url"] if c in df.columns]
    if url_cols:
        bad = df[url_cols].apply(lambda r: all(is_empty(v) for v in r), axis=1)
        if bad.any():
            examples = df.loc[bad, [c for c in ["sample_id", "final_url", "original_url", "source_dir"] if c in df.columns]].head(example_limit).to_dict("records")
            report.error("empty_url", "存在 final_url / original_url 同时为空的样本。", count=int(bad.sum()), examples=examples)

    if "split" in df.columns:
        bad = ~df["split"].isin(ALLOWED_SPLITS)
        if bad.any():
            examples = df.loc[bad, [c for c in ["sample_id", "split", "group_key"] if c in df.columns]].head(example_limit).to_dict("records")
            report.error("invalid_split", "存在非法 split，必须为 train/val/test。", count=int(bad.sum()), examples=examples)

    if "review_status" in df.columns:
        bad = ~df["review_status"].isin(ALLOWED_REVIEW_STATUS)
        if bad.any():
            examples = df.loc[bad, [c for c in ["sample_id", "review_status", "label_source"] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn("invalid_review_status", "存在非常规 review_status。", count=int(bad.sum()), examples=examples)

    if "quality_grade" in df.columns:
        bad = (~df["quality_grade"].isin(ALLOWED_QUALITY)) & (df["quality_grade"].astype(str).str.strip() != "")
        if bad.any():
            examples = df.loc[bad, [c for c in ["sample_id", "quality_grade"] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn("invalid_quality_grade", "存在非常规 quality_grade。", count=int(bad.sum()), examples=examples)


def check_paths(df: pd.DataFrame, data_root: Path, report: Report, example_limit: int) -> None:
    path_cols = [c for c in ["screenshot_path", "html_path", "metadata_path", "rule_labels_path", "text_path"] if c in df.columns]
    for col in path_cols:
        exists_mask = []
        for v in df[col].tolist():
            p = resolve_relpath(data_root, v)
            exists_mask.append(False if p is None else p.exists())
        exists_mask = pd.Series(exists_mask, index=df.index)

        required = col in {"screenshot_path", "html_path"}
        missing = (~exists_mask) & (~df[col].apply(is_empty))
        if missing.any():
            examples = []
            view_cols = [c for c in ["sample_id", col, "source_dir"] if c in df.columns]
            for _, row in df.loc[missing, view_cols].head(example_limit).iterrows():
                ex = row.to_dict()
                ex["resolved_path"] = str(resolve_relpath(data_root, row[col])) if col in row else None
                examples.append(ex)
            if required:
                report.error(f"missing_{col}", f"存在失效的 {col} 路径。", count=int(missing.sum()), examples=examples)
            else:
                report.warn(f"missing_{col}", f"存在失效的 {col} 路径。", count=int(missing.sum()), examples=examples)

        if required:
            empty = df[col].apply(is_empty)
            if empty.any():
                examples = df.loc[empty, [c for c in ["sample_id", col, "source_dir"] if c in df.columns]].head(example_limit).to_dict("records")
                report.error(f"empty_{col}", f"存在空 {col}。", count=int(empty.sum()), examples=examples)

    # 与 has_* 标志进行交叉检查
    pair_checks = [
        ("screenshot_path", "has_screenshot"),
        ("html_path", "has_html"),
        ("text_path", "has_text"),
        ("rule_labels_path", "has_rule_labels"),
    ]
    for path_col, flag_col in pair_checks:
        if path_col not in df.columns or flag_col not in df.columns:
            continue
        flag_true_but_empty = (df[flag_col].astype(str).str.lower() == "true") & df[path_col].apply(is_empty)
        flag_false_but_has_path = (df[flag_col].astype(str).str.lower() == "false") & (~df[path_col].apply(is_empty))
        if flag_true_but_empty.any():
            examples = df.loc[flag_true_but_empty, [c for c in ["sample_id", flag_col, path_col] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn(f"flag_path_mismatch_{path_col}_1", f"存在 {flag_col}=true 但 {path_col} 为空。", count=int(flag_true_but_empty.sum()), examples=examples)
        if flag_false_but_has_path.any():
            examples = df.loc[flag_false_but_has_path, [c for c in ["sample_id", flag_col, path_col] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn(f"flag_path_mismatch_{path_col}_2", f"存在 {flag_col}=false 但 {path_col} 非空。", count=int(flag_false_but_has_path.sum()), examples=examples)


def check_brand_logic(df: pd.DataFrame, report: Report, example_limit: int) -> None:
    if "brand" not in df.columns:
        return
    brand = df["brand"].apply(lambda x: safe_str(x).strip())
    none_like = brand.str.lower().isin({"", "none", "null", "na", "<na>"})

    if "brand_confidence" in df.columns:
        bad_range = (~df["brand_confidence"].isna()) & ((df["brand_confidence"] < 0) | (df["brand_confidence"] > 1))
        if bad_range.any():
            examples = df.loc[bad_range, [c for c in ["sample_id", "brand", "brand_confidence", "brand_source"] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn("brand_confidence_out_of_range", "存在 brand_confidence 不在 [0,1] 的样本。", count=int(bad_range.sum()), examples=examples)

        conf_without_brand = (~df["brand_confidence"].isna()) & none_like
        if conf_without_brand.any():
            examples = df.loc[conf_without_brand, [c for c in ["sample_id", "brand", "brand_confidence", "brand_source"] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn("brand_conf_without_brand", "存在 brand 为空/none 但 brand_confidence 非空。", count=int(conf_without_brand.sum()), examples=examples)

    if "brand_source" in df.columns:
        src = df["brand_source"].apply(lambda x: safe_str(x).strip())
        src_without_brand = (~src.eq("")) & none_like
        if src_without_brand.any():
            examples = df.loc[src_without_brand, [c for c in ["sample_id", "brand", "brand_source", "brand_confidence"] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn("brand_source_without_brand", "存在 brand 为空/none 但 brand_source 非空。", count=int(src_without_brand.sum()), examples=examples)


def check_label_logic(df: pd.DataFrame, report: Report, example_limit: int) -> None:
    if "label_binary" not in df.columns:
        return

    if "risk_type" in df.columns:
        risk = df["risk_type"].apply(lambda x: safe_str(x).strip().lower())
        suspicious_neg = (df["label_binary"] == 0) & risk.isin(POSITIVE_RISK_HINTS)
        if suspicious_neg.any():
            examples = df.loc[suspicious_neg, [c for c in ["sample_id", "label_binary", "risk_type", "brand", "label_source"] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn("negative_with_positive_risk_type", "存在 label_binary=0 但 risk_type 呈明显正样本含义的样本。", count=int(suspicious_neg.sum()), examples=examples)

    if "review_status" in df.columns and "label_source" in df.columns:
        src = df["label_source"].apply(lambda x: safe_str(x).strip().lower())
        reviewed_but_rule = (df["review_status"] == "reviewed") & src.eq("rule")
        if reviewed_but_rule.any():
            examples = df.loc[reviewed_but_rule, [c for c in ["sample_id", "review_status", "label_source", "label_binary"] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn("reviewed_but_rule_source", "存在 review_status=reviewed 但 label_source=rule 的样本，请确认是否忘了写回 human/mixed。", count=int(reviewed_but_rule.sum()), examples=examples)

        unreviewed_but_human = (df["review_status"] == "unreviewed") & src.isin({"human", "manual", "reviewed", "gold"})
        if unreviewed_but_human.any():
            examples = df.loc[unreviewed_but_human, [c for c in ["sample_id", "review_status", "label_source", "label_binary"] if c in df.columns]].head(example_limit).to_dict("records")
            report.warn("unreviewed_but_human_source", "存在 review_status=unreviewed 但 label_source 看起来像人工标签的样本。", count=int(unreviewed_but_human.sum()), examples=examples)


def _cross_split_collisions(df: pd.DataFrame, key_col: str) -> List[Dict[str, Any]]:
    rows = []
    if key_col not in df.columns or "split" not in df.columns:
        return rows
    valid = df.loc[(~df[key_col].apply(is_empty)) & (df["split"].isin(ALLOWED_SPLITS)), [key_col, "split", "sample_id"]].copy()
    if valid.empty:
        return rows

    for key, group in valid.groupby(key_col):
        splits = sorted(set(group["split"].astype(str)))
        if len(splits) > 1:
            rows.append({
                "key": safe_str(key),
                "splits": splits,
                "sample_ids": group["sample_id"].astype(str).head(10).tolist(),
                "count": int(len(group)),
            })
    return rows


def check_leakage(df: pd.DataFrame, report: Report, example_limit: int) -> None:
    leakage_keys = [
        ("registered_domain", "cross_split_registered_domain"),
        ("group_key", "cross_split_group_key"),
        ("dedup_key", "cross_split_dedup_key"),
        ("content_fingerprint", "cross_split_content_fingerprint"),
    ]
    for key_col, code in leakage_keys:
        if key_col not in df.columns:
            continue
        rows = _cross_split_collisions(df, key_col)
        if rows:
            report.error(code, f"存在 {key_col} 跨 split 泄漏。", count=len(rows), examples=rows[:example_limit])


def check_distribution(df: pd.DataFrame, report: Report, example_limit: int) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "num_rows": int(len(df)),
        "class_distribution": counter_dict(df["label_binary"]) if "label_binary" in df.columns else {},
        "split_distribution": counter_dict(df["split"]) if "split" in df.columns else {},
        "review_distribution": counter_dict(df["review_status"]) if "review_status" in df.columns else {},
        "label_source_distribution": counter_dict(df["label_source"]) if "label_source" in df.columns else {},
        "quality_distribution": counter_dict(df["quality_grade"]) if "quality_grade" in df.columns else {},
        "risk_type_distribution": counter_dict(df["risk_type"]) if "risk_type" in df.columns else {},
        "brand_top20": dict(list(counter_dict(df["brand"]).items())[:20]) if "brand" in df.columns else {},
    }

    if "split" in df.columns and "label_binary" in df.columns:
        pivot = pd.crosstab(df["split"], df["label_binary"])
        for split in sorted(ALLOWED_SPLITS):
            if split in pivot.index:
                row = pivot.loc[split]
                if 0 not in row.index or int(row.get(0, 0)) == 0:
                    report.warn("split_missing_negative", f"split={split} 中缺少负样本。", count=1, examples=[{"split": split, "row": row.to_dict()}])
                if 1 not in row.index or int(row.get(1, 0)) == 0:
                    report.warn("split_missing_positive", f"split={split} 中缺少正样本。", count=1, examples=[{"split": split, "row": row.to_dict()}])

    if "brand" in df.columns:
        brand_series = df["brand"].apply(lambda x: safe_str(x).strip().lower())
        brand_series = brand_series[~brand_series.isin({"", "none", "<na>", "null"})]
        if len(brand_series) > 0:
            vc = brand_series.value_counts()
            top_share = float(vc.iloc[0]) / float(vc.sum())
            if top_share >= 0.50:
                report.warn(
                    "brand_distribution_collapsed",
                    f"品牌分布过于塌缩，top1 brand 占比约 {top_share:.2%}。",
                    count=1,
                    examples=[{"top_brand": vc.index[0], "top_count": int(vc.iloc[0]), "total_nonempty_brand": int(vc.sum())}],
                )

    if "risk_type" in df.columns:
        rs = df["risk_type"].apply(lambda x: safe_str(x).strip().lower())
        rs = rs[rs != ""]
        if len(rs) > 0:
            vc = rs.value_counts()
            top_share = float(vc.iloc[0]) / float(vc.sum())
            if top_share >= 0.70:
                report.warn(
                    "risk_type_distribution_collapsed",
                    f"risk_type 分布过于单一，top1 占比约 {top_share:.2%}。",
                    count=1,
                    examples=[{"top_risk_type": vc.index[0], "top_count": int(vc.iloc[0]), "total_nonempty_risk_type": int(vc.sum())}],
                )

    return summary


def build_markdown_report(report: Report, summary: Dict[str, Any], args: argparse.Namespace) -> str:
    lines: List[str] = []
    lines.append("# TRAINSET_V1 consistency report")
    lines.append("")
    lines.append(f"- manifest: `{args.manifest}`")
    lines.append(f"- data_root: `{args.data_root}`")
    lines.append(f"- rows: {summary.get('num_rows', 0)}")
    lines.append(f"- strict: {args.strict}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- errors: {len(report.errors)}")
    lines.append(f"- warnings: {len(report.warnings)}")
    lines.append("")

    def dump_counter(title: str, data: Dict[str, Any], limit: int = 20) -> None:
        lines.append(f"### {title}")
        lines.append("")
        if not data:
            lines.append("- <empty>")
            lines.append("")
            return
        for i, (k, v) in enumerate(data.items()):
            if i >= limit:
                break
            lines.append(f"- {k}: {v}")
        lines.append("")

    dump_counter("class_distribution", summary.get("class_distribution", {}))
    dump_counter("split_distribution", summary.get("split_distribution", {}))
    dump_counter("review_distribution", summary.get("review_distribution", {}))
    dump_counter("label_source_distribution", summary.get("label_source_distribution", {}))
    dump_counter("quality_distribution", summary.get("quality_distribution", {}))
    dump_counter("risk_type_distribution", summary.get("risk_type_distribution", {}), limit=15)
    dump_counter("brand_top20", summary.get("brand_top20", {}), limit=20)

    lines.append("## Findings")
    lines.append("")

    if not report.errors and not report.warnings:
        lines.append("- No major issues found.")
        lines.append("")
    else:
        for bucket_name, bucket in [("Errors", report.errors), ("Warnings", report.warnings)]:
            lines.append(f"### {bucket_name}")
            lines.append("")
            if not bucket:
                lines.append("- None")
                lines.append("")
                continue
            for item in bucket:
                lines.append(f"- `{item['code']}`: {item['message']} (count={item['count']})")
                for ex in item.get("examples", [])[: args.example_limit]:
                    lines.append(f"  - example: `{json.dumps(ex, ensure_ascii=False)}`")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Check Warden TRAINSET_V1 manifest consistency")
    p.add_argument("--data-root", default=CONFIG_DATA_ROOT, help="数据根目录，例如 ./data")
    p.add_argument("--manifest", default=CONFIG_MANIFEST_PATH, help="manifest 路径")
    p.add_argument("--out-dir", default=CONFIG_OUTPUT_DIR, help="输出目录")
    p.add_argument("--require-label", action="store_true", help="将 label_binary 视为必备，缺失则记为 error")
    p.add_argument("--strict", action="store_true", help="若存在 error，则返回非 0")
    p.add_argument("--example-limit", type=int, default=10, help="每类问题最多保留多少个示例")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    data_root = Path(args.data_root).resolve()
    manifest = Path(args.manifest).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not manifest.exists():
        raise SystemExit(f"manifest 不存在: {manifest}")

    df = normalize_df(read_table(manifest))
    report = Report()

    report.info("manifest_loaded", "已加载 manifest。", count=len(df), payload={"manifest": str(manifest)})

    check_schema(df, report)
    check_ids(df, report, example_limit=args.example_limit)
    check_core_fields(df, report, example_limit=args.example_limit, require_label=args.require_label)
    check_paths(df, data_root, report, example_limit=args.example_limit)
    check_brand_logic(df, report, example_limit=args.example_limit)
    check_label_logic(df, report, example_limit=args.example_limit)
    check_leakage(df, report, example_limit=args.example_limit)
    summary = check_distribution(df, report, example_limit=args.example_limit)

    payload = {
        "manifest": str(manifest),
        "data_root": str(data_root),
        "summary": summary,
        "errors": report.errors,
        "warnings": report.warnings,
        "infos": report.infos,
        "status": "fail" if report.has_errors() else "pass",
    }

    json_path = out_dir / "consistency_report.json"
    md_path = out_dir / "consistency_report.md"
    payload_path = out_dir / "summary.json"

    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(build_markdown_report(report, summary, args), encoding="utf-8")
    payload_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    log(f"[done] rows={len(df)}")
    log(f"[done] errors={len(report.errors)} warnings={len(report.warnings)}")
    log(f"[done] json={json_path}")
    log(f"[done] md={md_path}")

    if args.strict and report.has_errors():
        raise SystemExit(2)


if __name__ == "__main__":
    main()
