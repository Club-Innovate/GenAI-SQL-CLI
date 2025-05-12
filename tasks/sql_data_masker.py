from utils.prompt_manager import PromptManager
from core.base_ai_client import AIClient

class SQLDataMasker:
    """
    A class for masking sensitive data in SQL queries using AI-driven prompts.
    """

    def __init__(self, ai_client: AIClient, prompt_manager: PromptManager):
        """
        Initializes the SQLDataMasker with AI client and prompt manager.
        """
        self.ai_client = ai_client
        self.prompt_manager = prompt_manager

    async def mask_sensitive_data(self, sql_query: str) -> str:
        """
        Masks sensitive data in the given SQL query using AI.

        :param sql_query: The SQL query string to be masked.
        :return: The SQL query with sensitive data masked.
        """
        # Load the appropriate prompt for masking sensitive data
        prompt = self.prompt_manager.load_prompt("data_masker.mask_sensitive_data", sql_query=sql_query)

        # Send the prompt to the AI client
        response = await self.ai_client.generate(prompt)

        return response.strip()

    async def detect_sensitive_data(self, sql_query: str) -> str:
        """
        Detects sensitive data in the given SQL query using AI.

        :param sql_query: The SQL query string to be analyzed.
        :return: A description of detected sensitive data.
        """
        # Load the appropriate prompt for detecting sensitive data
        prompt = self.prompt_manager.load_prompt("data_masker.detect_sensitive_data", sql_query=sql_query)

        # Send the prompt to the AI client
        response = await self.ai_client.generate(prompt)

        return response.strip()


# Example usage
if __name__ == "__main__":
    import asyncio
    ai_client = AIClient()
    prompt_manager = PromptManager("prompts/index.yaml")

    masker = SQLDataMasker(ai_client, prompt_manager)

    sample_query = """
        SELECT * FROM users
        WHERE email = 'user@example.com'
        AND phone = '+1-800-555-1234'
        AND credit_card = '4111 1111 1111 1111'
        AND ssn = '123-45-6789';
    """

    print("Original Query:")
    print(sample_query)

    async def run():
        masked_query = await masker.mask_sensitive_data(sample_query)
        print("\nMasked Query:")
        print(masked_query)

        detected_data = await masker.detect_sensitive_data(sample_query)
        print("\nDetected Sensitive Data:")
        print(detected_data)

    asyncio.run(run())