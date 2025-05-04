
"""
File Utilities for SQL Toolchain

Includes secure file I/O, recursive directory traversal, and backup handling.
"""

import os
import shutil
from datetime import datetime

def read_sql_file(filepath):
    """
    Reads a SQL file and returns its content as a string.

    :param filepath: Path to the SQL file
    :return: SQL string
    """
    with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
        return file.read()

def write_sql_file(filepath, content):
    """
    Writes content to a SQL file, overwriting the existing content.

    :param filepath: File path to write to
    :param content: SQL string content
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

def backup_sql_file(filepath):
    """
    Creates a .bak timestamped backup of a SQL file.

    :param filepath: Path to the original SQL file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{filepath}.{timestamp}.bak"
    shutil.copy2(filepath, backup_path)
    print(f"[🔒 Backup created]: {backup_path}")
    return backup_path

def get_sql_files_in_directory(directory, recursive=True):
    """
    Retrieves all .sql files from a directory (optionally recursively).

    :param directory: Root directory path
    :param recursive: Whether to search subdirectories
    :return: List of full file paths
    """
    sql_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".sql") and not file.endswith(".bak.sql"):
                sql_files.append(os.path.join(root, file))
        if not recursive:
            break
    return sql_files
