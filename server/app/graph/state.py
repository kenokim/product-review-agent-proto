from typing import TypedDict, List, Annotated
from langgraph.graph import add_messages
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
    
    # 검색 관련 데이터 (quickstart 패턴 참고)
    search_queries: Annotated[list, operator.add]
    search_results: Annotated[list, operator.add]
    web_research_result: Annotated[list, operator.add]  # 병렬 웹 검색 결과 병합
    
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

# ========== 유틸리티 함수 ==========

def get_latest_user_message(messages: List) -> str:
    """최신 사용자 메시지 추출"""
    for message in reversed(messages):
        if hasattr(message, 'type') and message.type == 'human':
            return message.content
        elif isinstance(message, dict) and message.get('type') == 'human':
            return message['content']
    return ""
