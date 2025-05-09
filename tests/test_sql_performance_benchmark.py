import pytest
from tasks.sql_performance_benchmark import SQLPerformanceBenchmark


@pytest.mark.asyncio
async def test_sql_performance_benchmark():
    # Initialize the benchmarking task
    benchmark_task = SQLPerformanceBenchmark()

    # Mock SQL input
    sql_query = "SELECT * FROM employees WHERE department = 'Engineering';"

    # Mock expected output (example)
    expected_output = (
        "Estimated execution time: 0.02s\n"
        "Optimization Suggestions:\n"
        "- Add an index on the 'department' column.\n"
        "- Avoid SELECT * and specify required columns.\n"
    )

    # Mock the AI client's response
    benchmark_task.client.get_completion = lambda prompt, temperature: expected_output

    # Run the task
    result = await benchmark_task.run(sql_query)

    # Assert the results
    assert result == expected_output
