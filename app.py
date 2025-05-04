
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
import subprocess
from utils.file_utils import (
    read_sql_file,
    write_sql_file,
    backup_sql_file,
    get_sql_files_in_directory
)
from core.config_loader import Config
from utils.sanitizer import clean_output

# Task imports
from tasks.sql_commenter import SQLCommenter
from tasks.sql_analyzer import SQLAnalyzer
from tasks.sql_refactorer import SQLRefactorer
from tasks.sql_explainer import SQLExplainer
from tasks.sql_security_auditor import SQLSecurityAuditor
from tasks.sql_test_generator import SQLTestGenerator

# Task registry
TASKS = {
    "comment": SQLCommenter,
    "analyze": SQLAnalyzer,
    "refactor": SQLRefactorer,
    "explain": SQLExplainer,
    "audit": SQLSecurityAuditor,
    "test": SQLTestGenerator,
}

async def process_sql_file(filepath, task_class, backup=False, dry_run=False, sanitize=False, output_path=None, git=False):
    print(f"🔍 Processing: {filepath}")
    sql_code = read_sql_file(filepath)
    
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
    parser.add_argument("--path", required=True, help="SQL file or directory path")
    parser.add_argument("--recursive", action="store_true", help="Recursively process folders")
    parser.add_argument("--backup", action="store_true", help="Backup files before modifying")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without saving")
    parser.add_argument("--sanitize", action="store_true", help="Clean output to remove markdown and explanations")
    parser.add_argument("--output", help="Write output to a separate file instead of overwriting")
    parser.add_argument("--git", action="store_true", help="Stage modified files to Git")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print("❌ Provided path does not exist.")
        return

    task_class = TASKS[args.task]

    if os.path.isfile(args.path):
        await process_sql_file(args.path, task_class, args.backup, args.dry_run, args.sanitize, args.output, args.git)
    elif os.path.isdir(args.path):
        sql_files = get_sql_files_in_directory(args.path, recursive=args.recursive)
        if not sql_files:
            print("⚠️ No SQL files found.")
            return
        for file in sql_files:
            await process_sql_file(file, task_class, args.backup, args.dry_run, args.sanitize, None, args.git)

if __name__ == "__main__":
    asyncio.run(main())
