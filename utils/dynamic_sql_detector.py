import re
from typing import List, Dict, Tuple
from utils.prompt_manager import PromptManager
from core.base_ai_client import AIClient


class DynamicSQLDetector:
    """
    A utility for detecting and analyzing dynamically generated SQL queries.
    This includes identifying risks such as SQL injection vulnerabilities and
    providing optimization suggestions.
    """

    def __init__(self, ai_client: AIClient, prompt_manager: PromptManager):
        """
        Initializes the DynamicSQLDetector.

        :param ai_client: An instance of the AIClient for LLM interactions.
        :param prompt_manager: An instance of the PromptManager for loading prompts.
        """
        self.ai_client = ai_client
        self.prompt_manager = prompt_manager

    async def detect_dynamic_sql(self, sql_code: str) -> Dict[str, str]:
        """
        Detects dynamic SQL patterns in the given SQL code.

        :param sql_code: The SQL code to analyze.
        :return: A dictionary with detected patterns and their descriptions.
        """
        # Load the appropriate prompt for detecting dynamic SQL
        prompt = self.prompt_manager.load_prompt("dynamic_sql.detector", sql_code=sql_code)
        
        # Interact with the AI model to identify dynamic SQL patterns
        response = await self.ai_client.generate(prompt)
        return {"dynamic_sql_analysis": response.strip()}

    async def analyze_risks_and_optimization(self, sql_code: str) -> str:
        """
        Analyzes the dynamically generated SQL for risks and optimization opportunities.

        :param sql_code: The SQL code to analyze.
        :return: A report detailing risks and optimization suggestions.
        """
        # Load the prompt for analyzing risks and optimizations
        prompt = self.prompt_manager.load_prompt("dynamic_sql.risks_and_optimization", sql_code=sql_code)
        
        # Interact with the AI model to analyze risks and optimizations
        response = await self.ai_client.generate(prompt)
        return response.strip()


# Example usage
if __name__ == "__main__":
    import asyncio

    # Initialize AI client and prompt manager
    ai_client = AIClient()
    prompt_manager = PromptManager("prompts/index.yaml")

    detector = DynamicSQLDetector(ai_client, prompt_manager)

    # Example dynamic SQL code
    sql_code = """
    DECLARE @sql NVARCHAR(MAX);
    SET @sql = 'SELECT * FROM ' + @tableName + ' WHERE UserID = ' + @userID;
    EXEC sp_executesql @sql;
    """

    async def run():
        # Detect dynamic SQL
        detection_result = await detector.detect_dynamic_sql(sql_code)
        print("\nDynamic SQL Detection Result:")
        print(detection_result)

        # Analyze risks and optimizations
        analysis_result = await detector.analyze_risks_and_optimization(sql_code)
        print("\nRisk and Optimization Analysis:")
        print(analysis_result)

    asyncio.run(run())
