"""
Claude Code documentation agent runner.

功能：
1. 通过 Python 调用 Claude Code 非交互模式
2. 允许 Claude 修改 docs/ 目录下的文档
3. 自动创建独立 git branch
4. 执行后检查是否越权修改 docs/ 外文件
5. 生成 git diff 和 JSON report
6. 将执行状态、变更文件、diff 摘要发送到飞书群

安全边界：
- 不自动 commit
- 不自动 push
- 不自动 merge
- 只允许 docs/ 路径下的文件变更

Windows 修复：
- subprocess 强制使用 UTF-8
- errors="replace" 防止 GBK 解码 Claude 输出时报错
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

from feishu_notify import send_feishu_text


PROJECT_ROOT = Path.cwd()
AGENTOPS_DIR = PROJECT_ROOT / ".agentops"
REPORT_DIR = AGENTOPS_DIR / "reports"
DIFF_DIR = AGENTOPS_DIR / "diffs"


def build_safe_env() -> dict:
    """
    构造子进程环境变量。

    作用：
    1. 在 Windows / PowerShell 下尽量强制 Python 和子进程使用 UTF-8
    2. 避免 Claude Code 输出 UTF-8 字符时被 Python 用 GBK 解码导致崩溃
    """
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def run_cmd(args: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """
    执行命令并返回结果。

    注意：
    - text=True 会把 stdout/stderr 解码成字符串
    - encoding="utf-8" 避免 Windows 默认 GBK 解码
    - errors="replace" 避免遇到非法字节时报 UnicodeDecodeError
    """
    process = subprocess.run(
        args,
        cwd=PROJECT_ROOT,
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


def ensure_agentops_excluded() -> None:
    """
    将 .agentops/ 写入 .git/info/exclude，避免本地报告污染 git status。

    这不会修改仓库里的 .gitignore，因此不会产生项目文件变更。
    """
    exclude_path = PROJECT_ROOT / ".git" / "info" / "exclude"
    exclude_path.parent.mkdir(parents=True, exist_ok=True)

    existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""

    lines_to_add = []
    if ".agentops/" not in existing:
        lines_to_add.append(".agentops/")
    if ".agentops/*" not in existing:
        lines_to_add.append(".agentops/*")

    if lines_to_add:
        with exclude_path.open("a", encoding="utf-8") as file:
            file.write("\n# Warden AgentOps local reports\n")
            for line in lines_to_add:
                file.write(line + "\n")


def sanitize_branch_name(task_id: str) -> str:
    """
    将任务 ID 转成安全的 git branch 名称。
    """
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", task_id).strip("-")
    return f"agent/{safe}"


def ensure_clean_worktree() -> None:
    """
    确保当前工作区干净，避免 Claude 覆盖你已有的修改。

    注意：
    如果你刚刚新增或修改了 tools/agentops/ 里的脚本，还没有提交，
    这里会拦截。这是正常的安全行为。
    """
    status = run_cmd(["git", "status", "--porcelain"], check=True).stdout.strip()

    if status:
        raise RuntimeError(
            "当前 git 工作区不干净。请先处理已有改动，再运行文档 Agent。\n\n"
            f"git status --porcelain:\n{status}"
        )


def switch_to_task_branch(task_id: str) -> str:
    """
    切换到独立任务分支。

    如果分支不存在则创建，存在则切换。
    """
    branch_name = sanitize_branch_name(task_id)

    existing_branches = run_cmd(
        ["git", "branch", "--list", branch_name],
        check=True,
    ).stdout.strip()

    if existing_branches:
        run_cmd(["git", "switch", branch_name], check=True)
    else:
        run_cmd(["git", "switch", "-c", branch_name], check=True)

    return branch_name


def build_prompt(task: str) -> str:
    """
    构造给 Claude Code 的文档任务提示词。
    """
    return f"""
You are the Claude documentation agent inside the Warden-AgentOps workflow.

Task:
{task}

Hard rules:
1. You may modify files only under docs/.
2. Do not modify source code.
3. Do not modify data files.
4. Do not modify configuration files.
5. Do not modify README.md unless the task explicitly says so.
6. Do not commit, push, or merge.
7. Prefer Markdown.
8. For Warden project documents, use bilingual format:
   - Chinese section first.
   - English section after Chinese.
9. Keep the change minimal and directly tied to the task.
10. At the end, report:
   - files changed
   - summary of changes
   - whether further review is needed
"""


def run_claude_doc_task(task: str, task_id: str) -> dict:
    """
    调用 Claude Code 执行文档任务。
    """
    prompt = build_prompt(task)

    command = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--max-turns",
        "12",
        "--max-budget-usd",
        "2.00",
        "--permission-mode",
        "dontAsk",
        "--tools",
        "Read,Glob,Grep,Edit,MultiEdit,Write",
        "--allowedTools",
        "Read,Glob,Grep,Edit,MultiEdit,Write",
    ]

    started_at = time.time()

    process = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=1800,
        env=build_safe_env(),
    )

    elapsed_seconds = round(time.time() - started_at, 2)

    return {
        "task_id": task_id,
        "task": task,
        "returncode": process.returncode,
        "elapsed_seconds": elapsed_seconds,
        "stdout": process.stdout or "",
        "stderr": process.stderr or "",
    }


def get_changed_files() -> List[str]:
    """
    获取 tracked + untracked 的变更文件。
    """
    tracked = run_cmd(["git", "diff", "--name-only"], check=True).stdout.splitlines()

    untracked = run_cmd(
        ["git", "ls-files", "--others", "--exclude-standard"],
        check=True,
    ).stdout.splitlines()

    files = sorted(
        set(
            item.strip().replace("\\", "/")
            for item in tracked + untracked
            if item.strip()
        )
    )

    return files


def split_safe_and_unsafe_files(files: List[str]) -> Tuple[List[str], List[str]]:
    """
    将变更文件分为 docs/ 内和 docs/ 外。
    """
    safe = []
    unsafe = []

    for file_path in files:
        normalized = file_path.replace("\\", "/")
        if normalized.startswith("docs/"):
            safe.append(normalized)
        else:
            unsafe.append(normalized)

    return safe, unsafe


def save_diff(task_id: str) -> Path:
    """
    保存 docs/ 目录下的 git diff。

    注意：
    git diff 默认不会包含 untracked 文件，所以这里额外把新建 docs 文件内容写入 diff 报告。
    """
    DIFF_DIR.mkdir(parents=True, exist_ok=True)
    diff_path = DIFF_DIR / f"{task_id}.diff"

    diff_text = run_cmd(["git", "diff", "--", "docs/"], check=True).stdout

    untracked_docs = [
        p
        for p in run_cmd(
            ["git", "ls-files", "--others", "--exclude-standard", "docs/"],
            check=True,
        ).stdout.splitlines()
        if p.strip()
    ]

    if untracked_docs:
        diff_text += "\n\n# Untracked docs files created by agent\n"

        for file_path in untracked_docs:
            full_path = PROJECT_ROOT / file_path
            diff_text += f"\n\n--- BEGIN UNTRACKED FILE: {file_path} ---\n"

            try:
                diff_text += full_path.read_text(encoding="utf-8", errors="replace")
            except Exception as error:
                diff_text += f"[Could not read file: {repr(error)}]"

            diff_text += f"\n--- END UNTRACKED FILE: {file_path} ---\n"

    diff_path.write_text(diff_text, encoding="utf-8")
    return diff_path


def get_diff_stat() -> str:
    """
    获取 docs/ 目录下的 diff stat。
    """
    return run_cmd(["git", "diff", "--stat", "--", "docs/"], check=True).stdout.strip()


def extract_result_text(stdout: str | None) -> str:
    """
    从 Claude Code JSON 输出中提取 result 字段。

    Windows 下如果子进程输出异常，stdout 可能为空。
    这里必须兜底，避免二次崩溃。
    """
    if not stdout:
        return "(Claude Code 没有返回 stdout，请查看 stderr 或 .agentops/reports/ 下的 JSON 报告。)"

    stdout = stdout.strip()

    try:
        data = json.loads(stdout)
        result = data.get("result", "")
        if result:
            return result.strip()
    except json.JSONDecodeError:
        pass
    except TypeError:
        pass

    return stdout[:3000]


def save_report(
    result: dict,
    branch_name: str,
    changed_files: List[str],
    safe_files: List[str],
    unsafe_files: List[str],
    diff_path: Path,
) -> Path:
    """
    保存完整执行报告。
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        **result,
        "branch_name": branch_name,
        "changed_files": changed_files,
        "safe_files": safe_files,
        "unsafe_files": unsafe_files,
        "diff_path": str(diff_path),
    }

    report_path = REPORT_DIR / f"{result['task_id']}.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report_path


def main() -> None:
    """
    命令行入口。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True, help="任务编号，例如 TASK-CLAUDE-002")
    parser.add_argument("--task", required=True, help="交给 Claude Code 的文档任务")
    args = parser.parse_args()

    try:
        ensure_agentops_excluded()
        ensure_clean_worktree()
        branch_name = switch_to_task_branch(args.task_id)

        send_feishu_text(
            f"[Claude Doc Agent Started]\n"
            f"Task ID: {args.task_id}\n"
            f"Branch: {branch_name}\n"
            f"Scope: docs/ only\n"
            f"Task: {args.task}"
        )

        result = run_claude_doc_task(task=args.task, task_id=args.task_id)

        changed_files = get_changed_files()
        safe_files, unsafe_files = split_safe_and_unsafe_files(changed_files)
        diff_path = save_diff(args.task_id)
        diff_stat = get_diff_stat()

        report_path = save_report(
            result=result,
            branch_name=branch_name,
            changed_files=changed_files,
            safe_files=safe_files,
            unsafe_files=unsafe_files,
            diff_path=diff_path,
        )

        result_text = extract_result_text(result.get("stdout"))

        if result["returncode"] != 0:
            send_feishu_text(
                f"[Claude Doc Agent Failed]\n"
                f"Task ID: {args.task_id}\n"
                f"Branch: {branch_name}\n"
                f"Return Code: {result['returncode']}\n"
                f"Report: {report_path}\n\n"
                f"stderr:\n{result.get('stderr', '')[:2500]}"
            )
            sys.exit(result["returncode"])

        if unsafe_files:
            send_feishu_text(
                f"[Claude Doc Agent Scope Violation]\n"
                f"Task ID: {args.task_id}\n"
                f"Branch: {branch_name}\n\n"
                f"Unsafe files changed outside docs/:\n"
                f"{chr(10).join(unsafe_files)}\n\n"
                f"Report: {report_path}\n"
                f"Diff: {diff_path}\n\n"
                f"Action: Do not commit. Inspect with git status and git diff."
            )
            sys.exit(2)

        if not changed_files:
            send_feishu_text(
                f"[Claude Doc Agent Completed - No Changes]\n"
                f"Task ID: {args.task_id}\n"
                f"Branch: {branch_name}\n"
                f"Elapsed: {result['elapsed_seconds']}s\n"
                f"Report: {report_path}\n\n"
                f"Claude summary:\n{result_text[:1800]}"
            )
            return

        changed_files_text = chr(10).join(safe_files)
        diff_stat_text = diff_stat if diff_stat else "(new untracked docs file or no tracked diff stat)"

        send_feishu_text(
            f"[Claude Doc Agent Completed]\n"
            f"Task ID: {args.task_id}\n"
            f"Branch: {branch_name}\n"
            f"Elapsed: {result['elapsed_seconds']}s\n"
            f"Changed files:\n{changed_files_text}\n\n"
            f"Diff stat:\n{diff_stat_text}\n\n"
            f"Report: {report_path}\n"
            f"Diff: {diff_path}\n\n"
            f"Claude summary:\n{result_text[:1800]}"
        )

    except Exception as error:
        send_feishu_text(
            f"[Claude Doc Agent Error]\n"
            f"Task ID: {args.task_id}\n"
            f"Error: {repr(error)}"
        )
        raise


if __name__ == "__main__":
    main()