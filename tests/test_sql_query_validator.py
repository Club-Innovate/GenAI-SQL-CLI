import sys
import os
import pytest
from unittest.mock import AsyncMock

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from tasks.sql_query_validator import SQLQueryValidator  # Import after setting the path


@pytest.mark.asyncio
async def test_sql_query_validator():
    # Initialize the validation task
    validator_task = SQLQueryValidator()

    # Mock SQL input
    sql_query = "SELECT name, age FROM users WHERE active = true;"

    # Mock expected output (example)
    expected_output = (
        "Validation Results:\n"
        "- Syntax: No errors detected.\n"
        "- Logical Check: Query is logically sound.\n"
        "- Suggestions:\n"
        "  - Consider adding an index on the 'active' column for better performance.\n"
    )

    # Mock the AI client's get_completion method
    validator_task.client.get_completion = AsyncMock(return_value=expected_output)

    # Run the task
    result = await validator_task.run(sql_query)

    # Assert the results
    assert result == expected_output