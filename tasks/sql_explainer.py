
"""
SQL Explainer Tool (Async + Modular)

Provides a step-by-step explanation of SQL queries for educational and onboarding use cases.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
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
            prompt = (
                "Explain the following SQL query step-by-step in simple, human-readable language. "
                "Cover what each clause (SELECT, WHERE, JOIN, etc.) is doing. "
                "If there are subqueries, CTEs, or window functions, explain those as well. "
                "Only return the explanation in plain text.\n\n"
                f"{sql_query}"
            )
            result = await self.client.get_completion(prompt, temperature=0.3)
            self.logger.info("SQL explanation generated successfully.")

            return clean_output(result)

        except Exception as e:
            self.logger.error(f"SQL explanation failed: {e}")
            raise RuntimeError(f"SQLExplainer error: {e}")
