import os
from dotenv import load_dotenv
from pydantic import SecretStr, StrictStr
from pydantic_settings import BaseSettings


load_dotenv()


class BotAPISettings(BaseSettings):
    token_key: SecretStr = os.getenv('TOKEN_API', None)
    api_key: SecretStr = os.getenv('API_KEY', None)
    api_host: SecretStr = os.getenv('API_HOST', None)
    api_host_weather: SecretStr = os.getenv('API_HOST_WEATHER', None)

