# EVT Dataset Output Frozen Spec v1.1

版本：v1.1  
状态：冻结（Frozen）  
来源：**以当前脚本实现为准**，不是以旧版口头说明或过时草稿为准。  
适用脚本：
- `capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `evt_dataset_backfill_labels_brandlex.py`
- `evt_auto_label_utils_brandlex.py`

---

## 1. 目的

这份文档用于冻结 **当前脚本真实落盘的数据结构**，包括：

- 成功抓取样本目录里会有哪些文件
- 每个 `json/txt/png/html` 文件里具体有什么
- 自动弱标签 `auto_labels.json` 与规则标签 `rule_labels.json` 的完整结构
- 哪些文件默认生成，哪些是可选生成
- 哪些字段后续**不再变动**（除非审稿要求或明确升版本）

这份文档的定位是：

**以后数据目录、补标脚本、统计脚本、训练脚本，都以这份文档作为数据结构基线。**

---

## 2. 冻结原则

### 2.1 以当前脚本实现为准

如果旧文档、早期聊天记录、字段草稿，和当前脚本实现不一致，**以当前脚本输出为准**。

### 2.2 冻结范围

本次冻结的范围包括：

- 样本目录结构
- 各文件名
- JSON 顶层字段名
- 自动标签 `auto_labels.json` 的字段名
- 规则标签 `rule_labels.json` 的字段名
- 可选目录 `after_action/` 与 `variants/` 的文件结构

### 2.3 后续允许改动的唯一情况

只允许以下两种情况改动：

1. 审稿要求必须新增或调整字段；
2. 明确升版本，例如 `v1.2 / v2.0`。

否则：

- 不允许偷改字段名
- 不允许偷偷改枚举值
- 不允许把旧字段删掉不告知

---

## 3. 顶层样本目录结构

一个**成功样本**目录的标准结构如下。

```text
sample_dir/
├─ meta.json
├─ url.json
├─ env.json
├─ redirect_chain.json
├─ html_raw.html                  # 可选，默认开启
├─ html_rendered.html             # 可选，默认开启
├─ visible_text.txt               # 可选，默认开启
├─ forms.json                     # 可选，默认开启
├─ screenshot_viewport.png        # 必有（成功样本）
├─ screenshot_full.png            # 可选，默认尝试保存
├─ net_summary.json               # 必有
├─ auto_labels.json               # 默认开启
├─ rule_labels.json               # 默认关闭；离线补标可开启
├─ manual_labels.json             # 不由当前脚本自动生成；人工标注时新增
│
├─ actions.jsonl                  # 仅 ENABLE_STEP1_ACTION=True 时生成
├─ after_action/                  # 仅 step1 成功时生成
│  ├─ step1_screenshot_viewport.png
│  ├─ step1_html_rendered.html
│  ├─ step1_visible_text.txt
│  ├─ step1_forms.json
│  └─ step1_net_summary.json
│
└─ variants/                      # 仅 ENABLE_VARIANTS=True 时生成
   ├─ <variant_name_1>/
   │  ├─ meta_variant.json
   │  ├─ screenshot_viewport.png
   │  ├─ html_rendered.html
   │  ├─ visible_text.txt
   │  ├─ forms.json
   │  └─ net_summary.json
   ├─ <variant_name_2>/
   │  └─ ...
   └─ diff_summary.json           # 注意：实际写在 sample_dir 根目录，不在 variants/ 内
```

---

## 4. 生成条件

### 4.1 成功样本才会建目录

当前采集脚本的规则是：

- **失败 / 不可访问 / 状态码不允许 / 明显拦截页 / 截图质量失败**：不创建样本目录
- **成功样本**：才创建样本目录并落盘

### 4.2 默认开启 / 默认关闭

按当前脚本默认值：

- 默认开启：
  - `html_raw.html`
  - `html_rendered.html`
  - `visible_text.txt`
  - `forms.json`
  - `screenshot_full.png`（但若页面过高或截图失败，可缺失）
  - `auto_labels.json`
  - `net_summary.json`

- 默认关闭：
  - `actions.jsonl`
  - `after_action/`
  - `variants/`
  - `diff_summary.json`
  - `rule_labels.json`

---

## 5. 样本根目录命名与 sample_id

样本目录名由：

- URL 经过清洗后的安全文件夹名
- 加上 UTC 时间戳

共同组成。

`meta.json.sample_id` 直接等于样本目录名。

---

## 6. 文件级结构说明

---

## 6.1 `meta.json`

用途：记录样本基础元信息。

### 实际字段

```json
{
  "sample_id": "<folder_name>",
  "label": "phish | benign",
  "crawl_time_utc": "YYYYMMDDTHHMMSSZ",
  "http_status": 200,
  "page_title": "...",
  "etld1_mode": "..."
}
```

### 字段说明

- `sample_id`：样本目录名
- `label`：根目录标签提示，一般来自 crawler 当前处理的集合（如 `phish/benign`），**不是人工金标**
- `crawl_time_utc`：抓取时间（UTC，紧凑格式）
- `http_status`：主文档响应状态码
- `page_title`：页面标题
- `etld1_mode`：eTLD+1 提取模式（脚本内部配置）

---

## 6.2 `url.json`

用途：记录输入 URL、最终 URL 与原始跳转链。

### 实际字段

```json
{
  "input_url": "https://...",
  "final_url": "https://...",
  "redirect_chain": [
    "https://...",
    "https://..."
  ]
}
```

### 字段说明

- `input_url`：原始输入 URL（归一化后）
- `final_url`：页面最终落点 URL
- `redirect_chain`：按请求跳转顺序记录的 URL 字符串数组

---

## 6.3 `env.json`

用途：记录抓取环境参数。

### 实际字段

```json
{
  "browser_channel": "chrome",
  "headless": true,
  "viewport": {"width": 1365, "height": 768},
  "java_script_enabled": true,
  "service_workers": "block",
  "ignore_https_errors": false,
  "bypass_csp": false,
  "proxy_server": null,
  "user_agent": "..."
}
```

### 字段说明

- `browser_channel`：浏览器通道
- `headless`：是否无头
- `viewport`：窗口大小
- `java_script_enabled`：是否启用 JS
- `service_workers`：service worker 策略
- `ignore_https_errors`：是否忽略 HTTPS 错误
- `bypass_csp`：是否绕过 CSP
- `proxy_server`：代理地址；无代理时通常为 `null`
- `user_agent`：页面实际 UA

---

## 6.4 `redirect_chain.json`

用途：单独保存跳转链，方便下游直接读取。

### 实际结构

```json
[
  "https://first-hop.example/...",
  "https://second-hop.example/...",
  "https://final.example/..."
]
```

说明：它与 `url.json.redirect_chain` 含义一致，只是单独落一份文件，方便训练/统计直接消费。

---

## 6.5 `html_raw.html`

用途：主文档原始响应体（raw HTML）。

### 特点

- 来自响应体 `resp.text()`
- 可能包含 `<!-- TRUNCATED -->` 标记
- 长度受 `MAX_HTML_CHARS` 限制

---

## 6.6 `html_rendered.html`

用途：浏览器渲染后的 DOM 内容。

### 特点

- 来自 `page.content()`
- 可能与 `html_raw.html` 不同
- 长度受 `MAX_HTML_CHARS` 限制

---

## 6.7 `visible_text.txt`

用途：页面可见文本抽取结果。

### 特点

- 默认包含标题 + 页面主体可见文本
- 若正文很空，会回退收集 `h1/h2/h3/button/a/label/p/span`
- 长度受 `MAX_VISIBLE_TEXT_CHARS` 限制

这份文件是当前文本塔 / 离线补标的重要输入之一。

---

## 6.8 `forms.json`

用途：页面表单与输入字段结构。

### 实际结构

```json
{
  "forms": [
    {
      "action": "...",
      "action_abs": "https://...",
      "method": "GET | POST | ...",
      "inputs": [
        {
          "tag": "input | textarea | select",
          "type": "text | password | email | ...",
          "name": "...",
          "id": "...",
          "autocomplete": "...",
          "placeholder": "...",
          "aria_label": "..."
        }
      ],
      "has_password": true,
      "has_otp": false,
      "has_card": false
    }
  ]
}
```

### 字段说明

#### 顶层
- `forms`：页面中所有 `form` 的数组

#### 单个 form
- `action`：原始 action
- `action_abs`：绝对化后的 action URL
- `method`：表单提交方法
- `inputs`：表单内部所有 `input/textarea/select`
- `has_password`：表单内是否存在密码相关证据
- `has_otp`：表单内是否存在 OTP 相关证据
- `has_card`：表单内是否存在卡支付相关证据

#### 单个 input
- `tag`
- `type`
- `name`
- `id`
- `autocomplete`
- `placeholder`
- `aria_label`

---

## 6.9 `screenshot_viewport.png`

用途：首屏截图。

说明：

- 成功样本必有
- 通过了基本截图质量闸门
- 是视觉后续人工复核、OCR、轻量视觉摘要的原始依据

---

## 6.10 `screenshot_full.png`

用途：整页截图。

说明：

- 默认尝试保存
- 若页面过高或 full-page 截图失败，可能不存在
- 不存在不代表样本失败

---

## 6.11 `net_summary.json`

用途：轻量网络证据摘要。

当前脚本有三种来源：

1. 默认：`NetEvidenceLiteCollector` 在线统计得到摘要  
2. 若改成 HAR 模式：由 `network.har` 再汇总  
3. 若网络证据关闭：写入 `{"note": "net_summary_disabled"}`

### 默认 lite 模式下的实际结构

```json
{
  "final_url": "https://...",
  "top_frame_final_origin": "https://...",
  "request_counts": {
    "total": 123,
    "by_resource_type": {"document": 1, "script": 12},
    "by_method": {"GET": 120, "POST": 3}
  },
  "domain_counts": [
    {
      "domain_etld1": "example.com",
      "count": 10,
      "methods": {"GET": 9, "POST": 1}
    }
  ],
  "third_party_domains": ["cdn.example.net", "evil.com"],
  "post_targets": [
    {"domain_etld1": "evil.com", "count": 2}
  ],
  "status_counts": {...},
  "timing_ms": {
    "ttfb_p50": 100.0,
    "ttfb_p95": 300.0,
    "response_end_p50": 500.0,
    "response_end_p95": 1500.0
  },
  "navigation_chain": [
    {"url": "https://...", "status": 301},
    {"url": "https://...", "status": 200}
  ],
  "anomalies": ["many_third_party", "post_to_third_party"],
  "errors": ["..."]
}
```

### 字段说明

- `final_url`：最终 URL（安全摘要形式）
- `top_frame_final_origin`：最终 origin
- `request_counts.total`：请求总数
- `request_counts.by_resource_type`：按资源类型计数
- `request_counts.by_method`：按 HTTP 方法计数
- `domain_counts`：按 eTLD+1 聚合的请求计数和方法统计
- `third_party_domains`：与顶层站点不同的第三方域列表
- `post_targets`：POST 目标域及计数
- `status_counts`：HTTP 状态码分组统计
- `timing_ms`：网络时延分位数
- `navigation_chain`：带状态码的导航链
- `anomalies`：网络异常/风险提示
- `errors`：收集过程中的轻微异常

### `anomalies` 当前可能值

- `many_third_party`
- `post_to_third_party`
- `too_many_redirects`

---

## 6.12 `network.har`

用途：HAR 原始网络证据。

说明：

- 当前默认 `RECORD_NET_EVIDENCE_LITE=True`，因此通常不会落 `network.har`
- 若切到 HAR 模式，会保存该文件，并再由 HAR 生成 `net_summary.json`

### HAR 摘要模式下 `net_summary.json` 结构

如果由 `summarize_har()` 生成，则结构会变成：

```json
{
  "har_path": "network.har",
  "entry_count": 100,
  "unique_domains": 12,
  "top_domains": [["example.com", 40]],
  "post_domains": [["evil.com", 2]],
  "methods": [["GET", 90], ["POST", 10]],
  "status": [[200, 85], [302, 10]],
  "mime": [["text/html", 5], ["application/javascript", 40]]
}
```

所以：

**`net_summary.json` 是固定文件名，但内部结构取决于当前网络证据模式。**

---

## 6.13 `actions.jsonl`

用途：记录 step1 轻量交互候选与最终决策。

### 生成条件

仅在 `ENABLE_STEP1_ACTION=True` 时生成。

### 行结构

每一行是一个 JSON 对象，常见有两种：

#### 候选项行

```json
{
  "type": "candidate",
  "selector": "...",
  "xpath": "...",
  "text": "...",
  "tag": "button",
  "attributes": {...},
  "in_form": true,
  "form_action": "...",
  "form_method": "POST",
  "score_total": 67,
  "score_breakdown": {...},
  "chosen": false
}
```

#### 决策行

```json
{
  "type": "decision",
  "chosen_selector": "...",
  "chosen_reason": "...",
  "before_url": "https://...",
  "after_url": "https://...",
  "popup_count": 0,
  "download_count": 0,
  "error": "optional_error"
}
```

### 可能的 `decision.error`

- `no_candidates`
- `no_candidate_above_threshold`
- `cross_domain_navigation`
- `click_failed:<ExceptionType>`
- 其他异常字符串

---

## 6.14 `after_action/` 目录

用途：step1 轻量交互后的页面快照。

### 生成条件

只有 step1 执行成功且返回结果时才生成。

### 结构

```text
after_action/
├─ step1_screenshot_viewport.png
├─ step1_html_rendered.html
├─ step1_visible_text.txt
├─ step1_forms.json
└─ step1_net_summary.json
```

### 说明

- `step1_forms.json` 结构与 `forms.json` 一致
- `step1_net_summary.json` 结构与 `net_summary.json` 的 lite 模式类似，但仅对应 step1 后阶段

---

## 6.15 `variants/` 与 `diff_summary.json`

用途：多环境变体抓取与可能 cloaking 差异分析。

### 生成条件

仅在 `ENABLE_VARIANTS=True` 时生成。

### 单个变体目录结构

```text
variants/<variant_name>/
├─ meta_variant.json
├─ screenshot_viewport.png
├─ html_rendered.html
├─ visible_text.txt
├─ forms.json
└─ net_summary.json
```

### `meta_variant.json` 结构

```json
{
  "name": "desktop_zh",
  "config": {
    "user_agent": "...",
    "locale": "zh-CN",
    "timezone_id": "Asia/Shanghai",
    "viewport": {"width": 1365, "height": 768},
    "headless": true,
    "proxy_server": null
  },
  "status": 200,
  "final_url": "https://...",
  "title": "...",
  "error": null,
  "elapsed_ms": 1234
}
```

### 根目录下 `diff_summary.json` 结构

```json
{
  "base": {
    "final_url": "https://...",
    "status": 200,
    "title": "...",
    "visible_text_len": 1000,
    "visible_text_simhash": 123456,
    "forms_summary": {
      "has_password": true,
      "has_otp": false,
      "input_count": 3,
      "input_types": {"password": 1, "text": 2},
      "action_domains": ["evil.com"]
    },
    "network_summary": {
      "third_party_domains": ["evil.com"],
      "post_targets": ["evil.com"]
    }
  },
  "variants": {
    "desktop_en": { ... 同 base 结构 ... }
  },
  "diff": {
    "desktop_en": {
      "visible_text": {
        "simhash_distance": 12,
        "jaccard": 0.55,
        "len_delta": 200
      },
      "forms": {
        "has_password_changed": true,
        "input_count_delta": 1,
        "action_domain_changed": false
      },
      "network": {
        "third_party_domains_delta": 4,
        "post_targets_changed": true
      },
      "final_url_changed": false
    }
  },
  "flags": ["possible_cloaking", "dynamic_redirect", "variant_failed"],
  "errors": {
    "desktop_en": "variant_total_timeout"
  }
}
```

### `flags` 当前可能值

- `dynamic_redirect`
- `possible_cloaking`
- `variant_failed`

---

## 6.16 `auto_labels.json`

用途：脚本自动生成的弱标签层。

### 重要说明：这里以**当前实现真实输出**为准

虽然 `schema_version` 会写成 `evt_v1.1`，但当前实际脚本输出的字段与早期 schema 草稿并非完全一字不差。以后请以**当前实现冻结版**为准。

### 顶层结构

```json
{
  "schema_version": "evt_v1.1",
  "generated_at_utc": "2026-03-16T...Z",
  "source": "crawler_v6_inline | backfill",
  "label_hint": "phish | benign | unknown | null",
  "page_stage_candidate": "login | verification | payment | wallet_connect | pii_collection | download | transition | other",
  "language_candidate": "zh | ja | ko | arabic | cyrillic | latin | unknown",
  "url_features": {...},
  "form_features": {...},
  "html_features": {...},
  "brand_signals": {...},
  "intent_signals": {...},
  "evasion_signals": {...},
  "network_features": {...},
  "risk_outputs": {...}
}
```

### 6.16.1 顶层字段说明

- `schema_version`：固定为 `evt_v1.1`
- `generated_at_utc`：自动标签生成时间
- `source`：例如 `crawler_v6_inline` 或 `backfill`
- `label_hint`：来源提示，不是人工真值
- `page_stage_candidate`：页面阶段候选
- `language_candidate`：粗语言/文字脚本候选

### 6.16.2 `page_stage_candidate` 当前实际枚举

**当前实现真实取值为：**

- `login`
- `verification`
- `payment`
- `wallet_connect`
- `pii_collection`
- `download`
- `transition`
- `other`

> 冻结说明：后续统计与训练以这组实际枚举为准，不再参考早期草稿里的 `landing / wallet / notification / unknown` 等旧值。

### 6.16.3 `language_candidate` 枚举

- `zh`
- `ja`
- `ko`
- `arabic`
- `cyrillic`
- `latin`
- `unknown`

说明：这是**粗脚本/粗语言候选**，不是严格语言识别。

---

### 6.16.4 `url_features`

```json
{
  "input_url": "https://...",
  "final_url": "https://...",
  "host": "sub.example.com",
  "etld1": "example.com",
  "subdomain_depth": 2,
  "is_ip_host": false,
  "has_punycode": false,
  "url_length": 123,
  "path_length": 20,
  "digit_count": 4,
  "special_char_count": 3,
  "suspicious_url_keywords": ["login", "verify"],
  "path": "/signin",
  "netloc": "sub.example.com",
  "path_loginish": true
}
```

说明：

- `is_ip_host`：注意字段名是 `is_ip_host`，不是 `has_ip_host`
- `suspicious_url_keywords`：命中的高风险 URL 关键词列表
- `path_loginish`：path 是否像登录/验证/支付/钱包相关路径

---

### 6.16.5 `form_features`

```json
{
  "form_count": 1,
  "input_total": 3,
  "input_types": {"password": 1, "text": 2},
  "input_attr_hints": {
    "email_like": 0,
    "phone_like": 0,
    "otp_like": 1,
    "user_like": 1,
    "name_like": 0,
    "address_like": 0,
    "card_like": 0
  },
  "has_password": true,
  "has_otp": true,
  "has_card": false,
  "form_methods": {"POST": 1},
  "action_domains": ["evil.com"],
  "off_domain_form_action": true
}
```

说明：

- `input_attr_hints` 是通过字段属性推断出的弱语义提示
- `off_domain_form_action` 是后续补上的跨域提交判断

---

### 6.16.6 `html_features`

```json
{
  "external_script_count": 12,
  "external_script_domain_count": 4,
  "external_script_domains": ["cdn.jsdelivr.net", "googleapis.com"],
  "known_js_libraries": ["jquery"],
  "known_js_library_hits": {"jquery": ["jquery"]},
  "library_version_candidates": ["3.6.0"],
  "inline_obfuscation_like_count": 2,
  "captcha_evidence": false,
  "download_evidence": false
}
```

说明：

- 当前实现里 **没有** `title / text_len / urgency_evidence / wallet_evidence / password_evidence` 这类字段
- 当前 `html_features` 重点偏向：外部脚本、已知 JS 库、版本候选、简单混淆痕迹、captcha/download 证据

---

### 6.16.7 `brand_signals`

```json
{
  "brand_claim_present_candidate": true,
  "claimed_brands": ["paypal"],
  "brand_claim_source": "text | url | mixed | none",
  "text_brand_candidates": ["paypal"],
  "url_brand_candidates": ["paypal"],
  "domain_brand_consistency_candidate": "consistent | mismatch | no_brand_claim | unknown",
  "brand_token_in_url": ["paypal"]
}
```

说明：

- `claimed_brands`：综合 `text + url` 后去重得到的品牌候选
- `brand_claim_source`：
  - `text`
  - `url`
  - `mixed`
  - `none`
- `domain_brand_consistency_candidate`：
  - `consistent`
  - `mismatch`
  - `no_brand_claim`
  - `unknown`

---

### 6.16.8 `intent_signals`

```json
{
  "credential_intent_candidate": true,
  "otp_intent_candidate": false,
  "payment_intent_candidate": false,
  "wallet_connect_intent_candidate": false,
  "personal_info_intent_candidate": false,
  "urgency_or_threat_language_candidate": true,
  "social_engineering_language_candidate": true,
  "download_intent_candidate": false
}
```

说明：

- 这是页面在“索要什么 / 诱导做什么”的弱语义层
- `download_intent_candidate` 会参考 HTML download 证据和文本下载关键词

---

### 6.16.9 `evasion_signals`

```json
{
  "captcha_present_candidate": true,
  "dynamic_redirect_candidate": false,
  "cloak_suspected_candidate": false,
  "anti_bot_or_cloaking_candidate": true,
  "variant_failed_candidate": false,
  "needs_interaction_candidate": true
}
```

说明：

- `captcha_present_candidate`：HTML/文本层面的 CAPTCHA 候选
- `dynamic_redirect_candidate`：variants 对比里最终 URL 是否变化
- `cloak_suspected_candidate`：根据 variants 差异与 flags 判断
- `anti_bot_or_cloaking_candidate`：CAPTCHA / cloudflare / cloaking 的合并判断
- `variant_failed_candidate`：变体采集失败或 diff_summary 有错误
- `needs_interaction_candidate`：需要交互才能揭示主要内容的候选

---

### 6.16.10 `network_features`

```json
{
  "third_party_domain_count": 2,
  "third_party_domains": ["evil.com", "cdn.net"],
  "post_target_count": 1,
  "post_to_third_party": true,
  "many_third_party": false,
  "too_many_redirects": false,
  "request_total": 25,
  "resource_type_counts": {"document": 1, "script": 8},
  "response_headers_present": {
    "content_security_policy": false,
    "strict_transport_security": true,
    "x_frame_options": false,
    "x_content_type_options": true,
    "referrer_policy": false
  }
}
```

说明：

- `response_headers_present` 只记录**是否存在**，不保存 header 内容

---

### 6.16.11 `risk_outputs`

```json
{
  "risk_score_weak": 72,
  "risk_level_weak": "low | medium | high | critical",
  "risk_reasons": [
    "brand_domain_mismatch",
    "credential_intent",
    "off_domain_form_action"
  ]
}
```

### `risk_reasons` 当前可能值

按当前实现，原因列表来自以下规则项：

- `brand_domain_mismatch`
- `credential_intent`
- `payment_intent`
- `otp_intent`
- `wallet_connect_intent`
- `urgency_language`
- `off_domain_form_action`
- `post_to_third_party`
- `many_third_party`
- `captcha_or_cloak`
- `dynamic_redirect`
- `punycode_or_ip_host`
- `suspicious_url_keywords`
- `inline_obfuscation_like`

### `risk_level_weak` 阈值

- `critical`：`score >= 70`
- `high`：`45 <= score < 70`
- `medium`：`20 <= score < 45`
- `low`：`score < 20`

---

## 6.17 `rule_labels.json`

用途：基于 `auto_labels.json` 的规则补齐结果。

### 生成方式

- 离线补标脚本：`--emit-rule-labels`
- 在线采集脚本：只有 `SAVE_RULE_LABELS=True` 才生成

### 结构

```json
{
  "schema_version": "evt_v1.1",
  "generated_at_utc": "2026-03-16T...Z",
  "rule_flags": {
    "escalate_to_l2_candidate": true,
    "brand_mismatch_with_sensitive_intent": true,
    "off_domain_sensitive_form": true
  },
  "review_priority": "p0 | p1 | p2 | p3",
  "threat_taxonomy_v1": {
    "primary_threat_label_candidate": "credential_theft | payment_fraud | wallet_drain_or_web3_approval_fraud | pii_kyc_harvesting | fake_support_or_contact_diversion | malware_or_fake_download | benign | uncertain",
    "primary_threat_label_confidence": 0.0,
    "primary_threat_label_rules": ["..."],
    "scenario_label_candidate": "finance_banking | ecommerce_retail | payment_platform | logistics_delivery | enterprise_mail_cloud | social_media | government_public_service | crypto_web3 | gaming | telecom_utility | tech_support | job_recruitment | other",
    "scenario_label_confidence": 0.0,
    "scenario_label_rules": ["..."],
    "narrative_tags_candidate": ["brand_impersonation"],
    "evidence_tags_candidate": ["credential_form_present"],
    "evasion_tags_candidate": ["requires_interaction_to_reveal"],
    "ecosystem_tags_candidate": ["illicit_service_content"],
    "taxonomy_source": "rule_derived_from_auto_labels",
    "taxonomy_review_status": "weak_candidate_only"
  }
}
```

### 字段说明

- `escalate_to_l2_candidate`：是否应进入高层复核
- `brand_mismatch_with_sensitive_intent`：品牌不一致 + 敏感意图
- `off_domain_sensitive_form`：异域提交 + 敏感表单
- `review_priority`：
  - `p0`：`risk_level_weak == critical`
  - `p1`：`high`
  - `p2`：`medium`
  - `p3`：其余
- `threat_taxonomy_v1`：长期保留在 `rule_labels.json` 下的活跃弱标签命名空间，不是临时实验字段
- `primary_threat_label_candidate`：一级主威胁候选标签，不等同于人工金标
- `primary_threat_label_confidence`：规则派生置信度，属于启发式分数，不是校准概率
- `primary_threat_label_rules`：触发该候选标签的规则来源列表
- `scenario_label_candidate`：行业 / 场景外壳候选标签
- `scenario_label_confidence`：场景候选的规则派生置信度
- `scenario_label_rules`：触发该场景候选的规则来源列表
- `narrative_tags_candidate`：社工叙事候选标签列表
- `evidence_tags_candidate`：显式证据候选标签列表
- `evasion_tags_candidate`：对抗 / 规避候选标签列表
- `ecosystem_tags_candidate`：生态 / 内容属性候选标签列表
- `taxonomy_source`：固定标记为规则派生来源
- `taxonomy_review_status`：固定弱标签安全语义，当前默认值为 `weak_candidate_only`

### 使用边界

- `threat_taxonomy_v1` 应继续通过统一离线 backfill 提高覆盖率
- 它承载 Warden 多威胁主问题定义，但不直接提升为 TrainSet V1 primary 默认金标
- 当前 primary manifest 核心字段不默认展开写入该命名空间

---

## 6.18 `manual_labels.json`

用途：人工金标层。

说明：

- 当前采集脚本和离线补标脚本**不会自动生成**这个文件
- 这是你后续人工标注时新增的文件
- 推荐与当前 EVT v1.1 逻辑 schema 对齐

### 冻结推荐结构

```json
{
  "manual_final_label": "benign | phishing | suspicious | unknown",
  "hard_case_reason": "",
  "manual_review_status": "unreviewed | reviewed | disputed"
}
```

---

## 7. 离线补标脚本的输入与输出

适用脚本：`evt_dataset_backfill_labels_brandlex.py`

### 输入要求

被识别为样本目录的条件是：

- 目录存在 `meta.json`
- 目录存在 `url.json`

### 读取的文件

- `meta.json`
- `url.json`
- `forms.json`（不存在则视为 `{"forms": []}`）
- `net_summary.json`（不存在则 `{}`）
- `diff_summary.json`（不存在则 `null`）
- `visible_text.txt`
- `html_rendered.html`
- 若 `html_rendered.html` 不存在，则回退读 `html_raw.html`

### 生成的文件

- 默认：`auto_labels.json`
- 开启 `--emit-rule-labels`：额外生成 `rule_labels.json`

它不会重写：

- `meta.json`
- `url.json`
- `env.json`
- `redirect_chain.json`
- 截图文件
- `manual_labels.json`

---

## 8. 品牌词典加载规则

适用脚本：

- `capture_url_v6_optimized_v6_2_plus_labels_brandlex.py`
- `evt_dataset_backfill_labels_brandlex.py`
- `evt_auto_label_utils_brandlex.py`

### 优先级

1. 显式传参的品牌词典路径
2. 当前目录/脚本同目录自动发现：
   - `evt_brand_lexicon_v1.json`
   - `evt_brand_lexicon.json`
3. 内置小词典兜底

### 品牌信号来源

- `text_brand_candidates`：来自标题 + 可见文本
- `url_brand_candidates`：来自 host token + 受限 typo 匹配
- `claimed_brands`：二者合并去重

---

## 9. 当前实现与旧 schema 草稿的差异说明（必须知道）

为了防止后面自己坑自己，这里把最关键的一条说死：

**当前脚本实现已经是数据真相。**

尤其下面这些地方，后续请以当前实现为准：

### 9.1 `page_stage_candidate` 以当前实现枚举为准

当前实现真实值：

- `login`
- `verification`
- `payment`
- `wallet_connect`
- `pii_collection`
- `download`
- `transition`
- `other`

### 9.2 `url_features` 当前真实字段名是 `is_ip_host`

不是早期草稿里那种 `has_ip_host`。

### 9.3 `html_features` 当前更偏“脚本/库/混淆/下载/captcha”

不是那种大而全的 HTML 语义总表。

### 9.4 `manual_labels.json` 是推荐结构，不是当前脚本自动产物

---

## 10. 冻结建议

从现在开始，建议你把这份文档当成：

**EVT 数据集落盘与标签结构的冻结版规范。**

如果后续要改：

- 先改文档版本号
- 再改脚本
- 再改补标和训练工具

不要反过来先改脚本，再让文档追着擦屁股。

---

## 11. 最终结论

这份文档冻结的是：

- 当前新版抓取脚本的**真实落盘文件结构**
- 当前自动补标脚本的**真实标签结构**
- 当前规则补齐层的**真实输出结构**
- 后续人工标注建议使用的 `manual_labels.json` 结构

**从这版起，EVT 数据结构默认不再变动。除非审稿要求，或者你明确升版本。**
