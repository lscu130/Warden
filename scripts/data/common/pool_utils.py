#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import math
from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Sequence, Tuple


def summarize_cluster_records(records: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    family_counts = Counter(str(row.get("family_key") or "unknown_family") for row in records)
    return {
        "total_records": len(records),
        "valid_records": sum(1 for row in records if row.get("page_validity_status") == "valid"),
        "invalid_records": sum(1 for row in records if row.get("page_validity_status") != "valid"),
        "cluster_count": len({row.get("cluster_id") for row in records}),
        "subcluster_count": len({row.get("subcluster_id") for row in records}),
        "family_count": len(family_counts),
        "top_families": [
            {"family_key": family_key, "count": count}
            for family_key, count in family_counts.most_common(20)
        ],
    }


def assign_pool_decisions(records: Sequence[Dict[str, Any]], family_share_cap: float) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    ordered = sorted(
        records,
        key=lambda row: (
            str(row.get("cluster_id") or ""),
            str(row.get("subcluster_id") or ""),
            str(row.get("capture_time_utc") or ""),
            str(row.get("sample_id") or ""),
        ),
    )

    decisions: List[Dict[str, Any]] = []
    canonical_candidates: List[Dict[str, Any]] = []
    subcluster_seen: set[str] = set()

    for row in ordered:
        decision = {
            "sample_id": row.get("sample_id"),
            "sample_dir": row.get("sample_dir"),
            "family_key": row.get("family_key"),
            "cluster_id": row.get("cluster_id"),
            "subcluster_id": row.get("subcluster_id"),
            "page_validity_status": row.get("page_validity_status"),
            "pool_bucket": "",
            "reason_code": "",
            "keep_in_train": False,
            "move_to_reserve": False,
            "exclude_from_train": False,
        }
        if row.get("page_validity_status") != "valid":
            decision.update(
                {
                    "pool_bucket": "reject",
                    "reason_code": "invalid_page_evidence",
                    "exclude_from_train": True,
                }
            )
            decisions.append(decision)
            continue

        subcluster_id = str(row.get("subcluster_id") or "")
        if subcluster_id not in subcluster_seen:
            subcluster_seen.add(subcluster_id)
            decision.update(
                {
                    "pool_bucket": "train_candidate",
                    "reason_code": "canonical_subcluster_representative",
                    "keep_in_train": True,
                }
            )
            canonical_candidates.append(decision)
        else:
            decision.update(
                {
                    "pool_bucket": "reserve",
                    "reason_code": "subcluster_overflow",
                    "move_to_reserve": True,
                    "exclude_from_train": True,
                }
            )
        decisions.append(decision)

    train_candidates = [row for row in decisions if row["pool_bucket"] == "train_candidate"]
    if family_share_cap > 0 and train_candidates:
        max_per_family = max(1, int(math.floor(len(train_candidates) * family_share_cap)))
        family_groups: defaultdict[str, List[Dict[str, Any]]] = defaultdict(list)
        for decision in train_candidates:
            family_groups[str(decision.get("family_key") or "unknown_family")].append(decision)
        for family_rows in family_groups.values():
            family_rows.sort(key=lambda row: (str(row.get("cluster_id") or ""), str(row.get("subcluster_id") or ""), str(row.get("sample_id") or "")))
            for overflow in family_rows[max_per_family:]:
                overflow.update(
                    {
                        "pool_bucket": "reserve",
                        "reason_code": "family_share_cap",
                        "keep_in_train": False,
                        "move_to_reserve": True,
                        "exclude_from_train": True,
                    }
                )

    summary = {
        "total_records": len(decisions),
        "train_count": sum(1 for row in decisions if row["pool_bucket"] == "train_candidate"),
        "reserve_count": sum(1 for row in decisions if row["pool_bucket"] == "reserve"),
        "reject_count": sum(1 for row in decisions if row["pool_bucket"] == "reject"),
        "family_share_cap": family_share_cap,
    }
    return decisions, summary


def build_review_manifest(records: Sequence[Dict[str, Any]], decisions: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    decision_map = {str(row.get("sample_id")): row for row in decisions}
    review_rows: List[Dict[str, Any]] = []
    for record in records:
        sample_id = str(record.get("sample_id") or "")
        decision = decision_map.get(sample_id, {})
        review_rows.append(
            {
                "sample_id": sample_id,
                "sample_dir": record.get("sample_dir"),
                "family_key": record.get("family_key"),
                "cluster_id": record.get("cluster_id"),
                "subcluster_id": record.get("subcluster_id"),
                "page_validity_status": record.get("page_validity_status"),
                "pool_bucket": decision.get("pool_bucket") or "",
                "reason_code": decision.get("reason_code") or "",
                "input_url": record.get("input_url"),
                "final_url": record.get("final_url"),
                "normalized_input_url": record.get("normalized_input_url"),
                "normalized_final_url": record.get("normalized_final_url"),
                "registrable_domain": record.get("registrable_domain"),
                "claimed_brands": record.get("claimed_brands") or [],
                "page_stage_candidate": record.get("page_stage_candidate"),
                "language_candidate": record.get("language_candidate"),
            }
        )
    return review_rows


def build_training_exclusion_list(decisions: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for decision in decisions:
        if not decision.get("exclude_from_train"):
            continue
        rows.append(
            {
                "sample_id": decision.get("sample_id"),
                "sample_dir": decision.get("sample_dir"),
                "pool_bucket": decision.get("pool_bucket"),
                "reason_code": decision.get("reason_code"),
            }
        )
    return rows
