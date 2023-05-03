import os
from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr


load_dotenv()


class BotAPISettings(BaseSettings):
    token_key: SecretStr = os.getenv('TOKEN_API', None)
