from utils.prompt_manager import PromptManager
from core.base_ai_client import AIClient

class SQLStyleEnforcer:
    """
    A class to enforce SQL coding standards dynamically using AI-driven prompts.
    """

    def __init__(self, ai_client: AIClient, prompt_manager: PromptManager):
        """
        Initializes the SQLStyleEnforcer with AI client and prompt manager.
        """
        self.ai_client = ai_client
        self.prompt_manager = prompt_manager

    async def enforce_style(self, sql_code: str, dialect: str = "generic") -> str:
        """
        Enforces SQL style guide dynamically using AI.

        :param sql_code: The SQL code to analyze.
        :param dialect: The SQL dialect (e.g., "PostgreSQL", "T-SQL").
        :return: AI-enhanced SQL with enforced style guide.
        """
        # Load the appropriate prompt for SQL Style Guide Enforcement
        prompt = self.prompt_manager.get_prompt("style_enforcer.enforce_style")
        prompt = prompt.format(sql_code=sql_code, sql_dialect=dialect)

        # Send the prompt to the AI client
        response = await self.ai_client.generate(prompt)

        return response.strip()