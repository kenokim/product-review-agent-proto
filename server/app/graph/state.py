import os
from typing import TypedDict, List, Annotated, Optional
from pydantic import BaseModel, Field
from langgraph.graph import add_messages
from langchain_core.runnables import RunnableConfig
import operator

# ========== 타입 정의 ==========

class Product(TypedDict):
    name: str
    source_url: str
    purchase_link: str
    review_summary: str
    price_range: str

class ProductRecommendationState(TypedDict):
    # 대화 기록 (LangGraph 표준)
    messages: Annotated[list, add_messages]
    
    # 사용자 요청 분석 결과
    is_request_specific: bool
    user_intent: str
    
    # 검색 관련 데이터
    search_queries: Annotated[list, operator.add]
    search_results: Annotated[list, operator.add]
    
    # 제품 데이터
    candidate_products: Annotated[list, operator.add]
    sources_gathered: Annotated[list, operator.add]  # 출처 추적
    
    # reflection 관련 상태
    is_sufficient: bool
    additional_queries: Annotated[list, operator.add]
    search_loop_count: int
    max_search_loops: int
    
    # 응답 데이터
    response_to_user: str
    
    # 설정값
    max_products: int
    search_depth: int



# ========== 설정 시스템 ==========

class ProductRecommendationConfig(BaseModel):
    # LLM 모델 설정
    validation_model: str = Field(default="gemini-2.5-flash", description="요청 검증용 모델")
    search_model: str = Field(default="gemini-2.5-flash", description="검색어 생성용 모델")
    analysis_model: str = Field(default="gemini-2.5-flash", description="제품 분석용 모델")
    
    # 검색 설정
    max_search_queries: int = Field(default=3, description="최대 검색어 수")
    max_products_per_query: int = Field(default=5, description="검색어당 최대 제품 수")
    max_candidate_products: int = Field(default=10, description="최대 후보 제품 수")
    
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

# ========== 유틸리티 함수 ==========

def get_latest_user_message(messages: List) -> str:
    """최신 사용자 메시지 추출"""
    for message in reversed(messages):
        if hasattr(message, 'type') and message.type == 'human':
            return message.content
        elif isinstance(message, dict) and message.get('type') == 'human':
            return message['content']
    return ""
