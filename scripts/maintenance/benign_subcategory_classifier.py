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
# - 规定截图读取优先级：优先看 screenshot_viewport.png，缺失才回退到 screenshot_full.png
# - 规定状态、日志、目标历史文件名，便于后续维护
# ============================================================

VIEWPORT_IMAGE_NAME = "screenshot_viewport.png"
FALLBACK_IMAGE_NAME = "screenshot_full.png"
IMAGE_NAME_PRIORITY = (VIEWPORT_IMAGE_NAME, FALLBACK_IMAGE_NAME)
DEFAULT_CLASSIFIED_DIR_NAME = "benign_classified"
STATE_FILE_NAME = ".benign_subcategory_state.json"
LOG_FILE_NAME = "benign_subcategory_actions.log"
TARGETS_FILE_NAME = ".benign_subcategory_targets.json"

DEFAULT_WINDOW_SIZE = "1600x980"
MIN_WINDOW_SIZE = (1250, 780)

ZOOM_STEP = 1.2
MIN_ZOOM = 0.2
MAX_ZOOM = 6.0
MAX_RECENT_TARGETS = 12
IMAGE_CACHE_LIMIT = 3
PRELOAD_AHEAD_COUNT = 1
REDRAW_DEBOUNCE_MS = 60
CATEGORY_BUTTON_WRAP = 2
CATEGORY_LABEL_LIMIT = 24

STATE_SESSION_KEY = "__benign_subcategory_session__"
STATE_SAMPLES_KEY = "__benign_subcategory_samples__"

try:
    RESAMPLE_FILTER = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE_FILTER = Image.LANCZOS


# ============================================================
# 模块 2：数据结构定义
# 作用：
# - SampleRecord：描述一个待分类样本目录及其当前状态
# - ActionRecord：记录一步分类/跳过/冲突操作，供“撤销上一步”使用
# - CategoryRecord：描述一个分类目标子文件夹及其按钮展示文本
# ============================================================

@dataclass
class SampleRecord:
    key: str
    original_dir: Path
    current_dir: Path
    image_path: Path
    image_name: str
    status: str = "pending"            # pending / classified / skipped / conflict_skipped / load_failed / missing_image
    category: str = ""
    last_error: str = ""


@dataclass
class ActionRecord:
    sample_index: int
    action: str                         # classify / skip / conflict_skip / auto_skip
    previous_status: str
    previous_category: str = ""
    previous_error: str = ""
    src: Optional[Path] = None
    dst: Optional[Path] = None


@dataclass
class CategoryRecord:
    name: str
    path: Path
    label: str


# ============================================================
# 模块 3：主应用类
# 作用：
# - 管理 UI、样本扫描、分类目标目录、状态持久化、日志记录、图片显示、交互操作
# - 这是整个 benign 细类划分工具的核心控制器
# ============================================================

class BenignSubcategoryClassifierApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Benign 细类划分工具 v1")
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        self.root.minsize(*MIN_WINDOW_SIZE)

        # 当前选择的待分类根目录
        self.dataset_root: Optional[Path] = None
        self.state_file: Optional[Path] = None
        self.log_file: Optional[Path] = None
        self.targets_file: Optional[Path] = None

        # 当前分类输出根目录与历史目录
        self.current_target_root: Optional[Path] = None
        self.recent_target_roots: List[Path] = []
        self.categories: List[CategoryRecord] = []
        self.category_buttons: List[ttk.Button] = []

        # 样本与操作历史
        self.samples: List[SampleRecord] = []
        self.history: List[ActionRecord] = []
        self.current_visible_pos: int = 0
        self.current_sample_index: Optional[int] = None

        # 图片显示状态
        self.current_pil_image: Optional[Image.Image] = None
        self.current_photo = None
        self.current_render_key = None
        self.zoom_factor: float = 1.0
        self.image_cache: Dict[str, Image.Image] = {}
        self.image_cache_order: List[str] = []
        self.redraw_after_id = None
        self.preload_after_id = None

        # 状态缓存与日志对象
        self.state_cache: Dict[str, Dict[str, str]] = {}
        self.session_state: Dict[str, object] = {}
        self.logger: Optional[logging.Logger] = None

        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._handle_close)

    # ========================================================
    # 模块 4：界面构建
    # 作用：
    # - 顶部：选择需要分类的目标文件夹，保持原脚本顶部选择逻辑
    # - 中部左侧：显示 screenshot_viewport.png；没有 viewport 时回退 full
    # - 中部右侧上方：选择分类后的文件夹，并按其子文件夹自动生成分类按钮
    # - 中部右侧下方：显示分类进度、当前样本状态、跳过与撤销控制
    # ========================================================

    def _build_ui(self):
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")

        self.select_btn = ttk.Button(top_frame, text="选择需要分类的目标文件夹", command=self.choose_root_folder)
        self.select_btn.pack(side="left")

        self.root_path_var = tk.StringVar(value="尚未选择目录")
        ttk.Label(top_frame, textvariable=self.root_path_var).pack(side="left", padx=12)

        self.pending_only_var = tk.BooleanVar(value=True)
        self.pending_only_check = ttk.Checkbutton(
            top_frame,
            text="仅看未分类样本",
            variable=self.pending_only_var,
            command=self.refresh_view_after_filter_change
        )
        self.pending_only_check.pack(side="right")

        self.main_paned = ttk.Panedwindow(self.root, orient="horizontal")
        self.main_paned.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.left_frame = ttk.Frame(self.main_paned)
        self.right_frame = ttk.Frame(self.main_paned, width=420)
        self.main_paned.add(self.left_frame, weight=4)
        self.main_paned.add(self.right_frame, weight=1)

        self._build_image_panel(self.left_frame)
        self._build_control_panel(self.right_frame)

    def _build_image_panel(self, parent: ttk.Frame):
        info_frame = ttk.Frame(parent, padding=(0, 0, 0, 8))
        info_frame.pack(fill="x")

        self.name_var = tk.StringVar(value="样本文件夹：-")
        self.image_source_var = tk.StringVar(value="截图来源：-")
        ttk.Label(info_frame, textvariable=self.name_var, font=("Arial", 12, "bold")).pack(anchor="w")
        ttk.Label(info_frame, textvariable=self.image_source_var).pack(anchor="w", pady=(4, 0))

        image_outer = ttk.Frame(parent)
        image_outer.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(image_outer, bg="#1e1e1e", highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(image_outer, orient="vertical", command=self.canvas.yview)
        self.h_scroll = ttk.Scrollbar(image_outer, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        image_outer.rowconfigure(0, weight=1)
        image_outer.columnconfigure(0, weight=1)

        self.canvas.bind("<ButtonPress-1>", self._start_pan)
        self.canvas.bind("<B1-Motion>", self._do_pan)
        self.canvas.bind("<Configure>", lambda event: self._schedule_redraw_current_image())

        self.canvas.bind("<MouseWheel>", self._on_mousewheel_windows)
        self.canvas.bind("<Control-MouseWheel>", self._on_ctrl_mousewheel_windows)
        self.canvas.bind("<Button-4>", self._on_mousewheel_linux_up)
        self.canvas.bind("<Button-5>", self._on_mousewheel_linux_down)
        self.canvas.bind("<Control-Button-4>", self._on_ctrl_mousewheel_linux_up)
        self.canvas.bind("<Control-Button-5>", self._on_ctrl_mousewheel_linux_down)

        zoom_frame = ttk.Frame(parent, padding=(0, 8, 0, 0))
        zoom_frame.pack(fill="x")

        self.zoom_in_btn = ttk.Button(zoom_frame, text="放大", command=self.zoom_in, state="disabled")
        self.zoom_in_btn.pack(side="left", padx=(0, 4))

        self.zoom_out_btn = ttk.Button(zoom_frame, text="缩小", command=self.zoom_out, state="disabled")
        self.zoom_out_btn.pack(side="left", padx=4)

        self.zoom_reset_btn = ttk.Button(zoom_frame, text="重置缩放", command=self.reset_zoom, state="disabled")
        self.zoom_reset_btn.pack(side="left", padx=4)

    def _build_control_panel(self, parent: ttk.Frame):
        target_group = ttk.LabelFrame(parent, text="分类输出目录", padding=10)
        target_group.pack(fill="x", padx=(10, 0), pady=(0, 10))

        self.target_choice_var = tk.StringVar(value="")
        self.target_combo = ttk.Combobox(
            target_group,
            textvariable=self.target_choice_var,
            state="normal",
            width=44
        )
        self.target_combo.pack(fill="x")
        self.target_combo.bind("<<ComboboxSelected>>", lambda event: self.apply_target_from_input())
        self.target_combo.bind("<Return>", lambda event: self.apply_target_from_input())

        target_buttons = ttk.Frame(target_group)
        target_buttons.pack(fill="x", pady=(8, 0))

        self.apply_target_btn = ttk.Button(
            target_buttons,
            text="应用目录",
            command=self.apply_target_from_input,
            state="disabled"
        )
        self.apply_target_btn.pack(side="left", padx=(0, 4))

        self.pick_target_btn = ttk.Button(
            target_buttons,
            text="选择分类目录",
            command=self.choose_target_folder,
            state="disabled"
        )
        self.pick_target_btn.pack(side="left", padx=4)

        self.refresh_category_btn = ttk.Button(
            target_buttons,
            text="刷新类别按钮",
            command=self.refresh_categories,
            state="disabled"
        )
        self.refresh_category_btn.pack(side="left", padx=4)

        self.target_path_var = tk.StringVar(value="分类目录：尚未选择")
        ttk.Label(target_group, textvariable=self.target_path_var, wraplength=380).pack(anchor="w", pady=(8, 0))

        category_group = ttk.LabelFrame(parent, text="类别按钮（来自分类目录的子文件夹）", padding=10)
        category_group.pack(fill="both", expand=True, padx=(10, 0), pady=(0, 10))

        self.category_canvas = tk.Canvas(category_group, highlightthickness=0)
        self.category_scroll = ttk.Scrollbar(category_group, orient="vertical", command=self.category_canvas.yview)
        self.category_inner = ttk.Frame(self.category_canvas)

        self.category_inner.bind(
            "<Configure>",
            lambda event: self.category_canvas.configure(scrollregion=self.category_canvas.bbox("all"))
        )
        self.category_canvas_window = self.category_canvas.create_window((0, 0), window=self.category_inner, anchor="nw")
        self.category_canvas.configure(yscrollcommand=self.category_scroll.set)
        self.category_canvas.bind("<Configure>", self._resize_category_canvas_window)

        self.category_canvas.pack(side="left", fill="both", expand=True)
        self.category_scroll.pack(side="right", fill="y")

        progress_group = ttk.LabelFrame(parent, text="分类进度", padding=10)
        progress_group.pack(fill="x", padx=(10, 0))

        self.progress_var = tk.StringVar(value="进度：0 / 0")
        self.status_var = tk.StringVar(value="状态：请先选择需要分类的目标文件夹")
        self.summary_var = tk.StringVar(value="")
        self.current_category_var = tk.StringVar(value="当前分类：-")

        ttk.Label(progress_group, textvariable=self.progress_var).pack(anchor="w")
        ttk.Label(progress_group, textvariable=self.status_var, wraplength=380).pack(anchor="w", pady=(4, 0))
        ttk.Label(progress_group, textvariable=self.current_category_var).pack(anchor="w", pady=(4, 0))
        ttk.Label(progress_group, textvariable=self.summary_var, wraplength=380).pack(anchor="w", pady=(4, 8))

        action_frame = ttk.Frame(progress_group)
        action_frame.pack(fill="x")

        self.skip_btn = ttk.Button(action_frame, text="跳过 / 暂不判断", command=self.skip_current, state="disabled")
        self.skip_btn.pack(side="left", padx=(0, 4))

        self.undo_btn = ttk.Button(action_frame, text="上一张 / 撤销上一步", command=self.undo_last, state="disabled")
        self.undo_btn.pack(side="left", padx=4)

    def _resize_category_canvas_window(self, event):
        self.category_canvas.itemconfigure(self.category_canvas_window, width=event.width)

    # ========================================================
    # 模块 5：目录选择、状态文件、日志初始化
    # 作用：
    # - 选择待分类根目录
    # - 加载持久化状态
    # - 恢复上次使用的分类输出目录
    # - 扫描待分类样本并刷新界面
    # ========================================================

    def choose_root_folder(self):
        folder = filedialog.askdirectory(title="选择需要分类的目标文件夹")
        if not folder:
            return

        self.dataset_root = Path(folder).resolve()
        self.state_file = self.dataset_root / STATE_FILE_NAME
        self.log_file = self.dataset_root / LOG_FILE_NAME
        self.targets_file = self.dataset_root / TARGETS_FILE_NAME

        self.root_path_var.set(str(self.dataset_root))
        self.samples = []
        self.history.clear()
        self._clear_runtime_image_state()

        self._setup_logger()
        self.state_cache = self._load_state_file()
        self._load_target_history()
        self._restore_saved_target_root()

        self.status_var.set("状态：正在扫描待分类样本...")
        self.root.update_idletasks()

        self._reload_samples_from_current_root(restore_current=False)
        self._restore_session_view_state()
        self._enable_controls(bool(self.samples))
        self.show_current_sample()

    def _setup_logger(self):
        if self.log_file is None:
            return

        logger = logging.getLogger("benign_subcategory_classifier")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        logger.propagate = False

        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        self.logger = logger
        self.logger.info("===== 打开待分类目录：%s =====", self.dataset_root)

    def _load_state_file(self) -> Dict[str, Dict[str, str]]:
        self.session_state = {}

        if self.state_file is None or not self.state_file.exists():
            return {}

        try:
            with self.state_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return {}

                samples = data.get(STATE_SAMPLES_KEY)
                session = data.get(STATE_SESSION_KEY)
                if isinstance(session, dict):
                    self.session_state = session

                if isinstance(samples, dict):
                    return {k: v for k, v in samples.items() if isinstance(v, dict)}

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

        for sample in self.samples:
            self.state_cache[sample.key] = {
                "status": sample.status,
                "category": sample.category,
                "last_error": sample.last_error,
                "image_name": sample.image_name,
                "updated_at": datetime.now().isoformat(timespec="seconds"),
            }

        payload = {
            STATE_SAMPLES_KEY: self.state_cache,
            STATE_SESSION_KEY: self._build_session_state(),
        }
        with self.state_file.open("w", encoding="utf-8") as f:
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

    def _enable_controls(self, has_samples: bool):
        sample_state = "normal" if has_samples else "disabled"
        target_state = "normal" if self.dataset_root else "disabled"

        self.apply_target_btn.config(state=target_state)
        self.pick_target_btn.config(state=target_state)
        self.refresh_category_btn.config(state=target_state)
        self.skip_btn.config(state=sample_state)
        self.zoom_in_btn.config(state=sample_state)
        self.zoom_out_btn.config(state=sample_state)
        self.zoom_reset_btn.config(state=sample_state)
        self.undo_btn.config(state="normal" if self.history else "disabled")
        self._set_category_buttons_state(sample_state)

    # ========================================================
    # 模块 6：分类输出目录管理
    # 作用：
    # - 支持实时切换“分类后的文件夹”
    # - 读取该文件夹下的直接子文件夹，自动生成分类按钮
    # - 避免分类输出目录被重新扫描成待分类样本
    # ========================================================

    def _load_target_history(self):
        self.recent_target_roots = []

        if self.dataset_root is None:
            return

        default_target = self.dataset_root / DEFAULT_CLASSIFIED_DIR_NAME
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
                messagebox.showwarning("分类目录历史读取失败", f"将忽略旧分类目录历史：\n{e}")

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
            raw_path = self.dataset_root / DEFAULT_CLASSIFIED_DIR_NAME
        else:
            raw_path = Path(value)
            if not raw_path.is_absolute():
                raw_path = self.dataset_root / raw_path

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
        self.target_path_var.set(f"分类目录：{resolved}")

        if save_history:
            self._register_target_root(resolved)

        self.refresh_categories()

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
            target_root = self.dataset_root / DEFAULT_CLASSIFIED_DIR_NAME if self.dataset_root else None

        if target_root is not None:
            self._set_current_target(target_root, save_history=True)

    def apply_target_from_input(self):
        if self.dataset_root is None:
            messagebox.showwarning("尚未选择待分类目录", "请先选择需要分类的目标文件夹。")
            return

        old_current_key = self._get_current_sample_key()
        target_root = self._resolve_target_input(self.target_choice_var.get(), create=True)
        if target_root is None:
            return

        self._set_current_target(target_root, save_history=True)
        self.status_var.set(f"状态：分类目录已切换到 {target_root}")
        self._reload_samples_from_current_root(restore_current=True, preferred_key=old_current_key)
        self.show_current_sample()

    def choose_target_folder(self):
        if self.dataset_root is None:
            messagebox.showwarning("尚未选择待分类目录", "请先选择需要分类的目标文件夹。")
            return

        initial_dir = str(self.current_target_root or self.dataset_root)
        folder = filedialog.askdirectory(title="选择分类后的文件夹", initialdir=initial_dir, mustexist=False)
        if not folder:
            return

        old_current_key = self._get_current_sample_key()
        target_root = Path(folder).resolve()
        target_root.mkdir(parents=True, exist_ok=True)
        self._set_current_target(target_root, save_history=True)
        self.status_var.set(f"状态：分类目录已切换到 {target_root}")
        self._reload_samples_from_current_root(restore_current=True, preferred_key=old_current_key)
        self.show_current_sample()

    def refresh_categories(self):
        self.categories = []
        self.category_buttons = []

        for child in self.category_inner.winfo_children():
            child.destroy()

        if self.current_target_root is None:
            ttk.Label(self.category_inner, text="尚未选择分类目录。", foreground="gray").grid(row=0, column=0, sticky="w")
            return

        subdirs = sorted(
            [p for p in self.current_target_root.iterdir() if p.is_dir()],
            key=lambda p: p.name.lower()
        )

        if not subdirs:
            ttk.Label(
                self.category_inner,
                text="当前分类目录下没有子文件夹。\n请先在该目录中建立类别子文件夹，\n再点击“刷新类别按钮”。",
                foreground="gray",
                justify="left"
            ).grid(row=0, column=0, sticky="w")
            return

        for index, path in enumerate(subdirs):
            category = CategoryRecord(
                name=path.name,
                path=path,
                label=self._short_category_label(path.name),
            )
            self.categories.append(category)

            btn = ttk.Button(
                self.category_inner,
                text=category.label,
                command=lambda c=category: self.classify_current(c),
                state="normal" if self.samples else "disabled"
            )
            row = index // CATEGORY_BUTTON_WRAP
            col = index % CATEGORY_BUTTON_WRAP
            btn.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
            self.category_inner.columnconfigure(col, weight=1)
            self.category_buttons.append(btn)

        self._set_category_buttons_state("normal" if self.samples else "disabled")

    def _short_category_label(self, name: str) -> str:
        text = name.strip().replace("_", " ").replace("-", " ")
        text = " ".join(text.split()) or name
        if len(text) <= CATEGORY_LABEL_LIMIT:
            return text
        return text[:CATEGORY_LABEL_LIMIT - 1] + "…"

    def _set_category_buttons_state(self, state: str):
        if state not in ("normal", "disabled"):
            state = "disabled"
        for btn in self.category_buttons:
            btn.config(state=state)

    def _is_inside_any_managed_target_root(self, path: Path) -> bool:
        candidate = path.resolve()
        for target_root in self.recent_target_roots:
            try:
                candidate.relative_to(target_root.resolve())
                return True
            except ValueError:
                continue
        return False

    # ========================================================
    # 模块 7：样本扫描
    # 作用：
    # - 递归查找 screenshot_viewport.png 与 screenshot_full.png
    # - 每个找到图片的父目录视为一个样本目录
    # - 同一目录同时存在 viewport/full 时，优先使用 screenshot_viewport.png
    # - 自动跳过分类输出目录，避免已分类样本被重复扫描
    # ========================================================

    def _reload_samples_from_current_root(self, restore_current: bool = True, preferred_key: Optional[str] = None):
        if self.dataset_root is None:
            return

        if preferred_key is None and restore_current:
            preferred_key = self._get_current_sample_key()

        self.samples = self.scan_samples(self.dataset_root)
        self._clear_runtime_image_state(keep_position=True)

        if preferred_key:
            for idx, sample in enumerate(self.samples):
                if sample.key == preferred_key:
                    visible = self.get_visible_indices()
                    if idx in visible:
                        self.current_visible_pos = visible.index(idx)
                    else:
                        self.current_visible_pos = min(self.current_visible_pos, max(len(visible) - 1, 0))
                    break

        self._enable_controls(bool(self.samples))

    def scan_samples(self, root_dir: Path) -> List[SampleRecord]:
        sample_dirs = set()

        for image_name in IMAGE_NAME_PRIORITY:
            for image_path in root_dir.rglob(image_name):
                if self._is_inside_any_managed_target_root(image_path):
                    continue
                sample_dirs.add(image_path.parent.resolve())

        samples: List[SampleRecord] = []
        for sample_dir in sorted(sample_dirs, key=lambda p: str(p).lower()):
            viewport_path = sample_dir / VIEWPORT_IMAGE_NAME
            fallback_path = sample_dir / FALLBACK_IMAGE_NAME

            if viewport_path.exists():
                image_path = viewport_path
                image_name = VIEWPORT_IMAGE_NAME
            elif fallback_path.exists():
                image_path = fallback_path
                image_name = FALLBACK_IMAGE_NAME
            else:
                continue

            try:
                key = str(sample_dir.relative_to(root_dir)).replace("\\", "/")
            except ValueError:
                key = str(sample_dir)

            saved = self.state_cache.get(key, {})
            status = saved.get("status", "pending")
            category = saved.get("category", "")
            last_error = saved.get("last_error", "")

            samples.append(
                SampleRecord(
                    key=key,
                    original_dir=sample_dir,
                    current_dir=sample_dir,
                    image_path=image_path,
                    image_name=image_name,
                    status=status,
                    category=category,
                    last_error=last_error,
                )
            )

        samples.sort(key=lambda s: s.key.lower())
        return samples

    # ========================================================
    # 模块 8：过滤与统计
    # 作用：
    # - 根据“仅看未分类样本”开关生成可见样本列表
    # - 计算待分类、已分类、跳过、冲突、异常等统计信息
    # ========================================================

    def get_visible_indices(self) -> List[int]:
        if self.pending_only_var.get():
            return [i for i, s in enumerate(self.samples) if s.status == "pending"]
        return list(range(len(self.samples)))

    def update_summary(self):
        total = len(self.samples)
        visible = len(self.get_visible_indices())

        pending = sum(1 for s in self.samples if s.status == "pending")
        classified = sum(1 for s in self.samples if s.status == "classified")
        skipped = sum(1 for s in self.samples if s.status == "skipped")
        conflict = sum(1 for s in self.samples if s.status == "conflict_skipped")
        failed = sum(1 for s in self.samples if s.status in ("load_failed", "missing_image"))

        self.summary_var.set(
            f"总数: {total}  当前视图: {visible}  待分类: {pending}  "
            f"已分类: {classified}  跳过: {skipped}  冲突: {conflict}  异常: {failed}"
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

    # ========================================================
    # 模块 9：图片加载与自动跳过异常样本
    # 作用：
    # - 只加载当前样本截图，降低内存占用
    # - 优先加载 screenshot_viewport.png，缺失时才使用 screenshot_full.png
    # - 如果缺图或图片损坏，自动记录状态并跳过
    # ========================================================

    def show_current_sample(self):
        self.update_summary()
        visible = self.get_visible_indices()

        if not self.samples:
            self._show_empty_message("没有找到任何样本。\n扫描规则：优先 screenshot_viewport.png，缺失时回退 screenshot_full.png。")
            self.status_var.set("状态：目录中未发现可分类样本")
            return

        if not visible:
            msg = "没有符合当前过滤条件的样本"
            if self.pending_only_var.get():
                msg = "未分类样本已全部处理完毕"
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
            self.image_source_var.set("截图来源：-")
            return

        while True:
            visible = self.get_visible_indices()
            if not visible:
                self._show_empty_message("未分类样本已全部处理完毕")
                self.status_var.set("状态：当前视图为空")
                return

            if self.current_visible_pos >= len(visible):
                self._show_empty_message("当前视图已到末尾")
                self.status_var.set("状态：当前视图已到末尾")
                self.progress_var.set(f"进度：{len(visible)} / {len(visible)}")
                self.name_var.set("样本文件夹：-")
                self.image_source_var.set("截图来源：-")
                return

            sample_index = visible[self.current_visible_pos]
            sample = self.samples[sample_index]

            problem = self._load_current_image(sample)
            if problem is None:
                self.current_sample_index = sample_index
                self.name_var.set(f"样本文件夹：{sample.current_dir.name}")
                self.image_source_var.set(f"截图来源：{sample.image_name}")
                self.progress_var.set(f"进度：{self.current_visible_pos + 1} / {len(visible)}")
                self.status_var.set(f"状态：当前样本状态 = {sample.status}")
                self.current_category_var.set(f"当前分类：{sample.category or '-'}")
                self.redraw_current_image()
                self._save_state_file()
                self._schedule_preload()
                self.undo_btn.config(state="normal" if self.history else "disabled")
                self._set_category_buttons_state("normal" if self.samples and self.categories else "disabled")
                return

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
        previous_category = sample.category
        previous_error = sample.last_error

        if "缺少图片文件" in reason:
            sample.status = "missing_image"
        else:
            sample.status = "load_failed"

        sample.category = ""
        sample.last_error = reason
        self._save_state_file()

        self.history.append(
            ActionRecord(
                sample_index=sample_index,
                action="auto_skip",
                previous_status=previous_status,
                previous_category=previous_category,
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
    # - 根据画布大小与缩放倍率渲染当前截图
    # - 支持鼠标拖动、滚轮滚动、Ctrl+滚轮缩放
    # - 支持放大、缩小、重置缩放
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
    # 模块 11：分类 / 跳过 / 撤销
    # 作用：
    # - 分类：将整个样本目录移动到对应类别子文件夹中，并记录类别名
    # - 跳过：只写状态，不移动目录，适合暂时无法判断的样本
    # - 撤销：恢复上一步状态，包括把已移动目录搬回原路径
    # ========================================================

    def classify_current(self, category: CategoryRecord):
        sample_index = self._get_current_sample_index()
        if sample_index is None:
            return

        sample = self.samples[sample_index]
        previous_status = sample.status
        previous_category = sample.category
        previous_error = sample.last_error

        src_dir = sample.current_dir
        dst_dir = category.path / Path(*sample.key.split("/"))

        if dst_dir.exists():
            sample.status = "conflict_skipped"
            sample.category = category.name
            sample.last_error = f"目标类别目录中已存在同名目录：{dst_dir}"
            self._save_state_file()

            self.history.append(
                ActionRecord(
                    sample_index=sample_index,
                    action="conflict_skip",
                    previous_status=previous_status,
                    previous_category=previous_category,
                    previous_error=previous_error,
                )
            )

            if self.logger:
                self.logger.warning("CONFLICT_SKIP | key=%s | category=%s | dst=%s", sample.key, category.name, dst_dir)

            messagebox.showwarning("重名冲突", f"目标类别目录中已存在同名文件夹，已跳过本次分类：\n{dst_dir}")
            self._advance_after_action(sample_index)
            return

        try:
            dst_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_dir), str(dst_dir))

            sample.status = "classified"
            sample.category = category.name
            sample.last_error = ""
            sample.current_dir = dst_dir
            sample.image_path = self._select_image_path(dst_dir)
            sample.image_name = sample.image_path.name
            self._save_state_file()

            self.history.append(
                ActionRecord(
                    sample_index=sample_index,
                    action="classify",
                    previous_status=previous_status,
                    previous_category=previous_category,
                    previous_error=previous_error,
                    src=src_dir,
                    dst=dst_dir,
                )
            )

            if self.logger:
                self.logger.info(
                    "CLASSIFY | key=%s | category=%s | src=%s | dst=%s",
                    sample.key, category.name, src_dir, dst_dir
                )

            self._advance_after_action(sample_index)

        except Exception as e:
            messagebox.showerror("分类失败", f"移动样本文件夹失败：\n{e}")
            if self.logger:
                self.logger.error("CLASSIFY_FAIL | key=%s | category=%s | error=%s", sample.key, category.name, e)

    def skip_current(self):
        sample_index = self._get_current_sample_index()
        if sample_index is None:
            return

        sample = self.samples[sample_index]
        previous_status = sample.status
        previous_category = sample.category
        previous_error = sample.last_error

        sample.status = "skipped"
        sample.category = ""
        sample.last_error = ""
        self._save_state_file()

        self.history.append(
            ActionRecord(
                sample_index=sample_index,
                action="skip",
                previous_status=previous_status,
                previous_category=previous_category,
                previous_error=previous_error,
            )
        )

        if self.logger:
            self.logger.info("SKIP | key=%s", sample.key)

        self._advance_after_action(sample_index)

    def undo_last(self):
        if not self.history:
            return

        action = self.history.pop()
        sample = self.samples[action.sample_index]

        try:
            if action.action in ("skip", "conflict_skip", "auto_skip"):
                sample.status = action.previous_status
                sample.category = action.previous_category
                sample.last_error = action.previous_error

                if self.logger:
                    self.logger.info("UNDO_%s | key=%s", action.action.upper(), sample.key)

            elif action.action == "classify":
                if action.src is None or action.dst is None:
                    raise RuntimeError("撤销记录不完整，无法恢复")

                if action.src.exists():
                    raise RuntimeError(f"原路径已存在，无法撤销：{action.src}")

                if not action.dst.exists():
                    raise RuntimeError(f"目标类别目录中的样本不存在，无法撤销：{action.dst}")

                shutil.move(str(action.dst), str(action.src))
                sample.status = action.previous_status
                sample.category = action.previous_category
                sample.last_error = action.previous_error
                sample.current_dir = action.src
                sample.image_path = self._select_image_path(action.src)
                sample.image_name = sample.image_path.name

                if self.logger:
                    self.logger.info("UNDO_CLASSIFY | key=%s | restore_to=%s", sample.key, action.src)

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

    def _select_image_path(self, sample_dir: Path) -> Path:
        viewport_path = sample_dir / VIEWPORT_IMAGE_NAME
        fallback_path = sample_dir / FALLBACK_IMAGE_NAME
        if viewport_path.exists():
            return viewport_path
        return fallback_path

    # ========================================================
    # 模块 12：通用状态与空视图处理
    # 作用：
    # - 获取当前样本索引/键
    # - 清理运行时图片缓存
    # - 在空视图或处理完毕时给出明确提示
    # - 关闭窗口前保存状态
    # ========================================================

    def _get_current_sample_index(self) -> Optional[int]:
        if self.current_sample_index is None:
            return None
        if self.current_sample_index < 0 or self.current_sample_index >= len(self.samples):
            return None
        return self.current_sample_index

    def _get_current_sample_key(self) -> Optional[str]:
        sample_index = self._get_current_sample_index()
        if sample_index is None:
            return None
        return self.samples[sample_index].key

    def _show_empty_message(self, message: str):
        self.current_sample_index = None
        self.current_pil_image = None
        self.current_photo = None
        self.current_render_key = None

        self.name_var.set("样本文件夹：-")
        self.image_source_var.set("截图来源：-")
        self.progress_var.set("进度：0 / 0")
        self.current_category_var.set("当前分类：-")
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

    def _clear_runtime_image_state(self, keep_position: bool = False):
        if not keep_position:
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
# - 初始化 Tk 根窗口并启动 benign 细类划分工具
# ============================================================

def main():
    root = tk.Tk()
    app = BenignSubcategoryClassifierApp(root)
    app.run()


if __name__ == "__main__":
    main()
