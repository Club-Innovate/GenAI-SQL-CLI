import os
import yaml

PROMPT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../prompts"))
INDEX_PATH = os.path.join(PROMPT_ROOT, "index.yaml")

# PROMPT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../prompts"))
# INDEX_PATH = os.path.join(PROMPT_ROOT, "index.yaml")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    PROMPT_INDEX = yaml.safe_load(f)


class PromptManager:
    @staticmethod
    def load_prompt(key: str, **kwargs) -> str:
        entry = PROMPT_INDEX.get(key)
        if not entry:
            raise ValueError(f"Prompt key '{key}' not found in index.yaml")

        if "inline" in entry:
            template = entry["inline"]
        elif "file" in entry:
            file_path = os.path.join(PROMPT_ROOT, entry["file"])
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"Prompt file not found at: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                template = f.read()
        else:
            raise ValueError(f"No prompt source ('inline' or 'file') for key: {key}")

        # Validate inputs
        expected_inputs = set(entry.get("inputs", []))
        missing = expected_inputs - set(kwargs.keys())
        if missing:
            raise KeyError(f"Missing prompt inputs: {missing} for prompt '{key}'")

        return template.format(**kwargs)

    @staticmethod
    def list_prompts():
        return list(PROMPT_INDEX.keys())

    @staticmethod
    def get_metadata(key: str):
        return PROMPT_INDEX.get(key, {})

