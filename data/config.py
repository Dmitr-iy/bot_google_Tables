from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    bot_token: SecretStr
    db_user: str
    db_password: SecretStr
    db_name: str
    db_host: str
    db_port: str
    admin_id: int
    allowed_chat_ids: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config_settings = Settings()
