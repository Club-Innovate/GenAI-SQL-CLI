import unittest
import asyncio
from tasks.sql_style_enforcer import SQLStyleEnforcer
from utils.prompt_manager import PromptManager
from core.base_ai_client import MockAIClient  # Mock AI Client for testing

class TestSQLStyleEnforcer(unittest.TestCase):
    def setUp(self):
        self.prompt_manager = PromptManager("prompts/index.yaml")
        self.ai_client = MockAIClient()  # Use a mock AI client to simulate responses
        self.enforcer = SQLStyleEnforcer(self.ai_client, self.prompt_manager)

    def test_enforce_style(self):
        sample_query = """
        select * from UsersTable
        where UserName = 'JohnDoe'
        """
        expected_response = """
        SELECT *
        FROM users_table
        WHERE user_name = 'JohnDoe'
        """

        # Mock AI response
        self.ai_client.set_mock_response(expected_response)

        # Run the style enforcer
        result = asyncio.run(self.enforcer.enforce_style(sample_query, dialect="PostgreSQL"))

        # Assert the result matches the expected response
        self.assertEqual(result.strip(), expected_response.strip())

if __name__ == "__main__":
    unittest.main()
