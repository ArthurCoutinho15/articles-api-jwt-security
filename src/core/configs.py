import os 
from dotenv import load_dotenv

from typing import ClassVar
from pydantic_settings import BaseSettings 
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = f"mysql+aiomysql://{str(os.getenv('USER'))}:{str(os.getenv('PASS'))}@localhost:3306/faculdade"
    DBBaseModel: ClassVar = declarative_base()
    
    JWT_SECRET: str = 'Lx-ZhdpXog0LQslkyHyPy6CzUB7YPrBXyRTQWufIubc'
    """
        import secrets 
        token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    
    # 60 minutos * 24 horas * 7 dias = 1 semana em minutos
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True
        
settings: Settings = Settings()