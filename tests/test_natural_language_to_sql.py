import sys
import os
import pytest
from unittest.mock import AsyncMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# Import the NaturalLanguageToSQL task
from tasks.natural_language_to_sql import NaturalLanguageToSQL


@pytest.mark.asyncio
async def test_natural_language_to_sql_with_schema():
    # Initialize the NL to SQL converter
    nl_to_sql_task = NaturalLanguageToSQL(schema_file="schema/HealthClaimsDW.json")

    # Mock natural language input
    nl_query = "Get list of all patients were diagnosed with diabetes last month."
    sql_dialect = "T-SQL"

    # Mock expected SQL output
    expected_sql = "SELECT * FROM users WHERE created_at >= NOW() - INTERVAL '1 month';"

    # Mock the AI client's get_completion method
    nl_to_sql_task.client.get_completion = AsyncMock(return_value=expected_sql)

    # Run the task
    result = await nl_to_sql_task.run(nl_query, sql_dialect)

    # Assert the results
    assert result.strip() == expected_sql.strip()