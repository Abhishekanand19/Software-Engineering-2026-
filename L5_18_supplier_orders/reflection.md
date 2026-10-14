# Lab Reflection

### 1. What is the purpose and scope of static code analysis in the development lifecycle?
Static code analysis analyzes source code without executing the program. Its scope covers early detection of security vulnerabilities, syntax errors, adherence to industry styling standards, and architectural anti-patterns. Integrating it into the workflow catches critical defects before code merges or reaches production environments.

### 2. How do Pylint, Bandit, and Flake8 complement each other?
- **Bandit:** Acts as an AST-based security scanner targeting common vulnerabilities, dangerous system calls (`os.system`), and injection attack vectors.
- **Pylint:** Functions as an in-depth code reviewer, evaluating design quality, unused parameters, variable scoping, broad exception handling, and structural best practices.
- **Flake8:** Enforces PEP 8 grammar, whitespace rules, operator formatting, and line-length limits to maintain stylistic consistency across the codebase.

Together, they provide layered analysis: security (Bandit), structural quality and correctness (Pylint), and readability (Flake8).

### 3. How do fixes for issues like SQL injection and broad exceptions improve software reliability?
- Replacing string concatenation with parameterized SQL prevents malicious inputs from executing unauthorized queries or corrupting database contents.
- Removing bare and broad `except Exception: pass` blocks prevents silent failures, allowing real database connection or schema errors to surface with informative stack traces rather than failing silently.

### 4. What challenges arise when balancing automated tool suggestions with functional requirements?
Automated tools can flag false positives or recommend refactoring signatures (such as unused parameters) that external callers depend upon. Balancing tool suggestions requires prioritizing high and medium severity security issues first, then carefully refactoring naming conventions and exception clauses without altering the runtime behavior of the program.