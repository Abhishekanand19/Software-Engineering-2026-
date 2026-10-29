# Lab 6 — ATM Withdrawal: Code and Branch Coverage

**Student:** Abhishek Anand · **SRN:** PES1UG24CS017

**Assigned repository:** https://github.com/SETAPESU26/L6_L7_18_atm_withdrawal  
**Submission repository:** https://github.com/Abhishekanand19/Software-Engineering-2026-

The application file `atm_withdrawal.py` and the starter tests `test_atm_withdrawal.py` have been copied unchanged from the assigned repository. Only the new test suites have been added.

## Run tests from the Lab-06-ATM-Withdrawal folder

Install dependencies once:

```powershell
py -m pip install pytest coverage
```

### Screenshot 1 — code coverage

```powershell
py -m coverage erase
py -m coverage run --source=atm_withdrawal -m pytest -q CodeCoverageTest_atm_withdrawal_application.py
py -m coverage report -m
```

Take a real VS Code terminal screenshot *now*, including the test results and total coverage row. Save as `screenshots/code-coverage.png`.

### Screenshot 2 — branch coverage

```powershell
py -m coverage erase
py -m coverage run --branch --source=atm_withdrawal -m pytest -q BranchCoverageTest_atm_withdrawal_application.py
py -m coverage report -m
```

Take another real VS Code terminal screenshot *now*, including the Branch column and total coverage row. Save as `screenshots/branch-coverage.png`.

## Verification

Local test verification (run against the original application):

| Measure | Tests passed | Coverage |
|---|---:|---:|
| Code coverage | 13 | 100% (34 of 34 statements) |
| Branch coverage | 28 | 100% (22 of 22 branches) |

The screenshots must show your own VS Code run. Re-run the exact commands if the local environment produces different results. The PowerShell automation supplied with the downloadable bundle stops twice for screenshots and creates two commits, including the matching test suite and screenshot in each commit.

Do not commit `.coverage`, `.pytest_cache`, `__pycache__`, or virtual environments.
