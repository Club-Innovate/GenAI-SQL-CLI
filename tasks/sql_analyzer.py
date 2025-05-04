
"""
SQL Analyzer Tool (Async + Modular)

Analyzes SQL queries for optimization opportunities, formatting issues, and best practices using Azure OpenAI.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from utils.sanitizer import clean_output

class SQLAnalyzer(SQLTask):
    def __init__(self):
        self.client = BaseAIClient()
        self.logger = get_logger("sql_analyzer")

    async def run(self, sql_query: str) -> str:
        """
        Executes the SQL optimization analysis.

        :param sql_query: SQL query string
        :return: LLM-generated analysis and optimization suggestions
        """

        try:
            self.logger.info("Analyzing SQL query...")
            prompt = (
                "Analyze the following SQL query for potential performance improvements. "
                "Identify anti-patterns, missing indexes, excessive joins, and suggest refactoring. "
                "Use SQL best practices. Avoid SELECT * if found. Recommend using CTEs or window functions if relevant.\n\n"
                f"{sql_query}"
            )
            result = await self.client.get_completion(prompt, temperature=0.2)
            self.logger.info("SQL analysis completed successfully.")

            return result

        except Exception as e:
            self.logger.error(f"SQL analysis failed: {e}")
            raise RuntimeError(f"SQLAnalyzer error: {e}")
