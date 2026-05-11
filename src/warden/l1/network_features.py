"""Network summary feature extraction for the L1 rule baseline."""

from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

from .url_features import approximate_registrable_domain, host_from_url


def _requests(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("requests", "request_log", "entries"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def extract_network_features(net_summary: Any, *, final_host: str = "") -> Dict[str, Any]:
    requests = _requests(net_summary)
    methods = Counter()
    third_party_domains: set[str] = set()
    post_targets: set[str] = set()
    final_reg = approximate_registrable_domain(final_host)

    for item in requests:
        method = str(item.get("method") or item.get("request_method") or "GET").upper()
        methods[method] += 1
        url = str(item.get("url") or item.get("request_url") or "")
        host = host_from_url(url)
        if not host:
            continue
        if method == "POST":
            post_targets.add(host)
        if final_reg and approximate_registrable_domain(host) != final_reg:
            third_party_domains.add(host)

    chain = {}
    anomalies: List[str] = []
    if isinstance(net_summary, dict):
        chain = net_summary.get("navigation_chain") or net_summary.get("redirect_chain") or {}
        raw_anomalies = net_summary.get("network_anomalies") or net_summary.get("anomalies") or []
        if isinstance(raw_anomalies, list):
            anomalies = [str(item) for item in raw_anomalies]
        elif raw_anomalies:
            anomalies = [str(raw_anomalies)]

    return {
        "request_total": len(requests) if requests else ("unknown" if not isinstance(net_summary, (dict, list)) else 0),
        "methods_summary": dict(sorted(methods.items())),
        "post_targets": sorted(post_targets),
        "third_party_domains": sorted(third_party_domains),
        "navigation_chain_summary": chain,
        "network_anomalies": anomalies,
    }
