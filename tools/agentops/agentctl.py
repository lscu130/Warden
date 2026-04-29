"""
Warden AgentOps local control tool.

功能：
1. 查看 AgentOps 任务报告
2. 查看任务 diff
3. 本地 approve：把当前任务分支上的安全改动提交成 commit
4. 本地 reject：丢弃当前任务分支上的安全改动
5. 可选向飞书发送审批结果通知

当前边界：
- 不自动 push
- 不自动 merge 到 main
- approve 只允许提交 docs/ 下的改动
- reject 默认不做破坏性操作，必须加 --force 才会丢弃改动
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


def build_safe_env() -> dict:
    """
    构造安全环境变量。

    作用：
    - Windows / PowerShell 下强制 UTF-8
    - 避免 subprocess 读取 git / agent 输出时被 GBK 坑掉
    """
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_cmd(args: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """
    执行命令并返回结果。

    所有输出统一按 UTF-8 解码。
    """
    process = subprocess.run(
        args,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        env=build_safe_env(),
    )

    if check and process.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(args)}\n"
            f"stdout:\n{process.stdout or ''}\n"
            f"stderr:\n{process.stderr or ''}"
        )

    return process


def get_project_root() -> Path:
    """
    获取当前 Git 仓库根目录。
    """
    process = run_cmd(["git", "rev-parse", "--show-toplevel"], check=True)
    return Path(process.stdout.strip())


PROJECT_ROOT = get_project_root()
AGENTOPS_DIR = PROJECT_ROOT / ".agentops"
REPORT_DIR = AGENTOPS_DIR / "reports"
DIFF_DIR = AGENTOPS_DIR / "diffs"


def notify_feishu_safely(text: str) -> None:
    """
    尝试发送飞书通知。

    如果飞书环境变量不存在或发送失败，不阻断本地审批流程。
    """
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "tools" / "agentops"))
        from feishu_notify import send_feishu_text

        send_feishu_text(text)
    except Exception as error:
        print(f"[warn] Feishu notification skipped: {repr(error)}")


def normalize_path(path: str) -> str:
    """
    统一路径分隔符，方便 Windows 下判断 docs/ 范围。
    """
    return path.strip().replace("\\", "/")


def get_current_branch() -> str:
    """
    获取当前 Git 分支名。
    """
    return run_cmd(["git", "branch", "--show-current"], check=True).stdout.strip()


def get_status_porcelain() -> str:
    """
    获取 git status --porcelain 输出。
    """
    return run_cmd(["git", "status", "--porcelain"], check=True).stdout.strip()


def get_changed_files() -> List[str]:
    """
    获取当前工作区 tracked + untracked 的变更文件。
    """
    tracked = run_cmd(["git", "diff", "--name-only"], check=True).stdout.splitlines()
    staged = run_cmd(["git", "diff", "--cached", "--name-only"], check=True).stdout.splitlines()
    untracked = run_cmd(
        ["git", "ls-files", "--others", "--exclude-standard"],
        check=True,
    ).stdout.splitlines()

    files = sorted(
        set(
            normalize_path(item)
            for item in tracked + staged + untracked
            if item.strip()
        )
    )

    return files


def split_safe_and_unsafe_files(files: List[str]) -> Tuple[List[str], List[str]]:
    """
    将变更文件分为安全文件和越权文件。

    当前 003 版本只允许 docs/ 下文件作为可审批改动。
    """
    safe = []
    unsafe = []

    for file_path in files:
        normalized = normalize_path(file_path)

        if normalized.startswith("docs/"):
            safe.append(normalized)
        else:
            unsafe.append(normalized)

    return safe, unsafe


def get_untracked_files() -> List[str]:
    """
    获取 untracked 文件列表。
    """
    return [
        normalize_path(item)
        for item in run_cmd(
            ["git", "ls-files", "--others", "--exclude-standard"],
            check=True,
        ).stdout.splitlines()
        if item.strip()
    ]


def load_report(task_id: str) -> dict:
    """
    读取任务 JSON 报告。
    """
    report_path = REPORT_DIR / f"{task_id}.json"

    if not report_path.exists():
        raise FileNotFoundError(
            f"找不到任务报告：{report_path}\n"
            f"请确认 task id 是否正确，或先运行对应 Agent。"
        )

    return json.loads(report_path.read_text(encoding="utf-8"))


def get_diff_path(task_id: str, report: dict | None = None) -> Path:
    """
    获取任务 diff 路径。

    优先使用 report 里的 diff_path；没有则使用默认路径。
    """
    if report:
        raw = report.get("diff_path")
        if raw:
            return Path(raw)

    return DIFF_DIR / f"{task_id}.diff"


def cmd_list(_: argparse.Namespace) -> None:
    """
    列出已有 AgentOps 报告。
    """
    if not REPORT_DIR.exists():
        print("No AgentOps reports found.")
        return

    reports = sorted(REPORT_DIR.glob("*.json"))

    if not reports:
        print("No AgentOps reports found.")
        return

    print("AgentOps tasks:")
    for report_file in reports:
        try:
            report = json.loads(report_file.read_text(encoding="utf-8"))
            task_id = report.get("task_id", report_file.stem)
            branch_name = report.get("branch_name", "(unknown branch)")
            returncode = report.get("returncode", "(unknown)")
            changed_files = report.get("changed_files", [])
            print(f"- {task_id} | branch={branch_name} | returncode={returncode} | changed={len(changed_files)}")
        except Exception:
            print(f"- {report_file.stem} | unreadable report")


def cmd_status(args: argparse.Namespace) -> None:
    """
    显示任务状态。
    """
    report = load_report(args.task_id)

    current_branch = get_current_branch()
    status = get_status_porcelain()

    print(f"Task ID: {report.get('task_id', args.task_id)}")
    print(f"Task: {report.get('task', '')}")
    print(f"Report branch: {report.get('branch_name', '(unknown)')}")
    print(f"Current branch: {current_branch}")
    print(f"Return code: {report.get('returncode', '(unknown)')}")
    print(f"Elapsed seconds: {report.get('elapsed_seconds', '(unknown)')}")
    print(f"Diff path: {get_diff_path(args.task_id, report)}")

    print("\nChanged files from report:")
    for file_path in report.get("changed_files", []):
        print(f"  {file_path}")

    print("\nSafe files from report:")
    for file_path in report.get("safe_files", []):
        print(f"  {file_path}")

    print("\nUnsafe files from report:")
    unsafe = report.get("unsafe_files", [])
    if unsafe:
        for file_path in unsafe:
            print(f"  {file_path}")
    else:
        print("  (none)")

    print("\nCurrent git status:")
    if status:
        print(status)
    else:
        print("  clean")


def cmd_diff(args: argparse.Namespace) -> None:
    """
    显示任务 diff。
    """
    report = load_report(args.task_id)
    diff_path = get_diff_path(args.task_id, report)

    if not diff_path.exists():
        raise FileNotFoundError(f"找不到 diff 文件：{diff_path}")

    diff_text = diff_path.read_text(encoding="utf-8", errors="replace")

    if args.full:
        print(diff_text)
        return

    limit = args.limit
    if len(diff_text) > limit:
        print(diff_text[:limit])
        print(f"\n[truncated] diff is {len(diff_text)} characters. Use --full to print all.")
    else:
        print(diff_text)


def cmd_approve(args: argparse.Namespace) -> None:
    """
    审批任务。

    行为：
    - 检查当前分支必须是任务分支
    - 检查当前工作区只能有 docs/ 下改动
    - git add docs/ 改动
    - git commit
    - 不 push
    - 不 merge
    """
    report = load_report(args.task_id)

    report_branch = report.get("branch_name")
    current_branch = get_current_branch()

    if not report_branch:
        raise RuntimeError("任务报告中没有 branch_name，拒绝 approve。")

    if current_branch != report_branch:
        raise RuntimeError(
            f"当前分支不是任务分支，拒绝 approve。\n"
            f"Current branch: {current_branch}\n"
            f"Task branch: {report_branch}\n"
            f"请先执行：git switch {report_branch}"
        )

    changed_files = get_changed_files()
    safe_files, unsafe_files = split_safe_and_unsafe_files(changed_files)

    if unsafe_files:
        raise RuntimeError(
            "检测到 docs/ 外改动，拒绝 approve。\n\n"
            + "\n".join(unsafe_files)
        )

    if not safe_files:
        print("No safe files to approve. Working tree has no docs/ changes.")
        return

    run_cmd(["git", "add", "--"] + safe_files, check=True)

    staged = run_cmd(["git", "diff", "--cached", "--name-only"], check=True).stdout.strip()
    if not staged:
        print("No staged changes after git add. Nothing to commit.")
        return

    commit_message = args.message or f"Approve AgentOps task {args.task_id}"

    run_cmd(["git", "commit", "-m", commit_message], check=True)

    print(f"Approved and committed task: {args.task_id}")
    print(f"Branch: {current_branch}")
    print("Committed files:")
    for file_path in safe_files:
        print(f"  {file_path}")

    notify_feishu_safely(
        f"[AgentOps Approved]\n"
        f"Task ID: {args.task_id}\n"
        f"Branch: {current_branch}\n"
        f"Commit message: {commit_message}\n"
        f"Files:\n" + "\n".join(safe_files)
    )


def cmd_reject(args: argparse.Namespace) -> None:
    """
    拒绝任务。

    默认只预览会丢弃哪些文件。
    加 --force 后才会执行丢弃。
    """
    report = load_report(args.task_id)

    report_branch = report.get("branch_name")
    current_branch = get_current_branch()

    if not report_branch:
        raise RuntimeError("任务报告中没有 branch_name，拒绝 reject。")

    if current_branch != report_branch:
        raise RuntimeError(
            f"当前分支不是任务分支，拒绝 reject。\n"
            f"Current branch: {current_branch}\n"
            f"Task branch: {report_branch}\n"
            f"请先执行：git switch {report_branch}"
        )

    changed_files = get_changed_files()
    safe_files, unsafe_files = split_safe_and_unsafe_files(changed_files)

    if unsafe_files:
        raise RuntimeError(
            "检测到 docs/ 外改动，拒绝自动 reject。请手动检查。\n\n"
            + "\n".join(unsafe_files)
        )

    if not safe_files:
        print("No docs/ changes to reject.")
        return

    print("Docs changes that would be rejected:")
    for file_path in safe_files:
        print(f"  {file_path}")

    if not args.force:
        print("\nDry run only. Add --force to discard these changes.")
        return

    untracked_files = set(get_untracked_files())

    tracked_safe_files = [file_path for file_path in safe_files if file_path not in untracked_files]
    untracked_safe_files = [file_path for file_path in safe_files if file_path in untracked_files]

    if tracked_safe_files:
        run_cmd(["git", "restore", "--"] + tracked_safe_files, check=True)

    if untracked_safe_files:
        run_cmd(["git", "clean", "-f", "--"] + untracked_safe_files, check=True)

    print(f"Rejected task and discarded docs/ changes: {args.task_id}")

    notify_feishu_safely(
        f"[AgentOps Rejected]\n"
        f"Task ID: {args.task_id}\n"
        f"Branch: {current_branch}\n"
        f"Discarded files:\n" + "\n".join(safe_files)
    )


def build_parser() -> argparse.ArgumentParser:
    """
    构造命令行 parser。
    """
    parser = argparse.ArgumentParser(
        description="Warden AgentOps local control tool"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List local AgentOps task reports")
    list_parser.set_defaults(func=cmd_list)

    status_parser = subparsers.add_parser("status", help="Show task status")
    status_parser.add_argument("task_id")
    status_parser.set_defaults(func=cmd_status)

    diff_parser = subparsers.add_parser("diff", help="Show task diff")
    diff_parser.add_argument("task_id")
    diff_parser.add_argument("--full", action="store_true", help="Print full diff")
    diff_parser.add_argument("--limit", type=int, default=12000, help="Max characters unless --full is used")
    diff_parser.set_defaults(func=cmd_diff)

    approve_parser = subparsers.add_parser("approve", help="Approve task by committing safe docs/ changes")
    approve_parser.add_argument("task_id")
    approve_parser.add_argument("-m", "--message", help="Git commit message")
    approve_parser.set_defaults(func=cmd_approve)

    reject_parser = subparsers.add_parser("reject", help="Reject task by discarding safe docs/ changes")
    reject_parser.add_argument("task_id")
    reject_parser.add_argument("--force", action="store_true", help="Actually discard docs/ changes")
    reject_parser.set_defaults(func=cmd_reject)

    return parser


def main() -> None:
    """
    主入口。
    """
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as error:
        print(f"[agentctl error] {repr(error)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()