import sys
import os
import pytest
from unittest.mock import AsyncMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Import the EnhancedSQLSecurityAuditor task
from tasks.sql_security_auditor import EnhancedSQLSecurityAuditor


@pytest.mark.asyncio
async def test_enhanced_sql_security_auditor():
    # Initialize the security auditor
    auditor_task = EnhancedSQLSecurityAuditor()

    # Mock SQL input
    sql_query = "SELECT * FROM users WHERE username = 'admin' AND password = 'password123';"

    # Mock expected output (example)
    expected_output = (
        "Security Audit Report:\n"
        "- Vulnerability: SQL Injection (Critical)\n"
        "  - Issue: User input directly used in the query without sanitization.\n"
        "  - Remediation: Use parameterized queries or prepared statements.\n"
        "- Vulnerability: Accessing Sensitive Data (High)\n"
        "  - Issue: Query accesses sensitive fields like 'password'.\n"
        "  - Remediation: Encrypt sensitive fields and restrict access.\n"
    )

    # Mock the AI client's get_completion method
    auditor_task.client.get_completion = AsyncMock(return_value=expected_output)

    # Run the task
    result = await auditor_task.run(sql_query)

    # Strip trailing whitespace before asserting equality
    assert result.strip() == expected_output.strip()