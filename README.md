
# 🧠 GenAI SQL Tools Suite

A production-ready suite of modular, asynchronous tools for analyzing, refactoring, commenting, and auditing SQL code using Azure OpenAI (GPT-4o).

> Designed with **security**, **performance**, **auditability**, and **HIPAA/HITECH compliance** in mind.

---

## 📁 Project Structure

```
consolidated_sql_tools/
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
│   ├── sql_refactorer.py
│   ├── sql_explainer.py
│   ├── sql_security_auditor.py
│   └── sql_test_generator.py
└── utils/
    ├── file_utils.py           # File I/O, backup, and directory handling
    └── sanitizer.py            # LLM output cleaner (markdown, GPT comments)
```

---

## ✅ Features

- ⚙️ Modular task engine (`comment`, `analyze`, `refactor`, `audit`, `explain`, `test`)
- ⚡ Asynchronous OpenAI integration using `httpx`
- 🧼 Sanitized output with `--sanitize`
- 🔁 Directory recursion and batching with `--recursive`
- 🧪 Preview results before modifying files with `--dry-run`
- 🔐 Backup and HIPAA-safe logging
- 🔀 Git integration: auto-stage files with `--git`
- 📤 Export to separate files using `--output`

---

## 🧪 CLI Usage

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

## 🔐 Security & Compliance

- Logs are created per task, stored in `logs/`
- T-SQL comments (`--`) and block-comments (`/* ... */`) used safely
- Sanitizer ensures only code is preserved when `--sanitize` is enabled
- Designed to meet HIPAA/HITECH guidelines

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

---

## 🤝 Contributing

- Fork and open a PR
- Stick to modular design and SOLID principles
- Ensure logging, error handling, and configuration security

---

## 🙌 Authors & Acknowledgments

- Vision and engineering by Hans Esquivel
- Powered by Azure OpenAI
- Special thanks to the SQL and ML community for best practices
