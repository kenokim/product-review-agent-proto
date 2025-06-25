import os
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig

# ========== 설정 시스템 ==========

class ProductRecommendationConfig(BaseModel):
    # LLM 모델 설정
    validation_model: str = Field(default="gemini-2.0-flash", description="요청 검증용 모델")
    search_model: str = Field(default="gemini-2.0-flash", description="검색어 생성용 모델")
    analysis_model: str = Field(default="gemini-2.0-flash", description="제품 분석용 모델")
    
    # 검색 설정
    max_search_queries: int = Field(default=4, description="최대 검색어 수 (4개 요청)")
    required_search_results: int = Field(default=3, description="필요한 최소 검색 결과 수 (빠른 3개 사용)")
    max_products_per_query: int = Field(default=5, description="검색어당 최대 제품 수")
    max_candidate_products: int = Field(default=10, description="최대 후보 제품 수")
    search_timeout: int = Field(default=25, description="개별 검색 타임아웃 (초)")
    
    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "ProductRecommendationConfig":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        
        # Get raw values from environment or config
        raw_values = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }
        
        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}
        
        return cls(**values)
