"""
SQL Test Generator Tool (Async + Modular)

Generates test cases and scenarios for SQL queries to validate correctness and logic.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from utils.prompt_manager import PromptManager
from utils.sanitizer import clean_output

class SQLTestGenerator(SQLTask):
    def __init__(self):
        self.client = BaseAIClient()
        self.logger = get_logger("sql_test_generator")

    async def run(self, sql_query: str) -> str:
        """
        Creates SQL test cases based on the logic of the input query.

        :param sql_query: SQL query string
        :return: Test cases and sample input/output for validation
        """
        try:
            self.logger.info("Generating SQL test cases...")

            # Use PromptManager to load the prompt
            prompt = PromptManager.load_prompt(
                "test_generator.unit_tests",
                sql_query=sql_query
            )

            # Send the prompt to the AI model
            result = await self.client.get_completion(prompt, temperature=0.3)
            self.logger.info("SQL test generation completed.")

            return clean_output(result)

        except Exception as e:
            self.logger.error(f"SQL test generation failed: {e}")
            raise RuntimeError(f"SQLTestGenerator error: {e}")
