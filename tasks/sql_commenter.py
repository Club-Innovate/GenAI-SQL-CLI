
"""
SQL Commenter Tool (Async + Modular)

Adds standardized headers and inline comments to SQL queries using Azure OpenAI.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from datetime import datetime
import getpass
import re
from utils.sanitizer import clean_output

class SQLCommenter(SQLTask):
    def __init__(self):
        self.client = BaseAIClient()
        self.logger = get_logger("sql_commenter")
        self.user = getpass.getuser()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def run(self, sql_query: str) -> str:
        """
        Adds comments and metadata headers to the SQL query.

        :param sql_query: SQL query string
        :return: Commented SQL string
        """

        try:
            self.logger.info("Generating SQL comments...")

            prompt = f"""
You are a T-SQL expert. Given the SQL code below, please:
1. Prepend a comment header block with:
   -- =============================================
   -- Author:      {self.user}
   -- Create date: {self.timestamp}
   -- Description: <Provide a detailed overview of this query>
   -- =============================================

2. Add or improve inline comments throughout the query.
3. Only return the updated SQL code with no markdown formatting.

SQL Code:
{sql_query}
"""
            result = await self.client.get_completion(prompt, temperature=0.2)
            cleaned = self._sanitize_output(result)

            self.logger.info("SQL commenting completed.")

            return clean_output(result)

        except Exception as e:
            self.logger.error(f"SQL commenting failed: {e}")
            raise RuntimeError(f"SQLCommenter error: {e}")

    def _sanitize_output(self, output: str) -> str:
        """
        Removes markdown fences and trailing explanation sections.

        :param output: Raw LLM output
        :return: Cleaned SQL string
        """
        output = re.sub(r"(?i)```(?:sql)?\s*", "", output.strip())
        output = re.sub(r"(?i)\s*```", "", output.strip())
        output = re.sub(r"(?i)### Explanation:.*", "", output.strip(), flags=re.DOTALL)

        return output.strip()
