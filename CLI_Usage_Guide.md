# 🧪 GenAI-SQL CLI Usage Guide

This guide provides examples and explanations for using the `GenAI-SQL` CLI (`app.py`) with various task and execution options.

---

## 🧼 Clean and Save to a New File

```bash
python app.py --task=comment --path=example.sql --sanitize --output=cleaned_example.sql
```

### 🔍 What It Does:
- **Task**: `comment` — adds header and inline documentation to `example.sql`.
- **`--sanitize`**: Removes extra GPT explanations or markdown.
- **`--output=...`**: Writes the updated SQL to `cleaned_example.sql` instead of overwriting the original file.

---

## 🔍 Preview Refactored Query (No File Overwrite)

```bash
python app.py --task=refactor --path=query.sql --dry-run
```

### 🔍 What It Does:
- **Task**: `refactor` — rewrites legacy SQL to modern best practices (CTEs, clean formatting).
- **`--dry-run`**: Only shows the result in the terminal, without modifying `query.sql`.

---

## 🗃️ Process All `.sql` Files in a Folder (With Backups)

```bash
python app.py --task=analyze --path=./sql_scripts --recursive --backup
```

### 🔍 What It Does:
- **Task**: `analyze` — finds inefficiencies and suggests performance improvements.
- **`--recursive`**: Processes all `.sql` files in the folder and subfolders.
- **`--backup`**: Creates `.bak` files before overwriting each script.

---

## 🔐 Run Security Audit and Stage for Git

```bash
python app.py --task=audit --path=query.sql --git
```

### 🔍 What It Does:
- **Task**: `audit` — scans `query.sql` for:
  - SQL injection risk
  - PHI/PII exposure
  - Dynamic SQL misuse
  - HIPAA/HITECH flags
- **`--git`**: Automatically stages the updated file with `git add`, making it ready for commit in version control.

---

## 🗣️ Explain Query Logic in Natural Language

```bash
python app.py --task=explain --path=query.sql --output=explanation.txt
```

### 🔍 What It Does:
- **Task**: `explain` — translates the logic of `query.sql` into a natural language explanation, making it easier to understand complex queries.
- **`--output=...`**: Saves the explanation to `explanation.txt`.

---

## 🧪 Generate Unit Test Ideas for SQL Logic

```bash
python app.py --task=test --path=query.sql --output=test_ideas.txt
```

### 🔍 What It Does:
- **Task**: `test` — analyzes `query.sql` and generates unit test ideas to validate its logic.
- **`--output=...`**: Saves the generated test ideas to `test_ideas.txt`.

---

## 📊 Benchmark SQL Query Performance

```bash
python app.py --task=benchmark --path=example.sql --dry-run
```

### 🔍 What It Does:
- **Task**: `benchmark` — simulates query execution to measure performance metrics like:
  - Execution time
  - Index usage
  - Query plan efficiency
- **`--dry-run`**: Displays results in the terminal without altering the original file.

---

## 📈 Visualize Query Execution Plan

```bash
python app.py --task=visualize --path=query.sql --output=query_plan.png
```

### 🔍 What It Does:
- **Task**: `visualize` — generates a graphical representation of the query execution plan.
- **`--output=...`**: Saves the visualization as `query_plan.png`.

---

## 🚀 Convert Natural Language to SQL

### Inline Natural Language Query

```bash
python app.py --task=nl_to_sql --path="list all patients diagnosed with diabetes last month" --sql_dialect="PostgreSQL" --schema_path="schema.json" --dry-run
```

### Natural Language Query from File

```bash
python app.py --task=nl_to_sql --path=nl_query.txt --sql_dialect="T-SQL" --schema_path="schema/HealthClaimsDW.json" --output=generated_query.sql
```

### 🔍 What It Does:
- **Task**: `nl_to_sql` — converts plain language queries into SQL using the specified schema.
- **`--sql_dialect=...`**: Specifies the SQL dialect (e.g., T-SQL, PostgreSQL).
- **`--schema_path=...`**: Points to the schema for generating valid SQL.

---

## 🧠 Tip: Combine Flags

You can combine options for more control:

```bash
python app.py --task=comment --path=query.sql --sanitize --output=query_commented.sql --backup --git
```

- Comments and cleans the SQL
- Saves to a new file
- Backs up the original
- Stages the result for Git commit
- **Note**: Not all tasks can be combined. For example, `audit` and `explain` cannot be used together as they serve different purposes.

---

## 🔒 Mask Sensitive Data in SQL Queries

```bash
python app.py --task=mask --path=example.sql --output=masked_example.sql
```

### 🔍 What It Does:
- **Task**: `mask` — Automatically identifies and masks sensitive data such as:
  - Email addresses.
  - Phone numbers.
  - Credit card numbers.
  - Social Security Numbers (SSNs).
- **`--output=...`**: Writes the masked SQL to a new file.
- **`--dry-run`**: Prints the masked SQL in the terminal without modifying the input file.

---

## 🛠️ Enforce SQL Style Guide

```bash
python app.py --task=style_enforce --path=example.sql --sql_dialect=PostgreSQL --output=styled_example.sql
```

### 🧑‍🏫 What It Does:
- **Task**: `style_enforce` — Enforces SQL coding standards dynamically using AI.
- **`--sql_dialect=...`**: Specifies the SQL dialect (e.g., PostgreSQL, T-SQL).
- **`--output=...`**: Writes the styled SQL to a new file.
- **`--dry-run`**: Displays the AI-styled SQL without saving the changes.

---

## 🔧 Available Tasks

| Task       | Description                                  |
|------------|----------------------------------------------|
| `comment`  | Add header and inline documentation          |
| `analyze`  | Review performance and indexing opportunities|
| `refactor` | Rewrite for readability, modern SQL          |
| `audit`    | Detect security/PII/PHI/HIPAA risks          |
| `explain`  | Translate query logic into natural language  |
| `test`     | Generate unit test ideas for SQL logic       |
| `benchmark`| Simulate query execution and measure performance|
| `visualize`| Generate query execution plan visualizations |
| `nl_to_sql`| Convert natural language to SQL              |
| `mask`     | Mask sensitive data in SQL queries           |
| `style_enforce`| Enforce SQL coding standards             |

---

## 📂 Example Directory Setup

```
project-root/
├── sql_tools/
│   ├── app.py
│   ├── core/
│   ├── tasks/
│   ├── utils/
│   ├── .gitignore
│   ├── .gitattributes
│   ├── README.md
│   └── CLI_Usage_Guide.md
```

---

## 📄 License

See the [MIT License](./LICENSE) for usage terms.

---