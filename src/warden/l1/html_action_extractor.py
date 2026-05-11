"""Actionable HTML extraction using Python standard library parsing."""

from __future__ import annotations

from html.parser import HTMLParser
from typing import Dict, List, Tuple
from urllib.parse import urlparse

from .url_features import approximate_registrable_domain


SENSITIVE_NAME_HINTS = ("password", "passwd", "pass", "otp", "code", "card", "cc", "cvv", "wallet", "seed")
PRIMARY_CTA_HINTS = ("login", "sign in", "verify", "continue", "submit", "pay", "connect", "download", "claim")


def _compact(text: str) -> str:
    return " ".join((text or "").split())


class _ActionableHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.form_count = 0
        self.input_count = 0
        self.password_input_count = 0
        self.otp_or_code_input_hint_count = 0
        self.card_or_payment_input_hint_count = 0
        self.iframe_count = 0
        self.script_count = 0
        self.select_count = 0
        self.textarea_count = 0
        self.button_texts: List[str] = []
        self.link_texts: List[str] = []
        self.hrefs: List[str] = []
        self.meta_texts: List[str] = []
        self.title_texts: List[str] = []
        self.heading_texts: List[str] = []
        self._capture_stack: List[Tuple[str, List[str]]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        attr = {name.lower(): (value or "") for name, value in attrs}
        tag = tag.lower()
        if tag == "form":
            self.form_count += 1
        elif tag == "input":
            self.input_count += 1
            input_type = attr.get("type", "").lower()
            joined = " ".join([input_type, attr.get("name", ""), attr.get("id", ""), attr.get("placeholder", "")]).lower()
            if input_type == "password" or "password" in joined:
                self.password_input_count += 1
            if "otp" in joined or "code" in joined or "2fa" in joined:
                self.otp_or_code_input_hint_count += 1
            if "card" in joined or "cvv" in joined or "payment" in joined or "cc" in joined:
                self.card_or_payment_input_hint_count += 1
        elif tag == "iframe":
            self.iframe_count += 1
        elif tag == "script":
            self.script_count += 1
        elif tag == "select":
            self.select_count += 1
        elif tag == "textarea":
            self.textarea_count += 1
        elif tag == "a":
            href = attr.get("href", "")
            if href:
                self.hrefs.append(href)
            self._capture_stack.append(("a", []))
        elif tag == "button":
            self._capture_stack.append(("button", []))
        elif tag == "title":
            self._capture_stack.append(("title", []))
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._capture_stack.append(("heading", []))
        elif tag == "meta":
            content = attr.get("content", "")
            if content:
                self.meta_texts.append(_compact(content)[:120])

    def handle_data(self, data: str) -> None:
        if self._capture_stack:
            self._capture_stack[-1][1].append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if not self._capture_stack:
            return
        capture_tag, parts = self._capture_stack[-1]
        if (tag == "a" and capture_tag == "a") or (tag == "button" and capture_tag == "button"):
            self._capture_stack.pop()
            text = _compact(" ".join(parts))[:120]
            if text and capture_tag == "a":
                self.link_texts.append(text)
            elif text:
                self.button_texts.append(text)
        elif tag == "title" and capture_tag == "title":
            self._capture_stack.pop()
            text = _compact(" ".join(parts))[:120]
            if text:
                self.title_texts.append(text)
        elif tag.startswith("h") and capture_tag == "heading":
            self._capture_stack.pop()
            text = _compact(" ".join(parts))[:120]
            if text:
                self.heading_texts.append(text)


def _host_from_href(href: str) -> str:
    return (urlparse(href or "").hostname or "").lower().strip(".")


def extract_actionable_html_features(html_text: str | None, *, base_host: str = "", html_truncated: bool = False) -> Dict[str, object]:
    parser = _ActionableHTMLParser()
    try:
        parser.feed(html_text or "")
    except Exception:
        pass

    base_reg = approximate_registrable_domain(base_host)
    href_domains: List[str] = []
    external = 0
    for href in parser.hrefs:
        host = _host_from_href(href)
        if not host:
            continue
        href_domains.append(host)
        if base_reg and approximate_registrable_domain(host) != base_reg:
            external += 1

    node_count = (
        parser.form_count
        + parser.input_count
        + len(parser.button_texts)
        + len(parser.link_texts)
        + parser.iframe_count
        + parser.script_count
        + parser.select_count
        + parser.textarea_count
        + len(parser.title_texts)
        + len(parser.heading_texts)
        + len(parser.meta_texts)
    )
    compact_parts = (
        parser.title_texts
        + parser.heading_texts
        + parser.button_texts
        + parser.link_texts
        + parser.meta_texts
    )
    primary_cta = [
        text
        for text in parser.button_texts + parser.link_texts
        if any(hint in text.lower() for hint in PRIMARY_CTA_HINTS)
    ][:20]

    return {
        "form_count": parser.form_count,
        "input_count": parser.input_count,
        "password_input_count": parser.password_input_count,
        "otp_or_code_input_hint_count": parser.otp_or_code_input_hint_count,
        "card_or_payment_input_hint_count": parser.card_or_payment_input_hint_count,
        "button_texts_sample": parser.button_texts[:20],
        "link_texts_sample": parser.link_texts[:20],
        "href_domains_sample": sorted(set(href_domains))[:20],
        "external_link_count": external,
        "iframe_count": parser.iframe_count,
        "script_count": parser.script_count,
        "select_count": parser.select_count,
        "textarea_count": parser.textarea_count,
        "primary_cta_texts": primary_cta,
        "html_actionable_text_compact": _compact(" | ".join(compact_parts))[:4000],
        "html_actionable_node_count": node_count,
        "html_truncated": bool(html_truncated),
    }
