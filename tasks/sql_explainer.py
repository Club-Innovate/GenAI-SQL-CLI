"""
SQL Explainer Tool (Async + Modular)

Provides a step-by-step explanation of SQL queries for educational and onboarding use cases.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from utils.prompt_manager import PromptManager
from utils.sanitizer import clean_output

class SQLExplainer(SQLTask):
    def __init__(self):
        self.client = BaseAIClient()
        self.logger = get_logger("sql_explainer")

    async def run(self, sql_query: str) -> str:
        """
        Generates a detailed, human-readable explanation of the SQL query.

        :param sql_query: SQL query string
        :return: Natural language explanation of the SQL logic
        """
        try:
            self.logger.info("Explaining SQL query...")

            # Use PromptManager to load the prompt
            prompt = PromptManager.load_prompt(
                "explainer.step_by_step",
                sql_query=sql_query
            )

            # Send the prompt to the AI model
            result = await self.client.get_completion(prompt, temperature=0.3)
            self.logger.info("SQL explanation generated successfully.")

            return clean_output(result)

        except Exception as e:
            self.logger.error(f"SQL explanation failed: {e}")
            raise RuntimeError(f"SQLExplainer error: {e}")
