##################################################################
# IMPORTANT
#
# OpenAI Sub-Quota Limits
    # - Some OpenAI deployments (e.g., Azure OpenAI) enforce sub-quotas for specific models, endpoints, or deployments.
    # - For instance, you might have a limit of 10,000 requests per minute globally but only 1,000 requests per minute for the specific model you're using (e.g., gpt-4).
    
# Solution:
    # - Check your Azure OpenAI dashboard for specific sub-quotas.
    # - Switch to a less popular model or endpoint if possible.
#
##################################################################


import sys
import os
import logging
import asyncio

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_ai_client import BaseAIClient
from utils.prompt_manager import PromptManager  # Assuming this manages prompts

# Logging setup
LOG_FILE = "learn_mode.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SQLLearnMode:
    """
    Interactive SQL Education Mode for guiding users through SQL concepts
    using quizzes, examples, practice sessions, and conversational guidance.
    """

    def __init__(self):
        # Initialize the AI client and prompt manager
        self.ai_client = BaseAIClient()  # Replace with actual key
        self.prompt_manager = PromptManager()
        self.conversation_history = []

    def log_event(self, message):
        """Log user interactions and system events."""
        logging.info(message)

    async def ask_agent(self, user_query, system_prompt="You are a T-SQL expert who provides detailed and accurate SQL guidance to users."):
        """
        Query the conversational agent with a dynamic system prompt and user input.
        """
        try:
            # Construct the full prompt
            full_prompt = f"{system_prompt}\n{user_query}"
            
            # Use the BaseAIClient to get a completion
            response = await self.ai_client.get_completion(full_prompt)
            
            # Log and return results
            self.log_event(f"User Query: {user_query}")
            self.log_event(f"Agent Response: {response}")
            
            return response.strip()
        except Exception as e:
            logging.error(f"Error during agent interaction: {e}")
            return "An error occurred while communicating with the agent. Please try again."

    async def dynamic_quiz(self):
        """
        Generate dynamic SQL quizzes using GPT.
        Continuously generates new, unique concept-based questions until the user types 'exit'.
        """
        print("\n📝 Starting Dynamic SQL Quiz...")
        asked_concepts = set()  # Maintain a set to track concepts already covered
    
        # Predefined fallback questions
        initial_fallback_questions = [
            {
                "question": "What does the SQL SELECT statement do?",
                "options": ["a) Inserts data", "b) Deletes data", "c) Retrieves data", "d) Updates data"],
                "answer": "c",
                "concept": "SELECT"
            },
            {
                "question": "Which SQL clause is used to filter records?",
                "options": ["a) WHERE", "b) GROUP BY", "c) HAVING", "d) ORDER BY"],
                "answer": "a",
                "concept": "WHERE"
            },
            {
                "question": "What is the purpose of the SQL JOIN clause?",
                "options": ["a) Combine rows from multiple tables", "b) Create a new table", "c) Filter data", "d) Update data"],
                "answer": "a",
                "concept": "JOIN"
            },
        ]
        fallback_questions = initial_fallback_questions.copy()

        while True:
            # Prompt the user for action or exit
            exit_prompt = input("\nType 'exit' to end the quiz or press Enter to continue: ").strip().lower()
            if exit_prompt == "exit":
                print("Exiting the quiz mode.")
                break

            quiz_prompt = (
                "Generate a random SQL quiz question with four multiple-choice options. "
                "The question must include a unique concept (e.g., SELECT, JOIN, GROUP BY, HAVING). "
                "Provide the answer and the concept being tested in the format:\n"
                "{'question': '...', 'options': ['a) ...', 'b) ...', 'c) ...', 'd) ...'], 'answer': 'a', 'concept': '...'}"
            )

            try:
                # Generate a new unique quiz question
                while True:
                    try:
                        # Attempt to generate a question using the OpenAI API
                        quiz_data = await self.ai_client.get_completion(quiz_prompt)
                        quiz = eval(quiz_data)  # Convert the response to a dictionary (ensure trusted input)
                    except Exception as e:
                        logging.error(f"Error generating question from OpenAI: {e}")
                        print("Error generating question from OpenAI. Using fallback.")

                        # Use fallback questions
                        if fallback_questions:
                            quiz = fallback_questions.pop(0)
                        else:
                            print("No more fallback questions available. Restarting fallback questions...")
                            fallback_questions = initial_fallback_questions.copy()
                            quiz = fallback_questions.pop(0)

                    # Check if the concept is unique
                    if quiz['concept'] not in asked_concepts:
                        asked_concepts.add(quiz['concept'])
                        break  # Exit the loop if the concept is unique

                # Display the question and options
                print(f"\n{quiz['question']}")
                for option in quiz['options']:
                    print(option)

                # Get and evaluate the user's answer
                user_answer = input("Your answer: ").strip().lower()
                if user_answer == quiz["answer"]:
                    print("✅ Correct!")
                    self.log_event(f"Correct answer for question: {quiz['question']} (Concept: {quiz['concept']})")
                else:
                    print(f"❌ Incorrect. The correct answer is {quiz['answer']}.")
                    self.log_event(f"Incorrect answer for question: {quiz['question']} (Concept: {quiz['concept']})")
            except Exception as e:
                logging.error(f"Error during quiz generation: {e}")
                print("An error occurred while generating the quiz. Please try again.")

    async def practice_sql(self):
        """
        Provide a code editor-like experience to practice SQL queries.
        """
        print("\n💻 Practice SQL Mode")
        print("Enter your SQL query below. Type 'exit' to quit.")
        while True:
            query = input("SQL> ").strip()
            if query.lower() == "exit":
                print("Exiting practice mode.")
                break
            feedback = await self.ask_agent(f"Evaluate this SQL query: {query}")
            print(f"Feedback: {feedback}")

    async def chat_with_agent(self):
        """
        Provide a conversational interface for SQL questions and guidance.
        """
        print("\n🤖 Chat with the SQL Agent")
        print("Ask any SQL-related question. Type 'exit' to quit.")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                print("Exiting chat mode.")
                break
            response = await self.ask_agent(user_input)
            print(f"Agent: {response}")

    async def run(self):
        """
        Main method to run the education mode.
        """
        print("\n🎓 Welcome to SQL Education Mode!")
        print("1. Take a dynamic quiz")
        print("2. Practice SQL")
        print("3. Chat with the SQL Agent")
        print("4. Exit")

        while True:
            choice = input("\nChoose an option (1-4): ").strip()
            if choice == "1":
                await self.dynamic_quiz()
            elif choice == "2":
                await self.practice_sql()
            elif choice == "3":
                await self.chat_with_agent()
            elif choice == "4":
                print("Thank you for using SQL Education Mode!")
                break
            else:
                print("Invalid choice. Please try again.")


def main():
    """
    Main entry point for testing/debugging.
    """
    education_mode = SQLLearnMode()
    asyncio.run(education_mode.run())


if __name__ == "__main__":
    main()