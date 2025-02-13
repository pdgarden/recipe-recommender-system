from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    llm_base_url: str = Field(
        description="Base URL of the LLM API. Used through OpenAI SDK.",
        default="http://localhost:11434/v1",
    )
    llm_api_key: str = Field(
        description="API key to connect to the LLM API. Used through OpenAI SDK.",
        default="ollama",
    )
    llm_model: str = Field(
        description="Name of LLM model used. Used through OpenAI SDK.",
        default="gemma2:2b",
    )


config = Config(_env_file=".env")
