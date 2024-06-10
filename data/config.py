from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    bot_token: SecretStr
    admin_id: int
    USER_ID: int
    allowed_chat_ids: str
    folder_id: SecretStr
    email_admin: str
    email_user: str
    proxy: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config_settings = Settings()
