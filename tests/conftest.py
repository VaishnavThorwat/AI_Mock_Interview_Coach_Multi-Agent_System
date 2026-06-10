import os
import pytest
import litellm
from dotenv import load_dotenv
from deepeval.models.base_model import DeepEvalBaseLLM

load_dotenv()

class GeminiJudge(DeepEvalBaseLLM):
    """
    Wraps Gemini via LiteLLM so DeepEval can use it as a judge model.
    """

    MODEL = "gemini/gemini-3.5-flash"

    def load_model(self):
        return self.MODEL

    def generate(self, prompt: str) -> str:
        response = litellm.completion(
            model=self.MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        return response.choices[0].message.content

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self) -> str:
        return self.MODEL


@pytest.fixture(scope="session")
def judge():
    return GeminiJudge()