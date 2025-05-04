
from abc import ABC, abstractmethod

class SQLTask(ABC):
    """
    Abstract base class for all GenAI SQL tools.
    """

    @abstractmethod
    async def run(self, sql_query: str) -> str:
        """
        Executes the task on the given SQL query.
        """
        pass
