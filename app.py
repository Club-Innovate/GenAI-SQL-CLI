"""
GenAI SQL Tool Runner

Command-line interface to execute GenAI SQL tasks (commenting, analysis, auditing, etc.)
across single files or directories.

Usage:
    python app.py --task=comment --path="queries/" --backup --log --dry-run
"""

import argparse
import asyncio
import os
import sys
import subprocess
from utils.file_utils import (
    read_sql_file,
    write_sql_file,
    backup_sql_file,
    get_sql_files_in_directory
)
from core.config_loader import Config
from utils.sanitizer import clean_output
from utils.prompt_manager import PromptManager
from core.base_ai_client import AIClient

# Task imports
from tasks.sql_commenter import SQLCommenter
from tasks.sql_analyzer import SQLAnalyzer
from tasks.sql_refactorer import SQLRefactorer
from tasks.sql_explainer import SQLExplainer
from tasks.sql_security_auditor import EnhancedSQLSecurityAuditor
from tasks.sql_test_generator import SQLTestGenerator
from tasks.sql_performance_benchmark import SQLPerformanceBenchmark
from tasks.sql_query_validator import SQLQueryValidator
from tasks.natural_language_to_sql import NaturalLanguageToSQL
from tasks.sql_data_masker import SQLDataMasker
from tasks.sql_style_enforcer import SQLStyleEnforcer
from utils.dynamic_sql_detector import DynamicSQLDetector

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
sys.path.insert(0, project_root)

# Task registry
TASKS = {
    "comment": SQLCommenter,
    "analyze": SQLAnalyzer,
    "refactor": SQLRefactorer,
    "explain": SQLExplainer,
    "audit": EnhancedSQLSecurityAuditor,
    "test": SQLTestGenerator,
    "benchmark": SQLPerformanceBenchmark,
    "validate": SQLQueryValidator,
    "nl_to_sql": NaturalLanguageToSQL,
    "mask": SQLDataMasker,
    "style_enforce": SQLStyleEnforcer,  # SQL Style Guide Enforcement
    "dynamic_sql": DynamicSQLDetector,  # Dynamic SQL Detection
}


async def process_sql_file(filepath, task_class, backup=False, dry_run=False, sanitize=False, output_path=None, git=False, **kwargs):
    print(f"🔍 Processing: {filepath}")
    sql_code = read_sql_file(filepath)

    # Initialize AI client and prompt manager (used by AI-driven tasks)
    ai_client = AIClient()
    prompt_manager = PromptManager("prompts/index.yaml")

    # Special logic for SQLDataMasker
    if task_class == SQLDataMasker:
        task = task_class()
        result = task.mask_sensitive_data(sql_code)
    elif task_class == SQLStyleEnforcer:
        # Handle specific logic for SQL Style Enforcement
        task = task_class(ai_client, prompt_manager)
        result = await task.enforce_style(sql_code, kwargs.get("sql_dialect", "generic"))
    elif task_class == NaturalLanguageToSQL:
        # Handle specific logic for NaturalLanguageToSQL
        nl_query = sql_code  # Treat the file content as the natural language query
        schema_path = kwargs.get("schema_path", "schema.json")
        sql_dialect = kwargs.get("sql_dialect", "generic")

        task = task_class(schema_file=schema_path)
        result = await task.run(nl_query, sql_dialect=sql_dialect)
    elif task_class == DynamicSQLDetector:
        # Handle specific logic for Dynamic SQL Detection
        task = task_class(ai_client, prompt_manager)
        if kwargs.get("detect_only", False):
            result = await task.detect_dynamic_sql(sql_code)
        else:
            result = await task.analyze_risks_and_optimization(sql_code)
    else:
        task = task_class()
        result = await task.run(sql_code)

    if sanitize:
        result = clean_output(result)

    if dry_run:
        print("🧪 Dry run output:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        return

    if backup:
        backup_sql_file(filepath)

    if output_path:
        write_sql_file(output_path, result)
        print(f"📤 Output written to: {output_path}")
    else:
        write_sql_file(filepath, result)
    print(f"✅ Updated: {filepath}")

    if git and not output_path:
        try:
            subprocess.run(["git", "add", filepath], check=True)
            print(f"✅ Git staged: {filepath}")
        except Exception as e:
            print(f"⚠️ Git stage failed: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Run GenAI SQL tools.")
    parser.add_argument("--task", required=True, choices=TASKS.keys(), help="Task to perform")
    parser.add_argument("--path", required=True, help="SQL file, directory path, or natural language query")
    parser.add_argument("--recursive", action="store_true", help="Recursively process folders")
    parser.add_argument("--backup", action="store_true", help="Backup files before modifying")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without saving")
    parser.add_argument("--sanitize", action="store_true", help="Clean output to remove markdown and explanations")
    parser.add_argument("--output", help="Write output to a separate file instead of overwriting")
    parser.add_argument("--git", action="store_true", help="Stage modified files to Git")
    parser.add_argument("--sql_dialect", required=False, help="SQL dialect to use (e.g., T-SQL, PostgreSQL).")
    parser.add_argument("--schema_path", help="Path to the JSON schema file.", default="schema.json")  # Default to 'schema.json'
    parser.add_argument("--detect_only", action="store_true", help="Only detect dynamic SQL patterns without analyzing risks or optimizations (specific to 'dynamic_sql' task).")

    args = parser.parse_args()

    task_class = TASKS[args.task]

    # Special handling for NaturalLanguageToSQL
    if args.task == "nl_to_sql":
        schema_path = args.schema_path
        sql_dialect = args.sql_dialect or "generic"

        # Check if --path is a file, directory, or direct natural language query
        if os.path.exists(args.path):
            # If it's a file, read the query from the file
            if os.path.isfile(args.path):
                with open(args.path, "r", encoding="utf-8") as f:
                    nl_query = f.read().strip()
            else:
                print("❌ Provided path is a directory. For nl_to_sql, provide a file or direct query.")
                return
        else:
            # Treat --path as a direct natural language query
            nl_query = args.path

        # Instantiate the NaturalLanguageToSQL task
        task_instance = task_class(schema_file=schema_path)
        result = await task_instance.run(nl_query, sql_dialect=sql_dialect)

        # Output result
        if args.dry_run:
            print("🧪 Dry run output:")
            print("-" * 60)
            print(result)
            print("-" * 60)
        elif args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"📤 Output written to: {args.output}")
        else:
            print(f"Generated SQL Query:\n{result}")
        return

    # For other tasks
    if os.path.exists(args.path):
        if os.path.isfile(args.path):
            await process_sql_file(
                args.path, 
                task_class, 
                args.backup, 
                args.dry_run, 
                args.sanitize, 
                args.output, 
                args.git, 
                schema_path=args.schema_path, 
                sql_dialect=args.sql_dialect, 
                detect_only=args.detect_only
            )
        elif os.path.isdir(args.path):
            sql_files = get_sql_files_in_directory(args.path, recursive=args.recursive)
            if not sql_files:
                print("⚠️ No SQL files found.")
                return
            for file in sql_files:
                await process_sql_file(
                    file, 
                    task_class, 
                    args.backup, 
                    args.dry_run, 
                    args.sanitize, 
                    None, 
                    args.git, 
                    schema_path=args.schema_path, 
                    sql_dialect=args.sql_dialect, 
                    detect_only=args.detect_only
                )
    else:
        print("❌ Provided path does not exist.")


if __name__ == "__main__":
    asyncio.run(main())