
import getpass

class Config:
    """
    Configuration loader that is suitable for consistent use across tools in the modular architecture.
    
    """

    # User
    USER = getpass.getuser()

    # Azure OpenAI Key
    AOPAI_KEY= 'your azure openai key'

    # Azure OpenAI API Endpoint
    API_BASE= 'https://your-resource-name.openai.azure.com/'

    # Azure OpenAI API Version
    AOPAI_API_VERSION = 'Example: 2025-01-01-preview' # <--- change this to the name of your API Version

    AOPAI_DEPLOY_MODEL = 'Example: gpt-4o' # <--- change this to the name of your model deployment

    # SQL Script Directory
    SQL_DIR = r'your/directory/'

    @staticmethod
    def load():
        return {
            "USER": Config.USER,
            "AOPAI_KEY": Config.AOPAI_KEY,
            "API_BASE": Config.API_BASE,
            "AOPAI_API_VERSION": Config.AOPAI_API_VERSION,
            "AOPAI_DEPLOY_MODEL": Config.AOPAI_DEPLOY_MODEL,
            "SQL_DIR": Config.SQL_DIR,
        }
