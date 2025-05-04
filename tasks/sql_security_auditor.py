
"""
SQL Security Auditor Tool (Async + Modular)

Audits SQL queries for security risks, compliance flags (HIPAA/HITECH), and unsafe coding practices.
"""

from core.base_ai_client import BaseAIClient
from core.sql_task_base import SQLTask
from core.logger import get_logger
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
            prompt = (f"""
Perform a security audit on the following SQL query. 

Identify any of the following:
- SQL Injection vulnerabilities
- Improper data exposure (especially PHI/PII)
- Absence of access controls
- Unsafe use of dynamic SQL
- HIPAA or HITECH compliance risks

Provide a list of findings with recommendations.

SQL Code:
{sql_query}
"""
            )
            result = await self.client.get_completion(prompt, temperature=0.25)
            self.logger.info("SQL security audit completed.")

            return clean_output(result)

        except Exception as e:
            self.logger.error(f"SQL security audit failed: {e}")
            raise RuntimeError(f"SQLSecurityAuditor error: {e}")
