"""
SQL Refactorer Tool (Async + Modular)

Refactors complex SQL queries into more modular, maintainable components using CTEs, views, or subqueries.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from utils.prompt_manager import PromptManager
from utils.sanitizer import clean_output

class SQLRefactorer(SQLTask):
    def __init__(self):
        self.client = BaseAIClient()
        self.logger = get_logger("sql_refactorer")

    async def run(self, sql_query: str) -> str:
        """
        Refactors the SQL query for better readability, modularity, and performance.

        :param sql_query: SQL query string
        :return: Refactored SQL query
        """
        try:
            self.logger.info("Refactoring SQL query...")

            # Use PromptManager to load the prompt
            prompt = PromptManager.load_prompt(
                "refactorer.improve_modularity",
                sql_query=sql_query
            )

            # Send the prompt to the AI model
            result = await self.client.get_completion(prompt, temperature=0.25)
            self.logger.info("SQL refactoring completed.")

            return clean_output(result)

        except Exception as e:
            self.logger.error(f"SQL refactoring failed: {e}")
            raise RuntimeError(f"SQLRefactorer error: {e}")
