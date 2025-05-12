"""
SQL Query Validator Tool (Async)

Simulates query execution and validates SQL syntax and logic.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from utils.prompt_manager import PromptManager
from utils.sanitizer import clean_output


class SQLQueryValidator(SQLTask):
    def __init__(self):
        self.client = BaseAIClient()
        self.logger = get_logger("sql_query_validator")

    async def run(self, sql_query: str) -> str:
        """
        Simulates and validates SQL queries.

        :param sql_query: SQL query string
        :return: Validation results and simulation feedback
        """
        try:
            self.logger.info("Validating SQL query...")

            # Use PromptManager to load the validation prompt
            prompt = PromptManager.load_prompt(
                "query_validator.simulate_and_validate",
                sql_query=sql_query
            )

            # Send the prompt to the AI model
            result = await self.client.get_completion(prompt, temperature=0.3)
            cleaned = clean_output(result)

            self.logger.info("SQL query validation completed.")
            return cleaned

        except Exception as e:
            self.logger.error(f"SQL Query Validation failed: {e}")
            raise RuntimeError(f"SQLQueryValidator error: {e}")
