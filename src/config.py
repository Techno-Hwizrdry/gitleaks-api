import os
from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

dir_path = os.path.dirname(os.path.realpath(__file__))
full_path = os.path.join(dir_path, 'gitleaks_api.env')

class Settings(BaseSettings):
    app_name: str = "GitLeaks API"
    admin_email: EmailStr = Field(default=None, env="ADMIN_EMAIL")
    gitleaks_path: str = Field(default=None, env="GITLEAKS_PATH")
    model_config = SettingsConfigDict(env_file=full_path)