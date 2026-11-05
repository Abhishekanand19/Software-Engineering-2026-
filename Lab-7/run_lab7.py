"""Produce reproducible before/after console evidence for Lab 7.

Run using the project virtual environment. The original code is copied to a
throwaway working directory; the checked-in fixed file is never overwritten.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / ".lab7_runs"
EVIDENCE = ROOT / "evidence"


def execute(stage: str, source: Path, command: list[str], filename: str,
            stdin: str | None = None) -> tuple[int, str]:
    work = RUNS / stage
    work.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, work / "atm_withdrawal.py")
    shutil.copyfile(ROOT / "test_atm_withdrawal.py", work / "test_atm_withdrawal.py")

    env = os.environ.copy()
    env["PYTHONHASHSEED"] = "0"
    # The exact tested code is the file in the stage-specific directory.
    full_command = [sys.executable] + command
    completed = subprocess.run(
        full_command,
        input=stdin,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=work,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    display_command = "python " + " ".join(command)
    content = (
        f"LAB 7 - {stage.upper()}\n"
        f"Directory: {stage}/\n"
        f"Command: {display_command}\n"
        + (f"Scripted console input: {stdin!r}\n" if stdin is not None else "")
        + "-" * 68 + "\n"
        + completed.stdout
        + f"\nProcess exit code: {completed.returncode}\n"
    )
    (EVIDENCE / filename).write_text(content, encoding="utf-8")
    print(f"\n--- {filename} (exit={completed.returncode}) ---")
    lines = content.rstrip().splitlines()
    print("\n".join(lines[-12:]))
    return completed.returncode, content


def main() -> int:
    EVIDENCE.mkdir(exist_ok=True)
    RUNS.mkdir(exist_ok=True)

    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or newer required.", file=sys.stderr)
        return 2

    print("LAB 7: automated before/after fuzz testing")
    print("Project:", ROOT)
    print("Expected original bugs: invalid numeric input, invalid card format, malformed CSV")

    buggy_cli_rc, _ = execute(
        "buggy", ROOT / "atm_withdrawal_buggy.py",
        ["atm_withdrawal.py"], "01_buggy_application.txt",
        stdin="abc\n1234\n100,,300\n",
    )
    buggy_tests_rc, buggy_tests = execute(
        "buggy", ROOT / "atm_withdrawal_buggy.py",
        ["-m", "pytest", "test_atm_withdrawal.py", "-q", "--tb=short", "-rA"],
        "02_failing_fuzz_tests.txt",
    )
    fixed_cli_rc, fixed_cli = execute(
        "fixed", ROOT / "atm_withdrawal.py",
        ["atm_withdrawal.py"], "03_fixed_application.txt",
        stdin="abc\n1234\n100,,300\n",
    )
    fixed_tests_rc, fixed_tests = execute(
        "fixed", ROOT / "atm_withdrawal.py",
        ["-m", "pytest", "test_atm_withdrawal.py", "-q", "--tb=short", "-rA"],
        "04_passing_fuzz_tests.txt",
    )

    # Do not misreport environment errors as genuine test failures.
    test_names = (
        "test_notes_needed_no_crash",
        "test_mask_card_no_crash",
        "test_average_withdrawal_no_crash",
    )
    meaningful_failures = all(name in buggy_tests for name in test_names)
    passed = bool(re.search(r"\b\d+ passed\b", fixed_tests))
    expected_failure = buggy_cli_rc != 0 and buggy_tests_rc != 0 and meaningful_failures
    expected_success = (
        fixed_cli_rc == 0 and fixed_tests_rc == 0 and passed
        and "Number of 100 Notes: 0" in fixed_cli
        and "Masked Card: Invalid card number" in fixed_cli
        and "Average Withdrawal: 0" in fixed_cli
    )

    print("\n" + "=" * 68)
    print("VALIDATION:")
    print("Original application crashes on invalid input:", "YES" if buggy_cli_rc else "NO")
    print("Original Hypothesis tests expose failures:", "YES" if expected_failure else "NO")
    print("Fixed application handles invalid input:", "YES" if fixed_cli_rc == 0 else "NO")
    print("Fixed Hypothesis tests all pass:", "YES" if fixed_tests_rc == 0 and passed else "NO")
    print("Evidence logs:", EVIDENCE)

    if not (expected_failure and expected_success):
        print("ERROR: one or more expected checks were not satisfied. Review the evidence logs.")
        return 1

    try:
        from build_report import build_report
        build_report()
    except Exception as exc:
        print("Report generation was not completed:", exc)
        return 1

    print("\nDONE: all four evidence logs were produced from actual executions.")
    print("Take genuine terminal screenshots and save them using the filenames in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
