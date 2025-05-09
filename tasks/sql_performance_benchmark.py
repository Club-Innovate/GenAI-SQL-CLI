"""
SQL Performance Benchmark Tool (Async + Modular)

Simulates query execution and provides performance metrics and optimization suggestions.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from utils.prompt_manager import PromptManager
from utils.sanitizer import clean_output


class SQLPerformanceBenchmark(SQLTask):
    def __init__(self):
        self.client = BaseAIClient()
        self.logger = get_logger("sql_performance_benchmark")

    async def run(self, sql_query: str) -> str:
        """
        Simulates query execution and provides performance metrics.

        :param sql_query: SQL query string
        :return: Performance insights and optimization suggestions
        """
        try:
            self.logger.info("Simulating SQL query execution...")

            # Use PromptManager to load the prompt
            prompt = PromptManager.load_prompt(
                "performance_benchmark.simulate",
                sql_query=sql_query
            )

            # Send the prompt to the AI model
            result = await self.client.get_completion(prompt, temperature=0.3)
            cleaned = clean_output(result)

            self.logger.info("SQL performance benchmarking completed.")
            return cleaned

        except Exception as e:
            self.logger.error(f"SQL Performance Benchmarking failed: {e}")
            raise RuntimeError(f"SQLPerformanceBenchmark error: {e}")
