"""
Enhanced SQL Security Auditor Tool (Async)

Analyzes SQL queries for potential security vulnerabilities and provides remediation steps.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
from utils.prompt_manager import PromptManager
from utils.sanitizer import clean_output


class EnhancedSQLSecurityAuditor(SQLTask):
    def __init__(self):
        self.client = BaseAIClient()
        self.logger = get_logger("enhanced_sql_security_auditor")

    async def run(self, sql_query: str) -> str:
        """
        Analyzes SQL queries for security vulnerabilities.

        :param sql_query: SQL query string
        :return: Security audit report with vulnerabilities and remediation steps
        """
        try:
            self.logger.info("Starting security audit for SQL query...")

            # Use PromptManager to load the security audit prompt
            prompt = PromptManager.load_prompt(
                "security_audit.enhanced",
                sql_query=sql_query
            )

            # Send the prompt to the AI model
            result = await self.client.get_completion(prompt, temperature=0.3)
            cleaned = clean_output(result)

            self.logger.info("Security audit completed.")
            return cleaned

        except Exception as e:
            self.logger.error(f"SQL Security Audit failed: {e}")
            raise RuntimeError(f"EnhancedSQLSecurityAuditor error: {e}")