import importlib.util
import shutil
from pathlib import Path

MODULE_PATH = Path(r"E:\Warden\temp\dataset_reviewed_switchable_targets.py")

spec = importlib.util.spec_from_file_location("dataset_reviewer_module", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DummyButton:
    def config(self, **kwargs):
        self.last_config = kwargs


class DummyBoolVar:
    def __init__(self, value=False):
        self.value = value

    def get(self):
        return self.value


tmp_root = Path(r"E:\Warden\tmp\dataset_reviewer_undo_validation_root")
if tmp_root.exists():
    shutil.rmtree(tmp_root, ignore_errors=True)
tmp_root.mkdir(parents=True, exist_ok=True)
try:
    dataset_root = tmp_root / "dataset"
    sample_dir = dataset_root / "phish" / "case1"
    image_path = sample_dir / module.IMAGE_NAME
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(b"not-an-image-but-good-enough-for-path-test")

    app = module.DatasetReviewerApp.__new__(module.DatasetReviewerApp)
    app.dataset_root = dataset_root
    app.current_target_root = dataset_root / module.REMOVED_DIR_NAME
    app.current_target_root.mkdir(parents=True, exist_ok=True)
    app.samples = [
        module.SampleRecord(
            key="phish/case1",
            original_dir=sample_dir,
            current_dir=sample_dir,
            image_path=image_path,
        )
    ]
    app.history = []
    app.current_sample_index = 0
    app.logger = None
    app.undo_btn = DummyButton()
    app.pending_only_var = DummyBoolVar(False)
    app._save_state_file = lambda: None
    app._advance_after_action = lambda sample_index: None
    app._focus_sample = lambda sample_index: None
    app._get_current_sample_index = lambda: 0

    app.remove_current()

    removed_dir = dataset_root / module.REMOVED_DIR_NAME / "phish" / "case1"
    assert removed_dir.exists(), f"expected removed path to exist: {removed_dir}"
    assert not sample_dir.exists(), f"source path should be moved away: {sample_dir}"

    app.undo_last()

    assert sample_dir.exists(), f"expected canonical restore path to exist: {sample_dir}"
    assert not removed_dir.exists(), f"removed path should be gone after undo: {removed_dir}"
    assert not (dataset_root / "phish" / module.REMOVED_DIR_NAME).exists(), "unexpected nested phish/removed directory created"
    assert not (dataset_root / module.REMOVED_DIR_NAME / "phish").exists(), "empty removed/phish directory should be pruned"

    print("validation_passed")
    print(f"restored_to={sample_dir}")
finally:
    shutil.rmtree(tmp_root, ignore_errors=True)
