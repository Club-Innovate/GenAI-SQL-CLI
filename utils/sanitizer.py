
"""
Final SQL Block Extractor and Sanitizer

Isolates the SQL code block and wraps only the surrounding prose in a block comment.
"""

import re

def clean_output(raw: str) -> str:
    """
    Extracts SQL code between ```sql ... ``` or returns full content if no fences,
    and wraps any surrounding commentary in a T-SQL block comment.

    :param raw: LLM raw response
    :return: Sanitized SQL code + optionally wrapped recommendations
    """
    raw = raw.strip()

    # Try to extract the ```sql ... ``` fenced block
    match = re.search(r"```sql\s*(.*?)\s*```", raw, re.DOTALL | re.IGNORECASE)
    if match:
        sql_code = match.group(1).strip()
        before = raw[:match.start()].strip()
        after = raw[match.end():].strip()
    else:
        # Fallback if no code block — assume entire output is SQL
        return raw

    # Wrap before/after content in /* ... */ block if present
    wrapped_comment = ""
    if before or after:
        wrapped_comment = "\n/*\n" + before + ("\n\n" if before and after else "") + after + "\n*/"

    return sql_code + wrapped_comment
