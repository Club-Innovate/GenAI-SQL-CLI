
import httpx
import asyncio
import logging
from core.config_loader import Config

class BaseAIClient:
    """
    Asynchronous Azure OpenAI client for executing LLM calls.
    """

    def __init__(self):
        self.config = Config.load()
        self.headers = {
            "api-key": self.config["AOPAI_KEY"],
            "Content-Type": "application/json"
        }
        self.endpoint = f"{self.config['API_BASE']}openai/deployments/{self.config['AOPAI_DEPLOY_MODEL']}/chat/completions?api-version={self.config['AOPAI_API_VERSION']}"

    async def get_completion(self, prompt: str, temperature: float = 0.3) -> str:
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.endpoint, json=payload, headers=self.headers)
                response.raise_for_status()

                return response.json()["choices"][0]["message"]["content"]

            except Exception as e:
                logging.exception("LLM API call failed")
                raise RuntimeError(f"OpenAI request failed: {e}")
