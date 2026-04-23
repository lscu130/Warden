# Warden_DATA_INGEST_RUNBOOK_V1

## 涓枃鐗?

> 闈㈠悜 AI 鐨勮鏄庯細GPT銆丟emini銆丆odex銆丟rok銆丆laude 浠呭皢涓嬫柟鑻辨枃鐗堣涓烘潈濞佺増鏈€備腑鏂囦粎渚涗汉绫婚槄璇汇€佸崗浣滀笌蹇€熷瑙堛€?

### 浣跨敤璇存槑

- 鏈枃妗ｆ槸鏃ュ父閲囨牱鎶撳彇鐨勬搷浣滄墜鍐岋紝涓嶆槸鏋舵瀯璁捐鏂囨。銆?
- 鏂囦腑鍛戒护浣跨敤缁濆璺緞鍗犱綅绗︼紝浣犲彧闇€瑕佹妸 `<WARDEN_ROOT>`銆乣<WARDEN_DATA_ROOT>`銆乣<RUN_DATE>`銆乣<BATCH_NAME>` 涔嬬被鍗犱綅绗︽浛鎹㈡垚浣犺嚜宸辩殑瀹為檯璺緞鍜屾壒娆″悕銆?- 鑻ヤ腑鑻卞唴瀹瑰啿绐侊紝浠ヨ嫳鏂囩増涓哄噯銆?

## 1. 鐩殑

杩欎唤 runbook 瑙ｅ喅鐨勬槸鈥滃钩甯告€庝箞鐢ㄢ€濄€?
閲嶇偣瑕嗙洊锛?

- 灏忚妯?benign 鎶撳彇
- 姣忔棩 malicious 鎵归噺鎶撳彇锛屽挨鍏舵槸澶х害 300 鏉?
- 鎶撳彇瀹屾垚鍚庣殑 cluster / train-reserve / review / exclusion 浜х墿鐢熸垚
- Windows 涓嬪父瑙佸潙

## 2. 鐩稿叧鑴氭湰

- benign 鎶撳彇鍏ュ彛锛歚scripts/data/benign/run_benign_capture.py`
- 鎭舵剰 feed 瀵煎叆锛歚scripts/data/malicious/ingest_public_malicious_feeds.py`
- malicious 鎶撳彇鍏ュ彛锛歚scripts/data/malicious/run_malicious_capture.py`
- 鏃?HTML 杞?JSON锛歚scripts/data/maintenance/convert_legacy_html_to_json.py`
- 鎭舵剰鑱氱被锛歚scripts/data/malicious/build_malicious_clusters.py`
- train / reserve 鍒掑垎锛歚scripts/data/malicious/build_malicious_train_pool.py`
- review manifest锛歚scripts/data/maintenance/build_dedup_review_manifest.py`
- exclusion list锛歚scripts/data/maintenance/build_training_exclusion_lists.py`

## 3. 鍓嶇疆鏉′欢

- 鍙互姝ｅ父杩愯 `python`
- 鎶撳彇鐜涓凡缁忓畨瑁呭苟鍙敤 `playwright`
- 鎶撳彇鐜涓凡缁忓畨瑁呭苟鍙敤 `playwright-stealth`
- 鍦ㄤ粨搴撴牴鐩綍鎵ц鍛戒护鏈€鐪佷簨
- 渚嬪瓙閲岀殑缁濆璺緞瑕佹浛鎹㈡垚浣犺嚜宸辩殑鐪熷疄璺緞

寤鸿鍏堣窇锛?
```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py --help
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py --help
```

## 4. 璺緞绾﹀畾

寤鸿姣忔杩愯閮藉崟鐙缓涓€涓壒娆＄洰褰曪紝涓嶈鎶婃瘡澶╃殑涓存椂涓棿缁撴灉鍏ㄦ贩鍦ㄤ竴璧枫€?

绀轰緥鍗犱綅锛?
- `<WARDEN_ROOT>`锛氫緥濡?`E:\Warden`
- `<WARDEN_DATA_ROOT>`锛氫緥濡?`E:\WardenData`
- `<RUN_DATE>`锛氫緥濡?`2026-03-24`
- `<BATCH_NAME>`锛氫緥濡?`daily300`

褰撳墠鏈湴榛樿鍚堝悓锛?
- 鎵€鏈夎繍琛屾湡鏁版嵁鐩綍榛樿浣嶄簬 `E:\WardenData`
- repo 内 `E:\Warden\data\README.md` 仅保留说明文档，不再作为大体量运行期数据根
- 如果你在旧 handoff 或旧命令里看到 `<WARDEN_ROOT>\data\...`，当前执行时应替换为 `<WARDEN_DATA_ROOT>\...`

寤鸿鐩綍锛?

- benign 杈撳叆锛歚<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\`
- malicious feed 涓棿浜х墿锛歚<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\`
- malicious cluster 涓棿浜х墿锛歚<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\`
- malicious pool 涓棿浜х墿锛歚<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\`
- malicious review / exclusion锛歚<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_review\`銆乣<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_exclusions\`
- benign 杈撳嚭鏍癸細`<WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME>\`
- malicious 杈撳嚭鏍癸細`<WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>\`

## 5. 甯哥敤鍦烘櫙 A锛氬皬瑙勬ā benign 鎶撳彇

### 5.1 鍑嗗 URL 鏂囨湰

鍑嗗涓€涓?UTF-8 鏂囨湰鏂囦欢锛屼緥濡傦細

`<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt`

姣忚涓€涓?URL銆?

### 5.2 ????

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en
```

### 5.3 ????????
- ?????????????
- ???????? `benign_capture_run.json`
- ?????????? capture ???????
- `meta.json` ????? `ingest_metadata` ??

### 5.4 benign ?????????

???? recovery ??????????????
????? benign ?????????????????????? Tranco ???????????????????????? URL ?????

???????

- ?? URL ????? supervised ??????? `skip`
- ?????????????????????????
- ???? benign ??????????? Tranco ??
- ?????????????????? recovery ????????

### 5.5 benign 鍗?URL 鍗′綇鏃剁殑 supervised 妯″紡

榛樿 benign runner 杩樻槸鈥滀竴娆℃媺璧蜂竴涓?capture 瀛愯繘绋嬭窇瀹屾暣鎵规鈥濄€?
鍙湁鍦ㄤ綘鏄惧紡鍔犱簡涓嬮潰杩欎袱涓弬鏁颁箣涓€鏃讹紝runner 鎵嶄細鍒囧埌 supervised 妯″紡锛?

- `--interactive_skip`
- `--url_hard_timeout_ms <姣>`

supervised 妯″紡涓嬶紝runner 浼氭寜 URL 閫愭潯鎷夎捣 capture 瀛愯繘绋嬨€?
杩欐牱褰撳墠 URL 濡傛灉鍗′綇锛屼綘鍙互鍦ㄧ粓绔緭鍏ワ細

```text
skip
```

鐒跺悗鍙粓姝㈠綋鍓?URL锛岀户缁悗闈㈢殑绔欑偣銆?

濡傛灉浣犺繕鎯崇粰姣忔潯 URL 涓€涓‖涓婇檺锛屽彲浠ュ啀鍔狅細

```powershell
--url_hard_timeout_ms 120000
```

绀轰緥锛?

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000
```

鎵规缁撴潫鍚庯紝`benign_capture_run.json` 浼氶澶栬褰曪細

- `supervised_mode`
- `interactive_skip`
- `url_hard_timeout_ms`
- `all_success`
- `skipped_urls`
- `timed_out_urls`
- `results`

## 6. 甯哥敤鍦烘櫙 B锛氭瘡澶╂姄澶х害 300 鏉?malicious

杩欐槸鏈€甯哥敤鐨勬搷浣滄祦绋嬨€?

### 6.1 鍏堟媺鍏叡 feed

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\ingest_public_malicious_feeds.py `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed
```

鐢熸垚鐨勫叧閿枃浠讹細

- `malicious_feed_candidates.jsonl`
- `malicious_feed_candidates.txt`
- `malicious_feed_summary.json`

### 6.2 浠庡€欓€夐噷鍒囦竴涓?daily 300 manifest

涓嶈鐢?`Get-Content | Set-Content` 鐩存帴鍒?JSONL锛學indows 涓嬪鏄撴妸 BOM 甯﹁繘绗竴琛屻€?

鐢ㄤ笅闈㈣繖涓?Python 鐗囨鏈€绋筹細

```powershell
@'
import json
import random
from pathlib import Path

src = Path(r"<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates.jsonl")
dst = Path(r"<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl")

rows = []
with src.open("r", encoding="utf-8-sig", errors="ignore") as f:
    for line in f:
        text = line.lstrip("\ufeff").strip()
        if not text:
            continue
        rows.append(json.loads(text))

random.seed(12345)
if len(rows) > 300:
    rows = random.sample(rows, 300)

with dst.open("w", encoding="utf-8", newline="\n") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("selected_rows =", len(rows))
print("output =", dst)
'@ | python -
```

濡傛灉浣犱笉鎯抽殢鏈烘娊鏍凤紝涔熷彲浠ユ妸 `random.sample(rows, 300)` 鏀规垚 `rows[:300]`銆?

### 6.3 璺?malicious 鎶撳彇

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --feed_manifest <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

### 6.4 鎴愬姛鍚庡厛妫€鏌ヤ粈涔?

鍏堢湅锛?

- `<WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>\malicious_capture_run.json`

閲嶇偣瀛楁锛?

- `all_success`
- `returncodes`

濡傛灉 `all_success` 涓?`true`锛岃鏄庤繖鎵?capture 杩涚▼绾у埆鏄垚鍔熺殑銆?

### 6.5 瀵硅繖鎵?malicious 鏍锋湰鍋?cluster

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_clusters.py `
  --input_roots <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters
```

鐢熸垚锛?

- `malicious_cluster_records.jsonl`
- `malicious_cluster_summary.json`

### 6.6 鏋勫缓 train / reserve pool

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_train_pool.py `
  --clusters_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool `
  --family_share_cap 0.10
```

鐢熸垚锛?

- `pool_decisions.jsonl`
- `train_pool_manifest.jsonl`
- `reserve_pool_manifest.jsonl`
- `pool_summary.json`

### 6.7 鐢熸垚 review / exclusion 浜х墿

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_dedup_review_manifest.py `
  --clusters_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --pool_decisions_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_review
```

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_training_exclusion_lists.py `
  --pool_decisions_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_exclusions
```

## 7. 甯哥敤鍦烘櫙 C锛氬彧鎯虫墜宸ユ姄涓€灏忔壒 malicious URL

濡傛灉浣犲凡缁忔湁涓€涓伓鎰?URL 鏂囨湰鏂囦欢锛屼笉鎯冲厛璧?feed ingest锛屼篃鍙互鐩存帴璺戯細

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

### 7.1 PT `verified_online.csv` 鎸夌‘璁ゆ椂闂村鍑?URL-only CSV

濡傛灉浣犵殑杈撳叆涓嶆槸 feed锛岃€屾槸鏈湴鐨?PT `verified_online.csv`锛屽苟涓斾綘鍙兂鍏堟寜 `verification_time` 鎴嚭鏌愪竴澶╁強涔嬪悗鐨?URL锛屽啀鍗曠嫭鎶撳彇锛屽彲浠ョ敤锛?
```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv
```

鑴氭湰鍚姩鍚庝細鍏堟彁绀轰綘杈撳叆锛?
```text
2026/3/27
```

瑙勫垯锛?
- 鎸?`verification_time` 鐨?UTC 鏃ユ湡鍋氳繃婊?- 閫変腑鑼冨洿鏄€滆緭鍏ユ棩鏈熷綋澶╁強涔嬪悗鈥?- 涓€娆¤繍琛屽悓鏃惰緭鍑猴細
  - 涓€浠?URL-only CSV锛屽彧鏈?`url` 鍒?  - 涓€浠戒竴琛屼竴涓?URL 鐨?TXT
- 榛樿杈撳嚭鍒?`<WARDEN_DATA_ROOT>\processed\pt_csv_exports\`

濡傛灉浣犳兂鎸囧畾杈撳嚭璺緞锛?
```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv `
  --output_csv <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
```

濡傛灉浣犱笉鏄惧紡缁?`--output_txt`锛岄粯璁や細鍦?CSV 鍚岀洰褰曠敓鎴愬悓鍚?`.txt` 鏂囦欢銆?
鎷垮埌 TXT 鍚庣洿鎺ユ姄锛?
```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt `
  --source phishtank `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

涔熷氨鏄畬鏁?PT 鏈湴娴佺▼鏄細

1. `export_phishtank_verified_urls.py`
2. `run_malicious_capture.py --input_path ...`

濡傛灉浣犳墜澶村凡缁忔湁鏃х殑 URL-only CSV锛屾病鏈夊搴?TXT锛屽啀鐢ㄥ鐢ㄨ剼鏈ˉ杞細

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\convert_url_csv_to_txt.py `
  --input_csv <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
```

## 8. 姣忔杩愯鍚庡缓璁汉宸ユ鏌ョ殑鏂囦欢

- benign锛歚benign_capture_run.json`
- malicious锛歚malicious_capture_run.json`
- cluster锛歚malicious_cluster_summary.json`
- pool锛歚pool_summary.json`
- 浠诲彇涓€涓牱鏈洰褰曢噷鐨?`meta.json`

閲嶇偣鐪嬶細

- `returncode` / `all_success`
- `ingest_metadata`
- `total_records`
- `train_count` / `reserve_count`
- `family_share_cap`

## 9. 甯歌闂

### 9.1 `playwright` 鎴?`playwright-stealth` 瀵煎叆澶辫触

璇存槑杩愯鐜娌″噯澶囧ソ锛屼笉鏄笂灞傝剼鏈弬鏁伴敊浜嗐€傚厛淇幆澧冿紝鍐嶉噸璺戙€?

甯歌淇硶锛?

```powershell
python -m pip install playwright
python -m pip install playwright-stealth
playwright install
```

### 9.2 JSONL 棣栬 BOM 瀵艰嚧 鈥渓ine 1 is not valid JSON鈥?

杩欓€氬父鏄墜宸ュ垏鏂囦欢鏃剁敤浜嗭細

```powershell
Get-Content ... | Set-Content ...
```

澶勭悊鏂瑰紡锛?

- 浼樺厛鐢ㄤ笂闈㈢殑 Python 鐗囨鍒?JSONL
- 涓嶈鐢?shell 鏂囨湰绠￠亾纭垏 JSONL

### 9.3 杈撳嚭鐩綍鍐欓敊

鏈€甯歌闂涓嶆槸鑴氭湰鍧忎簡锛岃€屾槸 `--output_root` 鎸囧埌浜嗘棫鐩綍锛岀粨鏋滀綘鍦ㄩ敊璇殑鍦版柟鎵句骇鐗┿€?

## 10. 鏈€灏忔棩甯稿懡浠ゆ竻鍗?

### 姣忓ぉ鎶?300 malicious

1. `ingest_public_malicious_feeds.py`
2. Python 鐗囨鍒?300 鏉?manifest
3. `run_malicious_capture.py`
4. `build_malicious_clusters.py`
5. `build_malicious_train_pool.py`
6. `build_dedup_review_manifest.py`
7. `build_training_exclusion_lists.py`

### 鍋跺皵琛ヤ竴鎵?benign

1. 鍑嗗 `benign_urls.txt`
2. `run_benign_capture.py`
3. 妫€鏌?`benign_capture_run.json`

### 9.4 `Timeout 25000ms exceeded` 浣嗘祻瑙堝櫒閲岀湅璧锋潵鍙堣兘鎵撳紑

杩欓€氬父涓嶄唬琛ㄩ〉闈㈢湡鐨勫畬鍏ㄦ墦涓嶅紑锛屾洿甯歌鐨勬槸锛?

- 鏃х増 `page.goto(..., wait_until="load")` 澶嫑鍒伙紝鑰岄〉闈富浣撳叾瀹炲凡缁忓嚭鏉ヤ簡
- 褰撳墠鎶撳彇鐜鐨?IP / 鍖哄煙 / 缃戠粶璺緞姣斾綘鎵嬪伐鎵撳紑缃戦〉鏃舵洿鎱?
- 鎶撳彇娴忚鍣ㄥ拰鎵嬪伐娴忚鍣ㄥ苟涓嶅湪鍚屼竴鏉＄綉缁滆矾寰勪笂
- Google / consent.google 杩欑被绔欑偣杩樺彲鑳藉厛鍗″湪 consent 鎴?bot 妫€娴嬪墠缃〉

褰撳墠榛樿 hardening 宸插唴寤猴細

- 榛樿瀵艰埅瓒呮椂宸叉斁瀹藉埌 `60000ms`
- 榛樿 `goto_wait_until` 宸叉敼涓?`commit`
- 瀵艰埅鍚庝細鍐嶇瓑涓€娆?`domcontentloaded` 鍜岀煭鏆?hydration
- Google 鍩熷悕浼氳嚜鍔ㄥ皾璇?consent 澶勭悊
- 娴忚鍣ㄩ〉鍒涘缓鍚庨粯璁ゅ惎鐢?stealth

褰撳墠 runner 鍜?capture 鑴氭湰浠嶆敮鎸佷互涓嬪彲閫夊弬鏁帮細

- `--nav_timeout_ms`
- `--proxy_server`
- `--proxy_username`
- `--proxy_password`
- `--disable_route_intercept`
- `--goto_wait_until`

寤鸿椤哄簭锛?

1. 鍏堢洿鎺ョ敤鏂扮殑榛樿閰嶇疆閲嶈瘯锛屼笉瑕佸厛鏀逛竴鍫嗗弬鏁?
2. 濡傛灉鎶ョ殑鏄?`net::ERR_ABORTED` 涓斿崱鍦?`wait_until="commit"`锛屽厛鍋氫竴涓瀬灏忔壒娆″鐓у苟鍔?`--disable_route_intercept`
3. 濡傛灉鍚岀被绔欑偣杩樻槸鎸佺画 timeout锛屽啀鏄惧紡鎸囧畾 `--goto_wait_until domcontentloaded` 鎴?`--goto_wait_until networkidle` 鍋氬皬鎵瑰鐓?
4. 鍐嶈€冭檻鍙斁瀹借秴鏃?
5. 浠ｇ悊淇濇寔鍙€夊紑鍏筹紝涓嶈鐩存帴鏀规垚榛樿寮哄埗寮€鍚?

绀轰緥锛歮alicious

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000
```

濡傛灉浣犺鐩存帴鏀规垚鏄惧紡鐨勬洿瀹芥澗瀵艰埅绛夊緟妯″紡锛?

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000 `
  --goto_wait_until networkidle
```

濡傛灉浣犵湅鍒扮殑鏄?`net::ERR_ABORTED`锛屽厛浼樺厛鍋氳繖涓鐓э細

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --disable_route_intercept
```

绀轰緥锛歜enign

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en `
  --nav_timeout_ms 60000 `
  --proxy_server http://127.0.0.1:7890
```

## English Version

> AI note: GPT, Gemini, Codex, Grok, and Claude must treat this English section as the authoritative version. The Chinese section above is for human readers and quick orientation.

## 1. Purpose

This document is an operational runbook, not an architecture document.
It explains normal day-to-day usage of the current ingest scripts, especially:

- small benign capture runs,
- daily malicious batch capture, especially a roughly 300-URL batch,
- post-capture cluster / pool / review / exclusion generation,
- common Windows pitfalls.

## 2. Relevant Scripts

- benign capture entry: `scripts/data/benign/run_benign_capture.py`
- malicious public-feed ingest: `scripts/data/malicious/ingest_public_malicious_feeds.py`
- malicious capture entry: `scripts/data/malicious/run_malicious_capture.py`
- legacy HTML-to-JSON conversion: `scripts/data/maintenance/convert_legacy_html_to_json.py`
- malicious clustering: `scripts/data/malicious/build_malicious_clusters.py`
- train/reserve routing: `scripts/data/malicious/build_malicious_train_pool.py`
- dedup review manifest: `scripts/data/maintenance/build_dedup_review_manifest.py`
- training exclusion list: `scripts/data/maintenance/build_training_exclusion_lists.py`

## 3. Preconditions

- `python` must be available.
- `playwright` must already be installed and usable in the capture environment.
- `playwright-stealth` must already be installed and usable in the capture environment.
- It is simplest to run commands from the repository root.
- Replace all absolute-path placeholders with your real paths before running commands.

Recommended quick checks:

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py --help
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py --help
```

## 4. Suggested Path Convention

Use a separate batch directory for each operational run instead of mixing all temporary artifacts together.

Suggested placeholders:

- `<WARDEN_ROOT>`: for example `E:\Warden`
- `<WARDEN_DATA_ROOT>`: for example `E:\WardenData`
- `<RUN_DATE>`: for example `2026-03-24`
- `<BATCH_NAME>`: for example `daily300`

Current local default contract:

- the runtime data root is `E:\WardenData`
- `E:\Warden\data\README.md` remains repo-local documentation only
- if an older handoff or older command still shows `<WARDEN_ROOT>\data\...`, replace that path with `<WARDEN_DATA_ROOT>\...` when you actually run it

Suggested directories:

- benign input: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\`
- malicious feed intermediates: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\`
- malicious clustering outputs: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\`
- malicious pool outputs: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\`
- malicious review / exclusion outputs: `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_review\` and `<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_exclusions\`
- benign output root: `<WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME>\`
- malicious output root: `<WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>\`

## 5. Common Scenario A: Small Benign Capture

### 5.1 Prepare a UTF-8 URL file

Example path:

`<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt`

One URL per line.

### 5.2 Run the benign capture command

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en
```

### 5.3 Expected outputs

- sample subdirectories under the output root,
- `benign_capture_run.json` under the output root,
- the normal capture-engine files inside each sample directory,
- an additive `ingest_metadata` object inside `meta.json`.

HTML payload note:

- newly captured HTML payloads are stored as JSON wrappers such as `html_rendered.json` and `html_raw.json`
- older sample directories may still contain legacy `.html` files until they are migrated
- use `scripts/data/maintenance/convert_legacy_html_to_json.py` when you need to convert old sample directories

### 5.4 What to do if benign sample count is still short

Do not treat recovery-based second-pass recapture as the default operator workflow.
For the current Warden operator path, if benign sample count is still short after a run, prefer preparing another fresh benign input batch and continuing capture.

In practice this means:

- keep the current batch outputs as they are,
- use supervised benign mode with `skip` if a single site stalls,
- if the final benign count is still not enough, expand with more Tranco batches instead of trying to salvage every missing URL from the interrupted batch.

This keeps the workflow simple and auditable:

- stalled URLs do not block the whole batch,
- operators do not need to classify every failure into timeout / 403 / 404 / partial-leftover buckets before continuing,
- additional benign volume comes from fresh Tranco coverage rather than uncertain second-pass retries.

### 5.5 Supervised benign mode for stuck URLs

The default benign runner still uses one capture subprocess for the full batch.
It switches into supervised mode only when you explicitly enable one of these flags:

- `--interactive_skip`
- `--url_hard_timeout_ms <milliseconds>`

In supervised mode, the benign runner launches one capture worker per URL.
If the current URL gets stuck, type this in the terminal:

```text
skip
```

That aborts only the current URL and continues with the remaining URLs.
If the worker was killed while it was already writing sample files, a partial sample directory may remain under `output_root`.
Current operator guidance is still to continue the batch with `skip`, and if benign volume remains short after the run, add more Tranco input batches rather than treating leftover partial directories as a default recovery workflow.

If you also want a hard ceiling per URL, add:

```powershell
--url_hard_timeout_ms 120000
```

Example:

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000
```

When supervised mode is used, `benign_capture_run.json` records these additive fields:

- `supervised_mode`
- `interactive_skip`
- `url_hard_timeout_ms`
- `all_success`
- `skipped_urls`
- `timed_out_urls`
- `results`

## 6. Common Scenario B: Daily Malicious Batch of Roughly 300 URLs

This is the main operational workflow.

### 6.1 Ingest public malicious feeds

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\ingest_public_malicious_feeds.py `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed
```

Key outputs:

- `malicious_feed_candidates.jsonl`
- `malicious_feed_candidates.txt`
- `malicious_feed_summary.json`

### 6.2 Create a daily-300 manifest

Do not slice JSONL with `Get-Content | Set-Content`.
On Windows, that often injects a BOM into the first line and breaks JSONL parsing.

Use this Python snippet instead:

```powershell
@'
import json
import random
from pathlib import Path

src = Path(r"<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates.jsonl")
dst = Path(r"<WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl")

rows = []
with src.open("r", encoding="utf-8-sig", errors="ignore") as f:
    for line in f:
        text = line.lstrip("\ufeff").strip()
        if not text:
            continue
        rows.append(json.loads(text))

random.seed(12345)
if len(rows) > 300:
    rows = random.sample(rows, 300)

with dst.open("w", encoding="utf-8", newline="\n") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("selected_rows =", len(rows))
print("output =", dst)
'@ | python -
```

If you want a deterministic head-300 instead of random sampling, replace `random.sample(rows, 300)` with `rows[:300]`.

### 6.3 Run the malicious capture

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --feed_manifest <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\malicious_feed_candidates_<BATCH_NAME>.jsonl `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

### 6.4 First artifact to inspect

Inspect:

`<WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>\malicious_capture_run.json`

Key fields:

- `all_success`
- `returncodes`

If `all_success` is `true`, the batch-level capture process succeeded.

### 6.4A Supervised malicious mode for stuck URLs

The default malicious runner still uses the current grouped-subprocess batch mode.
It switches into supervised mode only when you explicitly enable one of these flags:

- `--interactive_skip`
- `--url_hard_timeout_ms <milliseconds>`

In supervised mode, the malicious runner launches one capture worker per URL.
If the current URL gets stuck, type this in the terminal:

```text
skip
```

That aborts only the current malicious URL and continues with the remaining malicious URLs.

If you also want a hard ceiling per URL, add:

```powershell
--url_hard_timeout_ms 120000
```

Unlike the benign recovery path, malicious does not preserve partial leftovers for later recovery.
If the current malicious URL is skipped, times out, or fails, any sample directories newly created during that URL attempt are deleted immediately.

Example:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --disable_route_intercept `
  --interactive_skip `
  --url_hard_timeout_ms 120000 `
  --nav_timeout_ms 60000 `
  --goto_wait_until commit
```

When supervised mode is used, `malicious_capture_run.json` records these additive fields:

- `supervised_mode`
- `interactive_skip`
- `url_hard_timeout_ms`
- `skipped_urls`
- `timed_out_urls`
- `deleted_partial_sample_dirs`
- `results`

Important note:

- In supervised malicious runs, `results[*].status = "success"` only means the child capture process exited with code `0` and was not operator-aborted or hard-timed-out.
- Do not treat supervised `malicious_capture_run.json` as the authoritative malicious sample-count source for later experiments. Authoritative malicious counting must come from discovered sample directories and downstream cluster records.

### 6.5 Build malicious clusters

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_clusters.py `
  --input_roots <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters
```

Outputs:

- `malicious_cluster_records.jsonl`
- `malicious_cluster_summary.json`

### 6.6 Build train/reserve pool decisions

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\build_malicious_train_pool.py `
  --clusters_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool `
  --family_share_cap 0.10
```

Outputs:

- `pool_decisions.jsonl`
- `train_pool_manifest.jsonl`
- `reserve_pool_manifest.jsonl`
- `pool_summary.json`

### 6.7 Build review and exclusion artifacts

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_dedup_review_manifest.py `
  --clusters_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_clusters\malicious_cluster_records.jsonl `
  --pool_decisions_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_review
```

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\build_training_exclusion_lists.py `
  --pool_decisions_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_pool\pool_decisions.jsonl `
  --output_dir <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_exclusions
```

## 7. Common Scenario C: Manual Small Malicious URL Set

If you already have a text file of malicious URLs and do not want to ingest public feeds first:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

### 7.1 PT `verified_online.csv` to URL-only CSV by verification date

If your input is not a public feed but a local PT `verified_online.csv`, and you first want a URL-only CSV filtered by PT confirmation time before later capture, use:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv
```

The script will first prompt for a date such as:

```text
2026/3/27
```

Rules:

- filtering is based on the UTC calendar date of `verification_time`
- the selected range is inclusive of the entered date
- one run writes both:
  - a URL-only CSV with one column: `url`
  - a one-URL-per-line TXT file for direct capture
- the default output directory is `<WARDEN_DATA_ROOT>\processed\pt_csv_exports\`

If you want an explicit output path:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\export_phishtank_verified_urls.py `
  --source_csv C:\Users\20516\Downloads\verified_online.csv `
  --output_csv <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
```

If you do not pass `--output_txt`, the script will create a sibling `.txt` path next to the CSV automatically.

Then run capture directly:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt `
  --source phishtank `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME>
```

That means the full local PT workflow is:

1. `export_phishtank_verified_urls.py`
2. `run_malicious_capture.py --input_path ...`

If you already have an older URL-only CSV without a matching TXT, the fallback helper still exists:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\convert_url_csv_to_txt.py `
  --input_csv <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.csv `
  --output_txt <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\pt_verified_since_2026-03-27_urls.txt
```

### 7.2 Convert legacy sample HTML files to JSON wrappers

If you have older sample directories that still contain legacy `.html` capture artifacts, convert them with:

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\convert_legacy_html_to_json.py `
  --input_roots <WARDEN_DATA_ROOT>\raw\phish <WARDEN_DATA_ROOT>\raw\benign
```

If you want a report only without writing files:

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\convert_legacy_html_to_json.py `
  --input_roots <WARDEN_DATA_ROOT>\raw\phish <WARDEN_DATA_ROOT>\raw\benign `
  --dry_run
```

In this mode the script only reports `would_convert` / `would_overwrite` style counts.
It does not write any JSON files.

If you want to remove the legacy `.html` files after successful conversion:

```powershell
python <WARDEN_ROOT>\scripts\data\maintenance\convert_legacy_html_to_json.py `
  --input_roots <WARDEN_DATA_ROOT>\raw\phish <WARDEN_DATA_ROOT>\raw\benign `
  --delete_original_html
```

If you run the conversion without `--delete_original_html`, the new JSON wrappers are written and the old `.html` files are intentionally kept.

## 8. Files To Inspect After Each Run

- benign: `benign_capture_run.json`
- malicious: `malicious_capture_run.json`
- clustering: `malicious_cluster_summary.json`
- pool routing: `pool_summary.json`
- at least one sample `meta.json`

Key fields to inspect:

- `returncode` / `all_success`
- `ingest_metadata`
- `total_records`
- `train_count` / `reserve_count`
- `family_share_cap`

## 9. Common Problems

### 9.1 `playwright` or `playwright-stealth` import failure

This is an environment problem, not an upper-layer CLI problem.
Fix the runtime environment first, then rerun the capture command.

Typical recovery commands:

```powershell
python -m pip install playwright
python -m pip install playwright-stealth
playwright install
```

### 9.2 JSONL first-line BOM causing `line 1 is not valid JSON`

This usually happens when a JSONL file was sliced with:

```powershell
Get-Content ... | Set-Content ...
```

Preferred fix:

- use the Python snippet above to create the subset manifest,
- do not slice JSONL with shell text piping.

### 9.3 Wrong output root

One of the most common operational mistakes is simply checking the wrong directory because `--output_root` pointed somewhere else than expected.

### 9.4 `Timeout 25000ms exceeded` even though the page seems to open manually

This does not necessarily mean the site is truly unreachable.
The more common cases are:

- the older `page.goto(..., wait_until="load")` criterion was too strict even though the page body was already usable,
- the site is slower on the current IP / region / network path used by the capture environment,
- the capture browser and your manual browser are not using the same network path,
- Google / consent.google may insert a consent or anti-bot front page before the useful content.

The default hardening path is now built in:

- default navigation timeout is `60000ms`,
- default `goto_wait_until` is `commit`,
- the browser waits for `domcontentloaded` plus a short hydration delay after navigation,
- Google domains attempt consent handling automatically,
- stealth is applied by default on page creation.

The current runners and capture script still support these optional flags:

- `--nav_timeout_ms`
- `--proxy_server`
- `--proxy_username`
- `--proxy_password`
- `--disable_route_intercept`
- `--goto_wait_until`

Recommended order of operations:

1. first retry with the new built-in defaults before adding more overrides,
2. if the failure is `net::ERR_ABORTED` while waiting for `commit`, first run a tiny comparison batch with `--disable_route_intercept`,
3. if timeouts still cluster on the same sites, explicitly test `--goto_wait_until domcontentloaded` or `--goto_wait_until networkidle` on a small batch,
4. only then extend timeouts further if needed,
5. keep proxy usage optional instead of switching the whole pipeline to proxy-by-default.

Example: malicious

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000
```

If you want to force an even looser navigation mode directly:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --nav_timeout_ms 60000 `
  --goto_wait_until networkidle
```

If the specific failure is `net::ERR_ABORTED`, try this before changing more knobs:

```powershell
python <WARDEN_ROOT>\scripts\data\malicious\run_malicious_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_malicious_feed\manual_urls.txt `
  --source manual_malicious `
  --output_root <WARDEN_DATA_ROOT>\raw\phish\<RUN_DATE>_<BATCH_NAME> `
  --disable_route_intercept
```

Example: benign

```powershell
python <WARDEN_ROOT>\scripts\data\benign\run_benign_capture.py `
  --input_path <WARDEN_DATA_ROOT>\processed\<RUN_DATE>_benign\benign_urls.txt `
  --output_root <WARDEN_DATA_ROOT>\raw\benign\<RUN_DATE>_<BATCH_NAME> `
  --source manual_benign `
  --rank_bucket manual_batch `
  --page_type homepage `
  --language en `
  --nav_timeout_ms 60000 `
  --proxy_server http://127.0.0.1:7890
```

## 10. Minimal Daily Command Checklist

### Daily malicious batch of about 300 URLs

1. `ingest_public_malicious_feeds.py`
2. Python snippet to create a 300-row manifest
3. `run_malicious_capture.py`
4. `build_malicious_clusters.py`
5. `build_malicious_train_pool.py`
6. `build_dedup_review_manifest.py`
7. `build_training_exclusion_lists.py`

### Occasional benign batch

1. prepare `benign_urls.txt`
2. `run_benign_capture.py`
3. inspect `benign_capture_run.json`

