#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Mine review-only T01 benign hard-negative candidates from triaged Tranco data.

The script reads lightweight artifacts from existing triage sample directories
and writes a candidate CSV/report for human review. It never moves, relabels,
deletes, or edits source samples.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.data.common.io_utils import ensure_dir, write_lines
from scripts.data.common.url_utils import host_from_url, registrable_domain


DEFAULT_TRIAGE_ROOT = Path(r"E:\WardenData\manifests\tranco_benign_triage_v1")
DEFAULT_OUTPUT_DIR = Path(r"E:\WardenData\manifests\t01_candidate_mining_v1")
DEFAULT_INCLUDE_LABELS = ("T00_clear_benign",)
DEFAULT_OPTIONAL_REVIEW_SOURCES: tuple[str, ...] = ()

MANIFEST_NAME = "t01_candidate_manifest_v1.csv"
REPORT_NAME = "t01_candidate_report_v1.md"
REVIEW_DIR_NAME = "t01_candidate_review_v1"

TEXT_MAX_CHARS = 50000
HIGH_SCORE_MIN = 8
MEDIUM_SCORE_MIN = 5

CSV_COLUMNS = [
    "sample_id",
    "current_label",
    "candidate_score",
    "score_band",
    "candidate_bucket",
    "secondary_buckets",
    "reasons",
    "exclude_reasons",
    "current_path",
    "final_url",
    "final_host",
    "etld1",
    "visible_text_chars",
    "effective_visible_text_chars",
    "form_count",
    "input_count",
    "has_password",
    "has_login_hint",
    "has_payment_hint",
    "has_finance_hint",
    "has_wallet_hint",
    "has_download_hint",
    "has_support_hint",
    "has_ai_token_hint",
    "has_donation_hint",
    "has_hosting_hint",
    "has_screenshot_viewport",
    "has_screenshot_view",
    "has_screenshot_full",
    "missing_artifacts",
    "parse_warnings",
    "needs_review",
]

BUCKETS = {
    "C01_login_auth": {
        "weight": 1,
        "patterns": [
            r"\blog[ -]?in\b",
            r"\bsign[ -]?in\b",
            r"\bsign[ -]?up\b",
            r"\bregister\b",
            r"\bpassword\b",
            r"\bpasscode\b",
            r"\bmfa\b",
            r"\botp\b",
            r"\b2fa\b",
            r"\bverify account\b",
            r"\baccount verification\b",
            r"\boauth\b",
            r"\bsso\b",
            r"登录|登入|注册|账号|账户|密码|验证码|验证",
        ],
    },
    "C02_payment_checkout": {
        "weight": 1,
        "patterns": [
            r"\bcheckout\b",
            r"\bpayment\b",
            r"\bbilling\b",
            r"\binvoice\b",
            r"\bcredit card\b",
            r"\bcard number\b",
            r"\bcvv\b",
            r"\bsubscription\b",
            r"\brenew\b",
            r"\border confirmation\b",
            r"\bpricing\b",
            r"\bplans\b",
            r"\bupgrade\b",
            r"付款|支付|账单|发票|订阅|续费|订单",
        ],
    },
    "C03_finance_banking": {
        "weight": 1,
        "patterns": [
            r"\bbank(?:ing)?\b",
            r"\bfintech\b",
            r"\binvest(?:ment|ing)?\b",
            r"\binsurance\b",
            r"\bloan\b",
            r"\bmortgage\b",
            r"\bbrokerage\b",
            r"\btrading account\b",
            r"银行|金融|贷款|保险|投资|证券",
        ],
    },
    "C04_crypto_web3_wallet": {
        "weight": 1,
        "patterns": [
            r"\bcrypto\b",
            r"\bwallet\b",
            r"\bconnect wallet\b",
            r"\bwalletconnect\b",
            r"\bmetamask\b",
            r"\bkyc\b",
            r"\bdeposit\b",
            r"\bwithdraw\b",
            r"\bstaking\b",
            r"\bnft\b",
            r"\bbridge\b",
            r"\bcrypto exchange\b",
            r"钱包|加密货币|充值|提现|质押",
        ],
    },
    "C05_download_app": {
        "weight": 1,
        "patterns": [
            r"\bdownload\b",
            r"\binstall\b",
            r"\bextension\b",
            r"\bplugin\b",
            r"\bapk\b",
            r"\bexe\b",
            r"\bdmg\b",
            r"\bmsi\b",
            r"\blauncher\b",
            r"\bsoftware update\b",
            r"下载|安装|应用|插件|更新",
        ],
    },
    "C06_support_contact": {
        "weight": 1,
        "patterns": [
            r"\bsupport\b",
            r"\bhelp center\b",
            r"\bcontact\b",
            r"\blive chat\b",
            r"\bcustomer service\b",
            r"\bticket\b",
            r"\bcall support\b",
            r"客服|支持|帮助中心|联系我们|工单",
        ],
    },
    "C07_ai_api_token_dashboard": {
        "weight": 1,
        "patterns": [
            r"\bapi key\b",
            r"\bapi token\b",
            r"\bcredits\b",
            r"\bplayground\b",
            r"\bmodel dashboard\b",
            r"\bai platform\b",
            r"\bmodel billing\b",
            r"API[ \-]?密钥|令牌|控制台|仪表盘",
        ],
    },
    "C08_donation_charity": {
        "weight": 1,
        "patterns": [
            r"\bdonate\b",
            r"\bdonation\b",
            r"\bcharity\b",
            r"\bfundraiser\b",
            r"\bnonprofit\b",
            r"\bsupport us\b",
            r"\bchurch\b",
            r"捐赠|慈善|募捐|支持我们",
        ],
    },
    "C09_domain_hosting_telecom": {
        "weight": 1,
        "patterns": [
            r"\bdomain\b",
            r"\bhosting\b",
            r"\bvps\b",
            r"\bserver\b",
            r"\bssl\b",
            r"\bcdn\b",
            r"\bdns\b",
            r"\bbroadband\b",
            r"\bdata plan\b",
            r"\btelecom\b",
            r"域名|主机|服务器|宽带|流量套餐",
        ],
    },
}

EXCLUSION_PATTERNS = {
    "gray_or_regulated_content": [
        r"\bgambling\b",
        r"\bcasino\b",
        r"\bbetting\b",
        r"\badult\b",
        r"\bporn\b",
        r"\bxxx\b",
        r"\bescort\b",
        r"\btogel\b",
        r"\btoto\b",
    ],
    "manipulative_reward_or_profit": [
        r"\bprize\b",
        r"\bjackpot\b",
        r"\bquick rich\b",
        r"\bguaranteed profit\b",
        r"\bhigh return\b",
        r"\bdouble your money\b",
        r"稳赚|高回报|中奖|彩金",
    ],
    "dangerous_wallet_secret_request": [
        r"\bseed phrase\b",
        r"\brecovery phrase\b",
        r"\bprivate key\b",
        r"\bkeystore\b",
        r"助记词|私钥|恢复短语",
    ],
    "bad_capture_or_error": [
        r"\b404\b",
        r"\b403\b",
        r"\b500\b",
        r"\bnot found\b",
        r"\baccess denied\b",
        r"\bchecking your browser\b",
        r"\bcloudflare\b",
        r"\bcaptcha\b",
        r"\bjust a moment\b",
        r"\bparked domain\b",
        r"\bfor sale\b",
    ],
    "deceptive_download_pressure": [
        r"\burgent\b.*\bdownload\b",
        r"\bdownload\b.*\brequired\b",
        r"\bupdate required\b",
        r"\bsecurity update\b",
    ],
}


@dataclass
class ArtifactRead:
    data: Any = None
    text: str = ""
    missing: bool = False
    warning: str = ""


@dataclass
class SampleRecord:
    row: Dict[str, Any]
    raw_positive_score: int
    source_label: str
    missing_artifacts: List[str] = field(default_factory=list)
    parse_warnings: List[str] = field(default_factory=list)


def compile_patterns(patterns: Iterable[str]) -> list[re.Pattern[str]]:
    return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]


COMPILED_BUCKETS = {bucket: {**spec, "compiled": compile_patterns(spec["patterns"])} for bucket, spec in BUCKETS.items()}
COMPILED_EXCLUSIONS = {reason: compile_patterns(patterns) for reason, patterns in EXCLUSION_PATTERNS.items()}


def safe_str(value: Any) -> str:
    return "" if value is None else str(value)


def read_json_artifact(sample_dir: Path, name: str) -> ArtifactRead:
    path = sample_dir / name
    if not path.exists():
        return ArtifactRead(missing=True)
    try:
        return ArtifactRead(data=json.loads(path.read_text(encoding="utf-8-sig", errors="ignore")))
    except Exception as exc:
        return ArtifactRead(warning=f"{name}:{type(exc).__name__}:{exc}")


def read_text_artifact(sample_dir: Path, name: str, max_chars: int) -> ArtifactRead:
    path = sample_dir / name
    if not path.exists():
        return ArtifactRead(missing=True)
    try:
        return ArtifactRead(text=path.read_text(encoding="utf-8-sig", errors="ignore")[:max_chars])
    except Exception as exc:
        return ArtifactRead(warning=f"{name}:{type(exc).__name__}:{exc}")


def iter_sample_dirs(label_root: Path) -> Iterable[Path]:
    if not label_root.exists():
        return []
    return sorted((child for child in label_root.iterdir() if child.is_dir()), key=lambda path: path.name.lower())


def extract_final_url(url_info: Any) -> str:
    if not isinstance(url_info, Mapping):
        return ""
    return safe_str(url_info.get("final_url")).strip() or safe_str(url_info.get("input_url")).strip()


def count_form_inputs(forms: Any) -> tuple[int, int, bool]:
    if not isinstance(forms, Mapping):
        return 0, 0, False
    form_items = forms.get("forms")
    if not isinstance(form_items, list):
        return 0, 0, False
    text = json.dumps(form_items, ensure_ascii=False).lower()
    input_count = len(re.findall(r'"tag"\s*:\s*"input"|"type"\s*:', text))
    if input_count == 0:
        input_count = len(re.findall(r"\binput\b", text))
    return len(form_items), input_count, ("password" in text or '"type": "password"' in text)


def net_text(net_summary: Any) -> str:
    if not isinstance(net_summary, Mapping):
        return ""
    return json.dumps(net_summary, ensure_ascii=False)


def effective_text_chars(text: str) -> int:
    return len(re.sub(r"\s+", " ", text or "").strip())


def match_bucket_scores(blob: str, form_count: int, input_count: int, has_password: bool) -> tuple[Dict[str, int], Dict[str, List[str]]]:
    scores: Dict[str, int] = {}
    reasons: Dict[str, List[str]] = {}
    for bucket, spec in COMPILED_BUCKETS.items():
        hits = []
        for pattern in spec["compiled"]:
            if pattern.search(blob):
                hits.append(pattern.pattern)
        if hits:
            scores[bucket] = len(hits) * int(spec["weight"])
            reasons[bucket] = [f"{bucket}:keyword:{hit}" for hit in hits[:6]]

    if has_password:
        scores["C01_login_auth"] = scores.get("C01_login_auth", 0) + 6
        reasons.setdefault("C01_login_auth", []).append("artifact:has_password")
    if form_count > 0:
        scores["C01_login_auth"] = scores.get("C01_login_auth", 0) + 2
        reasons.setdefault("C01_login_auth", []).append(f"artifact:form_count={form_count}")
    if input_count > 0:
        scores["C01_login_auth"] = scores.get("C01_login_auth", 0) + 1
        reasons.setdefault("C01_login_auth", []).append(f"artifact:input_count={input_count}")
    return scores, reasons


def match_exclusions(blob: str, has_password: bool) -> List[str]:
    reasons = []
    for reason, patterns in COMPILED_EXCLUSIONS.items():
        if any(pattern.search(blob) for pattern in patterns):
            reasons.append(reason)
    if has_password and any(reason in reasons for reason in ["dangerous_wallet_secret_request", "manipulative_reward_or_profit"]):
        reasons.append("sensitive_form_with_high_risk_language")
    return sorted(set(reasons))


def score_band(score: int) -> str:
    if score >= HIGH_SCORE_MIN:
        return "high"
    if score >= MEDIUM_SCORE_MIN:
        return "medium"
    return "low"


def build_sample_record(sample_dir: Path, current_label: str) -> SampleRecord:
    url_read = read_json_artifact(sample_dir, "url.json")
    forms_read = read_json_artifact(sample_dir, "forms.json")
    net_read = read_json_artifact(sample_dir, "net_summary.json")
    visible_read = read_text_artifact(sample_dir, "visible_text.txt", TEXT_MAX_CHARS)

    missing = []
    warnings = []
    for name, read in [
        ("url.json", url_read),
        ("forms.json", forms_read),
        ("net_summary.json", net_read),
        ("visible_text.txt", visible_read),
    ]:
        if read.missing:
            missing.append(name)
        if read.warning:
            warnings.append(read.warning)

    final_url = extract_final_url(url_read.data)
    final_host = host_from_url(final_url)
    etld1 = registrable_domain(final_url) if final_url else ""
    parsed_path = urlparse(final_url).path if final_url else ""

    form_count, input_count, has_password = count_form_inputs(forms_read.data)
    visible_text = visible_read.text or ""
    blob = "\n".join(
        [
            sample_dir.name,
            final_url,
            final_host,
            etld1,
            parsed_path,
            visible_text,
            net_text(net_read.data),
        ]
    )
    bucket_scores, bucket_reasons = match_bucket_scores(blob, form_count, input_count, has_password)
    exclude_reasons = match_exclusions(blob, has_password)
    raw_score = sum(bucket_scores.values())
    penalty = min(4, len(exclude_reasons) * 2)
    candidate_score = max(0, raw_score - penalty)

    if bucket_scores:
        ranked_buckets = sorted(bucket_scores, key=lambda bucket: (-bucket_scores[bucket], bucket))
        candidate_bucket = ranked_buckets[0]
        secondary_buckets = ranked_buckets[1:]
    else:
        candidate_bucket = "C99_mixed_or_uncertain"
        secondary_buckets = []

    if len(bucket_scores) >= 3 and candidate_score < MEDIUM_SCORE_MIN:
        candidate_bucket = "C99_mixed_or_uncertain"

    reasons: List[str] = []
    for bucket in sorted(bucket_reasons):
        reasons.extend(bucket_reasons[bucket])

    has_flags = {bucket: bucket in bucket_scores for bucket in BUCKETS}
    needs_review = bool(exclude_reasons or current_label != "T00_clear_benign")

    row = {
        "sample_id": sample_dir.name,
        "current_label": current_label,
        "candidate_score": candidate_score,
        "score_band": score_band(candidate_score),
        "candidate_bucket": candidate_bucket,
        "secondary_buckets": ";".join(secondary_buckets),
        "reasons": ";".join(reasons),
        "exclude_reasons": ";".join(exclude_reasons),
        "current_path": str(sample_dir.resolve()),
        "final_url": final_url,
        "final_host": final_host,
        "etld1": etld1,
        "visible_text_chars": len(visible_text),
        "effective_visible_text_chars": effective_text_chars(visible_text),
        "form_count": form_count,
        "input_count": input_count,
        "has_password": has_password,
        "has_login_hint": has_flags["C01_login_auth"],
        "has_payment_hint": has_flags["C02_payment_checkout"],
        "has_finance_hint": has_flags["C03_finance_banking"],
        "has_wallet_hint": has_flags["C04_crypto_web3_wallet"],
        "has_download_hint": has_flags["C05_download_app"],
        "has_support_hint": has_flags["C06_support_contact"],
        "has_ai_token_hint": has_flags["C07_ai_api_token_dashboard"],
        "has_donation_hint": has_flags["C08_donation_charity"],
        "has_hosting_hint": has_flags["C09_domain_hosting_telecom"],
        "has_screenshot_viewport": (sample_dir / "screenshot_viewport.png").exists(),
        "has_screenshot_view": (sample_dir / "screenshot_view.png").exists(),
        "has_screenshot_full": (sample_dir / "screenshot_full.png").exists(),
        "missing_artifacts": ";".join(missing),
        "parse_warnings": ";".join(warnings),
        "needs_review": needs_review,
    }
    return SampleRecord(row=row, raw_positive_score=raw_score, source_label=current_label, missing_artifacts=missing, parse_warnings=warnings)


def should_emit(record: SampleRecord, min_score: int) -> bool:
    return int(record.row["candidate_score"]) >= min_score or (
        record.raw_positive_score >= min_score and bool(record.row["exclude_reasons"])
    )


def write_manifest(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in CSV_COLUMNS})


def write_review_folders(review_dir: Path, rows: Sequence[Dict[str, Any]]) -> None:
    ensure_dir(review_dir)
    by_bucket: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_bucket[safe_str(row["candidate_bucket"])].append(row)
    for bucket in list(BUCKETS) + ["C99_mixed_or_uncertain"]:
        bucket_dir = ensure_dir(review_dir / bucket)
        bucket_rows = sorted(by_bucket.get(bucket, []), key=lambda row: (-int(row["candidate_score"]), safe_str(row["sample_id"])))
        write_lines(bucket_dir / "paths.txt", (safe_str(row["current_path"]) for row in bucket_rows))
        with (bucket_dir / "candidates.csv").open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(bucket_rows)


def markdown_count_table(counter: Mapping[str, int], empty_label: str = "none") -> List[str]:
    if not counter:
        return [f"- {empty_label}: 0"]
    return [f"- {key}: {counter[key]}" for key in sorted(counter)]


def write_report(path: Path, args: argparse.Namespace, scanned_counts: Mapping[str, int], rows: Sequence[Dict[str, Any]], all_records: Sequence[SampleRecord]) -> None:
    bucket_counts = Counter(safe_str(row["candidate_bucket"]) for row in rows)
    band_counts = Counter(safe_str(row["score_band"]) for row in rows)
    missing_counts = Counter()
    parse_warning_count = 0
    exclusion_count = 0
    for record in all_records:
        missing_counts.update(record.missing_artifacts)
        parse_warning_count += len(record.parse_warnings)
    for row in rows:
        if safe_str(row["exclude_reasons"]):
            exclusion_count += 1

    review_order = sorted(rows, key=lambda row: (safe_str(row["needs_review"]) != "False", -int(row["candidate_score"]), safe_str(row["candidate_bucket"]), safe_str(row["sample_id"])))
    lines = [
        "# T01 Candidate Mining Report V1",
        "",
        "## Summary",
        "",
        "- Output type: candidate-only review queue.",
        "- Source samples were not moved, deleted, relabeled, or overwritten.",
        f"- Triage root: `{Path(args.triage_root).resolve()}`",
        f"- Output directory: `{Path(args.output_dir).resolve()}`",
        f"- Include labels: `{', '.join(args.include_labels)}`",
        f"- Optional review sources: `{', '.join(args.optional_review_source) if args.optional_review_source else 'none'}`",
        f"- Minimum positive score: `{args.min_score}`",
        f"- Total scanned samples: {sum(scanned_counts.values())}",
        f"- Total candidates found: {len(rows)}",
        f"- Candidates with exclusion/suspicious flags: {exclusion_count}",
        f"- Parse warning count: {parse_warning_count}",
        "",
        "## Scanned Samples By Current Label",
        "",
        *markdown_count_table(scanned_counts),
        "",
        "## Candidates By Bucket",
        "",
        *markdown_count_table(bucket_counts),
        "",
        "## Candidates By Score Band",
        "",
        *markdown_count_table(band_counts),
        "",
        "## Missing Artifact Counts",
        "",
        *markdown_count_table(missing_counts),
        "",
        "## Recommended Manual Review Order",
        "",
        "Review high-score rows first, then rows with `needs_review=True` and non-empty `exclude_reasons`.",
        "",
        "| rank | sample_id | label | bucket | score | band | needs_review | exclude_reasons |",
        "|---:|---|---|---|---:|---|---|---|",
    ]
    for rank, row in enumerate(review_order[:50], 1):
        lines.append(
            "| {rank} | `{sample}` | `{label}` | `{bucket}` | {score} | `{band}` | `{review}` | `{exclude}` |".format(
                rank=rank,
                sample=safe_str(row["sample_id"]).replace("|", "\\|"),
                label=safe_str(row["current_label"]),
                bucket=safe_str(row["candidate_bucket"]),
                score=row["candidate_score"],
                band=safe_str(row["score_band"]),
                review=safe_str(row["needs_review"]),
                exclude=safe_str(row["exclude_reasons"]).replace("|", "\\|"),
            )
        )
    lines.extend(
        [
            "",
            "## Reminder",
            "",
            "This report is not a relabeling artifact. Human review remains the authority for any future T00 to T01 adjustment.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run(args: argparse.Namespace) -> int:
    triage_root = Path(args.triage_root).resolve()
    output_dir = ensure_dir(Path(args.output_dir).resolve())
    labels = list(args.include_labels) + list(args.optional_review_source)
    missing_roots = [label for label in labels if not (triage_root / label).is_dir()]
    if missing_roots:
        raise SystemExit(f"missing label roots under {triage_root}: {missing_roots}")

    all_records: List[SampleRecord] = []
    rows: List[Dict[str, Any]] = []
    scanned_counts: Counter[str] = Counter()
    for label in labels:
        for sample_dir in iter_sample_dirs(triage_root / label):
            scanned_counts[label] += 1
            record = build_sample_record(sample_dir, label)
            all_records.append(record)
            if should_emit(record, args.min_score):
                rows.append(record.row)
            if args.limit and sum(scanned_counts.values()) >= args.limit:
                break
        if args.limit and sum(scanned_counts.values()) >= args.limit:
            break

    rows.sort(key=lambda row: (-int(row["candidate_score"]), safe_str(row["candidate_bucket"]), safe_str(row["sample_id"])))
    manifest_path = output_dir / MANIFEST_NAME
    report_path = output_dir / REPORT_NAME
    write_manifest(manifest_path, rows)
    write_report(report_path, args, scanned_counts, rows, all_records)
    if args.write_review_folders:
        write_review_folders(output_dir / REVIEW_DIR_NAME, rows)

    print(f"[done] scanned={sum(scanned_counts.values())}")
    print(f"[done] candidates={len(rows)}")
    print(f"[done] manifest={manifest_path}")
    print(f"[done] report={report_path}")
    if args.write_review_folders:
        print(f"[done] review_dir={output_dir / REVIEW_DIR_NAME}")
    print("[done] source samples not moved, deleted, relabeled, or overwritten")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage-root", default=str(DEFAULT_TRIAGE_ROOT), help="Root containing triaged benign bucket directories.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory for candidate CSV/report/review lists.")
    parser.add_argument("--include-labels", nargs="+", default=list(DEFAULT_INCLUDE_LABELS), help="Primary label/source folders to scan.")
    parser.add_argument(
        "--optional-review-source",
        nargs="*",
        default=list(DEFAULT_OPTIONAL_REVIEW_SOURCES),
        help="Optional extra source folders such as T90_uncertain_or_suspicious. These are review-only and never promoted.",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=3,
        help="Minimum adjusted candidate score required to emit a row; rows with exclusion reasons are kept when raw positive score reaches this value.",
    )
    parser.add_argument("--limit", type=int, default=0, help="Optional maximum number of sample directories to scan for smoke validation.")
    parser.add_argument("--write-review-folders", action="store_true", help="Write per-bucket path lists and CSV files. Original samples are not moved.")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Compatibility flag. The script is always read-only for source samples.")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
