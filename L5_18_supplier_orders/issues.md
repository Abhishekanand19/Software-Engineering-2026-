# Static Code Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- |
| SQL Injection (Bandit B608) | Security (High) | 11 | Formatted raw strings directly into an SQL statement via `%s` and `%d`, allowing arbitrary SQL injection. | Replaced string interpolation with parameterized queries using placeholders (`:supplier`, `:item`, `:quantity` or standard positional parameter tuples). |
| Subprocess Shell Injection (Bandit B605/B607) | Security (Medium) | 19 | Used `os.system()` which invokes an underlying system shell, creating command injection risks. | Replaced with `subprocess.run()` passing arguments as a safe list without `shell=True`. |
| Broad Exception Caught (Pylint W0718) | Bug / Quality | 23-26 | Catching generic `Exception` with a silent `pass` swallows unexpected errors and masks bugs. | Replaced broad `Exception` with specific `sqlite3.OperationalError` and logged the error message. |
| Unused Parameter (Pylint W0613) | Code Smell | 15 | `remarks` parameter defined in `markReceived` is never read or used in the function body. | Set default to `remarks=None` and assigned `_ = remarks` to satisfy the interface. |
| Invalid Function Name (Pylint C0103) | Style | 8, 14, 18, 28 | Function names used `camelCase` rather than standard Python `snake_case`. | Renamed functions to `place_order`, `mark_received`, `notify_warehouse`, and `pending_count`. |
| Missing Whitespace / Long Lines (Flake8 E225, E501) | PEP 8 Formatting | 12, 5 | Missing whitespace around `+=` operator and SQL table creation statement exceeded line length limits. | Reformatted statements with proper operator spacing and split long queries across multiple lines. |