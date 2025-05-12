"""
Natural Language to SQL Conversion Tool (Async)

Converts natural language queries into valid SQL queries.
"""

import json
import os
import sys
from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from utils.prompt_manager import PromptManager
from utils.sanitizer import clean_output

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


class NaturalLanguageToSQL(SQLTask):
    def __init__(self, schema_file: str = "schema.json"):
        self.client = BaseAIClient()
        self.logger = get_logger("natural_language_to_sql")
        self.schema_file = schema_file
        self.schema = self._load_schema()

    def _load_schema(self):
        """
        Load the schema JSON file.
        """
        try:
            with open(self.schema_file, "r") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load schema file: {e}")
            raise RuntimeError(f"Schema file loading error: {e}")

    async def run(self, nl_query: str, sql_dialect: str = "generic") -> str:
        """
        Converts natural language queries into SQL using the predefined schema.

        :param nl_query: Natural language query string.
        :param sql_dialect: SQL dialect (e.g., MySQL, PostgreSQL, SQLite).
        :return: Generated SQL query.
        """
        try:
            self.logger.info("Converting natural language query to SQL...")

            # Load the prompt
            prompt = PromptManager.load_prompt(
                "nl_to_sql.convert",
                nl_query=nl_query,
                sql_dialect=sql_dialect,
                schema=json.dumps(self.schema)  # Pass the schema as a JSON string
            )

            # Generate SQL query
            result = await self.client.get_completion(prompt, temperature=0.3)
            return clean_output(result).strip()

        except Exception as e:
            self.logger.error(f"Natural Language to SQL conversion failed: {e}")
            raise RuntimeError(f"NaturalLanguageToSQL error: {e}")
