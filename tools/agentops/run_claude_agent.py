"""
Claude Code agent runner.

功能：
1. 接收一个任务描述
2. 调用 Claude Code 的非交互模式执行任务
3. 保存 Claude Code 输出到 .agentops/reports/
4. 将任务开始、成功、失败状态发送到飞书群

当前版本限制：
- 只允许 Claude Code 使用 Read / Glob / Grep / git status
- 不允许 Edit / Write / Bash 任意命令
- 主要用于验证 Claude Code 能否接入飞书 AgentOps 流程
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from feishu_notify import send_feishu_text


PROJECT_ROOT = Path.cwd()
REPORT_DIR = PROJECT_ROOT / ".agentops" / "reports"
LOG_DIR = PROJECT_ROOT / ".agentops" / "logs"


def build_prompt(task: str) -> str:
    """
    构造给 Claude Code 的任务提示词。

    当前阶段只让 Claude 做只读分析，不允许修改文件。
    """
    return f"""
You are the Claude Code agent inside the Warden-AgentOps workflow.

Task:
{task}

Rules:
1. Do not modify files.
2. Do not create files.
3. Inspect the repository only if needed.
4. Produce a concise execution report.
5. Include:
   - What you inspected
   - Findings
   - Suggested next action
   - Whether code/file changes are needed
6. Respond in Chinese by default, unless the task explicitly requires English.
"""


def run_claude(task: str, task_id: str) -> dict:
    """
    调用 Claude Code 非交互模式，并返回结构化执行结果。
    """
    prompt = build_prompt(task)

    command = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--max-turns",
        "6",
        "--max-budget-usd",
        "1.00",
        "--allowedTools",
        "Read,Glob,Grep,Bash(git status *)",
    ]

    started_at = time.time()

    process = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=900,
    )

    elapsed_seconds = round(time.time() - started_at, 2)

    return {
        "task_id": task_id,
        "task": task,
        "returncode": process.returncode,
        "elapsed_seconds": elapsed_seconds,
        "stdout": process.stdout,
        "stderr": process.stderr,
    }


def save_report(result: dict) -> Path:
    """
    保存 Claude Code 执行结果。
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    task_id = result["task_id"]
    report_path = REPORT_DIR / f"{task_id}.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)

    return report_path


def extract_result_text(stdout: str | None) -> str:
    """
    从 Claude Code JSON 输出里提取 result 字段。

    Windows 下如果 subprocess 解码失败，stdout 可能是 None。
    这里要兜底，避免二次崩溃。
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

    return stdout[:3000]


def main() -> None:
    """
    命令行入口。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True, help="任务编号，例如 TASK-CLAUDE-001")
    parser.add_argument("--task", required=True, help="交给 Claude Code 的任务内容")
    args = parser.parse_args()

    send_feishu_text(
        f"[Claude Agent Started]\n"
        f"Task ID: {args.task_id}\n"
        f"Task: {args.task}"
    )

    try:
        result = run_claude(task=args.task, task_id=args.task_id)
        report_path = save_report(result)
        result_text = extract_result_text(result["stdout"])

        if result["returncode"] == 0:
            send_feishu_text(
                f"[Claude Agent Completed]\n"
                f"Task ID: {args.task_id}\n"
                f"Elapsed: {result['elapsed_seconds']}s\n"
                f"Report: {report_path}\n\n"
                f"Summary:\n{result_text[:2500]}"
            )
        else:
            send_feishu_text(
                f"[Claude Agent Failed]\n"
                f"Task ID: {args.task_id}\n"
                f"Return Code: {result['returncode']}\n"
                f"Report: {report_path}\n\n"
                f"stderr:\n{result['stderr'][:2500]}"
            )
            sys.exit(result["returncode"])

    except Exception as error:
        send_feishu_text(
            f"[Claude Agent Error]\n"
            f"Task ID: {args.task_id}\n"
            f"Error: {repr(error)}"
        )
        raise


if __name__ == "__main__":
    main()