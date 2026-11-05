# Lab 7 - ATM Withdrawal Fuzz Testing

**Student:** Abhishek Anand | **SRN:** PES1UG24CS017 | **Section:** 5A

Original assignment: [`SETAPESU26/L6_L7_18_atm_withdrawal/Lab 7`](https://github.com/SETAPESU26/L6_L7_18_atm_withdrawal/tree/main/Lab%207).

This folder contains the completed Hypothesis fuzz tests, hardened ATM utility code, the unchanged assigned buggy version (for before/after evidence), and a reproducible one-command runner.

## One-command run (Windows CMD)

1. Clone the personal repository, if it isn't already on your PC:
   ```bat
   git clone https://github.com/Abhishekanand19/Software-Engineering-2026-.git
   cd Software-Engineering-2026-\Lab-7
   ```
2. Execute:
   ```bat
   run_lab7.cmd
   ```

The batch file creates a project-local virtual environment, installs dependencies, runs the original and fixed applications, runs the same Hypothesis tests against both, and saves four **real terminal outputs** in `evidence/`. It does not modify the original or final application files.

Alternatively, on Linux/macOS, after installing `requirements.txt`, run `python run_lab7.py`.

## Mandatory screenshots for the handout

After running the command, open **Command Prompt in the `Lab-7` folder**. Show each real output in your terminal using `type`, then capture the screen using **Win+Shift+S**. Save the screenshot using the exact filename below:

| Handout step | Command to display real output | Screenshot destination |
|---|---|---|
| Step 2: buggy program | `type evidence\01_buggy_application.txt` | `screenshots\01_buggy_application.png` |
| Step 4: failing Hypothesis tests | `type evidence\02_failing_fuzz_tests.txt` | `screenshots\02_failing_fuzz_tests.png` |
| Step 5: fixed program | `type evidence\03_fixed_application.txt` | `screenshots\03_fixed_application.png` |
| Step 6: passing Hypothesis tests | `type evidence\04_passing_fuzz_tests.txt` | `screenshots\04_passing_fuzz_tests.png` |

**Screenshot guidance:** `02_failing_fuzz_tests.txt` is long, so use `powershell -Command "Get-Content evidence\02_failing_fuzz_tests.txt -Tail 28"` to show the test failure summary clearly in CMD before capturing the screenshot. All four captures must be of actual output on your own system; do not fabricate screenshots. If Windows Snipping Tool saves `.jpg` rather than `.png`, save it as PNG for the report builder.

Once the four PNG screenshots are saved in `screenshots/`, simply run **`run_lab7.cmd` again**. It automatically creates the final report:

`PES1UG24CS017_Lab7_Fuzz_Testing_Report.pdf`

Or build only the report (after setting up dependencies): `.venv\Scripts\python.exe build_report.py`.

## Deliverables

The lab handout requires three items:

1. **PDF report with 4 execution screenshots**: `PES1UG24CS017_Lab7_Fuzz_Testing_Report.pdf` (generated only once all real screenshots exist).
2. **Fixed application**: `atm_withdrawal.py`.
3. **Updated Hypothesis tests**: `test_atm_withdrawal.py`.

The instructions mention `processor.py` / `test_processor.py` generically; **this assigned ATM project uses the equivalent filenames `atm_withdrawal.py` / `test_atm_withdrawal.py`**.

## Input-validation decisions

| Function | Valid input | Invalid input behavior |
|---|---|---|
| `notes_needed()` | Nonnegative whole-number string, optionally comma-grouped (e.g., `2,500`) | Returns `0` |
| `mask_card()` | Exactly 16 digits, optional spaces or hyphens | Returns `Invalid card number` |
| `average_withdrawal()` | CSV of nonnegative integers (e.g., `500,1000,2000`) | Returns `0` |

The lab's no-crash requirement motivated these safe-return policies. Production banking systems should instead reject invalid financial transactions with explicit validation errors.

## GitHub submission

After adding all 4 screenshots and generating the report:

```bat
cd ..
git add Lab-7
git commit -m "Complete Lab 7 fuzz testing with evidence and PDF"
git push origin main
```

Avoid committing `.venv`, pytest caches, and temporary workspaces; they are ignored automatically.
