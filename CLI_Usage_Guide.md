
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
- **`--git`**: Automatically stages the updated file with `git add` for version control.

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

