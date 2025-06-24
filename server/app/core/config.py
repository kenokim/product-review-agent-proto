from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # API 설정
    api_title: str = "Product Recommendation Agent"
    api_version: str = "1.0.0"
    
    # LLM 설정
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # 그래프 설정
    max_search_queries: int = 3
    max_search_loops: int = 2
    
    # 모델 설정
    validation_model: str = "gemini-2.0-flash"
    search_model: str = "gemini-2.0-flash"
    analysis_model: str = "gemini-2.0-flash"
    
    # 데이터베이스 설정 (향후 확장용)
    database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 글로벌 설정 인스턴스
settings = Settings() 