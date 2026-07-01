from openai import OpenAI
from app.core.config import settings

class LocalLLMClient:
    def __init__(self):
        self.client = OpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY)
        self.model_name = settings.LLM_MODEL_NAME

    def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()