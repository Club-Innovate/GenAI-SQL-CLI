# 🧠 GenAI SQL Tools Suite

A production-ready suite of modular, asynchronous tools for analyzing, refactoring, commenting, and auditing SQL code using Azure OpenAI (GPT-4o).

> Designed with **security**, **performance**, **auditability**, and **HIPAA/HITECH compliance** in mind.

---

## 📁 Project Structure

```
sql_tools/
├── app.py                      # CLI interface and controller
├── requirements.txt
├── README.md
├── LICENSE
├── core/                       # Framework and shared logic
│   ├── base_ai_client.py       # Async Azure OpenAI client
│   ├── config_loader.py        # Configuration loader (mirrors original config.py)
│   ├── logger.py               # HIPAA-compliant logging utility
│   └── sql_task_base.py        # Abstract base class for GenAI SQL tasks
├── tasks/                      # Modular GenAI SQL task classes
│   ├── sql_analyzer.py
│   ├── sql_commenter.py
│   ├── sql_data_masker.py
│   ├── sql_refactorer.py
│   ├── sql_explainer.py
│   ├── sql_security_auditor.py
│   ├── sql_test_generator.py
│   ├── sql_performance_benchmark.py  # New: Added performance benchmarking and optimization
│   ├── sql_data_masker.py           # New: Data masking and anonymization
│   ├── sql_visualizer.py            # New: Visualization and insights
│   ├── sql_error_corrector.py       # New: Error correction and debugging
│   ├── sql_style_enforcer.py        # New: Style guide enforcement
│   ├── natural_language_to_sql.py   # New: Natural language to SQL conversion
├── prompts/                    # Centralized prompt management
│   ├── index.yaml              # YAML file defining all prompts and metadata
│   ├── summarization/          # Summarization-related prompt templates
│   ├── classification/         # Classification-related prompt templates
└── utils/
    ├── file_utils.py           # File I/O, backup, and directory handling
    ├── prompt_manager.py       # Centralized prompt loading and validation
    ├── sanitizer.py            # LLM output cleaner (markdown, GPT comments)
    ├── dynamic_sql_detector.py # New: Utility for dynamic SQL detection
```

---

## ✅ Features

- 🧹 Data Masking and Anonymization - Automatically masks sensitive data such as emails, phone numbers, credit card numbers, and SSNs.
- ⚙️ Modular task engine (comment, analyze, refactor, audit, explain, test)
- 🔍 Query Simulation and Validation
- 📋 Centralized prompt management via `prompts/index.yaml`
- ⚡ Asynchronous OpenAI integration using `httpx`
- 🧼 Sanitized output with `--sanitize`
- 🔁 Directory recursion and batching with `--recursive`
- 🧪 Preview results before modifying files with `--dry-run`
- 🔐 Backup and HIPAA-safe logging
- 🔀 Git integration: auto-stage files with `--git`
- 📤 Export to separate files using `--output`
- 🌐 Support for multiple SQL dialects using nl_to_sql task (e.g., T-SQL, PostgreSQL, Oracle)
- 🚀 Natural Language to SQL Conversion
- 🔐 Enhanced security audits with SQL injection and role misuse detection
- 📊 Performance benchmarking and optimization
- 🔧 Data masking and anonymization
- 🎨 SQL Style Guide Enforcement
- 🛠 Dynamic SQL Detection
- 🧑‍🏫 SQL Education Mode (Interactive Tutorials)

---

## 🧪 CLI Usage

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

### 🔧 Enforce SQL Style Guide
```bash
python app.py --task=style_enforce --path=example.sql --sql_dialect=PostgreSQL --output=styled_example.sql
```

### What It Does:
- **Task**: `style_enforce` — Enforces SQL coding standards dynamically using AI.
- **`--sql_dialect=...`**: Specifies the SQL dialect (e.g., PostgreSQL, T-SQL).
- **`--output=...`**: Writes the styled SQL to a new file.

### 🔧 Comment a SQL file
```bash
python app.py --task=comment --path=example.sql
```

### 🧼 Clean and save to new file
```bash
python app.py --task=comment --path=example.sql --sanitize --output=cleaned_example.sql
```

### 🔍 Preview refactored query (no overwrite)
```bash
python app.py --task=refactor --path=query.sql --dry-run
```

### 🗃️ Process all .sql files in folder (with backups)
```bash
python app.py --task=analyze --path=./sql_scripts --recursive --backup
```

### 🔐 Run security audit and stage for Git
```bash
python app.py --task=audit --path=query.sql --git
```

### 🧪 Generate SQL test cases
```bash
python app.py --task=test --path=example.sql --dry-run
```

### 🚀 Natural Language to SQL Conversion (inline query)
```bash
python app.py --task=nl_to_sql --path="list all patients diagnosed with diabetes last month" --sql_dialect="PostgreSQL" --schema_path="schema/schema.json" --dry-run
```

### 🚀 Natural Language to SQL Conversion (query file)
```bash
python app.py --task=nl_to_sql --path=queries/nl_query.txt --sql_dialect="T-SQL" --schema_path="schema/HealthClaimsDW.json" --output=output/generated_query.sql
```

### 📊 Benchmark SQL query performance
```bash
python app.py --task=benchmark --path=example.sql --dry-run
```

### 📈 Visualize query execution plan
```bash
python app.py --task=visualize --path=example.sql
```

### 🔍 Dynamic SQL Detection

Detect dynamic SQL patterns and analyze risks/optimizations:

#### Analyze risks and optimizations - Detect patterns only:
```bash
python app.py --task=dynamic_sql --path="queries/sample_query.sql" --detect_only --dry-run
```

#### Process all SQL files in a directory recursively:

```bash
python app.py --task=dynamic_sql --path="queries/" --recursive
```

---

## 🛠 Configuration

Edit `core/config_loader.py` to match your Azure OpenAI deployment:

```python
AOPAI_KEY = "your-api-key"
API_BASE = "https://your-resource.openai.azure.com/"
AOPAI_API_VERSION = "2025-01-01-preview"
AOPAI_DEPLOY_MODEL = "gpt-4o-dev"
```

---

## 📦 Install Requirements

```bash
pip install -r requirements.txt
```

---

## 📋 Centralized Prompt Management

All prompts are defined in a single `index.yaml` file, which maps specific tasks to their associated prompt templates. This design enables:

- Consistent prompt formatting
- Easier version control and auditing
- Reusability across multiple modules

Each task class dynamically loads its associated prompt using metadata from this file.

### 🧾 Example `index.yaml` Entry

```yaml
commenter.add_comments:
  inline: |
    "You are a T-SQL expert. Given the SQL code below, please:
    1. Prepend a comment header block with:
       -- =============================================
       -- Author:      {user}
       -- Create date: {timestamp}
       -- Description: <Provide a detailed overview of this query>
       -- =============================================

    2. Add or improve inline comments throughout the query.
    3. Only return the updated SQL code with no markdown formatting.

    SQL Code:
    {sql_query}"
  used_by: tasks.sql_commenter.SQLCommenter
  inputs:
    - sql_query
    - user
    - timestamp
  version: 1.0
  description: Add comments and metadata headers to SQL queries.
```

---

## 🔐 Security & Compliance

- Logs are stored per task under the `logs/` directory
- Safe use of T-SQL comments (`--`, `/* ... */`)
- Output sanitized for code-only results when using `--sanitize`
- Aligned with HIPAA/HITECH compliance standards

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

## 🤝 Contributing

- Fork and open a PR
- Follow modular design and SOLID principles
- Ensure proper logging, error handling, and secure configuration

---

## 🙌 Authors & Acknowledgments

- Vision and engineering by **Hans Esquivel**
- Powered by **Azure OpenAI**
- Thanks to the SQL and ML community for insights and best practices
---
