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
    remaining_steps: int
    
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
    
    # 답변 검증 관련
    answer_is_valid: bool
    answer_validation_reason: str
    
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

def get_recent_user_messages(messages: List, limit: int = 20) -> str:
    """지정된 개수(limit)만큼 최신 사용자 메시지를 합쳐 하나의 문자열로 반환합니다.

    LangGraph 상태의 messages 리스트에는 `HumanMessage`, `AIMessage` 객체와
    dict 형식 메시지가 섞여 있을 수 있습니다. 이 함수는 사람(human) 타입의
    메시지만 필터링한 뒤, 가장 최신 순서대로 최대 *limit*개까지 가져와
    상대적으로 오래된 순서(대화 흐름 유지)로 조인합니다.
    """
    # 사용자 메시지만 추출 (최신순)
    user_msgs: List[str] = []
    for msg in reversed(messages):
        # LangChain Message 객체의 경우
        if hasattr(msg, "type") and msg.type == "human":
            user_msgs.append(msg.content)
        # dict 로 저장된 경우
        elif isinstance(msg, dict) and msg.get("type") == "human":
            user_msgs.append(msg["content"])
        # limit 만족 시 중단
        if len(user_msgs) >= limit:
            break

    # 대화 흐름 보존을 위해 시간순(오래된 → 최신)으로 재정렬 후 합치기
    return "\n".join(reversed(user_msgs))
