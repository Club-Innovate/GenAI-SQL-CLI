# Extended Sample CLI Commands for GenAI SQL Tool Runner

This document contains extended sample CLI commands for each task supported by the GenAI SQL Tool Runner. The commands include various combinations of parameters/arguments to demonstrate flexibility.

---

## 1. SQL Commenter
Adds comments to SQL files.

### Process a single file with a backup and dry run:
```bash
python app.py --task=comment --path="queries/sample_query.sql" --backup --dry-run
```

### Process all SQL files in a directory recursively:
```bash
python app.py --task=comment --path="queries/" --recursive --backup
```

### Process a single file and save the output to a new file:
```bash
python app.py --task=comment --path="queries/sample_query.sql" --output="output/commented_query.sql"
```

---

## 2. SQL Analyzer
Analyzes SQL queries.

### Analyze a single file with a dry run:
```bash
python app.py --task=analyze --path="queries/sample_query.sql" --dry-run
```

### Analyze SQL files in a directory recursively:
```bash
python app.py --task=analyze --path="queries/" --recursive
```

### Analyze a single file and sanitize the output:
```bash
python app.py --task=analyze --path="queries/sample_query.sql" --sanitize
```

---

## 3. SQL Refactorer
Refactors SQL files.

### Refactor a single file with a backup and dry run:
```bash
python app.py --task=refactor --path="queries/sample_query.sql" --backup --dry-run
```

### Refactor all SQL files in a directory recursively:
```bash
python app.py --task=refactor --path="queries/" --recursive --backup
```

### Refactor a single file and save the output to a new file:
```bash
python app.py --task=refactor --path="queries/sample_query.sql" --output="output/refactored_query.sql"
```

---

## 4. SQL Explainer
Explains the purpose of SQL queries in a human-readable format.

### Explain a single file with a dry run:
```bash
python app.py --task=explain --path="queries/sample_query.sql" --dry-run
```

### Explain all SQL files in a directory recursively:
```bash
python app.py --task=explain --path="queries/" --recursive --backup
```

---

## 5. Enhanced SQL Security Auditor
Audits SQL files for potential security issues.

### Audit a single file with a dry run:
```bash
python app.py --task=audit --path="queries/sample_query.sql" --dry-run
```

### Audit all SQL files in a directory recursively:
```bash
python app.py --task=audit --path="queries/" --recursive --backup
```

### Audit a single file and save the output to a new file:
```bash
python app.py --task=audit --path="queries/sample_query.sql" --output="output/audited_query.sql"
```

---

## 6. SQL Test Generator
Generates SQL test cases.

### Generate tests for a single file with a dry run:
```bash
python app.py --task=test --path="queries/sample_query.sql" --dry-run
```

### Generate tests for all SQL files in a directory recursively:
```bash
python app.py --task=test --path="queries/" --recursive
```

### Generate tests for a single file and save the output to a new file:
```bash
python app.py --task=test --path="queries/sample_query.sql" --output="output/tests.sql"
```

---

## 7. SQL Performance Benchmark
Benchmarks SQL query performance.

### Benchmark a single file with a dry run:
```bash
python app.py --task=benchmark --path="queries/sample_query.sql" --dry-run
```

### Benchmark all SQL files in a directory recursively:
```bash
python app.py --task=benchmark --path="queries/" --recursive
```

### Benchmark a single file with a backup and save the output to a new file:
```bash
python app.py --task=benchmark --path="queries/sample_query.sql" --backup --output="output/benchmark_results.sql"
```

---

## 8. SQL Query Validator
Validates SQL queries.

### Validate a single file with a dry run:
```bash
python app.py --task=validate --path="queries/sample_query.sql" --dry-run
```

### Validate all SQL files in a directory recursively:
```bash
python app.py --task=validate --path="queries/" --recursive
```

### Validate a single file and stage it for Git:
```bash
python app.py --task=validate --path="queries/sample_query.sql" --git
```

---

## 9. Natural Language to SQL (with a file)
Reads the natural language query from a file and generates SQL using the specified schema.

### Generate SQL from a file with a dry run:
```bash
python app.py --task=nl_to_sql --path="queries/nl_query.txt" --sql_dialect="T-SQL" --schema_path="schema/HealthClaimsDW.json" --dry-run
```

### Generate SQL from a file and save the output to a new file:
```bash
python app.py --task=nl_to_sql --path="queries/nl_query.txt" --sql_dialect="T-SQL" --schema_path="schema/HealthClaimsDW.json" --output="output/generated_query.sql"
```

---

## 10. Natural Language to SQL (with an inline query)
Processes an inline natural language query and generates SQL using the specified schema.

### Generate SQL from an inline query with a dry run:
```bash
python app.py --task=nl_to_sql --path="list all patients that were diagnosed with diabetes last month" --sql_dialect="T-SQL" --schema_path="schema/HealthClaimsDW.json" --dry-run
```

### Generate SQL from an inline query and save the output to a new file:
```bash
python app.py --task=nl_to_sql --path="list all patients that were diagnosed with diabetes last month" --sql_dialect="T-SQL" --schema_path="schema/HealthClaimsDW.json" --output="output/generated_query.sql"
```

### Generate SQL from an inline query using a different SQL dialect:
```bash
python app.py --task=nl_to_sql --path="list all patients that were diagnosed with diabetes last month" --sql_dialect="PostgreSQL" --schema_path="schema/HealthClaimsDW.json" --dry-run
```

---

## 11. SQL Data Masker
Masks sensitive data in SQL queries.

### Mask sensitive data in a single file with a dry run:
```bash
python app.py --task=mask --path="queries/sample_query.sql" --dry-run
```

### Mask sensitive data in all SQL files in a directory recursively:
```bash
python app.py --task=mask --path="queries/" --recursive
```

### Mask sensitive data in a single file and save the output:
```bash
python app.py --task=mask --path="queries/sample_query.sql" --output="output/masked_query.sql"
```

---

## 12. SQL Style Guide Enforcement
Enforces SQL coding standards.

### Enforce SQL style guide for a single file with a dry run:
```bash
python app.py --task=style_enforce --path="queries/sample_query.sql" --sql_dialect="PostgreSQL" --dry-run
```

### Enforce SQL style guide in all SQL files in a directory recursively:
```bash
python app.py --task=style_enforce --path="queries/" --recursive --sql_dialect="T-SQL"
```

### Enforce SQL style guide for a single file and save the output:
```bash
python app.py --task=style_enforce --path="queries/sample_query.sql" --sql_dialect="PostgreSQL" --output="output/styled_query.sql"
```

---

## 13. Dynamic SQL Detection
Identifies and analyzes dynamically generated SQL for risks and optimizations.

### Detect patterns only:
```bash
python app.py --task=dynamic_sql --path="queries/sample_query.sql" --detect_only --dry-run
```

### Analyze risks and optimizations:
```bash
python app.py --task=dynamic_sql --path="queries/sample_query.sql" --dry-run
```

### Process all SQL files in a directory recursively:
```bash
python app.py --task=dynamic_sql --path="queries/" --recursive
```

---

## 14. SQL Learning Mode

SQL Education Mode uses a conversational AI command-line interface. The implementation will feature quizzes, a practice code editor, walkthrough examples, and text-based guidance. It will also be secure, performant, and compliant with best practices.

### Run the Learning Mode directly:

```bash
python learn/sql_learn_mode.py
```