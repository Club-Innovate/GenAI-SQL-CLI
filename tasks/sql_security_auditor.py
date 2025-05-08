"""
SQL Security Auditor Tool (Async + Modular)

Audits SQL queries for security risks, compliance flags (HIPAA/HITECH), and unsafe coding practices.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from utils.prompt_manager import PromptManager
from utils.sanitizer import clean_output

class SQLSecurityAuditor(SQLTask):
    def __init__(self):
        self.client = BaseAIClient()
        self.logger = get_logger("sql_security_auditor")

    async def run(self, sql_query: str) -> str:
        """
        Audits the SQL query for security vulnerabilities and compliance risks.

        :param sql_query: SQL query string
        :return: List of potential security issues and best practice violations
        """
        try:
            self.logger.info("Auditing SQL query for security and compliance...")

            # Use PromptManager to load the prompt
            prompt = PromptManager.load_prompt(
                "auditor.security_audit",
                sql_query=sql_query
            )

            # Send the prompt to the AI model
            result = await self.client.get_completion(prompt, temperature=0.25)
            self.logger.info("SQL security audit completed.")

            return clean_output(result)

        except Exception as e:
            self.logger.error(f"SQL security audit failed: {e}")
            raise RuntimeError(f"SQLSecurityAuditor error: {e}")
