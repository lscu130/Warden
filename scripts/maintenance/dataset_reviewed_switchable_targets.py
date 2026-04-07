import json
import logging
import shutil
import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Optional

try:
    from PIL import Image, ImageTk, ImageOps
except ImportError:
    raise SystemExit("缺少 Pillow，请先安装：pip install pillow")


# ============================================================
# 模块 1：全局配置
# 作用：
# - 统一管理脚本中的固定参数
# - 便于后续调整文件名、状态文件名、日志文件名、缩放参数
# ============================================================

IMAGE_NAME = "screenshot_full.png"
REMOVED_DIR_NAME = "removed"
STATE_FILE_NAME = ".review_state.json"
LOG_FILE_NAME = "review_actions.log"
TARGETS_FILE_NAME = ".review_targets.json"

DEFAULT_WINDOW_SIZE = "1500x980"
MIN_WINDOW_SIZE = (1180, 780)

ZOOM_STEP = 1.2
MIN_ZOOM = 0.2
MAX_ZOOM = 6.0
MAX_RECENT_TARGETS = 12
IMAGE_CACHE_LIMIT = 3
PRELOAD_AHEAD_COUNT = 1
REDRAW_DEBOUNCE_MS = 60

STATE_SESSION_KEY = "__dataset_reviewer_session__"
STATE_SAMPLES_KEY = "__dataset_reviewer_samples__"

try:
    RESAMPLE_FILTER = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_FILTER = Image.LANCZOS


# ============================================================
# 模块 2：数据结构定义
# 作用：
# - SampleRecord：描述一个样本目录及其审阅状态
# - ActionRecord：记录一步操作，供“撤销上一步”使用
# ============================================================

@dataclass
class SampleRecord:
    key: str
    original_dir: Path
    current_dir: Path
    image_path: Path
    status: str = "pending"           # pending / kept / removed / conflict_skipped / load_failed / missing_image
    last_error: str = ""


@dataclass
class ActionRecord:
    sample_index: int
    action: str                       # keep / remove / conflict_skip / auto_skip
    previous_status: str
    previous_error: str = ""
    src: Optional[Path] = None
    dst: Optional[Path] = None


# ============================================================
# 模块 3：主应用类
# 作用：
# - 管理 UI、样本扫描、状态持久化、日志记录、图片显示、交互操作
# - 这是整个工具的核心控制器
# ============================================================

class DatasetReviewerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Dataset 无效样本筛除工具 v3")
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)

        # 当前选择的数据集根目录
        self.dataset_root: Optional[Path] = None
        self.removed_root: Optional[Path] = None
        self.state_file: Optional[Path] = None
        self.log_file: Optional[Path] = None
        self.targets_file: Optional[Path] = None

        # 当前分离目标目录与历史目标目录
        self.current_target_root: Optional[Path] = None
        self.recent_target_roots: List[Path] = []

        # 所有样本
        self.samples: List[SampleRecord] = []
        self.history: List[ActionRecord] = []

        # 当前视图位置（注意：这是“当前可见列表”里的位置，不是 samples 原始索引）
        self.current_visible_pos: int = 0
        self.current_sample_index: Optional[int] = None

        # 当前图像缓存
        # 为了控制内存，只保留“当前这一张”的原始 PIL 图和当前显示用 PhotoImage
        self.current_pil_image: Optional[Image.Image] = None
        self.current_photo = None
        self.current_render_key = None
        self.zoom_factor: float = 1.0

        # 状态缓存与日志对象
        self.state_cache: Dict[str, Dict[str, str]] = {}
        self.session_state: Dict[str, object] = {}
        self.logger: Optional[logging.Logger] = None
        self.image_cache: Dict[str, Image.Image] = {}
        self.image_cache_order: List[str] = []
        self.redraw_after_id = None
        self.preload_after_id = None

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._handle_close)

    # ========================================================
    # 模块 4：界面构建
    # 作用：
    # - 创建目录选择、信息栏、图片画布、滚动条、操作按钮、缩放按钮、过滤开关
    # ========================================================

    def _build_ui(self):
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")

        self.select_btn = ttk.Button(top_frame, text="选择数据库根目录", command=self.choose_root_folder)
        self.select_btn.pack(side="left")

        self.root_path_var = tk.StringVar(value="尚未选择目录")
        ttk.Label(top_frame, textvariable=self.root_path_var).pack(side="left", padx=12)

        self.pending_only_var = tk.BooleanVar(value=True)
        self.pending_only_check = ttk.Checkbutton(
            top_frame,
            text="仅看未处理样本",
            variable=self.pending_only_var,
            command=self.refresh_view_after_filter_change
        )
        self.pending_only_check.pack(side="right")

        # 分离目标目录控制：允许在审阅过程中实时切换不同文件夹
        target_frame = ttk.Frame(self.root, padding=(10, 0, 10, 0))
        target_frame.pack(fill="x")

        ttk.Label(target_frame, text="当前分离目标：").pack(side="left")

        self.target_choice_var = tk.StringVar(value="")
        self.target_combo = ttk.Combobox(
            target_frame,
            textvariable=self.target_choice_var,
            state="normal",
            width=55
        )
        self.target_combo.pack(side="left", padx=(0, 6))
        self.target_combo.bind("<<ComboboxSelected>>", lambda event: self.apply_target_from_input())
        self.target_combo.bind("<Return>", lambda event: self.apply_target_from_input())

        self.apply_target_btn = ttk.Button(
            target_frame,
            text="应用目标",
            command=self.apply_target_from_input,
            state="disabled"
        )
        self.apply_target_btn.pack(side="left", padx=4)

        self.pick_target_btn = ttk.Button(
            target_frame,
            text="选择/新建目标目录",
            command=self.choose_target_folder,
            state="disabled"
        )
        self.pick_target_btn.pack(side="left", padx=4)

        self.target_path_var = tk.StringVar(value="目标目录：尚未选择")
        ttk.Label(target_frame, textvariable=self.target_path_var).pack(side="left", padx=10)

        info_frame = ttk.Frame(self.root, padding=(10, 0, 10, 0))
        info_frame.pack(fill="x")

        self.name_var = tk.StringVar(value="样本文件夹：-")
        self.progress_var = tk.StringVar(value="进度：0 / 0")
        self.status_var = tk.StringVar(value="状态：请先选择数据库根目录")
        self.summary_var = tk.StringVar(value="")

        ttk.Label(info_frame, textvariable=self.name_var, font=("Arial", 12, "bold")).pack(anchor="w")
        ttk.Label(info_frame, textvariable=self.progress_var).pack(anchor="w", pady=(4, 0))
        ttk.Label(info_frame, textvariable=self.status_var).pack(anchor="w", pady=(4, 0))
        ttk.Label(info_frame, textvariable=self.summary_var).pack(anchor="w", pady=(4, 8))

        image_outer = ttk.Frame(self.root, padding=10)
        image_outer.pack(fill="both", expand=True)

        # 画布与滚动条：用于显示图片和缩放后滚动浏览
        self.canvas = tk.Canvas(image_outer, bg="#1e1e1e", highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(image_outer, orient="vertical", command=self.canvas.yview)
        self.h_scroll = ttk.Scrollbar(image_outer, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        image_outer.rowconfigure(0, weight=1)
        image_outer.columnconfigure(0, weight=1)

        # 拖动画布浏览
        self.canvas.bind("<ButtonPress-1>", self._start_pan)
        self.canvas.bind("<B1-Motion>", self._do_pan)
        self.canvas.bind("<Configure>", lambda event: self._schedule_redraw_current_image())

        # 鼠标滚轮：普通滚动用于上下浏览；Ctrl+滚轮用于缩放
        self.canvas.bind("<MouseWheel>", self._on_mousewheel_windows)
        self.canvas.bind("<Control-MouseWheel>", self._on_ctrl_mousewheel_windows)
        self.canvas.bind("<Button-4>", self._on_mousewheel_linux_up)
        self.canvas.bind("<Button-5>", self._on_mousewheel_linux_down)
        self.canvas.bind("<Control-Button-4>", self._on_ctrl_mousewheel_linux_up)
        self.canvas.bind("<Control-Button-5>", self._on_ctrl_mousewheel_linux_down)

        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.pack(fill="x")

        self.remove_btn = ttk.Button(bottom_frame, text="移除", command=self.remove_current, state="disabled")
        self.remove_btn.pack(side="left", padx=4)

        self.keep_btn = ttk.Button(bottom_frame, text="保留", command=self.keep_current, state="disabled")
        self.keep_btn.pack(side="left", padx=4)

        self.undo_btn = ttk.Button(
            bottom_frame,
            text="上一张 / 撤销上一步",
            command=self.undo_last,
            state="disabled"
        )
        self.undo_btn.pack(side="left", padx=4)

        ttk.Separator(bottom_frame, orient="vertical").pack(side="left", fill="y", padx=8)

        self.zoom_in_btn = ttk.Button(bottom_frame, text="放大", command=self.zoom_in, state="disabled")
        self.zoom_in_btn.pack(side="left", padx=4)

        self.zoom_out_btn = ttk.Button(bottom_frame, text="缩小", command=self.zoom_out, state="disabled")
        self.zoom_out_btn.pack(side="left", padx=4)

        self.zoom_reset_btn = ttk.Button(bottom_frame, text="重置缩放", command=self.reset_zoom, state="disabled")
        self.zoom_reset_btn.pack(side="left", padx=4)

    # ========================================================
    # 模块 6：目录选择、状态文件、日志初始化
    # 作用：
    # - 选择根目录
    # - 创建 removed 目录
    # - 加载持久化状态
    # - 初始化日志文件
    # ========================================================

    def choose_root_folder(self):
        folder = filedialog.askdirectory(title="选择数据库根目录")
        if not folder:
            return

        self.dataset_root = Path(folder)
        self.removed_root = self.dataset_root / REMOVED_DIR_NAME
        self.state_file = self.dataset_root / STATE_FILE_NAME
        self.log_file = self.dataset_root / LOG_FILE_NAME
        self.targets_file = self.dataset_root / TARGETS_FILE_NAME

        self.removed_root.mkdir(exist_ok=True)
        self.root_path_var.set(str(self.dataset_root))
        self.samples = []
        self.history.clear()

        self._setup_logger()
        self.state_cache = self._load_state_file()

        self._load_target_history()
        self._restore_saved_target_root()

        self.status_var.set("状态：正在扫描样本目录...")
        self.root.update_idletasks()

        self.samples = self.scan_samples(self.dataset_root)
        self.history.clear()
        self._clear_runtime_image_state()
        self._restore_session_view_state()

        enabled = "normal" if self.samples else "disabled"
        self.remove_btn.config(state=enabled)
        self.keep_btn.config(state=enabled)
        self.zoom_in_btn.config(state=enabled)
        self.zoom_out_btn.config(state=enabled)
        self.zoom_reset_btn.config(state=enabled)
        self.undo_btn.config(state="disabled")
        self.apply_target_btn.config(state="normal")
        self.pick_target_btn.config(state="normal")

        self.show_current_sample()

    def _setup_logger(self):
        if self.log_file is None:
            return

        logger = logging.getLogger("dataset_reviewer")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        logger.propagate = False

        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        self.logger = logger
        self.logger.info("===== 打开数据集目录：%s =====", self.dataset_root)

    def _load_state_file(self) -> Dict[str, Dict[str, str]]:
        self.session_state = {}

        if self.state_file is None or not self.state_file.exists():
            return {}

        try:
            with self.state_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    samples = data.get(STATE_SAMPLES_KEY)
                    session = data.get(STATE_SESSION_KEY)
                    if isinstance(samples, dict):
                        if isinstance(session, dict):
                            self.session_state = session
                        return {k: v for k, v in samples.items() if isinstance(v, dict)}
                    if isinstance(session, dict):
                        self.session_state = session
                    return {
                        k: v
                        for k, v in data.items()
                        if k not in (STATE_SESSION_KEY, STATE_SAMPLES_KEY) and isinstance(v, dict)
                    }
        except Exception as e:
            messagebox.showwarning("状态文件读取失败", f"将忽略旧状态文件：\n{e}")
        return {}

    def _save_state_file(self):
        if self.state_file is None:
            return

        data = {}
        for sample in self.samples:
            data[sample.key] = {
                "status": sample.status,
                "last_error": sample.last_error,
                "updated_at": datetime.now().isoformat(timespec="seconds"),
            }

        with self.state_file.open("w", encoding="utf-8") as f:
            payload = dict(data)
            payload[STATE_SESSION_KEY] = self._build_session_state()
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def _build_session_state(self) -> Dict[str, object]:
        current_sample_key = ""
        sample_index = self._get_current_sample_index()
        if sample_index is not None:
            current_sample_key = self.samples[sample_index].key

        return {
            "current_sample_key": current_sample_key,
            "current_visible_pos": self.current_visible_pos,
            "pending_only": bool(self.pending_only_var.get()),
            "current_target_root": str(self.current_target_root) if self.current_target_root else "",
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }

    # ========================================================
    # 模块 6.1：分离目标目录管理
    # 作用：
    # - 支持实时切换不同的分离目标目录
    # - 记住最近使用的目录
    # - 避免位于数据集根目录内的分离目录被重新扫描成样本
    # ========================================================

    def _load_target_history(self):
        self.recent_target_roots = []

        if self.dataset_root is None:
            return

        default_target = self.dataset_root / REMOVED_DIR_NAME
        loaded_paths: List[Path] = []

        if self.targets_file is not None and self.targets_file.exists():
            try:
                with self.targets_file.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, str) and item.strip():
                            loaded_paths.append(Path(item))
            except Exception as e:
                messagebox.showwarning("目标目录历史读取失败", f"将忽略旧目标目录历史：\n{e}")

        normalized: List[Path] = []
        seen = set()
        for path in [default_target] + loaded_paths:
            resolved = self._resolve_target_input(str(path), create=False)
            if resolved is None:
                continue
            key = str(resolved).lower()
            if key in seen:
                continue
            seen.add(key)
            normalized.append(resolved)

        self.recent_target_roots = normalized[:MAX_RECENT_TARGETS]
        self._refresh_target_combo_values()
        self._save_target_history()

    def _save_target_history(self):
        if self.targets_file is None:
            return

        serializable = [str(path) for path in self.recent_target_roots[:MAX_RECENT_TARGETS]]
        with self.targets_file.open("w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)

    def _refresh_target_combo_values(self):
        values = [self._display_target_path(path) for path in self.recent_target_roots]
        self.target_combo["values"] = values

    def _display_target_path(self, path: Path) -> str:
        if self.dataset_root is None:
            return str(path)
        try:
            return str(path.relative_to(self.dataset_root)).replace("\\", "/")
        except ValueError:
            return str(path)

    def _resolve_target_input(self, user_value: str, create: bool = False) -> Optional[Path]:
        if self.dataset_root is None:
            return None

        value = (user_value or "").strip()
        if not value:
            return self.dataset_root / REMOVED_DIR_NAME

        raw_path = Path(value)
        if not raw_path.is_absolute():
            raw_path = (self.dataset_root / raw_path).resolve()
        else:
            raw_path = raw_path.resolve()

        if create:
            raw_path.mkdir(parents=True, exist_ok=True)

        return raw_path

    def _register_target_root(self, target_root: Path):
        normalized = target_root.resolve()
        lower_key = str(normalized).lower()

        self.recent_target_roots = [
            p for p in self.recent_target_roots if str(p.resolve()).lower() != lower_key
        ]
        self.recent_target_roots.insert(0, normalized)
        self.recent_target_roots = self.recent_target_roots[:MAX_RECENT_TARGETS]
        self._refresh_target_combo_values()
        self._save_target_history()

    def _set_current_target(self, target_root: Path, save_history: bool = True):
        resolved = target_root.resolve()
        resolved.mkdir(parents=True, exist_ok=True)
        self.current_target_root = resolved

        display = self._display_target_path(resolved)
        self.target_choice_var.set(display)
        self.target_path_var.set(f"目标目录：{resolved}")

        if save_history:
            self._register_target_root(resolved)

        if self.logger:
            self.logger.info("SET_TARGET | target=%s", resolved)

        if self.samples:
            self._save_state_file()

    def _restore_saved_target_root(self):
        saved_target = self.session_state.get("current_target_root")
        target_root = None

        if isinstance(saved_target, str) and saved_target.strip():
            target_root = self._resolve_target_input(saved_target, create=True)

        if target_root is None:
            target_root = self.removed_root

        if target_root is not None:
            self._set_current_target(target_root, save_history=True)

    def _restore_session_view_state(self):
        pending_only = self.session_state.get("pending_only")
        if isinstance(pending_only, bool):
            self.pending_only_var.set(pending_only)

        visible = self.get_visible_indices()
        saved_key = self.session_state.get("current_sample_key")

        if isinstance(saved_key, str) and saved_key:
            for sample_index, sample in enumerate(self.samples):
                if sample.key != saved_key:
                    continue
                if sample_index in visible:
                    self.current_visible_pos = visible.index(sample_index)
                    return
                break

        saved_pos = self.session_state.get("current_visible_pos")
        if visible and isinstance(saved_pos, int):
            self.current_visible_pos = max(0, min(saved_pos, len(visible) - 1))
        else:
            self.current_visible_pos = 0

    def apply_target_from_input(self):
        if self.dataset_root is None:
            messagebox.showwarning("尚未选择根目录", "请先选择数据库根目录。")
            return

        target_root = self._resolve_target_input(self.target_choice_var.get(), create=True)
        if target_root is None:
            return

        self._set_current_target(target_root, save_history=True)
        self.status_var.set(f"状态：当前分离目标已切换到 {target_root}")

    def choose_target_folder(self):
        if self.dataset_root is None:
            messagebox.showwarning("尚未选择根目录", "请先选择数据库根目录。")
            return

        initial_dir = str(self.current_target_root or self.removed_root or self.dataset_root)
        folder = filedialog.askdirectory(title="选择分离目标目录", initialdir=initial_dir, mustexist=False)
        if not folder:
            return

        target_root = Path(folder).resolve()
        target_root.mkdir(parents=True, exist_ok=True)
        self._set_current_target(target_root, save_history=True)
        self.status_var.set(f"状态：当前分离目标已切换到 {target_root}")

    def _is_inside_any_managed_target_root(self, path: Path) -> bool:
        candidate = path.resolve()
        for target_root in self.recent_target_roots:
            try:
                candidate.relative_to(target_root)
                return True
            except ValueError:
                continue
        return False

    # ========================================================
    # 模块 7：样本扫描
    # 作用：
    # - 递归查找 screenshot_full.png
    # - 每个找到的图片，其父目录视为一个样本目录
    # - 自动跳过 removed 目录和所有已登记的分离目标目录
    # - 载入上次保存的状态
    # ========================================================

    def scan_samples(self, root_dir: Path) -> List[SampleRecord]:
        samples: List[SampleRecord] = []
        seen_dirs = set()

        for image_path in root_dir.rglob(IMAGE_NAME):
            if self._is_inside_any_managed_target_root(image_path):
                continue

            sample_dir = image_path.parent
            if sample_dir in seen_dirs:
                continue
            seen_dirs.add(sample_dir)

            key = str(sample_dir.relative_to(root_dir)).replace("\\", "/")
            saved = self.state_cache.get(key, {})
            status = saved.get("status", "pending")
            last_error = saved.get("last_error", "")

            samples.append(
                SampleRecord(
                    key=key,
                    original_dir=sample_dir,
                    current_dir=sample_dir,
                    image_path=image_path,
                    status=status,
                    last_error=last_error,
                )
            )

        samples.sort(key=lambda s: s.key.lower())
        return samples

    # ========================================================
    # 模块 8：过滤与统计
    # 作用：
    # - 根据“仅看未处理样本”开关生成可见样本列表
    # - 计算保留/移除/失败/待处理等统计信息
    # ========================================================

    def get_visible_indices(self) -> List[int]:
        if self.pending_only_var.get():
            return [i for i, s in enumerate(self.samples) if s.status == "pending"]
        return list(range(len(self.samples)))

    def update_summary(self):
        total = len(self.samples)
        visible = len(self.get_visible_indices())

        pending = sum(1 for s in self.samples if s.status == "pending")
        kept = sum(1 for s in self.samples if s.status == "kept")
        removed = sum(1 for s in self.samples if s.status == "removed")
        conflict = sum(1 for s in self.samples if s.status == "conflict_skipped")
        failed = sum(1 for s in self.samples if s.status in ("load_failed", "missing_image"))

        self.summary_var.set(
            f"总数: {total}  当前视图: {visible}  待处理: {pending}  保留: {kept}  "
            f"移除: {removed}  冲突跳过: {conflict}  自动跳过: {failed}"
        )

    def refresh_view_after_filter_change(self):
        current_idx = self.current_sample_index
        visible = self.get_visible_indices()

        if not visible:
            self.current_visible_pos = 0
            self.show_current_sample()
            return

        if current_idx is not None and current_idx in visible:
            self.current_visible_pos = visible.index(current_idx)
        else:
            self.current_visible_pos = min(self.current_visible_pos, len(visible) - 1)

        self.show_current_sample()

    # ========================================================
    # 模块 9：图片加载与自动跳过异常样本
    # 作用：
    # - 只加载“当前这张图”，避免一次性吃太多内存
    # - 如果缺图或图片损坏，自动记日志、改状态、跳过到下一条
    # ========================================================

    def show_current_sample(self):
        self.update_summary()

        visible = self.get_visible_indices()

        if not self.samples:
            self._show_empty_message("没有找到任何样本")
            self.status_var.set("状态：目录中未发现可审阅样本")
            return

        if not visible:
            msg = "没有符合当前过滤条件的样本"
            if self.pending_only_var.get():
                msg = "未处理样本已全部审阅完毕"
            self._show_empty_message(msg)
            self.status_var.set("状态：当前视图为空")
            return

        if self.current_visible_pos < 0:
            self.current_visible_pos = 0

        if self.current_visible_pos >= len(visible):
            self._show_empty_message("当前视图已到末尾")
            self.status_var.set("状态：当前视图已到末尾")
            self.progress_var.set(f"进度：{len(visible)} / {len(visible)}")
            self.name_var.set("样本文件夹：-")
            return

        while True:
            visible = self.get_visible_indices()
            if not visible:
                self._show_empty_message("未处理样本已全部审阅完毕")
                self.status_var.set("状态：当前视图为空")
                return

            if self.current_visible_pos >= len(visible):
                self._show_empty_message("当前视图已到末尾")
                self.status_var.set("状态：当前视图已到末尾")
                self.progress_var.set(f"进度：{len(visible)} / {len(visible)}")
                self.name_var.set("样本文件夹：-")
                return

            sample_index = visible[self.current_visible_pos]
            sample = self.samples[sample_index]

            problem = self._load_current_image(sample)
            if problem is None:
                self.current_sample_index = sample_index
                self.name_var.set(f"样本文件夹：{sample.current_dir.name}")
                self.progress_var.set(f"进度：{self.current_visible_pos + 1} / {len(visible)}")
                self.status_var.set(f"状态：当前样本状态 = {sample.status}")
                self.redraw_current_image()
                self._save_state_file()
                self._schedule_preload()
                self.undo_btn.config(state="normal" if self.history else "disabled")
                return

            # 自动跳过异常样本
            self._auto_skip_sample(sample_index, problem)

    def _load_current_image(self, sample: SampleRecord) -> Optional[str]:
        if not sample.image_path.exists():
            return f"缺少图片文件：{sample.image_path}"

        try:
            cached = self._get_cached_image(sample)
            if cached is None:
                with Image.open(sample.image_path) as img:
                    img = ImageOps.exif_transpose(img)
                    cached = img.convert("RGB").copy()
                self._store_cached_image(sample, cached)

            self.current_pil_image = cached
            self.current_render_key = None
            self.zoom_factor = 1.0
            return None
        except Exception as e:
            return f"图片加载失败：{e}"

    def _auto_skip_sample(self, sample_index: int, reason: str):
        sample = self.samples[sample_index]
        previous_status = sample.status
        previous_error = sample.last_error

        if "缺少图片文件" in reason:
            sample.status = "missing_image"
        else:
            sample.status = "load_failed"

        sample.last_error = reason
        self._save_state_file()

        self.history.append(
            ActionRecord(
                sample_index=sample_index,
                action="auto_skip",
                previous_status=previous_status,
                previous_error=previous_error,
            )
        )

        if self.logger:
            self.logger.warning("AUTO_SKIP | key=%s | reason=%s", sample.key, reason)

        if not self.pending_only_var.get():
            self.current_visible_pos += 1

        self.undo_btn.config(state="normal" if self.history else "disabled")

    # ========================================================
    # 模块 10：图片渲染、缩放、拖拽和平移
    # 作用：
    # - 根据画布大小与缩放倍率渲染当前图片
    # - 提供放大、缩小、重置缩放
    # - 支持拖拽查看放大后的局部区域
    # ========================================================

    def redraw_current_image(self):
        if self.current_pil_image is None:
            self.canvas.delete("all")
            self.current_photo = None
            self.current_render_key = None
            self.canvas.create_text(
                30, 30,
                anchor="nw",
                text="没有可显示的图片",
                fill="white",
                font=("Arial", 14)
            )
            self.canvas.configure(scrollregion=(0, 0, 1, 1))
            return

        canvas_w = max(self.canvas.winfo_width(), 600)
        canvas_h = max(self.canvas.winfo_height(), 400)

        img_w, img_h = self.current_pil_image.size
        if img_w <= 0 or img_h <= 0:
            return

        fit_scale = min(canvas_w / img_w, canvas_h / img_h)
        fit_scale = max(fit_scale, 0.01)

        final_scale = fit_scale * self.zoom_factor
        final_scale = max(MIN_ZOOM * fit_scale, min(MAX_ZOOM * fit_scale, final_scale))

        new_w = max(1, int(img_w * final_scale))
        new_h = max(1, int(img_h * final_scale))

        render_key = (id(self.current_pil_image), new_w, new_h, round(self.zoom_factor, 4))
        if self.current_render_key != render_key or self.current_photo is None:
            display_img = self.current_pil_image.resize((new_w, new_h), RESAMPLE_FILTER)
            self.current_photo = ImageTk.PhotoImage(display_img)
            self.current_render_key = render_key

        x = max((canvas_w - new_w) // 2, 0)
        y = max((canvas_h - new_h) // 2, 0)

        self.canvas.delete("all")
        self.canvas.create_image(x, y, anchor="nw", image=self.current_photo)
        self.canvas.configure(scrollregion=(0, 0, max(canvas_w, new_w), max(canvas_h, new_h)))

    def _schedule_redraw_current_image(self):
        if self.redraw_after_id is not None:
            self.root.after_cancel(self.redraw_after_id)
        self.redraw_after_id = self.root.after(REDRAW_DEBOUNCE_MS, self._run_scheduled_redraw)

    def _run_scheduled_redraw(self):
        self.redraw_after_id = None
        self.redraw_current_image()

    def _image_cache_key(self, sample: SampleRecord) -> str:
        return str(sample.image_path.resolve()).lower()

    def _get_cached_image(self, sample: SampleRecord) -> Optional[Image.Image]:
        cache_key = self._image_cache_key(sample)
        image = self.image_cache.get(cache_key)
        if image is None:
            return None

        if cache_key in self.image_cache_order:
            self.image_cache_order.remove(cache_key)
        self.image_cache_order.append(cache_key)
        return image

    def _store_cached_image(self, sample: SampleRecord, image: Image.Image):
        cache_key = self._image_cache_key(sample)
        self.image_cache[cache_key] = image
        if cache_key in self.image_cache_order:
            self.image_cache_order.remove(cache_key)
        self.image_cache_order.append(cache_key)

        while len(self.image_cache_order) > IMAGE_CACHE_LIMIT:
            expired_key = self.image_cache_order.pop(0)
            self.image_cache.pop(expired_key, None)

    def _schedule_preload(self):
        if self.preload_after_id is not None:
            self.root.after_cancel(self.preload_after_id)
        self.preload_after_id = self.root.after(10, self._preload_adjacent_images)

    def _preload_adjacent_images(self):
        self.preload_after_id = None
        sample_index = self._get_current_sample_index()
        if sample_index is None:
            return

        visible = self.get_visible_indices()
        if sample_index not in visible:
            return

        current_pos = visible.index(sample_index)
        stop_pos = min(len(visible), current_pos + 1 + PRELOAD_AHEAD_COUNT)

        for pos in range(current_pos + 1, stop_pos):
            candidate = self.samples[visible[pos]]
            if self._get_cached_image(candidate) is not None:
                continue
            if not candidate.image_path.exists():
                continue
            try:
                with Image.open(candidate.image_path) as img:
                    img = ImageOps.exif_transpose(img)
                    self._store_cached_image(candidate, img.convert("RGB").copy())
            except Exception:
                continue

    def zoom_in(self):
        if self.current_pil_image is None:
            return
        self.zoom_factor = min(self.zoom_factor * ZOOM_STEP, MAX_ZOOM)
        self.redraw_current_image()

    def zoom_out(self):
        if self.current_pil_image is None:
            return
        self.zoom_factor = max(self.zoom_factor / ZOOM_STEP, MIN_ZOOM)
        self.redraw_current_image()

    def reset_zoom(self):
        if self.current_pil_image is None:
            return
        self.zoom_factor = 1.0
        self.redraw_current_image()

    def _start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def _do_pan(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_mousewheel_windows(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_ctrl_mousewheel_windows(self, event):
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def _on_mousewheel_linux_up(self, event):
        self.canvas.yview_scroll(-1, "units")

    def _on_mousewheel_linux_down(self, event):
        self.canvas.yview_scroll(1, "units")

    def _on_ctrl_mousewheel_linux_up(self, event):
        self.zoom_in()

    def _on_ctrl_mousewheel_linux_down(self, event):
        self.zoom_out()

    # ========================================================
    # 模块 11：保留 / 移除 / 撤销
    # 作用：
    # - 保留：只写状态，不改动目录
    # - 移除：把整个样本目录移动到“当前分离目标目录”下
    # - 撤销：恢复上一步，包括把目标目录中的目录搬回去
    # ========================================================

    def keep_current(self):
        sample_index = self._get_current_sample_index()
        if sample_index is None:
            return

        sample = self.samples[sample_index]
        previous_status = sample.status
        previous_error = sample.last_error

        sample.status = "kept"
        sample.last_error = ""
        self._save_state_file()

        self.history.append(
            ActionRecord(
                sample_index=sample_index,
                action="keep",
                previous_status=previous_status,
                previous_error=previous_error,
            )
        )

        if self.logger:
            self.logger.info("KEEP | key=%s", sample.key)

        self._advance_after_action(sample_index)

    def remove_current(self):
        sample_index = self._get_current_sample_index()
        if sample_index is None or self.current_target_root is None:
            return

        sample = self.samples[sample_index]
        previous_status = sample.status
        previous_error = sample.last_error

        src_dir = sample.current_dir
        dst_dir = self.current_target_root / Path(*sample.key.split("/"))

        if dst_dir.exists():
            sample.status = "conflict_skipped"
            sample.last_error = f"目标目录中已存在同名目录：{dst_dir}"
            self._save_state_file()

            self.history.append(
                ActionRecord(
                    sample_index=sample_index,
                    action="conflict_skip",
                    previous_status=previous_status,
                    previous_error=previous_error,
                )
            )

            if self.logger:
                self.logger.warning("CONFLICT_SKIP | key=%s | dst=%s", sample.key, dst_dir)

            messagebox.showwarning("重名冲突", f"目标目录中已存在同名文件夹，已跳过本次移除：\n{dst_dir}")
            self._advance_after_action(sample_index)
            return

        try:
            dst_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_dir), str(dst_dir))

            sample.status = "removed"
            sample.last_error = ""
            sample.current_dir = dst_dir
            sample.image_path = dst_dir / IMAGE_NAME
            self._save_state_file()

            self.history.append(
                ActionRecord(
                    sample_index=sample_index,
                    action="remove",
                    previous_status=previous_status,
                    previous_error=previous_error,
                    src=src_dir,
                    dst=dst_dir,
                )
            )

            if self.logger:
                self.logger.info(
                    "REMOVE | key=%s | src=%s | dst=%s | target_root=%s",
                    sample.key, src_dir, dst_dir, self.current_target_root
                )

            self._advance_after_action(sample_index)

        except Exception as e:
            messagebox.showerror("移除失败", f"移动文件夹失败：\n{e}")
            if self.logger:
                self.logger.error("REMOVE_FAIL | key=%s | error=%s", sample.key, e)

    def undo_last(self):
        if not self.history:
            return

        action = self.history.pop()
        sample = self.samples[action.sample_index]

        try:
            if action.action in ("keep", "conflict_skip", "auto_skip"):
                sample.status = action.previous_status
                sample.last_error = action.previous_error

                if self.logger:
                    self.logger.info("UNDO_%s | key=%s", action.action.upper(), sample.key)

            elif action.action == "remove":
                if action.src is None or action.dst is None:
                    raise RuntimeError("撤销记录不完整，无法恢复")

                if action.src.exists():
                    raise RuntimeError(f"原路径已存在，无法撤销：{action.src}")

                if not action.dst.exists():
                    raise RuntimeError(f"目标目录中的样本不存在，无法撤销：{action.dst}")

                shutil.move(str(action.dst), str(action.src))
                sample.status = action.previous_status
                sample.last_error = action.previous_error
                sample.current_dir = action.src
                sample.image_path = action.src / IMAGE_NAME

                if self.logger:
                    self.logger.info("UNDO_REMOVE | key=%s | restore_to=%s", sample.key, action.src)

            self._save_state_file()
            self._focus_sample(action.sample_index)
            self.undo_btn.config(state="normal" if self.history else "disabled")

        except Exception as e:
            messagebox.showerror("撤销失败", str(e))
            if self.logger:
                self.logger.error("UNDO_FAIL | key=%s | error=%s", sample.key, e)

    def _advance_after_action(self, processed_index: int):
        if not self.pending_only_var.get():
            visible = self.get_visible_indices()
            if processed_index in visible:
                self.current_visible_pos = visible.index(processed_index) + 1

        self.undo_btn.config(state="normal" if self.history else "disabled")
        self.show_current_sample()

    def _focus_sample(self, sample_index: int):
        visible = self.get_visible_indices()

        if not visible:
            self.current_visible_pos = 0
            self.show_current_sample()
            return

        if sample_index in visible:
            self.current_visible_pos = visible.index(sample_index)
        else:
            self.current_visible_pos = min(self.current_visible_pos, len(visible) - 1)

        self.show_current_sample()

    def _get_current_sample_index(self) -> Optional[int]:
        if self.current_sample_index is None:
            return None
        if self.current_sample_index < 0 or self.current_sample_index >= len(self.samples):
            return None
        return self.current_sample_index

    # ========================================================
    # 模块 12：空视图提示
    # 作用：
    # - 当当前过滤结果为空或已到末尾时，在画布上给出明确提示
    # ========================================================

    def _show_empty_message(self, message: str):
        self.current_sample_index = None
        self.current_pil_image = None
        self.current_photo = None
        self.current_render_key = None

        self.name_var.set("样本文件夹：-")
        self.progress_var.set("进度：0 / 0")
        self.update_summary()

        self.canvas.delete("all")
        self.canvas.configure(scrollregion=(0, 0, 1, 1))
        self.canvas.create_text(
            30, 30,
            anchor="nw",
            text=message,
            fill="white",
            font=("Arial", 16)
        )

        if self.samples:
            self._save_state_file()

    def _clear_runtime_image_state(self):
        self.current_visible_pos = 0
        self.current_sample_index = None
        self.current_pil_image = None
        self.current_photo = None
        self.current_render_key = None
        self.zoom_factor = 1.0
        self.image_cache.clear()
        self.image_cache_order.clear()

        if self.preload_after_id is not None:
            self.root.after_cancel(self.preload_after_id)
            self.preload_after_id = None

        if self.redraw_after_id is not None:
            self.root.after_cancel(self.redraw_after_id)
            self.redraw_after_id = None

    def _handle_close(self):
        if self.samples:
            self._save_state_file()
        self.root.destroy()

    # ========================================================
    # 模块 13：主循环入口
    # 作用：
    # - 启动整个桌面程序
    # ========================================================

    def run(self):
        self.root.mainloop()


# ============================================================
# 模块 14：程序入口
# 作用：
# - 初始化 Tk 根窗口并启动应用
# ============================================================

def main():
    root = tk.Tk()
    app = DatasetReviewerApp(root)
    app.run()


if __name__ == "__main__":
    main()
